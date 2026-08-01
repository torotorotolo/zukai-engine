# -*- coding: utf-8 -*-
"""ナレーション・BGM・効果音を1本のトラックに混ぜる。

■ なぜ BGM を自作の合成音にしたか（2026-07-29）
  DOVA-SYNDROME や 甘茶の音楽工房 は商用可・クレジット不要で規約上は使える。
  ただし **DOVA は「音源ファイルの配布」を禁じている**。
  このリポジトリは Actions の課金制限を避けるため **public** にしてあるので、
  mp3 を置くと再配布に当たる恐れがある（実際に規約へ明記されている）。
  そこで、事故検証の音づくりに必要な要素だけを自前で合成する。
  権利問題がゼロになり、尺にも完全に合わせられる。
  → 専用アカウントで private リポジトリを用意できたら、既製BGMに差し替えてよい。

■ 音の設計（シリアス・恐怖感）
  ドローン   … 低い持続音。55Hz を軸に少しだけ離調させてうねりを作る
  下支え     … 27.5Hz の超低音。鳴っていると気づかないが、抜くと軽くなる
  空気       … ごく小さいノイズ。無音の「死んだ感じ」を消す
  心拍       … 48拍/分。**原因が判明していく c4 / c5 だけ**に入れる
  低い衝撃音 … 掴み(p1)と、剥離の瞬間(c2)の2回だけ

  ⚠️ 金属の軋みや警報の「再現音」は入れない。
     実際の事故で鳴っていない音を足すと、検証番組としての信用が落ちる。
     （2026-07-29 カズヤくん決定：効果音は控えめ＝低い衝撃音と心拍だけ）

■ 音量（深読みフクロウの実績値 BGM 0.12 に合わせる）

■ 🔴 2026-07-31：語尾が BGM に埋もれていた（カズヤくんの試写指摘①）
  冒頭の「午前10時47分」が「じゅうじ よんじゅうなな」と聞こえた。
  読みは正しかった（kana_log も YOMI 辞書も `ジュウジヨンジュウナナフン`）。
  `tools/check_mora.py` で実測した原因はこうだった。

  | 80〜400Hz（鼻音「ン」の帯）で測った値 | |
  |---|---|
  | 直前の母音「ナ」 | 母音は BGM の **20dB 上** |
  | 文末の「ン」     | BGM の **1.5dB 上**しかない |

  日本語の「ン」は 80〜400Hz の鼻音 murmur にしか実体が無い。
  ところがドローンは 27.5／55／82.5／110／164.8Hz ＝**まったく同じ帯**を鳴らす。
  → 語尾が丸ごとマスクされる。**辞書を触ってはいけない事案だった。**

  直した2点（どちらもドローンの「低い持続音」という性格は壊さない）
   ① 声とぶつかる倍音（82.5／110／164.8Hz）を削る。
      ⚠️ ドローンのエネルギーは **89.9% が 80Hz 未満**にある。
         声の帯に居るのは 9.8% だけなので、そこを削っても低音の圧は残る。
   ② ナレーションが鳴っている間だけ寝床を下げる（サイドチェイン）。
      カット間の無音では元の高さに戻るので、間で BGM が息を吹き返す。

  検査 … `python tools/check_mask.py`（語尾とドローンの余裕 dB を全417行で測る）
"""
import json
import os
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S

SR = 44100
HERE = S.HERE

# ── ★既製BGM（2026-08-01 カズヤくん指定） ─────────────────
# 「陰鬱な灰色の気配」蒲鉾さちこ（DOVA-SYNDROME・2分23秒）
#   https://dova-s.jp/bgm/detail/21602
#   商用利用OK／クレジット任意。**ただし作者が音源の再配布を禁止している。**
#
# 🔴 だから **リポジトリに置かない**（このリポジトリは public なので、
#    置いた時点で再配布に当たる）。.gitignore にも入れてある。
#    置き場所は3つのどれか。見つかった順に使う：
#      ① 環境変数 ZUKAI_BGM が指すファイル
#      ② Modal の保管庫  /assets/bgm.mp3     ← クラウドで焼くときはここ
#      ③ ローカルの     assets/bgm.mp3       ← 手元で試すときはここ
#    どれも無ければ**自作のドローンに自動で戻る**（パイプラインは壊れない）。
#
#    Modal への置き方（最初の1回だけ）：
#      modal volume put jiko-assets "ダウンロードしたファイル.mp3" bgm.mp3
BGM_PATHS = [os.environ.get("ZUKAI_BGM", ""), "/assets/bgm.mp3",
             str(S.HERE / "assets" / "bgm.mp3")]
BGM_CREDIT = "BGM：陰鬱な灰色の気配／蒲鉾さちこ（DOVA-SYNDROME）"
# 既製曲は音の詰まり方が自作ドローンと違うので、**音量は割合でなく実測で決める**。
#
# 🔴 実測（2026-08-01）。**この曲は 90〜420Hz にエネルギーの 52.3% がある**
#    （自作ドローンは 9.8%）。そこは語尾の「ン」が鳴る帯そのものなので、
#    **同じ音量ならドローンの5倍マスクしやすい。** 音量は耳でなく測って決めた。
#
#    ■ カズヤくんの耳での判定を3回受けて、ここまで動かした
#      -38dB … 「全く聞こえない」（削る前）
#      -30dB … 「まだ小さい」    （90-420Hz を 12dB 削って +8dB 上げた）
#    **-24dB … 現在**            （削る量を 18dB にして、さらに +6dB 上げた）
#
#    ■ 削る量と、語尾が消えない上限（全417行で実測）
#      削る量 -12dB → 上限 -30dB ／ -16dB → -26dB ／ **-18dB → -24dB** ／ -20dB → -22dB
#      削る量を深くすると、そのぶんほぼ 1:1 で全体を上げられる。
#      ⚠️ ただし深くするほど音が痩せる（低音が抜けて「電話ごし」に近づく）。
#         -18dB あたりが、音楽として保てる限界に近い。
#
#    ⚠️ **曲を替えたら必ずこの表を取り直す**（`python tools/check_mask.py`）。
#      帯域の分布が違えば、同じ音量でも結果はまったく変わる。
#    🔴🔴 2026-08-01（2回目の指摘）「BGMが一切聞こえません」。
#      焼いた mp4 を実測したら、発話の切れ目で **-38〜-47dB**。
#      ナレーション（-14〜-16dB）より **25〜30dB 下**で、これは聞こえない。
#      設定は -24dB なのに実効が -38dB だった内訳：
#        -24（設定）－7（サイドチェインが95〜97%の時間ずっと効く）－7.4（ピーク正規化）
#      ⚠️ 上の「耳で3回詰めた」記録は `--head` の短い抜粋で聴いた値。
#        **抜粋はピークが低いので正規化量が違い、全長で焼くと数dB小さくなる。**
#        音量を耳で決めるときは**必ず全長で焼いたものを聴く**こと。
#    ✅ 2026-08-01（決着）：カズヤくんが **r13 を全長で聴いて「BGM音量は今のままで良い」**
#      と判定した。r13 は -24.0 ／ 削り -18.0 で焼いてある。
#      → **上げた値（-15.0／削り-30.0）は取り消し、r13 の値に戻した。**
#        上の調査（実効 -38dB の内訳・削る量と語尾の関係）は正しいので記録として残すが、
#        **「25〜30dB 下＝聞こえない」という機械の判定は耳の判定と食い違った。**
#        この用途では -38dB 相当でも十分に聞こえている＝**次に音量を疑うときも、
#        まず全長を聴いてから測ること**（機械の数字だけで動かさない）。
BGM_RMS = -24.0          # BGMだけのときの実効音量（dBFS RMS）★r13＝カズヤくん判定OK

# 🔴 2026-08-01 カズヤくん「BGMが全く聞こえない。もう少し大きく」。
#    原因は音量設定ではなく**サイドチェインが99%の時間ずっと効いている**こと
#    （ナレーションがほぼ途切れないため）。実質 -38 -7 = -45dB で鳴っていた。
#
#    そのまま上げると語尾が埋もれる。そこで**声とぶつかる帯だけ削ってから上げる**。
#    この曲の帯域は 90-420Hz が 52.3%／420-2000Hz が 47.1%／2kHz以上はほぼ0%。
#    語尾の「ン」が居るのは 90-420Hz だけなので、**そこを削れば残り半分は自由に上げられる**。
#    → 音楽としての存在感（中音）は残したまま、マスクだけ減らせる。
#    18dB 削ると 90-420Hz は 52.3% → 約6% になり、音楽の中心が 420-2000Hz に移る。
#    🔴 2026-08-01（2回目の指摘で作り直した）。18dB／-24dB では**一切聞こえなかった**ので、
#      削る量を 30dB、音量を -15dB にした（正味 +9dB）。
#      ⚠️ **削る量を深めると語尾の余裕はむしろ増える。**
#        余裕は 80〜400Hz でしか測らないので、その帯を削る速度のほうが上げる速度より速い。
#          削り18／-24 → c502 の余裕 7.9dB（従来）
#          削り26／-18 → 9.4dB ／ 削り30／-15 → **10.3dB** ／ 削り34／-12 → 11.0dB
#        つまり**トレードオフは語尾ではなく「BGMの太さ」だけ**。
#        30dB 削ると低音がほぼ消え、中音のパッドのような響きになる。
#      → **聞こえないBGMより、痩せていても聞こえるBGM**を採った（2026-08-01）。
#    🔴🔴 根本原因：**この曲は 90〜420Hz にエネルギーの 52.3% がある。**
#      そこは語尾の「ン」が鳴る帯そのもの。つまり**曲の半分を捨ててようやく使える**曲で、
#      構造的にこの用途に向いていない。**500Hz 以上に重心のある曲に替えれば、
#      削らずに10dB以上上げられる。** 音量で詰まったら、次は曲を替えること。
#    ✅ 2026-08-01（決着）：カズヤくんの全長試聴で **「BGM音量は今のままで良い」**。
#      → 削り -30.0 は取り消し、**r13 の -18.0 に戻した**（BGM_RMS も -24.0 に戻した）。
#        深く削るほど語尾の余裕が増えるという上の表自体は有効なので、
#        **将来また語尾で詰まったら、音量を下げずに削りを深める**のが先手。
BGM_CARVE = (90, 420, -18.0)     # (下端Hz, 上端Hz, 何dB下げるか)★r13＝カズヤくん判定OK
BGM_CARVE_OCT = 0.5              # 端をなだらかにする幅（オクターブ）
BGM_XFADE = 3.0          # ループの継ぎ目をまたぐクロスフェード（秒）

V_NARR = 1.00
V_BGM = 0.12             # ★自作ドローンに戻ったときだけ使う値
V_HEART = 0.10
V_IMPACT = 0.30

# 🔴 サイドチェイン：ナレーションが鳴っている間だけ寝床を下げる（2026-07-31）。
#    深さは実測で決めた。**倍音を削るだけでは語尾の余裕が基準に届かなかった**ので併用する。
#    立ち上がりを速く・戻りを遅くすると、文と文の切れ目で BGM が持ち上がって
#    「うねって」聞こえる。**戻りをゆっくり（1.1秒）**にしてうねりを消す。
# 🔴🔴 2026-08-01：7.0dB は**「たまに下がる」量としては妥当だが、
#    「95〜97%の時間ずっと下がっている」量としては深すぎた。**
#    サイドチェインは「話している間だけ下げる」設計なのに、この台本は間がほとんど無く、
#    実測で 95〜97% の時間ずっと効いている＝**実質は常時 -7dB の減衰**になっていた。
#    → 常時かかる前提なら浅くてよい。**語尾の保護は主に 18dB の帯域カット（BGM_CARVE）
#      が担っている**ので、深さを削っても語尾は守られる（check_mask で毎回確認すること）。
#    ⚠️ 2026-08-01 に 4.5dB へ浅くしてみたが、**`c502` の語尾が 7.9→5.4dB＝「消える」**に
#      落ちたので 7.0 に戻した。語尾の余裕は BGM の音量と 1:1 で減る。
DUCK_DB = 7.0            # 話しているあいだ寝床を何dB下げるか
DUCK_ATK = 0.12          # 下がりきるまで（秒）
# 🔴 2026-08-01：1.10秒は**長すぎた**。文と文の切れ目（0.3〜0.5秒）や
#    カット間の無音（0.85秒）でBGMが戻りきる前に次の声が来るので、
#    **34分ずっと下がりっぱなし**になっていた（「話している時間 99%」の正体）。
#    0.45秒にすると、句読点ごとにBGMが息を吹き返す＝音量を上げずに存在感が出る。
DUCK_REL = 0.45          # 戻りきるまで（秒）
DUCK_FLOOR = -42.0       # これ以下のナレーションは「鳴っていない」とみなす（dBFS）

# 🔴 ナレーションの圧縮（2026-08-01 追加）。
#    BGMを下げただけでは足りなかった。**声そのものの語尾が弱い。**
#      pr01「47分」… 直前の母音 −14.4dB → 語尾の「ン」 −27.4dB（13dB落ちる）
#      c117「49分」… 直前の母音 −12.6dB → 語尾の「ン」 −21.1dB（指摘が出ていない方）
#    同じ話者・同じ話速でも 6dB 違い、−27dB は聞き取れない。
#    → 大きいところを抑えて全体を持ち上げ、**語尾だけが相対的に上がる**ようにする。
#    ⚠️ 解放を長くすると語尾まで一緒に抑え込んでしまう。**0.13秒**で戻す
#       （「ナ」→「フン」の間が 0.1〜0.2 秒なので、そこで利得が回復している必要がある）。
COMP_T = -24.0           # これより大きいところを抑える（dBFS）
COMP_R = 3.0             # 圧縮比
COMP_ATK = 0.005         # 効き始め（秒）
COMP_REL = 0.13          # 戻り（秒）★ここが肝
# 🔴 ここで一度まちがえた記録（2026-08-01）。
#    ナレーションの wav は **すでに 0dBFS まで正規化されている**ので、
#    ピークを保つメイクアップを足すと BGM を乗せる余地が無くなり、
#    最後の全体正規化が 0.584倍まで効いた。それを避けようとして
#    **ナレーションだけを 5dB 下げた**が、これは誤り。
#    BGM は下がらないので、**声とBGMの差が 5dB 縮まった**
#    （check_mask で「消える」が 0行→4行に増えて気づいた）。
#    → 正しくは **0 のまま**。全体正規化は声もBGMも同じ倍率で下げるので、
#      比は保たれる。YouTube 側でも音量は正規化されるので、絶対値は問題にならない。
COMP_HEADROOM = 0.0

# 🔴 2026-07-31：ここはテスト映像（アロハ航空）のカットIDのままだった。
#    `p1` `c2` `c4` `c5` はタイタン号の台本に存在しないので、**心拍も衝撃音も
#    一度も鳴らないまま34分が焼かれるところだった。**
#
# ■ どこに入れるかの判断（人が亡くなる場面には入れない）
#    心拍は「見ている人が危険に気づく」ところに入れる。**人が亡くなる場面には入れない。**
#    c115b（耐圧殻が壊れ、5名が亡くなった）に鼓動を敷くのは、
#    デリケートな事象の利用(exploit)に近づく。規約でもチャンネルの性格でも取らない。
#    → 装置が警告し続けていたと分かる c529〜c534 と、
#      11か月の空白から88回目へ向かう c614〜c617 に入れる。
HEART_CUTS = {"c529", "c530", "c531", "c532", "c533", "c534",
              "c614", "c615", "c616", "c617"}
# 低い衝撃音は**掴みの1回だけ**。爆縮の瞬間には置かない。
# そこに衝撃音を置くと「再現音」になり、実際に鳴っていない音を足すことになる
# （2026-07-29 決定：再現音は入れない）。
IMPACT_AT = {"pr01": 0.15}


def read_wav(p):
    with wave.open(str(p)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        if w.getnchannels() == 2:
            a = a.reshape(-1, 2).mean(axis=1)
        if w.getframerate() != SR:
            n = int(len(a) * SR / w.getframerate())
            a = np.interp(np.linspace(0, len(a), n, endpoint=False),
                          np.arange(len(a)), a)
    return a.astype(np.float64) / 32768.0


def drone(n):
    """低い持続音。純音を重ねると機械的なので、わずかに離調させてうねらせる。

    🔴 2026-07-31：82.5／110／164.8Hz を削った。
       ここは阿井田茂（男声）の基本周波数と鼻音「ン」の murmur が乗る帯で、
       **語尾がまるごとマスクされていた**（実測 1.5dB 差）。
       ドローンのエネルギーの 89.9% は 80Hz 未満にあるので、
       削っても「低く重い持続音」という性格は残る。
    """
    t = np.arange(n) / SR
    y = np.zeros(n)
    for f, a in ((27.5, 0.55), (55.0, 1.00), (55.31, 0.85), (82.5, 0.20),
                 (110.0, 0.07), (164.8, 0.00)):
        y += a * np.sin(2 * np.pi * f * t + a * 3.1)
    y /= 3.1
    # 11秒周期のゆっくりした膨らみ
    y *= 0.62 + 0.38 * (0.5 - 0.5 * np.cos(2 * np.pi * t / 11.0))
    # 空気（ごく小さいノイズ。移動平均で高域を落とす）
    rng = np.random.default_rng(20260729)
    air = rng.standard_normal(n)
    k = 24
    air = np.convolve(air, np.ones(k) / k, mode="same")
    y += 0.10 * air / (np.abs(air).max() + 1e-9)
    return y


def find_bgm():
    """既製BGMの実体を探す。無ければ None（自作ドローンに戻る）。"""
    for p in BGM_PATHS:
        if p and Path(p).exists():
            return Path(p)
    return None


def carve(x, band=None, oct_=None):
    """BGMから**声とぶつかる帯だけ**を削る。音楽の存在感は中音に残す。

    🔴 なぜ必要か
       ナレーションがほぼ途切れないので、サイドチェインは 99% の時間ずっと効いている。
       つまり BGM は実質「常に7dB下がった状態」で鳴っていて、聞こえない。
       かといって全体を上げると、語尾の「ン」（80〜400Hz）が埋もれる。
       → **ぶつかる帯だけ下げて、全体を上げる。**
    ⚠️ 端を切り立たせると「電話の音」のような不自然さが出る。
       0.5オクターブかけてなだらかに落とす。
    """
    lo, hi, gain = band or BGM_CARVE
    oct_ = oct_ or BGM_CARVE_OCT
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.ones(len(fr))
    k = 10 ** (gain / 20.0)
    g[(fr >= lo) & (fr <= hi)] = k
    # 下の端（lo/2^oct → lo）と上の端（hi → hi*2^oct）をなだらかにつなぐ
    for a, b, rising in ((lo / 2 ** oct_, lo, False), (hi, hi * 2 ** oct_, True)):
        m = (fr > a) & (fr < b)
        if not m.any():
            continue
        t = (np.log2(fr[m] / a)) / max(np.log2(b / a), 1e-9)
        s = 0.5 - 0.5 * np.cos(np.pi * t)          # 0→1 のなめらかな曲線
        g[m] = (1 + (k - 1) * s) if not rising else (k + (1 - k) * s)
    return np.fft.irfft(X * g, len(x))


def music(n, path):
    """既製BGMを尺いっぱいに敷く。**継ぎ目はクロスフェードでつなぐ。**

    ⚠️ 2分23秒の曲を34分に敷くと **14回以上ループ**する。
       ぶつ切りで並べると継ぎ目でプツッと鳴るので、必ず重ねて渡す。
    ⚠️ 音量は「元ファイルの何倍」ではなく **実効音量（RMS）を測って揃える**。
       曲を差し替えても体感の大きさが変わらないようにするため。
    """
    # mp3 → 生の 44.1kHz モノラルに落とす（ffmpeg は既に使っている）
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le",
         "-acodec", "pcm_s16le", "-ar", str(SR), "-ac", "1", "-"],
        capture_output=True)
    if r.returncode or not r.stdout:
        print(f"🔴 BGM を読めなかった: {path} … 自作ドローンに戻す")
        return None
    src = np.frombuffer(r.stdout, dtype="<i2").astype(np.float64) / 32768.0
    if len(src) < SR * 5:
        print(f"🔴 BGM が短すぎる（{len(src)/SR:.1f}秒）… 自作ドローンに戻す")
        return None
    src = carve(src)
    # ⚠️ 実効音量は**削ったあと**にそろえる。先にそろえると、削ったぶんだけ小さくなる。
    rms = np.sqrt((src ** 2).mean())
    src *= 10 ** (BGM_RMS / 20.0) / max(rms, 1e-9)

    xf = int(BGM_XFADE * SR)
    body = len(src) - xf
    out = np.zeros(n + len(src))
    fade_in = np.linspace(0.0, 1.0, xf)
    pos, first = 0, True
    while pos < n:
        seg = src.copy()
        if not first:
            seg[:xf] *= fade_in            # 頭を持ち上げながら
        seg[-xf:] *= fade_in[::-1]         # 尻を落として重ねる
        out[pos:pos + len(seg)] += seg
        pos += body
        first = False
    print(f"BGM「{path.name}」{len(src)/SR:.0f}秒を "
          f"{-(-n // body)} 回つないだ（継ぎ目 {BGM_XFADE:.0f}秒の重ね）", flush=True)
    return out[:n]


def heartbeat(n, bpm=48.0):
    """48拍/分。lub-dub の2打で1拍。低い正弦に速い減衰をかける。"""
    y = np.zeros(n)
    period = 60.0 / bpm
    for beat in np.arange(0, n / SR, period):
        for off, amp in ((0.0, 1.0), (0.30, 0.62)):
            i = int((beat + off) * SR)
            ln = int(0.34 * SR)
            if i + ln > n:
                break
            t = np.arange(ln) / SR
            env = np.exp(-t * 17.0)
            y[i:i + ln] += amp * env * np.sin(2 * np.pi * 46.0 * t)
    return y


def impact(dur=2.4):
    """低い衝撃音。60Hz から 28Hz へ落ちる掃引＋ごく短いノイズの立ち上がり。"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 60.0 * np.exp(-t * 1.5) + 26.0
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t * 2.1)
    rng = np.random.default_rng(4321)
    nz = rng.standard_normal(n) * np.exp(-t * 26.0)
    k = 40
    nz = np.convolve(nz, np.ones(k) / k, mode="same")
    y += 0.9 * nz / (np.abs(nz).max() + 1e-9)
    return y / (np.abs(y).max() + 1e-9)


def compress(x, t=COMP_T, r=COMP_R, atk=COMP_ATK, rel=COMP_REL):
    """ナレーションを圧縮して、**弱い語尾を相対的に持ち上げる。**

    大きいところ（母音）だけを抑え、抑えたぶんを全体に足し戻す（メイクアップ）。
    結果として、もともと閾値より小さい語尾は**そのまま**、母音だけが下がるので、
    2つの差が縮まる。声を大きくするのではなく**差を縮める**のが狙い。

    ⚠️ 1サンプルずつ Python で回すと 34分＝9,000万回で終わらない。
       **1ms のブロック単位**で利得を出して掛ける（語尾は 100ms 以上あるので足りる）。
    """
    blk = max(1, int(0.001 * SR))
    k = len(x) // blk
    if k < 2:
        return x
    lv = np.abs(x[:k * blk].reshape(k, blk)).max(axis=1)
    db = 20 * np.log10(lv + 1e-12)
    over = np.maximum(0.0, db - t)              # 閾値をどれだけ超えているか
    tgt = -over * (1.0 - 1.0 / r)               # 目標の利得（dB・0以下）
    ka = 1 - np.exp(-blk / SR / max(atk, 1e-6))
    kr = 1 - np.exp(-blk / SR / max(rel, 1e-6))
    g = np.empty(k)
    cur = 0.0
    for i, v in enumerate(tgt):
        cur += (v - cur) * (ka if v < cur else kr)
        g[i] = cur
    # メイクアップは**その音声自身のピーク**から出す。閾値から出すと
    # 「ピークが 0dBFS の音声」を前提にした量になり、余裕が残らない。
    peak_db = float(db.max())
    makeup = max(0.0, peak_db - t) * (1.0 - 1.0 / r) - COMP_HEADROOM
    lin = 10 ** ((g + makeup) / 20.0)
    out = x.copy()
    body = out[:k * blk].reshape(k, blk)
    body *= lin[:, None]
    out[k * blk:] *= lin[-1]
    return out


def duck_gain(narr, n, blk=None):
    """ナレーションが鳴っているあいだ寝床を下げる倍率を、10ms ごとに返す。

    🔴 全長ぶんの倍率を配列で持つと 34 分で 720MB になる。**ブロック単位で持つ**。
       立ち上がり 0.12 秒・戻り 1.10 秒の一極フィルタなので、
       10ms のブロックのまま掛けても段差は聞こえない。
    """
    blk = blk or int(0.010 * SR)
    k = n // blk
    lv = np.zeros(k)
    m = min(k * blk, len(narr))
    lv[:m // blk] = np.abs(narr[:m].reshape(-1, blk)).max(axis=1)
    lv = 20 * np.log10(lv + 1e-12)
    tgt = np.where(lv > DUCK_FLOOR, 10 ** (-DUCK_DB / 20), 1.0)
    # 一極の追従（下がるのは速く、戻るのはゆっくり）
    ka = 1 - np.exp(-blk / SR / max(DUCK_ATK, 1e-6))
    kr = 1 - np.exp(-blk / SR / max(DUCK_REL, 1e-6))
    g = np.empty(k)
    cur = 1.0
    for i, v in enumerate(tgt):
        cur += (v - cur) * (ka if v < cur else kr)
        g[i] = cur
    return g, blk


def main(head=None, out_name="mix.wav", duck=True):
    """head に秒を渡すと**先頭その秒だけ**を混ぜる。

    🔴 34分ぶんを混ぜると float64 の配列だけで数GBになり、**4GBのPCでは開けない**。
       聴き比べのために頭だけ焼きたいときは `--head=14` を使う。
    """
    cuts = S.CUTS
    if head:
        keep, t = [], 0.0
        for cid, sec in cuts:
            keep.append((cid, sec))
            t += sec
            if t >= head:
                break
        cuts = keep
    total = sum(s for _, s in cuts)
    n = int(total * SR) + SR
    # ★既製BGMがあればそれを、無ければ自作ドローンを敷く
    src = find_bgm()
    bed = music(n, src) if src else None
    if bed is None:
        bed = drone(n) * V_BGM
        print("BGM＝自作のドローン（既製BGMが見つからない）", flush=True)
    mix = np.zeros(n)

    starts, t = {}, 0.0
    for cid, sec in cuts:
        starts[cid] = t
        t += sec

    # ナレーション
    audio = HERE / "audio"
    for cid, _ in cuts:
        p = audio / f"{cid}.wav"
        if not p.exists():
            print(f"! {cid}.wav が無い")
            continue
        # ★カットごとに圧縮する。34分をまとめて掛けると、静かなカットの
        #   ノイズまで持ち上がる（カット間の無音はここには入っていない）。
        a = compress(read_wav(p)) * V_NARR
        i = int((starts[cid] + S.LEAD) * SR)
        mix[i:i + len(a)] += a[:max(0, n - i)]

    # 🔴 サイドチェイン。**ナレーションだけ**を鍵にして寝床を下げる
    #    （心拍と衝撃音は鍵に入れない。鳴った瞬間に BGM が沈んで不自然になる）。
    if duck:
        dg, blk = duck_gain(mix, n)
        for i, v in enumerate(dg):
            bed[i * blk:(i + 1) * blk] *= v
        print(f"サイドチェイン：話している時間 {100 * (dg < 0.9).mean():.0f}% ／ "
              f"最大 {-20 * np.log10(dg.min()):.1f}dB 下げた")

    # 心拍（該当カットだけ。頭で 0.8 秒かけて立ち上げ、尻で落とす）
    hb = heartbeat(n) * V_HEART
    gate = np.zeros(n)
    for cid, sec in cuts:
        if cid not in HEART_CUTS:
            continue
        i, j = int(starts[cid] * SR), int((starts[cid] + sec) * SR)
        ramp = int(0.8 * SR)
        g = np.ones(j - i)
        g[:ramp] = np.linspace(0, 1, ramp)
        g[-ramp:] = np.linspace(1, 0, ramp)
        gate[i:j] = np.maximum(gate[i:j], g)
    mix += hb * gate

    # 低い衝撃音
    imp = impact()
    for cid, off in IMPACT_AT.items():
        if cid not in starts:
            continue
        i = int((starts[cid] + off) * SR)
        e = min(n, i + len(imp))
        mix[i:e] += imp[:e - i] * V_IMPACT

    # ⚠️ 2026-08-01：ここで「BGMを足す前にナレーションを正規化する」順序に変えたが、
    #    **撤回した。** 設定値と実音が食い違う件（下記）は本当だが、順序を変えると
    #    **BGMだけが正規化を免れて声との比が約6dB変わり、`check_mask` の測定が
    #    実際より甘く出る**（あの検査は正規化を含めずに比を測っているため）。
    #    語尾の検査が信用できなくなる代償のほうが大きい。
    #    → 音量は **BGM_RMS と BGM_CARVE で稼ぐ**（どちらも check_mask が正しく追える）。
    #
    # 🔴 記録：設定 -24dBFS に対し、**最終ファイルでの実効は約 -38dB**だった。
    #    内訳 = -24（設定）-7（サイドチェインが95〜97%の時間ずっと効く）
    #           -7.4（ピーク正規化 0.425倍）。焼いた mp4 の実測とも一致する。
    #    ⚠️ 耳で3回詰めた記録（-38→-30→-24）は `--head` の短い抜粋で聴いた値。
    #      **抜粋はピークが低いので正規化量が違い、全長では数dB小さくなる。**
    mix += bed
    peak = np.abs(mix).max()
    if peak > 0.97:
        mix *= 0.97 / peak
        print(f"ピークが {peak:.2f} だったので {0.97 / peak:.3f} 倍に下げた")
        print(f"　→ BGMの実効音量は設定より {-20 * np.log10(0.97 / peak):.1f}dB 小さくなる")

    out = HERE / "out" / "jiko"
    out.mkdir(parents=True, exist_ok=True)
    p = out / out_name
    with wave.open(str(p), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print(f"wrote {p}  {total:.1f}秒  ピーク {np.abs(mix).max():.2f}")


if __name__ == "__main__":
    import sys as _s
    hd = next((float(a.split("=")[1]) for a in _s.argv[1:] if a.startswith("--head=")), None)
    nm = next((a.split("=")[1] for a in _s.argv[1:] if a.startswith("--out=")), "mix.wav")
    main(head=hd, out_name=nm, duck="--noduck" not in _s.argv[1:])
