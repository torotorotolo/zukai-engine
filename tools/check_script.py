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
#
# 🔴🔴 2026-09-08（6本目③）に取り直した。旧コメントの「5.37 は推定」はそのとおりで、**実測は 5.62**。
#    ① `eleven_v3` は `voice_settings.speed` を**見ていない**（`tools/el_speed_probe.py` で実測）。
#       speed 0.7 と 1.2 で同じ8文を合成しても秒の比は中央値 0.98（線形なら 0.583）。
#       同じ文・同じ設定の引き直しのばらつきが 3.04% なので、**効果は誤差に埋もれている＝効いていない**。
#       ＝「6本目から話速 1.05」は**このモデルでは実現できない**（1.0 のまま）。
#    ② 旧の式（chars/CPS + TAIL*n）は完成尺を **7.5〜8.5% 短く**読んでいた。
#       抜けていたのは**カット内の行間 GAP**（narration.json の gap=0.4秒 ×（行数−カット数））と **LEAD**。
#       ⚠️ **GAP が抜けていること自体は 2026-09-07 に気づかれていた**（記憶 reference-elevenlabs-tts
#          「check_script の話速は字幕1行の発話だけで GAP 223か所×0.40＝89秒が入らない」）。
#          **気づいたが門番は直さなかった**ので、5本目も6本目も同じ短い数字が出ていた。
#          → [[feedback-rules-need-gates]]（気づきをコードに入れるまで、粗は消えない）
#       検算（ElevenLabs の2本の完成尺と突き合わせ。陽性対照＝下の SL1_REF / SS_REF）:
#         4本目 サーフサイド 予測 2128.2 / 実測 2127.3 → **+0.04%**
#         5本目 SL-1        予測 2181.2 / 実測 2181.3 → **-0.01%**
#    → [[feedback-gates-go-stale-when-upstream-changes]] / [[feedback-dont-state-inferences-as-findings]]
CPS_FALLBACK = 5.62     # 文字/秒（話速1.0 の**実測**＝SL-1 の発話秒 1877.9 ÷ 10,553字。音があれば narration.json から）
PER_CUT = 10.29         # 秒/カット（話速1.0 の**実測**＝SL-1 の完成尺 2181.3秒 ÷ 212カット）
LEAD, TAIL = 0.35, 0.50
GAP = 0.40              # カット内の行と行のあいだ（narration.json の gap と同じ値。替えたら両方直す）
TAIL_EXTRA_QUOTE = 2.0
# 陽性対照＝この2本を下の measure() の式に当てて 0.5% 以内に入ること（--refcheck）
SL1_REF = dict(name="5本目 SL-1", n=212, lines=435, chars=10553, nq=17, cps=5.62, real=2181.3)
SS_REF = dict(name="4本目 サーフサイド", n=240, lines=486, chars=11027, nq=12, cps=6.12, real=2127.3)
EP2_CPS = 5.00          # ep2 の設計値
MAX_CHARS_PER_LINE = 41
# 🔴🔴 2026-09-08 カズヤくん指示「次回から動画尺の下限を27分に変更してください」
#    （**事故検証chだけ**・6本目から）。旧＝30分（09-07）／その前は35分。
#    ⚠️ これは 2026-08-03 の「固定の下限は置かない（題材ごとに競合を実測して決める）」を
#       **上書きする**（新しい指示を採る）。上限 38分は一度も動かしていない。
#    ⚠️ 実測では **35〜50分帯が1.47倍**。27〜35分はその帯の外側なので、
#       そこに寄せるなら題材の側に理由が要る（この門番は「外」とは言わなくなるだけ）。
#       ＝**下限を下げたのは「素材の薄い題材を無理に伸ばさない」ためで、短くするためではない。**
DUR_MIN = 27 * 60
# 🔴🔴 2026-09-08 カズヤくん指示「**今後どの動画尺においても上限を40分とします**」。
#    ⚠️ **このチャンネル（事故検証ch「そのとき、何が起きたか」）限定**（2026-09-08 本人が明示）。
#       心理ch・フクロウ・ショートには当てない（それぞれ別のリポジトリに別の定数がある）。
#    ＝ 事故検証ch の**恒久の既定**。同じ日の「この動画においては上限は40分」（＝この回だけ）は
#      本人が**訂正**したので撤回ずみ（[[feedback-new-rules-override-old]]＝新しい指示を採る）。
#    旧＝38分（4本目から一度も動かしていなかった）。下限 27分は据え置き。
DUR_MAX_DEFAULT = 40 * 60

# 回ごとの上書き。いまは**空**（＝全回 40分）。次に「この回だけ」と言われたときの置き場として残す。
# ⚠️ ここに書いたら、その回が終わったときに消すこと（消し忘れると次の回へ黙って持ち越される）。
DUR_MAX_OVERRIDE = {}


def _slug():
    """いま作っている回の名前。取れなければ None（＝上書きを当てない＝既定の 38分）。"""
    try:
        import el_script
        return el_script.SLUG
    except Exception:
        return None


DUR_MAX = DUR_MAX_OVERRIDE.get(_slug(), DUR_MAX_DEFAULT)


def measured_cps(cuts=None, path="audio/narration.json"):
    """🔴 実際に合成した音から 文字/秒 を測る。無ければ／別の回のものなら None（定数に落ちる）。

    ⚠️ `narration.json` の `speed` 欄は**帳簿の値**であって送った値ではない
       （4本目は `speed: 1.0`・`settings: null` と書いてあるのに、声側の既定 1.14 で読まれていた）。
       だから欄を読まず、**字幕の実測の長さ**から測る。
    ⚠️⚠️ **`narration.json` は前の回のものが残る。**
       題材を替えた直後は 4本目（サーフサイド）の音が置いたままなので、
       そのまま測ると**別の回の速さを 5本目の台本に当てる**。
       `cuts`（いま検査している台本）を渡して、**重なりが半分未満なら使わない**。
       → [[feedback-gates-go-stale-when-upstream-changes]]

    🔴🔴 2026-09-07（5本目④）：**カットIDの重なりだけでは足りなかった。**
       `pr01` `c101` `c201` … は題材をまたいで必ずぶつかる（1本目229中201件が2本目と重複した実績）。
       SL-1 の台本を掛けたら重なりが半分を超え、**4本目の 6.12 文字/秒（実効 speed 1.14）が
       黙って採用された**。尺の表には「narration.json の実測」と出るので、気づけない形の誤りだった。
       → **IDが重なっても「文が違えば別の回」**とする層を足した（空白を除いた文字列の一致）。
       ⚠️ 門番は壊れず、**黙って間違った合格**を出す。
    """
    import json
    from pathlib import Path
    p = Path(__file__).resolve().parent.parent / path
    if not p.exists():
        return None, "音がまだ無い"
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        sub = d["subtitles"]
        if cuts is not None:
            want = {cid: [clean(x) for x in ls] for cid, _, ls in cuts}
            hit = same = 0
            for cid, lines in want.items():
                segs = sub.get(cid)
                if not segs:
                    continue
                hit += 1
                a = re.sub(r'\s', '', ''.join(lines))
                b = re.sub(r'\s', '', ''.join(s.get("text", "") for s in segs))
                same += (a == b)
            if not want or hit / len(want) < 0.5:
                return None, f"narration.json は別の回のもの（カットの重なり {hit}/{len(want)}）"
            if same / hit < 0.5:
                return None, (f"🔴 カットIDは重なるが**文が違う**＝別の回の音"
                              f"（ID一致 {hit}/{len(want)}・文一致 {same}/{hit}）")
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


def use_measured_cps(cuts):
    """検査する台本が決まった時点で CPS を実測に差し替える（合わなければ定数のまま）。"""
    global CPS, CPS_SOURCE
    v, why = measured_cps(cuts)
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
    use_measured_cps(cuts)
    lines = [clean(l) for _, _, ls in cuts for l in ls]
    chars = sum(len(l) for l in lines)
    n, nq = len(cuts), sum(1 for _, _, ls in cuts if any(STAR_RE.match(l) for l in ls))
    d1 = n * PER_CUT
    d2 = chars / EP2_CPS
    d3 = est_sec(chars, len(lines), n, nq, CPS)
    return dict(cuts=cuts, lines=lines, chars=chars, n=n, nq=nq,
                d1=d1, d2=d2, d3=d3, med=sorted([d1, d2, d3])[1])


def est_sec(chars, lines, n, nq, cps):
    """🔴 完成尺の見積り。**行間 GAP とカット頭の LEAD を落とすと 8% 短く出る**（上のコメント②）。

    発話 chars/cps ＋ カット内の行間 GAP×(行数−カット数) ＋ カット頭尻 (LEAD+TAIL)×カット数
    ＋ 決め所の余白 2.0×決め所数。"""
    return (chars / cps + GAP * (lines - n)
            + (LEAD + TAIL) * n + TAIL_EXTRA_QUOTE * nq)


def refcheck(tol=0.5):
    """陽性対照＝完成尺が分かっている2本に est_sec を当てて、ずれが tol% 以内か見る。"""
    bad = 0
    for r in (SS_REF, SL1_REF):
        p = est_sec(r["chars"], r["lines"], r["n"], r["nq"], r["cps"])
        d = 100 * (p - r["real"]) / r["real"]
        ok = abs(d) <= tol
        bad += not ok
        print("  %s %-18s 予測 %.1f / 実測 %.1f → %+.2f%%"
              % ("✓" if ok else "E", r["name"], p, r["real"], d))
    if bad:
        print("E 尺の式が陽性対照から %.1f%% 以上ずれている。定数か上流が変わった" % tol)
    return bad


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

    # 🔴 2026-09-10（6本目キー橋 ⑤c' 2巡目・§T-9-1）：**句点の様式を規則として書く。**
    #    ⑤c の目視で「22カットだけ最終行に句点が無い。様式か、揃っていないだけか」と
    #    保留になった。全443行を数えると、句点の無い52行の内訳は
    #      ・読点で次の行へ続く … 30行（句点を打たないのが正しい）
    #      ・**カットの最終行** … 22行（短い言い切り）
    #      ・**カットの途中の行 … 0行**
    #    22行が偶然すべて最終行に落ちることはない ＝ **設計**。よって様式として確定した。
    #    ⚠️ 規則がどこにも書かれていなかったので、ここに門番を足す
    #    （[[feedback-rules-need-gates]]。検査の無い規則は次の回で崩れる）。
    #    規則 ＝ **句点で終わらない行は、読点で続く行か、カットの最終行のどちらか**。
    for cid, _, ls in cuts:
        for i, l in enumerate(ls):
            t = clean(l)
            if not t or t.endswith('。') or t.endswith('、') or t.endswith('，'):
                continue
            if i != len(ls) - 1:
                E.append('E %s の途中の行が句点でも読点でも終わっていない: %s'
                         % (cid, t))

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

    # 🔴 2026-09-12 追加。5本目 SL-1 に付いた視聴者コメント
    #    「物の単位をメートル法などに直していただけるだけでも大変助かります」＋
    #    カズヤくん「初めて見た人・中学生が理解できるかを基準に」。
    #    ヤード・ポンド法の数字は、**同じカットの中**にメートル換算が無ければ E。
    #    ⚠️ 換算は門番を通すためでなく、聞く人が量を掴むために置く（意味の無い換算はしない）。
    #    ⚠️ 6本目キー橋は 28か所中 24か所が換算なしだった（公開ずみなので直さない）。
    #    🔴 2026-09-13（7本目②）に2か所直した:
    #      (a) **「華氏」と「°F」が網に無かった。**9.11 は鉄と火災＝温度の話をする回で、
    #          この穴を開けたまま④に入ると**温度だけ原単位のまま通る**。
    #      (b) **`met.search(body)` で「カットのどこかに1語でもメートル法があれば全体を免除」
    #          していた。** ＝「全長1,200メートルの橋で、船は毎時8ノット」が素通りする。
    #          → **原単位1つずつに、その単位に対応する換算語が近く（±60字）にあるか**を見る。
    IMP = {
        'フィート': r'メートル|センチ|キロ',
        'インチ': r'センチ|ミリ|メートル',
        'ヤード': r'メートル|キロ',
        'マイル': r'キロ|メートル',
        'ノット': r'時速|キロ',
        'ポンド': r'キロ|グラム|トン',
        'ガロン': r'リットル',
        # ⚠️ ここに「度」を入れてはいけない。**「華氏1,000度」の「度」が自分に当たって
        #    免除される**（陽性対照 t01 が2回続けて鳴らなかった原因がこれ）。
        '華氏': r'摂氏|℃|°C',
        '°F': r'摂氏|℃|°C',
    }
    #      (c) ⚠️ **陽性対照で見つけた3つ目の穴。**「華氏1,000度」は日本語だと
    #          **単位が数の前**に来る。`[0-9]…(華氏)` の形では**一度も鳴らない**
    #          （実測：t01「鋼材は華氏1,000度」が鳴らなかった）。数の前後どちらも見る。
    _u = '|'.join(map(re.escape, IMP))
    imp = re.compile(r'[0-9][0-9,.]*\s*(' + _u + r')'          # 1,368フィート
                     r'|(' + _u + r')\s*[0-9][0-9,.]*')         # 華氏1,000
    WIN = 60
    for cid, _, ls in cuts:
        body = ''.join(clean(l) for l in ls)
        for m in imp.finditer(body):
            unit = m.group(1) or m.group(2)
            near = body[max(0, m.start() - WIN):m.end() + WIN]
            if re.search(IMP[unit], near):
                continue
            E.append('E %s の単位が原文のまま（前後%d字にメートル換算が無い）: %s'
                     % (cid, WIN, m.group(0)))

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

    # 🔴 単位（2026-09-12）。⚠️ 陽性対照は「鳴った／鳴らない」でなく**件数の差**で見る
    #    （[[feedback-verify-your-own-instrument]]＝もともと0件の指標は真偽だけだと動いて見える）
    base = report_quiet(parse(SAMPLE))
    imp_bad = SAMPLE.replace('> あいうえお', '> 橋まで939フィート。速力7.5ノット')
    imp_ok = SAMPLE.replace('> あいうえお', '> 橋まで286メートル（939フィート）')
    chk('単位の換算なしを検出', report_quiet(parse(imp_bad)) - base, 2)
    chk('同じカットに換算があれば鳴らない', report_quiet(parse(imp_ok)) - base, 0)

    # 🔴 尺の下限・上限（2026-09-07 に下限を 35分→30分 にしたとき新設）。
    #    ⚠️ それまで**しきい値そのものを試す検算が1本も無かった**＝
    #       値を書き換えても誰も気づかない状態だった（[[feedback-rules-need-gates]]）。
    #    境目のちょうど上・ちょうど下・1秒外を、**本番の dur_ok() そのもの**に入れる。
    chk('尺 27分00秒は通る', dur_ok(27 * 60), True)
    chk('尺 26分59秒は落ちる', dur_ok(27 * 60 - 1), False)
    chk('尺 上限ちょうどは通る', dur_ok(DUR_MAX), True)
    chk('尺 上限＋1秒は落ちる', dur_ok(DUR_MAX + 1), False)
    # 旧の下限だった帯が、いまは通ること＝変更が効いていること
    chk('尺 32分（旧下限35分の下）が通る', dur_ok(32 * 60), True)
    chk('尺 28分（旧下限30分の下）が通る', dur_ok(28 * 60), True)
    chk('下限の表示が定数と揃う', fmt(DUR_MIN), '27分00秒')
    # 🔴 上限そのものの検算（2026-09-08 に 38→40分。事故検証ch 限定・全回）。
    #    ⚠️ 定数を書き換えても誰も気づかない状態にしない。上限の**値**をここに直接書く。
    chk('上限の既定は40分', DUR_MAX_DEFAULT, 40 * 60)
    chk('回ごとの上書きは いまは無い', dict(DUR_MAX_OVERRIDE), {})
    chk('上限の表示が定数と揃う', fmt(DUR_MAX), '40分00秒')
    chk('尺 39分（旧上限38分の上）が通る', dur_ok(39 * 60), True)
    chk('尺 40分01秒は落ちる', dur_ok(40 * 60 + 1), False)

    # 🔴🔴 2026-09-07 新設：**カットIDが重なっても「文が違えば別の回」**と判定できるか。
    #    ⚠️ ここが無かったせいで、5本目の台本に 4本目（サーフサイド・実効 speed 1.14）の
    #       6.12 文字/秒 が黙って当たった。尺の表は「narration.json の実測」と出るので気づけない。
    #    陽性対照（同じ回＝使う）・陰性対照2種（文が違う／IDが違う＝使わない）の3本を本番の関数に入れる。
    import json as _json, os as _os, tempfile as _tf
    _tmp = _os.path.join(_tf.gettempdir(), 'check_script_selftest_narration.json')

    def _write(subs):
        with open(_tmp, 'w', encoding='utf-8') as f:
            _json.dump({'subtitles': subs}, f, ensure_ascii=False)

    A, B = 'あいうえおかきくけこ', 'さしすせそたちつてと'          # 10字ずつ＝合計20字
    tc = [('pr01', '実写', [A]), ('c101', '実写', [B])]
    try:
        _write({'pr01': [{'text': A, 'd': 2.0}], 'c101': [{'text': B, 'd': 2.0}]})
        chk('同じ回の音は実測を使う', measured_cps(tc, _tmp)[0], 5.0)          # 20字÷4.0秒
        _write({'pr01': [{'text': 'まったくちがうもんくです', 'd': 2.0}],
                'c101': [{'text': 'これもちがうもんくです', 'd': 2.0}]})
        chk('🔴IDが重なっても文が違えば捨てる', measured_cps(tc, _tmp)[0], None)
        _write({'zz01': [{'text': A, 'd': 2.0}]})
        chk('IDが重ならなければ捨てる', measured_cps(tc, _tmp)[0], None)
        chk('音が無ければ定数に落ちる', measured_cps(tc, _tmp + '.nope')[0], None)
    finally:
        if _os.path.exists(_tmp):
            _os.remove(_tmp)

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
    if '--refcheck' in sys.argv:
        print('尺の式の陽性対照（完成尺が分かっている2本に当てる）')
        sys.exit(1 if refcheck() else 0)
    if len(sys.argv) < 2:
        print('usage: check_script.py <台本.md> | --selftest | --refcheck')
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
