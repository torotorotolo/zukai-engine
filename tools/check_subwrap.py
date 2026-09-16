# -*- coding: utf-8 -*-
r"""check_subwrap.py — **字幕**の折り返しの門番（9本目テネリフェ ⑤a・2026-09-16 新設）。

  python tools/check_subwrap.py            … audio/narration.json の字幕を全部、本番の wrap2 で折って判定
  python tools/check_subwrap.py --selftest … 陽性・陰性対照（narration.json を読まない）

■ なぜ要るか
  字幕は描画のときに `scene_jiko.wrap2()` が折る（実測幅が SUB_MAXW を超えたら2行。読点が無ければ**幅の真ん中の字の境目**）。
  ⚠️ wrap2 は**禁則も語の途中の割れも見ていない**。しかも、これを検査する門番がリポに1本も無かった
     （`wrap2(` の呼び出しは scene_jiko.sub_row の1か所だけ＝2026-09-16 に grep で確認）。
  図の中の文字には `check_wrap.py` があるが、あれは `titan_fig.wrap/balance` を包む門番で、**字幕は通らない**。
  ＝ 長い行が来た回に「ボーイング7／47」「「離陸中／」とは」が**黙って**画面に出る（机上検査は1本も鳴らない）。

■ どう見るか（🔴 本番の経路と同じ物差し）
  - 折り方＝ `scene_jiko.wrap2`（描画と同じ関数を呼ぶ。自前で折り直さない）
  - 境目の規則＝ `titan_fig._midword`（図の文字の門番と**同じ1か所**。行頭と行末の禁則を対で持つ
    → 記憶 feedback-kinsoku-needs-both-ends）
  - 字幕の出どころ＝ `audio/narration.json`（描画が読むもの）。**台本（narration.SCRIPT）と1字も違わない**ことも突き合わせる
    （feedback-checks-read-cached-narration＝検査はキャッシュを読む。build のあとに回す）

■ 違反（1件でも exit 1）
  E1 折った1行が SUB_MAXW を超える（2行に折っても入らない）
  E2 折り目が語の途中（_midword）＝数の途中・カタカナ語の途中・漢字の熟語の途中・行頭の「、。」」・行末の「「（」
  E3 折った片方が3字以下（尻切れ）
  E4 narration.json の字幕と narration.SCRIPT の行が食い違う（数・順・文字）
"""
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

ORPHAN = 3


def judge(text):
    """1枚の字幕 → (折った行, 違反の一覧)。"""
    import scene_jiko as S
    import titan_fig as T
    rows = S.wrap2(text)
    bad = []
    for r in rows:
        w = S.fm.width(r, S.SUB_SIZE, "Noto")
        if w > S.SUB_MAXW:
            bad.append(f"E1 幅 {w:.0f}px > {S.SUB_MAXW}px「{r}」")
    if len(rows) >= 2:
        for a, b in zip(rows, rows[1:]):
            if T._midword(a.rstrip()[-1:], b.lstrip()[:1]):
                bad.append(f"E2 語の途中で折れる「{a}／{b}」")
        if min(len(r.strip()) for r in rows) <= ORPHAN:
            bad.append(f"E3 尻切れ（{ORPHAN}字以下）「{'／'.join(rows)}」")
    return rows, bad


def run():
    import narration
    p = ROOT / "audio" / "narration.json"
    if not p.exists():
        print(f"🔴 {p} が無い（先に el_build）")
        return 1
    subs = json.loads(p.read_text(encoding="utf-8"))["subtitles"]
    want = [(cid, [t.strip() for t in ls]) for cid, ls in narration.SCRIPT]
    errs, n, folded = [], 0, 0
    got_ids = list(subs.keys())
    if [c for c, _ in want] != got_ids:
        miss = [c for c, _ in want if c not in subs]
        extra = [c for c in got_ids if c not in dict(want)]
        errs.append(f"E4 カットの並びが台本と違う（無い {miss[:5]}／余分 {extra[:5]}）")
    for cid, ls in want:
        rows = [s["text"] for s in subs.get(cid, [])]
        if rows != ls:
            errs.append(f"E4 {cid}: 字幕 {rows} ≠ 台本 {ls}")
        for i, t in enumerate(rows, 1):
            n += 1
            folded_rows, bad = judge(t)
            folded += len(folded_rows) >= 2
            errs += [f"{cid}-{i} {b}" for b in bad]
    print(f"字幕 {n}枚（{len(subs)}カット）／2行に折れる {folded}枚")
    if errs:
        print(f"🔴 違反 {len(errs)}件:\n  " + "\n  ".join(errs[:40]))
        return 1
    print("✓ 違反 0件（E1 幅・E2 語の途中・E3 尻切れ・E4 台本との食い違い）")
    return 0


def selftest():
    import scene_jiko as S
    fails = []
    base = "あ" * 60
    cut = len(S.wrap2(base)[0])            # 読点の無い文を wrap2 がどこで折るか（本番の関数で測る）

    def at(mid, left="あ", right="い"):
        """mid の真ん中の字の境目が、wrap2 の折り目に来るように並べる。"""
        k = len(mid) // 2
        return left * (cut - k) + mid + right * (60 - (cut - k) - len(mid))

    pos = [("数の途中", at("747便")),                       # 7|47 → E2
           ("カタカナ語の途中", at("ボーイング")),
           ("行頭の閉じ括弧", at("中」と", "あ", "い")),
           ("行末の始め括弧", at("「離陸", "あ", "い")),
           ("漢字の熟語の途中", at("滑走路")),
           ("尻切れ", "あ" * 40 + "、" + "いい" + "う" * 0)]
    for name, t in pos:
        rows, bad = judge(t)
        if not bad:
            fails.append(f"陽性対照が鳴らない: {name} → {'／'.join(rows)}")
    # 陰性対照＝読点で折れる長い文（鳴ってはいけない）
    neg = "報告書は、根本の原因をこう書いている。KLMの機長が、次の四つをしたこと。そして四つとも、止まるための機会だった。"
    rows, bad = judge(neg)
    if bad:
        fails.append(f"陰性対照が鳴った: {bad}")
    if len(rows) < 2:
        fails.append("陰性対照が折れていない（対照になっていない）")
    print(f"wrap2 の折り目（読点なし・60字）= {cut}字目")
    if fails:
        print("🔴 selftest:\n  " + "\n  ".join(fails))
        return 1
    print(f"selftest: 陽性 {len(pos)}/{len(pos)} 鳴った・陰性 1/1 静か")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else run())
