#!/usr/bin/env bash
# 12本目⑤a: el_build を「章ごと」に分けて回す（2026-09-23。11本目の qa_out/ep11_build_batches.sh を写した）。
#
# 🔴 なぜ分けるか（11本目で3回落ちた）:
#   el_build を引数なしで回すと全行を1つの python プロセスで組み立てる。この環境はコミット上限がぎりぎりなので、
#   長く走るほど落ちる確率が上がる。章ごとに分ければ 1プロセスが短命・小さくなり、落ちてもその章だけやり直せばよい。
#   ✅ 落ちてもクレジットは無駄にならない（合成キャッシュは行の中身で引く）。
#
# ⭐ 累積で効く: `--cuts` は「対象外のカット」を narration.json から持ち越す（指紋が一致し wav がある場合だけ）。
#   ⚠️ 最初の章のときは narration.json が ep11 のままなので、他の章は「未作成」と警告が出る＝正しい。
#
# 11本目との違い: 12本目は冒頭の pr 章・締めの ep 章が無い（c101 から始まり c920 で終わる）＋共通エンディング ed。
#
# 使い方: bash qa_out/ep12_build_batches.sh [章 …]   （引数なし＝全章。ログは audio/el_qa/build_ep12_<章>.log）
set -u
cd "$(dirname "$0")/.." || exit 1
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1

CHAPS="${*:-c1 c2 c3 c4 c5 c6 c7 c8 c9 ed}"
fail=0
for ch in $CHAPS; do
    ids=$(python -c "
import sys; sys.path.insert(0,'tools')
import narration, re
p='$ch'
print(','.join(c for c,_ in narration.SCRIPT if re.match(p+r'\d',c)))
")
    if [ -z "$ids" ]; then
        echo "🔴 章 $ch のカットIDが1件も取れない＝止める"; exit 1
    fi
    n=$(echo "$ids" | tr ',' '\n' | wc -l)
    log="audio/el_qa/build_ep12_${ch}.log"
    echo "── 章 $ch（${n}カット）→ $log"
    python tools/el_build.py --cuts "$ids" > "$log" 2>&1
    rc=$?
    echo "exit=$rc" >> "$log"
    # 🔴🔴 exit 1 は「落ちた」とは限らない（el_build は台本の全カットが揃うまで 1 を返す＝fail closed）。
    #    見分けるのは「締めの集計行が出たか」。
    if ! grep -qE "^合成 [0-9]+ カット" "$log"; then
        echo "   🔴 章 $ch は途中で落ちた（集計行が無い・exit $rc）:"
        tail -5 "$log" | sed 's/^/     /'
        fail=1
        break
    fi
    grep -E "^合成 " "$log" | sed 's/^/   /'
done
echo "=================="
if [ $fail -ne 0 ]; then echo "🔴 途中で落ちた（上を見る）"; exit 1; fi
last="audio/el_qa/build_ep12_ed.log"
if [ -f "$last" ] && grep -q "まだ作っていないカット" "$last"; then
    echo "🔴 全章回したのに、まだ作っていないカットが残っている:"
    grep "まだ作っていないカット" "$last" | sed 's/^/   /'
    exit 1
fi
[ -f "$last" ] && grep -E "^合成 |^本編の見込み" "$last" | sed 's/^/   /'
echo "✅ 指定の章はおわり"
exit 0
