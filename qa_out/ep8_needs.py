# -*- coding: utf-8 -*-
"""⑤b：実写103カットの欄に、台帳の中で**当たりが在るか**をまとめて数える。

■ なぜ要るか
  ②の網は「候補」を絞る道具で、**欄が別物を拾っていた実績が4件ある**
  （`debris_field` `reentry` `test` `orbit`）。⑤bはカット単位で確かめる必要があるが、
  103回 `pick` を叩くと往復だけで潰れる。**まず件数だけ一気に出して、
  0件の欄と、読む価値のある欄を分ける。**

■ ⚠️ これは「在るか」を測る道具。「写っているか」は測っていない
  件数が出た欄は `qa_out/ep8_pick.py` で1行ずつ読む。
  → [[feedback-inventory-is-not-usable-material]]

■ 🔴 陽性対照（道具そのものを検算する）
  `--selftest` で、②が読んで**本物だと確かめた欄**と**別物だと分かった欄**の
  両方に当てる。前者が0件、または後者が本物を名乗ったら、この道具が壊れている。
  → [[feedback-verify-your-own-instrument]]

    python qa_out/ep8_needs.py
    python qa_out/ep8_needs.py --selftest
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from ep8_pick import load, caption           # noqa: E402

# カット → (欄の名, 当てる語). 語は**説明文の英語**に当てる。
# ⚠️ 「同型」と書いてある欄（c604 c615）は、別のミッションの写真で代用することになる。
#    採るかどうかは件数ではなく、**その物が写っているか**で決める。
NEEDS = [
    # ── 冒頭 ──
    ('pr01', 'KSC の滑走路', r'shuttle landing facility|landing facility|runway 33|runway 15'),
    ('pr02', 'テキサス東部の空', r'east texas.*sky|sky over texas|contrail'),
    ('pr03', '乗員7名の公式写真', r'crew portrait|official portrait|sts-107 crew|crew members pose'),
    ('pr05', '2003-01-16 の打ち上げ', r'lift[- ]?off|launch of.*columbia|hurtles'),
    ('pr07', '追跡フィルムの確認', r'film|photograph(ic|y) (lab|team)|processing.*film'),
    ('pr09', '軌道上の乗員', r'sts107-\d|on[- ]orbit|in the spacehab'),
    ('pr11', '報告書の表紙', r'report cover|volume i|final report'),
    # ── 第1章 ──
    ('c101', 'STS-1 の打ち上げ 1981', r'sts-1\b|first space shuttle (flight|launch)|april 12, 1981'),
    ('c102', 'ヤングとクリッペン', r'young and crippen|crippen|john w\. young'),
    ('c103', '発射台の全景', r'launch pad 39|rotating service structure|mobile launcher'),
    ('c104', 'オービタ地上の全景', r'orbiter columbia|columbia is towed|orbiter processing'),
    ('c106', '外部タンク', r'external tank'),
    ('c108', '外部タンクの表面', r'external tank.*(foam|surface|insulat)'),
    ('c114', '5機のオービタ', r'fleet|five orbiters|orbiter fleet'),
    ('c115', '中デッキ・気密室', r'middeck|mid-deck|airlock'),
    ('c117', '翼の前のふち', r'leading edge|rcc panel|reinforced carbon'),
    # ── 第2章 ──
    ('c201', '前夜の発射台', r'launch pad.*(night|evening|xenon)|floodlight'),
    ('c202', '搭乗（ホワイトルーム）', r'white room|suits up|ingress|astronaut van'),
    ('c203', '打ち上げ前の射点', r'pad 39-a|launch pad 39a|ready for launch'),
    ('c204', '打ち上げの瞬間', r'spewing flames|blast off|thunder'),
    ('c210', '追跡カメラの画', r'seconds after t-0|tracking camera'),
    ('c212', '射点まわりの追跡カメラ', r'tracking camera|camera site|e-?21[0-9]\b'),
    ('c215', '軌道上のコロンビア（初日）', r'flight day 1|fd01|first day'),
    ('c217', '外部タンクの分離', r'tank separation|et sep|jettison'),
    ('c219', 'バイポッド部', r'bipod'),
    ('c222', 'STS-112 の打ち上げ', r'sts-112'),
    # ── 第3章 ──
    ('c302', '現像したてのフィルム', r'film|negative|darkroom'),
    ('c305', '解析にかけたコマ', r'80-84 seconds|81-82 seconds'),
    ('c308', '画像を解析する作業', r'image analysis|analyz|enhanc'),
    ('c314', '国家画像地図局', r'nima|national imagery'),
    ('c318', '報告を配る作業', r'e-?mail|memo'),
    ('c320', '週末の作業場', r'weekend'),
    # ── 第4章 ──
    ('c401', '船内での集合', r'sts107-735|crew.*(pose|portrait).*(orbit|middeck)|in-flight'),
    ('c402', 'ハズバンドとマクール', r'husband|mccool'),
    ('c403', 'アンダーソンとブラウン', r'anderson|brown'),
    ('c404', 'チャウラとクラーク', r'chawla|clark'),
    ('c406', 'スペースハブ', r'spacehab|research double module'),
    ('c408', '実験に取り組む乗員', r'experiment|microgravity|payload specialist.*work'),
    ('c409', '軌道上の記者会見', r'in-flight (press|news)|crew news conference'),
    ('c415', '機内で作業する乗員', r'sts107-\d{3}-\d'),
    ('c420', '軌道から見た地球', r'earth (observation|limb)|sunrise|from the crew cabin'),
    # ── 第5章 ──
    ('c502', 'デブリ評価チーム', r'debris assessment'),
    ('c508', '米戦略軍（司令部）', r'strategic command|usstratcom|cheyenne|colorado springs'),
    ('c509', '運用評価室', r'mission evaluation room'),
    ('c511', '計算に向かう技術者', r'engineer'),
    ('c513', '落ちる氷（過去の飛行）', r'\bice\b|icicle|debris shed'),
    ('c517', '説明会の資料の頁', r'viewgraph|briefing (chart|slide)|presentation'),
    ('c522', 'ミッション運営チームの会議室', r'mission management team|mmt'),
    ('c524', '1月24日の説明会', r'january 24'),
    ('c527', '議事録', r'minutes|transcript'),
    # ── 第6章 ──
    ('c604', 'リチウムハイドロキシド缶', r'lithium hydroxide|lioh'),
    ('c606', 'アトランティス号', r'atlantis'),
    ('c608', '組立棟の固体ロケット＋タンク', r'solid rocket booster and external tank'),
    ('c615', '船内の工具', r'\btool\b|tool box|toolbox'),
    ('c619', '貨物室', r'payload bay'),
    ('c621', '委員会の会合', r'accident investigation board|gehman'),
    # ── 第7章 ──
    ('c703', 'インド洋上空の軌道', r'indian ocean'),
    ('c707', '記録装置 MADS', r'\bmads\b|modular auxiliary data|oex recorder'),
    ('c709', '左翼の前のふち（構造）', r'left wing|wing leading edge|spar'),
    ('c711', 'カリフォルニア沖の夜明け', r'california|dawn|sunrise'),
    ('c715', 'ネバダ上空の光', r'nevada'),
    ('c717', 'アルバカーキ上空', r'albuquerque|new mexico'),
    ('c723', '途切れた電波の記録', r'telemetry|loss of signal'),
    # ── 第8章 ──
    ('c802', '通報を受ける現場', r'nacogdoches|hemphill|lufkin|911 call'),
    ('c803', '落下した破片（地上）', r'debris (found|on the ground|in a field)|piece of debris'),
    ('c805', '捜索に入る隊列', r'searchers|search team|volunteer'),
    ('c806', '列を組んで歩く捜索', r'scour|walking (grid|line)|shoulder to shoulder|systematically'),
    ('c808', '沼と藪の捜索', r'forest|woods|swamp|brush|creek'),
    ('c809', 'ヘリコプター', r'helicopter'),
    ('c811', '破片の集積所', r'collection (point|site)|barksdale|corsicana|staging'),
    ('c813', '格納庫に並べられた破片', r'rlv hangar|debris hangar|reconstruction'),
    ('c815', '左翼前縁の再構成', r'leading edge.*(grid|reconstruct)|reconstruct.*wing'),
    ('c817', '記録装置の回収', r'oex|recorder|powerhead|main engine'),
    ('c819', '破片を返しに来る人', r'turn(ed)? in|returned (a )?(piece|debris)'),
    # ── 第9章 ──
    ('c901', '委員会の会合', r'board (member|meet)|hearing|testimony'),
    ('c903', '焼け抜けた破片', r'burn|slag|erosion|melted'),
    ('c905', 'NASA本部', r'headquarters|washington'),
    ('c907', '衝突試験', r'impacted by foam|impact test|southwest research|swri'),
    ('c909', '安全を担当する部署', r'safety'),
    ('c911', '1986年チャレンジャー号', r'challenger'),
    ('c915', '報告書のページ', r'report'),
    # ── 締め ──
    ('ep04', '2003年、湖を潜った捜索', r'toledo bend|lake|dive|diver|sonar'),
]

# 🔴 陽性対照：②が**読んで本物と確かめた**欄（必ず当たる）と、
#    ②が**別物だと分かった**欄（当たっても中身が違う＝件数で判断してはいけない例）
SELFTEST_HIT = [
    ('格納庫の再構成（395点あるはず）', r'rlv hangar|debris hangar|reconstruction', 100),
    ('衝突のコマ（2点あるはず）', r'8[01]-8[24] seconds after t-0', 2),
    ('CAIB の視察（143点あるはず）', r'accident investigation board', 100),
]
SELFTEST_TRAP = [
    ('野外の捜索を "field" で引くと格納庫が混ざる', r'\bfield\b'),
]


def count(rx):
    r = re.compile(rx, re.I)
    return [it for it in load() if r.search(caption(it))]


def selftest():
    ok = True
    items = load()
    print(f'台帳 {len(items)} 件（3冊を nasa_id で潰した数）\n')
    print('── 当たらねばならない欄（0件なら道具が壊れている）──')
    for name, rx, least in SELFTEST_HIT:
        n = len(count(rx))
        good = n >= least
        ok &= good
        print(f'  {"✓" if good else "🔴"} {name:<34} {n:>4}件（{least}件以上を期待）')
    print('\n── 件数で判断してはいけない例（②が実際に踏んだ）──')
    for name, rx in SELFTEST_TRAP:
        hits = count(rx)
        hangar = sum(1 for it in hits
                     if re.search(r'hangar|reconstruction', caption(it), re.I))
        print(f'  ⚠️ {name}')
        print(f'     {len(hits)}件 当たり、うち **{hangar}件が格納庫**'
              f'（＝野外ではない）。件数だけ見ると在庫に見える')
        ok &= hangar > 0        # 罠が再現しなければ、台帳か語が変わっている
    return ok


def cand(prefix, n=4, chars=150):
    """欄ごとに候補を上から n 件、**説明文つき**で出す（読むための表）。

    並びは「2003年が先 → 幅が広い順」。⚠️ 並びは読む順を決めるだけで、
    採否は説明文を読んで決める（幅が広い＝写っている、ではない）。
    """
    for cid, what, rx in NEEDS:
        if prefix and not cid.startswith(tuple(prefix)):
            continue
        hits = count(rx)
        hits.sort(key=lambda it: (it.get('year') != 2003, -(it.get('w') or 0)))
        print(f'\n━━ {cid}  {what}  （当たり {len(hits)}）')
        if not hits:
            print('   🔴 0件 → 図へ落とす')
            continue
        for it in hits[:n]:
            w, h = it.get('w'), it.get('h')
            print(f"   {it['nasa_id']:<22} {it.get('date_created','')[:10]} "
                  f"{f'{w}x{h}' if w else '未測':<10} {(it.get('center') or ''):<6}"
                  f" {caption(it)[:chars]}")


def main():
    if '--selftest' in sys.argv:
        sys.exit(0 if selftest() else 1)
    if '--cand' in sys.argv:
        i = sys.argv.index('--cand')
        pre = [a for a in sys.argv[i + 1:] if not a.startswith('-')]
        n = 4
        if '-n' in sys.argv:
            n = int(sys.argv[sys.argv.index('-n') + 1])
        cand(pre, n)
        return
    items = load()
    print(f'台帳 {len(items)} 件（3冊を nasa_id で潰した数）')
    print('⚠️ 件数は「候補」。0件＝図へ落とす確定。1件以上＝pick で1行ずつ読む\n')
    zero = []
    for cid, what, rx in NEEDS:
        hits = count(rx)
        big = sum(1 for it in hits if (it.get('w') or 0) >= 1280)
        y03 = sum(1 for it in hits if it.get('year') == 2003)
        mark = '🔴 0件' if not hits else ('⚠️ 幅不足' if not big else '   ')
        if not hits:
            zero.append(cid)
        print(f'{mark} {cid:<7} {what:<24} 当たり{len(hits):>4} '
              f'／幅1280以上 {big:>4} ／2003年 {y03:>4}')
    print(f'\n🔴 0件＝図へ落とすしかない欄（{len(zero)}件）: {" ".join(zero)}')


if __name__ == '__main__':
    main()
