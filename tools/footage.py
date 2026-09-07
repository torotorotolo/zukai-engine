# -*- coding: utf-8 -*-
"""実写**動画**を差し込むための素材まわり（2026-08-01 追加／2026-09-05 4本目で作り直し）。

🔴 なぜ入れたか（カズヤくん指示・2026-08-01）
   「PDでない写真・動画であっても積極的に使ってください。競合はそうしています。」
   ＋ r13 の試写「色使いが少なく、似た演出が続いて視覚的に飽きる」。
   静止画をもう1枚足すより、**実際に動いている映像**を入れるほうが効く。

■ 置き場所の約束
   🔴 **動画をリポジトリに入れない**（wav 163MB で学んだのと同じ問題）。
      ワークフローの中で URL から取り、コマを切り出して使う。
      落とした mp4     … out/jiko/clip/<name>.mp4   （gitignore・落とす方式のときだけ）
      切り出したコマ    … out/jiko/foot/<cid>/00000.jpg …（gitignore）

■ 🔴 **落とさずに、使う区間だけを URL から直接切り出す**
   4本目（NIST の Kaltura 配信）は1本 600MB〜2GB あり、全部落とすと C: にも Actions にも入らなかった。
   5本目（NARA の SL-1）も同じやり方で通る＝**`catalog.archives.gov` の mp4 は範囲取得に対応**
   （②素材の実測：`Range: bytes=0-1023` に **206** を返し、`ffprobe <URL>` がそのまま通る）。
   `ffmpeg -ss <秒> -i <URL>` で**その区間だけ**を読む。署名も期限も無いので URL は固定でよい。

■ 🔴 rate（スロー）
   1ショットがカットの尺より短いときに使う。SL-1 の実測は 中央値 7秒（Ph1&2）／5秒（Ph3）で、
   カットの尺（約9〜10秒）より短いショットが多いので**出番は4本目より多い**。
   `rate=0.5` と書くと 0.5倍速（=2倍の長さ）で切り出す。ffmpeg の setpts でコマを複製するだけ
   （補間しない）。動きの少ないショットに使う。**顔のあるショットには使わない**。

■ 出典の書き方（★ここを間違えない）
   5本目＝AEC（米原子力委員会）が撮り、NARA が公開した記録映画。合衆国政府の職務著作＝
   パブリックドメイン（根拠は下の CLIPS の注記に全部書いてある）。
   ⚠️ 1本目の ROV 映像（"courtesy of Pelagic Research Services"）のように**PDでない映像**を
      PD と書いてはいけない。⚠️ **映画の中に第三者の映像が混ざる危険**は残るので、
      ショットを選ぶときに局のロゴ・クレジット・見慣れた報道映像が無いかを見ること。

■ 使い方
     python tools/footage.py fetch          … 使う区間だけ切り出す（落とさない）
     python tools/footage.py fetch --check  … 切り出さずに、割り当てだけ確認する
     python tools/footage.py --selftest     … 陽性対照

■ 🔴 exit コード（2026-09-07・設計ノート §9-5 で `until=` を必須にした）
     0 … 通った
     1 … カットの尻がショットの終わりを越えている（`TOL` 超）
     **2 … `until=` が書いていない欄がある**＝「測れる状態になっていない」。1 より重い
     **3 … (start, until) が実測のショットをまたいでいる**＝**範囲の中で絵が別物**。いちばん重い
     ⚠️ **静止画（`still=True`）の欄も必須**。`overruns()` は静止画を飛ばすので、
        ここを飛ばすと**構造上見えない穴**になる（2026-09-07 に実測：36欄中4欄が
        until 無しのまま4本目を通っていた＝c106 c223 c434 pr02。どれも `still`）。

■ 🔴 秒数は**目で決めない。`ref/sl1/shots.json` から採る**
   4本目は 3秒刻みの見取り図で秒を選び、**注記の範囲の中で絵が別物**になった（3件）。
   5本目は `tools/shots.py` で**1秒刻み**に境目を実測してある（`SHOTS`）。
   ⚠️ ffmpeg の scene 検出だけでは**ディゾルブ（重ね消し）を見ない**。
      SL-1 でハード検出だけだと 77本／165本、1秒刻みだと **139本／271本**＝**168本を見落としていた**。
"""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
CLIP = HERE / "out" / "jiko" / "clip"
FOOT = HERE / "out" / "jiko" / "foot"
FPS = 30
UA = ("zukai-engine/1.0 (accident-documentary research; "
      "https://github.com/torotorotolo/zukai-engine; konariri8@gmail.com)")

# ── 5本目：SL-1 原子炉暴走事故（1961-01-03）の記録映画 ────────
# 🔴 4本目サーフサイド（NIST の Kaltura 配信）の CLIPS/USE は git の `4e4c1fb` にある。
#    カットIDが題材をまたいでぶつかるので**残さない**。
#
# 🔴 権利（②素材のチャットで確かめた。結論＝**使える**）
#    NARA のこの2本は `useRestriction = "Restricted - Possibly"／Copyright` が付いているが、
#    これは**シリーズ一括の定型文**であって、この2本への個別の判断ではない：
#      ・シリーズ本体 `88680113`（Moving Images Related to Combat Visual Information）が
#        **同じ注記を持つ**／同シリーズの兄弟レコード **299件が 299/299 で同じ札**
#      ・NARA の SL-1 の3件目 `66396247`（RG 434 エネルギー省）にも同じ札が付く
#    作者は連邦機関なので合衆国法典 17編105条により著作権が発生しない：
#      ・`contributors` の Originator ＝ **Department of Defense / Department of the Army**
#      ・`scopeAndContentNote` ＝「**U.S. Atomic Energy Commission** reports on phases 1 and 2…」
#      ・同じ AEC アイダホ支所のブリーフィング映画を **DOE/OSTI 自身が公開**している
#        （OSTI ID 1122857）。Commons にも PD として上がっている
#    ⚠️ **残る危険＝映画の中に第三者の映像（ニュース映画・音楽）が混ざっている可能性**。
#       ⑤b でショットを選ぶときに、局のロゴ・クレジット・見慣れた報道映像が無いかを見ること。
CR_NARA = "出典：米国国立公文書館（NARA）／米原子力委員会（AEC）撮影"
_MOPIX = "https://catalog.archives.gov/medialz/mopix/330/DIMOC/{f}.mp4"

# name: (ファイル名, naId, 尺(秒), 幅, 高さ, 出典, 中身)
_SL1 = {
    "sl1_ph12": ("330-dimoc-redstone1860", 174689848, 1494.71, 1920, 1080,
                 f"{CR_NARA} 「SL-1 Accident Phase I & II」（NARA naId 174689848）／パブリックドメイン",
                 "24分55秒。事故の発生と初期対応（第1・2段階）。139ショット"),
    "sl1_ph3": ("330-dimoc-redstone1861", 174689849, 1847.50, 1920, 1080,
                f"{CR_NARA} 「SL-1 Accident Phase III」（NARA naId 174689849）／パブリックドメイン",
                "30分48秒。炉の解体と埋設（第3段階）。271ショット"),
}
CLIPS = {}
for _n, (_f, _nid, _sec, _w, _h, _cr, _note) in _SL1.items():
    CLIPS[_n] = dict(url=_MOPIX.format(f=_f), naid=_nid, sec=_sec, w=_w, h=_h,
                     credit=_cr, note=_note, stream=True)

# ── 🔴 ショットの境目（`tools/shots.py` で1秒刻みに実測）────────────
# 4本目は「128〜133.9秒 レプリカの全景」と書いた**範囲の中で絵が別物**だった（3件）。
# 秒を3秒刻みの見取り図で選んでいたのが原因。→ [[feedback-measure-the-source-before-choosing-the-crop]]
# ここに実測のショット表を持たせ、`USE` の (start, until) が**1本のショットに収まっているか**を
# 機械で見る（`outside_shot()`）。⚠️ ffmpeg の scene 検出だけでは**ディゾルブを見ない**ので、
# 1秒ごとの見た目の署名で採ってある（1本のショットが333秒、という嘘が出ていた）。
SHOTS = {}
_SHOT_FILE = HERE / "ref" / "sl1" / "shots.json"
if _SHOT_FILE.exists():
    _sd = json.loads(_SHOT_FILE.read_text(encoding="utf-8"))
    SHOTS = {k: [(s["start"], s["until"], s["motion"]) for s in v["shots"]]
             for k, v in _sd.items()}


def shot_of(clip, t):
    """秒 t を含むショット (start, until, motion) を返す。無ければ None。"""
    for s in SHOTS.get(clip, []):
        if s[0] <= t < s[1]:
            return s
    return None


# 🔴🔴 使ってはいけない**秒**（2026-09-07・5本目 SL-1 ⑤c'・J-01/L-03/L-06）
#    `sl1_shots.BANNED` は「ショット単位」の禁止札だが、SL-1 の終幕タイトルは
#    **ショットの途中からディゾルブで浮き上がる**ので、ショット単位では表せない。
#    ＝ pr01（動画の1カット目）は禁止札の付いていない #137 を使いながら、
#      画面のまん中に「THE END」を出したまま焼き上がっていた。
#    ⚠️ **OCR は 1485〜1489 で1文字も読めない**（大きく潰れた字＋背景が忙しい）。
#      だから「OCR が0件だから文字は無い」で決めてはいけない
#      → [[feedback-absence-of-a-word-is-not-absence]]
#    実測（相対しきい値＝画面の p98 を超える画素の割合。対照＝すぐ左の同じ高さは全時刻 0.00%）:
#      1485.0 まで 0.00%／**1485.1 で 0.04%（浮き始め）**／1485.4 で 2.83%／1486.0 で 14.69%
#    ＝ 使ってよいのは **1478.0〜1485.0**。
NOGO = {
    "sl1_ph12": [(1485.0, 1495.0,
                  "終幕タイトル（THE END／THE U.S. ATOMIC ENERGY COMMISSION／"
                  "Contract No. AT(10-1)-1087）がディゾルブで浮く。実測 1485.1 から")],
}


def in_nogo(use=None, secs=None):
    """🔴 実際に読む秒が「使ってはいけない秒」に掛かっている欄。

    ⚠️ `until` だけを見ても止まらない。`until` は**ショットの終わり**として書かれるので、
       ショットの途中から禁止の秒が始まる場合に構造上見えない（pr01 がその実例）。
    """
    if secs is None:
        import scene_jiko as S
        secs = dict(S.CUTS)
    use = USE if use is None else use
    out = []
    for cid, u in use.items():
        rng = NOGO.get(u.get("clip"))
        if not rng:
            continue
        a = float(u["start"])
        b = a if u.get("still") else a + secs.get(cid, 0.0) * float(u.get("rate", 1.0))
        for x0, x1, why in rng:
            if b > x0 + 1e-9 and a < x1:
                out.append((cid, u["clip"], a, b, x0, x1, why))
    return out


def outside_shot(use=None):
    """🔴 (start, until) が1本のショットに収まっていない欄。

    ⚠️ `until=` を必須にしただけでは「数が入っていればよい」で終わる。
       **その数が実測のショットの終わりと合っているか**まで見ないと、4本目と同じ
       「範囲の中で絵が別物」が通る。ショット表が無いクリップは見ない（fail open ではなく対象外）。
    """
    use = USE if use is None else use
    out = []
    for cid, u in use.items():
        clip = u.get("clip")
        if clip not in SHOTS or u.get("until") is None:
            continue
        a, b = float(u["start"]), float(u["until"])
        sh = shot_of(clip, a)
        if sh is None:
            out.append((cid, clip, a, b, None))
        elif b > sh[1] + TOL:
            out.append((cid, clip, a, b, sh))
    return out


# ── どのカットに、どの動画の何秒目から当てるか ────────────────
# 🔴 5本目（SL-1）はまだ空。**⑤b で台本 §4 の画の欄と1対1になるように書く。**
#    4本目（サーフサイド）の36欄は git の `4e4c1fb` にある。
#
# 🔴 守ること
#   1. **そのカットで話している対象そのもの**であること（壁紙にしない）
#   2. 表題カード・顔の寄り・局のクレジットは使わない
#   3. `until=` は**全欄に必須**（`still=True` の欄も）。無いと `fetch --check` が exit 2
#   4. 🔴 (start, until) は `SHOTS` の**1本のショットに収める**。またぐと exit 3
#      ＝ 4本目で3件踏んだ「範囲の中で絵が別物」を機械で止める
#   5. 秒は `ref/sl1/shots.json`（1秒刻みの実測）から採る。目分量で書かない
#
# 書き方（4本目の例。数は SL-1 のものに置き換える）
#     "c103": dict(clip="sl1_ph12", start=412.0, until=421.0),
#     "c118": dict(clip="sl1_ph3", start=88.0, until=94.0, rate=0.6),
#     "c204": dict(clip="sl1_ph12", start=735.0, still=True, until=741.0),
# 🔴 2026-09-07（⑤b）：**全410ショットを見て決めた35欄。** 台帳＝`ref/sl1/SHOTS_INDEX.md`。
#    (start, until) は `ref/sl1/shots.json` の実測ショットの境目そのもの。
#    `rate` は「そのショットの残り ÷ カットの尺」を切り捨てた値（機械で計算した。手で書いていない）。
#    ⚠️ 尺が変わったら取り直す（`el_build --dry` の見込みが動いたら再計算）。
#
# 🔴🔴 台本 §4 の「実写 Ph1&2（〜）」30欄のうち、**13欄は主題が2本のどちらにも無い**
#    （夜の屋外・消防車・救急車・担架・門衛所・雪の砂漠）。**代用していない。**
#    → `ref/sl1/SHOTS_INDEX.md` §0／§3 と Vault の⑤b引き継ぎの表。
#    ⚠️ また、台本が Ph1&2 と書いた主題の多くは**実際には Ph3 に在る**（階段・除染・公道・空撮）。
#       リールを振り替えてある（同じ主題なので代用ではない）。
USE = {
    # ── 冒頭 ─────────────────────────────────────────
    # 🔴🔴 2026-09-07（⑤c' J-01/L-03）：**動画の1カット目に「THE END」が写っていた。**
    #    #137（1478〜1491）は SL-1 の敷地を俯瞰する理想的な引きだが、
    #    **1485.1秒から終幕タイトルがディゾルブで浮く**（`NOGO` を見よ）。
    #    ⚠️ 台帳の直し案「#135（1420〜1470）へ振り替える」は**不成立**＝#135 は
    #      屋内のトーキングヘッド（L-04）。#136 は ep06 が使っている（同じ俯瞰の続き）。
    #    → 絵は変えず、**読む秒を 1478.0〜1484.6 に縮めて rate で埋める**。
    #      式＝尺 11.57秒 × rate 0.57 ＝ 6.60秒。終わり 1484.60（浮き始めまで 0.50秒）。
    #      0.57 は本編で既に使っている遅回しの幅の中（c508 が 0.57）。
    "pr01": dict(clip="sl1_ph12", start=1478.0, until=1485.0, rate=0.57),
    "pr03": dict(clip="sl1_ph3", start=794.0, until=805.0, rate=0.88),   # #099 屋外の覆いのある階段
    "pr10": dict(clip="sl1_ph3", start=707.0, until=724.0),      # #087 クレーンのブームと建屋
    # ── 第2〜3章 ────────────────────────────────────
    "c202": dict(clip="sl1_ph3", start=1495.0, until=1511.0),    # #231 試験場の建物と道路の俯瞰
    "c301": dict(clip="sl1_ph3", start=258.0, until=273.0),      # #014 事故後の運転階（遠隔・白黒）
    "c305": dict(clip="sl1_ph3", start=208.0, until=216.0, rate=0.82),   # #008 敷地の空撮
    "c318": dict(clip="sl1_ph12", start=178.0, until=220.0),     # #023 炉内の残骸（49秒のショットの中）
    "c321": dict(clip="sl1_ph12", start=270.0, until=280.0),     # #032 炉内の残骸（色つき）
    # ── 第4〜6章 ────────────────────────────────────
    "c407": dict(clip="sl1_ph3", start=404.0, until=410.0, rate=0.67),   # #037 面体・防護具の受け渡し
    "c501": dict(clip="sl1_ph3", start=827.0, until=837.0, rate=0.88),   # #105 階段を上がる防護服
    "c504": dict(clip="sl1_ph3", start=690.0, until=696.0, rate=0.51),   # #084 建屋の外壁の開口部
    "c508": dict(clip="sl1_ph3", start=788.0, until=794.0, rate=0.57),   # #098 階段の2人
    "c520": dict(clip="sl1_ph3", start=805.0, until=812.0, rate=0.68),   # #100 階段とクレーン
    "c601": dict(clip="sl1_ph3", start=598.0, until=609.0, rate=0.96),   # #065 防護服の着脱
    "c603": dict(clip="sl1_ph3", start=1511.0, until=1519.0, rate=0.79),  # #232 床の除染
    # ── 第7章 ──────────────────────────────────────
    "c701": dict(clip="sl1_ph12", start=285.0, until=295.0),     # #034 炉内の残骸（色つき）
    "c708": dict(clip="sl1_ph3", start=724.0, until=739.0),      # #088 運転階の残骸の山
    "c710": dict(clip="sl1_ph3", start=1185.0, until=1193.0, rate=0.54),  # #170 クレーンと建屋（搬出）
    "c711": dict(clip="sl1_ph3", start=773.0, until=782.0, rate=0.93),   # #095 残骸の上の制御棒駆動部
    "c717": dict(clip="sl1_ph3", start=1406.0, until=1413.0, rate=0.62),  # #211 部品の計測
    # 🔴 c719「模型を作り、人が手で引く速さを測っている」は **Ph3 ではなく Ph1&2** に在る
    #    （実験室で駆動部を組み直す一連。台本の欄は Ph3 だが、実物はこちら）
    "c719": dict(clip="sl1_ph12", start=784.0, until=793.0, rate=0.83),  # #103 実験室での引き抜き試験
    "c726": dict(clip="sl1_ph3", start=1281.0, until=1289.0, rate=0.84),  # #186 工場の中へ入れる
    # ── 第8章 ──────────────────────────────────────
    "c801": dict(clip="sl1_ph3", start=424.0, until=440.0),      # #040 建屋の外に防護服の一団
    "c802": dict(clip="sl1_ph3", start=844.0, until=853.0, rate=0.78),   # #107 屋上のクレーンと作業員
    "c806": dict(clip="sl1_ph3", start=1220.0, until=1229.0, rate=0.90),  # #179 トレーラーの圧力容器
    "c807": dict(clip="sl1_ph3", start=1269.0, until=1277.0, rate=0.73),  # #184 工場へ入れる
    "c811": dict(clip="sl1_ph3", start=978.0, until=984.0, rate=0.65),   # #126 長い管を掲げる3人
    "c813": dict(clip="sl1_ph3", start=1387.0, until=1393.0),    # #207 鉄骨だけになった建屋
    "c814": dict(clip="sl1_ph3", start=1393.0, until=1399.0, rate=0.65),  # #208 鉄骨に取りつく作業員
    "c815": dict(clip="sl1_ph3", start=1368.0, until=1384.0),    # #205 ローダーと建屋
    "c821": dict(clip="sl1_ph3", start=1239.0, until=1255.0),    # #182 公道と工場
    "c822": dict(clip="sl1_ph3", start=1255.0, until=1269.0),    # #183 化学処理工場の建物
    # ── 第9章・締め ─────────────────────────────────
    "c905": dict(clip="sl1_ph3", start=893.0, until=906.0, rate=0.96),   # #115 試験場の遠景
    "c912": dict(clip="sl1_ph3", start=1654.0, until=1667.0, rate=0.70),  # #257 顕微鏡での分析
    "ep06": dict(clip="sl1_ph12", start=1470.0, until=1478.0, rate=0.92),  # #136 敷地の空撮（引き）
}
# ❌ 見たうえで**当てないと決めた**もの
#   ph12 #000 #001 #138／ph3 #000 #001 #002 #003 #269 #270
#     … NARA の収蔵カード・出所カード・表題・制作クレジット・End of Recording／SECOND PART TO FOLLOW
#   ph12 #020 #097 #110 #113 #127〜#135／ph3 #004 #006 #057 #264 #265
#     … スタジオの語り手（人物の寄り。この動画の文法に合わない）
#   ph12 #004 #005 #056 #109／ph3 #044 #259 #266〜#268
#     … 英字の札やグラフが焼き込まれている（こちらの注記と二重になる）
#   ph3 #255 #256 … 上半身裸の被検者（全身カウンタ・検診）。人物が特定できる寄り
#   4本目の分（87 Park・銘板・NIST ロゴ入りヘルメット・インタビューの顔）は git の 4e4c1fb にある。


# ── 🔴 G-11：カットの尻が、そのショットの終わりを越えていないか ─────────
#   なぜ要るか（2026-09-06・⑤c 見る C）
#     c703 と c726 は**検品画像が NIST の表題カードそのもの**だった。カットの尻が
#     注記の言うショットの終わり（「204秒からカード」「114秒からカード」）を
#     0.45秒・0.39秒だけ越えていたため。台本 §5 注意6「表題カードは使わない」に反し、
#     c726 は**実在の個人名のテロップ**まで出ていた。
#   ⚠️ 真因は「注記が自由記述で、機械が読んでいなかった」こと。だから注記ではなく
#     **`until=`（そのショットが終わる秒）**という欄を USE に足して、そこを見る。
#   しきい値 0.10秒（3コマ）… 本番 37カットに当てて出た越えは
#     0.01/0.03/0.05×3/0.06×2/0.09 と 0.16/0.21/0.39/0.43/0.45×3/0.65/5.29 に割れる。
#     台帳の ⚠️ と ・ の境がちょうどここ（[[feedback-gate-threshold-from-ledger-split]]）。
TOL = 0.10


def overruns(use=None, secs=None):
    """(cid, 越えた秒, start, end, until) の一覧。**判定はここ1本**（本番も検算も通る）。"""
    if secs is None:
        import scene_jiko as S
        secs = dict(S.CUTS)
    use = USE if use is None else use
    out = []
    for cid, u in use.items():
        if u.get("still"):
            # 静止画は1コマだけなので「尻がはみ出す」は起きないが、**その1コマが
            # ショットの中に在るか**は同じ根拠で言える（2026-09-07 追加）。
            # ⚠️ until を義務にしただけだと「数が入っていればよい」になるので、ここで意味を持たせる
            if u.get("until") is not None and float(u["start"]) > float(u["until"]):
                out.append((cid, float(u["start"]) - float(u["until"]),
                            float(u["start"]), float(u["start"]), float(u["until"])))
            continue
        if cid not in secs:
            continue
        # 🔴 fail closed：until が無いカットは「測れない」＝落とす（0 で埋めない）
        if u.get("until") is None:
            out.append((cid, None, float(u["start"]), None, None))
            continue
        end = float(u["start"]) + secs[cid] * float(u.get("rate", 1.0))
        gap = end - float(u["until"])
        if gap > TOL:
            out.append((cid, gap, float(u["start"]), end, float(u["until"])))
    return out


def missing_until(use=None):
    """🔴 `until=` が書いていない USE の欄（2026-09-07・設計ノート §9-5 で**必須**にした）。

    ⚠️ `overruns()` は静止画（`still=True`）を飛ばすが、こちらは**全部の欄**を見る。
       静止画でも「そのショットが何秒で終わるか」は切り出しの当たりを決める根拠なので、
       書いていないなら**書いてから通す**（自由記述の注記に書き戻さない）。
    ⚠️ ここが空でも `overruns()` は 0件と答えられてしまう＝**黙って通る穴**になる。
       なので `fetch --check` は overrun（exit 1）より重い **exit 2** で落とす。
    """
    use = USE if use is None else use
    return sorted(c for c, u in use.items() if u.get("until") is None)


def check_until():
    """(はみ出し, until が無い欄, ショットをまたいだ欄) を返す。呼び手が exit コードを決める。"""
    miss = missing_until()
    for cid in miss:
        print(f"  🔴 {cid}: until= が無い（そのショットが何秒で終わるか機械が読めない）")
    bad = [r for r in overruns() if r[1] is not None]
    for cid, gap, st, end, until in sorted(bad, key=lambda r: -r[1]):
        print(f"  🔴 {cid}: 尻が {gap:+.2f}秒 はみ出す"
              f"（{st:.1f}〜{end:.2f}秒／ショットの終わり {until:.1f}秒）")
    out = outside_shot()
    for cid, clip, a, b, sh in out:
        if sh is None:
            print(f"  🔴 {cid}: start={a:.1f}秒 が {clip} のどのショットにも入っていない")
        else:
            print(f"  🔴 {cid}: {a:.1f}〜{b:.1f}秒 が**ショットをまたぐ**"
                  f"（{clip} の実測ショットは {sh[0]:.0f}〜{sh[1]:.0f}秒）"
                  f"＝範囲の中で絵が別物になる")
    if miss:
        print(f"🔴 `until=` が無い欄が {len(miss)} 件（必須。書くまで切り出さない）")
    if bad:
        print(f"🔴 ショットの終わりを {TOL:.2f}秒 より越えているカットが {len(bad)} 件")
    if out:
        print(f"🔴 実測のショットをまたいでいるカットが {len(out)} 件"
              f"（秒は ref/sl1/shots.json から採る）")
    nog = in_nogo()
    for cid, clip, a, b, x0, x1, why in nog:
        print(f"  🔴 {cid}: {a:.1f}〜{b:.2f}秒 が**使ってはいけない秒** "
              f"{x0:.1f}〜{x1:.1f} に掛かる（{clip}）＝{why}")
    if nog:
        print(f"🔴 使ってはいけない秒に掛かっているカットが {len(nog)} 件"
              f"（`footage.NOGO` を見よ。rate を下げるか、別のショットへ振り替える）")
    if not miss and not bad and not out and not nog:
        n_sh = sum(len(v) for v in SHOTS.values())
        print(f"✓ 全 {len(USE)} 欄に until= があり、尻のはみ出しも "
              f"ショットまたぎも無く、使ってはいけない秒にも掛かっていない"
              f"（実測ショット {n_sh} 本と照合）")
    return bad, miss, out, nog


def selftest():
    """陽性対照。**本番の判定関数そのもの**に、わざと壊した欄を入れて鳴らす。

    🔴 2026-09-07（5本目）：**作り物の USE で回すように書き直した。**
       前の版は本番の `USE` から犠牲者を1つ選んでいたので、題材を替えて `USE = {}` に
       した瞬間に「素で通っているカットが無い」で落ちた＝**題材の切れ目に検算ができない**。
       陽性対照は本番の中身が空でも通らなければならない。
       → [[feedback-selftest-must-not-reach-real-side-effects]]
    """
    ok = []

    def chk(name, got, want):
        ok.append(got == want)
        print(f"  {'✓' if got == want else '🔴'} {name} … "
              f"{'鳴る' if got else '黙る'}（期待 {'鳴る' if want else '黙る'}）")

    # 作り物のショット表＝10〜20秒／20〜35秒 の2本
    keep_shots, keep_use, keep_clips = dict(SHOTS), dict(USE), dict(CLIPS)
    keep_nogo = dict(NOGO)
    try:
        globals()["SHOTS"] = {"t_clip": [(10.0, 20.0, 5.0), (20.0, 35.0, 1.0)]}
        CLIPS["t_clip"] = dict(url="http://example.invalid/t.mp4", sec=35.0,
                               w=1920, h=1080, credit="（検算用）", note="", stream=True)
        secs = {"x01": 6.0, "x02": 6.0, "x03": 6.0}

        # ① overruns：尻がショットの終わりを越える
        base = dict(clip="t_clip", start=12.0, until=20.0)      # 12+6=18 ≦ 20 → 黙る
        chk("尻が内側（12.0〜18.0／終わり20.0）", bool(overruns({"x01": base}, secs)), False)
        chk("尻が 0.5秒 はみ出す",
            bool(overruns({"x01": dict(base, until=17.5)}, secs)), True)
        chk("しきい値の内側（0.05秒）",
            bool(overruns({"x01": dict(base, until=17.95)}, secs)), False)
        chk("until が無い（fail closed）",
            bool(overruns({"x01": dict(clip="t_clip", start=12.0)}, secs)), True)

        # ② missing_until：静止画の欄も見る（overruns は静止画を飛ばす）
        chk("until 無しを missing_until が名指しで拾う",
            missing_until({"x01": dict(clip="t_clip", start=12.0)}) == ["x01"], True)
        chk("静止画でも until 無しを拾う",
            missing_until({"x02": dict(clip="t_clip", start=12.0, still=True)}) == ["x02"], True)

        # ③ 🔴 outside_shot：数は入っているが実測のショットをまたぐ（4本目で3件踏んだ穴）
        chk("1本のショットに収まっている（12.0〜20.0）",
            bool(outside_shot({"x01": dict(clip="t_clip", start=12.0, until=20.0)})), False)
        chk("ショットをまたぐ（12.0〜25.0＝境目20.0を越える）",
            bool(outside_shot({"x01": dict(clip="t_clip", start=12.0, until=25.0)})), True)
        chk("start がどのショットにも入らない（5.0秒）",
            bool(outside_shot({"x01": dict(clip="t_clip", start=5.0, until=8.0)})), True)
        chk("静止画でもまたぎを見る",
            bool(outside_shot({"x02": dict(clip="t_clip", start=12.0, until=25.0, still=True)})),
            True)
        chk("ショット表の無いクリップは対象外（fail open にしない＝黙る）",
            bool(outside_shot({"x03": dict(clip="sl1_ph12", start=12.0, until=25.0)})), False)

        # ④ 🔴 in_nogo：**書いた数は正しいのに、実際に読む秒が禁止の秒に掛かる**
        #    （2026-09-07・pr01 がその実例。until はショットの終わりとして正しかった）
        globals()["NOGO"] = {"t_clip": [(17.0, 30.0, "（検算用）表題カード")]}
        chk("読む秒が禁止の秒に掛かる（12.0〜18.0／禁止 17.0〜）",
            bool(in_nogo({"x01": dict(clip="t_clip", start=12.0, until=20.0)}, secs)), True)
        chk("rate を下げれば掛からない（12.0〜15.0）",
            bool(in_nogo({"x01": dict(clip="t_clip", start=12.0, until=20.0, rate=0.5)},
                         secs)), False)
        chk("until が正しくても読む秒で判定する（until=20.0 は禁止に掛からない）",
            bool(in_nogo({"x01": dict(clip="t_clip", start=12.0, until=17.0)}, secs)), True)
        chk("静止画は1コマだけなので掛からない（start=12.0）",
            bool(in_nogo({"x02": dict(clip="t_clip", start=12.0, until=20.0, still=True)},
                         secs)), False)
        chk("禁止の表に無いクリップは対象外",
            bool(in_nogo({"x03": dict(clip="zz_clip", start=12.0, until=20.0)}, secs)), False)

        # ⑤ exit コードが 2（until 無し）→ 3（またぎ）→ 4（禁止の秒）の順で重いこと
        import scene_jiko as S
        keep_cuts = S.CUTS
        try:
            S.CUTS = [("x01", 6.0)]
            globals()["USE"] = {"x01": dict(clip="t_clip", start=12.0)}
            rc2 = fetch(check=True)
            globals()["USE"] = {"x01": dict(clip="t_clip", start=12.0, until=25.0)}
            rc3 = fetch(check=True)
            globals()["USE"] = {"x01": dict(clip="t_clip", start=12.0, until=20.0)}
            rc4 = fetch(check=True)                       # 禁止 17.0〜 に掛かる
            globals()["NOGO"] = {}
            rc0 = fetch(check=True)
        finally:
            S.CUTS = keep_cuts
        for name, rc, want in (("until 無し", rc2, 2), ("ショットまたぎ", rc3, 3),
                               ("禁止の秒", rc4, 4), ("正しい欄", rc0, 0)):
            ok.append(rc == want)
            print(f"  {'✓' if rc == want else '🔴'} {name} → `fetch --check` exit {rc}（期待 {want}）")
    finally:
        globals()["SHOTS"] = keep_shots
        globals()["USE"] = keep_use
        globals()["CLIPS"] = keep_clips
        globals()["NOGO"] = keep_nogo

    # ⚠️ 本番の状態は「検算の合否」と分けて必ず表に出す（道具の緑と中身の緑を混ぜない）
    now = missing_until(USE)
    n_sh = sum(len(v) for v in SHOTS.values())
    print(f"  ⚠️ いまの本番：USE {len(USE)}欄（until 無し {len(now)}）／"
          f"実測ショット {n_sh}本／クリップ {len(CLIPS)}本")
    good = all(ok)
    print("  " + (f"✓ 陽性対照 {len(ok)}/{len(ok)}" if good
                  else f"🔴 陽性対照 {sum(ok)}/{len(ok)} で落ちた"))
    return good


def urls_of(name):
    c = CLIPS[name]
    if c.get("url"):
        return [c["url"]]
    raise RuntimeError(f"{name} に url がない（4本目の Kaltura 経由は git の 4e4c1fb にある）")


def have(cid):
    """そのカットのコマが切り出してあるか。無ければ静止画に落ちる（壊れない）。"""
    return (FOOT / cid / "00000.jpg").exists()


def credit_of(cid):
    return CLIPS[USE[cid]["clip"]]["credit"] if cid in USE else None


def _cut_stream(cid, u, secs):
    """URL から、そのカットに要る区間だけをコマに切り出す（落とさない）。"""
    c = CLIPS[u["clip"]]
    rate = float(u.get("rate", 1.0))
    n = int(round(secs * FPS)) + 2
    vf = []
    if abs(rate - 1.0) > 1e-6:
        vf.append(f"setpts={1.0 / rate:.4f}*PTS")
    vf.append(f"fps={FPS}")
    # 4K はそのまま切り出すと 1コマ 1.5MB。寄り（zoom）に要る幅だけ残して縮める
    want = min(int(c["w"]), int(round(1920 * float(u.get("zoom", 1.0)) * 1.02)))
    if want < int(c["w"]):
        vf.append(f"scale={want}:-2")
    d = FOOT / cid
    d.mkdir(parents=True, exist_ok=True)
    last = None
    for url in urls_of(u["clip"]):
        for attempt in range(3):
            cmd = ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
                   "-user_agent", UA, "-ss", f"{float(u['start']):.2f}", "-i", url,
                   "-t", f"{secs + 0.6:.2f}", "-vf", ",".join(vf),
                   "-frames:v", str(n), "-q:v", "3", "-start_number", "0",
                   str(d / "%05d.jpg")]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            got = len(list(d.glob("*.jpg")))
            if r.returncode == 0 and got >= n - 4:
                return got, n
            last = (r.stderr or "").strip()[-200:] or f"コマ {got}/{n}"
            print(f"     ⚠️ {cid}: {last}（{attempt + 1}回目）", flush=True)
            time.sleep(4 * (attempt + 1))
    return len(list(d.glob("*.jpg"))), n


def fetch(check=False):
    import scene_jiko as S
    secs = dict(S.CUTS)
    missing = [c for c in USE if c not in secs]
    if missing:
        print(f"🔴 台本に無いカットに動画を割り当てている: {missing}")
        return 1
    stills = [c for c, u in USE.items() if u.get("still")]
    print(f"■ 動画を当てるカット {len(USE) - len(stills)} 件（＋静止画で受ける {len(stills)} 件: {' '.join(stills)}）")
    for cid, u in USE.items():
        c = CLIPS[u["clip"]]
        if u.get("still"):
            print(f"  {cid}  尺{secs[cid]:5.2f}s  ← {u['clip']} {u['start']:.1f}秒の静止画（fb_{cid}.jpg・ゆっくり寄る）")
            continue
        rate = float(u.get("rate", 1.0))
        end = float(u["start"]) + secs[cid] * rate
        flag = "" if end <= float(c["sec"]) + 0.05 else "  🔴 動画の終端を越える"
        print(f"  {cid}  尺{secs[cid]:5.2f}s  ← {u['clip']} {u['start']:.1f}〜{end:.1f}秒"
              f"（{rate:.2f}倍速）{flag}")
    over, miss, out, nog = check_until()
    # 🔴 `until=` は必須（2026-09-07・設計ノート §9-5）。無ければ **exit 2** で落とす。
    #    ⚠️ はみ出し（exit 1）より重い。「測れる状態になっていない」ので切り出しにも進まない
    if miss:
        print("🔴 exit 2 ＝ `until=`（そのショットが終わる秒）を USE に書いてから通す。"
              "秒は `ref/sl1/shots.json`（1秒刻みの実測）から採る")
        return 2
    # 🔴 exit 3 ＝ 数は入っているが、実測のショットをまたいでいる（2026-09-07・5本目で追加）。
    #    ⚠️ until= を必須にしただけでは「数が入っていればよい」で終わり、4本目で3件踏んだ
    #       「注記の範囲の中で絵が別物」がそのまま通る。ここが**その穴**を塞ぐ門番
    if out:
        print("🔴 exit 3 ＝ (start, until) を1本のショットの中に収める。"
              "`python tools/shots.py show ref/sl1/shots.json --key <clip>` で境目を見る")
        return 3
    # 🔴 exit 4 ＝ 実際に読む秒が「使ってはいけない秒」に掛かる（2026-09-07・5本目 ⑤c'）。
    #    ⚠️ exit 2/3 は**書いた数**を見る門番で、ここだけが**実際に読む範囲**を見る。
    #       pr01 は until=1491.0（ショットの終わり）と正しく書いてあったのに、
    #       尺 10.72秒 × rate 1.0 ＝ 1488.7秒まで読み、終幕タイトルを画面に出していた。
    if nog:
        print("🔴 exit 4 ＝ `footage.NOGO` の秒に掛かっている。"
              "rate を下げて読む秒を縮めるか、別のショットへ振り替える")
        return 4
    if check:
        return 1 if over else 0
    bad = 0
    for cid, u in USE.items():
        if u.get("still"):
            continue
        if have(cid):
            print(f"  {cid}: すでにある", flush=True)
            continue
        print(f"  {cid}: {u['clip']} の {u['start']}秒目から切り出す", flush=True)
        try:
            got, n = _cut_stream(cid, u, secs[cid])
        except Exception as e:                           # noqa: BLE001
            print(f"  🔴 {cid}: {type(e).__name__}: {e}")
            bad += 1
            continue
        print(f"     → {got}コマ（要 {n}）")
        if got < n - 4:
            print(f"  🔴 {cid}: コマが足りない（{got}/{n}）。start が終端に近すぎる")
            bad += 1
    done = [c for c in USE if have(c)]
    print(f"✓ 切り出し完了 {len(done)}/{len(USE) - len(stills)} カット: {'、'.join(done) or 'なし'}")
    if bad:
        print(f"⚠️ {bad} カットは**静止画に落ちる**。パイプラインは止めない。")
    return 1 if bad else 0


if __name__ == "__main__":
    if "scan" in sys.argv:
        # 4本目は Kaltura から範囲取得で見取り図を作った（scratchpad の sheet_*.jpg）。ここでは作らない
        print("scan は4本目では使わない（見取り図は手元で作った）。何もしない")
        sys.exit(0)
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    sys.exit(fetch(check="--check" in sys.argv))
