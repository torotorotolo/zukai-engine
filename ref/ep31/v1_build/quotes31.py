# -*- coding: utf-8 -*-
"""31本目 出典の欄の原文の片（バッククォートの中）を、一次資料の文字に機械で当てる（④・2026-11-07・30本目の quotes30.py を写した）。

  python -P ref/ep31/v1_build/quotes31.py ref/ep31/daihon_v1.md [--out 結果.tsv]
  python -P ref/ep31/v1_build/quotes31.py --selftest

なぜ要るか：決め所（★）が0＝tools/check_facts.py の照合が働かない（ルール 4-2 の「多文書の回」）。§4 の全カットの「出典の欄」のバッククォートを、書いた資料に当てる。
書き方＝`記号（`原文の片`…`原文の片`）`。記号＝判（最高裁 1983-09-22）・白（運輸白書 昭和47年度）・法（昭和50年法律第58号）・記（国交省 2002-09-04）・
国〈issueID〉/〈発言の番号〉（国会会議録）・町（雫石町の頁＝手元に無い＝当てない）・会（会社の頁＝当てない）・画（画面の表示＝当てない）。資料はすべて ref/ep31/src/（git の外）。
揃え＝NFKC・空白と句読点と括弧を消す・「ヶ」を「ケ」に・小書きの「つ」を並字に（判決は「あつた」と書く）。「…」で区切った片を全部探す。
⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ・帰属・条件節）は人と係が見る（ルール 4'-12）。
"""
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')
DOCS = {
    '判': ['hanrei/hanrei-58088.txt'],
    '白': ['web/hakusho47_002.txt', 'web/hakusho47_001.txt'],
    '法': ['web/law_s50_58.txt'],
    '記': ['web/mlit_kisha_2002.txt'],
}
NOCHECK = {'町': '町', '会': '会', '画': '画'}
CUT_RE = re.compile(r'^\*\*([a-z][0-9a-z]\d{2})\*\*\s*(?:🔧\s*)?／\s*.*?\s*／\s*(.*)$', re.M)
TOK = re.compile(r'(?P<kok>国\d{6,}X\d+/\d+)（|(?P<doc>[判白法記町会画])（|`(?P<q>[^`]+)`')
DROP = re.compile(r'[\s、。，．,.「」『』（）()\[\]［］〔〕・･:：;；"\'’”“!！?？　]')
_cache = {}
_kokkai = None


def norm(s):
    s = unicodedata.normalize('NFKC', s or '')
    s = s.replace('ヶ', 'ケ').replace('ｹ', 'ケ').replace('っ', 'つ').replace('ッ', 'ツ').replace('ゃ', 'や') \
         .replace('ゅ', 'ゆ').replace('ょ', 'よ').replace('ャ', 'ヤ').replace('ュ', 'ユ').replace('ョ', 'ヨ')
    return DROP.sub('', s)


PAGE_NO = re.compile(r'^\s*-\s*\d+\s*-\s*$', re.M)      # 判決の文字の層の頁番号「- 6 -」＝文の途中に挟まる（11-07）


def text_of(rel):
    if rel not in _cache:
        p = os.path.join(SRC, rel)
        _cache[rel] = (norm(PAGE_NO.sub('', open(p, encoding='utf-8', errors='replace').read()))
                       if os.path.exists(p) else None)
    return _cache[rel]


def kokkai(iid, order):
    global _kokkai
    if _kokkai is None:
        _kokkai = {}
        for fn in ('meetings.jsonl', 'speeches.jsonl'):
            p = os.path.join(SRC, 'kokkai', fn)
            if not os.path.exists(p):
                continue
            for ln in open(p, encoding='utf-8'):
                r = json.loads(ln)
                _kokkai.setdefault((r['issueID'], str(r['speechOrder'])), norm(r['speech']))
    return _kokkai.get((iid, str(order)))


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
            t = kokkai(m.group(1), m.group(2)) if m else None
            out.append(('OK' if t and n in t else ('資料が無い' if t is None else '無し'), part))
            continue
        if doc not in DOCS:
            out.append(('記号が無い:' + doc, part))
            continue
        hit, missing = False, True
        for rel in DOCS[doc]:
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
    bad = [r for r in res if r[1] not in ('OK', '町', '会', '画')]
    for cid, v, s in bad:
        print('🔴 %s %s: %s' % (cid, v, s[:80]))
    if outp:
        with open(outp, 'w', encoding='utf-8', newline='\n') as f:
            for cid, v, s in res:
                f.write('%s\t%s\t%s\n' % (cid, v, s))
    return 1 if bad else 0


def selftest():
    ok = norm('霞ヶ関 駅。「あ」') == '霞ケ関駅あ'
    r = check_fragment('判', '漠然と手指で指し示して')
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('判', '何ら検討を加えることなくそのままこれを承認した')
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('判', '教官が地図の上で指で決めた')              # 陰性対照（崩れた通説）
    ok &= bool(r) and r[0][0] == '無し'
    r = check_fragment('白', '少なくとも接触約7秒前から視認していたと推定される')
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('国106614889X00119710802/13', '十三時二十八分')
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('国106614889X00119710802/13', '十三時三十三分')       # 陰性対照（別の発言の時刻）
    ok &= bool(r) and r[0][0] == '無し'
    r = check_fragment('法', '他の航空機その他の物件と衡突しないように見張りをしなければならない')
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('記', '全国各地にある訓練空域４７を細分化し、１１９ヶ所とした')
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('町', '森のしずく公園')
    ok &= bool(r) and r[0][0] == '町'
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    op = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(run(sys.argv[1], op))
