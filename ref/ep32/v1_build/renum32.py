# -*- coding: utf-8 -*-
"""31本目 ④：台本のカットIDを章ごとに振り直す（書きながら足した枝番 c513b などを c514 …に）。

  python -P ref/ep31/v1_build/renum31.py ref/ep31/daihon_v1.md [--dry]

・章＝カットIDの頭2字（c1〜c9・ca〜cc）。章の中は文書の順に 01 から振る（c1 は c101〜）。
・本文の中の参照（「c101 と同じ」など）も同じ対応表で直す（2段で置き換える＝衝突しない）。
・章の見出しの「（Nカット）」を実際の数に直す。
・前後で、カットの数・行・句読点を除いた字が同じか確かめ、違えば1字も書かない（fail closed）。
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ID_RE = re.compile(r'^\*\*(c[0-9a-c]\d{2}[a-z]?)\*\*', re.M)
HEAD_RE = re.compile(r'^(### .+?)（(\d+)カット）$', re.M)


def body_sig(text):
    """カットIDと見出しの数を除いた本文の指紋（語りの行だけ）。"""
    return [ln for ln in text.split('\n') if ln.startswith('> ')]


def main(path, dry=False):
    text = open(path, encoding='utf-8', newline='').read()
    olds = ID_RE.findall(text)
    if len(olds) != len(set(olds)):
        dup = sorted({x for x in olds if olds.count(x) > 1})
        print('🔴 同じカットIDが2回ある:', dup)
        return 1
    order = {}
    mapping = {}
    for cid in olds:
        ch = cid[:2]
        order[ch] = order.get(ch, 0) + 1
        n = order[ch]
        new = '%s%02d' % (ch, n) if ch != 'c1' else 'c1%02d' % n
        if ch[1].isdigit() and ch != 'c1':
            new = '%s%02d' % (ch, n)
        mapping[cid] = new
    changed = {k: v for k, v in mapping.items() if k != v}
    # 2段の置き換え（語の境＝前後が英数字でない所だけ）
    tmp = {}
    out = text
    for i, (old, new) in enumerate(sorted(changed.items(), key=lambda kv: -len(kv[0]))):
        ph = '\x00ID%04d\x00' % i
        tmp[ph] = new
        out = re.sub(r'(?<![0-9a-z])%s(?![0-9a-z])' % re.escape(old), ph, out)
    for ph, new in tmp.items():
        out = out.replace(ph, new)
    # 章の見出しのカット数
    counts = {}
    for cid in ID_RE.findall(out):
        counts[cid[:2]] = counts.get(cid[:2], 0) + 1
    heads = list(HEAD_RE.finditer(out))
    chs = list(counts.keys())
    if len(heads) != len(chs):
        print('🔴 章の見出し %d と章の数 %d が合わない' % (len(heads), len(chs)))
        return 1
    for m, ch in zip(reversed(heads), reversed(chs)):
        out = out[:m.start()] + '%s（%dカット）' % (m.group(1), counts[ch]) + out[m.end():]
    # 確かめ
    if body_sig(out) != body_sig(text) or len(ID_RE.findall(out)) != len(olds):
        print('🔴 語りの行かカットの数が変わった＝書かない')
        return 1
    print('カット %d・振り直し %d件・章ごと %s' % (len(olds), len(changed), counts))
    for old, new in sorted(changed.items(), key=lambda kv: olds.index(kv[0])):
        print('  %s → %s' % (old, new))
    if dry:
        return 0
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(out)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], '--dry' in sys.argv))
