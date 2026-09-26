# -*- coding: utf-8 -*-
"""16本目④'：第2版を組む → 門番 → 機械の数え・台帳 → gates.md に書いて §0 に差す → 組み直す → もう一度回して同じか確かめる。
15本目 ref/ep15/v2_build/final15.py を16本目に写した。道具（tools/）は1文字も変えない。
    python ref/ep16/v2_build/final16.py
回すもの：
  cs   tools/check_script.py ref/ep16/daihon_v2.md（🔴 尺の E は既知の誤り＝ElevenLabs の定数・ルール §5a-28b。形の検査を読む）
  cf   tools/check_facts.py（原文＝ref/ep16/src/ep16_pages.txt）
  df   tools/check_script_diff.py daihon_v1.md daihon_v2.md
  mech ref/ep16/v2_build/mech16.py（尺はゆっくりの式・聞き役は tools/check_listener.py の judge()・roles.tsv＝v2_build）
  cts  Vault Resources/事故検証ch-案C見本/count_text_screens.py --gate（文字だけ2割・3連続なし）
  ledger ref/ep16/v2_build/ledger.py（所見の台帳）
⚠️ tools/check_listener.py そのものは回さない＝el_script.SLUG（いま ep14）の音の台本を読む道具で、16本目の台本を渡す口が無い
終了コード 0＝組めて2周同じ / 2＝組み損ない / 3＝2周で出力が違う
"""
import os, subprocess, sys, filecmp
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
B = ROOT / "ref/ep16/v2_build"
O = B / "out"
O.mkdir(exist_ok=True)
V1, V2 = "ref/ep16/daihon_v1.md", "ref/ep16/daihon_v2.md"
CTS = "C:/Users/konar/Documents/Obsidian Vault/Resources/事故検証ch-案C見本/count_text_screens.py"
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

# 役割表＝係ごとの roles_G*.tsv をつなぐ（係が出していない章は第1版の表 v1_build/roles.tsv の行を使う）
CH = {"G1": ("c1", "c2"), "G2": ("c3", "c4"), "G3": ("c5", "c6"), "G4": ("c7", "c8"), "G5": ("c9", "ca"), "G6": ("cb",)}
v1rows = [l for l in (ROOT / "ref/ep16/v1_build/roles.tsv").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
rows = []
for g, chs in CH.items():
    f = B / f"roles_{g}.tsv"
    src = [l for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")] if f.exists() else v1rows
    rows += [l for l in src if l.split("\t")[0][:2] in chs]
head = "# 16本目④' 第2版：聞き役（行頭 `> Q: `）の役割。cid<TAB>役割<TAB>聞き役の文（印を除く）。mech16.py が tools/check_listener.py の judge() で台本と1行ずつ突き合わせる\n"
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
        ("check_script", "cs", [sys.executable, "tools/check_script.py", V2]),
        ("check_facts", "cf", [sys.executable, "tools/check_facts.py", V2, "ref/ep16/src/ep16_pages.txt"]),
        ("check_script_diff", "df", [sys.executable, "tools/check_script_diff.py", V1, V2]),
        ("mech16", "mech", [sys.executable, str(B / "mech16.py"), V2, "--roles", str(B / "roles.tsv")]),
        ("count_text_screens --gate", "cts", [sys.executable, CTS, V2, "--gate"]),
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
    head = mech.split("\n## ", 1)[0]
    out = [
        "### 0-1. 門番（④'が自分で回した。`tools/` は1文字も変えていない）",
        "`python ref/ep16/v2_build/final16.py`（組む → 門番 → §0 に差す → 組み直す → もう一度回して同じか確かめる）の終了コード：",
        "```", r("g1_rc.txt"), "```", "",
        "**check_script.py ref/ep16/daihon_v2.md**（🔴 尺の E は既知の誤り＝`est_sec` が ElevenLabs の定数のまま・ルール §5a-28b。尺はゆっくりの式＝下の mech16 で測る。「冒頭:」の秒も同じ理由で使わない）",
        "```", r("g1_cs.txt"), "```", "",
        "**check_facts.py**（抜粋）", "```"] + [l for l in r("g1_cf.txt").split("\n") if l.startswith(("原文", "決め所", "数字", "   "))] + ["```", "",
        "**check_script_diff.py daihon_v1.md daihon_v2.md**（変わった中身の列は省いた）", "```"] + [l for l in r("g1_df.txt").split("\n") if not l.startswith("  変わった中身")] + ["```", "",
        "**count_text_screens.py --gate**（文字だけの画面＝パネル・決め所・文字の頁＝2割まで・3カット以上続けない＝ルール 5b-79）", "```", r("g1_cts.txt"), "```", "",
        "**mech16.py**（尺＝句読点なし÷380・ゆっくりの式）", "```", head.strip(), "```", "",
        "### 0-2. 聞き役（最小限の聞き役・ルール §4-15）",
        "`mech16.py` §7＝`tools/check_listener.py` の `judge()` をそのまま呼び、秒だけ ÷380 の式で渡した（役割＝`ref/ep16/v2_build/roles.tsv`・台本と1行ずつ突き合わせ・漢数字も数字として止める）",
        "```", sec("7").strip(), "```", "",
        "### 0-3. 冒頭の秒・章ごと・文字だけの連続・見る向き",
        # 見出しを「## 」で始めない（mech16 の節の区切りに読まれて2周目で結果が変わる）
        "```", "〔mech §8〕 " + sec("8").strip(), "", "〔mech §9〕 " + sec("9").strip(), "", "〔mech §10〕 " + sec("10").strip(), "", "〔mech §11〕 " + sec("11").strip(), "```", "",
        "### 0-4. タイトル（4'-8）・内部の数字（4'-17）・使わない言い方・文と行・出典の札",
        "```", "〔mech §1〕 " + sec("1").strip(), "", "〔mech §5〕 " + (sec("5").strip() or "0件"), "", "〔mech §6〕 " + (sec("6").strip() or "0件"),
        "", "〔mech §4〕 " + sec("4").strip(), "", "〔mech §2〕 " + sec("2").strip(), "", "〔mech §3〕 " + sec("3").strip(), "```", "",
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
for k in ["cs", "cf", "df", "mech", "cts", "ledger", "rc"]:
    a, b = O / f"g1_{k}.txt", O / f"g2_{k}.txt"
    if not a.exists() and not b.exists():
        continue
    ok = a.exists() and b.exists() and filecmp.cmp(a, b, shallow=False)
    same &= ok
    print(("same " if ok else "DIFF ") + k)
print(b2.strip())
print((O / "g2_rc.txt").read_text(encoding="utf-8").strip())
sys.exit(0 if same else 3)
