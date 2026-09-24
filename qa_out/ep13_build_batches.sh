#!/usr/bin/env bash
# 13本目⑤a: el_build を「章ごと」に分けて回す（2026-09-24。12本目の qa_out/ep12_build_batches.sh を写した）。
#
# 🔴 なぜ分けるか（11本目で3回落ちた）:
#   el_build を引数なしで回すと全行を1つの python プロセスで組み立てる。この環境はコミット上限がぎりぎりなので、
#   長く走るほど落ちる確率が上がる。章ごとに分ければ 1プロセスが短命・小さくなり、落ちてもその章だけやり直せばよい。
#   ✅ 落ちてもクレジットは無駄にならない（合成キャッシュは行の中身で引く）。
#
# 12本目との違い:
#   ① 🔴 **残高の見張り**（2026-09-24 カズヤくん決定「今の残りで全編の合成だけ先に。12本目⑥の直しの分を残す」）。
#      章に入る前に口座の残りを読み、「残り − その章の見込み」が FLOOR を割るなら**その章に入らずに止める**。
#      見込み＝その章の送信字数 × 0.55 × 1.3（異音の振り直しの上乗せ。12本目の実測は 1.12 倍）。
#   ② 13本目は**別の作業ツリー**（Desktop/zukai-engine-ep13a5）で焼く。12本目⑥が公開するまで本線の audio/ を触らない。
#
# 使い方: bash qa_out/ep13_build_batches.sh [章 …]   （引数なし＝全章。ログは audio/el_qa/build_ep13_<章>.log）
set -u
cd "$(dirname "$0")/.." || exit 1
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1
FLOOR="${FLOOR:-2500}"

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
    # 🔴 残高の見張り（読むだけ・0クレジット）。読めなければ止める（fail closed）
    guard=$(python -c "
import sys; sys.path.insert(0,'tools')
import el_tts, el_script as E
ids=set('$ids'.split(','))
chars=sum(len(E.el_text(l.text)) for l in E.lines() if l.cid in ids)
used,lim=el_tts.credits_used()
est=int(chars*0.55*1.3)
print(lim-used, est, chars)
") || { echo "🔴 残高が読めない＝止める"; exit 1; }
    set -- $guard
    left=$1; est=$2; chars=$3
    if [ $((left - est)) -lt "$FLOOR" ]; then
        echo "🔴 章 $ch に入らずに止める：残り ${left} − 見込み ${est}（${chars}字）＜ 下限 ${FLOOR}"
        fail=1
        break
    fi
    n=$(echo "$ids" | tr ',' '\n' | wc -l)
    log="audio/el_qa/build_ep13_${ch}.log"
    echo "── 章 $ch（${n}カット・${chars}字・見込み ${est}／残り ${left}）→ $log"
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
    grep -E "^合成 |^API |^クレジット " "$log" | sed 's/^/   /'
done
echo "=================="
if [ $fail -ne 0 ]; then echo "🔴 途中で止めた（上を見る）"; exit 1; fi
last="audio/el_qa/build_ep13_ed.log"
if [ -f "$last" ] && grep -q "まだ作っていないカット" "$last"; then
    echo "🔴 全章回したのに、まだ作っていないカットが残っている:"
    grep "まだ作っていないカット" "$last" | sed 's/^/   /'
    exit 1
fi
[ -f "$last" ] && grep -E "^合成 |^本編の見込み" "$last" | sed 's/^/   /'
echo "✅ 指定の章はおわり"
exit 0
