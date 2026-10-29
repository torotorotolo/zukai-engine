# -*- coding: utf-8 -*-
"""27本目 映像方針（2026-10-29・チャット5）：説明カットの「地の写真の暗さ」と「SNS の注釈」の見本を作る（カズヤくんが選ぶための静止画・本番の描き手ではない）。
配置は本番に合わせた：字幕の帯 y900〜1080（真っ黒）・左右の余白72・出典の行 y≈872（左下）・地の写真の出典 y≈196・章の印は右上・
右下の透かし（1920換算 x≥1768・y≥905）を避ける。字＝ch の Noto Sans JP（fonts/*.woff2）。写真は色を変えず明るさだけ下げる（掛け算）。

  python -I ref/ep27/eizou_build/mock27.py fig <写真> <明るさ 0〜1> <出力.png>
  python -I ref/ep27/eizou_build/mock27.py sns <写真> <明るさ 0〜1> <出力.png>
出力の横に、字の周りの地との明るさの比（コントラスト比・4.5:1 以上が目安＝ルール §5b-6d）と、地の写真の平均の明るさを出す。
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
FONT = os.path.join(REPO, 'fonts')
W, H = 1920, 1080
INK_W, LINE, ACC = (234, 242, 246), (143, 182, 201), (232, 163, 61)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT, name), size)


def cover(path, k):
    im = Image.open(path).convert('RGB')
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))
    return im.point(lambda v: round(v * k))          # 色はそのまま・明るさだけ下げる


def lum(rgb):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def box_lum(im, box):
    """箱の中の地の明るさ（上位10%の明るい画素の平均＝字にいちばん厳しい所）"""
    px = sorted(lum(p) for p in im.crop(box).resize((64, 32)).getdata())
    top = px[int(len(px) * 0.9):]
    return sum(top) / len(top)


def chrome(d, chapter, title, sub, credit_photo, credit, narr):
    # 章の印（右上）
    f = font('NotoSansJP-Medium.woff2', 26)
    w = d.textlength(chapter, font=f)
    d.rounded_rectangle([1848 - w - 28, 44, 1848, 92], 10, outline=LINE, width=2)
    d.text((1848 - w - 14, 50), chapter, font=f, fill=LINE)
    # 見出しと副題（左上）
    d.text((72, 52), title, font=font('NotoSansJP-Black.woff2', 66), fill=INK_W)
    d.text((74, 140), sub, font=font('NotoSansJP-Medium.woff2', 34), fill=LINE)
    # 地の写真の出典（本体枠の上・CRED_BACK_Y＝196）
    d.text((632, 196), credit_photo, font=font('NotoSansJP-Medium.woff2', 22), fill=(205, 214, 220))
    # 出典の行（左下・CRED_Y＝872）
    d.text((72, 858), credit, font=font('NotoSansJP-Medium.woff2', 24), fill=(215, 224, 230))
    # 字幕の帯（真っ黒・y900〜1080）
    d.rectangle([0, 900, W, H], fill=(0, 0, 0))
    fs = font('NotoSansJP-Bold.woff2', 52)
    for i, line in enumerate(narr):
        lw = d.textlength(line, font=fs)
        d.text(((W - lw) / 2, 930 + i * 70), line, font=fs, fill=(255, 255, 255))


def fig(im, d):
    """c405（2つの疑い＝地 CM254）の形を借りた見本"""
    chrome(d, '第3章　ひき逃げから殺人へ', '2つの疑い', '2025年6月2日　逮捕状', '地の写真：（撮影者名）／CC BY 2.0／改変：明るさ',
           '出典：OAB大分朝日放送（2025年6月2日）・テレビ大分（2025年6月3日）', ['殺人は亡くなった大学生、殺人未遂は',
                                                                       'けがをした友人に対する疑いだ。'])
    fh, fb = font('NotoSansJP-Black.woff2', 54), font('NotoSansJP-Bold.woff2', 44)
    boxes = []
    for i, (head, body, col) in enumerate([('殺人の疑い', '亡くなった大学生', ACC), ('殺人未遂の疑い', 'けがをした友人', LINE)]):
        x0 = 150 + i * 840
        d.rounded_rectangle([x0, 330, x0 + 780, 700], 18, outline=col, width=6)
        d.text((x0 + 48, 372), head, font=fh, fill=col)
        d.line([x0 + 48, 470, x0 + 732, 470], fill=col, width=3)
        d.text((x0 + 48, 520), '→ ' + body, font=fb, fill=INK_W)
        boxes += [(x0 + 48, 372, x0 + 520, 440), (x0 + 48, 520, x0 + 620, 580)]
    return boxes + [(72, 52, 72 + 360, 132), (632, 196, 1300, 222), (72, 858, 1100, 888)]


def sns(im, d):
    chrome(d, '第4章　1万3978件', 'SNS の声', 'X の投稿から（原文どおり）', '地の写真：（撮影者名）／CC BY 2.0／改変：明るさ',
           '出典：X の投稿（2026年10月29日）', ['SNS上では、「なんか八田與一にめっちゃ似てる人と', 'すれ違ったんだけどたぶん違う」、'])
    d.rounded_rectangle([300, 300, 1620, 640], 24, fill=(245, 246, 247))
    fq = font('NotoSansJP-Bold.woff2', 50)
    for i, line in enumerate(['なんか八田與一にめっちゃ似てる人と', 'すれ違ったんだけどたぶん違う']):
        d.text((360, 352 + i * 80), line, font=fq, fill=(20, 24, 28))
    d.text((360, 560), 'X の投稿（2026年10月29日）', font=font('NotoSansJP-Medium.woff2', 30), fill=(100, 110, 118))
    # 🔴 注釈（右・字幕の帯の上・透かし x≥1768,y≥905 と左下の出典の行と右上の章の印を避ける）
    note = '※SNS の投稿です。事実かどうかは確かめられていません'
    fn = font('NotoSansJP-Bold.woff2', 30)
    nw = d.textlength(note, font=fn)
    x0 = 1848 - nw - 24
    d.rounded_rectangle([x0, 808, 1848, 856], 10, fill=(0, 0, 0))
    d.text((x0 + 12, 812), note, font=fn, fill=(255, 214, 102))
    return [(x0, 808, 1848, 856), (72, 52, 400, 132), (632, 196, 1300, 222), (72, 858, 700, 888)]


def main():
    mode, photo, k, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    bg = cover(photo, k)
    im = bg.copy()
    d = ImageDraw.Draw(im)
    boxes = fig(im, d) if mode == 'fig' else sns(im, d)
    im.save(out)
    L_text = lum(INK_W)
    worst = min((L_text + 0.05) / (box_lum(bg, b) + 0.05) for b in boxes)
    mean = sum(lum(p) for p in bg.crop((0, 0, W, 900)).resize((96, 45)).getdata()) / (96 * 45)
    print('%s 明るさ×%.2f：字と地のコントラスト比（いちばん厳しい所）%.1f:1・地の平均の明るさ %.3f → %s' % (mode, k, worst, mean, out))


if __name__ == '__main__':
    main()
