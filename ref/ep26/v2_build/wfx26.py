# -*- coding: utf-8 -*-
"""26本目④'：Workflow の記録（journal.jsonl）から、係の返した結果をファイルへ取り出す（親の文脈に全文を流さないため）。

  python -P ref/ep26/v2_build/wfx26.py <journal.jsonl> check     # 照合の係 → findings_Gn.json・check_Gn.md
  python -P ref/ep26/v2_build/wfx26.py <journal.jsonl> fix       # 直す係 → fix_Gn.json（返りの "fix" の中身）・fixnote_Gn.md
  python -P ref/ep26/v2_build/wfx26.py <journal.jsonl> review    # 当て直しの係 → review_Rn.json・check_Rn.md

ラベル（check:G3・fix:G3・review:R1）で係を決める。結果は {"result": {...}} に包まれていることがある（④ の落とし穴）。
出すのは件数だけ（中身は出さない）。書いたファイルには名前の網（namecheck26.py）を必ずあとで当てる。
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def unwrap(v):
    for _ in range(4):
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except Exception:
                return v
        if isinstance(v, dict) and 'result' in v and len(v) <= 3 and isinstance(v['result'], (dict, str)):
            v = v['result']
        else:
            break
    return v


def entries(path):
    label, out = {}, []
    for ln in open(path, encoding='utf-8'):
        try:
            d = json.loads(ln)
        except Exception:
            continue
        if d.get('type') == 'started':
            label[d.get('key')] = d.get('label')
        elif d.get('key') in label and d.get('type') != 'started':
            for k in ('result', 'value', 'output', 'return'):
                if k in d:
                    out.append((label[d['key']], d.get('type'), unwrap(d[k])))
                    break
    return out


def main(path, kind):
    n = 0
    for lab, typ, r in entries(path):
        if not lab or not lab.startswith(kind + ':') or not isinstance(r, dict):
            continue
        g = lab.split(':', 1)[1]
        if kind == 'check':
            fs = r.get('findings') or []
            json.dump(fs, open(os.path.join(HERE, 'findings_%s.json' % g), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            md = ['# ④\' 原文照合の係 %s（26本目・2026-10-27・Workflow の返りを wfx26.py が書き出した）' % g, '',
                  '- 当てた頁＝%s' % (r.get('pages_checked') or '（record の頭を見る）'),
                  '- 所見＝[findings_%s.json](findings_%s.json)（%d件）' % (g, g, len(fs)), '',
                  r.get('record_md') or '', '', '## 親へ', '', r.get('notes_for_parent') or '—', '']
            open(os.path.join(HERE, 'check_%s.md' % g), 'w', encoding='utf-8', newline='\n').write('\n'.join(md))
            sev = {}
            for f in fs:
                sev[f.get('sev')] = sev.get(f.get('sev'), 0) + 1
            print('%s: 所見 %d %s・記録 %d字' % (g, len(fs), sev, len(r.get('record_md') or '')))
        elif kind == 'fix':
            fx = r.get('fix') if isinstance(r.get('fix'), dict) else None
            if fx is None and isinstance(r.get('fix_json'), str):
                fx = json.loads(r['fix_json'])
            json.dump(fx or {}, open(os.path.join(HERE, 'fix_%s.json' % g), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            open(os.path.join(HERE, 'fixnote_%s.md' % g), 'w', encoding='utf-8', newline='\n').write(
                '# ④\' 直す係 %s の報告（wfx26.py が書き出した）\n\n%s\n' % (g, r.get('report') or ''))
            print('%s: 扱い %d・_extra %d' % (g, len([k for k in (fx or {}) if k != '_extra']), len((fx or {}).get('_extra', []))))
        elif kind == 'review':
            fs = r.get('findings') or []
            json.dump(fs, open(os.path.join(HERE, 'review_%s.json' % g), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            open(os.path.join(HERE, 'check_%s.md' % g), 'w', encoding='utf-8', newline='\n').write(
                '# ④\' 当て直しの係 %s（wfx26.py が書き出した）\n\n%s\n\n## 親へ\n\n%s\n' % (g, r.get('record_md') or '', r.get('notes_for_parent') or '—'))
            print('%s: 所見 %d' % (g, len(fs)))
        n += 1
    print('書き出した係 %d' % n)
    return 0 if n else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
