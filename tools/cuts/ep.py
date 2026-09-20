# -*- coding: utf-8 -*-
"""締め その後に残ったもの ep01–ep14（14カット）。10本目（三豊百貨店）。

■ 写真は7カット。7点とも CC BY-SA ＝**額装だけ**（`panel=True` のみ）。
  ⚠️ ep01・ep02・ep04・ep06・ep08 は**このカットの話を何も語らない地**
     （拘束・捜査・控訴・民事を写した写真はこの世に無い）。
     **副題は写っているものだけ**を言う（→ `ref/ep10/photos.md` §3）。
  ⚠️ `volunteers_02`（ep08）は**何の配給かを断定しない**（原本に説明が無い）。
■ 🔴 **画面にハングルを書かない**（Noto に字が無く豆腐になる）。
  出典の `법제처` は「韓国 法制処」、判例番号は「大法院 1996年8月23日 判決」と日本語で書く。
■ ⚠️ ep12 の刑は「3年以上の懲役／無期」の順で書く。字幕の行が17字と短く、
  同じ語順で書くと `check_echo` の一致率が跳ねる（④' が直した行なので語そのものは変えない）。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC_DAE96 = "大法院 1996年8月23日 判決（刑事）"
SRC_HOUSEI = "韓国 法制処"

SPEC = {

    # ⚠️ 地（拘束・起訴を写した写真は存在しない）。
    "ep01": dict(
        t="7月1日に、4人が拘束された",
        s="かすみの道路と、救急車の列　1995年撮影",
        photo=P("ambulance_line_02"), panel=True,
    ),

    # ⚠️ 地（捜査を写した写真は存在しない）。
    "ep02": dict(
        t="対象は、11人に広がった",
        s="ケーブルの中で作業する隊員　1995年撮影",
        photo=P("rescue_work_08"), panel=True,
    ),

    "ep03": dict(
        t="仕事は、四つの段階に分かれる",
        s="建物ができるまでと、できたあと",
        fig=("process", dict(
            steps=[dict(t="計画", d="立てる", c=J.INST),
                   dict(t="図面", d="描く", c=J.INST),
                   dict(t="施工", d="実際に建てる", c=J.LINE),
                   dict(t="維持管理", d="建ったあとの手入れ", c=J.AMBER)],
            note=SRC_DAE96)),
    ),

    # ⚠️ 地（判決を写した写真は存在しない）。写っているのは他市から来た隊。
    "ep04": dict(
        t="1審は、その年の12月27日",
        s="よその市から来た隊員　1995年撮影",
        photo=P("rescue_work_13"), panel=True,
    ),

    "ep05": dict(
        t="言い渡された刑の一覧",
        s="2審の主文",
        fig=("panel", dict(
            blocks=[dict(k="いちばん重い", t="懲役 7年6か月", v="1人", c=J.ALERT),
                    dict(k="そのほか", t="禁錮1年／懲役1年6か月／懲役10か月",
                         v="各1人", c=J.AMBER),
                    dict(k="執行猶予つき", t="禁錮1年6か月", v="2人", c=J.TICK)],
            cols=3, note="ソウル高法 1996年5月10日")),
    ),

    # ⚠️ 地（控訴の結果を写した写真は存在しない）。
    "ep06": dict(
        t="ほかの12人は、退けられた",
        s="鉄筋を切る隊員の寄り　1995年撮影",
        photo=P("rescue_work_04"), panel=True,
    ),

    "ep07": dict(
        # ⚠️「業務上過失致死傷の共同正犯」は字幕がそのまま言う（`check_echo`）。
        #    画面は**役の並び**を持ち、罪名そのものは字幕に任せる。
        t="四つの段階を、一つに束ねた",
        s="判決が使った罪名",
        fig=("people", dict(
            nodes=[dict(x=0.14, y=0.24, t="計画", d="", c=J.INST, kind="person"),
                   dict(x=0.14, y=0.76, t="図面", d="", c=J.INST, kind="person"),
                   dict(x=0.50, y=0.50, t="一つの事故", d="共同正犯", c=J.ALERT,
                        kind="doc"),
                   dict(x=0.86, y=0.24, t="施工", d="", c=J.LINE, kind="person"),
                   dict(x=0.86, y=0.76, t="維持管理", d="", c=J.AMBER,
                        kind="person")],
            edges=[dict(a=0, b=2, t=""), dict(a=1, b=2, t=""),
                   dict(a=3, b=2, t=""), dict(a=4, b=2, t="")],
            note=SRC_DAE96)),
    ),

    # ⚠️ 地（民事の判断を写した写真は存在しない）。
    "ep08": dict(
        t="民事は、高裁へ差し戻された",
        s="給油所の前庭の物資と、人　1995年撮影",
        photo=P("volunteers_02"), panel=True,
    ),

    "ep09": dict(
        t="ひとつの段階の話ではない",
        s="刑事の判決が認めたこと",
        fig=("quote", dict(
            phrase="過失は、この四つすべてにあった",
            rows=[("どの裁判", "刑事（大法院）", J.INST),
                  ("いつの判決", "1996年8月23日", J.AMBER),
                  ("四つの段階", "計画・図面・施工・維持管理", J.INK_W)],
            paper=True)),
    ),

    "ep10": dict(
        t="19日後に、新しい法律ができた",
        s="削岩機で壁を壊す隊員　1995年撮影",
        photo=P("rescue_work_22"), panel=True,
    ),

    "ep11": dict(
        t="災難という区分が、できた",
        s="災難管理法が決めたこと",
        fig=("panel", dict(
            blocks=[dict(k="何を災難と決めたか", t="火災・爆発・崩壊など",
                         v="自然災害ではない事故", c=J.INST),
                    dict(k="だれがやるか", t="国と自治体", v="備えと後始末",
                         c=J.OK)],
            cols=2, note=SRC_HOUSEI + "（制定理由）")),
    ),

    # ⚠️ 刑は「3年以上の懲役／無期」の順で書く（字幕の行が17字と短いため）。
    "ep12": dict(
        # ⚠️ 副題に「1995年12月30日」を書くと、段の答えを先に言ってしまう（A型）。
        t="建築法をふくむ、5つの法律",
        s="同じ日に改められた法律",
        fig=("panel", dict(
            blocks=[dict(k="いつ", t="5つの法律が同じ日に", v="1995年12月30日",
                         c=J.AMBER),
                    dict(k="そのうち1つ", t="建築法", v="改正", c=J.INST),
                    dict(k="わざとの手抜き工事", t="人を死なせた場合",
                         v="3年以上の懲役／無期", c=J.ALERT)],
            cols=3, note=SRC_HOUSEI)),
    ),

    "ep13": dict(
        t="それまでで、いちばん多かった",
        s="隊員の顔の近景　1995年撮影",
        photo=P("rescue_work_01"), panel=True,
    ),

    "ep14": dict(
        # ⚠️「この動画」は楽屋の言葉（B型）、「その日」は指示語（C型）。どちらも画面に出さない。
        t="合図は、届いていた",
        s="ここまでに分かったこと",
        fig=("panel", dict(
            blocks=[dict(k="出ていた", t="床と天井の合図", v="朝から", c=J.ALERT),
                    dict(k="気づいた", t="現場の人たち", v="崩れた日のうち", c=J.AMBER),
                    dict(k="届いた", t="幹部・社長・会長", v="14:30ごろまでに",
                         c=J.AMBER),
                    dict(k="されなかった", t="客を外へ出すこと", v="最後まで",
                         c=J.ALERT)],
            cols=2, note="国政調査結果報告書 p.30・p.32")),
    ),

}
