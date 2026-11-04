# -*- coding: utf-8 -*-
"""30本目 出典の欄の原文の片（バッククォートの中）を、一次資料の文字に機械で当てる（④・2026-11-04・26本目の quotes26.py の考えを日本語の資料に替えた）。

  python ref/ep30/v1_build/quotes30.py ref/ep30/daihon_v1.md [--out 結果.tsv]
  python ref/ep30/v1_build/quotes30.py --selftest

なぜ要るか：決め所（★）が0＝tools/check_facts.py の照合が働かない（ルール 4-2 の「多文書の回」）。§4 の全カットの「出典の欄」のバッククォートを、書いた資料に当てる。
書き方＝`記号（`原文の片`…`原文の片`）`。記号の一覧は DOCS。資料はすべて ref/ep30/src/（git の外）。
揃え＝NFKC・空白と句読点と括弧を消す・「ヶ」を「ケ」に。「…」で区切った片を全部探す。
⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ・帰属・条件節）は人と係が見る（ルール 4'-12）。
⚠️ 無線と OH（自動字幕）は語の字が崩れる＝機械で当てない（「字幕」と出す）。無線の語は耳で未確認（sources.md §3）。
"""
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')
DOCS = {
    '白2': ['hakusho/h080102.txt'], '白3': ['hakusho/h080103.txt'], '白5': ['hakusho/h080105.txt'],
    '判T': ['hanrei/hanrei-pdf-5572.txt'], '判A': ['hanrei/hanrei-pdf-81875.txt'], '判B': ['hanrei/hanrei-pdf-5770.txt'],
    '判C': ['hanrei/hanrei-pdf-5817.txt'], '判D': ['hanrei/hanrei-pdf-40.txt'], '判E': ['hanrei/hanrei-pdf-89530.txt'],
    '手助役': ['shuki/shuki_ocr.txt'], '手運転士': ['shuki/shuki_ocr.txt'], '手警部補': ['shuki/shuki_ocr.txt'],
    '手機関員': ['shuki/shuki_ocr.txt'], '手院長': ['shuki/shuki_ocr.txt'],
    '声代表': ['shuki/voice/v_daihyo.txt'], '声松本': ['shuki/voice/v_matsumoto.txt'], '声事務長': ['shuki/voice/v_jimucho.txt'],
    '声兄': ['shuki/voice/v_ani_a.txt'], '声丸ノ内': ['shuki/voice/v_higaisha_o.txt'],
    '公': ['web/psia.txt'], '特': ['web/psia.txt'],
    '消a': ['shobo/kento088_74_shiryo4.txt'], '消b': ['shobo/sanjikann191204.txt'], '東消': ['shobo/kyoubasi_00015.txt'],
    '犯白': ['hakusho/hanzai_r1.txt'], '給a': ['hakusho/higai_2011.txt'], '給b': ['hakusho/higai_2012.txt'],
    '窓': ['web/psia.txt'],
}
NOCHECK = {'無線': '字幕', 'OH': '字幕', '画': '画'}
CUT_RE = re.compile(r'^\*\*([a-z][0-9a-z]\d{2})\*\*\s*(?:🔧\s*)?／\s*.*?\s*／\s*(.*)$', re.M)
TOK = re.compile(r'(?P<kok>国\d{6,}X\d+/\d+)（|(?P<doc>[白判手声公特消東犯給窓無OH画][^\s（）`・／]{0,4})（|`(?P<q>[^`]+)`')
DROP = re.compile(r'[\s、。，．,.「」『』（）()\[\]［］・･:：;；"\'’”“!！?？　]')
_cache = {}


def norm(s):
    s = unicodedata.normalize('NFKC', s or '')
    s = s.replace('ヶ', 'ケ').replace('ｹ', 'ケ')
    return DROP.sub('', s)


def text_of(rel):
    if rel not in _cache:
        p = os.path.join(SRC, rel)
        _cache[rel] = norm(open(p, encoding='utf-8', errors='replace').read()) if os.path.exists(p) else None
    return _cache[rel]


def check_fragment(doc, q):
    """(判定, 片) の列を返す。"""
    out = []
    for part in re.split(r'…|\.\.\.', q):
        part = part.strip()
        n = norm(part)
        if not n:
            continue
        if len(n) < 3:
            out.append(('短い', part))
            continue
        if doc in NOCHECK:
            out.append((NOCHECK[doc], part))
            continue
        if doc.startswith('国'):
            m = re.match(r'国(\d{6,}X\d+)/(\d+)$', doc)
            rel = 'kokkai/%s_%s.txt' % (m.group(1), m.group(2))
            rels = [rel]
        elif doc in DOCS:
            rels = DOCS[doc]
        else:
            out.append(('記号が無い:' + doc, part))
            continue
        hit, missing = False, True
        for rel in rels:
            t = text_of(rel)
            if t is None:
                continue
            missing = False
            if n in t:
                hit = True
        out.append(('OK' if hit else ('資料が無い' if missing else '無し'), part))
    return out


def run(md, outp=None):
    text = open(md, encoding='utf-8').read()
    res = []
    empty = []
    for m in CUT_RE.finditer(text):
        cid, src = m.group(1), m.group(2)
        doc = None
        nq = 0
        for t in TOK.finditer(src):
            if t.group('kok'):
                doc = t.group('kok')
            elif t.group('doc'):
                doc = t.group('doc')
            elif t.group('q'):
                nq += 1
                if doc is None:
                    res.append((cid, '記号なし', t.group('q')))
                    continue
                for verdict, part in check_fragment(doc, t.group('q')):
                    res.append((cid, verdict, doc + ' ' + part))
        if nq == 0:
            empty.append(cid)
    cnt = {}
    for _, v, _ in res:
        cnt[v] = cnt.get(v, 0) + 1
    print('片 %d: %s' % (len(res), ' '.join('%s=%d' % kv for kv in sorted(cnt.items()))))
    print('片の無いカット %d: %s' % (len(empty), ' '.join(empty)))
    bad = [r for r in res if r[1] not in ('OK', '字幕', '画')]
    for cid, v, s in bad:
        print('🔴 %s %s: %s' % (cid, v, s))
    if outp:
        with open(outp, 'w', encoding='utf-8', newline='\n') as f:
            for cid, v, s in res:
                f.write('%s\t%s\t%s\n' % (cid, v, s))
    return 1 if bad else 0


def selftest():
    ok = norm('霞ヶ関 駅。「あ」') == '霞ケ関駅あ'
    r = check_fragment('白3', 'サリンが分解した際にもできる化学物質')
    ok &= r and r[0][0] == 'OK'
    r = check_fragment('白3', 'この文は白書に無いはずの作った文である')
    ok &= r and r[0][0] == '無し'
    r = check_fragment('判C', '強制捜査を一時しのぎ的に回避すること')
    ok &= r and r[0][0] == 'OK'
    r = check_fragment('国113614720X01119960523/38', '被疑者不詳で捜索')
    ok &= r and r[0][0] == 'OK'
    r = check_fragment('手院長', '午前 11 時半過ぎ')
    ok &= r and r[0][0] == 'OK'
    r = check_fragment('無線', '病人2名')
    ok &= r and r[0][0] == '字幕'
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    op = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(run(sys.argv[1], op))
