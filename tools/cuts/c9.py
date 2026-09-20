# -*- coding: utf-8 -*-
"""第9章 502人 c901–c916（16カット）。10本目（三豊百貨店）。

■ 写真は8カット。公共ヌリ（手直し可）は `mourning_01`（c901）・`rescue_work_19`（c903）・
  `officials_visit_02`（c911）の3点。残り5点は CC BY-SA ＝額装だけ。
■ 🔴🔴 `rescue_work_19`（c903）は**並んだ袋が写る**。`cuts/ss.py` の `RESTRICTED` が
  救助・行方不明を語るカットだけに許している点で、c903 はその1つ。
  **副題で中身を断定しない**（原本に説明が無い）。⚠️ ⑤c で原寸を見て写り方を確かめる。
■ ⚠️ `site_cleanup_03`（c905）・`ambulance_line_04`（c915）は**人も袋も写らない**点を選んである。
  「1人あたり3億8千万ウォン」の下に、お金と遺体を並べないため（→ `ref/ep10/photos.md` §0-2）。
■ ⚠️ `officials_visit_02`（c911）は**市議会の議長団**。市長と書かない。
■ ⚠️ `street_cordon_05`（c908）は**右手前の兵士が大きい**＝「遠景」と書かない。
■ 🔴 c907 は**字幕が言った2つの年代だけ**を出す。21〜30歳の258人は c909 の決め所で出す
  （図が台本より先に答えを出すと、決め所が死ぬ）。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC_H93 = "白書 p93"
# ⚠️ 「1995年10月」＋「国政監査」は字幕の1文に**2か所で割れて一致する**（実測87%）。
#    年月は副題が持っているので、出典は資料の頁だけを名乗る。
SRC_KOKKAN = "国政監査の資料 p.24・p.105"

SPEC = {

    "c901": dict(
        t="区民会館に、焼香所ができた",
        s="合同焼香所の幕と、白菊　1995年撮影",
        photo=P("mourning_01"), **ss.kind(P("mourning_01")),
    ),

    "c902": dict(
        t="10月の時点では、501人",
        s="1995年10月の報告",
        fig=("breakdown", dict(
            total=501,
            parts=[dict(v=471, t="遺体が見つかった人", c=J.LINE),
                   dict(v=30, t="死亡と認められた人", c=J.AMBER)],
            unit="人", note=SRC_KOKKAN)),
    ),

    # ⚠️ 並んだ袋が写る点。**中身を断定しない**。
    "c903": dict(
        t="そのままでは、数えられない",
        s="現場に立つ軍と隊員　1995年撮影",
        photo=P("rescue_work_19"), **ss.kind(P("rescue_work_19")),
    ),

    "c904": dict(
        t="委員会が、いったん扱いを決める",
        s="死亡と認めるまでの手順",
        fig=("process", dict(
            steps=[dict(t="16人の委員会", d="つくられる", c=J.INST),
                   dict(t="届け出 70人", d="そのうち", c=J.LINE),
                   dict(t="64人", d="死亡として扱う", c=J.AMBER),
                   dict(t="34人", d="鑑定で判明", c=J.OK)],
            note=SRC_KOKKAN)),
    ),

    "c905": dict(
        t="11月29日に、確定した",
        s="クレーンと、青いコンテナ　1995年撮影",
        photo=P("site_cleanup_03"), panel=True,
    ),

    # 1,439 は白書が印字している数（こちらで足した数ではない）。
    "c906": dict(
        t="最後に確定した数",
        s="白書が示した内訳",
        fig=("breakdown", dict(
            total=1439,
            parts=[dict(v=502, t="亡くなった人", c=J.ALERT),
                   dict(v=937, t="けがをした人", c=J.AMBER)],
            unit="人", note="10月の報告との差1人は、資料では埋まらない　白書 p92")),
    ),

    # 🔴 字幕が言った2つの年代だけ。21〜30歳は c909 の決め所で出す。
    "c907": dict(
        t="下の年代から見ていく",
        s="年代ごとの人数",
        fig=("compare", dict(
            items=[dict(v=14, t="10歳まで", disp="14", c=J.LINE),
                   dict(v=71, t="11〜20歳", disp="71", c=J.AMBER)],
            unit="人", vmax=100, note=SRC_H93)),
    ),

    # ⚠️「遠景」と書かない（右手前の兵士が大きい）。
    "c908": dict(
        t="どの年代にも、広がっている",
        s="消防車の列と、手前の兵士　1995年撮影",
        photo=P("street_cordon_05"), panel=True,
    ),

    "c909": dict(
        t="いちばん多かった年代",
        s="白書に載っている年齢の内訳",
        fig=("quote", dict(
            phrase="502人のうち258人が21歳から30歳",
            rows=[("どの年代", "21歳から30歳", J.ALERT),
                  ("何を数えた", "亡くなった人の年齢", J.INK_W),
                  ("書かれていた文書", "白書 p93", J.DOC)],
            paper=True)),
    ),

    "c910": dict(
        t="女性が、396人",
        s="亡くなった502人の男女の別",
        fig=("breakdown", dict(
            total=502,
            parts=[dict(v=106, t="男性", c=J.LINE),
                   dict(v=396, t="女性", c=J.AMBER)],
            unit="人", note=SRC_H93)),
    ),

    # ⚠️ 市長ではなく**市議会の議長団**。
    "c911": dict(
        t="白書が挙げた、一つめ",
        s="現場を訪れた市議会の議長団　1995年撮影",
        photo=P("officials_visit_02"), **ss.kind(P("officials_visit_02")),
    ),

    # 🔴 2026-09-20（⑤c'）：c912／c913 の副題が「休む隊員」で同じだった（別の写真）。
    #    実見の違い（瓦礫の上に**座り込む** ／ 手を止めている）で書き分ける。
    "c912": dict(
        t="二つめは、崩れた時刻",
        s="瓦礫の上に座り込む隊員　1995年撮影",
        photo=P("rescue_work_20"), panel=True,
    ),

    "c913": dict(
        t="話し合いは、翌年3月にまとまった",
        s="手を止めている隊員たち　1995年撮影",
        photo=P("rescue_work_11"), panel=True,
    ),

    # ⚠️ 分母が違う（502 と 937）ので**棒で並べない**。数のまま置く。
    "c914": dict(
        t="支払いが終わった人数",
        s="1996年6月の集計",
        fig=("panel", dict(
            blocks=[dict(k="亡くなった人", t="502人のうち", v="464人", c=J.AMBER),
                    dict(k="けがをした人", t="937人のうち", v="709人", c=J.AMBER)],
            cols=2, note=SRC_H93)),
    ),

    # ⚠️ 人も袋も写らない点。お金の話の下に遺体を並べないため。
    # 🔴 2026-09-20（⑤c'）：`ep01` と副題の後半が同じだった（別の写真）。
    #    こちらは**残った棟が写る**点なので、そこで書き分ける。
    "c915": dict(
        t="1人あたり、3億8千万ウォン",
        s="残った棟の前に並ぶ救急車　1995年撮影",
        photo=P("ambulance_line_04"), panel=True,
    ),

    "c916": dict(
        t="最後に、責任の話をする",
        s="ここまでと、この先",
        fig=("panel", dict(
            blocks=[dict(k="ここまで", t="502人の内訳", v="第9章", c=J.LINE),
                    dict(k="次に見ること", t="だれが、何を問われたか", v="締め",
                         c=J.ALERT)],
            cols=2, note="大法院 1996年8月23日 判決（刑事）")),
    ),

}
