# -*- coding: utf-8 -*-
"""33本目④'：台本 第2版（daihon_v2.md）から「読みやすい版」を組む（読むだけ・手で写さない・32本目 readable32.py を写した）。

  python -P ref/ep33/v2_build/readable33.py [出力の置き場]

既定の置き場＝Vault の Projects/事故検証-33本目-台本第2版-読みやすい版-20261112.md
1カット＝［目安の時刻］カット番号（🔧＝直したカット）・画面の種類と副題・話し手つきの語り（まりさ＝語り／れいむ＝聞き役）。
時刻＝句読点なしの字を1分365字で積み上げたカットの頭（m33.py の②と同じ数え）。出典の欄は載せない（正本の台本にある）。
"""
import hashlib
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
V2 = os.path.join(EP, 'daihon_v2.md')
VAULT = r'C:\Users\konar\Documents\Obsidian Vault\Projects'
DEF_OUT = os.path.join(VAULT, '事故検証-33本目-台本第2版-読みやすい版-20261112.md')
PUNCT = set('、。？！「」（）・')
CPM = 365.0
CUT = re.compile(r'^\*\*(c[0-9a-c]\d{2})\*\*\s*(🔧)?')


def nopunct(s):
    return ''.join(ch for ch in s if ch not in PUNCT and not ch.isspace())


def pic_label(pic):
    kind = re.split(r'[（(]', pic, 1)[0].strip()
    sub = re.search(r'副題「([^」]*)」', pic)
    return kind, (sub.group(1) if sub else '')


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else DEF_OUT
    raw = open(V2, 'rb').read()
    text = raw.decode('utf-8').replace('\r\n', '\n')
    s4 = text[text.index('## 4. 台本'):text.index('\n## 5.')]
    title = text.split('\n', 1)[0].lstrip('# ').strip()
    lines = ['---', 'title: 事故検証 33本目 台本 第2版 読みやすい版（グレンフェルタワー火災）', 'created: 2026-11-12',
             'tags: [project/jiko-kensho, area/video, ep33]', '---', '',
             '# 33本目 台本 第2版（読みやすい版）', '',
             '> 正本＝リポ `ref/ep33/daihon_v2.md`（md5 `%s`）から `v2_build/readable33.py` が機械で組んだ。**手で直さない**（直すのは正本の差し替え表）。' % hashlib.md5(raw).hexdigest(),
             '> 🔧＝④' + "'" + ' で語りか画面を直したカット。［時刻］＝句読点なしの字を1分365字で積み上げた目安。まりさ＝語り・れいむ＝聞き役。出典の欄は正本にある。',
             '> 元の題：%s' % title, '']
    secs = 0.0
    n = nfix = 0
    cur = None
    buf = []

    def flush():
        nonlocal secs
        if cur is None:
            return
        cid, fix, kind, sub, sp = cur
        mm, ss = divmod(int(secs), 60)
        lines.append('**［%d:%02d］%s**%s ｜ %s%s' % (mm, ss, cid, ' 🔧' if fix else '', kind, ('｜ 副題「%s」' % sub) if sub else ''))
        for who, t in sp:
            lines.append('- %s：%s' % (who, t))
        lines.append('')
        secs += sum(len(nopunct(t)) for _, t in sp) / CPM * 60

    for l in s4.split('\n'):
        m = CUT.match(l)
        if m:
            flush()
            parts = l.split('／')
            kind, sub = pic_label(parts[1] if len(parts) > 1 else '')
            cur = (m.group(1), bool(m.group(2)), kind, sub, [])
            n += 1
            nfix += bool(m.group(2))
            continue
        if l.startswith('### '):
            flush()
            cur = None
            lines.append('## ' + l[4:].strip())
            lines.append('')
            continue
        if cur is not None and l.startswith('>'):
            t = re.sub(r'^>\s?', '', l)
            if t.startswith('Q: '):
                cur[4].append(('れいむ', t[3:]))
            else:
                cur[4].append(('まりさ', t))
    flush()
    mm, ss = divmod(int(secs), 60)
    lines.append('（語りの終わり［%d:%02d］→ 共通エンディング ed01）' % (mm, ss))
    lines.append('')
    lines.append('## 関連')
    lines.append('- [[引き継ぎ-事故検証-33本目-20261112-④' + "'" + '台本チェック]]・[[事故検証-33本目-①芯の確認と数の表-20261112]]・[[事故検証-状況整理-20260926]]')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print('読みやすい版：%d カット（🔧 %d）・語りの終わり %d:%02d → %s' % (n, nfix, mm, ss, out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
