# -*- coding: utf-8 -*-
"""ep9_slots.py — 9本目テネリフェの素材を「欄ごと」に確定して JSON に落とす（2026-09-16・②素材）。

■ なぜ要るか
    `commons_catlist.py` は分類の中身を1行ずつ読める形にする。そこまでは網の仕事。
    **選ぶのは人**なので、読んだ結果（＝どの点をどの欄に当てるか）をここに書き留める。
    ⚠️ 欄の名前は「その物が写っていないと書けない文」で作る
    （→[[feedback-inventory-is-not-usable-material]]）。

■ 継承（share-alike）の扱い
    🔴 CC BY-SA は**使わない**。継承が動画全体に伝染する。
    CC0 / Public domain / CC BY(2.0,2.5,3.0,4.0) だけを入れる。
    この道具は取得した extmetadata で**もう一度**継承を検査し、当たったら落として警告する。

■ 使い方
    python tools/ep9_slots.py ref/ep9/slots_commons.json
"""
import json, re, sys, time, urllib.parse, urllib.request

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine/1.0 (material research; contact: konariri8@gmail.com)'
SA = re.compile(r'\bSA\b|share[- ]?alike|GFDL', re.I)

# 欄 -> Commons のファイル名（File: は付けない）。②で一覧を1行ずつ読んで選んだもの
SLOTS = {
    # ── 事故そのもの（1977-03-27・Anefo／オランダ国立公文書館 CC0）───────────
    'wreck_klm': [
        'Het verongelukte KLM-toestel De Rijn, Bestanddeelnr 929-1003.jpg',
        'Het verongelukte KLM-toestel De Rijn, Bestanddeelnr 929-1004.jpg',
        'Het verongelukte KLM-toestel De Rijn, Bestanddeelnr 929-1005.jpg',
    ],
    'wreck_both': [
        'Eén de twee verongelukte toestellen, Bestanddeelnr 929-1006.jpg',
        'Beeld van één van de twee verongelukte toestellen, Bestanddeelnr 929-1007.jpg',
    ],
    'wreck_engine': [
        'Vliegtuigmotor van één van de verongelukte jumbojets, Bestanddeelnr 929-1008.jpg',
    ],
    # ── 事故機そのもの ───────────────────────────────────────────────
    'panam_n736pa': [
        'Pan Am Boeing 747-121 N736PA at Sydney.jpg',
    ],
    # ⚠️ PH-BUF（KLM機）そのものは Commons に2点あるが**両方 CC BY-SA＝使えない**。
    #    代わりに「同じ型のKLMの747」を使い、副題でそう書く
    'klm_747_same_type': [
        'De Boeing 747 aan de pier op het platform, Bestanddeelnr 923-6386.jpg',
        'De Boeing 747 zet de landing in, Bestanddeelnr 923-6390.jpg',
        'De Boeing 747 taxiet naar aankomstplaats op Schiphol, Bestanddeelnr 923-6398.jpg',
    ],
    'panam_747_same_type': [
        'Pan Am (Boeing 747).jpg',
        'Pan Am Clipper B747-121.jpg',
        'Photograph of President Gerald R. Ford Carrying a Vietnamese Baby from Clipper 1742, One of the Operation Babylift Planes that Transported Approximately 325 South Vietnamese Orphans from Saigon to the United State(...) - NARA - 7839930.jpg',
    ],
    # ── ジャンボ機の登場（1969-70）──────────────────────────────────
    'jumbo_era': [
        'Pat Nixon christens Boeing 747 2749-18.jpg',
        'Een model van een Boeing jumbo jet, Bestanddeelnr 922-6599.jpg',
        'Een model van het interieur van een Boeing jumbo jet, Bestanddeelnr 922-6598.jpg',
        'Een model van het interieur van een Boeing jumbo jet, Bestanddeelnr 922-6600.jpg',
        'Pat Nixon in first 747.png',
    ],
    # ── ロス・ロデオス（テネリフェ北）空港 ─────────────────────────────
    'losrodeos_1930': [
        'Primer vuelo Península - Canarias (1930).jpg',
    ],
    'losrodeos_now': [
        'Santa Cruz de Tenerife airport runway, Canary Islands, Spain - panoramio.jpg',
        'Santa Cruz de Tenerife airport runway, Canary Islands, Spain - panoramio (1).jpg',
        'Santa Cruz de Tenerife airport runway landing system, Canary Islands, Spain - panoramio.jpg',
        'Tenerife North Airport radar.jpg',
        'Bell 412SP aterrizando en el aeropuerto de Los Rodeos (Tenerife Norte).jpg',
        'Plataforma tfn.jpg',
        'Terminal tfn.jpg',
        'Tenerife lennujaam.jpg',
    ],
    # ── グランカナリア（ラスパルマス）空港 ─────────────────────────────
    'laspalmas_now': [
        'Aeropuerto de Gran Canaria interior (5195390363).jpg',
        'Aeropuerto de Gran Canaria interior (5195391885).jpg',
        'Check-In Aeropuerto de Gran Canaria (5195973172).jpg',
        'Gates (5195996258).jpg',
        'Boarding (5196003292).jpg',
        'Busy traveller (5195388141).jpg',
        'Aeropuerto de Gran Canaria Tower (5195405623).jpg',
        'Tower - panoramio (34).jpg',
        'Airporttower(Cran Canaria) - panoramio.jpg',
        'Aeropuerto LPA Gran Canaria.jpg',
        'Gran Canaria International Airport R01.jpg',
        'Planes (10136783155).jpg',
        'In Reih und Glied - panoramio.jpg',
        'Airport(Eingang) - panoramio.jpg',
        'Boarding aircraft (5195400705).jpg',
        'Boarding rear door (5195398367).jpg',
    ],
    # ── 機体の部位 ────────────────────────────────────────────────
    'cockpit_747': [
        'KLM Boeing 747 Cockpit.jpg',
    ],
    'engine_747': [
        'Jet engine (5195403907).jpg',
    ],
    # ── オランダ側の後日（1977-03-28〜04-07・Anefo CC0）────────────────
    'nl_crisis': [
        'Crisiscentrum te Amstelveen, Bestanddeelnr 929-0963.jpg',
        'Crisiscentrum te Amstelveen, Bestanddeelnr 929-0964.jpg',
        'Overzicht crisiscentrum te Amstelveen, Bestanddeelnr 929-0965.jpg',
        'Vlaggen halfstok voor het KLM-hoofdkantoor te Amstelveen, Bestanddeelnr 929-0961.jpg',
        'President-directeur van KLM Orlandini staat de pers te woord, Bestanddeelnr 929-0962.jpg',
    ],
    'nl_mourning': [
        '1 minuut stilte aan het begin van de herdenking, Bestanddeelnr 929-1118.jpg',
        '1 minuut stilte aan het begin van de herdenking, Bestanddeelnr 929-1119.jpg',
        'Toespraak door de president-directeur van KLM, Sergio Orlandini, Bestanddeelnr 929-1120.jpg',
        'Minister-president Den Uyl en minister Westerterp (Verkeer en Waterstaat) langs , Bestanddeelnr 929-1121.jpg',
        'Geëmotioneerde familieleden tijdens de dienst, Bestanddeelnr 929-1122.jpg',
        'De kisten van de slachtoffers van de ramp, Bestanddeelnr 929-1123.jpg',
        'Aanwezigen verlaten de hal aan het einde van de dienst, Bestanddeelnr 929-1124.jpg',
        'Aanwezigen verlaten de hal aan het einde van de dienst, Bestanddeelnr 929-1125.jpg',
        'Slachtoffers, herdenkingen, vliegtuigongevallen, rampen, Bestanddeelnr 929-1126.jpg',
        'Tweede Kamer neemt voor het debat een minuut stilte in acht voor de slachtoffers, Bestanddeelnr 929-0988.jpg',
    ],
    'nl_funeral': [
        'Stoet trekt langs de kisten, Bestanddeelnr 929-1130.jpg',
        'Stoet trekt langs de kisten, Bestanddeelnr 929-1131.jpg',
        'Burgemeester Ivo Samkalden van Amsterdam legt een herdenkingskrans, Bestanddeelnr 929-1132.jpg',
        'Stoet trekt langs de kisten, Bestanddeelnr 929-1133.jpg',
        'Burgemeester Ivo Samkalden van Amsterdam loopt langs de kisten, Bestanddeelnr 929-1134.jpg',
        'Burgemeester Ivo Samkalden van Amsterdam na de kranslegging, Bestanddeelnr 929-1135.jpg',
    ],
    # ── 出発地スキポール空港（1977〜78・CC0）────────────────────────
    # 🔴 KLM 4805 が 9:00z に飛び立った空港。**事故の年そのものの写真**が CC0 で在る
    'schiphol_1977': [
        'HUA-170857-Gezicht op de vertrekhal Noord van de luchthaven Schiphol, vanaf de hal van het in aanbouw zijnde N.S.-station Schiphol.jpg',
        'Proef met gescheiden paspoortcontrole op Schiphol bord in aankomsthal wijst r, Bestanddeelnr 929-2655.jpg',
        'Vliegtuigkijkers bij Schiphol, Bestanddeelnr 929-9386.jpg',
    ],
    'memorial': [
        'International Tenerife Memorial March 27, 1977.jpg',
        'Memorial plaque at International Tenerife Memorial March 27, 1977.jpg',
        'TenerifeMemorial.JPG',
        'VvZ Westgaarde.jpg',
    ],
}


def q(params):
    params = dict(params, format='json', formatversion='2')
    req = urllib.request.Request(API, data=urllib.parse.urlencode(params).encode(),
                                 headers={'User-Agent': UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception:
            if i == 3:
                raise
            time.sleep(2 * (i + 1))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'ref/ep9/slots_commons.json'
    titles = sorted({t for v in SLOTS.values() for t in v})
    info = {}
    for i in range(0, len(titles), 30):
        d = q({'action': 'query', 'titles': '|'.join('File:' + t for t in titles[i:i + 30]),
               'prop': 'imageinfo', 'iiprop': 'url|size|mime|bitdepth|extmetadata',
               'iiextmetadatafilter': 'DateTimeOriginal|LicenseShortName|Artist|Credit|ImageDescription'})
        for p in d.get('query', {}).get('pages', []):
            t = p['title'].replace('File:', '')
            if p.get('missing') or not p.get('imageinfo'):
                info[t] = None
                continue
            ii = p['imageinfo'][0]
            em = ii.get('extmetadata', {}) or {}
            g = lambda k: re.sub('<[^>]+>', '', str((em.get(k, {}) or {}).get('value', ''))).strip()
            info[t] = {'w': ii['width'], 'h': ii['height'], 'mime': ii['mime'],
                       'bits': ii.get('bitdepth', 0), 'lic': g('LicenseShortName'),
                       'year': (re.search(r'(1[89]\d\d|20\d\d)', g('DateTimeOriginal')) or [None]),
                       'artist': g('Artist')[:80], 'credit': g('Credit')[:80],
                       'url': ii['url'], 'page': ii['descriptionurl']}
            y = info[t]['year']
            info[t]['year'] = y.group(1) if hasattr(y, 'group') else ''
    res, bad, miss = {}, [], []
    for slot, ts in SLOTS.items():
        rows = []
        for t in ts:
            m = info.get(t)
            if m is None:
                miss.append((slot, t)); continue
            if SA.search(m['lic']):
                bad.append((slot, t, m['lic'])); continue
            rows.append(dict(m, title=t))
        res[slot] = rows
    tot = sum(len(v) for v in res.values())
    big = sum(1 for v in res.values() for r in v if r['w'] >= 1280)
    payload = {'measured': '2026-09-16', 'episode': 9, 'theme': 'テネリフェ空港衝突事故',
               'note': '②素材。CC BY-SA は継承が動画全体に伝染するので入れていない。'
                       '動く映像は Commons に0本（実測）＝【映像あり】は名乗らない。',
               'total': tot, 'width_ge_1280': big, 'slots': res,
               'rejected_share_alike': bad, 'missing': miss}
    open(out, 'w', encoding='utf-8').write(json.dumps(payload, ensure_ascii=False, indent=1))
    print(f'書いた: {out}  欄{len(res)} 点{tot}（幅1280以上 {big}）')
    if bad:
        print('⚠️ 継承ありで落とした:', bad)
    if miss:
        print('⚠️ 見つからない（題名が違う）:', miss)
    for s, v in res.items():
        print(f'  {s:<22} {len(v):>3}点  最大幅 {max([r["w"] for r in v], default=0)}')


if __name__ == '__main__':
    main()
