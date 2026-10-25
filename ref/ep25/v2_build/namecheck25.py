# -*- coding: utf-8 -*-
"""25本目④'：書かない名前の網（リポは公開＝人の名前・撮影者の個人名を、リポに入るファイルに書かない・24本目 namecheck24.py を写した）。

  python ref/ep25/v2_build/namecheck25.py <ファイル> [<ファイル> …]
  python ref/ep25/v2_build/namecheck25.py --selftest

網は2つ：
 1. 出さない名前＝git の外の src/names_private.txt（被告人・委員・社長など。注の行〈#〉は飛ばす）＝当たれば E。
 2. 撮影者の個人名＝git の外の src/credits_private.tsv の**作者の列だけ**（機関名の行は除く・「 at Japanese Wikipedia」「 (talk)」を外す）
    ＝ラテン文字は語の境で・漢字はそのまま当てる＝当たれば E。
当たった所は名前を伏せて「ファイル:行・語の頭1字＋○」だけ出す（この出力も gates.md に入る＝リポに名前を写さない）。
終了コード 0=0件 / 1=当たりあり / 2=表が読めない（fail closed）
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
NAMES = os.path.join(EP, 'src', 'names_private.txt')
CRED = os.path.join(EP, 'src', 'credits_private.tsv')
ORG_ROW = re.compile(r'Board|Commission|Agency|Ministry|Office|Government|Bureau|Railway Company', re.I)


def private_names():
    if not os.path.exists(NAMES):
        return None
    return [ln.strip() for ln in open(NAMES, encoding='utf-8') if ln.strip() and not ln.startswith('#')]


def author_tokens():
    if not os.path.exists(CRED):
        return None
    toks = set()
    for k, ln in enumerate(open(CRED, encoding='utf-8')):
        cols = ln.rstrip('\n').split('\t')
        if k == 0 or ln.startswith('#') or len(cols) < 5:
            continue
        a = cols[4].strip()
        if not a or ORG_ROW.search(a):
            continue
        a = re.sub(r'\s+at\s+\S+\s+Wikipedia$', '', a)
        a = re.sub(r'\s*\(talk\)$', '', a)
        for t in re.findall(r'[A-Za-z][A-Za-z0-9]{2,}', a):
            toks.add(t)
        for t in re.findall(r'[㐀-鿿぀-ヿ]{2,}', a):
            toks.add(t)
    return toks


def mask(w):
    return w[0] + '○' * (len(w) - 1)


def nets():
    names, toks = private_names(), author_tokens()
    if names is None or toks is None:
        return None
    out = [('出さない名前', n, re.compile(re.escape(n))) for n in names]
    for t in sorted(toks):
        rx = re.compile(r'(?<![A-Za-z0-9])' + re.escape(t) + r'(?![A-Za-z0-9])') if t.isascii() else re.compile(re.escape(t))
        out.append(('撮影者の名前', t, rx))
    return out


def scan_text(text, fname, net, out):
    hits = 0
    for i, ln in enumerate(text.split('\n'), 1):
        for kind, n, rx in net:
            if rx.search(ln):
                hits += 1
                out.append('E %s:%d %s「%s」' % (fname, i, kind, mask(n)))
    return hits


def main(files):
    net = nets()
    if net is None:
        print('🔴 名前の表か作者の表が読めない:', NAMES, CRED)
        return 2
    hits, buf = 0, []
    for f in files:
        try:
            text = open(f, encoding='utf-8').read()
        except Exception as e:
            print('🔴 読めない:', f, e)
            return 2
        hits += scan_text(text, os.path.basename(f), net, buf)
    for b in buf:
        print(b)
    na = sum(1 for k, _, _ in net if k == '出さない名前')
    print('名前の網：出さない名前 %d 語＋撮影者の語 %d（作者の列だけ）／ファイル %d／当たり %d' % (na, len(net) - na, len(files), hits))
    return 1 if hits else 0


def selftest():
    net = nets()
    if net is None:
        print('selftest ✗（表が読めない）')
        return 2
    ok = True
    names = private_names()
    toks = sorted(t for k, t, _ in net if k == '撮影者の名前')
    # 陽性対照：表の名前・作者の語を文に埋めると当たる／陰性対照：機関名・一般の語は当たらない
    pos = '報告書によれば%sは' % names[-1]
    ok &= scan_text(pos, 'pos', net, []) == 1
    ok &= all(scan_text('撮影 %s の写真' % t, 'pos', net, []) >= 1 for t in toks)
    neg = 'Japan Transport Safety Board の写真・航空・鉄道事故調査委員会・運転士・車掌・社長（当時）・Commons・Wikipedia'
    ok &= scan_text(neg, 'neg', net, []) == 0
    # 大文字だけの名義は語の境で当てる＝先頭だけ大文字の別の語には当たらない（名義の字はここに書かない）
    caps = [t for t in toks if t.isascii() and t.isupper()]
    ok &= all(scan_text(t.capitalize() + 'hiro', 'neg', net, []) == 0 for t in caps)
    print('出さない名前 %d・撮影者の語 %d（%s）→ selftest %s' % (len(names), len(toks), '・'.join(mask(t) for t in toks), 'OK' if ok else '✗'))
    return 0 if ok else 1


if __name__ == '__main__':
    a = sys.argv[1:]
    sys.exit(selftest() if not a or a[0] == '--selftest' else main(a))
