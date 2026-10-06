# -*- coding: utf-8 -*-
"""19本目④'：台本 第1版に差し替え表を当てて第2版を組む（第1版は1文字も書き換えない）。

  python build19_v2.py patches19.json [--check]

差し替え表（JSON の配列）の1件＝{"cut": "c305" | "§0" など, "old": "…", "new": "…", "why": "…", "id": "…"}
- cut がカット番号なら、そのカットの塊（`**c305**` の行から次のカットの頭・`---`・`###` の手前まで）の中で
  old がちょうど1回あるときだけ当てる。無い・2回以上なら止める（当て損ないを黙って通さない）。
- cut が "§" で始まるなら、§4 の外（台本の頭から `## 4. 台本` の手前、または `## 5.` から終わり）でちょうど1回。
- cut が "*" なら、台本の全体でちょうど1回（章の見出しなど、カットの塊に入らない行）。
- new が old を含み、すでに new が塊の中にあるなら当てない（二重に足さない＝17本目の守り）。
- 当てたカットの見出しの行に 🔧 を1つ付ける（すでにあれば付けない）。
- 第1版の md5 を前後で比べる。--check は書き出さずに当たり具合だけ見る。
"""
import hashlib
import json
import re
import sys

ROOT = 'C:/Users/konar/Desktop/zukai-engine/ref/ep19/'
V1 = ROOT + 'daihon_v1.md'
V2 = ROOT + 'daihon_v2.md'


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def blocks(lines):
    """カット番号 → (始まりの行, 終わりの行) を返す。"""
    out, cur, start = {}, None, None
    for i, ln in enumerate(lines):
        m = re.match(r'^\*\*(c[0-9a-c][0-9]{2})\*\*', ln)
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


def main():
    args = sys.argv[1:]
    check = '--check' in args
    pfile = [a for a in args if not a.startswith('--')][0]
    patches = json.load(open(pfile, encoding='utf-8'))
    before = md5(V1)
    lines = open(V1, encoding='utf-8').read().split('\n')
    sec4 = next(i for i, ln in enumerate(lines) if ln.startswith('## 4. 台本'))
    sec5 = next(i for i, ln in enumerate(lines) if ln.startswith('## 5.'))
    bad, done, skipped, touched = [], 0, 0, []
    for k, p in enumerate(patches):
        cut, old, new = p['cut'], p['old'], p['new']
        pid = p.get('id', str(k))
        blk = blocks(lines)
        if cut == '*':
            # 章の見出しなど、どのカットの塊にも入らない行＝台本の全体でちょうど1回
            ranges = [(0, len(lines))]
        elif cut.startswith('§'):
            ranges = [(0, sec4), (sec5, len(lines))]
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
            bad.append(f'{pid} {cut}: old が {n} 回（ちょうど1回でない）: {old[:40]}')
            continue
        for a, b in ranges:
            seg = '\n'.join(lines[a:b])
            if old in seg:
                seg = seg.replace(old, new, 1)
                newl = seg.split('\n')
                lines[a:b] = newl
                if not cut.startswith('§') and cut != '*':
                    h = lines[a]
                    if '🔧' not in h:
                        lines[a] = re.sub(r'^(\*\*c[0-9a-c][0-9]{2}\*\*)', r'\1 🔧', h)
                    touched.append(cut)
                # 行数が変わると後ろの範囲がずれるので sec4/sec5 を取り直す
                sec4 = next(i for i, ln in enumerate(lines) if ln.startswith('## 4. 台本'))
                sec5 = next(i for i, ln in enumerate(lines) if ln.startswith('## 5.'))
                break
        done += 1
    after = md5(V1)
    print(f'当てた {done}・二重なので当てない {skipped}・当て損ない {len(bad)}／🔧 のカット {len(set(touched))}')
    for b in bad:
        print('  ✗', b)
    print('第1版 md5', before, '→', after, '（同じ）' if before == after else '（🔴 変わった）')
    if bad or before != after:
        sys.exit(1)
    if not check:
        open(V2, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
        print('書いた', V2, md5(V2))
        print('🔧', ' '.join(sorted(set(touched))))


if __name__ == '__main__':
    main()
