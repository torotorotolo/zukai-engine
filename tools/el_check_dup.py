# -*- coding: utf-8 -*-
r"""el_check_dup.py — 合成音の「重複読み」を探す（2026-09-02・ep009 s101 で見つけた型）。

  python tools\el_check_dup.py ep009
  python tools\el_check_dup.py --selftest

なぜ要るか:
  eleven_v3 は**同じ句をもう一度読む**ことがある。ep009 s101 は
  「ここで、サインの3つ目です。」を2回読み、3テイク振り直しても3回とも同じ位置で重複した。
  ⚠️ el_artifacts の異音の門番は「無音に挟まれた短い塊」を見るので、**1文の重複は見えない**。
  ⚠️ 一致率（el_check_yomi）でも埋もれる（s101 は 88.0% で、25位の中に紛れていた）。
  ⚠️ 秒数でも出ない（s101 は 6.53秒＝字/秒 z-1.10 で正常範囲だった）。
  ＝ 既存の3つの網すべてを素通りする型なので、専用の網を1枚足す。

やること:
  台本/<slug>_el_yomi.tsv（el_check_yomi.py の出力）の「聞こえた文」から、
  記号を落としたうえで **N文字以上の同じ並びが続けて2回**出る行を挙げる。

⚠️ これは当たり付けです。決め手は Scribe の**語ごとの時刻**（2回目が実音の時間を占めているか）。
   本物なら、そのテイクは振り直しでは直らないことがある（本文が誘発している）。
   その場合は EL_YOMI で**句点のあとに空白**を入れる（ep009 s101 で実証）。
出力: 疑わしい行。1行でもあれば exit 1。
"""
import csv
import re
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
MIN_LEN = 6          # これ未満は助詞の並びで普通に再現する（「のは」「ました」など）


def strip_marks(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"[、。「」『』・！？…,.!?\"'\s]", "", s)


def find_dup(heard: str, min_len: int = MIN_LEN, gap: int = 3):
    """『同じ並びが**続けて**2回出る』一番長い並びを返す。無ければ None。

    ⚠️ 「文のどこかに2回出る」で判定してはいけません。2026-09-02 に ep009 s061
       「0%、25%、50%、75%、100%」で誤報が出ました（「二十五パーセント」と
       「七十五パーセント」が『十五パーセント』を共有する）。台本の側と突き合わせる案は、
       送信「25%」／聞取「二十五パーセント」の**表記違い**で当たらないので使えません。
    ⭐ 実際に出た重複読み（s101）は「…3つ目です。3つ目です。…」と**隣接**していました。
       間に短い挿入が入る場合に備えて gap 文字までは離れていてよいことにします。
    """
    h = strip_marks(heard)
    best = None
    for n in range(len(h) - min_len + 1):
        seg = h[n:n + min_len]
        if not re.search(re.escape(seg) + "." + "{0,%d}" % gap + re.escape(seg), h):
            continue
        end = n + min_len          # できるだけ長く伸ばして報告する（原因を掴みやすい）
        while end < len(h):
            longer = h[n:end + 1]
            if not re.search(re.escape(longer) + "." + "{0,%d}" % gap + re.escape(longer), h):
                break
            end += 1
        cand = h[n:end]
        if best is None or len(cand) > len(best):
            best = cand
    return best


def selftest():
    cases = [
        ("ここでサインの三つ目です。サインの三つ目です。楽しくないのに", "サインの三つ目です"),
        ("ここでサインの三つ目です。楽しくないのに気づけば", None),
        ("割合にすると六十七パーセント、つまりおよそ三人に二人にあたります。", None),
        ("必ずもらえる百パーセントと絶対にもらえない零パーセントでは", None),
        # 🔴 離れた場所で並びを共有するだけの誤報（ep009 s061 で実際に出た）
        ("ゼロパーセント、二十五パーセント、五十パーセント、七十五パーセント、百パーセントの五段階です。", None),
        # 続けて2回なら鳴る（⚠️ 報告される並びは繰り返しの「どこから見たか」でずれるので、
        #    期待値は含まれていればよい形にする）
        ("二十五パーセントから四十パーセントから四十パーセントに相当する", "から四十"),
        ("", None),
    ]
    bad = []
    for heard, want in cases:
        got = find_dup(heard)
        ok = (got == want) if want is None else (got is not None and want in got)
        if not ok:
            bad.append(f"「{heard[:30]}」→ {got}／期待 {want}")
    if bad:
        print("selftest 失敗:\n  " + "\n  ".join(bad))
        return 1
    print(f"selftest: {len(cases)}/{len(cases)} 合格")
    return 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    import el_script as ES     # 事故検証ch：tsv は audio/el_qa/<SLUG>_el_yomi.tsv
    tsv = ES.qa_path("el_yomi.tsv")
    if not tsv.exists():
        print(f"★{tsv} がありません。先に el_check_yomi.py を回してください（fail closed）")
        return 2
    rows = list(csv.reader(tsv.open(encoding="utf-8"), delimiter="\t"))
    hdr = rows[0]
    i_id, i_heard = hdr.index("場面"), hdr.index("聞こえた文")
    hits = []
    for r in rows[1:]:
        if len(r) <= i_heard:
            continue
        dup = find_dup(r[i_heard])
        if dup:
            hits.append((r[i_id], dup, r[i_heard]))
    for sid, dup, heard in hits:
        print(f"🔴 {sid}  「{dup}」が2回以上")
        print(f"     聞取: {heard[:100]}")
    print(f"検査 {len(rows)-1}行 → 重複読みの疑い {len(hits)}行"
          + ("（⚠️ 語ごとの時刻で本物か確かめること）" if hits else " ✅"))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
