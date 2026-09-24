# -*- coding: utf-8 -*-
"""15本目③：章立て案を check_script.est_sec と同じ式で秒に直す（道具は読むだけ・直さない）。"""
import sys
sys.path.insert(0, r'C:/Users/konar/Desktop/zukai-engine/tools')
import check_script as cs  # noqa: E402

# 章, 中身, カット, 行, 本文字数, 決め所, 扉
CH = [
    ('c1', '引き（9秒・観客席・外れたのは最大Gの3秒あと）', 12, 27, 660, 1, 0),
    ('c2', 'その日のステッド（コース・観客席までの距離＝図1・図3）', 20, 45, 1160, 1, 1),
    ('c3', '9秒（時系列の表・図5〜10・17.3G・1秒未満の意識）', 24, 54, 1392, 3, 1),
    ('c4', '1944年生まれのレーサー（来歴・Miss Candace・保管・2009年）', 20, 45, 1160, 1, 1),
    ('c5', '図面の無い改造（図2・おもり2倍・タブ1枚・しわ）', 24, 54, 1392, 2, 1),
    ('c6', '書類（飛行制限・3時間と23分・no・59・2,700時間）', 24, 54, 1392, 3, 1),
    ('c7', '26年前のナット（ねじが短すぎる・図13・14・疲労・フラッター）', 26, 59, 1508, 2, 1),
    ('c8', '観客席の62分（10人・64人以上・想定23人・幕・500と1,000フィート）', 22, 50, 1276, 2, 1),
    ('c9', 'その後（公聴会・勧告10件・コースを北へ）＋問い＋共通エンディング', 20, 45, 1150, 1, 1),
]

print('CPS', cs.CPS_FALLBACK, 'GAP', cs.GAP, 'LEAD+TAIL', cs.LEAD + cs.TAIL, 'Q', cs.TAIL_EXTRA_QUOTE, 'CARD', cs.CARD_SEC, 'PER_CUT', cs.PER_CUT)
tot = [0] * 5
cum = 0.0
print('| 章 | カット | 行 | 字 | 決め所 | 扉 | 秒 | 累計 |')
for c, what, n, ln, ch, q, card in CH:
    s = cs.est_sec(ch, ln, n, q, cs.CPS_FALLBACK, card)
    cum += s
    for i, v in enumerate((n, ln, ch, q, card)):
        tot[i] += v
    print('| %s | %d | %d | %d | %d | %d | %.1f | %d:%02d |' % (c, n, ln, ch, q, card, s, int(cum // 60), int(cum % 60)))
n, ln, ch, q, card = tot
S = cs.est_sec(ch, ln, n, q, cs.CPS_FALLBACK, card)
print('計 カット %d 行 %d 字 %d 決め所 %d 扉 %d → %.1f 秒 = %d分%02d秒' % (n, ln, ch, q, card, S, int(S // 60), int(S % 60)))
print('字数の上限 600+58×カット =', 600 + 58 * n, ' 余り', 600 + 58 * n - ch)
print('①カット×PER_CUT = %.1f 秒 ／ ②字数÷5 = %.1f 秒 ／ ②−① = %.1f 秒（≦120）' % (n * cs.PER_CUT, ch / 5, ch / 5 - n * cs.PER_CUT))
for f in (0.93, 1.07):
    s2 = cs.est_sec(ch, ln, n, q, cs.CPS_FALLBACK * f, card)
    print('話速 ×%.2f → %.1f 秒 = %d分%02d秒 dur_ok=%s' % (f, s2, int(s2 // 60), int(s2 % 60), cs.dur_ok(s2)))
print('写真・映像の下限 20% =', -(-n * 20 // 100), 'カット（PHOTO_LO=%s）' % cs.PHOTO_LO)
