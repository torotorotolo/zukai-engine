# -*- coding: utf-8 -*-
"""21本目④'：出典の欄の引用を資料の字に当てる＝v1_build/quotes21.py に「運輸省の監察総監の報告」（④'で取った一次）を足して回す。

  python ref/ep21/v2_build/quotes21v2.py ref/ep21/daihon_v2.md --out ref/ep21/v2_build/quotes21_v2.tsv

足した資料：運輸省の監察総監の報告 CC-2006-085（2006-08-31）＝ src/new/web5/dot_oig_cc2006085.txt（PDF の文字の層・git の外）
v1_build/quotes21.py は直さない（第1版の記録を変えない）。ここで資料の表と札の正規表現だけ足して、同じ判定で回す。
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'v1_build'))
import quotes21 as Q  # noqa: E402

Q.FLAT['運輸省の監察総監の報告'] = os.path.join('..', 'web5', 'dot_oig_cc2006085')
Q.TOK = re.compile(r'(?P<doc>委員会報告|図表|スタッフ声明|NTSB\s*(?:11|175|77|93)便|CVR|国立公園局|AP|法律|検視局|記念館'
                   r'|運輸省の監察総監の報告|監察総監|運輸長官の証言|NIST)'
                   r'|(?P<pg>p\.?\s*(?P<p1>[ivx]+|\d+)(?:\s*〜\s*p?\.?\s*(?P<p2>\d+))?)'
                   r'|`(?P<q>[^`]+)`')

if __name__ == '__main__':
    a = sys.argv[1:]
    out = a[a.index('--out') + 1] if '--out' in a else os.path.join(HERE, 'quotes21_v2.tsv')
    n = Q.main(a[0], out)
    sys.exit(1 if n else 0)
