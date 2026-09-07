# -*- coding: utf-8 -*-
"""台本（Vault の `…台本第N版-….md`）の机上検査。

数えるもの: カット数・字幕行・字数・決め所・1行の字数・尺（3通り）・章ごとの割合・
            冒頭の実尺・禁止語・二重表示・決め所の位置。

🔴 使う前に `--selftest` を通すこと（答えの分かっている入力で検算する）。
   → [[feedback-verify-your-own-instrument]] / [[feedback-measure-the-script-in-seconds]]

    python tools/check_script.py <台本.md>
    python tools/check_script.py --selftest

終了コード: 0=E無し / 1=E有り（fail closed） / 2=道具の異常
"""
import io
import re
import sys
from statistics import median

# ── 実測ずみの既定値（[[project-jiko-rules-index]] §5。推定で置き換えない） ──
# 🔴 2026-09-07（5本目②）：**この定数は上流を替えると黙って古くなる。**
#    1〜3本目は VOICEVOX（話速0.95）で 5.52 文字/秒だった。4本目から ElevenLabs に移ったが
#    `voice_settings` を送っていなかったので**声側の既定 speed 1.14** で読まれていた。
#    4本目 240カット・字幕486行を `audio/narration.json` で実測すると **6.12 文字/秒**＝
#    **定数 5.52 は 11% 遅く見積もっていた**。それでも門番は鳴らない（尺が長めに出るだけ）。
#    → [[feedback-gates-go-stale-when-upstream-changes]]
#    そこで **narration.json があればそこから測り直す**（定数は音がまだ無いときの当てに落とす）。
#
# 🔴 カズヤくん指示（2026-09-07）「話速は1.0」＝ ElevenLabs の `speed` を 1.0 にする
#    （いまの実効 1.14 より **14% ゆっくり**）。⑤a で `el_script.SETTINGS` に書く。
#    ⚠️ 下の 5.37 は **6.12 × 1.0/1.14 の推定であって実測ではない。**
#       ElevenLabs の speed が尺に線形に効くかは確かめていない（②では課金APIを叩かない約束）。
#       **⑤a で narration.json ができた時点で、この数字は自動で実測に置き換わる。**
CPS_FALLBACK = 5.37     # 文字/秒（話速1.0 の**推定**。実測は narration.json から）
PER_CUT = 9.40          # 秒/カット（話速1.0 の推定。4本目実測 7.91秒 の発話ぶんを 1.14倍した値）
LEAD, TAIL = 0.35, 0.50
TAIL_EXTRA_QUOTE = 2.0
EP2_CPS = 5.00          # ep2 の設計値
MAX_CHARS_PER_LINE = 41
# 🔴 2026-09-07 カズヤくん指示「尺の下限を30分に変更してください」（**事故検証chだけ**）。
#    旧＝35分（1本目35分／2本目38分の実測から置いた値）。
#    ⚠️ これは 2026-08-03 の「固定の下限は置かない（題材ごとに競合を実測して決める）」を
#       **上書きする**（新しい指示を採る）。上限 38分は動かしていない。
#    ⚠️ 実測では **35〜50分帯が1.47倍**。30〜35分はその帯の外側なので、
#       そこに寄せるなら題材の側に理由が要る（この門番は「外」とは言わなくなるだけ）。
DUR_MIN, DUR_MAX = 30 * 60, 38 * 60


def measured_cps(cids=None, path="audio/narration.json"):
    """🔴 実際に合成した音から 文字/秒 を測る。無ければ／別の回のものなら None（定数に落ちる）。

    ⚠️ `narration.json` の `speed` 欄は**帳簿の値**であって送った値ではない
       （4本目は `speed: 1.0`・`settings: null` と書いてあるのに、声側の既定 1.14 で読まれていた）。
       だから欄を読まず、**字幕の実測の長さ**から測る。
    ⚠️⚠️ **`narration.json` は前の回のものが残る。**
       題材を替えた直後は 4本目（サーフサイド）の音が置いたままなので、
       そのまま測ると**別の回の速さを 5本目の台本に当てる**。
       `cids`（いま検査している台本のカットID）を渡して、**重なりが半分未満なら使わない**。
       → [[feedback-gates-go-stale-when-upstream-changes]]
    """
    import json
    from pathlib import Path
    p = Path(__file__).resolve().parent.parent / path
    if not p.exists():
        return None, "音がまだ無い"
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        sub = d["subtitles"]
        if cids is not None:
            cids = set(cids)
            hit = len(cids & set(sub))
            if not cids or hit / len(cids) < 0.5:
                return None, f"narration.json は別の回のもの（カットの重なり {hit}/{len(cids)}）"
        c = s = 0
        for segs in sub.values():
            for x in segs:
                if len(x["text"]) >= 8 and x["d"] > 0:
                    c += len(x["text"])
                    s += x["d"]
        return (round(c / s, 2), "narration.json の実測") if s > 0 else (None, "字幕が空")
    except Exception as e:                               # noqa: BLE001
        return None, f"narration.json を読めない（{type(e).__name__}）"   # 止めはせず定数に落とす


CPS, CPS_SOURCE = CPS_FALLBACK, "定数（話速1.0 の推定）"


def use_measured_cps(cids):
    """検査する台本が決まった時点で CPS を実測に差し替える（合わなければ定数のまま）。"""
    global CPS, CPS_SOURCE
    v, why = measured_cps(cids)
    CPS, CPS_SOURCE = (v, why) if v else (CPS_FALLBACK, f"定数（話速1.0 の推定・{why}）")
    return CPS


def dur_ok(sec):
    """🔴 尺の合否はここ1本（本番も検算も通る。判定を2か所に書かない）。"""
    return DUR_MIN <= sec <= DUR_MAX
PHOTO_LO, PHOTO_HI = 0.45, 0.50
HOOK_DEADLINE = 46.0    # 冒頭のこの秒までに引きを置き切る（3本の実測）

# ⚠️ カットIDは pr01/ep16 の「2文字+2桁」と c101 の「1文字+3桁」の両方がある。
#    [a-z]{2} だけにすると c101 を丸ごと取り逃がし、その行が前のカットに混ざる。
# 🔧＝「第1版から直したカット」の印（2026-09-05 第2版から）。無くても有っても拾う
CUT_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／\s*([^／]*)／')
SUB_RE = re.compile(r'^>\s?(.*)$')
STAR_RE = re.compile(r'^★')

# 煽り語。⚠️「衝撃荷重」は NIST の Impulsive loads の訳＝技術用語なので除く。
#    判定は「こちらが盛ったか」であって単語そのものではない。
HYPE = ['即死', '絶命', '闇', '隠蔽', '悲劇', '戦慄', '驚愕', '恐怖の']
HYPE_ALLOW = {'衝撃': ['衝撃荷重']}


def clean(line):
    return STAR_RE.sub('', line).replace('**', '').strip()


def parse(text):
    """§4 台本 の中だけを読む。§5 以降は読まない。"""
    cuts, cur, on = [], None, False
    for raw in text.split('\n'):
        line = raw.rstrip()
        if line.startswith('## 4. 台本'):
            on = True
            continue
        if on and re.match(r'^## \d', line):
            break
        if not on:
            continue
        m = CUT_RE.match(line)
        if m:
            cur = (m.group(1), m.group(2).strip(), [])
            cuts.append(cur)
            continue
        m = SUB_RE.match(line)
        if m and cur is not None and m.group(1).strip():
            cur[2].append(m.group(1).strip())
    return cuts


def pic_kind(pic):
    if '実写' in pic:
        return 'A'          # 映像
    if re.search(r'図\s*p\d', pic):
        return 'B'          # 報告書の図（実物）
    if pic.startswith('図'):
        return 'C'          # 自作の模式図 → 写真映像に数えない
    return 'D'              # 型のみ


def fmt(s):
    return '%d分%02d秒' % (int(s) // 60, int(s) % 60)


def measure(cuts):
    # 🔴 実測の 文字/秒 に差し替えられるならする（別の回の音なら定数のまま）
    use_measured_cps([c for c, _, _ in cuts])
    lines = [clean(l) for _, _, ls in cuts for l in ls]
    chars = sum(len(l) for l in lines)
    n, nq = len(cuts), sum(1 for _, _, ls in cuts if any(STAR_RE.match(l) for l in ls))
    d1 = n * PER_CUT
    d2 = chars / EP2_CPS
    d3 = chars / CPS + TAIL * n + TAIL_EXTRA_QUOTE * nq
    return dict(cuts=cuts, lines=lines, chars=chars, n=n, nq=nq,
                d1=d1, d2=d2, d3=d3, med=sorted([d1, d2, d3])[1])


def report(cuts):
    E, W = [], []
    m = measure(cuts)
    n, chars = m['n'], m['chars']
    print('カット %d / 字幕行 %d / 本文 %d字 / 決め所 %d' % (n, len(m['lines']), chars, m['nq']))
    print('1カット平均 %.1f字 / %.2f行   1行 中央値%d字 最長%d字'
          % (chars / n, len(m['lines']) / n, median(sorted(len(l) for l in m['lines'])),
             max(len(l) for l in m['lines'])))
    print('① %s  ② %s  ③ %s  → 中央値 %s (+1.5%%で %s)'
          % (fmt(m['d1']), fmt(m['d2']), fmt(m['d3']), fmt(m['med']), fmt(m['med'] * 1.015)))
    # 🔴 尺の数字が**どの速さで出た値か**を必ず表に出す（定数が古くても黙って通るのを防ぐ）
    print('   話速 %.2f 文字/秒 ← %s' % (CPS, CPS_SOURCE))
    spread = max(m['d1'], m['d2'], m['d3']) - min(m['d1'], m['d2'], m['d3'])
    print('   3通りの開き %s' % fmt(spread))
    if spread > 120:
        W.append('W 尺の3通りの開きが %s ある。①は字数を見ていないので、①だけ見ると気づけない' % fmt(spread))
    if not dur_ok(m['med']):
        # ⚠️ しきい値を直したら文言も一緒に動くようにする（定数と文が食い違わないため）
        E.append('E 尺 %s が %s〜%s の外' % (fmt(m['med']), fmt(DUR_MIN), fmt(DUR_MAX)))

    # 1行41字 / 1カット1〜3行
    for cid, _, ls in cuts:
        for l in ls:
            if len(clean(l)) > MAX_CHARS_PER_LINE:
                E.append('E %s 1行%d字（上限%d）: %s' % (cid, len(clean(l)), MAX_CHARS_PER_LINE, clean(l)))
        if not 1 <= len(ls) <= 3:
            E.append('E %s の行数が %d（1〜3行）' % (cid, len(ls)))

    # 決め所はカットの最後の行に置く（with_last のため）
    for cid, _, ls in cuts:
        idx = [i for i, l in enumerate(ls) if STAR_RE.match(l)]
        if idx and (len(idx) != 1 or idx[0] != len(ls) - 1):
            E.append('E %s の★が最後の行にない（with_last が成立しない）' % cid)

    # 二重表示: 決め所の文言が、ほかのカットの字幕にも出ていないか
    phr = {cid: clean(ls[-1]) for cid, _, ls in cuts if any(STAR_RE.match(l) for l in ls)}
    allline = [(cid, clean(l)) for cid, _, ls in cuts for l in ls]
    for cid, p in phr.items():
        core = p.rstrip('。')
        for c2, l in allline:
            if c2 == cid and l.rstrip('。') == core:
                continue
            if core and core in l:
                E.append('E 決め所の二重表示: %s「%s」が %s にも出る' % (cid, p, c2))

    # 煽り語
    for cid, _, ls in cuts:
        for l in ls:
            t = clean(l)
            for w in HYPE:
                if w in t:
                    E.append('E %s に煽り語「%s」: %s' % (cid, w, t))
            for w, allow in HYPE_ALLOW.items():
                if w in t and not any(a in t for a in allow):
                    W.append('W %s に「%s」。盛った語でないなら可（例: %s）: %s'
                             % (cid, w, '／'.join(allow), t))

    # 写真映像の割合（全体と章ごと。⚠️ 全体だけだと章の穴が見えない）
    ch = {}
    for cid, pic, _ in cuts:
        k = cid[:2]
        a, b, tot = ch.get(k, (0, 0, 0))
        kind = pic_kind(pic)
        ch[k] = (a + (kind == 'A'), b + (kind == 'B'), tot + 1)
    A = sum(v[0] for v in ch.values())
    B = sum(v[1] for v in ch.values())
    ratio = (A + B) / n
    print('写真映像 %d（実写%d＋報告書の図%d）/ %d = %.1f%%' % (A + B, A, B, n, 100 * ratio))
    if ratio < PHOTO_LO:
        E.append('E 写真映像が %.1f%%（下限%.0f%%）' % (100 * ratio, 100 * PHOTO_LO))
    elif ratio > PHOTO_HI:
        W.append('W 写真映像が %.1f%%（目安の上は%.0f%%。趣旨は「半分近く」なので可）'
                 % (100 * ratio, 100 * PHOTO_HI))
    print('  章ごと: ' + ' '.join('%s=%.0f%%' % (k, 100 * (v[0] + v[1]) / v[2]) for k, v in ch.items()))
    for k, (a, b, tot) in ch.items():
        if (a + b) / tot < PHOTO_LO:
            W.append('W 章 %s の写真映像が %.1f%%（%d/%d）。ここがいちばん飽きやすい'
                     % (k, 100 * (a + b) / tot, a + b, tot))

    # 冒頭の実尺（引きが46秒より前に置き切れているか）
    t = 0.0
    print('冒頭:', end=' ')
    for cid, _, ls in cuts[:8]:
        c = sum(len(clean(l)) for l in ls)
        t += c / CPS + LEAD + TAIL
        print('%s=%.1fs' % (cid, t), end=' ')
        if t > HOOK_DEADLINE:
            break
    print()
    qi = [i for i, (_, _, ls) in enumerate(cuts) if any(STAR_RE.match(l) for l in ls)]
    if qi:
        gaps = [qi[0]] + [qi[k] - qi[k - 1] for k in range(1, len(qi))] + [n - 1 - qi[-1]]
        print('決め所の位置: %s   最大の空白 %dカット ≒ %s'
              % (qi, max(gaps), fmt(max(gaps) * PER_CUT)))
        if max(gaps) * PER_CUT > 300:
            W.append('W 決め所の空白が最大 %s。画面に大きな文字が出ない区間が長い' % fmt(max(gaps) * PER_CUT))

    print()
    for x in E:
        print('🔴 ' + x)
    for x in W:
        print('⚠️ ' + x)
    print('E %d件 / W %d件' % (len(E), len(W)))
    return len(E)


SAMPLE = '''## 4. 台本

**pr01** ／ 実写 B-Roll #1 `0:07` ／ NIST
> あいうえお
> かきくけこ

**c101** ／ 図 p75（断面）／ 技術的知見 p75
> さしすせそ
> ★**たちつてと**

## 5. つぎ
**c999** ／ これは数えてはいけない ／ ―
> ぬねの
'''


def selftest():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print('  %s %-22s 期待 %-12s 実際 %s' % ('OK ' if good else '🔴NG', name, want, got))

    cuts = parse(SAMPLE)
    chk('カット数', len(cuts), 2)
    chk('c101を拾う', [c for c, _, _ in cuts], ['pr01', 'c101'])
    chk('§5を読まない', 'c999' in [c for c, _, _ in cuts], False)
    # 🔧 付きの見出し行も拾えるか（第2版の書式。落とすと直したカットが丸ごと消える）
    fixed = parse('## 4. 台本\n**c412** 🔧 ／ 図 p75（断面）／ 技術的知見 p75\n> なにぬねの\n')
    chk('🔧付きを拾う', [(c, pic_kind(p)) for c, p, _ in fixed], [('c412', 'B')])
    chk('字幕行', sum(len(ls) for _, _, ls in cuts), 4)
    m = measure(cuts)
    # 5字×4行＝20。★と ** は字数に数えない
    chk('字数(★と**を除く)', m['chars'], 20)
    chk('決め所', m['nq'], 1)
    chk('画の種別A', pic_kind('実写 B-Roll #1 `0:07`'), 'A')
    chk('画の種別B', pic_kind('図 p75（断面）'), 'B')
    chk('画の種別C', pic_kind('図（自作の模式）'), 'C')
    chk('画の種別D', pic_kind('panel（結論）'), 'D')

    # 41字超・★が最後でない・二重表示を、わざと作って検出できるか
    bad = SAMPLE.replace('> かきくけこ', '> ' + 'あ' * 42)
    chk('41字超を検出', report_quiet(parse(bad)) > 0, True)
    bad2 = SAMPLE.replace('> さしすせそ\n> ★**たちつてと**', '> ★**たちつてと**\n> さしすせそ')
    chk('★が最後でないのを検出', report_quiet(parse(bad2)) > 0, True)
    bad3 = SAMPLE.replace('> あいうえお', '> たちつてと')
    chk('二重表示を検出', report_quiet(parse(bad3)) > 0, True)
    bad4 = SAMPLE.replace('> あいうえお', '> 即死であった')
    chk('煽り語を検出', report_quiet(parse(bad4)) > 0, True)

    # 🔴 尺の下限・上限（2026-09-07 に下限を 35分→30分 にしたとき新設）。
    #    ⚠️ それまで**しきい値そのものを試す検算が1本も無かった**＝
    #       値を書き換えても誰も気づかない状態だった（[[feedback-rules-need-gates]]）。
    #    境目のちょうど上・ちょうど下・1秒外を、**本番の dur_ok() そのもの**に入れる。
    chk('尺 30分00秒は通る', dur_ok(30 * 60), True)
    chk('尺 29分59秒は落ちる', dur_ok(30 * 60 - 1), False)
    chk('尺 38分00秒は通る', dur_ok(38 * 60), True)
    chk('尺 38分01秒は落ちる', dur_ok(38 * 60 + 1), False)
    # 旧の下限（35分）だった帯が、いまは通ること＝変更が効いていること
    chk('尺 32分（旧下限の下）が通る', dur_ok(32 * 60), True)
    chk('下限の表示が定数と揃う', fmt(DUR_MIN), '30分00秒')

    print('selftest:', 'PASS' if ok else '🔴FAIL')
    return ok


def report_quiet(cuts):
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        return report(cuts)
    finally:
        sys.stdout = old


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    if '--selftest' in sys.argv:
        sys.exit(0 if selftest() else 1)
    if len(sys.argv) < 2:
        print('usage: check_script.py <台本.md> | --selftest')
        sys.exit(2)
    text = open(sys.argv[1], encoding='utf-8').read()
    cuts = parse(text)
    if not cuts:
        print('🔴 カットを1つも拾えなかった。"## 4. 台本" の節があるか、'
              'カットの行が **id** ／ 画 ／ 出典 の形かを確かめる')
        sys.exit(2)          # fail closed。0件を「合格」にしない
    sys.exit(1 if report(cuts) else 0)


if __name__ == '__main__':
    main()
