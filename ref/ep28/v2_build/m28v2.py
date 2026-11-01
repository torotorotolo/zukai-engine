# -*- coding: utf-8 -*-
"""28本目④'：第2版の机上の数え＝④ の m28.py（v1_build・数え＋会社の事件の網）をそのまま呼び、④' の網を3つ足す（27本目 m27v2.py を写した）。

  python -P ref/ep28/v2_build/m28v2.py ref/ep28/daihon_v2.md --roles ref/ep28/v2_build/roles.tsv
  python -P ref/ep28/v2_build/m28v2.py --selftest

足す網：
  1 確かめようのない否定＝語り（聞き役と引用の「」の外）の「報じられていない」「報道は無い」「公表していない／されていない」「はっきりしているのは」を W
    （「こちらが読んだ範囲」の言い方になっているかを人が見る＝記憶 feedback-dont-state-inferences-as-findings）
  2 SNS の字＝画の欄が「図 SNS」のカットで、語りの「」の中の字が git の外の src/sns/sns_posts_verified_20261031.tsv の
    「使う言葉」の列のどれかにそのまま入っているか（無ければ E）。カードの画の欄に「注釈」「アカウント名」が無いも E
  3 「漏れ」＝語り（「」の外）の「漏れ」を W（会社の言葉「漏えい」でそろえる＝sources.md §4-10。章の題は承認①で決める）
終了コード＝m28 の E か、足した網の E があれば 1
"""
import importlib.util
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
_spec = importlib.util.spec_from_file_location('m28', os.path.join(EP, 'v1_build', 'm28.py'))
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
CS, SP = M.CS, M.speaker
SNS_FILE = os.path.join(EP, 'src', 'sns', 'sns_posts_verified_20261031.tsv')   # git の外（アカウント名なし）
ABSENT = re.compile(r'報じられていない|報道は無い|報道はない|公表していない|公表されていない|はっきりしているのは')
MORE = re.compile(r'漏れ')
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


def more_hits(line):
    """引用の「」を外した語りの中の「漏れ」。"""
    return MORE.findall(QUOTE.sub('', line))


def sns_bad(line, posts):
    """語りの「」の中の字のうち、SNS の原文のどれにもそのまま入っていないもの。"""
    return [q for q in QUOTE.findall(line) if not any(q in p for p in posts)]


def extra(path):
    cuts = CS.parse(open(path, encoding='utf-8').read())
    posts = load_posts()
    E, W = [], []
    if posts is None:
        E.append('E src/sns/sns_posts_verified_20261031.tsv が無い＝SNS の字を当てられない（fail closed）')
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
            t = SP.bare(raw.strip())
            for w in more_hits(t):
                W.append('W %s「%s」（会社の言葉は「漏えい」・聞き役も）: %s' % (cid, w, t[:40]))
            if who == SP.WHO_Q:
                continue
            for w in absent_hits(t):
                W.append('W %s 確かめようのない否定「%s」（範囲の言い方か人が見る）: %s' % (cid, w, t[:40]))
            if is_sns:
                for q in sns_bad(t, posts):
                    E.append('E %s SNS の字が控えの原文に無い:「%s」' % (cid, q[:40]))
    return E, W


def selftest():
    ok = True
    posts = ['免許証の画像７年保管してたのも、本当おかしいし。', 'ここはしっかり対応してるのでそこは素晴らしい']
    cases = [
        (absent_hits('本人だと確かめられたという報道は無い。'), ['報道は無い']),
        (absent_hits('「報道は無い」と書いた。'), []),                      # 引用の中は数えない
        (absent_hits('名乗り出たという報道も、見当たらない。'), []),
        (sns_bad('「免許証の画像７年保管してたのも、本当おかしいし。」という声。', posts), []),
        (sns_bad('「免許証の画像7年保管してたのも、本当おかしいし。」という声。', posts),
         ['免許証の画像7年保管してたのも、本当おかしいし。']),            # 陽性対照（全角と半角の違いも止める）
        (more_hits('では、免許証の情報が漏れると、何が起こりうるのか。'), ['漏れ']),
        (more_hits('「漏れた」と書いた。'), []),
    ]
    for i, (got, want) in enumerate(cases, 1):
        print('selftest %d %s got=%s want=%s' % (i, 'OK' if got == want else 'NG', got, want))
        ok &= got == want
    print('SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main(path, roles):
    rc = M.main(path, roles)
    E, W = extra(path)
    print('== m28v2 の足した網（確かめようのない否定・SNS の字・「漏れ」）')
    for x in E + W:
        print(('🔴 ' if x.startswith('E') else '⚠️ ') + x)
    print('足した網 E %d件・W %d件' % (len(E), len(W)))
    return 1 if (rc or E) else 0


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(main(sys.argv[1], rp))
