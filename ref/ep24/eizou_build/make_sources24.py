# -*- coding: utf-8 -*-
"""24本目 映像方針：素材の出どころの表 sources24.psv を組む（2026-10-22・チャット5）。23本目の make_sources23.py の役を、24本目の素材の形で書き直した。

  python ref/ep24/eizou_build/make_sources24.py          # Commons の API で大きさ・許諾・URL を引き直して sources24.psv を書く
  python ref/ep24/eizou_build/make_sources24.py --offline # 引き直さず、前回の api24.json から書く

出力：eizou_build/sources24.psv（区切り「|」・手で直さない）・eizou_build/api24.json（API の控え）
      src/credits_private.tsv に作者欄を足す（git の外＝撮影者・投稿者の名前はここだけ）
列：code|type|title|page|get|dims|rights|basis|credit|era|people|file|note
  era＝前（事故の前）／当夜／後（1986〜88年＝事故のあと）／今・中（今の写真＝壊れていない部屋や盤）／今・跡（今の写真＝石棺・覆い・跡・立入禁止区域）／他所（同じ型のほかの発電所）／文書（報告書・会議録の紙面）／イメージ（フリー素材）
  people＝なし／遠景（顔が判らない）／背中（後ろ姿）／顔（顔が判る）
門番 make_list24.py がこの era と people を読む（前の章に「後・今・跡」を置かない／責める行に「顔」を置かない）。
名乗りにメールや @ を入れない。
"""
import csv
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
UA = 'zukai-engine/1.0 (ep24 visual plan research)'
API = 'https://commons.wikimedia.org/w/api.php'
OUT = os.path.join(HERE, 'sources24.psv')
CACHE = os.path.join(HERE, 'api24.json')
PRIVATE = os.path.join(EP, 'src', 'credits_private.tsv')
SRC = 'ref/ep24/src/eizou'
IAEA_LIST = os.path.join(EP, 'src', 'flickr', 'iaea0279_list.tsv')

# ── IAEA 0279（USFCRFC の1986年の写真・CC BY-SA 2.0）＝番号 → (era, people, 何)
IAEA = {
    '11': ('後', '顔', '交替のあとの健康診断（線量計で調べる看護師と医師・職員）'),
    '13': ('後', '遠景', '3・4号機の屋根のちりを抑える作業（クレーン・コンクリートポンプ車）'),
    '14': ('後', '遠景', '1986年5月1日、キエフの大通りで水による除染（地下鉄の「M」）'),
    '15': ('後', 'なし', '爆発の翌日にヘリから撮った壊れた4号炉（縦長）'),
    '17': ('後', '背中', '応急の救護所（テント・救急車・机の医師＝私人は背中だけ）'),
    '18': ('後', '顔', 'Mi-8 の前で地図を見るヘリの乗員3人（公的な任務・名前は言わない）'),
    '19': ('後', '遠景', '防護服で車に放水（召集された予備役の除染）'),
    '22': ('前', 'なし', '雪の中の発電所と送電塔（説明の語「1986年の冬」＝事故の前と読める）'),
    '23': ('前', 'なし', '発電所の入口の看板「ЧАЭС имени В.И. Ленина」'),
    '24': ('後', 'なし', '片づけの最初の班が見た壊れた4号機と排気筒'),
    '25': ('後', 'なし', '森の道の「放射能」の標識'),
    '26': ('前', '遠景', '事故の前のプリピャチ（団地・「СЛАВА КПСС」・花）'),
    '27': ('後', 'なし', '有刺鉄線の向こうの団地（事故のあとのプリピャチ）'),
    '28': ('前', 'なし', '町の碑「ЧОРНОБИЛЬ」'),
    '30': ('後', '顔', 'マスクの兵士の敬礼（片づけに加わった兵士）'),
    '32': ('後', 'なし', '多軸の大型運搬車（片づけに使った軍の機材）'),
    '34': ('前', '顔', '電話の当直（原発の職員は昼も夜も働いた＝何号機か・いつかは書いていない）'),
    '35': ('前', '顔', '炉心の見取りのランプ盤の前の運転員（何号機の制御室かは書いていない）'),
    '36': ('後', 'なし', '壊れた4号炉の前を飛ぶヘリ（専門家が損傷を調べるのを助ける）'),
    '40': ('後', 'なし', '溶接の火花'),
    '42': ('後', '顔', '白衣の3人（科学者は最も汚染された所にいた）'),
    '44': ('後', '顔', '新聞を読む作業員（毎日届いた新聞＝新聞の字が写る）'),
    '45': ('後', '顔', '背広の一行とクレーン（ルイシコフ ソ連閣僚会議議長の視察＝公人）'),
    '48': ('後', '顔', '遠隔操作の盤（無線でブルドーザーを動かす操作員＝名前は言わない）'),
    '49': ('後', 'なし', '装甲のブルドーザー'),
    '50': ('後', 'なし', '排気筒・巨大な鉄骨・クレーン（石棺を据える準備）'),
    '55': ('後', '顔', '背広の人々（ブリクス IAEA 事務局長の1988年5月の訪問＝公人）'),
    '56': ('後', '顔', '事故後検討会議の記者会見（1986年8月・ウィーン）'),
    '57': ('後', '顔', '記者会見の別の1枚'),
    '58': ('後', '顔', '会議のソ連側の席（名札「V. LEGASOV」とソ連の大使の名札）'),
    '59': ('後', '顔', '記者会見の別の1枚'),
    '60': ('後', '顔', '名札「V. LEGASOV / HEAD, USSR EXPERTS」（②で原寸で確かめた）'),
    '61': ('後', '顔', '会議の議長と IAEA 事務局長の席（名札「H. BLIX DIRECTOR GENERAL IAEA」）'),
    '62': ('後', '顔', '議長と事務局長の名札の席'),
}

# ── Commons の点＝code → (題, era, people, 何)
CM = {
    'P84': ('File:Припять 1984.jpg', '前', 'なし', '1984年1月29日 アメリカの偵察衛星の写真（USGS EarthExplorer）。発電所とプリピャチと冷却池。原本から切り出す（寄りの名＝発電所・町）'),
    'CR1': ('File:ChNPP Unit1control.JPG', '今・中', 'なし', '1号機の主制御室（炉の運転員の盤と炉心の表示・2011年・壊れていない）'),
    'CR3A': ('File:Control Room of Chernobyl Nuclear Power Plant Unit 3.jpg', '今・中', '遠景', '3号機の制御室（IAEA 02710152・2010年・職員は遠景）'),
    'CR3B': ('File:Sterownia reaktora 3 Czarnobylskiej Elektrowni Atomowej.jpg', '今・中', 'なし', '3号機の制御室（2021年・右下の端に人の服の一部＝顔なし）'),
    'CR4': ('File:Sterownia reaktora 4 Czarnobylskiej Elektrowni Atomowej.jpg', '今・中', 'なし', '4号機の制御室（2021年・炉心の見取り盤・人なし）'),
    'CR4B': ('File:Physics student inside the Control Room of Unit 4 at Chernobyl NPP.jpg', '今・中', 'なし', '4号機の制御室（2025年・CC0）＝学生の写らない左の盤だけを切り出す（寄りの名＝左の盤）'),
    'SEL': ('File:Selsyny řídících tyčí.jpg', '今・中', 'なし', '制御棒の位置の計器（セルシン・×100cm の目盛り・1号機・2014年）'),
    'AZ5': ('File:Řízení jaderné části RBMK1000.jpg', '今・中', 'なし', '炉の制御盤の寄り（左に「АЗ-5」の箱・3号機・2019年・白衣の腕だけ）'),
    'R15': ('File:RIAN archive 305015 Leningrad nuclear power plant.jpg', '他所', '顔', 'レニングラード原発の主制御盤（2008年・運転員1人）'),
    'R11': ('File:RIAN archive 305011 Leningrad nuclear power plant.jpg', '他所', '遠景', 'レニングラード原発の炉の上（円い床＝管と制御棒の頭・2008年・職員は遠景）'),
    'R96': ('File:RIAN archive 341196 Kursk Nuclear Power Plant.jpg', '他所', '背中', 'クルスク原発の中央ホール（炉の上で作業する職員1人・顔はヘルメットで隠れる・2008年）'),
    'R09': ('File:RIAN archive 305009 Leningrad nuclear power plant.jpg', '他所', '遠景', 'レニングラード原発の原子炉の建屋（縦長・2008年・職員は遠景）'),
    'R94': ('File:RIAN archive 894445 Leningradskaya nuclear power plant.jpg', '他所', '背中', 'レニングラード原発の炉の上を見る職員（後ろ姿・2011年）'),
    'LENW': ('File:Leningrad Nuclear Power Plant 20JUL2010-4 (cropped to western reactor).jpg', '他所', 'なし', 'レニングラード原発の3・4号機の空撮（2010年）'),
    'LENN': ('File:Leningrad Nuclear Power Plant 20JUL2010-4 (cropped to northern reactor).jpg', '他所', 'なし', 'レニングラード原発の1・2号機の空撮（2010年）'),
    'IGA': ('File:Ignalina Nuclear Power Plant Units.jpg', '他所', 'なし', 'イグナリナ原発の2つの号機と2本の排気筒'),
    'IGB': ('File:Ignalina Nuclear Power Plant, Visaginas, Lithuania - 20080730.jpg', '他所', 'なし', 'イグナリナ原発の正面（夕方・2008年・CC0）'),
    'MX7': ('File:Csernobil makett 7.jpeg', '今・跡', 'なし', '爆発のあとの4号炉の模型（チェルノブイリの展示・2006年・ずれた炉のふた）'),
    'MEMF': ('File:Тим, хто врятував світ.jpg', '今・跡', 'なし', '消防士たちの碑「世界を救った人々へ」（チェルノブイリの町・2021年）'),
    'MIT': ('File:Chernobyl memorial.jpg', '今・跡', 'なし', 'モスクワ・ミチノ墓地の慰霊碑と墓（2013年）＝墓の名は⑤b で原寸'),
    'C486': ('File:Chernobyl nuclear power plant (38342070546).jpg', '今・跡', 'なし', '発電所の記念碑と新しい覆い（2017年）'),
    'C475': ('File:Chernobyl 10 (13511028923).jpg', '今・跡', 'なし', '建設中の新しい覆い・石棺の4号機・排気筒が水辺の向こうに並ぶ（2013年）'),
    'C3309': ('File:Construction of the new sarcophagus in Chernobyl.jpg', '今・跡', 'なし', '新しい覆いの赤い骨組みと4号炉（2013年）'),
    'C488': ('File:Chernobyl Nuclear Power Plant in 2006.jpg', '今・跡', 'なし', '森の向こうの石棺と排気筒（2006年）'),
    'C496': ('File:Chernobyl snow storm (31397711360).jpg', '今・跡', 'なし', '吹雪の中の石棺（2016年）'),
    'C27': ('File:Chernobyl - 39484641685.jpg', '今・跡', 'なし', '雪の森の黄色いバス（2018年）'),
    'C3319': ('File:New Safe Confinement Structure.jpg', '今・跡', 'なし', '組み立て中の新しい覆い（2016年6月）'),
    'C3290': ('File:Chernobyl nuclear disaster aftermath abandoned town of Pripyat 02.jpg', '今・跡', 'なし', 'プリピャチの団地の向こうに新しい覆い（2018年・CC0）'),
    'C3305': ('File:Chernobyl second sarcophacus 2018 hnapel 14a.jpg', '今・跡', 'なし', '記念碑（手と鐘）と完成した新しい覆い（2018年・CC0）'),
    'C3313': ('File:ISS-57 Chernobyl Nuclear Power Plant, Ukraine.jpg', '今・跡', 'なし', '宇宙から見た発電所（2018年・NASA）'),
    'C0': ('File:Chernobyl, fourth reactor bloc.JPG', '今・跡', 'なし', '4号機の石棺と排気筒（2008年）'),
    'C1': ('File:Reactor bloc of the Chernobyl Nuclear Power Plant.JPG', '今・跡', 'なし', '石棺の鉄骨と黄色い足場（2008年）'),
    'C2': ('File:Chernobylreactor.jpg', '今・跡', 'なし', '4号炉と石棺と排気筒（2007年）'),
    'C3': ('File:Chernobyl and Pripyat - June 2013.jpg', '今・跡', 'なし', '冷却水路と遠くの発電所のパノラマ（2013年・横長）'),
    'T143': ('File:Transmission towers for the transfer of electricity frame the damaged unit 4 reactor at Chernobyl (02710143).jpg', '今・跡', 'なし', '送電塔のあいだの4号機と排気筒（2010年・IAEA）'),
    'T157': ('File:The ventilation stack of the damaged unit 4 reactor at Chernobyl (02710157).jpg', '今・跡', 'なし', '4号機の排気筒の寄り（2010年・IAEA）'),
    'T138': ('File:The damaged unit 4 reactor and shelter at Chernobyl (02710138).jpg', '今・跡', 'なし', '冷却水路に映る4号機と排気筒（2010年・IAEA）'),
    'T155': ('File:The damaged unit 4 reactor and shelter at Chernobyl (02710155).jpg', '今・跡', 'なし', '排気筒と配管と線路の標識（2010年・IAEA）'),
    'T158': ('File:Chernobyl Unit 4 Reactor (02710158).jpg', '今・跡', 'なし', '石棺と排気筒の白黒の写真（2010年・IAEA）'),
    'NSC17': ('File:NSC-Oct-2017.jpg', '今・跡', 'なし', '4号機を覆った新しい覆い（2017年10月・森の向こう）'),
    'H01': ('File:Chernobyl second sarcophacus 2018 hnapel 01.jpg', '今・跡', 'なし', '冷却水路の先の新しい覆い（2018年）'),
    'H06': ('File:Chernobyl second sarcophacus 2018 hnapel 06.jpg', '今・跡', 'なし', '送電線ごしの新しい覆い（2018年）'),
    'H11': ('File:Chernobyl second sarcophacus 2018 hnapel 11.jpg', '今・跡', 'なし', '木立ごしの新しい覆い（2018年）'),
    'WBG': ('File:Autoradiography, grass sample after Chernobyl disaster in 1986.jpg', '後', 'なし', '西ベルリンの草の放射線写真（1986年5月14日）'),
    'R1': ('File:Onderzoek naar veranderde Radioactiviteit door RIVM na nucleaire ramp in Sovjet , Bestanddeelnr 933-6455.jpg', '後', '顔', 'オランダ RIVM の放射線の測定（1986年5月1日・オランダの通信社の写真・職員＝公的な任務）'),
    'CIA': ('File:Chornobyl radiation map.jpg', '文書', 'なし', 'CIA「Radiation Hotspots」の地図（1996年）'),
    'MX7_': None,
}
CM.pop('MX7_')

# ── 手元の物（②③ が取った USGS・報告書の PDF）＝code → (置き場, rights, basis, era, 何)
LOCAL = {
    'U1': ('ref/ep24/src/usgs/412_L.jpg', 'PD', 'アメリカ政府の著作物（USGS）', '前', 'Landsat 5 の1986年4月22日・29日の2枚（＋2015年）の掲示'),
    'U2': ('ref/ep24/src/usgs/0_4-29-1986_Chernobyl_Intro-label.png', 'PD', 'アメリカ政府の著作物（USGS）', '後', '1986年4月29日の自然色・注記つき'),
    'U4F12': ('ref/ep24/src/usgs/1986_USGS_Image_Data_of_the_Nuclear_Accident_Near_Chernobyl_Report1.pdf#19', 'PD', 'アメリカ政府の著作物（USGS Bulletin 1785・1987）', '文書',
              '図12（PDF 19頁・印刷14頁）＝TM バンド6・1985年6月6日／1986年4月22日／4月29日／5月8日（頁の画像で確かめた 10-22）'),
}
# ── 報告書・会議録の頁（引用＝© の物は無加工・額装）
PAGES = {
    'S1p34': ('INSAG-7（IAEA 1992）', 'ref/ep24/src/insag7_pub913e.pdf#34', '印刷24頁・6章の結論', '文字'),
    'S3p19+S1p62': ('ソ連の報告 Part I（1986年8月）p.19 と INSAG-7 付属書I p.62', 'ref/ep24/src/ussr_report_part1.pdf#19+ref/ep24/src/insag7_pub913e.pdf#62', '左右に並べる', '文字'),
    'S1p63': ('INSAG-7 付属書I 表I-I', 'ref/ep24/src/insag7_pub913e.pdf#63', '印刷53頁・7:10 ORM 13.2 の行', '文字'),
    'S2p39': ('GC(SPL.I)/3＝INSAG-1 の本文', 'ref/ep24/src/gc_spl1_3_insag1text.pdf#39', '表I の行', '文字'),
    'S1p28': ('INSAG-7', 'ref/ep24/src/insag7_pub913e.pdf#28', '印刷18頁・5.2.1', '文字'),
    'GCp43': ('GC(SPL.I)/3＝INSAG-1 の図1', 'ref/ep24/src/gc_spl1_3_insag1text.pdf#43', '出力・反応度・圧力の線（ソ連の作業文書の図4から・カラーのスキャン）', '図'),
    'S1p65': ('INSAG-7 付属書I 表I-I', 'ref/ep24/src/insag7_pub913e.pdf#65', '印刷55頁・1:23:43 と 01:24 Severe shocks の行', '文字'),
    'K19860507': ('国会会議録 1986-05-07 参議院 科学技術特別委員会 第6号', 'https://kokkai.ndl.go.jp/img/110413928X00619860507', '河野長官の答弁の頁（頁は⑤b で画像から決める）', '文字'),
    'S3p26': ('ソ連の報告 Part I（1986年8月）', 'ref/ep24/src/ussr_report_part1.pdf#26', '印刷22頁・第4章の違反の表', '文字'),
    'S2p18': ('GC(SPL.I)/3＝INSAG-1 の本文', 'ref/ep24/src/gc_spl1_3_insag1text.pdf#18', '要約・原因の文', '文字'),
    'S3p28': ('ソ連の報告 Part I（1986年8月）', 'ref/ep24/src/ussr_report_part1.pdf#28', '印刷24頁・改造の計画の中の止める棒の一文', '文字'),
    'S1p15': ('INSAG-7 の図1', 'ref/ep24/src/insag7_pub913e.pdf#15', '印刷5頁・止める棒（(a)・(b)）', '図'),
    'S1p41': ('INSAG-7 付属書I', 'ref/ep24/src/insag7_pub913e.pdf#41', '印刷31頁', '文字'),
    'K19861127': ('国会会議録 1986-11-27 衆議院 科学技術委員会', 'https://kokkai.ndl.go.jp/', '佐々木局長の答弁の頁（会議の番号と頁は⑤b で決める）', '文字'),
    'S1p127': ('INSAG-7 付属書II の図 II-3・II-4', 'ref/ep24/src/insag7_pub913e.pdf#127', '印刷117頁・出力の時間の変化（3200→1600）と残した棒の数の変化（計算）', '図'),
    'GCp142': ('GC(SPL.I)/3＝INSAG-1 の Fig.11', 'ref/ep24/src/gc_spl1_3_insag1text.pdf#142', '非常用の冷却の仕組みの図（横長のスキャン）', '図'),
    'S1p128': ('INSAG-7 付属書II の図 II-5', 'ref/ep24/src/insag7_pub913e.pdf#128', '印刷118頁・キセノンがたまるあいだの炉の高さごとの中性子（0:00・7:00・22:00・24:30）', '図'),
    'GCp140': ('GC(SPL.I)/3＝INSAG-1 の Fig.9', 'ref/ep24/src/gc_spl1_3_insag1text.pdf#140', '2つの系統・4台ずつの循環ポンプ・タービン7と8（横長のスキャン）', '図'),
    'S1p129': ('INSAG-7 付属書II の図 II-6', 'ref/ep24/src/insag7_pub913e.pdf#129', '印刷119頁・01:22:30 の制御棒の差し込みの深さ（cm）の炉心図', '図'),
    'S1p133': ('INSAG-7 付属書II の図 II-10', 'ref/ep24/src/insag7_pub913e.pdf#133', '印刷123頁・上から差す棒が反応を強める仕組み（吸収材・押しのけ棒・水）', '図'),
    'S1p141': ('INSAG-7 付属書II の図 II-15', 'ref/ep24/src/insag7_pub913e.pdf#141', '印刷131頁・止める仕組みの効き方（1：1986年4月26日の4号炉 ORM 7本）', '図'),
    'S1p138': ('INSAG-7 付属書II の図 II-13', 'ref/ep24/src/insag7_pub913e.pdf#138', '印刷128頁・昔の棒と改良した棒（寸法 cm）', '図'),
    'L1p8': ('チェルノブイリ・フォーラム『Chernobyl\'s Legacy』2006 の図1', 'ref/ep24/src/forum_legacy_2006.pdf#8', '印刷10頁・ヨーロッパのセシウム137', '図'),
    'L1p15': ('チェルノブイリ・フォーラム 図3', 'ref/ep24/src/forum_legacy_2006.pdf#15', '印刷17頁・子どもの甲状腺がん', '図'),
}
# ── フリー素材（Pexels・イメージ）＝id → 何（②③ の見本帳 s_pexels_1〜3 で代表画像を見た）
PEXELS = {
    '13188726': '森の向こうの地平線に新しい覆いの白いアーチ（ドローン）',
    '13188720': 'プリピャチの広い空撮',
    '12191470': 'プリピャチの観覧車',
    '12160827': '町の碑「ЧОРНОБИЛЬ」の今',
    '13188717': 'プリピャチのドローンの眺め',
    '13183773': 'プリピャチの空き家の建物の正面',
    '13188723': '捨てられた町のドローン（新しい覆いが写る区間を⑤b でコマから選ぶ）',
    '30560421': 'プリピャチの空撮',
}


def q(params):
    params = dict(params, format='json', formatversion='2')
    data = urllib.parse.urlencode(params).encode()
    last = None
    for i in range(6):
        try:
            req = urllib.request.Request(API, data=data, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # 429 などは間をあけて
            last = e
            time.sleep(5 * (i + 1))
    raise last


def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()


INSTITUTION = ('IAEA Imagebank', 'U.S. Geological Survey', 'NASA', 'CIA')


def clean_author(a):
    """作者の列＝人の名前（または投稿者の名前）だけにする。機関は空（出典の列に機関名を書く）。
    10-22：「from 地名」「ファイル名.jpg:」「- User: …」「URL」が混ざり、名前の網が地名や一般の語を拾った＝ここで外す"""
    a = strip(a)
    if not a or any(a.startswith(x) for x in INSTITUTION):
        return ''
    a = re.sub(r'https?://\S+', '', a)
    a = re.sub(r'^[^:]*\.(?:jpe?g|png|tif)\s*:\s*', '', a, flags=re.I)
    a = re.sub(r'\s+-\s+User:.*$', '', a)
    a = re.sub(r'\s+(?:from|for)\s+.*$', '', a)
    a = re.sub(r'\s*\((?:WT-shared)[^)]*\)', '', a)
    return a.strip(' .')


def iaea_titles():
    out = {}
    for ln in open(IAEA_LIST, encoding='utf-8'):
        m = re.match(r'IAEA (0279\d{4}) fl(\d+) ([^\t]+?) (\d+x\d+)\t(\S+)', ln)
        if m:
            out[m.group(1)[-2:]] = dict(num=m.group(1), flickr=m.group(2), dims_b=m.group(4), url_b=m.group(5),
                                        title='File:IAEA %s (%s).jpg' % (m.group(1), m.group(2)))
    # 記者会見の7点（Flickr の 0279 の一覧に無い・Commons の「Chernobyl Post-Accident Review Meeting」＝②③ の台帳の題）
    for num, fl in (('02790056', '5612555893'), ('02790057', '5612555629'), ('02790058', '5613134426'), ('02790059', '5613134174'),
                    ('02790060', '5612554949'), ('02790061', '5613133650'), ('02790062', '5613133306')):
        out[num[-2:]] = dict(num=num, flickr=fl, dims_b='', url_b='', title='File:IAEA %s (%s).jpg' % (num, fl))
    return out


def fetch_api(titles):
    res = {}
    for k in range(0, len(titles), 20):
        chunk = titles[k:k + 20]
        d = q(dict(action='query', titles='|'.join(chunk), prop='imageinfo|revisions', rvprop='content', rvslots='main',
                   iiprop='url|size|mime|sha1|extmetadata', iiurlwidth='3840',
                   iiextmetadatafilter='LicenseShortName|Artist|Credit|DateTimeOriginal|ImageDescription'))
        norm = {n['to']: n['from'] for n in d['query'].get('normalized', [])}
        for p in d['query']['pages']:
            t = norm.get(p['title'], p['title'])
            if p.get('missing'):
                res[t] = None
                continue
            ii = p['imageinfo'][0]
            em = ii.get('extmetadata', {})
            wt = ''
            if p.get('revisions'):
                wt = p['revisions'][0]['slots']['main'].get('content', '')
            # 許諾の札（{{self|PD-self}} の中の札も拾う＝PD の根拠3種を書き分けるため）
            lic_tpl = re.findall(r'(?<![\w-])((?:PD|Cc|CC)-[\w.-]+)', wt)
            res[t] = dict(w=ii['width'], h=ii['height'], size=ii['size'], mime=ii['mime'], sha1=ii['sha1'], url=ii['url'], thumb=ii.get('thumburl'),
                          page=ii['descriptionurl'], lic=strip(em.get('LicenseShortName', {}).get('value')), artist=strip(em.get('Artist', {}).get('value'))[:200],
                          credit=strip(em.get('Credit', {}).get('value'))[:200], dto=strip(em.get('DateTimeOriginal', {}).get('value'))[:40],
                          tpl=sorted(set(x.strip() for x in lic_tpl))[:6])
        time.sleep(2)
    return res


def get_mode(w, lic):
    """取り方＝原本の幅が3840超→3840／1920超→1920（BY-SA の額装は1920で足りる）／ほかは原本（記憶 reference-commons-standard-thumbnail-sizes）"""
    if w > 3840:
        return 'commons:3840'
    if w > 1920 and 'SA' in lic:
        return 'commons:1920'
    if w > 1920:
        return 'commons:3840' if w > 3840 else 'commons:orig'
    return 'commons:orig'


def credit_of(code, a):
    lic = a['lic']
    if code.startswith('I') and code[1:].isdigit():
        return 'IAEA Imagebank／Photo: USFCRFC（%s）' % lic
    if code.startswith('T') or code == 'CR3A':
        return 'IAEA Imagebank（%s）・撮影者は作者欄のとおり' % lic
    if code.startswith('R') and code[1:].isdigit():
        return 'RIA Novosti archive（%s）・撮影者は作者欄のとおり' % lic
    if code == 'C3313':
        return 'NASA（Public domain）'
    if code == 'P84':
        return 'アメリカの偵察衛星の写真（USGS EarthExplorer・Public domain）'
    if code == 'CIA':
        return 'CIA（Public domain）'
    if code == 'R1':
        return 'Nationaal Archief（オランダ国立公文書館・CC0）'
    return '写真：作者欄のとおり（src/credits_private.tsv）／%s' % lic


def main():
    offline = '--offline' in sys.argv
    iaea = iaea_titles()
    titles = [iaea[n]['title'] for n in IAEA] + [v[0] for v in CM.values()]
    if offline and os.path.exists(CACHE):
        api = json.load(open(CACHE, encoding='utf-8'))
    else:
        api = fetch_api(titles)
        json.dump(api, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    rows, private, E = [], [], []
    for n, (era, people, what) in IAEA.items():
        it = iaea[n]
        a = api.get(it['title'])
        code = 'I' + n
        if a:
            rows.append([code, 'commons', it['title'][5:], a['page'], get_mode(a['w'], a['lic']), '%dx%d' % (a['w'], a['h']), a['lic'], 'CC の許諾',
                         credit_of(code, a), era, people, '%s/%s.jpg' % (SRC, code), what])
        else:  # Commons に無い＝Flickr の大きい版（1024px）
            rows.append([code, 'flickr', 'IAEA %s（Flickr %s）' % (it['num'], it['flickr']), 'https://www.flickr.com/photos/iaea_imagebank/%s/' % it['flickr'],
                         'flickr:b', it['dims_b'], 'CC BY-SA 2.0', 'CC の許諾', 'IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）', era, people,
                         '%s/%s.jpg' % (SRC, code), what + '（Commons に版が無い＝Flickr の 1024px）'])
    for code, (t, era, people, what) in CM.items():
        a = api.get(t)
        if not a:
            E.append('Commons に無い：%s %s' % (code, t))
            continue
        basis = 'CC の許諾'
        if 'Public' in a['lic'] or 'PD' in a['lic'] or a['lic'] == 'CC0':
            basis = '・'.join(a['tpl']) or a['lic']
        ext = os.path.splitext(t)[1].lower().replace('.jpeg', '.jpg')
        rows.append([code, 'commons', t[5:], a['page'], get_mode(a['w'], a['lic']) if code != 'P84' else 'commons:orig(切り出し)', '%dx%d' % (a['w'], a['h']),
                     a['lic'], basis, credit_of(code, a), era, people, '%s/%s%s' % (SRC, code, ext), what + ('｜sha1 %s' % a['sha1'][:12])])
        if a['artist'] or a['credit']:
            private.append([code, t[5:], a['lic'], clean_author(a['artist']), a['credit'], a['page']])
    for code, (path, lic, basis, era, what) in LOCAL.items():
        rows.append([code, 'local', os.path.basename(path), '', 'local', '', lic, basis, 'USGS（Public domain）', era, 'なし', path, what])
    for code, (rep, path, what, kind) in PAGES.items():
        rows.append([code, 'page', rep, path if path.startswith('http') else '', 'page', '', '引用（頁）' if not code.startswith(('U', 'CIA')) else 'PD',
                     '著作権法32条（引用）＝無加工・出典', '出典：%s' % rep, '文書', 'なし', path, '%s｜%s' % (what, kind)])
    for pid, what in PEXELS.items():
        rows.append(['X' + pid, 'stock', 'Pexels %s' % pid, 'https://www.pexels.com/video/%s/' % pid, 'stock', '幅1920 の版', 'Pexels License', '無料・表示は不要・手直し可',
                     'イメージ（Pexels）', 'イメージ', 'なし', '%s/X%s.mp4' % (SRC, pid), what])
    head = ['code', 'type', 'title', 'page', 'get', 'dims', 'rights', 'basis', 'credit', 'era', 'people', 'file', 'note']
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 生成物＝手で直さない（make_sources24.py）。作者の名前は src/credits_private.tsv（git の外）だけ\n')
        f.write('|'.join(head) + '\n')
        for r in rows:
            f.write('|'.join(str(x).replace('|', '／').replace('\n', ' ') for x in r) + '\n')
    # 作者欄＝git の外へ足す（同じ code の行は置き換え）
    old = []
    if os.path.exists(PRIVATE):
        old = [ln.rstrip('\n') for ln in open(PRIVATE, encoding='utf-8')]
    keep = [ln for ln in old if not ln.startswith('e24:')]
    with open(PRIVATE, 'w', encoding='utf-8', newline='\n') as f:
        for ln in keep:
            f.write(ln + '\n')
        for p in private:
            f.write('e24:' + '\t'.join(str(x).replace('\t', ' ') for x in p) + '\n')
    print('sources24.psv %d 行（IAEA %d・Commons %d・手元 %d・頁 %d・Pexels %d）・作者欄 %d 行を git の外へ' % (
        len(rows), len(IAEA), len(CM), len(LOCAL), len(PAGES), len(PEXELS), len(private)))
    for r in rows:
        if r[1] in ('commons', 'flickr'):
            print('  %-6s %-10s %-11s %-14s %s' % (r[0], r[6][:10], r[5], r[4], r[7][:40]))
    for e in E:
        print('  E', e)
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main())
