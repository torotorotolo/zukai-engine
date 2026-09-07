# -*- coding: utf-8 -*-
"""焼く前の門番を**1コマンドで全部**回す（2026-09-07 新設・工程の新設計 §9-8）。

■ なぜ要るか
    「単発で回す門番は忘れられる」＝規則があっても呼ばれない
    （[[feedback-gates-blind-spot-is-the-scan-direction]]）。
    **⑤b の出口は「これが全部 0件」**。0件になってから検品画像を焼く。

■ 🔴 守っていること（過去に踏んだ罠）
    1. **`| tee` を使わない。** パイプでつなぐと失敗が exit 0 に化ける
       （[[feedback-pipes-mask-exit-codes]]）。出力はこの中で受け取って自分で出す
    2. **`&&` でつながない。** 途中で止まると後ろの門番が1本も走らない
       （[[project-psych-channel]]）。**全部走らせてから**いちばん重い exit を返す
    3. **子プロセスの文字コードを固定する。** Windows の既定 cp932 だと `✓` を出す瞬間に
       `UnicodeEncodeError` で落ち、**出力が読めないまま「通った」ことになる**
       （[[feedback-verify-your-own-instrument]]）。`PYTHONIOENCODING=utf-8` を渡す
    4. **落ちた門番を「0件」と数えない**（fail closed）。落ちたら exit の最悪値に混ぜる

■ 出すもの
    門番ごとに **🔴 の行**と**最後の2行**（要約）だけ。全文は各コマンドを直接回す。

■ 使い方
    python tools/qa_all.py            # 全部回す
    python tools/qa_all.py --list     # 何を回すかだけ見る
    python tools/qa_all.py --full     # 各門番の全文も出す
    python tools/qa_all.py --selftest # 物差しの検算
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
PY = sys.executable

# 🔴 ⑤b の出口。**この順で全部 0件**になってから検品画像を焼く
GATES = [
    ("layout", ["tools/check_layout.py"], "文字の位置（枠外・重なり・帯）"),
    ("echo", ["tools/check_echo.py"], "図がナレーションの複写になっていないか"),
    ("dup", ["tools/check_dup.py"], "同じ画面で同じ言葉を二度出していないか"),
    ("box", ["tools/check_box.py"], "枠の内側が空いていないか"),
    ("color", ["tools/check_color.py"], "地との比と色どうしの離れ方"),
    ("slide", ["tools/check_slide.py"], "焼き込みの文字×切り方（G-09/10/13/14/15）"),
    ("blank", ["tools/check_blank.py"], "切り出し窓が空っぽでないか"),
    ("footage", ["tools/footage.py", "fetch", "--check"], "until＝ショットの終わり"),
]


def worst_of(codes):
    """🔴 いちばん重い exit を返す。**1本でも落ちたら 0 にしない。**"""
    return max(codes) if codes else 0


def run(cmd):
    """1本回して (exit, 出力) を返す。🔴 落ちても 0 で埋めない。"""
    env = dict(os.environ)
    # ⚠️ 子の既定が cp932 だと ✓ を出す瞬間に落ちる。落ちた出力は誰も読まない
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    t0 = time.time()
    r = subprocess.run([PY, *cmd], cwd=HERE, capture_output=True, env=env)
    txt = (r.stdout + b"\n" + r.stderr).decode("utf-8", errors="replace").strip()
    return r.returncode, txt, time.time() - t0


def main(full=False):
    print(f"■ 焼く前の門番 {len(GATES)}本（🔴 の行と要約だけ。全文は各コマンドを直接）")
    worst, rows = 0, []
    for name, cmd, what in GATES:
        rc, txt, sec = run(cmd)
        lines = [l for l in txt.splitlines() if l.strip()]
        red = [l for l in lines if l.lstrip().startswith("🔴")]
        crashed = rc not in (0, 1, 2) or "Traceback" in txt
        worst = worst_of([worst, 3 if crashed else rc])
        mark = "🔴" if crashed else ("✓" if rc == 0 else "🔴")
        print(f"\n{mark} {name:8} exit {rc}  {sec:5.1f}秒  {what}")
        if crashed:
            print("   🔴 門番そのものが落ちた（0件と数えない）")
            for l in lines[-6:]:
                print(f"   | {l[:150]}")
        else:
            for l in (lines if full else red[:12]):
                print(f"   {l[:170]}")
            if not full and len(red) > 12:
                print(f"   …ほか 🔴 {len(red) - 12}行（`python {' '.join(cmd)}` で全部）")
            for l in lines[-2:]:
                print(f"   | {l[:170]}")
        rows.append((name, rc, len(red), crashed))

    print("\n" + "─" * 60)
    ng = [r for r in rows if r[1] != 0 or r[3]]
    for name, rc, nred, crashed in rows:
        print(f"  {'🔴' if (rc or crashed) else '✓'} {name:8} exit {rc}"
              f"  🔴 {nred}行{'  ← 門番が落ちた' if crashed else ''}")
    if ng:
        print(f"🔴 門番 {len(ng)}／{len(rows)} 本が通っていない。"
              f"**通るまで検品画像を焼かない**（exit {worst}）")
    else:
        print(f"✓ 門番 {len(rows)}本すべて 0件。検品画像を焼いてよい"
              f"（`python tools/qa_sheet.py <slug>` の前に build → Actions で r01）")
    return worst


def selftest():
    """物差しの検算。**外に出る副作用を出さない**（門番は1本も回さない）。"""
    ok = True

    def say(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '🔴'} {msg}")

    missing = [c[0] for _, c, _ in GATES if not (HERE / c[0]).exists()]
    say(not missing, f"門番 {len(GATES)}本のファイルが全部ある"
                     + (f"（無い: {missing}）" if missing else ""))
    say(len({n for n, *_ in GATES}) == len(GATES), "名前が重なっていない")

    # 🔴 落ちた門番を 0件と数えない（わざと落ちる子を回す）
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "boom.py"
        bad.write_text("raise RuntimeError('わざと落とす')\n", encoding="utf-8")
        rc, txt, _ = run([str(bad)])
        say(rc != 0 and "Traceback" in txt, f"落ちる子は exit {rc}＋Traceback で返る")
        # cp932 で落ちない（✓ を出す子）
        uni = Path(td) / "uni.py"
        uni.write_text("print('✓ 通った')\n", encoding="utf-8")
        rc2, txt2, _ = run([str(uni)])
        say(rc2 == 0 and "✓ 通った" in txt2,
            "子の出力が utf-8 で受け取れる（cp932 で落ちない）")
        # 🔴 exit 2（footage の until 無し）が exit 1 より重く扱われる
        two = Path(td) / "two.py"
        two.write_text("import sys; print('🔴 x'); sys.exit(2)\n", encoding="utf-8")
        rc3, _, _ = run([str(two)])
        say(max(0, 1, rc3) == 2, f"exit 2 は exit 1 より重い（max で {max(0, 1, rc3)}）")

        # 🔴 パイプ（`| tee`）も `&&` も、**シェルを通さなければ書けない**。
        #    ⚠️ ここは最初「ソースに tee / shell=True と書いてないか」で見ていたが、
        #       **自分の説明文に鳴って2回続けて赤になった**（2026-09-07）。
        #       字面ではなく**ふるまい**で測る：引数の中の `|` と `&&` が
        #       解釈されずそのまま子に届けば、シェルは通っていない。
        argv = Path(td) / "argv.py"
        argv.write_text("import sys; print('ARGS', sys.argv[1:])\n", encoding="utf-8")
        rc4, txt4, _ = run([str(argv), "a | tee b", "x && y"])
        say(rc4 == 0 and "a | tee b" in txt4 and "x && y" in txt4,
            "引数はシェルを通らずそのまま届く（`| tee` で exit が化ける余地も "
            "`&&` で止まる余地も無い）")
    say(worst_of([0, 1, 0]) == 1 and worst_of([0, 1, 2]) == 2
        and worst_of([0, 0]) == 0 and worst_of([]) == 0,
        "いちばん重い exit を返す（2 > 1 > 0・1本でも落ちたら 0 にしない）")
    print("  " + ("✓ 物差しは正しい" if ok else "🔴 物差しに落ちた"))
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    if "--list" in sys.argv:
        print(f"■ 焼く前の門番 {len(GATES)}本")
        for name, cmd, what in GATES:
            print(f"   {name:8} python {' '.join(cmd):42} {what}")
        sys.exit(0)
    sys.exit(main(full="--full" in sys.argv))
