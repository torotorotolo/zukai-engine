# -*- coding: utf-8 -*-
"""23本目④'：書かない名前の網（リポは公開＝私人・経営者・公務員・設計者・構造技術者の名前を、リポに入るファイルに書かない）。

  python ref/ep23/v2_build/namecheck23.py <ファイル> [<ファイル> …] [--show]

網は2つ：
 1. 一覧＝Vault の棚卸しノート（git の外）の「## 2. 名前」の表（v1_build/m23.py の load_names と同じ読み方）＝当たれば E。
 2. 原文から拾う候補＝国会の記録 K6 と判決3本の文字の層で、役職の語（회장・사장・이사・차장・부장・과장・대리・소장・반장・
    주임・기사・기술사・구청장・국장・계장・대표・실장・교수・피고인）のすぐ後ろにある、ハングル2〜3字の語＝当たれば「要確認」（W）。
    役職の語の後ろには名前でない語も来る（「사장 등」など）ので、要確認の中身は人が見る（--show で行を出す）。
当たった所は名前を伏せて「ファイル:行・語の頭1字＋○」だけ出す（この出力も gates.md に入る＝リポに名前を写さない）。
終了コード 0=一覧の名前0 / 1=一覧の名前あり / 2=一覧が読めない（fail closed）
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(EP, 'v1_build'))
import m23                          # noqa: E402  load_names を使う

NAMES = r'C:/Users/konar/Documents/Obsidian Vault/Projects/事故検証-23本目-旧版の棚卸し-ノート-20261017.md'
SRC = r'C:\Users\konar\Desktop\zukai-engine\ref\ep10\src'
SRCS = ['assembly_sampoong_tokui_no6_19950912_id19114.txt', 'lawgokr_prec114109_96do1231.txt',
        'lawgokr_prec79152_98da29797.txt', 'casenote_seoulhigh_96no118_visible.txt']
TITLE = r'(?:회장|사장|이사|차장|부장|과장|대리|소장|반장|주임|기사|기술사|구청장|국장|계장|대표|실장|교수|피고인)'
AFTER = re.compile(TITLE + r'\s*([가-힣]{2,3})(?=[\s,)(·등은는이가의에]|$)')
# 役職の語のすぐ後ろに来る、名前でない語（拾った候補から除く）
STOP = {'등', '등은', '등의', '으로', '에게', '이며', '이고', '과장', '부장', '사장', '회장', '이사', '대리', '차장', '소장', '반장',
        '주임', '대표', '실장', '국장', '계장', '교수', '이었', '였던', '으로서', '에서', '이던', '이었던', '겸', '직무', '직무대',
        '외', '외의', '및', '또는', '단', '보고', '도착', '지시', '확인', '방문', '현장', '등과', '등에', '회의', '에게서', '들은',
        '들이', '들의', '이었던', '인', '인데', '으로부터', '로부터', '과는', '과의', '은', '는', '이', '가', '의'}


SURNAME = set('김이박최정강조윤장임한오서신권황안송류유전홍고문양손배백허남심노하곽성차주우구민진나지엄채원천방공현함변염여추도소석선설마길연위표명기반왕금옥육인맹제모탁국어은편용예경봉')
PARTICLE_END = set('에의을를이가은는로서과와도만')
STOP3 = {'전진단', '이사인', '임시협'}


def mined():
    """役職の語のすぐ後ろの、姓の字で始まるハングル3字（助詞で終わらない）＝名前の候補（2026-10-18 に拾った47語を見て絞った）。"""
    out = set()
    for f in SRCS:
        p = os.path.join(SRC, f)
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8', errors='replace').read()
        for m in AFTER.finditer(s):
            w = m.group(1)
            if w in STOP or w in STOP3 or len(w) != 3 or w[0] not in SURNAME or w[-1] in PARTICLE_END:
                continue
            out.add(w)
    return out


def mask(w):
    return w[0] + '○' * (len(w) - 1)


# 一覧の表の「名前」の欄に混じる、名前でない語（注・役の語）＝除く／欄の注の中にある名前＝足す（2026-10-18 ④'で一覧を見て決めた）
JUNK = {'漢字は「李鐏」「李㵒」「李準」と割れる＝原本で未確認', '慰霊塔の写真の撮影者', 'B＝会長」は推論', '画面は片仮名',
        '使っていない', '施設部次長', '施設部長'}
EXTRA = ['李鐏', '李㵒', '李準']


def main(files, show):
    names = [n for n in m23.load_names(NAMES) if n not in JUNK]
    names = sorted(set(names + EXTRA), key=len, reverse=True) if names else []
    if not names:
        print('🔴 名前の一覧が読めない（%s）＝測れていない' % NAMES)
        return 2
    cand = mined() - set(names)
    hits, maybe = [], []
    for f in files:
        if os.path.abspath(f) == os.path.abspath(__file__):
            continue
        for i, ln in enumerate(open(f, encoding='utf-8', errors='replace'), 1):
            for w in names:
                if w in ln:
                    hits.append('%s:%d  %s' % (os.path.basename(f), i, mask(w)))
            for w in cand:
                for m in re.finditer(re.escape(w), ln):
                    # 前後がハングルなら別の語の一部＝数えない
                    a, b = m.start(), m.end()
                    if (a > 0 and re.match(r'[가-힣]', ln[a - 1])) or (b < len(ln) and re.match(r'[가-힣]', ln[b]) and ln[b] not in '은는이가의등에께'):
                        continue
                    maybe.append((os.path.basename(f), i, w, ln.strip()))
    print('書かない名前（一覧 %d語）%d件／原文から拾った候補（%d語）の要確認 %d件（%dファイル）' % (
        len(names), len(hits), len(cand), len(maybe), len(files)))
    for h in hits:
        print('  ✗', h)
    for f, i, w, ln in maybe:
        print('  ？ %s:%d  %s' % (f, i, mask(w)))
        if show:
            print('     ', ln[:160])
    return 1 if hits else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    sys.exit(main([x for x in a if not x.startswith('--')], '--show' in a))
