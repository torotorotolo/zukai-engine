# -*- coding: utf-8 -*-
"""🔴 無料枠を絶対に超えないための門番。

■ 考え方
  「気をつける」では守れないので、**Modalを呼ぶ前に必ずここを通す**設計にする。
  見積もりが上限を1セントでも超えたら SystemExit で止まる。通らなければ何も起きない。

■ 二重の上限
  1. CAP_USD          … このプロジェクトで使ってよい総額（既定 $5.00）
                        Modalの無料枠 $30/月 の**6分の1**に置いてある。
                        ここを使い切っても無料枠にはまだ $25 残る。
  2. CAP_PER_RUN_USD  … 1回の実行で使ってよい額（既定 $1.00）
                        暴走したジョブが一撃で枠を溶かすのを防ぐ。

■ 見積もりは必ず「多め」に出す
  - コンテナ起動（イメージ展開・Blender起動）に実測40〜90秒かかる。
    これも課金対象なので OVERHEAD_SEC=120 を必ず足す（実測より多めに置く）。
  - レンダ時間は実測値の 1.5倍で見る（機体差が実測±20%あるため）。
  → 「予想より安く済む」方向にしか外れない。

■ 台帳
  b3d/spend.json に、実行ごとの見積もりと実測を追記する。
  ⚠️ この台帳は**このリポジトリから実行したぶんだけ**を数える。
     Modalの請求そのものではないので、月に一度は
     https://modal.com/settings/usage で実際の残高を見ること。
"""
import json
import os
import pathlib

# ── 上限（ここを変えるとき以外は触らない）──────────────────────
# 🔴 2026-08-02 再訂正：**無料クレジットは $30/月で正しい。**
#    2026-08-01 にここを $1.00 へ書き換えたが、**それが誤り**だった。
#    一次情報3つが $30 で一致する（modal.com/pricing・/signup・/llms.txt）。
#
#    ではダッシュボードで見えた $1 は何か ＝ **支出上限（Workspace budget）**。
#      docs/guide/budgets:「The maximum budget you can set depends on
#        **prior successful charges** for the Workspace.」
#      docs/guide/billing:「you must have a payment method on file in order to use Modal.」
#    ＝ 支払い方法が未登録だと上限が $1 に抑えられ、**$30 は付いていても使えない**。
#    2026-08-02、事故検証の本編がレイヤー 650/1188 で `workspace is disabled` に
#    なって止まったのはこれ。**枠切れではなく上限切れ。**
#
# ⚠️ **超過しても Modal は止めてくれない**（閾値を超えると自動請求に化ける）。
#    だからこの門番は $30 に合わせて上げない。**意図的にずっと内側**に置く。
#    決め方は「無料枠がいくらか」ではなく「**事故ってもこの額しか出ない**」。
FREE_CREDIT_USD = 30.00     # Modal Starter の月次無料クレジット（公式・毎月リセット）
CAP_USD = 5.00              # 月の総額上限。無料枠の 1/6。使い切っても $25 残る
CAP_PER_RUN_USD = 1.00      # 1回の実行の上限（本編1本 約$0.25／プレビュー1巡 約$0.03）

OVERHEAD_SEC = 120          # コンテナ起動などの固定費（多めに置く）
SAFETY = 1.5                # レンダ時間の見積もり係数（機体差±20%を吸収）

# $/秒（Modal 公式価格。時給を3600で割った値）
PRICE_PER_SEC = {
    "T4": 0.59 / 3600,
    "L4": 0.80 / 3600,
    "A10G": 1.10 / 3600,
    "L40S": 1.95 / 3600,
    "A100": 2.10 / 3600,
}

LEDGER = pathlib.Path(__file__).with_name("spend.json")


def _load():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    # 2026-08-01 の切り分け（EEVEE/Cycles/GPU比較/デノイズ）の実績を初期値に入れてある
    # 🔴 初期値はダッシュボードの実測値。自前の概算を信じない。
    return {"spent_usd": 0.45, "runs": [
        {"label": "2026-08-01 実測（ダッシュボード Usage $0.45）", "usd": 0.45}
    ]}


def _save(d):
    LEDGER.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def estimate(gpu: str, frames: int, sec_per_frame: float, runs: int = 1) -> float:
    """この実行にかかる額を、多めに見積もって返す。"""
    per_sec = PRICE_PER_SEC.get(gpu)
    if per_sec is None:
        raise SystemExit(f"[budget] 単価の分からないGPUです: {gpu}")
    seconds = (frames * sec_per_frame * SAFETY + OVERHEAD_SEC) * runs
    return seconds * per_sec


def check(gpu: str, frames: int, sec_per_frame: float, label: str,
          runs: int = 1) -> float:
    """🔴 Modalを呼ぶ前に必ずこれを通す。上限を超えるなら実行せずに止まる。"""
    d = _load()
    est = estimate(gpu, frames, sec_per_frame, runs)
    spent = d["spent_usd"]

    print("┌" + "─" * 60)
    print(f"│ 【課金の見積もり】{label}")
    print(f"│   GPU {gpu} / {frames}コマ × {sec_per_frame:.2f}秒 × 安全係数{SAFETY}")
    print(f"│   ＋ コンテナ起動 {OVERHEAD_SEC}秒 × {runs}回")
    print(f"│   今回の見込み : ${est:.4f}（約¥{est * 160:.1f}）")
    print(f"│   これまで     : ${spent:.4f}")
    print(f"│   合計         : ${spent + est:.4f} / 上限 ${CAP_USD:.2f}")
    left = FREE_CREDIT_USD - spent - est
    print(f"│   無料枠の残り : 約 ${left:.3f} / ${FREE_CREDIT_USD:.2f}"
          f"{'  ⚠️ 残り僅か' if left < 0.15 else ''}")
    print("└" + "─" * 60)

    if est > CAP_PER_RUN_USD:
        raise SystemExit(
            f"[budget] 中止：1回の上限 ${CAP_PER_RUN_USD:.2f} を超えます"
            f"（見込み ${est:.4f}）。frames か sec_per_frame を見直してください。")
    if spent + est > CAP_USD:
        raise SystemExit(
            f"[budget] 中止：総額の上限 ${CAP_USD:.2f} を超えます"
            f"（これまで ${spent:.4f} ＋ 今回 ${est:.4f}）。")
    return est


def record(gpu: str, actual_sec: float, label: str, est: float = 0.0):
    """実行後に、実際にかかった秒数から実額を台帳へ足す。"""
    d = _load()
    per_sec = PRICE_PER_SEC.get(gpu, 0.0)
    usd = (actual_sec + OVERHEAD_SEC) * per_sec
    d["spent_usd"] = round(d["spent_usd"] + usd, 6)
    d["runs"].append(dict(label=label, gpu=gpu, sec=round(actual_sec, 1),
                          usd=round(usd, 6), est=round(est, 6)))
    _save(d)
    print(f"[budget] 実績 ${usd:.4f}（見込み ${est:.4f}）"
          f" / 累計 ${d['spent_usd']:.4f} / 上限 ${CAP_USD:.2f}"
          f" / 無料枠の残り 約${FREE_CREDIT_USD - d['spent_usd']:.2f}")
    return usd


def status():
    d = _load()
    print(f"累計 ${d['spent_usd']:.4f} / 上限 ${CAP_USD:.2f} "
          f"/ 無料枠の残り 約${FREE_CREDIT_USD - d['spent_usd']:.2f}")
    for r in d["runs"]:
        print(f"  ${r.get('usd', 0):.4f}  {r.get('label')}")


if __name__ == "__main__":
    status()
