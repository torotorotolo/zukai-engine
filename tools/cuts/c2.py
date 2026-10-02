# -*- coding: utf-8 -*-
"""第2章　谷とアーチダム c201–c220（20カット）。16本目（バイオントダム災害）。

■ 🔴 2026-10-01（⑤b-1）：15本目（リノ・エアレース2011）の中身を空にした＝git の `c646174`（`git show c646174:tools/cuts/c2.py`）。
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
    "c201": dict(kind='写真',
               plan='台本の画：実写 #087 1956年の峡谷',
               src='S8 p.43'),
    "c202": dict(kind='写真',
               plan='台本の画：実写 #100 1934年の地形図【上から】（イタリア軍地理院）',
               src='S1 PDF98'),
    "c203": dict(kind='写真',
               plan='台本の画：実写 #033 1955年の峡谷',
               src='S1 PDF49・PDF50・PDF51・PDF98'),
    "c204": dict(kind='図解',
               plan='【地図】地図 drift：水の通り道（湖 → 発電所）・ベッルーノとラクイラ（映像方針 §6）｜台本の画：図 地図【上から】 水の通り道（バイオントの湖 → 下流の発電所）（rec= PDF51）'
                    '｜🆕 ⑤b-8（2026-10-02）：流れ図（箱の型）に替えた＝湖と発電所の位置・距離が資料に無い（門番 check_drift ③）＝映像方針 §18',
               src='S1 PDF51'),
    "c205": dict(kind='図解',
               plan='台本の画：図 数の比べ 1957年の計画の変更（高さ202→266m・最も高い水位677→722.50m・容量1億5,000万m³）（rec= PDF63）',
               src='S1 PDF63'),
    "c206": dict(kind='写真',
               plan='台本の画：実写 BY-SA #073 建設中のダム（Simone Aime の記録・CC BY-SA 4.0・額装）',
               src='S1 PDF63'),
    "c207": dict(kind='図解',
               plan='台本の画：図 数の比べ（c205 の図を戻す・つくれる電気は数を出さず「増える」の矢印だけ）（rec= PDF63）',
               src='S1 PDF63'),
    "c208": dict(kind='写真',
               plan='🆕 ⑤b-7（10-02）：#075 → #080（#075 は1958年の管の橋だけ＝ダムが写っていない・#080＝1960年 下流から見た'
                    '工事中のダム・Torno・BY-SA・額装＝映像方針 §17）｜台本の画：実写 BY-SA #075 建設中のダム（Simone Aime の記録・CC BY-SA 4.0・額装）',
               src='S1 PDF72・S8 p.41・S9 PDF6'),
    "c209": dict(kind='図解',
               plan='台本の画：図 アーチダムのしくみ【上から】（左に上から見た弓なりの形・水の力が両岸の岩へ・札「上から見ると」・2行目の「縦にも」で右に横から切った反りを小さく添える・札「横から切ると」）（rec= S8 p.41・p.43・S9 PDF6）',
               src='S8 p.41・p.43'),
    "c210": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='S8 p.43'),
    "c211": dict(kind='図解',
               plan='【断面の図解】断面の図解（模式図）：ダムの断面（寸法）・斜面の目印・2人の見立てと反対の見方・地下を調べる揺れと試しの穴・水理模型・しみこんだ水。VB と同じ地形の線を使う（向きがそろう）（映像方針 §6）｜台本の画：図 断面【横から】 ダムの断面（高さ261.60m・天端の標高725.50m・厚さ 底22.11m・上3.40m）合図（向きの札「横から見ると」・c209 の右の反りの絵を大きくする）（rec= S9 PDF6）｜合図（映像方針 §4-2 #4・c209 から）：台本どおり（c209 の右の反りの絵を大きくする）＋「横から見ると」',
               src='S9 PDF6'),
    "c212": dict(kind='写真',
               plan='台本の画：実写 #078 天端と操作の建物（事故の前）',
               src='S9 PDF6'),
    "c213": dict(kind='写真',
               plan='台本の画：実写 #089 ダムと湖（事故の前）',
               src='S1 PDF63'),
    "c214": dict(kind='写真',
               plan="台本の画：実写 #076 1961年の絵はがき｜⚠️ #076 は ⑤b で原寸を見てから（④'・映像方針の申し送り）",
               src='S9 PDF6・materials #088（altezza m. 280）'),
    "c215": dict(kind='写真',
               plan='台本の画：実写 #079 エルト村（事故の前）',
               src='S1 PDF171'),
    "c216": dict(kind='写真',
               plan='台本の画：実写 #082 カラーの絵はがき（事故の前のダムと湖）',
               src='S1 PDF72'),
    "c217": dict(kind='図解',
               plan='台本の画：図 年表 サーデからエネルへ（1962-12-06 法律第1643号でエネルを設立・1963-03-14 大統領令第221号で電気の事業を移す）（rec= PDF90・PDF91）',
               src='S1 PDF90・PDF91'),
    "c218": dict(kind='図解',
               plan='台本の画：図 年表（c217 の図を戻す・1963年3月に印）',
               src='S1 PDF91・PDF98・S10 PDF20'),
    "c219": dict(kind='写真',
               plan='台本の画：実写 #084 天端と満水に近い湖（事故の前・撮影年は資料で割れる）',
               src='S1 PDF72'),
    "c220": dict(kind='写真',
               plan='台本の画：実写 #090 1960年の空撮（事故の前）',
               src='S1 PDF72'),
}

SPEC = {
    # ── 🆕 ⑤b-7（2026-10-02）：写真と頁の束（`qa_out/ep16_assets.py`）。BY-SA の2点（c206・c208）は額装・原色・1点1カット ──
    # #087（1956年）＝バイオントの峡谷と橋と道
    "c201": dict(
        t="石灰岩の峡谷",
        s="1956年　バイオントの峡谷と橋",
        photo=P("gorge_1956"), **ss.kind(P("gorge_1956")),
    ),
    # #100（イタリア軍地理院・1934年の地形図・PD）＝谷・峡谷の出口・ピアーヴェ川の谷・ロンガローネ。
    #   ⚠️ 額装（⑤b-7）：地図は上下の端まで地名と凡例の字がある＝全画面で寄ると、どちらかの端の字の行を切る（門番 edges・
    #   窓下 k0.90）。額装は寄りが小さい（0.35倍）＝端の字が残る
    "c202": dict(
        t="イタリア軍の地形図",
        s="1934年　峡谷の出口とピアーヴェ川の谷",
        photo=P("igm_1934"), panel=True,
    ),
    # #033（1955年・『Il grande Vajont』2012 所収）＝ダムを築く前の峡谷・アーチの橋・上の小屋
    "c203": dict(
        t="ダムを築く前の峡谷",
        s="1955年　峡谷にかかる橋と小屋",
        photo=P("gorge_1955"), **ss.kind(P("gorge_1955")),
    ),
    # #073（Enel・CC BY-SA 4.0）＝1956年 峡谷に架けるアーチの橋の工事。🔴 ダムは写っていない＝副題は「橋の工事」まで
    "c206": dict(
        t="工事の始まった峡谷",
        s="1956年　峡谷に架ける橋の工事（Enel の記録）",
        photo=P("bridge_works_1956"), panel=True, color=1.0,
    ),
    # #080（Torno S.p.A.・CC BY-SA 4.0）＝1960年 下流から見た工事中のダム（⑤b-7：PLAN の #075＝管の橋だけ から替えた）
    "c208": dict(
        t="工事中のダム",
        s="1960年　下流から見たダム（Torno の記録）",
        photo=P("dam_works_1960"), panel=True, color=1.0,
    ),
    # #078（1963年より前）＝天端と操作の建物（10月9日の夜の場所）。天端の右の人影は流れてぼけている（顔は見えない）
    "c212": dict(
        t="天端の操作室",
        s="事故の前　天端の端に立つ操作室",
        photo=P("crest_cabin"), **ss.kind(P("crest_cabin")),
    ),
    # #089（1960年）＝天端の道と湖
    "c213": dict(
        t="天端と湖",
        s="1960年　ダムの天端から見た湖",
        photo=P("crest_lake_1960"), **ss.kind(P("crest_lake_1960")),
    ),
    # #076（1961年の絵はがき）＝下に「Diga Del Vajont (altezza m. 280)」と刷られている（原寸で読んだ）
    "c214": dict(
        t="刷られた「280」",
        s="1961年の絵はがき（下に「altezza m. 280」）",
        photo=P("postcard_280_1961"), **ss.kind(P("postcard_280_1961")),
    ),
    # #079（1960年の絵はがき「Erto m. 775 - Lago del Vaiont」）＝湖とエルトの村
    "c215": dict(
        t="湖の北の岸の村",
        s="1960年の絵はがき　湖とエルトの村",
        photo=P("erto_1960"), **ss.kind(P("erto_1960")),
    ),
    # #082（カラーの絵はがき・撮影年は分からない＝年を書かない）＝左岸の道とトンネルの口・赤い車・ダム・奥にトックの斜面
    "c216": dict(
        t="ダムと湖の絵はがき",
        s="事故の前のカラーの絵はがき　左岸の道とダム",
        photo=P("color_postcard"), **ss.kind(P("color_postcard")),
    ),
    # #084（撮影年が割れる＝#088 の1960年の絵はがきと同じ写真＝年を書かない）＝天端と満水に近い湖・トックの斜面
    "c219": dict(
        t="湖の南の岸の山",
        s="事故の前　天端と湖、奥にトック山の斜面",
        photo=P("crest_full_lake"), **ss.kind(P("crest_full_lake")),
    ),
    # #090（1960年）＝上空から見た湖とダム・雪の山
    "c220": dict(
        t="空から見た湖",
        s="1960年　上空から見た湖とダム",
        photo=P("aerial_1960"), **ss.kind(P("aerial_1960")),
    ),
    # ── 🆕 ⑤b-6a（2026-10-01）：量・箱・年表（14・15本目の型）と c209 アーチダムのしくみ（vsec16 の arch）──
    # c205（11.55秒）＝1957年の計画の変更（S1 p63）：1行目＝もとの計画の棒2本（高さ・いちばん高い水位）／2行目＝高さ 202→266m／
    #   3行目＝水位 677→722.5m。数は字幕だけ（棒は 0 から＝§5b-94）
    "c205": dict(
        t="大きくした計画", s="1957年の変更（会社の申請）",
        fig=("qty", dict(view="bar", groups=[ss.QG["dam_h"], ss.QG["lake_max"]], steps=[
            dict(add=[ss.qb("h_old"), ss.qb("l_old")]),
            dict(add=ss.qb("h_new")),
            dict(add=ss.qb("l_new"))],
            note="水位は海面からの高さ（標高）", src=ss.src(["S1 p63"]))),
    ),
    # c207（4.46秒）＝計画を大きくすると（S1 p63＝容量と年間の発電量が上がった）。🔴 PLAN は「c205 の図を戻す＋電気は矢印だけ」＝
    #   量の型は矢印を描けず、変更の前の容量と発電量は記録に無い（棒にできない）→ 箱の型の流れ図で「増える」を矢印で言う
    #   （映像方針 §15）。1行目（聞き役）＝高くする → 水が増える／2行目＝→ 電気が増える
    "c207": dict(
        t="計画を大きくすると", s="会社の申請（1957年）",
        fig=("boxes", dict(view="flow", layout=ss.FL_GROW, steps=[
            dict(add=ss.ce("g1", "g2")),
            dict(add=ss.ce("g2", "g3"))],
            src=ss.src(["S1 p63"]))),
    ),
    # c209（8.53秒）＝アーチダムのしくみ：1行目＝上から見た弓（天端の弦 168m・長さ 190.15m・上の厚さ 3.40m＝S9 PDF6）に水の力と、
    #   両側の岩へ逃がす力の矢印・札「上から見ると」／2行目（縦にも）＝右に横から切った断面（🔴 c211 と同じ形＝c211 が大きくする）・
    #   札「横から切ると」。二重のアーチ（double-arch）＝S8 p1041・p1043
    "c209": dict(
        t="アーチダムのしくみ", s="バイオントダムの形",
        fig=("vsec", dict(view="arch", steps=[
            dict(state=dict(force="on"), delay=0.4, tag=dict(t="上から見ると", at="plan", d="横に弓なり")),
            dict(state=dict(sec="on"), delay=0.2, tag=dict(t="横から切ると", at="sec", d="縦にも反る"))],
            note="形は模式（上から見た弓は天端の長さと弦から・縦横同じ縮尺）・力の矢印の長さは模式",
            src=ss.src(["S9 p2006", "S8 p1041", "S8 p1043"]))),
    ),
    # c217（9.29秒）・c218（11.09秒）＝サーデからエネルへ（S1 p90＝1962年12月6日の法律・p91＝1963年3月14日の大統領令）。
    #   c217：1行目（会社のほうが変わる）は帯だけ／2行目＝エネルができる／3行目＝札「国がつくった公社」
    #   c218：エネルの点を沈めて続ける。1行目＝事業がエネルへ／2行目＝札「エネル・サーデの名で」（S1 p222）／
    #   3行目＝札「技術の責任者ビアデーネ」（S10 p3020「direttore del Servizio costruzioni idrauliche della Sade」）
    "c217": dict(
        t="会社が変わる", s="国の電力公社エネル",
        fig=("axis", dict(**ss.AX_ENEL, steps=[
            dict(),
            dict(add=ss.ax("n_enel"), cur="1962-12-06"),
            dict(add=dict(k="chips", at="1962-12-06", chips=["国がつくった公社"], rec="S1 p90"))],
            src=ss.src(["S1 p90"]))),
    ),
    "c218": dict(
        t="事業の引き継ぎ", s="サーデからエネルへ",
        fig=("axis", dict(**ss.AX_ENEL, past=[ss.ax("n_enel")], start=dict(cur="1962-12-06"), steps=[
            dict(add=ss.ax("n_move"), cur="1963-03-14"),
            dict(add=dict(k="chips", at="1963-03-14", chips=["エネル・サーデの名で"], rec=["S1 p91", "S1 p222"])),
            dict(add=dict(k="chips", at="1963-03-14", chips=["技術の責任者ビアデーネ"], rec=["S1 p91", "S10 p3020"], i0=1))],
            src=ss.src(["S1 p90", "S1 p91", "S1 p222", "S10 p3020"]))),
    ),

    # ── 🆕 ⑤b-4（2026-10-01）：断面の図解（`tools/vsec16.py`＝「再現イラスト」の札は出さない）──
    # c211（8.00秒）＝合図（映像方針 §4-2 #4・c209 の上から見た図から）＝見出し「横から見ると」・c209 の右の「横から切った反り」を
    #   大きくした形（VC と同じダムの断面＝左が上流〈湖〉）。1行目「いちばん下で約22メートル」で底の厚さ＋高さ／2行目「いちばん上では
    #   3.4メートル」で上の厚さ／3行目「水の力を、厚さでなく、形で受け止める」で水の力の矢印（長さは模式）。寸法は S9 PDF6
    "c211": dict(
        t="横から見ると", s="ダムの断面（厚さ）",
        fig=("vsec", dict(view="dam",
                          steps=[dict(state=dict(base="on"), delay=0.3,
                                      tag=[dict(t="約22m", at="base"), dict(t="高さ261.6m", at="height")]),
                                 dict(state=dict(top="on"), delay=0.3, tag=dict(t="3.4m", at="top")),
                                 dict(state=dict(force="on"), delay=0.4, tag=dict(t="水の力", at="force"))],
                          rel=[dict(t="約22m", src="S9 PDF6（底の厚さ22.11m）"), dict(t="3.4m", src="S9 PDF6（上の厚さ3.40m）"),
                               dict(t="261.6m", src="S9 PDF6（高さ261.60m）")],
                          note="断面の反りと水の力の矢印の長さは模式・縦横同じ縮尺・湖は最も高い水位（722.50m）まで",
                          src="バイオント財団の年表 PDF 6頁／イタリア議会 調査委員会 最終報告 PDF 63頁")),
    ),

    # ── 🆕 ⑤b-8（2026-10-02）：流れ図 c204・決め所 c210 ──
    # c204（9.59秒）＝水の通り道。🔴 PLAN は地図 drift だったが、湖と下流の発電所（ソヴェルゼーネ）の位置・距離は資料に無い
    #   （S1・S8・S9・S10 を「km・chilometri・座標」で引いた）＝門番 check_drift ③（記録の宣言が無い地図は止める）を正直には
    #   通せない → 計画の流れ（台本の3行どおり）を流れ図で＝映像方針 §18。S1 PDF51「la sezione della valle del Vajont presa in
    #   considerazione per la costruzione della diga di sbarramento」「dal serbatoio del Vajont … addotte alla grande centrale di
    #   Soverzene」。1行目＝ダム → 湖／2行目＝湖 → 下流の発電所（電気をつくる）／3行目＝湖に「発電のための水がめ」
    "c204": dict(
        t="ダムと発電の計画",
        s="会社の申請の中身",
        fig=("boxes", dict(
            view="flow",
            layout=dict(heads=[dict(id="lake", kind="node", t="大きな湖", x=(760, 1160), y=(450, 550), rec="S1 p51")]),
            steps=[dict(add=[dict(k="role", id="dam", t="谷をせき止めるダム", pos=(160, 600), y=500, rec="S1 p51"),
                             dict(k="edge", fr="dam", to="lake")]),
                   dict(add=[dict(k="role", id="plant", t="下流の発電所", pos=(1320, 1760), y=500, rec="S1 p51"),
                             dict(k="edge", fr="lake", to="plant"),
                             dict(k="chip", at="plant", t="電気をつくる", dy=70, rec="S1 p51")]),
                   dict(add=dict(k="chip", at="lake", t="発電のための水がめ", dy=85, rec="S1 p51"))],
            src=ss.src(["S1 p51"]))),
    ),
    # 決め所（台本の★・c210）。S8 p1043「The Vaiont dam, a 276 meter high thin arch dam, was the highest double-arch dam in Europe」。
    #   ⚠️ S8 の 276m は高さの別の測り方＝画面に出さない（高さの数は c211 の S9 PDF6＝261.60m）。完成の年＝S8 p1041（1957〜1960）
    "c210": dict(
        t="当時のダム",
        s="1960年に完成したダム",
        fig=("quote", dict(phrase=["当時ヨーロッパで最も高い", "二重アーチダム"], rows=ss.qrows("S8", "43頁"), paper=True)),
    ),
}
