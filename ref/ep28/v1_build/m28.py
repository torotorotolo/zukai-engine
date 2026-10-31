# -*- coding: utf-8 -*-
"""28本目 台本の机上の数え（27本目の m27.py を写し、28本目＝会社のシステムが攻撃された事件・B 枠・16分の目安と、会社の事件の網に替えた）。

  python ref/ep28/v1_build/m28.py ref/ep28/daihon_v1.md --roles ref/ep28/v1_build/roles.tsv
  python ref/ep28/v1_build/m28.py --selftest

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28・aq_build と同じ）・
3通りの尺（①カット×8.97秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3 の目安と並べる）・
1行41字超・1カット1〜3行・冒頭の秒（÷365 を1カットずつ）・章の頭から最初の聞き役までの秒・聞き役（tools/check_listener.judge をそのまま呼ぶ）・
写真（画の欄の頭が「実写」＝引用〈会社〉・公的・Commons の内わけ）・フリー素材（「イメージ」）・文字だけの画面（Vault の count_text_screens）・
図の型（「図 〈型〉」＝全編で2回まで・続けない）・同じ写真の点の2回使い（BY-SA は1点1カット＝E）・
🆕 会社の事件の網（ルール §B2-11・§B2-9・記憶 feedback-jiko-recheck-time-bound-claims）：
  ・「犯人」「加害者」＝「」の外なら E（会社と役員を言い切らない・攻撃した者は「第三者」「攻撃した者」）／「」の中は W（SNS の原文と弁護士の言葉＝人が見る）
  ・言わない語（真相・流出・漏洩・特例・14県・要請・ランサムウェア ほか＝当たったら人が文脈を見る W）
  ・帰属（44億円＝計算・10万人＝弁護士・1500人＝TBS・点検＝報道・ローン＝相談と会社の言葉 ほか＝同じカットに出どころの語が要る W）
  ・時点の言い切り（まだ・されていない・分かっていない ほか＝同じカットに「10月31日の時点」などの日付が要る W）
  ・引用の印（「実写 引用」は 額装・無加工・出典 が無ければ E）・公的（額装・出典 が無ければ E）
  ・SNS の印（「図 SNS」は 注釈・出典の行・アカウント名とアイコンなし が無ければ E／語りに「声」が無ければ W）
  ・地＝写真（「図」の説明カットは「地＝写真 CMnnn」が無ければ W／地が BY-SA なら E・PD なら W）
  ・です・ます（最後の問いのカットのほかは W＝記憶 feedback-jiko-narration-plain-form）
  ・Commons の番号と題名の一致（`src/commons/commons_meta28_cats.tsv` の0から数えた行の番号＝0行目は見出し）
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
LAST_CUT = 'c706'                  # 最後の問いのカット（です・ます はここだけ）
# kousei.md §3（c7 は 365 から ed01 の46を引いた本文の目安）
CH_TARGET = {'c1': 365, 'c2': 913, 'c3': 913, 'c4': 1278, 'c5': 913, 'c6': 1095, 'c7': 319}
CH_CUTS = {'c1': 7, 'c2': 17, 'c3': 17, 'c4': 23, 'c5': 17, 'c6': 20, 'c7': 6}
CH_Q = {'c1': 2, 'c2': 4, 'c3': 4, 'c4': 6, 'c5': 4, 'c6': 5, 'c7': 1}
# materials.md §6（数える分 24〜32）の章への割り振り（目安＝W も出さない）
CH_PHOTO = {'c1': 5, 'c2': 7, 'c3': 5, 'c4': 6, 'c5': 5, 'c6': 3, 'c7': 1}
CH_FREE = {'c1': 1, 'c2': 3, 'c3': 3, 'c4': 2, 'c5': 3, 'c6': 1, 'c7': 1}
# 型の決まった図（10-15＝同じ型は全編で2回まで・続けない）。「模式」はどれも別の絵＝数だけ出す。SNS は別に数える
TEMPLATE = {'帯', '年表', '暦', '時計', '地図', '棒', '線', '箱', '札', '流れ', '比べ', '並べ', '割合', '窓口',
            '問答', '条文', '言葉', '式'}
# 言わない語（§B2-11・§B4-9「真相」・sources.md §4・materials.md §1-3「漏えい」で揃える・§4-13 波ダッシュ）。当たったら人が文脈を見る（W）
NG = ['真相', '流出', '漏洩', '特例', '14県', '26都県', '要請', 'ランサムウェア', '犯行グループ', '組織的', '内部の犯行',
      '隠蔽', '闇', '衝撃', '瞬間', '最悪', '史上', '判明', '確定', '清算条項', '146万5349', '攻撃者', '〜', '～']
NG_RE = [(r'逮捕(され|した)', '「逮捕された」は起きていない（「報道は見当たらない」の中か人が見る）'),
         (r'特定(され|した)', '「特定された」は起きていない（人が見る）'),
         (r'(ロシア|中国|北朝鮮|海外)の', '国や集団の名を推測で出さない（§B2-11 ②）')]
STRONG = ('犯人', '加害者')          # 「」の外なら E（会社と役員を言い切らない）
# 帰属（同じカットの中に出どころの語が要る数と見方）
ATTR = [(r'44億円', r'計算|かけると', '見舞金の総額（会社は言っていない＝計算）'),
        (r'10万人', r'弁護士|参加|加わり|訴え', '参加希望10万人超（弁護士側の会見）'),
        (r'1500人', r'TBS', '都内の再交付（TBS の取材）'),
        (r'列ができ', r'テレビ朝日|報じ', '免許センターの列（テレビ朝日）'),
        (r'点検を求め', r'報道|共同|NHK|金融庁|促', '国交省の点検（報道）'),
        (r'被害者かつ加害者|低すぎる|切り捨てられている|最大の争点', r'弁護士', '弁護士の言葉'),
        (r'ローンを組まれた', r'相談', 'ローン（弁護士に寄せられた相談）'),
        (r'不安も不満も', r'毎日|話した', '会員の声（毎日新聞）'),
        (r'年内', r'目指|めど|目処|という|とした|としている', '年内（弁護士側・会社の言葉）'),
        (r'という声', r'SNS|報道|声', 'SNS の声（世間の声として）')]
TIME_RE = re.compile(r'まだ|されていない|分かっていない|決まっていない|出ていない|見当たらない|いまも|今も|検討中')
TIME_OK = re.compile(r'10月31日の時点|10月23日の(発表|時点)|10月27日|10月23日に更新')
DESU_RE = re.compile(r'(です|(?<!だ)ます|でした|ました|ません)か?(?:[。、？！」]|$)')   # 「だます」は除く
HONOR_RE = re.compile(r'[一-龥ァ-ヶ]{1,4}(さん|くん|ちゃん|氏)')
QUOTE_SPAN = re.compile(r'「[^」]*」')
CM_RE = re.compile(r'CM(\d{3})')
CM_TITLE_RE = re.compile(r'CM(\d{3})「([^」]+)」')
QDOC_RE = re.compile(r'実写 引用 (第\d報|開示\d{4}[ab]?)')
PUB_RE = re.compile(r'実写 公的 (\S+)')
NAMES_FILE = r'C:\Users\konar\Desktop\zukai-engine\ref\ep28\src\names_private.txt'   # git の外（1行1語・# は注）
META_FILE = r'C:\Users\konar\Desktop\zukai-engine\ref\ep28\src\commons\commons_meta28_cats.tsv'  # git の外（作者名を含む）
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
    """CMnnn → (題名, ライセンス)。nnn＝0から数えた行の番号（0行目は見出し＝CM001 が1件目）。"""
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


def in_quote(c, pos):
    return any(a.start() <= pos < a.end() for a in QUOTE_SPAN.finditer(c))


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
            if '地＝' not in pic:
                W.append('W %s 説明カットの地（地＝写真）が書いていない' % cid)
            g = ground_cm(pic)
            if g is not None and meta is not None:
                if g not in meta:
                    E.append('E %s 地の CM%03d が目録に無い' % (cid, g))
                elif 'SA' in meta[g][1]:
                    E.append('E %s 地の CM%03d は %s＝暗くする手直しができない' % (cid, g, meta[g][1]))
                elif 'Public domain' in meta[g][1]:
                    W.append('W %s 地の CM%03d は PD（地は CC BY・CC0 が既定）' % (cid, g))
        fig_seq.append((cid, 'SNS' if ft == 'SNS' else ft))
        if is_photo:
            for k in ('引用', '公的', 'Commons'):
                if pic.startswith('実写 ' + k):
                    kinds[k] += 1
            if pic.startswith('実写 引用'):
                for need in ('額装', '無加工', '出典'):
                    if need not in pic:
                        E.append('E %s 引用の印（%s）が無い' % (cid, need))
                m = QDOC_RE.match(pic)
                if m:
                    keys[('引用', m.group(1))].append(cid)
            if pic.startswith('実写 公的'):
                for need in ('額装', '出典'):
                    if need not in pic:
                        E.append('E %s 公的な機関の紙面の印（%s）が無い' % (cid, need))
                m = PUB_RE.match(pic)
                if m:
                    keys[('公的', m.group(1))].append(cid)
            if pic.startswith('実写 Commons'):
                m = CM_RE.search(pic)
                if m:
                    num = int(m.group(1))
                    lic = meta[num][1] if meta and num in meta else '?'
                    keys[('BY-SA' if 'SA' in lic else 'A', 'CM%03d' % num)].append(cid)
                    if 'SA' in lic and '額装' not in pic:
                        E.append('E %s CM%03d は %s＝額装が要る' % (cid, num, lic))
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
                if need not in pic:
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
                E.append('E %s 決め所の行（28本目は決め所0）: %s' % (cid, c))
            outside = QUOTE_SPAN.sub('', c)
            for w in STRONG:
                for m in re.finditer(w, c):
                    inq = in_quote(c, m.start())
                    (W if inq else E).append('%s %s 「%s」%s: %s' % ('W' if inq else 'E', cid, w,
                                                                    '（引用の中＝人が見る）' if inq else '＝「」の外（言い切らない）', c))
            for w in NG:
                if w in c:
                    W.append('W %s 言わない語「%s」%s: %s' % (cid, w, '（引用の中）' if w not in outside else '', c))
            for rx, why in NG_RE:
                if re.search(rx, outside):
                    W.append('W %s 言わない形（%s）: %s' % (cid, why, c))
            if cid != LAST_CUT and DESU_RE.search(outside):
                W.append('W %s です・ます（語りは言い切り）: %s' % (cid, c))
            if HONOR_RE.search(c):
                W.append('W %s 敬称の網（名前が入っていないか）: %s' % (cid, c))
            if names:
                for nm in names:
                    if nm in c or nm in pic:
                        E.append('E %s 名前の網に当たった（git の外の表の %d字の語）' % (cid, len(nm)))
        for rx, need, why in ATTR:
            if re.search(rx, cut_text) and not re.search(need, cut_text):
                W.append('W %s 帰属の語が無い（%s）' % (cid, why))
        outside_cut = QUOTE_SPAN.sub('', cut_text)
        if TIME_RE.search(outside_cut) and not TIME_OK.search(cut_text) and cid != LAST_CUT:
            W.append('W %s 時点の言い切りに日付が無い（「10月31日の時点で」など）: %s'
                     % (cid, TIME_RE.search(outside_cut).group(0)))
        if ft == 'SNS':
            nxt = CS.clean(' '.join(cuts[idx + 1][2])) if idx + 1 < n else ''
            if not re.search(r'という声|SNS上では|声も', cut_text + nxt):
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
    print('写真（実写）%d（%.1f%%）＝引用 %d・公的 %d・Commons %d ／ フリー素材（イメージ）%d ／ 図 %d ／ SNS の画面 %d'
          % (nphoto, nphoto / max(1, n) * 100, kinds['引用'], kinds['公的'], kinds['Commons'], nfree,
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
        if k not in TEMPLATE and k != '模式':
            W.append('W 図の型「%s」は表に無い（綴りで門番をかわしていないか）' % k)
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
    ok &= ground_cm('図 札（…・地＝写真 CM044 を暗く）') == 44 and ground_cm('図 地図（地＝略図）') is None
    ok &= bool(HONOR_RE.search('田中さんは')) and not HONOR_RE.search('みなさんへ')
    ok &= bool(CL.NUM_RE.search('七年の')) and not CL.NUM_RE.search('どこにいるの？')
    ok &= in_quote('弁護士は「被害者かつ加害者」と', 9) and not in_quote('会社は加害者だ', 3)
    ok &= bool(TIME_RE.search('まだ分かっていない')) and bool(TIME_OK.search('10月31日の時点で'))
    ok &= bool(DESU_RE.search('考えたことはありますか。')) and not DESU_RE.search('ますます増えた')
    ok &= QDOC_RE.match('実写 引用 第5報の頁（…）').group(1) == '第5報'
    ok &= QDOC_RE.match('実写 引用 開示1023b（…）').group(1) == '開示1023b'
    m = load_meta()
    if m is not None:
        ok &= m[8][0].startswith('Times Car Key Case') and m[8][1] == 'CC BY 4.0'
        ok &= m[108][0].startswith('運転免許みほん') and m[108][1] == 'CC BY 4.0'
        ok &= m[1][0].startswith('Carshare24') and m[1][1] == 'CC0'
        ok &= 'SA' in m[4][1] and m[0][0] == 'title'
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
