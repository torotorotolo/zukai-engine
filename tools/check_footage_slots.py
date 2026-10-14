# -*- coding: utf-8 -*-
"""🔴 実写の欄が**全部埋まっているか**を、カットの側から数える門番（2026-09-08 ⑤b-4 新設）。

■ なぜ要るか（この日に実際に踏んだ）
  `python tools/footage.py fetch --check` は
    「✓ 全 35 欄に until= があり…」
  と**合格を出す**。しかし 35 は `USE` に書いた欄の数であって、
  **実写が要るカットの数（66）ではない**。
  ＝ 31欄が空のままでも、この門番は「0件を調べて合格」を出す
     → [[feedback-gates-blind-to-the-new-material]]

■ 何を数えるか
  章ファイルで `photo=ss.fb("<cid>")` と書いてあるカット ＝ 実写の欄。
  そのカットが `footage.USE` にあるか。**両側から突き合わせる**（片側だけだと
  「USE に在るがカットに無い」欄＝台本を直したあとの取り残しが見えない）。

■ 使い方
    python tools/check_footage_slots.py
    python tools/check_footage_slots.py --selftest
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent
# 🔴🔴 2026-09-13（7本目 ⑤b-2）**`ss.rg("…")` を知らなかった。**
#   7本目の ⑤b-1 で `cuts/ss.py` に `rg(cid, **kw)` という1行で書ける助けを新設し、
#   章ファイルは `"c222": ss.rg("c222", …)` と書く（中で `photo=fb(cid)` になる）。
#   ところがこの門番は **`photo=ss.fb("…")` という字面しか探していない**ので、
#   実写18カットを1件も拾えず「**実写の欄が1つも見つからない**」で exit 2 を出した。
#   ＝ 門番が在るのに、新しい書き方を見ていない
#     （[[feedback-gates-blind-to-the-new-material]]／[[feedback-per-episode-constants-go-stale]]）。
#   ⚠️ 古い書き方も残す（前の回の章ファイルを読むときに要る）。
#
# 🔴🔴 2026-09-15（8本目 ⑤b-2）**同じ穴をもう一度踏んだ。**
#   8本目は `cuts/ss.py` の **`vid(cid, pw, clip=None, **kw)`** で書く
#   （`ss.rg` は 7本目の RG237 専用の名前だった）。字面が違うので、
#   この門番はまた「実写の欄が1つも見つからない」で exit 2 を出した。
#   → **新しい書き方を足すたびに、ここも足す。**逆に、ここに無い書き方で書かない。
#   🆕 2026-10-05（18本目 ⑤b-7c）：映像の差し込み（頭）＝`intro=ss.head("c109")`（footage.USE の head=True）も拾う
#   🆕 2026-10-07（19本目 ⑤b-7c）：映像の差し込み（尻）＝`tail=ss.tailv("c104", …)`（footage.USE の鍵 `c104~t`・tail=True）
FB = re.compile(r'(?:photo=ss\.fb\("(\w+)"\)|ss\.rg\(\s*"(\w+)"|ss\.vid\(\s*"(\w+)"|ss\.head\(\s*"(\w+)"|ss\.tailv\(\s*"(\w+)")')


def slots(cutdir=None):
    """章ファイルから「実写が要るカット」を拾う。**SPEC ではなく本文を読む**。

    ⚠️ `scene_jiko` 経由で読むと、章ファイルが1本落ちていても
       「残った分で0件」になりうる。ここは .py の本文を直接読む。
    """
    d = Path(cutdir) if cutdir else HERE / "cuts"
    out = {}
    for f in sorted(d.glob("*.py")):
        if f.name in ("__init__.py", "ss.py"):
            continue
        for m in FB.finditer(f.read_text(encoding="utf-8")):
            if m.group(5):
                out[m.group(5) + "~t"] = f.name                 # 尻の映像の欄（scene_jiko.TAIL_KEY）
                continue
            out[m.group(1) or m.group(2) or m.group(3) or m.group(4)] = f.name
    return out


def main(only=None):
    import footage as F
    need = slots()
    use = set(F.USE)
    if not need:
        # 🔴🔴 2026-09-16（9本目 テネリフェ ⑤b-1）**動く映像が0本の回では、この門番は永久に落ちた。**
        #    「字面が1つも無い＝章ファイルを読めていない」と決めつけていたので、215カットを
        #    書き終えても exit 2 のまま（9本目は Commons を8通りの語で当たって映像0本）。
        #    ⚠️ ただし「0件を合格にしない」は崩さない。**字面ではなく `cuts` の読み込みで**見分ける：
        #      ・`footage.CLIPS` も `USE` も空（＝この回は映像を持たない）
        #      ・`cuts.BROKEN` が空で、章ファイルが `CHAPTER_FILES` の枚数そろっていて、SPEC が空でない
        #    このときだけ「動画の欄は0で正しい」と言う。どれか欠ければ従来どおり exit 2。
        if not F.CLIPS and not use:
            import cuts                                          # noqa: PLC0415
            files = [f for f in HERE.joinpath("cuts").glob("*.py")
                     if f.name not in ("__init__.py", "ss.py")]
            if cuts.BROKEN or not cuts.SPEC or len(files) < len(cuts.CHAPTER_FILES):
                print(f"🔴 章ファイルを読めていない（読めない章 {sorted(cuts.BROKEN)}／"
                      f"章ファイル {len(files)}枚／SPEC {len(cuts.SPEC)}カット）。合格にしない")
                return 2
            print(f"✓ この回は動く映像0本（footage.CLIPS 0・USE 0）。章ファイル {len(files)}枚・"
                  f"{len(cuts.SPEC)}カットを読めていて、動画の欄は0で正しい")
            return 0
        print("🔴 実写の欄が1つも見つからない＝**章ファイルを読めていない**（合格にしない）")
        return 2
    missing = sorted(set(need) - use)
    extra = sorted(use - set(need))
    print(f"■ 実写が要るカット {len(need)} 欄／`footage.USE` に書けている {len(use & set(need))} 欄")
    if missing:
        print(f"🔴 まだ埋まっていない {len(missing)} 欄:")
        for i in range(0, len(missing), 10):
            print("   " + " ".join(missing[i:i + 10]))
    if extra:
        print(f"🔴 USE に在るのに実写のカットでない {len(extra)} 欄: {' '.join(extra)}")
    if not missing and not extra:
        print("✓ 実写の欄とカットが1対1")
    return 0 if not missing and not extra else 1


def selftest():
    """陽性対照＝**本番の中身が空でも回ること**と、欠けをちゃんと鳴らすこと。"""
    ok = True
    n = len(slots())
    print(f"  章ファイルから拾えた実写の欄 {n}")
    if n == 0:
        print("🔴 0件＝読めていない"); ok = False
    tmp = Path(__file__).parent.parent / "out" / "jiko" / "_slots_selftest"
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "z.py").write_text('photo=ss.fb("zz01")\nphoto=ss.fb("zz02")\nintro=ss.head("zz03")\n',
                              encoding="utf-8")
    got = slots(tmp)
    if sorted(got) != ["zz01", "zz02", "zz03"]:
        print(f"🔴 拾い方が違う: {got}"); ok = False
    else:
        print("  当て木の章ファイル4欄を拾えた（ss.fb 2件＋ss.rg 2件）")
    (tmp / "z.py").unlink()
    tmp.rmdir()
    # 🆕 2026-10-13（21本目 ⑤b-7）：額装だけの点（BY-SA）を映像のひかえに当てたカットは、`footage.USE` の欄も額装の網（cuts/ss.check_frame_only）が見る
    #    ＝寄り 1.0・等速・plain=True 以外を止める（⑤b-2 の宿題）。この回の束に額装だけの映像のひかえが無ければ見ない
    import cuts.ss as ss
    # 🔴 2026-10-14（22本目 ⑤b-1）：回を替えた直後は**この回の束（`ref/<回>/assets.json`）がまだ無い**＝`ss.frame_only()` が止まる
    #    （fail closed＝本番の照合では正しい）。selftest のこの対照は「この回の束の中の額装だけの映像」で作る作りなので、束が無いうちは
    #    理由を出して見ない（束のチャットで assets.json を作れば戻る）。⚠️ 束があるのに額装だけの映像が0点なら、今までどおり黙って見ない
    if not (ss.REF / "assets.json").exists():
        print(f"  額装だけの映像の対照：この回の束 {ss.REF.name}/assets.json がまだ無い＝見ない（束のチャットで戻る）")
        fo = []
    else:
        fo = [n for n in ss.frame_only() if "/fb_" in n]
    if fo:
        cid = fo[0].rsplit("fb_", 1)[1].split(".")[0]
        spec = {cid: dict(photo=fo[0], panel=True, color=1.0)}
        good = {cid: dict(clip="X", start=0.0, until=1.0, rate=1.0, zoom=1.0, plain=True)}
        bad = {cid: dict(clip="X", start=0.0, until=1.0, rate=0.9, zoom=1.03)}
        g, b = ss.check_frame_only(spec, use=good), ss.check_frame_only(spec, use=bad)
        if g:
            print(f"🔴 陰性対照：額装だけの映像（{cid}）を寄り 1.0・等速・plain で使って鳴った：{g}"); ok = False
        elif not (len(b) == 1 and all(w in b[0] for w in ("zoom", "rate", "plain"))):
            print(f"🔴 陽性対照：額装だけの映像（{cid}）を寄り 1.03・0.9倍・地のぼかしで使って鳴らない：{b}"); ok = False
        else:
            print(f"  額装だけの映像（{cid}）：寄り・倍率・地を変えると鳴り、変えなければ鳴らない（cuts/ss.check_frame_only）")
    print("✓ selftest 通過" if ok else "🔴 selftest 失敗")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(0 if selftest() else 1)
    raise SystemExit(main())
