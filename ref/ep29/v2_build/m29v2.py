# -*- coding: utf-8 -*-
"""29本目④'：第2版の机上の数え＝④ の m29.py（v1_build・数え＋会社の事件の網）をそのまま呼び、④' の網を4つ足す（28本目 m28v2.py を写した）。

  python -P ref/ep29/v2_build/m29v2.py ref/ep29/daihon_v2.md --roles ref/ep29/v2_build/roles.tsv
  python -P ref/ep29/v2_build/m29v2.py --selftest

足す網：
  1 確かめようのない否定＝語り（聞き役と引用の「」の外）の「報じられていない」「報道は無い」「公表していない／されていない」「はっきりしているのは」を W
    （「こちらが読んだ範囲」の言い方になっているかを人が見る＝記憶 feedback-dont-state-inferences-as-findings）
  2 SNS の字＝画の欄が「図 SNS」のカットで、語りの「」の中の字が git の外の src/sns/yrt_20261103*.tsv の本文（検索語の印 START・END を除く）の
    どれかにそのまま入っているか（無ければ E）。カードの画の欄に「注釈」「アカウント名」が無いも E
  3 「漏れ」＝語り（「」の外）の「漏れ」を W（会社の言葉「漏えい」でそろえる）
  4 🆕 結びつきの網＝同じカットの語りに「2年前」か「指摘」と「侵入」「入られ」「攻撃」が並ぶ行を W（2年前の指摘と今回の侵入を結びつけない＝人が聞いて見る）
終了コード＝m29 の E か、足した網の E があれば 1
"""
import importlib.util
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
_spec = importlib.util.spec_from_file_location('m29', os.path.join(EP, 'v1_build', 'm29.py'))
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
CS, SP = M.CS, M.speaker
SNS_FILES = [os.path.join(EP, 'src', 'sns', x) for x in ('yrt_20261103.tsv', 'yrt_20261103b.tsv')]   # git の外（アカウント名なし）
ABSENT = re.compile(r'報じられていない|報道は無い|報道はない|公表していない|公表されていない|はっきりしているのは')
MORE = re.compile(r'漏れ')
QUOTE = re.compile(r'「([^」]*)」')
TIE_A = re.compile(r'2年前|指摘')
TIE_B = re.compile(r'侵入|入られ|攻撃')


def load_posts(files=SNS_FILES):
    out = []
    for p in files:
        if not os.path.exists(p):
            return None
        for ln in open(p, encoding='utf-8'):
            f = ln.rstrip('\n').split('\t')
            if len(f) >= 4 and f[0] != 'term':
                out.append(re.sub(r'\s*(?:START|END)\s*', '', f[3]))   # 検索語の印は前後の空白ごと外す
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


def tie_hit(text):
    """同じカットの語りに、2年前の指摘の語と今回の侵入の語が並ぶか。"""
    return bool(TIE_A.search(text) and TIE_B.search(text))


def extra(path):
    cuts = CS.parse(open(path, encoding='utf-8').read())
    posts = load_posts()
    E, W = [], []
    if posts is None:
        E.append('E src/sns/yrt_20261103*.tsv が無い＝SNS の字を当てられない（fail closed）')
        posts = []
    for cid, pic, ls in cuts:
        is_sns = M.fig_type(pic) == 'SNS'
        if is_sns:
            if '注釈' not in pic:
                E.append('E %s SNS のカードの画の欄に「注釈」が無い' % cid)
            if 'アカウント名' not in pic:
                E.append('E %s SNS のカードの画の欄に「アカウント名なし」の書き込みが無い' % cid)
        narr = []
        for raw in ls:
            who = SP.split(raw)[0]
            t = SP.bare(raw.strip())
            for w in more_hits(t):
                W.append('W %s「%s」（会社の言葉は「漏えい」・聞き役も）: %s' % (cid, w, t[:40]))
            if who == SP.WHO_Q:
                continue
            narr.append(t)
            for w in absent_hits(t):
                W.append('W %s 確かめようのない否定「%s」（範囲の言い方か人が見る）: %s' % (cid, w, t[:40]))
            if is_sns:
                for q in sns_bad(t, posts):
                    E.append('E %s SNS の字が控えの原文に無い:「%s」' % (cid, q[:40]))
        if tie_hit(''.join(narr)):
            W.append('W %s 結びつきの網（2年前の指摘と今回の侵入の語が同じカット＝結びついて聞こえないか人が見る）: %s' % (cid, ''.join(narr)[:50]))
    return E, W


def selftest():
    ok = True
    posts = ['GMOの正午になる前にPCの電源切ってとかいう呼びかけ今知った。こんなん気づかなかった人が殆どなのでは……。',
             'それでも、叩く順番はまず犯人じゃない？']
    cases = [
        (absent_hits('本人だと確かめられたという報道は無い。'), ['報道は無い']),
        (absent_hits('「報道は無い」と書いた。'), []),                      # 引用の中は数えない
        (absent_hits('名乗り出たという報道も、見当たらない。'), []),
        (sns_bad('「こんなん気づかなかった人が殆どなのでは」という声。', posts), []),
        (sns_bad('「こんなん気づかなかった人がほとんどなのでは」という声。', posts),
         ['こんなん気づかなかった人がほとんどなのでは']),                 # 陽性対照（1字違いも止める）
        (more_hits('では、情報が漏れると、何が起こりうるのか。'), ['漏れ']),
        (more_hits('「漏れた」と書いた。'), []),
        (tie_hit('2年前の指摘の穴から侵入された。'), True),               # 陽性対照
        (tie_hit('2年前に指摘があった。'), False),
    ]
    for i, (got, want) in enumerate(cases, 1):
        print('selftest %d %s got=%s want=%s' % (i, 'OK' if got == want else 'NG', got, want))
        ok &= got == want
    print('SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main(path, roles):
    rc = M.main(path, roles)
    E, W = extra(path)
    print('== m29v2 の足した網（確かめようのない否定・SNS の字・「漏れ」・結びつき）')
    for x in E + W:
        print(('🔴 ' if x.startswith('E') else '⚠️ ') + x)
    print('足した網 E %d件・W %d件' % (len(E), len(W)))
    return 1 if (rc or E) else 0


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(main(sys.argv[1], rp))
