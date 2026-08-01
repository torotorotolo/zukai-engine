# -*- coding: utf-8 -*-
"""実写**動画**を差し込むための素材まわり（2026-08-01 追加）。

🔴 なぜ入れたか（カズヤくん指示・2026-08-01）
   「PDでない写真・動画であっても積極的に使ってください。競合はそうしています。」
   ＋ r13 の試写「色使いが少なく、似た演出が続いて視覚的に飽きる」。
   静止画をもう1枚足すより、**海底で実際に動いている映像**を入れるほうが効く。

■ 置き場所の約束
   🔴 **動画をリポジトリに入れない**（wav 163MB で学んだのと同じ問題）。
      ワークフローの中で URL から落とし、コマを切り出して使う。
      落とした mp4     … out/jiko/clip/<name>.mp4   （gitignore）
      切り出したコマ    … out/jiko/foot/<cid>/00000.jpg …（gitignore）

■ 出典の書き方（★ここを間違えない）
   ⚠️ USCG の公開資料に載っている ROV 映像は、凡例が
      "U.S. Coast Guard video courtesy of Pelagic Research Services" となっている。
      **これを「パブリックドメイン」と書いてはいけない。** 撮影は民間会社である。
      → 事実のとおり「沿岸警備隊 海難審判部の公開資料／撮影：Pelagic Research Services」
        と出す。検証番組で出所を偽ると、内容そのものの信用が落ちる。

■ 使い方
     python tools/footage.py fetch          … 落として、必要なコマだけ切り出す
     python tools/footage.py fetch --check  … 落とさずに、割り当てだけ確認する
"""
import json
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

IA = "https://archive.org/download/uscg-titan-submersible-hearings/"

# ── 使う動画（Internet Archive の USCG 海難審判部アーカイブ） ──────
CLIPS = {
    "rov_tailcone": dict(
        # ⚠️ 同じ中身の複製が複数ある。1つが 500 を返しても次を試せるように並べておく
        #    （2026-08-01 の r16 で実際に archive.org のノードが 500 を返した）。
        paths=["Testimony Media/04_ROV Titan Submersible Tail Cone.mp4",
               "NTSB Titan Docket - DCA23FM036/04_ROV SNIPS-Rel.mp4",
               "Testimony Media/04_ROV Titan Submersible Tail Cone.ia.mp4"],
        path="Testimony Media/04_ROV Titan Submersible Tail Cone.mp4",
        credit="出典：アメリカ沿岸警備隊 海難審判部 公開資料／ROV撮影：Pelagic Research Services",
        note="60.7秒 1920×1080 30fps。尾部コーンに寄っていく。中盤に開口部の中が見える",
    ),
    "rov_aftdome": dict(
        paths=["Testimony Media/07_ROV Titan Submersible Aft Dome Aft Ring Hull Remnants.mp4",
               "NTSB Titan Docket - DCA23FM036/07_ROV SNIPS-Rel.mp4",
               "Testimony Media/07_ROV Titan Submersible Aft Dome Aft Ring Hull Remnants.ia.mp4"],
        path="Testimony Media/07_ROV Titan Submersible Aft Dome Aft Ring Hull Remnants.mp4",
        credit="出典：アメリカ沿岸警備隊 海難審判部 公開資料／ROV撮影：Pelagic Research Services",
        note="107.4秒 1920×1080 30fps。後部ドーム・リング・耐圧殻の破片",
    ),
}

# ── どのカットに、どの動画の何秒目から当てるか ────────────────
# 🔴 守ること
#   1. **そのカットで話している対象そのもの**であること（壁紙にしない）
#   2. 全部の実写カットを動画にしない。**動くのは数カットだけ**だから効く
#   3. ROV映像には焼き込みがある。本編は爆縮地点を **3,346m** と言っているので、
#      **深度の数字が1桁でも読める切り方をしない**（写真のときと同じ理由）。
#      🔴 実測した焼き込みの位置（1920×1080 の原寸）：
#        左上 "OceanGate"(y≈40) "Dive: 01"(y≈75) "Depth (m): 3775.5"(y≈110)／右端 x≈310 まで
#        下   日付(y≈1000)／"HDG"・"Alt"(y≈1035)
#        左端 ROV自身のアーム（x≈120 まで）
#      → 安全な窓は **y 130〜980・x 320〜1920**。
#        zoom=1.42（切り出し高さ 771px）／bias=0.55（上端 y≈170）／xbias=0.62（左端 x≈340）
#      ⚠️ 最初 zoom=1.30・bias=0.50 で切ったら上端が y≈124 になり、
#        深度表示の下半分が残って「776.1」と読めた（焼いて確認した）。
USE = {
    # 掴み。「水深3,346メートルで、ひとつの潜水艇が消えた」＝海底の残骸そのもの
    "pr01": dict(clip="rov_aftdome", start=41.0, xbias=0.62, zoom=1.42, bias=0.55),
    # 「6月22日、海底で残骸を見つけた。尾部と、2つのチタンのドーム」
    #   ⭐この映像そのものが**尾部コーン**で、焼き込みの日付も 06-22-2023 で一致する
    "c132": dict(clip="rov_tailcone", start=22.0, xbias=0.62, zoom=1.42, bias=0.55),
    # 「海底の残骸は、この形と一致していた。円筒は層に分かれていた」
    "c624": dict(clip="rov_aftdome", start=79.0, xbias=0.62, zoom=1.42, bias=0.55),
}
# ❌ 当てるのをやめたところ（記録）
#   c129「最初に無人探査機を積んだ船が着いた。だが3,000メートルまでしか潜れない」
#     … これは**捜索側の話**で、残骸の映像ではない。ここに残骸を出すと
#       「6月20日に見つかった」と読めてしまう。実際に見つかるのは6月22日。
#   c133「捜索に加わったのは船が11隻」／ep07「同じ音が聞こえていた」も同じ理由で当てない。


def urls_of(name):
    c = CLIPS[name]
    return [IA + urllib.parse.quote(p) for p in c.get("paths") or [c["path"]]]


def have(cid):
    """そのカットのコマが切り出してあるか。無ければ静止画に落ちる（壊れない）。"""
    return (FOOT / cid / "00000.jpg").exists()


def credit_of(cid):
    return CLIPS[USE[cid]["clip"]]["credit"] if cid in USE else None


def _dl(name):
    CLIP.mkdir(parents=True, exist_ok=True)
    dst = CLIP / f"{name}.mp4"
    if dst.exists() and dst.stat().st_size > 1_000_000:
        print(f"  {name}: すでにある（{dst.stat().st_size/1e6:.0f}MB）")
        return dst
    # 🔴 archive.org は `/download/` から実体のノードへ 302 で飛ばす。
    #    そのノードが 500 を返すことがある（2026-08-01 の r16 で実際に起きた）。
    #    **複製を順に試し、それぞれ数回まで粘る。**
    last = None
    for u in urls_of(name):
        for attempt in range(3):
            try:
                print(f"  {name}: 落とす {u}" + (f"（{attempt+1}回目）" if attempt else ""),
                      flush=True)
                req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=900) as r, open(dst, "wb") as f:
                    while True:
                        b = r.read(1 << 20)
                        if not b:
                            break
                        f.write(b)
                if dst.stat().st_size > 1_000_000:
                    print(f"     → {dst.stat().st_size/1e6:.0f}MB")
                    return dst
                last = f"中身が小さすぎる（{dst.stat().st_size}バイト）"
            except Exception as e:                       # noqa: BLE001
                last = f"{type(e).__name__}: {e}"
                print(f"     ⚠️ {last}", flush=True)
                time.sleep(4 * (attempt + 1))
    print(f"  🔴 {name}: どの複製も落とせなかった（最後の理由 {last}）")
    print("     ⚠️ このカットは**静止画に落ちる**。パイプラインは止めない。")
    return None


def fetch(check=False):
    import scene_jiko as S
    secs = dict(S.CUTS)
    missing = [c for c in USE if c not in secs]
    if missing:
        print(f"🔴 台本に無いカットに動画を割り当てている: {missing}")
        return 1
    print(f"■ 動画を当てるカット {len(USE)} 件")
    for cid, u in USE.items():
        print(f"  {cid}  尺{secs[cid]:5.2f}s  ← {u['clip']} の {u['start']}秒目から")
    if check:
        return 0
    got_clip = {}
    for name in {u["clip"] for u in USE.values()}:
        got_clip[name] = _dl(name) is not None
    for cid, u in USE.items():
        if not got_clip.get(u["clip"]):
            print(f"  {cid}: 動画が無いので飛ばす（静止画のまま）")
            continue
        d = FOOT / cid
        d.mkdir(parents=True, exist_ok=True)
        n = int(round(secs[cid] * FPS)) + 2
        src = CLIP / f"{u['clip']}.mp4"
        print(f"  {cid}: {n}コマ切り出す", flush=True)
        # ⚠️ -ss を -i の前に置く（キーフレーム単位で速く飛べる）。
        #    画質は元が 1920×1080 なので、そのまま出して build 側で切る。
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-ss", str(u["start"]), "-i", str(src),
             "-frames:v", str(n), "-q:v", "3", "-start_number", "0",
             str(d / "%05d.jpg")], check=True)
        got = len(list(d.glob("*.jpg")))
        print(f"     → {got}コマ")
        if got < n - 4:
            print(f"  🔴 {cid}: コマが足りない（{got}/{n}）。start が終端に近すぎる")
            return 1
    done = [c for c in USE if have(c)]
    print(f"✓ 切り出し完了 {len(done)}/{len(USE)} カット: {'、'.join(done) or 'なし'}")
    return 0


if __name__ == "__main__":
    sys.exit(fetch(check="--check" in sys.argv))
