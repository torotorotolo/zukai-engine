# -*- coding: utf-8 -*-
"""27本目④'：第2版の机上の数え＝④ の m27.py（v1_build・数え＋事件の回の網）をそのまま呼び、④' で分かった網を2つ足す。

  python -P ref/ep27/v2_build/m27v2.py ref/ep27/daihon_v2.md --roles ref/ep27/v2_build/roles.tsv
  python -P ref/ep27/v2_build/m27v2.py --selftest

足す網：
  1 確かめようのない否定＝語り（聞き役と引用の「」の外）の「報じられていない」「報道は無い」「公表していない／されていない」「はっきりしているのは」を W
    （「こちらが読んだ範囲」の言い方になっているかを人が見る＝記憶 feedback-dont-state-inferences-as-findings・④' の所見）
  2 SNS の字＝画の欄が「図 SNS」のカットで、語りの「」の中の字が git の外の src/sns_posts.tsv の原文のどれかにそのまま入っているか（無ければ E）。
    カードの画の欄に「注釈」が無い・「アカウント名なし」が無いも E（m27 も見るが、ここでは第2版の直しで崩れていないかを二重に）
終了コード＝m27 の E か、足した網の E があれば 1
"""
import importlib.util
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
_spec = importlib.util.spec_from_file_location('m27', os.path.join(EP, 'v1_build', 'm27.py'))
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
CS, SP = M.CS, M.speaker
SNS_FILE = os.path.join(EP, 'src', 'sns_posts.tsv')        # git の外（アカウント名なし）
ABSENT = re.compile(r'報じられていない|報道は無い|報道はない|公表していない|公表されていない|はっきりしているのは')
QUOTE = re.compile(r'「([^」]*)」')


def load_posts(p=SNS_FILE):
    if not os.path.exists(p):
        return None
    out = []
    for ln in open(p, encoding='utf-8'):
        if ln.startswith('#') or not ln.strip():
            continue
        f = ln.rstrip('\n').split('\t')
        if len(f) >= 4:
            out.append(f[3])
    return out


def absent_hits(line):
    """引用の「」を外した語りの中の、確かめようのない否定の語。"""
    return ABSENT.findall(QUOTE.sub('', line))


def sns_bad(line, posts):
    """語りの「」の中の字のうち、SNS の原文のどれにもそのまま入っていないもの。"""
    return [q for q in QUOTE.findall(line) if not any(q in p for p in posts)]


def extra(path):
    cuts = CS.parse(open(path, encoding='utf-8').read())
    posts = load_posts()
    E, W = [], []
    if posts is None:
        E.append('E src/sns_posts.tsv が無い＝SNS の字を当てられない（fail closed）')
        posts = []
    for cid, pic, ls in cuts:
        is_sns = M.fig_type(pic) == 'SNS'
        if is_sns:
            if '注釈' not in pic:
                E.append('E %s SNS のカードの画の欄に「注釈」が無い' % cid)
            if 'アカウント名' not in pic:
                E.append('E %s SNS のカードの画の欄に「アカウント名なし」の書き込みが無い' % cid)
        for raw in ls:
            who = SP.split(raw)[0]
            if who == SP.WHO_Q:
                continue
            t = SP.bare(raw.strip())
            for w in absent_hits(t):
                W.append('W %s 確かめようのない否定「%s」（範囲の言い方か人が見る）: %s' % (cid, w, t[:40]))
            if is_sns:
                for q in sns_bad(t, posts):
                    E.append('E %s SNS の字が控えの原文に無い:「%s」' % (cid, q[:40]))
    return E, W


def selftest():
    ok = True
    posts = ['なんか似てる人とすれ違ったんだけどたぶん違う', '関東で目撃情報が寄せられているから、重点的に調べるべきではないか']
    cases = [
        (absent_hits('本人だと確かめられたという報道は無い。'), ['報道は無い']),
        (absent_hits('「報道は無い」と書いた。'), []),                      # 引用の中は数えない
        (absent_hits('本人だと確かめられたという報道は、見当たらない。'), []),
        (sns_bad('「重点的に調べるべきではないか」という声もある。', posts), []),
        (sns_bad('「重点的に調べるべきだ」という声もある。', posts), ['重点的に調べるべきだ']),   # 陽性対照
    ]
    for i, (got, want) in enumerate(cases, 1):
        print('selftest %d %s got=%s want=%s' % (i, 'OK' if got == want else 'NG', got, want))
        ok &= got == want
    print('SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main(path, roles):
    rc = M.main(path, roles)
    E, W = extra(path)
    print('== m27v2 の足した網（確かめようのない否定・SNS の字）')
    for x in E + W:
        print(('🔴 ' if x.startswith('E') else '⚠️ ') + x)
    print('足した網 E %d件・W %d件' % (len(E), len(W)))
    return 1 if (rc or E) else 0


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(main(sys.argv[1], rp))
