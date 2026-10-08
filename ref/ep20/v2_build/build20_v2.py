# -*- coding: utf-8 -*-
"""20本目④'：台本 第1版に差し替え表を当てて第2版を組む（第1版は1文字も書き換えない・19本目 build19_v2.py を写した）。

  python ref/ep20/v2_build/build20_v2.py ref/ep20/v2_build/patches20.json [--check] [--out 置き場]

差し替え表（JSON の配列）の1件＝{"id": "G3-004", "cut": "c603" | "§" | "*", "old": "…", "new": "…", "why": "…"}
- cut がカット番号なら、そのカットの塊（`**c603**` の行から次のカットの頭・`---`・`###`・`##` の手前まで）の中で
  old がちょうど1回あるときだけ当てる。無い・2回以上なら止める（当て損ないを黙って通さない）。
- cut が "§" なら、§4 の外（`## 1.` から `## 4. 台本` の手前、または `## 5.` から終わり）でちょうど1回。
- cut が "*" なら、台本の全体でちょうど1回（章の見出しなど、カットの塊に入らない行）。
- new が old を含み、すでに new が塊の中にあるなら当てない（二重に足さない＝17本目の守り）。
- 当てたカットの見出しの行に 🔧 を1つ付ける（"noflag": true なら付けない＝出典の欄だけの直し）。
- 頭（1行目〜`## 1.` の手前）は v2_build/v2_head.md に差し替える（無ければ第1版の頭のまま＝試し組み）。
- 第1版の md5 を前後で比べる。--check は書き出さずに当たり具合だけ見る。
終了コード 0=組めた / 1=当て損ない・第1版が変わった
"""
import hashlib
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V1 = os.path.join(ROOT, 'daihon_v1.md')
HEAD = os.path.join(HERE, 'v2_head.md')
CUTID = re.compile(r'^\*\*(c[0-9a-c][0-9]{2})\*\*')


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def blocks(lines):
    """カット番号 → (始まりの行, 終わりの行)。"""
    out, cur, start = {}, None, None
    for i, ln in enumerate(lines):
        m = CUTID.match(ln)
        end_mark = ln.startswith('---') or ln.startswith('### ') or ln.startswith('## ')
        if m or end_mark:
            if cur:
                out[cur] = (start, i)
                cur = None
            if m:
                cur, start = m.group(1), i
    if cur:
        out[cur] = (start, len(lines))
    return out


def sig(lines, rng):
    """カットの「画の欄」と語り・聞き役の行（空行を除く）。出典の欄は入れない。"""
    a, b = rng
    head = lines[a].replace(' 🔧', '')
    parts = head.split(' ／ ')
    ga = parts[1].strip() if len(parts) > 1 else ''
    return (ga, tuple(x.strip() for x in lines[a + 1:b] if x.strip().startswith('>')))


def find_sec(lines):
    s1 = next(i for i, ln in enumerate(lines) if ln.startswith('## 1. '))
    s4 = next(i for i, ln in enumerate(lines) if ln.startswith('## 4. 台本'))
    s5 = next(i for i, ln in enumerate(lines) if ln.startswith('## 5. '))
    return s1, s4, s5


def main():
    args = sys.argv[1:]
    check = '--check' in args
    out = args[args.index('--out') + 1] if '--out' in args else os.path.join(ROOT, 'daihon_v2.md')
    pfile = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] != '--out')][0]
    patches = json.load(open(pfile, encoding='utf-8'))
    before = md5(V1)
    lines = open(V1, encoding='utf-8').read().split('\n')
    bad, done, skipped, touched = [], 0, 0, []
    ids = [p.get('id') for p in patches]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        bad.append('id が重なっている: %s' % dup)
    for k, p in enumerate(patches):
        cut, old, new = p['cut'], p['old'], p['new']
        pid = p.get('id', str(k))
        if not old:
            bad.append(f'{pid} {cut}: old が空')
            continue
        blk = blocks(lines)
        s1, s4, s5 = find_sec(lines)
        if cut == '*':
            ranges = [(0, len(lines))]
        elif cut == '§':
            ranges = [(s1, s4), (s5, len(lines))]
        elif cut in blk:
            ranges = [blk[cut]]
        else:
            bad.append(f'{pid} {cut}: カットが無い')
            continue
        text = '\n'.join('\n'.join(lines[a:b]) for a, b in ranges)
        if new and old in new and new in text:
            skipped += 1
            continue
        n = text.count(old)
        if n != 1:
            bad.append(f'{pid} {cut}: old が {n} 回（ちょうど1回でない）: {old[:50]}')
            continue
        for a, b in ranges:
            seg = '\n'.join(lines[a:b])
            if old in seg:
                seg = seg.replace(old, new, 1)
                lines[a:b] = seg.split('\n')
                if cut not in ('§', '*'):
                    touched.append(cut)
                break
        done += 1
    # 🔧 は「画の欄か語りの行が第1版から変わったカット」だけに付ける（出典の欄だけの直しは付けない＝check_script_diff と同じ見方）
    v1lines = open(V1, encoding='utf-8').read().split('\n')
    b1, b2 = blocks(v1lines), blocks(lines)
    flagged = []
    for c in sorted(set(touched)):
        if sig(v1lines, b1[c]) != sig(lines, b2[c]):
            a = b2[c][0]
            if '🔧' not in lines[a]:
                lines[a] = CUTID.sub(lambda m: m.group(0) + ' 🔧', lines[a], count=1)
            flagged.append(c)
    touched = flagged
    # 頭（1行目〜## 1. の手前）を v2_head.md に
    s1, _, _ = find_sec(lines)
    if os.path.exists(HEAD):
        head = open(HEAD, encoding='utf-8').read().rstrip('\n').split('\n')
        lines = head + [''] + lines[s1:]
        headnote = 'v2_head.md を差した'
    else:
        headnote = '頭は第1版のまま（v2_head.md が無い＝試し組み）'
    after = md5(V1)
    print(f'当てた {done}・二重なので当てない {skipped}・当て損ない {len(bad)}／直したカット {len(set(touched))}／{headnote}')
    for b in bad:
        print('  ✗', b)
    print('第1版 md5', before, '→', after, '（同じ）' if before == after else '（🔴 変わった）')
    if bad or before != after:
        sys.exit(1)
    if not check:
        open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
        print('書いた', out, md5(out))
        print('🔧', ' '.join(sorted(set(touched), key=lambda c: (c[1], c))))


if __name__ == '__main__':
    main()
