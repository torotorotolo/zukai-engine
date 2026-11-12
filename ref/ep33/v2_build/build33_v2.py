# -*- coding: utf-8 -*-
"""33本目④'：台本 第1版に差し替え表を当てて第2版を組む（第1版は1文字も書き換えない・32本目 build32_v2.py を写した）。

  python -P ref/ep33/v2_build/build33_v2.py [ref/ep33/v2_build/patches33.json] [--out 置き場] [--check]

差し替え表（JSON の配列）の1件＝{"id": "P-001", "cut": "c105" | "§" | "*", "old": "…", "new": "…", "why": "…", "from": ["G2-003"]}
- cut がカット番号なら、そのカットの塊（`**c105**` の行から次のカットの頭・`---`・`###`・`##` の手前まで）の中で
  old がちょうど1回あるときだけ当てる。無い・2回以上なら止める（当て損ないを黙って通さない）。old と new は複数行でもよい。
- cut が "§" なら、§4 の外（§0 を除く頭と、§5 から終わり）でちょうど1回。
- cut が "*" なら、§0 を除く台本の全体でちょうど1回（章の見出しなど、カットの塊に入らない行）。
- 表は上から順に当てる（あとの差し替えの old は、前の差し替えを当てたあとの字）。
頭＝v2_build/v2_head.md（題の行・注・§0）を、第1版の頭（1行目〜「## 2. 照合の表」の手前）と差し替える。無ければ題の行だけ「第2版」にした仮の頭。
🔧＝画の欄か語り・聞き役の行が第1版と違うカットの見出し（`**c105** 🔧 ／ …`）。出典の欄だけの直しには付けない（check_script_diff は画と字幕だけを比べる）。
第1版の md5 を前後で比べる。1件でも当たらなければ1字も書かない（終了コード 1）。--check は書かずに当たるかだけ見る。
"""
import hashlib
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
V1 = os.path.join(EP, 'daihon_v1.md')
V2 = os.path.join(EP, 'daihon_v2.md')
HEADF = os.path.join(HERE, 'v2_head.md')
CUT = re.compile(r'^\*\*(c[0-9a-c]\d{2})\*\*')


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def split_doc(text):
    """頭（〜§0）・§0 のあと〜§4 の手前・§4・§5〜 に分ける。"""
    lines = text.split('\n')
    i2 = next(i for i, l in enumerate(lines) if l.startswith('## 2. 照合の表'))
    i4 = next(i for i, l in enumerate(lines) if l.startswith('## 4. 台本'))
    i5 = next(i for i, l in enumerate(lines) if i > i4 and l.startswith('## 5.'))
    return '\n'.join(lines[:i2]), '\n'.join(lines[i2:i4]), '\n'.join(lines[i4:i5]), '\n'.join(lines[i5:])


def cut_spans(s4):
    """§4 の中のカットの塊の位置（開始・終了の字の位置）。"""
    lines = s4.split('\n')
    pos, spans, cur, start = 0, {}, None, 0
    offs = []
    for l in lines:
        offs.append(pos)
        pos += len(l) + 1
    for i, l in enumerate(lines):
        m = CUT.match(l)
        stop = l.startswith('### ') or l.startswith('## ') or l.strip() == '---' or m
        if stop and cur is not None:
            spans[cur] = (start, offs[i])
            cur = None
        if m:
            cur, start = m.group(1), offs[i]
    if cur is not None:
        spans[cur] = (start, len(s4))
    return spans


def apply(patches, mid, s4, tail):
    for p in patches:
        pid, cut, old, new = p['id'], p['cut'], p['old'], p['new']
        if old == new:
            raise SystemExit('🔴 %s old と new が同じ' % pid)
        if cut == '§':
            n = mid.count(old) + tail.count(old)
            if n != 1:
                raise SystemExit('🔴 %s §（§4 の外）で old が %d 回: %r' % (pid, n, old[:60]))
            if mid.count(old):
                mid = mid.replace(old, new, 1)
            else:
                tail = tail.replace(old, new, 1)
        elif cut == '*':
            n = mid.count(old) + s4.count(old) + tail.count(old)
            if n != 1:
                raise SystemExit('🔴 %s 全体で old が %d 回: %r' % (pid, n, old[:60]))
            if mid.count(old):
                mid = mid.replace(old, new, 1)
            elif s4.count(old):
                s4 = s4.replace(old, new, 1)
            else:
                tail = tail.replace(old, new, 1)
        else:
            sp = cut_spans(s4)
            if cut not in sp:
                raise SystemExit('🔴 %s カット %s が無い' % (pid, cut))
            a, b = sp[cut]
            blk = s4[a:b]
            n = blk.count(old)
            if n != 1:
                raise SystemExit('🔴 %s %s の中で old が %d 回: %r' % (pid, cut, n, old[:80]))
            s4 = s4[:a] + blk.replace(old, new, 1) + s4[b:]
    return mid, s4, tail


def face(block):
    """画の欄と語り・聞き役の行（出典の欄を除く）＝🔧 の判定に使う。"""
    ls = block.rstrip('\n').split('\n')
    head = re.sub(r'\s*🔧', '', ls[0])
    parts = head.split('／')
    pic = parts[1].strip() if len(parts) > 1 else ''
    speech = [l for l in ls[1:] if l.startswith('>')]
    return pic, speech


def mark(s4_v1, s4_v2):
    sp1, sp2 = cut_spans(s4_v1), cut_spans(s4_v2)
    marked = []
    out = s4_v2
    for cid in sorted(sp2, key=lambda c: sp2[c][0], reverse=True):
        a, b = sp2[cid]
        blk2 = out[a:b]
        if cid in sp1:
            a1, b1 = sp1[cid]
            if face(s4_v1[a1:b1]) == face(blk2):
                continue
        first = blk2.split('\n', 1)
        hd = re.sub(r'^(\*\*c[0-9a-c]\d{2}\*\*)\s*', r'\1 🔧 ', first[0], count=1)
        out = out[:a] + hd + ('\n' + first[1] if len(first) > 1 else '') + out[b:]
        marked.append(cid)
    return out, sorted(marked)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    ptab = args[0] if args else os.path.join(HERE, 'patches33.json')
    out = V2
    if '--out' in sys.argv:
        out = sys.argv[sys.argv.index('--out') + 1]
    m_before = md5(V1)
    text = open(V1, encoding='utf-8').read().replace('\r\n', '\n')
    head, mid, s4, tail = split_doc(text)
    patches = json.load(open(ptab, encoding='utf-8')) if os.path.exists(ptab) else []
    ids = [p['id'] for p in patches]
    if len(ids) != len(set(ids)):
        raise SystemExit('🔴 差し替えの id が重なる')
    mid2, s4_2, tail2 = apply(patches, mid, s4, tail)
    s4_2, marked = mark(s4, s4_2)
    n1, n2 = len(cut_spans(s4)), len(cut_spans(s4_2))
    if os.path.exists(HEADF):
        head2 = open(HEADF, encoding='utf-8').read().replace('\r\n', '\n').rstrip('\n')
    else:
        first, rest = head.split('\n', 1)
        head2 = first.replace('台本 第1版', '台本 第2版') + '\n\n> （仮の頭＝v2_head.md がまだ無い）\n'
    doc = head2 + '\n\n' + mid2 + '\n' + s4_2 + '\n' + tail2
    if not doc.endswith('\n'):
        doc += '\n'
    if md5(V1) != m_before:
        raise SystemExit('🔴 第1版の md5 が変わった')
    print('差し替え %d件を当てた・カット %d → %d・🔧 %d（%s）' % (len(patches), n1, n2, len(marked), ' '.join(marked)))
    print('第1版 md5 %s（前後で同じ）' % m_before)
    if '--check' in sys.argv:
        print('（--check＝書いていない）')
        return 0
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(doc)
    print('→ %s md5 %s' % (out, md5(out)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
