# -*- coding: utf-8 -*-
"""27本目 台本の机上の数え（26本目の m26.py を写し、27本目＝事件の回・B 枠・16分の目安と、事件の回の網に替えた）。

  python ref/ep27/v1_build/m27.py ref/ep27/daihon_v1.md --roles ref/ep27/v1_build/roles.tsv
  python ref/ep27/v1_build/m27.py --selftest

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28・aq_build と同じ）・
3通りの尺（①カット×8.97秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3 の目安と並べる）・
1行41字超・1カット1〜3行・冒頭の秒（÷365 を1カットずつ）・章の頭から最初の聞き役までの秒・聞き役（tools/check_listener.judge をそのまま呼ぶ）・
写真（画の欄の頭が「実写」＝引用・衛星・Commons の内わけ）・フリー素材（「イメージ」）・文字だけの画面（Vault の count_text_screens）・
図の型（「図 〈型〉」＝全編で2回まで・続けない）・同じ写真の点の2回使い（BY-SA は1点1カット＝E）・
🆕 事件の回の網（ルール §B2-10・§B2-9）：
  ・容疑者の呼び名＝「八田與一」の後ろに「容疑者」が無ければ E（引用の「」の中は W＝県警の字と SNS の原文）／「八田容疑者」の略は W
  ・言わない語（死亡・犯人・真相・逃亡犯・確定 ほか＝当たったら人が文脈を見る W）
  ・帰属（速さ・殺人に近い形態・すぐそば・手がかり・人違い ほか＝同じカットに出どころの語が要る W）
  ・引用の印（「実写 引用」は 額装・無加工 が無ければ E／YouTube は秒が無ければ W）
  ・SNS の印（「図 SNS」は 注釈・出典の行・アカウント名なし が無ければ E／語りに「声」が無ければ W）
  ・地＝写真（「図」の説明カットは「地＝写真 CMnnn」が無ければ W／地が BY-SA なら E＝暗くするのは手直し）
  ・Commons の番号と題名の一致（`src/commons/commons_meta.tsv` の nnn+1 行目＝0から数える）
  ・名前（git の外の src/names_private.txt に書いた語が台本に1つでもあれば E）・敬称の網（さん・くん・ちゃん・氏 を W）
⚠️ check_script の尺の式は ElevenLabs／Otani の定数のまま＝ゆっくりの回は信じない（ルール §5a-28b）。尺はこの道具の②で見る。
"""
import collections
import importlib.util
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\konar\Desktop\zukai-engine\tools')
import check_script as CS          # noqa: E402  parse・clean を使う（道具は直さない）
import check_listener as CL        # noqa: E402  judge をそのまま呼ぶ
import speaker                     # noqa: E402

PUNCT = set('、。？！「」（）・')
CPM = 365.0
SEC_PER_CUT = 8.97                 # kousei.md §0（16.0分÷107カット）
ED01 = 46                          # 共通エンディング ed01 の句読点なし字数（26本目の④で数えた値）
TARGET = 5840                      # kousei.md §0（ed01 こみ・16分00秒）
LO, HI = 5690, 5990                # ±150字（約±25秒）＝目安の幅（B の枠 8〜20分の中）
HOOK_SEC = 46.0                    # 冒頭の引きはこの秒より前（ルール §4-7）
HEAD_Q_SEC = 20.0                  # 章の頭（扉の直後）から最初の聞き役まで
# kousei.md §3（c7 は 365 から ed01 の46を引いた本文の目安）
CH_TARGET = {'c1': 365, 'c2': 1095, 'c3': 1095, 'c4': 913, 'c5': 1095, 'c6': 913, 'c7': 319}
CH_CUTS = {'c1': 7, 'c2': 20, 'c3': 20, 'c4': 17, 'c5': 20, 'c6': 17, 'c7': 6}
CH_Q = {'c1': 2, 'c2': 5, 'c3': 5, 'c4': 4, 'c5': 5, 'c6': 4, 'c7': 1}
# materials.md §5（県警12〜14・衛星 約8・Commons 10〜12＝30〜34）の章への割り振り（目安＝W も出さない）
CH_PHOTO = {'c1': 6, 'c2': 9, 'c3': 8, 'c4': 4, 'c5': 2, 'c6': 4, 'c7': 1}
CH_FREE = {'c1': 0, 'c2': 1, 'c3': 0, 'c4': 0, 'c5': 3, 'c6': 0, 'c7': 0}
# 型の決まった図（10-15＝同じ型は全編で2回まで・続けない）。「模式」はどれも別の絵＝数だけ出す。SNS は別に数える
TEMPLATE = {'帯', '年表', '暦', '時計', '地図', '棒', '線', '箱', '札', '流れ', '比べ', '並べ', '割合', '窓口'}
# 言わない語（ルール §B2-4 死の語・§B2-10 推定無罪・§B4-9「真相」・§4-13 波ダッシュ）。当たったら人が文脈を見る（W）
NG = ['死亡', '即死', '絶命', '悲劇', '地獄', '戦慄', '驚愕', '恐怖', '惨劇', '瞬間', 'ﾀﾋ', '衝撃', '遺体', '死体',
      '犯人', '真相', '逃亡犯', '逃走犯', '確定', '判明', '最悪', '史上', '凶悪', '殺人犯', 'ひき逃げ犯', '〜', '～']
NG_RE = [(r'逮捕され(た|て)', '「逮捕された」は起きていない（デマの話の中か人が見る）'),
         (r'死んだ|死ん', '死の語（SNS の原文の中か人が見る）'),
         (r'(?<!容疑者の)(?<!容疑者が)(?<!容疑者と)車でひいた|わざと(ぶつけ|ひい)', '故意の言い切り（帰属か人が見る）'),
         (r'関東に(いる|潜伏)(?!ってこと)', '関東潜伏の言い切り（説か人が見る）')]
# 帰属（同じカットの中に出どころの語が要る数と見方）
ATTR = [(r'70キロ|100キロ近く', r'捜査関係者|報じ|報道|見方', '速さ（報道・捜査関係者の話）'),
        (r'殺人に近い形態', r'報道|警察庁', '殺人に近い形態（警察庁・報道）'),
        (r'すぐそばにいる可能性', r'警察|幹部|呼びかけ', 'すぐそばにいる可能性（県警）'),
        (r'手がかりは見つかっていない', r'捜査関係者', '有力な手がかりなし（捜査関係者）'),
        (r'海へ逃げた可能性|海に入って逃げた可能性', r'警察|報道|視野', '海へ逃げた可能性（県警・報道）'),
        (r'別の人だった|別人', r'報じ|報道', '人違い（報道）'),
        (r'名誉毀損', r'元検事|指摘', '名誉毀損（元検事）'),
        (r'声をかけない|どんどん110番', r'元刑事', '元刑事の助言'),
        (r'言いがかり|15秒か30秒', r'友人|話して', 'やり取り（けがをした友人の話）'),
        (r'なぜ、?今', r'遺族|報じ', '「なぜ、今なんですか。」（遺族・報道）'),
        (r'凶器を車に', r'父親|告訴|訴え', '「凶器を車に変えただけ」（亡くなった大学生の父親）'),
        (r'約447万円', r'福岡高|裁判', '民事の二審（福岡高裁）'),
        (r'裸足', r'警察|逃げた|走って|とみられ', '裸足（防犯カメラ・報道）'),
        (r'DNA', r'警察|報道|とされ', 'DNA の型（報道＝とされる）'),
        (r'カラーバス|目に入りやすく', r'元刑事', '似た人が目に入る（元刑事）'),
        (r'怒られるわけじゃない', r'元刑事|言う', '元刑事の言葉'),
        (r'風化していた', r'遺族', '遺族の言葉（2023年）'),
        (r'目撃', r'確かめ|報じ|情報|SNS|説', '目撃（本人と確かめられていない）')]
NAME_RE = re.compile(r'八田與一(?!容疑者)')
SHORT_RE = re.compile(r'八田容疑者')
HONOR_RE = re.compile(r'[一-龥ァ-ヶ]{1,4}(さん|くん|ちゃん|氏)')
QUOTE_SPAN = re.compile(r'「[^」]*」')
CM_RE = re.compile(r'CM(\d{3})')
CM_TITLE_RE = re.compile(r'CM(\d{3})「([^」]+)」')
NAMES_FILE = r'C:\Users\konar\Desktop\zukai-engine\ref\ep27\src\names_private.txt'   # git の外（1行1語・# は注）
META_FILE = r'C:\Users\konar\Desktop\zukai-engine\ref\ep27\src\commons\commons_meta.tsv'  # git の外（作者名を含む）
_spec = importlib.util.spec_from_file_location(
    'cts', r'C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証ch-案C見本\count_text_screens.py')
CTS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CTS)


def nopunct(s):
    return sum(1 for ch in s if ch not in PUNCT)


def fmt(s):
    return '%d分%02d秒' % (int(s) // 60, int(s) % 60)


def fig_type(pic):
    m = re.match(r'図\s+([^\s（(]+)', pic)
    return m.group(1) if m else None


def load_meta():
    """CMnnn → (題名, ライセンス)。nnn＝0から数えた行の番号（nnn+1 行目）。"""
    if not os.path.exists(META_FILE):
        return None
    out = {}
    for i, ln in enumerate(open(META_FILE, encoding='utf-8')):
        f = ln.rstrip('\n').split('\t')
        if len(f) >= 7:
            out[i] = (f[1].replace('File:', ''), f[6])
    return out


def load_roles(p):
    out = {}
    if not p or not os.path.exists(p):
        return None
    for ln in open(p, encoding='utf-8'):
        if ln.startswith('#') or not ln.strip():
            continue
        cid, role, text = ln.rstrip('\n').split('\t')
        out[(cid, text)] = role
    return out


def load_names():
    if not os.path.exists(NAMES_FILE):
        return None
    return [ln.strip() for ln in open(NAMES_FILE, encoding='utf-8') if ln.strip() and not ln.startswith('#')]


def ground_cm(pic):
    m = re.search(r'地＝写真\s*CM(\d{3})', pic)
    return int(m.group(1)) if m else None


def main(path, roles_path=None):
    text = open(path, encoding='utf-8').read()
    cuts = CS.parse(text)
    n = len(cuts)
    lines = [(cid, l) for cid, _, ls in cuts for l in ls]
    E, W = [], []
    per_ch = collections.OrderedDict()
    tot = 0
    rows = []          # check_listener.judge の形 (cid, i, 話者, 文, 秒)
    t = 0.0
    hook = []
    starts = {}
    first_q = {}
    figs = collections.Counter()
    fig_seq = []
    keys = collections.defaultdict(list)
    names = load_names()
    meta = load_meta()
    kinds = collections.Counter()
    sns_cuts = []
    for idx, (cid, pic, ls) in enumerate(cuts):
        ch = cid[:2]
        starts.setdefault(ch, t)
        d = per_ch.setdefault(ch, dict(cuts=0, lines=0, chars=0, photo=0, free=0, fig=0, sns=0, q=0))
        d['cuts'] += 1
        d['lines'] += len(ls)
        is_photo = pic.startswith('実写')
        d['photo'] += is_photo
        d['free'] += pic.startswith('イメージ')
        ft = fig_type(pic)
        if pic.startswith('図'):
            if ft == 'SNS':
                d['sns'] += 1
                sns_cuts.append(cid)
            else:
                d['fig'] += 1
                figs[ft] += 1
            if ft != '地図' and '地＝' not in pic:
                W.append('W %s 説明カットの地（地＝写真）が書いていない' % cid)
            g = ground_cm(pic)
            if g is not None and meta is not None:
                if g not in meta:
                    E.append('E %s 地の CM%03d が目録に無い' % (cid, g))
                elif 'SA' in meta[g][1]:
                    E.append('E %s 地の CM%03d は %s＝暗くする手直しができない' % (cid, g, meta[g][1]))
        fig_seq.append((cid, 'SNS' if ft == 'SNS' else ft))
        if is_photo:
            for k in ('引用', '衛星', 'Commons'):
                if pic.startswith('実写 ' + k):
                    kinds[k] += 1
            if pic.startswith('実写 引用'):
                if '額装' not in pic or '無加工' not in pic:
                    E.append('E %s 引用の印（額装・無加工）が無い' % cid)
                if 'YT' in pic and '秒' not in pic:
                    W.append('W %s 県警の動画の「どの秒」が無い' % cid)
                keyq = re.match(r'実写 引用 (\S+ \S+)', pic)
                if keyq:
                    keys[('引用', keyq.group(1))].append(cid)
            if pic.startswith('実写 Commons'):
                m = CM_RE.search(pic)
                if m:
                    num = int(m.group(1))
                    lic = meta[num][1] if meta and num in meta else '?'
                    keys[('BY-SA' if 'SA' in lic else 'A', 'CM%03d' % num)].append(cid)
                    if 'SA' in lic and '額装' not in pic:
                        E.append('E %s CM%03d は %s＝額装が要る' % (cid, num, lic))
            if pic.startswith('実写 衛星'):
                m = re.match(r'実写 衛星 (G\d)', pic)
                if m:
                    keys[('衛星', m.group(1))].append(cid)
        for m in CM_TITLE_RE.finditer(pic):
            num, title = int(m.group(1)), m.group(2)
            if meta is None:
                break
            if num not in meta:
                E.append('E %s CM%03d が目録に無い' % (cid, num))
            elif not meta[num][0].startswith(title):
                E.append('E %s CM%03d の題名が違う（目録＝%s）' % (cid, num, meta[num][0][:50]))
        if ft == 'SNS':
            for need in ('注釈', '出典の行', 'アカウント名とアイコンなし'):
                if need not in pic and not (need == 'アカウント名とアイコンなし' and sns_cuts[:-1]):
                    E.append('E %s SNS の画面に「%s」が無い' % (cid, need))
        if not 1 <= len(ls) <= 3:
            E.append('E %s 行数 %d' % (cid, len(ls)))
        cut_text = ''
        for i, raw in enumerate(ls, 1):
            c = CS.clean(raw)
            cut_text += c
            if len(c) > 41:
                E.append('E %s 1行%d字: %s' % (cid, len(c), c))
            np_ = nopunct(c)
            who = speaker.split(raw)[0]
            if who == speaker.WHO_Q:
                first_q.setdefault(ch, t)
            rows.append((cid, i, who, speaker.bare(CS.STAR_RE.sub('', raw).replace('**', '').strip()), t))
            t += np_ / CPM * 60
            d['chars'] += np_
            tot += np_
            if who == speaker.WHO_Q:
                d['q'] += 1
                if CL.NUM_RE.search(c):
                    E.append('E %s 聞き役の行に数字（漢数字も）: %s' % (cid, c))
            if CS.STAR_RE.match(raw):
                E.append('E %s 決め所の行（27本目は決め所0）: %s' % (cid, c))
            outside = QUOTE_SPAN.sub('', c)
            for m in NAME_RE.finditer(c):
                inq = any(a.start() <= m.start() < a.end() for a in QUOTE_SPAN.finditer(c))
                (W if inq else E).append('%s %s 「八田與一」に「容疑者」が無い%s: %s'
                                         % ('W' if inq else 'E', cid, '（引用の中）' if inq else '', c))
            if SHORT_RE.search(outside):
                W.append('W %s 「八田容疑者」の略（地の文は「八田與一容疑者」）: %s' % (cid, c))
            for w in NG:
                if w in c:
                    W.append('W %s 言わない語「%s」%s: %s' % (cid, w, '（引用の中）' if w not in outside else '', c))
            for rx, why in NG_RE:
                if re.search(rx, c):
                    W.append('W %s 言わない形（%s）: %s' % (cid, why, c))
            if HONOR_RE.search(c):
                W.append('W %s 敬称の網（名前が入っていないか）: %s' % (cid, c))
            if names:
                for nm in names:
                    if nm in c or nm in pic:
                        E.append('E %s 名前の網に当たった（git の外の表の %d字の語）' % (cid, len(nm)))
        for rx, need, why in ATTR:
            if re.search(rx, cut_text) and not re.search(need, cut_text):
                W.append('W %s 帰属の語が無い（%s）' % (cid, why))
        if ft == 'SNS':
            nxt = CS.clean(' '.join(cuts[idx + 1][2])) if idx + 1 < n else ''
            if not re.search(r'という声|SNS上では', cut_text + nxt):
                W.append('W %s SNS の画面の語りに「〜という声」が無い（世間の声として）' % cid)
        if ch == 'c1':
            hook.append('%s=%.1fs' % (cid, t))
    total_sec = t + ED01 / CPM * 60
    allch = tot + ED01
    d1 = n * SEC_PER_CUT
    d2 = allch / CPM * 60
    d3 = (sum(v['chars'] for v in per_ch.values()) + ED01) / CPM * 60
    nphoto = sum(v['photo'] for v in per_ch.values())
    nfree = sum(v['free'] for v in per_ch.values())
    print('カット %d / 行 %d / 句読点なし %d字＋ed01 %d＝%d字（目標 %d・幅 %d〜%d＝%s）'
          % (n, len(lines), tot, ED01, allch, TARGET, LO, HI, '内' if LO <= allch <= HI else '🔴外'))
    print('写真（実写）%d（%.1f%%）＝引用 %d・衛星 %d・Commons %d ／ フリー素材（イメージ）%d ／ 図 %d ／ SNS の画面 %d'
          % (nphoto, nphoto / max(1, n) * 100, kinds['引用'], kinds['衛星'], kinds['Commons'], nfree,
             sum(v['fig'] for v in per_ch.values()), sum(v['sns'] for v in per_ch.values())))
    allc = [CS.clean(l) for _, l in lines]
    if allc:
        print('1行 中央値 %d字・最長 %d字・1カット %.2f行' % (sorted(len(x) for x in allc)[len(allc) // 2],
                                                   max(len(x) for x in allc), len(lines) / max(1, n)))
    print('尺 ① カット×%.2f秒 %s ／ ② 句読点なし÷365 %s ／ ③ 章ごとの合計 %s → 開き %s'
          % (SEC_PER_CUT, fmt(d1), fmt(d2), fmt(d3), fmt(max(d1, d2, d3) - min(d1, d2, d3))))
    if max(d1, d2, d3) - min(d1, d2, d3) > 60:
        E.append('E 尺の3通りの開きが1分を超えた（どれかが壊れている）')
    print('冒頭（÷365 を1カットずつ足した秒・カットの終わり）: ' + ' '.join(hook))
    print('章ごと: 章 始まり カット（目安） 行 句読点なし（目安・差） 分 写真（目安）割合 イメージ（目安） 図 SNS 聞き役（目安） 頭から最初の聞き役')
    for ch, v in per_ch.items():
        tg = CH_TARGET.get(ch, 0)
        fq = first_q.get(ch)
        fqs = (fq - starts[ch]) if fq is not None else None
        if ch != 'c1' and (fqs is None or fqs > HEAD_Q_SEC):
            W.append('W %s 章の頭から最初の聞き役まで %s' % (ch, '無し' if fqs is None else '%.1f秒' % fqs))
        pp = v['photo']
        if pp / max(1, v['cuts']) < 0.20:
            W.append('W %s 写真が %d/%d（20%%未満）' % (ch, pp, v['cuts']))
        print('  %s %s %3d（%3d） %3d %5d（%5d・%+4d） %5.2f %2d（%2d）%3.0f%% %2d（%d） %2d %d %2d（%d） %s'
              % (ch, fmt(starts[ch]), v['cuts'], CH_CUTS.get(ch, 0), v['lines'], v['chars'], tg,
                 v['chars'] - tg, v['chars'] / CPM, pp, CH_PHOTO.get(ch, 0), pp / max(1, v['cuts']) * 100,
                 v['free'], CH_FREE.get(ch, 0), v['fig'], v['sns'], v['q'], CH_Q.get(ch, 0),
                 '-' if fqs is None else '%.1f秒' % fqs))
    print('  ed01 %s' % fmt(t))
    print('図の型: ' + '・'.join('%s %d' % (k, v) for k, v in figs.most_common()))
    for k, v in figs.items():
        if k in TEMPLATE and v > 2:
            E.append('E 図の型「%s」が %d 回（全編で2回まで）' % (k, v))
    for (c0, f0), (c1, f1) in zip(fig_seq, fig_seq[1:]):
        if f0 and f0 == f1 and f0 in TEMPLATE:
            E.append('E 図の型「%s」が続く: %s → %s' % (f0, c0, c1))
        elif f0 and f0 == f1:
            W.append('W 図の型「%s」が続く（別の絵か人が見る）: %s → %s' % (f0, c0, c1))
    for (kind, key), cids in sorted(keys.items()):
        if len(cids) > 1:
            (E if kind == 'BY-SA' else W).append('%s 写真の点 %s %s を %d回: %s'
                                                 % ('E' if kind == 'BY-SA' else 'W', kind, key, len(cids), ' '.join(cids)))
    print('名前の網: ' + ('🔴 表が無い（src/names_private.txt）' if names is None else '%d語を当てた' % len(names)))
    print('Commons の目録: ' + ('🔴 無い' if meta is None else '%d行' % len(meta)))
    roles = load_roles(roles_path)
    if roles is None:
        print('🔴 roles.tsv が無い（--roles を付ける）＝聞き役は数えない')
        e2, w2 = ['roles.tsv が無い'], []
    else:
        e2, w2, info = CL.judge(rows, total_sec, roles)
        print('聞き役: %s' % {k: (round(v, 3) if isinstance(v, float) else v) for k, v in info.items()})
    for x in e2:
        print('  🔴 ' + x)
    for x in w2:
        print('  ⚠️ ' + x)
    tc = CTS.parse(path)
    CTS.report(tc, {}, None, '画の欄のまま')
    for x in W:
        print('⚠️ ' + x)
    for x in E:
        print('🔴 ' + x)
    print('E %d件（形）・聞き役 E %d件・W %d件・言わない語 %d件'
          % (len(E), len(e2), len(w2) + len(W), sum(1 for x in W if '言わない' in x)))
    return len(E) + len(e2)


def selftest():
    ok = nopunct('「あ、い。」（う）・え？お！') == 5
    ok &= nopunct('SNS上では') == 6
    ok &= CS.clean('Q: そうなの？') == 'そうなの？'
    ok &= abs(sum(CH_TARGET.values()) + ED01 - TARGET) <= 10 and sum(CH_CUTS.values()) == 107
    ok &= 24 <= sum(CH_Q.values()) <= 32 and abs(SEC_PER_CUT * 107 - 16.0 * 60) < 2.0
    ok &= fig_type('図 帯（交差点）') == '帯' and fig_type('図 SNS（カード1）') == 'SNS'
    ok &= fig_type('実写 Commons CM044') is None
    ok &= bool(NAME_RE.search('八田與一は')) and not NAME_RE.search('八田與一容疑者は')
    ok &= bool(SHORT_RE.search('八田容疑者が')) and not SHORT_RE.search('八田與一容疑者が')
    ok &= ground_cm('図 札（…・地＝写真 CM044 を暗く）') == 44 and ground_cm('図 地図（地＝略図）') is None
    ok &= bool(HONOR_RE.search('田中さんは')) and not HONOR_RE.search('みなさんへ')
    ok &= bool(CL.NUM_RE.search('八田の')) and not CL.NUM_RE.search('どこにいるの？')
    m = load_meta()
    if m is not None:
        ok &= m[72][0].startswith('Beppu marina 2024') and 'SA' in m[72][1]
        ok &= m[44][0].startswith('Beppu 20220910214737') and m[44][1] == 'CC BY 2.0'
        ok &= m[0][0].startswith('A train station in Kyushu')
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
