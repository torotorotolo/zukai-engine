# -*- coding: utf-8 -*-
"""23本目④'：係の所見の扱い（直す係の fix_G*.json ＋ G0 の上書き OVR）→ decisions23.json・patches_g0.json・g0_ledger.json・roles_map.json を書き出す（22本目 decide22.py を写し、直す係の扱いの表を読むようにした）。

  python ref/ep23/v2_build/decide23.py

扱いの決め方（上ほど強い）：
  1. OVR（G0＝このチャットの親が原文に引き直して決めた所）
  2. fix_G*.json（直す係が decisions.md に沿って決めた扱い）
  3. どちらにも無い所見＝止める（fail closed＝扱いの決まっていない所見を黙って採らない）
fix の "_extra"（所見に無い直し＝字数の調整・橋）と G0 の足し（下の G0）は patches_g0.json と g0_ledger.json に入る。
聞き役の役割＝第1版の ROLE（v1_build/roles23.py）に、採った所見の "role" を重ねて roles_map.json に書く（手で直さない）。
⚠️ 「採る」で new が空・old が空の所見は止める（old を消してしまうため）。
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'v1_build'))
import roles23                     # noqa: E402  第1版の役割（ROLE）

DEFAULT_NOTE = '係の案どおり（G0 が見た）'
EIZO = '映像方針へ（画の欄の食い違い・画像で決める）'

# G0 の上書き：'id': ('扱い', '理由', {old/new/cut/patches/role})
# 当て直しの係（review_R1・R2＝4'-18）の所見は、G0 が原文に当てて決めた（2026-10-18）
OVR = {
    'R1-001': ('採る', 'K6-市 p.37「소형장비 및 인력 위주의 작업」＝「中心」を落としていた（G0 の字の縮め＝4\'-18 の型）'),
    'R1-002': ('採る', '大96 理由1「4-6㎝(가장 낮은 부분은 13-18㎝) 정도 가라앉은」＝「ほど」と、もっと深い所がある（最も低い所）を戻す。§1-5 の行も G0-031 で直した'),
    'R1-003': ('採る', 'K6-検 p.48 の年表の1〜3次（89.11.27・90.3.9・90.4.24＝사후승인）は開店（89.12.1）の前後＝94年の承認（c617）と分ける'),
    'R1-004': ('採る', 'c614 の「途中の検査」と同じ物と分かるように（大99「중간검사」）'),
    'R1-005': ('採る', 'c606 を「怠った」と書く形にしたので逆接を外す'),
    'R1-006': ('採る', 'c601 の問いと同じ形を避ける'),
    'R2-001': ('採る', 'G0 が K6-検 p.53 別紙3 の15行を足した＝300＋1,300＋1,200＋300＋200＋400＋1,000＋1,300＋1,050＋1,400＋150＋100＋100＋180＋100＝9,080万。市の3人（百貨店の開設承認・虚偽の復命書＝300・200・400）を除く区の12人＝8,180万＝噂（区への総額）と同じ範囲で閉じる（記憶 counterevidence-must-match-the-claims-scope）。§9 は G0-032'),
    'R2-002': ('採る', 'c811 で区を相手の裁判（大99）を言った直後＝小分けの文は大96（会長の刑事の裁判）だけ'),
    'R2-003': ('採る', 'K6-検 p.52 別紙2 は会長も社長も被疑事実の要旨＝どちらも「とされる」'),
    'R2-004': ('採る', '主語のねじれ（中身は K6-検 p.49 どおり）'),
    'R2-005': ('採る', 'c901 の答え（大きく変わる）の片＝大96 理由2.가「차이가 크므로」'),
    'R2-006': ('一部', 'G0 が白書 p85 の頁の画像を原寸で読んだ（画像1枚）＝「민간공사에 대한 준공검사는 공무원이 … 설계도면과 시공이 일치하는지 여부만을 파악하는데 그치고 있다」＝民間は「民間の工事」（検査するのは区の公務員）＝範囲を戻す', {
        'cut': 'ca11',
        'old': '> 白書によれば、建物の竣工の検査は、図面と工事が合っているかを見るだけだった。',
        'new': '> 白書によれば、民間の工事の竣工の検査は、図面と工事が合っているかを見るだけだった。'}),
    'R2-007': ('今のまま', 'cc01 は「どこかで止められなかったか」に「止められる場所」で答え、章の答え（誰なら）は cd04 が人で締める＝どちらもカットの中で問いと答えが合う'),
    'R2-008': ('採る', '§1-4 の記録を第2版に合わせる'),
    'R2-009': ('採る', '§1-4 の円の目安を4か所に'),
    'R2-010': ('採る', '§1-4 ⑩の行き先を第2版に'),
    'R2-011': ('採る', '§1-5 を cb09 の言い方（白書には書かれていない）に'),
    'R2-012': ('採る', '§1-5 を cc10 の言い方（とされる）に'),
    'R2-013': ('採る', '§6 の出る所を第2版で数えた所に'),
    'R2-014': ('済み', '§2・§3 は第1版の数のまま残し、頭に注を足した（G0-033・G0-034）＝第2版の数は §0（v2_head.md＝gates.md の写し）'),
    # ✅ 承認①（2026-10-18・④'のチャットでカズヤくん「承認①は推奨どおりで承認します」）＝台本の文は変えない・§1 に記録（G0-036〜G0-039）
    'G1-012': ('今のまま', '✅ 承認①（10-18）＝題 A のまま（「2時間前」は16時の会議からの丸め＝本編 c105・c310・c311 と同じ事実）'),
    'G7-044': ('今のまま', '✅ 承認①（10-18）＝題 A'),
    'G7-045': ('採らない', '✅ 承認①（10-18）＝題 A に決まった'),
    'G7-046': ('採らない', '✅ 承認①（10-18）＝題 A に決まった'),
    'G7-047': ('今のまま', '✅ 承認①（10-18）＝サムネの赤 A'),
    'G7-048': ('採らない', '✅ 承認①（10-18）＝赤 A に決まった'),
    'G7-049': ('採らない', '✅ 承認①（10-18）＝赤 A に決まった'),
    'G7-050': ('今のまま', '✅ 承認①（10-18）＝問い A（cd09 のまま）'),
    'G7-051': ('採らない', '✅ 承認①（10-18）＝問い A に決まった'),
    'G7-052': ('採らない', '✅ 承認①（10-18）＝問い A に決まった'),
}

# G0 の足し（所見に無い直し）：{'id': 'G0-001', 'cut': …, 'sev': …, 'face': …, 'what': …, 'old': …, 'new': …}
G0 = [
    {'id': 'G0-031', 'cut': '§', 'order': 90, 'sev': '🟢', 'face': 'B', 'what': '§1-5 の上の鉄筋の沈みを c715（R1-002）に合わせる',
     'old': '数センチ深い（記録によって4センチから8センチ）（c715）',
     'new': '記録によって4センチから8センチほど・もっと深い所もあった（大96 の最も低い所 13〜18cm）（c715）'},
    {'id': 'G0-032', 'cut': '§', 'order': 90, 'sev': '🟢', 'face': 'B', 'what': '§9 の cc11 の式（R2-001）',
     'old': "| cc11 | （④'で語りから外した＝噂の1,300万の出どころは言わない・式は記録として残す） | 1,000万＋200万＋100万＝1,300万ウォン（高96 主文1.바） |",
     'new': "| cc11 | 区の12人だけで8,180万ウォン・市の3人を合わせて9,080万ウォン（噂の1,300万の出どころは言わない） | 別紙3 の15行の計9,080万−市の3人（300万＋200万＋400万）＝8,180万（K6-検 p.53）／記録として：1,000万＋200万＋100万＝1,300万ウォン（高96 主文1.바＝2審の3人の追徴の合計・語りでは使わない） |"},
    {'id': 'G0-033', 'cut': '§', 'order': 90, 'sev': '🟢', 'face': 'C', 'what': '§2 の数は第1版のまま＝注（R2-014）',
     'old': '| OK（書いた頁にある・判決は全文にある） | **245** |',
     'new': '| OK（書いた頁にある・判決は全文にある） | **245**（第1版。第2版は260＝§0） |'},
    {'id': 'G0-034', 'cut': '§', 'order': 90, 'sev': '🟢', 'face': 'C', 'what': '§3 の表は第1版の数のまま＝注（R2-014）',
     'old': '## 3. 章ごと（始まりは句読点なし÷365 の積み上げ）',
     'new': '## 3. 章ごと（始まりは句読点なし÷365 の積み上げ）\n\n> ⚠️ この表は第1版（④）の数。第2版の章ごとの数は `v2_build/gates.md` の m23 の「章ごと」（§0 に要約）'},
    {'id': 'G0-035', 'cut': 'cc11', 'order': 99, 'sev': '🟢', 'face': 'F', 'what': '画の欄の記録の札を R2-001 に合わせる（区の12人・8,180万）',
     'old': '記録＝区と市の15人の合計9,080万ウォン＝図の見た目を分ける',
     'new': '記録＝区の12人で8,180万ウォン・市の3人と合わせて9,080万ウォン＝図の見た目を分ける'},
    # ✅ 承認①（2026-10-18）の記録
    {'id': 'G0-036', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'C', 'what': '§1-1 に承認①の記録（題 A）',
     'old': '（G7-046）＝承認①で決める',
     'new': '（G7-046）＝承認①で決める\n- ✅ **承認①（2026-10-18・④\'のチャットでカズヤくん）＝A**（推奨どおり）'},
    {'id': 'G0-037', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'C', 'what': '§1-2 に承認①の記録（赤 A）',
     'old': 'C は「異変」がぼんやり（G7-049）',
     'new': 'C は「異変」がぼんやり（G7-049）\n- ✅ **承認①（2026-10-18）＝A「犠牲502人 店は開いたまま」**（推奨どおり）'},
    {'id': 'G0-038', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'C', 'what': '§1-3 に承認①の記録（問い A）',
     'old': 'C は不安と、身近な店の名指しを招きうる（G7-052）',
     'new': 'C は不安と、身近な店の名指しを招きうる（G7-052）\n- ✅ **承認①（2026-10-18）＝A**（推奨どおり＝cd09 のまま）'},
    {'id': 'G0-039', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'C', 'what': '§1-4 に承認①の記録（cb16・cd07）',
     'old': '遺体は描かない・遺骨の件は写真なし',
     'new': '遺体は描かない・遺骨の件は写真なし\n- ✅ **承認①（2026-10-18・④\'のチャットでカズヤくん＝推奨どおり）**：遺骨と遺品（cb16）＝国会の「ずさん」「慎重さを欠き」を入れた3行（場所の名なし・写真なし・聞き役なし）／2026年の造形（cd07）＝「2026年6月、ソウル市は新しい追悼の造形の作品を選んだ」まで（除幕の月は言わない＝⑥の前に報道は確かめる）'},
]


def main():
    fs = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'findings_G*.json'))) + sorted(glob.glob(os.path.join(HERE, 'review_R*.json'))):
        for x in json.load(open(f, encoding='utf-8')):
            fs[x['id']] = x
    fix, extra = {}, []
    for f in sorted(glob.glob(os.path.join(HERE, 'fix_G*.json'))):
        fx = json.load(open(f, encoding='utf-8'))
        for pid, d in fx.items():
            if pid == '_extra':
                extra += [dict(e, note=e.get('note', '直す係の足し（%s）' % os.path.basename(f))) for e in d]
            else:
                if pid in fix:
                    print('🔴 同じ所見の扱いが2つの fix にある:', pid, os.path.basename(f))
                    sys.exit(1)
                fix[pid] = d
    out, bad = {}, []
    for pid, x in fs.items():
        if pid in OVR:
            o = OVR[pid]
            d = {'v': o[0], 'note': o[1]}
            if len(o) > 2:
                d.update(o[2])
        elif pid in fix:
            d = dict(fix[pid])
            d.setdefault('note', DEFAULT_NOTE)
        else:
            bad.append(pid + '（扱いが無い）')
            continue
        v = d.get('v')
        if v not in ('採る', '一部', '採らない', '今のまま', '映像方針へ', '済み', '親へ'):
            bad.append('%s（v の字が違う：%s）' % (pid, v))
        o_, n_ = d.get('old', x.get('old')) or '', d.get('new', x.get('new')) or ''
        # new が空でよいのは「行ごと消す」形（old が改行で始まるか終わる）だけ
        if v == '採る' and not d.get('patches') and (not o_.strip() or (not n_.strip() and not (o_.startswith('\n') or o_.endswith('\n')))):
            bad.append(pid + '（採るなのに old が空か、行ごと消す形でないのに new が空）')
        if v == '一部' and not (d.get('patches') or (d.get('old') and 'new' in d)):
            bad.append(pid + '（一部なのに old/new が無い）')
        out[pid] = d
    unknown = sorted(set(OVR) - set(fs)) + sorted(set(fix) - set(fs))
    if bad or unknown:
        print('🔴 扱いが決まっていない・形が違う:', bad, '／所見が無いのに扱いがある:', unknown)
        sys.exit(1)
    json.dump(out, open(os.path.join(HERE, 'decisions23.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    adds = extra + G0
    ids = [g['id'] for g in adds]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        print('🔴 足しの id が重なっている:', dup)
        sys.exit(1)
    patches = [{'id': g['id'], 'cut': g['cut'], 'old': g['old'], 'new': g['new'], 'why': g.get('what', ''),
                **({'order': g['order']} if 'order' in g else {})} for g in adds if g.get('old')]
    json.dump(patches, open(os.path.join(HERE, 'patches_g0.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    json.dump([dict(g, v=g.get('v', '採る'), note=g.get('note', 'G0 の直し'), sev=g.get('sev', '🟢'), face=g.get('face', 'A')) for g in adds],
              open(os.path.join(HERE, 'g0_ledger.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    # 聞き役の役割表（第1版の ROLE ＋ 採った所見・足しの role）
    role = dict(roles23.ROLE)
    changes = []
    for pid, d in out.items():
        r = d.get('role') or (fs[pid].get('role') if d['v'] == '採る' else None)
        if d['v'] in ('採る', '一部') and r:
            changes.append((fs[pid]['cut'] if not d.get('cut') else d['cut'], r, pid))
    for g in adds:
        if g.get('role'):
            changes.append((g['cut'], g['role'], g['id']))
    for cut, r, pid in changes:
        if r in ('質問', 'なし'):
            role.pop(cut, None)
        elif r in ('まとめ', '反応'):
            role[cut] = r
        else:
            print('🔴 role の字が違う:', pid, r)
            sys.exit(1)
    json.dump(role, open(os.path.join(HERE, 'roles_map.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    cnt = {}
    for d in out.values():
        cnt[d['v']] = cnt.get(d['v'], 0) + 1
    print('decisions23.json %d件 %s／足し %d件（直す係 %d・G0 %d）／役割の変更 %d' % (len(out), cnt, len(adds), len(extra), len(G0), len(changes)))


if __name__ == '__main__':
    main()
