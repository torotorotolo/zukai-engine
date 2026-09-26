#!/bin/sh
# 14本目④'：第2版を組む → 門番（check_script そのまま／聞き役を知る差し替え実行・check_facts・check_script_diff）
#            → 機械の数え（mech.py）・台帳（ledger.py）→ gates.md に書いて §0 に差す → 組み直す → もう一度回して同じか確かめる
# 道具（tools/）は1文字も変えない。聞き役を知る実行は、読み込んだ中で2点だけ差し替える（① `Q: ` を字数から外す ②「？」「！」で終わる聞き役の行を文の終わりと見る）
# ⑤a（2026-09-25）：置き場所から数える（本線の直書きだと、別の作業ツリーから回しても本線を読み書きしていた）
B="$(cd "$(dirname "$0")" && (pwd -W 2>/dev/null || pwd))"
O="$B/out"
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1
cd "$B/../../.." || exit 9
mkdir -p "$O"
cat "$B"/roles_G[0-6].tsv | sed '/^\s*$/d' > "$B/roles.tsv"
run_gates() {  # $1 = 出力の接頭辞
  python tools/check_script.py ref/ep14/daihon_v2.md > "$O/$1_cs.txt" 2>&1; echo "check_script（そのまま） exit=$?" > "$O/$1_rc.txt"
  python - > "$O/$1_csq.txt" 2>&1 <<'EOF'
import sys, re
sys.path.insert(0, 'tools'); import check_script as cs
_c = cs.clean
cs.clean = lambda l: re.sub(r'^Q:\s', '', _c(l))
src = open('ref/ep14/daihon_v2.md', encoding='utf-8').read()
src = re.sub(r'^(> Q: .*[？！])$', r'\1、', src, flags=re.M)
cs.report(cs.parse(src))
EOF
  echo "check_script（聞き役を知る差し替え実行） exit=$?" >> "$O/$1_rc.txt"
  python tools/check_facts.py ref/ep14/daihon_v2.md ref/ep14/src/sewol_pages.txt > "$O/$1_cf.txt" 2>&1; echo "check_facts exit=$?" >> "$O/$1_rc.txt"
  python tools/check_script_diff.py ref/ep14/daihon_v1.md ref/ep14/daihon_v2.md > "$O/$1_df.txt" 2>&1; echo "check_script_diff exit=$?" >> "$O/$1_rc.txt"
  python "$B/mech.py" ref/ep14/daihon_v2.md "$B/titles.json" > "$O/$1_mech.txt" 2>&1; echo "mech exit=$?" >> "$O/$1_rc.txt"
  python "$B/ledger.py" --review --items > "$O/$1_ledger.txt" 2>&1; echo "ledger exit=$?" >> "$O/$1_rc.txt"
}
rm -f "$B/gates.md"
python "$B/build_v2.py" > "$O/b1.txt" 2>&1 || { cat "$O/b1.txt"; exit 2; }
run_gates g1
python - "$O" "$B" <<'EOF'
import sys, re
O, B = sys.argv[1], sys.argv[2]
r = lambda n: open(f"{O}/{n}", encoding="utf-8").read().strip("\n")
cs = r("g1_cs.txt").split("\n")
n_q = sum(1 for l in cs if "途中の行が句点でも読点でも終わっていない: Q:" in l)
rest = [l for l in cs if "途中の行が句点でも読点でも終わっていない: Q:" not in l]
mech = r("g1_mech.txt")
sec = lambda k: mech.split(f"## {k} ", 1)[1].split("\n## ", 1)[0]
led = r("g1_ledger.txt")
out = [
 "### 0-1. 門番（④'が2026-09-25に自分で回した。`tools/` は1文字も変えていない）", "終了コード：", "```", r("g1_rc.txt"), "```", "",
 f"**check_script.py ref/ep14/daihon_v2.md（そのまま）**＝下の枠のほかに、聞き役の行の「途中の行が句点でも読点でも終わっていない: Q: …？」が **{n_q}件**（全部「？」で終わる聞き役の質問＝門番が聞き役を知らないため。⑤で道具を直す＝§1-12）", "```"] + rest + ["```", "",
 "**聞き役を知る差し替え実行**（読み込んだ中で①`Q: ` を字数から外す ②「？」「！」で終わる聞き役の行を文の終わりと見る、の2点だけ差し替え）", "```", r("g1_csq.txt"), "```", "",
 "**check_facts.py**（抜粋）", "```"] + [l for l in r("g1_cf.txt").split("\n") if l.startswith(("原文", "決め所", "数字", "   "))] + ["```", "",
 "**check_script_diff.py daihon_v1.md daihon_v2.md**（変わった中身の列は省いた）", "```"] + [l for l in r("g1_df.txt").split("\n") if not l.startswith("  変わった中身")] + ["```", "",
 "**読み方**：E は「聞き役の質問の？」だけ＝差し替え実行で E 0。W 5件＝`cc13`「衝撃」2件は原文「외부충격」の訳語（語りと聞き役「衝撃で、沈んだの？」）・`c605`「5度」`c606`「145度」`c609`「79度」は角度（回す量と方位）＝温度ではない。判定の尺 ① は `PER_CUT`×195 で動かない＝② ③ を見る。`冒頭:` の c105 は 46.0秒より前（ただしこの行は行間と決め所の余白を数えない＝同じ式で全部数えると c105 の終わりは約51秒＝§0-9）", "",
 "### 0-2. 聞き役（最小限の聞き役・ルール §4-15）", "`python ref/ep14/v2_build/mech.py ref/ep14/daihon_v2.md` の §7（秒は check_script の③と同じ式・印 `Q: ` を除く・`ca`〜`cd` の扉も数える）", "```", sec("7").split("\n   Q ")[0].strip(), "```",
 "目安＝行の10〜15%／1分に1.5〜2回／空き90秒まで／質問5割・まとめ2〜3割・反応2割まで／冒頭15〜45秒に1問／数字を言う行0（聞き役の行は `roles.tsv` とこの版の本文で1行ずつ突き合わせた＝表に無い行・台本に無い行が出れば上に出る）", "",
 "### 0-3. 音声（ゆっくり＝抑揚の平らな声で聞き取りやすく）", "```", sec("4").strip(), "```",
 "第1版＝文455・40字超14・最長59字・「った。」の3連続3か所・同じ語尾3字の3連続2か所（同じ数え方＝カットの中で行をつなぎ、句点・？・！と★の行と話者の替わり目で割る。④の §0-3 の「40字超24・最長72字」は割り方が書かれておらず再現できなかった）", "",
 "### 0-4. タイトル（4'-8）と内部の数字（4'-17）", "```", sec("1").strip(), "```", "```", sec("5").strip() or "（該当なし）", "```",
 "**読み方**：タイトル案は3本とも公開ずみ12本の型（つかみ。もう一つの事実、N人が…の真相【事故検証】）と字数（68〜94字）の内（§1-1）。grep に出た行は写真の割合・章の字の割合と、第1版 §4 の「冒頭の数十秒に大きな離脱」＝**チャンネルの内部の数字（維持率・再生数など）は0件**（「離脱」の行は数字が無いので残した）", "",
 "### 0-5. 所見の台帳（161件・1行1粗・直す前にファイルへ1回書いた＝`findings_G1〜G7.json`・`check_G1〜G7.md`）",
 "照合＝第1〜13章を6本の係が原文で1行ずつ（★も地の文も・394行）＋通し読み1本（中学生がはじめて聞いて分かるか・聞き役の置き場）。🔴 と話の芯に響く ⚠️ は④'が自分で原文を引き直した（誤報0件）。直す係は B・C の所見を1件ずつ原文で確かめてから直した。**直したあと、別の目2本が第1版→第2版の対照（`diff_v1_v2.md`）を当て直した**＝下の2つ目の表（30件・🔴1＝④'自身が `cb15` に入れた「第一報」＝起点のずれ）", "",
 led, ""]
open(f"{B}/gates.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
EOF
python "$B/build_v2.py" > "$O/b2.txt" 2>&1 || { cat "$O/b2.txt"; exit 2; }
run_gates g2
for f in cs csq cf df mech ledger rc; do cmp -s "$O/g1_$f.txt" "$O/g2_$f.txt" && echo "same $f" || echo "DIFF $f"; done
cat "$O/b2.txt"; cat "$O/g2_rc.txt"
