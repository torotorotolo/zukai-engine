# -*- coding: utf-8 -*-
"""30本目④'：聞き役の役割表 roles.tsv を第2版から書き出す（ルール 4-15 の正本の置き場＝ref/ep30/v2_build/roles.tsv・29本目 roles29_v2.py を写した）。
④ の roles30.py の build をそのまま使い、役割の表だけ第2版のもの（v2_build/roles_map.json）に替える。

  python -P ref/ep30/v2_build/roles30_v2.py ref/ep30/daihon_v2.md ref/ep30/v2_build/roles.tsv [--map 表.json]

載っていない聞き役の行は「質問」。まとめ＝語りが言い終えた直後の言い直し・次の語りは「そう。」で受ける。
反応＝事実と数を言わない感想。⚠️ 1カットに役割の違う聞き役の行を2つ置かない（表はカットの単位）。
役割を替えたら roles_map.json を直す（手で roles.tsv を書かない）。始まりは第1版（v1_build/roles30.py）と同じ。
"""
import importlib.util
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('roles30', os.path.join(os.path.dirname(HERE), 'v1_build', 'roles30.py'))
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)
MAP = os.path.join(HERE, 'roles_map.json')


def main(md, out, mp=MAP):
    R.ROLE = json.load(open(mp, encoding='utf-8'))
    rows = R.build(md)
    unused = sorted(set(R.ROLE) - {c for c, _, _ in rows})
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 30本目 聞き役の役割（roles30_v2.py が daihon_v2.md から書き出す・手で直さない）\n')
        for cid, role, text in rows:
            f.write('%s\t%s\t%s\n' % (cid, role, text))
    n = {r: sum(1 for _, x, _ in rows if x == r) for r in ('質問', 'まとめ', '反応')}
    print('%d行 → %s  %s' % (len(rows), out, n))
    if unused:
        print('🔴 表に書いたのに聞き役の行が無いカット:', unused)
        return 1
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    sys.exit(main(a[0], a[1], a[a.index('--map') + 1] if '--map' in a else MAP))
