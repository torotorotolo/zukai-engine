# -*- coding: utf-8 -*-
"""27本目④'：台本 第2版（daihon_v2.md）から「読みやすい版」を組む（読むだけ・手で写さない）。

  python -P ref/ep27/v2_build/readable27.py [出力の置き場]

既定の置き場＝Vault の Projects/事故検証-27本目-台本第2版-読みやすい版-20261029.md
1カット＝［目安の時刻］カット番号（🔧＝直したカット）・画面の種類と副題・話し手つきの語り（まりさ＝語り／れいむ＝聞き役）。
時刻＝句読点なしの字を1分365字で積み上げたカットの頭（m27.py の②と同じ数え）。出典の欄は載せない（正本の台本にある）。
"""
import hashlib
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
V2 = os.path.join(EP, 'daihon_v2.md')
OUT = r'C:\Users\konar\Documents\Obsidian Vault\Projects\事故検証-27本目-台本第2版-読みやすい版-20261029.md'
PUNCT = set('、。？！「」（）・')
CPM = 365.0
CUT = re.compile(r'^\*\*(c\d{3})\*\*( 🔧)?')
KINDS = [('実写 引用', '実写（警察の素材の引用）'), ('実写 衛星', '実写（衛星写真）'), ('実写 Commons', '実写（写真）'),
         ('図 SNS', '図（SNS の声のカード・注釈つき）'), ('図', '図'), ('イメージ', 'イメージ（フリー素材）')]


def nopunct(s):
    return sum(1 for ch in s if ch not in PUNCT)


def mmss(sec):
    return '%d:%02d' % (int(sec) // 60, int(sec) % 60)


def pic_label(pic):
    kind = next((lab for k, lab in KINDS if pic.startswith(k)), pic.split('（')[0][:20])
    if kind == '図':
        m = re.match(r'図\s+([^\s（(]+)', pic)
        kind = '図（%s）' % m.group(1) if m else '図'
    sub = re.search(r'副題「([^」]+)」', pic)
    return kind + ('　副題「%s」' % sub.group(1) if sub else '')


def main(out):
    src = open(V2, 'rb').read()
    md5 = hashlib.md5(src).hexdigest()
    lines = src.decode('utf-8').split('\n')
    on, t, body, ncut, nfix = False, 0.0, [], 0, 0
    for ln in lines:
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        if not on:
            continue
        if ln.startswith('### '):
            body += ['', '## %s（%s〜）' % (ln[4:].strip(), mmss(t * 60 / CPM)), '']
            continue
        m = CUT.match(ln)
        if m:
            parts = ln.split(' ／ ')
            pic = parts[1].strip() if len(parts) > 1 else ''
            ncut += 1
            nfix += bool(m.group(2))
            if body and body[-1] != '':
                body.append('')
            body.append('**［%s］%s**%s　画面：%s' % (mmss(t * 60 / CPM), m.group(1), ' 🔧' if m.group(2) else '', pic_label(pic)))
            continue
        if ln.startswith('> '):
            text = ln[2:].strip()
            if text.startswith('Q: '):
                body.append('- **れいむ**：' + text[3:])
                t += nopunct(text[3:])
            else:
                body.append('- まりさ：' + text)
                t += nopunct(text)
    head = [
        '---',
        'title: 事故検証 27本目 台本 第2版（読みやすい版）',
        'created: 2026-10-29',
        'tags: [project/jiko-kensho, ep27]',
        '---',
        '',
        '# 27本目 台本 第2版（読みやすい版）＝八田與一容疑者の事件',
        '',
        '> 正本はリポの `ref/ep27/daihon_v2.md`（md5 `%s`）。この頁は `ref/ep27/v2_build/readable27.py` が正本から組んだ写し＝**手で直さない**（直すのは正本の差し替え表）。出典の欄は載せていない（正本にある）。' % md5,
        '> 読み方＝各カットの頭が［目安の時刻］とカット番号（🔧＝④\' と承認①で直したカット）・画面の種類と副題。**まりさ**＝語り（だ・である）、**れいむ**＝聞き役。時刻は句読点なしの字を1分365字で積み上げた目安（本番の声の長さとは少しずれる）。',
        '> 全体＝%dカット（🔧 %d）・本文 %s（このあと共通エンディング `ed01`＝高評価・チャンネル登録の画面と3行＝台本の外）。' % (ncut, nfix, mmss(t * 60 / CPM)),
        '',
        '## 承認①（2026-10-29）で変えた所',
        '- **c704**＝「似た人を見た話は、この動画のコメント欄にも、書かないでください。」をカット',
        '- **c706（最後の問い）**＝「この事件に関して、あなたが最も許せないことはなんですか。」（カズヤくんの字。行の途中の「？」は字幕の決まりで「。」に）＋これまでの回と同じ「よければ、コメントで教えてください。」',
        '- **締めの章 c701〜c705**＝「です・ます」をやめ、これまでの回と同じ言い切り（だ・である）に。です・ますは最後の問いのカットだけ',
        '- **語の補足**＝海・航空・建築など限られた業界の専門語だけに（一般に知られている語の補足を外した＝言いがかり c208・DNA c218・ひき逃げ c302 と c401・土地勘 c306・告訴 c403・逮捕状 c406・殺意 c409・時効 c410〜c411（聞き役の問いを「どんな意味？」に）・民事の裁判 c416・ドライブレコーダー c511・名誉毀損 c515・風化 c516）。残した補足＝重要指名手配 c310・捜査特別報奨金 c312・推定無罪 c406・「刑事の裁判とは別」c416',
        '- そのほか承認①は推奨どおり（題 A2・サムネ A・冒頭の引き「それでも、」・c405・SNS の声3件）。✅ **台本 OK**（2026-10-29 カズヤくん）',
    ]
    tail = ['', '## 関連',
            '- [[引き継ぎ-事故検証-27本目-20261029-④\'台本チェック]]・[[事故検証-27本目-①題材と年表-20261029]]・[[事故検証-状況整理-20260926]]']
    open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(head + body + tail).rstrip() + '\n')
    print('カット %d（🔧 %d）・本文 %s → %s' % (ncut, nfix, mmss(t * 60 / CPM), out))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else OUT))
