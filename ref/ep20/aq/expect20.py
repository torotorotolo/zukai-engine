# -*- coding: utf-8 -*-
"""20本目 日本航空123便 ⑤a-1：読み一覧に「期待の読み」を機械で当てる（2026-10-08）。

  python ref/ep20/aq/expect20.py            … 当たらない語・語の途中で割れた語を全部出す（あれば exit 1）
  python ref/ep20/aq/expect20.py --list     … 語ごとに、出た行・位置（頭／中／尻）・判定を全部出す
  python ref/ep20/aq/expect20.py --chars 何縁下方  … その字を含む行の文と読みを並べる（人が目で見る）
  python ref/ep20/aq/expect20.py --selftest … 答えの分かっている見本で検算

19本目の `ref/ep19/aq/expect19.py` を写した（18本目・16本目の expect16.py が元）。変えたのは3点:
  ① 表 KANJI・MULTI（20本目の語）
  ② 🆕 **利用者辞書 userdict.csv の全語にも期待の読みを当てる**（表層形を NFKC にした字・発音をひらがなにした読み）。
     なぜ：1字の鍵「縁」は「後ろの縁」「前の縁」でしか選ばれず、「穴の縁」「板の縁」ほか5行は えん のまま残った
     （2026-10-08・全行の突き合わせで見つけた）＝「辞書に入れた」は「その行で効いた」ではない。辞書の語が文脈で選ばれない事故を
     全行で拾う。⚠️ 読みの答えは辞書そのもの＝読みの正しさは表 KANJI と人の目（ここが見るのは「効いたか」と「句が割れないか」）
  ③ selftest の見本を20本目の実物（辞書なしの読み一覧の誤り）に
読むもの＝ref/ep20/aq/yomi_sheet.tsv（先に `python tools/aq_kana.py --sheet`）。
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
    # 台本 §6 の漢字
    "隔壁": "かくへき", "与圧": "よあつ", "昇降舵": "しょうこうだ", "方向舵": "ほうこうだ", "補助翼": "ほじょよく",
    "継ぎ板": "つぎいた", "鋲": "びょう", "縞": "しま", "中破": "ちゅうは", "若しくは": "もしくわ", "空挺": "くうてい",
    "猟友会": "りょうゆうかい", "防火壁": "ぼうかへき", "化粧室": "けしょうしつ", "暗視装置": "あんしそうち",
    "断熱材": "だんねつざい", "付着物": "ふちゃくぶつ", "余白": "よはく", "物入れ": "ものいれ", "建議": "けんぎ",
    "勧告": "かんこく", "趣旨": "しゅし", "頁": "ぺーじ",
    # 台本 §6 の地名（語りに出るもの）
    "上野村": "うえのむら", "奥多摩町": "おくたままち", "大月": "おおつき", "熊谷": "くまがや", "相模湾": "さがみわん",
    "駿河湾": "するがわん", "横田": "よこた", "伊豆半島": "いずはんとう", "羽田": "はねだ", "スゲノ沢": "すげのさわ",
    "名古屋": "なごや", "群馬県": "ぐんまけん", "山梨県": "やまなしけん", "長野県警": "ながのけんけい",
    # 台本 §6 の英字・番号・CVR の英語
    "JA8119": "じぇいえいはちいちいちきゅう", "747": "ななよんなな", "APU": "えいぴーゆー", "FAA": "えふえいえい",
    "L18": "えるじゅうはち", "R18": "あーるじゅうはち", "C整備": "しーせいび", "U字溝": "ゆーじこう", "GPS": "じーぴーえす",
    "CVR": "しーぶいあーる", "NTSB": "えぬてぃーえすびー", "uncontrol": "あんこんとろーる", "C-130": "しーひゃくさんじゅう",
    "スコーク77": "すこーくなななな", "77は": "ななななわ", "7700": "ななななぜろぜろ",
    # ⑤a-1 で見つけて直した語（2026-10-08・辞書なしの読み一覧を語＝読みの組で全部見た）
    "縁": "ふち", "尾部": "びぶ", "深海": "しんかい", "上下": "じょうげ", "下半分": "したはんぶん", "上半分": "うえはんぶん",
    "上の方": "うえのほう", "後ろの方": "うしろのほう", "亡くなった方": "なくなったかた", "道すじの下": "みちすじのした",
    "当て板": "あていた", "から松林": "からまつばやし", "1回転": "いっかいてん", "摂氏0度": "せっしれいど", "近すぎ": "ちかすぎ",
    "何度": "なんど", "何列": "なんれつ", "何本": "なんぼん", "何日": "なんにち", "何でしたか": "なんでしたか",
    "何も": "なにも", "何が": "なにが", "何か": "なにか",
    "っていたからだ": "っていたからだ", "なるからだ": "なるからだ", "チームが行った": "ちーむがおこなった",
    "継ぎ方": "つぎかた", "着け方": "つけかた", "揺れ方": "ゆれかた", "壊れ方": "こわれかた",
    # 係2本（前半・後半）の指摘を自分で確かめて直した語（2026-10-08）＝辞書の語は B で当たる・ここは手書きで直した所と型の見張り
    "山の上": "やまのうえ", "表からは": "おもてからわ", "開いた穴": "あいたあな", "穴が開い": "あながあい", "穴が開き": "あながあき",
    "大きく開いた": "おおきくひらいた", "壊れ得る": "こわれうる", "そのあと": "そのあと", "32分ぶん": "さんじゅうにふんぶん",
    "富士山": "ふじさん",
}
# 語の中に別の語として含まれる字の並び＝回数から引く（辞書の1字の鍵「山」は 富士山・登山口・登山道 の中の 山 を数えない）
EXCLUDE = {"山": ("富士山", "登山")}
# 助詞・記号・英字をはさむ語＝2つの句に分かれるのが自然（② を見ない）
MULTI = {"スコーク77", "何も", "何が", "何か", "チームが行った", "開いた穴", "穴が開い", "穴が開き", "大きく開いた", "山の上"}
# 長音とみなさない語＝期待の読みを字のとおりに当てる（19本目・20本目 c620-2 の 山の上＝やまのーえ の型）
STRICT = {"山の上"}
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
    # 20本目の見本＝辞書なしの読み一覧（2026-10-08）の実物の誤り（陽性）と、直したあとの形（陰性）
    ok(judge("フゴイドと呼ぶ。", "ふ'/ごい'どと/よぶ。", "フゴイド", "ふごいど") == (1, 1, 0),
       "陽性対照：フゴイド＝ふ/ごいど（行の頭で割れた）を拾う")
    ok(judge("この日、JA8119 は、", "この'ひ、じぇいえ'い/はっせんひゃくじゅーきゅ'ーわ、", "JA8119",
             "じぇいえいはちいちいちきゅう")[1] == 0, "陽性対照：登録記号を数（はっせん…）で読んだら拾う")
    ok(judge("この日、JA8119 は、", "この'ひ、じぇいえいはちいちいちきゅーわ、", "JA8119",
             "じぇいえいはちいちいちきゅう") == (1, 1, 1), "陰性対照：はちいちいちきゅー なら通る")
    ok(judge("方向舵と", "ほーこ'ーかじと", "方向舵", "ほうこうだ")[1] == 0, "陽性対照：方向舵＝ほうこうかじ を拾う")
    ok(judge("リベットの穴の縁から、", "りべ'っとの/あな'の/え'んから、", "縁", "ふち")[1] == 0, "陽性対照：縁＝えん を拾う")
    ok(judge("壁の上の方は、", "かべの/うえの'かたわ、", "上の方", "うえのほう")[1] == 0, "陽性対照：上の方＝うえのかた を拾う")
    ok(judge("壁の上の方が", "かべのうえ'のほおが", "上の方", "うえのほう") == (1, 1, 1),
       "陰性対照：ほお は ほう と同じ音（長音）＝通す")
    ok(judge("約2万4,000フィート", "や'く/にまんよ'ん、ぜろぜろぜろふぃ'ーと", "4,000フィート", "よんせんふぃーと")[1] == 0,
       "陽性対照：カンマで割れた数を拾う")
    ok(judge("何度も", "なに'ども", "何度", "なんど")[1] == 0, "陽性対照：何度＝なにど を拾う")
    ok(judge("「But now uncontrol.」", "ばっと'なうゆーえぬしーおーえぬてぃーあーるおーえる。", "uncontrol",
             "あんこんとろーる")[1] == 0, "陽性対照：英語を1字ずつ読んだら拾う")
    ok(judge("APU の前の", "えいぴ'ー/ゆ'ー/の'/ま'えの", "APU", "えいぴーゆー") == (1, 1, 0),
       "陽性対照：英字の略語が2つの句に割れた（えいぴー/ゆー）を拾う")
    # 🆕 ② 辞書の全語を当てる（読みの答えは辞書の発音）
    d = from_dict()
    ok(d.get("縁") == "ふち" and d.get("JA8119") == "じぇいえいはちいちいちきゅー" and d.get("4,000フィート") == "よんせんふぃーと",
       "辞書の表層形は NFKC・発音はひらがな（ＪＡ８１１９→JA8119・４，０００→4,000）")
    if fails:
        print(f"selftest: 落ちた {len(fails)}: {fails}")
        return 1
    print("selftest: 全部合格（19項目）")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--chars" in sys.argv:
        sys.exit(chars(sys.argv[sys.argv.index("--chars") + 1]))
    sys.exit(main())
