# -*- coding: utf-8 -*-
r"""13本目 ⑤a：**音声だけの試聴**（再発防止策7）の mp3 と目次を作る（2026-09-24・API 不使用・0クレジット）。

  python qa_out/ep13_listen.py [--tag t130]
      → out/ep13_listen/ep13_listen_<tag>.mp3（80kbps・モノラル・30MB 以下）
        out/ep13_listen/ep13_listen_<tag>_index.md（聞き所の一覧＋全行の目次。秒は mp3 の秒）

積み方（本編の映像と同じ間＝あとで本編の時刻とほぼそろう）:
  章の頭 2.0秒（12本目からの扉。c2〜c9 の頭と ed01）＋ カットの前 LEAD 0.35秒 ＋ カットの音（audio/<cid>.wav）
  ＋ カットの後 TAIL 0.50秒 ＋ 決め所（★）のカットのあと 2.0秒
⚠️ 本編の尺は ⑤b の設計（扉・絵の長さ）で変わる＝目次の秒は「試聴の mp3 の秒」。
⚠️ 音は `audio/<cid>.wav`（el_build が組んだ出荷する音＝TEMPO・句点の間・フェードを通したあと）を読む。

聞き所（機械では読みを確かめられない型。Vault「事故検証-読みの再発防止策-20260924」§1〜§2 の型から）:
  かな長 … 数を長いひらがなで送った行（12本目の試写で抑揚が崩れた型）／空白 … 辞書が半角空白を入れた行（間になる型）
  はち   … ひらがなの数に「は」が入る行（「は」が助詞の「わ」に読まれる型＝12本目の降灰）
  漢数字 … 漢数字で送った行（聞取は読みを字に戻すので、ふん／ぷん・なな／しち を確かめられない）
  行頭かな … 行の頭をかな・カタカナにした行（行頭は崩れやすい）
  読み2通り … 同じ字で読みが2つある語（床＝ゆか／とこ・側＝がわ／そば・縁＝ふち／えん・点け・梢）
  前の回で崩れた語 … 旅客機（12本目「別の語に聞こえる」）・北東（12本目の東北東が『とうほくひがし』）
  ★ … 決め所（画面に大きく出る引用）／問い … c920 コメントの問い／異音 … 合成の門番が「要耳」とした行
"""
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "qa_out"))
import el_script as ES          # noqa: E402
import narration                # noqa: E402
import ep13_script_copy as SC   # noqa: E402  章の見出し（台本 md から）

SR = 24000
LEAD, TAIL, QUOTE_EXTRA, CARD = 0.35, 0.50, 2.0, 2.0
OUT = ROOT / "out" / "ep13_listen"
TAG = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else "t130"

HIRA_RUN = re.compile(r"[ぁ-ゖー]{12,}")
KANJI_NUM = re.compile(r"[一二三四五六七八九十百千]")
TWO_READ = re.compile(r"床|胴体の側|縁|点け|梢")
DANGER = re.compile(r"旅客機|北東")


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


def tags_of(lid, cid, text, quotes, retake):
    hits = []
    sent = ES.el_text(text, hits)
    t = []
    new_runs = [r for r in HIRA_RUN.findall(sent) if r not in text]
    if new_runs:
        t.append("かな長")
    if any(" " in v for _, v, _ in hits):
        t.append("空白")
    if any("は" in v and re.fullmatch(r"[ぁ-ゖー\s]+", v.split("（")[0].replace("キロ", "").replace("メートル", ""))
           for _, v, _ in hits):
        t.append("はち")
    if any(KANJI_NUM.search(v) for _, v, _ in hits):
        t.append("漢数字")
    if sent and sent[0] != text[0] and re.match(r"[ぁ-ゖァ-ヺ]", sent[0]):
        t.append("行頭かな")
    if TWO_READ.search(text):
        t.append("読み2通り")
    if DANGER.search(text):
        t.append("前の回で崩れた語")
    if cid in quotes:
        t.append("★")
    if cid == "c920":
        t.append("問い")
    if retake.get(lid) in ("unsure", "real"):
        t.append("異音")
    return t


def main():
    nj = json.loads((ROOT / "audio" / "narration.json").read_text(encoding="utf-8"))
    subs = nj["subtitles"]
    quotes = ES.quote_cuts()
    _, heads, _ = SC.from_md()
    retake = {}
    rt = ROOT / "audio" / "el_qa" / f"{ES.SLUG}_el_retakes.tsv"
    if rt.exists():
        for ln in rt.read_text(encoding="utf-8").splitlines()[1:]:
            c = ln.split("\t")
            if len(c) >= 2:
                retake[c[0]] = c[1]
    # 🔴 台本と narration.json が1行ずつ同じか（違えば古い音＝止める）
    bad = []
    for cid, ls in narration.SCRIPT:
        rows = subs.get(cid)
        if rows is None or [r["text"] for r in rows] != [x.strip() for x in ls]:
            bad.append(cid)
    if bad:
        raise SystemExit(f"🔴 narration.json と台本が食い違う（el_build を回し直す）: {bad[:8]}")

    pcm, t, index, cur_head = bytearray(), 0.0, [], None
    sil = lambda s: b"\x00\x00" * int(round(s * SR))  # noqa: E731
    first = True
    for cid, ls in narration.SCRIPT:
        ch = cid[:2] if cid.startswith("c") else cid
        if ch != cur_head:
            if not first:
                pcm += sil(CARD)
                t += CARD
            cur_head, first = ch, False
            index.append(("head", heads.get(cid, "共通エンディング" if cid == "ed01" else cid), t))
        with wave.open(str(ROOT / "audio" / f"{cid}.wav"), "rb") as w:
            assert w.getframerate() == SR and w.getnchannels() == 1 and w.getsampwidth() == 2, cid
            body = w.readframes(w.getnframes())
        pcm += sil(LEAD)
        t0 = t + LEAD
        for i, r in enumerate(subs[cid], 1):
            lid = f"{cid}-{i}"
            index.append(("line", lid, t0 + r["t"], r["text"], tags_of(lid, cid, r["text"], quotes, retake)))
        pcm += body
        t = t0 + len(body) / 2 / SR + TAIL
        pcm += sil(TAIL)
        if cid in quotes:
            pcm += sil(QUOTE_EXTRA)
            t += QUOTE_EXTRA

    OUT.mkdir(parents=True, exist_ok=True)
    mp3 = OUT / f"ep13_listen_{TAG}.mp3"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "s16le", "-ar", str(SR),
                        "-ac", "1", "-i", "-", "-c:a", "libmp3lame", "-b:a", "80k", str(mp3)],
                       input=bytes(pcm), capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"🔴 ffmpeg が失敗: {r.stderr.decode('utf-8', 'replace')[-400:]}")
    mb = mp3.stat().st_size / 1e6
    if mb > 30:
        raise SystemExit(f"🔴 mp3 が {mb:.1f}MB＝30MB を超える（ビットレートを下げる）")

    # ── 目次 ──
    lines = [x for x in index if x[0] == "line"]
    order = ["かな長", "空白", "はち", "漢数字", "行頭かな", "読み2通り", "前の回で崩れた語", "★", "問い", "異音"]
    md = [f"# 13本目 トルコ航空981便 ── 音声だけの試聴（{TAG}・{mmss(t)}・{mb:.1f}MB）", "",
          f"mp3＝`{mp3.name}`。声＝{nj.get('voice_name')}・TEMPO {nj.get('tempo')}・{len(narration.SCRIPT)}カット／{len(lines)}行。",
          "おかしい所は **mp3 の時刻（分:秒）** か **行の頭の数語** で教えてください（下の目次で行に引けます）。",
          "間の取り方＝カットの前 0.35秒・後 0.50秒・決め所のあと 2.0秒・章の頭 2.0秒（本編の映像と同じ）。", "",
          "## 聞き所（機械では読みを確かめられない型）", ""]
    for tg in order:
        hit = [x for x in lines if tg in x[4]]
        if not hit:
            continue
        md.append(f"### {tg}（{len(hit)}行）")
        for _, lid, a, txt, _ in hit:
            md.append(f"- {mmss(a)}　{lid}　{txt}")
        md.append("")
    md += ["## 全行の目次", ""]
    for x in index:
        if x[0] == "head":
            md.append(f"### {mmss(x[2])}　{x[1]}")
        else:
            _, lid, a, txt, tg = x
            md.append(f"- {mmss(a)}　{lid}　{txt}" + (f"　〔{'・'.join(tg)}〕" if tg else ""))
    idx = OUT / f"ep13_listen_{TAG}_index.md"
    idx.write_text("\n".join(md) + "\n", encoding="utf-8")
    cnt = {tg: sum(1 for x in lines if tg in x[4]) for tg in order}
    print(f"mp3 {mp3}（{mmss(t)}・{mb:.1f}MB）")
    print(f"目次 {idx}（{len(lines)}行）")
    print("聞き所 " + "・".join(f"{k}{v}" for k, v in cnt.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
