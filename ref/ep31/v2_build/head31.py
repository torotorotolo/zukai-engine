# -*- coding: utf-8 -*-
"""31本目④'：第2版の頭と §0（v2_build/v2_head.md）を、ひな形 v2_head_tmpl.md と門番の出力（gates.md）・台帳（ledger31.md）・差し替え表から組む（数を手で写さない）。

  python -P ref/ep31/v2_build/head31.py [--c "C_TOKENS=…;C_TOOLS=…;C_MIN=…;C_LEAKS=…"]

順番＝final31.py（gates.md）→ この道具 → build31_v2.py（v2_head.md を頭に差す）→ final31.py → この道具（2周目は同じ字になるはず）。
§4（本文）の数は頭に左右されない＝2周目も同じ。差し込めない札（{{…}}）が残れば止める（fail closed）。
"""
import hashlib
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
ORDER = '123456789abcd'


def section(g, name):
    m = re.search(r'^## %s（exit=(\d+)）\n```\n(.*?)\n```' % re.escape(name), g, re.S | re.M)
    return (int(m.group(1)), m.group(2)) if m else (None, '')


def line(txt, pat):
    for ln in txt.split('\n'):
        if re.search(pat, ln):
            return ln.strip()
    return ''


def main():
    a = sys.argv[1:]
    extra = {}
    if '--c' in a:
        for kv in a[a.index('--c') + 1].split(';'):
            if '=' in kv:
                k, v = kv.split('=', 1)
                extra[k.strip()] = v.strip()
    g = open(os.path.join(HERE, 'gates.md'), encoding='utf-8').read()
    _, m = section(g, 'm31')
    vals = {
        'V1_MD5': hashlib.md5(open(os.path.join(EP, 'daihon_v1.md'), 'rb').read()).hexdigest(),
        'M_TOTAL': line(m, r'^カット \d+ / 行'),
        'M_PHOTO': line(m, r'^写真・映像・紙面'),
        'M_TEXT': line(m, r'^文字の頁の見込み').split(':')[0],
        'M_LINE': line(m, r'^1行 中央値'),
        'M_DUR': line(m, r'^尺 ①'),
        'M_OPEN': line(m, r'^冒頭（').split(': ', 1)[-1],
        'M_FIG': line(m, r'^図の型:'),
        'M_Q': line(m, r'^聞き役:'),
        'M_E': line(m, r'^E \d+件（形）'),
    }
    rw = [ln.strip().replace('⚠️ ', '') for ln in m.split('\n') if '役割「' in ln]
    vals['M_ROLEW'] = '・'.join(rw) if rw else '（役割の W なし）'
    _, q = section(g, 'quotes')
    vals['QUOTES'] = line(q, r'^片 \d+:')
    _, cs = section(g, 'check_script')
    vals['CS'] = '%s・%s（%s）' % (line(cs, r'^E \d+件 / W'), line(cs, r'^形の E'), line(cs, r'^🔴 E 尺').replace('🔴 ', ''))
    _, csd = section(g, 'check_script_diff')
    vals['CSD'] = '%s・%s・%s' % (line(csd, r'^カット \d+ → '), line(csd, r'^🔧 の印'), line(csd, r'欠番: '))
    _, tg = section(g, 'tags')
    vals['TAGS'] = '%s・%s' % (line(tg, r'^札 \d+種'), line(tg, r'^置き場か台帳に無い札'))
    _, so = section(g, 'sou')
    vals['SOU'] = '%s・%s' % (line(so, r'^聞き役の行 '), line(so, r'^まとめの後が'))
    _, nm = section(g, 'namecheck')
    vals['NAMES'] = line(nm, r'^名前の網 ')
    _, lo = section(g, 'lost')
    vals['LOST'] = line(lo, r'^消えた語')
    mm = re.search(r'消えた語 (\d+)', vals['LOST'])
    vals['LOST_N'] = mm.group(1) if mm else '?'
    codes = re.findall(r'^## (\w+)（exit=(\d+)）', g, re.M)
    vals['GATES'] = '・'.join('%s=%s' % c for c in codes)
    led = open(os.path.join(HERE, 'ledger31.md'), encoding='utf-8').read()
    ml = re.search(r'^## 数\n(.*?)\n\n', led, re.S | re.M)
    vals['LEDGER'] = ml.group(1).strip() if ml else ''
    P = json.load(open(os.path.join(HERE, 'patches31.json'), encoding='utf-8'))
    kinds = [('親', lambda i: i.startswith('B-')), ('直す係', lambda i: re.match(r'F\d-', i)),
             ('当て直しと親の追加', lambda i: i.startswith(('R0-', 'RP-', 'C0-', 'CP-'))),
             ('§ と見出し', lambda i: re.match(r'S-\d', i) or i.startswith('S-N')), ('読み', lambda i: i == 'S-YOMI')]
    vals['NPATCH'] = '%d件＝' % len(P) + '・'.join('%s %d' % (k, sum(1 for p in P if f(p['id']))) for k, f in kinds)
    v2 = open(os.path.join(EP, 'daihon_v2.md'), encoding='utf-8').read()
    fixed = re.findall(r'^\*\*(c[0-9a-d]\d{2})\*\* 🔧', v2, re.M)
    vals['FIX_CUTS'] = '%d＝%s' % (len(fixed), '・'.join(fixed))
    allc = set(re.findall(r'^\*\*(c[0-9a-d]\d{2})\*\*', v2, re.M))
    src_only = sorted({p['cut'] for p in P if re.match(r'c[0-9a-d]\d{2}$', p['cut'])} - set(fixed) - (set(p['cut'] for p in P) - allc),
                      key=lambda c: (ORDER.index(c[1]), c))
    vals['SRC_ONLY'] = '%d＝%s' % (len(src_only), '・'.join(src_only)) if src_only else 'なし'
    for k in ('C_TOKENS', 'C_TOOLS', 'C_MIN', 'C_LEAKS'):
        vals[k] = extra.get(k, '（未）')
    t = open(os.path.join(HERE, 'v2_head_tmpl.md'), encoding='utf-8').read()
    for k, v in vals.items():
        if not v:
            print('🔴 値が読めない:', k)
            return 1
        t = t.replace('{{%s}}' % k, v)
    left = re.findall(r'\{\{[A-Z_0-9]+\}\}', t)
    if left:
        print('🔴 差し込めない札:', left)
        return 1
    out = os.path.join(HERE, 'v2_head.md')
    open(out, 'w', encoding='utf-8', newline='\n').write(t)
    print('v2_head.md を書いた（%d字・差し替え %s・🔧 %s・出典だけ %s）' % (len(t), vals['NPATCH'], len(fixed), len(src_only)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
