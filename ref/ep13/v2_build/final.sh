#!/bin/sh
# ④'：第2版を組む → 門番3本（＋写真の新方針の差し替え実行）→ 出力を §0-1 に差しこんで組み直す → もう一度回して同じか確かめる
S="C:/Users/konar/AppData/Local/Temp/claude/C--Users-konar-Documents-Obsidian-Vault/a7fd1db9-f3f0-49d2-9a25-17ca9d147913/scratchpad"
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1
cd C:/Users/konar/Desktop/zukai-engine || exit 9
run_gates() {  # $1 = 出力の接頭辞
  python tools/check_script.py --selftest > "$S/$1_st.txt" 2>&1; echo "selftest exit=$?" > "$S/$1_rc.txt"
  python tools/check_script.py ref/ep13/daihon_v2.md > "$S/$1_cs.txt" 2>&1; echo "check_script exit=$?" >> "$S/$1_rc.txt"
  python tools/check_facts.py ref/ep13/daihon_v2.md ref/ep13/src/thy_pages.txt > "$S/$1_cf.txt" 2>&1; echo "check_facts exit=$?" >> "$S/$1_rc.txt"
  python tools/check_script_diff.py ref/ep13/daihon_v1.md ref/ep13/daihon_v2.md > "$S/$1_df.txt" 2>&1; echo "check_script_diff exit=$?" >> "$S/$1_rc.txt"
  python - > "$S/$1_new.txt" 2>&1 <<'EOF'
import sys; sys.path.insert(0,'tools'); import check_script as cs
cs.PHOTO_LO, cs.PHOTO_HI = 0.20, 1.01
cs.report(cs.parse(open('ref/ep13/daihon_v2.md',encoding='utf-8').read()))
EOF
  echo "新方針の差し替え実行 exit=$?" >> "$S/$1_rc.txt"
}
rm -f "$S/gates.md"
python "$S/build_v2.py" > "$S/b1.txt" 2>&1 || { cat "$S/b1.txt"; exit 2; }
run_gates g1
python - "$S" <<'EOF'
import sys, re
S = sys.argv[1]
r = lambda n: open(f"{S}/{n}", encoding="utf-8").read().strip("\n")
cs = "\n".join(l for l in r("g1_cs.txt").split("\n") if not re.match(r"⚠️ W 章 c\d の写真映像", l))
out = ["2026-09-24 に回した（`tools/` は直していない）。終了コード：", "```", r("g1_rc.txt"), "```", "",
       "**check_script.py ref/ep13/daihon_v2.md**（旧方針の定数のまま。章ごとの写真の W 9行は省いた＝新方針では出ない）", "```", cs, "```", "",
       "**新方針（下限20%・上限なし）に定数だけ差し替えて実行**（§0-7 のコマンド）", "```", r("g1_new.txt"), "```", "",
       "**check_facts.py**（抜粋）", "```"]
cf = r("g1_cf.txt").split("\n")
out += [l for l in cf if l.startswith(("原文", "決め所", "数字", "   ")) or "c212" in l] + ["```", "",
       "**check_script_diff.py daihon_v1.md daihon_v2.md**", "```", r("g1_df.txt"), "```", "",
       "**読み方**：写真の E 1件は第1版と同じ理由（`check_script.py` の `PHOTO_LO, PHOTO_HI = 0.45, 0.50` が旧方針のまま＝⑤bの最初に直す）。新方針に差し替えると E 0。"
       "尺は第1版の判定36分30秒 → 上の判定（直しで字が増えた。③の設計は36分23秒・尺の帯は27〜40分で目標36〜37分）。本文の字数は上限（600＋58×192＝11,736字）の5字手前＝⑤aで足すなら同じだけ削る。⑤aで実測の話速が出たら測り直し、40分を超えるなら削る。"
       "冒頭：`c103` の★は35秒台で終わる（46秒より前）。`c104` の「電話1本」の行は40秒台の頭から始まる（第1版 §0 の「46秒より前に電話1本」は、第1版でも c104 の終わりが45.7秒で、行の頭で数えた値だった）。"]
open(f"{S}/gates.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
EOF
python "$S/build_v2.py" > "$S/b2.txt" 2>&1 || { cat "$S/b2.txt"; exit 2; }
run_gates g2
for f in cs cf df new rc; do cmp -s "$S/g1_$f.txt" "$S/g2_$f.txt" && echo "same $f" || echo "DIFF $f"; done
cat "$S/b2.txt"; cat "$S/g2_rc.txt"
