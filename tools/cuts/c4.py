# -*- coding: utf-8 -*-
"""第4章 15時間半 c401–c442（42カット）。

■ この章の役目
  ★台本の背骨。いちばん長く、いちばん静かに書く。追うのは**記録の空白と時刻**。

■ 🔴 この章で守ること
  1 **生存者の証言そのものを使わない**（2026-08-04 カズヤくん判断）。
    原典（『新潮45』1986年1月号の独占手記／吉岡忍『墜落の夏』）を読めておらず、
    中身を裏づけられないため。代わりに**確認できた事実そのもの**を言う。
    → 存命の方に一切触れない。個人が特定できる属性も出さない。
  2 「食い違い」ではなく **「空白」** として扱う。c435〜c442 へまっすぐつながる。
  3 `c409` の「即死若しくは」は**報告書の原文どおり**（本文2.13.3）。
    ⚠️ ただし**タイトルとサムネには出さない**（制作ルール §5 の例外規定）。
  4 図に**遺体の写真を出さない**。報告書にもそうした写真は無い。

■ 出どころ
  時刻は本文2.14／2.14.2、救助の可否は解説書 §9。
"""
import jiko_style as J

SPEC = {

    "c401": dict(
        t="墜落は18時56分、救出は翌朝",
        s="本文2.1／2.14.2",
        fig=("moment", dict(clock="18:56", label="救い出されたのは翌朝",
                            day=18.93, dayspan=(18, 24),
                            facts=[dict(t="墜落", v="18:56", c=J.ALERT),
                                   dict(t="生存者の発見", v="翌 10:45ごろ",
                                        c=J.AMBER)])),
    ),

    "c402": dict(
        t="こう言われることがある",
        s="—",
        fig=("panel", dict(blocks=[
            dict(k="問い", c=J.AMBER,
                 t="もっと早ければ、助かった人がいたのではないか")],
            lead="この章が扱う問い")),
    ),

    "c403": dict(
        t="答えは出ていない",
        s="出ていないこと自体が記録に残っている",
        fig=("absent", dict(mode="single", items=[
            dict(t="この問いへの答え", d="はっきりしたものは出ていない", ok=False)],
            lead="報告書と解説書を読むかぎり")),
    ),

    "c404": dict(
        t="まず、どう壊れたかを見る",
        s="付図-3　墜落現場の状況",
        photo="ja123/f003.jpg", panel=True, side="right",
        ann=[dict(t="手がかり", d="遺体の収容の記録", dc=J.LINE, ds=32),
             dict(t="機内の整理", d="5つの部位に分けられた", dc=J.AMBER, ds=32)],
    ),

    "c405": dict(
        t="機内は5つに分けられた",
        s="付図-5　胴体ステーション及び座席配置図（本文2.13.2）",
        photo="ja123/f005.jpg", panel=True, side="right", bias=0.34,
        ann=[dict(t="区分", d="2階席／1〜8／10〜18／19〜31列目", dc=J.LINE, ds=30),
             dict(t="続き", d="32〜42／43〜60列目", dc=J.LINE, ds=30)],
    ),

    "c406": dict(
        t="散らばり方に差があった",
        s="付図-14　残骸分布図―墜落地点（本文2.13.2）",
        photo="ja123/f014.jpg", panel=True, side="right",
        ann=[dict(t="前の方の部位", d="激突した地点の近く", dc=J.LINE, ds=32),
             dict(t="中ほどの部位", d="尾根の上や右前方の斜面に広く", dc=J.AMBER,
                  ds=30)],
    ),

    "c407": dict(
        t="最後尾だけが違っていた",
        s="写真-4　後部胴体の残骸（1）",
        photo="ja123/p004.jpg", panel=True, side="right",
        ann=[dict(t="どこへ落ちたか", d="壊れた機体とともに沢へ", dc=J.LINE, ds=32),
             dict(t="見つかり方", d="狭い場所に集まった状態", dc=J.AMBER, ds=32)],
    ),

    "c408": dict(
        t="4人はこの部位から救出された",
        s="写真-5　後部胴体の残骸（2）（本文2.13.2／2.13.3）",
        photo="ja123/p005.jpg", panel=True, side="right",
        ann=[dict(t="報告書の記述", d="比較的損傷の少ないものも認められた",
                  dc=J.LINE, ds=30),
             dict(t="生存者4人", d="いずれもこの部位から", dc=J.OK, ds=32)],
    ),

    # ── c409 報告書の原文どおりの表記。**煽らない。淡々と置く** ────────
    "c409": dict(
        t="報告書はこう書いている",
        s="本文2.13.3　医師の検案にもとづく記述",
        fig=("panel", dict(blocks=[
            dict(k="原文", c=J.DOC,
                 t="生存者4名を除いた他の者は、即死若しくはそれに近い状況であった"),
            dict(k="根拠", c=J.LINE, t="遺体を検案した医師の所見にもとづく")],
            cols=1)),
    ),

    "c410": dict(
        t="記録のほうを見ておきたい",
        s="生存者は何を語り、何に使われたのか",
        fig=("moment", dict(clock="—", label="口述という記録",
                            facts=[dict(t="何を語ったか", v="—", c=J.LINE),
                                   dict(t="何に使われたか", v="—", c=J.AMBER)])),
    ),

    # ── c411 口述は**証拠として使われている**（3行＝3段）───────────
    "c411": dict(
        t="口述は証拠に使われている",
        s="本文2.1／3.1.4.1／解説書 §5",
        fig=("panel", dict(blocks=[
            dict(k="1", c=J.OK, t="客室に霧が出たこと"),
            dict(k="2", c=J.OK, t="酸素ボトルの状態"),
            dict(k="3", c=J.OK, t="異常が起きた直後の、音のこと")], cols=1)),
    ),

    # ── c412 使われているのは、そこまで（3行＝3段）───────────────
    "c412": dict(
        t="書かれているのは、そこまで",
        s="本文2.13／2.14",
        fig=("absent", dict(mode="ledger", items=[
            dict(t="事故の経過について", d="口述が証拠として使われている", ok=True),
            dict(t="墜落したあとに見たもの", d="書かれていない", ok=False),
            dict(t="墜落したあとに聞いたもの", d="書かれていない", ok=False)],
            lead="報告書にも解説書にも")),
    ),

    "c413": dict(
        t="節そのものは存在する",
        s="本文2.13.1／2.14.2",
        fig=("panel", dict(blocks=[
            dict(k="2.13.1", c=J.DOC, t="生存者の受傷の状況"),
            dict(k="2.14.2", c=J.DOC, t="生存者発見から救出収容までの状況"),
            dict(k="中身", c=J.LINE, t="時刻と、場所と、傷の程度")],
            cols=1)),
    ),

    "c414": dict(
        t="無かったのは、仕組みのほう",
        s="—",
        fig=("absent", dict(mode="single", items=[
            dict(t="尋ねて記録する仕組み", d="当時は無かった", ok=False)],
            lead="そのあいだ何を見て、何を聞いたのか")),
    ),

    # ── c415 空白（3行＝3段）──────────────────────────────
    "c415": dict(
        t="あるのは空白である",
        s="—",
        fig=("panel", dict(blocks=[
            dict(k="×", c=J.LINE, t="食い違いではない"),
            dict(k="—", c=J.ALERT, t="空白である"),
            dict(k="いま", c=J.AMBER, t="40年たっても埋まっていない")],
            cols=1)),
    ),

    "c416": dict(
        t="分かっている時刻を並べる",
        s="すべて公の記録に残っている",
        fig=("moment", dict(clock="—", label="ここからは時刻だけを並べる",
                            facts=[dict(t="出どころ", v="本文2.14", c=J.DOC)])),
    ),

    # ── c417 付図-24 東京レーダー（19時）。**機影が消えた直後の記録** ────
    "c417": dict(
        t="18時57分、機影が消えた",
        s="付図-24　東京レーダー・スケッチ図（19時）",
        photo="ja123/f024.jpg", panel=True, side="right",
        ann=[dict(t="墜落", v="18:56", vc=J.ALERT, vs=78),
             dict(t="レーダーから消えた", v="18:57", vc=J.ALERT, vs=78)],
    ),

    "c418": dict(
        t="19時15分、火災を発見",
        s="本文2.14.1.1　アメリカ軍の輸送機",
        fig=("moment", dict(clock="19:15", label="アメリカ軍の輸送機が火災を発見",
                            day=19.25, dayspan=(18, 24),
                            facts=[dict(t="位置の誤差", v="約3 km", c=J.AMBER)])),
    ),

    "c419": dict(
        t="19時21分、戦闘機が確認",
        s="本文2.14　航空自衛隊",
        fig=("moment", dict(clock="19:21", label="戦闘機2機が炎を確認",
                            day=19.35, dayspan=(18, 24),
                            facts=[dict(t="位置の誤差", v="約6 km", c=J.AMBER)])),
    ),

    "c420": dict(
        t="20時42分、ヘリが確認",
        s="本文2.14　自衛隊のヘリコプター",
        fig=("moment", dict(clock="20:42", label="ヘリコプターが確認",
                            day=20.7, dayspan=(18, 24),
                            facts=[dict(t="位置の誤差", v="約4 km", c=J.AMBER)])),
    ),

    "c421": dict(
        t="場所が正確に決まらない",
        s="付図-2　墜落現場付近図（本文2.14／解説書 §9）",
        photo="ja123/f002.jpg", panel=True, side="right",
        ann=[dict(t="3回の確認の誤差", v="3 km ／ 6 km ／ 4 km", vc=J.ALERT, vs=54),
             dict(t="山の中では", d="上空からは見えるのに、地上からは着けない",
                  dc=J.LINE, ds=30)],
    ),

    "c422": dict(
        t="1985年にGPSは無かった",
        s="解説書 §9",
        fig=("beforeafter", dict(
            a=dict(k="いま", t="GPSがある", lines=["位置はすぐに分かる"], c=J.OK),
            b=dict(k="1985年", t="それは無かった", c=J.ALERT))),
    ),

    "c423": dict(
        t="頼れるのは方位と距離だけ",
        s="解説書 §9　当時の測位",
        fig=("absent", dict(mode="seat", items=[
            dict(t="衛星による測位", d="当時は無い", ok=False),
            dict(t="地上の電波施設", d="方位と距離を読む", ok=True),
            dict(t="夜間の目視", d="炎は見えるが位置が決まらない", ok=False)],
            lead="夜間に航空機から墜落場所を特定する方法")),
    ),

    "c424": dict(
        t="午前1時、誘導に失敗",
        s="本文2.14",
        fig=("moment", dict(clock="01:00", label="ヘリが地上の県警を誘導しようとした",
                            day=1.0, dayspan=(0, 12),
                            facts=[dict(t="結果", v="失敗している", c=J.ALERT)])),
    ),

    "c425": dict(
        t="なぜ降りなかったのか",
        s="解説書 §9　そこにも答えている",
        fig=("moment", dict(clock="—", label="火が見えているのなら",
                            facts=[dict(t="問い", v="ヘリで降りればよいのでは",
                                        c=J.AMBER)])),
    ),

    "c426": dict(
        t="夜間の吊り上げは海上でやる",
        s="解説書 §9",
        fig=("process", dict(steps=[
            dict(t="障害物のない海上", d="通常はここで行う", c=J.OK),
            dict(t="照明弾を落とす", d="夜間の視界を確保する", c=J.AMBER)])),
    ),

    "c427": dict(
        t="山では、どちらもできない",
        s="解説書 §9",
        fig=("absent", dict(mode="ledger", items=[
            dict(t="照明弾", d="火災のおそれがあり落とせない", ok=False),
            dict(t="自動操縦での進入", d="段差のある山岳地帯ではできない",
                 ok=False)],
            lead="地上（山岳地帯）では")),
    ),

    "c428": dict(
        t="暗視装置は無かった",
        s="解説書 §9",
        fig=("absent", dict(mode="single", items=[
            dict(t="当時の自衛隊の暗視装置", d="その装備は無かった", ok=False)],
            lead="暗視装置を着けて操縦する方法もあるが")),
    ),

    "c429": dict(
        t="二次災害の危険が極めて高い",
        s="解説書 §9",
        fig=("panel", dict(blocks=[
            dict(k="分からない", c=J.ALERT, t="障害物"),
            dict(k="分からない", c=J.ALERT, t="降下する場所の状況"),
            dict(k="結論", c=J.DOC, t="夜間のヘリ救助は二次災害の危険が極めて高い")],
            cols=1)),
    ),

    "c430": dict(
        t="夜明け、残骸が確認された",
        s="本文2.14　8月13日",
        fig=("timeline", dict(t0=4.5, t1=6,
                              ticks=[(4.65, "04:39"), (5.62, "05:37")],
                              events=[dict(t=4.65, top="自衛隊が残骸を確認",
                                           c=J.LINE),
                                      dict(t=5.62, top="長野県警のヘリが発見",
                                           c=J.OK, big=True)])),
    ),

    "c431": dict(
        t="地上の部隊が斜面を登る",
        s="付図-19　一本から松からU字溝にかけての状況",
        photo="ja123/f019.jpg", panel=True, side="right",
        ann=[dict(t="夜が明けて", d="ようやく場所が定まった", dc=J.LINE, ds=32),
             dict(t="現場", d="険しい山岳地帯", dc=J.AMBER, ds=32)],
    ),

    "c432": dict(
        t="午前10時45分ごろ",
        s="本文2.14.2　スゲノ沢第3支流",
        fig=("moment", dict(clock="10:45", label="生存者が発見された",
                            day=10.75, dayspan=(0, 12),
                            facts=[dict(t="場所", v="スゲノ沢 第3支流", c=J.LINE)])),
    ),

    "c433": dict(
        t="4メートル四方の範囲だった",
        s="付図-14　残骸分布図―墜落地点（本文2.14.2）",
        photo="ja123/f014.jpg", panel=True, side="right", bias=0.66,
        ann=[dict(t="救出", v="11:40ごろまでに4人", vc=J.OK, vs=62),
             dict(t="見つかった範囲", v="約4 m × 4 m", vc=J.AMBER, vs=62)],
    ),

    "c434": dict(
        t="およそ15時間半",
        s="本文2.14　19:15 → 翌 10:45〜11:40",
        fig=("timeline", dict(t0=19, t1=35,
                              ticks=[(19, "19:15"), (24, "0時"), (29, "5時"),
                                     (34.7, "10:45")],
                              band=[dict(a=19, b=29.5, c=J.ALERT, op=0.20,
                                         t="そのほとんどが夜")],
                              events=[dict(t=19, top="火を確認", c=J.AMBER),
                                      dict(t=34.7, top="救出", c=J.OK,
                                           big=True)])),
    ),

    "c435": dict(
        t="報告書は答えていない",
        s="—",
        fig=("moment", dict(clock="—", label="もっと早く着いていれば助かったのか",
                            facts=[dict(t="報告書の答え", v="無い", c=J.ALERT)])),
    ),

    "c436": dict(
        t="答えなかったのではない",
        s="解説書 §9",
        fig=("absent", dict(mode="single", items=[
            dict(t="被害の軽減を調べる仕組み", d="当時は無かった", ok=False)],
            lead="答えなかったのではなく")),
    ),

    "c437": dict(
        t="解説書に書かれていること",
        s="解説書 §9",
        fig=("panel", dict(blocks=[
            dict(k="当時", c=J.LINE, t="事故の原因は調査していた")],
            lead="調査の範囲")),
    ),

    "c438": dict(
        t="そこまでは調べていなかった",
        s="解説書 §9",
        fig=("absent", dict(mode="pair", items=[
            dict(t="事故の原因", d="調査していた", ok=True, n=1),
            dict(t="被害をどう軽減できたか", d="調査を行うようになっていなかった",
                 ok=False, n=0)],
            lead="当時の調査の範囲")),
    ),

    "c439": dict(
        t="国が2011年に自ら書いた",
        s="解説書 §9",
        fig=("quote", dict(phrase="詳細な記録は残っていない",
                           who="運輸安全委員会",
                           to="報告書についての解説 §9",
                           when="2011年",
                           doc="当時は被害の軽減まで調査していなかった")),
    ),

    "c440": dict(
        t="無いことが、隠したに見える",
        s="—",
        fig=("beforeafter", dict(
            a=dict(k="言い換え", t="隠していた", c=J.ALERT),
            b=dict(k="記録が示すこと", t="そこまで調べる決まりが無かった",
                   lines=["記録に無いことが、隠したことのように見える"], c=J.LINE))),
    ),

    "c441": dict(
        t="いまは、そこまで調べる",
        s="解説書 冒頭　運輸安全委員会",
        fig=("beforeafter", dict(
            a=dict(k="当時", t="原因の調査まで", c=J.LINE),
            b=dict(k="いま", t="被害をどう減らせたかまで",
                   lines=["遺族への説明も法律に書かれている"], c=J.OK))),
    ),

    "c442": dict(
        t="分からないままである",
        s="—",
        fig=("moment", dict(clock="—", label="あの夜、何ができたのか",
                            facts=[dict(t="確かなこと", v="分からない、ということ",
                                        c=J.LINE)])),
    ),
}
