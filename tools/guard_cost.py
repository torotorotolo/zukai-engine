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
    python tools/guard_cost.py --selftest … 🔴 物差しそのものを検算する
  終了コード 0 なら回してよい。1 なら**回してはいけない**。

■ 🔴 2026-08-07：**この門番は一度壊れていた**（下の parse() の注記を読むこと）
  modal の出力形式が表に変わり、金額を1つも読めないまま **$0.00 と表示して
  「✓ 回してよい」と言い続けていた**。読めないものを 0 と見なす作りだったため。
  → いまは **fail closed**（読めなければ止まる）。
  ⚠️ **modal を上げたら `--selftest` を通す。** 出力形式はまた変わる。
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
    got = parse(txt)
    if got is None:
        return None, ("請求額を1つも読み取れなかった。modal の出力形式が変わった可能性。\n"
                      f"   --- 実際の出力 ---\n{txt.strip()[:400]}")
    return got, txt


# ══ 🔴 2026-08-07：**この門番は壊れていた** ═══════════════════════════
#  `modal billing summary` の出力が**枠線つきの表**に変わっていた：
#        | Metered Cost:     |  1.83 |
#  旧 `rf"{label}:\s*\$?(-?[\d.]+)"` は `:` の直後の `|` で止まるので**全項目 None**。
#  それを main() の `used = used or 0.0` / `billed = billed or 0.0` が
#  **黙って $0.00 に化かしていた**。
#  → 実測 $1.83 使っているのに「使用量 $0.00・クレジット残 $30.00・予算まで $4.50」と
#    表示し、**役目①（請求が出ていたら止める）が完全に無効**になっていた。
#    Billed Cost が $12 でも「✓ 回してよい」と言う状態だった。
#  直しは2つ。**両方入れる**：
#    ① 枠線を許す正規表現にする（新旧どちらの形でも読める）
#    ② 🔴 **読めなかったら 0 で埋めずに止める（fail closed）**。
#       門番が「読めない」を「安全」と読み替えるのがいちばん危ない。
#  → [[feedback-verify-your-own-instrument]]（自分の物差しをまず疑う）
#  ⚠️ この `_NUM` も**最初に書いたものは間違っていた**（`:` と `|` のあいだの空白を
#     取りこぼし、実物の表を読めなかった）。`--selftest` が拾った。
#     コロンのあと → 空白 → 縦棒(省略可) → 空白 → $(省略可) → 数値、の順で書く。
_NUM = r"\s*\|?\s*\$?\s*(-?\$?[\d,]+\.?\d*)"


def parse(txt: str):
    """(使用量, 充当クレジット, 請求額) を返す。**1つでも読めなければ None**。"""
    def pick(label):
        m = re.search(rf"{re.escape(label)}\s*:{_NUM}", txt)
        if not m:
            return None
        return float(m.group(1).replace(",", "").replace("$", ""))

    vals = (pick("Metered Cost"), pick("Credits"), pick("Billed Cost"))
    return None if any(v is None for v in vals) else vals


def selftest() -> int:
    """🔴 物差しは、既知の1件で当ててから信じる。
    新しい表形式・昔の平文・読めない形の3種を通す。"""
    cases = [
        ("表形式（2026-08-07 の実物）",
         "+---------------------------+\n"
         "| Metered Cost:     |  1.83 |\n"
         "|   Ephemeral Apps: |  1.83 |\n"
         "|   Volumes:        |  0.01 |\n"
         "| Credits:          | -1.83 |\n"
         "| Free Storage:     | -0.01 |\n"
         "| Billed Cost:      | $0.00 |\n"
         "+---------------------------+\n", (1.83, -1.83, 0.00)),
        ("平文（旧形式・これは前から読めていた）",
         "Metered Cost: $12.34\nCredits: -10.00\nBilled Cost: $2.34\n", (12.34, -10.0, 2.34)),
        ("桁区切りあり", "| Metered Cost: | 1,234.50 |\n| Credits: | -30.00 |\n"
                    "| Billed Cost: | $1,204.50 |\n", (1234.50, -30.0, 1204.50)),
        ("マイナスの$（-$10.00）", "Metered Cost: 5.00\nCredits: -$5.00\nBilled Cost: $0.00\n",
         (5.0, -5.0, 0.0)),
        ("🔴 読めない形 → None（0で埋めない）", "Something went wrong\n", None),
        ("🔴 項目が欠けた形 → None", "| Metered Cost: | 1.83 |\n| Billed Cost: | $0.00 |\n", None),
    ]
    ng = 0
    for name, txt, want in cases:
        got = parse(txt)
        ok = (got is None and want is None) or (
            got is not None and want is not None
            and all(abs(a - b) < 1e-9 for a, b in zip(got, want)))
        print(f"  {'✓' if ok else '✗'} {name}\n      → {got}（期待 {want}）")
        ng += 0 if ok else 1
    print("\n✓ 物差しは正しい。" if not ng else f"\n🔴 {ng}件ずれている。信じてはいけない。")
    return 1 if ng else 0


def main(est=0.0):
    got, raw = summary()
    if got is None:
        print("🔴 請求情報を読めなかったので**止める**。")
        print(f"   {raw}")
        print("   → ワークスペースが無効化されている可能性がある。")
        print("      https://modal.com/settings/torotorotolo/usage を見ること。")
        return 1

    # 🔴 `or 0.0` で埋めない。summary() は1つでも読めなければ None を返して
    #    上で止まる作りにしたので、ここに来たときは3つとも読めている。
    #    （前は None を 0.0 に化かしていて、それが門番を無効にしていた）
    used, credits, billed = got
    avail = CREDITS_USD - used            # 残っているクレジット
    room = BUDGET_USD * MARGIN - used     # 予算まであとどれだけ使えるか

    print(f"  使用量        ${used:.2f}")
    print(f"  充当クレジット ${credits:.2f}")
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
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    e = 0.0
    for i, a in enumerate(sys.argv):
        if a == "--est" and i + 1 < len(sys.argv):
            e = float(sys.argv[i + 1])
        elif a.startswith("--est="):
            e = float(a.split("=", 1)[1])
    sys.exit(main(e))
