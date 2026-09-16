# -*- coding: utf-8 -*-
"""第4章 燃料を足すという判断 c401–c420（20カット）。9本目（テネリフェ）。

■ 台本の写真8カットのうち2カットを図にし、地に写真を敷いた（写真映像の数は変わらない）
  - c416 … 短波の無線でアムステルダムにつなぐ＝地図。地に `klm_747_1973_01` の寄り（BACKDROP）
  - c420 … 給油の30分＝時間の図。地に `klm_747_1971_01`（BACKDROP）
  ⚠️ `schiphol_1977_02` は旅券審査の大きな案内板（オランダ語）と歩く人の顔＝地にも敷かない
    （焼き込みの文字は地に敷くと `check_slide` が参考に落として鳴らない）。
■ 同じ章で見せ方が続かないように、c411（前と後）→ c413（時間軸）→ c414（無い）と替えた。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SPEC = {

    "c401": dict(
        t="KLMは、燃料を足すと伝えた",
        s="KLMの747（雨の駐機場）　1973年撮影",
        photo=P("klm_747_1973_01"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("klm_747_1973_01")),
        ann=[dict(t="かかる時間", v="約30分", vc=J.AMBER, vs=96)],
    ),

    "c402": dict(
        t="30分は、短くない",
        s="前の機体と、うしろの機体",
        fig=("process", dict(
            steps=[dict(t="前のKLM機", v="30分", d="給油で止まる", c=J.AMBER),
                   dict(t="うしろのパンナム機", v="30分", d="動けない", c=J.ALERT)],
            note="事故報告書 p28")),
    ),

    # 右端に展示パネルの英字（x≥0.85）＝左へ寄って外へ出す。
    "c403": dict(
        t="量だけでは、多いか分からない",
        s="747に使われたエンジン（博物館）　2017年撮影",
        photo=P("engine_747_02"), bias=0.55, xbias=0.20, zoom=1.25,
        side="right", ann_y=330,
        **ss.kind(P("engine_747_02")),
        ann=[dict(t="入れた燃料", v="55,500リットル", vc=J.AMBER, vs=64),
             dict(t="多いかどうかは", d="行き先までの距離", dc=J.INK_W, ds=32)],
    ),

    "c404": dict(
        t="乗客を乗せたまま、給油した",
        s="ターミナルへ戻ったKLMの乗客",
        fig=("beforeafter", dict(
            a=dict(k="給油の前", t="ターミナル", lines=["いったん降りていた"], c=J.LINE),
            b=dict(k="給油のあいだ", t="機内の席", lines=["もう一度座って待つ"], c=J.AMBER),
            note="事故報告書 p28")),
    ),

    "c405": dict(
        t="ラスパルマスまで、およそ25分",
        s="現在のグランカナリア空港　2012年撮影",
        photo=P("laspalmas_now_13"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("laspalmas_now_13")),
        ann=[dict(t="テネリフェからの飛行", v="約25分", vc=J.INK_W, vs=92),
             dict(t="入れた燃料", v="55,500リットル", vc=J.ALERT, vs=64)],
    ),

    "c406": dict(
        t="報告書が考えた理由",
        s="テネリフェでの給油について",
        fig=("people", dict(
            nodes=[dict(x=0.18, y=0.40, t="KLMの機長", d="", c=J.INK_W, kind="person"),
                   dict(x=0.78, y=0.40, t="ラスパルマスでの給油", d="避けたかった",
                        c=J.ALERT, kind="org")],
            edges=[dict(a=0, b=1, t="報告書の見方", c=J.DOC)],
            note="事故報告書 p28")),
    ),

    # 下半分に機体のロゴ（transavia.com・TUIfly）＝上へ寄せる。
    "c407": dict(
        t="集まった機体で、給油も混む",
        s="現在のグランカナリア空港の駐機場　2013年撮影",
        photo=P("laspalmas_now_12"), bias=0.25, side="right", ann_y=356,
        **ss.kind(P("laspalmas_now_12")),
        ann=[dict(t="だから", d="先に入れておく", dc=J.AMBER, ds=44)],
    ),

    # 🔴 テネリフェはラスパルマスの北西（左上）。アムステルダムは北東。
    "c408": dict(
        t="アムステルダムまで戻れる量",
        s="入れた燃料で飛べたところ",
        fig=("mapfig", dict(
            points=[dict(x=0.14, y=0.80, t="テネリフェ", d="ここで入れた", c=J.INK_W,
                         side="left"),
                    dict(x=0.26, y=0.88, t="ラスパルマス", d="入れ直さなくてよい",
                         c=J.AMBER, side="right"),
                    dict(x=0.84, y=0.10, t="アムステルダム", d="そのまま戻れた", c=J.OK)],
            link=(1, 2), scale="報告書が確かめた量",
            note="上が北・右が東（縮尺と位置は正確ではない）　事故報告書 p28")),
    ),

    "c409": dict(
        t="もう一つの時計",
        s="KLMの展示会の747の客室の模型　1969年撮影",
        # 🔴 check_slide G-10：全画面だと焼き込みの「KLM BOEING 747B」が画面の端で切れた＝額装で切らない
        photo=P("jumbo_era_03"), panel=True, side="right", ann_y=356,
        ann=[dict(t="上限があるもの", d="乗員が働いていい時間", dc=J.AMBER, ds=36)],
    ),

    "c410": dict(
        t="働ける時間には、上限がある",
        s="乗員の乗務時間の決まり",
        fig=("panel", dict(
            blocks=[dict(k="上限", t="続けて働ける時間", v="", c=J.INK_W),
                    dict(k="目的", t="疲れを避ける", v="", c=J.OK),
                    dict(k="オランダ", t="決まりが変わったばかり", v="", c=J.ALERT)],
            note="事故報告書 p26", cols=3)),
    ),

    "c411": dict(
        t="以前は、上限に融通がきいた",
        s="オランダの乗務時間の決まり",
        fig=("beforeafter", dict(
            a=dict(k="変わる前", t="延ばせた", lines=["機長の判断で", "目的地まで飛びきる"],
                   c=J.LINE),
            b=dict(k="変わったあと", t="延ばせない", lines=["超えることは禁止"], c=J.ALERT),
            note="事故報告書 p26")),
    ),

    "c412": dict(
        t="一切、延ばせなくなった",
        s="変わったあとの決まり",
        fig=("quote", dict(
            phrase="超えたら、法律で裁かれる",
            rows=[("決まり", "オランダの乗務時間の上限", J.INK_W),
                  ("変わったあと", "機長が上限を超えることは禁止", J.ALERT),
                  ("出どころ", "事故報告書 p26", J.DOC)],
            paper=True)),
    ),

    "c413": dict(
        t="計算の決まりも変わった",
        s="上限の計算の決まり",
        fig=("timeline", dict(
            events=[dict(t=1976.95, top="1976年12月", t2="ここまでは簡単な計算",
                         c=J.OK, big=True, up=True),
                    dict(t=1977.24, top="1977年3月27日", t2="この日", c=J.AMBER,
                         big=True, up=False)],
            t0=1976.55, t1=1977.45,
            ticks=[(1977.0, "1977年")],
            band=[dict(a=1976.55, b=1976.95, t="見る項目が少ない", c=J.OK)],
            src="事故報告書 p26")),
    ),

    "c414": dict(
        t="自分の上限を、自分で出せない",
        s="1976年12月からの計算",
        fig=("absent", dict(
            mode="single",
            items=[dict(t="操縦室で出す上限", d="事実上、決められない", ok=False,
                        c=J.ALERT)],
            lead="とても複雑になった計算", note="事故報告書 p26")),
    ),

    "c415": dict(
        t="会社に問い合わせるしかない",
        s="上限を知る方法",
        fig=("people", dict(
            nodes=[dict(x=0.16, y=0.40, t="機長", d="テネリフェ", c=J.INK_W, kind="person"),
                   dict(x=0.80, y=0.40, t="KLMの運航の部署", d="アムステルダム",
                        c=J.INST, kind="org")],
            edges=[dict(a=0, b=1, t="あと何分働けるか", c=J.AMBER)],
            note="事故報告書 p26　問い合わせることが強くすすめられていた")),
    ),

    # 図＋地（BACKDROP＝klm_747_1973_01 の寄り）
    "c416": dict(
        t="テネリフェから、アムステルダムへ",
        s="機長がつないだ先",
        fig=("mapfig", dict(
            points=[dict(x=0.16, y=0.84, t="テネリフェ", d="KLMの機長", c=J.INK_W),
                    dict(x=0.84, y=0.12, t="アムステルダム", d="KLMの運航の部署", c=J.INST)],
            link=(0, 1), scale="短波の無線",
            note="上が北・右が東（縮尺は正確ではない）　事故報告書 p26")),
    ),

    "c417": dict(
        t="答えは、はっきりしなかった",
        s="会社から返ってきた答え",
        fig=("absent", dict(
            mode="ledger",
            items=[dict(t="答え", d="時刻しだいで、たぶん大丈夫", ok=True,
                        c=J.INK_W),
                   dict(t="境目の時刻", d="報告書に残っていない", ok=False, c=J.TICK)],
            note="事故報告書 p26")),
    ),

    "c418": dict(
        t="危ないと分かるのは、着いたあと",
        s="危なかった場合の知らせ方",
        fig=("process", dict(
            steps=[dict(t="危なければ", d="電報を送る", c=J.ALERT),
                   dict(t="送り先", d="ラスパルマス（行った先）", c=J.LINE),
                   dict(t="機長", d="上限を知らないまま出発", c=J.AMBER)],
            note="事故報告書 p26")),
    ),

    "c419": dict(
        t="上限の不確かさは、心理に響いた",
        s="スキポールからローマへ飛ぶ747の操縦室　1971年撮影",
        photo=P("cockpit_747_04"), side="right", ann_y=356,
        **ss.kind(P("cockpit_747_04")),
        ann=[dict(t="報告書が挙げたもの", d="限界を決められない不確かさ", dc=J.DOC, ds=32)],
    ),

    # 図＋地（BACKDROP＝klm_747_1971_01 の寄り。c102 と別の絵にする）
    "c420": dict(
        t="あとで数え直される、30分",
        s="出発の準備がそろったとき",
        fig=("moment", dict(
            clock="30分", label="給油に使った時間",
            facts=[dict(t="燃料", v="入った", c=J.OK),
                   dict(t="乗客", v="席に戻った", c=J.INK_W)],
            sub="事故報告書 p28")),
    ),
}
