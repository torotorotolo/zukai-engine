# -*- coding: utf-8 -*-
"""26本目 聞き役の役割表 roles.tsv を台本から書き出す（④・2026-10-27・25本目の roles25.py を写した）。

  python ref/ep26/v1_build/roles26.py ref/ep26/daihon_v1.md ref/ep26/v1_build/roles.tsv

役割は下の ROLE（カットID→役割）で決める。載っていない聞き役の行は「質問」。
⚠️ 1カットに役割の違う聞き役の行を2つ置かない（ROLE はカットの単位）。
文は台本の字幕から `Q: ` を外したもの（check_listener.judge が1字違いを別の行とみなすため、手で写さない）。
まとめ＝語りが言い終えた直後の言い直し・次の語りは「そう。」で受ける。反応＝事実と数を言わない感想（犠牲者の場面には置かない）。
⚠️ ルール 4-15 の正本の置き場は `ref/ep26/v2_build/roles.tsv`（④' が第2版から書き出す）。第1版の表はここ（v1_build）に置く（24・25本目と同じ）。
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\konar\Desktop\zukai-engine\tools')
import check_script as CS          # noqa: E402  parse を使う（道具は直さない）
import speaker                     # noqa: E402

# 質問以外の行（カットID → 役割）。まとめ＝語りが言い終えた直後の言い直し・次の語りは「そう。」で受ける
ROLE = {
    'c219': 'まとめ', 'c315': 'まとめ', 'c410': 'まとめ', 'c513': 'まとめ',
    'c612': 'まとめ', 'c625': 'まとめ', 'c627': 'まとめ', 'c636': 'まとめ',
    'c707': 'まとめ', 'c713': 'まとめ', 'c807': 'まとめ', 'c821': 'まとめ',
    'c214': 'まとめ', 'c623': 'まとめ', 'c908': 'まとめ', 'c911': 'まとめ', 'c929': 'まとめ', 'c942': 'まとめ',
    'ca04': 'まとめ', 'ca07': 'まとめ', 'ca11': 'まとめ', 'cb05': 'まとめ',
    'c409': '反応', 'c802': '反応', 'c937': '反応', 'c321': '反応', 'c639': '反応',
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
        f.write('# 26本目 聞き役の役割（roles26.py が daihon_v1.md から書き出す・手で直さない）\n')
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
