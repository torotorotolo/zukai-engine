# -*- coding: utf-8 -*-
"""🔴 Modal を叩く前の門番。**課金が1円でも起きうるなら、押す前に止める。**

■ なぜ要るか（2026-08-02 の事故）
  この日、本編を2回焼こうとして2回とも失敗した。
    1回目 … `PYTHONIOENCODING` 未設定で、ローカルの cp932 が `✓` を出せず
             クライアントごと落ちた（リモートは動き始めていた）
    2回目 … レイヤー 650/1188 まで進んだところで
             `workspace ... is disabled` で停止
  2回目の正体は**枠切れではなく「支出上限（Workspace budget）切れ」**だった。
  支払い方法が未登録だと上限が $1 に抑えられ、$30 のクレジットは
  **付いていても一度も使えない**。
  ⚠️ どちらも**押す前に分かったはずのこと**。押してから30分待って気づいた。

■ 「絶対に課金しない」の担保（2026-08-02 カズヤくん指示）
  いちばん効いているのは**この道具ではなく、ワークスペースの予算設定**：

      予算 $5  <  クレジット $30/月

  予算は「**使用量**がその額に達したらアプリを停止」する仕組みで、
  クレジットは使用量を $30 まで吸収する。$5 で止まる時点で必ず $30 の内側なので、
  **請求は構造的に発生しない**。予算を $30 未満に保つ限りこれは崩れない。

  この道具は**その内側の二枚目**。役目は2つ：
    ① 万一 `Billed Cost` が $0 でなくなっていたら、**何もせず止める**
    ② 上限に当たって**途中で切られる**のを、押す前に防ぐ
       （切られると使用量だけ食って成果物が残らない。1回目の失敗がまさにこれ）

■ 使い方
    python tools/guard_cost.py            … いまの状態を見るだけ
    python tools/guard_cost.py --est 0.30 … $0.30 使う予定で回してよいか判定
  終了コード 0 なら回してよい。1 なら**回してはいけない**。
"""
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ── 上限（b3d/budget.py と同じ考え方で置く）────────────────────
# ⚠️ 「無料枠がいくらか」ではなく「**事故ってもこの額しか出ない**」で決める。
CREDITS_USD = 30.00      # Starter の月次クレジット（公式・毎月リセット）
BUDGET_USD = 5.00        # ワークスペースに設定した支出上限（ダッシュボード側の実値）
MARGIN = 0.90            # 上限のこれ以上は使わない（切られる前に自分で止まる）


def summary():
    """`modal billing summary` を読んで (使用量, 充当クレジット, 請求額) を返す。"""
    try:
        r = subprocess.run(["modal", "billing", "summary"],
                           capture_output=True, text=True, timeout=120,
                           encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return None, "modal コマンドが無い"
    if r.returncode:
        # ワークスペースが止められているとここに落ちる
        return None, (r.stderr or r.stdout or "").strip()[:400]
    txt = r.stdout

    def pick(label):
        m = re.search(rf"{label}:\s*\$?(-?[\d.]+)", txt)
        return float(m.group(1)) if m else None

    return (pick("Metered Cost"), pick("Credits"), pick("Billed Cost")), txt


def main(est=0.0):
    got, raw = summary()
    if got is None:
        print("🔴 請求情報を読めなかったので**止める**。")
        print(f"   {raw}")
        print("   → ワークスペースが無効化されている可能性がある。")
        print("      https://modal.com/settings/torotorotolo/usage を見ること。")
        return 1

    used, credits, billed = got
    used = used or 0.0
    billed = billed or 0.0
    avail = CREDITS_USD - used            # 残っているクレジット
    room = BUDGET_USD * MARGIN - used     # 予算まであとどれだけ使えるか

    print(f"  使用量        ${used:.2f}")
    print(f"  充当クレジット ${credits or 0.0:.2f}")
    print(f"  **請求額      ${billed:.2f}**")
    print(f"  クレジット残  ${avail:.2f} / ${CREDITS_USD:.2f}")
    print(f"  予算まで      ${room:.2f}（上限 ${BUDGET_USD:.2f} の {MARGIN:.0%} まで使う）")
    if est:
        print(f"  今回の見積り  ${est:.2f}")

    # ① すでに課金が発生していたら、理由を問わず止める
    if billed > 0.0:
        print()
        print(f"🔴 **すでに ${billed:.2f} 請求されている。何もせず止める。**")
        print("   「絶対に課金しない」という約束が破れているので、"
              "原因が分かるまで Modal を叩かないこと。")
        return 1

    # ② クレジットを超えるなら、そこから先は実費になる
    if est and used + est > CREDITS_USD:
        print()
        print(f"🔴 回すと使用量が ${used + est:.2f} になり、"
              f"クレジット ${CREDITS_USD:.2f} を超える＝**実費が出る**。止める。")
        return 1

    # ③ 予算に当たって途中で切られるなら、押す前に止める（使用量だけ食って無駄になる）
    if est and est > room:
        print()
        print(f"🔴 回すと予算 ${BUDGET_USD:.2f} に当たって**途中で切られる**"
              f"（あと ${room:.2f} しか使えない）。")
        print("   切られると使用量だけ食って成果物が残らない。押す前に止める。")
        print("   → 請求サイクルが変わるのを待つか、ダッシュボードで予算を上げること")
        print(f"      （⚠️ 上げてよいのは ${CREDITS_USD:.2f} 未満まで。"
              "そこを超えると請求が発生しうる）。")
        return 1

    print()
    print("✓ 回してよい（請求は発生しない見込み）。")
    return 0


if __name__ == "__main__":
    e = 0.0
    for i, a in enumerate(sys.argv):
        if a == "--est" and i + 1 < len(sys.argv):
            e = float(sys.argv[i + 1])
        elif a.startswith("--est="):
            e = float(a.split("=", 1)[1])
    sys.exit(main(e))
