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

■ 🔴 秒数は**目で決めない。`SHOT_FILE`（いまは `ref/keybridge/shots.json`）から採る**
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

# ── 6本目：フランシス・スコット・キー橋 崩落（2024-03-26）の PD 動画 28本 ────────
# 🔴 5本目 SL-1（NARA MoPix の記録映画2本）の CLIPS/USE/PILLAR/NOGO は git の `58cd823` にある。
#    カットIDが題材をまたいでぶつかるので**残さない**。
#
# 🔴 5本目までと造りが違うところ（2026-09-08・6本目②）
#    ・**素材が1〜2本ではなく28本**（合計49.7分）。名前は DVIDS の識別子（`240407-A-PA223-1003`）。
#      表をこのファイルに直に書くと60行の literal になるので、**実測から作った JSON を読む**。
#      正本＝`ref/keybridge/clips.json`（`tools/keybridge_index.py` が作る。git に載せる）。
#    ・ショットの境目の台帳＝`ref/keybridge/SHOTS_INDEX.md`（**全355ショット・1秒刻み**）。
#      `USE` の `start=` / `until=` はこの台帳の値をそのまま写す。**推測で書かない。**
#
# 🔴 権利（②素材で1点ずつ確かめた。詳細は `ref/CREDITS.md` §キー橋）
#    28本すべて Commons で Public domain。撮影は米沿岸警備隊・米陸軍工兵隊・NTSB の職務著作
#    ＝合衆国法典 17編105条。⚠️ **写真のほうは事情が違う**（郡が自分で PD 宣言したものが191点、
#    州知事室の CC BY が582点ある）。動画と写真を同じ「PD」で数えない。
#    ⚠️ 残る危険＝B-roll に第三者の映像が混ざる可能性。ショットを選ぶときに局のロゴを見る。
#    ⚠️ **ホワイトハウスの総集編『A look back at March 2024』（23.9分）は入れていない**
#       （キー橋以外が大半で、報道由来の映像が混ざる）。
#
# ⚠️ `upload.wikimedia.org` は名乗らないと **429**。下の UA を必ず渡す（`shots.UA` と同じ役目）。
_CLIPS_JSON = HERE / "ref" / "keybridge" / "clips.json"
CLIPS = json.loads(_CLIPS_JSON.read_text(encoding="utf-8")) if _CLIPS_JSON.exists() else {}

# 🔴🔴 2026-09-07（5本目 SL-1 ⑤c'・K-12）：**素材そのものが横に黒帯を持っている。**
#    NARA の MoPix は 4:3 の原版を **1920×1080 の箱に 1440×1080 で入れて**配信している。
#    ＝左右 240px ずつが黒。`USE` は 35欄すべて zoom を書いていなかったので、
#    **記録映画のカット全部の左右に黒帯が出たまま焼けていた**（台帳 K-12・J-05）。
#    ⚠️ 台帳 A-03（c107 c108）は誤報で、こちらが本体（35カット全部の話）。
#    実測＝切り出したコマ 35本を1枚ずつ測って **全部が x240〜1679（絵の幅 1440）**。
#    要る寄り ＝ 1920/1440 = **1.3333**。ここに置いて**1か所で効かせる**
#    （35欄に書くと、欄を足したときに書き忘れる）。
#
# 🔴 2026-09-08（6本目②）: **空にした。まだ測っていないので 1.0 でなく「未測」である。**
#    キー橋の28本は 3840×2160 と 1920×1080 が主で、名目の縦横比は 16:9。
#    ただし **`720×958` と `480×848` の2本は縦位置**（携帯・機内撮影）で、全画面には使えない。
#    ⚠️ **名目の寸法は黒帯の有無を教えない**（SL-1 も 1920×1080 と名乗って中身は 1440）。
#    → ⑤で切り出したコマを `measure_pillar(cid)` で1本ずつ測ってから、必要な欄だけここに書く。
PILLAR = {}


def zoom_of(cid, u=None):
    """そのカットに実際にかける寄り。**素材の黒帯ぶんを必ず含める。**

    ＝ 欄に書いた `zoom`（画作りの寄り） × 1/PILLAR（黒帯を画面の外へ出す寄り）。
    """
    u = (USE.get(cid) if u is None else u) or {}
    pl = PILLAR.get(u.get("clip"), 1.0)
    return float(u.get("zoom", 1.0)) / max(pl, 1e-6)


def measure_pillar(cid):
    """切り出したコマから、**その素材の絵の幅の割合**を測る（PILLAR の検算）。

    🔴 定数は腐る（[[feedback-gates-go-stale-when-upstream-changes]]）。
       配信の版が変わって黒帯の幅が変われば、書いてある 1440/1920 は黙って間違う。
       → 実際に切り出したコマを測って突き合わせる。コマが無ければ None（0 で埋めない）。
    """
    fs = sorted((FOOT / cid).glob("*.jpg"))
    if not fs:
        return None
    from PIL import Image
    import numpy as np
    a = np.asarray(Image.open(fs[len(fs) // 2]).convert("L")).astype(float)
    w = a.shape[1]
    med = np.median(a, axis=0)
    xs = [x for x in range(w) if med[x] >= 18]      # 18 未満＝黒帯（実測の帯は 0〜3）
    if not xs:
        return None
    return (max(xs) - min(xs) + 1) / w


def bars_left(cid, u=None):
    """その寄りで**残る黒帯の幅**（画面の片側・px）。0 なら消えている。"""
    u = (USE.get(cid) if u is None else u) or {}
    pl = PILLAR.get(u.get("clip"), 1.0)
    return max(0.0, 960.0 - 960.0 * pl * zoom_of(cid, u))


# ── 🔴 ショットの境目（`tools/shots.py` で1秒刻みに実測）────────────
# 4本目は「128〜133.9秒 レプリカの全景」と書いた**範囲の中で絵が別物**だった（3件）。
# 秒を3秒刻みの見取り図で選んでいたのが原因。→ [[feedback-measure-the-source-before-choosing-the-crop]]
# ここに実測のショット表を持たせ、`USE` の (start, until) が**1本のショットに収まっているか**を
# 機械で見る（`outside_shot()`）。⚠️ ffmpeg の scene 検出だけでは**ディゾルブを見ない**ので、
# 1秒ごとの見た目の署名で採ってある（1本のショットが333秒、という嘘が出ていた）。
#
# 🔴🔴 2026-09-08（6本目②）：**ここのパスを題材ごとに差し替えるのを忘れない。**
#    素材のパスを名指しした門番は、題材を替えると「0件を調べて合格」になる
#    （5本目で370件が隠れていた）。→ [[feedback-gates-blind-to-the-new-material]]
#    ＝ `SHOTS` が空のまま `outside_shot()` を回すと、**全欄が「対象外」で素通り**する。
#    そうならないように `unknown_clip()` を足した（`fetch --check` が呼ぶ）。
SHOTS = {}
SHOT_FILE = HERE / "ref" / "keybridge" / "shots.json"      # 6本目。前は ref/sl1/shots.json
if SHOT_FILE.exists():
    _sd = json.loads(SHOT_FILE.read_text(encoding="utf-8"))
    SHOTS = {k: [(s["start"], s["until"], s["motion"]) for s in v["shots"]]
             for k, v in _sd.items()}


def unknown_clip(use=None):
    """🔴 `USE` が使っているのにショット表が無いクリップ。**在れば止める。**

    `outside_shot()` はショット表の無いクリップを「対象外」として飛ばすので、
    表のパスが古い題材を向いたままだと**全欄が黙って通る**。ここがその穴を塞ぐ。
    """
    use = USE if use is None else use
    return sorted({u.get("clip") for u in use.values()
                   if u.get("clip") not in SHOTS})


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
    # 🔴 2026-09-08（6本目②）: **空にした。「危険が無い」ではなく「まだ見ていない」。**
    #    5本目は⑤c' で1カット目に『THE END』が写っていたのを見つけて足した欄。
    #    キー橋の28本は DVIDS の B-roll なので終幕タイトルは想定しにくいが、
    #    ⚠️ **局のロゴ・提供クレジット・DVIDS のスレート**が頭尻に入る型は在りうる。
    #    → ⑤でショットを見たときに、見つけたぶんをここへ書く。
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
#   5. 秒は `ref/keybridge/SHOTS_INDEX.md`（1秒刻みの実測）から写す。目分量で書かない
#
# 書き方（4本目の例。数は SL-1 のものに置き換える）
#     "c103": dict(clip="sl1_ph12", start=412.0, until=421.0),
#     "c118": dict(clip="sl1_ph3", start=88.0, until=94.0, rate=0.6),
#     "c204": dict(clip="sl1_ph12", start=735.0, still=True, until=741.0),
# 🔴 2026-09-07（⑤b）：**全410ショットを見て決めた35欄。** 台帳＝`ref/sl1/SHOTS_INDEX.md`。
#    (start, until) は `ref/sl1/shots.json`（当時）の実測ショットの境目そのもの。
#    `rate` は「そのショットの残り ÷ カットの尺」を切り捨てた値（機械で計算した。手で書いていない）。
#    ⚠️ 尺が変わったら取り直す（`el_build --dry` の見込みが動いたら再計算）。
#
# 🔴🔴 台本 §4 の「実写 Ph1&2（〜）」30欄のうち、**13欄は主題が2本のどちらにも無い**
#    （夜の屋外・消防車・救急車・担架・門衛所・雪の砂漠）。**代用していない。**
#    → `ref/sl1/SHOTS_INDEX.md` §0／§3 と Vault の⑤b引き継ぎの表。
#    ⚠️ また、台本が Ph1&2 と書いた主題の多くは**実際には Ph3 に在る**（階段・除染・公道・空撮）。
#       リールを振り替えてある（同じ主題なので代用ではない）。
USE = {
    # 🔴 2026-09-08（6本目②）: **空にした。**④の台本が通ってから書く。
    #
    # 書き方（守らないと `fetch --check` が止まる）:
    #   "c101": dict(clip="240326-G-KH296-2189", start=12.0, until=22.0, rate=0.97),
    #   ・`clip` は `ref/keybridge/clips.json` の鍵（＝DVIDS の識別子）
    #   ・🔴 **`until=` は全欄に必ず書く**（無いと exit 2。4本目は静止画4欄が空のまま通っていた）
    #   ・`start` / `until` は **`ref/keybridge/SHOTS_INDEX.md` のショットの境目をそのまま写す**。
    #     ⚠️ ショットの範囲の中で絵が別物になることがある（4本目で3件踏んだ）ので、
    #        **境目をまたがない**。またぐと `footage.outside_shot()` が exit 3 で止める。
    #   ・`rate` は「そのショットの長さ ÷ カットの尺」を切り捨てた値。台帳の「rate の目安」欄に出してある。
    #
    # 素材の下ごしらえ（②で実測ずみ）:
    #   28本・49.7分・355ショット。**8秒以上が152本（うち動きのあるもの142本）**
    #   ＝1カット 10.29秒 をそのまま埋められる玉。
    #   ⚠️ **崩落の瞬間の映像は無い**（当日撮影は3本だけで、どれも崩落後）。
    #
    # ==============================================================
    # 2026-09-08（⑤b-4 実写【見る】）: 35欄。**手で書いていない。**
    #   正本＝`tools/keybridge_pick.py` の `PICK`（カットID・クリップ・ショット番号だけ）。
    #   秒と rate はそこで計算して書き出す（`python tools/keybridge_pick.py`）。
    #   ⚠️ **直すときは `PICK` を直して書き出し直す**（ここを手で書き換えない）。
    #
    # `until` は「ショットの終わり −1.0秒」にしてある
    #   ②の境目は `tools/shots.py` が1秒に1コマの標本から出していて、`boundaries()` は
    #   境目を**後ろ側の秒**に置く。＝ ショット [a,b) の t=b は**もう次のショット**で、
    #   本当の切れ目は (b-1, b] のどこか。until=b のままだと、カットの尻に
    #   次のショットの絵が最大1秒混じる。**outside_shot() は同じ台帳を読むので鳴らない。**
    #
    # 台帳に出てこないスレートを、1秒の地図で全部の秒について弾いてある
    #   `out/jiko/kb1s/map.json`（28本を1秒に1コマ・真っ暗／焼き込み文字／顔）。
    #   実例＝`240401-G-TL908-2303` の「#14 64〜76秒」の中の 66〜67秒が真っ黒の
    #   スレート（`MEDIUM / BOW ... DALI`）。台帳には現れない。
    #   ⚠️ NTSB の3本は頭と尻に**濃紺の題字カード**が入る（真っ暗ではないので
    #      暗さの網では落ちない）。`keybridge_shotscan.is_card()` で落としてある。
    # ==============================================================
    # <<<KB_USE ここから ここまでは `python tools/keybridge_pick.py --apply` が書く。手で触らない
    # 崩落した中央径間の空撮（2024-03-26）
    "pr01": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=54.0, until=82.0),
    # 未明・応急艇の操舵席と落ちた橋
    "pr02": dict(clip="240326-G-KH296-2189", start=12.0, until=21.0, rate=0.94),
    # 水面に沈んだトラスと橋脚
    "pr03": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=130.0, until=151.0),
    # NTSB 調査員がトラスを撮る（後ろ姿）
    "pr05": dict(clip="NTSB_B_Roll_Investigators_Aboard_the_Car", start=179.0, until=189.0, rate=0.91),
    # ダリの船首に載った橋桁（寄り）
    "pr08": dict(clip="240330-A-PA223-1001", start=34.0, until=43.0, rate=0.89),
    # ダリの船体と凪いだ水面
    "c215": dict(clip="NTSB_B_Roll_Investigators_Aboard_the_Car", start=109.0, until=126.0),
    # ダリの船尾（船名と船籍港が写る）
    "c301": dict(clip="240331-A-PA223-1003", start=0.0, until=8.0, rate=0.74),
    # 橋へ向かう主航路（空撮・広い）
    "c318": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=306.0, until=337.0),
    # ダリの操舵室（窓の外に落ちた橋）
    "c306": dict(clip="NTSB_B_Roll_Hazardous_Material_Investiga", start=365.0, until=371.0, rate=0.55),
    # 航海データ記録装置を吸い出す手元
    "c405": dict(clip="NTSB_B_Roll_Hazardous_Material_Investiga", start=383.0, until=391.0, rate=0.73),
    # 操舵室の操作卓（手元と計器）
    "c411": dict(clip="NTSB_B_Roll_Hazardous_Material_Investiga", start=443.0, until=449.0, rate=0.60),
    # ダリの船橋（操舵室の中）
    "c409": dict(clip="NTSB_B_Roll_Hazardous_Material_Investiga", start=403.0, until=415.0),
    # 橋と主航路（船の長さを見せる広い空撮）
    "c424": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=276.0, until=305.0),
    # 崩落直後の橋（空撮・寄り）
    "c508": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=159.0, until=165.0, rate=0.87),
    # 崩落した径間と橋脚（空撮）
    "c512": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=87.0, until=105.0),
    # 崩落した径間（空撮・引き）
    "c517": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=244.0, until=275.0),
    # 水面に散った残骸
    "c519": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=168.0, until=181.0),
    # 折れた17番橋脚まわり（空撮）
    "c601": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=112.0, until=122.0),
    # 船首の上に載った橋桁
    "c607": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=229.0, until=243.0),
    # 崩落現場の全景（引きの空撮）
    "c616": dict(clip="240401-G-TL908-2303", start=153.0, until=180.0),
    # 潰れたコンテナと橋桁（真上から）
    "c617": dict(clip="240407-G-DV874-3002", start=56.0, until=66.0),
    # 夜明けの現場（応急艇から）
    "c619": dict(clip="240326-G-KH296-2189", start=47.0, until=57.0, rate=0.82),
    # 航路に残るダリ（横から）
    "c701": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=338.0, until=352.0),
    # 現場の空撮（引き）
    "c806": dict(clip="240401-G-TL908-2303", start=103.0, until=131.0),
    # 橋脚と現場の空撮
    "c818": dict(clip="240401-G-TL908-2303", start=45.0, until=53.0, rate=0.84),
    # 現場の空撮（クレーン台船）
    "c819": dict(clip="240401-G-TL908-2303", start=54.0, until=63.0, rate=0.90),
    # 崩落現場（撤去が始まる前）
    "c823": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=353.0, until=368.0),
    # 塞がった航路（引きの空撮）
    "c901": dict(clip="240401-G-TL908-2303", start=135.0, until=149.0),
    # 各機関の調査員が船上で支度をする
    "c903": dict(clip="240327-A-SE916-1046", start=10.0, until=21.0),
    # 潜水士の支度（潜る）
    "c904": dict(clip="240404-G-KY623-1002", start=36.0, until=59.0),
    # トラスを溶断する作業員
    "c905": dict(clip="240330-G-LB555-1001", start=78.0, until=103.0),
    # コンテナを載せた台船
    "c907": dict(clip="240407-A-PA223-1003", start=27.0, until=35.0),
    # 仮設航路を通る台船
    "c908": dict(clip="240401-G-LB555-1002", start=10.0, until=31.0),
    # トラスを運ぶクレーン台船
    "c909": dict(clip="240407-A-PA223-1005", start=10.0, until=15.0, rate=0.71),
    # 崩落した中央径間（空撮）
    "ca01": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=369.0, until=385.0),
    # 残った桁と崩落部（空撮）
    "ep01": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=404.0, until=429.0),
    # 崩落現場（引きの空撮）
    "ep05": dict(clip="NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc", start=430.0, until=443.0),
    # KB_USE>>> ここまで
}
# 🔴 まだ決まっていない 29欄（**代用で埋めていない**）＝ Vault の ⑤b-4 引き継ぎ §3
#   数え方の正本＝`python tools/check_footage_slots.py`（カットの側から数える）。
#   ⚠️ `fetch --check` の「✓ 全37欄」は **USE に書いた欄しか数えていない**。
#
#   (A) 事故前が主題（動画28本は**全部が崩落後**）17欄
#       c201 c203 c212 c213 c214 c414 c502 c503 c515 c518 c520 c610 c801 c802 c813 ca09 ep06
#       → `ss.PRE_*`（事故前の写真7点）を当てるか、図に落とす。⑤b-5 で決める。
#   (B) 機関室・高圧配電盤・錨まわり（28本の中に**1コマも無い**）10欄
#       c311 c316 c417 c421 c426 c703 c704 c706 c708 ca03
#       → 報告書の図版（`ss.page()`）に落とすのが素直。第7章はもともと図の章。
#   (C) 主題は在るが玉が足りない 2欄
#       c307（離岸のタグボート＝崩落後のタグしか無い）
#       c914（ダリの出港＝2024-06-24 の映像が28本の中に無い。撮影は3/26〜4/11 と 10/4）
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
              f"（秒は {SHOT_FILE} から採る）")
    # 🔴 素材の黒帯（K-12）。書いた寄りで**帯が消えるか**を式で見る
    bars = [(cid, bars_left(cid)) for cid in sorted(USE) if bars_left(cid) > 0.5]
    for cid, w in bars:
        print(f"  🔴 {cid}: 素材の黒帯が片側 {w:.0f}px 残る"
              f"（zoom_of={zoom_of(cid):.4f}／要る寄り "
              f"{1 / PILLAR.get(USE[cid].get('clip'), 1.0):.4f} 以上）")
    if bars:
        print(f"🔴 素材の黒帯が残るカットが {len(bars)} 件"
              f"（`footage.PILLAR` と `zoom_of()` を見よ）")
    nog = in_nogo()
    for cid, clip, a, b, x0, x1, why in nog:
        print(f"  🔴 {cid}: {a:.1f}〜{b:.2f}秒 が**使ってはいけない秒** "
              f"{x0:.1f}〜{x1:.1f} に掛かる（{clip}）＝{why}")
    if nog:
        print(f"🔴 使ってはいけない秒に掛かっているカットが {len(nog)} 件"
              f"（`footage.NOGO` を見よ。rate を下げるか、別のショットへ振り替える）")
    if not miss and not bad and not out and not nog and not bars:
        n_sh = sum(len(v) for v in SHOTS.values())
        print(f"✓ 全 {len(USE)} 欄に until= があり、尻のはみ出しも "
              f"ショットまたぎも無く、使ってはいけない秒にも掛かっておらず、"
              f"素材の黒帯も残らない（実測ショット {n_sh} 本と照合）")
    return bad, miss, out, nog, bars


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
    keep_pillar = dict(PILLAR)
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

        # ⑤ 🔴 PILLAR：素材の黒帯を寄りで消す（K-12）。**定数は実測と突き合わせる**
        globals()["PILLAR"] = {"t_clip": 0.75}
        chk("zoom を書かなければ帯ぶんだけ寄る（1/0.75＝1.3333）",
            abs(zoom_of("x01", dict(clip="t_clip")) - 4 / 3) < 1e-9, True)
        chk("欄の zoom は帯の寄りに掛け算される（1.2 → 1.6）",
            abs(zoom_of("x01", dict(clip="t_clip", zoom=1.2)) - 1.6) < 1e-9, True)
        chk("その寄りなら帯は残らない",
            bars_left("x01", dict(clip="t_clip")) < 0.5, True)
        chk("寄りを 1.0 に固定すると帯が残る（片側 240px）",
            abs(bars_left("x01", dict(clip="t_clip", zoom=0.75)) - 240.0) < 1.0, True)
        chk("帯の表に無いクリップは寄らない（1.0 のまま）",
            abs(zoom_of("x03", dict(clip="zz_clip")) - 1.0) < 1e-9, True)

        # ⑥ exit コードが 2（until 無し）→ 3（またぎ）→ 4（禁止の秒）→ 5（黒帯）の順
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
            globals()["USE"] = {"x01": dict(clip="t_clip", start=12.0, until=20.0,
                                            zoom=0.75)}
            rc5 = fetch(check=True)                       # 帯が 240px 残る
            globals()["USE"] = {"x01": dict(clip="t_clip", start=12.0, until=20.0)}
            rc0 = fetch(check=True)
            # 🔴 exit 6 ＝ ショット表に無いクリップ（表のパスが前の題材を向いたままの型）
            globals()["USE"] = {"x01": dict(clip="mukashi_no_dai", start=1.0, until=5.0)}
            globals()["CLIPS"] = dict(CLIPS, mukashi_no_dai=dict(
                url="http://example.invalid/x.mp4", sec=100.0, w=1920, h=1080,
                credit="（検算用）", note="（検算用）", stream=True))
            rc6 = fetch(check=True)
        finally:
            S.CUTS = keep_cuts
        for name, rc, want in (("until 無し", rc2, 2), ("ショットまたぎ", rc3, 3),
                               ("禁止の秒", rc4, 4), ("素材の黒帯", rc5, 5),
                               ("正しい欄", rc0, 0),
                               ("ショット表に無いクリップ", rc6, 6)):
            ok.append(rc == want)
            print(f"  {'✓' if rc == want else '🔴'} {name} → `fetch --check` exit {rc}（期待 {want}）")
    finally:
        globals()["SHOTS"] = keep_shots
        globals()["USE"] = keep_use
        globals()["CLIPS"] = keep_clips
        globals()["NOGO"] = keep_nogo
        globals()["PILLAR"] = keep_pillar

    # ⚠️ 本番の状態は「検算の合否」と分けて必ず表に出す（道具の緑と中身の緑を混ぜない）
    # 🔴 定数の検算＝**切り出したコマを実際に測って** PILLAR と突き合わせる
    for clip, pl in sorted(PILLAR.items()):
        cids = [c for c, u in USE.items() if u.get("clip") == clip]
        got = [measure_pillar(c) for c in cids]
        got = [g for g in got if g is not None]
        if not got:
            print(f"  ⚠️ {clip}: 切り出したコマが無いので PILLAR を検算できない"
                  f"（書いてある値 {pl:.4f}）")
            continue
        ok.append(all(abs(g - pl) < 0.01 for g in got))
        print(f"  {'✓' if ok[-1] else '🔴'} {clip}: PILLAR {pl:.4f} と"
              f"切り出した {len(got)} 本の実測（{min(got):.4f}〜{max(got):.4f}）が合う")
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
    over, miss, out, nog, bars = check_until()
    # 🔴 exit 6 ＝ USE が使っているクリップのショット表が無い（2026-09-08・6本目②で追加）。
    #    ⚠️ これは「粗が無い」ではなく「**見ていない**」。表のパスが前の題材を向いたままだと
    #       exit 3 の門番が全欄を「対象外」で飛ばして黙って通る
    #       → [[feedback-gates-blind-to-the-new-material]]
    if unknown_clip():
        print(f"🔴 exit 6 ＝ ショット表に無いクリップを使っている: {unknown_clip()}。"
              f"`{SHOT_FILE}` を題材のものに差し替える")
        return 6
    # 🔴 `until=` は必須（2026-09-07・設計ノート §9-5）。無ければ **exit 2** で落とす。
    #    ⚠️ はみ出し（exit 1）より重い。「測れる状態になっていない」ので切り出しにも進まない
    if miss:
        print("🔴 exit 2 ＝ `until=`（そのショットが終わる秒）を USE に書いてから通す。"
              "秒は `ref/keybridge/SHOTS_INDEX.md`（1秒刻みの実測）から写す")
        return 2
    # 🔴 exit 3 ＝ 数は入っているが、実測のショットをまたいでいる（2026-09-07・5本目で追加）。
    #    ⚠️ until= を必須にしただけでは「数が入っていればよい」で終わり、4本目で3件踏んだ
    #       「注記の範囲の中で絵が別物」がそのまま通る。ここが**その穴**を塞ぐ門番
    if out:
        print("🔴 exit 3 ＝ (start, until) を1本のショットの中に収める。"
              "`python tools/shots.py show ref/keybridge/shots.json --key <clip>` で境目を見る")
        return 3
    # 🔴 exit 4 ＝ 実際に読む秒が「使ってはいけない秒」に掛かる（2026-09-07・5本目 ⑤c'）。
    #    ⚠️ exit 2/3 は**書いた数**を見る門番で、ここだけが**実際に読む範囲**を見る。
    #       pr01 は until=1491.0（ショットの終わり）と正しく書いてあったのに、
    #       尺 10.72秒 × rate 1.0 ＝ 1488.7秒まで読み、終幕タイトルを画面に出していた。
    if nog:
        print("🔴 exit 4 ＝ `footage.NOGO` の秒に掛かっている。"
              "rate を下げて読む秒を縮めるか、別のショットへ振り替える")
        return 4
    # 🔴 exit 5 ＝ 素材の黒帯が画面に残る（2026-09-07・5本目 K-12）
    if bars:
        print("🔴 exit 5 ＝ 素材の左右の黒帯が画面に残る。"
              "`footage.PILLAR` の割合ぶんは `zoom_of()` が自動で寄せるので、"
              "欄の zoom を 1.0 未満にしないこと")
        return 5
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
