# -*- coding: utf-8 -*-
"""21本目 聞き役の役割表 roles.tsv を台本から書き出す（④・2026-10-11・20本目の roles20.py を写した）。

  python ref/ep21/v1_build/roles21.py ref/ep21/daihon_v1.md ref/ep21/v1_build/roles.tsv

役割は下の ROLE（カットID→役割）で決める。載っていない聞き役の行は「質問」。
⚠️ 1カットに役割の違う聞き役の行を2つ置かない（ROLE はカットの単位）。
文は台本の字幕から `Q: ` を外したもの（check_listener.judge が1字違いを別の行とみなすため、手で写さない）。
"""
import sys

sys.path.insert(0, r'C:\Users\konar\Desktop\zukai-engine\tools')
import check_script as CS          # noqa: E402  parse を使う（道具は直さない）
import speaker                     # noqa: E402

# 質問以外の行（カットID → 役割）。まとめ＝語りが言い終えた直後の言い直し・次の語りは「そう。」で受ける
ROLE = {
    'c217': 'まとめ', 'c305': 'まとめ', 'c308': 'まとめ', 'c314': 'まとめ', 'c411': 'まとめ', 'c425': 'まとめ',
    'c507': 'まとめ',
    'c520': 'まとめ', 'c608': 'まとめ', 'c614': 'まとめ', 'c708': 'まとめ', 'c715': 'まとめ', 'c835': 'まとめ',
    'c912': 'まとめ', 'c917': 'まとめ', 'ca07': 'まとめ', 'ca17': 'まとめ', 'cb10': 'まとめ',
    'c424': '反応', 'c514': '反応', 'c612': '反応', 'c710': '反応', 'c832': '反応', 'ca02': '反応', 'cb15': '反応',
    'cc04': '反応',
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
        f.write('# 21本目 聞き役の役割（roles21.py が daihon_v1.md から書き出す・手で直さない）\n')
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
