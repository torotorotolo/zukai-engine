# -*- coding: utf-8 -*-
"""commons_catlist.py — Commons のカテゴリを「1行ずつ読める一覧」にして吐く（2026-09-16・9本目②）。

■ なぜ要るか
    `commons_probe.py` は**数**を出し、`commons_year_probe.py` は**撮影年で割る**。
    どちらも「その欄の物が写っているか」は見ない（→[[feedback-inventory-is-not-usable-material]]）。
    網は候補を絞る道具であって選ぶ道具ではないので、**最後は題を1行ずつ人が読む**。
    この道具は、その「読む一覧」を作る。

■ 何を出すか（1点1行）
    幅x高 / ライセンス / 継承の有無 / 撮影年 / 題 / 説明の先頭
    - 🔴 **継承（share-alike）の有無**を最初に立てる。CC BY-SA だけが動画全体に伝染する。
      CC0・PD・CC BY（2.0/2.5/3.0/4.0）は継承なし＝使える枠
    - 幅1280未満は全画面に使えない（額装か地に回す）ので印を付ける

■ 使い方
    python tools/commons_catlist.py <出力ファイル> <深さ> "Category:..." ["Category:..." ...]
    ⚠️ 出力先は**呼ぶ側が必ず明示する**（→[[feedback-external-tools-wipe-their-output-dir]]）
"""
import json, re, sys, time, urllib.parse, urllib.request
from collections import Counter

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine/1.0 (material research; contact: konariri8@gmail.com)'

# 継承（share-alike）＝動画全体に伝染する札。ここに当たったら使わない
SA = re.compile(r'\bSA\b|share[- ]?alike|GFDL', re.I)


def q(params):
    params = dict(params, format='json', formatversion='2')
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(API, data=data, headers={'User-Agent': UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception:
            if i == 3:
                raise
            time.sleep(2 * (i + 1))


def walk(cat, depth):
    seen, cats, frontier = {cat}, [cat], [cat]
    for _ in range(depth):
        nxt = []
        for c in frontier:
            cont = {}
            while True:
                d = q(dict({'action': 'query', 'list': 'categorymembers', 'cmtitle': c,
                            'cmtype': 'subcat', 'cmlimit': '500'}, **cont))
                for m in d.get('query', {}).get('categorymembers', []):
                    if m['title'] not in seen:
                        seen.add(m['title']); cats.append(m['title']); nxt.append(m['title'])
                if 'continue' in d:
                    cont = d['continue']
                else:
                    break
        frontier = nxt
    return cats


def files_of(cats):
    out = []
    for c in cats:
        cont = {}
        while True:
            d = q(dict({'action': 'query', 'list': 'categorymembers', 'cmtitle': c,
                        'cmtype': 'file', 'cmlimit': '500'}, **cont))
            out += [m['title'] for m in d.get('query', {}).get('categorymembers', [])]
            if 'continue' in d:
                cont = d['continue']
            else:
                break
    return sorted(set(out))


def meta(titles):
    rows = []
    for i in range(0, len(titles), 40):
        d = q({'action': 'query', 'titles': '|'.join(titles[i:i + 40]), 'prop': 'imageinfo',
               'iiprop': 'url|size|mime|bitdepth|extmetadata',
               'iiextmetadatafilter': 'DateTimeOriginal|LicenseShortName|ImageDescription|Artist|Credit'})
        for p in d.get('query', {}).get('pages', []):
            ii = (p.get('imageinfo') or [{}])[0]
            em = ii.get('extmetadata', {}) or {}
            g = lambda k: str((em.get(k, {}) or {}).get('value', ''))
            desc = re.sub('<[^>]+>', ' ', g('ImageDescription'))
            desc = re.sub(r'\s+', ' ', desc).strip()
            date = g('DateTimeOriginal')
            yr = (re.search(r'(1[89]\d\d|20\d\d)', date) or [''])
            yr = yr.group(1) if hasattr(yr, 'group') else ''
            rows.append({
                'title': p['title'].replace('File:', ''),
                'w': ii.get('width', 0), 'h': ii.get('height', 0),
                'mime': ii.get('mime', ''), 'bits': ii.get('bitdepth', 0),
                'lic': g('LicenseShortName'), 'year': yr, 'desc': desc[:150],
            })
    return rows


def main():
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(2)
    out, depth, cats = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    allcats = []
    for c in cats:
        allcats += walk(c, depth)
    allcats = list(dict.fromkeys(allcats))
    titles = files_of(allcats)
    rows = meta(titles)
    usable = [r for r in rows if not SA.search(r['lic'])]
    lines = []
    lines.append(f'# Commons カテゴリ一覧  分類{len(allcats)}件 / ファイル{len(rows)}点')
    lines.append(f'# 継承なし（使える枠）: {len(usable)}点 / 継承あり（CC BY-SA・使えない）: {len(rows)-len(usable)}点')
    lines.append('# ライセンス内訳: ' + json.dumps(dict(Counter(r["lic"] for r in rows)), ensure_ascii=False))
    lines.append('# 種類内訳: ' + json.dumps(dict(Counter(r["mime"] for r in rows)), ensure_ascii=False))
    lines.append('')
    lines.append('## 継承なし（幅の大きい順）')
    for r in sorted(usable, key=lambda r: -r['w']):
        flag = '  ' if r['w'] >= 1280 else '小'
        vid = '🎞' if r['mime'].startswith('video') else ' '
        lines.append(f'{flag}{vid} {r["w"]:>5}x{r["h"]:<5} {r["year"]:<5} {r["lic"]:<16} | {r["title"][:78]} | {r["desc"][:80]}')
    lines.append('')
    lines.append('## 継承あり＝CC BY-SA（使わない。参考）')
    for r in sorted([r for r in rows if SA.search(r['lic'])], key=lambda r: -r['w'])[:40]:
        lines.append(f'   {r["w"]:>5}x{r["h"]:<5} {r["year"]:<5} {r["lic"]:<16} | {r["title"][:78]}')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'書いた: {out}  分類{len(allcats)} ファイル{len(rows)} 継承なし{len(usable)}')


if __name__ == '__main__':
    main()
