# -*- coding: utf-8 -*-
"""第10章　船長のその後 cb01–cb07（7カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/cb.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep26/make_plan26.py` で
  映像方針の一覧 `ref/ep26/eizou_build/list26.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep26/eizou_list26.md`）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  🔴 額装・帯の写真は静止（26本目から＝`build_jiko.FRAME_STILL`）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  ⚠️ 人＝乗員・ほかの船の船長と航海士と通信士・審問の長は名前＋役職／会社の人とドンキーマンは役職だけ／乗客は名前なし（①・承認①）。
     名前の載る紙面・頁は注の「…外」のとおり寄る範囲から名前を外す
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'cb01': dict(kind='写真',
               plan='S3-675:引き｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号の船長スタンリー・ロード〈1912年5月・英国の審問のころ〉｜動き：引く｜権利：PD｜時期：後・審問｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（4回目・引き）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.19（`He lost his post with the Leyland Line, but soon gained employment with another British company`…`he remained at sea throughout the Great War and into the 1920s with that Company. He died in 1962. No formal action was ever taken against him`）'),
    'cb02': dict(kind='文字の頁',
               plan='🔧 P-G2-23:結び｜一覧の種類：頁｜見せ方：頁（引用・額装）｜副題：海難調査局の報告書 p.19〈1992年〉｜動き：静止｜見た目の型：文字の頁｜権利：引用（OGL v3.0 か Crown copyright か未確定）｜時期：文書｜人：なし｜出典の行：出典：英国運輸省 海難調査局『RMS "TITANIC" Reappraisal of Evidence Relating to SS "CALIFORNIAN"』（1992年）より引用｜注：⚠️ 頁の末の署名（次長の名前）は切り出しの外｜新しい画（映像方針）：🔧 寄る → 静止の切り出し（結びの段落・引用の型）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.19（`it is difficult not to believe that some at least of those responsible at the Board of Trade felt a substantial measure of doubt as to the justice of the findings`）'),
    'cb03': dict(kind='写真',
               plan='S1-084:船尾｜一覧の種類：実写｜見せ方：全面｜副題：クイーンズタウンのタイタニック号〈1912年4月11日・オランダ国立公文書館〉｜動き：寄る（船尾へ）｜権利：PD｜時期：前｜人：小さい（⑤b で原寸）｜出典の行：出典：オランダ国立公文書館（Spaarnestad Photo）｜新しい画（映像方針）：台本どおり（2回目・c205 と別の寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.19（`Neither party will be entirely satisfied with this Report`）'),
    'cb04': dict(kind='写真',
               plan='S6-480:漕ぐボート｜一覧の種類：実写｜見せ方：全面｜副題：4月15日の朝、海の上のボート〈1912年・BnF〉｜動き：左へ（漕ぐボートへ）｜権利：PD｜時期：後・救助｜人：遠景（⑤b で原寸）｜出典の行：出典：フランス国立図書館（BnF）｜新しい画（映像方針）：台本どおり（3回目・別の寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.19（`there are no villains in this story: just human beings with human characteristics`）'),
    'cb05': dict(kind='フリー素材',
               plan='X-sea-night｜映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・月の写らないもの・要る秒＝扉を除いた中身 11.82秒＝narration.json の実測）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜の海｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜新しい画（映像方針）：台本どおり（月の写らないもの）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`she might have saved many if not all of the lives`）・G2 p.3（`only 5 to 7 miles off`…`between 17 and 20 miles from TITANIC`…`I think it possible that she was seen`…`but more likely that she was not seen`）'),
    'cb06': dict(kind='写真',
               plan='S8-625:引き｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号〈カルパチア号の甲板から撮られたとみられる・NARA〉｜動き：引く｜権利：PD｜時期：後・救助｜人：なし｜出典の行：出典：米国立公文書館（NARA）｜新しい画（映像方針）：台本どおり（4回目・引き）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.14（`I entirely agree with him`）・G2 p.3（`proper action was not taken. I agree on both counts`）'),
    'cb07': dict(kind='写真',
               plan='S1-002:引き｜一覧の種類：実写｜見せ方：全面｜副題：出航するタイタニック号〈1912年4月10日・サウサンプトン〉｜動き：引く｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：共通エンディングの前の最後の1枚｜新しい画（映像方針）：台本どおり（2回目・引き）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='—'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-10-27）：フリー素材（Pexels・イメージ）＝`ss.vid`（見出し・副題は書かない＝左上の「イメージ」と出典だけ）
SPEC.update({
    "cb05": ss.vid("cb05"),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-28）：写真と頁（第10章の6カット）＝書き方は c2.py の ⑤b-7 の注と同じ
# ══════════════════════════════════════════════════════════
_S3675, _PG223, _S1084, _S6480, _S8625, _S1002 = P("s3_675"), P("p_g2_23"), P("s1_084"), P("s6_480"), P("s8_625"), P("s1_002")
SPEC.update({
    # cb01（3行）＝顔（x 0.57・y 0.35）から引く（c601・c622・c824 は寄る）
    "cb01": dict(photo=_S3675, **ss.mv(_S3675, "out", fx=0.57, fy=0.35, z=1.4), side="none", color=1.0,
                 t="処分は一度も無い", s="カリフォルニアン号の船長スタンリー・ロード〈1912年5月・英国の審問のころ〉"),
    # cb02（2行）＝p.19 の結びの段落（引用＝束の段で頁の末の署名の場所を外した）＝額装・静止
    "cb02": dict(photo=_PG223, panel=True, pw=1640, color=1.0,
                 t="疑っていた人", s="結びの段落"),
    # cb03（1行）＝c205 と同じ写真・同じ副題＝船体に沿って船尾（右）へ流す（c205 は船尾の字へ寄る）
    "cb03": dict(photo=_S1084, **ss.mv(_S1084, "r", fy=0.52, span=(0.3, 0.9)), side="none", color=1.0,
                 t="満足しきれない", s="クイーンズタウンのタイタニック号〈1912年4月11日・オランダ国立公文書館〉"),
    # cb04（2行）＝帆のボート（x 0.68）から漕ぐボート（x 0.33・y 0.35）へ左に流す（c104 は右へ・c641 は帆のボートへ寄る）
    "cb04": dict(photo=_S6480, **ss.mvz(_S6480, (0.62, 0.42, 1.4), (0.39, 0.38, 1.4)), side="none", color=1.0,   # 終わりの真ん中 x 0.39＝左の黒い縁 2.1% に窓を当てない
                 t="悪者はいない", s="4月15日の朝、海の上のボート〈1912年・BnF〉"),
    # cb06（2行）＝真ん中から引く（c102 は右へ・c605 は左へ・c811 は煙突とマストへ寄る）
    "cb06": dict(photo=_S8625, **ss.mv(_S8625, "out", fx=0.5, fy=0.5, z=1.3), side="none", color=1.0,
                 t="2人が認めたこと", s="カリフォルニアン号〈カルパチア号の甲板から撮られたとみられる・NARA〉"),
    # cb07（2行）＝最後の1枚（共通エンディングの前）＝c101 の船首から引く
    "cb07": dict(photo=_S1002, **ss.mv(_S1002, "out", fx=0.80, fy=0.56), side="none", color=1.0,
                 t="あなたへの問い", s="出航するタイタニック号〈1912年4月10日・サウサンプトン〉"),
})
