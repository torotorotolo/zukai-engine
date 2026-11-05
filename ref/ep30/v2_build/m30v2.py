# -*- coding: utf-8 -*-
"""30本目④'：第2版の机上の数え＝④ の m30.py（v1_build・数え＋判決が確定した事件の網）をそのまま呼び、④' の網を足す（29本目 m29v2.py を写した）。

  python -P ref/ep30/v2_build/m30v2.py ref/ep30/daihon_v2.md --roles ref/ep30/v2_build/roles.tsv
  python -P ref/ep30/v2_build/m30v2.py --selftest

足す網：
  1 言い切りの網＝語り（聞き役と引用の「」の外）の「目が向」「犯人扱い」「放置」「知っていて」「黙って」「隠し」「見逃」「見過ご」「怠」「防げ」「防ぎよう」
    「止められた」「遅すぎ」「手遅れ」「はっきりしているのは」を W（人が文脈を見る＝動画の声で言い切っていないか）
  2 帰属の網＝出典の欄に手記か無線の札がある語りで、時刻か言葉を語っているのに、同じカットに出どころの語が無ければ W（帰属はカットをまたぐと切れる）
  3 語りの行の全角のカンマ・半角のカンマを E（読みと字幕が崩れる）
終了コード＝m30 の E か、足した網の E があれば 1
"""
import importlib.util
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
_spec = importlib.util.spec_from_file_location('m30', os.path.join(EP, 'v1_build', 'm30.py'))
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
CS, SP = M.CS, M.speaker
QUOTE = re.compile(r'「[^」]*」')
FLAT = re.compile(r'目が向|犯人扱い|放置|知っていて|黙って|隠し|見逃|見過ご|怠|防げ|防ぎよう|止められた|遅すぎ|手遅れ|はっきりしているのは')
SRC_TAG = re.compile(r'(?<![`])(手助役|手運転士|手警部補|手機関員|手院長|無線)（')
ATTR_WORD = {
    '手助役': r'助役|手記', '手運転士': r'運転士|手記', '手警部補': r'警部補|手記', '手機関員': r'隊員|消防の手記|手記',
    '手院長': r'院長|副医長|手記', '無線': r'無線|本部',
}
COMMA = re.compile(r'，|(?<![0-9]),|,(?![0-9])')   # 数字の位取りの半角カンマ（5,800）は当てない


def flat_hits(line):
    """引用の「」を外した語りの中の、言い切りの語。"""
    return FLAT.findall(QUOTE.sub('', line))


def attr_missing(src, narr):
    """出典の欄の札のうち、語りに出どころの語が無いもの。"""
    src2 = re.sub(r'`[^`]*`', '', src)
    return sorted({t for t in SRC_TAG.findall(src2) if not re.search(ATTR_WORD[t], narr)})


def extra(path):
    text = open(path, encoding='utf-8').read()
    cuts = CS.parse(text)
    srcs = M.raw_sources(text)
    E, W = [], []
    for cid, pic, ls in cuts:
        narr = []
        for raw in ls:
            who = SP.split(raw)[0]
            t = SP.bare(raw.strip())
            if COMMA.search(t):
                E.append('E %s 語りにカンマ: %s' % (cid, t[:40]))
            if who == SP.WHO_Q:
                continue
            narr.append(t)
            for w in flat_hits(t):
                W.append('W %s 言い切りの網「%s」（人が文脈を見る）: %s' % (cid, w, t[:44]))
        miss = attr_missing(srcs.get(cid, ''), ''.join(narr))
        if miss:
            W.append('W %s 帰属の網（札 %s の出どころの語が同じカットに無い）: %s' % (cid, '・'.join(miss), ''.join(narr)[:40]))
    return E, W


def selftest():
    ok = True
    cases = [
        (flat_hits('捜査の目は、その家へ向く。放置した。'), ['放置']),
        (flat_hits('「放置」と書いた。'), []),                               # 引用の中は数えない
        (flat_hits('知っていて黙っていた。'), ['知っていて', '黙って']),   # 陽性対照
        (flat_hits('疑いは、事件の前からあった。'), []),
        (attr_missing('手院長（`午前 11 時半過ぎ`）', '11時半すぎに届いた。'), ['手院長']),   # 陽性対照
        (attr_missing('手院長（`午前 11 時半過ぎ`）', '院長の手記では、11時半すぎに届いた。'), []),
        (attr_missing('公（`手院長（`）', '届いた。'), []),                  # 片の中の字は札に数えない
        (bool(COMMA.search('「阻止，かく乱」')), True),
        (bool(COMMA.search('「阻止、かく乱」')), False),
        (bool(COMMA.search('5,800人以上')), False),                          # 数字の位取りは当てない
        (bool(COMMA.search('阻止,かく乱')), True),
    ]
    for i, (got, want) in enumerate(cases, 1):
        print('selftest %d %s got=%s want=%s' % (i, 'OK' if got == want else 'NG', got, want))
        ok &= got == want
    print('m30v2 の網の selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


def main():
    if '--selftest' in sys.argv:
        r0 = M.selftest()
        return r0 or selftest()
    path = sys.argv[1]
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    r = M.main(path, rp)
    e, w = extra(path)
    print('--- ④\' の足した網（言い切り・帰属・カンマ）')
    for x in w:
        print('⚠️ ' + x)
    for x in e:
        print('🔴 ' + x)
    print('足した網 E %d件・W %d件' % (len(e), len(w)))
    return 1 if (r or e) else 0


if __name__ == '__main__':
    sys.exit(main())
