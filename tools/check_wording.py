# -*- coding: utf-8 -*-
"""画面の言葉づかいの門番（2026-09-10 新設・6本目キー橋 ⑤c'【直す】3巡目）。

■ なぜ要るか
  ⑤c 検品【見る】3周目で、**目で見ないと出てこない粗**を24件出した。そのうち5型は
  **設計の文字列だけで機械的に取れる**（[[feedback-rules-need-gates]]。検査の無い規則は守られない）。

    A 見出し・副題が、答えをそのまま先に言う          （台帳 §V-14・13件）
    B 画面が視聴者に語りかける「楽屋の言葉」          （台帳 §V-15・5件）
    C 見出しと答えが指示語で始まる／指示語しか指さない（台帳 §V-16・5件）
    D 答えが名詞句でない（動詞終止・読点入りの文）    （台帳 §V-17・11件）
    E 段ラベルが1枚の中で通し番号とそれ以外で混ざる   （台帳 §V-25・2件）

  ⚠️ **絵を見ないと決まらない粗（§V-18 写っていないものを名乗る／§V-19 絵と時点の食い違い）は
     ここには入らない。** 門番にできないので ⑤c' で人が絵を見て決める。

■ しきい値の決め方（[[feedback-gate-threshold-from-ledger-split]]）
  語の一覧も長さの下限も、**本編216カットの全件に当ててから**、台帳が「粗」と書いた件が
  鳴り、「粗ではない」と検算ずみの件が黙る線に置いた。`--all` で黙っている候補も出る。

■ 使い方
    python -u tools/check_wording.py            # 🔴 だけ
    python -u tools/check_wording.py --all      # 黙らせている候補も出す
    python -u tools/check_wording.py --selftest # 物差しの検算（陽性対照つき）

  exit 0 ＝ 0件／1 ＝ 粗あり。⚠️ 例外で落ちたら 0件と数えない（fail closed）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

from cuts import SPEC                                       # noqa: E402

# ── B 楽屋の言葉 ────────────────────────────────────────────────
# 画面が「この動画」「視聴者」を名指すもの、番組の進行を語るもの。
# ⚠️ 「報告書が」「NTSBが」は主体が作品の外なので入れない。
GREENROOM = ("視聴者", "この動画", "この番組", "本編", "ここから見て",
             "見ていきます", "以下、", "と呼ぶ", "が追うもの", "ここで浮かぶ",
             "読むところ", "どこに書かれているか", "この動きへの")

# ── C 指示語 ────────────────────────────────────────────────────
# 🔴 しきい値は**本編216カットの全件に当ててから**決めた（[[feedback-gate-threshold-from-ledger-split]]）。
#    最初は見出しも見ていたが、それだと 14件のうち 11件が
#    「その検査で、何も出ていない」（c112）「その夜、8人だけだった」（c210）のように
#    **直前のカットを受けた正しい連続**だった。34分の語りで前のカットを指すのは型であって粗ではない。
#    → **答え（`v`／`v` の無い段の `d`）だけ**を見る。答えは単独で読めなければならない。
#      台帳 §V-16 が挙げた5件のうち、答えの側は `c719`「これで起きた」`pr02`「それを見て回っていた」で、
#      どちらもこの線で鳴る。見出しの側（`c809` `c823` `ep03`）は ⑤c' で目視して直した。
DEIXIS = ("この", "その", "それ", "これ", "ここ", "あの", "そう")

# ── D 答えが名詞句でない ────────────────────────────────────────
# 末尾がこの形なら動詞・形容詞の終止（＝文）。名詞で終わる答えは鳴らない。
VERB_TAIL = ("った", "いた", "えた", "した", "きた", "ちた", "んだ", "ない",
             "ている", "ていた", "える", "きる", "がる", "なる", "する",
             "はず", "だろう", "ではないか", "かった", "らない", "れた",
             "った", "だった", "ます", "です", "しい", "かる")
# ⚠️ 名詞で終わるのに上に当たってしまう語は、ここで**明示して**外す
#    （黙らせた理由が読めるようにする。正規表現で誤魔化さない）。
NOT_VERB = ("見立て", "手はず", "気配", "しるし")

NUM = re.compile(r"^[0-9,.]+$")


def answers(sp):
    """そのカットの「答え」を (どこ, 字面) で返す。

    ⚠️ `v` が無い段では `d` が答えそのもの（`titan_fig` 型⑩の注と同じ扱い）。
       `v` がある段の `d` は本当の補足なので答えに数えない。
    """
    out = []
    for i, a in enumerate(sp.get("ann", []) or []):
        if a.get("v"):
            out.append((f"ann{i + 1}.v", str(a["v"])))
        elif a.get("d"):
            out.append((f"ann{i + 1}.d", str(a["d"])))
    f = sp.get("fig")
    if f and f[0] in ("panel", "moment"):
        for i, b in enumerate(f[1].get("blocks", []) or []):
            if b.get("v"):
                out.append((f"blk{i + 1}.v", str(b["v"])))
    return out


def questions(sp):
    out = []
    for i, a in enumerate(sp.get("ann", []) or []):
        if a.get("t"):
            out.append((f"ann{i + 1}.t", str(a["t"])))
    f = sp.get("fig")
    if f and f[0] in ("panel", "moment"):
        for i, b in enumerate(f[1].get("blocks", []) or []):
            if b.get("t"):
                out.append((f"blk{i + 1}.t", str(b["t"])))
    return out


def labels(sp):
    f = sp.get("fig")
    if not f or f[0] != "panel":
        return []
    return [str(b["k"]) for b in (f[1].get("blocks", []) or []) if b.get("k")]


def scan(spec, minlen=3):
    """(型, カット, 欄, 字面, ひとこと) の並びを返す。"""
    hits = []
    for cid, sp in spec.items():
        t, s = str(sp.get("t", "")), str(sp.get("s", ""))
        ans = answers(sp)

        # A 見出し・副題が答えを先に言う
        for where, v in ans:
            if len(v) < minlen or NUM.match(v):
                continue
            for name, head in (("見出し", t), ("副題", s)):
                if v and v in head:
                    hits.append(("A", cid, where, v,
                                 f"{name}「{head}」が答えをそのまま含む"))

        # B 楽屋の言葉
        for name, txt in (("見出し", t), ("副題", s)) + tuple(
                (w, x) for w, x in questions(sp)):
            for g in GREENROOM:
                if g in txt:
                    hits.append(("B", cid, name, txt, f"楽屋の言葉「{g}」"))
                    break

        # C 指示語（⚠️ **答えだけ**。見出しと問いは黙る。上の注を見る）
        for where, txt in ans:
            for d in DEIXIS:
                if txt.startswith(d) or f"、{d}" in txt:
                    hits.append(("C", cid, where, txt, f"指示語「{d}」"))
                    break

        # D 答えが名詞句でない
        for where, v in ans:
            why = ""
            if "、" in v:
                why = "読点が入っている＝文になっている"
            elif any(v.endswith(x) for x in VERB_TAIL) and \
                    not any(v.endswith(x) for x in NOT_VERB):
                why = f"末尾「{v[-2:]}」＝動詞・形容詞の終止"
            if why:
                hits.append(("D", cid, where, v, why))

        # E 段ラベルの混在
        ks = labels(sp)
        if ks:
            num = [k for k in ks if k.isdigit()]
            oth = [k for k in ks if not k.isdigit()]
            if num and oth:
                hits.append(("E", cid, "panel.k", "／".join(ks),
                             "通し番号とそれ以外が1枚で混ざる"))
    return hits


NAMES = {"A": "見出し・副題が答えを先に言う", "B": "楽屋の言葉",
         "C": "指示語", "D": "答えが名詞句でない", "E": "段ラベルの混在"}

# 🔴 exit を動かす型（＝焼く前に 0件でなければならないもの）。
# ⚠️ **D は入れない。** 全216カットに当てると31件出るが、その多くは
#    「電気が来ない」「生きていた」「奥まで入っていない」のように**否定形・動詞終止のほうが
#    正しい答え**で、名詞句に直すと言葉が冷たくなる。台帳 §V-17 が粗と数えたのは
#    **絵と前後を見たうえで**噛み合っていなかった11件で、机上では区別が付かない
#    （[[feedback-desk-checks-dont-see-pictures]]）。
#    → D は**数えて必ず画面に出すが、exit は動かさない**。⑤c の目視で1件ずつ決める。
#    ⚠️ 「数が多いから黙らせる」ではない。黙らせたら忘れられる
#      （[[feedback-gates-blind-spot-is-the-scan-direction]]）ので、毎回出す。
BLOCKING = "ABCE"


def main(show_all=False):
    print("■ 画面の言葉づかい（§V-14 A／§V-15 B／§V-16 C／§V-17 D／§V-25 E）")
    print(f"■ cuts: {Path(sys.modules['cuts'].__file__).resolve()}／SPEC {len(SPEC)} カット")
    hits = scan(SPEC)
    bad = [h for h in hits if h[0] in BLOCKING]
    for kind in "ABCDE":
        rows = [h for h in hits if h[0] == kind]
        mark = "" if kind in BLOCKING else "（⚠️ 目視で決める。exit は動かさない）"
        print(f"\n── {kind}. {NAMES[kind]} ＝ {len(rows)} 件{mark}")
        for _k, cid, where, txt, why in (rows if show_all else rows[:20]):
            print(f"  {'🔴' if kind in BLOCKING else '⚠️'} {cid} [{where}]"
                  f"「{txt}」── {why}")
        if not show_all and len(rows) > 20:
            print(f"  …ほか {len(rows) - 20} 件（--all で全部）")
    print(f"\n{'🔴' if bad else '✓'} exit を動かす型（{BLOCKING}）＝ {len(bad)} 件"
          f"／目視で決める型（D）＝ {len(hits) - len(bad)} 件")
    print("  ⚠️ §V-18（写っていないものを名乗る）と §V-19（絵と時点の食い違い）は"
          "**絵を見ないと決まらない**ので、この門番では取れない。")
    return 1 if bad else 0


def selftest():
    """物差しの検算。⚠️ 件数だけでなく**どの型が鳴ったか**で見る。"""
    ok = True

    def say(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '🔴'} {msg}")

    # 陽性対照：わざと5型ぜんぶを踏む1カットを作る
    bad = {"zz01": dict(
        t="この造りのせいだった",                       # A・C
        s="視聴者がいちばん先に思うこと",               # B
        ann=[dict(t="ここで浮かぶ問い", v="この造りのせいだった")],
        fig=("panel", dict(blocks=[dict(k="問", t="なぜ", v="工事のために、元からいた"),
                                   dict(k="1", t="いつ", v="休憩中だった")])))}
    h = scan(bad)
    got = {k for k, *_ in h}
    for kind in "ABCDE":
        say(kind in got, f"陽性対照で {kind}（{NAMES[kind]}）が鳴る")

    # 陰性対照：直したあとの形は1件も鳴らない
    good = {"zz02": dict(
        t="疑いは、造りのほうへ向く",
        s="報告書が使う呼び名",
        ann=[dict(t="橋の骨組み", v="非冗長鋼引張部材")],
        fig=("panel", dict(blocks=[dict(k="1", t="なぜ", v="工事のため"),
                                   dict(k="2", t="いつ", v="休憩中")])))}
    say(not scan(good), f"陰性対照は0件（出た: {scan(good)}）")

    # ⚠️ 「見立て」のように名詞で終わるのに末尾が動詞に見える語を黙らせているか
    say(not [x for x in scan({"zz03": dict(t="あ", s="い",
                                           ann=[dict(t="問", v="報告書の見立て")])})
             if x[0] == "D"], "名詞で終わる「見立て」は D で鳴らない")
    print(f"\n{'✓ 物差しは通った' if ok else '🔴 物差しが壊れている'}")
    return 0 if ok else 3


if __name__ == "__main__":
    a = sys.argv[1:]
    raise SystemExit(selftest() if "--selftest" in a else main("--all" in a))
