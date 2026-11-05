# -*- coding: utf-8 -*-
"""30本目④'：親の差し替え（patches_base.json）・直す係（src/agents/wf30c/fix_F*.json）・当て直しと点検の直し（patches_r.json）・§ の直し（patches_sec.json）を
1本の差し替え表 patches30.json へまとめ、聞き役の役割表 roles_map.json を更新する（数を必ず突き合わせる＝26本目の教訓）。

  python -P ref/ep30/v2_build/merge30.py

- 順番＝base → F1〜F6 → r → sec（後ろの差し替えの old は前の差し替えのあとの字）。id の重なりは止める。
- role＝質問・なし は役割表から外す／まとめ・反応 は役割表に入れる。もとの役割表は roles_map_v1.json に残す（無ければ今の roles_map.json を写す）。
- 読み＝fix_F*.json の yomi を、§6 の表の末尾に足す差し替えを1本作る（同じ語は1行に）。
- 出すのは数だけ。終了コード 0＝組めた／1＝id の重なりか形の誤り。
"""
import glob
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
AG = os.path.join(EP, 'src', 'agents', 'wf30c')


def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []


def main():
    base = load('patches_base.json')
    fixes = []
    yomi = {}
    per = {}
    for p in sorted(glob.glob(os.path.join(AG, 'fix_F*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        ps = d.get('patches') or []
        per[os.path.basename(p)[4:6]] = len(ps)
        fixes += ps
        for y in d.get('yomi') or []:
            w = y['word'].strip()
            if w in yomi:
                yomi[w]['cuts'] = yomi[w]['cuts'] + '・' + y['cuts']
            else:
                yomi[w] = dict(y)
    rs = load('patches_r.json')
    sec = load('patches_sec.json') + load('patches_sec_num.json')
    yrows = load('yomi_extra.json')
    yfrom = []
    for y in yrows:                      # 親の表＝同じ語は親の行で上書き（どこの欄を直すため）
        yomi[y['word'].strip()] = y
        yfrom += y.get('from') or []
    for w in load('yomi_drop.json'):     # 親が落とした行（語りから外れた語・読みが割れない語・同じ行の重なり）
        yomi.pop(w, None)
    ypatch = []
    if yomi:
        rows = '\n'.join('| %s | %s | %s |' % (y['word'], y['reading'], y['cuts']) for y in yomi.values())
        anchor = '| 5,800人・1,364人・約1万1千人・約2,500人 | 数字は先回りしてかなで固定（記憶 feedback-tts-misreads-are-positional） | c105・c209・c822・c917・ca01 |'
        ypatch = [{'id': 'S-YOMI', 'cut': '§', 'old': anchor, 'new': anchor + '\n' + rows, 'why': "④' の係の読みの所見をまとめて足した", 'from': yfrom}]
    all_p = base + fixes + rs + sec + ypatch
    ids = [p.get('id') for p in all_p]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        print('🔴 id の重なり', dup)
        return 1
    for p in all_p:
        if not p.get('move_after') and ('old' not in p or 'new' not in p):
            print('🔴 形の誤り', p.get('id'))
            return 1
    json.dump(all_p, open(os.path.join(HERE, 'patches30.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    rp = os.path.join(HERE, 'roles_map.json')
    r1 = os.path.join(HERE, 'roles_map_v1.json')
    if not os.path.exists(r1):
        shutil.copy(rp, r1)
    rmap = json.load(open(r1, encoding='utf-8'))
    n_role = 0
    for p in all_p:
        if p.get('role'):
            n_role += 1
            if p['role'] in ('質問', 'なし'):
                rmap.pop(p['cut'], None)
            else:
                rmap[p['cut']] = p['role']
    json.dump(rmap, open(rp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('差し替え %d＝親 %d・直す係 %s=%d・当て直しと点検 %d・§ %d・読み %d行（%d本）' % (
        len(all_p), len(base), per, len(fixes), len(rs), len(sec), len(yomi), len(ypatch)))
    print('役割の変更 %d件・役割表 %d件（第1版 %d件）' % (n_role, len(rmap), len(json.load(open(r1, encoding='utf-8')))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
