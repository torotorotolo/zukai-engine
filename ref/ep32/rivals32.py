# -*- coding: utf-8 -*-
"""32本目 ① 競合の数え（YouTube Data API v3＝公式の窓口・動画は落とさない）。ref/ep31/rivals31.py を写した。

なぜ API か：youtube.com の robots.txt は `User-agent: *` に `Disallow: /results` と
`Disallow: /youtubei/` を書いている（31本目 2026-11-06 に確かめた）＝検索の頁は機械で読まない。

  python -X utf8 ref/ep32/rivals32.py <出力フォルダ（git の外）>

費用＝videos.list 1単位（50本まで）× 2 ＋ search.list 100単位 × 語の数（既定 4語＝約400単位）。
結果の JSON は出力フォルダへ（リポに入れない）。このファイルに人の名前は書かない（題・局・尺・数・章の題・資料の行だけを出す）。
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))
import yt_theme_probe as P  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

# pool.json（09-08 の写し）で 1549便に当たった2本＋同じ局の「ハドソン川の奇跡以前」の1本
POOL_IDS = ['PfIc-CmQUBk', '9kTltq12k9A', 'VbmJmEcDsMU']
MAIN = 'PfIc-CmQUBk'  # 主な競合（ゆっくり事故検証 2026-06-24）＝説明欄の章を全部読む
WORDS = ['ハドソン川の奇跡', 'USエアウェイズ1549便', 'ハドソン川 不時着水']
HIT = ['ハドソン', '1549便', 'USエアウェイズ', 'USエアー', 'USAIRWAYS', 'USAIR', '1549']
FALSE = ['1549973']  # 再生数の字が題に混ざった形は無いが、念のため
PD_WORD = 'US Airways 1549 Coast Guard video'  # 米国の機関（沿岸警備隊）の映像の当たり


def nf(s):
    return unicodedata.normalize('NFKC', s or '').upper().replace(' ', '')


def hit(title):
    t = nf(title)
    return any(nf(h) in t for h in HIT) and not any(f in t for f in FALSE)


def iso_sec(d):
    m = re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    if not m:
        return None
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def details(yt, ids):
    items = []
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part='snippet,contentDetails,statistics,status',
                             id=','.join(ids[i:i + 50])).execute()
        items += r.get('items', [])
    return items


def show(it, full=False):
    sn, cd, st = it['snippet'], it['contentDetails'], it.get('statistics', {})
    sec = iso_sec(cd.get('duration'))
    desc = sn.get('description', '')
    chap = [ln.strip() for ln in desc.split('\n') if re.match(r'\s*\d{1,2}:\d{2}', ln)]
    src = [ln.strip() for ln in desc.split('\n')
           if re.search(r'参考|出典|資料|引用|報告書|文献|NTSB|Wikipedia|wiki|映像|素材', ln)]
    kind = 'ショート' if sec is not None and sec <= 180 else '長い回'
    print(f"- {it['id']} | {sn['channelTitle']} | {sn['publishedAt'][:10]} | "
          f"{sec // 60 if sec else '?'}分{sec % 60 if sec else ''}秒 | {kind} | 再生 {st.get('viewCount')} | "
          f"license={it.get('status', {}).get('license')}")
    print(f"    題：{sn['title']}")
    n = None if full else 14
    print(f"    章 {len(chap)}：" + ' / '.join(c[:60] for c in chap[:n]))
    for ln in src[:None if full else 6]:
        print(f"    資料の行：{ln[:200]}")


def main():
    yt = P._yt()
    raw = {}
    print('== pool の3本（いまの数）')
    items = details(yt, POOL_IDS)
    raw['pool'] = items
    for it in items:
        show(it, full=(it['id'] == MAIN))
    print(f'== 語で探す（日付の制限なし・語 {len(WORDS)}・各50件）')
    new = []
    raw['search'] = {}
    for w in WORDS:
        r = yt.search().list(part='snippet', q=w, type='video', maxResults=50,
                             regionCode='JP', relevanceLanguage='ja').execute()
        raw['search'][w] = r
        got = [x for x in r.get('items', []) if hit(x['snippet']['title'])]
        print(f"  語「{w}」：{len(r.get('items', []))}件のうち題に当たり {len(got)}")
        for x in got:
            vid = x['id']['videoId']
            if vid not in POOL_IDS and vid not in new:
                new.append(vid)
    if new:
        items2 = details(yt, new)
        raw['new'] = items2
        items2.sort(key=lambda it: it['snippet']['publishedAt'])
        for it in items2:
            show(it)
    else:
        print('  新しい回 0本')
    print(f'== 米国の機関の映像の当たり（語「{PD_WORD}」）')
    r = yt.search().list(part='snippet', q=PD_WORD, type='video', maxResults=25,
                         relevanceLanguage='en').execute()
    raw['pd'] = r
    for x in r.get('items', []):
        sn = x['snippet']
        print(f"  {x['id']['videoId']} | {sn['channelTitle']} | {sn['publishedAt'][:10]} | {sn['title'][:70]}")
    with open(os.path.join(OUT, 'rivals32_raw.json'), 'w', encoding='utf-8') as f:
        json.dump(raw, f, ensure_ascii=False, indent=1)
    print('単位の見込み＝videos.list', 1 + (1 if new else 0), '＋ search.list', (len(WORDS) + 1) * 100)


if __name__ == '__main__':
    main()
