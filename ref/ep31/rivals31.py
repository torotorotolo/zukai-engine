# -*- coding: utf-8 -*-
"""31本目 ① 競合の数え（YouTube Data API v3＝公式の窓口・動画は落とさない）。

なぜ API か：youtube.com の robots.txt は `User-agent: *` に `Disallow: /results` と
`Disallow: /youtubei/` を書いている（2026-11-06 に確かめた）。yt-dlp の検索（ytsearch・検索の頁）は
この道を通るので、30本目までの rivals30.py の形は使わない。

  python -X utf8 ref/ep31/rivals31.py <出力フォルダ（git の外）>

費用＝videos.list 1単位（50本まで）＋ search.list 100単位 × 語の数（既定 3語＝約300単位）。
結果の JSON は出力フォルダへ（リポに入れない）。名前は出さない（題・局・尺・数・章の題・資料の行だけ）。
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

# pool.json（09-08 の写し）で「雫石」に当たった7本
POOL_IDS = ['EqJ2FthseXQ', '9XnJVMdrwJI', '5CoHioQXm8w', 'bE9Vtx4W9AU',
            'fRcopNhs-EM', 'GA0YpVJH320', 'mnDNR0fkLhI']
AFTER = '2026-09-08T00:00:00Z'  # 母集団を測った日＝これより後の回を外で拾う
WORDS = ['雫石 衝突事故', '全日空 自衛隊機 衝突']
HIT = ['雫石', '全日空58', 'ANA58']
MOD_WORD = '昭和46年 防衛庁記録'  # 防衛省の記録映像の年の版があるか


def nf(s):
    return unicodedata.normalize('NFKC', s or '')


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


def show(it):
    sn, cd, st = it['snippet'], it['contentDetails'], it.get('statistics', {})
    sec = iso_sec(cd.get('duration'))
    desc = sn.get('description', '')
    chap = [ln.strip() for ln in desc.split('\n') if re.match(r'\s*\d{1,2}:\d{2}', ln)]
    src = [ln.strip() for ln in desc.split('\n')
           if re.search(r'参考|出典|資料|引用|報告書|文献|Wikipedia|wiki', ln)]
    print(f"- {it['id']} | {sn['channelTitle']} | {sn['publishedAt'][:10]} | "
          f"{sec // 60 if sec else '?'}分{sec % 60 if sec else ''}秒 | 再生 {st.get('viewCount')} | "
          f"license={it.get('status', {}).get('license')}")
    print(f"    題：{sn['title']}")
    print(f"    章 {len(chap)}：" + ' / '.join(c[:40] for c in chap[:14]))
    for ln in src[:6]:
        print(f"    資料の行：{ln[:150]}")


def main():
    yt = P._yt()
    raw = {}
    print('== pool の7本（いまの数）')
    items = details(yt, POOL_IDS)
    raw['pool'] = items
    for it in items:
        show(it)
    print(f'== 母集団の外（{AFTER[:10]} より後・語 {len(WORDS)}）')
    new = []
    raw['search'] = {}
    for w in WORDS:
        r = yt.search().list(part='snippet', q=w, type='video', maxResults=50,
                             publishedAfter=AFTER, regionCode='JP',
                             relevanceLanguage='ja').execute()
        raw['search'][w] = r
        got = [x for x in r.get('items', []) if any(h in nf(x['snippet']['title']) for h in HIT)]
        print(f"  語「{w}」：{len(r.get('items', []))}件のうち題に当たり {len(got)}")
        for x in got:
            vid = x['id']['videoId']
            if vid not in POOL_IDS and vid not in new:
                new.append(vid)
    if new:
        items2 = details(yt, new)
        raw['new'] = items2
        for it in items2:
            show(it)
    else:
        print('  新しい回 0本')
    print(f'== 防衛省の記録映像（語「{MOD_WORD}」）')
    r = yt.search().list(part='snippet', q=MOD_WORD, type='video', maxResults=25,
                         regionCode='JP', relevanceLanguage='ja').execute()
    raw['mod'] = r
    for x in r.get('items', []):
        sn = x['snippet']
        print(f"  {x['id']['videoId']} | {sn['channelTitle']} | {sn['publishedAt'][:10]} | {sn['title'][:60]}")
    with open(os.path.join(OUT, 'rivals31_raw.json'), 'w', encoding='utf-8') as f:
        json.dump(raw, f, ensure_ascii=False, indent=1)
    print('単位の見込み＝videos.list', 1 + (1 if new else 0), '＋ search.list', (len(WORDS) + 1) * 100)


if __name__ == '__main__':
    main()
