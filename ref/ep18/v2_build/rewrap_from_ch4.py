# -*- coding: utf-8 -*-
"""台本の行を「、」「。」の所でだけ切り直す（字は1字も変えない）。

規則（tools/check_script.py）：句点で終わらない行は、読点で続く行か、カットの最終行のどちらか。
話者が替わる前の行は。？！で閉じる。★は最後の行のまま。1行41字まで。1カット1〜3行。

方法：カットの中で「同じ話し手が続く語りの行」をつなぎ、「、」「。」の後ろで区切った
かたまりを、元の行数のまま、いちばん長い行が短くなるように詰め直す（動的計画法）。
元の行数で41字に収まらなければ、1カット3行までなら1行増やす。どちらも無理なら止めて報告。

使い方: python rewrap.py parts/c2.md [...]   （上書き。書き換える前の md5 と字の数を出す）
"""
import hashlib
import re
import sys

CUT = re.compile(r'^\*\*(c[0-9a-z]\d{2})\*\*')
MAXC = 41


def clean_len(s):
    return len(s.replace('**', ''))


def segs(text):
    out, cur = [], ''
    for ch in text:
        cur += ch
        if ch in '、。':
            out.append(cur)
            cur = ''
    if cur:
        out.append(cur)
    return out


def pack(sg, k):
    """sg を k 行に分け、最長の行を最小にする。返り値＝行のリスト or None。"""
    n = len(sg)
    if k > n:
        return None
    L = [0]
    for s in sg:
        L.append(L[-1] + clean_len(s))
    INF = 10 ** 9
    best = [[INF] * (n + 1) for _ in range(k + 1)]
    back = [[-1] * (n + 1) for _ in range(k + 1)]
    best[0][0] = 0
    for j in range(1, k + 1):
        for i in range(1, n + 1):
            for p in range(j - 1, i):
                w = max(best[j - 1][p], L[i] - L[p])
                if w < best[j][i]:
                    best[j][i] = w
                    back[j][i] = p
    if best[k][n] > MAXC:
        return None
    lines, i = [], n
    for j in range(k, 0, -1):
        p = back[j][i]
        lines.append(''.join(sg[p:i]))
        i = p
    return lines[::-1]


def fix_cut(lines):
    """lines＝'> ' を外した行。戻り値＝新しい行（'> ' なし）。"""
    groups = []   # [kind, [texts]] kind: 'n' 語り / 'q' 聞き役 / 's' 決め所
    for l in lines:
        kind = 'q' if l.startswith('Q: ') else ('s' if l.startswith('★') else 'n')
        if groups and groups[-1][0] == kind == 'n':
            groups[-1][1].append(l)
        else:
            groups.append([kind, [l]])
    out = []
    budget = 3 - sum(len(g[1]) for g in groups if g[0] != 'n')
    ngroups = [g for g in groups if g[0] == 'n']
    orig_n = sum(len(g[1]) for g in ngroups)
    extra = 3 - (orig_n + (sum(len(g[1]) for g in groups) - orig_n))
    for g in groups:
        if g[0] != 'n':
            out.extend(g[1])
            continue
        text = ''.join(g[1])
        sg = segs(text)
        k = len(g[1])
        res = pack(sg, k)
        if res is None and extra > 0:
            res = pack(sg, k + 1)
            if res is not None:
                extra -= 1
        if res is None:
            raise ValueError('収まらない: ' + text)
        out.extend(res)
    return out


def main(paths):
    for p in paths:
        src = open(p, encoding='utf-8').read()
        before = hashlib.md5(src.encode('utf-8')).hexdigest()
        chars_before = sum(len(l[2:]) for l in src.split('\n') if l.startswith('> '))
        out, cur, buf = [], None, []

        def flush():
            if buf:
                new = fix_cut([b[2:] for b in buf])
                out.extend('> ' + x for x in new)
                buf.clear()

        for line in src.split('\n'):
            if line.startswith('> '):
                buf.append(line)
                continue
            flush()
            out.append(line)
        flush()
        dst = '\n'.join(out)
        chars_after = sum(len(l[2:]) for l in dst.split('\n') if l.startswith('> '))
        assert chars_before == chars_after, (p, chars_before, chars_after)
        assert re.sub(r'\n> ', '', src).replace('\n', '') .count('。') == re.sub(r'\n> ', '', dst).replace('\n', '').count('。')
        open(p, 'w', encoding='utf-8').write(dst)
        print(p, 'md5', before[:8], '→', hashlib.md5(dst.encode('utf-8')).hexdigest()[:8], '字', chars_before, '=', chars_after)


if __name__ == '__main__':
    main(sys.argv[1:])
