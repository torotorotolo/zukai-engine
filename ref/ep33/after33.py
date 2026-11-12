# -*- coding: utf-8 -*-
"""33本目 ① 母集団の外（09-08 より後）の回を、14局のアップロード一覧から拾う（YouTube Data API v3・動画は落とさない）。

なぜ一覧か：search.list は1回100単位で、題に名前の無い回を取りこぼす。各局のアップロード一覧
（playlistItems.list＝1単位で50本）なら、09-08 より後に出た回を名前に関係なく全部拾える。
youtube.com の robots.txt は /results と /youtubei/ を拒否する（2026-11-06 に確かめた）＝yt-dlp の検索は使わない。

  python -X utf8 ref/ep33/after33.py <出力フォルダ（git の外）>

出すもの（出力フォルダへ・リポに入れない）：
  after33_rows.json  … 09-08 より後の回（pool.json と同じ形＝id/title/channel/sec/views/published）
  after33_peers.json … 近所の幅のために取り直した、07-25〜09-07 の pool の回のいまの数
近所比は pool.json（09-08 の数）と混ぜない。ここでの比は「いまの数どうし」の別の物差し＝記録だけ。
費用＝playlistItems 1単位×頁＋videos.list 1単位×50本ごと（見込み 20〜40単位）。
"""
import json
import os
import sys
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import yt_theme_probe as P  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

AFTER = '2026-09-08'      # pool.json の最新の公開日の翌日＝ここから後を拾う
PEER_FROM = '2026-07-25'  # 09-08 直後の回の「前後45日」に入る pool の回
CH_FILE = os.path.join(ROOT, 'analytics', 'themes', 'genre_channels.json')
POOL = os.path.join(ROOT, 'ref', 'themes', 'pool.json')
UNITS = {'playlistItems': 0, 'videos': 0}


def iso_sec(dur):
    import re
    m = re.fullmatch(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', dur or '')
    if not m:
        return None
    d_, h, mi, s = (int(x) if x else 0 for x in m.groups())
    return d_ * 86400 + h * 3600 + mi * 60 + s


def details(yt, ids):
    rows = []
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part='snippet,contentDetails,statistics',
                             id=','.join(ids[i:i + 50]), maxResults=50).execute()
        UNITS['videos'] += 1
        for it in r.get('items', []):
            sn, cd, st = it['snippet'], it['contentDetails'], it.get('statistics', {})
            rows.append({'id': it['id'], 'title': sn['title'], 'channel': sn['channelTitle'],
                         'sec': iso_sec(cd.get('duration')), 'views': int(st.get('viewCount', 0)),
                         'published': sn['publishedAt'][:10], 'live': sn.get('liveBroadcastContent')})
    return rows


def main():
    pool = json.load(open(POOL, encoding='utf-8'))
    pool_ch = {r['channel'] for r in pool}
    chans = [c for c in json.load(open(CH_FILE, encoding='utf-8')) if c['title'] in pool_ch]
    print(f'局 {len(chans)}（pool.json の局と名前で突き合わせ）／pool の最短 {min(r["sec"] for r in pool)}秒')
    yt = P._yt()
    new_ids = []
    for c in chans:
        tok, got, stop = None, 0, False
        while not stop:
            r = yt.playlistItems().list(part='contentDetails', playlistId=c['uploads'],
                                        maxResults=50, pageToken=tok).execute()
            UNITS['playlistItems'] += 1
            for it in r.get('items', []):
                pub = (it['contentDetails'].get('videoPublishedAt') or '')[:10]
                if not pub:
                    continue
                if pub < AFTER:
                    stop = True
                    continue
                new_ids.append(it['contentDetails']['videoId'])
                got += 1
            tok = r.get('nextPageToken')
            if not tok:
                stop = True
        print(f'  {c["title"][:16]:<16} 09-08 より後 {got}本')
    rows = details(yt, new_ids)
    with open(os.path.join(OUT, 'after33_rows.json'), 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    peer_ids = [r['id'] for r in pool if r['published'] >= PEER_FROM]
    peers = details(yt, peer_ids)
    with open(os.path.join(OUT, 'after33_peers.json'), 'w', encoding='utf-8') as f:
        json.dump(peers, f, ensure_ascii=False, indent=1)
    print(f'09-08 より後の回 {len(rows)}本（うち 180秒未満 {sum(1 for x in rows if (x["sec"] or 0) < 180)}）'
          f'／取り直した pool の回 {len(peers)}本（{len(peer_ids)}本を頼んだ）')
    print('使った単位', UNITS, '計', sum(UNITS.values()))


if __name__ == '__main__':
    main()
