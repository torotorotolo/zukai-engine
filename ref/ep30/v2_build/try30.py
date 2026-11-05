# -*- coding: utf-8 -*-
"""30本目④'：直す係の差し替えを第1版の写しに当てて門番を回す「試し組み」（第1版は読むだけ・書き換えない・26本目 try26.py の考えを写した）。
差し替えは標準入力の JSON で渡す（係はファイルを書かない）。

  python -I -X utf8 ref/ep30/v2_build/try30.py --tag F3 --cover c7 <<'EOF'
  [{"id":"F3-001","cut":"c711","old":"…","new":"…","why":"…","from":["G3-001"],"role":"質問"}]
  EOF

  python -I -X utf8 ref/ep30/v2_build/try30.py --tag ALL --file ref/ep30/v2_build/patches30.json   # 全部を重ねて見る（親）

すること：
 1. 形＝id・cut・old・new があるか。build30_v2.apply と同じ当て方（old がカットの塊にちょうど1回）。
 2. new の語りの行＝1行41字まで・聞き役（`> Q: `）の行に数字（漢数字も）が無い・「死亡」が無い・カンマが無い。
 3. 当てた写しを %TEMP%/ep30_try_<tag>.md に書き（リポの外）、役割表を作り（roles_map.json に各件の "role"＝質問・まとめ・反応・なし を重ねる）、
    m30v2.py（字数・尺・冒頭・聞き役・線・名前）と tools/check_script.py（形）を回す。
 4. 出すのは E・字数（第1版との差・幅の上限 13,505 までの残り）・冒頭の秒（c105 は46秒まで）・聞き役の数・当てたカットの W。--cover c7 は、その章だけの字の増減も出す。
終了コード 0＝E なし（check_script の尺の既知の E は除く）／1＝E か当て損ないがある
"""
import json
import os
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build30_v2 as B             # noqa: E402

EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
NUM = re.compile(r'[0-9０-９一二三四五六七八九十百千万〇零壱弐参]')
PUNCT = set('、。？！「」（）・')
V1_CHARS, HI, OPEN_MAX = 13471, 13505, 46.0
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
BASE = os.path.join(HERE, 'patches_base.json')


def clean(x):
    return re.sub(r'^>\s?(?:Q:\s)?', '', x.strip())


def chap_chars(lines):
    out, cur, on = {}, None, False
    for ln in lines:
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        if not on:
            continue
        m = CUT.match(ln)
        if m:
            cur = m.group(1)[:2]
        elif cur and ln.startswith('>'):
            out[cur] = out.get(cur, 0) + sum(1 for ch in clean(ln) if ch not in PUNCT)
    return out


def main():
    a = sys.argv[1:]
    tag = a[a.index('--tag') + 1] if '--tag' in a else 'T'
    cover = a[a.index('--cover') + 1].split(',') if '--cover' in a else []
    if '--file' in a:
        patches = json.load(open(a[a.index('--file') + 1], encoding='utf-8'))
    else:
        patches = json.loads(sys.stdin.read())
    base = []
    if '--nobase' not in a and os.path.exists(BASE):   # 親の差し替えを先に当てる（係の old はこの上に当たる）
        base = json.load(open(BASE, encoding='utf-8'))
    patches = base + patches
    errs = []
    for p in patches:
        if p.get('move_after'):
            continue
        for k in ('id', 'cut', 'old', 'new'):
            if k not in p:
                errs.append('E %s に %s が無い' % (p.get('id'), k))
        for ln in str(p.get('new', '')).split('\n'):
            if ln.startswith('>') or '> ' in ln[:2]:
                t = clean(ln)
                if len(t) > 41:
                    errs.append('E %s 1行%d字: %s' % (p.get('id'), len(t), t))
                if ln.startswith('> Q:') and NUM.search(t):
                    errs.append('E %s 聞き役の行に数字: %s' % (p.get('id'), t))
        if '死亡' in str(p.get('new', '')):
            errs.append('E %s 「死亡」' % p.get('id'))
    v1 = open(B.V1, encoding='utf-8').read().split('\n')
    lines, done, skipped, bad, touched = B.apply(patches, v1)
    print('当てた %d・二重なので当てない %d・当て損ない %d／語りか画が変わったカット %d' % (done, skipped, len(bad), len(set(touched))))
    for b in bad:
        errs.append('E 当て損ない ' + b)
    tmp = tempfile.gettempdir()
    md = os.path.join(tmp, 'ep30_try_%s.md' % tag)
    open(md, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    rmap = json.load(open(os.path.join(HERE, 'roles_map.json'), encoding='utf-8'))
    for p in patches:
        if p.get('role'):
            if p['role'] == 'なし' or p['role'] == '質問':
                rmap.pop(p['cut'], None)
            else:
                rmap[p['cut']] = p['role']
    mp = os.path.join(tmp, 'ep30_try_%s_roles.json' % tag)
    json.dump(rmap, open(mp, 'w', encoding='utf-8'), ensure_ascii=False)
    rt = os.path.join(tmp, 'ep30_try_%s_roles.tsv' % tag)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'roles30_v2.py'), md, rt, '--map', mp], cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        errs.append('E 役割表: ' + (r.stdout + r.stderr).strip()[-200:])
    r = subprocess.run([sys.executable, os.path.join(HERE, 'm30v2.py'), md, '--roles', rt], cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    txt = r.stdout + r.stderr
    tc = set(touched)
    m = re.search(r'＝(\d+)字（目標', txt)
    n = int(m.group(1)) if m else -1
    print('字数 %d（第1版 %d から %+d・上限 %d まで %d）' % (n, V1_CHARS, n - V1_CHARS, HI, HI - n))
    if n > HI and tag == 'ALL':
        errs.append('E 字数 %d が上限 %d を超えた' % (n, HI))
    o = dict(re.findall(r'(c10[1-7])=([\d.]+)s', txt))
    print('冒頭 c105=%s秒（%d秒まで）・c107=%s秒' % (o.get('c105'), OPEN_MAX, o.get('c107')))
    if o.get('c105') and float(o['c105']) > OPEN_MAX:
        errs.append('E 冒頭の引き c105 の終わり %s秒が46秒を超えた' % o['c105'])
    for ln in txt.split('\n'):
        if ln.startswith('聞き役:'):
            print(ln[:170])
        if ln.startswith('🔴') or ln.strip().startswith('🔴'):
            errs.append(ln.strip())
        elif ln.startswith('⚠️'):
            cs = re.findall(r'c[0-9a-d]\d{2}', ln)
            if cs and cs[0] in tc:
                print(ln[:150])
    if cover:
        c0, c1 = chap_chars(v1), chap_chars(lines)
        cb = chap_chars(B.apply(base, v1)[0])
        print('章の字の増減（第1版から）: ' + '・'.join('%s %+d' % (c, c1.get(c, 0) - c0.get(c, 0)) for c in cover))
        print('章の字の増減（親の差し替えのあとから＝この係のぶん）: ' + '・'.join('%s %+d' % (c, c1.get(c, 0) - cb.get(c, 0)) for c in cover))
    r2 = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'check_script.py'), md], cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    for ln in (r2.stdout + r2.stderr).split('\n'):
        s = ln.strip()
        if s.startswith('🔴 E') and '尺 ' not in s:
            errs.append('check_script ' + s)
    for e in errs:
        print('🔴', e)
    print('E %d件' % len(errs))
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
