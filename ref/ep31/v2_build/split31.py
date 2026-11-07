# -*- coding: utf-8 -*-
"""31本目④'：照合の係に渡す写しを、章の組ごとに git の外（src/agents/wf31b/）へ書き出す（第1版・直す前の台本は読むだけ）。

  python -P ref/ep31/v2_build/split31.py

出すもの（ref/ep31/src/agents/wf31b/）：
  in_Gn.txt     その組のカットの全行（見出し＝**カット番号** ／ 画の欄 ／ 出典の欄、続く `> ` が語り、`> Q: ` は聞き役）
  fixed_Gn.txt  ④ の係の照合のあとの直し（直す前の台本 src/agents/wf31/daihon_v1_before_wf31.md → 第1版）のうち、その組のカットのもの
                ＝カットごとに、変わった行だけ「− 直す前」「＋ 第1版」で並べる（ルール 4'-5＝ここから当たる）。消えたカットも出す
  prior_Gn.txt  ④ の係の所見（src/agents/wf31/wf31_findings.json）のうち、その組のカットのもの（④ の扱い＝案をそのまま当てた／ほか）
  narr_all.txt  全カットの章の見出し・カット番号・語りと聞き役だけ（G7＝通し読み）
  cuts_v1.txt   全カットの全行（wfx31.py が当て残しのカットを数える）
組＝資料と話が近い章をまとめた：G1 c1〜c3／G2 c4・c5／G3 c6／G4 c7・c8／G5 c9／G6 ca・cb・cc
直す前と第1版のカットの対応は、カット番号ではなく文の似ている度で決める（④ で構成を動かし、番号を振り直したため）。
"""
import difflib
import importlib.util
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
V1 = os.path.join(EP, 'daihon_v1.md')
OLD = os.path.join(EP, 'src', 'agents', 'wf31')
BEFORE = os.path.join(OLD, 'daihon_v1_before_wf31.md')
OUT = os.path.join(EP, 'src', 'agents', 'wf31b')
GROUPS = {'G1': ('c1', 'c2', 'c3'), 'G2': ('c4', 'c5'), 'G3': ('c6',), 'G4': ('c7', 'c8'), 'G5': ('c9',),
          'G6': ('ca', 'cb', 'cc')}
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2}[a-z]?)\*\*')


def cuts(path):
    """§4 の中のカット＝[(番号, 行), …]（空行を除く・文書の順）と、章の見出しの位置。"""
    out, cur, on, heads = [], None, False, []
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        if not on:
            continue
        m = CUT.match(ln)
        if m:
            cur = [m.group(1), [ln]]
            out.append(cur)
        elif ln.startswith('### '):
            heads.append((len(out), ln))
            cur = None
        elif ln.startswith('---'):
            cur = None
        elif cur and ln.strip():
            cur[1].append(ln)
    return out, heads


def body(ls):
    """番号を外した見出しの行と、語り・聞き役の行（似ている度を測る文）。"""
    return '\n'.join([CUT.sub('', ls[0]).replace(' 🔧', '')] + [x for x in ls[1:] if x.startswith('>')])


def group_of(cid):
    for g, hs in GROUPS.items():
        if cid[:2] in hs:
            return g
    return None


def load_accept():
    p = os.path.join(EP, 'v1_build', 'build_patch31.py')
    spec = importlib.util.spec_from_file_location('bp31', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return {str(x) for x in getattr(m, 'ACCEPT', ())}


def main():
    os.makedirs(OUT, exist_ok=True)
    v1, heads = cuts(V1)
    b0, _ = cuts(BEFORE)
    bt = [body(ls) for _, ls in b0]
    best = {}                                # 第1版の番号 → (直す前の添字, 似ている度)
    for cid, ls in v1:
        t = body(ls)
        cand = []
        for i, x in enumerate(bt):
            sm = difflib.SequenceMatcher(None, t, x, autojunk=False)
            if sm.real_quick_ratio() < 0.35 or sm.quick_ratio() < 0.35:
                continue
            cand.append((sm.ratio(), -abs(i - len(cand)), i))
        if cand:
            r, _, i = max(cand)
            best[cid] = (i, r)
    used = {i for i, r in best.values() if r >= 0.4}
    to_v1 = {}
    for cid, (i, r) in best.items():
        if r >= 0.4:
            to_v1.setdefault(b0[i][0], cid)
    accept = load_accept()
    rows = json.load(open(os.path.join(OLD, 'wf31_findings.json'), encoding='utf-8'))['rows']
    prior = {}
    for x in rows:
        fid = '%s%02d' % (x['ag'], int(x['k']))
        cs = re.findall(r'c[0-9a-d]\d{2}[a-z]?', x.get('cid') or '')
        mapped = [to_v1.get(c, c) for c in cs] or ['?']
        how = '案をそのまま当てた' if (fid in accept or ('%s%s' % (x['ag'], x['k'])) in accept) else '親が組んだ直し・まとめた・回した・採らない のどれか（第1版 §0-3）'
        line = '%s %s %s（第1版では %s）[%s] %s ｜ 根拠: %s ｜ 案: %s → %s ｜ ④ の扱い: %s' % (
            fid, x.get('sev'), x.get('cid'), '・'.join(mapped), x.get('kind'), x.get('issue'), x.get('evidence'),
            x.get('fix_old') or '-', x.get('fix_new') or '-', how)
        g = group_of(mapped[0]) or group_of(cs[0] if cs else '') or 'G7'
        prior.setdefault(g, []).append(line)
    n_changed = {}
    for g, hs in GROUPS.items():
        mine = [(c, ls) for c, ls in v1 if c[:2] in hs]
        with open(os.path.join(OUT, 'in_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as f:
            for c, ls in mine:
                f.write('\n'.join(ls) + '\n\n')
        k = 0
        with open(os.path.join(OUT, 'fixed_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# %s：④ の係の照合のあとの直し（直す前 → 第1版・変わった行だけ）。番号は第1版\n\n' % g)
            for c, ls in mine:
                if c not in best or best[c][1] < 0.4:
                    f.write('■ %s＝新しく足したカット（直す前に似たカットなし）\n' % c)
                    for x in ls:
                        f.write('  ＋ %s\n' % x)
                    k += 1
                    continue
                i, r = best[c]
                a, b = b0[i][1], ls
                ta = [CUT.sub('', a[0]).replace(' 🔧', '')] + a[1:]
                tb = [CUT.sub('', b[0]).replace(' 🔧', '')] + b[1:]
                if ta == tb:
                    continue
                k += 1
                f.write('■ %s（直す前は %s・似ている度 %.2f）\n' % (c, b0[i][0], r))
                for d in difflib.ndiff(ta, tb):
                    if d.startswith('- '):
                        f.write('  − 直す前: %s\n' % d[2:])
                    elif d.startswith('+ '):
                        f.write('  ＋ 第1版: %s\n' % d[2:])
            gone = [(bc, ls) for j, (bc, ls) in enumerate(b0) if j not in used and bc[:2] in hs]
            for bc, ls in gone:
                f.write('■ 消えたカット（直す前の %s・第1版に似たカットなし）\n' % bc)
                for x in ls:
                    f.write('  − %s\n' % x)
                k += 1
        n_changed[g] = k
        with open(os.path.join(OUT, 'prior_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# %s：④ の係（A＝判決・白書・法律・記者発表／B＝国会会議録・町の頁／C＝線・分かりやすさ・聞き役・画の欄／D＝通し読み・構成）の所見\n' % g)
            for x in prior.get(g, []):
                f.write(x + '\n')
        print('%s カット %d・④ のあとで変わったカット %d・④ の所見 %d' % (g, len(mine), k, len(prior.get(g, []))))
    if prior.get('G7'):
        with open(os.path.join(OUT, 'prior_G7.txt'), 'w', encoding='utf-8', newline='\n') as f:
            for x in prior['G7']:
                f.write(x + '\n')
    hp = dict(heads)
    with open(os.path.join(OUT, 'narr_all.txt'), 'w', encoding='utf-8', newline='\n') as f:
        for j, (c, ls) in enumerate(v1):
            if j in hp:
                f.write('\n' + hp[j] + '\n')
            f.write('[%s]\n' % c)
            for x in ls[1:]:
                if x.startswith('>'):
                    f.write(x + '\n')
    with open(os.path.join(OUT, 'cuts_v1.txt'), 'w', encoding='utf-8', newline='\n') as f:
        for c, ls in v1:
            f.write('\n'.join(ls) + '\n\n')
    print('第1版 %d カット・直す前 %d カット・対応のついた直す前のカット %d・④ の所見 %d（組の外 %d）' % (
        len(v1), len(b0), len(used), len(rows), len(prior.get('G7', []))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
