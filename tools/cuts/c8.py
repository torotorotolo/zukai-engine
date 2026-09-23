# -*- coding: utf-8 -*-
"""第8章 日本に帰ってきた灰 c801–c820（20カット）。12本目（キャッスル・ブラボー）。⑤b-4（2026-09-23）で書いた。

■ 実写 5/20（写真3・報告書の頁2）。章の色＝セピア。
■ 出典は web の証拠（`ref/ep12/src/web_evidence_japan.md` の B1〜B8）の出どころを図の注に書く
   （国会会議録・都立第五福竜丸展示館・広島平和記念資料館・米国務省の外交文書 FRUS・杉並区）
■ c814・c815 は報告書の第16図（DNA p114 の上半分・ブラボーの前と後の警戒の区域が1枚に載っている）を**カメラで**見せる：
   c814 前の区域（エニウェトクとビキニを囲む長方形）の上を横へなぞる → c815 そこから引いて、広げられた扇形の区域を明かす。
   同じ写真には同じ副題（§5b-19）。⚠️ p114 の下の本文の段は第4章 c404（別の中身）
■ ⚠️ 実名は無線長の久保山愛吉さんだけ（台本 §1-2）。病床の写真は使わない（②で落とした）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
NOTE_KK4 = "出典：国会会議録（1954年）"
NOTE_D5F = "出典：都立第五福竜丸展示館ほか"
# 報告書の第16図（p114 の上半分）。前の区域の長方形の中ほど＝切ったあとの絵の (0.44, 0.56) あたり
FIG16 = dict(photo=ss.page(114), panel=True, trim=(0.10, 0.10, 0.93, 0.675))


SPEC = {

    # ⚠️ 副題「焼津に戻った乗組員」は字幕の文の切り取り（check_echo）／「戻った日の診察」は札と語が重なる（check_dup）
    "c801": dict(
        t="帰港の日",
        s="帰港した乗組員",
        fig=("moment", dict(
            clock="3月14日", label="1954年",
            facts=[dict(t="戻った日のうちに", v="焼津の病院で診察", c=J.AMBER)],
            sub=NOTE_KK4 + "ほか")),
    ),

    "c802": dict(
        t="東京で分かったこと",
        s="焼津から東京へ",
        fig=("process", dict(
            steps=[dict(t="焼津の病院", d="3月14日", c=J.LINE),
                   dict(t="東京大学の病院", d="3月15日・症状の重い人", c=J.AMBER),
                   dict(t="はっきりした", d="放射線を浴びている", c=J.ALERT)],
            note=NOTE_KK4 + "ほか")),
    ),

    "c803": dict(
        t="日本じゅうへ",
        s="新聞の報道",
        fig=("moment", dict(
            clock="3月16日", label="1954年",
            facts=[dict(t="伝えた新聞", v="読売新聞", c=J.AMBER),
                   dict(t="ビキニの灰", v="全国に知られる", c=J.ALERT)],
            sub=NOTE_KK4 + "ほか")),
    ),

    # 23人が2つの病院に分かれた（何人ずつかは台本に無い＝数を描かない）
    "c804": dict(
        t="2つの病院へ",
        s="入院した病院",
        fig=("people", dict(
            nodes=[dict(x=0.18, y=0.45, t="乗組員23人", d="3月の下旬に東京へ", kind="person", c=J.AMBER),
                   dict(x=0.78, y=0.22, t="東京大学の病院", d="入院", kind="org", c=J.INST),
                   dict(x=0.78, y=0.70, t="国立東京第一病院", d="入院", kind="org", c=J.INST)],
            edges=[dict(a=0, b=1, t="", c=J.LINE), dict(a=0, b=2, t="", c=J.LINE)],
            note=NOTE_KK4 + "ほか")),
    ),

    # Commons「Technical experts checking contamination」（公的な任務の技術者）
    "c805": dict(
        t="マグロにも、放射能",
        s="魚市場でマグロを調べる技術者　1954年",
        photo=P("jp_tuna_check"), **ss.kind(P("jp_tuna_check")),
        cam="pan_r",
        side="right", ann_y=330,
        ann=[dict(t="問題", d="人の体だけでなく", dc=J.TICK),
             dict(t="持ち帰ったマグロ", d="放射能を検出", dc=J.ALERT)],
    ),

    # 検査は3月18日から12月の終わりまで（国会会議録）。t＝月（3月18日＝3.55）
    "c806": dict(
        t="船と魚を調べる",
        s="国の検査",
        fig=("timeline", dict(
            events=[dict(t=3.55, top="5つの港に絞る", t2="3月18日", c=J.AMBER),
                    dict(t=12.97, top="検査の終わり", t2="12月の終わり", c=J.LINE, big=True)],
            band=[dict(a=3.55, b=12.97, t="船と魚の検査", c=J.AMBER)],
            t0=3.0, t1=13.5,
            ticks=[(4, "4月"), (7, "7月"), (10, "10月")],
            src=NOTE_KK4)),
    ),

    # Commons「A signboard appealing shoppers」（朝日グラフ）。看板の字は「原子マグロ」＝写っている字のまま
    #   🔴 店の女性2人（右）は束の道具で・戸口の顔2つ（上）は `ss.TRIM` で落とした（私人の顔を出さない）
    "c807": dict(
        t="「原爆マグロ」",
        s="魚屋の看板　1954年",
        photo=P("jp_fish_sign"), **ss.kind(P("jp_fish_sign")),
        side="right", ann_y=356,
        ann=[dict(t="看板の字", d="原子マグロは買いません", dc=J.AMBER)],
    ),

    # 856隻＝1954年の終わりまでに汚染されたマグロを水揚げした漁船（B3-1）。ブラボー1回の数ではない
    "c808": dict(
        t="水揚げした船の数",
        s="1954年の終わりまで",
        fig=("panel", dict(
            blocks=[dict(k="汚染マグロの水揚げ", t="856隻", c=J.ALERT),
                    dict(k="もとの実験", t="3月〜5月の6回", c=J.AMBER)],
            cols=2,
            note="出典：都立第五福竜丸展示館・広島平和記念資料館")),
    ),

    # Commons「Eisenhower and Strauss」
    "c809": dict(
        t="大統領への報告",
        s="大統領と原子力委員会の委員長　1954年",
        photo=P("eisenhower_strauss"), **ss.kind(P("eisenhower_strauss")),
        side="right", ann_y=330,
        ann=[dict(t="水爆実験の報告", v="3月30日", vc=J.AMBER),
             dict(t="翌31日", d="第五福竜丸にもふれる", dc=J.TICK)],
    ),

    # 委員長の言い分（DNA p480 の覚え書きが引く発言）
    "c810": dict(
        t="委員長の言い分",
        s="船長の話として",
        fig=("panel", dict(
            blocks=[dict(k="光から音まで", t="6分", c=J.ALERT),
                    dict(k="短いほど", t="爆心に近い", c=J.AMBER)],
            cols=2)),
    ),

    # 🔴 決め所（DNA p480「it must have been well within the danger area」）
    "c811": dict(
        t="委員長の結論",
        s="船の位置についての発言",
        fig=("quote", dict(
            phrase="船は危険区域の十分内側にいたはず",
            who="原子力委員会の委員長",
            when="1954年3月31日",
            doc="日本大使館の覚え書きが引く発言")),
    ),

    # 「7、8分」は幅のある値＝棒で長さを比べない（bar=False）
    "c812": dict(
        t="音が届くまで",
        s="光から音までの時間",
        fig=("compare", dict(
            items=[dict(v=6, t="委員長の言い分", disp="6", unit="分", c=J.ALERT),
                   dict(v=7.5, t="日本側・1982年の報告書", disp="7、8", unit="分", c=J.AMBER)],
            bar=False,
            note="出典：日本大使館の覚え書き（1954年4月12日）・国防原子力局の報告書（1982年）")),
    ),

    # 🔴 決め所（DNA p480「19 miles and 26 miles outside the danger-zone」）
    "c813": dict(
        t="日本側の反論",
        s="船の位置についての反論",
        fig=("quote", dict(
            phrase="船は危険区域の外にいたとみられる",
            who="日本政府",
            to="アメリカ政府",
            when="1954年4月12日",
            doc="在米大使館の覚え書き")),
    ),

    # 報告書の第16図。前の区域（長方形）の上を西から東へなぞる
    "c814": dict(
        t="区域の外で",
        s="報告書の第16図　実験場と警戒の区域",
        **FIG16,
        # ⑤c'（09-23）：窓の上の辺が「SECURITY ZONE」の行を横に切っていた（見えて64%）＝縦を 0.62→0.66 へ下げて外す。
        #    c815 の頭と同じ値にしておく（カメラがつながる）（台帳 §7-4）
        cam={"from": (0.30, 0.66, 1.6), "to": (0.42, 0.66, 1.6)},
        side="right",
        ann=[dict(t="光を見た所", d="区域から30キロあまり外", dc=J.AMBER),
             dict(t="灰を浴びた所", d="さらに外", dc=J.ALERT),
             dict(t="区域の知らせ", d="船乗り向けの公報", dc=J.TICK)],
    ),

    # 同じ第16図。前の区域から引いて、ブラボーのあとの扇形（POST-CASTLE SECURITY ZONE）を明かす
    "c815": dict(
        t="広げられた区域",
        s="報告書の第16図　実験場と警戒の区域",
        **FIG16,
        cam={"from": (0.42, 0.66, 1.6), "to": (0.5, 0.5, 1.0)},    # ⑤c'（09-23）：頭は c814 の尻と同じ
        side="right",
        ann=[dict(t="ブラボーのあと", d="区域を大きく", dc=J.ALERT),
             dict(t="新しい区域", v="半径833キロ", vc=J.AMBER, d="扇形")],
    ),

    # ⚠️ 実名は久保山愛吉さんだけ。写真は使わない（病床の写真は②で落とした）
    "c816": dict(
        t="無線を受け持った人",
        s="第五福竜丸の乗組員",
        fig=("panel", dict(
            blocks=[dict(k="無線長", t="久保山愛吉さん", c=J.AMBER),
                    dict(k="無線の資格", t="船でただ一人", c=J.TICK),
                    dict(k="治療", t="東京の病院で", c=J.LINE)])),
    ),

    # 3月1日から9月23日。t＝1月1日から数えた日（3月1日＝60・9月23日＝266）
    "c817": dict(
        t="無線長の206日",
        s="1954年3月から9月",
        fig=("timeline", dict(
            events=[dict(t=60, top="灰を浴びる", t2="3月1日", c=J.ALERT),
                    dict(t=266, top="久保山さん", t2="9月23日　40歳", c=J.AMBER, big=True)],
            band=[dict(a=60, b=266, t="206日", c=J.AMBER)],
            t0=50, t1=280,
            ticks=[(91, "4月"), (152, "6月"), (213, "8月")],
            src=NOTE_D5F)),
    ),

    # 日本政府・解剖した医師／アメリカ政府の内部の電報と日本の医師の一部（B2-2・B2-3）
    "c818": dict(
        t="見方の分かれた原因",
        s="日本とアメリカの見方",
        fig=("panel", dict(
            blocks=[dict(k="日本政府", t="放射能の影響", c=J.ALERT),
                    dict(k="解剖した医師", t="放射能による変化", c=J.ALERT),
                    dict(k="米政府の電報・一部の医師", t="輸血による肝炎の疑い", c=J.TICK)])),
    ),

    # 1955年1月4日の交換公文（B5-1）と配分（B5-2）
    "c819": dict(
        t="200万ドルで決着",
        s="1955年1月4日",
        fig=("process", dict(
            steps=[dict(t="慰謝料", d="200万ドル", c=J.AMBER),
                   dict(t="当時の円で", d="7億2千万円", c=J.AMBER),
                   dict(t="6割あまり", d="マグロの損害へ", c=J.ALERT)],
            note="法的な責任は問わない形　出典：国会会議録（1955年）・米国務省の外交文書")),
    ),

    # 署名の始まり（1954年5月・杉並）と1955年の秋（B7）。章の終わり＝尻で暗転（自動）
    "c820": dict(
        t="広がった署名",
        # ⚠️ 副題「原水爆禁止の署名」は字幕の文の切り取り（check_echo）
        s="各地の署名運動",
        fig=("timeline", dict(
            events=[dict(t=1954.35, top="署名の始まり", t2="東京の杉並など", c=J.AMBER),
                    dict(t=1955.75, top="3200万を超える", t2="1955年の秋", c=J.ALERT, big=True)],
            t0=1954.0, t1=1956.2,
            ticks=[(1954, "1954"), (1955, "1955"), (1956, "1956")],
            src="出典：杉並区ほか")),
    ),

}
