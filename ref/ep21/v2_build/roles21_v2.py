# -*- coding: utf-8 -*-
"""21本目④'：第2版の聞き役の役割表 roles.tsv を台本から書き出す（v1_build/roles21.py・20本目 roles20_v2.py を写した）。

  python ref/ep21/v2_build/roles21_v2.py ref/ep21/daihon_v2.md ref/ep21/v2_build/roles.tsv

役割は roles_map.json（カットID→役割）で決める。載っていない聞き役の行は「質問」。
⚠️ 1カットに役割の違う聞き役の行を2つ置かない（役割はカットの単位）。
文は台本の字幕から `Q: ` を外したもの（check_listener.judge が1字違いを別の行とみなすため、手で写さない）。
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\konar\Desktop\zukai-engine\tools')
import check_script as CS          # noqa: E402  parse を使う（道具は直さない）
import speaker                     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROLE = json.load(open(os.path.join(HERE, 'roles_map.json'), encoding='utf-8'))


def main(md, out):
    cuts = CS.parse(open(md, encoding='utf-8').read())
    rows = []
    for cid, _, ls in cuts:
        for raw in ls:
            who = speaker.split(raw)[0]
            if who == speaker.WHO_Q:
                rows.append((cid, ROLE.get(cid, '質問'), speaker.bare(raw.strip())))
    bad = sorted(set(ROLE) - {c for c, _, _ in rows})
    wrong = sorted(c for c, r in ROLE.items() if r not in ('質問', 'まとめ', '反応'))
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 21本目 聞き役の役割（第2版・roles21_v2.py が daihon_v2.md と roles_map.json から書き出す・手で直さない）\n')
        for cid, role, text in rows:
            f.write('%s\t%s\t%s\n' % (cid, role, text))
    n = {r: sum(1 for _, x, _ in rows if x == r) for r in ('質問', 'まとめ', '反応')}
    tot = len(rows) or 1
    print('%d行 → %s  %s（質問 %.0f%%・まとめ %.0f%%・反応 %.0f%%）' % (
        len(rows), out, n, 100 * n['質問'] / tot, 100 * n['まとめ'] / tot, 100 * n['反応'] / tot))
    if bad or wrong:
        print('🔴 roles_map に書いたのに聞き役の行が無いカット:', bad, '／役割の字が違う:', wrong)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
