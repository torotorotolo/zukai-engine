# -*- coding: utf-8 -*-
"""第6章　鉛 c601–c611（11カット・109秒）。

■ この章の役目
  **追うのは、棺と墓の測定表。ここでは人物の像を出さない。**
  物証は IDO-19302 印字 p.91〜100 と Table 5.1（印字 p.102）。
  決め所は c606「鉛で包み、金属の帯で締めた」。

■ 🔴 素材の実測（⑤b）
  c609「輸送機と車列」は記録映画2本のどちらにも無い。
  **代用せず**、そのカットの出典 p.96 に落とした。
  ⚠️ `SL-1Burial.jpg`（Commons）は台本 §5-1 の4で「中身を確認していない」ため**使わない**。

■ ⚠️ 伏せ字を使わない。報告書の語は原文どおり。像は描かない。
"""
import jiko_style as J
import cuts.ss as ss

SPEC = {

    # ── c601 1月4日の朝 ─────────────────────────────
    # 実写 Ph3 #065（防護服の着脱）。⚠️ 台本は Ph1&2 だが実物は Ph3。
    "c601": dict(
        t="1分で交代しながら作業した",
        s="防護服の着脱（記録映画 Phase III）",
        photo=ss.fb("c601"), bias=0.5, side="right", ann_y=330,
        ann=[dict(t="1月4日 5時30分", d="5人の組が作業に入る", dc=J.INK_W,
                  ds=30),
             dict(t="置いた役", d="記録係と時間係", dc=J.DOC, ds=32),
             dict(t="交代", v="1分", vc=J.ALERT, vs=104)],
    ),

    # ── c602 衣類を外しても下がらない ───────────────────
    "c602": dict(
        t="測った値は、3か所とも高い",
        s="1月4日の測定（p.91）　単位は R/hr",
        fig=("absent", dict(
            mode="ledger", lead="1人目の測定",
            items=[dict(t="体の上", d="100〜200 R/hr", ok=True, c=J.ALERT),
                   dict(t="腕のあたり", d="300 R/hr", ok=True, c=J.ALERT),
                   dict(t="衣類を外したあと", d="目に見えて下がらない",
                        ok=False, c=J.LINE)])),
    ),

    # ── c603 除染は打ち切られた ────────────────────────
    # 実写 Ph3 #232（床の除染）。⚠️ 台本は Ph1&2 だが実物は Ph3。
    "c603": dict(
        t="洗っても落ちず、打ち切った",
        s="除染の作業（記録映画 Phase III）",
        photo=ss.fb("c603"), bias=0.5, side="left", ann_y=330,
        ann=[dict(t="9時30分〜11時30分", d="洗剤を使って洗った",
                  dc=J.LINE, ds=30),
             dict(t="結果", d="落ちない。除染は打ち切り", dc=J.ALERT,
                  ds=32)],
    ),

    # ── c604 回収の完了まで ──────────────────────────
    "c604": dict(
        t="回収の完了は、1月9日だった",
        s="1月9日から13日まで（p.33・p.94）",
        fig=("timeline", dict(
            t0=9.0, t1=13.5, title="単位は日。1961年1月",
            ticks=[(9, "9日"), (11, "11日"), (13, "13日")],
            # ⚠️ 1/9 の旗2本が近く、t2 が 1/10 の旗と 10x15px 重なる。語を詰める
            events=[dict(t=9.03, top="0:45", t2="3人目を降ろす",
                         c=J.ALERT, big=True),
                    dict(t=9.2, top="4:42", t2="回収の完了", c=J.INK_W),
                    dict(t=10, top="1/10", t2="鉛の容器へ", c=J.DOC),
                    dict(t=13, top="1/13", t2="埋葬のために整える",
                         c=J.DOC, big=True)])),
    ),

    # ── c605 鉛を張った容器 ──────────────────────────
    "c605": dict(
        t="4インチの鉛を張った容器へ",
        s="1月10日の測定（p.94・p.96）　単位は R/hr",
        fig=("absent", dict(
            mode="ledger", lead="容器に接して測った値",
            items=[dict(t="頭", d="30 R/hr", ok=True, c=J.ALERT),
                   dict(t="胸", d="50 R/hr", ok=True, c=J.ALERT)],
            note="容器の鉛の厚さは4インチ")),
    ),

    # ── c606 ★決め所「鉛で包み、金属の帯で締めた」───────────
    "c606": dict(
        t="手順が、1行ずつ書いてある",
        s="埋葬のために整えた手順（印字 p.95）",
        photo=ss.IDO_P95, **ss.text_focus(ss.IDO_P95, 0.149, 1.35),
        fig=("quote", dict(
            phrase="鉛で包み、帯で締めた",
            rows=[("やったのは", "8人の組", J.INK_W),
                  ("いつ", "1961年1月13日の朝", J.LINE),
                  ("どこに", "IDO-19302 印字 p.95", J.DOC)],
            ctx="原文 wrapped in 1/8 inch lead sheeting ... banded with "
                "metal straps and placed in a casket",
            paper=True)),
    ),

    # ── c607 使った鉛の重さ ──────────────────────────
    "c607": dict(
        t="重さは、3人で違っている",
        s="Table 5.1（印字 p.102）　単位はポンド",
        fig=("compare", dict(
            items=[dict(v=450, t="1人目", disp="450", unit="lb", c=J.AMBER),
                   dict(v=650, t="2人目", disp="650", unit="lb", c=J.AMBER),
                   dict(v=750, t="3人目", disp="750", unit="lb",
                        sub="板は 3/4 インチ", c=J.ALERT)],
            vmax=750, note="1人目と2人目の板は 1/8 インチ")),
    ),

    # ── c608 棺に入れた2枚の札 ────────────────────────
    "c608": dict(
        t="入れられたのは、注意の札だ",
        s="模式図　入れられた札（p.95〜96 の記述から）",
        fig=("panel", dict(
            lead="棺の中に入れられたもの",
            blocks=[dict(k="1", t="注意、高線量区域", c=J.ALERT),
                    dict(k="2", t="注意、放射性物質", c=J.ALERT)],
            cols=2,
            note="原文は Caution - High Radiation Area ／ "
                 "Caution - Radioactive Materials")),
    ),

    # ── c609 1月22日の輸送 ──────────────────────────
    # 🔴 台本「実写 Ph1&2（輸送機と車列）」は素材に無い。出典 p.96 を出す。
    "c609": dict(
        t="1月22日、3人は別々に運ばれた",
        s="輸送の記述（印字 p.96）",
        photo=ss.IDO_P96, side="right", ann_y=330,
        **ss.text_focus(ss.IDO_P96, 0.294, 1.35),
        ann=[dict(t="空軍機", v="2人", d="東海岸の2か所",
                  vc=J.INK_W, vs=96, dc=J.LINE, ds=28),
             dict(t="海軍機", v="1人", d="ミシガンへ", vc=J.INK_W, vs=96,
                  dc=J.LINE, ds=28)],
    ),

    # ── c610 キングストンの墓地 ────────────────────────
    "c610": dict(
        t="棺を出して並べてほしい、と",
        s="キングストンでの記述（印字 p.100）",
        photo=ss.IDO_P100, side="left", ann_y=330,
        **ss.text_focus(ss.IDO_P100, 0.283, 1.35),
        ann=[dict(t="求められたこと", d="墓地からの求め",
                  dc=J.LINE, ds=30),
             dict(t="報告書の書き方", d="軍の形式で並べられた", dc=J.DOC,
                  ds=30)],
    ),

    # ── c611 3つの墓 ───────────────────────────────
    "c611": dict(
        t="底と横と上を、固めてある",
        s="模式図　墓の作り（p.98・p.100 の記述から）　単位は in／ft",
        fig=("compare", dict(
            items=[dict(v=18, t="下", disp="18", unit="in", c=J.LINE),
                   dict(v=24, t="横", disp="2", unit="ft",
                        sub="24インチ", c=J.LINE),
                   dict(v=20, t="上", disp="20", unit="in", c=J.LINE)],
            vmax=24, note="深さは、ひとつが 10 ft")),
    ),
}
