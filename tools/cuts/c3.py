# -*- coding: utf-8 -*-
"""第3章　日本で生まれた船 c301–c312（12カット）。14本目（セウォル号）。

■ 🔴 2026-09-28（⑤b-1）：13本目（トルコ航空981便）の中身を空にした＝git の `b54ee4f`（`git show b54ee4f:tools/cuts/c3.py`）。
  ⚠️ 第10〜13章（ca〜cd）は14本目で初めてのファイル（13本目までは9章）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep14/make_plan.py` で
  台本 §4・承認ずみの絵コンテ（映像方針 §2-2・§4）・追補 §4・§7 から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2〜⑤b-7 で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝⑤b-7 の門番 check_text_screens が「文字だけ2割まで・3カット以上続けない」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所（ルール §5b-79）
  記号＝【案C】再現イラスト（置き場 A〜E）・【F】断面F・【地図】drift・【年表】【帯】【棒】【マス】【人の形】【書類】【流れ】【並べ】（追補 §3）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    "c301": dict(kind='写真',
               plan='台本の画：実写 J1 鹿児島港の「フェリーなみのうえ」（2010年2月14日・写真の説明による・CC BY-SA 2.0・額装）',
               src='海審 p1016'),
    "c302": dict(kind='図解',
               plan='【年表】1994 の点（追補 §4）',
               src='海審 p1013'),
    "c303": dict(kind='図解',
               plan='【年表】1994〜2012 の区間（追補 §4）',
               src='海審 p1016'),
    "c304": dict(kind='図解',
               plan='台本の画：図 年表（1994 進水 → 2012 韓国へ → 2013 客を乗せ始める → 2014 事故）',
               src='海審 p1013・p1016・p1026'),
    "c305": dict(kind='図解',
               plan='【地図】インチョン港に印（追補 §4）',
               src='海審 p1016'),
    "c306": dict(kind='写真',
               plan='台本の画：実写 K1（額装・船首の「SEWOL 세월」の文字に枠・2014年3月27日・PD）',
               src='海審 p1026'),
    "c307": dict(kind='図解',
               plan='【地図】航路を往復する船の点（追補 §4）',
               src='海審 p1026'),
    "c308": dict(kind='文字の頁',
               plan='台本の画：図 p1016（海審の9頁・「나미노우에호」の記述）',
               src='海審 p1013・p1016・p1026'),
    "c309": dict(kind='図解',
               plan='台本の画：図 船の横から見た形（5階＝船橋の甲板・4階＝A甲板・3階＝B甲板・その下＝C〜E甲板）',
               src='海審 p1018・p1019・裁決 p2008'),
    "c310": dict(kind='図解',
               plan='台本の画：図 5階＝船橋の甲板（操舵室・1等客室・ロビー・展示室）',
               src='海審 p1018・裁決 p2008'),
    "c311": dict(kind='図解',
               plan='台本の画：図 救命いかだ44個・シューター4つ',
               src='海審 p1018'),
    "c312": dict(kind='図解',
               plan='【年表】2012-10-08→10-12→2013-02-12（追補 §4）',
               src='海審 p1016'),
}

SPEC = {
    # ── 🔴 ⑤b-4（2026-09-29）：地図（drift）＝`cuts/ss.py` の `sewol_map("wide")`（門番 check_drift）──
    # 2012-10-22 インチョンを本籍の港に登録（海審 p1016 2.2.2）
    "c305": dict(
        t="セウォル号として登録",
        s="2012年10月22日",
        fig=ss.sewol_map("wide", [
            dict(),
            dict(ship=dict(at="incheon", deg=180, t="セウォル号")),
            dict(move=[dict(kind="ring", at="incheon", r=70)], tag=dict(at="incheon", t="本籍の港", side="left"))],
            recs=["海審 p1016", "海審 p1065"]),
    ),

    # 2013年3月からインチョン〜チェジュを定期に運航（海審 p1024 2.4.9）＝航路を往復する点
    "c307": dict(
        t="インチョンとチェジュを往復",
        s="2013年3月から",
        fig=ss.sewol_map("wide", [
            dict(tag=dict(at="_l1", t="約1年1か月", side="left")),
            dict(move=[dict(kind="path", sec=2.0,
                            via=ss.ROUTE[:6] + ["chujado", "jeju", "chujado"] + ss.ROUTE[5::-1])])],
            recs=["海審 p1024", "海審 p1034", "海審 p1065"]),
    ),

    # ── 🔴 ⑤b-5（2026-09-29）：軸の型＝`tools/axis.py`（門番 check_axis）──
    # 造った年（1994年1月25日に竜骨を据え・4月1日に進水＝海審 p1013）。2つの点が近いので月の寄りの年表で
    "c302": dict(
        t="日本の造船所で",
        s="林兼造船",
        fig=("axis", dict(ss.AX_BUILD,
                          steps=[dict(), dict(add=[ss.ax("keel"), ss.ax("launch", big=True)], cur="1994-04-01"), dict()],
                          note="年表：工事の始まり＝竜骨（船の背骨）を据えた日", src=ss.src(["海審 p1013"]))),
    ),

    # 日本での18年（マルエーフェリーの「なみのうえ」＝海審 p1016）。区間の名は船の名だけ（会社と航路は字幕）
    "c303": dict(
        t="日本の船だった時代",
        s="九州・沖縄の航路",
        fig=("axis", dict(ss.AX_SHIP,
                          past=[ss.ax("launch"), ss.ax("accident", t="", lab=False)],
                          steps=[dict(add=ss.ax("naminoue"), cur="2012-10-08"), dict()],
                          note="年表：日本の会社が使った期間", src=ss.src(["海審 p1013", "海審 p1016"]))),
    ),

    # 2012年10月8日に日本から導入（海審 p1016）。進水からの長さは括弧（数は字幕）
    "c304": dict(
        t="韓国の会社へ",
        s="韓国の海運会社",
        fig=("axis", dict(ss.AX_SHIP,
                          past=[ss.ax("launch"), ss.ax("japan"), ss.ax("accident", t="", lab=False)],
                          steps=[dict(add=ss.ax("import", big=True), cur="2012-10-08"),
                                 dict(add=dict(k="br", a="1994-04-01", b="2012-10-08", rec=["海審 p1013", "海審 p1016"]))],
                          note="年表：進水から導入まで", src=ss.src(["海審 p1013", "海審 p1016"]))),
    ),

    # 改造（2012-10-12〜2013-02-12・全羅南道ヨンアムの造船所＝海審 p1016）→ 初めての運航 2013-03-16（p1026）
    "c312": dict(
        t="客を乗せる前の工事",
        s="2012年10月〜2013年2月",
        fig=("axis", dict(ss.AX_KAIZO,
                          steps=[dict(add=[ss.ax("import"), ss.ax("first")], cur="2012-10-08"),
                                 dict(add=ss.ax("kaizo"), cur="2013-02-12")],
                          note="年表：月の寄り", src=ss.src(["海審 p1016", "海審 p1026"]))),
    ),

    # ── 🔴 ⑤b-7a（2026-09-29）：写真と頁 ──
    # J1（CC BY-SA 2.0＝額装・無改変・1点1カット）。2010年2月14日・鹿児島港（Commons の撮影日・説明）
    "c301": dict(
        t="日本を走っていたころ",
        s="2010年2月14日の写真",
        photo=P("naminoue_2010"), panel=True, color=1.0,
    ),

    # K1（PD）を船首の文字に寄せる（`trim`＝このカットだけの切り出し・900px の写真＝引き伸ばしは `pw` で 1.4倍まで）。
    #   ⚠️ 枠や印は描かない（写真の上に描く型が無い）＝寄せて見せる
    # ⚠️ 見出しにハングル（세월）を書かない＝見出しの字体 Dela にハングルの字形が無い（門番 layout の豆腐・09-29）
    "c306": dict(
        t="船首の文字",
        s="2014年3月27日（寄り）",
        photo=P("sewol_incheon"), panel=True, trim=(0.33, 0.33, 0.98, 0.83), pw=820,
    ),

    # 報告書 2.2（船の改造と前後の比べ）の頁＝「나미노우에호」（なみのうえ号）が出てくる行を真ん中に（`pages.json` の trim）
    "c308": dict(
        t="船の経歴の節",
        s="日本時代の船名が出てくる",
        photo=ss.page(1016), panel=True, color=1.0,
    ),
}
