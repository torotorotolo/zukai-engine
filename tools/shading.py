# -*- coding: utf-8 -*-
"""まちがい探し喫茶：陰影・質感の共通部品。

参考にした水準（ClaudeCode+Remotion 製の日本史アニメ・2026-07-24）から抜き出した、
「平塗りのクリップアート」と「作品」を分ける4点をここに実装する。

  1. **平塗りをやめる** … すべての面に放射/線形グラデーションを敷く
  2. **地紋を敷く** … 無地の色面を残さない（木目・布目・和紙の粒）
  3. **光の落ち方** … 画面周辺を落とす（周辺減光）／艶（ハイライト）を必ず1つ入れる
  4. **線を機械的にしない** … 微小な揺らぎフィルタで手描きの気配を出す

グラデーションの id は「色と役割のハッシュ」にする。
同じ色・同じ役割なら A面/B面で共有され、色ちがいの変異が起きた瞬間に別 id になるので、
定義の衝突（先勝ちで色が戻ってしまう事故）が起きない。
"""
import hashlib

from palette import shade


def gid(*parts) -> str:
    return "g" + hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:10]


def sphere(col, hi=0.52, lo=-0.30, cx="34%", cy="26%", r="82%"):
    """球・丸い食べもの用の放射グラデーション。"""
    i = gid("sph", col, hi, lo, cx, cy, r)
    return i, (f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}">'
               f'<stop offset="0%" stop-color="{shade(col, hi)}"/>'
               f'<stop offset="52%" stop-color="{col}"/>'
               f'<stop offset="100%" stop-color="{shade(col, lo)}"/></radialGradient>')


def dish(col):
    """陶器用。中心はやや沈み、縁が明るく立ち上がる。"""
    i = gid("dish", col)
    return i, (f'<radialGradient id="{i}" cx="38%" cy="30%" r="86%">'
               f'<stop offset="0%" stop-color="{shade(col, 0.55)}"/>'
               f'<stop offset="62%" stop-color="{col}"/>'
               f'<stop offset="88%" stop-color="{shade(col, -0.12)}"/>'
               f'<stop offset="100%" stop-color="{shade(col, -0.26)}"/></radialGradient>')


def slope(col, a=0.26, b=-0.26, x2="55%", y2="100%"):
    """平たいもの用の線形グラデーション（左上が明るい）。"""
    i = gid("slp", col, a, b, x2, y2)
    return i, (f'<linearGradient id="{i}" x1="0%" y1="0%" x2="{x2}" y2="{y2}">'
               f'<stop offset="0%" stop-color="{shade(col, a)}"/>'
               f'<stop offset="100%" stop-color="{shade(col, b)}"/></linearGradient>')


def metal(col):
    """金属用。明暗の帯を重ねると一気に金属に見える。"""
    i = gid("met", col)
    return i, (f'<linearGradient id="{i}" x1="0%" y1="0%" x2="100%" y2="14%">'
               f'<stop offset="0%" stop-color="{shade(col, -0.30)}"/>'
               f'<stop offset="20%" stop-color="{shade(col, 0.62)}"/>'
               f'<stop offset="42%" stop-color="{col}"/>'
               f'<stop offset="62%" stop-color="{shade(col, 0.40)}"/>'
               f'<stop offset="84%" stop-color="{shade(col, -0.18)}"/>'
               f'<stop offset="100%" stop-color="{shade(col, -0.34)}"/></linearGradient>')


def glassy(col):
    """ガラス・液体用。上から下へ透明感が増す。"""
    i = gid("gls", col)
    return i, (f'<linearGradient id="{i}" x1="10%" y1="0%" x2="70%" y2="100%">'
               f'<stop offset="0%" stop-color="{shade(col, 0.62)}"/>'
               f'<stop offset="46%" stop-color="{col}"/>'
               f'<stop offset="100%" stop-color="{shade(col, -0.22)}"/></linearGradient>')


def gloss(cx, cy, rx, ry, rot=-28, op=0.55):
    """艶。1つ入れるだけで「描いてある」感じが出る。"""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#ffffff" '
            f'opacity="{op}" transform="rotate({rot} {cx} {cy})"/>')


# ── 画面全体にかける質感 ───────────────────────────────────────────

def scene_defs(w, h, warm="#5a3d1e"):
    """地紋（和紙の粒）・周辺減光・落ち影・手描きの揺らぎ。シーンの先頭に置く。"""
    return f'''<defs>
      <filter id="grain" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" seed="5"/>
        <feColorMatrix type="saturate" values="0"/>
      </filter>
      <filter id="rough" x="-8%" y="-8%" width="116%" height="116%">
        <feTurbulence type="fractalNoise" baseFrequency="0.016" numOctaves="2" seed="9" result="n"/>
        <feDisplacementMap in="SourceGraphic" in2="n" scale="2.4"
                           xChannelSelector="R" yChannelSelector="G"/>
      </filter>
      <filter id="drop" x="-30%" y="-30%" width="170%" height="170%">
        <feDropShadow dx="4" dy="9" stdDeviation="8" flood-color="#2c2114" flood-opacity="0.30"/>
        <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#2c2114" flood-opacity="0.22"/>
      </filter>
      <radialGradient id="vig" cx="46%" cy="34%" r="78%">
        <stop offset="0%" stop-color="#ffffff" stop-opacity="0.16"/>
        <stop offset="58%" stop-color="#ffffff" stop-opacity="0"/>
        <stop offset="100%" stop-color="{warm}" stop-opacity="0.34"/>
      </radialGradient>
    </defs>'''


def overlay(w, h):
    """地紋と周辺減光。すべてのプロップの上に重ねる（最後に描く）。"""
    return (f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity="0.10"/>'
            f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
