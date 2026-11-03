# -*- coding: utf-8 -*-
"""29本目 check_facts に当てる「原文の片」のファイルを組む（④・2026-11-03・28本目の frag28.py を写した）。

  python ref/ep29/v1_build/frag29.py        # → ref/ep29/src/news_frag.txt（git の外）

片の出どころ＝係の記録（src/agents/wf29/A.md・B.md＝頁から抜いた字）と sources.md（② で一次資料に当てた字）と、
🆕 字幕の文字（src/kaiken_subs_transcript.txt・qa_subs_ntv_early.txt・qa_subs_ntv_late.txt＝丸ごと1頁・自動生成＝語の字は崩れる）。
片のファイルはバッククォートで囲んだ字だけを取る（「」の要約は取らない）。1ファイル＝1頁（=== pN ===）。無いファイルは飛ばして言う。
⚠️ この照合は「台本の3桁以上の数が、原文の片のどこかにあるか」まで。言い換えの強さと帰属は人と係が見る（ルール 4'-12）。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
EP = r'C:\Users\konar\Desktop\zukai-engine\ref\ep29'
SRC = [('係A の記録（c101〜c420 の原文の片）', os.path.join(EP, 'src', 'agents', 'wf29', 'A.md')),
       ('係B の記録（c501〜c706 の原文の片）', os.path.join(EP, 'src', 'agents', 'wf29', 'B.md')),
       ('sources.md（② で一次資料に当てた片）', os.path.join(EP, 'sources.md'))]
WHOLE = [('説明会の字幕（第1部・第2部）', os.path.join(EP, 'src', 'kaiken_subs_transcript.txt')),
         ('質疑の字幕（前半）', os.path.join(EP, 'src', 'qa_subs_ntv_early.txt')),
         ('質疑の字幕（後半）', os.path.join(EP, 'src', 'qa_subs_ntv_late.txt'))]
OUT = os.path.join(EP, 'src', 'news_frag.txt')
TICK = re.compile(r'`([^`\n]*)`')   # 長さで絞らない（{2,} にすると1字の片を飛ばして閉じと次の開きを組にする＝selftest で見つけた）


def frags(path):
    seen, out = set(), []
    for m in TICK.finditer(open(path, encoding='utf-8').read()):
        s = m.group(1).strip()
        if 2 <= len(s) <= 200 and s not in seen:
            seen.add(s)
            out.append(s)
    return out


def main():
    n = 0
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        page = 0
        for name, path in SRC:
            if not os.path.exists(path):
                print('（無い）%s: %s' % (name, path))
                continue
            page += 1
            fr = frags(path)
            n += len(fr)
            f.write('=== p%d ===\n# %s\n' % (page, name))
            for s in fr:
                f.write(s + '\n')
            print('p%d %s: %d片' % (page, name, len(fr)))
        for name, path in WHOLE:
            page += 1
            f.write('=== p%d ===\n# %s\n' % (page, name))
            f.write(open(path, encoding='utf-8').read())
            print('p%d %s: 丸ごと' % (page, name))
    print('計 %d片＋字幕3本 → %s' % (n, OUT))
    return 0


def selftest():
    import tempfile
    t = tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8')
    t.write('a `6,628,007件` b `x` c `6,628,007件` 「要約」 `1,464,800件`\n')
    t.close()
    ok = frags(t.name) == ['6,628,007件', '1,464,800件']
    os.unlink(t.name)
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(selftest() if '--selftest' in sys.argv else main())
