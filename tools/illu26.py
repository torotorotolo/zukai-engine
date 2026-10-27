# -*- coding: utf-8 -*-
"""illu26.py — 案C の再現イラスト：26本目（タイタニック号沈没事故・1912-04-14〜15・北大西洋）の置き場 K1〜K9（⑤b-4・2026-10-27 新設）。

`tools/illu.py` の末尾で読み込み、型の表（FIELDS・CHOICES・VIEWS・REC_FIELDS・NOTE）と置き場の登録 `illu.EXTRA` へ足す（illu25 と同じ作り）。
🔴 置き場の名は **K1〜K6**（A〜E・A1〜A5・C1〜C7・N1〜N4・S1〜S7・RA〜RD・SA〜SD・VA〜VD・F1〜F6 と重ねない）。欄の名は頭に k（共有の表 CHOICES で前の回とぶつけない）。
🔴 §0b（題材を替えるとき）：このファイルは26本目の型の値そのもの＝次の回は読み込みを外すか、置き場の名がぶつからないか確かめる。

■ 置き場（映像方針 26本目 了承② 決め4・一覧 `ref/ep26/eizou_list26.md` の案C・台本 §4 の画の欄）
  K1 … カリフォルニアン号の船橋（横から・夜）＝一覧の案C-1・7・8・9 の4場面を1つの置き場で（同じ絵＝場面が替わっても置き場は替わらない＝
       門番 ㉑ の見る向きの合図は置き場の名の替わりで鳴る＝同じ船橋のつながり c625→c627・c632→c633 に意味の無い合図を出さない）
       案C-1（c606 東から近づく灯・三等航海士／c614 モールス灯に答えなし・二等航海士が上がってくる／c615 灯を指さして引き継ぐ）・
       案C-7（c618 双眼鏡の見習い・マストの灯と赤い舷灯と後ろの甲板の白い灯りの群れ／c625 モールス灯で呼ぶ・低く白い信号弾3発）・
       案C-8（c627 双眼鏡の2人／c632 灯りがだんだん消えていく）・案C-9（c633 伝声管の前の二等航海士・見えなくなった方角／c936 同じ）
  K2 … 海図室（c621 横になる船長・伝声管の口／c630 戸が開いて見習い／c631 船長が全部白かと時刻を聞く）
  K3 … カリフォルニアン号の無線室（c320 電鍵を打つ通信士／c506 寝台で眠る通信士・机の上のヘッドホン）
  K4 … タイタニック号のボート甲板（view deck＝c508 1号艇のそばの筒から信号弾・白い星／view wing＝c512 船橋の端の屋根の上のモールス灯）
  K5 … 1号艇の40の席と埋まった12（c701・上から・人の形で数を名乗らない＝席の印）
  K6 … カルパチア号・夜明け・2号艇を横に着ける（c712）
■ 守りの線（映像方針 26本目＝門番 check_illu ㊽ が記録の値を門番の側に持つ＝ここの定数を読まない）
  ・カリフォルニアン号の船橋・海図室・無線室の写真は無い＝**記録の語だけで描く**（部屋の形・置き場・道具の形は模式＝左下の断り）
  ・遠くの船は**灯の点だけ**（船の形を描かない＝描き分けない）。カリフォルニアン号から見た船をタイタニック号と名乗らない
  ・人は**顔の無い影**（縁だけ明るく）・役職だけ（名前を書かない）・心の中は描かない。乗客は群れの型（数えられない形）だけ
  ・時計の札は `ss.ILLU_CLOCK_OK` の時刻だけ・**どの船の時計か**を札に書く（sources.md §6）
"""
from __future__ import annotations

import math

import illu as IL
import titan_fig as F

W, H = IL.W, IL.H
KEY_DELAY = IL.KEY_DELAY
_part = IL._part

# ── 絵の色（全章で固定・章の色の置き換えが拾う値＝jiko_style の BG・BG2・GRID・LINE・LINE_DIM・TICK・INK_W を使わない）──
C26 = dict(
    sky0="#070f1c", sky1="#18283d", sea0="#0b1626", sea1="#04090f", wave="#24374d",
    hull="#0d141b", hull_ln="#2f4052", bul="#111a23", bul_top="#3d5064", deck="#0a1016",
    wall="#17212c", wall_ln="#2c3c4d", win="#22344a", win_ln="#3a4f66", roof="#0b1218",
    pipe="#8a7a5c", pipe_ln="#3b3326", lamp="#c9d2d8", lamp_ln="#1b232b", glow="#fff4cf",
    fig="#03070c", rim="#6d8aa8",
    light="#fbf6e4", light_glow="#fff2c4", red="#ff4a3a", red_glow="#ff7a5c", flare="#ffffff",
    room0="#121b25", room1="#0d141c", floor="#0a0f15", ceil="#0b1118", trim="#2b3a49",
    settee="#2a2f36", settee_ln="#454c55", back="#22272e", door="#27313c", door_ln="#3f4c5a", lit0="#33465c", lit1="#22313f",
    desk="#3a3128", desk_top="#4c4134", desk_ln="#211b15", box="#2e3a44", box_ln="#56677a", dial="#c9d2d8",
    bunk="#2b3138", bunk_ln="#454c55", blanket="#3a4652", phones="#7d8b97",
    tdeck="#141c25", tdeck_ln="#33424f", super="#1a2531", super_ln="#2d3c4b", boat="#c9cfd3", boat_ln="#4a535b",
    davit="#7e8a94", rail="#4d5d6c", crowd0="#04080d", crowd1="#080d13", crowd2="#0c121a",
    star="#ffffff", trail="#ffe9b0",
    seat="#c9d2d8", seat_on="#f2c14e", gun="#d7dde1", thwart="#7d8892", bilge="#1d2731",
    dawn0="#2a3d5c", dawn1="#c99a7a", dawn_sea0="#33465c", dawn_sea1="#121c28", ship="#1d252e", ship_ln="#3b4854",
    funnel="#2b3036", berg="#d8e2ea", berg_sh="#9fb0bf", mast="#4b5864",
    amber="#f2c14e", ink="#eef3f5", ol="#0a0f14",
)

FIG_H = 330.0                 # 船橋の人の影の背（画素）
ROOM_H = 360.0                # 部屋の中の人の影の背


def _d(pts, close=True):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")


def _path(pts, fill, stroke=None, sw=0.0, op=None, close=True, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    return f'<path d="{_d(pts, close)}" fill="{fill}"{st}{o}{extra}/>'


def _rect(x, y, w, h, fill, stroke=None, sw=0.0, rx=0.0, op=None, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{r} fill="{fill}"{st}{o}{extra}/>'


def _line(x1, y1, x2, y2, col, w=3.0, extra=""):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" '
            f'stroke-linecap="round"{extra}/>')


def _circ(x, y, r, fill, op=None, extra=""):
    o = f' opacity="{op}"' if op is not None else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"{o}{extra}/>'


def _grad(gid, c0, c1):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c0}"/>'
            f'<stop offset="1" stop-color="{c1}"/></linearGradient></defs>')


def _switch_part(text):
    return dict(_part("switch", IL.va_switch_svg(text), "", keys=IL._switch_keys()), signal=True)


# 切り替えの字（欄 ksw＝見る向きの合図・門番 ㉑）。見る向きが替わる所は向き・同じ向きで置き場（船や部屋）が替わる所は場所の名
KSW = dict(side="横から見ると", top="上から見ると", bridge="船橋では", titanic="タイタニック号では", wireless="無線室では")


def _head_only(place, start, states, fields):
    for f in fields:
        if any(st[f] != start[f] for st in states):
            raise ValueError(f"illu {place}：{f} は場面の頭（start）で1つだけ")


def _akeys(start, states, steps, on, dur=0.6, extra=0.0):
    """濃さだけの鍵（on＝状態 → 見せるか）。段の行頭＋delay＋extra から dur 秒で"""
    ks = [dict(stage=0, delay=0.0, a=float(on(start)))]
    cur = on(start)
    for i, (st, sp) in enumerate(zip(states, steps)):
        v = on(st)
        if v != cur:
            ks.append(dict(stage=i, delay=float(sp.get("delay", KEY_DELAY)) + extra, dur=float(sp.get("dur", dur)), a=float(v)))
            cur = v
    return ks


def _blink_keys(start, states, steps, on, n=5, t_on=0.32, t_off=0.26, lead=0.3):
    """点けたり消したり（モールス灯）。on(st) が真になった段の行頭から n 回"""
    ks = [dict(stage=0, delay=0.0, a=0.0)]
    prev = on(start)
    for i, st in enumerate(states):
        if on(st) and not prev:
            t = lead
            for _k in range(n):
                ks.append(dict(stage=i, delay=t, dur=0.08, a=1.0))
                ks.append(dict(stage=i, delay=t + t_on, dur=0.08, a=0.0))
                t += t_on + t_off
        prev = on(st)
    return ks


# ══════════════════════════════════════════════════════════
#  人の影（顔も服の細部も無い・縁だけ明るい）＝型紙（sprite）。foot＝層の中の足もと
# ══════════════════════════════════════════════════════════
def _fig_style():
    return f' fill="{C26["fig"]}" stroke="{C26["rim"]}" stroke-width="3.5" stroke-linejoin="round" paint-order="stroke fill"'


def fig26(pose, h, foot, s=-1):
    """pose＝stand（立つ）／binoc（双眼鏡を目に当てる）／lie（横になる＝頭が右）／sit（腰かけて手を前の机へ・ヘッドホン）。
    s＝向き（-1＝左を向く・+1＝右を向く）。顔・服の細部・名前の印は描かない"""
    x0, y0 = foot
    r = 0.115 * h
    st = _fig_style()
    if pose == "lie":
        body = [(x0, y0 - 0.20 * h), (x0 + 0.80 * h, y0 - 0.22 * h), (x0 + 0.80 * h, y0), (x0, y0)]
        return (f'<path d="{_d(body)}"{st}/>'
                f'<circle cx="{x0 + 0.90 * h:.1f}" cy="{y0 - 0.12 * h:.1f}" r="{r:.1f}"{st}/>')
    if pose == "sit":
        hip = (x0 - s * 0.02 * h, y0 - 0.30 * h)
        sh = (x0 + s * 0.04 * h, y0 - 0.70 * h)
        torso = [(sh[0] - 0.17 * h, sh[1]), (sh[0] + 0.17 * h, sh[1]), (hip[0] + 0.15 * h, hip[1] + 0.04 * h), (hip[0] - 0.15 * h, hip[1] + 0.04 * h)]
        thigh = [(hip[0], hip[1] - 0.06 * h), (x0 + s * 0.30 * h, y0 - 0.33 * h), (x0 + s * 0.30 * h, y0 - 0.22 * h), (hip[0], hip[1] + 0.08 * h)]
        shin = [(x0 + s * 0.24 * h, y0 - 0.26 * h), (x0 + s * 0.33 * h, y0 - 0.26 * h), (x0 + s * 0.33 * h, y0), (x0 + s * 0.24 * h, y0)]
        arm = [(sh[0], sh[1] + 0.02 * h), (x0 + s * 0.55 * h, y0 - 0.73 * h), (x0 + s * 0.55 * h, y0 - 0.66 * h), (sh[0], sh[1] + 0.12 * h)]
        hx, hy = sh[0] + s * 0.02 * h, sh[1] - r * 0.9
        return (f'<path d="{_d(thigh)}"{st}/><path d="{_d(shin)}"{st}/><path d="{_d(torso)}"{st}/><path d="{_d(arm)}"{st}/>'
                f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{r:.1f}"{st}/>')
    # 立つ（stand・binoc）
    body = (f'M {x0 - 0.20 * h:.1f} {y0 - 0.78 * h:.1f} Q {x0:.1f} {y0 - 0.86 * h:.1f} {x0 + 0.20 * h:.1f} {y0 - 0.78 * h:.1f} '
            f'L {x0 + 0.17 * h:.1f} {y0 - 0.40 * h:.1f} L {x0 + 0.13 * h:.1f} {y0:.1f} L {x0 - 0.13 * h:.1f} {y0:.1f} '
            f'L {x0 - 0.17 * h:.1f} {y0 - 0.40 * h:.1f} Z')
    g = f'<path d="{body}"{st}/><circle cx="{x0:.1f}" cy="{y0 - h + r:.1f}" r="{r:.1f}"{st}/>'
    if pose == "binoc":
        arm = [(x0 + s * 0.02 * h, y0 - 0.76 * h), (x0 + s * 0.20 * h, y0 - 0.90 * h), (x0 + s * 0.26 * h, y0 - 0.86 * h),
               (x0 + s * 0.10 * h, y0 - 0.66 * h)]
        bx = x0 + s * 0.19 * h
        g += (f'<path d="{_d(arm)}"{st}/>'
              f'<rect x="{min(bx, bx + s * 0.13 * h):.1f}" y="{y0 - 0.95 * h:.1f}" width="{0.13 * h:.1f}" height="{0.075 * h:.1f}" rx="4"{st}/>')
    return g


def arm26(h, foot, s=-1):
    """回す腕（下へ垂らした形で描く＝鍵の rot で前へ上げる）。返り値＝(svg, 肩＝回す中心)"""
    x0, y0 = foot
    sh = (x0 + s * 0.13 * h, y0 - 0.74 * h)
    w, L = 0.075 * h, 0.40 * h
    pts = [(sh[0] - w / 2, sh[1]), (sh[0] + w / 2, sh[1]), (sh[0] + w * 0.4, sh[1] + L), (sh[0] - w * 0.4, sh[1] + L)]
    return f'<path d="{_d(pts)}"{_fig_style()}/>', sh


def arm_rot(s, ang):
    """腕を「下」から前へ ang 度上げる回転（画面で時計回りが正）。左向き（s=-1）は時計回り"""
    return -s * ang


def _sprite(pid, pose, h, at, rec, s=-1, stage=0, delay=-1.0, path=None):
    foot = IL.big_foot(h)
    inst = [dict(stage=stage, delay=delay, path=[list(p) for p in (path or [at])])]
    return dict(_part(pid, fig26(pose, h, foot, s), rec), kind="sprite", foot=list(foot), inst=inst, role="crew", fig_h=h,
                fig_deg=0.0, geo=dict(kind="fig", pose=pose, at=list(path[-1] if path else at), h=h, s=s))


# ══════════════════════════════════════════════════════════
#  K1・K7・K8・K9　カリフォルニアン号の船橋（横から・夜）
# ══════════════════════════════════════════════════════════
BR = dict(hz=600.0, floor=900.0, bul=800.0, x_wing=480.0, x_wh=1420.0, wh_top=390.0)
BR_SPOT = dict(A=760.0, B=1040.0, P=1370.0)          # 人の立つ所（足もとの x）。P＝伝声管の前
BR_LADDER = 1300.0                                     # 下の甲板からの階段の上（模式）
BR_LAMP = (600.0, 742.0)                               # モールス灯の光る所（張り出しの手すりの上＝置き場は模式）
BR_PIPE = (1478.0, 640.0)                              # 伝声管の口（操舵室の壁＝置き場は模式）
BR_SHIP = dict(x=345.0, mast=(352.0, 522.0), red=(334.0, 588.0),
               deck=((356.0, 589.0), (368.0, 588.0), (379.0, 590.0)),
               glare=((388.0, 585.0), (396.0, 588.0), (404.0, 584.0), (411.0, 589.0), (419.0, 586.0), (426.0, 589.0), (401.0, 591.0)))
BR_FLARES = ((318.0, 552.0), (350.0, 546.0), (382.0, 553.0))     # 低い信号弾3発（マストの灯より低い＝Q7921 の「半分ほどの高さ」の向き）
BR_ANG = dict(down=0.0, lamp=72.0, point=112.0)                   # 腕の上げ（度）
BR_LAB = "横から見た図（カリフォルニアン号の船橋・夜）"
BR_REC = dict(
    ship="G1 p57（At about 11 p. m. a steamer's light was seen approaching from the eastward）",
    stop="G1 p57（Her steaming lights were still visible and also her port side light）",
    glare="G1 p58（He could see a masthead light, her red light (with glasses), and a glare of white lights on her afterdeck）",
    lamp="G1 p57（Call her up on the Morse lamp, and see if you can get any answer）",
    pipe="G1 p58（Mr. Stone reported to the captain by voice pipe）",
    point="G1 p58（In turning the Californian over to him, he pointed out the steamer）",
    flare="G1 p58（He got no reply, but the vessel fired three more white rockets）",
    fade="G1 p59（A gradual disappearing of all her lights, which would be perfectly natural with a ship steaming away from us）",
    gone="G1 p59（had disappeared bearing SW.）",
)


def br_bg_svg():
    hz = BR["hz"]
    g = [_grad("k26sky", C26["sky0"], C26["sky1"]), _grad("k26sea", C26["sea0"], C26["sea1"]),
         _rect(0, 0, W, hz, "url(#k26sky)"), _rect(0, hz, W, H - hz, "url(#k26sea)")]
    for k, y in enumerate((612, 628, 650, 680, 720, 770)):
        x0 = 40 + (k * 173) % 300
        while x0 < W:
            g.append(_line(x0, y, x0 + 90 + 18 * k, y, C26["wave"], 1.6 + 0.4 * k, ' opacity="0.55"'))
            x0 += 260 + 40 * k
    return "".join(g)


def br_deck_svg():
    """操舵室（右）・伝声管・階段の手すり（張り出しの手前の手すりと船体は前の層 br_front_svg）"""
    x_wh, top, fl = BR["x_wh"], BR["wh_top"], BR["floor"]
    g = [_rect(x_wh - 30, top - 26, W - x_wh + 60, 30, C26["roof"], C26["hull_ln"], 2.0),
         _rect(x_wh, top, W - x_wh + 10, fl - top, C26["wall"], C26["wall_ln"], 3.0)]
    for k in range(3):
        g.append(_rect(x_wh + 120 + 130 * k, top + 70, 92, 120, C26["win"], C26["win_ln"], 3.0, rx=6))
    px, py = BR_PIPE
    g += [_line(px + 14, py + 14, px + 14, fl - 2, C26["pipe_ln"], 16.0), _line(px + 14, py + 14, px + 14, fl - 2, C26["pipe"], 10.0),
          _path([(px + 22, py - 22), (px - 14, py - 30), (px - 14, py + 30), (px + 22, py + 22)], C26["pipe"], C26["pipe_ln"], 3.0,
                extra=' data-k="pipe"')]
    lx = BR_LADDER
    for x in (lx - 30, lx + 30):
        g.append(_line(x, fl - 120, x, fl, C26["bul_top"], 6.0))
    g.append(_line(lx - 30, fl - 120, lx + 30, fl - 120, C26["bul_top"], 6.0))
    return "".join(g)


def br_front_svg():
    """張り出しの手すり（腰の高さ）と船体＝人の影の前に重ねる（足もとが隠れる）"""
    x0, bul, fl = BR["x_wing"], BR["bul"], BR["floor"]
    lx, ly = BR_LAMP
    return (_rect(x0, bul, W - x0 + 10, fl - bul + 8, C26["bul"], C26["hull_ln"], 2.0)
            + _rect(x0 - 6, bul - 10, W - x0 + 16, 16, C26["bul_top"], C26["ol"], 2.0, rx=4)
            + _rect(x0 - 40, fl, W - x0 + 50, H - fl + 10, C26["hull"], C26["hull_ln"], 2.0)
            + _line(lx + 22, bul - 8, lx + 22, ly + 18, C26["lamp_ln"], 8.0)
            + _rect(lx - 2, ly - 22, 50, 40, C26["lamp"], C26["lamp_ln"], 3.0, rx=6, extra=' data-k="lamp"')
            + _circ(lx - 2, ly - 2, 13, C26["light"], extra=f' stroke="{C26["lamp_ln"]}" stroke-width="3"'))


def br_glow_svg():
    lx, ly = BR_LAMP
    return (f'<defs><radialGradient id="k26lg"><stop offset="0" stop-color="{C26["glow"]}" stop-opacity="0.95"/>'
            f'<stop offset="1" stop-color="{C26["glow"]}" stop-opacity="0"/></radialGradient></defs>'
            + _circ(lx - 2, ly - 2, 70, "url(#k26lg)") + _circ(lx - 2, ly - 2, 13, C26["glow"]))


def _dot(x, y, r, col, glow, rg):
    return _circ(x, y, rg, glow, 0.30) + _circ(x, y, r, col)


def br_lights_svg(kind):
    """遠くの船の灯（点だけ＝船の形を描かない）。kind＝approach（近づく灯）／stop（マストの灯と左の赤い舷灯）／glare（＋後ろの甲板の白い灯りの群れ）"""
    S = BR_SHIP
    g = [_dot(*S["mast"], 5.5, C26["light"], C26["light_glow"], 15)]
    if kind in ("stop", "glare"):
        g.append(_dot(*S["red"], 5.0, C26["red"], C26["red_glow"], 13))
    for x, y in S["deck"]:
        g.append(_dot(x, y, 3.0, C26["light"], C26["light_glow"], 8))
    if kind == "glare":
        g.append(f'<ellipse cx="406" cy="588" rx="34" ry="9" fill="{C26["light_glow"]}" opacity="0.28"/>')
        for x, y in S["glare"]:
            g.append(_circ(x, y, 2.8, C26["light"]))
    return "".join(g)


def br_flare_svg(k):
    x, y = BR_FLARES[k]
    g = [_circ(x, y, 26, C26["light_glow"], 0.35), _circ(x, y, 7, C26["flare"], extra=' data-k="flare"')]
    for a in range(0, 360, 60):
        t = math.radians(a)
        g.append(_circ(x + 16 * math.cos(t), y + 16 * math.sin(t), 2.4, C26["flare"]))
    return "".join(g)


def _br_people(start, states, steps):
    """人の影と腕（場面の頭の置き方＝g・s・j・欄 pose）。s の up＝その段で階段から上がってくる"""
    parts, R = [], BR_REC
    h = FIG_H
    fl = BR["floor"]
    allst = [start] + states
    if start["kg"] != "off":
        parts.append(_sprite("off3", "stand", h, (BR_SPOT["A"], fl), "G1 p57（Mr. Groves, third officer of the Californian, who was the officer of the first watch）"))
    if start["kj"] != "off":
        parts.append(_sprite("app", start["kj"], h, (BR_SPOT["A"], fl),
                             "G1 p58（Mr. Stone had with him during the middle watch an apprentice）"))
    if start["ks"] in ("stand", "binoc"):
        parts.append(_sprite("off2", start["ks"], h, (BR_SPOT["B"], fl), "G1 p58（relieved by Mr. Stone, the second officer）"))
    elif start["ks"] == "pipe":
        parts.append(_sprite("off2", "stand", h, (BR_SPOT["P"], fl), R["pipe"], s=1))
    else:
        up = next((i for i, st in enumerate(states) if st["ks"] == "up"), None)
        if up is not None:
            parts.append(_sprite("off2", "stand", h, None, "G1 p58（He remained on the bridge until relieved by Mr. Stone, the second officer, just after midnight）",
                                 stage=up, delay=0.3, path=[(BR_LADDER, fl + 150), (BR_LADDER, fl), (BR_SPOT["B"], fl)]))
    # 腕（三等航海士＝garm・見習い＝jarm）。下へ垂らした形を描き、鍵で前へ上げる
    for who, fld in (("kg", "kgarm"), ("kj", "kjarm")):
        if start[who] == "off" or start[who] == "binoc" or all(st[fld] == "down" for st in allst):
            continue
        svg, sh = arm26(h, (BR_SPOT["A"], fl), -1)
        ks = IL._keys(start, states, steps, lambda st, f=fld: dict(rot=arm_rot(-1, BR_ANG[st[f]])))
        rec = R["lamp"] if any(st[fld] == "lamp" for st in allst) else R["point"]
        parts.append(dict(_part(f"arm_{who}", svg, rec, sh, ks), geo=dict(kind="arm", who=who, ang=[BR_ANG[st[fld]] for st in allst])))
    return parts


def _scene_bridge(place):
    def scene(start, states, steps):
        allst = [start] + states
        _head_only(place, start, states, ("view", "ksw", "kg", "kj"))
        if any(st["ks"] != start["ks"] and not (start["ks"] == "off" and st["ks"] == "up") for st in states):
            raise ValueError(f"illu {place}：二等航海士（s）は頭で決める（off→up＝階段から上がってくる だけ段で変えてよい）")
        R = BR_REC
        parts = [_part("bg", br_bg_svg(), R["ship"])]
        # 遠くの灯（点だけ）。approach＝左の遠くから寄って来る／fade＝だんだん消える／gone＝無い
        kind0 = start["kship"]
        if kind0 != "off" or any(st["kship"] != "off" for st in states):
            base = "glare" if any(st["kship"] in ("glare", "fade", "gone") for st in allst) else (
                "stop" if any(st["kship"] == "stop" for st in allst) else "approach")
            rec = dict(approach=R["ship"], stop=R["stop"], glare=R["glare"])[base]

            def lk(st):
                v = st["kship"]
                if v == "far":
                    return dict(dx=-150.0, a=0.45)
                if v == "off":
                    return dict(dx=-150.0, a=0.0)          # 出るときは遠くの側から（近づく灯）
                if v == "gone":
                    return dict(dx=0.0, a=0.0)
                return dict(dx=0.0, a=1.0)
            ks = IL._keys(start, states, steps, lk)
            for k, (st, sp) in enumerate(zip(states, steps)):
                if st["kship"] == "fade":
                    ks[k + 1]["dur"] = float(sp.get("dur", 3.2))      # だんだん消える＝段の dur（秒）で長く
                    ks[k + 1]["a"] = 0.0
            parts.append(dict(_part("ship", br_lights_svg(base), rec, (BR_SHIP["x"], 588.0), ks),
                              geo=dict(kind="lights", base=base, states=[st["kship"] for st in allst])))
        parts.append(_part("deck", br_deck_svg(), R["pipe"]))
        parts += _br_people(start, states, steps)
        parts.append(dict(_part("front", br_front_svg(), R["lamp"]), geo=dict(kind="brfront", lamp=list(BR_LAMP))))
        if any(st["klamp"] == "blink" for st in allst):
            parts.append(dict(_part("lamp", br_glow_svg(), R["lamp"],
                                    keys=_blink_keys(start, states, steps, lambda st: st["klamp"] == "blink")), geo=dict(kind="blink")))
        if any(st["kflares"] == "on" for st in allst):
            i0 = next(i for i, st in enumerate(states) if st["kflares"] == "on")
            for k in range(3):
                d = float(steps[i0].get("delay", KEY_DELAY)) + 0.2 + 0.85 * k
                parts.append(dict(_part(f"flare{k}", br_flare_svg(k), R["flare"],
                                        keys=[dict(stage=0, delay=0.0, a=0.0), dict(stage=i0, delay=d, dur=0.15, a=1.0),
                                              dict(stage=i0, delay=d + 0.5, dur=0.6, a=0.55)]),
                                  obj=dict(flare=1), geo=dict(kind="flare", xy=list(BR_FLARES[k]))))
        parts += IL._pulse_part("voice", IL.ring_svg((BR_SPOT["P"] + 70.0, 612.0), 0.0, r=46), R["pipe"],
                                (BR_SPOT["P"] + 70.0, 612.0), states, steps, "rings", "out")
        if start["ksw"] != "off":
            parts.append(_switch_part(KSW[start["ksw"]]))
        return parts
    return scene


def _br_anchors(st):
    fl, h = BR["floor"], FIG_H
    return dict(A=(BR_SPOT["A"], fl - h - 6), B=(BR_SPOT["B"], fl - h - 6), P=(BR_SPOT["P"], fl - h - 6),
                ship=(BR_SHIP["x"] + 20, 560.0), mast=BR_SHIP["mast"], red=BR_SHIP["red"], glare=(406.0, 582.0),
                lamp=(BR_LAMP[0] - 2, BR_LAMP[1] - 26), pipe=(BR_PIPE[0] - 14, BR_PIPE[1] - 30), flares=(350.0, 532.0),
                sw=(150.0, 590.0))


def _br_note(st0, states):
    return "船橋の形・灯と道具の置き場は模式（写真が無い＝記録の語だけ）・遠くの船は灯の点だけ"


# ══════════════════════════════════════════════════════════
#  K2　海図室（横から）
# ══════════════════════════════════════════════════════════
CR = dict(floor=900.0, ceil=170.0, seat=760.0, x0=230.0, x1=1000.0)
CR_CAP = (520.0, 760.0)                     # 横になった船長の足もと（足の側の下）＝頭は右（伝声管の口の近く）
CR_PIPE = (952.0, 600.0)                    # 伝声管の口
CR_DOOR = (1400.0, 1620.0, 430.0)           # 戸（左・右・上の端）
CR_APP = (1510.0, 900.0)                    # 戸口に立つ見習いの足もと
CR_LAB = "横から見た図（カリフォルニアン号の海図室）"
CR_REC = dict(
    room="G1 p59（Gibson states that he went down to the chart room and told the master）・T1 p6784（書き起こし just below the upper bridge）",
    cap="T1 p7280（書き起こし I do not know; I was asleep）・G1 p59（although he remembered Gibson opening and closing the chart-room door）",
    pipe="G1 p58（Mr. Stone reported to the captain by voice pipe）",
    door="G1 p59（although he remembered Gibson opening and closing the chart-room door）",
    app="G1 p58（after watching the steamer for some 20 minutes more he sent Gibson down to the master）",
    ask="G1 p59（the master asked him if all the rockets were white, and also asked him the time）",
)


def cr_room_svg():
    fl, ce = CR["floor"], CR["ceil"]
    x0, x1, sy = CR["x0"], CR["x1"], CR["seat"]
    dl, dr, dt = CR_DOOR
    px, py = CR_PIPE
    g = [_grad("k26cr", C26["room0"], C26["room1"]), _rect(0, 0, W, H, "url(#k26cr)"),
         _rect(0, 0, W, ce, C26["ceil"], C26["trim"], 2.0), _rect(0, fl, W, H - fl, C26["floor"], C26["trim"], 2.0),
         # 長いす（横になる所）＝形は模式
         _rect(x0, sy - 130, x1 - x0, 130, C26["back"], C26["settee_ln"], 3.0, rx=10),
         _rect(x0 - 10, sy, x1 - x0 + 20, 38, C26["settee"], C26["settee_ln"], 3.0, rx=8),
         _rect(x0, sy + 38, x1 - x0, fl - sy - 38, C26["back"], C26["settee_ln"], 2.0),
         # 伝声管（天井から下りて口が長いすの頭の側へ）
         _line(px + 30, ce - 4, px + 30, py - 10, C26["pipe_ln"], 18.0), _line(px + 30, ce - 4, px + 30, py - 10, C26["pipe"], 12.0),
         _path([(px + 38, py - 22), (px - 6, py - 34), (px - 6, py + 30), (px + 38, py + 18)], C26["pipe"], C26["pipe_ln"], 3.0,
               extra=' data-k="pipe"'),
         # 戸の枠
         _rect(dl - 14, dt - 14, dr - dl + 28, fl - dt + 14, C26["trim"])]
    return "".join(g)


def cr_door_svg(open_):
    dl, dr, dt = CR_DOOR
    fl = CR["floor"]
    if not open_:
        return (_rect(dl, dt, dr - dl, fl - dt, C26["door"], C26["door_ln"], 3.0)
                + _circ(dl + 26, (dt + fl) / 2, 9, C26["lamp"]))
    return (_grad("k26lit", C26["lit0"], C26["lit1"]) + _rect(dl, dt, dr - dl, fl - dt, "url(#k26lit)")
            + _path([(dr, dt), (dr + 60, dt - 30), (dr + 60, fl + 26), (dr, fl)], C26["door"], C26["door_ln"], 3.0))


def _scene_K2(start, states, steps):
    allst = [start] + states
    _head_only("K2", start, states, ("view", "ksw"))
    R = CR_REC
    parts = [_part("room", cr_room_svg(), R["room"])]
    opened = any(st["k2door"] == "open" for st in allst)
    parts.append(dict(_part("door_c", cr_door_svg(False), R["door"],
                            keys=_akeys(start, states, steps, lambda st: st["k2door"] != "open", 0.5)), geo=dict(kind="door")))
    if opened:
        parts.append(dict(_part("door_o", cr_door_svg(True), R["door"],
                                keys=_akeys(start, states, steps, lambda st: st["k2door"] == "open", 0.5)), geo=dict(kind="door")))
    parts.append(_sprite("cap", "lie", ROOM_H, CR_CAP, R["cap"]))
    if opened:
        i0 = 0 if start["k2door"] == "open" else next(i for i, st in enumerate(states) if st["k2door"] == "open")
        parts.append(_sprite("app", "stand", ROOM_H, CR_APP, R["app"], s=-1, stage=i0,
                             delay=-1.0 if start["k2door"] == "open" else 0.75))
    cap_head = (CR_CAP[0] + 0.9 * ROOM_H, CR_CAP[1] - 0.12 * ROOM_H)
    parts += IL._pulse_part("pipe_ring", IL.ring_svg((CR_PIPE[0] - 16, CR_PIPE[1]), 180.0, r=44), R["pipe"],
                            (CR_PIPE[0] - 16, CR_PIPE[1]), states, steps, "rings_in", "out")
    parts += IL._pulse_part("talk", IL.ring_svg((CR_APP[0] - 80, CR_APP[1] - ROOM_H + 40), 180.0, r=40), R["app"],
                            (CR_APP[0] - 80, CR_APP[1] - ROOM_H + 40), states, steps, "rings", "out")
    parts += IL._pulse_part("ask", IL.ask_svg((cap_head[0] + 40, cap_head[1] - 70)), R["ask"],
                            (cap_head[0] + 40, cap_head[1] - 70), states, steps, "asks", "ask")
    if start["ksw"] != "off":
        parts.append(_switch_part(KSW[start["ksw"]]))
    return parts


def _k2_anchors(st):
    h = ROOM_H
    return dict(cap=(CR_CAP[0] + 0.9 * h, CR_CAP[1] - 0.24 * h), pipe=(CR_PIPE[0] + 30, CR_PIPE[1] - 120),
                pipe_up=(CR_PIPE[0] + 30, CR["ceil"] + 30), app=(CR_APP[0], CR_APP[1] - h - 6), door=(CR_DOOR[0], CR_DOOR[2] + 40))


def _k2_note(st0, states):
    return "部屋の形・長いす・伝声管と戸の置き場は模式（写真が無い＝記録の語だけ）"


# ══════════════════════════════════════════════════════════
#  K3　カリフォルニアン号の無線室（横から）
# ══════════════════════════════════════════════════════════
WR = dict(floor=900.0, ceil=170.0, desk=(980.0, 1720.0, 650.0), box=(1150.0, 1460.0, 455.0), key=(1068.0, 640.0),
          bunk=(130.0, 820.0, 690.0), phones=(1560.0, 636.0))
WR_OP = (860.0, 900.0)                       # 腰かけた通信士の足もと（右を向く）
WR_SLEEP = (215.0, 690.0)                    # 寝台に横になった通信士の足もと（頭は右）
WR_LAB = "横から見た図（カリフォルニアン号の無線室）"
WR_REC = dict(
    room="G1 p57（The master went to Evans's room and asked what ships he had）",
    send="G1 p57（This Evans did, calling up the Titanic and sending: We are stopped and surrounded by ice）",
    sleep="G1 p54（she had only one Marconi operator on board and he was asleep）・G1 p57（up to the time he turned in at 11.30 p. m.）",
)


def wr_room_svg():
    fl, ce = WR["floor"], WR["ceil"]
    dx0, dx1, dy = WR["desk"]
    bx0, bx1, by = WR["box"]
    kx, ky = WR["key"]
    ux0, ux1, uy = WR["bunk"]
    g = [_grad("k26wr", C26["room0"], C26["room1"]), _rect(0, 0, W, H, "url(#k26wr)"),
         _rect(0, 0, W, ce, C26["ceil"], C26["trim"], 2.0), _rect(0, fl, W, H - fl, C26["floor"], C26["trim"], 2.0),
         # 机と無線の機械（形は模式＝形のもとは了承②の写真の機械の箱）
         _rect(dx0, dy, dx1 - dx0, 26, C26["desk_top"], C26["desk_ln"], 3.0),
         _rect(dx0 + 20, dy + 26, dx1 - dx0 - 40, fl - dy - 26, C26["desk"], C26["desk_ln"], 3.0),
         _rect(bx0, by, bx1 - bx0, dy - by, C26["box"], C26["box_ln"], 3.0, rx=6)]
    for k in range(3):
        g.append(_circ(bx0 + 60 + 95 * k, by + 60, 22, C26["box"], extra=f' stroke="{C26["dial"]}" stroke-width="4"'))
        g.append(_line(bx0 + 60 + 95 * k, by + 60, bx0 + 60 + 95 * k + 12, by + 46, C26["dial"], 3.0))
    g += [_rect(bx0 + 30, by + 110, bx1 - bx0 - 60, 60, C26["box_ln"], C26["ol"], 2.0, rx=4),
          _line(bx0 + 150, by, bx0 + 150, ce, C26["box_ln"], 5.0),                     # 空中線へ（模式）
          # 電鍵
          _rect(kx - 40, ky - 6, 80, 16, C26["box_ln"], C26["ol"], 2.0, rx=3),
          # 寝台（形は模式）
          _rect(ux0, uy + 40, ux1 - ux0, 30, C26["bunk"], C26["bunk_ln"], 3.0, rx=6),
          _rect(ux0, uy, ux1 - ux0, 40, C26["blanket"], C26["bunk_ln"], 2.0, rx=10),
          _line(ux0 + 20, uy + 70, ux0 + 20, fl, C26["bunk_ln"], 10.0), _line(ux1 - 20, uy + 70, ux1 - 20, fl, C26["bunk_ln"], 10.0),
          _rect(ux0 - 20, uy - 160, 26, fl - uy + 160, C26["bunk_ln"], rx=6),
          # 腰かけ（模式）
          _rect(WR_OP[0] - 60, WR_OP[1] - 0.30 * ROOM_H + 8, 120, 18, C26["bunk_ln"], rx=4),
          _line(WR_OP[0] - 40, WR_OP[1] - 0.30 * ROOM_H + 26, WR_OP[0] - 40, WR_OP[1], C26["bunk_ln"], 8.0),
          _line(WR_OP[0] + 40, WR_OP[1] - 0.30 * ROOM_H + 26, WR_OP[0] + 40, WR_OP[1], C26["bunk_ln"], 8.0)]
    return "".join(g)


def wr_key_svg():
    kx, ky = WR["key"]
    return _rect(kx - 30, ky - 16, 52, 12, C26["dial"], C26["ol"], 2.0, rx=4)


def wr_phones_svg(on_head):
    if on_head:
        h = ROOM_H
        hx = WR_OP[0] + 0.06 * h
        hy = WR_OP[1] - 0.70 * h - 0.115 * h * 0.9
        r = 0.115 * h
        return (f'<path d="M {hx - r - 4:.1f} {hy:.1f} A {r + 4:.1f} {r + 6:.1f} 0 0 1 {hx + r + 4:.1f} {hy:.1f}" fill="none" '
                f'stroke="{C26["phones"]}" stroke-width="7"/>' + _rect(hx - 14, hy - 8, 28, 26, C26["phones"], C26["ol"], 2.0, rx=8))
    x, y = WR["phones"]
    return (f'<path d="M {x - 46:.1f} {y:.1f} A 46 40 0 0 1 {x + 46:.1f} {y:.1f}" fill="none" stroke="{C26["phones"]}" stroke-width="7"/>'
            + _rect(x - 62, y - 22, 30, 26, C26["phones"], C26["ol"], 2.0, rx=8) + _rect(x + 32, y - 22, 30, 26, C26["phones"], C26["ol"], 2.0, rx=8))


def _scene_K3(start, states, steps):
    allst = [start] + states
    _head_only("K3", start, states, ("view", "ksw", "k3op"))
    R = WR_REC
    parts = [_part("room", wr_room_svg(), R["room"])]
    if start["k3op"] == "send":
        parts.append(_sprite("op", "sit", ROOM_H, WR_OP, R["send"], s=1))
        parts.append(dict(_part("phones", wr_phones_svg(True), R["send"]), geo=dict(kind="phones", on="head")))
        tap = [dict(stage=0, delay=0.0, dy=0.0)]
        for i, st in enumerate(states):
            if st["k3key"] == "tap" and allst[i]["k3key"] != "tap":
                t = 0.35
                for _k in range(7):
                    tap += [dict(stage=i, delay=t, dur=0.07, dy=5.0), dict(stage=i, delay=t + 0.18, dur=0.07, dy=0.0)]
                    t += 0.42
        parts.append(dict(_part("key", wr_key_svg(), R["send"], keys=tap), geo=dict(kind="key")))
    else:
        parts.append(_part("key", wr_key_svg(), R["room"]))
        parts.append(_sprite("op", "lie", ROOM_H, WR_SLEEP, R["sleep"]))
        parts.append(dict(_part("phones", wr_phones_svg(False), R["sleep"]), geo=dict(kind="phones", on="desk")))
    bx0, bx1, by = WR["box"]
    parts += IL._pulse_part("radio", IL.ring_svg((bx0 + 150, WR["ceil"] + 40), -90.0, r=46), R["send"],
                            (bx0 + 150, WR["ceil"] + 40), states, steps, "rings", "out")
    if start["ksw"] != "off":
        parts.append(_switch_part(KSW[start["ksw"]]))
    return parts


def _k3_anchors(st):
    h = ROOM_H
    return dict(op=(WR_OP[0] + 0.06 * h, WR_OP[1] - 0.70 * h - 0.25 * h), sleep=(WR_SLEEP[0] + 0.9 * h, WR_SLEEP[1] - 0.25 * h),
                key=(WR["key"][0], WR["key"][1] - 18), phones=(WR["phones"][0], WR["phones"][1] - 44), box=(WR["box"][0] + 150, WR["box"][2]))


def _k3_note(st0, states):
    return "部屋の形・寝台と机の置き場は模式（写真が無い＝記録の語だけ）・機械の箱は形のもとの写真から模式"


# ══════════════════════════════════════════════════════════
#  K4　タイタニック号のボート甲板（横から・夜）＝view deck（c508）／wing（c512）
# ══════════════════════════════════════════════════════════
TD = dict(hz=600.0, floor=880.0, rail=800.0)
TD_BOAT = (170.0, 700.0, 640.0, 712.0)              # 1号艇（左・右・上・下）＝横から（形は模式）
TD_SOCKET = (792.0, 800.0)                           # 信号弾の筒（1号艇のそば＝G1 p54）
TD_BURST = (930.0, 250.0)
TD_CROWD = (1060.0, 1920.0)                          # 群れの枠
TD_SHELTER = (760.0, 1180.0, 600.0)                  # 船橋の端の屋根のある所（左・右・上）
TD_LAMP = (930.0, 566.0)                             # 屋根の上のモールス灯（G1 p16 above the shelters at each end of the navigating bridge）
TD_FAR = dict(white=(330.0, 566.0), red=(316.0, 590.0))
TD_OFF4 = (1330.0, 880.0)
TD_LAB = dict(deck="横から見た図（タイタニック号のボート甲板・夜）", wing="横から見た図（タイタニック号の船橋の端・夜）")
TD_REC = dict(
    deck="G1 p54（sent off at intervals from a socket by No. 1 emergency boat on the boat deck）",
    stars="G1 p54（They were the ordinary distress signals, exploding in the air and throwing off white stars）",
    crowd="G1 p54（The firing of these signals began about the time that No. 7 boat was lowered (12.45 a. m.)）",
    lamp="G1 p16（flash signal lamps fitted above the shelters at each of the navigating bridge for Morse signaling）・"
         "G1 p54（Mr. Boxall was also using a Morse light from the bridge）",
    far="G1 p54（a ship whose lights he saw about half a point on the port bow of the Titanic at a distance, as he thought, of about 5 or 6 miles）",
)


def td_base_svg(view):
    hz, fl = TD["hz"], TD["floor"]
    g = [_grad("k26tsky", C26["sky0"], C26["sky1"]), _grad("k26tsea", C26["sea0"], C26["sea1"]),
         _rect(0, 0, W, hz, "url(#k26tsky)"), _rect(0, hz, W, H - hz, "url(#k26tsea)")]
    if view == "deck":
        # 奥の部屋の壁（群れの後ろ）・甲板
        g += [_rect(1000, 520, W - 990, fl - 520, C26["super"], C26["super_ln"], 3.0)]
        for k in range(6):
            g.append(_rect(1060 + 140 * k, 590, 70, 90, C26["win"], C26["win_ln"], 2.0, rx=5))
        bx0, bx1, by0, by1 = TD_BOAT
        for x in (bx0 + 50, bx1 - 50):
            g.append(f'<path d="M {x:.1f} {fl:.1f} L {x:.1f} {by0 - 70:.1f} Q {x:.1f} {by0 - 120:.1f} {x + (30 if x < 400 else -30):.1f} {by0 - 120:.1f}" '
                     f'fill="none" stroke="{C26["davit"]}" stroke-width="12"/>')
            g.append(_line(x + (30 if x < 400 else -30), by0 - 120, x + (30 if x < 400 else -30), by0 + 4, C26["davit"], 3.0))
        g.append(_path([(bx0, by0), (bx1, by0), (bx1 - 30, by1), (bx0 + 40, by1)], C26["boat"], C26["boat_ln"], 3.0, extra=' data-k="boat1"'))
        g.append(_rect(TD_SOCKET[0] - 9, TD_SOCKET[1] - 44, 18, 48, C26["davit"], C26["ol"], 2.0, rx=3))
    else:
        sl, sr, st = TD_SHELTER
        g += [_rect(sl, st, sr - sl, fl - st, C26["super"], C26["super_ln"], 3.0),
              _rect(sl - 20, st - 16, sr - sl + 40, 18, C26["roof"], C26["super_ln"], 2.0),
              _rect(sl + 60, st + 60, 110, 90, C26["win"], C26["win_ln"], 2.0, rx=5),
              _rect(sl + 240, st + 60, 110, 90, C26["win"], C26["win_ln"], 2.0, rx=5),
              _line(TD_LAMP[0], st - 16, TD_LAMP[0], TD_LAMP[1] + 16, C26["lamp_ln"], 8.0),
              _rect(TD_LAMP[0] - 26, TD_LAMP[1] - 20, 52, 38, C26["lamp"], C26["lamp_ln"], 3.0, rx=6, extra=' data-k="lamp"'),
              _circ(TD_LAMP[0] - 26, TD_LAMP[1] - 1, 12, C26["light"], extra=f' stroke="{C26["lamp_ln"]}" stroke-width="3"')]
    return "".join(g)


def td_front_svg():
    fl, rl = TD["floor"], TD["rail"]
    g = [_rect(0, fl, W, H - fl, C26["tdeck"], C26["tdeck_ln"], 2.0), _line(0, rl, W, rl, C26["rail"], 6.0)]
    x = 30.0
    while x < W:
        g.append(_line(x, rl, x, fl, C26["rail"], 4.0))
        x += 90.0
    g.append(_line(0, rl + 40, W, rl + 40, C26["rail"], 3.0))
    return "".join(g)


def td_crowd():
    x0, x1 = TD_CROWD
    lay = IL.crowd_layout(x0, x1, TD["floor"] - 4, 112.0, rows=3, row_dy=30.0)
    svg = (f'<defs><clipPath id="k26cc"><rect x="{x0}" y="0" width="{x1 - x0}" height="{H}"/></clipPath></defs>'
           f'<g clip-path="url(#k26cc)">{IL.crowd_svg(lay, (C26["crowd0"], C26["crowd1"], C26["crowd2"]))}</g>')
    return svg, lay


def td_rocket_svg():
    sx, sy = TD_SOCKET
    bx, by = TD_BURST
    return (f'<path d="M {sx:.1f} {sy - 44:.1f} Q {sx + 40:.1f} {(sy + by) / 2:.1f} {bx:.1f} {by:.1f}" fill="none" '
            f'stroke="{C26["trail"]}" stroke-width="4" stroke-dasharray="14 10" opacity="0.8"/>')


def td_burst_svg():
    bx, by = TD_BURST
    g = [_circ(bx, by, 90, C26["light_glow"], 0.22), _circ(bx, by, 14, C26["star"])]
    for k in range(18):
        t = math.radians(k * 20 + 7)
        rr = 120 + 40 * ((k * 7) % 3)
        g.append(_line(bx + 22 * math.cos(t), by + 22 * math.sin(t), bx + rr * math.cos(t), by + rr * math.sin(t) + 18,
                       C26["star"], 2.0, ' opacity="0.55"'))
        g.append(_circ(bx + rr * math.cos(t), by + rr * math.sin(t) + 18, 5.5, C26["star"]))
    return "".join(g)


def td_far_svg():
    return (_dot(*TD_FAR["white"], 5.0, C26["light"], C26["light_glow"], 14) + _dot(*TD_FAR["red"], 4.5, C26["red"], C26["red_glow"], 12))


def td_blink_svg():
    x, y = TD_LAMP[0] - 26, TD_LAMP[1] - 1
    return (f'<defs><radialGradient id="k26tl"><stop offset="0" stop-color="{C26["glow"]}" stop-opacity="0.95"/>'
            f'<stop offset="1" stop-color="{C26["glow"]}" stop-opacity="0"/></radialGradient></defs>'
            + _circ(x, y, 66, "url(#k26tl)") + _circ(x, y, 12, C26["glow"]))


def td_dist_svg():
    x0, y0 = TD_LAMP[0] - 40, TD_LAMP[1]
    x1, y1 = TD_FAR["white"][0] + 18, TD_FAR["white"][1] + 6
    return _line(x0, y0, x1, y1, C26["amber"], 3.0, ' stroke-dasharray="12 10" opacity="0.85"')


def _scene_K4(start, states, steps):
    allst = [start] + states
    _head_only("K4", start, states, ("view", "ksw"))
    view = start["view"]
    R = TD_REC
    on = lambda f, v="on": (lambda st: st[f] == v)       # noqa: E731
    parts = [dict(_part("base", td_base_svg(view), R["deck"] if view == "deck" else R["lamp"]),
                  geo=dict(kind="td_" + view, lamp_bottom=TD_LAMP[1] + 18, roof_top=TD_SHELTER[2] - 16,
                           lamp_x=TD_LAMP[0], shelter=[TD_SHELTER[0], TD_SHELTER[1]]))]
    if view == "deck":
        if start["k4crowd"] == "on":
            svg, lay = td_crowd()
            parts.append(_part("crowd", svg, R["crowd"], role="passengers", crowd=[dict(layout=lay, x0=TD_CROWD[0], x1=TD_CROWD[1])]))
        parts.append(_part("front", td_front_svg(), R["deck"]))
        if any(st["k4rocket"] != "off" for st in allst):
            parts.append(dict(_part("trail", td_rocket_svg(), R["deck"],
                                    keys=_akeys(start, states, steps, lambda st: st["k4rocket"] in ("up", "burst"), 0.5)), geo=dict(kind="trail")))
            i0 = next((i for i, st in enumerate(states) if st["k4rocket"] == "burst"), None)
            if i0 is not None:
                d = float(steps[i0].get("delay", KEY_DELAY)) + 0.9
                parts.append(dict(_part("burst", td_burst_svg(), R["stars"], TD_BURST,
                                        keys=[dict(stage=0, delay=0.0, a=0.0, sc=0.3), dict(stage=i0, delay=d, dur=1.2, a=1.0, sc=1.0)]),
                                  geo=dict(kind="burst")))
    else:
        parts.append(dict(_part("far", td_far_svg(), R["far"], keys=_akeys(start, states, steps, on("k4far"), 0.8)), geo=dict(kind="lights", base="far")))
        parts.append(_part("front", td_front_svg(), R["lamp"]))
        parts.append(_sprite("off4", "stand", 300.0, TD_OFF4, R["lamp"]))
        svg, sh = arm26(300.0, TD_OFF4, -1)
        parts.append(dict(_part("arm", svg, R["lamp"], sh, IL._keys(start, states, steps, lambda st: dict(rot=arm_rot(-1, 72.0 if st["k4lamp"] == "blink" else 0.0)))),
                          geo=dict(kind="arm", who="off4")))
        parts.append(dict(_part("blink", td_blink_svg(), R["lamp"], keys=_blink_keys(start, states, steps, on("k4lamp", "blink"), n=8)),
                          geo=dict(kind="blink")))
        if any(st["k4dist"] == "on" for st in allst):
            parts.append(dict(_part("dist", td_dist_svg(), R["far"], keys=_akeys(start, states, steps, on("k4dist"), 0.6)), geo=dict(kind="dist")))
    if start["ksw"] != "off":
        parts.append(_switch_part(KSW[start["ksw"]]))
    return parts


def _k4_anchors(st):
    bx0, bx1, by0, _by1 = TD_BOAT
    return dict(boat=((bx0 + bx1) / 2, by0 - 4), socket=(TD_SOCKET[0], TD_SOCKET[1] - 50), burst=(TD_BURST[0] + 60, TD_BURST[1] - 40),
                lamp=(TD_LAMP[0], TD_LAMP[1] - 24), far=(TD_FAR["white"][0] + 6, TD_FAR["white"][1] - 14),
                off4=(TD_OFF4[0], TD_OFF4[1] - 306), dist=((TD_LAMP[0] + TD_FAR["white"][0]) / 2, (TD_LAMP[1] + TD_FAR["white"][1]) / 2 - 8))


def _k4_note(st0, states):
    if st0["view"] == "deck":
        return "甲板とボートの形・筒の置き場は模式・乗客は群れ"
    return "船橋の端の形は模式・遠くの船は灯の点だけ"


# ══════════════════════════════════════════════════════════
#  K5　1号艇の40の席（上から・人の形で数を名乗らない＝席の印）
# ══════════════════════════════════════════════════════════
BT = dict(x0=330.0, x1=1600.0, cy=560.0, half=176.0)    # 長さ 1270・幅 352 ＝ 25フィート2インチ：7フィート2インチ（G1 p25）
BT_ROWS = 8                                              # 席の列（腰かけ板の並びは模式）
BT_PER = 5                                               # 1列の席の数（模式）
BT_FILL = (0, 2, 4, 6, 9, 12, 15, 18, 21, 24, 29, 33)    # 埋まった12の席の番号（並びは模式・数は記録）
BT_LAB = "上から見た図（1号艇）"
BT_REC = dict(
    boat="G1 p25（One wood cutter, 25 feet 2 inches long by 7 feet 2 inches broad by 3 feet deep…constructed to carry 40 persons）",
    seats="G1 p52（this was an emergency boat with a carrying capacity of 40）",
    fill="G1 p51（No. 1 certainly left with only 12）",
)


def bt_outline():
    x0, x1, cy, hf = BT["x0"], BT["x1"], BT["cy"], BT["half"]
    pts = []
    L = x1 - x0
    for k in range(41):
        u = k / 40
        x = x0 + L * u
        if u < 0.72:
            w = hf * (1 - ((0.36 - u) / 0.36) ** 2 * 0.18) if u < 0.36 else hf
        else:
            w = hf * math.sqrt(max(0.0, 1 - ((u - 0.72) / 0.28) ** 2))
        pts.append((x, cy - w))
    pts += [(x, 2 * cy - y) for x, y in reversed(pts)]
    return pts


def bt_seats():
    x0, x1, cy, hf = BT["x0"], BT["x1"], BT["cy"], BT["half"]
    out = []
    for r in range(BT_ROWS):
        x = x0 + 120 + r * 125
        for c in range(BT_PER):
            y = cy - hf * 0.62 + c * (hf * 1.24 / (BT_PER - 1))
            out.append((x, y))
    return out


def bt_boat_svg():
    pts = bt_outline()
    x0, x1, cy, hf = BT["x0"], BT["x1"], BT["cy"], BT["half"]
    g = [_rect(0, 0, W, H, "#0d1824"), _path(pts, C26["bilge"], C26["gun"], 10.0, extra=' data-k="hull"')]
    for r in range(BT_ROWS):
        x = x0 + 120 + r * 125
        g.append(_rect(x - 26, cy - hf * 0.86, 52, hf * 1.72, C26["thwart"], C26["ol"], 2.0, rx=6, op=0.55))
    return "".join(g)


def bt_seats_svg(filled):
    g = []
    for k, (x, y) in enumerate(bt_seats()):
        on = filled and k in BT_FILL
        if on:
            g.append(_circ(x, y, 19, C26["seat_on"], extra=f' stroke="{C26["ol"]}" stroke-width="3" data-k="seat" data-f="1"'))
        elif not filled:
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="19" fill="none" stroke="{C26["seat"]}" stroke-width="4" data-k="seat" data-f="0"/>')
    return "".join(g)


def _scene_K5(start, states, steps):
    allst = [start] + states
    _head_only("K5", start, states, ("view", "ksw"))
    R = BT_REC
    parts = [_part("boat", bt_boat_svg(), R["boat"]),
             dict(_part("seats", bt_seats_svg(False), R["seats"]), obj=dict(seat=len(bt_seats())),
                  geo=dict(kind="seats", n=len(bt_seats()), len=BT["x1"] - BT["x0"], width=2 * BT["half"]))]
    if any(st["k5fill"] == "on" for st in allst):
        parts.append(dict(_part("fill", bt_seats_svg(True), R["fill"], keys=_akeys(start, states, steps, lambda st: st["k5fill"] == "on", 1.4)),
                          obj=dict(filled=len(BT_FILL)), geo=dict(kind="filled", n=len(BT_FILL))))
    if start["ksw"] != "off":
        parts.append(_switch_part(KSW[start["ksw"]]))
    return parts


def _k5_anchors(st):
    return dict(boat=(BT["x0"] + 200, BT["cy"] - BT["half"] - 8), seats=(BT["x0"] + 745, BT["cy"] - BT["half"] - 8),
                fill=(BT["x0"] + 120, BT["cy"] + BT["half"] + 6))


def _k5_note(st0, states):
    return "席の印は模式（数は記録の値・席の並びと埋まった席の場所は模式・人の形で数を名乗らない）"


# ══════════════════════════════════════════════════════════
#  K6　カルパチア号・夜明け・2号艇（横から）
# ══════════════════════════════════════════════════════════
CA = dict(hz=640.0, x0=420.0, x1=1720.0, deck=470.0, wl=700.0)
CA_BOAT = (1000.0, 1180.0, 690.0)                # 2号艇（左・右・上）＝船の横（形は模式）
CA_LAB = "横から見た図（カルパチア号・夜明け）"
CA_REC = dict(
    ship="G1 p54（the steamship Carpathia, 13,600 tons gross, of the Cunard Line）",
    stop="G1 p55（he stopped his ship at 4.05）",
    boat="G1 p55（He sighted the first boat (No. 2) and picked her up at 4.10）",
    ice="G1 p55（There was then a large number of icebergs around him, and it was just daylight）",
)


def ca_svg():
    hz = CA["hz"]
    x0, x1, dk, wl = CA["x0"], CA["x1"], CA["deck"], CA["wl"]
    g = [_grad("k26dsky", C26["dawn0"], C26["dawn1"]), _grad("k26dsea", C26["dawn_sea0"], C26["dawn_sea1"]),
         _rect(0, 0, W, hz, "url(#k26dsky)"), _rect(0, hz, W, H - hz, "url(#k26dsea)")]
    for bx, bw, bh in ((150.0, 120.0, 46.0), (1810.0, 90.0, 34.0), (1500.0, 60.0, 20.0)):
        g.append(_path([(bx - bw / 2, hz + 2), (bx - bw * 0.2, hz - bh), (bx + bw * 0.15, hz - bh * 0.8), (bx + bw / 2, hz + 2)],
                       C26["berg"], C26["berg_sh"], 2.0))
    hull = [(x0, dk + 40), (x1 - 40, dk + 40), (x1 + 20, dk + 10), (x1 - 30, wl + 30), (x0 + 30, wl + 30), (x0 - 10, dk + 50)]
    g.append(_path(hull, C26["ship"], C26["ship_ln"], 3.0, extra=' data-k="hull"'))
    g.append(_rect(x0 + 360, dk - 50, 640, 92, C26["ship"], C26["ship_ln"], 2.0))
    g.append(_rect(x0 + 600, dk - 260, 76, 216, C26["funnel"], C26["ship_ln"], 3.0))
    for mx in (x0 + 110, x0 + 330, x1 - 330, x1 - 120):
        g.append(_line(mx, dk + 40, mx, dk - 300, C26["mast"], 7.0))
    for k in range(14):
        g.append(_circ(x0 + 120 + 85 * k, dk + 110, 6, C26["ship_ln"]))
    return "".join(g)


def ca_boat_svg():
    bl, br_, bt = CA_BOAT
    return _path([(bl, bt), (br_, bt), (br_ - 20, bt + 34), (bl + 24, bt + 34)], C26["boat"], C26["boat_ln"], 3.0, extra=' data-k="boat2"')


def _scene_K6(start, states, steps):
    _head_only("K6", start, states, ("view", "ksw"))
    R = CA_REC
    parts = [_part("ship", ca_svg(), R["ship"])]
    mv = lambda st: dict(dx=0.0 if st["k6boat"] == "along" else -260.0, dy=0.0 if st["k6boat"] == "along" else 60.0, a=1.0)  # noqa: E731
    parts.append(dict(_part("boat", ca_boat_svg(), R["boat"], keys=IL._keys(start, states, steps, mv)), geo=dict(kind="boat2")))
    if start["ksw"] != "off":
        parts.append(_switch_part(KSW[start["ksw"]]))
    return parts


def _k6_anchors(st):
    bl, br_, bt = CA_BOAT
    return dict(boat=((bl + br_) / 2, bt - 6), ship=(CA["x0"] + 640, CA["deck"] - 270), ice=(150.0, CA["hz"] - 50))


def _k6_note(st0, states):
    return "船の形は写真から模式（人は描かない）・ボートと氷山の形と並びは模式"


# ══════════════════════════════════════════════════════════
#  登録
# ══════════════════════════════════════════════════════════
# 🔴 欄の名は前の回の置き場と共有の表（CHOICES・REC_FIELDS）に入る＝頭に k を付けて分ける（同じ名だと前の回の型の選べる値を黙って上書きする）
BR_FIELDS = dict(view="night", kship="off", kg="off", ks="off", kj="off", kgarm="down", kjarm="down", klamp="off", kflares="off",
                 ksw="off", cam=1.0)


def register():
    IL.FIELDS.update(
        K1=dict(BR_FIELDS),
        K2=dict(view="room", k2door="shut", ksw="off", cam=1.0),
        K3=dict(view="room", k3op="send", k3key="still", ksw="off", cam=1.0),
        K4=dict(view="deck", k4crowd="off", k4rocket="off", k4far="off", k4lamp="off", k4dist="off", ksw="off", cam=1.0),
        K5=dict(view="top", k5fill="off", ksw="off", cam=1.0),
        K6=dict(view="dawn", k6boat="near", ksw="off", cam=1.0))
    IL.CHOICES.update(ksw=("off",) + tuple(KSW), kship=("off", "far", "near", "stop", "glare", "fade", "gone"), kg=("off", "stand"), ks=("off", "up", "stand", "binoc", "pipe"),
                      kj=("off", "stand", "binoc"), kgarm=("down", "lamp", "point"), kjarm=("down", "lamp"), klamp=("off", "blink"), kflares=IL.ONOFF,
                      k2door=("shut", "open"), k3op=("send", "sleep"), k3key=("still", "tap"), k4crowd=IL.ONOFF, k4rocket=("off", "up", "burst"),
                      k4far=IL.ONOFF, k4lamp=("off", "blink"), k4dist=IL.ONOFF, k5fill=IL.ONOFF, k6boat=("near", "along"))
    IL.VIEWS.update(K1=("night",), K2=("room",), K3=("room",), K4=("deck", "wing"), K5=("top",), K6=("dawn",))
    IL.REC_FIELDS = IL.REC_FIELDS + ("kship", "kg", "ks", "kj", "kgarm", "kjarm", "klamp", "kflares", "k2door", "k3op", "k3key", "k4crowd",
                                     "k4rocket", "k4far", "k4lamp", "k4dist", "k5fill", "k6boat")
    IL.NOTE.update(K1=_br_note, K2=_k2_note, K3=_k3_note, K4=_k4_note, K5=_k5_note, K6=_k6_note)
    c = lambda st0, states: (960.0, 540.0)       # noqa: E731
    IL.EXTRA.update(
        K1=dict(scene=_scene_bridge("K1"), anchors=_br_anchors, camc=c, label=lambda st0, states: BR_LAB),
        K2=dict(scene=_scene_K2, anchors=_k2_anchors, camc=c, label=lambda st0, states: CR_LAB),
        K3=dict(scene=_scene_K3, anchors=_k3_anchors, camc=c, label=lambda st0, states: WR_LAB),
        K4=dict(scene=_scene_K4, anchors=_k4_anchors, camc=c, label=lambda st0, states: TD_LAB[st0["view"]]),
        K5=dict(scene=_scene_K5, anchors=_k5_anchors, camc=c, label=lambda st0, states: BT_LAB),
        K6=dict(scene=_scene_K6, anchors=_k6_anchors, camc=c, label=lambda st0, states: CA_LAB))


register()
