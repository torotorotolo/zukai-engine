# -*- coding: utf-8 -*-
"""エピローグ 余裕 ep01–ep16（16カット）。

■ この章の役目
  **追うのは、Closing Remarks の1枚（p191）。**決め所は ep11「余裕は決定的に小さかった」。
  ⚠️ 結論5点の「建設時点から余裕が小さかった」は5点全部にかからない＝波括弧は左2つだけ（p191・p86）。

■ 出どころ
  技術的知見 p16・p86・p191・section 2／NIST ニュース 2026-08-13（次の諮問委員会）／B-Roll #1。
"""
import jiko_style as J
import cuts.ss as ss

SPEC = {

    # ── ep01 最後の1枚 ───────────────────
    "ep01": dict(
        t="最後の1枚は、結びの言葉",
        s="Closing Remarks（p191）",
        photo=ss.P191, panel=True, pw=1500,
    ),

    # ── ep02 左から順に ───────────────────
    "ep02": dict(
        t="設計の耐力不足と、施工の逸脱",
        s="5つの箱　左の2つ（p191）",
        photo=ss.P191, side="right", ann_y=330,
        **ss.focus(ss.P191, 0.22, 0.40, 2.2),
        # ⚠️ EP-02/G-09：d が箱の英文の丸写しで、その英文の真上に載っていた
        ann=[dict(t="1", d="図面どおりでも、耐力が足りない", dc=J.ALERT, ds=30),
             dict(t="2", d="図面どおりには造られていない", dc=J.ALERT, ds=30)],
    ),

    # ── ep03 右の3つ ────────────────────
    "ep03": dict(
        t="プランター、盛土と舗装、劣化",
        s="5つの箱　右の3つ（p191）",
        photo=ss.P191, side="left", ann_y=330,
        **ss.focus(ss.P191, 0.78, 0.40, 2.2),
        # ⚠️ EP-05/G-09：d が箱の英文の丸写し（"Added fill and paving" は同じ英文の真上）
        ann=[dict(t="3", d="土と植木が、重く広く", dc=J.AMBER, ds=28),
             dict(t="4", d="上に土と舗装を足した", dc=J.AMBER, ds=28),
             dict(t="5", d="年月による傷み", dc=J.AMBER, ds=28)],
    ),

    # ── ep04 最大・広範の札 ───────────────
    "ep04": dict(
        t="1つめには「最大」と「広範」",
        s="箱に書き添えられた言葉（p191）",
        photo=ss.P191, side="right", ann_y=330,
        **ss.focus(ss.P191, 0.20, 0.42, 2.6),
        # ⚠️ EP-06/G-09：t が箱の英文の丸写し。指しているのは**左の箱1**なので side も左へ
        ann=[dict(t="1つめに添えられた語", d="最大、そして広い範囲", dc=J.ALERT, ds=30),
             dict(t="2つめにも同じ語", d="広い範囲（pervasive）", dc=J.ALERT, ds=30)],
    ),

    # ── ep05 波括弧 ──────────────────
    "ep05": dict(
        t="括弧の中は、左の2つだけ",
        s="p191 の波括弧",
        photo=ss.P191, side="right", ann_y=330,
        **ss.focus(ss.P191, 0.28, 0.62, 2.2),
        ann=[dict(t="括弧", d="下から、左の2つをくくる", dc=J.ALERT, ds=32)],
    ),

    # ── ep06 括弧の意味 ───────────────
    "ep06": dict(
        t="括弧の下に、一文がある",
        s="括弧の意味（p191）",
        fig=("panel", dict(
            lead="括弧がくくっているもの",
            blocks=[dict(k="上", t="設計の耐力不足＋施工の逸脱", c=J.ALERT),
                    dict(k="下", t="その結果を言う一文", c=J.DOC)],
            cols=2)),
    ),

    # ── ep07 一文の前半 ───────────────
    "ep07": dict(
        t="余裕の乏しさの大半は、この2つ",
        s="括弧の下の一文　前半（p191）",
        photo=ss.P191, side="left", ann_y=330,
        **ss.focus(ss.P191, 0.28, 0.78, 2.6),
        # ⚠️ EP-12/G-09：d が画面の同じ一文の写し＝1つの画面に同じ文が大小2回出ていた
        ann=[dict(t="原文の語", d="bulk＝大半", dc=J.INK_W, ds=28)],
    ),

    # ── ep08 余裕とは ─────────────────
    "ep08": dict(
        t="余裕とは、壊れるまでの間",
        s="margins against failure",
        fig=("panel", dict(
            lead="余裕（margin）",
            blocks=[dict(k="何", t="壊れるまでの距離", c=J.INK_W),
                    dict(k="設計", t="余裕を持たせるのが通常", c=J.LINE)],
            cols=2)),
    ),

    # ── ep09 一文の後半 ───────────────
    "ep09": dict(
        t="いつからそうだったか、まで書いてある",
        s="括弧の下の一文　後半（p191）",
        photo=ss.P191, side="right", ann_y=330,
        **ss.focus(ss.P191, 0.32, 0.84, 2.2),
        # ⚠️ EP-14/G-09：d が画面の同じ英文の写し。訳を出す
        ann=[dict(t="原文の訳", d="建設が終わった時点から", dc=J.INK_W, ds=28)],
    ),

    # ── ep10 1981 → 2021 ─────────────
    "ep10": dict(
        t="40年前から、決まっていた",
        s="1981年から2021年まで（p191）",
        fig=("timeline", dict(
            t0=1979, t1=2023, title="単位は年。余裕が小さかったのは、40年のどこかからではない",
            ticks=[(1981, "1981"), (2001, "2001"), (2021, "2021")],
            events=[dict(t=1981, top="建設完了", t2="この時点から、余裕は小さかった", c=J.ALERT, big=True),
                    dict(t=2021, top="崩落", c=J.INK_W)])),
    ),

    # ── ep11 ★決め所「余裕は決定的に小さかった」──────────
    "ep11": dict(
        t="3枚のスライドで繰り返される言葉",
        s="p16・p86・p191 の共通句",
        fig=("quote", dict(
            phrase="余裕は決定的に小さかった",
            rows=[("誰が", "NIST", J.INST),
                  ("いつ", "2026年6月22日 公表", J.LINE),
                  ("どこに", "技術的知見 スライド16・86・191（3枚に出る）", J.DOC)],
            ctx="原文 critically low margins against failure",
            paper=True)),
    ),

    # ── ep12 40年の意味 ───────────────
    "ep12": dict(
        t="40年、まだ落ちていなかっただけ",
        s="40年の意味が変わる",
        fig=("absent", dict(
            mode="pair", lead="この建物の40年",
            items=[dict(t="持ちこたえていた", d="そう読める言い方ではない", ok=False, c=J.LINE),
                   dict(t="まだ落ちていなかった", d="余裕は建設時から小さかった", ok=True, c=J.ALERT)])),
    ),

    # ── ep13 最後の3週間 ───────────────
    "ep13": dict(
        t="人の目に見えたのは、最後の3週間",
        s="3週間前から崩落まで（section 2）",
        fig=("timeline", dict(
            t0=-22, t1=1, title="単位は日。崩落を 0 とする",
            ticks=[(-21, "3週間前"), (-7, "1週間前"), (0, "崩落")],
            events=[dict(t=-21, top="門", t2="開かなくなる", c=J.ALERT, up=True),
                    dict(t=-7, top="水", t2="柱を伝う", c=J.ALERT, up=False),
                    dict(t=-0.7, top="隙間", t2="床に10センチ（17時間前）", c=J.ALERT, up=True),
                    dict(t=0, top="01:22", c=J.INK_W, big=True, up=False)])),
    ),

    # ── ep14 責める話にしない ─────────────
    "ep14": dict(
        t="どれも、修理の話に見えた",
        s="印の受け取られ方（p52・p58）",
        fig=("panel", dict(
            lead="沈んでいる印に見えなかった3つ",
            blocks=[dict(k="門", t="直された（p52）", c=J.LINE),
                    dict(k="水", t="駐車場の水漏れは、よくあること", c=J.LINE),
                    dict(k="隙間", t="床の傷みに見える", c=J.LINE)],
            cols=3, note="NIST は個人の責任を書いていない。この動画も、責める側に立たない")),
    ),

    # ── ep15 まだ出ていない報告書 ───────────
    "ep15": dict(
        t="調査は、終わっていない",
        s="NIST ニュース 2026年8月13日",
        fig=("absent", dict(
            mode="ledger", lead="これから",
            items=[dict(t="最終報告書", d="未刊", ok=False, c=J.ALERT),
                   dict(t="次の諮問委員会", d="2026年9月", ok=True, c=J.INST)],
            note="技術的知見（2026年6月22日）は途中の結論")),
    ),

    # ── ep16 銘板 ─────────────────
    "ep16": dict(
        t="残る問いは、なぜ読めなかったか",
        s="建物の銘板（NIST 記録映像の1コマ）",
        photo=ss.S_SIGN, side="left", ann_y=340, bias=0.5, xbias=0.6, zoom=1.2,
        ann=[dict(t="分かったこと", d="崩れた理由", dc=J.OK, ds=32),
             dict(t="分かっていないこと", d="誰にも読めなかった理由", dc=J.ALERT, ds=32)],
    ),
}
