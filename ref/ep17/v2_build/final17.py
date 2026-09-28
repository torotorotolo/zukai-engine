# -*- coding: utf-8 -*-
"""17本目④'：第2版を組む → 門番 → 機械の数え・台帳 → gates.md に書いて §0 に差す → 組み直す → もう一度回して同じか確かめる。
15本目 ref/ep15/v2_build/final15.py を写して17本目に合わせた。道具（tools/）は1文字も変えない。
    python ref/ep17/v2_build/final17.py
回すもの：
  cs   tools/check_script.py（🔴 尺の E は既知の誤り＝ElevenLabs の定数のまま・ルール §5a-28b。判定は mech の ②＝句読点なし÷380）
  cf   tools/check_facts.py（原文＝ref/ep17/src/ep17_pages.txt）
  df   tools/check_script_diff.py daihon_v1.md daihon_v2.md
  mech ref/ep17/v2_build/mech17.py（④の m17.py の数え＋役割表 roles.tsv との1行ずつの突き合わせ）
  cts  Vault Resources/事故検証ch-案C見本/count_text_screens.py --gate（文字だけの画面＝2割まで・3カット以上続けない）
  ti   ref/ep17/v2_build/titles17.py（タイトル案と公開ずみの題の照合）
  priv 内部の数字・メールの grep（ルール 4'-17・公開リポ）
  ledger ref/ep17/v2_build/ledger.py（所見の台帳）
終了コード 0＝組めて2周同じ / 2＝組み損ない / 3＝2周で出力が違う
"""
import os, re, subprocess, sys, filecmp
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
B = ROOT / "ref/ep17/v2_build"
O = B / "out"
O.mkdir(exist_ok=True)
V1, V2 = "ref/ep17/daihon_v1.md", "ref/ep17/daihon_v2.md"
CTS = r"C:/Users/konar/Documents/Obsidian Vault/Resources/事故検証ch-案C見本/count_text_screens.py"
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

# 役割表＝係ごとの roles_G*.tsv をつなぐ（無ければ第1版の表を使う）
head = "# 17本目④' 第2版：聞き役（行頭 `> Q: `）の役割。cid<TAB>役割<TAB>聞き役の文（印を除く）。mech17.py が台本と1行ずつ突き合わせる\n"
rows = []
for f in sorted(B.glob("roles_G*.tsv")):
    rows += [l for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#") and not l.startswith("cid\t")]
if rows:
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


def priv():
    t = (ROOT / V2).read_text(encoding="utf-8")
    # 🔴 この grep 自身の見出し（§0 に差し込まれる）は数えない＝2周目で自分に当たって DIFF になった
    hits = [f"{n}: {l[:80]}" for n, l in enumerate(t.splitlines(), 1)
            if not l.startswith("内部の数字・メールの grep") and re.search(r"維持率|平均視聴|再生回数|再生数|インプレッション|CTR|クリック率|@[A-Za-z0-9_.-]+\.(com|jp)", l)]
    return 1 if hits else 0, "内部の数字・メールの grep（維持率・平均視聴・再生回数・再生数・インプレッション・CTR・クリック率・メール）：" + (f"{len(hits)}件\n" + "\n".join(hits) if hits else "0件")


def gates(pre):
    R = [
        ("check_script", "cs", [sys.executable, "tools/check_script.py", V2]),
        ("check_facts", "cf", [sys.executable, "tools/check_facts.py", V2, "ref/ep17/src/ep17_pages.txt"]),
        ("check_script_diff", "df", [sys.executable, "tools/check_script_diff.py", V1, V2]),
        ("mech17", "mech", [sys.executable, str(B / "mech17.py"), V2, str(B / "roles.tsv")]),
        ("count_text_screens --gate", "cts", [sys.executable, CTS, V2, "--gate"]),
        ("titles17", "ti", [sys.executable, str(B / "titles17.py")]),
    ]
    if (B / "check_result.json").exists():
        R.append(("ledger", "ledger", [sys.executable, str(B / "ledger.py")] + (["--review"] if (B / "review_result.json").exists() else []) + ["--items"]))
    rcs = []
    for label, k, cmd in R:
        rc, out = run(cmd)
        (O / f"{pre}_{k}.txt").write_text(out, encoding="utf-8")
        rcs.append(f"{label} exit={rc}")
    rc, out = priv()
    (O / f"{pre}_priv.txt").write_text(out + "\n", encoding="utf-8")
    rcs.append(f"priv exit={rc}")
    (O / f"{pre}_rc.txt").write_text("\n".join(rcs) + "\n", encoding="utf-8")


def compose():
    r = lambda n: (O / n).read_text(encoding="utf-8").strip("\n") if (O / n).exists() else ""
    # 見出しを「## 」で始めない（台本の節の区切りと取り違えないよう「▼ 」に替える）
    nohash = lambda s: re.sub(r"^## ", "▼ ", s, flags=re.M)
    mech = r("g1_mech.txt")
    sec = lambda k: mech.split(f"## {k}", 1)[1].split("\n## ", 1)[0] if f"## {k}" in mech else ""
    out = [
        "### 0-1. 門番（④'が自分で回した。`tools/` は1文字も変えていない）",
        "`python ref/ep17/v2_build/final17.py`（組む → 門番 → §0 に差す → 組み直す → もう一度回して同じか確かめる）の終了コード：",
        "```", r("g1_rc.txt"), "```", "",
        "**check_script.py ref/ep17/daihon_v2.md**（🔴 尺の E（約51分）は**既知の誤り**＝`est_sec` が ElevenLabs の定数のまま・ルール §5a-28b。判定は下の mech §2 の ②＝句読点なし÷380字/分。`冒頭:` の秒も同じ定数＝mech §7 を見る）",
        "```", r("g1_cs.txt"), "```", "",
        "**check_facts.py**（抜粋）", "```"] + [l for l in r("g1_cf.txt").split("\n") if l.startswith(("原文", "決め所", "数字", "   "))] + ["```", "",
        "**check_script_diff.py daihon_v1.md daihon_v2.md**（変わった中身の列は省いた）", "```"] + [l for l in r("g1_df.txt").split("\n") if not l.startswith("  変わった中身")] + ["```", "",
        "**count_text_screens.py --gate**（文字だけの画面＝2割まで・3カット以上続けない＝§5b-79）", "```", r("g1_cts.txt"), "```", "",
        "### 0-2. 聞き役（最小限の聞き役・ルール §4-15）",
        "`python ref/ep17/v2_build/mech17.py ref/ep17/daihon_v2.md` の §6（m17 の数え＝役割は文の形から推した値）と §6b（人が決めた役割表 `ref/ep17/v2_build/roles.tsv` と本文を1行ずつ突き合わせた値＝こちらが正）",
        "```", nohash("## §6" + sec("§6 聞き役")).strip(), "", nohash("## §6b" + sec("§6b")).strip(), "```",
        "目安＝行の10〜15%／1分に1.5〜2回／空き90秒まで／質問5割・まとめ2〜3割・反応2割まで／冒頭15〜45秒に1問／数字を言う行0／まとめの次の語りは「そう。」", "",
        "### 0-3. 数・尺・形・写真・文字だけの画面・冒頭の秒・使わない語（mech17＝④の m17.py と同じ数え方）",
        "```", nohash("## §1" + sec("§1 数")).strip(), "", nohash("## §2" + sec("§2 尺")).strip(), "```", "",
        nohash("## §3" + sec("§3 章ごと")).strip(), "",
        "```", nohash("## §3b" + sec("§3b 形")).strip(), "", nohash("## §4" + sec("§4 ")).strip(), "", nohash("## §5" + sec("§5 ")).strip(), "",
        nohash("## §7" + sec("§7 ")).strip(), "", nohash("## §8" + sec("§8 ")).strip(), "```", "",
        "### 0-4. タイトル（4'-8＝公開ずみの題と全数照合）と内部の数字（4'-17）", "```", r("g1_ti.txt"), "", r("g1_priv.txt"), "```", "",
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
for k in ["cs", "cf", "df", "mech", "cts", "ti", "priv", "ledger", "rc"]:
    a, b = O / f"g1_{k}.txt", O / f"g2_{k}.txt"
    if not a.exists() and not b.exists():
        continue
    ok = a.exists() and b.exists() and filecmp.cmp(a, b, shallow=False)
    same &= ok
    print(("same " if ok else "DIFF ") + k)
print(b2.strip())
print((O / "g2_rc.txt").read_text(encoding="utf-8").strip())
sys.exit(0 if same else 3)
