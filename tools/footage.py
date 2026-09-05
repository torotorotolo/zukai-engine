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

■ 🔴 4本目（サーフサイド）：**落とさずに、使う区間だけを URL から直接切り出す**
   NIST の記録映像は Kaltura 配信で、1本 600MB〜2GB（4K）。8本を全部落とすと 10GB を超えて
   Actions のランナーにも C: にも入らない。Kaltura の実ファイルは HTTP の範囲取得に対応しているので
   （②素材の実測。1コマ 3.5秒）、`ffmpeg -ss <秒> -i <URL>` で**その区間だけ**を読む。
   ⚠️ 署名付き URL は期限があるので、毎回 playManifest から取り直す（`kaltura_url`）。

■ 🔴 rate（スロー）
   B-Roll は1ショットが 3〜6 秒しかなく、カットの尺（6〜15秒）より短い。
   `rate=0.5` と書くと 0.5倍速（=2倍の長さ）で切り出す。ffmpeg の setpts でコマを複製するだけ
   （補間しない）。動きの少ないショットに使う。**顔のあるショットには使わない**。
   タイムラプス（6.8秒）は `rate=0.25` で3カットに割る（台本 §5 注意 7）。

■ 出典の書き方（★ここを間違えない）
   NIST（米国立標準技術研究所）の職務著作＝パブリックドメイン。B-Roll は "for the media" で配布。
   ⚠️ B-Roll #8 は**ミネソタ大学の試験場**で撮られている（撮影は NIST）。撮影者と場所を分けて書く。
   ⚠️ 1本目の ROV 映像（"courtesy of Pelagic Research Services"）のように**PDでない映像**を
      PD と書いてはいけない。今回の素材は全部 NIST 撮影なので当たらない。

■ 使い方
     python tools/footage.py fetch          … 使う区間だけ切り出す（落とさない）
     python tools/footage.py fetch --check  … 切り出さずに、割り当てだけ確認する

■ 🔴 秒数は**見てから決める**（r17 で1度失敗している）
   4本目は 1秒刻みの見取り図（scratchpad の sheet_*.jpg）を見て**ショットの境目**を書いた。
   下の USE の注記が、そのショットが何秒から何秒までかの実測。
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

# ── Kaltura（NIST の配信）──────────────────────────────────
# 🔴 1〜3本目（Internet Archive の USCG 資料・NARA の記録映画）の CLIPS/USE は
#    git の `ad6882a` にある。カットIDが題材をまたいでぶつかるので**残さない**。
KALTURA = ("https://cdnapisec.kaltura.com/p/684682/sp/68468200/playManifest"
           "/entryId/{e}/format/download/protocol/https/flavorParamId/0")
CR_NIST = "出典：NIST（米国立標準技術研究所）"

# name: (entry_id, 尺(秒), 幅, 高さ, 出典, 中身)
_SS = {
    "ss_b1": ("1_ju6nndhb", 250.1, 1920, 1014,
              f"{CR_NIST} 記録映像 B-Roll #1（崩落現場）／パブリックドメイン",
              "崩落現場。0:07まで題名カード／3:24以降はインタビュー。顔の寄りが多い"),
    "ss_b2": ("1_64zdekws", 309.7, 4096, 2160,
              f"{CR_NIST} 記録映像 B-Roll #2（空撮・現場）／パブリックドメイン",
              "0:08〜0:11 海岸線の空撮／0:12〜0:14 現場と 87 Park／1:39〜1:53 ドローン／1:54以降インタビュー"),
    "ss_b3": ("1_h4yeyz2f", 74.2, 1920, 1080,
              f"{CR_NIST} 記録映像 B-Roll #3（証拠倉庫）／パブリックドメイン",
              "倉庫で部材と鉄筋を測る"),
    "ss_b4": ("1_jvdq95ze", 216.3, 1920, 1080,
              f"{CR_NIST} 記録映像 B-Roll #4（部材の搬送）／パブリックドメイン",
              "部材の梱包・積み込み・トレーラーでの搬送"),
    "ss_b5": ("1_ecar0b6h", 333.4, 3840, 2160,
              f"{CR_NIST} 記録映像 B-Roll #5（コア抜き・倉庫）／パブリックドメイン",
              "倉庫の床一面の部材／コア抜き／コアの記録"),
    "ss_b6": ("1_zdyysoml", 263.2, 3840, 2160,
              f"{CR_NIST} 記録映像 B-Roll #6（コンクリートコアの試験）／パブリックドメイン",
              "圧縮試験・弾性係数試験"),
    "ss_b7": ("1_glesd05g", 337.0, 3840, 2160,
              f"{CR_NIST} 記録映像 B-Roll #7（鉄筋の試験）／パブリックドメイン",
              "鉄筋の標本・引張試験機"),
    "ss_b8": ("1_lebmphjw", 207.0, 3840, 2160,
              f"{CR_NIST} 記録映像 B-Roll #8（実物大試験・ミネソタ大学）／パブリックドメイン",
              "0:08まで表題カード。実物大レプリカ試験。2:08〜ワシントン大の試験"),
    "ss_tl": ("1_gvpcaamy", 6.8, 3840, 2160,
              f"{CR_NIST} 材料試験タイムラプス（スラブ・梁・柱の試験）／パブリックドメイン",
              "6.8秒。柱まわりのスラブが割れて外れる。⚠️ 右下に NIST の透かし（x0.63〜0.95・y0.84〜0.89）"),
}
CLIPS = {}
for _n, (_e, _sec, _w, _h, _cr, _note) in _SS.items():
    CLIPS[_n] = dict(entry=_e, sec=_sec, w=_w, h=_h, credit=_cr, note=_note, stream=True)
# NIST が公開したパンチング・シアの動く図（GIF・1920x1080・167コマ）
CLIPS["ss_gif"] = dict(
    url=("https://www.nist.gov/sites/default/files/styles/2800_x_2800_limit/public/"
         "images/2026/06/22/PunchingShear_001.gif?itok=e2hzBAS5"),
    sec=17.0, w=1920, h=1080, stream=True,
    credit=f"{CR_NIST} 押し抜きせん断の動画図（2026年6月22日公表）／パブリックドメイン",
    note="167コマ。力が柱の周りに集まり、ひびが回り込んで抜ける")


def kaltura_url(entry):
    """playManifest → 実ファイルの署名付き URL（期限あり。毎回取り直す）。"""
    req = urllib.request.Request(KALTURA.format(e=entry),
                                 headers={"User-Agent": UA, "Range": "bytes=0-0"})
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.geturl()
        except Exception as e:                           # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Kaltura の URL が取れない（{entry}）: {last}")


# ── どのカットに、どの動画の何秒目から当てるか ────────────────
# 🔴 守ること
#   1. **そのカットで話している対象そのもの**であること（壁紙にしない）
#   2. 顔の寄り・NIST ロゴ入りヘルメットの寄り・表題カードは使わない（台本 §5 注意 5・6）
#   3. ショットの長さがカットより短いときは `rate` で遅くする（上の説明）。
#      注記の「N〜M秒」が見取り図で確かめたショットの範囲。**次のショットに食い込ませない**
#   4. `zoom` `xbias` `bias` は切り方（`build_jiko.fit` と同じ意味）。4K は zoom 2 まで劣化しない
USE = {
    # ── プロローグ ─────────────────────────────────────
    # 8〜10秒 建物の銘板「CHAMPLAIN TOWERS 8777 SOUTH」／11〜14秒 崩れた棟の正面／15〜18秒 瓦礫と捜索
    "pr01": dict(clip="ss_b1", start=8.0, rate=0.5),
    # 54〜57.5秒 瓦礫の山と、その奥に残った棟（58秒から顔の寄り）
    # 🔴 still=True … 0.33〜0.38倍のスローはコマ落ちが目立つ（⑤b の決定・2026-09-05）。動画を当てず
    #    `ref/surfside/fb_<cid>.jpg` の静止画をゆっくり寄って使う。clip/start は出典と「どのショットか」の記録
    "pr02": dict(clip="ss_b1", start=53.8, still=True),
    # 15〜18.8秒 せん断された断面の下、瓦礫の上の捜索隊（19秒から別の引き）
    "pr03": dict(clip="ss_b1", start=15.0, rate=0.5),
    # ── 第1章 ────────────────────────────────────────
    # 8〜11.9秒 海岸線の空撮（12秒から現場の寄り）
    "c106": dict(clip="ss_b2", start=8.0, still=True),
    # 99〜107秒 ドローン。片づいたデッキの床面と重機
    "c119": dict(clip="ss_b2", start=99.0),
    # 115〜118.9秒 瓦礫の上の捜索隊と柱（119秒からクレーンの吊り）
    "c128": dict(clip="ss_b1", start=115.0, rate=0.6),
    # ── 第2章 ────────────────────────────────────────
    # 95.8〜98.8秒 デッキ面の引き（99秒からドローン）
    "c204": dict(clip="ss_b2", start=95.8, rate=0.4),
    # 74〜77.8秒 現場の床面。鉄筋の出た版とコーン（78秒から潰れた車）
    "c217": dict(clip="ss_b1", start=74.0, rate=0.5),
    # 🔴 2026-09-06（⑤c B-20）：78秒（潰れた車）は c217 の 74秒と同じショットで、6カットおいて使い回しに見えた。
    #    100〜104秒 瓦礫の山と重機の腕（99秒までと 105秒からは顔の寄り）の1コマを静止画で。0.33倍のスローもやめる
    "c223": dict(clip="ss_b1", start=102.5, still=True),
    # ── 第3章 ────────────────────────────────────────
    # 167コマ≒6.7秒しか無い（ss-r01 で 200/306 コマ＝末尾 3.5秒が止まった）。0.65倍で 10.1秒に伸ばす
    "c315": dict(clip="ss_gif", start=0.0, rate=0.65),
    # 10〜16.7秒 試験場の引き。試験機と背を向けた技術者（17秒から顔の寄り）
    "c321": dict(clip="ss_b8", start=10.0, rate=0.75),
    # 128〜133.9秒 レプリカと試験機の全景（134秒から計測器の寄り）
    "c322": dict(clip="ss_b8", start=128.0, rate=0.6),
    # 188〜197秒 スラブを真上から。格子と計測器
    "c324": dict(clip="ss_b8", start=188.0),
    # 47〜52.5秒 圧縮試験機に入ったコア（53秒から人）
    "c325": dict(clip="ss_b6", start=47.0, rate=0.7),
    # 24〜34秒 鉄筋の引張試験機（36秒からカード）
    "c326": dict(clip="ss_b7", start=24.0),
    # 80〜87秒 柱まわり。スラブの裏側のひびと露出した鉄筋
    "c327": dict(clip="ss_b8", start=80.0),
    # 64〜71秒 スラブの面を走るひびと計測カメラ
    "c328": dict(clip="ss_b8", start=64.0, rate=0.9),
    # 193.5〜202.5秒 真上から。上の面はまだ平ら（c324 と同じショットの後半・寄り違い）
    "c329": dict(clip="ss_b8", start=193.5, zoom=1.35, xbias=0.5, bias=0.55),
    # 121〜127秒 外れて落ちたスラブの裏側（128秒からカード）
    "c331": dict(clip="ss_b8", start=121.0),
    # ── タイムラプス 6.8秒を 0.25倍で3カットに割る。透かし（右下）を切り方で外す ──
    "c332": dict(clip="ss_tl", start=0.0, rate=0.25, zoom=1.25, xbias=0.5, bias=0.0),
    "c333": dict(clip="ss_tl", start=2.2, rate=0.25, zoom=2.0, xbias=0.45, bias=0.2),
    "c334": dict(clip="ss_tl", start=4.7, rate=0.25, zoom=1.5, xbias=0.4, bias=0.0),
    # ── 第4章 ────────────────────────────────────────
    # 40〜45秒 証拠倉庫で部材の鉄筋を測る（人は背中側）
    "c419": dict(clip="ss_b3", start=40.0, rate=0.6),
    # 102〜109秒 倉庫の引き。並んだ部材のあいだを歩く
    "c430": dict(clip="ss_b5", start=102.0),
    # 108〜118秒 部材を積んだトレーラーが走る（120秒からカード）
    "c431": dict(clip="ss_b4", start=108.0),
    # 8〜11.9秒 海岸線の空撮（c106 と同じショット・寄せを変える）
    "c434": dict(clip="ss_b2", start=8.0, still=True),
    # ── 第5章 ────────────────────────────────────────
    # 46〜49.8秒 デッキの床面を歩く作業員（50秒から試料袋の寄り）
    "c505": dict(clip="ss_b2", start=46.0, rate=0.45),
    # 42〜46秒 錆びた鉄筋の標本（袋と札）（48秒から人）
    "c513": dict(clip="ss_b7", start=42.0, rate=0.5),
    # 39〜48秒 コア抜きの刃と水
    "c519": dict(clip="ss_b5", start=39.0),
    # 116〜124秒 圧縮試験機の中のコア（計測器つき）
    "c520": dict(clip="ss_b6", start=116.0),
    # 11〜17秒 倉庫の床一面の部材（18秒からコア抜き機の寄り）
    "c521": dict(clip="ss_b5", start=11.0, rate=0.65),
    # ── 第6章 ────────────────────────────────────────
    # 32〜37.7秒 試験機の全景（38秒から顔）
    "c607": dict(clip="ss_b8", start=32.0, rate=0.65),
    # 158〜163.6秒 残った棟の断面。刃物で切ったように立つ床（164秒から人）
    "c628": dict(clip="ss_b1", start=158.0, rate=0.55),
    # ── 第7章 ────────────────────────────────────────
    # 198〜204秒 高い所からの現場の引き（海が見える）（204秒からカード）
    "c703": dict(clip="ss_b1", start=198.0),
    # 138〜141.9秒 残った棟＝住民が住んでいた建物の断面（142秒から顔）
    "c709": dict(clip="ss_b1", start=138.0, rate=0.42),
    # 153〜159秒 コアに計測器をあてる手元
    "c713": dict(clip="ss_b5", start=153.0, rate=0.65),
    # 110〜114.4秒 ドローン。現場の引き（114秒からカード）
    "c726": dict(clip="ss_b2", start=110.0, rate=0.5),
}
# ❌ 見たうえで**当てないと決めた**もの（2026-09-05・記録として残す）
#   c705（87 Park）… B-Roll #2 の 12〜14秒しか写っていない（3秒）。0.3倍速はコマ落ちが目立つので
#     **1コマを静止画で抜き**、ゆっくり寄る（`ref/surfside/ss_b2_87park.jpg`）。
#   pr10・ep16（銘板の寄り）… 8〜10秒の3秒しか無い。同じく静止画（`ss_b1_sign.jpg`）。
#   B-Roll #1 4:02 前後（NIST ロゴ入りヘルメットの寄り）／各巻の 1:41 2:10 2:25 などの顔の寄り
#   B-Roll #2 1:30 1:45 2:10（台本第3版の候補）… 1:30 は人物、2:10 はインタビュー。**使わない**
#     → c119 c505 c204 は上の秒に差し替えた（実見して決めた）


def urls_of(name):
    c = CLIPS[name]
    if c.get("url"):
        return [c["url"]]
    return [kaltura_url(c["entry"])]


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
    if check:
        return 0
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
    sys.exit(fetch(check="--check" in sys.argv))
