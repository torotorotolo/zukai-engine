# -*- coding: utf-8 -*-
"""第11章　今も立つダム cb01–cb20（20カット）。16本目（バイオントダム災害）。

■ 🔴 2026-10-01（⑤b-1）：新しく作った（15本目は9章）。14本目の同じ名前の章ファイル（第10・11章＝別の中身）は
  git の `dc6ecf4`（`git show dc6ecf4:tools/cuts/cb.py`）。
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
    "cb01": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='S10 PDF20'),
    "cb02": dict(kind='写真',
               plan='台本の画：実写 #119 家並みの上に見える今のダム（現在）',
               src='S10 PDF20・S1 PDF98'),
    "cb03": dict(kind='写真',
               plan='台本の画：実写 #118 ロンガローネから峡谷ごしに見る今のダム（現在・CC BY 3.0）',
               src='S9 PDF17・S1 PDF213'),
    "cb04": dict(kind='写真',
               plan='台本の画：実写 #116 下流から見た今のダム（現在）',
               src='S9 PDF17・S1 PDF41'),
    "cb05": dict(kind='写真',
               plan='台本の画：実写 #120 トック山の崩れた跡（現在・CC BY 3.0）',
               src='S1 PDF144'),
    "cb06": dict(kind='写真',
               plan='台本の画：実写 #121 すべり面の近景（現在・CC BY 2.5）',
               src='S1 PDF147・S8 p.41'),
    "cb07": dict(kind='写真',
               plan='台本の画：実写 #122 残った湖と崩れた山（現在・CC BY 4.0）',
               src='S1 PDF146・PDF41'),
    "cb08": dict(kind='再現イラスト',
               plan='【案C VA 上から見た谷】🆕 ⑤b-7（2026-10-02 カズヤくん）：Google Earth → 地図（VA）に替えた＝エルトとカッソ・'
                    '湖に近い集落（SPEC は ⑤b-8）｜台本の画：実写 Googleアース⑤ エルトとカッソ（現在・真上から）【上から】 合図（向きの札「上から見た図」・北の矢印）・崩れた山と残った湖の位置に印',
               src='S1 PDF171・PDF98'),
    "cb09": dict(kind='写真',
               plan='台本の画：実写 #115 「バイオントの救助者の通り」の標識（2023年）',
               src='—'),
    "cb10": dict(kind='写真',
               plan='台本の画：実写 #014 慰霊の十字架（1963年）',
               src='—'),
    "cb11": dict(kind='再現イラスト',
               plan='【案C VA 上から見た谷】🆕 ⑤b-7（2026-10-02 カズヤくん）：Google Earth → 地図（VA）に替えた＝ピアーヴェ川の下流'
                    '（ca26 と別の範囲・SPEC は ⑤b-8）｜台本の画：実写 Googleアース⑥ ピアーヴェ川の下流（現在・ca26 とは別の向き）',
               src='S10 PDF24・PDF11'),
    "cb12": dict(kind='図解',
               plan='台本の画：図 並べ図 3つの答え（議会の多数派〈予見できたかを確かめるのは裁判所の仕事・起きた形では誰も予見しなかった〉・少数派〈予見でき避けられた〉・破毀院〈崩落も含めて予見していながらの重い過失として2人を有罪〉）（rec= PDF178・PDF207・PDF241・S9 PDF18）',
               src='S1 PDF178・PDF207・S9 PDF18'),
    "cb13": dict(kind='図解',
               plan='台本の画：図 並べ図（同じ図）',
               src='S1 PDF207・S9 PDF18'),
    "cb14": dict(kind='図解',
               plan='台本の画：図 年表 決める場面（1960-11 崩落のあと・1961-02 約2億m³の報告・1962年春 下流の研究を見送る・1962-07 「700mなら安全」・1963-03 715mを求める・1963-09 速さが増す・1963-10-09）（rec= 各章の頁）',
               src='S8 p.43'),
    "cb15": dict(kind='図解',
               plan='台本の画：図 年表（同じ図・1960〜62年に印）',
               src='S1 PDF72・PDF77・PDF225'),
    "cb16": dict(kind='図解',
               plan='台本の画：図 年表（同じ図・1963年に印）',
               src='S1 PDF92・PDF93・PDF98'),
    "cb17": dict(kind='写真',
               plan='台本の画：実写 #117 真下から見た今のダム（現在・CC BY 3.0）',
               src='S1 PDF1'),
    "cb18": dict(kind='写真',
               plan='台本の画：実写 #023（第1章の写真を戻す）',
               src='S1 PDF171・PDF98・S9 PDF17・S10 PDF20'),
    "cb19": dict(kind='図解',
               plan='【線の図】場面1 水位と斜面の速さの線（型＝線の図）：上下2段（上＝水位・下＝斜面の速さ）・横軸は年月で共通。記録の点だけを結ぶ（点と点の間は模式＝S8 の図6 はなぞらない）・700m の線（模型）・715m の許可。⚠️ 画の欄の「再現イラスト」は図解として作る（「再現イラスト」の札は出さない）（映像方針 §6）｜台本の画：図 再現イラスト 場面1（3年分の線を全部見せる）',
               src='S1 PDF72・PDF85・PDF92・PDF93・PDF96・PDF226・S8 p.46・S9 PDF14'),
    "cb20": dict(kind='パネル',
               plan='台本の画：panel コメントの問い（です・ます・3行）',
               src='—'),
}

SPEC = {
    # ── 🆕 ⑤b-7（2026-10-02）：写真の束（`qa_out/ep16_assets.py`）＝いまの谷 ──
    # #119（Emanuele Paolini・PD）を戻す。⚠️ 見出しは章の題（第11章「今も立つダム」＝右上の章の札）と重ねない（門番 dup）
    "cb02": dict(
        t="家並みの上のダム",
        s="2005年8月　ロンガローネの家並みの上に見えるダム",
        photo=P("dam_houses_now"), **ss.kind(P("dam_houses_now")),
    ),
    # #118（Stefano Petri・CC BY 3.0）を戻す（bias 0.6＝c111 の注）
    "cb03": dict(
        t="峡谷のダム",
        s="2003年4月　ロンガローネから峡谷ごしに見たダム",
        photo=P("dam_gorge_now"), **ss.kind(P("dam_gorge_now")), bias=0.6,
    ),
    # #116（Riccardo Sartor・PD）を戻す
    "cb04": dict(
        t="終わらない検査",
        s="2008年2月　下流の峡谷から見たダム",
        photo=P("dam_now_downstream"), **ss.kind(P("dam_now_downstream")),
    ),
    # #120（Davide Cavalli・CC BY 3.0）を戻す
    "cb05": dict(
        t="トック山の跡",
        s="2016年8月　いまのトック山の斜面",
        photo=P("toc_now"), **ss.kind(P("toc_now")),
    ),
    # #121（Christian Thiergan・CC BY 2.5）を戻す
    "cb06": dict(
        t="すべり面",
        s="2005年7月　トック山のすべり面の近景",
        photo=P("slide_surface_now"), **ss.kind(P("slide_surface_now")),
    ),
    # #122（Gianmarco139・CC BY 4.0）を戻す
    "cb07": dict(
        t="残った湖",
        s="2015年5月　崩れた山と、上流側に残った湖",
        photo=P("lake_now"), **ss.kind(P("lake_now")),
    ),
    # #115（米陸軍 2023年10月8日・PD）＝「Viale Soccorritori del Vajont」の標識。🔴 ⑥の概要欄に米陸軍の断り書き
    "cb09": dict(
        t="記念の通りの名",
        s="2023年10月　「Viale Soccorritori del Vajont」の標識",
        photo=P("sign_2023"), **ss.kind(P("sign_2023")),
    ),
    # #014（イタリア消防・1963年・318px）＝慰霊の大きな木の十字架と花輪
    "cb10": dict(
        t="慰霊の十字架",
        s="1963年　木の十字架と花輪",
        photo=P("memorial_cross_1963"), **ss.kind(P("memorial_cross_1963")),
    ),
    # #117（Stefano Petri・CC BY 3.0）を戻す
    "cb17": dict(
        t="真下から見たダム",
        s="2003年4月　ダムの下流の面",
        photo=P("dam_now_below"), **ss.kind(P("dam_now_below")),
    ),
    # #023（米陸軍・1963年）を戻す（第8章の写真）
    "cb18": dict(
        t="ダムと谷",
        s="1963年10月　ダムの奥の谷を埋めた崩れた山",
        photo=P("dam_slide_1963"), **ss.kind(P("dam_slide_1963")),
    ),

    # ── 🆕 ⑤b-6b（2026-10-01）：並べ図（`boxes` の row）と年表（`axis` の date）＝14本目の型・門番 check_boxes・check_axis ──
    # cb12（12.31秒）＝3つの答え（多数派 S1 p178「così come si è manifestato, non fu previsto da nessuno」・少数派 S1 p207「prevedibile e
    #   probabile, e quindi evitabile」・破毀院 S9 p2018「aggravata dalla previsione dell'evento compresa la frana」）。同じ形で並べるだけ
    #   （どれかに決めない＝cb14「この動画も、答えを1つに決めない」）。1行目「2つの問いに戻る」で3つ／2〜3行目（多数派）は足さない。
    #   ⚠️ 並べ図は2つ以上が要る（門番 ⑧）＝語りの順に1つずつ出すと cb12 が1つになる＝3つを1行目で並べる（映像方針 §16）
    "cb12": dict(
        t="3つの答え", s="予見できたのか",
        fig=("boxes", dict(view="row", slots=3, steps=[
            dict(add=[ss.cause("ans_maj"), ss.cause("ans_min"), ss.cause("ans_cass")]), dict(), dict()],
            src=ss.src(["S1 p178", "S1 p207", "S9 p2018"]))),
    ),
    # cb13（9.84秒）＝同じ図（少数派・破毀院は語り）
    "cb13": dict(
        t="3つの答え", s="立場で違う答え",
        fig=("boxes", dict(view="row", slots=3,
                           past=[ss.cause("ans_maj", keep=True), ss.cause("ans_min", keep=True),
                                 ss.cause("ans_cass", keep=True)], steps=[dict(), dict(), dict()],
                           src=ss.src(["S1 p178", "S1 p207", "S9 p2018"]))),
    ),
    # cb14（11.18秒）＝決める場面の年表（ss.AX_DEC＝1960〜63年）。1行目で行き先の崩落（1963年10月9日）／2行目（学術の総説 S8 p.43
    #   ＝当時の知識と技術を踏まえて）は足さない／3行目「決める場面が、何度もあった」で5つの点（札なし）。1962年の春は札なしの点1つ
    #   （S1 p225 の4月）＝割れる日の印は cb15 で
    "cb14": dict(
        t="決める場面", s="1960〜1963年",
        fig=("axis", dict(**ss.AX_DEC, steps=[
            dict(add=ss.ax("d_end"), cur="1963-10-09"), dict(),
            dict(add=[ss.dot("d_fall60"), ss.dot("d_mul"), ss.ax("d_spr"), ss.dot("d_715"), ss.dot("d_speed")])],
            src=ss.src(["S8 p1043", "S1 p72", "S1 p76", "S1 p225", "S1 p92", "S1 p93", "S1 p98"]))),
    ),
    # cb15（10.30秒）＝1960〜62年に札（④' の G6＝PDF72・PDF76・PDF225）。1行目「1960年11月の崩落のあと。1961年2月、約2億立方メートルの
    #   報告のあと」で2つの点／2行目「1962年の春、下流の波の研究を、見送ったとき」で割れる日の印2つ（S9 p2012＝3月30日・S1 p225＝4月30日・
    #   c518 と同じ＝どちらが正しいと描かない・カーソルを置かない）
    "cb15": dict(
        t="決める場面", s="1960〜1962年",
        fig=("axis", dict(**ss.AX_DEC, past=[ss.ax("d_end"), ss.dot("d_715"), ss.dot("d_speed")], steps=[
            dict(add=[ss.ax("d_fall60"), ss.ax("d_mul")], cur="1961-02-03"),
            dict(add=[ss.ax("d_s1"), ss.ax("d_s2")])],
            note="下流の研究を見送った月は資料で割れる", src=ss.src(["S1 p72", "S1 p76", "S9 p2012", "S1 p225"]))),
    ),
    # cb16（7.59秒）＝1963年に札（S1 p92＝3月20日 715m を求める・p93＝9月2日から速さが増す・p98＝10月9日）。1行目で2つの点／2行目
    #   「そして、10月9日の夜」で崩落
    "cb16": dict(
        t="決める場面", s="1963年",
        fig=("axis", dict(**ss.AX_DEC, past=[ss.dot("d_fall60"), ss.dot("d_mul"), ss.ax("d_spr")], start=dict(cur="1961-02-03"),
                          steps=[dict(add=[ss.ax("d_715"), ss.ax("d_speed")], cur="1963-09-02"),
                                 dict(add=ss.ax("d_end"), cur="1963-10-09")],
                          src=ss.src(["S1 p92", "S1 p93", "S1 p98"]))),
    ),

    # ── 🆕 ⑤b-5（2026-10-01）：場面1 水位と斜面の速さの線（`tools/lv16.py`・門番 check_mech judge_lv）──
    # cb19（10.18秒）＝3年分の線を全部（1960年3月〜1963年10月9日・速さは 0〜210ミリ）。1行目「3年分の水位と速さの線を、もう一度並べる」
    #   で水位の線と700m・715m の線／2行目「この動画の線は、議会の報告書、学術の総説、財団の年表の数をつないだものだ」で速さの線（出典の
    #   行＝左下に3つの資料）／3行目「その線の上で、どこで手を止めるか」で cb16 の場面（1963年3月・9月・10月9日の夜）の点を囲む
    "cb19": dict(
        t=ss.LV_T, s="1960〜1963年",
        fig=ss.lv_fig(ss.LV_ALL, vr=ss.VR_HI, past=[ss.LV_EV["fall60"]], rel=[ss.LV_REL["model"], ss.LV_REL["permit"]], steps=[
            dict(add=ss.lv_upto("1963-10-09", rows="z") + [ss.LV_REF["model"], ss.LV_REF["permit"]]),
            dict(add=ss.lv_upto("1963-10-09", rows="v") + [ss.LV_BRK]),
            dict(add=[dict(k="ring", s="z", at="1963-03-15"), dict(k="ring", s="v", at="1963-09-02"),
                      dict(k="ring", s="v", at="1963-10-09")])]),
    ),

    # ── 🔴 ⑤b-1（2026-10-01）：字幕の試し焼きに使うパネル（最終の形）──
    # コメントの問い（13本目から・ed01 の直前）。13本目 c920・14本目 cd08・15本目 c920 と同じ形。「この動画」は画面に出さない
    # cb20＝語りの1行・2行・1行（2行目が2行に折れる）
    "cb20": dict(
        t="あなたなら、どうする",
        s="コメント欄で聞かせてください",
        fig=("panel", dict(
            blocks=[dict(k="問い1", t="どこで防げたか", c=J.AMBER),
                    dict(k="問い2", t="どこで手を止めるか", v="水位を決める立場なら", c=J.ALERT)],
            cols=2)),
    ),

    # ── 🆕 ⑤b-8（2026-10-02）：決め所 cb01・Google Earth⑤⑥ の替え cb08・cb11 ──
    # S10 p3020「per la prima volta in Italia una sentenza penale colpiva insieme l'esponente di una società industriale e finanziaria
    #   privata e un uomo appartenente all'istituzione pubblica dello Stato」
    "cb01": dict(
        t="判決の意味",
        s="何が初めてだったか",
        fig=("quote", dict(phrase=["イタリア初、", "会社と国の人を共に罰した判決"], rows=ss.qrows("S10", "PDF 20頁"), paper=True)),
    ),
    # cb08（7.45秒）＝Google Earth⑤ の替え。昼の VA wide＝崩れたあとの谷（塊・崩れた範囲・町と湖の岸の集落は泥の色＝c823 の終わりと
    #   c814 の状態＝門番 ⑫ の表 ss.ILLU_DESTROY_CUTS に足した）。1行目＝札「エルト」（S1 PDF171「L'abitato di Erto si salvò in parte
    #   notevole」＝エルトの建物の面は残っている）／2行目＝湖の岸の集落の札（ピネダ・サン・マルティーノ＝c814 と同じ位置・S1 PDF98）
    "cb08": dict(
        fig=("illu", dict(
            place="VA", start=dict(view="wide", tod="day", block="on", slide="on", towns="mud", shore="mud"),
            rec="S1 p147（1つの塊のまま）・S1 p98（10月10日の夜明けには…もう存在しなかった）",
            steps=[dict(rec="S1 p171（エルトの村はかなりの部分が助かった）",
                        tag=dict(t="エルト", at="erto", off=(40, -60), keep=True, delay=0.8)),
                   dict(rec="S1 p98（湖の岸のピネダとサン・マルティーノはもう存在しなかった）",
                        tag=[dict(t="ピネダ", at="pineda", off=(30, 75), keep=True, delay=0.6),
                             dict(t="サン・マルティーノ", at="smartino", off=(-40, 10), anchor="end", keep=True, delay=0.6)])])),
    ),
    # cb11（12.30秒）＝Google Earth⑥ の替え（ca26 と別の範囲）。昼の VA near＝いまも立つダムと、谷を埋めた塊（cb07 の写真と同じ
    #   いまの谷・町と湖の岸の集落は画面の外＝壊れる部品は使わない）を、3行をかけてダムへゆっくり寄る（頭から少し寄せる＝右の端の
    #   ピネダを画面の外に）。語りは裁判の記録の登録＝谷の絵は場所の目印（ピアーヴェ川の下流は ca26 で見せた＝映像方針 §18）
    "cb11": dict(
        fig=("illu", dict(
            place="VA", start=dict(view="near", tod="day", block="on", slide="on", cam=1.08), camc="dam",
            rec="S1 p147（1つの塊のまま）・S8 p1046（水平に300〜400m）",
            steps=[dict(state=dict(cam=1.11), delay=0.0, dur=4.6),
                   dict(state=dict(cam=1.14), delay=0.0, dur=3.7),
                   dict(state=dict(cam=1.17), delay=0.0, dur=3.6)])),
    ),
}
