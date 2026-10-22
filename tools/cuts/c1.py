# -*- coding: utf-8 -*-
"""つかみ c101–c107（7カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

■ 🆕 2026-10-22（⑤b-1）：新しいファイル。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep24/make_plan24.py` で
  映像方針の一覧 `ref/ep24/eizou_build/list24.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep24/eizou_list24.md`）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  ⚠️ 「関連（参考＝…）」と書いたカットは同じ型のほかの発電所の炉の写真（種類は写真・20% の数〈この発電所・この事故の写真〉には入れない・
     門番 check_text_screens が束の台帳 assets.json の related と照らす）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c101': dict(kind='フリー素材',
               plan='X13188726:原発｜映像の素材 25.05秒・倍率 3.00（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：現在のチェルノブイリ原発（Pexels）｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：台本どおり。森の向こうの地平線に新しい覆い（②③ の見本帳）。⑤b で使う区間を焼いて字と人を見る｜⑤b-2（10-22）：地平線の帯を原寸で4時刻見た＝全時刻で左に新しい覆いと排気筒・前のショット（0〜15秒）を使う（cb23 は後のショット）＝寄りの名「原発」｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='K1 1986-05-07 参院 科学技術特別委・河野洋平 科学技術庁長官（`五月三日に至り、東京都、千葉県、神奈川県におきまして`）・K1 1986-05-08 衆院 農林水産委・今村治 室長（`五月三日以降採取した浮遊じん、雨水等の核種分析の結果`）'),
    'c102': dict(kind='写真',
               plan='U1｜一覧の種類：実写｜見せ方：全面｜副題：事故の前（4月22日）と後（4月29日）の衛星写真（USGS）｜動き：寄る（2枚を重ねて切り替える）｜権利：PD｜時期：前｜人：なし｜出典の行：USGS（Public domain）｜注：台本どおり。PD＝全面で寄る｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='U1（USGS「Landsat Chernobyl」）・S3 p.21／17（`at about 1:24 there occurred two explosions one after the other`）'),
    'c103': dict(kind='写真',
               plan='I15｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：壊れた4号炉（1986年4月）｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり。Commons の大きい版（1328×2040）。撮影日は Flickr「翌日にヘリから」と Commons「4月26日」が割れる＝副題は「4月」まで｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src="S2 p.18／~13（`the accident was eaused by a remarkable range of human errors`・`in combination with specific reactor features which compounded and amplified the effects of the errors`）・S2 p.112／~105（`is to be found in the so-called 'human element'`）"),
    'c104': dict(kind='文字の頁',
               plan='S1p34｜一覧の種類：頁｜見せ方：頁｜副題：1992年の報告（INSAG-7）の結論の頁｜動き：寄る（「違反ではなかった」の行へ）｜見た目の型：文字の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7（IAEA 1992）｜注：台本どおり＝語りが名指しする所｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`were in fact not violations`）'),
    'c105': dict(kind='写真',
               plan='I36｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：壊れた4号炉とヘリコプター（1986年）｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.53／43（`during the physical startup of Ignalina Unit 1 and that of Chernobyl Unit 4`・`almost two-and-a-half years before the Chernobyl accident`）'),
    'c106': dict(kind='写真',
               plan='I24｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：壊れた4号機と排気筒（1986年）｜動き：額ごと上へ｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（人は写らない＝責める行でも可）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`critical actions of the operators were most ill judged`）'),
    'c107': dict(kind='フリー素材',
               plan='X13188720｜映像の素材 7.89秒・倍率 1.19（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：現在のプリピャチ（Pexels）｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：台本どおり → 第1章の扉（頭の c201 が BY-SA＝扉は方眼だけ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.33／23（`It is not known for certain what started the power excursion`）'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-2（2026-10-22）：つかみ c101〜c107＝実写と頁とイメージの映像だけ（映像方針 §3・了承②）
# ══════════════════════════════════════════════════════════
#   フリー素材（c101・c107）は `ss.vid`＝区間は `footage.USE`（`qa_out/ep24_assets.py use`＝STOCK_WINDOW・地平線の帯を原寸で見て決めた）・
#   見出し・副題は書かない（左上の「イメージ」と出典だけ）。BY-SA（IAEA 0279＝c103・c105・c106）は額装・無加工・額ごと動かす（`ss.fm`＝check_frame_only）。
#   見出し（t）は語りの丸写しにしない話題の札（門番 echo）・つかみは章の札なし（c107 のあとに第1章の扉）。副題（s）は一覧 `list24.tsv` の sub（写っているもの）
#   ＝⑤b-2 の試し焼きを原寸で見て最終に
_U0422, _U0429, _PAGE = P("u1_0422"), P("u1_0429"), P("s1p34")
SPEC.update({
    # c101（2行・8.4秒）＝Pexels 13188726 の前のショット（森の向こうの地平線に新しい覆いと排気筒＝⑤b-2 に地平線の帯を原寸で4時刻見た）
    "c101": ss.vid("c101"),
    # c102（2行）＝USGS の掲示の左の欄（1986年4月22日・冷却池の温かい水の帯＝橙〜黄）を寄る → 2行目「4月26日、4号炉が爆発で…」で
    #   真ん中の欄（4月29日・池の水が同じ温度の青＝運転が止まった）へ切り替える（尻の差し込み）。欄の日付は掲示の字（Landsat 5）
    "c102": dict(photo=_U0422, **ss.mv(_U0422, "in", fx=0.55, fy=0.42, z=1.25), side="none", color=1.0,
                 t="チェルノブイリ原子力発電所", s="事故の前の衛星写真（1986年4月22日・USGS）",
                 tail=dict(photo=_U0429, at=1, color=1.0, t="爆発の3日後", s="事故の後の衛星写真（1986年4月29日・USGS）")),
    # c103（3行）＝IAEA 02790015（壊れた4号炉・縦長・BY-SA 2.0）＝額ごと寄る
    "c103": dict(photo=P("i15"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="最初の結論", s="壊れた4号炉（1986年4月）"),
    # c104（2行）＝INSAG-7 p.34（印刷24頁）の (6) の段落の頭から8行（「in fact not violations」の文と、c106 で読む「most ill judged」の文を含む）
    #   ＝`qa_out/ep24_assets.py pbox S1p34 "(6)" "element in causing the accident"` が測った切り口（行は字の層で選び、上下の辺は束の絵の
    #   OCR の行のすき間でインクがいちばん少ない行）。引用＝無加工・額装・印は額の外（映像方針 §6-5）。
    #   ⚠️ ⑤b-2 の初めの切り口（下 0.344）は9行目の字の頭を額の下の辺で切っていた（試し焼き `39774051396` の at_c104_030 で見た・門番 edges は
    #   OCR の箱で 7.5%＜下限 8% を「外」と数えて通した）
    "c104": dict(photo=_PAGE, trim=(0.004, 0.184, 0.996, 0.340), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="見直された判断", s="1992年の報告（INSAG-7）の結論の頁"),   # 「INSAG-7 の結論」は出典の行の写し（門番 dup）
    # c105（2行）＝IAEA 02790036（壊れた4号炉の前を飛ぶヘリ・1986年6月13日）＝額ごと右へ
    "c105": dict(photo=P("i36"), panel=True, color=1.0, fmove=ss.fm("r"),
                 t="もう1つの原因", s="壊れた4号炉とヘリコプター（1986年）"),
    # c106（3行・1行目は聞き役の問い＝赤）＝IAEA 02790024（片づけの最初の班が見た壊れた4号機と排気筒・人は写らない＝責める行でも可）＝額ごと上へ
    "c106": dict(photo=P("i24"), panel=True, color=1.0, fmove=ss.fm("u"),
                 t="残った指摘", s="壊れた4号機と排気筒（1986年）"),
    # c107（2行・6.6秒）＝Pexels 13188720（プリピャチの広い空撮・1ショット）→ 第1章の扉
    "c107": ss.vid("c107"),
})
