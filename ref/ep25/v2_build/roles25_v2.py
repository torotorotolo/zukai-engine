# -*- coding: utf-8 -*-
"""25本目④'：第2版の聞き役の役割表 roles.tsv を台本から書き出す（24本目 roles24_v2.py を写した）。

  python ref/ep25/v2_build/roles25_v2.py ref/ep25/daihon_v2.md ref/ep25/v2_build/roles.tsv [--map 役割の表.json]

役割は roles_map.json（カットID→役割＝第1版の v1_build/roles25.py の ROLE の写し＋④' の直し）で決める。載っていない聞き役の行は「質問」。
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


def rows_of(md, role):
    cuts = CS.parse(open(md, encoding='utf-8').read())
    rows = []
    for cid, _, ls in cuts:
        for raw in ls:
            if speaker.split(raw)[0] == speaker.WHO_Q:
                rows.append((cid, role.get(cid, '質問'), speaker.bare(raw.strip())))
    return rows


def main(a):
    md, out = a[0], a[1]
    mp = a[a.index('--map') + 1] if '--map' in a else os.path.join(HERE, 'roles_map.json')
    role = json.load(open(mp, encoding='utf-8'))
    rows = rows_of(md, role)
    unused = sorted(set(role) - {c for c, _, _ in rows})
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 25本目 聞き役の役割（roles25_v2.py が %s から書き出す・手で直さない）\n' % os.path.basename(md))
        for cid, r, text in rows:
            f.write('%s\t%s\t%s\n' % (cid, r, text))
    n = {r: sum(1 for _, x, _ in rows if x == r) for r in ('質問', 'まとめ', '反応')}
    print('%d行 → %s  %s' % (len(rows), out, n))
    if unused:
        print('🔴 役割の表に書いたのに聞き役の行が無いカット:', unused)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
