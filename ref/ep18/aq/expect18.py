# -*- coding: utf-8 -*-
"""18本目 スレッシャー号 ⑤a-1：読み一覧に「期待の読み」を機械で当てる（2026-10-04）。

  python ref/ep18/aq/expect18.py            … 当たらない語・語の途中で割れた語を全部出す（あれば exit 1）
  python ref/ep18/aq/expect18.py --list     … 語ごとに、出た行・位置（頭／中／尻）・判定を全部出す
  python ref/ep18/aq/expect18.py --chars 何章島船人行入通  … その字を含む行の文と読みを並べる（人が目で見る）
  python ref/ep18/aq/expect18.py --selftest … 答えの分かっている見本で検算

16本目の `ref/ep16/aq/expect16.py` を写した。変えたのは表 KANJI・MULTI と selftest の見本1つ（英字が消える型）だけ。
読むもの＝ref/ep18/aq/yomi_sheet.tsv（先に `python tools/aq_kana.py --sheet`）。
当てる語:
  A. 台本に出るカタカナ語の**全部**（機械で拾う。「・」で切る）＝期待の読みはカタカナをひらがなにしたもの（ヴ→ば行）
  B. 台本 §6-2 の漢語・§1-6 の用語・英字の入る語・この回で見つけた語＝期待の読みは下の表 KANJI（人が書いた）
判定:
  ① 読み（音声記号列から ' と句読点を外したもの）に、期待の読みが「その語が文に出る回数」以上あるか
  ② 期待の読みが1つのアクセント句の中に収まっているか（語の途中で / ・、で割れていないか）
     ＝pyopenjtalk が外国の名前を「びあで/ーね」「ぴね/だ」と割った形（16本目 2026-10-01 実測）を拾う
  長音は「ー」と母音の字（こう・けい など）を同じとみなす（pyopenjtalk の発音は長音を ー で書く）
⚠️ 当たり＝「その読みが行のどこかにある」まで。どの語の読みかまでは見ていない＝最後は読み一覧を人とサブエージェントが読む
⚠️ 数（1日・1人日 など）はここでは見ない＝数の台帳 `check_aq_yomi`
"""
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
SHEET = HERE / "yomi_sheet.tsv"

# B. 漢語の期待の読み（長音は ー でも母音の字でもよい）。鍵は台本の字のまま
KANJI = {
    # 台本 §6-2（④の候補）。⚠️ 銀ろう付け＝AquesTalk の音節の表に「づ」が無い＝ず で書くのが正しい（仕様書 v2.0）
    "査問会": "さもんかい", "艦船局": "かんせんきょく", "継手": "つぎて", "銀ろう付け": "ぎんろうずけ",
    "保温材": "ほおんざい", "減圧弁": "げんあつべん", "こし器": "こしき", "主冷却材": "しゅれいきゃくざい",
    "内破": "ないは", "鋳物": "いもの", "予定表": "よていひょう", "喪失": "そうしつ", "怠慢": "たいまん",
    "帰せられない": "きせられない", "何通り": "なんとおり", "何時間": "なんじかん", "何メートル": "なんめーとる",
    "何が": "なにが", "行方不明": "ゆくえふめい", "考え方": "かんがえかた", "整備の間": "せいびのあいだ",
    # 台本 §6-2 🔧 第2版で足した語（④'の所見）
    "主タンク": "しゅたんく", "元設計部長": "もとせっけいぶちょう", "元分析官": "もとぶんせきかん",
    # ⚠️ 手りゅう弾＝台本 §6-2 は「てりゅうだん」だが、辞書の主な読み・ニュースの読みは しゅりゅうだん＝変換器のまま採る（2026-10-04 ⑤a-1）
    "分析官": "ぶんせきかん", "復水器": "ふくすいき", "頁": "ぺーじ", "手りゅう弾": "しゅりゅうだん",
    "兆し": "きざし", "真鍮": "しんちゅう", "重り": "おもり", "磁力計": "じりょくけい", "一区画": "ひとくかく",
    "AP通信": "えーぴーつうしん", "地質観測所": "ちしつかんそくじょ", "私生活": "しせいかつ", "曳いた": "ひいた",
    "綱": "つな", "記録簿": "きろくぼ", "賢明": "けんめい", "現役": "げんえき",
    # 台本 §1-6 の用語（初出で一言）
    "試験深度": "しけんしんど", "救難艦": "きゅうなんかん", "公聴会": "こうちょうかい", "認定": "にんてい",
    "勧告": "かんこく", "系統": "けいとう", "水中電話": "すいちゅうでんわ", "救難室": "きゅうなんしつ",
    "超音波": "ちょうおんぱ", "意見書": "いけんしょ", "潜水艇": "せんすいてい", "扉": "とびら", "人日": "にんにち",
    # ⑤a-1 の見直し（型の字の読みの組を重ねずに並べて目で見た・2026-10-04）で見つけた語
    "何度": "なんど", "何か月": "なんかげつ", "何だった": "なんだった", "造船所": "ぞうせんじょ", "観測所": "かんそくじょ",
    "上の人たち": "うえのひとたち", "より後": "よりあと", "通ってしまう": "とおってしまう", "メートル上": "めーとるうえ",
    # サブエージェント2本の指摘で直した語（自分で確かめた・2026-10-04）と、辞書の「管」1語で崩れないかの見張り（配管・管理者）
    "潜る": "もぐる", "札": "ふだ", "管どうし": "くだどうし", "真鍮の管": "しんちゅうのくだ", "管には": "くだにわ",
    "配管": "はいかん", "管理者": "かんりしゃ", "ろう付け": "ろうずけ", "開けた海": "ひらけたうみ", "ありうる": "ありうる",
}
# 助詞・記号・英字をはさむ語＝2つの句に分かれるのが自然（② を見ない）。
# ⚠️ 英字の語（ジョン・C・カルフーン ほか）は語りに出ない（画の欄だけ）＝語りの英字は「AP通信」3行だけ（2026-10-04 に読み一覧の文で数えた）
MULTI = {"整備の間", "AP通信", "上の人たち", "より後", "通ってしまう", "真鍮の管", "開けた海"}
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
    if word in KANJI:
        n = text.count(word)
    else:
        n = sum(1 for w in KATA.findall(text) if w == word)
    body = aq.replace("'", "")
    pat = pattern(want)
    inside = sum(len(pat.findall(p)) for p in SEP.split(body))
    return n, len(pat.findall(SEP.sub("", body))), inside


def where(text, word):
    t = text.rstrip("。、？！」）")
    i = text.find(word)
    return "頭" if i == 0 else "尻" if t.endswith(word) else "中"


def load():
    with open(SHEET, encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f, delimiter="\t")]


def terms(rows):
    """{語: 期待の読み}。カタカナ語は台本から全部拾う（2字以上・ー だけは除く）。"""
    out = {}
    for r in rows:
        for w in KATA.findall(r["文"]):
            if len(w.strip("ー")) >= 2:
                out.setdefault(w, hira(w))
    out.update(KANJI)
    return out


def main():
    rows = load()
    want = terms(rows)
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
    print(f"語 {sum(1 for v in seen.values() if v)}（カタカナ {len(want) - len(KANJI)}・漢語 {len(KANJI)}）／"
          f"当たらない・割れた {len(bad)}件／台本に出ない表の語 {unused}")
    for b in bad:
        print("  ✗ " + b)
    return 1 if bad else 0


def chars(cs):
    for r in load():
        if any(c in r["文"] for c in cs):
            print(f"{r['行ID']}\t{r['文']}\n\t{r['音声記号列']}")
    return 0


def selftest():
    fails = []
    ok = lambda c, n: None if c else fails.append(n)   # noqa: E731
    ok(judge("アルベリコ・ビアデーネだ。", "あるべり'こ/び'あで/ーねだ。", "ビアデーネ", "びあでーね") == (1, 1, 0),
       "陽性対照：語の途中で割れた（びあで/ーね）を拾う")
    ok(judge("アルベリコ・ビアデーネだ。", "あるべり'こ/びあでーねだ。", "ビアデーネ", "びあでーね") == (1, 1, 1),
       "陰性対照：1つの句なら通る")
    ok(judge("水理学の教授", "みずり'がくの/きょーじゅ", "水理学", "すいりがく")[1] == 0, "陽性対照：読み違い（みずりがく）を拾う")
    # ⚠️ 16本目の見本（控訴審・公社）は16本目の表 KANJI にある語が前提だった＝18本目の表の語で同じ型を見る（2026-10-04）
    ok(judge("公聴会で", "こーちょ'ーかいで", "公聴会", "こうちょうかい") == (1, 1, 1), "長音の ー と う を同じとみなす")
    ok(judge("艦の系統", "かんの/けーとー", "系統", "けいとう") == (1, 1, 1), "長音（けい＝けー・とう＝とー）")
    ok(hira("ピアーヴェ") == "ぴあーべ" and hira("ヴィッラノーヴァ") == "びっらのーば", "ヴ→ば行")
    ok(judge("ダムとダム", "だ'むと/だ'む", "ダム", "だむ") == (2, 2, 2), "回数を数える")
    ok(judge("ダムとダム", "だ'むと/だ", "ダム", "だむ")[1] == 1, "陽性対照：2回出る語の1回が読みに無い")
    ok(judge("法律で、エネルという", "ほーりつで、えね'ると/いう", "エネル", "えねる") == (1, 1, 1),
       "前の語の最後の母音（で）と次の語の頭（え）を長音とみなさない")
    ok(judge("責任者、アルベリコ", "せきに'んしゃ、あるべり'こ", "アルベリコ", "あるべりこ") == (1, 1, 1),
       "同上（しゃ＋あ）")
    # 18本目で足した見本：英字が黙って消える型（ルール 5a-26・14本目の A甲板）
    ok(judge("ジョン・C・カルフーン", "じょ'ん/かるふ'ーん", "C・カルフーン", "しーかるふーん")[1] == 0,
       "陽性対照：英字 C が読みから消えたら拾う")
    ok(judge("ジョン・C・カルフーン", "じょ'ん、し'ー、かるふ'ーん", "C・カルフーン", "しーかるふーん")[1] == 1,
       "陰性対照：C が しー と読めていれば通る")
    if fails:
        print(f"selftest: 落ちた {len(fails)}: {fails}")
        return 1
    print("selftest: 全部合格")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--chars" in sys.argv:
        sys.exit(chars(sys.argv[sys.argv.index("--chars") + 1]))
    sys.exit(main())
