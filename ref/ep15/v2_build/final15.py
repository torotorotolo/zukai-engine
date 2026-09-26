# -*- coding: utf-8 -*-
"""15本目④'：第2版を組む → 門番 → 機械の数え・台帳 → gates.md に書いて §0 に差す → 組み直す → もう一度回して同じか確かめる。
14本目 ref/ep14/v2_build/final.sh を Python に写した（Git Bash の PATH が壊れていることがあるため）。
    python ref/ep15/v2_build/final15.py
道具（tools/）は1文字も変えない。回すもの：
  cs   tools/check_script.py（09-26 本線 633f178 から聞き役を知る版＝14本目⑤a の 91e8f76。冒頭の秒は行間と決め所の余白まで数える）
       ⚠️ ④'のころの csq（差し替え実行）・csn（作業ツリー ep14a5 の次の版）は 15本目⑤a-1 で外した＝cs が同じ版になったため。
          csq の「？」→「？、」の差し替えは、次の版の「話者が替わる前の行は。？！で閉じる」に当たって偽の E を出す
  cf   tools/check_facts.py（原文＝ref/ep15/src/ep15_pages.txt）
  df   tools/check_script_diff.py daihon_v1.md daihon_v2.md
  mech ref/ep15/v2_build/mech15.py（roles.tsv＝v2_build のもの）
  ledger ref/ep15/v2_build/ledger.py（所見の台帳）
終了コード 0＝組めて2周同じ / 2＝組み損ない / 3＝2周で出力が違う
"""
import os, re, subprocess, sys, filecmp
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
# この作業ツリーの根（15本目⑤a-1：本線のフォルダの直書きを外した＝別の作業ツリーから回しても本線を読み書きしない。ルール 5a-23）
ROOT = Path(__file__).resolve().parents[3]
B = ROOT / "ref/ep15/v2_build"
O = B / "out"
O.mkdir(exist_ok=True)
V1, V2 = "ref/ep15/daihon_v1.md", "ref/ep15/daihon_v2.md"
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

# 役割表＝係ごとの roles_G*.tsv をつなぐ
head = "# 15本目④' 第2版：聞き役（行頭 `> Q: `）の役割。cid<TAB>役割<TAB>聞き役の文（印を除く）。mech15.py が台本と1行ずつ突き合わせる\n"
rows = []
for f in sorted(B.glob("roles_G*.tsv")):
    rows += [l for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
(B / "roles.tsv").write_text(head + "\n".join(rows) + "\n", encoding="utf-8")


def run(cmd):
    p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout + ("\n[stderr]\n" + p.stderr if p.stderr.strip() else "")


def build(tag):
    rc, out = run([sys.executable, str(B / "build_v2.py")])
    (O / f"{tag}.txt").write_text(out, encoding="utf-8")
    if rc:
        print(out); sys.exit(2)
    return out


def gates(pre):
    R = [
        ("check_script（聞き役を知る版＝本線 633f178）", "cs", [sys.executable, "tools/check_script.py", V2]),
        ("check_facts", "cf", [sys.executable, "tools/check_facts.py", V2, "ref/ep15/src/ep15_pages.txt"]),
        ("check_script_diff", "df", [sys.executable, "tools/check_script_diff.py", V1, V2]),
        ("mech15", "mech", [sys.executable, str(B / "mech15.py"), V2, "ref/ep14/v2_build/titles.json"]),
    ]
    if (B / "check_result.json").exists():
        R.append(("ledger", "ledger", [sys.executable, str(B / "ledger.py")] + (["--review"] if (B / "review_result.json").exists() else []) + ["--items"]))
    rcs = []
    for label, k, cmd in R:
        rc, out = run(cmd)
        (O / f"{pre}_{k}.txt").write_text(out, encoding="utf-8")
        rcs.append(f"{label} exit={rc}")
    (O / f"{pre}_rc.txt").write_text("\n".join(rcs) + "\n", encoding="utf-8")


def compose():
    r = lambda n: (O / n).read_text(encoding="utf-8").strip("\n") if (O / n).exists() else ""
    mech = r("g1_mech.txt")
    sec = lambda k: mech.split(f"## {k} ", 1)[1].split("\n## ", 1)[0] if f"## {k} " in mech else ""
    out = [
        "### 0-1. 門番（④'が自分で回した。`tools/` は1文字も変えていない。15本目⑤a-1 で回し直した＝下の注）",
        "`python ref/ep15/v2_build/final15.py`（組む → 門番 → §0 に差す → 組み直す → もう一度回して同じか確かめる）の終了コード：",
        "```", r("g1_rc.txt"), "```", "",
        "**check_script.py ref/ep15/daihon_v2.md**（聞き役を知る版＝14本目⑤a の `91e8f76` が 09-26 に本線 `633f178` へ入った。印 `Q: ` を字数に数えない・聞き役の「？」「！」で文を閉じてよい・`冒頭:` は行間と決め所の余白まで数える＝mech15 §8 と同じ式）。"
        "⚠️ ④'のころは本線の道具が聞き役を知らず、「そのまま」（聞き役の「？」で E）・差し替え実行・作業ツリー `ep14a5` の次の版の3通りを並べていた＝15本目⑤a-1 で1本にした（本文は1文字も変えていない）",
        "```", r("g1_cs.txt"), "```", "",
        "**check_facts.py**（抜粋）", "```"] + [l for l in r("g1_cf.txt").split("\n") if l.startswith(("原文", "決め所", "数字", "   "))] + ["```", "",
        "**check_script_diff.py daihon_v1.md daihon_v2.md**（変わった中身の列は省いた）", "```"] + [l for l in r("g1_df.txt").split("\n") if not l.startswith("  変わった中身")] + ["```", "",
        "### 0-2. 聞き役（最小限の聞き役・ルール §4-15）",
        "`python ref/ep15/v2_build/mech15.py ref/ep15/daihon_v2.md` の §7（秒は check_script の③と同じ式・印 `Q: ` を除く・扉8枚も数える・役割＝`ref/ep15/v2_build/roles.tsv`）",
        "```", sec("7").split("\n   Q ")[0].strip(), "```",
        "目安＝行の10〜15%／1分に1.5〜2回／空き90秒まで／質問5割・まとめ2〜3割・反応2割まで／冒頭15〜45秒に1問／数字を言う行0（聞き役の行は `roles.tsv` とこの版の本文で1行ずつ突き合わせた＝表に無い行・台本に無い行・「そう。」で受けないまとめが出れば上に ⚠️ で出る）", "",
        "### 0-3. 冒頭の秒・文・章ごと",
        # 見出しを「## 」で始めない（mech15 §5 の grep が「## 」を節の区切りに読むため、2周目で結果が変わる）
        "```", "〔mech §8〕 " + sec("8").strip(), "", "〔mech §4〕 " + sec("4").strip(), "", "〔mech §9〕 " + sec("9").strip(), "", "〔mech §10〕 " + sec("10").strip(), "```", "",
        "### 0-4. タイトル（4'-8）と内部の数字（4'-17）", "```", sec("1").strip(), "```", "```", sec("5").strip() or "（該当なし）", "```", "",
    ]
    led = r("g1_ledger.txt")
    if led:
        out += ["### 0-5. 所見の台帳（`ledger.py` が `check_result.json`・`changes_G*.md`・`decisions.md` から組んだ＝手で写していない）", "", led, ""]
    (B / "gates.md").write_text("\n".join(out) + "\n", encoding="utf-8")


gm = B / "gates.md"
if gm.exists():
    gm.unlink()
build("b1")
gates("g1")
compose()
b2 = build("b2")
gates("g2")
same = True
for k in ["cs", "cf", "df", "mech", "ledger", "rc"]:
    a, b = O / f"g1_{k}.txt", O / f"g2_{k}.txt"
    if not a.exists() and not b.exists():
        continue
    ok = a.exists() and b.exists() and filecmp.cmp(a, b, shallow=False)
    same &= ok
    print(("same " if ok else "DIFF ") + k)
print(b2.strip())
print((O / "g2_rc.txt").read_text(encoding="utf-8").strip())
sys.exit(0 if same else 3)
