# -*- coding: utf-8 -*-
"""第10章　海の底の593 ca01–ca23（23カット）。18本目（スレッシャー号のリメイク）。

■ 🔴 2026-10-04（⑤b-1）：16本目（バイオントダム災害）の中身を空にした＝git の `b044b56`（`git show b044b56:tools/cuts/ca.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep18/make_plan.py` で
  台本 §4・承認ずみの映像方針（§1-3 冒頭・§3 置き場・§4 合図・§5 案C・§6 前置き・§8 記録映画・§9 頁の版・§11 替える画）から
  機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」と「フリー素材」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所／フリー素材（ルール §5b-79・§2-5c）
  記号＝【案C SA】横から見た海・【案C SB】上から見た海（北が上）・【案C SC】上から見た海の底・【案C SD】横から見た海の底の捜索（§3）・
        【冒頭】（§1-3）・【混ざり】（§12 ⑦）
  🆕 フリー素材の映像（映像方針 §17）＝⑤b-7 で替える場面を表にして承認 → その種類を「フリー素材」に（20% と【映像あり】に数えない）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    "ca01": dict(kind='写真',
               plan='台本の画：実写 NARA 83737（1963年の捜索の記録映画・ケープコッドの東の海の艦）',
               src='J p.169（1964-02 の海軍長官の資料）'),
    "ca02": dict(kind='図解',
               plan='台本の画：図 地図 1963年の捜索の海域（基準の点〈北緯41度45分・西経65度〉を中心にした四角＝音で海の深さを測って探す・広さの数は出さない〈原文は 10 miles by 10 miles＝マイルの種類が書いていない〉）',
               src='R08 p.65〜66（アンドリュース大佐の証言）'),
    "ca03": dict(kind='写真',
               plan='台本の画：実写 NARA 83751（空からの捜索の記録映画・並んで進む艦）',
               src='R08 p.65〜66（アンドリュース大佐の証言＝LORAN-A は a mile and a half より近くは分からない／のちに DECCA と LORAN C に替えて far more accurate）'),
    "ca04": dict(kind='図解',
               plan='台本の画：図 書類の再現図 捜索の指揮官の証言（写すのはやさしい／難しいのは、潮で揺れるカメラを狙った物の約9メートル以内に置くこと＝高さ約2,600メートルの飛行機から、糸の先のカメラを寄せるようなもの）',
               src='R08 p.66（アンドリュース大佐の証言）'),
    "ca05": dict(kind='写真',
               plan='台本の画：実写 thr_t39（1963年・ラモント研究所の調査船コンラッドが撮った外殻の板・札は切る）',
               src='R08 p.169〜170（ウォーゼル副所長の証言）'),
    "ca06": dict(kind='写真',
               plan='台本の画：実写 Commons 330-PSA-110-63（USN 711302・1963年のセピアの海の底の破片＝アトランティス2世のカメラ）＋札「別の調査船が撮った海の底（1963年）」＝語りの重りの写真ではない（コンラッドの写真〈証拠241〜245〉に替えられるかは⑤b）',
               src='R08 p.171（ウォーゼル副所長の証言）'),
    "ca07": dict(kind='写真',
               plan='台本の画：実写 NARA 83759（ボストンの造船所・艦番号422の在来型の潜水艦トロ）',
               src='R08 p.67（アンドリュース大佐の証言）・R17 p.250（OCR）'),
    "ca08": dict(kind='写真',
               plan='台本の画：実写 NARA 83795（1963-06-29 現場の海の初代トリエステ・甲板に人）',
               src='J p.169・R08 p.84'),
    "ca09": dict(kind='写真',
               plan='台本の画：実写 NARA 83766（ボストンの造船所・赤と白の縞に塗った初代トリエステ）',
               src='J p.169・J p.30（1963-06-27 の公聴会＝前の日の潜航は No results）'),
    "ca10": dict(kind='写真',
               plan='台本の画：実写 Commons 330-PSA-191-63（USN 711348・艦の中の水密扉＝1963年8月の潜航の写真）',
               src='Commons の説明文（1963年の海軍の発表＝艦内の水密扉・1963-08-24・2回目の一連の潜航＝⑤bで説明文と写りを原寸で）・J p.186（second series of dives）'),
    "ca11": dict(kind='写真',
               plan='台本の画：実写 Commons 330-PSA-191-63（USN 711350・トリエステが回収した真鍮の管・刻印「593 Boat」）',
               src='J p.169・p.186（付録16 の図1）'),
    "ca12": dict(kind='写真',
               plan='台本の画：実写 NARA 83757（トリエステの試験潜航の記録映画・1963-05-03・海上のトリエステ）',
               src='J p.169・Commons の説明文'),
    "ca13": dict(kind='写真',
               plan='台本の画：実写 thr_t5（1963年・初代トリエステが撮った艦首の外板の喫水の数字・札は切る）＋画の札「外側の板（1963年・初代トリエステ）」',
               src="J p.169（no part of Thresher's pressure hull was sighted or photographed）"),
    "ca14": dict(kind='写真',
               plan='台本の画：実写 Commons 330-PSA-309-64（KN-9302C・海の上のトリエステ2世＝場所は名乗らない）',
               src='No.710-64（1964-10-01・原寸）'),
    "ca15": dict(kind='文字の頁',
               plan='台本の画：図 p9801（国防総省の発表 No.710-64 の紙・1964-10-01）',
               src='No.710-64（1964-10-01・原寸）'),
    "ca16": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='No.710-64（1964-10-01・原寸）'),
    "ca17": dict(kind='写真',
               plan='台本の画：実写 Commons 330-PSA-276-63（USN 711389・トリエステ2世の想像図・海軍の公式の絵）',
               src='No.710-64'),
    "ca18": dict(kind='写真',
               plan='台本の画：実写 Commons 330-PSA-309-64（USN 1104636-D・ミザーから降ろされる曳航カメラ「The Fish」）',
               src='No.710-64（2頁目＝the underwater camera-magnetometer array・G0 が画像で確かめた）・R17 p.97 の要旨（T p9802＝an unmanned vehicle which is remotely controlled and towed from a surface ship）'),
    "ca19": dict(kind='再現イラスト',
               plan='【案C SC 上から見た海の底】ca19 900個の目印（数えない形・枠の外まで続く）＋札「目印900個（国防総省の発表 No.710-64）」・広さの数は描かない（"1,200 square yard field" の読みが2通り）（映像方針 §5）｜合図（映像方針 §4 #4・ca18 から）：向きの札「上から見た海の底」だけ（前のカットが写真＝向きの切り替えではない）',
               src='No.710-64（2頁目・原寸＝G0 が画像で確かめた："a distinctively lettered and numbered two-foot nylon line and a heavy weight"・"900 markers by which TRIESTE II could locate herself"）'),
    "ca20": dict(kind='写真',
               plan='台本の画：実写 thr_t41（1964年・トリエステ2世が海の底に残した跡＝捨てたおもりの点と引きずった跡）',
               src='No.710-64・materials §5-1'),
    "ca21": dict(kind='再現イラスト',
               plan='【案C SC 上から見た海の底】ca21 直径 約370mの円＝札は「この円より広くない」（原文 "certainly no greater than a circle of diameter 400 yd"）・大きな塊は §2① の条件（映像方針 §5）｜⚠️ 大きな塊は R17 の Plate（形のもと）があるときだけ描く（無ければ円と札だけ＝映像方針 §2①）',
               src='R17 p.97（海軍研究所の報告の要旨・原寸）'),
    "ca22": dict(kind='再現イラスト',
               plan='【案C SD 横から見た海の底の捜索】ca22 SD（合図 #5）＝ミザー・The Fish・トリエステ2世・案内索のおもり（形のもと＝USN 1104636-D・USN 711389。⚠️ ミザーの横の形の PD の写真は台帳に無い＝⑤b-1 で探す・無ければ「船（模式）」の札）（映像方針 §5）｜合図（映像方針 §4 #5・ca21 から）：「横から見ると」・小さな地図（SC を縮めたもの）に切り口の線と目の印',
               src='R17 p.97（原寸）'),
    "ca23": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='R17 p.97（海軍研究所の報告の要旨・原寸）'),
}

SPEC = {
    # ── 🆕 ⑤b-3（2026-10-04）：案C の置き場 SC（上から見た海の底）・SD（横から見た海の底の捜索）＝`tools/illu.py` の「18本目 ⑤b-3」の節 ──
    # ca19（0〜3.52／4.01〜6.85／7.34〜9.74）＝合図 #4（ca18 は写真＝向きの札だけ）。目印900個（No.710-64）＝数えない形（枠の外まで
    #   続く・並びと間隔は模式・広さの数は描かない）→ 2行目：目印1つの拡大（文字と番号を付けたナイロンの綱と重り＝模式）→ 3行目：札だけ
    "ca19": dict(
        fig=("illu", dict(
            place="SC", start=dict(), rec="R17書 p9802（1964年の海の底）",
            steps=[dict(state=dict(mk="on"), delay=0.3, rec="No.710-64 p9801（a 1,200 square yard field of 900 markers）",
                        tag=dict(t="目印900個（国防総省の発表 No.710-64）", xy=(960, 196), anchor="middle", keep=True)),
                   dict(state=dict(mkx="on"), delay=0.2, rec="No.710-64 p9801（文字と番号を付けたナイロンの綱と重り）",
                        tag=dict(t="綱と重り", at="xtop", off=(0, -24), anchor="middle", keep=True)),
                   dict(rec="No.710-64 p9801（900 markers by which TRIESTE II could locate herself）",
                        tag=dict(t="目印で位置を知る", xy=(960, 820), anchor="middle"))])),
    ),
    # ca21（0〜3.74／4.23〜5.77／6.26〜9.90）＝R17 p.97「the hulk has broken into five or six large pieces, and many small pieces, with
    #   all major debris lying in an area certainly no greater than a circle of diameter 400 yd」。🔴 「5つか6つ」は数が1つに決まらない＝
    #   大きな塊は描かない（円と札だけ＝映像方針 §2①・⑤b-3 の決め）。円は縮尺どおり（直径 約370m＝1画素 1.5m で 244画素）
    "ca21": dict(
        fig=("illu", dict(
            place="SC", start=dict(), rec="R17書 p9802（1964年の海の底）",
            steps=[dict(state=dict(circ="on"), delay=0.3, dur=1.6,
                        rec="R17書 p9802（the hulk has broken into five or six large pieces・all major debris … circle）",
                        tag=dict(t="大きな塊　5つか6つ", at="center", off=(-330, -150), anchor="end", keep=True)),
                   dict(rec="R17書 p9802（and many small pieces）",
                        tag=dict(t="小さな破片も　たくさん", xy=(960, 760), anchor="middle", keep=True)),
                   dict(state=dict(dia="on"), delay=0.3, rec="R17書 p9802（certainly no greater than a circle of diameter 400 yd）",
                        tag=[dict(t="直径 約370m", at="dia_mid", off=(0, -38), anchor="middle"),
                             dict(t="この円より広くない", at="edge_r", off=(60, 90))])])),
    ),
    # ca22（0〜4.30・1行）＝合図 #5（ca21 の SC から）：左上の小さな地図（SC を縮めたもの）に切り口の線と目の印（切り替えの字は出さない＝
    #   語りが「横から見ると」と言う）。ミザーが音で位置を伝え、トリエステ2世が船体の一部の真上に着く（R17 p.97）。人は描かない・
    #   The Fish と案内索のおもりは描かない（語りに無い・同じ時刻に動いていた記録が無い）。深さは切れ目（≈）で縮める
    "ca22": dict(
        fig=("illu", dict(
            place="SD", start=dict(mini="SC", tri="down"), rec="R17書 p9802（1964年・MIZAR と TRIESTE II）",
            steps=[dict(state=dict(tri="on"), delay=0.2, dur=2.6, track=2, ring_delay=0.2,
                        rec="R17書 p9802（TRIESTE II, conned in by acoustic tracking information furnished by MIZAR, "
                            "was able to locate on top of a portion of the THRESHER hull）",
                        tag=[dict(t="ミザー", at="mizar", off=(-60, -40), anchor="end", delay=2.2),
                             dict(t="トリエステ2世", at="tri", off=(60, -40), delay=2.2),
                             dict(t="船体の一部", at="hull", off=(60, 10), delay=2.2)])])),
    ),
}
