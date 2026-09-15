# -*- coding: utf-8 -*-
"""第8章「テキサスに降ってきたもの」c801–c820（20カット）。8本目（コロンビア号）。

■ この章が渡すもの
  **拾い集めた人たちの話。**そして、落ちた場所の規則から**壊れた順が読めた**こと。
  第3章で絞り込んだ「8枚目」が、ここでもう一度出てくる。

■ 🔴 写真8カット＋地に敷く3カット（`c5` `c6` で落ちたぶんをここで取り返す）
  c803 `evidence_corsicana`／c805 `search_brief`／c806 `search_line`／c808 `engine_dig`／
  c811 `barksdale`／c813 `hangar_grid`／c815 `le_fixture`／c817 `oex_recorder`
  地に敷く＝c807 `search_queue`／c814 `hangar_floor`／c816 `hangar_caib`

■ ⚠️ `engine_dig` と `engine_found` は**右下に黄色い撮影日が焼き込まれている**
  （"30.03 2003" / "01.04 2003"）。全画面では `bias` を下げて枠の外へ出す。

■ ⚠️ `oex_recorder` は c707 と同じ写真（**1988年の同型**）。ここは寄りと側を変える。
  副題で必ず年を名乗る。→ [[feedback-fallback-stills-must-match-the-era]]
"""
import jiko_style as J
import cuts.ss as ss

SPEC = {

    # ── c801 🔴 橋のカット ────────────────────────────────
    "c801": dict(
        t="散らばった先は、県ひとつぶん",
        s="落ちた範囲の広さを、県の大きさで見る",
        fig=("panel", dict(
            blocks=[dict(k="散った範囲", t="テキサス州だけで",
                         v="5,180平方キロ超", c=J.ALERT),
                    dict(k="たとえると", t="千葉県がまるごと", v="入る広さ",
                         c=J.TICK)],
            note="事故調査委員会報告 p44・p45", cols=2)),
    ),

    # ── c802 通報 ─────────────────────────────────────────
    "c802": dict(
        t="夕方には、1分に18件",
        s="通報が入る速さ（1分あたりの件数）",
        fig=("icons", dict(
            n=18, on=18, kind="dot", cols=6, oncol=J.ALERT,
            note="事故調査委員会報告 p44")),
    ),

    # ── c803 触らないでほしい ─────────────────────────────
    "c803": dict(
        t="手を触れてはいけない",
        s="回収された破片（テキサス州コルシカナの拠点）",
        photo=ss.EVIDENCE_CORSICANA, bias=0.50, side="right", ann_y=356,
        **ss.kind(ss.EVIDENCE_CORSICANA),
        ann=[dict(t="呼びかけ", d="破片に手を触れないこと", dc=J.ALERT, ds=34),
             dict(t="理由", d="肺や皮膚を焼く燃料", dc=J.ALERT, ds=30)],
    ),

    # ── c804 濃く落ちた帯 ─────────────────────────────────
    "c804": dict(
        t="濃い帯は、南から東へ伸びた",
        s="破片が濃く落ちた帯",
        fig=("mapfig", dict(
            points=[dict(x=0.12, y=0.30, t="リトルフィールド",
                         d="いちばん西・耐熱タイル1枚", c=J.AMBER),
                    dict(x=0.42, y=0.44, t="フォートワースの南",
                         d="濃い帯の始まり", c=J.ALERT),
                    dict(x=0.86, y=0.62, t="ルイジアナ", d="濃い帯の終わり",
                         c=J.ALERT)],
            link=(1, 2),
            note="事故調査委員会報告 p45・p47　上が北・右が東（縮尺は正確ではない）")),
    ),

    # ── c805 捜索に入る ───────────────────────────────────
    "c805": dict(
        t="全米から、消防隊員が入った",
        s="捜索に入る前の説明",
        photo=ss.SEARCH_BRIEF, bias=0.46, side="right", ann_y=356,
        **ss.kind(ss.SEARCH_BRIEF),
        ann=[dict(t="2週間で", v="3千人", vc=J.AMBER, vs=96),
             dict(t="1か月で", v="4千人超", vc=J.AMBER, vs=96),
             dict(t="主力", d="森林火災の消防隊員", dc=J.LINE, ds=30)],
    ),

    # ── c806 列を組んで歩く ───────────────────────────────
    "c806": dict(
        t="見落とさないための、間隔だった",
        s="列を組んで歩く捜索",
        photo=ss.SEARCH_LINE, bias=0.46, side="right", ann_y=356,
        **ss.kind(ss.SEARCH_LINE),
        ann=[dict(t="ひと組", v="20人", vc=J.AMBER, vs=96),
             dict(t="列の間隔", v="3メートル", vc=J.AMBER, vs=96),
             dict(t="15センチ四方の物なら", v="75パーセント", vc=J.OK, vs=72)],
    ),

    # ── c807 歩いた面積 ───────────────────────────────────
    # 🔴 地に敷く写真＝`search_queue`（BACKDROP）。
    "c807": dict(
        t="歩いた広さは、全体の3割",
        s="当たった広さのうち、歩いた割合",
        fig=("breakdown", dict(
            total=10, unit="割",
            parts=[dict(v=3, t="歩いて捜した", c=J.AMBER)],
            note="事故調査委員会報告 p47・p224　"
                 "270機関・2万5千人以上・延べ150万時間")),
    ),

    # ── c808 沼と藪 ───────────────────────────────────────
    # ⚠️ 右下に黄色い撮影日が焼き込まれている。`bias` を下げて枠の外へ出す。
    "c808": dict(
        t="歩けない場所を、歩いた",
        s="東テキサスの捜索現場",
        photo=ss.ENGINE_DIG, bias=0.20, side="right", ann_y=356,
        **ss.kind(ss.ENGINE_DIG),
        ann=[dict(t="地面は", d="蛇のいる沼。泥の川底", dc=J.ALERT, ds=34),
             dict(t="藪では", d="朝いっぱいで百メートル", dc=J.ALERT, ds=32)],
    ),

    # ── c809 空からの捜索 ─────────────────────────────────
    "c809": dict(
        t="空からも、44機が出た",
        s="空から捜索に出た機数",
        fig=("compare", dict(
            items=[dict(v=37, t="ヘリコプター", disp="37", unit="機", c=J.LINE),
                   dict(v=7, t="固定翼機", disp="7", unit="機", c=J.LINE)],
            vmax=40,
            ref="1機が落ちて、2人が亡くなった",
            note="事故調査委員会報告 p46　ジュールズ・マイア／"
                 "チャールズ・クレネク")),
    ),

    # ── c810 湖の底 ───────────────────────────────────────
    "c810": dict(
        t="それだけやって、拾えたのは",
        s="湖の底を探した範囲と、その結果",
        fig=("panel", dict(
            blocks=[dict(k="ソナーで調べた広さ", t="湖の底", v="80平方キロ超",
                         c=J.LINE),
                    dict(k="潜った人", t="視界は数センチ", v="60人",
                         c=J.AMBER),
                    dict(k="拾えたもの", t="別の湖で", v="1点", c=J.ALERT)],
            note="事故調査委員会報告 p46")),
    ),

    # ── c811 集積所 ───────────────────────────────────────
    "c811": dict(
        t="一点ずつ、記録してから運んだ",
        s="破片の集積所",
        photo=ss.BARKSDALE, bias=0.50, side="right", ann_y=356,
        **ss.kind(ss.BARKSDALE),
        ann=[dict(t="運ぶ前にしたこと", d="位置の記録と写真", dc=J.DOC, ds=32),
             dict(t="回収された数", v="83,900点", vc=J.AMBER, vs=88)],
    ),

    # ── c812 決め所13件目 ─────────────────────────────────
    "c812": dict(
        t="並べてみたら、順番が見えた",
        s="この読み取りの出どころ",
        fig=("quote", dict(
            phrase="西の物ほど、先に離れた",
            who="事故調査委員会",
            when="2003年8月の報告",
            doc="事故調査委員会報告 p74・p75",
            ctx="破片の並びが示したこと")),
    ),

    # ── c813 格納庫 ───────────────────────────────────────
    "c813": dict(
        t="機体の形のまま、床に並べた",
        s="ケネディ宇宙センターの格納庫",
        photo=ss.HANGAR_GRID, bias=0.52, side="right", ann_y=356,
        **ss.kind(ss.HANGAR_GRID),
        ann=[dict(t="床にしたこと", d="テープを貼って区画を作る", dc=J.LINE,
                  ds=34),
             dict(t="置き方", d="元あった場所の近く", dc=J.OK, ds=34)],
    ),

    # ── c814 左の翼だけが足りない ─────────────────────────
    # 🔴 地に敷く写真＝`hangar_floor`（BACKDROP）。
    # 🔴 対比なので `arrow=False`。
    "c814": dict(
        t="左の翼だけが、足りない",
        s="右の翼と左の翼で、見つかり方がどう違ったか",
        fig=("beforeafter", dict(
            a=dict(k="右の翼", t="破片は多く見つかった",
                   lines=["左の翼より、ずっと多い"], c=J.OK),
            b=dict(k="左の翼", t="少ない",
                   lines=["外側のパネルほど西", "内側のパネルはずっと東"],
                   c=J.ALERT),
            arrow=False, note="事故調査委員会報告 p73・p74")),
    ),

    # ── c815 左翼前縁の再構成 ─────────────────────────────
    "c815": dict(
        t="8枚目の破片だけ、散り方が違った",
        s="翼の前のふちを並べる治具",
        photo=ss.LE_FIXTURE, side="right", ann_y=300,
        **ss.kind(ss.LE_FIXTURE),
        ann=[dict(t="いちばん西の耐熱タイル", d="8枚目と9枚目の真後ろ",
                  dc=J.AMBER, ds=30),
             dict(t="8枚目のパネルの破片", d="帯の端から端まで",
                  dc=J.ALERT, ds=30)],
    ),

    # ── c816 散り方が示したこと ───────────────────────────
    # 🔴 地に敷く写真＝`hangar_caib`（BACKDROP）。
    "c816": dict(
        t="散り方が、壊れた順を教えた",
        s="落ちた場所から壊れた順を読む",
        fig=("process", dict(
            steps=[dict(t="落ちた場所に規則がある", d="西の物ほど先に離れた",
                        c=J.LINE),
                   dict(t="当てはめる", d="壊れた順が読める", c=J.AMBER),
                   dict(t="読めたこと", d="左の翼の8枚目のあたり", c=J.ALERT)],
            note="事故調査委員会報告 p75・p78")),
    ),

    # ── c817 記録装置の回収 ───────────────────────────────
    # ⚠️ c707 と同じ写真（1988年の同型）。寄りと側を変える。
    "c817": dict(
        t="3月19日、記録装置が出てきた",
        s="同型の記録装置　1988年撮影",
        photo=ss.OEX_RECORDER, side="left", ann_y=300,
        **ss.kind(ss.OEX_RECORDER),
        ann=[dict(t="見つかった場所", d="テキサス州ヘンフィル",
                  dc=J.INK_W, ds=32),
             dict(t="状態", d="ほぼ無傷", dc=J.OK, ds=36),
             dict(t="ただし", d="落ちる力までは考えていない設計",
                  dc=J.TICK, ds=30)],
    ),

    # ── c818 テープに残っていたもの ───────────────────────
    "c818": dict(
        t="最後の最後まで、記録は続いた",
        s="テープに残っていたもの",
        fig=("panel", dict(
            blocks=[dict(k="残っていた値", t="センサの数", v="800個", c=J.AMBER),
                    dict(k="テープ", t="長さ", v="約2.9キロ", c=J.LINE),
                    dict(k="どこまで", t="電波が切れたあとの", v="14秒分",
                         c=J.ALERT)],
            note="事故調査委員会報告 p47")),
    ),

    # ── c819 破片を返す ───────────────────────────────────
    # 🔴 図。②の在庫に「破片を返しに来る人」は1点も無い（⑤b-1 §3-3）。
    "c819": dict(
        t="地上でけがをした人は、出なかった",
        s="破片をめぐって起きたこと／起きなかったこと",
        fig=("absent", dict(
            mode="ledger",
            items=[dict(t="罪に問わない期間", d="数日間もうけた", ok=True,
                        c=J.INST),
                   dict(t="賠償", d="約5万ドルにとどまった", ok=True, c=J.DOC),
                   dict(t="地上でけがをした人", d="出ていない", ok=False)],
            note="事故調査委員会報告 p47")),
    ),

    # ── c820 集めた重さ ───────────────────────────────────
    "c820": dict(
        t="集まったのは、38パーセント",
        s="機体の重さ（燃料と荷物を除く）に対する割合",
        fig=("breakdown", dict(
            total=100, unit="%",
            parts=[dict(v=38, t="集まった破片", c=J.AMBER)],
            note="事故調査委員会報告 p47・p224　合わせて約38,500キログラム")),
    ),
}
