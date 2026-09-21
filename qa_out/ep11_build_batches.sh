#!/usr/bin/env bash
# 11本目⑤a: el_build を「章ごと」に分けて回す（2026-09-21）。
#
# 🔴 なぜ分けるか:
#   el_build を引数なしで回すと **全473行を1つの python プロセスで**組み立てる。
#   この環境はコミット上限がぎりぎり（19.9GB 中 空き 0.2〜0.4GB）なので、
#   長く走るほど落ちる確率が上がる（実測＝369行目・419行目・c103 で3回落ちた）。
#   章ごとに分ければ 1プロセスが短命・小さくなり、落ちてもその章だけやり直せばよい。
#
# ⭐ 累積で効く: `--cuts` は「対象外のカット」を **narration.json から持ち越す**。
#   持ち越しの条件は「指紋が今の台本・声・設定と一致し、wav がある」こと。
#   だから **章を順に足していけば** narration.json が章ごとに育つ。
#   ⚠️ 最初の章のときは narration.json が ep10 のままなので、他の章は「未作成」と警告が出る。
#      これは**正しい**（ep10 の秒数と字幕が混ざるのを防いでいる）。最後の章まで回せば消える。
#
# 使い方: bash qa_out/ep11_build_batches.sh   （ログは audio/el_qa/build_ep11_<章>.log）
set -u
cd "$(dirname "$0")/.." || exit 1
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1

CHAPS="pr c1 c2 c3 c4 c5 c6 c7 c8 c9 ep ed"
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
    log="audio/el_qa/build_ep11_${ch}.log"
    echo "── 章 $ch（${n}カット）→ $log"
    python tools/el_build.py --cuts "$ids" > "$log" 2>&1
    rc=$?
    echo "exit=$rc" >> "$log"
    # 🔴🔴 **exit 1 は「落ちた」とは限らない。**
    #    el_build は `return 0 if len(durs) == n else 1`＝**台本の全カットが記録に揃うまで 1** を返す
    #    （fail closed。中途半端な narration.json を成功にしない正しい作り）。
    #    章ごとに回している途中は**必ず 1**なので、ここで止めると1章目で終わってしまう（実際にそうなった）。
    #    ＝ 見分けるのは終了コードではなく「**締めの集計行が出たか**」。
    #       出ていれば最後まで走った／出ていなければ途中で落ちた（Traceback）。
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
# 締めの検算＝最後の章のログで「未作成」が消えていること（＝191カット全部が記録に載った）
last="audio/el_qa/build_ep11_ed.log"
if grep -q "まだ作っていないカット" "$last"; then
    echo "🔴 全章回したのに、まだ作っていないカットが残っている:"
    grep "まだ作っていないカット" "$last" | sed 's/^/   /'
    exit 1
fi
grep -E "^合成 |^本編の見込み" "$last" | sed 's/^/   /'
echo "✅ 全章おわり（未作成 0）"
exit 0
