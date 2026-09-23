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
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.parse
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
# 🔴 2026-09-13（7本目②）：**ここを題材ごとに差し替える。**前は ref/keybridge/clips.json。
#    差し替え忘れは「前の回の28本を調べて合格」という**黙った嘘**になる
#    → [[feedback-gates-blind-to-the-new-material]]。
#    7本目＝NARA RG237（FAA）naId 7419198 の32点。`ref/ep7/clips.json` は
#    `analytics/materials/ep7/s2/make_clips.py` が ffprobe の実測から書き出す（手で書かない）。
#    🔴 2026-09-20（10本目 ⑤b-1）：**10本目も動く映像0本**（素材は写真92点だけ）。
#       `ref/ep10/clips.json` は作らない＝`CLIPS` は空。9本目は `ref/ep9/`、8本目は `ref/ep8/`。
#       🔴🔴 2026-09-21（11本目 ⑤c-2）：**11本目は動く映像が3本ある**
#          （NASA 記録映画 44分44秒・NARA 氷 `naId 39672` 8分04秒・USIA 公聴会）。
#          抜いた帯は `ref/ep11/vid/clips/`（git 管理外）、正本は `ref/ep11/footage_map.md` §1。
#       🔴 2026-09-23（12本目 ⑤b-2）：**12本目へ切り替えた。**動く映像は2本
#          （DOE の記録映像 0〜56秒・艦から撮った火球の4K 56.9秒）。
#          `ref/ep12/clips.json` は⑤b-2 で作る＝**無いあいだ CLIPS は空**（`unknown_clip()` が止める）。
_CLIPS_JSON = HERE / "ref" / "ep12" / "clips.json"
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
SHOT_FILE = HERE / "ref" / "ep12" / "shots.json"          # 12本目（動く映像2本）。11本目は ref/ep11/（3本）
# 🔴 2026-09-13（7本目②）：**この表はまだ無い。**⑤で `tools/shots.py` が作る。
#    無いあいだ SHOTS は空で、`outside_shot()` は全欄を「対象外」で飛ばす＝**素通りする**。
#    それを塞ぐのが下の `unknown_clip()`（`fetch --check` が呼ぶ）。USE を書いたら必ず通す。
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
    # ══════════════════════════════════════════════════════════
    # 🔴🔴 2026-09-16（9本目 テネリフェ ⑤b-1）**空にした。9本目は動く映像0本。**
    #   8本目（`guncam` `sts1` `tank`）と7本目（`?-AWA-716-*` ほか14本）の欄は
    #   git の `4c71bf0` にある（`git show 4c71bf0:tools/footage.py`）。
    #   ⚠️ 消した記録のうち、次の回にも効く教訓だけをここに残す：
    #     ・**「同じ型だから同じ秒を弾く」は誤り**（7本目 `5-AWA-213-ny_best.mp4` には
    #       頭の表題カードが無かった）。1本ずつ測る
    #     ・**0件は「危険が無い」ではなく「まだ見ていない」**（7本目 c716 が
    #       End of Recording を10秒映したまま `--check` を緑で通った）
    #     ・**時代の食い違い**（8本目 `tank` の残り3分は2011年の解説者）は門番が鳴らない
    #       → [[feedback-fallback-stills-must-match-the-era]]
    # ══════════════════════════════════════════════════════════
    #
    # 🔴 2026-09-08（6本目②）: **空にした。「危険が無い」ではなく「まだ見ていない」。**
    #    5本目は⑤c' で1カット目に『THE END』が写っていたのを見つけて足した欄。
    #    キー橋の28本は DVIDS の B-roll なので終幕タイトルは想定しにくいが、
    #    ⚠️ **局のロゴ・提供クレジット・DVIDS のスレート**が頭尻に入る型は在りうる。
    #    → ⑤でショットを見たときに、見つけたぶんをここへ書く。
    #
    # 🔴 2026-09-23（12本目 ⑤b-2）：DOE の終わりに英字の題字（②の `scan_burned_text.py` で 57.0 から浮く・
    #    ⑤b-2 の1秒刻みのシートで 57.5 と 58.5 に `CASTLE BRAVO / FEBRUARY 28, 1954 …` を確認）。
    #    ⚠️ 題字は**2月28日**（米本国の日付）＝現地3月1日と語る画面に出すと台本と食い違う。
    "doe": [(56.5, 60.0, "英字の題字（CASTLE BRAVO / FEBRUARY 28, 1954）")],
}


def in_nogo(use=None, secs=None):
    """🔴 実際に読む秒が「使ってはいけない秒」に掛かっている欄。

    ⚠️ `until` だけを見ても止まらない。`until` は**ショットの終わり**として書かれるので、
       ショットの途中から禁止の秒が始まる場合に構造上見えない（pr01 がその実例）。
    """
    if secs is None:
        import scene_jiko as S
        # 🔴 12本目から：映像が使うのは**扉を除いた中身の秒**（扉の2秒は映像を映さない）
        secs = {c: s - S.card_of(c) for c, s in S.CUTS}
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
    # ══════════════════════════════════════════════════════════
    # 🔴 2026-09-13（7本目②）：**空にした。**6本目キー橋の35欄は git `eb322ca` にある。
    #    欄は **④の台本が承認されてから**書く（6本目②と同じ手順）。
    #
    # 🔴🔴 7本目の素材で、切り出しの前に必ず効かせること（②で実測した）
    #   ① **画素が正方形でない。** RG237 の32点のうち **27点が SAR=10:11**（DAR 15:11）。
    #      そのまま切り出すと **横に10%ふくらむ**（レーダーの円が卵になる）。
    #      ⚠️ `_cut_stream()` の `scale={want}:-2` は **SAR を見ない**。
    #         しかも 720 < 1920 なので `want == c["w"]` になり **scale 自体が付かない**。
    #         → ⑤で `-vf` に `scale=iw*sar:ih`（720x480 → **655x480**）を足す。
    #         台帳 `ref/ep7/clips.json` の **`dispw`** がその幅。
    #   ② **`-an` を必ず付ける。** 32点中 **28点に音声トラックがある**。
    #      この回は①で「音は鳴らさない」と決めている。
    #   ③ **`yadif` は付けない。** 器の札は `field_order=tt` だが、3つの実測が
    #      「60p（1コマずつ本物）」と言っている＝
    #        ・nb_frames ÷ 秒 = 60.00（コマが実在する）
    #        ・`ffmpeg -vf idet` 200コマで TFF 0／BFF 0
    #        ・yadif あり/なしで櫛の指標が 0.5% しか動かない
    #      ⚠️ 札を信じて yadif を入れると **480本の縦解像度を無駄に半分**にする。
    #   ④ **額装パネル**（1920に届く点が0なので全画面にできない）。
    #      655x480 を `scene_jiko.PANEL_MAXW/H`（1120x648）に入れると **z=1.35（883x648）**。
    #      ⑤で原寸目視して、甘ければ `pw=655`（等倍）に落とす。
    # ══════════════════════════════════════════════════════════
    # ══════════════════════════════════════════════════════════
    # 🔴🔴 2026-09-14（8本目 コロンビア号 ⑤b-1）**7本目の17欄を全部捨てた。**
    #    中身は git の `ae30d49`（`git show ae30d49:tools/footage.py`）。
    #
    # ⚠️⚠️ **これは `tools/cuts/` と同じ罠だった。**7本目の18欄のうち **17欄**が
    #    8本目のカットIDとぶつかっていた（pr03 c222 c315 c316 c416 c417 c511 c512
    #    c513 c514 c611 c612 c617 c620 c621 c716 c810）。
    #    しかも `cuts/README.md` §0-8 のとおり **動画は写真より優先される**ので、
    #    残したまま焼くと「⑤b で当てた写真が1枚も出ないまま 9.11 の管制画面が流れる」。
    #    **エラーも出ず、机上検査も全部通る。**
    #    → [[project-jiko-rules-index]] §0b は `cuts/*.py` だけを名指ししていたが、
    #      **`footage.USE` も同じ手当てが要る**。
    # ══════════════════════════════════════════════════════════
    #
    # 🔴🔴 2026-09-16（9本目 テネリフェ ⑤b-1）**8本目の16欄を全部捨てた。**
    #    中身は git の `4c71bf0`（`git show 4c71bf0:tools/footage.py`）。
    #    ⚠️ 16欄とも9本目のカットIDと衝突していた（c101 c102 c418 c622 c701 c705 c711 c713
    #       c715 c717 c720 c724 c725 c727 ep01 ep02）。**写真より動画が優先**なので、
    #       残したまま焼くと9本目の写真が1枚も出ないままコロンビア号の映像が流れた。
    #    🔴 **9本目は動く映像0本**（`ref/ep9/materials.md` §3・Commons を8通りの語で実測）。
    #       ＝ この回は `USE` を**空のまま**使う。欄を足すなら②の実測をやり直してから。
    #
    # ⚠️ 次に映像のある回で秒を書くときに守ること（8本目 ⑤b-2 の教訓・守らないと止まる）
    #   1. `start` / `until` は `ref/<回>/shots.json`（1秒刻み）の**境目をそのまま写す**
    #   2. **`until=` は全欄に必ず書く**（`still=True` の欄も。無いと exit 2）
    #   3. (start, until) は**1本のショットに収める**（またぐと exit 3）。`until` は
    #      **ショットの終わり −1.0秒**（境目は後ろ側の秒に置かれるので尻に次の絵が混じる）
    #   4. `rate` は「そのショットの残り ÷ カットの尺」を切り捨てた値。機械で出す
    #   5. **ショットの中で絵が変わる**ことがある（8本目 `sts1` #01 は1ショットに3つの絵）。
    #      640px のシートで見てから書く（→ [[feedback-measure-the-source-before-choosing-the-crop]]）
    # KB_USE>>> ここまで
    #
    # ══════════════════════════════════════════════════════════
    # 🔴🔴 2026-09-23（12本目 キャッスル・ブラボー ⑤b-2）**11本目の8欄を空にした。**
    #   中身は git の `61039d2`（`git show 61039d2:tools/footage.py`）。
    #   ⚠️ 11本目の欄のうち pr02・pr07・c101・c307・c413・c503・c603 は**12本目にも同じIDがある**
    #      （c101・c307・c413・c503・c603）＝残すとチャレンジャー号の映像が黙って流れる。
    #   次の回にも効く教訓だけ残す：
    #     ・`rate` は「使える秒 ÷ **音の尺**」。**切り上げると尻が出る**（11本目 pr02 +0.59秒）
    #     ・`rate` が 0.6 を下回る欄は動画にせず、止め絵で `ss.still()` に置く（実写の数は同じ）
    #     ・ショットの中でも絵が変わる（11本目 c603＝元1034）＝`until` は切れ目の1.0秒手前
    #     ・額（ピラーボックス）はコマごとに変わる → [[feedback-container-labels-lie-about-the-picture]]
    # ══════════════════════════════════════════════════════════
    #
    # 🔴 2026-09-23（12本目 ⑤b-2）：**11欄**（DOE 5・4K 6）。残る DOE の3欄（c214・c420・c920）は
    #    `rate` が 0.4 を下回るので**止め絵**（`cuts/ss.py` の `still()`・実写の数は変わらない）。
    #    帯＝`ref/ep12/clips.json`／ショット＝`ref/ep12/shots.json`（1秒刻み）。
    #    中身の正本＝1秒刻みのシート（⑤b-2 で全コマを見た）＋明るさの0.1秒刻みの実測：
    #      DOE  0〜4.85 射点の小屋（色）／4.85 火球へ切り替わり 5.2〜5.9 明るくなり 6.0〜7.9 真っ白
    #           ／〜14 火球／16.6 に1コマの光→18.0〜19.0 真っ白→19〜24.5 ヤシの影
    #           ／**24.6 で黒へ切り替わる**（shots.json は 26 と出す＝1秒の粒度のずれ）→27.0〜29.9 真っ白
    #           ／30〜34 火球／35〜39 ヤシ・海・爆風に揺れるヤシ／40.5 暗転／41〜56 きのこ雲
    #           ／**57〜 英字の題字**（`NOGO`）
    #      4K   0〜1 暗い／1〜8 暗めの火球／8〜56 水平線の火球と雲がゆっくり育つ1ショット
    #           ／🔴 全コマの左下に透かし（y 0.78〜0.82）＝`zoom=1.33, bias=0` で画面の外へ
    #    ⚠️ **c101 は 4.85 の切り替わりを意図してまたぐ**（射点の小屋→閃光）。ショット表は
    #       4.0 を境にしているので門番は鳴らない＝**わざと**であることをここに書いておく。
    #    🔴 `rate` は `footage.py --check` の出す尺（余韻込み）で割って切り捨てた値（音の尺で割ると尻が
    #       0.3〜0.7秒はみ出した＝11本目と同じ罠）。0.40 以上なので動画のまま（§5b-17b）
    "c101": dict(clip="doe", start=4.0, until=13.0, rate=0.63),
    "c501": dict(clip="doe", start=14.0, until=24.4, rate=0.68),     # 24.6 の切り替わりの手前で止める
    "c607": dict(clip="doe", start=26.0, until=34.0, rate=0.81),     # 真っ白→火球＝乗組員が見た「光」
    "c506": dict(clip="doe", start=41.0, until=47.0, rate=0.68),     # 立ちのぼる柱＝吸い上げられるサンゴ
    "c608": dict(clip="doe", start=47.0, until=53.0, rate=0.46),     # 輪の雲が広がる
    "c324": dict(clip="bravo4k", start=1.0, until=7.0, rate=0.57, zoom=1.33, bias=0.0),
    "c502": dict(clip="bravo4k", start=8.0, until=16.0, rate=0.76, zoom=1.33, bias=0.0),
    "c606": dict(clip="bravo4k", start=16.0, until=25.0, rate=0.75, zoom=1.33, bias=0.0),
    "c110": dict(clip="bravo4k", start=25.0, until=37.0, rate=0.62, zoom=1.6, bias=0.0),
    "c102": dict(clip="bravo4k", start=37.0, until=48.0, rate=0.70, zoom=1.33, bias=0.0),
    "c522": dict(clip="bravo4k", start=48.0, until=56.0, rate=0.92, zoom=1.33, bias=0.0),
}
# 🔴 **まだ決まっていない2欄（代用で埋めていない）** → [[feedback-agents-substitute-missing-parts]]
#   c621「ARTCC 画面（点が消えた直後）」
#     … 使える ZOB-ARTCC は2本とも c612／c617／c620 で使っており、**同じ絵**になる。
#        残る8本（974〜1,514秒）はまだショットを測っていない。⑤b-2 で1本測って当てる。
#   c712「航跡レーダー（戦闘機の航跡）」
#     … 🔴 **戦闘機の航跡が写っているクリップが無い。** `5-AWA-716-C130-observer` は
#        AA77 を見分けた **C-130 輸送機**の航跡で、戦闘機ではない
#        （→ [[feedback-subtitle-must-match-what-is-visible]]／台本 c419 の主題そのもの）。
#        ⑤b-2 の選択肢＝(a) c712 を図に振り替える（第7章は図の章）
#                      (b) C-130 のクリップを **c419** へ回し、c712 は図にする
#        ⚠️ どちらでも**写真の総数98は動かさない**（章ごと45〜50%の網に鳴る）。
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
        # 🔴 12本目から：扉の秒は映像の until に数えない（中身の秒だけ）
        secs = {c: s - S.card_of(c) for c, s in S.CUTS}
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
        keep_probe = probe_media
        try:
            S.CUTS = [("x01", 6.0)]
            # ⚠️ 検算のあいだは**外に出ない**。既定のままだと exit 2〜6 の対照が
            #    example.invalid を引きに行き、7 に化けて「順番」が測れなくなる。
            globals()["probe_media"] = lambda _u, timeout=45: (None, 2_000_000)
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
            # 🔴🔴 exit 7 ＝ 媒体 URL が動画として引けない（2026-09-22・11本目 ⑤c-4）。
            #    ⚠️ `probe_media` は**外に出る唯一の口**なので差し替える
            #       （[[feedback-selftest-must-not-reach-real-side-effects]]）。
            #       差し替えないと、上の「正しい欄 → exit 0」が
            #       example.invalid を引きに行って落ちる＝物差しが本番を測れない。
            globals()["USE"] = {"x01": dict(clip="t_clip", start=12.0, until=20.0)}
            keep_clips_fx = dict(CLIPS)                        # 仕込みずみの CLIPS を控える
            rc7_ok = fetch(check=True)                        # 媒体は合格を返す
            globals()["probe_media"] = lambda _u, timeout=45: ("（検算：引けない）", 0)
            rc7 = fetch(check=True)                           # 引けない → 7
            globals()["probe_media"] = lambda _u, timeout=45: (None, 2_000_000)
            # 引用の頁（/details/）を渡したら media_of が止める。
            # ⚠️ 媒体は「引ける」ままにしてある＝**止めているのは URL の形**だと示すため
            fx = dict(CLIPS)
            fx["t_clip"] = dict(fx["t_clip"], media=None,
                                url="https://archive.org/details/xxxx")
            globals()["CLIPS"] = fx
            rc7d = fetch(check=True)
            # 🔴🔴 exit 8 ＝ 画素が正方形でないのに `dispw` が無い（横に太る型）
            fx8 = dict(CLIPS)
            fx8["t_clip"] = dict(keep_clips_fx["t_clip"], sar="8:9", w=720, h=480)
            fx8["t_clip"].pop("dispw", None)
            globals()["CLIPS"] = fx8
            rc8 = fetch(check=True)
            # 陰性対照＝`dispw` を足せば黙る（同じ SAR のまま）
            fx8b = dict(fx8)
            fx8b["t_clip"] = dict(fx8["t_clip"], dispw=640)
            globals()["CLIPS"] = fx8b
            rc8b = fetch(check=True)
            globals()["CLIPS"] = keep_clips_fx
        finally:
            S.CUTS = keep_cuts
            globals()["probe_media"] = keep_probe
        for name, rc, want in (("until 無し", rc2, 2), ("ショットまたぎ", rc3, 3),
                               ("禁止の秒", rc4, 4), ("素材の黒帯", rc5, 5),
                               ("正しい欄", rc0, 0),
                               ("ショット表に無いクリップ", rc6, 6),
                               ("媒体が引ける欄", rc7_ok, 0),
                               ("媒体が引けない", rc7, 7),
                               ("url が /details/ の頁", rc7d, 7),
                               ("SAR 8:9 なのに dispw が無い", rc8, 8),
                               ("陰性対照：dispw を足せば黙る", rc8b, 0)):
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
    # 🔴🔴 2026-09-13（7本目⑤b）**SAR の直しが本当に `-vf` に載っているか**を値で見る。
    #   ⚠️ 「件数」の対照では動かない（もともと全欄が該当しうる）＝**文字列の値**で見る
    #      → [[feedback-verify-your-own-instrument]]
    #   ⚠️ `_cut_stream` は ffmpeg と網に出るので、`subprocess.run` と `time.sleep` を
    #      差し替えて**コマンドだけ**を受け取る
    #      → [[feedback-selftest-must-not-reach-real-side-effects]]
    def _dl_fail(_u, _d):
        raise IOError("（検算：網には出ない）")

    def _vf_of(w, h, dispw, dl=_dl_fail):
        seen = {}

        class _R:
            returncode, stdout, stderr = 1, "", "（検算：ffmpeg は呼んでいない）"

        def fake_run(cmd, **kw):
            seen.setdefault("cmd", cmd)
            return _R()

        # ⚠️ `download_media` も外に出る口（12本目 ⑤c で足した）。差し替えないと網に出る
        keep_run, keep_sleep, keep_dl = subprocess.run, time.sleep, download_media
        keep_c = dict(CLIPS)
        try:
            subprocess.run = fake_run                      # type: ignore[assignment]
            time.sleep = lambda *_a, **_k: None            # type: ignore[assignment]
            globals()["download_media"] = dl
            _MEDIA.clear()
            CLIPS["_st_sar"] = dict(url="http://example.invalid/s.mp4", sec=99.0,
                                    w=w, h=h, dispw=dispw, credit="（検算用）",
                                    note="（検算用）", stream=True)
            _cut_stream("_st_sar_cut", dict(clip="_st_sar", start=1.0), 1.0)
        finally:
            subprocess.run = keep_run                      # type: ignore[assignment]
            time.sleep = keep_sleep                        # type: ignore[assignment]
            globals()["download_media"] = keep_dl
            _MEDIA.clear()
            CLIPS.clear(); CLIPS.update(keep_c)
        cmd = seen.get("cmd") or []
        return cmd[cmd.index("-vf") + 1] if "-vf" in cmd else "", cmd

    def _src_of(cmd):
        return cmd[cmd.index("-i") + 1] if "-i" in cmd else ""

    # 🔴 2026-09-23（12本目 ⑤c r01）：Ogg を網越しに -ss で開くと 429 で0コマ（local_media の注）
    _v, cmd_dl = _vf_of(1280, 720, 1280, dl=lambda _u, _d: 39_539_411)
    chk("陽性対照：http の媒体は丸ごと落とし、手元のファイルを ffmpeg に渡す",
        (not _src_of(cmd_dl).startswith("http")) and _src_of(cmd_dl).endswith(".mp4"), True)
    chk("陽性対照：手元のファイルには -user_agent を付けない（http の口の設定）",
        "-user_agent" in cmd_dl, False)

    vf_sq, cmd_sq = _vf_of(720, 480, 655)          # 画素が正方形でない（RG237 の27点）
    vf_11, _cmd11 = _vf_of(1280, 1024, 1280)       # 画素が正方形（残りの5点）
    chk("陽性対照：SAR 10:11 の素材に scale=iw*sar:ih が載る",
        "scale=iw*sar:ih" in vf_sq, True)
    chk("陽性対照：そのとき setsar=1 も載る", "setsar=1" in vf_sq, True)
    chk("陰性対照：SAR 1:1 の素材には載らない",
        "iw*sar" in vf_11 or "setsar" in vf_11, False)
    chk("陰性対照：yadif は付けない（札は tt だが中身は 60p）", "yadif" in vf_sq, False)
    chk("陽性対照：音声を落とす -an が付く", "-an" in cmd_sq, True)
    chk("陰性対照：媒体を落とせなければ今までどおり URL を渡す（名乗りも付ける）",
        _src_of(cmd_sq).startswith("http") and "-user_agent" in cmd_sq, True)
    print(f"     -vf（SAR 10:11）＝ {vf_sq}")
    print(f"     -vf（SAR 1:1 ）＝ {vf_11}")
    import shutil as _sh
    _sh.rmtree(FOOT / "_st_sar_cut", ignore_errors=True)

    now = missing_until(USE)
    n_sh = sum(len(v) for v in SHOTS.values())
    print(f"  ⚠️ いまの本番：USE {len(USE)}欄（until 無し {len(now)}）／"
          f"実測ショット {n_sh}本／クリップ {len(CLIPS)}本")
    good = all(ok)
    print("  " + (f"✓ 陽性対照 {len(ok)}/{len(ok)}" if good
                  else f"🔴 陽性対照 {sum(ok)}/{len(ok)} で落ちた"))
    return good


# 🔴🔴 archive.org の「引用の頁」。ffmpeg に渡すと HTML が返り
#    「Invalid data found when processing input」で落ちる。
_DETAILS = re.compile(r"archive\.org/details/", re.I)


def media_of(name):
    """ffmpeg に渡してよい**媒体そのもの**の URL と、足す秒を返す。

    🔴🔴 2026-09-22（11本目 ⑤c-4）で見つけた穴。
       `ref/ep11/clips.json` の `url` は **人が見る引用の頁**（`/details/`）で、
       ffmpeg は読めない。⑤c は帯を `ref/ep11/grab_clips.py` で**手元に抜いてから**
       進めたので気づけず、Actions の焼きで **7欄すべてが黙って静止画に落ちた**
       （ログは `✓ 切り出し完了 0/7`。`continue-on-error: true` なので**段は緑**）。
       ⚠️ `modal_app.py` も `python3 tools/footage.py` を呼ぶので、
          直さなければ**本編mp4にも静止画のまま載っていた**。
       → [[feedback-fetch-failure-falls-back-to-a-still]]／[[feedback-pipes-mask-exit-codes]]

    ⚠️ **秒の基準が2通りある。**
       `media` は「もとの1本」なので、帯の中の秒に `at`（帯の頭がもとの何秒か）を足す。
       `url` を直に使う回（7本目 DVIDS など）は1本＝1クリップなので足さない。
    ⚠️ **鍵の名前を `stream` にしてはいけない。**ep7・ep8・keybridge の clips.json では
       `stream` は「URL から流して読む」という**真偽値**（`True`）で、
       URL を入れると `True` を URL として ffmpeg に渡すことになる。
    """
    c = CLIPS[name]
    if c.get("media"):
        return c["media"], float(c.get("at") or 0.0)
    u = c.get("url")
    if not u:
        raise RuntimeError(f"{name} に url がない（4本目の Kaltura 経由は git の 4e4c1fb にある）")
    if _DETAILS.search(u):
        raise RuntimeError(
            f"{name} の url は archive.org の引用頁（/details/）で、ffmpeg は読めない。"
            f"clips.json に `media`（/download/… の直リンク）を書くこと")
    return u, 0.0


def urls_of(name):
    return [media_of(name)[0]]


def probe_media(url, timeout=45):
    """その URL が本当に**動画（媒体）として**引けるかを HEAD で見る。

    返すのは `(why, length)`。`why` が None なら合格。
    ⚠️ **外に出る唯一の口**なので、`--selftest` はここを差し替える
       （[[feedback-selftest-must-not-reach-real-side-effects]]）。
    """
    why, ln = None, 0
    for attempt in range(2):
        try:
            rq = urllib.request.Request(url, method="HEAD",
                                        headers={"User-Agent": UA})
            with urllib.request.urlopen(rq, timeout=timeout) as r:
                ct = (r.headers.get("Content-Type") or "").split(";")[0].lower().strip()
                ln = int(r.headers.get("Content-Length") or 0)
                ar = (r.headers.get("Accept-Ranges") or "").lower()
            # 🔴 2026-09-23（12本目 ⑤b-2）：Commons の `.ogv`（Ogg Theora）は `application/ogg` で返る
            #    （RFC 5334 の Ogg の容れ物の型）。頁（text/html）ではないので通す。大きさと区間読みは下で見る
            if not ct.startswith(("video/", "audio/", "application/octet-stream", "application/ogg")):
                why = f"Content-Type が `{ct or '空'}`＝動画でない（頁を渡している）"
            elif ln < 1_000_000:
                why = f"Content-Length {ln} が小さすぎる＝媒体でない"
            elif "bytes" not in ar:
                why = f"Accept-Ranges が `{ar or '空'}`＝区間だけ読めない"
            else:
                why = None
            return why, ln
        except Exception as e:                                # noqa: BLE001
            why = f"{type(e).__name__}: {e}"
            if attempt == 0:
                time.sleep(5)
    return why, ln


_MEDIA = {}                     # URL → ffmpeg に渡す入力（1回の実行で同じ媒体を二度落とさない）


def download_media(url, dst, timeout=60):
    """媒体を **1回の GET で丸ごと** `dst` へ落とし、大きさ（バイト）を返す。

    大きさが Content-Length と合わなければ止める（途中で切れた媒体を黙って使わない）。
    ⚠️ **外に出る口**なので、`--selftest` はここを差し替える
       （[[feedback-selftest-must-not-reach-real-side-effects]]）。
    """
    rq = urllib.request.Request(url, headers={"User-Agent": UA})
    part = dst.with_name(dst.name + ".part")
    with urllib.request.urlopen(rq, timeout=timeout) as r, open(part, "wb") as f:
        want = int(r.headers.get("Content-Length") or 0)
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    got = part.stat().st_size
    if want and got != want:
        part.unlink(missing_ok=True)
        raise IOError(f"落とした大きさ {got} が Content-Length {want} と合わない")
    part.replace(dst)
    return got


def local_media(url):
    """ffmpeg に渡す入力を返す。http(s) の媒体は**先に丸ごと落として手元のファイル**を渡す。

    🔴🔴 2026-09-23（12本目 ⑤c r01）**Ogg（.ogv）を網越しに `-ss` で開くと 429 で0コマになる。**
       Ogg には索引が無いので、ffmpeg は秒へ飛ぶのに**区間読みを何度も繰り返して二分探索**する。
       その連打が `upload.wikimedia.org` の回数制限（`HTTP error 429 Your bot is making too many
       requests`）に当たり `could not seek to position 26.000` ＝ **doe の5欄（c101 c501 c506 c607
       c608）が全部、黙って静止画に落ちた**（`✓ 切り出し完了 6/11`・段は緑）。
       WebM は索引（Cues）を持つので数回で飛べる＝ bravo4k の6欄は通っていた。
       ⚠️ `fetch --check` は HEAD を1回引くだけなので ✓ を出す＝**門番の経路と本番の経路が別**。
       ⚠️ 手元の回線でも同じく 429（Actions の回線に固有ではない）。`modal_app.py` も同じ関数を呼ぶ。
       → [[feedback-fetch-failure-falls-back-to-a-still]]
    ⚠️ 落とせなければ**今までどおり URL を渡す**（静止画に落ちるより先に網を試す）。
    """
    if not str(url).startswith(("http://", "https://")):
        return url
    if url in _MEDIA:
        return _MEDIA[url]
    d = FOOT / "_media"
    d.mkdir(parents=True, exist_ok=True)
    ext = Path(urllib.parse.urlparse(url).path).suffix or ".bin"
    dst = d / (hashlib.md5(url.encode("utf-8")).hexdigest()[:12] + ext)
    if dst.exists():                          # .part から名前を替えるのは大きさが合ったときだけ
        _MEDIA[url] = str(dst)
        return str(dst)
    for attempt in range(3):
        try:
            n = download_media(url, dst)
            print(f"     ✓ 媒体を手元に落とした（{n / 1e6:.1f}MB・{dst.name}）", flush=True)
            _MEDIA[url] = str(dst)
            return str(dst)
        except Exception as e:                                # noqa: BLE001
            print(f"     ⚠️ 媒体を落とせない：{type(e).__name__}: {e}（{attempt + 1}回目）", flush=True)
            time.sleep(10 * (attempt + 1))
    print("     ⚠️ 網から直に読む（Ogg は区間読みの連打で 429 になりやすい）", flush=True)
    _MEDIA[url] = url
    return url


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
    # 🔴🔴 2026-09-13（7本目⑤b）**画素が正方形でない素材を、先に正方形へ直す。**
    #   RG237 の32点のうち **27点が SAR=10:11／DAR=15:11**（②素材の実測）。
    #   ここは `scale={want}:-2` しか持っておらず、しかも 720 < 1920 なので
    #   `want == c["w"]` になって **scale そのものが付かない**＝素通りしていた。
    #   ＝ **レーダーの円が卵のまま焼ける。門番は1本も鳴らない**
    #      → [[feedback-container-labels-lie-about-the-picture]]
    #   台帳 `clips.json` の `dispw`（720→**655**）が正しい表示幅。
    #   ⚠️ ffmpeg は偶数に丸めるので実測の出力は **654×480**（1px 小さい）。
    #      `dispw` を「絵の幅」として使う側は 1px の差を粗と読まないこと。
    #   ⚠️ `setsar=1` まで書く。書かないと後段が SAR を持ち回って同じ歪みが戻る。
    #   ⚠️ **yadif は付けない。** 札は `field_order=tt` だが中身は 60p
    #      （コマ数 90,852÷1,514.3＝60.00・`ffmpeg -vf idet` は TFF 0／BFF 0）。
    #      札を信じると 480本しかない縦を無駄に半分にする。
    dispw = int(c.get("dispw") or c["w"])
    if dispw != int(c["w"]):
        vf += ["scale=iw*sar:ih", "setsar=1"]
    # 4K はそのまま切り出すと 1コマ 1.5MB。寄り（zoom）に要る幅だけ残して縮める
    want = min(dispw, int(round(1920 * float(u.get("zoom", 1.0)) * 1.02)))
    if want < dispw:
        vf.append(f"scale={want}:-2")
    d = FOOT / cid
    d.mkdir(parents=True, exist_ok=True)
    last = None
    # 🔴 `media` を使う回は帯の秒に `at` を足す（[[feedback-fetch-failure-falls-back-to-a-still]]）
    url, off = media_of(u["clip"])
    ss = off + float(u["start"])
    src = local_media(url)          # 🔴 http(s) は丸ごと落としてから切る（Ogg の 429＝local_media の注）
    for _ in (src,):
        for attempt in range(3):
            # ⚠️ `-an` … RG237 は **32本のうち28本に音声トラックがある**（②の実測）。
            #    この回は音を鳴らさない決定なので、指定しないと混ざる。
            # ⚠️ `-user_agent` は http の口の設定。手元のファイルに付けると止まる版がある
            net = ["-user_agent", UA] if str(src).startswith(("http://", "https://")) else []
            cmd = ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
                   *net, "-ss", f"{ss:.2f}", "-i", src,
                   "-an", "-t", f"{secs + 0.6:.2f}", "-vf", ",".join(vf),
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
    # 🔴 12本目から：切り出す長さも中身の秒（扉の2秒ぶん余計に切らない）
    secs = {c: s - S.card_of(c) for c, s in S.CUTS}
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
        # ⚠️ 2026-09-13（7本目⑤b）**この案内が前の題材のパスを名指ししていた**
        #    （`ref/keybridge/SHOTS_INDEX.md`）。門番の言うことを信じて別の題材の表を
        #    見に行くと、そこに在る秒を写してしまう → [[feedback-per-episode-constants-go-stale]]
        #    → `SHOT_FILE` から作る（題材を替えると自動で追いかける）。
        print("🔴 exit 2 ＝ `until=`（そのショットが終わる秒）を USE に書いてから通す。"
              f"秒は `{SHOT_FILE.relative_to(HERE).as_posix()}`（1秒刻みの実測）から写す。"
              f"無ければ `python tools/shots.py` で作る")
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
    # 🔴🔴 exit 7 ＝ 帯の媒体 URL が「動画として」引けない（2026-09-22・11本目 ⑤c-4 で新設）。
    #    ここまでの門番は**書いた秒**しか見ておらず、URL は1度も引かれていなかった。
    #    そのため `clips.json` の `url` が引用の頁（`/details/`）のままでも ✓ が出て、
    #    Actions の焼きで **7欄すべてが黙って静止画に落ちた**（`切り出し完了 0/7`）。
    #    ⚠️ **fail closed**（[[feedback-parsers-fail-closed]]）＝引けなければ 0 で埋めずに止める。
    #       この段は workflow で `continue-on-error` を付けていないので、ここで run が止まる。
    if check:
        bad_url = []
        for clip in sorted({u["clip"] for u in USE.values() if not u.get("still")}):
            try:
                mu, off = media_of(clip)
            except Exception as e:                            # noqa: BLE001
                bad_url.append((clip, f"{type(e).__name__}: {e}"))
                continue
            why, ln = probe_media(mu)
            if why:
                bad_url.append((clip, why))
            else:
                print(f"  ✓ {clip}: 媒体が引ける（{ln / 1e6:.0f}MB・もとの{off:.0f}秒〜）")
        if bad_url:
            for clip, why in bad_url:
                print(f"  🔴 {clip}: {why}")
            print("🔴 exit 7 ＝ 帯の媒体 URL が動画として引けない。"
                  "`clips.json` の `media`（/download/… の直リンク）を直すこと。"
                  "⚠️ ここを通さずに焼くと、その欄は**黙って静止画に落ちる**")
            return 7
        # 🔴🔴 exit 8 ＝ 画素が正方形でないのに、直す幅（`dispw`）が台帳に無い
        #    （2026-09-22・11本目 ⑤c-4 で新設）。`_cut_stream` が SAR の直しを当てる条件は
        #    `dispw != w` なので、**鍵が無いと素通りして横に太ったまま焼ける**。
        #    11本目は `make_clips.py` が `square_w` にしか書いておらず、実測で
        #    **720×480 の正方画素**（正しくは 640×480）が出た。**門番は1本も鳴らなかった。**
        #    → [[feedback-container-labels-lie-about-the-picture]]
        flat = []
        for clip in sorted({u["clip"] for u in USE.values() if not u.get("still")}):
            c = CLIPS[clip]
            sar = str(c.get("sar") or "1:1").replace("/", ":")
            try:
                sw, sh = (int(x) for x in sar.split(":"))
            except ValueError:
                flat.append((clip, f"sar が読めない（`{sar}`）")); continue
            if sw == sh:
                continue
            want = round(int(c["w"]) * sw / sh)
            if int(c.get("dispw") or c["w"]) == int(c["w"]):
                flat.append((clip, f"SAR {sar} なのに `dispw` が無い＝"
                                   f"横に {int(c['w']) / want * 100 - 100:.1f}% 太ったまま焼ける"
                                   f"（正しい幅 {want}）"))
        if flat:
            for clip, why in flat:
                print(f"  🔴 {clip}: {why}")
            print("🔴 exit 8 ＝ 画素が正方形でない帯に `dispw`（正方画素に直した幅）が無い。"
                  "台帳を作る道具（`ref/<題材>/make_clips.py`）で書き出すこと。"
                  "⚠️ `square_w` という名前では `_cut_stream` は読まない")
            return 8
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
