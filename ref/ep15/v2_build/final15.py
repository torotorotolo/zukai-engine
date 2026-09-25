# -*- coding: utf-8 -*-
"""15本目④'：第2版を組む → 門番 → 機械の数え・台帳 → gates.md に書いて §0 に差す → 組み直す → もう一度回して同じか確かめる。
14本目 ref/ep14/v2_build/final.sh を Python に写した（Git Bash の PATH が壊れていることがあるため）。
    python ref/ep15/v2_build/final15.py
道具（tools/）は1文字も変えない。回すもの：
  cs   tools/check_script.py（そのまま＝聞き役の「？」で E が出る。本線の道具はまだ聞き役を知らない）
  csq  聞き役を知る差し替え実行（読み込んだ中で①`Q: ` を字数から外す ②「？」「！」で終わる聞き役の行を文の終わりと見る）
  csn  14本目⑤a の作業ツリーの check_script.py（91e8f76＝聞き役の印を知る次の版。冒頭の秒は行間と決め所の余白まで数える）＝読むだけ
  cf   tools/check_facts.py（原文＝ref/ep15/src/ep15_pages.txt）
  df   tools/check_script_diff.py daihon_v1.md daihon_v2.md
  mech ref/ep15/v2_build/mech15.py（roles.tsv＝v2_build のもの）
  ledger ref/ep15/v2_build/ledger.py（所見の台帳）
終了コード 0＝組めて2周同じ / 2＝組み損ない / 3＝2周で出力が違う
"""
import os, re, subprocess, sys, filecmp
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("C:/Users/konar/Desktop/zukai-engine")
B = ROOT / "ref/ep15/v2_build"
O = B / "out"
O.mkdir(exist_ok=True)
NEXT_CS = Path("C:/Users/konar/Desktop/zukai-engine-ep14a5/tools/check_script.py")
V1, V2 = "ref/ep15/daihon_v1.md", "ref/ep15/daihon_v2.md"
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
QAWARE = r'''
import sys, re
sys.path.insert(0, 'tools'); import check_script as cs
_c = cs.clean
cs.clean = lambda l: re.sub(r'^Q:\s', '', _c(l))
src = open(sys.argv[1], encoding='utf-8').read()
src = re.sub(r'^(> Q: .*[？！])$', r'\1、', src, flags=re.M)
sys.exit(1 if cs.report(cs.parse(src)) else 0)
'''

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
        ("check_script（そのまま）", "cs", [sys.executable, "tools/check_script.py", V2]),
        ("check_script（聞き役を知る差し替え実行）", "csq", [sys.executable, "-c", QAWARE, V2]),
        ("check_script（14本目⑤aの次の版 91e8f76・読むだけ）", "csn", [sys.executable, str(NEXT_CS), V2]),
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
    cs = r("g1_cs.txt").split("\n")
    qpat = "途中の行が句点でも読点でも終わっていない: Q:"
    n_q = sum(1 for l in cs if qpat in l)
    rest = [l for l in cs if qpat not in l]
    mech = r("g1_mech.txt")
    sec = lambda k: mech.split(f"## {k} ", 1)[1].split("\n## ", 1)[0] if f"## {k} " in mech else ""
    out = [
        "### 0-1. 門番（④'が自分で回した。`tools/` は1文字も変えていない）",
        "`python ref/ep15/v2_build/final15.py`（組む → 門番 → §0 に差す → 組み直す → もう一度回して同じか確かめる）の終了コード：",
        "```", r("g1_rc.txt"), "```", "",
        f"**check_script.py ref/ep15/daihon_v2.md（そのまま）**＝下の枠のほかに、聞き役の行の「途中の行が句点でも読点でも終わっていない: Q: …？」が **{n_q}件**（全部「？」で終わる聞き役の質問＝本線の門番が聞き役をまだ知らないため。14本目⑤a の次の版 `91e8f76` で直る）",
        "```"] + rest + ["```", "",
        "**聞き役を知る差し替え実行**（読み込んだ中で①`Q: ` を字数から外す ②「？」「！」で終わる聞き役の行を文の終わりと見る、の2点だけ差し替え＝14本目④'と同じ）",
        "```", r("g1_csq.txt"), "```", "",
        "**14本目⑤a の次の版の check_script.py**（作業ツリー `zukai-engine-ep14a5`・`91e8f76`＝聞き役の印を知る・`冒頭:` は行間と決め所の余白まで数える＝mech15 §8 と同じ式）",
        "```", r("g1_csn.txt"), "```", "",
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
for k in ["cs", "csq", "csn", "cf", "df", "mech", "ledger", "rc"]:
    a, b = O / f"g1_{k}.txt", O / f"g2_{k}.txt"
    if not a.exists() and not b.exists():
        continue
    ok = a.exists() and b.exists() and filecmp.cmp(a, b, shallow=False)
    same &= ok
    print(("same " if ok else "DIFF ") + k)
print(b2.strip())
print((O / "g2_rc.txt").read_text(encoding="utf-8").strip())
sys.exit(0 if same else 3)
