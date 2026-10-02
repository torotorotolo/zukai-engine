# -*- coding: utf-8 -*-
"""第4章　約2億立方メートル c401–c423（23カット）。16本目（バイオントダム災害）。

■ 🔴 2026-10-01（⑤b-1）：15本目（リノ・エアレース2011）の中身を空にした＝git の `c646174`（`git show c646174:tools/cuts/c4.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep16/make_plan.py` で
  台本 §4・承認ずみの映像方針（§1-3 冒頭・§3 置き場・§4-2 合図・§5 案C・§6 図表・§8 替える画）から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所（ルール §5b-79）
  記号＝【案C VA】上から見た谷・【案C VB】谷を横切る断面・【案C VC】谷に沿う断面（ダム）・【案C VD】正面から見た斜面（§3）・
        【冒頭】（§1-3）・【線の図】場面1・【帯】場面4 時間の帯・【断面の図解】・【地図】drift（§6）・【混ざり】（§9⑦）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    "c401": dict(kind='図解',
               plan='台本の画：図 年表 専門家の報告（1960-02 人工の揺れで地下を調べる報告・1960-06 2人の地質学者・1961-02-03 ミュラー）（rec= PDF73〜77・S9 PDF6）',
               src='S1 PDF73・PDF148・S9 PDF4'),
    "c402": dict(kind='図解',
               plan='台本の画：図 年表（c401 の図・1960年6月に印）',
               src='S1 PDF73'),
    "c403": dict(kind='図解',
               plan='【断面の図解】断面の図解（模式図）：ダムの断面（寸法）・斜面の目印・2人の見立てと反対の見方・地下を調べる揺れと試しの穴・水理模型・しみこんだ水。VB と同じ地形の線を使う（向きがそろう）（映像方針 §6）｜台本の画：図 断面【横から】 2人の見立て（大昔にすべり落ちた大きな岩の塊・その下の面＝すべり面）（rec= PDF73）',
               src='S1 PDF73'),
    "c404": dict(kind='図解',
               plan='【断面の図解】断面の図解（模式図）：ダムの断面（寸法）・斜面の目印・2人の見立てと反対の見方・地下を調べる揺れと試しの穴・水理模型・しみこんだ水。VB と同じ地形の線を使う（向きがそろう）（映像方針 §6）｜台本の画：図 断面【横から】（c403 の図の横に「岩は元の場所にある」の見方を並べる）（rec= PDF74・PDF174）',
               src='S1 PDF74・PDF174'),
    "c405": dict(kind='図解',
               plan='【断面の図解】断面の図解（模式図）：ダムの断面（寸法）・斜面の目印・2人の見立てと反対の見方・地下を調べる揺れと試しの穴・水理模型・しみこんだ水。VB と同じ地形の線を使う（向きがそろう）（映像方針 §6）｜台本の画：図 断面【横から】（地下を調べる揺れの線と、試しの穴）',
               src='S1 PDF74・PDF76・PDF148・PDF174・S9 PDF6'),
    "c406": dict(kind='再現イラスト',
               plan='【案C VA 上から見た谷】🆕 ⑤b-7（2026-10-02 カズヤくん）：Google Earth → 地図（VA）に替えた＝1960年11月の崩落の'
                    '場所（SPEC は ⑤b-8）｜台本の画：実写 Googleアース③ 残った湖と崩れた山の表面（現在）',
               src='S1 PDF72・PDF75・PDF174'),
    "c407": dict(kind='図解',
               plan='台本の画：図 年表（c401 の図・1961年2月3日に印）',
               src='S1 PDF75・PDF144・S9 PDF4'),
    "c408": dict(kind='再現イラスト',
               plan='【案C VD 正面から見た斜面】亀裂と囲まれた範囲 → 2行目で右上に小さな断面（c403 と同じ線・模式）を出し、亀裂からすべり面の上の端へ線をつなぐ（映像方針 §5）｜🆕 ⑤b-4：「混ざり」から「再現イラスト」へ（門番 check_illu ⑦＝混ざりは全面の絵で書けない・小さな断面は VD の絵の中の枠）｜⚠️ 合図（c405 から）｜合図（映像方針 §4-2 #7・c405 から）：「正面から見ると」・小さな地図',
               src='S1 PDF77'),
    "c409": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='S1 PDF77'),
    "c410": dict(kind='図解',
               plan='台本の画：図 数の比べ 70万m³ と 2億m³（東京ドームで約半分と約160杯）（rec= PDF72・PDF77）',
               src='S1 PDF72・PDF77'),
    "c411": dict(kind='図解',
               plan='【線の図】場面1 水位と斜面の速さの線（型＝線の図）：上下2段（上＝水位・下＝斜面の速さ）・横軸は年月で共通。記録の点だけを結ぶ（点と点の間は模式＝S8 の図6 はなぞらない）・700m の線（模型）・715m の許可。⚠️ 画の欄の「再現イラスト」は図解として作る（「再現イラスト」の札は出さない）（映像方針 §6）｜台本の画：図 再現イラスト 場面1 水位と速さの線（1960〜61年の区間）',
               src='S1 PDF77・PDF175'),
    "c412": dict(kind='文字の頁',
               plan='台本の画：図 p217（少数派の報告がミュラーの報告を引く段・頁ごと）',
               src='S1 PDF77・PDF217'),
    "c413": dict(kind='図解',
               plan='台本の画：図 書類の再現図 ミュラーの報告の一文（少数派の報告が引く形・伊語の原文のまま・日本語は字幕だけ）（rec= PDF217）',
               src='S1 PDF217'),
    "c414": dict(kind='図解',
               plan='【線の図】場面1 水位と斜面の速さの線（型＝線の図）：上下2段（上＝水位・下＝斜面の速さ）・横軸は年月で共通。記録の点だけを結ぶ（点と点の間は模式＝S8 の図6 はなぞらない）・700m の線（模型）・715m の許可。⚠️ 画の欄の「再現イラスト」は図解として作る（「再現イラスト」の札は出さない）（映像方針 §6）｜台本の画：図 再現イラスト 場面1（c411 の線を戻す）',
               src='S1 PDF85・PDF175・S9 PDF4'),
    "c415": dict(kind='写真',
               plan="台本の画：実写 #083 ダムの上から見た湖と南の岸の崩れた跡（1960年11月）｜⚠️ #083 は ⑤b で原寸を見てから（④'・映像方針の申し送り）",
               src='S1 PDF179'),
    "c416": dict(kind='文字の頁',
               plan='台本の画：図 p179（議会の報告 PDF179 の段・頁ごと）',
               src='S1 PDF179'),
    "c417": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='S1 PDF179'),
    "c418": dict(kind='図解',
               plan='台本の画：図 流れ図 報告の行き先（会社 → 国のダム局・県ごとの土木局・国の地方の長官）（rec= PDF179・PDF232）',
               src='S1 PDF179・PDF232'),
    "c419": dict(kind='図解',
               plan='台本の画：図 並べ図 2つの見方（多数派「正式に送られたとは確認できない」・少数派「隠した」）（rec= PDF179・PDF232）',
               src='S1 PDF179・PDF232'),
    "c420": dict(kind='写真',
               plan='台本の画：実写 #079 エルト村（事故の前）',
               src='S1 PDF39・PDF170・PDF220'),
    "c421": dict(kind='図解',
               plan='台本の画：図 年表 メルリンの記事（1959-05-05・1960-11-08・1960-11-30 無罪・1961-02-21）（rec= PDF39）',
               src='S1 PDF39・PDF220・S9 PDF5'),
    "c422": dict(kind='図解',
               plan='台本の画：図 書類の再現図 1961年2月21日の記事の見出し（伊語の原文のまま・日本語は字幕だけ）（rec= PDF39）',
               src='S1 PDF39'),
    "c423": dict(kind='写真',
               plan='台本の画：実写 #089 ダムと湖（事故の前）',
               src='S1 PDF171'),
}

SPEC = {
    # ── 🆕 ⑤b-7（2026-10-02）：写真と頁の束（`qa_out/ep16_assets.py`）──
    # 少数派の報告（p217 左の段）＝ミュラーの報告の一文「Alla domanda se questi franamenti possono venire arrestati mediante
    #   misure artificiali, deve essere risposto negativamente…」をそのまま引く段
    "c412": dict(
        t="少数派の報告の引用",
        s="ミュラーの報告の一文を引く段",
        photo=ss.page(217), trim=ss.ptrim("c412"), panel=True, color=1.0,
    ),
    # #083（1960年11月）＝ダムの上から見た湖と崩れた跡（全体）
    "c415": dict(
        t="崩落のあとの湖",
        s="1960年11月　ダムの上から見た湖と崩れた跡",
        photo=P("slide_19601104"), **ss.kind(P("slide_19601104")),
    ),
    # 多数派の本文（p179 左の段）＝「…Mueller e delle prove su modello idraulico, si è visto che essi erano conosciuti alla
    #   Pubblica Amministrazione, benchè non consti che le relazioni siano state ufficialmente trasmesse…」（c417 の★も同じ段）
    "c416": dict(
        t="多数派の本文",
        s="報告と模型の実験の扱いを書く段",
        photo=ss.page(179), trim=ss.ptrim("c416"), panel=True, color=1.0,
    ),
    # #079（1960年の絵はがき）＝湖とエルトの村（北の岸の村の側＝記者の話）
    "c420": dict(
        t="北の岸の村",
        s="1960年の絵はがき　湖とエルトの村",
        photo=P("erto_1960"), **ss.kind(P("erto_1960")),
    ),
    # #089（1960年）＝天端の道と湖
    "c423": dict(
        t="反対の岸",
        s="1960年　ダムの天端から見た湖",
        photo=P("crest_lake_1960"), **ss.kind(P("crest_lake_1960")),
    ),
    # ── 🆕 ⑤b-6a（2026-10-01）：年表・量・箱（14・15本目の型）──
    # c401（12.06秒）・c402（10.97秒）・c407（7.51秒）＝崩落の前の専門家の報告（揺れの調べ S1 p36〈1960年2月4日〉・2人の地質学者 p73
    #   〈1960年6月〉・ミュラー p76〈1961年2月3日〉）。c401：1行目＝崩落の点（「崩落の前に戻す」）／2行目＝3つの報告（カーソルが前へ戻る）／
    #   3行目＝そのまま。c402＝地質学者の点を大きく＋札（名前・設計者の息子＝S1 p73「quest'ultimo figlio del progettista」）。
    #   c407＝ミュラーの点を大きく＋札「1957年から会社の依頼」（S9 p2004＝1957年8月6日の報告は会社が頼んだ2本目）
    "c401": dict(
        t="崩落の前の調べ", s="会社が頼んだ専門家",
        fig=("axis", dict(**ss.AX_EXP, steps=[
            dict(add=ss.ax("e_fall"), cur="1960-11-04"),
            dict(add=[ss.ax("e_caloi"), ss.ax("e_geo"), ss.ax("e_mul")], cur="1960-02-04"),
            dict()],
            src=ss.src(["S1 p36", "S1 p72", "S1 p73", "S1 p76"]))),
    ),
    "c402": dict(
        t="2人の見立て", s="崩落の前の報告",
        fig=("axis", dict(**ss.AX_EXP, past=[ss.ax("e_caloi"), ss.ax("e_fall"), ss.ax("e_mul")], start=dict(cur="1960-02-04"),
                          steps=[dict(add=ss.ax("e_geo", big=True, chips=["ジュディチ・セメンツァ"]), cur="1960-06"),
                                 dict(),
                                 dict(add=dict(k="chips", at="1960-06", chips=["セメンツァは設計者の息子"], rec="S1 p73", i0=1))],
                          src=ss.src(["S1 p36", "S1 p72", "S1 p73", "S1 p76"]))),
    ),
    "c407": dict(
        t="地盤の専門家", s="オーストリアから",
        fig=("axis", dict(**ss.AX_EXP, past=[ss.ax("e_caloi"), ss.ax("e_geo"), ss.ax("e_fall")], start=dict(cur="1960-11-04"),
                          steps=[dict(add=ss.ax("e_mul", big=True), cur="1961-02-03"),
                                 dict(add=dict(k="chips", at="1961-02-03", chips=["1957年から会社の依頼"],
                                               rec=["S1 p76", "S9 p2004"]))],
                          src=ss.src(["S1 p36", "S1 p72", "S1 p73", "S1 p76", "S9 p2004"]))),
    ),
    # c410（10.25秒）＝ミュラーの見積もり 2億（S1 p77）・崩れた量 70万（p72）・東京ドーム 124万。尺を 2億まで＝崩れた量と東京ドームは
    #   細い線（300倍・160杯の差がそのまま見える）。2〜3行目（聞き役と答え）は足さない
    "c410": dict(
        t="山の斜面ごと", s="ミュラーの見積もり",
        fig=("qty", dict(view="bar", groups=[ss.QG["vol_big"]],
                         steps=[dict(add=[ss.qb("v_fall"), ss.qb("v_dome"), ss.qb("v_mass")]), dict(), dict()],
                         note="東京ドームの容積は124万立方メートル",
                         src=ss.src(["S1 p72", "S1 p77"]) + "・東京ドームの容積（一般の事実）")),
    ),
    # c413（5.48秒）＝ミュラーの一文（少数派の報告が引く形＝S1 p217）：1行目＝紙と「問い」／2行目＝「答え」を書き込む。
    #   欄の字は原文のイタリア語のまま（日本語は字幕だけ＝PLAN）
    "c413": dict(
        t="止められるか", s="イタリア語の原文",
        fig=("boxes", dict(view="form", form=ss.FORM_MUELLER, steps=[
            dict(add=dict(k="paper")), dict(add=dict(k="fill", f="答え"))],
            note="欄の字は原文のまま・様式は再現", src=ss.src(["S1 p217"]))),
    ),
    # c418（13.16秒）＝報告の行き先：1行目（多数派の書き添え）＝会社 → 国の役所・地方の長官・土木局を点線（正式に送られたとは確認
    #   できない＝S1 p179）／2行目（少数派＝隠した・S1 p232）＝会社の下に札／3行目＝3つの報告 → 会社（S1 p232 が挙げる3つ）
    "c418": dict(
        t="報告の行き先", s="多数派と少数派の書き方",
        fig=("boxes", dict(view="flow", layout=ss.FL_HIDE, steps=[
            dict(add=[ss.fl("g_gov"), ss.fl("g_pref"), ss.fl("g_gc"),
                      ss.ce("co", ["g_gov", "g_pref", "g_gc"], style="leader")]),
            dict(add=dict(k="chip", at="co", t="少数派「隠した」", rec="S1 p232", dy=70)),
            dict(add=[ss.fl("r_geo"), ss.fl("r_mul"), ss.fl("r_mod"), ss.ce(["r_geo", "r_mul", "r_mod"], "co")])],
            note="点線＝役所は知っていたが、正式に送られたとは確認できない（多数派）", src=ss.src(["S1 p179", "S1 p232"]))),
    ),
    # c419（5.46秒）＝2つの見方を同じ形で並べる（どちらかに決めない＝並べ図）
    "c419": dict(
        t="割れた見方", s="議会の中の2つの報告",
        fig=("boxes", dict(view="row", slots=2, steps=[dict(add=[ss.cause("majority"), ss.cause("minority")]), dict()],
                           src=ss.src(["S1 p179", "S1 p232"]))),
    ),
    # c421（11.85秒）＝メルリンの記事（S1 p39・S9 p2005・S1 p220）：1行目＝1959年5月の記事／2行目＝札「「うその知らせ」で訴えられる」／
    #   3行目＝1960年11月30日 無罪＋札「ミラノの裁判所」
    "c421": dict(
        t="訴えられた記者", s="北の岸の村の危険",
        fig=("axis", dict(**ss.AX_MERLIN, steps=[
            dict(add=ss.ax("m_art"), cur="1959-05-05"),
            dict(add=dict(k="chips", at="1959-05-05", chips=["「うその知らせ」で訴えられる"],
                          rec=["S1 p39", "S9 p2005", "S1 p220"])),
            dict(add=ss.ax("m_free", chips=["ミラノの裁判所"]), cur="1960-11-30")],
            src=ss.src(["S1 p39", "S1 p220", "S9 p2005"]))),
    ),
    # c422（8.09秒）＝1961年2月21日の記事の見出し（S1 p39）：1行目＝紙／2行目＝見出しを書き込む（原文のイタリア語のまま）
    "c422": dict(
        t="記事の見出し", s="イタリア語の原文",
        fig=("boxes", dict(view="form", form=ss.FORM_UNITA, steps=[
            dict(add=dict(k="paper")), dict(add=dict(k="fill", f="見出し"))],
            note="欄の字は原文のまま・様式は再現", src=ss.src(["S1 p39"]))),
    ),

    # ── 🆕 ⑤b-5（2026-10-01）：場面1 水位と斜面の速さの線（`tools/lv16.py`・1960〜61年の区間＝ミュラーが見た線）──
    # c411（8.58秒）＝1行目（聞き役）は線を戻すだけ／2行目 2.21〜「…湖の水位と雨と斜面の速さの関係をつかめば、」で上がって下がった
    #   区間の水位と速さを太く重ねる（雨は記録の数が無い＝描かない）／3行目 6.58〜「速さを調整できるようになるだろう、と」で止まった点を囲む
    "c411": dict(
        t=ss.LV_T, s="1960〜1963年",
        fig=ss.lv_fig(ss.LV_ALL, past=ss.lv_upto("1961-01-08") + [ss.LV_EV["fall60"]], steps=[
            dict(add=[]),
            dict(add=[dict(k="hl", s="z", a="1960-10-05", b="1961-01-08"), dict(k="hl", s="v", a="1960-10-05", b="1961-01-08")]),
            dict(add=dict(k="ring", s="v", at="1961-01-08"))]),
    ),
    # c414（10.88秒）＝c411 の線を戻す。2行目「…ミュラーと…国の委員の地質学者は、こう見た」で1960年の水ための区間に帯／
    #   3行目「理屈の上では、水をためる試験が、動きを見張って抑える、いちばんの方法だと」で速さの上がり下がりを太く重ねる
    "c414": dict(
        t=ss.LV_T, s="1960〜1963年",
        fig=ss.lv_fig(ss.LV_ALL, past=ss.lv_upto("1961-01-08") + [ss.LV_EV["fall60"]], steps=[
            dict(add=[]),
            dict(add=dict(k="band", s="z", a="1960-03-15", b="1960-11-04", t="水ための試験", rec="S1 p72", c="AMBER")),
            dict(add=dict(k="hl", s="v", a="1960-10-05", b="1961-01-08"))]),
    ),

    # ── 🆕 ⑤b-4（2026-10-01）：断面の図解（`tools/vsec16.py`・VB と同じ線＝左が南・「再現イラスト」の札は出さない）──
    # c403（10.09秒）＝1行目「…大昔に一度すべり落ちてきた」で古い塊（模式）／3行目「その下の面、すべり面が谷のほうへ傾いていれば、
    #   また動き出すおそれ」ですべり面（点線）と動き出す向き（S1 PDF73・PDF174＝ジュディチとセメンツァ 1960年6月）
    "c403": dict(
        t="2人の見立て", s="ジュディチとセメンツァ（1960年6月）",
        fig=("vsec", dict(view="two",
                          # ⚠️ qa_all の echo（札が語りの写し）・dup（断り書きが見出し「2人の見立て」を覆う）＝札は名前だけ・
                          #   断り書きに見出しの言葉を入れない
                          # 試し焼き 36847144315：札に指す線が無かった＝塊とすべり面へ線
                          steps=[dict(state=dict(block="on"), delay=2.4, tag=dict(t="古い岩の塊（模式）", at="t1", to="block")),
                                 dict(),
                                 dict(state=dict(slip="on", move="on"), delay=0.4,
                                      tag=dict(t="すべり面（模式）", at="r1", to="slip"))],
                          note="塊とすべり面の形は模式・地形は1934年の地形図から・縦横同じ縮尺",
                          src="イタリア議会 調査委員会 最終報告 PDF 73・174頁")),
    ),
    # c404（9.84秒）＝左に c403 の図（2人の見立て）／2行目「反対の見方が強かった」で右に「岩は元の場所にある」断面（地層の筋が奥まで
    #   続く＝すべり面も塊も無い・模式）／3行目で札（S1 PDF74・PDF174）。⚠️ 学者の名は出さない（承認ずみの実名の外）
    "c404": dict(
        # ⚠️ qa_all の dup（札「反対の見方」が見出しを覆う・副題と札が同じ区切り）・echo（3行目の札が語りの写し）＝札は絵の名前だけ
        t="反対の見方", s="2つの見方を並べる",
        fig=("vsec", dict(view="pair",
                          steps=[dict(tag=dict(t="古い塊とすべり面", at="left")),
                                 dict(state=dict(right="on"), delay=0.4, tag=dict(t="地層が山の奥まで続く", at="right")),
                                 dict()],
                          note="形は模式・地形は1934年の地形図から・縦横同じ縮尺",
                          src="イタリア議会 調査委員会 最終報告 PDF 74・174頁")),
    ),
    # c405（9.23秒）＝1行目「人工の揺れで地下を探った報告も、調べた所では、厚い岩の土台がある」で調べた線（揺れを起こす所・受ける点・
    #   通り道）と、岩の土台の上の土（10〜20m＝S1 PDF74）／2行目「…試しの穴でも、その面は見つからなかった」で試し掘り3本・横穴2本
    #   （S1 PDF148）と2人の言うすべり面（点線・模式）。位置と深さは模式
    "c405": dict(
        t="地下を調べる", s="人工の揺れと、試しの穴",
        fig=("vsec", dict(view="probe",
                          steps=[dict(state=dict(survey="on"), delay=0.4,
                                      tag=dict(t="調べた線では、厚い岩の土台の上に土10〜20m", at="t1")),
                                 dict(state=dict(holes="on"), delay=0.4,
                                      tag=dict(t="試し掘り3本・横穴2本＝すべり面（点線）は見つからなかった", at="t2"))],
                          rel=[dict(t="10〜20m", src="S1 PDF74（崩れた土の厚さ10〜20m）"),
                               dict(t="試し掘り3本・横穴2本", src="S1 PDF148（1959〜60年の試し掘り3本・1961年の横穴2本）")],
                          note="位置と深さは模式（穴の数は記録）・点線のすべり面は2人の見立ての模式・地形は1934年の地形図から",
                          src="イタリア議会 調査委員会 最終報告 PDF 74・148・174頁")),
    ),
    # ── 🆕 ⑤b-4（2026-10-01）：案C の置き場 VD（正面から見た斜面・昼＝`tools/illu.py` の「16本目 ⑤b-4」の節）──
    # c408（9.36秒）＝合図（映像方針 §4-2 #7・c405 の断面の図解から）＝「正面から見ると」・小さな地図。1961年2月＝水位600m
    #   （1961年1月の初めに600m＝S8 p1046）・1960年11月4日の崩落の跡。1行目「…亀裂が囲む塊の大きさを見積もった」で範囲に色／
    #   2行目「地表の長い亀裂を、地下深くのすべり面の、地表に出た端と読んだ」で右上に小さな断面（c403 と同じ VB の線・模式）と、
    #   正面の亀裂の上の点（VB の切り口＝#100 の x740）からすべり面の上の端へ点線（S1 PDF77・PDF163）。
    #   🆕 画面の種類は「再現イラスト」（混ざりは全面の絵で書けない＝check_illu ⑦。小さな断面は絵の中の枠＝「横から見た断面（模式）」）
    "c408": dict(
        fig=("illu", dict(
            place="VD", start=dict(crack="on", water="600", c1960="fell", switch="on"),
            rec="S8 p1046（1961年1月の初めに水位600m）・S1 p72（1960年11月4日の崩落）",
            steps=[dict(state=dict(area="on"), delay=1.6, rec="S1 p77（ミュラー：亀裂が囲む塊は約2億m³）"),
                   dict(state=dict(pip="on"), delay=0.5,
                        rec="S1 p77（10月の亀裂＝深いすべり面が地表と交わる線）・S1 p163（周りの亀裂＝深いすべり面の地表との交わり）")])),
    ),

    # ── 🆕 ⑤b-8（2026-10-02）：Google Earth③ の替え c406・決め所 c409・c417 ──
    # c406（9.73秒）＝昼の VA near。合図（c405 の断面の図解＝VB と同じ南北の線）＝「上から見ると」・さっきの断面の線（B）。
    #   1行目（約1.8秒〜＝「1960年11月4日の崩落」）＝崩落の2か所（VD の c312 と同じ x の幅＝S1 PDF72・ダムの約500m上流＝PDF82・
    #   形は模式）と札／2行目（崩落のあとの現場の話し合い）＝同じ場所へゆっくり寄る
    "c406": dict(
        fig=("illu", dict(
            place="VA", start=dict(view="near", tod="day", prev="B", switch="on"), camc="c1960",
            rec="#100 p1（1934年の地形図＝谷と湖の位置）",
            steps=[dict(state=dict(c1960="fell"), delay=1.8,
                        rec="S1 p72（1960年11月4日・約70万m³・2か所）・S1 p82（ダムの約500m上流）",
                        # ⚠️ ⑤b-8 の echo：「1960年11月4日の崩落」は字幕の複写（100%）＝語りに無い「2か所」（S1 PDF72）を札に
                        tag=dict(t="崩れた2か所", at="c1960", off=(-60, 100), anchor="end", keep=True, delay=2.3)),
                   dict(state=dict(cam=1.08), delay=0.3, dur=4.5)])),
    ),
    # 決め所（台本の★）。S1 p77「il dottor Mueller, interpretando la fessura apparsa nell'ottobre 1960 come l'intersezione di una
    #   superficie di rottura profonda, riteneva che il volume … dovesse essere considerato di circa 200 milioni di metri cubi」
    "c409": dict(
        t="ミュラーの見積もり",
        s="1960年10月の亀裂から",
        fig=("quote", dict(phrase=["動いている塊は、", "約2億立方メートル"], rows=ss.qrows("S1", "PDF 77頁"), paper=True)),
    ),
    # 決め所（台本の★）。S1 p179（多数派）「essi erano conosciuti alla Pubblica Amministrazione, benché non consti che le relazioni
    #   siano state ufficialmente trasmesse」
    "c417": dict(
        t="報告の扱い",
        s="役所は中身を知っていた",
        fig=("quote", dict(phrase=["報告書が正式に送られたとは、", "確認できない"],
                           rows=ss.qrows("S1", "PDF 179頁", ("出どころ", "多数派の報告")), paper=True)),
    ),
}
