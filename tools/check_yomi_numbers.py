# -*- coding: utf-8 -*-
r"""check_yomi_numbers.py — **読みが固定されていない「危ない語・数」**を出す門番。

  python tools\check_yomi_numbers.py ep11
  python tools\check_yomi_numbers.py ep11 --list     … 🔴も⚠️も全部出す（台帳を作るとき）
  python tools\check_yomi_numbers.py --selftest      … 物差しそのものを確かめる

🔴🔴 なぜ要るか（2026-09-22・11本目の試写で**40件中13件が数字の誤読**だった）

  ① **数字の誤読は、文字起こしでは原理的に検出できない。**
     ElevenLabs の聞き起こし（Scribe）は「1984年」を
     「せんきゅうひゃくはちじゅう**しよ**ねん」と読んでも **「1984年」と書き戻す**。
     ＝一致率も聞取の字面も、正しく読めた場合とまったく同じになる。
     10本目の「502人＝ごひゃく**ふたり**」と同じ形
     （→ [[feedback-scribe-writes-the-right-word-for-misreadings]]）。
     **だから「聞取で確かめる」道は最初から閉じている。**

  ② **取り直しは読みを固定しない。**11本目の ⑤a は「取り直し26行・辞書5件」で閉じた
     （9本目は辞書79件・10本目65件）。取り直しは「そのテイクがたまたま正しく読めた」だけで、
     **読み方そのものは決めていない。**

  ③ **鍵を長い句で書くと、同じ語の別の出現に当たらない。**11本目は「札」を
     `札が掛かって` と `その札を掛けた` の2句でしか固定しておらず、
     `c813-2`「札が掛かったのは」`c814-2`「札のことは」`c814-3`「札を記した」の
     **3行に1つも当たっていなかった**（試写で3件とも「さつ」と読まれた）。
     → [[feedback-yomi-dict-must-be-verified]]（鍵は `--hits` で行数を数えてから入れる）。

■ この門番が見るもの（「在るか」ではなく「**送信文字列に残っているか**」）

  **`el_script.el_text()` を通したあとの文字列**＝実際にエンジンへ渡る文字列を見る。
  そこに下の型が生で残っていれば「読みは固定されていない」。

    A 西暦4桁      1984年 / 1985年          … 「しよねん」「ごごねん」に崩れた実績
    B 小数         58.788秒 / 0.678秒       … 桁の読みが崩れた実績（5件）
    C 数＋助数詞   37秒 / 7人 / 三つ        … 別の数に化けた実績（37→ごじゅうなな）
    D 型に入らない数 1500万トン / 40歳 / 第7 / リチウム6 … 🔴 2026-09-23（12本目⑤a）に足した。下の注

  🔴 D を足した理由（12本目⑤a）: A〜C は「崩れた実績のある助数詞」だけを見るので、**回ごとに新しい助数詞が
     出ると網の外になる**。12本目は「万トン・歳・隻・冊・割・週間・か月・階建て・ドル・円・第N・リチウムN」で
     **数の半分近くが A〜C のどれにも当たらなかった**（✓ のまま焼くところだった）。数は聞取で検証できない
     （5a-6）ので、型に入らなくても送信文字列に数字が残れば落とす。A〜C と重なる所は二重に数えない。
     ⚠️ これまでの陰性対照「裸の数は出ない（番号は1だ）」は外した＝裸の数も読みは固定されていない。
        陰性対照は「かな化ずみは出ない」が引き継ぐ。

  ⚠️ **全部を機械で白黒付けることはできない。**だから
  **「耳で通した」と記録した行は落とさない**＝台帳 `qa_out/<ep>_yomi_heard.tsv`。
  台帳に無い＝**誰も聞いていない**なので 🔴 で落とす（fail closed）。

■ 台帳の書き方（TSV・1行1件）
    行ID<TAB>語<TAB>判定<TAB>いつ・だれが
    c205-2	1984年	ng	2026-09-22 試写（しよねん）
    c202-2	7000時間	ok	2026-09-22 試写
    c101-1	1974年	phon	2026-09-24 音素の網（qa_out/phon_verify.py）＝耳ではない。耳の ok と分けて数える
   🔴 判定は ok（耳で通した）／phon（音素の網で読みを確かめた・13本目⑤a' から）／ng（直す）。

⚠️ この門番は「**読みが決まっているか**」しか見ない。**正しく読めるかは見ていない。**
   決着は耳（→ [[feedback-ear-beats-the-meter]]）。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent

# 助数詞は**実際に崩れた型**から採った（11本目の試写40件・10本目の「502人」）。
COUNTERS = ("秒", "人", "人目", "本", "つ", "度", "回", "回目", "時間", "分", "時",
            "年", "月", "日", "ミリ", "センチ", "メートル", "キロ", "種類", "倍", "巻", "コマ")
_CTR = "|".join(sorted(COUNTERS, key=len, reverse=True))

RE_YEAR = re.compile(r"[0-9]{4}年")
RE_DEC = re.compile(r"[0-9]+\.[0-9]+")
RE_CTR = re.compile(rf"[0-9]+(?:\.[0-9]+)?(?:{_CTR})")
# 和語の数詞（一つ〜十、三つ など）。「三つ、大きな」が「三つ大きな」に流れた実績
RE_WAGO = re.compile(r"[一二三四五六七八九十]つ")
# D 型に入らない数（2026-09-23 新設・冒頭の注）。全角の数字も拾う
RE_ANY = re.compile(r"[0-9０-９]+(?:[.．][0-9０-９]+)?")


def risky(sent: str):
    """送信文字列に**生で残っている**危ない数の並びを返す（重複なし・出た順）。
    A〜C の型を先に拾い、どの型にも入らない数字だけを D として足す（同じ数を二重に出さない）。"""
    out, seen, spans = [], set(), []
    for pat in (RE_YEAR, RE_DEC, RE_CTR, RE_WAGO):
        for m in pat.finditer(sent):
            spans.append(m.span())
            w = m.group(0)
            if w not in seen:
                seen.add(w)
                out.append(w)
    for m in RE_ANY.finditer(sent):
        if any(a <= m.start() and m.end() <= b for a, b in spans):
            continue
        w = m.group(0)
        if w not in seen:
            seen.add(w)
            out.append(w)
    return out


def load_heard(ep: str) -> dict:
    """`qa_out/<ep>_yomi_heard.tsv` を読む。無ければ空（＝全件が未確認）。"""
    p = ROOT / "qa_out" / f"{ep}_yomi_heard.tsv"
    got = {}
    if not p.exists():
        return got
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        c = ln.split("\t")
        if len(c) < 3:
            raise SystemExit(f"🔴 台帳の列が足りない（3列以上要る）: {ln!r}")
        got[(c[0].strip(), c[1].strip())] = c[2].strip().lower()
    return got


def scan(ep: str):
    import el_script as ES
    heard = load_heard(ep)
    ng, unknown, ok, covered, phon = [], [], 0, 0, 0
    for ln in ES.lines():
        sent = ES.el_text(ln.text)
        if sent != ln.text:
            covered += 1
        for w in risky(sent):
            v = heard.get((ln.lid, w))
            if v == "ok":
                ok += 1
            elif v == "phon":      # 🔴 2026-09-24 音素の網（qa_out/phon_*.py）で読みを確かめた＝**耳ではない**。耳の ok と分けて数える
                phon += 1
            elif v == "ng":
                ng.append((ln.lid, w, ln.text))
            else:
                unknown.append((ln.lid, w, ln.text))
    return ng, unknown, ok, covered, phon


def critical_left(ep: str):
    """`CRITICAL_EP` の語が、送信文字列に**漢字のまま**残っている行。

    🔴 11本目の「札」＝辞書が2句しか当たらず、3行が生のまま残っていた型。
    ⚠️ ここは落とさない（⚠️）。読みが一意に決まる語もあるため。
    🔴 2026-09-23（12本目⑤a）: **辞書で一部の行をかなにしている語だけ**を見るよう絞った。
       この型（札）は「ある行はかな・別の行は漢字」の取りこぼしで、12本目の「灰」「風」のように
       かなにしない鍵語（el_check_heard ④ 用）まで並べると、約90行が毎回 ⚠️ に出て本物を埋もれさせる。
       ⚠️ 鍵の中で**熟語の一部**になっている出現は数えない（「降灰」の鍵は「灰」を含むが別の語。
          最初は `w in k` で判定して、灰の62行が ⚠️ に並んだ＝自分で作った雑音）。
    """
    import el_script as ES
    kanji = lambda c: bool(c) and ("一" <= c <= "鿿" or c == "々")  # noqa: E731

    def standalone(w, k):
        for m in re.finditer(re.escape(w), k):
            a, b = m.start(), m.end()
            if not (kanji(k[a - 1] if a else "") or kanji(k[b] if b < len(k) else "")):
                return True
        return False
    fixed = [w for w in getattr(ES, "CRITICAL_EP", ()) if any(standalone(w, k) for k in ES.EL_YOMI)]
    rows = []
    for ln in ES.lines():
        sent = ES.el_text(ln.text)
        for w in fixed:
            if w in sent:
                rows.append((ln.lid, w, ln.text))
    return rows


def selftest() -> int:
    """🔴 本番の中身が空でも通らなければならない（陽性対照）。"""
    ok = True

    def chk(name, got, want):
        nonlocal ok
        if got != want:
            print(f"  🔴 {name}: {got!r} ≠ {want!r}")
            ok = False
        else:
            print(f"  ✓ {name}")

    chk("西暦", risky("1984年に飛んだ"), ["1984年"])
    chk("小数", risky("そして58.788秒。"), ["58.788", "58.788秒"])
    chk("助数詞", risky("37秒から64秒"), ["37秒", "64秒"])
    chk("和語", risky("三つ、大きな"), ["三つ"])
    chk("かな化ずみは出ない", risky("さんじゅうななびょうから"), [])
    # ⚠️ 陰性対照は**助数詞の付かない裸の数**にする。
    #    最初は `第1巻` を陰性対照にしていたが、`巻` は「いちまき」と読まれうる
    #    ＝**本当に危ない型**で、誤っていたのは門番ではなくテストのほうだった。
    # 🔴 2026-09-23: 「裸の数は出ない」→「出る」に反転（D 型。冒頭の注）
    chk("裸の数も出る（D）", risky("番号は1だ"), ["1"])
    chk("助数詞が付けば出る", risky("第1巻の全文"), ["1巻"])
    chk("型に入らない助数詞も出る（D）", risky("1500万トンと40歳と第7と２冊"), ["1500", "40", "7", "２"])
    # ⚠️ 「月」は C の助数詞＝「3月」は C で出るのが正しい（最初は "3" が D で出ると書いて落ちた＝誤りはテスト側）
    chk("A〜C と重なる数は二重に出ない", risky("1954年3月1日と2.5倍"), ["1954年", "2.5", "3月", "1日", "2.5倍"])
    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    eps = [a for a in sys.argv[1:] if not a.startswith("--")]
    # 🔴 回の名前は**引数が無ければ台本から取る**（`el_script.SLUG`）。
    #    `qa_all.py` に "ep11" と直書きすると、次の回で**前作の名前のまま回り続ける**
    #    （→ [[feedback-per-episode-constants-go-stale]]）。
    if eps:
        ep = eps[0]
    else:
        import el_script as ES
        ep = ES.SLUG
        print(f"（回は el_script.SLUG から取った: {ep}）")
    ng, unknown, ok, covered, phon = scan(ep)
    show_all = "--list" in sys.argv

    print(f"■ {ep} ／ 読み辞書が当たった行 {covered}")
    print(f"   耳で通した {ok} ／ 音素の網で通した {phon} ／ 🔴 直す {len(ng)} ／ ⚠️ 未確認 {len(unknown)}")
    if ng:
        print("\n🔴 台帳が ng と書いている（読みを固定していない）")
        for i, w, t in ng:
            print(f"   {i:9s} {w:12s} {t}")
    if unknown:
        print(f"\n⚠️ 台帳に無い＝**誰も聞いていない** {len(unknown)} 件")
        for i, w, t in (unknown if show_all else unknown[:20]):
            print(f"   {i:9s} {w:12s} {t}")
        if not show_all and len(unknown) > 20:
            print(f"   … ほか {len(unknown) - 20} 件（--list で全部出る）")
    left = critical_left(ep)
    if left:
        print(f"\n⚠️ `CRITICAL_EP` の語が漢字のまま残っている行 {len(left)}")
        for i, w, t in (left if show_all else left[:10]):
            print(f"   {i:9s} {w:12s} {t}")
        if not show_all and len(left) > 10:
            print(f"   … ほか {len(left) - 10} 件")
    if ng or unknown:
        print("\n🔴 読みが決まっていない数がある。"
              "**耳で聞いて台帳へ書くか、EL_YOMI でかなに固定する**まで焼かない。")
        return 1
    print("\n✓ 危ない型の数は、すべて固定されているか、耳か音素の網で通っている")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
