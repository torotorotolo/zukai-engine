# -*- coding: utf-8 -*-
"""24本目 ⑥：サムネの H 型の反転版（承認①の A＝上「犠牲31人 書き直された報告」・大きな語「チェルノブイリ」・下「原発事故の真相」）。
Vault の hx.py・hx3.py（14〜16本目の反転版の横展開の道具）の lay()・hx2()・pieces()・inv_pair()・compare() を読むだけで使う
（Vault の道具は書き換えない・焼くのは scratchpad の out/）。
地の候補＝改変して使える写真だけ（PD・CC0・CC BY）。BY-SA（IAEA 0279・RIA Novosti）は字を重ねる＝翻案になるので使わない。
    python hx24.py pieces   … 字ごとの塊の検査（小さい「ェ」・「ブ」の濁点・「ル」「リ」の2画が縁でくっつかないか）
    python hx24.py cand     … 地の候補8枚（明るさ 1.15＝本線の v1 の足し込みと同じ）＋並べ2枚（640／210／168px）
    python hx24.py ai       … 生成 AI の地（gen_thumb_ai chn_a・chn_b）＝夜は字の外の明るさ 1.00／1.30／1.60・昼は 1.15／1.30
✅ 10-24 カズヤくん「案A明るさ1.6をA、案B明るさ1.3をBサムネとして設定します。サムネBの設定は私が手動でやる」＝
   A＝`ep24_Hinv_ai_a_b160.png`（→ out/thumb/ep24-ab/ep24_A_Hinv_ai_a_b160.png・md5 f93f733f…）／B＝`ep24_Hinv_ai_b_b130.png`（→ …_B_Hinv_ai_b_b130.png・md5 b3194d29…）
✅ 10-24 公開のあと カズヤくん「Bサムネを、もっと背景の建物が大きく見えるように拡大してください。建物が少し見切れる程度でも良いです」→
   `bzoom` で 1.35／1.6／1.9倍を並べ →「1.35倍」＝**B は `ep24_Hinv_ai_b_b130_z135.png`**（→ out/thumb/ep24-ab/ep24_B_Hinv_ai_b_b130_z135.png・md5 c93a5164…）
    python hx24.py bzoom    … B の地を建物へ寄せる3段（生成の原寸 1792×1008 から・下の端に寄せる cy=1.0）
⚠️ 記録の写し（⑥ の scratchpad の hx24.py）。リポで回すと qa_out/out/ に焼く＝本番の2枚は out/thumb/ep24-ab/ に写してある"""
import sys
from pathlib import Path

RES = Path(r"C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証-サムネ海外競合5ch-20261012")
sys.path.insert(0, str(RES))
import hx  # noqa: E402
import hx3  # noqa: E402
from hx import T, WHT, YEL, RED, txt, lay, hx2, bake2, compare  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).parent / "out"
T.OUT = OUT
hx3.OUT = OUT

GIANT = "チェルノブイリ"
# 太らせ：小さい字と濁点の字は0（19本目「ド」・14本目「ォ」）・2画が離れている字（ル・リ）と点の字は8（18本目「シ」）・ほかは16
BOLD = {"チ": 16, "ェ": 0, "ル": 8, "ノ": 16, "ブ": 0, "イ": 16, "リ": 8}
WSX = {"ブ": 1.25}                                   # 濁点の2本を離す（16本目「バ」「ダ」と同じ）
TOP = [("犠牲31人 ", WHT), ("書き直された", RED), ("報告", WHT)]   # 承認①の A・10-20 の型（「犠牲N人」は白・核心の語だけ赤）
BOTTOM = "原発事故の真相"
BAND = (128, 580)                                    # 16本目と同じ帯（上下の行とのすき間 6px 以上を gap で測る）
ADJ = (1.20, 1.25, 1.15)                             # 本線 h_type_inv の字の外＝vivid_adj (1.15,1.15,1.0)＋H_VIVID_ADD (0.05,0.10,0.15)
GROUNDS = (("c2", "ep24/c2.jpg", {}, "c2 PD\n4号炉と石棺\n（2007年）"),
           ("c0", "ep24/c0.jpg", {}, "c0 CC BY 3.0\n石棺と排気筒\n（2008年）"),
           ("c496", "ep24/c496.jpg", {}, "c496 CC BY 2.0\n吹雪の中の石棺\n（2016年）"),
           ("c488", "ep24/c488.jpg", {}, "c488 CC BY 2.0\n森の向こうの石棺\n（2006年）"),
           ("mx7", "ep24/mx7.jpg", {}, "mx7 CC BY 2.0\n爆発のあとの\n4号炉の模型"),
           ("c475", "ep24/c475.jpg", {}, "c475 CC BY 2.0\n建設中の覆いと\n石棺（2013年）"),
           ("c3309", "ep24/c3309.jpg", {}, "c3309 CC BY 2.0\n覆いの骨組みと\n4号炉（2013年）"),
           ("c3290", "ep24/c3290.jpg", {}, "c3290 CC0\n団地の向こうの\n覆い（2018年）"))


def glyphs():
    gl, fs, sx = lay(GIANT, BAND[0], BAND[1], gap=4, bold=BOLD, wsx=WSX)
    return gl, fs, sx


def extra():
    tfs = hx3.top_fs("".join(s for s, _ in TOP))
    return [txt(TOP, 40, 104, tfs, WHT), txt(BOTTOM, 40, 692, 112, YEL, sw=16)], tfs


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    gl, fs, sx = glyphs()
    if "pieces" in sys.argv:
        print(f"{GIANT}：大きさ {fs:.0f}・長体 {sx:.3f}")
        bad = hx3.pieces(gl)
        print("塊の検査：", "⚠️ " + "".join(bad) if bad else "0件")
    if "cand" in sys.argv:
        ex, tfs = extra()
        print(f"上の行の大きさ {tfs}・幅 {T.h_adv(''.join(s for s, _ in TOP), tfs):.0f}px")
        hx3.rim_only("_fit_ep24", gl)
        inside, red = hx3.inside_mask("_fit_ep24")
        rows = []
        for tag, src, crop, lb in GROUNDS:
            d, c = hx3.inv_pair(src, ADJ, crop)
            bake2(f"ep24_Hinv_{tag}", hx2(d, c, gl, ex))
            i, o, df = hx3.lum(f"ep24_Hinv_{tag}", inside, red)
            print(f"  {tag}: 字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}")
            rows.append((OUT / f"ep24_Hinv_{tag}.png", lb))
        compare(rows[:4], "cmp24_1.png")
        compare(rows[4:], "cmp24_2.png")
    if "ai" in sys.argv:
        # 10-24 カズヤくん「生成AI 案A＋案B」＝gen_thumb_ai chn_a（夜）・chn_b（昼）。夜は字の外の明るさ 1.00／1.30／1.60 の3段（記憶の決まり）
        ex, tfs = extra()
        hx3.rim_only("_fit_ep24", gl)
        inside, red = hx3.inside_mask("_fit_ep24")
        for tag, src, levels in (("ai_a", "ep24/ai/ep24_chn_a.jpg", (1.00, 1.30, 1.60)),
                                 ("ai_b", "ep24/ai/ep24_chn_b.jpg", (1.15, 1.30))):
            rows = [(T.HERE / "ref" / src, f"{tag} 生成の地\n（字なし）")]
            for b in levels:
                d, c = hx3.inv_pair(src, ADJ, {}, out_bright=b)
                name = f"ep24_Hinv_{tag}_b{round(b * 100)}"
                bake2(name, hx2(d, c, gl, ex))
                i, o, df = hx3.lum(name, inside, red)
                print(f"  {name}: 字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}")
                rows.append((OUT / f"{name}.png", f"{tag}\n字の外の明るさ\n{b:.2f}"))
            compare(rows, f"cmp24_{tag}.png")
    if "bzoom" in sys.argv:
        # 10-24 カズヤくん「Bサムネを、もっと背景の建物が大きく見えるように拡大してください。建物が少し見切れる程度でも良いです」
        #   建物（4号炉の建屋と排気筒）は絵の下＝cy=1.0（下の端に寄せる）・横は建屋の真ん中へ。寄せても粗くならないよう生成の原寸から切る
        #   ✅ カズヤくん「1.35倍」（ヘリ2機が上に残る）
        ex, tfs = extra()
        rows = [(OUT / "ep24_Hinv_ai_b_b130.png", "いまの B\n（寄せなし）")]
        for tag, z, cx in (("z135", 1.35, 0.72), ("z160", 1.60, 0.66), ("z190", 1.90, 0.63)):
            d, c = hx3.inv_pair("ep24/ai/ep24_chn_b_orig.png", ADJ, dict(zoom=z, cx=cx, cy=1.0), out_bright=1.30)
            name = f"ep24_Hinv_ai_b_b130_{tag}"
            bake2(name, hx2(d, c, gl, ex))
            rows.append((OUT / f"{name}.png", f"B {z:.2f}倍\n（建物に寄せる）"))
        compare(rows, "cmp24_bzoom.png")
