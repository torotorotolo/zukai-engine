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


def front_broken(script_text, heard_text):
    """台本の先頭2字が、聞取の先頭 FRONT_LOOK 字のどこにも無い＝文頭が落ちている。"""
    return script_text[:2] not in heard_text[:FRONT_LOOK]


def selftest():
    fails = []
    ok = lambda c, n: (None if c else fails.append(n))
    # 陽性対照＝頭が丸ごと落ちた形（7本目 c110-1 で実測した型）
    ok(front_broken("点は、ペンタゴンの", "はペンタゴンの西へ"), "頭が落ちていれば①")
    # 陰性対照＝先頭2字が聞取の6字以内にある
    ok(front_broken("着陸の予定は", "着陸の予定は現地時間の") is False, "そのままなら①ではない")
    ok(front_broken("2003年2月1日、朝。", "2010年2月1日、朝。") is False,
       "先頭2字が残っていれば①ではない（数の誤読は②で拾う）")
    # 境界: 先頭2字が7字目にある＝①と見る（FRONT_LOOK の窓の外）
    ok(front_broken("桁の裏の", "あああああ桁の裏の"), "先頭2字が7字目なら①（窓の外）")
    # 🔴 **既知の偽陽性**＝頭の表記が漢字→かなに替わっただけでも①に落ちる。
    #    読みは合っているので retake しても直らない。**①は目で1件ずつ見る**（下の run() の出力に実文を出す）。
    ok(front_broken("軍の指揮系統は", "ぐんの指揮系統は"),
       "🔴 既知の偽陽性: 頭が かな書きでも①に落ちる（読みは同じ）")
    if fails:
        print(f"selftest: 落ちた: {fails}")
        return 1
    print(f"selftest: 5/5 合格（FRONT_LOOK={FRONT_LOOK}・ファイルを読んでいない）")
    return 0


def run():
    import el_script as ES
    dpath, hpath = Q / f"{SLUG}_reading_diff.tsv", Q / f"{SLUG}_el_yomi.tsv"
    for p in (dpath, hpath):
        if not p.exists():
            raise SystemExit(f"🔴 まだ無い: {p}（先に el_check_yomi → el_reading_diff）")
    diff = list(csv.DictReader(dpath.read_text(encoding="utf-8").splitlines(), delimiter="\t"))
    heard = {r["場面"]: r["聞こえた文"] for r in
             csv.DictReader(hpath.read_text(encoding="utf-8").splitlines(), delimiter="\t")}
    lines = {l.lid: l.text for l in ES.lines()}

    front, mid, same = [], [], []
    for r in diff:
        lid = r.get("場面") or r.get("行")
        if lid in SAME_READING:
            same.append((lid, SAME_READING[lid]))
        elif lid in lines and front_broken(lines[lid], heard.get(lid, "")):
            front.append(lid)
        else:
            mid.append(lid)

    for name, ids in (("front", front), ("mid", mid)):
        p = Q / f"{SLUG}_triage_{name}.txt"
        body = []
        for lid in ids:
            body.append(f"{lid}\n  台本: {lines.get(lid,'?')}\n  聞取: {heard.get(lid,'?')}")
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
