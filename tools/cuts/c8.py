# -*- coding: utf-8 -*-
"""第8章 十七日間 c801–c822（22カット）。10本目（三豊百貨店）。

■ 写真は17カット（77%）。**この章は現場の記録そのものが素材になる章**。
  公共ヌリ（手直し可）は `missing_board_01`（c810）・`officials_visit_01`（c818）・
  `site_cleanup_01`（c820）の3点。残り14点は CC BY-SA ＝額装だけ。
■ 🔴🔴 `missing_board_01`（c810）は **私人の顔写真と名前が写っている**。
  **ぼかしてから焼く**（公共ヌリ第1類型＝手直し可）。ぼかす範囲は⑤cで原寸を見て決める。
  ⚠️ **`blur=` は cut の書き方として実装されていない**＝元画像そのものを直す。
  → 黙って素のまま焼かないように `tools/check_photo_mask.py` を新設した（`qa_all` に載せてある）。
  ⚠️ `tools/check_mask.py` は**音**（語尾が BGM に埋もれていないか）の検査。名前が似ているが別物。
■ ⚠️ `rescue_work_02`（c817）は**布を掛けたものを大勢で運び出す場面**。
  原本は中身を書いていない＝**副題で断定しない**（→ `ref/ep10/photos.md` §4）。
■ ⚠️ `officials_visit_01`（c818）は **7月1日に就任した新しい市長**。
  事故の日の市長とは**別人**なので、副題で「事故の日の市長」と書かない。
■ ⚠️ `night_work_02` は**記念写真**なので使っていない（c808・c816 は別の点）。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC_SI = "ソウル市の報告"
SRC_HAKU643 = "白書 p643"

SPEC = {

    "c801": dict(
        t="消防と警察が、すぐ向かった",
        s="消防車の列と、軍　1995年撮影",
        photo=P("street_cordon_02"), panel=True,
    ),

    # 🔴 字幕が「写真が残っている」と言っている、その写真そのもの。
    "c802": dict(
        t="のべ1,176台が入った",
        s="道路を埋めた救急車　1995年撮影",
        photo=P("ambulance_line_06"), panel=True,
    ),

    "c803": dict(
        t="歩いて、いる場所を探す",
        s="瓦礫の斜面に立つ大勢　1995年撮影",
        photo=P("rescue_work_10"), panel=True,
    ),

    "c804": dict(
        t="その日の夜に、動いたもの",
        s="1995年6月29日　夕方から夜へ",
        fig=("timeline", dict(
            events=[dict(t=17.917, top="17:55", t2="崩落", c=J.ALERT, big=True),
                    dict(t=18.0, top="18:00", t2="市の対策本部", c=J.INST),
                    dict(t=18.333, top="18:20", t2="現場の指揮本部", c=J.INST),
                    dict(t=18.833, top="18:50ごろ", t2="市長が現場へ", c=J.AMBER)],
            t0=17.80, t1=19.3,
            # ⚠️ 目盛りと旗の `top` に同じ「18:00」を置くと `check_dup` が鳴る。
            ticks=[(18.5, "18:30"), (19, "19:00")],
            src=SRC_SI + " p.35・瑞草区の報告 p.42")),
    ),

    "c805": dict(
        t="重機を止めて、手作業に",
        s="瓦礫を手で掘る隊員　1995年撮影",
        photo=P("rescue_work_09"), panel=True,
    ),

    "c806": dict(
        t="手伝いに来た人たちもいた",
        s="物資を運ぶ人と、支援の幕　1995年撮影",
        photo=P("volunteers_01"), panel=True,
    ),

    "c807": dict(
        t="のべ68,808人が入った",
        s="片付けにあたる軍　1995年撮影",
        photo=P("rescue_work_21"), panel=True,
    ),

    "c808": dict(
        t="夜も、作業は止まらない",
        s="夜、照らされたクレーンと警察　1995年撮影",
        photo=P("night_work_01"), panel=True,
    ),

    "c809": dict(
        t="一帯が、特別災害地域に",
        s="瓦礫の上に立つ大勢　1995年撮影",
        photo=P("rescue_work_12"), panel=True,
    ),

    # 🔴🔴 私人の顔写真と名前が写る。**隠してから焼く**（`qa_out/ep10_remask.py`）。
    # 🔴 2026-09-20（⑤c'）：σ=8 の全面ぼかしから**モザイク14px**に替えた。
    #    ぼかしだと、デュオトーンに落ちたときに貼り紙の輪郭まで消えて
    #    「灰色のもや」になっていた（⑤c の所見）。理由と実測は道具の docstring に。
    "c810": dict(
        t="家族が、貼り紙を貼っていった",
        s="名前と顔写真の貼り紙（個人のわかる部分を隠しています）　1995年撮影",
        photo=P("missing_board_01"), **ss.kind(P("missing_board_01")),
    ),

    "c811": dict(
        t="1日のうちに、訂正された",
        s="行方が分からない人の数",
        fig=("compare", dict(
            items=[dict(v=207, t="はじめの発表", disp="207", c=J.LINE),
                   dict(v=410, t="同じ日の訂正", disp="410", c=J.ALERT)],
            unit="人", vmax=450,
            note="届け出の窓口が2か所に分かれていた　国政調査結果報告書 p.32")),
    ),

    "c812": dict(
        t="230時間後に、1人",
        s="構造材の下の隊員と、濃い煙　1995年撮影",
        photo=P("rescue_work_16"), panel=True,
    ),

    "c813": dict(
        t="2日後、もう1人",
        s="崩落した屋内のはしごと、隊員　1995年撮影",
        photo=P("rescue_work_15"), panel=True,
    ),

    "c814": dict(
        t="17日目に、もう一人",
        s="1995年7月15日",
        fig=("quote", dict(
            phrase="377時間ぶりに、生きて助け出された",
            rows=[("いつ", "1995年7月15日（事故から17日目）", J.AMBER),
                  ("だれが書いた", "ソウル特別市", J.INST),
                  ("書かれていた文書", "白書 p643", J.DOC)],
            paper=True)),
    ),

    # 🔴 2026-09-20（⑤c'）：`ep06` と副題が同じ言い方だった（別の写真）。
    #    こちらは背中の「119구조대」の字が読める点なので、そこで書き分ける。
    "c815": dict(
        t="伝えるのは、人数と時間だけ",
        s="119救助隊の字が見える隊員　1995年撮影",
        photo=P("rescue_work_03"), panel=True,
    ),

    "c816": dict(
        t="ここから先は、別の作業",
        s="夜の切断作業と、火花　1995年撮影",
        photo=P("rescue_work_06"), panel=True,
    ),

    # ⚠️ 運び出しているものの中身は原本に無い＝**副題で断定しない**。
    "c817": dict(
        t="救助932人、遺体459人",
        s="大勢で運び出す場面　1995年撮影",
        photo=P("rescue_work_02"), panel=True,
    ),

    # ⚠️ 事故の日の市長とは**別人**（7月1日に就任）。
    "c818": dict(
        t="新しい市長が、その日に来た",
        s="現場を訪れた新しい市長　1995年撮影",
        photo=P("officials_visit_01"), **ss.kind(P("officials_visit_01")),
    ),

    # ⚠️ 3つの数は**足さない**（合算した数を大きく出さない）。並べるだけ。
    "c819": dict(
        t="数は、まだ動いていた",
        s="1995年7月27日の時点",
        fig=("panel", dict(
            # ⚠️ `panel` の段は `t` が必須（`k` は省ける）。`t` を落とすと KeyError で落ちる。
            blocks=[dict(t="亡くなった人", v="458人", c=J.ALERT),
                    dict(t="けがをした人", v="933人", c=J.AMBER),
                    dict(t="行方が分からない人", v="およそ105人", c=J.TICK)],
            cols=3, note="K6-検 p.45")),
    ),

    "c820": dict(
        t="同じ人を、別々に届けていた",
        s="重機が並ぶ現場の俯瞰　1995年撮影",
        photo=P("site_cleanup_01"), **ss.kind(P("site_cleanup_01")),
    ),

    "c821": dict(
        t="30,892トンが、運び出された",
        s="クレーンの網カゴで運ぶ瓦礫　1995年撮影",
        photo=P("site_cleanup_05"), panel=True,
    ),

    "c822": dict(
        t="最後の数字は、5か月後",
        s="ここまでと、この先",
        fig=("panel", dict(
            blocks=[dict(k="ここまで", t="十七日間の捜索", v="第8章", c=J.LINE),
                    dict(k="次に見ること", t="502人の内訳", v="第9章", c=J.ALERT)],
            cols=2, note="白書 p92")),
    ),

}
