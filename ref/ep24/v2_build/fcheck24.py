# -*- coding: utf-8 -*-
"""24本目④'：係の所見の案（findings_G*.json）を、第1版の写しに当てて門番を回す「試し組み」（23本目 fcheck23.py を写し、m24・roles24・名前の網に替えた）。

  python ref/ep24/v2_build/fcheck24.py ref/ep24/v2_build/findings_G1.json [ほかの findings …] [--tag G1]
  python ref/ep24/v2_build/fcheck24.py --fix ref/ep24/v2_build/fix_G1.json [--fix …] [--tag F1] [--cover c1,c2]   # 直す係の扱いで組む
  python ref/ep24/v2_build/fcheck24.py --allfix [--tag ALL]                                                  # fix_G*.json を全部重ねる

fix_Gn.json＝{"G1-003": {"v": "採る|一部|採らない|今のまま|映像方針へ|済み|親へ", "note": "理由", "old": "…", "new": "…", "cut": "…",
               "patches": [{"cut","old","new"}, …], "role": "…"}, …, "_extra": [{"id": "F1-001", "cut": "…", "old": "…", "new": "…", "what": "…"}]}
  採る＝所見の old/new（"new" を書けばそれに替える）／一部＝決めの old/new か patches／_extra＝所見に無い直し（字数の調整・橋）。

すること（第1版は読むだけ・書き換えない）：
 1. 所見の形（id・cut・face・sev・what・evidence・old・new）を確かめる。old が空の所見（直しの案なし＝要確認・親へ）は当てない。
 2. old が、そのカットの塊にちょうど1回あるか（build24_v2.apply と同じ当て方）。
 3. 案の new の行：語りの1行41字まで・聞き役（`> Q: `）の行に数字（漢数字も＝check_listener と同じ）が無い・「死亡」が無い。
 4. 当てた写しを %TEMP%/ep24_try_<tag>.md に書き、聞き役の役割表を作り直して（第1版の役割＋所見の "role"）、
    m24.py（字数・尺・冒頭・聞き役・名前・言わない語）と tools/check_script.py（形）と名前の網を回す。出すのは E と、当てたカットの W と要約だけ。
 所見に "role": "質問|まとめ|反応|なし" を書くと、そのカットの聞き役の役割を替える（なし＝聞き役の行を消したとき）。
終了コード 0＝E なし（check_script の尺の既知の E は除く）／1＝E か当て損ないがある
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(EP, 'v1_build'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import build24_v2 as B             # noqa: E402
import check_script as CS          # noqa: E402
import speaker                     # noqa: E402
import ledger24                    # noqa: E402

ROLE0 = json.load(open(os.path.join(HERE, 'roles_map.json'), encoding='utf-8'))   # 第1版の役割（v1_build/roles24.py の ROLE の写し）
NUM_RE = re.compile(r'[0-9０-９一二三四五六七八九十百千万]')
KEYS = ('id', 'cut', 'face', 'sev', 'what', 'evidence', 'old', 'new')
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
CUT_IN = re.compile(r'\b(c[0-9a-c]\d{2})\b')


def roles_rows(md, role_map):
    cuts = CS.parse(open(md, encoding='utf-8').read())
    rows = []
    for cid, _, ls in cuts:
        for raw in ls:
            if speaker.split(raw)[0] == speaker.WHO_Q:
                rows.append((cid, role_map.get(cid, '質問'), speaker.bare(raw.strip())))
    return rows


def all_findings():
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'findings_G*.json'))) + sorted(glob.glob(os.path.join(HERE, 'review_R*.json'))):
        for x in json.load(open(f, encoding='utf-8')):
            out[x['id']] = x
    return out


def from_fix(fixfiles):
    """直す係の扱い → 所見の形（fcheck の下の処理にそのまま流す）。"""
    fs = all_findings()
    out, errs = [], []
    for ff in fixfiles:
        fx = json.load(open(ff, encoding='utf-8'))
        for pid, d in fx.items():
            if pid == '_extra':
                for e in d:
                    out.append({'id': e['id'], 'cut': e['cut'], 'face': e.get('face', 'A'), 'sev': e.get('sev', '🟢'),
                                'what': e.get('what', ''), 'evidence': '', 'old': e['old'], 'new': e['new'],
                                **({'role': e['role']} if e.get('role') else {}),
                                **({'order': e['order']} if 'order' in e else {})})
                continue
            f = fs.get(pid)
            if f is None:
                errs.append('%s: 所見が無い id' % pid)
                continue
            v = d.get('v')
            if v not in ('採る', '一部', '採らない', '今のまま', '映像方針へ', '済み', '親へ'):
                errs.append('%s: v の字が違う（%s）' % (pid, v))
                continue
            role = {'role': d['role']} if d.get('role') else ({'role': f['role']} if f.get('role') and v == '採る' else {})
            if v not in ('採る', '一部'):
                continue
            base = {k: w for k, w in f.items() if k != 'role'}
            if d.get('patches'):
                for k, p in enumerate(d['patches']):
                    out.append(dict(base, id='%s.%d' % (pid, k + 1), cut=p.get('cut', f['cut']), old=p['old'], new=p['new'], **role))
                continue
            if v == '一部' and not (d.get('old') and 'new' in d):
                errs.append('%s: 一部なのに old/new が無い' % pid)
                continue
            out.append(dict(base, cut=d.get('cut', f['cut']), old=d.get('old', f['old']), new=d.get('new', f['new']), **role))
    return out, errs


def main():
    a = sys.argv[1:]
    tag = a[a.index('--tag') + 1] if '--tag' in a else 'try'
    fixfiles = [a[i + 1] for i, x in enumerate(a) if x == '--fix']
    if '--allfix' in a:
        fixfiles = sorted(glob.glob(os.path.join(HERE, 'fix_G*.json')))
    files = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--tag', '--fix', '--cover'))]
    fs, errs = [], []
    if fixfiles:
        fs, errs = from_fix(fixfiles)
    if '--cover' in a:
        pre = tuple(a[a.index('--cover') + 1].split(','))
        done = set()
        for ff in fixfiles:
            done |= {k for k in json.load(open(ff, encoding='utf-8')) if k != '_extra'}
        miss = sorted(i for i, x in all_findings().items() if (x.get('cut') or '').startswith(pre) and i not in done)
        print('担当 %s の所見で扱いが無い id: %d %s' % ('・'.join(pre), len(miss), ' '.join(miss)))
        if miss:
            errs.append('扱いが無い所見 %d 件' % len(miss))
    for f in files:
        try:
            arr = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print('🔴 JSON が読めない:', f, e)
            return 1
        if isinstance(arr, dict):
            arr = arr.get('findings', [])
        fs += arr
    role_map = dict(ROLE0)
    patches = []
    ids = set()
    for x in fs:
        miss = [k for k in KEYS if k not in x]
        if miss:
            errs.append('%s: 欄が無い %s' % (x.get('id'), miss))
            continue
        if x['id'] in ids:
            errs.append('%s: id が重なっている' % x['id'])
        ids.add(x['id'])
        if x['sev'] not in ('🔴', '🟡', '🟢'):
            errs.append('%s: sev は 🔴🟡🟢 のどれか' % x['id'])
        if x.get('role'):
            if x['role'] == 'なし':
                role_map.pop(x['cut'], None)
            elif x['role'] in ('質問', 'まとめ', '反応'):
                if x['role'] == '質問':
                    role_map.pop(x['cut'], None)
                else:
                    role_map[x['cut']] = x['role']
            else:
                errs.append('%s: role の字が違う' % x['id'])
        if not x['old']:
            continue
        for ln in (x['new'] or '').split('\n'):
            if not ln.startswith('> '):
                continue
            body = ln[2:]
            if body.startswith('Q: '):
                body = body[3:]
                if NUM_RE.search(body):
                    errs.append('%s %s: 聞き役の行に数字（漢数字も）: %s' % (x['id'], x['cut'], body))
            if len(body) > 41:
                errs.append('%s %s: 1行 %d字（41字まで）: %s' % (x['id'], x['cut'], len(body), body))
            if '死亡' in body:
                errs.append('%s %s: 「死亡」' % (x['id'], x['cut']))
        patches.append({'id': x['id'], 'cut': x['cut'], 'old': x['old'], 'new': x['new'],
                        'order': x.get('order', 99 if x['id'].startswith('R') else 50)})
    patches.sort(key=lambda p: (ledger24.cutkey(p['cut']), p['order'], p['id']))
    v1 = open(B.V1, encoding='utf-8').read().split('\n')
    lines, done, skipped, bad, touched = B.apply(patches, v1)
    tmp = os.path.join(tempfile.gettempdir(), 'ep24_try_%s.md' % tag)
    open(tmp, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    rtmp = os.path.join(tempfile.gettempdir(), 'ep24_try_%s_roles.tsv' % tag)
    rows = roles_rows(tmp, role_map)
    with open(rtmp, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 試し組みの役割表\n')
        for cid, role, text in rows:
            f.write('%s\t%s\t%s\n' % (cid, role, text))
    print('所見 %d・案あり %d → 当てた %d・二重 %d・当て損ない %d・🔧 %d／写し %s' % (
        len(fs), len(patches), done, skipped, len(bad), len(touched), tmp))
    for b in bad:
        print('  ✗', b)
    for e in errs:
        print('  ✗', e)
    tset = set(touched)
    nE = len(bad) + len(errs)
    r = subprocess.run([sys.executable, os.path.join(EP, 'v1_build', 'm24.py'), tmp, '--roles', rtmp],
                       cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (r.stdout or '') + (r.stderr or '')
    print('── m24（exit=%d）' % r.returncode)
    for k, ln in enumerate(out.split('\n')):
        cut = CUT_IN.search(ln)
        if k < 5 or ln.startswith('聞き役:') or ln.startswith('名前') or ln.startswith('E ') or '🔴' in ln \
                or (cut and cut.group(1) in tset and '模式' not in ln):
            print('  ' + ln)
    if r.returncode != 0:
        nE += 1
    r = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'check_script.py'), tmp],
                       cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (r.stdout or '') + (r.stderr or '')
    print('── check_script（尺の E は既知＝数えない・冒頭の秒は ElevenLabs の定数＝m24 の冒頭で見る）')
    for ln in out.split('\n'):
        cut = CUT_IN.search(ln)
        if ('E ' in ln and '尺' not in ln and not ln.startswith('E ')) or (cut and cut.group(1) in tset and ('W' in ln or 'E' in ln)):
            print('  ' + ln)
            if '🔴' in ln and '尺' not in ln:
                nE += 1
        elif ln.startswith('E '):
            print('  ' + ln)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'namecheck24.py'), tmp],
                       cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('── 名前の網（exit=%d）' % r.returncode)
    print('  ' + ((r.stdout or '') + (r.stderr or '')).strip().replace('\n', '\n  '))
    if r.returncode != 0:
        nE += 1
    print('== E（当て損ない・形・門番）%d 件' % nE)
    return 1 if nE else 0


if __name__ == '__main__':
    sys.exit(main())
