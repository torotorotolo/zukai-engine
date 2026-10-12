# -*- coding: utf-8 -*-
"""21本目 9.11 米国同時多発テロ（リメイク）⑤a-1：読み一覧に「期待の読み」を機械で当てる（2026-10-12）。

  python ref/ep21/aq/expect21.py            … 当たらない語・語の途中で割れた語を全部出す（あれば exit 1）
  python ref/ep21/aq/expect21.py --list     … 語ごとに、出た行・位置（頭／中／尻）・判定を全部出す
  python ref/ep21/aq/expect21.py --chars 何札方  … その字を含む行の文と読みを並べる（人が目で見る）
  python ref/ep21/aq/expect21.py --selftest … 答えの分かっている見本で検算

20本目の `ref/ep20/aq/expect20.py` を写した（19本目・18本目・16本目の expect16.py が元）。変えたのは2点:
  ① 表 KANJI・EXCLUDE・MULTI・STRICT（21本目の語）
  ② selftest の見本を21本目の実物（辞書なしの読み一覧＝2026-10-12 の誤り）に
20本目で足した「利用者辞書 userdict.csv の全語にも期待の読みを当てる」（B）はそのまま
  （なぜ：20本目の1字の鍵「縁」は7行中2行でしか選ばれなかった＝「辞書に入れた」は「その行で効いた」ではない。
   ⚠️ 読みの答えは辞書そのもの＝読みの正しさは表 KANJI と人の目（ここが見るのは「効いたか」と「句が割れないか」））
読むもの＝ref/ep21/aq/yomi_sheet.tsv（先に `python tools/aq_kana.py --sheet`）。
当てる語:
  A. 台本に出るカタカナ語の**全部**（機械で拾う。「・」で切る）＝期待の読みはカタカナをひらがなにしたもの（ヴ→ば行）
  B. 利用者辞書の全語（②）
  C. 台本 §6 の漢語・地名・英字・この回で見つけた語＝期待の読みは下の表 KANJI（人が書いた・B より優先）
判定:
  ① 読み（音声記号列から ' と句読点を外したもの）に、期待の読みが「その語が文に出る回数」以上あるか
  ② 期待の読みが1つのアクセント句の中に収まっているか（語の途中で / ・、で割れていないか）
  長音は「ー」と母音の字（こう・けい など）を同じとみなす（pyopenjtalk の発音は長音を ー で書く）
⚠️ 当たり＝「その読みが行のどこかにある」まで。どの語の読みかまでは見ていない＝最後は読み一覧を人とサブエージェントが読む
⚠️ 数の読みの正しさは数の台帳 `check_aq_yomi`（ここで数を含む語を見るのは「辞書が効いたか」と「句が割れないか」）
"""
import csv
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
SHEET = HERE / "yomi_sheet.tsv"
DICT = HERE / "userdict.csv"

# C. 漢語・地名・英字の期待の読み（長音は ー でも母音の字でもよい・助詞の は は わ と書く）。鍵は台本の字のまま
KANJI = {
    # 台本 §6 の漢字（④' で足した語を含む）
    "刃渡り": "はわたり", "寸前": "すんぜん", "決を": "けつを", "墜ちた": "おちた", "札": "ふだ", "頁": "ぺーじ", "要る": "いる",
    "首席補佐官": "しゅせきほさかん", "監察総監": "かんさつそうかん", "検視局": "けんしきょく", "追悼": "ついとう",
    "北棟": "きたとう", "南棟": "みなみとう", "空の": "そらの", "開いた": "ひらいた", "港湾公社": "こうわんこうしゃ",
    "何機": "なんき", "4,500機": "よんせんごひゃっき",
    # 台本 §6 の地名・施設（カタカナの地名は A で全部当たる）
    "ナショナル空港": "なしょなるくうこう", "北東部": "ほくとうぶ",
    # 台本 §6 の英字・便名・機種・CVR の英語
    "NEADS": "にーず", "NORAD": "のーらっど", "FAA": "えふえいえい", "NTSB": "えぬてぃーえすびー", "FBI": "えふびーあい",
    "NIST": "にすと", "AP": "えいぴー", "F-15": "えふじゅうご", "Roll it": "ろーるいっと",
    "11便": "じゅういちびん", "175便": "ひゃくななじゅうごびん", "77便": "ななじゅうななびん", "93便": "きゅうじゅうさんびん",
    "767": "ななろくなな", "757": "ななごーなな",
    # 台本 §6 の数
    "2,977人": "にせんきゅうひゃくななじゅうななにん", "4万3,000リットル": "よんまんさんぜんりっとる",
    "1万1,400ガロン": "いちまんせんよんひゃくがろん", "10時0分25秒": "じゅうじれいふんにじゅうごびょう",
    "10時0分42秒": "じゅうじれいふんよんじゅうにびょう", "8時46分40秒": "はちじよんじゅうろっぷんよんじゅうびょう",
    "250万頁": "にひゃくごじゅうまんぺーじ", "1,200人": "せんにひゃくにん",
    # ⑤a-1 で見つけて直した語（2026-10-12・辞書なしの読み一覧を語＝読みの組で全部見た）
    "上の人たち": "うえのひとたち", "東の方": "ひがしのほう", "違う方": "ちがうほう", "逆の方": "ぎゃくのほう",
    "やり方": "やりかた", "調べ方": "しらべかた", "飛び方": "とびかた",
    "同じ": "おなじ", "録って": "とって", "多かったぶん": "おおかったぶん",
    "何人": "なんにん", "何時": "なんじ", "何も": "なにも", "何が": "なにが", "何か": "なにか", "何を": "なにを",
    "7人": "ななにん", "37人": "さんじゅうななにん", "ハーンドン": "はーんどん",
    # 係2本の指摘を自分で確かめて直した語（2026-10-12）＝辞書の語は B でも当たる・ここは型の見張り
    "何分": "なんぷん", "北アメリカ": "きたあめりか", "旧ソ連": "きゅうそれん",
    "ったからだ": "ったからだ",   # 〜あった/からだ・〜なかった/からだ＝体 に聞こえる句の割れ（② で見る）
    # 「の上」＝うえ（地名の1語にされて のーえ になる型＝19本目・20本目の 山の上）
    "の上": "のうえ",
}
# 語の中に別の語として含まれる字の並び＝回数から引く（「空の」は 航空の の中を数えない・「の上」は の上司 を数えない）
EXCLUDE = {"空の": ("航空の",), "の上": ("の上司",)}
# 助詞・記号・英字をはさむ語＝2つの句に分かれるのが自然（② を見ない）
MULTI = {"何も", "何が", "何か", "何を", "決を", "F-15", "Roll it", "4万3,000リットル", "1万1,400ガロン",
         "10時0分25秒", "10時0分42秒", "8時46分40秒", "の上"}
# 長音とみなさない語＝期待の読みを字のとおりに当てる（19本目・20本目 c620-2 の 山の上＝やまのーえ の型）
STRICT = {"の上"}
SEP = re.compile(r"[/、。？！]")
KATA = re.compile(r"[ァ-ヴー]+")
VOWEL = {}
for v, row in zip("aiueo", ("あかさたなはまやらわがざだばぱぁゃ", "いきしちにひみりぎじぢびぴぃ",
                            "うくすつぬふむゆるぐずづぶぷぅゅ", "えけせてねへめれげぜでべぺぇ",
                            "おこそとのほもよろをごぞどぼぽぉょ")):
    for ch in row:
        VOWEL[ch] = v
LONG = {"a": "あ", "i": "い", "u": "う", "e": "えい", "o": "おう"}   # この母音のあとに来ると長音とみなす字


def pattern(want):
    """期待の読みを正規表現に：語の中の長音の位置だけ「ー か長音の字」を許す（こう＝こー・けい＝けー）。
    ⚠️ 読みの側（行）はそろえない＝前の語の最後の母音とつながって「〜でえねる」の え を長音とみなす誤りを作らない
    （16本目 2026-10-01 に自分で踏んだ：エネル・イタリア・アルベリコ・アドリアが「読みに無い」と出た）"""
    out, v = [], None
    for ch in want:
        if v and (ch == "ー" or ch in LONG[v]):
            out.append(f"[{LONG[v]}ー]")
            continue
        out.append(re.escape(ch))
        v = VOWEL.get(ch)
    return re.compile("".join(out))


def hira(kata):
    s = kata.replace("ヴァ", "バ").replace("ヴィ", "ビ").replace("ヴェ", "ベ").replace("ヴォ", "ボ").replace("ヴ", "ブ")
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)


def judge(text, aq, word, want):
    """(文に出る回数, 読みに出る回数, 句の中に収まる回数)。"""
    if KATA.fullmatch(word):
        n = sum(1 for w in KATA.findall(text) if w == word)
    else:
        n = text.count(word)          # 🔴 表 KANJI の中身に頼らない（19本目で直した）
        n -= sum(text.count(x) for x in EXCLUDE.get(word, ()))
    body = aq.replace("'", "")
    pat = re.compile(re.escape(want)) if word in STRICT else pattern(want)
    inside = sum(len(pat.findall(p)) for p in SEP.split(body))
    return n, len(pat.findall(SEP.sub("", body))), inside


def where(text, word):
    t = text.rstrip("。、？！」）")
    i = text.find(word)
    return "頭" if i == 0 else "尻" if t.endswith(word) else "中"


def load():
    with open(SHEET, encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f, delimiter="\t")]


def from_dict():
    """B. 利用者辞書の全語 {表層形（NFKC）: 発音のひらがな}。"""
    out = {}
    for row in csv.reader(DICT.read_text(encoding="utf-8").splitlines()):
        if row and not row[0].startswith("#") and len(row) >= 13:
            out[unicodedata.normalize("NFKC", row[0])] = hira(row[12])
    return out


def terms(rows):
    """{語: 期待の読み}。カタカナ語は台本から全部拾う（2字以上・ー だけは除く）→ 辞書の全語 → 表 KANJI（あとが勝つ）。"""
    out = {}
    for r in rows:
        for w in KATA.findall(r["文"]):
            if len(w.strip("ー")) >= 2:
                out.setdefault(w, hira(w))
    out.update(from_dict())
    out.update(KANJI)
    return out


def main():
    rows = load()
    want = terms(rows)
    n_dict = len(from_dict())
    bad, seen = [], {w: [] for w in want}
    for r in rows:
        for w, k in want.items():
            if w not in r["文"]:
                continue
            n, got, inside = judge(r["文"], r["音声記号列"], w, k)
            if n == 0:
                continue
            ok = got >= n and (inside >= n or w in MULTI)
            seen[w].append((r["行ID"], where(r["文"], w), ok))
            if not ok:
                why = "読みに無い" if got < n else "語の途中で句が割れた"
                bad.append(f"{r['行ID']}（{where(r['文'], w)}）「{w}」→ 期待 {k}：{why}｜{r['音声記号列']}")
    if "--list" in sys.argv:
        for w, hits in sorted(seen.items(), key=lambda x: -len(x[1])):
            if hits:
                marks = " ".join(f"{lid}{pos}{'' if ok else '✗'}" for lid, pos, ok in hits)
                print(f"{w}（{want[w]}）{len(hits)}行：{marks}")
    unused = [w for w in KANJI if not seen[w]]
    unused_dict = [w for w in from_dict() if not seen.get(w)]
    print(f"語 {sum(1 for v in seen.values() if v)}（表 KANJI {len(KANJI)}・辞書 {n_dict}・残りはカタカナ）／"
          f"当たらない・割れた {len(bad)}件／台本に出ない表の語 {unused}／台本に出ない辞書の語 {unused_dict}")
    for b in bad:
        print("  ✗ " + b)
    return 1 if bad or unused_dict else 0


def chars(cs):
    for r in load():
        if any(c in r["文"] for c in cs):
            print(f"{r['行ID']}\t{r['文']}\n\t{r['音声記号列']}")
    return 0


def selftest():
    fails = []
    ok = lambda c, n: None if c else fails.append(n)   # noqa: E731
    # 19本目までの見本（回によらない型）
    ok(judge("アルベリコ・ビアデーネだ。", "あるべり'こ/び'あで/ーねだ。", "ビアデーネ", "びあでーね") == (1, 1, 0),
       "陽性対照：語の途中で割れた（びあで/ーね）を拾う")
    ok(judge("アルベリコ・ビアデーネだ。", "あるべり'こ/びあでーねだ。", "ビアデーネ", "びあでーね") == (1, 1, 1),
       "陰性対照：1つの句なら通る")
    ok(judge("公聴会で", "こーちょ'ーかいで", "公聴会", "こうちょうかい") == (1, 1, 1), "長音の ー と う を同じとみなす（表の外の語）")
    ok(hira("ピアーヴェ") == "ぴあーべ" and hira("ヴィッラノーヴァ") == "びっらのーば", "ヴ→ば行")
    ok(judge("ダムとダム", "だ'むと/だ'む", "ダム", "だむ") == (2, 2, 2), "回数を数える")
    ok(judge("ダムとダム", "だ'むと/だ", "ダム", "だむ")[1] == 1, "陽性対照：2回出る語の1回が読みに無い")
    ok(judge("法律で、エネルという", "ほーりつで、えね'ると/いう", "エネル", "えねる") == (1, 1, 1),
       "前の語の最後の母音（で）と次の語の頭（え）を長音とみなさない")
    # 21本目の見本＝辞書なしの読み一覧（2026-10-12）の実物の誤り（陽性）と、直したあとの形（陰性）
    ok(judge("NEADS は、", "えぬいーえーでぃーえすわ、", "NEADS", "にーず")[1] == 0,
       "陽性対照：NEADS を1字ずつ（えぬいーえー…）読んだら拾う")
    ok(judge("NEADS は、", "に'ーずわ、", "NEADS", "にーず") == (1, 1, 1), "陰性対照：にーず なら通る")
    ok(judge("FAA の", "えふえ'い/え'い/の'", "FAA", "えふえいえい") == (1, 1, 0),
       "陽性対照：英字の略語が2つの句に割れた（えふえい/えい）を拾う")
    ok(judge("ハーンドンにある。", "は'ーん/ど'んに/あ'る。", "ハーンドン", "はーんどん") == (1, 1, 0),
       "陽性対照：地名が語の途中で割れた（はーん/どん）を拾う")
    ok(judge("何人かは、", "なににんかわ、", "何人", "なんにん")[1] == 0, "陽性対照：何人＝なににん を拾う")
    ok(judge("札は消えたが、", "さつわ/きえた'が、", "札", "ふだ")[1] == 0, "陽性対照：札＝さつ を拾う")
    ok(judge("同じってこと？", "ど'ーじってこと？", "同じ", "おなじ")[1] == 0, "陽性対照：同じ＝どうじ を拾う")
    ok(judge("上の人たちと", "うえの'じんたちと", "上の人たち", "うえのひとたち")[1] == 0, "陽性対照：上の人たち＝じん を拾う")
    ok(judge("違う方へ", "ちがうか'たえ", "違う方", "ちがうほう")[1] == 0, "陽性対照：違う方＝ちがうかた を拾う")
    ok(judge("約7,900メートル", "や'くなな、きゅーひゃくめ'ーとる", "7,900メートル", "ななせんきゅうひゃくめーとる")[1] == 0,
       "陽性対照：カンマで割れた数を拾う")
    ok(judge("10時0分25秒。", "じゅ'ーじ/ぜろ'ふん/にじゅーご'びょー。", "10時0分25秒", "じゅうじれいふんにじゅうごびょう")[1] == 0,
       "陽性対照：0分＝ぜろふん を拾う")
    ok(judge("英語で「Roll it」だ。", "えーごで/ろ'ーるあいてぃーだ。", "Roll it", "ろーるいっと")[1] == 0,
       "陽性対照：it を I・T と読んだら拾う")
    ok(judge("機体はボーイング767。", "きたいわ/ぼ'ーいんぐ/ななひゃくろくじゅーな'な。", "767", "ななろくなな")[1] == 0,
       "陽性対照：767＝ななひゃく… を拾う")
    ok(judge("航空の安全", "こーくーの/あ'んぜん", "空の", "そらの") == (0, 0, 0), "EXCLUDE：航空の の中の 空の を数えない")
    ok(judge("命令が何時何分に出たのかは、", "めーれーが/な'んじ/なに'ぷんに/で'たのかわ、", "何分", "なんぷん")[1] == 0,
       "陽性対照：1行の2つ目の「何」（何時何分の 何分＝なにぷん）を拾う＝an21.py の grep の穴を表で埋める")
    ok(judge("もう地上にあったからだ。", "も'ー/ちじょーに/あ'った/からだ。", "ったからだ", "ったからだ") == (1, 1, 0),
       "陽性対照：からだ の独り立ち（体 に聞こえる）を拾う")
    # ② 辞書の全語を当てる（読みの答えは辞書の発音）
    d = from_dict()
    ok(d.get("NEADS") == "にーず" and d.get("4,500機") == "よんせんごひゃっき" and d.get("it") == "いっと",
       "辞書の表層形は NFKC・発音はひらがな（ＮＥＡＤＳ→NEADS・４，５００→4,500）")
    if fails:
        print(f"selftest: 落ちた {len(fails)}: {fails}")
        return 1
    print("selftest: 全部合格（24項目）")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--chars" in sys.argv:
        sys.exit(chars(sys.argv[sys.argv.index("--chars") + 1]))
    sys.exit(main())
