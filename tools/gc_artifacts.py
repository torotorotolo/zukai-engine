# -*- coding: utf-8 -*-
"""クラウドの成果物（Artifacts）を掃除する。**これが実際に効いてくる制限**。

■ どの制限に当たるのか（2026-07-31 に実測して分かったこと）
  このリポジトリは **public** なので、**Actions の実行時間は無料で上限が無い**。
  尽きるのはそこではなく、**アカウント共通の成果物ストレージ 500MB** のほう。

  実測：テスト映像23巡＋サムネ8巡で **57件・1.02GB** まで積み上がっていた（無料枠の2倍）。
  1巡ごとに qa 10〜23MB ＋ mp4 24〜49MB が残り、**消さない限り90日間居座る**。
  本編は226カットあるので、qa だけで1巡 100MB を超える。**5巡回すと即座に枠を割る。**

■ 対策（この順で効く）
  1 ワークフロー側で `retention-days: 5` を付ける（render-jiko.yml で設定済み）
  2 巡が終わって中身を見たら、その巡の成果物を消す ← この道具
  3 それでも足りないときは深読みフクロウと同じ手：
    **アカウントを2つ持ち、片方の枠が尽きたらもう片方のミラーで焼く。**
    フクロウは `c8814040-dev` と `torotorotolo` の2つに同じリポジトリを置いている。
    ⚠️ ただしフクロウのリポジトリは private なので「実行時間2,000分/月」の枠を分けている。
    　 こちらは public で実行時間は無限なので、**分けたいのはストレージのほう**。
    　 ミラーを作るなら、そちらも public にすれば実行時間は無料のまま使える。

使い方：
  python tools/gc_artifacts.py                … 一覧と合計だけ出す（消さない）
  python tools/gc_artifacts.py --keep 4       … 新しい4件だけ残して消す
  python tools/gc_artifacts.py --older 7      … 7日より古いものを消す
"""
import json
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

REPO = "torotorotolo/zukai-engine"
API = f"repos/{REPO}/actions/artifacts?per_page=100"


def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode:
        sys.exit(f"gh が失敗しました: {r.stderr[:400]}")
    return r.stdout


def listing():
    # ⚠️ per_page を付けないと既定30件しか返らない。
    #    それに気づかず合計を出して「593MB」と誤って読んだ（実際は1.02GB）。
    d = json.loads(gh("api", API))
    return sorted(d["artifacts"], key=lambda a: a["created_at"], reverse=True)


def main():
    arts = listing()
    tot = sum(a["size_in_bytes"] for a in arts)
    print(f"{len(arts)} 件 / {tot / 1048576:.0f} MB（無料枠 500MB）")
    for a in arts:
        print(f'  {a["created_at"][:10]}  {a["size_in_bytes"] / 1048576:>6.0f}MB  '
              f'{a["name"]}')
    keep = older = None
    for i, a in enumerate(sys.argv):
        if a == "--keep":
            keep = int(sys.argv[i + 1])
        if a == "--older":
            older = int(sys.argv[i + 1])
    if keep is None and older is None:
        print("\n（消していません。--keep N か --older N を付けると消します）")
        return
    import datetime as dt
    now = dt.datetime.now(dt.timezone.utc)
    doomed = []
    for i, a in enumerate(arts):
        if keep is not None and i < keep:
            continue
        if older is not None:
            age = (now - dt.datetime.fromisoformat(a["created_at"])).days
            if age < older:
                continue
        doomed.append(a)
    if not doomed:
        print("\n消すものはありません")
        return
    freed = 0
    for a in doomed:
        gh("api", "-X", "DELETE", f'repos/{REPO}/actions/artifacts/{a["id"]}')
        freed += a["size_in_bytes"]
        print(f'  消した: {a["name"]}')
    print(f"\n{len(doomed)} 件 / {freed / 1048576:.0f} MB を空けた")


if __name__ == "__main__":
    main()
