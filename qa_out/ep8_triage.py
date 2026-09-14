# -*- coding: utf-8 -*-
r"""ep8_triage.py — 「読みが違う」行を **①文頭の崩れ ②語の読み ③字の当て違い** に機械で仕分ける（8本目・この回かぎり）。

■ なぜ要るか（7本目 `qa_out/ep7_triage.py` と同じ思想。**この回の定数で作り直した**）
    直し方が型ごとに違う（[[reference-elevenlabs-tts]]）:
      ① **文頭の崩れ** … 書き方では直らない。`el_retake`（頭に「　、」を足して振り直す）
      ② **語の読み**   … 行の途中でも崩れる＝本文が誘発。`EL_YOMI` に入れて A/B（`el_ab_yomi`）
      ③ **Scribe の字の当て違い** … 読みは同じ。**直さない**（交信→更新／責める→攻める）
    仕分けずに全部 retake すると、1行4テイクぶんを丸ごと捨てる。

■ 仕分けの規則（機械）
    - 台本の**先頭2字**が聞取の**先頭6字**のどこにも無い → ①文頭の崩れ
    - `SAME_READING` に人が理由つきで入れた行 → ③（直さない）
    - どちらでもない → ②（A/B の候補）
    ⚠️ 陽性・陰性対照は `--selftest`。**この回の実データで対照を差し替えてから使うこと**
       （7本目の対照は 9.11 の行IDなので、そのまま持ってくると黙って通る）。
    🔴 **①には既知の偽陽性がある**＝頭の表記が漢字→かなに替わっただけでも落ちる
       （「軍の」→聞取「ぐんの」＝読みは同じ）。**①は retake に回す前に実文を目で見る。**
       だから run() は行IDだけでなく**台本と聞取の実文を並べて**書き出す。

  python qa_out/ep8_triage.py            … 仕分けて3つのファイルへ
  python qa_out/ep8_triage.py --selftest … 対照（ファイルを読まない）
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

Q = ROOT / "audio" / "el_qa"
SLUG = "ep8"
FRONT_LOOK = 6

# ③ 読みが同じで字だけ違うと**人が確かめた**もの（1件ずつ理由つき。ここに入れたら直さない）。
#    🔴 空から始める。実データを1行ずつ見て、理由を書いてから足す。
SAME_READING = {
}


# 🔴🔴 **字ではなく「読み」で見る**（2026-09-14・実測で決めた）。
#    字で見ると Scribe の書き戻しが全部①に化ける:
#      「2日あまり回り」→「二日余り回り」（漢数字＋かな→漢字）／「いちばん」→「一番」
#    ＝ 122件のうち 42件が①に入り、そのほとんどが表記のゆれだった。
#    `el_reading_diff.tsv` は **janome で読みに直した列**（台本の読み／聞取の読み）を持っているので、
#    そちらの先頭を見る。表記のゆれはここで消える（読みは同じ）。
#    → [[feedback-verify-your-own-instrument]]（全部NGなら物差しを疑う）
FRONT_MORA = 3          # 読みの先頭3モーラ（カタカナ3字）
FRONT_LOOK = 8          # 聞取の読みの先頭8字のどこかにあれば「頭は残っている」


def front_broken(script_yomi, heard_yomi):
    """台本の読みの先頭 FRONT_MORA 字が、聞取の読みの先頭 FRONT_LOOK 字のどこにも無い。"""
    t, h = (script_yomi or "").strip(), (heard_yomi or "").strip()
    if len(t) < FRONT_MORA:
        return False          # 短すぎて①では判定できない → ②へ回す
    return t[:FRONT_MORA] not in h[:FRONT_LOOK]


def selftest():
    fails = []
    ok = lambda c, n: (None if c else fails.append(n))
    # 陽性対照＝頭が丸ごと落ちた形（7本目 c110-1「点は、ペンタゴンの」→「はペンタゴンの」）
    ok(front_broken("テンワペンタゴンノ", "ワペンタゴンノニシエ"), "頭が落ちていれば①")
    ok(front_broken("ツバサオササエルケタノ", "アアアアアアアアツバサオササエルケタノ"),
       "頭が9字目まで押し出されたら①（窓の外）")
    # 陰性対照＝先頭が残っている
    ok(front_broken("チャクリクノヨテエワ", "チャクリクノヨテエワゲンチジカンノ") is False, "そのままなら①ではない")
    # 🔴 字なら①に化けた型が、読みなら消えること（2026-09-14 で実際に化けた3つ）
    ok(front_broken("ニチアマリマワリ", "ニチアマリマワリ") is False,
       "『2日あまり』→『二日余り』は読みが同じ＝①ではない")
    ok(front_broken("トオリノケエロノウチ", "トオリノケエロノウチ") is False,
       "『15通り』→『十も通り』は数の壊れ＝①ではない（numbers_heard が拾う）")
    ok(front_broken("グンノシキケエトオワ", "グンノシキケエトオワ") is False,
       "『軍の』→『ぐんの』は読みが同じ＝①ではない")
    # 短すぎる行は①では決めない
    ok(front_broken("ア", "ゼンゼンチガウ") is False, "3モーラ未満は①にしない（②へ回す）")
    if fails:
        print(f"selftest: 落ちた: {fails}")
        return 1
    print(f"selftest: 7/7 合格（FRONT_MORA={FRONT_MORA}／FRONT_LOOK={FRONT_LOOK}・ファイルを読んでいない）")
    return 0


def run():
    import el_script as ES
    dpath, hpath = Q / f"{SLUG}_reading_diff.tsv", Q / f"{SLUG}_el_yomi.tsv"
    for p in (dpath, hpath):
        if not p.exists():
            raise SystemExit(f"🔴 まだ無い: {p}（先に el_check_yomi → el_reading_diff）")
    rows = list(csv.DictReader(dpath.read_text(encoding="utf-8").splitlines(), delimiter="\t"))
    # 🔴 **「読みが違う」だけを取る。**全行を渡すと 489件が仕分けに入り、①が意味を失う
    #    （2026-09-14 実測：フィルタを忘れて 489＝①102＋②387 と出た）。fail closed で列名も確かめる。
    if not rows or "判定" not in rows[0]:
        raise SystemExit(f"🔴 {dpath.name} に『判定』の列が無い（上流が替わった）")
    diff = [r for r in rows if r["判定"] == "読みが違う"]
    print(f"{dpath.name}: 全{len(rows)}行 → 『読みが違う』{len(diff)}行だけを仕分ける")
    heard = {r["場面"]: r["聞こえた文"] for r in
             csv.DictReader(hpath.read_text(encoding="utf-8").splitlines(), delimiter="\t")}
    lines = {l.lid: l.text for l in ES.lines()}

    front, mid, same = [], [], []
    for r in diff:
        lid = r.get("場面") or r.get("行")
        if lid in SAME_READING:
            same.append((lid, SAME_READING[lid]))
        elif front_broken(r["台本の読み"], r["聞取の読み"]):
            front.append((lid, r["食い違い"]))
        else:
            mid.append((lid, r["食い違い"]))

    for name, ids in (("front", front), ("mid", mid)):
        p = Q / f"{SLUG}_triage_{name}.txt"
        body = []
        for lid, gap in ids:
            body.append(f"{lid}  [{gap}]\n  台本: {lines.get(lid,'?')}\n  聞取: {heard.get(lid,'?')}")
        p.write_text("\n".join(body) + "\n", encoding="utf-8")
        print(f"{name}: {len(ids)}件 → {p.name}")
    print(f"same（直さない）: {len(same)}件")
    for lid, why in same:
        print(f"   {lid}  {why}")
    print(f"\n合計 {len(diff)}件 ＝ ①{len(front)} ＋ ②{len(mid)} ＋ ③{len(same)}")
    return 0


if __name__ == "__main__":
    unknown = [a for a in sys.argv[1:] if a.startswith("--") and a != "--selftest"]
    if unknown:
        raise SystemExit(f"🔴 知らない引数: {unknown}")
    sys.exit(selftest() if "--selftest" in sys.argv else run())
