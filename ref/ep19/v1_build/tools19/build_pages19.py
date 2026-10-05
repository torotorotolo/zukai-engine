# -*- coding: utf-8 -*-
"""19本目の一次資料を「=== p<N> ===」区切りの通し頁ファイル1本にまとめる（check_facts.py・係・④' が引ける形）。
字は変えない（HTML は札を外して空白を詰めるだけ）。出力は git の外の ref/ep19/src/。

通し頁の割り当て（台本 §0 の表と同じ）
  TR 文字起こしの行 N        → p(1000+N)      AC 諮問委員会の PDF 頁 N → p(2000+N)
  GJ 大陪審の PDF 頁 N（OCR） → p(3000+N)
  MC18（Davis-Stirling の写しの OCR 層）→ p(4000+N)   MIN18（A11）→ p(4100+N)
  REC（A10）→ p(4200+N)      A09 転送メール（EST18＝p4318）→ p(4300+N)
  HTML：A04 5001・A05 5002・A06 5003・A07 5004・B08 5005・A12 5101・A13 5102・B03 5201・B04 5202・A16 5801
  B05 警察 5300+N・B06 広報誌 5400+N・B07 郡長のメモ 5500+N・B01 GAO 5600+N・B02 FEMA 5700+N
  A14 SB 4-D 6000+N・A17 最終命令 7000+N・A18 売却の命令 7100+N・A19 売却の告知 7200+N
  TF のコマの OCR（25秒おき・索引）→ p(9000+通し番号)
"""
import hashlib
import html as H
import json
import os
import re
import sys

import fitz

SRC = 'C:/Users/konar/Desktop/zukai-engine/ref/ep19/src'
S1 = ('C:/Users/konar/AppData/Local/Temp/claude/C--Users-konar-Documents-Obsidian-Vault/'
      '4cbe5283-d9a0-4fd2-8ebc-1295638da157/scratchpad')
OUT = SRC + '/ep19_pages.txt'
IDX = SRC + '/ep19_pages_index.json'

pages = []


def add(n, label, text):
    pages.append((n, label, text.strip()))


def pdf(path, base, label):
    d = fitz.open(path)
    for i, p in enumerate(d, 1):
        add(base + i, f'{label} PDF p.{i}', p.get_text())
    return len(d)


def html_text(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>|</tr>', '\n', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = H.unescape(s)
    s = re.sub(r'[ \t\r\f\v]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n', s)
    return s


counts = {}
# TR
n = 0
for line in open(SRC + '/nist_tf_transcript_2026-08-26.lines.txt', encoding='utf-8'):
    m = re.match(r'^(\d{4}) (.*)$', line.rstrip('\n'))
    if m:
        add(1000 + int(m.group(1)), f'TR{m.group(1)}', m.group(2))
        n += 1
counts['TR'] = n
counts['AC'] = pdf(SRC + '/nist_ncstac_2026-09_CTSupdate.pdf', 2000, 'AC')
# GJ（チャット1の Windows OCR）
cur, buf, gj = None, [], 0
for line in open(S1 + '/ep19_view/gj_ocr.txt', encoding='utf-8'):
    m = re.match(r'^## .*gj_p(\d+)\.png', line)
    if m:
        if cur is not None:
            add(3000 + cur, f'GJ PDF p.{cur}（OCR）', '\n'.join(buf))
            gj += 1
        cur, buf = int(m.group(1)), []
        continue
    m = re.match(r'^\[[\d,\- ]+\]\s?(.*)$', line.rstrip('\n'))
    if m and cur is not None:
        buf.append(m.group(1))
if cur is not None:
    add(3000 + cur, f'GJ PDF p.{cur}（OCR）', '\n'.join(buf))
    gj += 1
counts['GJ'] = gj
counts['MC18_DS'] = pdf(S1 + '/pages/ds_2018-report.pdf', 4000, 'MC18（Davis-Stirling の写し）')
counts['MIN18'] = pdf(SRC + '/surfside_cts_board_minutes_2018-11-15.pdf', 4100, 'A11 MIN18')
counts['REC'] = pdf(SRC + '/surfside_morabito_2021-06_unverified_inspection_report.pdf', 4200, 'A10 REC')
counts['A09'] = pdf(SRC + '/surfside_email_2018_structural_report.pdf', 4300, 'A09 転送メール')
for num, lab, fn in [(5001, 'A04 NIST 2026-06-22', 'nist_news_2026-06-22_technical_findings.html'),
                     (5002, 'A05 NIST 2026-09-28', 'nist_news_2026-09-28_ncst_updates.html'),
                     (5003, 'A06 NIST 2025-06', 'nist_news_2025-06_video_update.html'),
                     (5004, 'A07 NIST 2021-07-16', 'nist_news_2021-07-16_update.html'),
                     (5005, 'B08 NIST 2024-11-21', 'nist_news_2024-11-21_evidence_transfer_mdpd.html'),
                     (5101, 'A12 町の頁', 'surfside_cts_news_and_resources_page.html'),
                     (5102, 'A13 町 2026-08-13', 'surfside_news_2026-08-13_memorial_final_approval.html'),
                     (5201, 'B03 郡 2021-07-04', 'miamidade_2021-07-04_demolition_release_wayback-20210706.html'),
                     (5202, 'B04 郡 2022', 'miamidade_state-of-the-county-2022_tragedy-in-surfside.html'),
                     (5801, 'A16 州検事 2021-12-15', 'miamisao_2021-12-15_grandjury_statement.html')]:
    add(num, lab, html_text(SRC + '/' + fn))
counts['B05'] = pdf(SRC + '/surfside_police_bulletin_2021-07-08.pdf', 5300, 'B05 警察')
counts['B06'] = pdf(SRC + '/surfside_gazette_2021-08.pdf', 5400, 'B06 広報誌')
counts['B07'] = pdf(SRC + '/miamidade_2023-10-26_mayor_memo_termination_local_emergency.pdf', 5500, 'B07 郡長のメモ')
counts['B01'] = pdf(SRC + '/gao_2024-02-06_gao-24-106558_accessible.pdf', 5600, 'B01 GAO')
counts['B02'] = pdf(SRC + '/fema_2021-07-17_federal_response_fact_sheet_print-2026-10-05.pdf', 5700, 'B02 FEMA')
counts['A14'] = pdf(SRC + '/fl_2022_SB4D_enrolled_ch2022-269.pdf', 6000, 'A14 SB 4-D')
counts['A17'] = pdf(SRC + '/court_cts_2022-06_final_order_and_judgment.pdf', 7000, 'A17 最終命令')
counts['A18'] = pdf(SRC + '/court_cts_2022-06-01_order_authorizing_sale.pdf', 7100, 'A18 売却の命令')
counts['A19'] = pdf(SRC + '/court_cts_2022-07_receiver_sale_notice.pdf', 7200, 'A19 売却の告知')
# TF のコマの OCR（索引）
k, cur, buf = 0, None, []
for line in open(SRC + '/tf_slides_ocr_2026-10-05.txt', encoding='utf-8', errors='replace'):
    m = re.match(r'^## (t\d+\.jpg)', line)
    if m:
        if cur:
            k += 1
            add(9000 + k, f'TF のコマ {cur}（OCR・索引）', ''.join(buf))
        cur, buf = m.group(1), []
        continue
    if cur:
        buf.append(line)
if cur:
    k += 1
    add(9000 + k, f'TF のコマ {cur}（OCR・索引）', ''.join(buf))
counts['TF'] = k
# 頁の画像で読んだ書き起こし（OCR／文字の層が崩れた決め所と数字の段）→ p98xx（チャット2・2026-10-06）
VER = SRC + '/ep19_verified_2026-10-06.txt'
vcur, vlab, vbuf, nv = None, None, [], 0
for line in open(VER, encoding='utf-8'):
    m = re.match(r'^## p(98\d\d)\s+(.*)$', line)
    if m:
        if vcur:
            add(vcur, vlab, ''.join(vbuf).strip())
            nv += 1
        vcur, vlab, vbuf = int(m.group(1)), m.group(2).strip(), []
        continue
    if vcur and not line.startswith('#'):
        vbuf.append(line)
if vcur:
    add(vcur, vlab, ''.join(vbuf).strip())
    nv += 1
counts['VER'] = nv

nums = [p[0] for p in pages]
assert len(nums) == len(set(nums)), '頁番号が重なった'
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    for num, lab, text in pages:
        f.write(f'=== p{num} ===\n［{lab}］\n{text}\n')
idx = {str(num): lab for num, lab, _ in pages}
json.dump({'counts': counts, 'labels': idx}, open(IDX, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
b = open(OUT, 'rb').read()
print('pages', len(pages), 'bytes', len(b), 'md5', hashlib.md5(b).hexdigest())
print(json.dumps(counts, ensure_ascii=False))
empty = [lab for num, lab, t in pages if not t and not lab.startswith('TF')]
print('空の頁（TF 以外）', len(empty), empty[:12])
