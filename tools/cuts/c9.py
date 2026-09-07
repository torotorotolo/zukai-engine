# -*- coding: utf-8 -*-
"""第9章　そのあと c901–c917（17カット・169秒）。

■ この章の役目
  **追うのは、条文そのもの。🔴 ここで通説を1つ、こちらから壊す。**
  通説＝「これ以後、制御棒1本で臨界にできる炉は禁じられた」。
  当たれる一次資料を全部当たったが、**その形の規則は見つからなかった**。
  決め所は c909「断定的に、こう述べたい」と c915「止めた炉で棒を扱う危険」。

■ 出どころ
  AEC 調査委員会報告（1961年6月・43ページ・全文検索で `single control rod` 0件）／
  ANL-6692 印字 p.35〜36（§VIII-F「単一の誤り、という基準」）／
  36 FR 3258（1971年2月20日・一般設計基準 25・26）／
  DOE 公式史 *Proving the Principle* 第16章 p.152・注8（原文には当たれていない）。

■ ⚠️ 「規則になった」と言わない。**近いが、別だ**（c917）。
"""
import jiko_style as J
import cuts.ss as ss

SPEC = {

    # ── c901 よく言われること ─────────────────────────
    "c901": dict(
        t="よく、こう言われている",
        s="跡地に残った管理棟 ARA-613",
        photo=ss.HAER_15, bias=0.5, side="right", ann_y=340,
        ann=[dict(t="通説", d="よく聞く言い方（出どころは不明）",
                  dc=J.LINE, ds=26)],
    ),

    # ── c902 当たれるものを全部当たった ───────────────────
    "c902": dict(
        t="資料を、4つ当たった",
        s="この章で当たった一次資料",
        fig=("process", dict(
            steps=[dict(t="1", d="AEC 調査委員会報告（1961年6月）", c=J.DOC),
                   dict(t="2", d="AEC 委員の議会での発言（1961年6月）",
                        c=J.DOC),
                   dict(t="3", d="ANL-6692（1962年11月）", c=J.DOC),
                   dict(t="4", d="官報（1971年2月20日）", c=J.INST)],
            note="この4件を、1つずつ見る")),
    ),

    # ── c903 調査委員会の報告 ─────────────────────────
    "c903": dict(
        t="まず、原因を扱った報告書",
        s="原因を扱った報告書の表紙",
        # 🔴 報告書の**本文ページ**なので暗幕を敷く（紙いちめんの英字の上に日本語が載るため）。濃さは `check_veil.py` の実測（この3ページは 0.79〜0.83 が必要）→ 0.84
        veil=0.84,
        photo=ss.AEC_COVER, side="left", ann_y=330,
        **ss.focus(ss.AEC_COVER, 0.50, 0.29, 1.85),
        ann=[dict(t="調べ方", d="全文を機械で調べた", dc=J.DOC, ds=32)],
    ),

    # ── c904 「1本の制御棒」は0件 ────────────────────────
    "c904": dict(
        t="「1本の制御棒」は、0件だった",
        s="43ページの全文検索の結果",
        fig=("absent", dict(
            mode="single", lead="この43ページに書かれていないもの",
            items=[dict(t="single control rod", d="0件", ok=False,
                        c=J.ALERT)],
            note="出典：AEC 調査委員会報告（1961年6月）")),
    ),

    # ── c905 AEC 委員の発言 ──────────────────────────
    # 実写 Ph3 #115（試験場の遠景）
    "c905": dict(
        t="次に、議会で述べたという記録",
        s="国立原子炉試験場（記録映画 Phase III）",
        photo=ss.fb("c905"), bias=0.5, side="right", ann_y=330,
        ann=[dict(t="述べたとされる人", d="AEC の委員",
                  dc=J.INST, ds=30),
             dict(t="載っているところ", d="DOE 公式史 第16章 p.152",
                  dc=J.DOC, ds=28)],
    ),

    # ── c906 出どころは書簡 ──────────────────────────
    "c906": dict(
        t="出どころは、1通の書簡である",
        s="公式史 第16章 p.152・注8（p.300）",
        fig=("panel", dict(
            lead="この記述の出どころ",
            blocks=[dict(k="日付", t="書簡（1961-06-01 付）", c=J.DOC),
                    dict(k="所蔵", t="アイダホ州歴史協会", c=J.INST),
                    dict(k="この動画", t="原文には当たれなかった", c=J.ALERT)],
            cols=3)),
    ),

    # ── c907 言えるのはここまで ────────────────────────
    "c907": dict(
        t="言えるのは、ここまでである",
        s="この動画が引ける範囲（同 注8）",
        fig=("absent", dict(
            mode="single", lead="この資料から言えること",
            items=[dict(t="規則そのもの", d="まだ出てこない", ok=False,
                        c=J.ALERT)],
            note="出典：同 注8（p.300）")),
    ),

    # ── c908 ANL-6692 ───────────────────────────
    "c908": dict(
        t="1962年11月の、振り返りの一冊",
        s="ANL-6692　1962年11月・54ページ",
        # 🔴 報告書の**本文ページ**なので暗幕を敷く（紙いちめんの英字の上に日本語が載るため）。濃さは `check_veil.py` の実測（この3ページは 0.79〜0.83 が必要）→ 0.84
        veil=0.84,
        photo=ss.ANL_COVER, side="left", ann_y=330,
        **ss.focus(ss.ANL_COVER, 0.50, 0.36, 1.90),
        ann=[dict(t="出したところ", d="アルゴンヌ国立研究所", dc=J.INST,
                  ds=30),
             dict(t="中身", d="ALPR（SL-1）の設計を振り返る検討報告書",
                  dc=J.DOC, ds=28)],
    ),

    # ── c909 ★決め所「断定的に、こう述べたい」─────────────
    "c909": dict(
        t="第8章に、F という節がある",
        s="単一の誤り、という基準（印字 p.35〜36）",
        photo=ss.ANL_VF, **ss.text_focus(ss.ANL_VF, 0.210),
        fig=("quote", dict(
            phrase="断定的に、こう述べたい",
            rows=[("書いたのは", "アルゴンヌ国立研究所", J.INST),
                  ("いつ", "1962年11月", J.LINE),
                  ("どこに", "ANL-6692 印字 p.36 §VIII-F", J.DOC)],
            ctx="原文 It would be tempting to state categorically that no "
                "future reactor design should be accepted if ...",
            paper=True)),
    ),

    # ── c910 言いたい内容 ────────────────────────────
    "c910": dict(
        t="1本で超臨界になる設計は認めない",
        s="ANL-6692 印字 p.36　言い切りたかった内容",
        fig=("panel", dict(
            lead="言い切りたかったこと",
            blocks=[dict(k="内容", t="今後の設計で、認めないこと", c=J.ALERT),
                    dict(k="ただし", t="だが、と続く", c=J.LINE)],
            cols=2, note="超臨界＝反応が増え続ける状態")),
    ),

    # ── c911 見送った理由 ────────────────────────────
    "c911": dict(
        t="避けると、別のところが悪くなる",
        s="ANL-6692 印字 p.36　見送った理由",
        fig=("panel", dict(
            lead="言い切らなかった理由",
            blocks=[dict(k="1", t="ほかの点で、設計が悪くなる", c=J.LINE),
                    dict(k="2", t="折り合いは、設計者が決める", c=J.INST)],
            cols=2)),
    ),

    # ── c912 新品の炉でも起きえた ──────────────────────
    # 実写 Ph3 #257（顕微鏡での分析）
    "c912": dict(
        t="1年10か月、条文は無い",
        s="工場での分析（記録映画 Phase III）",
        photo=ss.fb("c912"), bias=0.5, side="right", ann_y=330,
        ann=[dict(t="同じ節が書いていること",
                  d="新品の炉：中央の棒を抜けば超臨界",
                  dc=J.ALERT, ds=26),
             dict(t="事故から", v="1年10か月", d="条文：まだ無い",
                  vc=J.INK_W, vs=88, dc=J.LINE, ds=26)],
    ),

    # ── c913 引き抜きの速さ ──────────────────────────
    "c913": dict(
        t="同じ節に、いちばん鋭い数字がある",
        s="ANL-6692 印字 p.36　減速比の話",
        # 🔴 報告書の**本文ページ**なので暗幕を敷く（紙いちめんの英字の上に日本語が載るため）。濃さは `check_veil.py` の実測（この3ページは 0.79〜0.83 が必要）→ 0.84
        veil=0.84,
        photo=ss.ANL_VF, side="left", ann_y=330,
        **ss.text_focus(ss.ANL_VF, 0.451),
        ann=[dict(t="何の話か", d="歯棒と歯車の減速比", dc=J.LINE, ds=32),
             dict(t="決めているもの", d="反応度が入る速さの上限", dc=J.DOC, ds=30)],
    ),

    # ── c914 毎秒0.01% ─────────────────────────────
    "c914": dict(
        t="歯車が、速さの上限を決める",
        s="ANL-6692 印字 p.36　単位は毎秒の%",
        fig=("compare", dict(
            items=[dict(v=0.01, t="駆動装置で入る速さ", disp="0.01",
                        unit="%/秒", sub="歯車で決めてある", c=J.OK),
                   dict(v=20, t="手で速く引いた場合", disp="20", unit="%/秒",
                        sub="見積り", c=J.ALERT)],
            vmax=20, note="反応度が入る速さの上限")),
    ),

    # ── c915 ★決め所「止めた炉で棒を扱う危険」──────────────
    "c915": dict(
        t="差は、2000倍になりうる",
        s="ANL-6692 印字 p.36　§VIII-F",
        photo=ss.ANL_VF, **ss.text_focus(ss.ANL_VF, 0.45),
        fig=("quote", dict(
            phrase="止めた炉で棒を扱う危険",
            rows=[("何の差か", "毎秒0.01% と 毎秒20%（2000倍）", J.ALERT),
                  ("どんなときか", "駆動を外し、人が手で速く引いたら", J.LINE),
                  ("どこに", "ANL-6692 印字 p.36", J.DOC)],
            ctx="原文 This result dramatically illustrated a possible "
                "hazard of rod handling in a shutdown reactor",
            paper=True)),
    ),

    # ── c916 官報 1971年2月20日 ────────────────────────
    "c916": dict(
        t="条文は1971年2月20日である",
        s="官報 36 FR 3258　一般設計基準 25・26",
        # 🔴 報告書の**本文ページ**なので暗幕を敷く（紙いちめんの英字の上に日本語が載るため）。濃さは `check_veil.py` の実測（この3ページは 0.79〜0.83 が必要）→ 0.84
        veil=0.84,
        photo=ss.FR_GDC, side="right", ann_y=330,
        **ss.text_focus(ss.FR_GDC, 0.547),
        ann=[dict(t="25番", d="Criterion 25（原文の見出し）",
                  dc=J.INST, ds=26),
             dict(t="どこに", d="10 CFR 50 付録A", dc=J.DOC, ds=30)],
    ),

    # ── c917 近いが、別だ ────────────────────────────
    "c917": dict(
        t="近いが、別のことを言っている",
        s="跡地の遠景　管理棟とクレーン",
        photo=ss.HAER_14, bias=0.5, side="left", ann_y=330,
        ann=[dict(t="26番", d="棒の固着を見込んだ余裕",
                  dc=J.INST, ds=26),
             dict(t="どちらも書いていないこと", d="1本での臨界を禁じる条文",
                  dc=J.ALERT, ds=26)],
    ),
}
