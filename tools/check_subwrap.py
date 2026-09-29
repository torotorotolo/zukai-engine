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
  🆕 2026-09-28（14本目⑤b-1）：
  E5 字幕の文字の色が話し手どおりでない＝聞き役（who:"q"）は el_script.SUB_Q_COLOR（水色）・語りは白（J.INK_W）。
     🔴 **焼く直前の SVG**（render_all と同じ `J.remap(sub_strip(行), pal_of_layer("sub_<cid>"))`）で全行を測る
     （記憶 feedback-settings-may-not-reach-the-picture＝設定ではなく絵に届いたものを測る）。
     落ちる形2つ＝①話し手が途中で落ちる（render_all が文字だけ渡していた）②章の色の置き換えが水色を塗り替える
     （水色は J.LINE と同じ値＝赤銅の章で #f2ab95 に化ける）。聞き役の行があるのに色が白のまま（設定が無い）も E5
  E6 2行の字幕の置き方＝行の間が字の 1.25倍未満／字（フチこみ）が帯からはみ出す／2行の字どうしが重なる（`scene_jiko.sub_ys` の値で測る）。
     旧式（0.42／0.78）は 56px で行の間 64.8px＝鳴る
  E7 帯の形の設定（el_script.SUB_BAND＝solid 真っ黒／grad 下が濃く上へ薄い）が、焼く帯の SVG（scene_jiko.sub_band）に届いていない
     ⚠️ 帯の PNG は render_all が中身の指紋で焼き直す（09-28 まで「ファイルが無いときだけ」＝設定を替えても古い帯のまま合成された）
  🆕 2026-09-29（14本目⑥-2・試写1回目の指摘＝まりさ 黄＋黒フチ／れいむ 赤＋白フチ・書体 けいふぉんと）：
  E5 は**字とフチの両方**の色を測る（語り＝el_script.SUB_COLOR＋SUB_EDGE・聞き役＝SUB_Q_COLOR＋SUB_Q_EDGE）
  E6 の字の上下は**字幕の書体の実寸**（字幕に出る全部の字の字面の最大・fontmetrics）。それまでは Noto の漢字の枠（上 0.88・下 0.12）の
     決め打ち＝けいふぉんとは下 0.136em（「た」）で枠より深い。書体を替えたら物差しも替わる
  E8 字幕の書体（el_script.SUB_FONT）が絵に届かない＝①書体を開けない ②字幕に出る字が書体に無い（豆腐か別の書体に落ちる）
     ③焼く SVG の <text> の書体が SUB_FONT でない ④字幕の層の CSS（scene_jiko.sub_css）に SUB_FONT の @font-face が無い
     ⚠️ E1〜E3 の幅も SUB_FONT で測る（折り＝wrap2 も同じ書体。けいふぉんとの1行の幅は Noto の 0.94〜1.01倍）
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
# E6 の selftest と、字幕の束を渡さないときの字（上に高い字・下に深い字を含む＝14本目 c103・c101 の字幕から）
SAMPLE = "船長たちは？2014年4月16日の朝。韓国の南西の海で、旅客船セウォル号が傾いた。「」（）"


def _hex(c):
    """色の書き方をそろえる（#abc → #aabbcc・小文字）"""
    c = c.lower()
    return "#" + "".join(ch * 2 for ch in c[1:]) if len(c) == 4 else c


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
        w = S.fm.width(r, S.SUB_SIZE, S.SUB_FONT)       # 🆕 09-29：描く書体で測る（折り＝wrap2 と同じ）
        if w > S.SUB_MAXW:
            bad.append(f"E1 幅 {w:.0f}px > {S.SUB_MAXW}px「{r}」")
    if len(rows) >= 2:
        for a, b in zip(rows, rows[1:]):
            if T._midword(a.rstrip()[-1:], b.lstrip()[:1]):
                bad.append(f"E2 語の途中で折れる「{a}／{b}」")
        if min(len(r.strip()) for r in rows) <= ORPHAN:
            bad.append(f"E3 尻切れ（{ORPHAN}字以下）「{'／'.join(rows)}」")
    return bad


def judge_colors(cid, segs, strip=None):
    """E5：1カットの字幕を**焼く直前の SVG**にして、各行の文字の色が話し手どおりかを見る。
    strip … 字幕の束を作る関数（既定＝本番の scene_jiko.sub_strip。selftest が落ちる形を差し込む）"""
    import re
    import jiko_style as J
    import scene_jiko as S
    svg = J.remap((strip or S.sub_strip)(segs), S.pal_of_layer(f"sub_{cid}"))
    parts = svg.split('<g transform="translate(0,')[1:]
    if len(parts) != len(segs):
        return [f"E5 {cid}: 字幕 {len(segs)}行 ≠ 焼く SVG {len(parts)}行"]
    bad = []
    hexre = r'="(#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?)"'
    for i, (seg, part) in enumerate(zip(segs, parts), 1):
        q = seg.get("who") == "q"
        # 🆕 2026-09-29（14本目⑥-2）：字（fill）とフチ（stroke）の両方を測る
        want = [_hex(c) for c in ((S.SUB_Q_COLOR, S.SUB_Q_EDGE) if q else (S.SUB_COLOR, S.SUB_EDGE))]
        got = [sorted({_hex(m) for m in re.findall(a + hexre, part)}) for a in ("fill", "stroke")]
        if got != [[want[0]], [want[1]]]:
            bad.append(f"E5 {cid}-{i} 字 {got[0]}・フチ {got[1]} ≠ 字 {want[0]}・フチ {want[1]}"
                       f"（{'聞き役' if q else '語り'}）")
    return bad


def judge_q_setting(subs):
    """E5（回の設定）：聞き役の行があるのに、聞き役の字もフチも語りと同じ（el_script.SUB_Q_COLOR／SUB_Q_EDGE が無い）"""
    import scene_jiko as S
    nq = sum(1 for segs in subs.values() for s in segs if s.get("who") == "q")
    same = (_hex(S.SUB_Q_COLOR), _hex(S.SUB_Q_EDGE)) == (_hex(S.SUB_COLOR), _hex(S.SUB_EDGE))
    if nq and same:
        return [f"E5 聞き役の行が {nq}行あるのに、字とフチの色が語りと同じ（el_script.SUB_Q_COLOR・SUB_Q_EDGE を回ごとに書く）"]
    return []


def font_extent(chars):
    """字幕の書体（scene_jiko.SUB_FONT）で、その字の字面の上下の最大（em）＝(基線より上, 基線より下)。書体を開けなければ None"""
    import scene_jiko as S
    if not S.fm._load(S.SUB_FONT):
        return None
    vals = [S.fm._ink_em(c, S.SUB_FONT) for c in set(chars) if not c.isspace()]
    return (max(v[0] for v in vals), max(v[1] for v in vals)) if vals else None


def judge_geometry(chars=None):
    """E6：1行・2行の字幕の置き方（`scene_jiko.sub_ys`）＝2行の行の間が字の 1.25倍以上・字（フチこみ）が帯の中・2行の字どうしが重ならない。
    字の上下＝**字幕の書体の実寸**（chars＝字幕に出る全部の字。無ければ SAMPLE）＋フチの半分。下は帯の下端から 8px 空ける。
    🆕 2026-09-29（14本目⑥-2）：それまでは Noto の漢字の枠（上 0.88em・下 0.12em）の決め打ち"""
    import scene_jiko as S
    ext = font_extent(chars or SAMPLE)
    if ext is None:
        return [f"E6 字幕の書体 {S.SUB_FONT}（{S.fm.FAMILY_FILE.get(S.SUB_FONT)}）を実測できない"]
    up, dn = ext
    size, half, bad = S.SUB_SIZE, S.SUB_STROKE / 2, []
    for n in (1, 2):
        ys = S.sub_ys(n)
        top, bot = ys[0] - up * size - half, ys[-1] + dn * size + half
        if top < 0 or bot > S.SUB_H - 8:
            bad.append(f"E6 {n}行の字が帯（0〜{S.SUB_H}px・下 8px 空け）からはみ出す（上 {top:.0f}・下 {bot:.0f}）")
        if n == 2 and ys[1] - ys[0] < 1.25 * size:
            bad.append(f"E6 2行の行の間 {ys[1] - ys[0]:.1f}px < 字の 1.25倍（{1.25 * size:.0f}px）＝フチどうしが触れる")
        if n == 2:
            gap = (ys[1] - up * size - half) - (ys[0] + dn * size + half)
            if gap < 0:
                bad.append(f"E6 2行の字（フチこみ）どうしが {-gap:.1f}px 重なる（{S.SUB_FONT} 上 {up:.3f}・下 {dn:.3f}em）")
    return bad


def judge_font(subs, strip=None, css=None):
    """E8：字幕の書体（el_script.SUB_FONT）が絵に届くか（🆕 2026-09-29・14本目⑥-2）。
    ①書体を開ける（fontTools）②字幕に出る字が全部書体にある（無い字＝豆腐か、ブラウザが別の書体に落とす）
    ③焼く SVG（render_all と同じ `J.remap(sub_strip(行), …)`）の <text> がすべて font-family=SUB_FONT
    ④字幕の層を焼く CSS（scene_jiko.sub_css）に SUB_FONT の @font-face がある
    strip・css … selftest が落ちる形を差し込む（既定＝本番の sub_strip・sub_css）"""
    import re
    import jiko_style as J
    import scene_jiko as S
    fam = S.SUB_FONT
    if not S.fm._load(fam):
        return [f"E8 字幕の書体 {fam}（{S.fm.FAMILY_FILE.get(fam)}）を開けない"]
    bad = []
    text = "".join(s["text"] for segs in subs.values() for s in segs)
    miss = sorted(set(S.fm.missing(text, fam)))
    if miss:
        bad.append(f"E8 書体 {fam} に無い字 {len(miss)}種「{''.join(miss[:30])}」（豆腐か別の書体に落ちる）")
    for cid, segs in subs.items():
        if not segs:
            continue
        svg = J.remap((strip or S.sub_strip)(segs), S.pal_of_layer(f"sub_{cid}"))
        fams = set(re.findall(r'<text[^>]*?font-family="([^"]+)"', svg))
        if fams != {fam}:
            bad.append(f"E8 {cid}: 字幕の SVG の書体 {sorted(fams)} ≠ {fam}")
    c = S.sub_css() if css is None else css
    if f"font-family:'{fam}'" not in c:
        bad.append(f"E8 字幕の層の CSS に書体 {fam} の @font-face が無い（scene_jiko.sub_css）")
    return bad


def judge_band():
    """E7：帯の形の設定（el_script.SUB_BAND）が、焼く帯の SVG（scene_jiko.sub_band）に届いているか。"""
    import scene_jiko as S
    svg = S.sub_band()
    solid = 'fill="#000"' in svg and "stop-opacity" not in svg
    grad = "linearGradient" in svg and 'stop-opacity="0"' in svg
    if (S.SUB_BAND == "solid" and not solid) or (S.SUB_BAND == "grad" and not grad):
        return [f"E7 帯の設定 {S.SUB_BAND} が帯の SVG に届いていない（{svg[:70]}…）"]
    return []


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
        errs += judge_colors(cid, segs)
    chars = "".join(s["text"] for segs in subs.values() for s in segs)
    errs += judge_q_setting(subs) + judge_geometry(chars) + judge_band() + judge_font(subs)
    nq = sum(1 for segs in subs.values() for s in segs if s.get("who") == "q")
    import scene_jiko as S
    ext = font_extent(chars)
    face = f"・字面 上 {ext[0]:.3f}・下 {ext[1]:.3f}em" if ext else "・実測できない"
    print(f"字幕 {n}枚（{len(subs)}カット）／2行に折れる {folded}枚／聞き役 {nq}枚／帯 {S.SUB_BAND}"
          f"／書体 {S.SUB_FONT}（{S.fm.FAMILY_FILE[S.SUB_FONT]}{face}）")
    print(f"色＝語り 字 {S.SUB_COLOR}・フチ {S.SUB_EDGE}／聞き役 字 {S.SUB_Q_COLOR}・フチ {S.SUB_Q_EDGE}")
    if errs:
        print(f"🔴 違反 {len(errs)}件:\n  " + "\n  ".join(errs[:40]))
        return 1
    print("✓ 違反 0件（E1 幅・E2 語の途中・E3 尻切れ・E4 台本との食い違い・E5 話し手の字とフチの色・E6 2行の置き方・E7 帯の形・E8 書体）")
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
    # ③ 🆕 E5 話し手の色（2026-09-28・14本目⑤b-1）。見本＝c103 の形（聞き役1行＋語り2行）
    import jiko_style as J
    segs = [{"t": 0.0, "d": 0.7, "text": "船長たちは？", "who": "q"},
            {"t": 1.1, "d": 3.0, "text": "その数分前、助けに来た海洋警察の船に乗り移っていた。"}]
    keep_colors, keep_pal = (S.SUB_COLOR, S.SUB_EDGE, S.SUB_Q_COLOR, S.SUB_Q_EDGE), S.pal_of_layer
    try:
        # 🆕 2026-09-29（14本目⑥-2）：陰性対照は**この回の本番の値のまま**（まりさ 黄＋黒フチ／れいむ 赤＋白フチ）
        ok(not judge_colors("c103", segs), f"E5 陰性対照（本番の経路）が鳴った: {judge_colors('c103', segs)}")
        # 陽性①＝話し手を落とす（09-28 まで render_all は文字だけ渡していた）
        drop = lambda ss: S.sub_strip([s["text"] for s in ss])
        ok(judge_colors("c103", segs, strip=drop), "E5 陽性対照①（話し手が落ちる）が鳴らない")
        # 陽性②＝章の色で化ける色（09-28 の水色＝J.LINE）を聞き役に置き、字幕の層を赤銅の章で置き換える（#f2ab95 に化ける）
        S.SUB_Q_COLOR = J.LINE
        S.pal_of_layer = lambda k: "copper"
        ok(judge_colors("c103", segs), "E5 陽性対照②（章の色で J.LINE が化ける）が鳴らない")
        S.pal_of_layer, S.SUB_Q_COLOR = keep_pal, keep_colors[2]
        # 陽性③＝🆕 フチの色だけ違う（聞き役のフチが別の色で焼かれる）
        edge = lambda ss: S.sub_strip(ss).replace(f'stroke="{S.SUB_Q_EDGE}"', 'stroke="#123456"')
        ok(judge_colors("c103", segs, strip=edge), "E5 陽性対照③（フチの色が違う）が鳴らない")
        # 陽性④＝聞き役の行があるのに、字もフチも語りと同じ（回の設定が無い）
        S.SUB_Q_COLOR, S.SUB_Q_EDGE = S.SUB_COLOR, S.SUB_EDGE
        ok(judge_q_setting({"c103": segs}), "E5 陽性対照④（聞き役の字とフチが語りと同じ）が鳴らない")
        ok(not judge_q_setting({"c101": [{"text": "語りだけ"}]}), "E5 陰性対照（聞き役の無い回）が鳴った")
    finally:
        (S.SUB_COLOR, S.SUB_EDGE, S.SUB_Q_COLOR, S.SUB_Q_EDGE), S.pal_of_layer = keep_colors, keep_pal
    # ④ 🆕 E6 2行の置き方：本番（56px）と 38px は静か・旧式の置き方を 56px で使うと鳴る（字の上下は字幕の書体の実寸）
    keep_ys = S.sub_ys
    try:
        for size in (38, 56):
            S.SUB_SIZE, S.SUB_STROKE = size, round(7 * size / 38)
            ok(not judge_geometry(), f"E6 陰性対照（{size}px の本番の置き方）が鳴った: {judge_geometry()}")
        S.sub_ys = lambda n, h=S.SUB_H: [h * 0.64] if n == 1 else [h * 0.42, h * 0.78]
        ok(judge_geometry(), "E6 陽性対照（旧式の 0.42／0.78 を 56px で）が鳴らない")
    finally:
        S.sub_ys, S.SUB_SIZE, S.SUB_STROKE = keep_ys, keep, round(7 * keep / 38)
    # ⑤ 🆕 E7 帯の形：solid と grad は本番の sub_band で静か・設定を無視する sub_band（いつも grad を返す）で solid だと鳴る
    keep_band, keep_fn = S.SUB_BAND, S.sub_band
    try:
        for b in ("solid", "grad"):
            S.SUB_BAND = b
            ok(not judge_band(), f"E7 陰性対照（{b}）が鳴った: {judge_band()}")
        S.SUB_BAND = "solid"
        S.sub_band = lambda w=S.W, h=S.SUB_H: '<linearGradient id="g"><stop stop-opacity="0"/></linearGradient><rect fill="url(#g)"/>'
        ok(judge_band(), "E7 陽性対照（設定が帯に届かない）が鳴らない")
    finally:
        S.SUB_BAND, S.sub_band = keep_band, keep_fn
    # ⑥ 🆕 E8 書体（2026-09-29・14本目⑥-2）：本番の経路は静か・書体に無い字／SVG の書体違い／CSS に書体が無い、で鳴る
    subs = {"c103": segs}
    ok(not judge_font(subs), f"E8 陰性対照（本番の経路）が鳴った: {judge_font(subs)}")
    ok(judge_font({"c103": [{"text": "船長たちは\U0001F600"}]}), "E8 陽性対照①（書体に無い字＝絵文字）が鳴らない")
    wrong = lambda ss: S.sub_strip(ss).replace(f'font-family="{S.SUB_FONT}"', 'font-family="Nope"')
    ok(judge_font(subs, strip=wrong), "E8 陽性対照②（SVG の書体が回の書体でない）が鳴らない")
    ok(judge_font(subs, css="@font-face{font-family:'Other';}"), "E8 陽性対照③（字幕の層の CSS に書体が無い）が鳴らない")
    if fails:
        print("🔴 selftest:\n  " + "\n  ".join(fails))
        return 1
    print(f"selftest: 検出器 {len(det)}/{len(det)} 鳴った・陰性 静か／折り方 38px と {keep}px で違反なし・c813-1 の実例 ✓"
          f"／E5 字とフチの色 陽性4・陰性2 ✓／E6 置き方 陽性1・陰性2 ✓／E7 帯 陽性1・陰性2 ✓／E8 書体 陽性3・陰性1 ✓"
          f"（書体 {S.SUB_FONT}）")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else run())
