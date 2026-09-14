"""台本に、指定した直しをまとめて当てる。

なぜ道具にするか: 所見162件のうち90件超が「1行の置き換え」で、手で当てると往復が90回になる。
⚠️ 当てる前に「いまの行の頭」を全件照合し、1つでも食い違ったら**1件も当てずに止める**（fail closed）。
　 [[feedback-verify-your-own-instrument]]＝道具のほうが先に間違える。

仕様（TSV・タブ区切り・1行1件）:
    cid <TAB> 対象 <TAB> 照合する頭 <TAB> 新しい本文
  対象 = 1|2|3  … その字幕行を置き換える
       = PIC    … 画の欄を置き換える
       = SRC    … 出典の欄を置き換える
       = +1|+2  … その行の「あと」に1行足す（照合はその行の頭）
       = -1|-2  … その行を消す（新しい本文は空でよい）
"""
import re
import sys
import io
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CUT_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*(\s*(?:🔧\s*)?／\s*)([^／]*)(／\s*)(.*)$')
SUB_RE = re.compile(r'^(>\s?)(.*)$')


def load(path):
    raw = open(path, encoding='utf-8').read().split('\n')
    cuts, cur, on = [], None, False
    for i, line in enumerate(raw):
        if line.startswith('## 4. 台本'):
            on = True
            continue
        if on and re.match(r'^## \d', line):
            break
        if not on:
            continue
        m = CUT_RE.match(line)
        if m:
            cur = dict(cid=m.group(1), head=i, pic=m.group(3).strip(),
                       src=m.group(5).strip(), lines=[])
            cuts.append(cur)
            continue
        m = SUB_RE.match(line)
        if m and cur is not None and m.group(2).strip():
            cur['lines'].append((i, m.group(2).strip()))
    return raw, {c['cid']: c for c in cuts}, cuts


def norm(t):
    return t.replace('**', '').lstrip('★')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('spec')
    a = ap.parse_args()
    raw, index, cuts = load(a.path)

    plan = []          # (種類, 行番号, 文字列)
    errs = []
    for ln, s in enumerate(open(a.spec, encoding='utf-8'), 1):
        s = s.rstrip('\n')
        if not s.strip() or s.startswith('#'):
            continue
        parts = s.split('\t')
        if len(parts) < 4:
            errs.append('%d行目: タブが足りない: %s' % (ln, s[:40]))
            continue
        cid, tgt, pre, new = parts[0].strip(), parts[1].strip(), parts[2], '\t'.join(parts[3:])
        c = index.get(cid)
        if not c:
            errs.append('%d行目: %s が無い' % (ln, cid))
            continue
        if tgt in ('PIC', 'SRC'):
            cur = c['pic'] if tgt == 'PIC' else c['src']
            if not cur.startswith(pre):
                errs.append('%d行目: %s %s の頭が違う: 期待「%s」実際「%s」'
                            % (ln, cid, tgt, pre, cur[:24]))
                continue
            plan.append((tgt, c['head'], (cid, new)))
            continue
        m = re.match(r'^([+-]?)([123])$', tgt)
        if not m:
            errs.append('%d行目: 対象が不正: %s' % (ln, tgt))
            continue
        sign, k = m.group(1), int(m.group(2)) - 1
        if k >= len(c['lines']):
            errs.append('%d行目: %s に %d行目が無い（%d行）' % (ln, cid, k + 1, len(c['lines'])))
            continue
        lineno, cur = c['lines'][k]
        if not norm(cur).startswith(pre):
            errs.append('%d行目: %s の%d行目の頭が違う: 期待「%s」実際「%s」'
                        % (ln, cid, k + 1, pre, norm(cur)[:24]))
            continue
        if sign == '+':
            plan.append(('INS', lineno, new))
        elif sign == '-':
            plan.append(('DEL', lineno, None))
        else:
            plan.append(('SET', lineno, new))

    if errs:
        print('🔴 照合に失敗したので1件も当てていません（%d件）:' % len(errs))
        for e in errs[:40]:
            print('  ' + e)
        sys.exit(1)

    # 画・出典は行の中身を組み替える。字幕行は後ろから当てて行番号をずらさない。
    for kind, lineno, payload in plan:
        if kind in ('PIC', 'SRC'):
            cid, new = payload
            m = CUT_RE.match(raw[lineno])
            pic = new if kind == 'PIC' else m.group(3).strip()
            src = new if kind == 'SRC' else m.group(5).strip()
            raw[lineno] = '**%s**%s%s%s%s' % (cid, m.group(2), pic, m.group(4), src)
    body = [(k, n, p) for k, n, p in plan if k in ('SET', 'INS', 'DEL')]
    for kind, lineno, new in sorted(body, key=lambda x: -x[1]):
        if kind == 'SET':
            raw[lineno] = '> ' + new
        elif kind == 'INS':
            raw.insert(lineno + 1, '> ' + new)
        else:
            del raw[lineno]

    open(a.path, 'w', encoding='utf-8').write('\n'.join(raw))
    n = {}
    for k, _, _ in plan:
        n[k] = n.get(k, 0) + 1
    print('当てた: ' + ' / '.join('%s=%d' % kv for kv in sorted(n.items())))


if __name__ == '__main__':
    main()
