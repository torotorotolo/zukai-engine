# -*- coding: utf-8 -*-
"""20本目④'：係の所見（findings_G*.json）と G0 の決め（decisions20.json）から、短い一覧・差し替え表・台帳を組む。

  python ref/ep20/v2_build/ledger20.py brief [--sev 🔴] [--group G3] [--undecided] [--w 110]   # 所見を1行ずつ短く
  python ref/ep20/v2_build/ledger20.py patches     # → patches20.json（採る＝係の old/new・一部＝決めの old/new・G0 の足し＝patches_g0.json）
  python ref/ep20/v2_build/ledger20.py ledger      # → ledger20.md（1行1所見・扱いと理由）

decisions20.json＝{"G3-004": {"v": "採る|一部|採らない|今のまま|映像方針へ|済み", "note": "理由", "cut": "…", "old": "…", "new": "…"}, …}
  - 「一部」は old/new を必ず書く（係の案の文は採らない）。cut を省けば所見の cut。
  - 1つの所見を2つの差し替えに割るときは "patches": [{"cut","old","new"}, …]。
patches_g0.json＝G0（自分）が足す差し替え（id は G0-NNN）。
台帳はここから組む（手で写さない）。
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ORDER_RE = re.compile(r'c([0-9a-c])(\d{2})')


def load_findings():
    out = []
    files = sorted(glob.glob(os.path.join(HERE, 'findings_G*.json'))) + sorted(glob.glob(os.path.join(HERE, 'review_R*.json')))
    for f in files:
        g = os.path.basename(f).split('_')[1][:-5]
        try:
            arr = json.load(open(f, encoding='utf-8'))
        except Exception as e:  # 壊れた JSON は止める（黙って飛ばさない）
            print('🔴 読めない:', f, e)
            sys.exit(2)
        for x in arr:
            x['_g'] = g
            out.append(x)
    return out


def load_dec():
    p = os.path.join(HERE, 'decisions20.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def cutkey(c):
    m = ORDER_RE.search(c or '')
    if not m:
        return (9, c or '')
    ch = m.group(1)
    return ('123456789abc'.index(ch) if ch in '123456789abc' else 8, m.group(2))


def short(s, w):
    s = (s or '').replace('\n', '／')
    return s if len(s) <= w else s[:w] + '…'


def brief(a):
    w = int(a[a.index('--w') + 1]) if '--w' in a else 110
    sev = a[a.index('--sev') + 1] if '--sev' in a else None
    grp = a[a.index('--group') + 1] if '--group' in a else None
    und = '--undecided' in a
    dec = load_dec()
    fs = load_findings()
    n = 0
    for x in sorted(fs, key=lambda x: (cutkey(x.get('cut')), x.get('id', ''))):
        if sev and x.get('sev') != sev:
            continue
        if grp and x['_g'] != grp:
            continue
        if und and x.get('id') in dec:
            continue
        n += 1
        d = dec.get(x.get('id'), {}).get('v', '')
        print('%s｜%s｜%s｜%s｜%s｜%s ⇒ %s｜Δ%s%s' % (
            x.get('id'), x.get('cut'), x.get('sev'), x.get('kind'), short(x.get('problem'), w),
            short(x.get('old'), 40), short(x.get('new'), 60), x.get('delta'), ('｜扱い=' + d) if d else ''))
    tot = {}
    for x in fs:
        tot[x.get('sev')] = tot.get(x.get('sev'), 0) + 1
    print('== 出した %d 件／全 %d 件 %s／決め %d 件' % (n, len(fs), tot, len(dec)))


def patches(a):
    dec = load_dec()
    fs = {x['id']: x for x in load_findings()}
    out, miss = [], []
    for pid, d in dec.items():
        v = d.get('v')
        if v not in ('採る', '一部'):
            continue
        f = fs.get(pid)
        if f is None:
            miss.append(pid)
            continue
        why = '%s（%s）' % (d.get('note') or f.get('why', ''), f.get('kind'))
        if d.get('patches'):
            for k, p in enumerate(d['patches']):
                out.append({'id': '%s.%d' % (pid, k + 1), 'cut': p.get('cut', f['cut']), 'old': p['old'], 'new': p['new'],
                            'why': why, **({'noflag': True} if p.get('noflag') else {})})
            continue
        if v == '一部':
            out.append({'id': pid, 'cut': d.get('cut', f['cut']), 'old': d['old'], 'new': d['new'], 'why': why,
                        **({'noflag': True} if d.get('noflag') else {})})
        else:
            out.append({'id': pid, 'cut': d.get('cut', f['cut']), 'old': d.get('old', f['old']), 'new': d.get('new', f['new']),
                        'why': why, **({'noflag': True} if d.get('noflag') else {})})
    g0 = os.path.join(HERE, 'patches_g0.json')
    if os.path.exists(g0):
        out += json.load(open(g0, encoding='utf-8'))
    out.sort(key=lambda p: (cutkey(p['cut']), p.get('order', 50), p['id']))
    json.dump(out, open(os.path.join(HERE, 'patches20.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('patches20.json に %d 件' % len(out), '／🔴 決めに書いたのに所見が無い id:' if miss else '', miss or '')
    return 1 if miss else 0


def ledger(a):
    dec = load_dec()
    fs = load_findings()
    rows = ['| id | カット | 段 | 型 | 所見（要約） | 扱い | 理由・どう直したか |', '|---|---|---|---|---|---|---|']
    cnt = {}
    for x in sorted(fs, key=lambda x: (cutkey(x.get('cut')), x.get('id', ''))):
        d = dec.get(x.get('id'), {})
        v = d.get('v', '（未決）')
        cnt[v] = cnt.get(v, 0) + 1
        rows.append('| %s | %s | %s | %s | %s | %s | %s |' % (
            x.get('id'), x.get('cut'), x.get('sev'), x.get('kind'), short(x.get('problem'), 140).replace('|', '／'),
            v, short(d.get('note', ''), 160).replace('|', '／')))
    head = ['# 20本目 ④\' 所見の台帳（ledger20.py が findings_G*.json と decisions20.json から組む・手で直さない）', '',
            '扱いの数：' + '・'.join('%s %d' % (k, n) for k, n in sorted(cnt.items())), '']
    open(os.path.join(HERE, 'ledger20.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(head + rows) + '\n')
    print('ledger20.md', len(fs), '件', cnt)
    return 1 if '（未決）' in cnt else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    sys.exit({'brief': brief, 'patches': patches, 'ledger': ledger}[a[0]](a) or 0)
