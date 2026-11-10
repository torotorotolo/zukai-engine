# -*- coding: utf-8 -*-
"""32本目④'：第2版を組んで、門番をまとめて回す（出力は v2_build/gates.md・各門番の終了コードつき・31本目 final31.py の考えを写した）。

  python -P ref/ep32/v2_build/final32.py            # patches32.json で組み直す → 門番 → 対照表 → 消えた語
  python -P ref/ep32/v2_build/final32.py --nobuild  # 組まずに門番だけ

回すもの（順番どおり・1本ずつ＝コミットの空きが少ないため）：
  1 build32_v2.py patches32.json           第2版（第1版の md5 を前後で比べる）
  2 v1_build/roles32.py daihon_v2.md v2_build/roles.tsv   聞き役の役割表（役割は行の終わりで決まる）
  3 v1_build/m32.py --selftest             m32 の陽性対照（自分の物差しを先に確かめる）
  4 v1_build/m32.py daihon_v2.md --roles   字数・尺の3通り・冒頭の秒・行の形・聞き役＝check_listener.judge・写真の割合・図の型・線・名前・帰属・時点
  5 namecheck32.py                         書かない名前＝`git ls-files ref/ep32` の全部と v2_build の全部と第2版
  6 tools/check_script.py --refcheck／daihon_v2.md   形の門番（E は尺の古い定数〈§5a-28b〉だけか）
  7 tools/check_script_diff.py v1 v2       🔧 の印と差分の一致・欠番
  8 v1_build/quotes32.py --selftest／v2 --out v2_build/quotes32_v2.tsv   出典の欄の原文の片（外れ 0）
  9 sou        聞き役の「まとめ」のあとの語りが「そう。」で受けているか
 10 internal   頭と §0 に内部の数字の語が無いか（4'-17）
 11 band       字数の幅（13,120〜13,520）と冒頭の引き（c105 が46秒まで）＝m32 の出力から
 12 make_diff32.py   第1版→第2版の対照表
 13 lost32.py        第1版の語りにあって第2版に無い語（git の外へ）
終了コード 0＝全部 E 0（check_script の尺の E だけは既知）／1＝どこかが E。
"""
import glob
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
PY = sys.executable
V1 = os.path.join(EP, 'daihon_v1.md')
V2 = os.path.join(EP, 'daihon_v2.md')
ROLES = os.path.join(HERE, 'roles.tsv')
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
LO, HI, OPEN_MAX, HOOK = 13120, 13520, 46.0, 'c105'
INTERNAL = re.compile(r'維持率|再生数|再生回数|CTR|インプレッション|クリック率|登録者|平均視聴|視聴時間|流入')


def run(args, name):
    p = subprocess.run([PY, '-P', '-X', 'utf8'] + args, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def tail(s, n=6):
    ls = [l for l in s.strip().split('\n') if l.strip()]
    return ls[-n:]


def sou_check():
    text = open(V2, encoding='utf-8').read().replace('\r\n', '\n')
    s4 = text[text.index('## 4. 台本'):text.index('\n## 5.')]
    seq = []
    cur = None
    for l in s4.split('\n'):
        m = re.match(r'^\*\*(c[0-9a-c]\d{2})\*\*', l)
        if m:
            cur = m.group(1)
            continue
        if cur and l.startswith('>'):
            seq.append((cur, l))
    bad = []
    n = 0
    for i, (c, l) in enumerate(seq):
        if l.startswith('> Q: ') and l.rstrip().endswith('ね。'):
            n += 1
            nxt = seq[i + 1][1] if i + 1 < len(seq) else ''
            if not nxt.startswith('> そう'):
                bad.append(c)
    return n, bad


def main():
    out = []
    worst = 0
    os.chdir(REPO)

    def rec(name, code, body, keep=8, ok=(0,)):
        nonlocal worst
        mark = '✓' if code in ok else '🔴'
        if code not in ok:
            worst = 1
        out.append('### %s %s（exit %s）' % (mark, name, code))
        out.append('```')
        out.extend(tail(body, keep))
        out.append('```')
        out.append('')

    if '--nobuild' not in sys.argv:
        c, b = run([os.path.join(HERE, 'build32_v2.py'), os.path.join(HERE, 'patches32.json')], 'build')
        rec('1 第2版を組む（build32_v2.py）', c, b, 4)
        if c != 0:
            print('\n'.join(out))
            return 1
    c, b = run([os.path.join(EP, 'v1_build', 'roles32.py'), V2, ROLES], 'roles')
    rec('2 聞き役の役割表（roles32.py → v2_build/roles.tsv）', c, b, 3)
    c, b = run([os.path.join(EP, 'v1_build', 'm32.py'), '--selftest'], 'mself')
    rec('3 m32 の陽性対照（--selftest）', c, b, 2)
    c, m_out = run([os.path.join(EP, 'v1_build', 'm32.py'), V2, '--roles', ROLES], 'm32')
    rec('4 m32（字数・尺・冒頭・聞き役・写真・図・線・名前・帰属・時点）', c, m_out, 60)
    files = subprocess.run(['git', 'ls-files', 'ref/ep32'], cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout.split()
    files += [os.path.relpath(p, REPO).replace('\\', '/') for p in glob.glob(os.path.join(HERE, '*')) if os.path.isfile(p)]
    files += ['ref/ep32/daihon_v2.md']
    files = sorted(set(f for f in files if os.path.exists(os.path.join(REPO, f)) and not f.endswith('.pyc')))
    c, b = run([os.path.join(HERE, 'namecheck32.py')] + files, 'names')
    rec('5 名前の網（namecheck32.py・%d ファイル）' % len(files), c, b, 3)
    c, b = run(['tools/check_script.py', '--refcheck'], 'ref')
    rec('6a check_script --refcheck（尺の式の陽性対照）', c, b, 5)
    c, cs = run(['tools/check_script.py', V2], 'cs')
    e_lines = [l for l in cs.split('\n') if re.match(r'^🔴 E ', l)]
    e_other = [l for l in e_lines if '尺' not in l]
    out.append('### %s 6b check_script（形）＝E %d（うち尺の古い定数でないもの %d）' % ('✓' if not e_other else '🔴', len(e_lines), len(e_other)))
    out.append('```')
    out += [l for l in cs.split('\n') if re.search(r'^(カット|①|🔴 E|E \d+件)', l)][:12]
    out.append('```')
    out.append('')
    if e_other:
        worst = 1
    c, b = run(['tools/check_script_diff.py', V1, V2], 'csd')
    rec('7 check_script_diff（🔧 と差分・欠番）', c, b, 8)
    c, b = run([os.path.join(EP, 'v1_build', 'quotes32.py'), '--selftest'], 'qself')
    rec('8a quotes32 の陽性対照', c, b, 2)
    c, b = run([os.path.join(EP, 'v1_build', 'quotes32.py'), V2, '--out', os.path.join(HERE, 'quotes32_v2.tsv')], 'q')
    bad_q = re.search(r'外れ=(\d+)', b)
    rec('8b quotes32（出典の欄の原文の片）', c if not (bad_q and int(bad_q.group(1))) else 1, b, 4)
    n, bad = sou_check()
    out.append('### %s 9 まとめのあとの「そう。」＝まとめ %d・受けていない %d %s' % ('✓' if not bad else '🔴', n, len(bad), ' '.join(bad)))
    out.append('')
    if bad:
        worst = 1
    text = open(V2, encoding='utf-8').read()
    head = text[:text.index('## 2. 照合の表')]
    hits = sorted(set(INTERNAL.findall(head)))
    out.append('### %s 10 頭と §0 の内部の数字の語＝%s' % ('✓' if not hits else '🔴', '・'.join(hits) or '0件'))
    out.append('')
    if hits:
        worst = 1
    mc = re.search(r'＝(\d+)字（目標', m_out)
    mh = re.search(r'%s=([0-9.]+)s' % HOOK, m_out)
    tot = int(mc.group(1)) if mc else -1
    hook = float(mh.group(1)) if mh else 999.0
    ok_band = LO <= tot <= HI and hook <= OPEN_MAX
    out.append('### %s 11 字数の幅と冒頭＝%d字（幅 %d〜%d）・引き %s の終わり %.1f秒（%.0f秒まで）' % ('✓' if ok_band else '🔴', tot, LO, HI, HOOK, hook, OPEN_MAX))
    out.append('')
    if not ok_band:
        worst = 1
    c, b = run([os.path.join(HERE, 'make_diff32.py')], 'diff')
    rec('12 対照表（make_diff32.py）', c, b, 2)
    c, b = run([os.path.join(HERE, 'lost32.py')], 'lost')
    rec('13 消えた語（lost32.py）', c, b, 2)
    doc = ['# 32本目 ④' + "'" + ' 門番の出力（final32.py が書く・手で直さない）', ''] + out
    with open(os.path.join(HERE, 'gates.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(doc) + '\n')
    for l in out:
        if l.startswith('### '):
            print(l[4:])
    print('→ v2_build/gates.md')
    return worst


if __name__ == '__main__':
    sys.exit(main())
