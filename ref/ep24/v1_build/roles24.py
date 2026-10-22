# -*- coding: utf-8 -*-
"""24本目 聞き役の役割表 roles.tsv を台本から書き出す（④・2026-10-22・23本目の roles23.py を写した）。

  python ref/ep24/v1_build/roles24.py ref/ep24/daihon_v1.md ref/ep24/v1_build/roles.tsv

役割は下の ROLE（カットID→役割）で決める。載っていない聞き役の行は「質問」。
⚠️ 1カットに役割の違う聞き役の行を2つ置かない（ROLE はカットの単位）。
文は台本の字幕から `Q: ` を外したもの（check_listener.judge が1字違いを別の行とみなすため、手で写さない）。
まとめ＝語りが言い終えた直後の言い直し・次の語りは「そう。」で受ける。反応＝事実と数を言わない感想（犠牲者の場面には置かない）。
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\konar\Desktop\zukai-engine\tools')
import check_script as CS          # noqa: E402  parse を使う（道具は直さない）
import speaker                     # noqa: E402

# 質問以外の行（カットID → 役割）
ROLE = {
    'c221': 'まとめ', 'c313': 'まとめ', 'c410': 'まとめ', 'c416': 'まとめ', 'c609': 'まとめ',
    'c713': 'まとめ', 'c813': 'まとめ', 'c823': 'まとめ', 'c910': 'まとめ', 'c923': 'まとめ',
    'ca06': 'まとめ', 'ca20': 'まとめ', 'cb08': 'まとめ', 'cb21': 'まとめ',
    'c419': 'まとめ', 'c811': 'まとめ', 'c926': 'まとめ', 'ca15': 'まとめ', 'cb20': 'まとめ',
    'c514': '反応', 'c907': '反応', 'c916': '反応', 'c223': '反応',
    'c316': '反応', 'c716': '反応', 'c613': '反応', 'cc09': '反応',
}


def build(md):
    cuts = CS.parse(open(md, encoding='utf-8').read())
    rows = []
    for cid, _, ls in cuts:
        for raw in ls:
            who = speaker.split(raw)[0]
            if who == speaker.WHO_Q:
                rows.append((cid, ROLE.get(cid, '質問'), speaker.bare(raw.strip())))
    return rows


def main(md, out):
    rows = build(md)
    unused = sorted(set(ROLE) - {c for c, _, _ in rows})
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 24本目 聞き役の役割（roles24.py が daihon_v1.md から書き出す・手で直さない）\n')
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
