# -*- coding: utf-8 -*-
"""第2章　霧の夜の出港 c201–c214（14カット）。14本目（セウォル号）。

■ 🔴 2026-09-28（⑤b-1）：13本目（トルコ航空981便）の中身を空にした＝git の `b54ee4f`（`git show b54ee4f:tools/cuts/c2.py`）。
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
    "c201": dict(kind='写真',
               plan='台本の画：実写 Googleアース インチョン港の旅客ターミナル（現在）',
               src='海審 p1008・p1037'),
    "c202": dict(kind='写真',
               plan='台本の画：実写 K1 インチョン港のセウォル号（2014年3月27日・沈没の20日前・PD・額装）',
               src='海審 p1013・p1018'),
    "c203": dict(kind='図解',
               plan='【帯】`c207` の帯の最初の状態（夜の帯・予定だけ）（追補 §4）',
               src='海審 p1026'),
    "c204": dict(kind='図解',
               plan='【人の形】顔の無い同じ形を1つ＝1人で476個・色で分ける（生徒・先生・一般・船で働く人）（追補 §4）｜⚠️ 人の形＝顔の無い同じ形を1つ＝1人で476個（生徒325・先生14・一般104・船で働く人33〈船員15・係8・ほか10〉）。描いた形の数を描く側と同じ関数で数えて記録と照合。亡くなった方の数には使わない（追補 §7-7・ルール §C-1 #59）',
               src='海審 p1038・p1062'),
    "c205": dict(kind='図解',
               plan='【人の形】同じ並びの「一般」を灯す（追補 §4）｜⚠️ 人の形は c204 と同じ並び（追補 §7-7）',
               src='海審 p1062'),
    "c206": dict(kind='図解',
               plan='【人の形】船で働く33人を灯し、内わけの色に分ける（追補 §4）｜⚠️ 人の形は c204 と同じ並び（追補 §7-7）',
               src='海審 p1038〜1039'),
    "c207": dict(kind='図解',
               plan='台本の画：図 霧で遅れた出港（予定 18:30 → 実際 21:05）',
               src='海審 p1008・p1038'),
    "c208": dict(kind='図解',
               plan='【書類】用紙の再現図（報告書に書かれた欄の名だけ）が船から運航管理室へ（追補 §4）',
               src='海審 p1037'),
    "c209": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='海審 p1037'),
    "c210": dict(kind='図解',
               plan='台本の画：図 喫水（船が水に沈んでいる深さ）と満載の線',
               src='海審 p1037〜1038'),
    "c211": dict(kind='図解',
               plan='【図】`c210` の喫水の図に線を2本（追補 §4）',
               src='海審 p1038'),
    "c212": dict(kind='図解',
               plan='【地図】港を出た船から無線の輪（報告の中身は字幕）（追補 §4）',
               src='海審 p1038・p1041'),
    "c213": dict(kind='図解',
               plan='【地図】パルミドを過ぎて南へ（夜の色）（追補 §4）',
               src='海審 p1038'),
    "c214": dict(kind='図解',
               plan='【年表】船の歩みの予告（1994〜2014 の線・日本の区間に色）（追補 §4）',
               src='海審 p1016'),
}

SPEC = {
    # ── 🔴 ⑤b-4（2026-09-29）：地図（drift）＝`cuts/ss.py` の `sewol_map("wide")`（門番 check_drift）──
    # 🔴 インチョン港の寄りの地図は作らない：照合できる記録が無い（p1034 の「7.5マイル」は航路の長さ＝Wikidata の港の点から
    #    パルミドまでの直線 8.1マイルと 8% 食い違う＝門番の許し 5% を越える）→ 広い地図の上で描く（照合＝事故の地点）
    # 出港の報告は無線（VHF）で運航管理室へ（海審 p1038）。報告の数（旅客450・船員24・車150・貨物657トン）は字幕だけ
    "c212": dict(
        t="無線で出港の報告",
        s="4月15日の夜",
        fig=ss.sewol_map("wide", [
            dict(ship=dict(at="incheon", deg=200, t="セウォル号"), move=[dict(kind="ring", at="incheon", r=70)],
                 tag=dict(at="incheon", t="出港の報告（無線）", side="left")),
            dict(tag=dict(at="_r1", t="報告の数は実際と違った", side="right"))],
            recs=["海審 p1038", "海審 p1065"]),
    ),

    # 21時39分 パルミド通過の報告（海審 p1038）→ 夜のあいだ南へ（p1045：옹도 00:35・어청도 02:20・대흑산도 07:00）
    #   パルミドでの針路 210度（裁決 p2040「침로를 210도에」）
    "c213": dict(
        t="パルミドを通って南へ",
        s="4月15日 21時39分",
        fig=ss.sewol_map("wide", [
            dict(ship=dict(at="palmido", deg=210), tag=dict(at="palmido", t="パルミド　21時39分", side="left")),
            dict(move=[dict(kind="path", via=["palmido", "ongdo", "eocheongdo", "heuksando"], sec=3.2)],
                 tag=dict(at="heuksando", t="翌朝 7時ごろ", side="left"))],
            recs=["海審 p1038", "海審 p1045", "裁決 p2040", "海審 p1065"]),
    ),

    # ── 🔴 ⑤b-5（2026-09-29）：軸の型＝`tools/axis.py`（門番 check_axis）──
    # 出港の夜の帯（c203 の予定 → c207 の実際）。予定＝海審 p1026（火・木 18時30分にインチョン港→翌 9時10分ごろチェジュ港）
    "c203": dict(
        t="インチョン発・チェジュ行き",
        s="いつもの運航",
        fig=("axis", dict(ss.AX_NIGHT,
                          steps=[dict(add=[ss.ax("dep_plan"), ss.ax("arr_plan"), ss.ax("plan")], cur="18:30"),
                                 dict(), dict()],
                          note="週2往復の運航の予定", src=ss.src(["海審 p1026"]))),
    ),

    # 4月15日の夜。出港＝21時5分ごろ（海審 p1038）＝予定より2時間35分遅れ（数は字幕）
    "c207": dict(
        t="4月15日の夜",
        s="予定と実際",
        fig=("axis", dict(ss.AX_NIGHT,
                          past=[ss.ax("dep_plan"), ss.ax("arr_plan"), ss.ax("plan")],
                          steps=[dict(add=dict(k="pt", at="21:05", t="出港", rec="海審 p1038", big=True), cur="21:05"),
                                 dict(add=dict(k="span", a="18:30", b="21:05", t="遅れ", rec=["海審 p1026", "海審 p1038"],
                                               c="ALERT"))],
                          note="時刻の帯：時刻は報告書", src=ss.src(["海審 p1026", "海審 p1038"]))),
    ),

    # 船の歩みの予告（第3章の年表への入口）。日本の区間＝進水 1994-04-01（p1013）〜導入 2012-10-08（p1016）
    "c214": dict(
        t="この船の歩み",
        s="1994年〜2014年",
        fig=("axis", dict(ss.AX_SHIP,
                          steps=[dict(add=ss.ax("accident"), cur="2014-04-16"), dict(),
                                 dict(add=ss.ax("japan"), cur="1994-04-01")],
                          note="年表：進水から事故まで", src=ss.src(["海審 p1013", "海審 p1016", "海審 p1008"]))),
    ),

    # ── 🔴 ⑤b-6（2026-09-29）：量の型＝`tools/qty.py`（門番 check_qty）・箱の型＝`tools/boxes.py`（門番 check_boxes）──
    # 人の形＝1つ＝1人で476（海審 p1038）。🔴 この3カットだけ（ルール §C-1 #59）＝亡くなった方の数には使わない・
    #   同じ並びを後の章で灰色にしない。3カットとも同じ並び（ss.PEOPLE_ORDER）。数は字幕だけ（凡例は項目名）
    "c204": dict(
        t="乗っていた人",
        s="4月15日 インチョン港",
        fig=("qty", dict(view="people", order=ss.PEOPLE_ORDER, sets=ss.PEOPLE_SETS,
                         steps=[dict(add=[ss.pp("乗客", "LINE"), ss.pp("船で働く人", "DOC")]),
                                dict(add=[ss.pp("生徒", "AMBER", parent="乗客"), ss.pp("先生", "OK", parent="乗客")])],
                         src=ss.src(["海審 p1038", "海審 p1062"]))),
    ),

    # 一般の乗客 104（海審 p1038・表8 p1062）。ほかは沈めた色のまま（同じ並び）
    "c205": dict(
        t="修学旅行のほかに",
        fig=("qty", dict(view="people", order=ss.PEOPLE_ORDER, sets=ss.PEOPLE_SETS,
                         steps=[dict(add=ss.pp("一般の乗客", "LINE")), dict()],
                         src=ss.src(["海審 p1038", "海審 p1062"]))),
    ),

    # 船で働く人 33＝船員15・調理と事務の係8・ほか10（海審 p1038〜1039）
    "c206": dict(
        t="乗組員の内わけ",
        fig=("qty", dict(view="people", order=ss.PEOPLE_ORDER, sets=ss.PEOPLE_SETS,
                         steps=[dict(add=ss.pp("船で働く人", "DOC")),
                                dict(add=[ss.pp("船員", "INK_W", parent="船で働く人"),
                                          ss.pp("調理・事務の係", "INST", parent="船で働く人")]),
                                dict(add=ss.pp("ほか（アルバイトなど）", "OK", parent="船で働く人"))],
                         src=ss.src(["海審 p1038・p1039"]))),
    ),

    # 書類の再現図＝欄の名は報告書の文にあるものだけ（海審 p1037「승선인원, 화물량 등이 기재되어 있지 않았다」）。
    #   空の欄は次の決め所 c209「未記入」の前触れ（欄に値を書かない）。船→運航管理室へ（動かさず矢印で）
    "c208": dict(
        t="出港の前の書類",
        s="4月15日 17時ごろ",
        fig=("boxes", dict(view="form", form=ss.FORM_PRE,
                           steps=[dict(add=[dict(k="end", id="ship"), dict(k="paper"), dict(k="edge", fr="ship", to="paper")]),
                                  dict(add=[dict(k="end", id="office"), dict(k="edge", fr="paper", to="office")])],
                           note="書類の形は再現（欄の名は報告書の文にあるものだけ）", src=ss.src(["海審 p1037"]))),
    ),
}
