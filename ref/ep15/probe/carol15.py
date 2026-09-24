# -*- coding: utf-8 -*-
"""15本目②：CAROL の勧告10件の最終の分類と、往復書簡の最後を出す（md5 つき）。ドケットの目録の要約も。"""
import csv, glob, hashlib, io, json, os, re

SRC = r'C:/Users/konar/Desktop/zukai-engine/ref/ep15/src'
for f in sorted(glob.glob(SRC + '/ntsb_carol_sr_A-12-0*.json')):
    b = open(f, 'rb').read()
    d = json.loads(b.decode('utf-8'))
    look = {}
    for lk in d.get('Lookups', []):
        opts = lk.get('Options', [])
        if f.endswith('008.json') and lk.get('Column') == 'Status':
            print('   status option sample:', opts[:3])
        look[lk.get('Column')] = {str(next((o[k] for k in o if k.lower() in ('value', 'id', 'key', 'code')), '')): next((o[k] for k in o if k.lower() in ('text', 'name', 'label', 'description')), '') for o in opts}
    st = look.get('Status', {}).get(str(d.get('Status')), d.get('Status'))
    ad = d['Addressees'][0]
    ast = look.get('Status', {}).get(str(ad.get('Status')), ad.get('Status'))
    print('==', d['Srid'], d['OpenClosed'], (d.get('DateClosed') or '')[:10], '| status', st, '| addressee', ad.get('AddresseeName'), ast,
          '| md5', hashlib.md5(b).hexdigest(), len(b))
    print('   subject:', re.sub(r'\s+', ' ', d.get('Subject', ''))[:260])
    cs = sorted(ad.get('Correspondence', []), key=lambda c: (c.get('CorrespondenceDate') or c.get('LegacyDate') or ''))
    for c in cs:
        dt = (c.get('CorrespondenceDate') or c.get('LegacyDate') or '')[:10]
        txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', str(c.get('ResponseSummary') or '')))
        who = 'NTSB' if c.get('IsFromNtsb') else ad.get('AddressAcronym') or 'addressee'
        # NTSB の手紙は分類の語だけ拾う・最後の1通は長めに
        cls = re.findall(r'(?i)(?:open|closed)\s*[-—–]+\s*[a-z ]+?(?:response|action|alternate action|unacceptable action|superseded|no longer applicable|reconsidered)', txt)
        last = c is cs[-1]
        print('   -', dt, who, '|', ('; '.join(sorted(set(cls))) or '-'), '|', txt[:(700 if last else 160)])
print()
print('Status lookup:', look.get('Status'))

print('\n=== docket items')
rows = list(csv.reader(io.StringIO(open(SRC + '/ntsb_docket_items.tsv', encoding='utf-8').read()), delimiter='\t'))
hdr = [r for r in rows if r and r[0] == 'n'][0]
for r in rows:
    if not r or not r[0].isdigit():
        continue
    x = dict(zip(hdr, r))
    print('%2s p%-3s ph%-3s %-4s %-62s %s' % (x['n'], x['pages'], x['photos_in_docket'], 'DL' if x['local_file'] and os.path.exists(SRC + '/' + x['local_file']) else '--', x['title'][:62], x.get('note', '')[:90]))
