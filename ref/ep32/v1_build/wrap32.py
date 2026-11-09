# -*- coding: utf-8 -*-
"""32本目 ④：カットの途中の行が句点・読点で終わっていない所を、字を変えずに改行の位置だけ直す（check_script の「途中の行」の E）。

  python -P ref/ep32/v1_build/wrap32.py ref/ep32/daihon_v1.md [--dry]

・聞き役の行（> Q: ）はそのまま。語りの行のかたまりごとに、つないでから「、」「。」のあとでだけ切り直す（1行41字まで）
・行の数はできるだけ元のまま（カットの行の合計は3まで）。切り直せないかたまり（句読点のあいだが41字をこえる）は直さずに知らせる
・前後で、カットごとの語り（改行を除いた字）が1字でも違えば書かない（fail closed）
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HEAD = re.compile(r'^\*\*(c[0-9a-c]\d{2})\*\*')
MAXLEN = 41
ENDS = ('、', '。')


def chunks(s):
    out, cur = [], ''
    for ch in s:
        cur += ch
        if ch in ENDS:
            out.append(cur)
            cur = ''
    if cur:
        out.append(cur)
    return out


def wrap(seg_lines, want):
    s = ''.join(seg_lines)
    cs = chunks(s)
    if any(len(c) > MAXLEN for c in cs):
        return None
    best = None
    n = len(cs)
    # 何行に分けるかを want から順に試す（少ない行で収まれば、行の長さをそろえる）
    for k in range(max(1, want), 4):
        # 動的計画で、k 行に分けて最長の行をいちばん短くする
        import functools

        @functools.lru_cache(None)
        def f(i, rows):
            if i == n:
                return (0, ()) if rows == 0 else None
            if rows == 0:
                return None
            res = None
            ln = 0
            for j in range(i, n):
                ln += len(cs[j])
                if ln > MAXLEN:
                    break
                sub = f(j + 1, rows - 1)
                if sub is None:
                    continue
                cand = (max(ln, sub[0]), (j + 1,) + sub[1])
                if res is None or cand[0] < res[0]:
                    res = cand
            return res
        r = f(0, k)
        if r is not None:
            cuts = (0,) + r[1]
            best = [''.join(cs[cuts[t]:cuts[t + 1]]) for t in range(k)]
            break
    return best


def main(path, dry=False):
    raw = open(path, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in raw else '\n'
    lines = raw.replace('\r\n', '\n').split('\n')
    out, i, changed, failed = [], 0, [], []
    cur = None
    while i < len(lines):
        ln = lines[i]
        m = HEAD.match(ln)
        if m:
            cur = m.group(1)
        if cur and ln.startswith('> '):
            block = []
            while i < len(lines) and lines[i].startswith('> '):
                block.append(lines[i])
                i += 1
            segs, seg = [], []
            for b in block:
                if b.startswith('> Q: '):
                    if seg:
                        segs.append(('n', seg))
                        seg = []
                    segs.append(('q', [b]))
                else:
                    seg.append(b[2:])
            if seg:
                segs.append(('n', seg))
            need = any(kind == 'n' and any(not x.endswith(ENDS) for x in s[:-1]) for kind, s in segs)
            # かたまりの最後の行のあとに別のかたまり（聞き役）が続くとき、その最後の行も句読点で終える
            for t, (kind, s) in enumerate(segs[:-1]):
                if kind == 'n' and not s[-1].endswith(ENDS):
                    need = True
            if not need:
                out.extend(block)
                continue
            newblock = []
            ok = True
            for kind, s in segs:
                if kind == 'q':
                    newblock.extend(s)
                    continue
                w = wrap(s, len(s))
                if w is None:
                    ok = False
                    break
                newblock.extend('> ' + x for x in w)
            before = ''.join(b[2:] for b in block if not b.startswith('> Q: '))
            after = ''.join(b[2:] for b in newblock if not b.startswith('> Q: '))
            if not ok or before != after or len(newblock) > 3:
                failed.append((cur, len(newblock) if ok else 0))
                out.extend(block)
                continue
            if newblock != block:
                changed.append(cur)
            out.extend(newblock)
            continue
        out.append(ln)
        i += 1
    print('直したカット %d: %s' % (len(changed), ' '.join(changed)))
    if failed:
        print('🔴 切り直せないカット %d: %s' % (len(failed), ' '.join('%s(%d行)' % f for f in failed)))
    if dry:
        return 1 if failed else 0
    text = '\n'.join(out)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text.replace('\n', nl) if nl != '\n' else text)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], '--dry' in sys.argv))
