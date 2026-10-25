# -*- coding: utf-8 -*-
"""21本目（米国同時多発テロ〈9.11〉のリメイク・2001-09-11・9.11委員会の報告書と NIST・NTSB の記録の動画）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-10-14（22本目 タイタン号のリメイク ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `35fab37` と同じ）
  ・`cuts/ss.py` の21本目の値＝案C の出典の表（REC_DOCS＝委員会報告・図表・スタッフ声明・NTSB 11便／175便／77便／93便・CVR・NIST・運輸長官の証言・国立公園局・AP・
    法律・検視局・記念館・運輸省の監察総監の報告・RG237・NIST 1-6・委員会報告の序文・govinfo の20資料）・割れる時刻（ILLU_SPLIT_TIMES＝8:46:40・9:03:11・
    9:37:46・10:03:11）・軸の型（AX_MORN・AX_11・AX_HIST・AX_175・AX_93・AX_ORD・AX_ALL・AX_TESTI・AX_HIT1・AX_AFTER・AXI の項目・AXIS_DOCS＝NIST の2つの巻の名）・
    棒（QG＝alert・faa／QB＝alert_cw・alert_911・faa11・faa175）・原寸で見て字でないと決めた OCR の範囲（OCR_NOT_TEXT＝wtc_far_1976・
    flight93_memorial_aerial_2024_12 の2点）（21本目 ⑤b-3〜⑤b-7）。ILLU_CROWD_UNTIL ほか空のままだった案C の表（ILLU_ROLES・ILLU_SEC_OK・ILLU_CLOCK_OK・
    ILLU_COUNTS・ILLU_ASSUME・ILLU_DESTROY_CUTS・ILLU_TOP_NOSCALE・ILLU_SUB_*・ILLU_BOOM_CUTS・ILLU_MIX_TODO・ILLU_MIX_BUNDLE）も、21本目の状態として持つ
    （20本目の見本と同じ考え方）
  ・`titan_fig.GEO` の21本目の地点＝**無い**（21本目は地点の鍵を足さなかった＝`35fab37` の `titan_fig.GEO` は `b1ecd46`〈20本目の値を移した直後〉と同じ
    〈差分は模式図 `m21` の関数だけ〉。模式図 mech21 は自分の表 `MAP_PTS` で地図を描く）。GEO は空の表のまま持つ（15・16・18・19・20本目の見本と同じ作り＝apply/restore の対称）
  ・門番の記録の表（check_axis＝REC_AXIS・LANES_OK・REC_APPROX・REC_LANE・REC_WRONG／check_qty＝REC_QTY／check_mech＝REC_M21）。
    ORDER_REF_MIN は21本目も使わなかった＝空（None）の状態として持つ。check_boxes（REC_*）・check_illu（REC_S1〜REC_S7 ほか）は21本目で足した値が無い
    （git の `b1ecd46`〜`35fab37` で両ファイルの差分は0）＝この見本の GATES に載せない
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を21本目の実物でも確かめている＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は22本目の空の器にした
  （fixture_ep14・fixture_ep15・fixture_ep16・fixture_ep18・fixture_ep19・fixture_ep20 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep21
      fixture_ep21.apply(sys.modules[__name__])   # その処理の中だけ ss・GEO・この門番の記録の表が21本目になる
      try: …（検算）
      finally: fixture_ep21.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14・15・16・18・19・20本目の見本と重ねるとき（check_mech は14本目の検算と15・16・18・19・20・21本目の検算を1つの処理で回す）は
      fixture_ep21.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss・GEO は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと22本目以降の画に21本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。
■ 注意:
  ⚠️ 見本の頁の原文 `ref/ep21/src/ep21_pages.txt` は git の外（本線の作業ツリーにだけある）＝無いときは頁の照合を飛ばす
     （check_illu の `_pages()` が None を返す）。
  ⚠️ 21本目の selftest（`check_mech._selftest_m21`・`check_axis.selftest_ep21`・`check_qty.selftest_ep21`）は**章ファイルの SPEC を読まない**
     （場面・図は selftest の中で `F.m21`／`ss.ax`／`ss.qb` で組む）＝`apply()` だけで通る。それでも `apply_cuts()`（21本目の章ファイルを git の `CUTS_SHA`＝
     `35fab37` から取り出して `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ21本目に入れ替える・git が無い所では止める＝fail closed）を用意した＝
     21本目の実物の絵を門番にかけ直したいとき（`restore()` で22本目へ戻る・LIFO）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep21/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は21本目の道を持つ。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝21本目は 1.02）は見本に入れない（16・18・19・20本目の見本も入れていない）＝本番の ss は
     今の値のまま残し、22本目の束で取り直す。
  ⚠️ 写真の束の定数（`SLIDE_MOUNT`＝スライドの台紙の縁がある写真の名簿・`TRIM`・`NEEDS_MASK`・`PRIVATE_OUT`）は見本に入れない（前の回までと同じく、
     束の名〈ref/ep21 の写真の名〉に結んだ定数＝22本目の束のチャットが替える。`NEEDS_MASK`・`PRIVATE_OUT` は21本目も空のまま）。
  ⚠️ `check_mech._M21_NEED`（模式図 m21 の「先に起きることが先」の筋の表）は**見本に入れず本番の check_mech に残した**（理由は check_mech の `REC_M21` の注）：
     見え方〈view〉と欄の名の約束＝mech21 の型の側の規則で、記録の値を持たない（20本目の `judge_m20` の ① 筋が本番のコードに残っているのと同じ扱い）。
     `NUM_M21`（札の数と時刻を拾う正規表現）も型。
  ⚠️ `check_axis.REC_WRONG`（×の印を置いてよい値＝記録が「誤り」とした値）は21本目が足した表＝この見本の GATES["check_axis"] に入れた。
     14〜20本目の見本には無い鍵＝それらを重ねても本番の REC_WRONG（空）は触られない。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep21"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：案C の再現イラスト（`tools/illu.py`・門番 `check_illu`）── 21本目 ⑤b-3〜⑤b-6
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：次の回は下の表を**その回の資料と時刻**に替える（頁の番号の書き方・資料の名の決め方は REC_DOCS の注）。
#   REC_PAGES … 部品の出典（`rec=`）を当てる原文（`=== p<N> ===` で頁を割った1ファイル＝④ の make_pages.py の出力）
#   REC_DOCS  … 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面に出す名前・頁の出し方（print＝印字の頁／pdf＝PDF の頁）
#   ILLU_* … 21本目は人・秒の札・時計の札・描いてよい数・想定の札・壊れる物・縮尺を持たない上から見た絵・潜水艦・音の輪・混ざりのつなぎ待ちを使わなかった＝
#            空のまま（下の値）。割れる時刻（ILLU_SPLIT_TIMES）だけ使った
REC_PAGES = REF / "src" / "ep21_pages.txt"      # ④ の make_pages.py の出力（git の外＝手元だけ）
# 🆕 2026-10-12（21本目 ⑤b-3）：21本目の資料の表（台本 第2版の出典の欄の書き方＝`v2_build/quotes21v2.py` の札の名）。
#    頁の番号＝**通し番号**（1つの番号の並びに資料を並べる＝`ref/ep21/make_pages21.py` が同じ番号で `REC_PAGES` を書く）：
#      委員会報告＝印字の頁そのまま（GPO の PDF＝印字＋18）・図表＝同じ報告書の p32〜33 の図（文字の層なし＝②が原寸で読んだ写し）・
#      スタッフ声明 No.17＝1000＋PDF の頁・NTSB の飛行経路の調べ＝11便 2000＋／175便 3000＋／77便 4000＋／93便 5000＋（PDF の頁・スキャン）・
#      93便の CVR の逐語（P200056T）＝6000＋・NIST NCSTAR 1＝7000＋（PDF の頁）・運輸長官の証言（写し）＝8001・ウェブの写し（頁なし）＝p1・
#      RG237＝FAA のレーダーの再生の動画（頁なし＝p1）
#    画面の出典の行＝`illu.rec_line`（印字＝「20頁」・pdf＝「PDF 3頁」・None＝名だけ）。⚠️ 台本の頁（「NTSB 11便」は頁なし）は SPEC で通し番号に直して書く
REC_DOCS = {                                # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
    "委員会報告": dict(range=(1, 567), name="9.11委員会報告書（2004年）", page="print", base=0),
    "図表": dict(range=(32, 33), name="9.11委員会報告書（2004年）の図", page="print", base=0),
    "スタッフ声明": dict(range=(1001, 1029), name="9.11委員会 スタッフ声明 第17号（2004年）", page="pdf", base=1000),
    "NTSB 11便": dict(range=(2001, 2006), name="NTSB 11便の飛行経路の調べ（2002年）", page="pdf", base=2000),
    "NTSB 175便": dict(range=(3001, 3007), name="NTSB 175便の飛行経路の調べ（2002年）", page="pdf", base=3000),
    "NTSB 77便": dict(range=(4001, 4007), name="NTSB 77便の飛行経路の調べ（2002年）", page="pdf", base=4000),
    "NTSB 93便": dict(range=(5001, 5007), name="NTSB 93便の飛行経路の調べ（2002年）", page="pdf", base=5000),
    "CVR": dict(range=(6001, 6009), name="93便の操縦室の音声記録の逐語（裁判の証拠 P200056T）", page="pdf", base=6000),
    "NIST": dict(range=(7001, 7302), name="NIST NCSTAR 1（2005年）", page="pdf", base=7000),
    "運輸長官の証言": dict(range=(8001, 8001), name="運輸長官の証言（2003年5月23日・9.11委員会の公聴会）", page=None, base=0),
    "国立公園局": dict(range=(1, 1), name="米国立公園局（93便の国立記念碑）", page=None, base=0),
    "AP": dict(range=(1, 1), name="AP通信（2001年9月17日）", page=None, base=0),
    "法律": dict(range=(1, 1), name="米国の法律 107-71（2001年）", page=None, base=0),
    "検視局": dict(range=(1, 1), name="ニューヨーク市の検視局", page=None, base=0),
    "記念館": dict(range=(1, 1), name="9.11記念館", page=None, base=0),
    "運輸省の監察総監の報告": dict(range=(1, 1), name="米運輸省の監察総監の報告 CC-2006-085（2006年）", page=None, base=0),
    "RG237": dict(range=(1, 1), name="米連邦航空局のレーダーの再生（米国立公文書館 RG237）", page=None, base=0),
    # 🆕 2026-10-13（⑤b-6）：NIST NCSTAR 1-6（表6-1＝PDF 240頁・ca12 の 8:46:26）・委員会報告の序文（p.xv＝GPO の PDF 15頁＝ローマ数字の頁は
    #   「p数字」で書けない＝PDF の頁で）・govinfo の書誌（報告書の刊行日 2004-07-22＝sources §1-1）
    "NIST 1-6": dict(range=(9001, 9500), name="NIST NCSTAR 1-6（2005年）", page="pdf", base=9000),
    "委員会報告の序文": dict(range=(13, 18), name="9.11委員会報告書（2004年）の序文", page="pdf", base=0),
    "govinfo": dict(range=(1, 1), name="米政府印刷局 govinfo の書誌", page=None, base=0),
}
# 🆕 21本目 ⑤b-3：資料で割れる時刻（台本 §1-5＝委員会報告の値を語り、NIST・NTSB の値は言わない）＝時間の帯の点に出典の名（by=True）を添える
#    （門番 check_axis ③）。1機目 8:46:40（NIST 8:46:30）・2機目 9:03:11（NTSB 約9:02:40・NIST 9:02:59）・77便 9:37:46（NTSB 9:37:45）・
#    93便 10:03:11（委員会も some dispute）
ILLU_SPLIT_TIMES = ("8:46:40", "9:03:11", "9:37:46", "10:03:11")   # 資料で割れる時刻＝画面に時計・時刻の札として出さない
ILLU_CROWD_UNTIL = None                     # 乗客の群れを描いてよい場面の時刻の上限
ILLU_ROLES = dict(sprite=(), crowd=())      # 置いてよい役割（門番 check_illu ②）＝空の組なら、どの役割も置けない（fail closed）
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）
ILLU_CLOCK_OK = ()                          # 札に出してよい時計の時刻（門番 check_illu ⑤）
ILLU_COUNTS = {}                            # 描いてよい数＝{部品の obj の名: (数, 出典)}（門番 check_illu ③）
ILLU_ASSUME = {}                            # 想定の札を出すカット＝{カットID: 札の言葉}（門番 check_illu ④）
ILLU_DESTROY_CUTS = ()                      # 壊れる物の部品を描いてよいカット（門番 check_illu ⑫＝空なら全部止める）
ILLU_TOP_NOSCALE = {}                       # 縮尺を持たない模式の上から見た絵の置き場＝{置き場: 理由}（門番 check_illu ⑧ は縮尺の代わりに「人が0・模式の断り」を測る）
ILLU_SUB_UNTIL = None                      # 潜水艦の時刻の上限（門番 ⑮＝無ければ潜水艦を描いたカットは止まる）
ILLU_SUB_EXC = {}                           # 上の上限の例外＝{カットID: 時刻}
ILLU_SUB_STOP = None                        # 艦の絵を止めたカット（これより後に潜水艦を置かない）
ILLU_BOOM_CUTS = ()                         # 音の輪（9時18.1分の型）を置いてよいカット（門番 ⑰）
ILLU_MIX_TODO = {}                          # 混ざりの本物の側のつなぎ待ち＝{カットID: 理由}（門番 ⑦）
ILLU_MIX_BUNDLE = REF / "credits.json"      # 束ができたか（混ざりのつなぎ待ちの終わり）を見るファイル

# 🔴 2026-10-06（19本目 ⑤b-1）：空にした（18本目は割れる時刻・出典の名つきの点を使わなかった＝空のままの値＝`tools/fixture_ep18.py`）
AXIS_DOCS = {}
# 🆕 2026-10-13（21本目 ⑤b-6）：ca12 の割れる時刻の札＝NIST の2つの巻を見分ける（どちらも「NIST」と出すと同じ資料に読める）
AXIS_DOCS.update({"NIST": "NIST（本編）", "NIST 1-6": "NIST（別冊）"})


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：軸の型（`tools/axis.py`・門番 `check_axis`）── 21本目 ⑤b-3〜⑤b-6（時間の帯・年表・2段の帯）
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の AX_*・AXI の項目は21本目の値（22本目の ⑤b-1 で見本 fixture_ep21 へ）。
#   値と頁は委員会報告の文字の層（`ref/ep21/src/core_raw/GPO-911REPORT.pages.jsonl`＝印字＋18）で当てた＝門番の側の表（check_axis.REC_AXIS）と照らされる（§5b-88）。
# 軸の教訓（札が重なって縦の線が隣の札を貫いた＝振り分け・右の端を右上の章の札を避けて延ばす・左の端を札が画面の外へ出ない所に・目盛りを割れる時刻の印に
#   合わせない・past で沈めるだけの点は札を出さない）は下の各軸の注
# 部品（記録の頁つき。値と頁は門番 check_axis の REC_AXIS と照らされる）。t は項目名だけ（§5b-9）
AXI = {}

# 🆕 2026-10-12（21本目 ⑤b-3）：時間の帯の型（第3〜8章で使い回す）＝時刻はアメリカ東部の夏の時間・画面は「8:46」の形（check_wording.EP_TIMES）。
#   AX_MORN＝その朝の全体（7:50〜10:10＝4機の離陸から93便の墜落 10:03:11 まで）＝この回の芯の帯（c208・c217・c320〜）。
#   AX_11＝11便の寄り（8:10〜9:00）＝c412・c423。⚠️ 右の端は右上の章の札を避けて、最後の点より少し先まで（20本目の教訓）
#   値と頁は委員会報告の文字の層（`ref/ep21/src/core_raw/GPO-911REPORT.pages.jsonl`＝印字＋18）で当てた＝門番の側の表（check_axis.REC_AXIS）と照らされる。
#   🔴 1機目の衝突 8:46:40 は割れる時刻（ILLU_SPLIT_TIMES）＝点に出典の名（by=True）
#   ⚠️ 門番 axis（⑤b-3）：AX_MORN は1分＝約11画素＝8:14 と 8:20 の札が重なり、縦の線が隣の札を貫いた＝175便は左へ・77便は右へ振る。
#      past で沈めるだけの点は札を出さない（`ss.ax("dep175", t="", lab=False)`＝点だけ）
AX_MORN = dict(view="clock", span=("7:50", "10:10"), ticks=("8:00", "8:30", "9:00", "9:30", "10:00"))
AX_11 = dict(view="clock", span=("8:10", "9:00"), ticks=("8:10", "8:20", "8:30", "8:40", "8:50", "9:00"))
#   AX_HIST＝乗っ取りの「常識」の年表（c302・c309）。「1960年代から」は年代＝1960〜1969 の帯（日付を足さない）
AX_HIST = dict(view="date", span=("1958", "2006"), ticks=("1960", "1970", "1980", "1990", "2000"))
AXI.update({
    # 第1章（AX_MORN）：p4「The plane took off at 7:59」・p7「departed Logan Airport at 8:14」・p8「took off at 8:20」・p10「At 8:42, United Airlines
    #   Flight 93 took off」・p4「By 8:00 A.M. … they had defeated all the security layers」
    "dep11": dict(k="pt", at="7:59", t="11便", rec="委員会報告 p4", anchor="end"),
    "gate8": dict(k="pt", at="8:00", t="保安の関門を通り抜ける", rec="委員会報告 p4", c="INST", anchor="start"),
    "dep175": dict(k="pt", at="8:14", t="175便", rec="委員会報告 p7", anchor="end"),
    "dep77": dict(k="pt", at="8:20", t="77便", rec="委員会報告 p8", anchor="start"),
    "dep93": dict(k="pt", at="8:42", t="93便", rec="委員会報告 p10"),
    # 第3章（AX_11）：p4「we believe the hijacking began at 8:14 or shortly thereafter」・p18「At 8:21, American 11 turned off its transponder」・
    #   p19「At 8:24:38, the following transmission」・図表 p32「Boston Center aware of hijacking」（8:25）・p19「Between 8:25 and 8:32 …
    #   Boston Center managers started notifying their chain of command」・p20「At 8:37:52, Boston Center reached NEADS」・「scrambled at 8:46」・
    #   「airborne at 8:53」・p7「At 8:46:40, American 11 crashed into the North Tower」・p21「That nine minutes' notice before impact」
    "hj11": dict(k="pt", at="8:14", t="乗っ取りの始まり（委員会の見立て）", rec="委員会報告 p4", anchor="end"),
    "xpdr11": dict(k="pt", at="8:21", t="トランスポンダが切られる", rec="委員会報告 p18", anchor="end"),
    "voice11": dict(k="pt", at="8:24:38", t="管制の無線に声", rec="委員会報告 p19", anchor="start"),
    "aware11": dict(k="pt", at="8:25", t="ボストン・センターが知る", rec=["図表 p32", "委員会報告 p19"], c="INST", anchor="start"),
    "chain11": dict(k="span", a="8:25", b="8:32", t="FAA の上の段へ", rec="委員会報告 p19", c="INST"),
    "neads11": dict(k="pt", at="8:37:52", t="NEADS に知らせが届く", rec="委員会報告 p20", c="INST", anchor="end"),
    "scr11": dict(k="pt", at="8:46", t="発進の命令", rec="委員会報告 p20"),
    "hit11": dict(k="pt", at="8:46:40", t="北棟", rec="委員会報告 p7", c="ALERT", by=True, anchor="end"),
    "air11": dict(k="pt", at="8:53", t="F-15 が飛び立つ", rec="委員会報告 p20", anchor="start"),
    "nine11": dict(k="br", a="8:37:52", b="8:46:40", t="9分", rec=["委員会報告 p20", "委員会報告 p21", "委員会報告 p7"]),
    # 第2章（AX_HIST）：p85「elaborated over decades of experience with scores of hijackings, beginning in the 1960s」・
    #   「no terrorist had hijacked a U.S. commercial aircraft anywhere in the world since 1986」・p1「Tuesday, September 11, 2001」
    "cs60": dict(k="span", a="1960", b="1969", t="1960年代", rec="委員会報告 p85", c="INST"),
    "cs_all": dict(k="br", a="1960", b="2001-09-11", t="数十年の積み重ね", rec=["委員会報告 p85", "委員会報告 p1"]),
    "last86": dict(k="pt", at="1986", t="最後のテロの乗っ取り", rec="委員会報告 p85", anchor="end"),
    "quiet86": dict(k="span", a="1986", b="2001-09-11", t="起きていない", rec=["委員会報告 p85", "委員会報告 p1"], c="LINE"),
    "day911": dict(k="pt", at="2001-09-11", t="この朝", rec="委員会報告 p1", c="ALERT", anchor="start", fmt="y"),   # ⚠️ 試し焼き：左へ振ると「1986年」の札と横に並んで1つの札に読めた
})
# 🆕 2026-10-12（21本目 ⑤b-4）：第4〜6章。AX_175＝175便の寄り（8:40〜9:06＝c507）。原文（委員会報告の文字の層）：p7「at 8:47, when the aircraft
#   changed beacon codes twice within a minute」・p21「At 8:51, the controller noticed the transponder change from United 175」・p22「controller at 8:53,
#   saying that "we may have a hijack"」「At about 8:55, the controller in charge notified a New York Center manager」（about＝「ごろ」）・p23「came in a phone
#   call from New York Center to NEADS at 9:03」・p24「Two minutes later [8:54＋2], it disappeared completely from radar」・p25「transponder was turned off at
#   8:56」・p11「The hijackers attacked at 9:28」・p29「At 9:42, the Command Center learned from news reports」「At 9:46 the Command Center updated FAA
#   headquarters that United 93」。⚠️ 記録の言葉（「乗っ取りかもしれない」ほか）は札にしない＝項目名だけ
AX_175 = dict(view="clock", span=("8:40", "9:06"), ticks=("8:40", "8:45", "8:50", "8:55", "9:00", "9:05"))
AXI.update({
    "code175": dict(k="pt", at="8:47", t="番号が変わる", rec="委員会報告 p7", anchor="end"),
    "see175": dict(k="pt", at="8:51", t="管制官が気づく", rec="委員会報告 p21", anchor="end"),
    "may175": dict(k="pt", at="8:53", t="乗っ取りを疑う", rec="委員会報告 p22", anchor="end"),   # ⚠️ 門番 axis：右へ振ると 8:55 の縦の線が札を貫いた
    "mgr175": dict(k="pt", at="8:55", t="上司へ伝える", rec="委員会報告 p22", c="INST", anchor="start", approx=True),
    "mil11": dict(k="pt", at="8:37:52", t="11便：軍へ", rec="委員会報告 p20", c="INST", anchor="end"),
    "mil175": dict(k="pt", at="9:03", t="175便：軍へ", rec="委員会報告 p23", c="INST", anchor="start"),
    "off77": dict(k="pt", at="8:56", t="77便：画面から消える", rec=["委員会報告 p24", "委員会報告 p25"], anchor="end"),
    "hj93": dict(k="pt", at="9:28", t="93便の乗っ取り", rec="委員会報告 p11", c="ALERT", anchor="end"),
    "news42": dict(k="pt", at="9:42", t="報道で知る", rec="委員会報告 p29", c="INST", anchor="end"),
    "upd93": dict(k="pt", at="9:46", t="93便の位置を本部へ", rec="委員会報告 p29", c="INST", anchor="start"),
})
# 🆕 2026-10-12（21本目 ⑤b-5）：第7〜8章。AX_93＝93便の寄り（9:20〜10:08＝c810・c819・c830）・AX_ORD＝撃墜の許可（10:00〜10:36＝c901・c902・
#   c917）・AX_ALL＝その朝の4機と命令（7:50〜10:40＝c921）。原文（委員会報告の文字の層）：p11「The hijackers attacked at 9:28」・p28「By 9:34, word of
#   the hijacking had reached FAA headquarters」・p13「At 9:57, the passenger assault began」・p30「United 93 crashed in Pennsylvania at 10:03:11」
#   （割れる時刻＝by=True・p30「some dispute」）「NEADS first received a call about United 93 … at 10:07」・p31「The time of notification of the
#   crash of United 93 was 10:15」・p41「At some time between 10:10 and 10:15, a military aide told the Vice President … authorized」・
#   p42「at 10:31, General Larry Arnold instructed his staff to broadcast」・p45「Shootdown authority was first communicated to NEADS at 10:31」・
#   p8「At 9:03:11, United Airlines Flight 175 struck the South Tower」・p10「At 9:37:46, American Airlines Flight 77 crashed into the Pentagon」
#   ⚠️ 「35分」（9:28→10:03:11＝35分11秒）と「約4分」（10:03:11→10:07＝3分49秒）は台本の語り＝括弧の札（数字は語りと同じ）
AX_93 = dict(view="clock", span=("9:20", "10:08"), ticks=("9:20", "9:30", "9:40", "9:50", "10:00"))
AX_ORD = dict(view="clock", span=("9:45", "10:36"), ticks=("9:50", "10:00", "10:10", "10:20", "10:30"))   # ⚠️ 門番 layout：左の端 10:00 だと 10:03:11 の札（左へ振る）が画面の外へ出た
AX_ALL = dict(view="clock", span=("7:50", "10:50"), ticks=("8:00", "8:30", "9:00", "9:30", "10:00", "10:30"))   # 右の端＝10:31 の札を右へ振る余白
AXI.update({
    "hq93": dict(k="pt", at="9:34", t="FAA の本部へ伝わる", rec="委員会報告 p28", c="INST", anchor="start"),
    "as57": dict(k="pt", at="9:57", t="乗客の反撃", rec="委員会報告 p13", c="ALERT", anchor="end"),
    "crash93": dict(k="pt", at="10:03:11", t="墜落", rec="委員会報告 p30", c="ALERT", by=True, anchor="end"),
    "min35": dict(k="br", a="9:28", b="10:03:11", t="35分", rec=["委員会報告 p11", "委員会報告 p30"]),
    "neads93": dict(k="pt", at="10:07", t="NEADS へ", rec="委員会報告 p30", c="INST", anchor="start"),
    "gap4": dict(k="br", a="10:03:11", b="10:07", t="約4分", rec="委員会報告 p30"),
    "rpt15": dict(k="pt", at="10:15", t="墜落の知らせ", rec="委員会報告 p31", c="INST", anchor="start"),
    "auth": dict(k="span", a="10:10", b="10:15", t="副大統領の許可", rec="委員会報告 p41", c="AMBER"),
    "neads31": dict(k="pt", at="10:31", t="NEADS に許可", rec=["委員会報告 p42", "委員会報告 p45"], c="INST", anchor="end"),
    # ⚠️ 門番 axis（⑤b-5 c921）：右へ振ると 10:03:11 の縦の線が 9:37:46 の札を貫いた・10:31 の札が3段目へ上がって右上の章の札に触れた＝
    #    出典の名つきの札は幅が広い＝4機と命令を重ねる帯は全部「左へ」（左から順に段へ振られる作り＝後の点の縦の線が前の札を通らない）
    "hit175": dict(k="pt", at="9:03:11", t="南棟", rec="委員会報告 p8", c="ALERT", by=True, anchor="end"),
    "hit77": dict(k="pt", at="9:37:46", t="ペンタゴン", rec="委員会報告 p10", c="ALERT", by=True, anchor="end"),
})
# 🆕 2026-10-13（21本目 ⑤b-6）：第9章〜終章。原文は門番 check_axis の REC_AXIS の上（p26・p27・p34・NIST 表6-1・法律・序文・govinfo）。
#   AX_TESTI＝2段の帯（上＝2003年5月の公聴会の証言・下＝委員会が記録で当てた時刻）＝ca03〜ca08・ca16・ca17。
#     ×の印（x=True・札なし）は証言の 9:16・9:24 だけ（門番 REC_WRONG）。「14分」（9:24→9:37:46＝13分46秒）は括弧の札＝語りの数字
#     ⚠️ 上の段の札は「93便の知らせ」の長さまで（「93便の乗っ取りの知らせ」380px は 9:24 の札と同じ段に並べず、9:24 の縦の線が貫いた＝門番 axis）
#     ⚠️ 下の段の札は左右に振る（9:21 は左・9:23 は左の2段目・9:28 は右・9:36 は左の2段目・9:37:46 は右）＝縦の線が同じ段の札を貫かない
#   AX_HIT1＝1機目の衝突の3つの値（8:46:20〜8:46:50）＝ca12。割れる時刻の印（split）＝出典の名だけ・どれが正しいとは描かない
#   AX_AFTER＝その後の年表（2001年1月〜2004年12月）＝ca20・cb05・cb07・cb11・cb12。⚠️ 左の端を 2001年7月にすると「この朝」の札
#     （左へ振る＝右の「空の保安の法律」の札と並べるため）が画面の外へ出る
AX_TESTI = dict(view="tiers", span=("9:12", "9:42"), ticks=("9:15", "9:20", "9:25", "9:30", "9:35", "9:40"),
                lanes=("2003年の証言", "委員会の記録"))
AX_HIT1 = dict(view="clock", span=("8:46:20", "8:46:50"), ticks=("8:46:20", "8:46:35", "8:46:50"))
#   ⚠️ geom_gap：目盛りを 8:46:30・8:46:40 に置くと、割れる時刻の印（軸の下へ 22px 伸びる）が目盛りの字に 3.4px＝15秒おきの目盛りに
AX_AFTER = dict(view="date", span=("2001-01", "2004-12"), ticks=("2001", "2002", "2003", "2004"))
_TS, _TR = "2003年の証言", "委員会の記録"
AXI.update({
    "t916": dict(k="pt", at="9:16", t="93便の知らせ", rec="委員会報告 p34", c="INST", lane=_TS, anchor="start"),
    "t916x": dict(k="pt", at="9:16", rec="委員会報告 p34", c="INST", lane=_TS, lab=False, x=True),
    "t924": dict(k="pt", at="9:24", t="77便の知らせ", rec="委員会報告 p34", c="INST", lane=_TS, anchor="start"),
    "t924x": dict(k="pt", at="9:24", rec="委員会報告 p34", c="INST", lane=_TS, lab=False, x=True),
    "r921": dict(k="pt", at="9:21", t="11便の誤報", rec="委員会報告 p26", c="ALERT", lane=_TR, anchor="end"),
    "r921q": dict(k="pt", at="9:21", t="誤報の出どころは不明", rec="委員会報告 p26", c="ALERT", lane=_TR, anchor="end"),
    "r923": dict(k="pt", at="9:23", t="ラングレーへ発進の命令", rec="委員会報告 p27", lane=_TR, anchor="end"),
    "r928": dict(k="pt", at="9:28", t="93便の乗っ取り", rec="委員会報告 p11", c="ALERT", lane=_TR, anchor="start"),
    "r936": dict(k="pt", at="9:36", t="首都へ向かう不明の機", rec="委員会報告 p27", c="INST", lane=_TR, anchor="end"),
    "r946": dict(k="pt", at="9:37:46", t="ペンタゴン", rec="委員会報告 p10", c="ALERT", lane=_TR, by=True, anchor="start"),
    "s936": dict(k="span", a="9:36", b="9:37:46", rec=["委員会報告 p27", "委員会報告 p10"], c="ALERT", lane=_TR),
    "b14": dict(k="br", a="9:24", b="9:37:46", t="証言のとおりなら14分", rec=["委員会報告 p34", "委員会報告 p10"]),
    # ca12（AX_HIT1）：割れる時刻の印3つ＋どこから出た値か（項目の札）
    "sp840": dict(k="split", at="8:46:40", rec="委員会報告 p7"),
    "sp830": dict(k="split", at="8:46:30", rec="NIST p7134"),
    "sp826": dict(k="split", at="8:46:26", rec="NIST 1-6 p9240", anchor="end"),
    "ch840": dict(k="chips", at="8:46:40", chips=["飛んだ道の調べ（NTSB）から"], rec=["委員会報告 p7", "委員会報告 p454"]),
    "ch830": dict(k="chips", at="8:46:30", chips=["テレビの時刻表示から"], rec="NIST p7134"),
    # ca19・cc04（AX_ALL）：前もっての知らせが無かった3機（p31「no advance notice on the second … third … fourth」）
    "nn175": dict(k="chips", at="9:03:11", chips=["知らせ無し"], rec=["委員会報告 p8", "委員会報告 p31"]),
    "nn77": dict(k="chips", at="9:37:46", chips=["知らせ無し"], rec=["委員会報告 p10", "委員会報告 p31"]),
    "nn93": dict(k="chips", at="10:03:11", chips=["知らせ無し"], rec=["委員会報告 p30", "委員会報告 p31"]),
    "fly": dict(k="span", a="8:37:52", b="10:31", t="その場で組み立てた守り", rec=["委員会報告 p20", "委員会報告 p45"], c="AMBER"),
    # 年表（AX_AFTER）。⚠️ 語りの細かさ＝「2001年11月」「2002年11月」「2004年7月」＝札は年月まで（fmt="ym"）
    "law01": dict(k="pt", at="2001-11-19", t="空の保安の法律", rec="法律 p1", fmt="ym", anchor="start"),
    "law01y": dict(k="span", a="2001-11-19", b="2002-11-19", t="1年のうちに全空港へ", rec="法律 p1", c="INST"),
    "dhs02": dict(k="pt", at="2002-11", t="国土安全保障省の法律", rec="委員会報告 p391", fmt="ym", anchor="end"),
    "com02": dict(k="pt", at="2002-11-27", t="9.11委員会ができる", rec="委員会報告の序文 p15", fmt="ym", c="INST", anchor="start"),
    "rep04": dict(k="pt", at="2004-07-22", t="委員会の報告書", rec="govinfo p1", fmt="ym", c="INST", anchor="end"),
})


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：量の型（棒）── 21本目 ⑤b-3〜⑤b-4
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の QG・QB はこの回の記録（値と頁）。
#    記録の値は門番の側にも別に持つ（check_qty.REC_QTY＝§5b-88）＝回を替えたら両方を替える。
QG = {}
QB = {}
# 🆕 2026-10-12（21本目 ⑤b-3）：c317 すぐ飛び立てる待機の基地（委員会報告 p16「reduced from its Cold War high of 26」・p17「only seven alert sites left
#   in the United States, each with two fighter aircraft on alert」）。🔴 数字は画面に書かない（目盛りだけ）・行の名に日付の数字を書かない
QG.update({"alert": dict(id="alert", t="待機の基地の数（か所）", ticks=(0, 10, 20, 30), rows=("冷戦のころの最大", "事件の朝"))})
QB.update({
    "alert_cw": dict(k="bar", g="alert", t="冷戦のころの最大", v=26, rec="委員会報告 p16", c="TICK"),
    "alert_911": dict(k="bar", g="alert", t="事件の朝", v=7, rec="委員会報告 p17", c="AMBER"),
})
# 🆕 2026-10-12（21本目 ⑤b-4）：c516 乗っ取りから FAA が知る（強く疑う）まで（委員会報告 p455「Flight 11 was a hijacking 11 minutes after it was taken over;
#   Flight 175, 9 minutes after」）。時刻の帯にしない＝175便の乗っ取りの始まりは「8:42〜8:46 のあいだ」で点が決まらない
#   ⚠️ 門番 qty：行の名に数字（「11便」「175便」）を書かない＝便は「北棟の便」（11便＝p7）・「南棟の便」（175便＝p8）と呼ぶ
QG.update({"faa": dict(id="faa", t="乗っ取りから FAA が知るまで（分）", ticks=(0, 5, 10, 15), rows=("北棟の便", "南棟の便"))})
QB.update({
    "faa11": dict(k="bar", g="faa", t="北棟の便", v=11, rec="委員会報告 p455", c="TICK"),
    "faa175": dict(k="bar", g="faa", t="南棟の便", v=9, rec="委員会報告 p455", c="AMBER"),
})


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：原寸で見て字でないと決めた OCR の範囲 ── 21本目 ⑤b-7
# ══════════════════════════════════════════════════════
# 🆕 2026-10-13（21本目 ⑤b-7）：**原寸で見て字でないと決めた OCR の範囲**（OCR の読み置きのファイル名 → [((x0, y0, x1, y1)＝束の画素, 何か)]）。
#    `check_slide.load_ocr` がこの中に真ん中のある行を外す（外した行は「文字行と見なさなかった」の表に理由つきで出る）。
#    宣言が何の行にも当たらなければ止める（読み置きの取り直し・写真の差し替えで古くなった宣言を残さない）。§0b＝回を替えるとき空にする
#    ⑤b-7：門番 edges（c421・cb18）・slide G-13（cb18）が鳴った行を原寸の2倍で見た（scratchpad `ocr_suspects.jpg`）＝窓の明かりの列と雪の上の木立
OCR_NOT_TEXT = {
    "wtc_far_1976.jpg": [((440, 800, 715, 1940), "左の塔の壁面の窓の明かりの列"), ((980, 800, 1260, 1940), "右の塔の壁面の窓の明かりの列")],
    "flight93_memorial_aerial_2024_12.jpg": [((780, 700, 1850, 1780), "追悼の場のまわりの雪の上の木立")],
}


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：スライドの台紙の黒い縁がある写真の名簿 ── 21本目 ⑤b-7（2026-10-14 ⑤b-1 に親が足した）
# ══════════════════════════════════════════════════════
# 🆕 2026-10-13（21本目 ⑤b-7）：全画面で流す・寄る窓が縁に入らないかを門番 `tools/check_photo_edge.py` が測る名簿。
#    本番の ss は `P(f"lc_a05_{k}")` で組んでいた＝EP が ep22 になると鍵が `ep22/lc_a05_…`（無い名）に化ける＝見本は **`ep21/` の名を
#    文字で書いた**（値＝git の `35fab37` の ss.SLIDE_MOUNT を評価した結果と同じ8＋3点・説明の文は1字も変えていない）。
#    check_photo_edge の selftest が `apply()`＋`apply_cuts()`（21本目の c102＝LC-A17）で使う
SLIDE_MOUNT = {
    **{f"ep21/lc_a05_{k}.jpg": "議会図書館 LC-A05 のスライドの走査（四隅の丸い台紙）" for k in ("a01", "a03", "a05", "a06", "a09", "a10", "a17", "b20")},
    "ep21/loc_item210.jpg": "議会図書館 item 210 のスライドの走査（左と下に台紙・右の暗がりは絵）",
    "ep21/logan_1973.jpg": "EPA DOCUMERICA のスライドの走査（四隅の丸い台紙）",
    "ep21/logan_apron_1969.jpg": "Korab のスライドの走査（四辺の暗い縁）",
}


# `apply()` が cuts.ss に差し込む名の全部（上の値＝ss から移したもの）。ここに無い名は ss に置かない
#   （`AXI`・`QG`・`QB`・`REC_DOCS`・`AXIS_DOCS`・`OCR_NOT_TEXT`・`ILLU_*` などは ss に空の器が残る＝見本の値〈21本目の項目つき〉を差し込む。
#   `AX_MORN` ほかの `AX_*` は本番の ss に無い名＝restore で消す）。21本目は関数を ss へ足さなかった（`ax()`・`qb()` は型の道具＝本番に残した。
#   `mv()`・`MV_Z`・`MV_IN`・`check_frame_only(spec, use)` の拡張も型）。`_TS`・`_TR`（2段の帯の段の名の略）は上の AXI を組むための名＝ss には移さない
SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "AX_MORN", "AX_11", "AX_HIST", "AX_175", "AX_93",
            "AX_ORD", "AX_ALL", "AX_TESTI", "AX_HIT1", "AX_AFTER", "QG", "QB", "OCR_NOT_TEXT", "SLIDE_MOUNT")


# ══════════════════════════════════════════════════════════
#  titan_fig.GEO から：21本目の地点＝無い
# ══════════════════════════════════════════════════════════
#   21本目は `titan_fig.GEO` に地点を足さなかった（地図は模式図 mech21 の `MAP_PTS`〈緯度経度の表＝一般の座標〉と Natural Earth の陸 `ref/ep21/coast_ne50m.json`）。
#   `35fab37` の `titan_fig.GEO` は `b1ecd46`（20本目の値を移した直後）と同じ（差分は模式図 `m21` の関数だけ）
GEO = {}


# ══════════════════════════════════════════════════════
#  門番の記録の表（21本目）── 門番の側に別に持つ記録（ルール §5b-88）
# ══════════════════════════════════════════════════════
# 以下の表は、門番3本の本番の置き場にあった21本目の値を1文字も変えずに写したもの（GATES が門番ごとにまとめる）

# ── check_axis ──
# 🆕 2026-10-12（21本目 ⑤b-3）：第1〜3章の時間の帯と年表。頁＝委員会報告の印字の頁（GPO の PDF＝印字＋18・文字の層 `ref/ep21/src/core_raw/
#    GPO-911REPORT.pages.jsonl` で当てた）・図表 p32＝同じ報告書の図（②が原寸で読んだ写し＝`ref/ep21/sources.md` §11-1）。引いた原文：
#    p4「The plane took off at 7:59」「By 8:00 A.M. … they had defeated all the security layers」「the hijacking began at 8:14 or shortly thereafter」・
#    p7「departed Logan Airport at 8:14」「At 8:46:40, American 11 crashed into the North Tower」・p8「took off at 8:20」・p10「At 8:42, United Airlines
#    Flight 93 took off」・p18「At 8:21, American 11 turned off its transponder」・p19「At 8:24:38」「Between 8:25 and 8:32」・図表 p32「Boston Center
#    aware of hijacking」（8:25）・p20「At 8:37:52, Boston Center reached NEADS」「scrambled at 8:46」「airborne at 8:53」・p21「That nine minutes'
#    notice」・p85「beginning in the 1960s」（年代＝1960〜1969 の帯）「since 1986」・p1「Tuesday, September 11, 2001」
REC_AXIS = {}
REC_AXIS.update({"7:59": {"委員会報告 p4"}, "8:00": {"委員会報告 p4"}, "8:14": {"委員会報告 p4", "委員会報告 p7"}, "8:20": {"委員会報告 p8"},
                 "8:42": {"委員会報告 p10"}, "8:21": {"委員会報告 p18"}, "8:24:38": {"委員会報告 p19"},
                 "8:25": {"図表 p32", "委員会報告 p19"}, "8:32": {"委員会報告 p19"},
                 "8:37:52": {"委員会報告 p20", "委員会報告 p21"}, "8:46": {"委員会報告 p20"}, "8:53": {"委員会報告 p20"},
                 "8:46:40": {"委員会報告 p7", "委員会報告 p21"},
                 "1960": {"委員会報告 p85"}, "1969": {"委員会報告 p85"}, "1986": {"委員会報告 p85"},
                 "2001-09-11": {"委員会報告 p1", "委員会報告 p85"}})
# 🆕 2026-10-12（21本目 ⑤b-4）：第4〜6章（引いた原文は cuts/ss.py の AX_175 の上）。8:55 は about＝「ごろ」
#    ⚠️ 8:53 は第3章の F-15 の離陸（p20）と同じ時刻＝頁を足す（置き換えると c423 が落ちた）
REC_AXIS.update({"8:47": {"委員会報告 p7"}, "8:51": {"委員会報告 p21"}, "8:53": {"委員会報告 p20", "委員会報告 p22"}, "8:55": {"委員会報告 p22"},
                 "9:03": {"委員会報告 p23"}, "8:56": {"委員会報告 p24", "委員会報告 p25"}, "9:28": {"委員会報告 p11"},
                 "9:42": {"委員会報告 p29"}, "9:46": {"委員会報告 p29"}})
# 🆕 2026-10-12（21本目 ⑤b-5）：第7〜8章（引いた原文は cuts/ss.py の AX_93 の上）。⚠️ 同じ鍵が無いことを先に見た（9:28 は p11 のまま＝足すだけ）
REC_AXIS.update({"9:34": {"委員会報告 p28"}, "9:57": {"委員会報告 p13"}, "10:03:11": {"委員会報告 p30"}, "10:07": {"委員会報告 p30"},
                 "10:15": {"委員会報告 p31", "委員会報告 p41"}, "10:10": {"委員会報告 p41"},   # 10:15＝墜落の知らせ（p31）と許可の帯の終わり（p41）
                 "10:31": {"委員会報告 p42", "委員会報告 p45"},
                 "9:03:11": {"委員会報告 p8"}, "9:37:46": {"委員会報告 p10"}})
# 🆕 2026-10-13（21本目 ⑤b-6）：第9章〜終章。引いた原文（委員会報告の文字の層・印字＋18）：
#    p34「NORAD officials stated that at 9:16, NEADS received hijack notification of United 93 … This statement was incorrect」
#    「at 9:24, NEADS received notification of the hijacking of American 77 … also incorrect」・p26「At 9:21, NEADS received a report from the FAA」
#    （11便がまだ飛んでいる＝誤報）・p27「the crew commander issued the order at 9:23」（ラングレーへ発進）「At 9:36, the FAA's Boston Center called
#    NEADS and relayed the discovery about an unidentified aircraft closing in on Washington」。
#    1機目の衝突の割れる時刻＝NIST NCSTAR 1 表6-1（PDF 134頁＝印字 p84）「8:46:30」・NCSTAR 1-6 表6-1（PDF 240頁＝印字 p156）「8:46:26」
#    （ref/ep21/sources.md §11-2 #7・#8）。年表＝法律 107-71「November 19, 2001」・その「Not later than 1 year after the date of enactment」
#    （＝2002-11-19・期限の日は法律の日から数えた値）・p391「In November 2002, both the Homeland Security Act …」（月まで）・序文（PDF 15頁＝p.xv）
#    「Public Law 107-306, November 27, 2002」・govinfo の書誌 dateIssued 2004-07-22（sources §1-1）
REC_AXIS.update({"9:16": {"委員会報告 p34"}, "9:24": {"委員会報告 p34"}, "9:21": {"委員会報告 p26"}, "9:23": {"委員会報告 p27"},
                 "9:36": {"委員会報告 p27"},
                 "8:46:30": {"NIST p7134"}, "8:46:26": {"NIST 1-6 p9240"},
                 "2001-11-19": {"法律 p1"}, "2002-11-19": {"法律 p1"}, "2002-11": {"委員会報告 p391"},
                 "2002-11-27": {"委員会報告の序文 p15"}, "2004-07-22": {"govinfo p1"}})
LANES_OK = {"2003年の証言", "委員会の記録"}     # 🆕 21本目 ⑤b-6：2段の帯（ca03〜ca08・ca16・ca17）の段の名
REC_APPROX = {"8:55"}   # 記録が about の時刻（「ごろ」が要る）＝p22「At about 8:55」（第1〜3章は about の時刻を帯に置いていない）
REC_LANE = {}             # 2段の帯の記録ごとの段（値 → 段の名）
# 🆕 21本目 ⑤b-6：上の段＝2003年5月の公聴会の証言（p34）・下の段＝委員会が記録で当てた時刻（p10・p11・p26・p27）
REC_LANE.update({"9:16": "2003年の証言", "9:24": "2003年の証言",
                 "9:21": "委員会の記録", "9:23": "委員会の記録", "9:28": "委員会の記録", "9:36": "委員会の記録", "9:37:46": "委員会の記録"})
# 🆕 21本目 ⑤b-6：×の印（axis の x=True）を置いてよい値＝記録が「誤り」とした値と、その頁（p34「This statement was incorrect」「also incorrect」）
REC_WRONG = {"9:16": {"委員会報告 p34"}, "9:24": {"委員会報告 p34"}}
# 並び order の基準の時刻（分）。🔴 21本目は時計の時刻を含む並び（"1:16:27" の形）を使わなかった＝空（None）。本番も None
ORDER_REF_MIN = None

# ── check_qty ──
# 🆕 2026-10-12（21本目 ⑤b-3）：c317 待機の基地＝委員会報告 p16「reduced from its Cold War high of 26」・p17「only seven alert sites left in the
#    United States」（印字の頁・GPO の PDF＝印字＋18 の文字の層で当てた）
REC_QTY = {}          # (群の項目名＝画面の文字, 行の名＝画面の文字) → (値, 頁)
REC_QTY.update({("待機の基地の数（か所）", "冷戦のころの最大"): (26, {"委員会報告 p16"}),
                ("待機の基地の数（か所）", "事件の朝"): (7, {"委員会報告 p17"})})
# 🆕 2026-10-12（21本目 ⑤b-4）：c516＝委員会報告 p455（第1章の注）「Flight 11 was a hijacking 11 minutes after it was taken over; Flight 175, 9 minutes after」
#    行の名＝北棟の便（11便＝p7「crashed into the North Tower」）・南棟の便（175便＝p8「struck the South Tower」）
REC_QTY.update({("乗っ取りから FAA が知るまで（分）", "北棟の便"): (11, {"委員会報告 p455"}),
                ("乗っ取りから FAA が知るまで（分）", "南棟の便"): (9, {"委員会報告 p455"})})

# ── check_mech ──
# 🆕 21本目 ⑤b-3（2026-10-12）：模式図（m21＝`tools/mech21.py`・15の見え方）。⑤b-4〜⑤b-6 で見え方と記録の値を足した
# 🔴 記録の値は門番の側に持つ（§5b-88＝描く側の表 mech21.MAP_PTS・ROUTES・NE_BASES・GT・BL_LIMIT_IN・CH_ORDER・ES_MILES・PM_T を書き換えると鳴る）。
#    頁＝委員会報告の印字の頁（GPO の PDF＝印字＋18 の文字の層で当てた）。引いた原文：
#    p4「nonstop service from Boston to Los Angeles」（11便）・p7「scheduled to depart for Los Angeles」（175便＝p2 の「also bound for Los Angeles」と
#    p7「departed Logan Airport」＝ボストン）・p8「from Washington Dulles for Los Angeles」・p10「took off from Newark … bound for San Francisco」・
#    p17「NEADS, which is based in Rome, New York」「NEADS could call on two alert sites … Otis Air National Guard Base in Cape Cod, Massachusetts, and
#    Langley Air Force Base in Hampton, Virginia」・p3「set off the alarms for both the first and second metal detectors and was then hand-wanded」・
#    p84「knives with blades under 4 inches long」・p17〜18 の手順（管制官→上司→FAA の本部→国防総省の指揮所→国防長官の許し→NORAD の段→戦闘機）・
#    p18「five miles directly behind the hijacked aircraft」（5マイル＝約8キロ＝台本 §9）・p18 の3つの前提。
#    🔴 空港・基地・街の緯度経度は報告書の値ではない（一般の座標＝Wikidata と同じ桁）＝図の札に「模式」・ここでは描く側の表の写し違いを見る（±0.05度）。
#    札に出してよい時刻（記録の時刻）＝p4 8:14・p5 8:19・p18 8:21・p19 8:24:38・p20 8:34・8:37:52・8:46・8:53
#    🆕 ⑤b-4（第4〜6章）：札の時刻＝p7 8:42・8:46・8:47・p8 8:51・p21 8:51・p7 8:52・p22 8:53・8:55（about）・8:58・9:01・9:02・p23 9:03・p24 8:54・
#    p25 8:56・9:05・9:25・9:32・p26 9:21・p27 9:24・9:30・9:34・p9 9:00・p10 9:05〜9:10・p29 9:42・9:46。地点＝ハーンドン（p14「Command Center,
#    located in Herndon」）・ボルチモア（p27「north toward the Baltimore area」）・ホワイトハウス・ペンタゴン・レーガン空港（一般の座標）。
#    形の記録＝p34「an unknown plane was 6 miles southwest of the White House」・p25「reemerged … at 9:05, east of its last known position」・
#    p27「not headed north toward the Baltimore area as instructed, but east over the ocean」・p29「land at the nearest airport」・
#    p20「military-controlled airspace off the Long Island coast」
REC_M21 = dict(
    pts=dict(bos=(42.3656, -71.0096), ewr=(40.6925, -74.1687), iad=(38.9531, -77.4565), lax=(33.9425, -118.4081),
             sfo=(37.6189, -122.3750), rome=(43.2338, -75.4070), otis=(41.6584, -70.5214), langley=(37.0829, -76.3605),
             nyc=(40.7128, -74.0060), dc=(38.9072, -77.0369), boston=(42.3601, -71.0589),
             herndon=(38.9696, -77.3861), bal=(39.2904, -76.6122),
             wh=(38.8977, -77.0365), pent=(38.8719, -77.0563), dca=(38.8512, -77.0402),
             shk=(40.0514, -78.9044), cap=(38.8899, -77.0091), adw=(38.8108, -76.8669)),
    unk_mi=6.0, unk_brg=(202.5, 247.5),
    # 🆕 ⑤b-5：p30「United 93 crashed in Pennsylvania at 10:03:11, 125 miles from Washington, D.C.」（±10マイル＝街の点は一般の座標）・
    #   p11「his 16 transcontinental flights」・p42 の流れ（副大統領→NORAD→NEADS→戦闘機）・p45 の3つ（locate・authorization・communicate）・
    #   国立公園局「in the last nine rows of the plane」
    shk_mi=125.0, acars=16, cmd=("副大統領", "NORAD", "NEADS", "戦闘機"), need=3, rear=9,
    routes={("bos", "lax"), ("iad", "lax"), ("ewr", "sfo")},
    flights=dict(bos={"11便", "175便"}, iad={"77便"}, ewr={"93便"}),
    bases={"otis", "langley"}, neads="rome",
    arches=2,
    limit_in=4.0,
    chain=("管制官", "上司", "FAA の本部", "国防総省の指揮所", "国防長官の許し", "NORAD", "戦闘機"),
    escort=(5, 8),
    premise=3,
    clock={"8:14", "8:19", "8:21", "8:24:38", "8:34", "8:37:52", "8:46", "8:53",
           "8:42", "8:47", "8:51", "8:52", "8:55", "8:58", "9:01", "9:02", "9:03", "8:54", "8:56", "9:05", "9:21", "9:24", "9:30",
           "9:32", "9:34", "9:25", "9:00", "9:10", "9:42", "9:46",
           # 🆕 ⑤b-5：p11 9:19・9:23・9:24・9:26・9:28・p29 9:41・9:49・p13 9:57・9:58:57・p14 10:01（about＝「ごろ」）・p30 10:07・p31 10:15・
           #   p42 10:31・p44 10:45・p45 10:10
           "9:19", "9:23", "9:24", "9:26", "9:28", "9:41", "9:49", "9:57", "9:58:57", "10:01", "10:07", "10:15", "10:31", "10:45",
           "10:10"},
    src="委員会報告",
    # 🆕 ⑤b-6：序文（PDF 15頁＝p.xv）「Public Law 107-306, November 27, 2002」「more than 2.5 million pages of documents and interviewed more than
    #   1,200 individuals in ten countries」・運輸省の監察総監の報告 CC-2006-085 p1「referred to the Department of Defense (DOD) and Department of
    #   Transportation (DOT) Inspectors General」p3「the two current executives」・p456 の記録装置（11便と175便は見つからず・77便の音声は焼けて
    #   読めない・93便の2つと77便の飛行の記録は読めた＝p12・NTSB 77便 図2）・p311「2,973」・記念館「2,977」
    probe=dict(law="2002年11月", pages="250万", people="1,200", countries="10"),
    igs=("国防総省の監察総監", "運輸省の監察総監"), ig_execs=2,
    fdr={"11便": ("none", "none"), "175便": ("none", "none"), "77便": ("burn", "ok"), "93便": ("ok", "ok")},
    toll=(2973, 2977), toll_when=("2004年7月", "記念館"),
)

# ── check_boxes・check_illu ──
# 21本目は両ファイルに足した値が無い（`git diff b1ecd46 35fab37 -- tools/check_boxes.py tools/check_illu.py` は空）＝GATES に載せない。
# （20本目の見本の check_boxes〈REC_CAUSE ほか〉・check_illu〈REC_S1〜REC_S7〉のような、21本目の表は無い）


GATES = {
    # 21本目は時計の時刻を含む並び（order）を使わなかった＝ORDER_REF_MIN は None。2段の帯（tiers）と×の印を使った＝LANES_OK・REC_LANE・REC_WRONG が入る
    "check_axis": dict(REC_AXIS=REC_AXIS, LANES_OK=LANES_OK, REC_APPROX=REC_APPROX, REC_LANE=REC_LANE, REC_WRONG=REC_WRONG,
                       ORDER_REF_MIN=ORDER_REF_MIN),
    "check_qty": dict(REC_QTY=REC_QTY),
    "check_mech": dict(REC_M21=REC_M21),
}


_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・titan_fig.GEO・（gate を渡せば）その門番の記録の表を21本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss と GEO は触らない）＝14・15・16・18・19・20本目の見本 `fixture_ep14`・
    `fixture_ep15`・`fixture_ep16`・`fixture_ep18`・`fixture_ep19`・`fixture_ep20` と重ねるとき（check_mech の selftest は14・15・16・18・19・20・21本目の
    検算を1つの処理で回す＝先に14本目を全部差し込み、15・16・18・19・20・21本目は表だけ足す）。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が21本目の表で
       22本目の画を測る）。apply の前に**無かった名**（ss の AX_* …／門番の表）も覚えて、restore で**消す**
       ＝selftest のあとに21本目の名が本番へ残らない（fixture_ep15・fixture_ep16・fixture_ep18・fixture_ep19・fixture_ep20 と同じ作り）"""
    saved = dict(ss={}, ss_new=[], geo=None, gate=gate, tables={}, tables_new=[])
    if not tables_only:
        import titan_fig as F
        from cuts import ss
        saved["ss"] = {n: getattr(ss, n) for n in SS_NAMES if hasattr(ss, n)}
        saved["ss_new"] = [n for n in SS_NAMES if not hasattr(ss, n)]
        saved["geo"] = dict(F.GEO)
    tabs = {}
    if gate is not None:
        name = Path(getattr(gate, "__file__", "") or "").stem
        tabs = GATES.get(name, {})
        for k in tabs:
            if hasattr(gate, k):
                saved["tables"][k] = getattr(gate, k)
            else:
                saved["tables_new"].append(k)
    _SAVED.append(saved)         # 覚えてから差し込む＝途中で落ちても restore() が戻せる
    if not tables_only:
        g = globals()
        for n in SS_NAMES:
            setattr(ss, n, g[n])
        F.GEO.update(GEO)
    for k, v in tabs.items():
        setattr(gate, k, v)


CUTS_SHA = "35fab37"       # 21本目の章ファイルが最後に live だった版（章ファイルを22本目の空の器に替える前＝git の `35fab37`）
_CUTS21 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def _footage21():
    """21本目の映像の台帳 `CLIPS`（`ref/ep21/clips.json`）と使う区間 `USE`・器の黒帯の割合 `PILLAR`（git の CUTS_SHA の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}`）を返す。
    🆕 2026-10-25（25本目 ⑤b-3）：21本目の章ファイルは `ss.vid`・`ss.head`・`ss.tailv` で `footage.CLIPS`・`footage.USE` を引く（台帳の `"stock": true` なら
    「フリー素材に見出しは書かない」で止める）。本番の footage は25本目の表＝25本目のフリー素材 c713（X-blueprint）が USE に入ると、21本目の c713
    （W606 の記録映像に見出しと副題）が読み込みで落ちる＝c7.py がまるごと BROKEN（PLAN は200を超えるので `cuts_ep21` は止まらない＝黙って欠ける）。
    → 章ファイルを読む間だけ、この表を footage に差す（`cuts_ep21` が戻す＝17本目の `_footage17`・24本目の `_footage24` と同じ）。
    footage.py の `USE`・`PILLAR` は値だけの代入＝その2文だけを取り出して評価する（footage.py 全体は import しない）。
    ⚠️ 21本目の PILLAR は空（黒帯の器なし）＝空でも止めない。USE（11カット）と台帳が読めなければ止める"""
    import ast
    import json
    import subprocess
    p = subprocess.run(["git", "-C", str(ROOT), "show", f"{CUTS_SHA}:tools/footage.py"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 21本目の映像の使う区間を git の {CUTS_SHA} の tools/footage.py から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    ns = {}
    for node in ast.parse(p.stdout.decode("utf-8")).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("USE", "PILLAR") for t in node.targets):
            exec(compile(ast.Module([node], []), f"footage_{CUTS_SHA}", "exec"), ns)
    use, pillar = ns.get("USE"), ns.get("PILLAR")
    clips_file = REF / "clips.json"
    if not use or pillar is None or not clips_file.exists():
        raise RuntimeError(f"🔴 21本目の映像の表が読めていない（USE {len(use or {})}・PILLAR {'無い' if pillar is None else len(pillar)}・"
                           f"{clips_file} {'ある' if clips_file.exists() else '無い'}）")
    return json.loads(clips_file.read_text(encoding="utf-8")), use, pillar


def cuts_ep21():
    """21本目の章ファイル（git の CUTS_SHA の `tools/cuts/`）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。
    読む間だけ `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を21本目の表にする（`_footage21`＝本番の footage は25本目の表）。読み終えたら戻す。
    🆕 2026-10-25（25本目 ⑤b-3）：読めなかった章ファイル（`cuts.BROKEN`）があれば止める（黙って欠けた SPEC を見本にしない＝fail closed）"""
    if _CUTS21:
        return _CUTS21[0]
    import importlib
    import io
    import os
    import shutil
    import subprocess
    import sys
    import tarfile
    import tempfile
    import footage as _FO
    clips21, use21, pillar21 = _footage21()
    p = subprocess.run(["git", "-C", str(ROOT), "archive", CUTS_SHA, "tools/cuts"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 21本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts21_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep21 の写真・頁を読む＝根の下の作業場所の
        # フォルダ（ref・out ほか）へ一時フォルダから junction（Windows のフォルダへの道しるべ）を張る。消すときは先に道しるべだけ外す
        import _winapi
        for d in ROOT.iterdir():
            if d.is_dir() and d.name not in ("tools", ".git"):
                _winapi.CreateJunction(str(d), str(tmp / d.name))
                links.append(tmp / d.name)
        live = {k: v for k, v in sys.modules.items() if k == "cuts" or k.startswith("cuts.")}
        before = set(sys.modules)
        for k in live:
            del sys.modules[k]
        sys.path.insert(0, str(tmp / "tools"))
        keep_fo = (_FO.CLIPS, _FO.USE, _FO.PILLAR)
        _FO.CLIPS, _FO.USE, _FO.PILLAR = clips21, use21, pillar21          # 章ファイルを読む間だけ（finally で戻す）
        try:
            old = importlib.import_module("cuts")
            got = (dict(old.PLAN), dict(old.SPEC))
            broken = dict(getattr(old, "BROKEN", {}) or {})
        finally:
            _FO.CLIPS, _FO.USE, _FO.PILLAR = keep_fo
            sys.path.remove(str(tmp / "tools"))
            for k in set(sys.modules) - before:
                del sys.modules[k]
            for k in [k for k in sys.modules if k == "cuts" or k.startswith("cuts.")]:
                del sys.modules[k]
            sys.modules.update(live)
    finally:
        for ln in links:
            os.rmdir(ln)          # 道しるべだけを外す（中身＝本線のフォルダには触らない）
        if any(x.exists() for x in links):
            raise RuntimeError(f"🔴 一時フォルダの道しるべを外せない＝{tmp} を消さずに止める（本線のフォルダを消さないため）")
        shutil.rmtree(tmp, ignore_errors=True)
    if len(got[0]) < 200 or "c101" not in got[1]:
        raise RuntimeError(f"🔴 21本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}）")
    if broken:
        raise RuntimeError("🔴 21本目の章ファイルに読めないものがある＝" + "・".join(f"{k}（{type(e).__name__}: {str(e)[:120]}）" for k, e in broken.items()))
    _CUTS21.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を21本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で22本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep21()
    _SAVED.append(dict(cuts=(dict(cuts.PLAN), dict(cuts.SPEC))))
    cuts.PLAN.clear()
    cuts.PLAN.update(copy.deepcopy(plan))
    cuts.SPEC.clear()
    cuts.SPEC.update(copy.deepcopy(spec))


def restore():
    """apply() の前の本番の値に戻す（selftest のあと・本番の照合の前に呼ぶ）。apply を呼んでいなければ何もしない。
    ss と門番の表は、apply の前に無かった名を消す。GEO は fixture_ep14・15・16・18・19・20 と同じに、覚えた写しで入れ替える（clear → update）。
    tables_only で差し込んだ分は ss・GEO を覚えていない＝戻さない（先に差し込んだ別の見本を壊さない）。LIFO（あとに apply した順）"""
    while _SAVED:
        s = _SAVED.pop()
        if s.get("cuts") is not None:          # apply_cuts() の分＝22本目の PLAN・SPEC へ戻す
            import cuts
            plan, spec = s["cuts"]
            cuts.PLAN.clear()
            cuts.PLAN.update(plan)
            cuts.SPEC.clear()
            cuts.SPEC.update(spec)
            continue
        if s["geo"] is not None:
            import titan_fig as F
            from cuts import ss
            for n, v in s["ss"].items():
                setattr(ss, n, v)
            for n in s["ss_new"]:
                if hasattr(ss, n):
                    delattr(ss, n)
            F.GEO.clear()
            F.GEO.update(s["geo"])
        gate = s["gate"]
        for k, v in s["tables"].items():
            setattr(gate, k, v)
        for k in s["tables_new"]:
            if hasattr(gate, k):
                delattr(gate, k)
