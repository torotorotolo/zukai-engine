# -*- coding: utf-8 -*-
"""本編mp4を **Modal** で焼く。GitHub Actions では焼かない。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 なぜ移したか（2026-07-31）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GitHub の Terms for Additional Products and Features（Actions の節）は、
GitHub-hosted runner を **「そのリポジトリのソフトウェアプロジェクトの
production / testing / deployment / publication と無関係な活動」** に
使うことを禁じている。「便益に不釣り合いな負荷」も禁止列挙にある。

  - レンダラを**試すために数フレーム焼く**のは白
  - **YouTubeに出す本編34分・61,320コマを毎本焼く**のは、
    成果物が動画でありソフトウェアではない以上、黒

2026年3月、Actions を CI 以外の汎用計算に使った個人が
**永久BAN＋データ取り出し不可**という報告がある。

⚠️ 同一アカウント群に **深読みフクロウ・スカッと・健康スレ集・漂着日記** が載っている。
   BANの影響は動画1本ではなく、**全チャンネルの制作基盤**。

→ **Actions に残すのは `mode=qa`（検品画像）と3つの機械検査だけ**。
  本編の製造はここ（Modal）で回す。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 最初の1回だけ必要な準備（カズヤくんの操作）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    pip install modal
    modal setup          … ブラウザが開くのでGitHubアカウントでログインする

Starter プランに **毎月 $30 の無料枠**がある（2026-08-01 時点の公式料金表）。
本編1本の実測見積りは **$0.15〜0.50**（下の「■ 費用」参照）ので、
月に何十本焼いても無料枠に収まる。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 使い方
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ① 本編を焼く（**先に git push すること**。ここは GitHub から clone する）
    modal run modal_app.py::full --note r10

    # ② 焼けた mp4 を手元に落とす
    modal volume get jiko-out titan_audio.mp4 out/jiko/

    # ③ Modal の描画が Actions と一致しているかを確かめる
    #    ⚠️ ふだんは要らない。`full` が焼いたレイヤーの指紋をログに出すので、
    #       そちらを Actions の「Layer fingerprint」と見比べれば足りる。
    #       こちらは本編を焼かずに指紋だけ取りたいときに使う。
    modal run modal_app.py::layer_hash

    # 特定のコミットで焼きたいとき
    modal run modal_app.py::full --ref 1062550

🔴 **ローカルのPCでは焼かない**（メモリ4GB）。ここも Actions も同じ理由でクラウド。
🔴 **ローカルの未コミットの変更は焼かれない。** GitHub から clone するので、
   直したら必ず push してから回す。Actions と同じソースになるのが狙い。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 費用（2026-08-01 に modal.com/pricing で確認した実額）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴🔴 **2026-08-02：この経路は止めた。「今後は全部無料で運用する」（カズヤくん判断）。**
　　 旧「$0.15 の超過は許可」を上書きする新しいルール。

🔴🔴 **ここに書いてあった「無料枠 $30/月（Starter）」は誤りだった。実地で否定された。**
　　 r29 を焼いている最中、レイヤー **650/1188** まで進んだところで
　　 **`workspace ... is disabled`** で止まり、mp4 は出来なかった。
　　 $30 あるなら 1本 $0.25 で止まるはずがない。
　　 → 実際の無料枠は **$1.00/月**（[[reference-modal-blender-render]] の記録が正しかった）。
　　 ⚠️ **残高はダッシュボードが唯一の正。ここの数字を信じて見積もらないこと。**

    CPU     $0.0000131 / コア / 秒     （1コア＝物理コア＝2 vCPU 相当）
    メモリ  $0.00000222 / GiB / 秒
    保管庫  $0.09 / GiB / 月（1 TiB/月まで無料）
    無料枠  **$1.00 / 月**（上を読むこと。$30 と書いてあったのは誤り）

  Actions での実測は 34分（4 vCPU）。内訳はレイヤー書き出し11分＋合成20分ほど。
  ここは 8コア（16 vCPU）で回すので **20〜30分** を見込む。

    CPU     8 × 1800秒 × $0.0000131 = $0.189
    メモリ  16 × 1800秒 × $0.00000222 = $0.064
    ─────────────────────────────
    **1本あたり およそ $0.25**（30分かかった場合）

  🔴 ここには「見積りの2倍かかっても $0.5。**無料枠 $30 の 1〜2% しか使わない**」と
     書いてあった。**この一文が今日の判断を狂わせた。**
     実際の無料枠は $1.00/月なので、**1本焼くだけで枠の 1/4 を使う**。
     4本目で尽きて、実際に r29 の途中でワークスペースが止まった。
     ⚠️ 「枠の何%か」を見積もるときは、**枠そのものの数字を実地で確かめてから**にする。
     ⏱ 時間は制約ではない（[[feedback-render-time-not-a-constraint]]）ので、
        速さのためにコア数を上げる必要はない。詰まるのは時間ではなく**費用**だった。
"""
import os
import subprocess
import sys
import time

import modal

REPO = "https://github.com/torotorotolo/zukai-engine.git"
WORK = "/work/zukai-engine"
VOL = "/vol"

# ── 実行環境 ──────────────────────────────────────────────
# 🔴 **ubuntu:24.04 ＋ google-chrome-stable** で揃える。
#    Actions の ubuntu-latest と同じ組み合わせ。図は Chrome の headless で
#    SVG から焼いているので、ブラウザが変わると**折返し位置が変わりうる**。
#    226カットの検品9巡は Actions の出力を見て行ったので、
#    そこと画が一致していないと検品のやり直しになる。
#    → 一致は `modal run modal_app.py::layer_hash` で機械確認できる。
image = (
    modal.Image.from_registry("ubuntu:24.04", add_python="3.12")
    .apt_install("git", "ffmpeg", "wget", "gnupg", "ca-certificates", "fontconfig")
    .run_commands(
        "wget -q -O /tmp/chrome.deb "
        "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb",
        "apt-get update && apt-get install -y /tmp/chrome.deb && rm /tmp/chrome.deb",
        "google-chrome --version",
    )
    # requirements.txt は Pillow / numpy / fonttools / brotli の4つだけ
    .pip_install("Pillow==11.3.0", "numpy==2.3.2", "fonttools==4.63.0", "brotli==1.2.0")
    .env({"PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"})
)

app = modal.App("zukai-jiko")
vol = modal.Volume.from_name("jiko-out", create_if_missing=True)

# 🔴 既製BGM（DOVA-SYNDROME「陰鬱な灰色の気配」）の置き場所。
#    **作者が音源の再配布を禁止**しており、このリポジトリは public なので
#    リポジトリには入れられない。保管庫に1回入れておき、焼くときだけ読む。
#
#      modal volume put jiko-assets "ダウンロードしたファイル.mp3" bgm.mp3
#      modal volume ls jiko-assets            … 入っているか確認
#
#    ⚠️ 保管庫は自分のワークスペースにしか見えない＝再配布にならない。
ASSETS = "/assets"
assets = modal.Volume.from_name("jiko-assets", create_if_missing=True)

CPU = 8.0            # 物理コア。build_jiko は最大8並列で焼く
MEM = 16384          # MiB。audio_mix が34分ぶんの float64 配列を数本持つ
HOURS = 4


def sh(cmd, cwd=WORK, check=True):
    """1コマンド走らせて、出力をそのまま流す。**Actions と同じ手順を同じ順に踏む。**"""
    t0 = time.time()
    print(f"\n$ {cmd}", flush=True)
    r = subprocess.run(cmd, shell=True, cwd=cwd)
    print(f"  ({time.time() - t0:.0f}秒 / 終了コード {r.returncode})", flush=True)
    if check and r.returncode:
        raise SystemExit(f"🔴 失敗: {cmd}")
    return r.returncode


def clone(ref):
    os.makedirs("/work", exist_ok=True)
    sh(f"git clone --depth 1 {REPO} {WORK}", cwd="/work")
    if ref and ref != "main":
        # 特定のコミットを焼きたいときは深さを足してから checkout する
        sh(f"git fetch --depth 50 origin {ref}")
        sh(f"git checkout {ref}")
    sh("git log --oneline -1")


# ── ★本編mp4を焼く ────────────────────────────────────────
@app.function(image=image, cpu=CPU, memory=MEM, timeout=HOURS * 3600,
              volumes={VOL: vol, ASSETS: assets})
def full(note: str = "", ref: str = "main", workers: int = 8,
         allow_drone: bool = False):
    """226カット・61,320コマを mp4 にして、音を乗せて保管庫に置く。

    手順は `.github/workflows/render-jiko.yml` の mode=full と**まったく同じ**。
    実行環境だけが Actions から Modal に変わっている。
    """
    # 🔴 焼く前に BGM の実体を確かめる（2026-08-01 追加）。
    #    `audio_mix.find_bgm()` は既製BGMが見つからないと**黙って自作ドローンに戻る**。
    #    パイプラインは壊れないので、ここで止めないと
    #    **30分かけて「BGMが違う34分」が焼き上がるまで気づけない。**
    #      直し方: modal volume put jiko-assets "...\\assets\\bgm.mp3" bgm.mp3
    #    ドローンで焼きたいときだけ `--allow-drone` を付ける。
    bgm = os.path.join(ASSETS, "bgm.mp3")
    size = os.path.getsize(bgm) if os.path.exists(bgm) else 0
    print(f"BGM … {bgm} / {size / 1e6:.2f} MB", flush=True)
    if size < 1_000_000 and not allow_drone:
        raise SystemExit(
            "🔴 保管庫に BGM が無い（か壊れている）ので焼かずに止めた。\n"
            '   modal volume put jiko-assets "<手元の assets\\bgm.mp3>" bgm.mp3\n'
            "   ドローンのまま焼いてよいときだけ --allow-drone を付ける。")

    clone(ref)
    env = f"ZUKAI_WORKERS={workers} "

    # ① 焼く前の机上検査（Actions と同じ3つ。ここで止まるならレンダする意味が無い）
    sh("python3 tools/scene_jiko.py --report")
    sh("python3 tools/check_layout.py", check=False)
    sh("python3 tools/check_echo.py", check=False)

    # ② 音声を opus から wav に戻す（wav はリポジトリに入れていない）
    sh("python3 tools/audio_pack.py check")
    sh("python3 tools/audio_pack.py unpack")

    # ③ 語尾が BGM に埋もれていないか（2026-07-31 の指摘①で追加した検査）
    sh("python3 tools/check_mask.py", check=False)

    # ③b ★実写「動画」を落として、必要なコマだけ切り出す（2026-08-01 追加）。
    #     🔴 動画はリポジトリに入れていないので、ここで URL から取る。
    #     ⚠️ 取れなくても止めない。コマが無ければ build 側は**静止画に落ちる**。
    sh("python3 tools/footage.py", check=False)

    # ④ レイヤー書き出し（SVG → PNG。Chrome headless）
    sh(env + "python3 tools/scene_jiko.py --force")

    # ★この本編を作ったレイヤー**そのもの**の指紋（2026-08-01 追加）。
    #   Actions の「Layer fingerprint」ステップと突き合わせる。
    #   `layer_hash` を別に走らせるより強い。あちらは「同じソースをもう一度焼いた結果」で、
    #   ここは「いま出荷する mp4 の中身そのもの」だから。1回ぶんの焼き代も浮く。
    #   ⚠️ ここが落ちても製造は続ける（指紋は検品の裏取りであって製造工程ではない）。
    sh("python3 tools/layer_hash.py", check=False)

    # ⑤ 合成（PNG → mp4）。**ここが Actions で回してはいけなかった工程**
    sh(env + "python3 tools/build_jiko.py full")

    # ⑥ ナレーション＋BGM＋効果音 → 映像に乗せる
    # ⚠️ BGM は保管庫（/assets/bgm.mp3）から読む。無ければ自作ドローンに戻る。
    sh(f"ls -la {ASSETS}/ || true", check=False)
    sh("python3 tools/audio_mix.py")
    sh("ffmpeg -y -hide_banner -loglevel error "
       "-i out/jiko/titan.mp4 -i out/jiko/mix.wav "
       "-c:v copy -c:a aac -b:a 192k -shortest out/jiko/titan_audio.mp4")

    # ⑦ 保管庫へ。名前に note を入れて、前の巡を潰さないようにする
    name = f"titan_audio{('-' + note) if note else ''}.mp4"
    sh(f"cp out/jiko/titan_audio.mp4 {VOL}/{name}")
    sh(f"ffprobe -v error -show_entries format=duration -of default=nw=1 {VOL}/{name}",
       check=False)
    sh(f"ls -la {VOL}/")
    vol.commit()
    print(f"\n✓ 焼けた → modal volume get jiko-out {name} out/jiko/", flush=True)
    return name


# ── 検品画像だけ（Actions が詰まっているときの逃げ道） ──────────
@app.function(image=image, cpu=CPU, memory=MEM, timeout=HOURS * 3600,
              volumes={VOL: vol})
def qa(note: str = "", ref: str = "main", zoom: str = ""):
    """検品画像を焼く。**ふだんは Actions で回す**（規約上こちらは白なので）。"""
    clone(ref)
    sh("python3 tools/scene_jiko.py --report")
    sh("python3 tools/check_layout.py", check=False)
    sh("python3 tools/footage.py", check=False)      # ★実写動画のコマ
    sh("python3 tools/scene_jiko.py --force")
    sh(f"python3 tools/build_jiko.py qa{(' --zoom=' + zoom) if zoom else ''}")
    sh("python3 tools/check_space.py out/jiko/qa", check=False)
    sh("python3 tools/build_jiko.py shrink")
    name = f"qa{('-' + note) if note else ''}"
    sh(f"rm -rf {VOL}/{name} && cp -r out/jiko/qa {VOL}/{name}")
    vol.commit()
    print(f"\n✓ modal volume get jiko-out {name} out/jiko/", flush=True)


# ── 疎通確認（いちばん安い。移設直後とエラーの切り分けに使う） ──────
@app.function(image=image, cpu=2.0, memory=4096, timeout=900)
def check(ref: str = "main"):
    """★焼く前に**環境だけ**を確かめる。数十秒で終わるので費用はほぼゼロ。

    ここで見るのは4つ。どれか欠けると本編レンダが途中で落ちる。
      ① Chrome が入っているか（図は Chrome が SVG から焼く）
      ② ffmpeg が入っているか（コマを mp4 にする）
      ③ GitHub から clone できるか
      ④ 音声（opus）とフォントがそろっているか
    """
    sh("google-chrome --version", cwd="/")
    sh("ffmpeg -version | head -1", cwd="/")
    clone(ref)
    sh("python3 -c \"import PIL,numpy,fontTools;print('Pillow',PIL.__version__,"
       "'numpy',numpy.__version__)\"")
    sh("ls fonts/ && ls audio/opus/ | wc -l && ls ref/*.jpg | wc -l")
    sh("python3 tools/scene_jiko.py --report")
    sh("python3 tools/audio_pack.py check")
    # レイヤーを1枚だけ焼いて、Chrome が実際に絵を出せることまで確かめる
    sh("python3 tools/scene_jiko.py --force --only=pr01 && ls -la out/jiko/")
    print("\n✓ 環境はそろっている。本編は `modal run modal_app.py::full` で焼ける。",
          flush=True)


# ── ★Modal の描画が Actions と一致しているかを機械で確かめる ──────
@app.function(image=image, cpu=CPU, memory=MEM, timeout=3600)
def layer_hash(ref: str = "main"):
    """レイヤーPNGの指紋を出す。**Actions の同じ出力と突き合わせる。**

    226カットの検品9巡は Actions の出力を見てやった。実行環境を移したあとで
    1画素でも変わっていたら、その検品は無効になる。
    Actions 側は `.github/workflows/render-jiko.yml` の
    「Layer fingerprint」ステップが同じ値を出すので、ログを見比べる。
    """
    clone(ref)
    sh("python3 tools/scene_jiko.py --force")
    sh("python3 tools/layer_hash.py")


@app.local_entrypoint()
def main(note: str = "", ref: str = "main"):
    """`modal run modal_app.py` で本編を焼く（引数なしの既定）。"""
    print(full.remote(note=note, ref=ref))
