# -*- coding: utf-8 -*-
"""第5章 雲が滑走路へ降りてきた c501–c522（22カット）。9本目（テネリフェ）。

■ 🔴 `fog_laguna_*` は**空港が写っていない**（空港の北東の山地・2025年）。副題で場所と年を名乗り、
  **空港からの距離を書かない**（測っていない）。
■ 視程（見える距離）の数字は事故報告書 p12・p13 の気象の値（QAM）。c508〜c510 は
  **同じ目盛りで点を足していく**（16:36＝3キロ／16:50＝2〜3キロ／16:55＝1キロ／
  17:02＝滑走路の上300メートル・進入の側500メートル、ときどき5キロ）。
  ⚠️ 16:50 は幅のある値＝点ではなく**縦の帯**で描く（真ん中の値を作らない）。
■ 台本の写真9カットのうち5カットを図にし、地に写真を敷いた（写真映像の数は変わらない）
  c507（地 losrodeos_now_09）／c511（地 _10）／c518（地 _11）／c519（地 _02）／c521（地 _13）
  ＝「滑走路の写真を3回並べない」（photos.md §4-1）。⚠️ 管制塔の写真は0点＝代用しない。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
QAM = "事故報告書 p12・p13（空港の気象の値）"
QAMG = QAM + "　たて軸＝見える距離"
XT = [(6, "16:36"), (20, "16:50"), (25, "16:55"), (32, "17:02")]
YT = [(0, "0"), (1, "1キロ"), (3, "3キロ"), (5, "5キロ")]


def vis(upto):
    """滑走路の上の見える距離。upto＝何点目まで描くか（1〜3）。16:50 は帯。"""
    pts = [(6, 3.0), (25, 1.0), (32, 0.3)][:upto]
    out = [dict(pts=[(20, 2.0), (20, 3.0)], t="", c=J.INK_W, sw=14)]
    if len(pts) == 1:
        out.insert(0, dict(pts=pts, t="", c=J.INK_W, dots_only=True, dotr=12))
    else:
        out.insert(0, dict(pts=pts, t="", c=J.INK_W, sw=6, dot=True, dotr=10))
    return out


SPEC = {

    "c501": dict(
        t="この空港の天気は、ふつうと違う",
        s="雲が降りる、空港の北東の山地　2025年撮影",
        photo=P("fog_laguna_05"), bias=0.45, side="right", ann_y=356,
        **ss.kind(P("fog_laguna_05")),
        ann=[],
    ),

    "c502": dict(
        t="霧なら、数字にできる",
        s="霧と、この空港で起きること",
        fig=("beforeafter", dict(
            a=dict(k="霧", t="濃さを測れる", lines=["見える距離を数字にできる"], c=J.LINE),
            b=dict(k="ロス・ロデオス空港", t="数字にしにくいもの", lines=["見え方が刻々と変わる"],
                   c=J.ALERT),
            arrow=False, note="事故報告書 p39")),
    ),

    "c503": dict(
        t="雲の層が、流れてくる",
        s="雲が流れる、空港の北東の山地　2025年撮影",
        photo=P("fog_laguna_02"), bias=0.60, side="right", ann_y=356,
        **ss.kind(P("fog_laguna_02")),
        ann=[dict(t="見え方", d="かたまりが通るたびに変わる", dc=J.INK_W, ds=32)],
    ),

    "c504": dict(
        t="報告書の言い方",
        s="視界を悪くしたもの",
        fig=("quote", dict(
            phrase="霧ではない。地面についた雲だった",
            rows=[("場所", "ロス・ロデオス空港", J.INK_W),
                  ("出どころ", "事故報告書 p39・p40", J.DOC)],
            paper=True)),
    ),

    "c505": dict(
        t="0メートルから、1キロへ",
        s="数分ごとに変わる視界",
        fig=("graph", dict(
            series=[dict(pts=[(0, 0), (4, 1000), (8, 40)], t="", c=J.ALERT, sw=6,
                         dot=True, dotr=10)],
            xr=(-0.6, 8.6), yr=(-60, 1200),
            xticks=[(0, "ある瞬間"), (4, "数分後"), (8, "また")],
            yticks=[(0, "0"), (1000, "1キロ")],
            legend=False,
            note="事故報告書 p40　たて軸＝見える距離。報告書の言葉を並べた略図（時間の目盛りは無い）")),
    ),

    "c506": dict(
        t="時刻ごとの気象の値",
        s="空港が出していたもの",
        fig=("panel", dict(
            blocks=[dict(k="呼び方", t="このころの呼び方", v="QAM", c=J.INST),
                    dict(k="中身", t="決まった時刻の気象の値", v="", c=J.LINE)],
            note=QAM, cols=2)),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_09）
    "c507": dict(
        t="16:36、見える距離は3キロ",
        s="視界の数字の移り変わり",
        fig=("moment", dict(
            clock="16:36", label="空港の気象の値",
            facts=[dict(t="滑走路の上", v="3キロ", c=J.INK_W),
                   dict(t="遠くに", v="霧", c=J.LINE)],
            sub=QAM)),
    ),

    "c508": dict(
        t="16:50、2キロから3キロ",
        s="視界の数字の移り変わり",
        fig=("graph", dict(
            series=vis(1), xr=(3, 35), yr=(0, 5.6), xticks=XT, yticks=YT,
            legend=False,
            marks=[dict(x=20, y=3.0, t="2〜3キロ　進入の側も同じくらい", c=J.AMBER)],
            note=QAMG)),
    ),

    "c509": dict(
        t="16:55、1キロ",
        s="視界の数字の移り変わり",
        fig=("graph", dict(
            series=vis(2), xr=(3, 35), yr=(0, 5.6), xticks=XT, yticks=YT,
            legend=False,
            marks=[dict(x=25, y=1.0, t="1キロ", c=J.AMBER)],
            note=QAMG)),
    ),

    "c510": dict(
        t="17:02、300メートル",
        s="同じ時刻の、二つの場所の視界",
        fig=("graph", dict(
            series=vis(3) + [dict(pts=[(32, 0.5), (32, 5.0)], t="", c=J.LINE,
                                  dots_only=True, dotr=10)],
            xr=(3, 35), yr=(0, 5.6), xticks=XT, yticks=YT,
            legend=False,
            marks=[dict(x=32, y=0.3, t="滑走路 300メートル", c=J.ALERT, anchor="end",
                        dx=-26, dy=-10),
                   dict(x=32, y=5.0, t="進入の側 500メートル（ときに5キロ）", c=J.LINE,
                        anchor="end", dx=-26, dy=10)],
            note=QAMG)),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_10）。⚠️ 割った数（10分の1）を出さない。
    "c511": dict(
        t="26分で、3キロが300メートルに",
        s="視界の数字の移り変わり",
        fig=("compare", dict(
            items=[dict(v=3000, t="16:36", disp="3,000", unit="メートル", c=J.INK_W),
                   dict(v=300, t="17:02", disp="300", unit="メートル", c=J.ALERT)],
            vmax=3200, note=QAM + "　二機はまだ地上")),
    ),

    "c512": dict(
        t="地面についた雲が増えた",
        s="高さ0メートルの雲の量（空を8つに分けて数える）",
        fig=("beforeafter", dict(
            a=dict(k="はじめ", t="8分の1", lines=["空のわずか"], c=J.LINE),
            b=dict(k="増えたあと", t="8分の7", lines=["空のほとんど"], c=J.ALERT),
            note=QAM)),
    ),

    "c513": dict(
        t="気温と露点が、ほとんど同じ",
        s="空港の気温と露点",
        fig=("compare", dict(
            items=[dict(v=14, t="気温", disp="14", unit="度", c=J.AMBER),
                   dict(v=13, t="露点", disp="13", unit="度", c=J.LINE)],
            vmax=16,
            note="事故報告書 p12　露点＝空気が冷えて水の粒ができ始める温度")),
    ),

    "c514": dict(
        t="雲になる、一歩手前",
        s="気温と露点の差",
        fig=("moment", dict(
            clock="1度", label="この日の差",
            facts=[dict(t="差が小さいほど", v="雲に変わりやすい", c=J.AMBER)],
            sub="事故報告書 p12")),
    ),

    # 進入灯の列（x 0.28〜0.62・y 0.42〜0.5）へ寄る＝手前の民家を外す。
    "c515": dict(
        t="見える距離は、どう決めていた",
        s="現在のテネリフェ北空港の進入灯　2012年撮影",
        photo=P("losrodeos_now_03"), side="right", ann_y=356,
        **ss.focus(P("losrodeos_now_03"), 0.45, 0.46, zoom=1.8),
        **ss.kind(P("losrodeos_now_03")),
        ann=[],
    ),

    "c516": dict(
        t="機械で見通しを測る仕組み",
        s="視界を測る方法の一つ",
        fig=("panel", dict(
            blocks=[dict(k="名前", t="滑走路視距離", v="RVR", c=J.INST),
                    dict(k="測るもの", t="滑走路の脇に置いた機械", v="", c=J.LINE),
                    dict(k="出すもの", t="見通しの数字", v="", c=J.AMBER)],
            note="事故報告書 p12", cols=3)),
    ),

    "c517": dict(
        t="ロス・ロデオス空港に、RVRは無い",
        s="空港の設備の一覧",
        fig=("absent", dict(
            mode="single",
            # ⚠️ d は大きな Dela で出る＝長いと小さくなって漢字がつぶれる（check_layout）。短くする。
            items=[dict(t="RVR（滑走路視距離）", d="出されない",
                        ok=False, c=J.TICK)],
            note="事故報告書 p12")),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_11）。⚠️ 管制塔の写真は無い＝代用しない。
    "c518": dict(
        t="決めていたのは、管制官の目",
        s="見通しのよいときの決め方",
        fig=("people", dict(
            nodes=[dict(x=0.18, y=0.42, t="管制官", d="管制塔", c=J.INK_W, kind="person"),
                   dict(x=0.80, y=0.42, t="滑走路の端", d="見えている", c=J.LINE,
                        kind="part")],
            edges=[dict(a=0, b=1, t="自分の目で見て伝える", c=J.AMBER)],
            note="事故報告書 p12")),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_02）
    "c519": dict(
        t="どちらの場合も、決めたのは人",
        s="見える距離を決めていた人",
        fig=("beforeafter", dict(
            a=dict(k="端が見えるとき", t="管制官", lines=["自分の目で見る"], c=J.INK_W),
            b=dict(k="端が見えないとき", t="観測員", lines=["気象の観測塔から"], c=J.AMBER),
            arrow=False, note="事故報告書 p12　機械が出した数字ではない")),
    ),

    "c520": dict(
        t="中心線灯は、消えていた",
        s="霧の中の目印になる灯り",
        fig=("runway", dict(
            steps=[dict(lights=dict(on=True),
                        mark=[dict(at=0.5, y="above", t="中心線灯　進む向きを示す", c=J.AMBER)]),
                   dict(lights=dict(on=False),
                        mark=[dict(at=0.5, y="below", t="3月15日から使えない", c=J.ALERT)])],
            taxiway=False, note="模式図（灯りの数と間隔は正確ではない）",
            src="事故報告書 p17")),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_13）。⚠️ 写真は誘導路の線＝中心線灯と名乗らない。
    "c521": dict(
        t="パンナムの機長は、条件を付けた",
        s="中心線灯が消えていると知らされて",
        fig=("moment", dict(
            clock="17:04:58", label="管制塔が両機に伝えた",
            facts=[dict(t="中心線の灯り", v="使えない", c=J.ALERT),
                   dict(t="機長が要ると言った距離", v="800メートル", c=J.AMBER)],
            sub="操縦室の録音の書き起こし／事故報告書 p17・p37")),
    ),

    # pr01 と同じ写真＝上の雲へ寄る（別の絵にする）。
    "c522": dict(
        t="見えにくい滑走路へ、二機が向かう",
        s="現在のテネリフェ北空港（低い雲の日）　2007年撮影",
        photo=P("losrodeos_now_09"), bias=0.15, xbias=0.40, zoom=1.40,
        side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_09")),
        ann=[dict(t="見える距離", d="下がり続けている", dc=J.ALERT, ds=36),
             dict(t="測る機械", d="無い", dc=J.INK_W, ds=44)],
    ),
}
