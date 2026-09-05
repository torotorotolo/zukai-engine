# -*- coding: utf-8 -*-
r"""el_check_yomi.py — 合成した音を文字起こしして、台本と突き合わせる。

  python tools/el_check_yomi.py                      … 全行を検査（題材は el_script.SLUG）
  python tools/el_check_yomi.py --ids c112,c116-1    … その行だけ検査して tsv に差し込む（他の行の記録は残す）
  python tools/el_check_yomi.py --worst 25           … 一致率の低い順に25行だけ出す
  （事故検証ch 2026-09-05：行ID＝カットID-行番号。台本は narration.SCRIPT。出力は audio/el_qa/<slug>_el_yomi.tsv）

🔴🔴 これは**門番ではありません。当たりを付ける道具です。**
    ElevenLabs には「どう読んだか」を返す口が無いので、AivisSpeech でやっていた
    「moras から読みを取って機械照合する」層は作れません。代わりに
    **合成音 → 文字起こし（Scribe）→ 台本と比較** という遠回りをします。

    ⚠️ 文字起こし自体が誤ります（2026-08-26 実測）:
        「回りました」→「くぐりました」／「2位は」→「セディは」
    ⚠️ 数字の表記が食い違います:
        送信「1分23秒998」→ 聞取「一分二十三秒九九八」
    したがって **一致率が低い＝誤読、ではありません。**
    この道具の役目は「**聞くべき行を絞る**」ことです。合否はカズヤくんの耳が決めます。

出力: 台本/<slug>_el_yomi.tsv（場面ID / 送った文 / 聞こえた文 / 一致率）
"""
import difflib
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
import uuid
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_tts  # noqa: E402
import el_script as ES  # noqa: E402  行の列挙・EL_YOMI・キャッシュの場所（事故検証chは config/<slug>.json でなく narration.SCRIPT）
# ⚠️ 2026-08-26: 合成側は EL_YOMI を当てた文で焼くので、キャッシュの鍵も置換後の文で作られます。
#    ここで生の台本から鍵を作ると、**読みを直した行だけが「キャッシュが無い」ことになって
#    検査から漏れます**（実際に s018/s019/s061/s137/s142 の5行が漏れました）。
#    ＝直した行こそ検査したい行なので、これは致命的。必ず同じ置換を通すこと。
# 🔴 本番と同じ関数を呼ぶこと。自前で replace を並べ直すと、境界判定の違いで
#    「本番はこう送ったのに検査は別の文で鍵を作る」というズレが生まれます。
apply_yomi = ES.el_text

KANJI_NUM = str.maketrans("〇一二三四五六七八九", "0123456789")


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def norm(s: str) -> str:
    """比べるための正規化。⚠️ ここを凝りすぎると本物の誤読まで吸収してしまう。
    やるのは『表記のゆれ』だけ: 全角半角・記号・空白・漢数字の桁表現。"""
    s = unicodedata.normalize("NFKC", s)
    s = s.translate(KANJI_NUM)
    s = re.sub(r"[十百千万]", "", s)          # 「二十三」→「23」に寄せる（粗いが両側に等しく効く）
    s = re.sub(r"[、。「」『』・！？…,.!?\"'\s]", "", s)
    return s


def stt(pcm: bytes) -> str:
    """生PCMを wav にくるんで Scribe に投げる。"""
    import struct
    n = len(pcm)
    hdr = struct.pack("<4sI4s4sIHHIIHH4sI", b"RIFF", 36 + n, b"WAVE", b"fmt ",
                      16, 1, 1, el_tts.SR, el_tts.SR * 2, 2, 16, b"data", n)
    wav = hdr + pcm
    bd = "----" + uuid.uuid4().hex

    def part(k, v):
        return (f'--{bd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n').encode()

    body = part("model_id", "scribe_v1") + part("language_code", "jpn")
    body += (f'--{bd}\r\nContent-Disposition: form-data; name="file"; filename="a.wav"\r\n'
             f'Content-Type: audio/wav\r\n\r\n').encode() + wav + b"\r\n"
    body += f"--{bd}--\r\n".encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text",
                                 data=body, method="POST",
                                 headers={"xi-api-key": el_tts.key(),
                                          "Content-Type": "multipart/form-data; boundary=" + bd})
    with urllib.request.urlopen(req, timeout=300) as res:
        return json.load(res).get("text", "")


def load_tsv(path):
    """既存の tsv を {行ID: (台本, 聞取, 一致率, 送信文)} で返す（無ければ空）。"""
    out = {}
    if not path.exists():
        return out
    for l in path.read_text(encoding="utf-8").splitlines()[1:]:
        f = l.split("\t")
        if len(f) >= 4:
            out[f[0]] = (f[2], f[3], float(f[1]), f[4] if len(f) > 4 else "")
    return out


def main():
    # 引数は --ids だけ（題材は el_script.SLUG）。--ids を付けると**その行だけ検査して tsv に差し込む**
    # （他の行の記録は残す＝直した行だけかけ直しても台帳が歯抜けにならない）。
    ids = None
    if "--ids" in sys.argv:
        ids = set(ES.resolve_ids(arg("--ids", "")))
    worst = int(arg("--worst", "0"))
    out = ES.qa_path("el_yomi.tsv")
    prev = load_tsv(out) if ids else {}
    c0, lim = el_tts.credits_used()      # Scribe の消費を実測する（見込みに入れる）
    sec_total = 0.0

    rows, missing, failed = [], [], []
    for ln in ES.lines():
        if ids and ln.lid not in ids:
            continue
        text = ln.text
        sent = apply_yomi(text)          # 実際にエンジンへ送った文
        cache = ES.cache_path(sent)
        if not cache.exists():
            missing.append(ln.lid)       # fail closed: 合成していない行を「合格」にしない
            continue
        try:
            pcm = cache.read_bytes()
            sec_total += len(pcm) / 2 / el_tts.SR
            heard = stt(pcm)
        except urllib.error.HTTPError as e:
            failed.append((ln.lid, f"HTTP {e.code}"))
            continue
        except Exception as e:
            failed.append((ln.lid, f"{type(e).__name__}"))
            continue
        r = difflib.SequenceMatcher(None, norm(text), norm(heard)).ratio()
        rows.append((ln.lid, text, heard, r, sent))
        print(f"  {ln.lid} {r*100:5.1f}%  {heard[:56]}", flush=True)

    # tsv は SCRIPT の順。--ids のときは前回の記録に差し込む
    merged = dict(prev)
    for i, t, h, r, s in rows:
        merged[i] = (t, h, r, s)
    order = [ln.lid for ln in ES.lines()]
    out.write_text("場面\t一致率\t送った文\t聞こえた文\t送信文\n" +
                   "\n".join(f"{i}\t{merged[i][2]:.3f}\t{merged[i][0]}\t{merged[i][1]}\t{merged[i][3]}"
                             for i in order if i in merged) + "\n",
                   encoding="utf-8")
    rows = [(i, t, h, r) for i, t, h, r, _ in rows]
    rows.sort(key=lambda x: x[3])
    n = worst or len(rows)
    print(f"\n=== 一致率の低い順 {min(n, len(rows))}行（★耳で確かめる候補）===")
    for i, t, h, r in rows[:n]:
        print(f"\n{i}  一致率 {r*100:.1f}%")
        print(f"   台本: {t}")
        s2 = apply_yomi(t)
        if s2 != t:
            print(f"   送信: {s2}   ← EL_YOMI で書き換えた文")
        print(f"   聞取: {h}")

    print(f"\n検査 {len(rows)}行 -> {out}（記録 {len(merged)}行／台本 {len(order)}行）")
    c1, _ = el_tts.credits_used()
    print(f"Scribe: 音声 {sec_total:.1f}秒を文字起こし／クレジット {c0:,} → {c1:,}（消費 {c1-c0:,}／上限 {lim:,}）"
          f" ⚠️ 反映が遅れることがある")
    if missing:
        print(f"⚠️ 合成キャッシュが無くて検査できなかった行 {len(missing)}件: {','.join(missing[:12])}"
              f"{'…' if len(missing) > 12 else ''}")
    if failed:
        print(f"⚠️ 文字起こしに失敗した行 {len(failed)}件: {failed[:8]}")
    if missing or failed:
        print("🔴 未検査の行があります。『全部OK』とは言えません。")
        sys.exit(1)


if __name__ == "__main__":
    main()
