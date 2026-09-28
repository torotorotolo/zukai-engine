# -*- coding: utf-8 -*-
r"""check_subwrap.py — **字幕**の折り返しの門番（9本目テネリフェ ⑤a・2026-09-16 新設）。

  python tools/check_subwrap.py            … audio/narration.json の字幕を全部、本番の wrap2 で折って判定
  python tools/check_subwrap.py --selftest … 陽性・陰性対照（narration.json を読まない）

■ なぜ要るか
  字幕は描画のときに `scene_jiko.wrap2()` が折る（実測幅が SUB_MAXW を超えたら2行。読点が無ければ**幅の真ん中の字の境目**）。
  🆕 2026-09-28（14本目⑤a-2・字幕56px）：wrap2 は**収まる折り目の中から選ぶ**（はみ出し・尻切れ・語の途中を避ける）
     ＝この門番は「避けられなかったもの」を止める網。大きさは el_script.SUB_SIZE（描く側と同じ1か所）
  ⚠️（〜09-27）wrap2 は**禁則も語の途中の割れも見ていない**。しかも、これを検査する門番がリポに1本も無かった
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
    """1枚の字幕 → (折った行, 違反の一覧)。折るのは本番の wrap2。"""
    import scene_jiko as S
    rows = S.wrap2(text)
    return rows, judge_rows(rows)


def judge_rows(rows):
    """折った行 → 違反の一覧（E1〜E3）。🔴 2026-09-28：wrap2 が悪い折り目を避けるようになったので、
    検出器そのものは折った結果を直に渡して試す（selftest）。"""
    import scene_jiko as S
    import titan_fig as T
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
    return bad


def run():
    import narration
    p = ROOT / "audio" / "narration.json"
    if not p.exists():
        print(f"🔴 {p} が無い（先に el_build）")
        return 1
    subs = json.loads(p.read_text(encoding="utf-8"))["subtitles"]
    # 🔴 2026-09-25（14本目⑤a）: 聞き役の印 `Q: ` は字幕に出さない＝台本の側で外して比べ、話者（who）も突き合わせる。
    #    字幕に `Q:` が漏れれば文が食い違って E4 で止まる。印の無い回は話者がどちらも None＝結果は変わらない
    import speaker
    want = [(cid, [speaker.split(t) for t in ls]) for cid, ls in narration.SCRIPT]
    errs, n, folded = [], 0, 0
    got_ids = list(subs.keys())
    if [c for c, _ in want] != got_ids:
        miss = [c for c, _ in want if c not in subs]
        extra = [c for c in got_ids if c not in dict(want)]
        errs.append(f"E4 カットの並びが台本と違う（無い {miss[:5]}／余分 {extra[:5]}）")
    for cid, ls in want:
        segs = subs.get(cid, [])
        rows = [s["text"] for s in segs]
        texts = [t for _, t in ls]
        if rows != texts:
            errs.append(f"E4 {cid}: 字幕 {rows} ≠ 台本 {texts}")
        elif [s.get("who") for s in segs] != [w for w, _ in ls]:
            errs.append(f"E4 {cid}: 話者 {[s.get('who') for s in segs]} ≠ 台本 {[w for w, _ in ls]}")
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
    """🔴 2026-09-28（14本目⑤a-2）：2つに分けて試す。
    ① 検出器（judge_rows）＝悪い折り目を直に渡して鳴るか（wrap2 は悪い折り目を避けるので、wrap2 越しでは試せない）
    ② 折り方（wrap2）＝旧式が悪く折った文を、38px と この回の大きさ（el_script.SUB_SIZE）の両方で、違反なく折るか"""
    import scene_jiko as S
    fails = []
    ok = lambda c, name: None if c else fails.append(name)
    if ORPHAN != S.SUB_ORPHAN:
        fails.append(f"ORPHAN {ORPHAN} と scene_jiko.SUB_ORPHAN {S.SUB_ORPHAN} が違う")

    # ① 検出器の陽性対照（折り目を直に渡す）
    det = [("幅（E1）", ["あ" * 60, "い"]),
           ("数の途中（E2）", ["ボーイング7", "47便が"]),
           ("カタカナ語の途中（E2）", ["あいうボーイ", "ングえお"]),
           ("行頭の閉じ括弧（E2）", ["離陸中", "」とは"]),
           ("行末の始め括弧（E2）", ["あいう「", "離陸"]),
           ("漢字の熟語の途中（E2）", ["あいう滑走", "路えお"]),
           ("尻切れ（E3）", ["あ" * 20 + "、", "いい"])]
    for name, rows in det:
        ok(judge_rows(rows), f"検出器の陽性対照が鳴らない: {name}")
    ok(not judge_rows(["報告書は、根本の原因を", "こう書いている。"]), "検出器の陰性対照が鳴った")

    # ② 折り方：旧式が悪く折った形（真ん中が語の途中・読点が寄っていて片側がはみ出す）を、どの大きさでも違反なく折るか
    keep = S.SUB_SIZE
    try:
        for size in sorted({38, keep}):
            S.SUB_SIZE = size
            n = int(S.SUB_MAXW * 1.6 / size)          # 2行に折れる長さ（1行の約1.6倍）
            half = n // 2

            def at(mid, left="あ", right="い"):
                k = len(mid) // 2
                return left * (half - k) + mid + right * (n - (half - k) - len(mid))
            # ⚠️ ひらがなだけの文は、_midword では境目がほぼ全部「語の途中」＝折れる所が無い（実際の文でない）。
            #    読点の寄りと尻切れは、折れる所のある文（「船は」「海へ」の繰り返し）で試す
            k = int(n * 0.75)
            cases = [("数の途中", at("747便")), ("カタカナ語の途中", at("ボーイング")),
                     ("閉じ括弧", at("中」と")), ("始め括弧", at("「離陸")), ("熟語の途中", at("滑走路")),
                     ("読点が後ろ寄り", ("船は" * n)[:k] + "、" + ("海へ" * n)[:n - k - 1]),
                     ("尻切れ", ("船は" * n)[:n - 3] + "、" + "海へ")]
            for name, t in cases:
                rows, bad = judge(t)
                ok(len(rows) == 2 and not bad, f"{size}px {name}: 違反なく折れない → {'／'.join(rows)} {bad}")
            # 折れる所が1つも無い文は、wrap2 は旧式に落ち、門番が止める（網が素通りしない）
            ok(judge("あ" * n)[1], f"{size}px 折れる所の無い文で門番が鳴らない")
    finally:
        S.SUB_SIZE = keep
    # 14本目 56px で旧式が悪く折った実例 c813-1（語と助詞を割らない＝「何度／も」にしない。始め括弧の前で折る）
    S.SUB_SIZE = 56
    try:
        rows, bad = judge("判決によれば、そのころ2等航海士から何度も「どうしましょうか」と聞かれていた。")
        ok(rows == ["判決によれば、そのころ2等航海士から何度も", "「どうしましょうか」と聞かれていた。"] and not bad,
           f"56px の実例 c813-1 → {'／'.join(rows)}")
    finally:
        S.SUB_SIZE = keep
    # 陰性対照＝読点で素直に折れる文（38px で2行・鳴ってはいけない）
    S.SUB_SIZE = 38
    try:
        rows, bad = judge("報告書は、根本の原因をこう書いている。KLMの機長が、次の四つをしたこと。そして四つとも、止まるための機会だった。")
        ok(len(rows) == 2 and not bad, f"陰性対照: {bad or '折れていない'}")
    finally:
        S.SUB_SIZE = keep
    if fails:
        print("🔴 selftest:\n  " + "\n  ".join(fails))
        return 1
    print(f"selftest: 検出器 {len(det)}/{len(det)} 鳴った・陰性 静か／折り方 38px と {keep}px で違反なし・c813-1 の実例 ✓")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else run())
