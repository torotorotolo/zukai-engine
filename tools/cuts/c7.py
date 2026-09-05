# -*- coding: utf-8 -*-
"""第7章 そうではなかったもの c701–c726（26カット）。

■ この章の役目
  **追うのは、87パークの土と構造の解析。噂を出しっぱなしにしないための章。**
  🔴 噂を語るカット（c703 c709）には「噂」の札を出す（ルール §5＝噂と事実を画面で分ける）。
  決め所は c717「傷んだつなぎ目を壊すにも、小さすぎた」・c722「大きく寄与してはいない」。

■ 出どころ
  技術的知見 p184（数字だけ。Google の画像は出さない）・p185・p189／NIST ニュース 2026-06-22／B-Roll #1・#2・#5。
  ⚠️ 87 Park は建物の**南**隣（p3 で確認）。字幕は「エイティセブン・パーク」、画面の札は `87 Park`。
"""
import jiko_style as J
import cuts.ss as ss

RUMOR = dict(t="■ 言われていること", d="確かめられていない、噂の段階の話", c=J.ALERT, ts=40,
             dc=J.LINE, ds=30)

SPEC = {

    # ── c701 24通り ───────────────────────
    "c701": dict(
        t="検討した筋書きは、24通り",
        s="NIST ニュース 2026年6月22日",
        fig=("compare", dict(
            items=[dict(v=24, t="検討した筋書き", disp="24", unit="通り", c=J.LINE),
                   dict(v=1, t="残った筋書き", disp="1", unit="つ", sub="プールデッキの押し抜き", c=J.ALERT)],
            note="※ どこで、なぜ始まったかについて（NIST ニュース）")),
    ),

    # ── c702 残らなかった23通り ────────────────
    "c702": dict(
        t="落とされた説の中身",
        s="p189 の一覧の前に",
        fig=("absent", dict(
            mode="seat", lead="24通りの筋書き",
            items=[dict(t="残った", d="プールデッキの押し抜き", ok=True, c=J.OK),
                   dict(t="残らなかった", d="23通り", ok=False, c=J.LINE)],
            note="5つを次から見ていく（p189）")),
    ),

    # ── c703 いくつもの説（噂の札）─────────────────
    "c703": dict(
        t="起きた直後から、いくつもの説",
        s="現場の引き（NIST 記録映像）",
        photo=ss.fb("c703"), bias=0.5, side="right", ann_y=340,
        ann=[RUMOR],
    ),

    # ── c704 噂であることを明示 ─────────────────
    "c704": dict(
        t="確かめられてはいない、噂の段階",
        s="第7章で答える噂",
        fig=("panel", dict(
            lead="■ 言われていることの出どころ",
            blocks=[dict(k="噂", t="報道", c=J.LINE),
                    dict(k="噂", t="住民の話", c=J.LINE),
                    dict(k="噂", t="裁判のなか", c=J.LINE)],
            cols=3, note="※ ここは噂。出どころのある事実ではない。この章は、これに NIST の解析で答える")),
    ),

    # ── c705 隣の工事（87 Park）────────────────
    "c705": dict(
        t="すぐ南側に、別の高層マンション",
        s="87 Park と現場（NIST 空撮の1コマ）",
        photo=ss.S_87PARK, side="right", ann_y=340, bias=0.45, xbias=0.15, zoom=1.4,
        ann=[dict(t="87 Park", d="建物のすぐ南側に建設中だった", dc=J.INK_W, ds=32)],
    ),

    # ── c706 敷地の境界（自作）─────────────────
    "c706": dict(
        t="地面を掘り、鋼の板を打ち込んだ",
        s="敷地の境界（模式）",
        fig=("mapfig", dict(
            lead="北が上・縮尺なし",
            points=[dict(x=0.50, y=0.30, t="Champlain Towers South", d="崩れた建物", c=J.INK_W,
                         kind="part"),
                    dict(x=0.50, y=0.74, t="87 Park", d="建設中（掘削・鋼矢板）", c=J.ALERT,
                         kind="part")],
            link=(0, 1), scale="最短 約9フィート",
            note="距離は p184 の数字だけ（画像は Google のため出さない）")),
    ),

    # ── c707 約9フィート ─────────────────
    "c707": dict(
        t="最短で、およそ9フィート",
        s="NIST が測った距離（p184）",
        fig=("compare", dict(
            items=[dict(v=9, t="打ち込み位置 ⇄ 建物の壁", disp="約9", unit="ft", sub="最短", c=J.ALERT),
                   dict(v=150, t="建物の短辺", disp="150", unit="ft", sub="p3", c=J.LINE)],
            note="※ 9フィート＝NIST の実測（p184）")),
    ),

    # ── c708 9フィート＝約2.7メートル ────────────
    "c708": dict(
        t="2.7メートル、という近さ",
        s="9フィートをメートルに",
        fig=("compare", dict(
            items=[dict(v=2.7, t="最短距離", disp="2.7", unit="m", sub="約9フィート", c=J.ALERT)],
            vmax=10, ref="10 m",
            note="※ 人が両手を広げた幅の、およそ1.5倍")),
    ),

    # ── c709 住民の証言（噂の札）────────────────
    "c709": dict(
        t="住民は、揺れを感じたと話した",
        s="残った棟＝住民の建物（NIST 記録映像）",
        photo=ss.fb("c709"), bias=0.5, side="left", ann_y=340,
        ann=[RUMOR],
    ),

    # ── c710 そこから出た説 ──────────────────
    "c710": dict(
        t="工事の振動が、傷めたのではないか",
        s="噂から出た説",
        fig=("panel", dict(
            lead="■ 言われていること",
            blocks=[dict(k="噂", t="隣の工事の振動が原因？", c=J.LINE)],
            cols=1, note="※ ここは噂。このあと NIST の解析で答える")),   # 「次のカット」は制作の用語
    ),

    # ── c711 土と構造の解析モデル ───────────────
    "c711": dict(
        t="噂を、計算で確かめた",
        s="解析モデル（p185）",
        photo=ss.P185, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P185, 0.28, 0.48, 1.25),
        ann=[dict(t="Soil-Structure Interaction", d="地面と建物を一緒に解く", dc=J.INST, ds=30)],
    ),

    # ── c712 層の分解図 ───────────────────
    "c712": dict(
        t="骨組み・地下・基礎・地盤に分けた",
        s="層の分解（p185）",
        photo=ss.P185, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P185, 0.28, 0.52, 1.7),
        ann=[dict(t="superstructure", d="上の骨組み", dc=J.LINE, ds=28),
             dict(t="basement / foundations", d="地下・基礎", dc=J.LINE, ds=28),
             dict(t="soil-rock", d="地盤", dc=J.LINE, ds=28)],
    ),

    # ── c713 現場の計測 ─────────────────
    "c713": dict(
        t="地盤の性質が、計算に入っている",
        s="現場の計測（NIST 記録映像）",
        photo=ss.fb("c713"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="伝わり方", d="地盤で、伝わり方が別物になる", dc=J.LINE, ds=30)],
    ),

    # ── c714 1つめの結論 ─────────────────
    "c714": dict(
        t="答えは、3つ",
        s="p185 の右の箇条　1つめ",
        photo=ss.P185, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P185, 0.83, 0.60, 2.2),
        ann=[dict(t="1", d="振動の減り方", dc=J.INK_W, ds=32)],
    ),

    # ── c715 basement・substructure の層に寄る ────────
    "c715": dict(
        t="地下と鋼の壁が、振動を減らした",
        s="左の3Dの地下と基礎（p185）",
        photo=ss.P185, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P185, 0.30, 0.62, 2.3),
        ann=[dict(t="south basement", d="建物の南側の地下", dc=J.OK, ds=30),
             dict(t="sheet pile wall", d="鋼の板でできた壁", dc=J.OK, ds=30)],
    ),

    # ── c716 2つめの結論 ─────────────────
    "c716": dict(
        t="届いた振動の大きさを、計算した",
        s="p185 の右の箇条　2つめ",
        photo=ss.P185, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P185, 0.83, 0.72, 2.4),
        ann=[dict(t="2", d="つなぎ目に届いた振動の大きさ", dc=J.INK_W, ds=32)],
    ),

    # ── c717 ★決め所「傷んだつなぎ目を壊すにも、小さすぎた」──────
    "c717": dict(
        t="届いた振動は、壊す大きさではない",
        s="p185 の2つめの文",
        fig=("quote", dict(
            phrase="傷んだつなぎ目を壊すにも、小さすぎた",
            rows=[("誰が", "NIST（土と構造の解析）", J.INST),
                  ("いつ", "2026年6月22日 公表", J.LINE),
                  ("どこに", "技術的知見 スライド185", J.DOC)],
            ctx="原文 Computed vibrations at critical slab-column connections of CTS were too small to damage even the distressed connections.",
            paper=True)),
    ),

    # ── c718 3項目の引き（3つめを明るく）────────────
    "c718": dict(
        t="みっつめが、いちばん大事",
        s="p185 の右の3項目",
        photo=ss.P185, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P185, 0.83, 0.74, 1.6),
        ann=[dict(t="1・2", d="減り方・大きさ", dc=J.TICK, ds=30),
             dict(t="3", d="住民の体感について", dc=J.INK_W, ds=34)],
    ),

    # ── c719 3つめの文の寄り ─────────────────
    "c719": dict(
        t="住民の体感を、解析が裏付けた",
        s="p185 の3つめの文",
        photo=ss.P185, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P185, 0.83, 0.87, 2.6),
        ann=[dict(t="原文", d="Analyses corroborate reports …", dc=J.INK_W, ds=30)],
    ),

    # ── c720 感じる大きさと壊れる大きさ ───────────
    "c720": dict(
        t="感じる大きさは、壊す大きさのはるか下",
        s="人と建物のしきい値（p185）",
        fig=("compare", dict(
            items=[dict(v=1, t="人が感じ取れる振動", disp="低い", unit="", c=J.LINE),
                   dict(v=2, t="建物を壊す振動", disp="はるかに上", unit="", c=J.ALERT)],
            bar=False, note="原文 well below levels that would damage the structure")),
    ),

    # ── c721 この答えの形 ─────────────────
    "c721": dict(
        t="感じたことと、原因であることは別",
        s="この答えの形",
        fig=("absent", dict(
            mode="pair", lead="住民の証言は",
            items=[dict(t="うそ・思い違い", d="ではない", ok=False, c=J.LINE),
                   dict(t="本当に感じた", d="ただし、原因ではない", ok=True, c=J.OK)])),
    ),

    # ── c722 ★決め所「大きく寄与してはいない」───────────
    "c722": dict(
        t="こうした説を、1枚にまとめて",
        s="p189 の見出し",
        fig=("quote", dict(
            phrase="大きく寄与してはいない",
            rows=[("誰が", "NIST", J.INST),
                  ("いつ", "2026年6月22日 公表", J.LINE),
                  ("どこに", "技術的知見 スライド189 の見出し", J.DOC)],
            ctx="原文 Things that did not contribute significantly to the collapse",
            paper=True)),
    ),

    # ── c723 5項目（前半）─────────────────
    "c723": dict(
        t="並んでいるのは、5つ",
        s="p189 の一覧　1〜2",
        fig=("absent", dict(
            mode="ledger", lead="大きく寄与しなかったもの（p189）",
            items=[dict(t="87 Park の工事の振動", d="大きく寄与せず", ok=False, c=J.LINE),
                   dict(t="基礎の破壊・陥没・不同沈下", d="大きく寄与せず", ok=False, c=J.LINE)],
            note="原文は p189 の1〜2項目")),
    ),

    # ── c724 5項目（後半）─────────────────
    "c724": dict(
        t="ハリケーン、衝撃、屋上の工事",
        s="p189 の一覧　3〜5",
        fig=("absent", dict(
            mode="ledger", lead="大きく寄与しなかったもの（p189・続き）",
            items=[dict(t="ハリケーンと高潮", d="大きく寄与せず", ok=False, c=J.LINE),
                   dict(t="衝撃荷重", d="大きく寄与せず", ok=False, c=J.LINE),
                   dict(t="屋上の改修・アンカー工事（進行中）", d="大きく寄与せず", ok=False, c=J.LINE)],
            note="原文は p189 の3〜5項目")),
    ),

    # ── c725 沈下について ─────────────────
    "c725": dict(
        t="地盤の沈下も、この一覧の中",
        s="沈下について（p189）",
        fig=("panel", dict(
            lead="p189 の2番目の項目",
            blocks=[dict(k="陥没", t="sinkholes", c=J.LINE),
                    dict(k="不同沈下", t="differential settlement", c=J.LINE)],
            cols=2, note="どちらも「大きくは効いていない」側に入っている")),
    ),

    # ── c726 外から加えられたものではない ──────────
    "c726": dict(
        t="限界を越えたのは、建物自身のつくり",
        s="現場の引き（NIST ドローン）",
        photo=ss.fb("c726"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="外からの力", d="原因ではない（p189）", dc=J.LINE, ds=32)],
    ),
}
