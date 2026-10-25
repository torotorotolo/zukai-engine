# -*- coding: utf-8 -*-
"""25本目④'：係の所見（findings_G*.json・review_R*.json）と扱いの表（fix_G*.json・fix_R*.json）から、
短い一覧・差し替え表・台帳を組む（24本目 ledger24.py の考え方を、25本目の所見の形〈now・orig・why・fix・delta〉と
直す係の扱いの表〈fix_*.json〉に替えた）。台帳はここから組む（手で写さない）。

  python ref/ep25/v2_build/ledger25.py brief [--sev 🔴] [--group G3] [--cover c5,c6] [--undecided] [--w 110]
  python ref/ep25/v2_build/ledger25.py show --cover c5            # 担当の章の所見を全部の欄で（直す係が読む）
  python ref/ep25/v2_build/ledger25.py patches                    # → patches25.json（扱いの表の patches と _extra を全部）
  python ref/ep25/v2_build/ledger25.py ledger                     # → ledger25.md（1行1所見・扱いと理由）

扱いの表 fix_<係>.json＝{"G3-004": {"v": "採る|一部|採らない|今のまま|映像方針へ|済み|親へ", "note": "理由",
    "patches": [{"cut": "c512", "old": "…", "new": "…"}], "role": "質問|まとめ|反応|なし"}, …,
    "_extra": [{"id": "F3-001", "cut": "…", "old": "…", "new": "…", "what": "所見に無い直し（字数の調整・橋）", "role": "…"}]}
  - 採る・一部は patches を必ず書く（係の案の文をそのまま使うときも old/new で）。採らない・今のまま・映像方針へ・済み・親へは patches なし。
  - "order"（数・既定50）を patches の1件に書くと、同じカットの中の当てる順を決める（当て直し＝99）。
ledger_ovr.json＝{"G3-004": {"v": "…", "note": "…"}}＝G0（④'の本人）が中身を見て扱いを上書きする（「一部だけ採った」の書き方の揺れを正す）。
g0_ledger.json＝G0 自身の所見（[{"id": "G0-001", "cut", "sev", "face", "why", "v", "note"}]）。
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ORDER_RE = re.compile(r'c([0-9a-d])(\d{2})')
VS = ('採る', '一部', '採らない', '今のまま', '映像方針へ', '済み', '親へ')


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
        if isinstance(arr, dict):
            arr = arr.get('findings', [])
        for x in arr:
            x['_g'] = g
            out.append(x)
    return out


def load_fix():
    """id → 扱い（fix_*.json を全部・あとのファイルが勝つ）＋ _extra の並び。"""
    dec, extra = {}, []
    for f in sorted(glob.glob(os.path.join(HERE, 'fix_*.json'))):
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print('🔴 読めない:', f, e)
            sys.exit(2)
        for k, v in d.items():
            if k == '_extra':
                extra += [dict(e, _file=os.path.basename(f)) for e in v]
            else:
                dec[k] = dict(v, _file=os.path.basename(f))
    ovr = os.path.join(HERE, 'ledger_ovr.json')
    if os.path.exists(ovr):
        for k, v in json.load(open(ovr, encoding='utf-8')).items():
            dec[k] = dict(dec.get(k, {}), **v)
    return dec, extra


def cutkey(c):
    m = ORDER_RE.search(c or '')
    if not m:
        return (99, c or '')
    return ('123456789abcd'.index(m.group(1)), m.group(2))


def short(s, w):
    s = str(s or '').replace('\n', '／')
    return s if len(s) <= w else s[:w] + '…'


def brief(a):
    w = int(a[a.index('--w') + 1]) if '--w' in a else 110
    sev = a[a.index('--sev') + 1] if '--sev' in a else None
    grp = a[a.index('--group') + 1] if '--group' in a else None
    pre = tuple(a[a.index('--cover') + 1].split(',')) if '--cover' in a else None
    und = '--undecided' in a
    dec, _ = load_fix()
    fs = load_findings()
    n = 0
    for x in sorted(fs, key=lambda x: (cutkey(x.get('cut')), x.get('id', ''))):
        if sev and x.get('sev') != sev:
            continue
        if grp and x['_g'] != grp:
            continue
        if pre and not (x.get('cut') or '').startswith(pre):
            continue
        if und and x.get('id') in dec:
            continue
        n += 1
        d = dec.get(x.get('id'), {}).get('v', '')
        print('%s｜%s｜%s｜%s・%s｜%s｜原文 %s｜案 %s%s' % (
            x.get('id'), x.get('cut'), x.get('sev'), x.get('face'), x.get('type'), short(x.get('why'), w),
            short(x.get('src'), 30), short(x.get('fix'), 70), ('｜扱い=' + d) if d else ''))
    tot = {}
    for x in fs:
        tot[x.get('sev')] = tot.get(x.get('sev'), 0) + 1
    print('== 出した %d 件／全 %d 件 %s／扱い %d 件' % (n, len(fs), tot, len(dec)))


def show(a):
    pre = tuple(a[a.index('--cover') + 1].split(','))
    fs = [x for x in load_findings() if (x.get('cut') or '').startswith(pre)]
    for x in sorted(fs, key=lambda x: (cutkey(x.get('cut')), x.get('id', ''))):
        print('=== %s｜%s｜%s｜%s・%s｜%+d字%s' % (x['id'], x['cut'], x['sev'], x.get('face'), x.get('type'), int(x.get('delta') or 0),
                                         ('｜§0-1 の' + x['point']) if x.get('point') else ''))
        for k in ('now', 'src', 'orig', 'why', 'fix'):
            if x.get(k):
                print('%s: %s' % (k, x[k]))
    print('== %d 件（%s）' % (len(fs), '・'.join(pre)))


def patches(a):
    dec, extra = load_fix()
    fs = {x['id']: x for x in load_findings()}
    out, errs = [], []
    for pid, d in dec.items():
        v = d.get('v')
        if v not in VS:
            errs.append('%s: v の字が違う（%s）' % (pid, v))
            continue
        if pid not in fs and not pid.startswith('G0'):
            errs.append('%s: 所見が無い id（%s）' % (pid, d.get('_file')))
            continue
        if v not in ('採る', '一部'):
            continue
        ps = d.get('patches') or []
        if not ps:
            errs.append('%s: %s なのに patches が無い' % (pid, v))
            continue
        why = d.get('note') or (fs.get(pid) or {}).get('why', '')
        for k, p in enumerate(ps):
            cut = p.get('cut') or (fs.get(pid) or {}).get('cut')
            out.append({'id': '%s.%d' % (pid, k + 1) if len(ps) > 1 else pid, 'cut': cut, 'old': p['old'], 'new': p['new'],
                        'why': why, 'order': p.get('order', 99 if pid.startswith('R') else 50)})
    for e in extra:
        out.append({'id': e['id'], 'cut': e['cut'], 'old': e['old'], 'new': e['new'], 'why': e.get('what', ''),
                    'order': e.get('order', 99 if e['id'].startswith('R') else 60)})
    out.sort(key=lambda p: (cutkey(p['cut']), p.get('order', 50), p['id']))
    json.dump(out, open(os.path.join(HERE, 'patches25.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('patches25.json に %d 件' % len(out))
    for e in errs:
        print('  ✗', e)
    return 1 if errs else 0


def ledger(a):
    dec, extra = load_fix()
    fs = load_findings()
    g0f = os.path.join(HERE, 'g0_ledger.json')
    g0 = json.load(open(g0f, encoding='utf-8')) if os.path.exists(g0f) else []
    rows = ['| id | カット | 段 | 面・型 | 所見（要約） | 扱い | 理由・どう直したか |', '|---|---|---|---|---|---|---|']
    cnt = {}
    for x in sorted(fs + g0, key=lambda x: (cutkey(x.get('cut')), x.get('id', ''))):
        d = {'v': x.get('v', '採る'), 'note': x.get('note', '')} if x.get('id', '').startswith('G0-') else dec.get(x.get('id'), {})
        v = d.get('v', '（未決）')
        cnt[v] = cnt.get(v, 0) + 1
        rows.append('| %s | %s | %s | %s・%s | %s | %s | %s |' % (
            x.get('id'), x.get('cut'), x.get('sev'), x.get('face', ''), x.get('type', ''), short(x.get('why'), 150).replace('|', '／'),
            v, short(d.get('note', ''), 170).replace('|', '／')))
    rows += ['', '## 所見に無い直し（直す係の _extra）', '', '| id | カット | 何を | 置いたファイル |', '|---|---|---|---|']
    for e in sorted(extra, key=lambda e: (cutkey(e['cut']), e['id'])):
        rows.append('| %s | %s | %s | %s |' % (e['id'], e['cut'], short(e.get('what'), 150).replace('|', '／'), e['_file']))
    sev = {}
    for x in fs + g0:
        sev[x.get('sev')] = sev.get(x.get('sev'), 0) + 1
    head = ['# 25本目 ④\' 所見の台帳（ledger25.py が findings_G*.json・review_R*.json・g0_ledger.json と fix_*.json・ledger_ovr.json から組む・手で直さない）', '',
            '段の数：' + '・'.join('%s %d' % (k, n) for k, n in sorted(sev.items())) + '／扱いの数：' +
            '・'.join('%s %d' % (k, n) for k, n in sorted(cnt.items())) + '／所見に無い直し %d' % len(extra), '']
    open(os.path.join(HERE, 'ledger25.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(head + rows) + '\n')
    print('ledger25.md', len(fs) + len(g0), '件', cnt, '／_extra', len(extra))
    return 1 if '（未決）' in cnt else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    sys.exit({'brief': brief, 'show': show, 'patches': patches, 'ledger': ledger}[a[0]](a) or 0)
