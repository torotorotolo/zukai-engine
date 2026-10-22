# -*- coding: utf-8 -*-
"""24本目④'：係の所見の扱い（直す係の fix_G*.json＝G0 の fix_G0.json を含む ＋ G0 の上書き OVR）→ decisions24.json・patches_g0.json・g0_ledger.json・roles_map.json を書き出す（23本目 decide23.py を写した）。

  python ref/ep24/v2_build/decide24.py

扱いの決め方（上ほど強い）：
  1. OVR（G0＝このチャットの親が原文に引き直して決め直した所＝直す係の扱いを上書き）
  2. fix_G*.json（G0 の fix_G0.json と、直す係が decisions.md に沿って決めた扱い）
  3. どちらにも無い所見＝止める（fail closed＝扱いの決まっていない所見を黙って採らない）
fix の "_extra"（所見に無い直し＝字数の調整・橋）と G0 の足し（下の G0）は patches_g0.json と g0_ledger.json に入る。
聞き役の役割＝第1版の ROLE（v1_build/roles24.py）に、採った所見の "role" を重ねて roles_map.json に書く（手で直さない）。
⚠️ 「採る」で new が空・old が空の所見は止める（old を消してしまうため）。
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'v1_build'))
import roles24                     # noqa: E402  第1版の役割（ROLE）

DEFAULT_NOTE = '係の案どおり（G0 が見た）'

# G0 の上書き：'id': ('扱い', '理由', {old/new/cut/patches/role})
OVR = {
    # 当て直しの係（review_R1・R2＝4'-18）の所見は、G0 が原文の向きを見て決めた（2026-10-22）
    'R1-001': ('採る', '付属書I p.74／64「primarily as a result of the low reactor power level」＝主因は低い出力・流れは足し（In addition）＝重みを戻す'),
    'R1-002': ('採る', '表I-I は付属書I（1991年の委員会）の表＝c305「1991年の委員会の報告の表」と呼び分けをそろえる（c505 の主語とも続く）。decisions §4 の「1992年の報告の表」は G0 の書き損じ＝こちらが正'),
    'R1-003': ('採る', 'S1 p.21／11「during the critical part of the test」＝限定を戻す（4\'-18）'),
    'R1-004': ('採る', 'S2 p.132／~125「all absorber rods (except for the shortened rods)」・S1 p.14／4＝止めるときに入るのは上からの棒＝211本ぜんぶが止める棒ではない'),
    'R1-005': ('採る', 'S1 p.20／10＝強く書いたのは700MW 未満の禁止＝何を強く書いたかを戻す'),
    'R1-006': ('採る', '1カットに「ここで」「ここでは」＝c202 と同じ「この動画では」'),
    'R1-007': ('採る', 'S2 p.28／~25 の power reduction＝c315〜c317 の繰り返しを減らす（−4字）'),
    'R1-008': ('採る', 'c211 と同じ「最大の出力」（decisions §3 の2）＝画の欄の札だけ'),
    'R1-009': ('採る', '国会の答弁（K1 1986-05-07 の念のため）＝日本全体へ広げない・「〜んだ。」のまとめの形を外す'),
    'R2-001': ('採る', 'L3 p.24／64 第98段落＝低い線量の人たちに限る＝図の札も cb14 の語りにそろえる'),
    'R2-002': ('採る', 'R2-001 と組＝§1-5（図の札もこの値）'),
    'R2-003': ('採る', 'S1 p.21／11「suggest」＝ca17 の「ようだ」と同じ強さに（結びで断定に戻さない）'),
    'R2-004': ('採る', 'S1 p.34／24「unapproved changes in the test procedure」＝試験の計画（c220 とそろえる）'),
    'R2-005': ('採る', 'S1 p.34／24「deliberately」＝結びの天秤で人の側の決め手を落とさない（寄せない）'),
    'R2-006': ('採る', '付属書I p.81／71「this violation was not the cause」＝原因でないのはこの違反だけ'),
    'R2-007': ('採る', 'S1 p.14／4「depended on … the operating regime」＝c906 の限定（ことがある）を聞き役でも残す'),
    'R2-008': ('採る', '付属書I p.96／86「The personnel」＝同じ付属書を ca04・ca06〜ca08 は「職員」＝呼び分けをそろえる（decisions §2 の字は G0 の書き方の揺れ）'),
    'R2-009': ('採る', '聞き役が直前の語りの字をそのまま繰り返さない（まとめは言い直し）'),
    'R2-010': ('採る', 'L1 p.13／15「based on the experience of other populations」＝問いに次の語りがそのまま答える'),
    'R2-011': ('採る', 'S2 p.18／~13「in combination with specific reactor features」＝「原因を運転員とした」は ca21 で直した言い過ぎ＝運転員の側に置いた'),
    'R2-012': ('採る', 'S2 p.115／~108 の片を出典の欄に（画の欄の29の根拠）'),
    'R2-013': ('採る', '§6＝UNSCEAR は語りから外れた'),
    'R2-014': ('採る', '§6＝cb15 に被爆者が入った（G7-050）'),
    'R2-015': ('採る', '§9＝ca05 の1988年は語りから消えた（G5-026）'),
    'R2-016': ('採る', '§5＝ca12 の言い方（前触れと見る人もいる）にそろえる'),
    'R2-017': ('採る', '§8＝c906 から外した「入り始めた数秒」を概要欄からも外す（S1 p.14／4）'),
    'R2-018': ('採る', '§1-5＝ca07 が同じ節を時刻と値なしで言うことを書く'),
    'R2-019': ('採る', '§5＝R2-018 と組'),
    'R2-020': ('済み', 'G0-009 の new を「3.5倍から、およそ80倍」に直した（付属書II p.131／121＝approximately は80倍だけ・c922 の語りはもう同じ形）'),
    'R2-021': ('済み', 'fix_G0 の G6-005 の2行目を「管理を書面で職員に戻した、と3月31日にウクライナが伝えた。」に直した（WNN＝31日は伝えた日）'),
    'R2-022': ('親へ', '承認①で一言：題 B\' は「爆発した4号炉、」の直後に棒の欠陥＝欠陥が爆発の原因と確定したと読まれうる（INSAG-7＝It is not known for certain what started the power excursion）・題とサムネのどちらも運転員の誤り（most ill judged）を見せない'),
    'G6-017':('採る', 'G0：字に余りがある（直す係6本を重ねて上限まで約60字）＝受け手は事業者の頁 2019-07-11「to the Client, i.e. the SSE "Chornobyl NPP"」で G0 が確かめた'),
}

# G0 の足し（所見に無い直し）：{'id': 'G0-0NN', 'cut': …, 'old': …, 'new': …, 'what': …, 'sev': …, 'face': …, 'order': …}
# order 99＝同じカットの直す係の直し（order 50）のあとに当てる
G0 = [
    {'id': 'G0-001', 'cut': 'c504', 'order': 99, 'sev': '🟡', 'face': 'B',
     'what': 'c504→c505 が矛盾して聞こえる（F2 の申し送り）：0時36分に変えたのは蒸気の圧力の保護の設定（付属書I p.85／75「At 00:36:24 the personnel changed the set point … 55 … to 50」＝手順の内・表I-I p.64／54）。違反とされたのは水位の設定を切り替えなかった別の件（c505）。INSAG-7 本文 (6) は2つを1つの文で書く＝帰属を「報告の表」にして圧力と言う（本文の suggests のらしいは、表が時刻を言い切るので外す）',
     'old': '> 1992年の報告によれば、設定が変えられたのは、もっと早い0時36分らしい。\n> そして保護には2つの段があり、下の段は、最後まで効いていた。',
     'new': '> 1992年の報告の表では、もっと早い0時36分に、圧力の保護の設定が変わる。\n> そして水位の保護には2つの段があり、下の段は、最後まで効いていた。'},
    {'id': 'G0-002', 'cut': 'c504', 'order': 99, 'sev': '🟢', 'face': 'F', 'what': 'c504 の画の欄と出典の欄を G0-001 に合わせる（表I-I の 00:36:24 の行）',
     'old': '図 模式（ドラムの水位の保護の2つの段＝上の段の設定を変えた・下の段は最後まで効いていた）',
     'new': '図 模式（ドラムの保護＝0時36分に圧力の保護の設定を変えた〈手順の内〉・水位の保護の2つの段＝下の段は最後まで効いていた）'},
    {'id': 'G0-003', 'cut': 'c504', 'order': 99, 'sev': '🟢', 'face': 'B', 'what': 'c504 の出典の欄に表I-I の片',
     'old': '・S1 p.22／12（`protection at the lower steam drum level remained effective throughout the event`）',
     'new': '・S1 p.22／12（`protection at the lower steam drum level remained effective throughout the event`）・S1-表I-I p.64／54（`The EPS trip point in response to a pressure drop in the steam separator drums was changed`）'},
    {'id': 'G0-004', 'cut': 'cc13', 'order': 99, 'sev': '🟢', 'face': 'C',
     'what': 'cc12（2025年の無人機）から cc13（棒の改良）へ橋が無い（F6 の親へ・G6-014 の parent）＝話を戻す一言',
     'old': '> 事故のあと、RBMK の止める棒は改められた。',
     'new': '> 話を棒に戻そう。事故のあと、RBMK の止める棒は改められた。'},
    # §1（承認①の表のもと・割れる数の表）を第2版に合わせる
    {'id': 'G0-005', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'C', 'what': "§1-1 に ④' の推奨 B' と理由（G7-001〜003・公開ずみの題と型を照らした＝4'-8）",
     'old': '| C | 「原因は運転員」とした報告書は、6年後に書き直された。チェルノブイリ原発事故の真相【事故検証】【ゆっくり解説】 | 55 | c103〜c104・cc18（角度の言い方そのまま） |',
     'new': '| C | 「原因は運転員」とした報告書は、6年後に書き直された。チェルノブイリ原発事故の真相【事故検証】【ゆっくり解説】 | 55 | c103〜c104・cc18（角度の言い方そのまま） |\n'
            "| **B'（④'の推奨）** | 爆発した4号炉、止めるはずの棒には、2年半ほど前に見つかっていた欠陥があった。チェルノブイリ原発事故の真相【事故検証】【ゆっくり解説】 | 67 | c105・c911〜c913（付属書I p.53／43＝1983年11〜12月→1986年4月＝2年4〜5か月＝「ほど」）・G7-002 |\n"
            "- 🆕 **④'（10-22）：推奨を B' に替えた**（G7-001〜003）＝A は「違反ではなかった」が「運転員は無実」と読まれやすい／B は「2年半前」が「ほど」を落とし、頭に事件の絵の語が無い／C は「」が原文の引用に見え、書き直しが撤回に読める。公開ずみの21〜23本目の題（49〜70字・事実の1句＋〈事件名〉の真相【事故検証】【ゆっくり解説】）と型を照らした＝A（62字）・B'（67字）とも型の内。**承認①で決める**"},
    {'id': 'G0-006', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'C', 'what': "§1-2 に ④' の見立て（G7-004〜006）",
     'old': '- 「犠牲31人」＝ソ連の発表（INSAG-1・フォーラムも31）＝本編 c204・cb04・cb08 で帰属・cb06 で UNSCEAR の30人と言い分けた（①の承認）。長期の推計はサムネに出さない（①）',
     'new': '- 「犠牲31人」＝ソ連の発表（INSAG-1・フォーラムも31）＝本編 c204・cb04・cb08 で帰属・cb06 で UNSCEAR の30人と言い分けた（①の承認）。長期の推計はサムネに出さない（①）\n'
            "- 🆕 ④'（10-22）：推奨は **A のまま**（G7-004＝題 B' と別の入口になる）。B は「犠牲31人」と並ぶと棒の欠陥が亡くなった人の因果に読める（G7-005）・C は責める相手を作る（G7-006）。**承認①で決める**"},
    {'id': 'G0-007', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'C', 'what': "§1-3 に ④' の見立て（G7-007〜009・G7-061）",
     'old': '| C | あなたは、この動画で、いちばん意外だったのはどこでしたか。よければ、コメントで教えてください。 |',
     'new': '| C | あなたは、この動画で、いちばん意外だったのはどこでしたか。よければ、コメントで教えてください。 |\n'
            "- 🆕 ④'（10-22）：推奨は **A のまま**（G7-007）。cc21 は語順だけ直した＝「あなたは、この動画を見る前、チェルノブイリ原発事故の原因を、…」（G7-061）。B は角度とつながらない・C はどの回にも使える。**承認①で決める**"},
    {'id': 'G0-008', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'B', 'what': '§1-5 のドラムの保護を c504・c505 の第2版に（G0-001）',
     'old': '| ドラムの保護 | 0時36分（c504） | INSAG-1 1:19（c503） | S1 p.22／12 |',
     'new': '| ドラムの保護 | 0時36分＝圧力の保護の設定（c504・表I-I 00:36:24＝手順の内）／水位の設定を切り替えなかったのは違反だが事故の原因ではない（c505＝1991年の委員会） | INSAG-1 1:19（c503）・INSAG-7 本文 (6) は2つを1つの文で書く | S1 p.22／12・p.64／54・p.85／75・p.88／78 |'},
    {'id': 'G0-009', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'B', 'what': '§1-5 の出力の倍数を c922 の第2版に（G4-022＝比べるもとが違う）',
     'old': '| 出力の倍数 | 1986年の報告 100倍（4秒以内）・のちの計算 3.5倍から80倍（c922） |',
     'new': '| 出力の倍数 | 1986年の報告 最大の出力（定格・nominal）の100倍（4秒以内）・のちの計算 はじめの出力（initial value）の3.5倍から、およそ80倍（approximately は80倍だけ＝R2-020）＝比べるもとが違う（c922） |'},
    {'id': 'G0-010', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'B', 'what': '§1-5 の 1:22:30 の残した棒を c603 の第2版に（G3-004）',
     'old': '| 1:22:30 の残した棒 | 6本から8本（c603） |',
     'new': '| 1:22:30 の残した棒 | 6本から8本＝即時停止の15本の「およそ半分」（c603。S3 の not more than half は S3 の決まり〈30本〉に対して＝15本の半分以下とは言わない） |'},
    {'id': 'G0-011', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'B', 'what': '§1-5 の長期の推計を cb12 の第2版に（G5-004＝上乗せの数）',
     'old': '| 長期の推計 | フォーラム 最大4,000人・',
     'new': '| 長期の推計 | フォーラム 最大4,000人（60万人で、ほかの原因のがんの約10万人に**加えて**放射線で増える分＝L1 p.14／16）・'},
    {'id': 'G0-012', 'cut': '§', 'order': 95, 'sev': '🟢', 'face': 'B', 'what': '§1-5 の2022年を cc12 の第2版に＋2025年の行（G6-004・G6-005）',
     'old': '| 2022年 | 2月24日から支配・3月31日に管理を書面で引き渡した（cc12） | 「全員が去った」は言わない | IAEA Update 38（WNN の写し） |',
     'new': '| 2022年 | 2月24日から支配・3月31日に「書面で管理を職員に戻した」とウクライナが IAEA に伝えた（cc12＝ウクライナの通知に帰属） | 「全員が去った」は言わない | IAEA Update 38（WNN 2022-04-01 の写し） |\n'
            '| 🆕 2025年 | 2月14日 無人機が新しい覆い（アーチ）に当たった・12月 IAEA「閉じ込めの働きを含む主な安全の働きを失った」（cc12＝「とされる」） | 支える骨組みと監視の系は恒久の損傷なし・仮の屋根の直し＝語りでは言わない（尺） | 国連ニュース 2025-02-14・NucNet 2025-12-08・IAEA GOV/2026/7（2026-02-25） |'},
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
    json.dump(out, open(os.path.join(HERE, 'decisions24.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
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
    role = dict(roles24.ROLE)
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
    print('decisions24.json %d件 %s／足し %d件（直す係 %d・G0 %d）／役割の変更 %d' % (len(out), cnt, len(adds), len(extra), len(G0), len(changes)))


if __name__ == '__main__':
    main()
