# -*- coding: utf-8 -*-
"""第1章　北極でも動く炉 c101–c123（23カット・228秒）。

■ この章の役目
  **追うのは、炉そのもの。ここでは事故の話をしない。**
  物証は Fig 1.4（炉の縦断面・印字 p.16）と Fig 1.6（十字型の制御棒・印字 p.18）。
  決め所は c121「遮蔽ブロックは、外さないと届かない」。

■ 出どころ
  IDO-19302 p.1〜3（設計・遮蔽・運転の履歴）／p.10〜11 Table 1.1（出力と燃料）／
  図 Fig 1.1〜1.8（印字 p.13〜20）／HAER ID-33-D-52・53・73（1957〜58年の建設写真）。

■ ⚠️ 報告書の図は**英字が焼き込まれている**（ベクタで付いてこないというのは誤り）。
   逃がすのは `scene_jiko.TRIM_BY_PHOTO`（切る場所はカットでなくファイルに紐づける）。
"""
import jiko_style as J
import cuts.ss as ss

SPEC = {

    # ── c101 SL-1 という名前 ──────────────────────────
    "c101": dict(
        t="名前は、定置式・低出力の1号機",
        s="炉の縦断面　Fig 1.4（印字 p.16）",
        photo=ss.IDO_P16, side="right", ann_y=330, bias=0.45, xbias=0.30,
        zoom=1.15,
        ann=[dict(t="SL-1", d="Stationary Low Power Reactor No.1",
                  dc=J.LINE, ds=30),
             dict(t="分かっていないこと", d="事故の前から1つあった",
                  dc=J.ALERT, ds=32)],
    ),

    # ── c102 どこに置かれたか ──────────────────────────
    "c102": dict(
        t="置かれたのは、試験炉の並ぶ砂漠",
        s="試験場の全体図　Fig 1.1（印字 p.13）",
        photo=ss.IDO_P13, side="left", ann_y=330, bias=0.45, zoom=1.10,
        ann=[dict(t="設計", d="アルゴンヌ国立研究所", dc=J.INST, ds=32),
             dict(t="場所", d="NRTS（1949年設置）", dc=J.LINE, ds=32)],
    ),

    # ── c103 何のための炉か ────────────────────────────
    "c103": dict(
        t="送る先は、遠いレーダー基地",
        s="報告書が書いている用途（p.1）",
        fig=("panel", dict(
            lead="この炉が作るもの",
            blocks=[dict(k="1", t="電気", c=J.AMBER),
                    dict(k="2", t="暖房の熱", c=J.AMBER),
                    dict(k="＝", t="遠隔地の基地へ送る試作機", c=J.INK_W)],
            cols=3, note="量産の前の、1号機")),
    ),

    # ── c104 ALPR から SL-1 へ ────────────────────────
    "c104": dict(
        t="もとの名前は ALPR だった",
        s="完成間近の空撮　1958年5月22日",
        photo=ss.HAER_73, bias=0.5, side="right", ann_y=340,
        ann=[dict(t="旧称", d="Argonne Low Power Reactor", dc=J.LINE, ds=30),
             dict(t="改称", d="軍の呼び名にあわせた", dc=J.INK_W, ds=32)],
    ),

    # ── c105 4つの利点（前半）──────────────────────────
    "c105": dict(
        t="利点は、報告書に4つある",
        s="この型の利点（p.1）　1つめと2つめ",
        fig=("panel", dict(
            lead="報告書が挙げた利点",
            blocks=[dict(k="1", t="貨物機で運べる", c=J.OK),
                    dict(k="2", t="1回の燃料で3年動く", c=J.OK)],
            cols=2, note="残りの2つは、このあと")),
    ),

    # ── c106 4つの利点（後半）──────────────────────────
    "c106": dict(
        t="掘らずに建ち、水も要らない",
        s="この型の利点（p.1）　3つめと4つめ",
        fig=("panel", dict(
            lead="報告書が挙げた利点",
            blocks=[dict(k="3", t="地面の上に建てられる", c=J.OK),
                    dict(k="4", t="大量の水を必要としない", c=J.OK)],
            cols=2, note="極地でも工事ができる、という意味")),
    ),

    # ── c107 建設のはじまり ───────────────────────────
    "c107": dict(
        t="支柱から先に、立てていく",
        s="炉建屋の支柱　1957年9月5日",
        photo=ss.HAER_52, bias=0.5, side="right", ann_y=340,
        ann=[dict(t="着工", v="1957年", vc=J.INK_W, vs=104),
             dict(t="この写真", d="建屋を載せる支柱", dc=J.LINE, ds=32)],
    ),

    # ── c108 鋼の外殻 ───────────────────────────────
    "c108": dict(
        t="掘らずに建てる型である",
        s="鋼の外殻が支柱の上に立ち上がる　1957年9月20日",
        photo=ss.HAER_53, bias=0.5, side="left", ann_y=340,
        ann=[dict(t="外殻", d="円筒の鋼板を組み上げる", dc=J.LINE, ds=32),
             dict(t="地下", d="掘らない", dc=J.INK_W, ds=32)],
    ),

    # ── c109 出力 ─────────────────────────────────
    "c109": dict(
        t="熱3000、電気300、暖房400",
        s="Table 1.1 の設計値（印字 p.10）　単位は kW",
        fig=("compare", dict(
            items=[dict(v=3000, t="熱", disp="3,000", unit="kW", c=J.ALERT),
                   dict(v=300, t="電気", disp="300", unit="kW", c=J.AMBER),
                   dict(v=400, t="暖房の熱", disp="400", unit="kW", c=J.AMBER)],
            vmax=3000, note="取り出せるのは、熱の 23%")),
    ),

    # ── c110 圧力容器 ──────────────────────────────
    "c110": dict(
        t="中心にあるのは、縦長の筒",
        s="炉建屋の断面　Fig 1.3（印字 p.15）",
        photo=ss.IDO_P15, side="right", ann_y=330, bias=0.45, zoom=1.15,
        ann=[dict(t="高さ", v="約14.5 ft", vc=J.AMBER, vs=96),
             dict(t="鋼の厚さ", v="3/4 in", vc=J.AMBER, vs=96)],
    ),

    # ── c111 燃料40体 ──────────────────────────────
    "c111": dict(
        t="燃料は40体、ウランは14キロ",
        s="炉心の配置　Fig 1.5（印字 p.17）",
        photo=ss.IDO_P17, side="left", ann_y=330, bias=0.42, zoom=1.10,
        ann=[dict(t="燃料要素", v="40", d="1体は9枚の板の束", vc=J.AMBER,
                  vs=104, dc=J.LINE, ds=30),
             dict(t="ウラン235", v="14 kg", vc=J.AMBER, vs=96)],
    ),

    # ── c112 濃縮度とホウ素の帯 ────────────────────────
    "c112": dict(
        t="ウランは、試験炉の濃さだ",
        s="燃料要素　Fig 1.7（印字 p.19）",
        photo=ss.IDO_P19, side="right", ann_y=330, bias=0.45, zoom=1.10,
        ann=[dict(t="濃縮度", v="91%", d="試験炉らしい高い値", vc=J.ALERT,
                  vs=110, dc=J.LINE, ds=30),
             dict(t="板の側面", d="ホウ素を含む帯を溶接", dc=J.OK, ds=32)],
    ),

    # ── c113 ホウ素の役目 ─────────────────────────────
    "c113": dict(
        t="ホウ素が、燃えすぎを抑える",
        s="模式図　ホウ素の役目（p.2 の記述から）",
        fig=("process", dict(
            steps=[dict(t="核分裂", d="中性子が出る", c=J.ALERT),
                   dict(t="ホウ素", d="中性子を吸う", c=J.OK),
                   dict(t="反応", d="進みすぎない", c=J.INK_W)],
            note="出典：IDO-19302 印字 p.2")),
    ),

    # ── c114 減った量は決められていない ─────────────────────
    "c114": dict(
        t="どれだけ減ったかは書けない",
        s="ホウ素の損失についての記述（p.2）",
        fig=("absent", dict(
            mode="single", lead="ホウ素の損失について報告書が書いたこと",
            items=[dict(t="失われた量", d="決められない", ok=False, c=J.ALERT)],
            note="原文は「何らかの分からない仕組みで失われた」")),
    ),

    # ── c115 カドミウム板6枚 ──────────────────────────
    "c115": dict(
        t="対策は、カドミウム板6枚",
        s="模式図　差し込んだ位置（p.2 の記述から）",
        fig=("breakdown", dict(
            total=6, unit="枚",
            parts=[dict(v=3, t="2番の棒の溝", c=J.OK),
                   dict(v=3, t="6番の棒の溝", c=J.OK)],
            note="ホウ素が減ったぶんを、外から補う")),
    ),

    # ── c116 制御棒5本 ──────────────────────────────
    "c116": dict(
        t="制御棒は5本、十字の板だ",
        s="制御棒　Fig 1.6（印字 p.18）",
        photo=ss.IDO_P18, side="right", ann_y=330, bias=0.42, zoom=1.10,
        ann=[dict(t="本数", v="5", d="芯：カドミウム／外：金属",
                  vc=J.AMBER, vs=110, dc=J.LINE, ds=30),
             dict(t="1本の重さ", v="約22 kg", vc=J.AMBER, vs=92)],
    ),

    # ── c117 駆動と落下 ──────────────────────────────
    "c117": dict(
        t="電流を切れば、自分の重さで落ちる",
        s="制御棒の駆動　Fig 1.8（印字 p.20）",
        photo=ss.IDO_P20, side="left", ann_y=330, bias=0.45, zoom=1.15,
        ann=[dict(t="上下の仕組み", d="歯棒＋歯車",
                  dc=J.LINE, ds=30),
             dict(t="切ると", d="電磁クラッチが外れる", dc=J.ALERT, ds=32)],
    ),

    # ── c118 スクラム ──────────────────────────────
    # ⚠️ 落ちる途中の形は報告書に無い。**線でつながない**（点と帯だけ）。
    "c118": dict(
        t="30インチを、2秒かからず落ちる",
        s="緊急停止（スクラム）　p.2 の記述",
        fig=("graph", dict(
            series=[dict(pts=[(0, 30), (2, 0)], t="棒の位置", c=J.ALERT,
                         dots_only=True, dot=True)],
            xr=(0, 2.6), yr=(0, 34), xlab="秒", ylab="インチ",
            xticks=[(0, "0"), (1, "1"), (2, "2")],
            yticks=[(0, "0"), (15, "15"), (30, "30")],
            band=[dict(a=0, b=2, t="落ちきるまで", c=J.ALERT)],
            marks=[dict(x=0, y=30, t="全行程 30 インチ", c=J.AMBER, dy=-30),
                   dict(x=2, y=0, t="2秒かからない", c=J.ALERT, dy=30)],
            note="途中の速さは報告書に無いので、点だけを置いた")),
    ),

    # ── c119 砂利16フィート ────────────────────────────
    "c119": dict(
        t="放射線を止めるのは、砂利だった",
        s="模式図　遮蔽の厚み（p.3 の記述から）　単位は ft",
        fig=("compare", dict(
            items=[dict(v=12, t="見積り", disp="12", unit="ft", c=J.LINE),
                   dict(v=16, t="実際に入れた", disp="16", unit="ft", c=J.OK)],
            vmax=16, ratio="1.33倍", note="主な遮蔽は、水でも鉛でもなく砂利")),
    ),

    # ── c120 蓋の上の遮蔽ブロック ───────────────────────
    "c120": dict(
        t="蓋の上には、ブロックが載る",
        s="模式図　遮蔽ブロックの構成（p.3 の記述から）",
        fig=("panel", dict(
            lead="炉の蓋の上に載っているもの",
            blocks=[dict(k="1", t="鋼", c=J.LINE),
                    dict(k="2", t="板", c=J.LINE),
                    dict(k="3", t="コンクリートのブロック", c=J.INK_W)],
            cols=3, note="覆う範囲＝半径 6 ft")),
    ),

    # ── c121 ★決め所「遮蔽ブロックは、外さないと届かない」──────
    "c121": dict(
        t="この作りが、あとで効いてくる",
        s="蓋と遮蔽の重なり　Fig 1.4（印字 p.16）",
        photo=ss.IDO_P16, bias=0.40, xbias=0.35, zoom=1.15,
        fig=("quote", dict(
            phrase="外さないと、届かない",
            rows=[("何が", "炉の蓋の上の遮蔽ブロック", J.INK_W),
                  ("なぜ外すか", "制御棒の駆動部に手を触れるため", J.LINE),
                  ("どこに", "IDO-19302 印字 p.3", J.DOC)],
            ctx="原文 These shield blocks had to be removed from the reactor "
                "vessel head in order to allow personnel to work on the "
                "control rod mechanisms.",
            paper=True)),
    ),

    # ── c122 初臨界と引き継ぎ ──────────────────────────
    "c122": dict(
        t="動きはじめたのは、1958年夏",
        s="運転の履歴（p.3）",
        fig=("timeline", dict(
            t0=1958.5, t1=1961.1,
            title="単位は年。臨界＝核反応がひとりでに続く状態",
            ticks=[(1958.5, "1958年"), (1959.5, "1959年"),
                   (1960.5, "1960年"), (1961.0, "1961年")],
            events=[dict(t=1958.61, top="8/11", t2="初めて臨界", c=J.OK,
                         big=True),
                    dict(t=1959.10, top="2/5", t2="運転が民間会社へ", c=J.INST),
                    dict(t=1961.01, top="1/3", t2="事故", c=J.ALERT, big=True)])),
    ),

    # ── c123 使ったのは寿命の4割 ────────────────────────
    # 割合は「運転量 ÷ 寿命」の定義そのものなので、直線で描いてよい（作り物ではない）。
    "c123": dict(
        t="燃料は、半分も使っていない",
        s="事故までの運転量（p.3）　単位は MWD（メガワット日）",
        fig=("graph", dict(
            series=[dict(pts=[(0, 0), (931.5, 40.5)], t="使ったぶん",
                         c=J.AMBER, sw=6)],
            # ⚠️ ylab を「寿命に対する割合（%）」にすると左端が -125 で画面外に出る
            #    （`check_layout` が実測）。「寿命の何%か」でもまだ 25 で出る。4字まで詰める
            xr=(0, 2300), yr=(0, 100), xlab="運転量（MWD）", ylab="寿命の%",
            xticks=[(0, "0"), (931.5, "931.5"), (2300, "寿命")],
            yticks=[(0, "0"), (40.5, "40.5"), (100, "100")],
            band=[dict(a=931.5, b=2300, t="使っていないぶん", c=J.LINE_DIM)],
            marks=[dict(x=931.5, y=40.5, t="事故の時点", c=J.ALERT, dx=-140,
                        dy=-30)],
            note="割合は、運転量を寿命で割った値")),
    ),
}
