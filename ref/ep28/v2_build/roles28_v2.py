# -*- coding: utf-8 -*-
"""28本目④'：聞き役の役割表 roles.tsv を第2版から書き出す（ルール 4-15 の正本の置き場＝ref/ep28/v2_build/roles.tsv・27本目 roles27_v2.py を写した）。
④ の roles28.py の build をそのまま使い、役割の表 ROLE だけ第2版のものに替える。

  python -P ref/ep28/v2_build/roles28_v2.py ref/ep28/daihon_v2.md ref/ep28/v2_build/roles.tsv

載っていない聞き役の行は「質問」。まとめ＝語りが言い終えた直後の言い直し・次の語りは「そう。」で受ける。
反応＝事実と数を言わない感想。⚠️ 1カットに役割の違う聞き役の行を2つ置かない（ROLE はカットの単位）。
"""
import importlib.util
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('roles28', os.path.join(os.path.dirname(HERE), 'v1_build', 'roles28.py'))
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)

# 第2版の役割（④' で替えたら、ここを直す＝手で roles.tsv を書かない）。始まりは第1版（v1_build/roles28.py）と同じ
ROLE = {
    'c215': 'まとめ', 'c310': 'まとめ', 'c403': 'まとめ', 'c411': 'まとめ', 'c421': 'まとめ', 'c507': 'まとめ',
    'c607': 'まとめ', 'c619': 'まとめ',
    'c207': '反応', 'c315': '反応', 'c517': '反応',
    'c610': '反応', 'c615': '反応',   # ④' で足した（4-15＝質問が5割を超えていた・最長の空き c607→c613・c613→c619 を割る）
}


def main(md, out):
    R.ROLE = ROLE
    rows = R.build(md)
    unused = sorted(set(ROLE) - {c for c, _, _ in rows})
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 28本目 聞き役の役割（roles28_v2.py が daihon_v2.md から書き出す・手で直さない）\n')
        for cid, role, text in rows:
            f.write('%s\t%s\t%s\n' % (cid, role, text))
    n = {r: sum(1 for _, x, _ in rows if x == r) for r in ('質問', 'まとめ', '反応')}
    print('%d行 → %s  %s' % (len(rows), out, n))
    if unused:
        print('🔴 ROLE に書いたのに聞き役の行が無いカット:', unused)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
