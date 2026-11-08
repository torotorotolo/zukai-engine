# -*- coding: utf-8 -*-
"""31本目 ⑤b-4：札の字の記録（`tools/check_mech.py` の REC_M31）を、一次資料の字に機械で当てる（30本目 rec30_src.py を写した）。

  python -P ref/ep31/eizou_build/rec31_src.py [--skip]

なぜ要るか：門番 judge_m31 は「描く側の字＝記録の字」までしか見ない（Actions には資料が無い）。記録そのものが原文と合っているかはここで見る。
置き場＝抜き書きを作らず、資料そのもの（`ref/ep31/v1_build/quotes31.py` の DOCS と国会会議録の写し＝git の外の src/）。揃え方も quotes31（NFKC・空白と句読点と括弧を消す・小書きの「っ」を「つ」に）。
⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ・帰属）は人が見る。
⚠️ 片が「―」の行＝画面の字が資料の字でない（会議の日付＝会議録の番号から・時点の日付）＝当てない＝数だけ出す。町・会・画も当てない（quotes31 の NOCHECK）。
出すのは画面の字と記号だけ（資料の字は出さない＝名前を文脈に入れない）。
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'v1_build'))
import quotes31 as Q  # noqa: E402
from check_mech import REC_M31  # noqa: E402


def main():
    ok, skip, ng = 0, [], []
    for cid, rows in REC_M31['vals'].items():
        for r in rows:
            code, screen = r[0], r[1]
            frag = r[2] if len(r) > 2 else screen
            if code == '―' or frag == '―' or code in Q.NOCHECK:
                skip.append((cid, code, screen))
                continue
            doc = code if code in Q.DOCS else code   # 判・白・法・記 か 国<issueID>/<番号>
            for verdict, _part in Q.check_fragment(doc, frag):
                if verdict == 'OK':
                    ok += 1
                elif verdict in ('当てない', '短い'):
                    skip.append((cid, code, screen))
                else:
                    ng.append((cid, code, screen, verdict))
    print('当たった %d・当てない %d・🔴 無い %d' % (ok, len(skip), len(ng)))
    for x in ng:
        print('🔴', *x)
    if '--skip' in sys.argv:
        for x in skip:
            print('・', *x)
    return 1 if ng else 0


if __name__ == '__main__':
    sys.exit(main())
