# -*- coding: utf-8 -*-
"""32本目 ④：台本に差し替え表を当てる（元の文がちょうど1回あるときだけ・1つでも外れたら1字も書かない）。

  python -P ref/ep32/v1_build/patch32.py ref/ep32/daihon_v1.md 表.txt [--dry]

表の形（JSON にしない＝引用符の書き損じを避ける）：
  @@@ OLD
  （元の文。複数行でよい）
  @@@ NEW
  （新しい文）
  @@@ END
⚠️ 新しい文が元の文を含む直し（うしろに足す形）は、もう新しい文があれば当てない（17本目の patch_review.py の守り）。
⚠️ 当てたあと、カットの見出しの数・聞き役の行の数を前後で出す（数が狂っていないかを人が見る）。
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HEAD = re.compile(r'^\*\*(c[0-9a-c]\d{2}[a-z]?)\*\*', re.M)
QL = re.compile(r'^> Q: ', re.M)


def blocks(path):
    out, mode, old, new = [], None, [], []
    for ln in open(path, encoding='utf-8').read().split('\n'):
        if ln == '@@@ OLD':
            mode, old, new = 'old', [], []
        elif ln == '@@@ NEW':
            mode = 'new'
        elif ln == '@@@ END':
            out.append(('\n'.join(old), '\n'.join(new)))
            mode = None
        elif mode == 'old':
            old.append(ln)
        elif mode == 'new':
            new.append(ln)
    if mode is not None:
        raise SystemExit('🔴 表の終わりに @@@ END が無い')
    return out


def main(md, table, dry=False):
    text = open(md, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in text else '\n'
    work = text.replace('\r\n', '\n')
    bs = blocks(table)
    bad = 0
    skipped = 0
    for i, (old, new) in enumerate(bs, 1):
        n = work.count(old)
        if old in new and work.count(new) == 1:
            skipped += 1
            print('  #%d もう当たっている（飛ばす）' % i)
            continue
        if n != 1:
            bad += 1
            print('🔴 #%d 元の文が %d 回: %s' % (i, n, old[:60].replace('\n', '⏎')))
            continue
        work = work.replace(old, new)
    if bad:
        print('🔴 %d件が当たらない＝1字も書かない' % bad)
        return 1
    before = (len(HEAD.findall(text)), len(QL.findall(text.replace('\r\n', '\n'))))
    after = (len(HEAD.findall(work)), len(QL.findall(work)))
    print('表 %d件（当てた %d・飛ばした %d）・カット %d→%d・聞き役の行 %d→%d'
          % (len(bs), len(bs) - skipped, skipped, before[0], after[0], before[1], after[1]))
    if dry:
        return 0
    with open(md, 'w', encoding='utf-8', newline='') as f:
        f.write(work.replace('\n', nl) if nl != '\n' else work)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2], '--dry' in sys.argv))
