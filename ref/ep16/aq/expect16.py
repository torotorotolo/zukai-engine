# -*- coding: utf-8 -*-
"""16本目 バイオントダム災害 ⑤a-1：読み一覧に「期待の読み」を機械で当てる（2026-10-01）。

  python ref/ep16/aq/expect16.py            … 当たらない語・語の途中で割れた語を全部出す（あれば exit 1）
  python ref/ep16/aq/expect16.py --list     … 語ごとに、出た行・位置（頭／中／尻）・判定を全部出す
  python ref/ep16/aq/expect16.py --chars 何章島船人行入通  … その字を含む行の文と読みを並べる（人が目で見る）
  python ref/ep16/aq/expect16.py --selftest … 答えの分かっている見本で検算

読むもの＝ref/ep16/aq/yomi_sheet.tsv（先に `python tools/aq_kana.py --sheet`）。
当てる語:
  A. 台本に出るカタカナ語の**全部**（機械で拾う。「・」で切る）＝期待の読みはカタカナをひらがなにしたもの（ヴ→ば行）
  B. 台本 §6-2 の漢語・④' の申し送り（台本 §0-7）・この回で見つけた語＝期待の読みは下の表 KANJI（人が書いた）
判定:
  ① 読み（音声記号列から ' と句読点を外したもの）に、期待の読みが「その語が文に出る回数」以上あるか
  ② 期待の読みが1つのアクセント句の中に収まっているか（語の途中で / ・、で割れていないか）
     ＝pyopenjtalk が伊語の名前を「びあで/ーね」「ぴね/だ」「べっ/るーの」と割った形（2026-10-01 実測）を拾う
  長音は「ー」と母音の字（こう・けい など）を同じとみなす（pyopenjtalk の発音は長音を ー で書く）
⚠️ 当たり＝「その読みが行のどこかにある」まで。どの語の読みかまでは見ていない＝最後は読み一覧を人とサブエージェントが読む
⚠️ 数（1日・3年8か月 など）はここでは見ない＝数の台帳 `check_aq_yomi`
"""
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
SHEET = HERE / "yomi_sheet.tsv"

# B. 漢語の期待の読み（台本 §6-2・§0-7。長音は ー でも母音の字でもよい）。鍵は台本の字のまま
KANJI = {
    "トック山": "とっくさん", "天端": "てんば", "越流": "えつりゅう", "破毀院": "はきいん", "予審": "よしん",
    "恩赦": "おんしゃ", "控訴審": "こうそしん", "一審": "いっしん", "憲兵隊": "けんぺいたい", "水理模型": "すいりもけい",
    "水理学": "すいりがく", "石灰岩": "せっかいがん", "公社": "こうしゃ", "土木局": "どぼくきょく", "上院": "じょういん",
    "下院": "かいん", "塊": "かたまり", "悼": "いた", "葬り": "ほうむり", "償": "つぐな", "見立て": "みたて",
    "部会長": "ぶかいちょう", "峡谷": "きょうこく", "亀裂": "きれつ", "予見": "よけん", "見通": "みとお",
    "粘土": "ねんど", "泥まじり": "どろまじり", "差し押さえ": "さしおさえ", "測量技師": "そくりょうぎし",
    "公共事業大臣": "こうきょうじぎょうだいじん", "採決": "さいけつ", "過失": "かしつ", "谷底": "たにそこ",
    "頂上": "ちょうじょう", "理屈": "りくつ", "本文": "ほんぶん", "作業員小屋": "さぎょういんごや",
    "最低限": "さいていげん", "議長": "ぎちょう", "鐘の塔": "かねのとう", "1辺": "いっぺん",
    # ⑤a-1 の見直しで見つけた語（--chars と読み一覧の目視・2026-10-01）
    "何度": "なんど", "何人": "なんにん", "何日": "なんにち", "何週間": "なんしゅうかん",
    "いちばん上": "いちばんうえ", "いちばん下": "いちばんした", "メートル下": "めーとるした",
    "多数派": "たすうは", "少数派": "しょうすうは",
    "立ちのく": "たちのく", "立ちのかせ": "たちのかせ", "立ちのいて": "たちのいて",
    # サブエージェント（前半）の指摘で直した語
    "すべり面": "すべりめん", "刷られた": "すられた", "ピアーヴェ川": "ぴあーべがわ", "進み具合": "すすみぐあい",
    "第8章": "だいはっしょう", "第1章": "だいいっしょう",
    # サブエージェント（後半）の指摘で直した語（c720-2 の「山が」は手書き＝ここでは見ない）
    "1人1人": "ひとりひとり", "念のため": "ねんのため", "二重アーチダム": "にじゅうあーちだむ",
}
MULTI = {"鐘の塔"}   # 助詞をはさむ語＝2つの句に分かれるのが自然（② を見ない）
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
    （2026-10-01 に自分で踏んだ：エネル・イタリア・アルベリコ・アドリアが「読みに無い」と出た）"""
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
    ok(judge("控訴審で", "こーそ'しんで", "控訴審", "こうそしん") == (1, 1, 1), "長音の ー と う を同じとみなす")
    ok(judge("国の公社", "くにの/こーしゃ", "公社", "こうしゃ") == (1, 1, 1), "長音（こう＝こー）")
    ok(hira("ピアーヴェ") == "ぴあーべ" and hira("ヴィッラノーヴァ") == "びっらのーば", "ヴ→ば行")
    ok(judge("ダムとダム", "だ'むと/だ'む", "ダム", "だむ") == (2, 2, 2), "回数を数える")
    ok(judge("ダムとダム", "だ'むと/だ", "ダム", "だむ")[1] == 1, "陽性対照：2回出る語の1回が読みに無い")
    ok(judge("法律で、エネルという", "ほーりつで、えね'ると/いう", "エネル", "えねる") == (1, 1, 1),
       "前の語の最後の母音（で）と次の語の頭（え）を長音とみなさない")
    ok(judge("責任者、アルベリコ", "せきに'んしゃ、あるべり'こ", "アルベリコ", "あるべりこ") == (1, 1, 1),
       "同上（しゃ＋あ）")
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
