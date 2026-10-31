# -*- coding: utf-8 -*-
"""28本目 check_facts に当てる「原文の片」のファイルを組む（④・2026-11-01・27本目の news_frag.txt と同じ形）。

  python ref/ep28/v1_build/frag28.py        # → ref/ep28/src/news_frag.txt（git の外）

片の出どころ＝係の記録（src/agents/wf28/A.md・B.md＝WebFetch・pypdf・e-Gov API で頁から抜いた字）と sources.md（② で一次資料に当てた字）。
バッククォートで囲んだ字だけを取る（「」の要約は取らない）。1ファイル＝1頁（=== pN ===）。
⚠️ この照合は「台本の3桁以上の数が、原文の片のどこかにあるか」まで。言い換えの強さと帰属は人と係が見る（ルール 4'-12）。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
EP = r'C:\Users\konar\Desktop\zukai-engine\ref\ep28'
SRC = [('係A の記録（c101〜c423 の原文の片）', os.path.join(EP, 'src', 'agents', 'wf28', 'A.md')),
       ('係B の記録（c501〜c706 の原文の片）', os.path.join(EP, 'src', 'agents', 'wf28', 'B.md')),
       ('sources.md（② で一次資料に当てた片）', os.path.join(EP, 'sources.md'))]
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
        for i, (name, path) in enumerate(SRC, 1):
            fr = frags(path)
            n += len(fr)
            f.write('=== p%d ===\n# %s\n' % (i, name))
            for s in fr:
                f.write(s + '\n')
            print('p%d %s: %d片' % (i, name, len(fr)))
    print('計 %d片 → %s' % (n, OUT))
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
