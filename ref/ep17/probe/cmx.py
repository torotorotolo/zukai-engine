# -*- coding: utf-8 -*-
"""16本目②：Commons の分類を歩いて、1点1行の台帳を作る（scratchpad 専用・tools/ は直さない）。
使い方:
  python cmx.py tree  <out.txt> <depth> <Category:...>...   # 分類の木と点数だけ
  python cmx.py files <out.tsv> <depth> <Category:...>...   # 1点1行（権利・作者・日付・大きさ・隠しカテゴリ）
"""
import json, sys, time, urllib.parse, urllib.request

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine/1.0 (ep17 material research)'


def q(params, tries=6):
    params = dict(params, format='json', formatversion='2')
    url = API + '?' + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # 429 などは間を空けて再試行
            time.sleep(5 * (i + 1))
            last = e
    raise last


def members(cat, cmtype):
    out, cont = [], {}
    while True:
        d = q(dict(action='query', list='categorymembers', cmtitle=cat, cmtype=cmtype, cmlimit='500', **cont))
        out += [m['title'] for m in d['query']['categorymembers']]
        if 'continue' not in d:
            return out
        cont = {'cmcontinue': d['continue']['cmcontinue']}
        time.sleep(1)


def walk(roots, depth):
    seen, files, order = set(), {}, []
    stack = [(c, 0, None) for c in roots]
    while stack:
        cat, lv, parent = stack.pop(0)
        if cat in seen:
            continue
        seen.add(cat)
        fs = members(cat, 'file')
        subs = members(cat, 'subcat') if lv < depth else []
        order.append((lv, cat, len(fs), len(subs)))
        for f in fs:
            files.setdefault(f, cat)
        stack += [(s, lv + 1, cat) for s in subs]
        time.sleep(1)
    return order, files


def info(titles):
    rows = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        d = q(dict(action='query', titles='|'.join(chunk), prop='imageinfo|categories',
                   iiprop='url|size|mime|extmetadata|bitdepth', iiurlwidth='640',
                   clshow='hidden', cllimit='500'))
        for p in d['query']['pages']:
            ii = (p.get('imageinfo') or [{}])[0]
            em = ii.get('extmetadata', {})
            g = lambda k: (em.get(k, {}) or {}).get('value', '')
            rows[p['title']] = dict(
                w=ii.get('width', 0), h=ii.get('height', 0), mime=ii.get('mime', ''), bd=ii.get('bitdepth', ''),
                lic=g('LicenseShortName'), terms=g('UsageTerms'), artist=g('Artist'), credit=g('Credit'),
                dto=g('DateTimeOriginal'), desc=g('ImageDescription'), url=ii.get('url', ''),
                thumb=ii.get('thumburl', ''), page=ii.get('descriptionurl', ''),
                hidden=[c['title'].replace('Category:', '') for c in p.get('categories', [])])
        time.sleep(2)
    return rows


def strip(s):
    import re, html
    s = re.sub(r'<[^>]+>', ' ', s or '')
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


if __name__ == '__main__':
    mode, out, depth, roots = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4:]
    order, files = walk(roots, depth)
    with open(out, 'w', encoding='utf-8') as fo:
        if mode == 'tree':
            for lv, cat, nf, ns in order:
                fo.write(f"{'  ' * lv}{cat}\tfiles={nf}\tsubcats={ns}\n")
            fo.write(f'TOTAL unique files={len(files)}\n')
        else:
            rows = info(list(files))
            cols = ['title', 'cat', 'w', 'h', 'mime', 'bd', 'lic', 'artist', 'credit', 'dto', 'hidden', 'desc', 'page', 'thumb', 'url']
            fo.write('\t'.join(cols) + '\n')
            for t, cat in files.items():
                r = rows.get(t, {})
                vals = [t, cat, r.get('w', ''), r.get('h', ''), r.get('mime', ''), r.get('bd', ''), strip(r.get('lic', '')),
                        strip(r.get('artist', ''))[:120], strip(r.get('credit', ''))[:120], strip(r.get('dto', ''))[:60],
                        '|'.join(r.get('hidden', [])), strip(r.get('desc', ''))[:400], r.get('page', ''), r.get('thumb', ''), r.get('url', '')]
                fo.write('\t'.join(str(v).replace('\t', ' ') for v in vals) + '\n')
    print('done', len(files))
