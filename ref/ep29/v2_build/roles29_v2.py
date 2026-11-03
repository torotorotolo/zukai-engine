# -*- coding: utf-8 -*-
"""29本目④'：聞き役の役割表 roles.tsv を第2版から書き出す（ルール 4-15 の正本の置き場＝ref/ep29/v2_build/roles.tsv・28本目 roles28_v2.py を写した）。
④ の roles29.py の build をそのまま使い、役割の表 ROLE だけ第2版のものに替える。

  python -P ref/ep29/v2_build/roles29_v2.py ref/ep29/daihon_v2.md ref/ep29/v2_build/roles.tsv

載っていない聞き役の行は「質問」。まとめ＝語りが言い終えた直後の言い直し・次の語りは「そう。」で受ける。
反応＝事実と数を言わない感想。⚠️ 1カットに役割の違う聞き役の行を2つ置かない（ROLE はカットの単位）。
"""
import importlib.util
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('roles29', os.path.join(os.path.dirname(HERE), 'v1_build', 'roles29.py'))
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)

# 第2版の役割（④' で替えたら、ここを直す＝手で roles.tsv を書かない）。始まりは第1版（v1_build/roles29.py）と同じ
ROLE = {
    'c218': 'まとめ', 'c416': 'まとめ', 'c418': 'まとめ', 'c420': 'まとめ', 'c506': 'まとめ', 'c508': 'まとめ',
    'c620': 'まとめ',   # c613 の「まとめ」は ④' で問いにして c612 の頭へ移した＝表に無い聞き役は質問
    'c216': '反応', 'c308': '反応', 'c408': '反応', 'c212': '反応', 'c316': '反応',
}


def main(md, out):
    R.ROLE = ROLE
    rows = R.build(md)
    unused = sorted(set(ROLE) - {c for c, _, _ in rows})
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 29本目 聞き役の役割（roles29_v2.py が daihon_v2.md から書き出す・手で直さない）\n')
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
