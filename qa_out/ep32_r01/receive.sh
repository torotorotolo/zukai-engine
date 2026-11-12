#!/bin/bash
# 30本目 ⑥：本編を受け取ったあとの機械の検査を1本ずつ順に回す（コミットの空き＝同時に回さない・29本目の写し）
# 使い方： bash qa_out/ep32_r01/receive.sh titan_audio-ep32-r01.mp4
cd "$(dirname "$0")/../.." || exit 9
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1
M="${1:-titan_audio-ep32-r01.mp4}"
D=qa_out/ep32_r01
run() { # 札 出力 コマンド…
  local tag="$1" out="$2"; shift 2
  "$@" > "$D/$out" 2>&1
  local rc=$?
  echo "$tag exit=$rc"
}
run check_final check_final.txt python tools/check_final.py "out/jiko/$M"
run loud loud.txt python -u qa_out/kb_af_loud.py "out/jiko/$M"
run dumpwin dumpwin.txt python qa_out/ep32_r01_vs_qa.py --dump-win
# 🔧 32本目 ⑥（11-12）：照らす元＝⑤c' 周2 の Modal の検品（`qa-ep32_c2`＝版 202c0984・237カット＋扉11）→ 無ければ ⑤c が見た版（`qa-ep32_b7_full`）
#    ⚠️ 扉 c801・c901 と c801 の頭は周2 のあと（1feed2e5）に直した＝ここは必ず違う（原寸で見る）
run vs_qa vs_qa_run.txt python qa_out/ep32_r01_vs_qa.py "--mp4=$M" --qa=qa-ep32_c2,qa-ep32_b7_full
run cutframes cutframes.txt python qa_out/ep32_r01_cutframes.py "--mp4=$M"
run sub_center sub_center.txt python qa_out/sub_center.py out/jiko/ep32_r01_frames
run subscan subscan_run.txt python qa_out/ep32_r01_subscan.py "--mp4=$M"
run ground ground_run.txt python -P qa_out/ep32_r01_ground.py --cred --halo=3
run voiceq voiceq_run.txt python -P qa_out/ep32_r01_voiceq.py "out/jiko/$M"
echo done
