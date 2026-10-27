# -*- coding: utf-8 -*-
"""26本目④'：直す係の扱いの表（fix_*.json）を第1版の写しに当てて門番を回す「試し組み」（25本目 try25.py を写し、
m26・roles26_v2・namecheck26 と、26本目の冒頭〈引き＝c105〉に替えた）。第1版は読むだけ・書き換えない。

  python -P ref/ep26/v2_build/try26.py --fix ref/ep26/v2_build/fix_G3.json [--fix …] [--tag G3] [--cover c6]
  python -P ref/ep26/v2_build/try26.py --allfix [--tag ALL]          # fix_*.json を全部重ねる（全体の字数・冒頭の秒を見る）

すること：
 1. 扱いの表の形（v の字・採る/一部なら patches）を確かめる。--cover c6 なら、その章の所見で扱いが無い id を出す（E）。
 2. patches の old が、そのカットの塊にちょうど1回あるか（build26_v2.apply と同じ当て方）。
 3. new の語りの行：1行41字まで・聞き役（`> Q: `）の行に数字（漢数字も）が無い・「死亡」が無い・
    カットの中の途中の行は「、」か「。」で終える（check_script の形の E を先に当てる）。
 4. 当てた写しを %TEMP%/ep26_try_<tag>.md に書き、役割表を作り直して（roles_map.json＋扱いの表の "role"）、
    m26.py（字数・尺・冒頭・聞き役・名前・言わない語）と tools/check_script.py（形）と名前の網を回す。
    出すのは E・字数（第1版との差・上限 13,505 までの残り）・冒頭の秒（引き c105 は46秒まで）・当てたカットの W。
扱いの表に "role": "質問|まとめ|反応|なし" を書くと、そのカットの聞き役の役割を替える（なし＝聞き役の行を消したとき）。
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
import build26_v2 as B             # noqa: E402
import ledger26 as L               # noqa: E402
import roles26_v2 as R             # noqa: E402

NUM_RE = re.compile(r'[0-9０-９一二三四五六七八九十百千万〇零壱弐参]')
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
CUT_IN = re.compile(r'\b(c[0-9a-d]\d{2})\b')
V1_CHARS, HI, OPEN_MAX = 13475, 13505, 46.0
HOOK = 'c105'                      # 冒頭の引き「調べた2人の見方が、2つに割れた」＝46秒より前（ルール 4-7）


def from_fix(fixfiles):
    fs = {x['id']: x for x in L.load_findings()}
    out, errs, roles, seen = [], [], {}, set()
    for ff in fixfiles:
        try:
            fx = json.load(open(ff, encoding='utf-8'))
        except Exception as e:
            errs.append('JSON が読めない %s: %s' % (ff, e))
            continue
        for pid, d in fx.items():
            if pid == '_extra':
                for e in d:
                    if e['id'] in seen:
                        errs.append('%s: id が重なっている' % e['id'])
                    seen.add(e['id'])
                    out.append({'id': e['id'], 'cut': e['cut'], 'old': e['old'], 'new': e['new'], 'order': e.get('order', 60)})
                    if e.get('role'):
                        roles[e['cut']] = e['role']
                continue
            seen.add(pid)
            v = d.get('v')
            if v not in L.VS:
                errs.append('%s: v の字が違う（%s）' % (pid, v))
                continue
            if pid not in fs and not pid.startswith('G0'):
                errs.append('%s: 所見が無い id' % pid)
                continue
            if d.get('role'):
                roles[(d.get('patches') or [{}])[0].get('cut') or fs[pid]['cut']] = d['role']
            if v not in ('採る', '一部'):
                continue
            ps = d.get('patches') or []
            if not ps:
                errs.append('%s: %s なのに patches が無い' % (pid, v))
            for k, p in enumerate(ps):
                out.append({'id': '%s.%d' % (pid, k + 1) if len(ps) > 1 else pid, 'cut': p.get('cut') or fs[pid]['cut'],
                            'old': p['old'], 'new': p['new'], 'order': p.get('order', 99 if pid.startswith('R') else 50)})
    return out, errs, roles, seen


def check_new(p, errs):
    say = [ln for ln in (p['new'] or '').split('\n') if ln.startswith('>')]
    for ln in say:
        body = ln[1:].strip()
        if body.startswith('Q:'):
            b2 = body[2:].strip()
            if NUM_RE.search(b2):
                errs.append('%s %s: 聞き役の行に数字（漢数字も）: %s' % (p['id'], p['cut'], b2))
            body = b2
        if len(body) > 41:
            errs.append('%s %s: 1行 %d字（41字まで）: %s' % (p['id'], p['cut'], len(body), body))
        if '死亡' in body:
            errs.append('%s %s: 「死亡」' % (p['id'], p['cut']))


def shape_of_cut(lines, blk, cut, errs):
    a, b = blk[cut]
    say = [x[1:].strip() for x in lines[a + 1:b] if x.startswith('>')]
    for k, s in enumerate(say[:-1]):
        if not s.endswith(('、', '。', '？', '！')):
            errs.append('%s: 途中の行が「、」「。」で終わっていない: %s' % (cut, s[-20:]))


def run(args):
    r = subprocess.run([sys.executable] + args, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def main():
    a = sys.argv[1:]
    tag = a[a.index('--tag') + 1] if '--tag' in a else 'try'
    fixfiles = [a[i + 1] for i, x in enumerate(a) if x == '--fix']
    if '--allfix' in a:
        fixfiles = sorted(glob.glob(os.path.join(HERE, 'fix_*.json')))
    patches, errs, roles, seen = from_fix(fixfiles)
    if '--cover' in a:
        pre = tuple(a[a.index('--cover') + 1].split(','))
        miss = sorted(i for i, x in ((x['id'], x) for x in L.load_findings()) if (x.get('cut') or '').startswith(pre) and i not in seen)
        print('担当 %s の所見で扱いが無い id: %d %s' % ('・'.join(pre), len(miss), ' '.join(miss)))
        if miss:
            errs.append('扱いが無い所見 %d 件' % len(miss))
    for p in patches:
        check_new(p, errs)
    patches.sort(key=lambda p: (L.cutkey(p['cut']), p['order'], p['id']))
    v1 = open(B.V1, encoding='utf-8').read().split('\n')
    lines, done, skipped, bad, touched = B.apply(patches, v1)
    blk = B.blocks(lines)
    for c in sorted(set(p['cut'] for p in patches if p['cut'] in blk)):
        shape_of_cut(lines, blk, c, errs)
    tmp = os.path.join(tempfile.gettempdir(), 'ep26_try_%s.md' % tag)
    open(tmp, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    role_map = json.load(open(os.path.join(HERE, 'roles_map.json'), encoding='utf-8'))
    for c, r in roles.items():
        if r in ('質問', 'なし'):
            role_map.pop(c, None)
        elif r in ('まとめ', '反応'):
            role_map[c] = r
        else:
            errs.append('%s: role の字が違う（%s）' % (c, r))
    rtmp = os.path.join(tempfile.gettempdir(), 'ep26_try_%s_roles.tsv' % tag)
    rows = R.rows_of(tmp, role_map)
    with open(rtmp, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 試し組みの役割表\n')
        for cid, role, text in rows:
            f.write('%s\t%s\t%s\n' % (cid, role, text))
    print('扱いの表 %d・差し替え %d → 当てた %d・二重 %d・当て損ない %d・🔧 %d／写し %s' % (
        len(fixfiles), len(patches), done, skipped, len(bad), len(touched), tmp))
    for b in bad:
        print('  ✗', b)
    for e in errs:
        print('  ✗', e)
    tset = set(touched)
    nE = len(bad) + len(errs)
    rc, out = run([os.path.join(EP, 'v1_build', 'm26.py'), tmp, '--roles', rtmp])
    print('── m26（exit=%d）' % rc)
    m = re.search(r'＝(\d+)字（目標', out)
    o = dict(re.findall(r'(c10[1-7])=([\d.]+)s', out))
    if not m or HOOK not in o:
        print('  🔴 m26 の出力が読めない（字数か冒頭の秒が無い）')
        nE += 1
    else:
        n = int(m.group(1))
        print('  字数 %d（第1版 %d から %+d・上限 %d まで %d）／冒頭の引き %s=%s秒（%.0f秒まで）・c107=%s秒' % (
            n, V1_CHARS, n - V1_CHARS, HI, HI - n, HOOK, o[HOOK], OPEN_MAX, o.get('c107')))
        if n > HI:
            print('  🔴 字数が上限を越えた')
            nE += 1
        if float(o[HOOK]) > OPEN_MAX:
            print('  🔴 %s（冒頭の引き）が46秒を越えた' % HOOK)
            nE += 1
    for k, ln in enumerate(out.split('\n')):
        cut = CUT_IN.search(ln)
        if k < 4 or ln.startswith('聞き役:') or ln.startswith('名前') or ln.startswith('E ') or '🔴' in ln \
                or ('役割' in ln and '⚠️' in ln) or (cut and cut.group(1) in tset and '模式' not in ln and '写真の点' not in ln):
            print('  ' + ln)
    if rc != 0:
        nE += 1
    mE = re.search(r'E (\d+)件（形）・聞き役 E (\d+)件', out)
    if mE and (int(mE.group(1)) or int(mE.group(2))):
        nE += int(mE.group(1)) + int(mE.group(2))
    rc, out = run([os.path.join(REPO, 'tools', 'check_script.py'), tmp])
    print('── check_script（尺の E は既知＝数えない・秒は m26 で見る）')
    for ln in out.split('\n'):
        cut = CUT_IN.search(ln)
        if '🔴 E' in ln and '尺' not in ln:
            print('  ' + ln)
            nE += 1
        elif cut and cut.group(1) in tset and ('⚠️' in ln or '🔴' in ln):
            print('  ' + ln)
        elif ln.startswith('E '):
            print('  ' + ln)
    rc, out = run([os.path.join(HERE, 'namecheck26.py'), tmp] + fixfiles)
    print('── 名前の網（exit=%d）' % rc)
    print('  ' + out.strip().replace('\n', '\n  '))
    if rc != 0:
        nE += 1
    print('== E（当て損ない・形・門番）%d 件' % nE)
    return 1 if nE else 0


if __name__ == '__main__':
    sys.exit(main())
