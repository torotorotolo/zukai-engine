# -*- coding: utf-8 -*-
"""台本の第N版と第N+1版を突き合わせ、**🔧 の印が実際の差分と一致するか**を見る門番。

    python tools/check_script_diff.py <前の版.md> <あとの版.md>
    python tools/check_script_diff.py --selftest

なぜ要るか
----------
2026-09-08 に工程を変え、**④' 台本【チェックと修正】を別チャットに移した**
（→ 記憶 [[feedback-jiko-production-order]]／Vault 事故検証-制作ルール統合版 §0b）。
④' は毎回、**第2版と「変更台帳」**を出す。台帳は手で書くので、必ずずれる。

- **変わったのに 🔧 の印が無い** … 台帳に載らない直しができる＝レビューを素通りする
- **印があるのに変わっていない** … 台帳が嘘をつく（直したつもりで直っていない）
- **欠番**（前の版にあって、あとの版に無いカット） … 黙って消えるといちばん気づけない

⚠️ 5本目 SL-1 の第2版では、この検算で欠番4件（c311 c313 c315 c818）が確定した。

`check_script.py` の `parse` / `clean` をそのまま使う（**判定を2か所に書かない**）。
→ [[feedback-verify-your-own-instrument]] / [[feedback-rules-need-gates]]

⚠️ **この道具は「印と差分が合っているか」しか見ない。**
　 直しの中身が良いかは見ない。それは人の仕事。

終了コード: 0=印と差分が一致 / 1=ずれている / 2=道具の異常
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_script as cs                                    # noqa: E402

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 🔧 は見出し行のカットIDの直後。`**c412** 🔧 ／ …`
MARK_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*🔧', re.M)


def cuts_of(text):
    """{カットID: (画の欄, [字幕行…])}。★ と ** は落として比べる（印の有無で差分にしない）。"""
    return {cid: (pic.strip(), [cs.clean(l) for l in ls]) for cid, pic, ls in cs.parse(text)}


def diff(t1, t2):
    c1, c2 = cuts_of(t1), cuts_of(t2)
    marked = set(MARK_RE.findall(t2))
    added = set(c2) - set(c1)
    changed = {cid for cid in c2 if cid not in c1 or c1[cid] != c2[cid]}
    removed = set(c1) - set(c2)
    # 何が変わったかの内訳（文だけ／画だけ／両方）
    kind = {}
    for cid in sorted(changed - added):
        pic_ch = c1[cid][0] != c2[cid][0]
        sub_ch = c1[cid][1] != c2[cid][1]
        kind[cid] = '画と文' if (pic_ch and sub_ch) else ('画' if pic_ch else '文')
    return dict(marked=marked, changed=changed, removed=removed, added=added, kind=kind,
                n1=len(c1), n2=len(c2))


def report(t1, t2, quiet=False):
    d = diff(t1, t2)
    no_mark = sorted(d['changed'] - d['marked'])
    no_change = sorted(d['marked'] - d['changed'])
    p = (lambda *a: None) if quiet else print
    p('カット %d → %d（欠番 %d / 新設 %d）' % (d['n1'], d['n2'], len(d['removed']), len(d['added'])))
    p('🔧 の印 %d件 / 実際に変わった %d件' % (len(d['marked']), len(d['changed'])))
    p('  欠番: %s' % (sorted(d['removed']) or '無し'))
    p('  新設: %s' % (sorted(d['added']) or '無し'))
    if d['kind']:
        p('  変わった中身: ' + ' '.join('%s(%s)' % (c, k) for c, k in sorted(d['kind'].items())))
    if no_mark:
        p('🔴 変わったのに 🔧 の印が無い: %s' % no_mark)
    if no_change:
        p('🔴 🔧 の印があるのに変わっていない: %s' % no_change)
    if not no_mark and not no_change:
        p('✅ 印と差分が一致している')
    if d['removed'] and not quiet:
        p('⚠️ 欠番は「印」では表せない。**変更台帳に1行ずつ理由を書く**こと')
    return len(no_mark) + len(no_change)


V1 = '''## 4. 台本

**c101** ／ panel（甲）／ X p1
> あいうえお。
> かきくけこ。

**c102** ／ panel（乙）／ X p1
> さしすせそ。

**c103** ／ 図 p9（丙）／ X p9
> たちつてと。

**c104** ／ panel（丁）／ X p1
> なにぬねの。

## 5. つぎ
**c999** ／ 数えない ／ ―
> はひふへほ。
'''


def selftest():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print('  %s %-30s 期待 %-14s 実際 %s' % ('OK ' if good else '🔴NG', name, want, got))

    # ① 何も変えなければ、印も差分も0
    chk('同じ版どうしは差分0', report(V1, V1, quiet=True), 0)
    chk('  そのとき変わった件数も0', len(diff(V1, V1)['changed']), 0)

    # ② 文を変えて印を付けた＝正しい直し方
    good = V1.replace('**c101** ／', '**c101** 🔧 ／').replace('> かきくけこ。', '> かきくけこ、さ。')
    chk('文＋印は通る', report(V1, good, quiet=True), 0)
    chk('  内訳は「文」', diff(V1, good)['kind'].get('c101'), '文')
    # ⚠️ 🔧 は「前の版からの差」の印なので、**同じ版どうしを掛けると必ず落ちる**
    #    （印が残っているのに差が無い＝正しい振る舞い）。ここを取り違えて selftest を1度書き損じた。
    chk('  第2版どうしを掛けると落ちる', report(good, good, quiet=True), 1)

    # ③ 画だけ変えて印を付けた
    picm = V1.replace('**c102** ／ panel（乙）', '**c102** 🔧 ／ 実写 なにか（乙）')
    chk('画だけの変更も拾う', diff(V1, picm)['kind'].get('c102'), '画')
    chk('  画だけ＋印は通る', report(V1, picm, quiet=True), 0)

    # ④ 陽性対照：印を付けずに変えた／変えずに印を付けた／欠番
    bad1 = V1.replace('> さしすせそ。', '> さしすせそ、た。')
    chk('🔴印なしの変更を捕まえる', report(V1, bad1, quiet=True), 1)
    bad2 = V1.replace('**c103** ／', '**c103** 🔧 ／')
    chk('🔴空の印を捕まえる', report(V1, bad2, quiet=True), 1)
    gone = V1.replace('**c104** ／ panel（丁）／ X p1\n> なにぬねの。\n\n', '')
    chk('欠番を出す', sorted(diff(V1, gone)['removed']), ['c104'])
    chk('  欠番だけなら印のずれは0', report(V1, gone, quiet=True), 0)

    # ⑤ ★ と ** の付け外しだけでは差分にしない（clean をかけて比べているか）
    star = V1.replace('> たちつてと。', '> ★**たちつてと**。')
    chk('★の付け外しは差分でない', len(diff(V1, star)['changed']), 0)

    # ⑥ §5 以降を読んでいないこと
    chk('§5を読まない', 'c999' in cuts_of(V1), False)

    print('selftest:', 'PASS' if ok else '🔴FAIL')
    return 0 if ok else 2


def main(argv):
    if '--selftest' in argv:
        return selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2
    t1 = open(argv[1], encoding='utf-8').read()
    t2 = open(argv[2], encoding='utf-8').read()
    return 1 if report(t1, t2) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
