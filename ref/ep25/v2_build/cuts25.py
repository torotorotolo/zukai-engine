# -*- coding: utf-8 -*-
"""25本目④'：台本（第1版・第2版）をカットに割る小さな道具（照合の係・通し読み・対照表が同じ切り方で読む）。

  python ref/ep25/v2_build/cuts25.py narr ref/ep25/daihon_v1.md 出力.txt       # 語りと聞き役だけ（カット番号つき）＝通し読み用
  python ref/ep25/v2_build/cuts25.py show ref/ep25/daihon_v1.md c509 c520       # c509〜c520 の塊をそのまま
  python ref/ep25/v2_build/cuts25.py --selftest

カットの塊＝`**c101**` の行から、次のカットの頭・`---`・`###`・`##` の手前まで。頭の行＝「**cNNN** ／ 画の欄 ／ 出典の欄」。
語り＝`> ` の行・聞き役＝`> Q: ` の行（印は音にも字幕にも出さない）。
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
CUTID = re.compile(r'^\*\*(c[0-9a-d][0-9]{2})\*\*')
ORDER = '123456789ab'


def key(c):
    return (ORDER.index(c[1]), int(c[2:]))


def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    cuts, cur, chap = [], None, ''
    in4 = False
    for i, ln in enumerate(lines):
        if ln.startswith('## '):
            in4 = ln.startswith('## 4. ')
        if ln.startswith('### ') and in4:
            chap = ln[4:].strip()
        m = CUTID.match(ln)
        end = ln.startswith('---') or ln.startswith('### ') or ln.startswith('## ')
        if (m or end) and cur:
            cuts.append(cur)
            cur = None
        if m:
            parts = ln.split(' ／ ')
            cur = {'id': m.group(1), 'chap': chap, 'line': i + 1, 'head': ln,
                   'ga': parts[1].strip() if len(parts) > 1 else '',
                   'src': ' ／ '.join(parts[2:]).strip() if len(parts) > 2 else '',
                   'say': [], 'raw': [ln]}
        elif cur:
            cur['raw'].append(ln)
            if ln.startswith('>'):
                cur['say'].append(ln[1:].strip())
    if cur:
        cuts.append(cur)
    return cuts


def narr(path, out):
    cuts = parse(path)
    buf, chap = [], None
    for c in cuts:
        if c['chap'] != chap:
            chap = c['chap']
            buf.append('')
            buf.append('## ' + chap)
        for s in c['say']:
            if s.startswith('Q:'):
                buf.append('%s　【聞き役】%s' % (c['id'], s[2:].strip()))
            else:
                buf.append('%s　%s' % (c['id'], s))
    open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(buf).strip() + '\n')
    print('書いた', out, 'カット', len(cuts), '行', sum(len(c['say']) for c in cuts))


def show(path, a, b):
    for c in parse(path):
        if key(a) <= key(c['id']) <= key(b):
            print('\n'.join(x for x in c['raw'] if x.strip()))
            print()


def selftest():
    import os
    v1 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'daihon_v1.md')
    cuts = parse(v1)
    ok = len(cuts) == 242 and cuts[0]['id'] == 'c101' and cuts[-1]['id'] == 'cb14'
    ok &= sum(len(c['say']) for c in cuts) == 564
    ok &= sum(1 for c in cuts for s in c['say'] if s.startswith('Q:')) == 64
    ok &= cuts[4]['say'][0].startswith('Q:')                      # c105 の頭は聞き役
    print('カット', len(cuts), '行', sum(len(c['say']) for c in cuts), '聞き役',
          sum(1 for c in cuts for s in c['say'] if s.startswith('Q:')), '→', 'selftest OK' if ok else 'selftest ✗')
    return 0 if ok else 1


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == '--selftest':
        sys.exit(selftest())
    if a[0] == 'narr':
        narr(a[1], a[2])
    elif a[0] == 'show':
        show(a[1], a[2], a[3] if len(a) > 3 else a[2])
