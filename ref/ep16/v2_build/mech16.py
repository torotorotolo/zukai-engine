# -*- coding: utf-8 -*-
"""16本目④'：台本の機械の数え（読むだけ・tools/ は import するだけで直さない）。
④の scratchpad の m16.py と 15本目 ref/ep15/v2_build/mech15.py を16本目に合わせて1本にした。
    python ref/ep16/v2_build/mech16.py ref/ep16/daihon_v2.md [--roles ref/ep16/v2_build/roles.tsv]
    python ref/ep16/v2_build/mech16.py --selftest
尺の式（ゆっくり・ルール §5a-28・§5a-28b）＝句読点なし字数 ÷ 380字/分（句読点＝ 、。？！「」（）・ ）。
  ⚠️ 門番 check_script の est_sec は ElevenLabs の定数のまま＝この台本では約50分と出る（既知の誤り）。ここでは使わない
節
 1 タイトル案（§1-1 の表）の字数と型・公開ずみ13本の題（titles16.json＝oEmbed で 09-26 に取った今の題）
 2 出典の札（文書ごとの延べ・範囲外の頁・略号で始まらない札）
 3 ★の位置（最後の行か）と字数（20字以内か）
 4 文の長さ（カットの中で行をつなぎ、。？！で割る。★の行と話者の替わり目も切れ目）・40字超／1行40字超
 5 内部の数字の grep（% 維持 再生 視聴 登録 チャンネル CTR インプレ）＝ルール 4'-17（§0 を除く全体）
 6 使わない言い方（sources.md §3・§B2-4・§B3-5）
 7 聞き役（tools/check_listener.py の judge() をそのまま使う。秒だけ ÷380 の式で渡す）＋ roles.tsv と1行ずつ
 8 冒頭の秒（÷380 を1行ずつ足す）
 9 章ごと（カット・行・句読点なし・分・写真・頁・再現・図解・文字だけ・決め所・聞き役）と3通りの尺
10 文字だけの連続（パネル・決め所・文字の頁）
11 見る向き（画の欄の【横から】【上から】と「合図」）＝ルール 5b-80
"""
import collections
import json
import os
import re
import statistics
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
os.chdir(ROOT)
import check_script as cs  # noqa: E402
import check_listener as cl  # noqa: E402
import speaker  # noqa: E402

NP = set("、。？！「」（）・")
RATE = 380.0
KOUSEI_NP = 13870                      # kousei.md の目標（句読点なし）
BAND = (36 * 60, 37 * 60)              # 目標36〜37分（ルール §③・§5a-28）
ID_RE = r"c[1-9ab]\d{2}"


def np_len(s):
    return sum(1 for ch in s if ch not in NP)


def mmss(sec):
    s = int(round(sec))
    return "%d:%02d" % (s // 60, s % 60)


def kind(pic):
    p = pic.strip()
    if p.startswith("quote"):
        return "決め所"
    if p.startswith("panel"):
        return "パネル"
    if p.startswith("実写"):
        return "写真"
    if re.match(r"図\s*p\d", p):
        return "頁"
    if p.startswith("図 再現イラスト") or p.startswith("図 案C"):
        return "再現イラスト"
    if p.startswith("図"):
        return "図解"
    return "?"


def view(pic):
    """画の欄の見る向き。【上から】【横から】を正に読み、無ければ語で推し量る（推し量りは ? を付ける）。"""
    if "【上から】" in pic:
        return "上"
    if "【横から】" in pic:
        return "横"
    if "【正面から】" in pic:
        return "正面"
    if kind(pic) not in ("再現イラスト", "図解"):
        return None
    if re.search(r"上から|地図", pic):
        return "上?"
    if "断面" in pic:
        return "横?"
    return None


def rows_of(cuts):
    """check_listener.judge() に渡す行＝(cid, 行番号, who, 文, 開始秒)。秒は ÷380 を1行ずつ足す。"""
    rows, t = [], 0.0
    for cid, _, ls in cuts:
        for i, raw in enumerate(ls, 1):
            who, b = speaker.split(cs.STAR_RE.sub("", raw).strip())
            rows.append((cid, i, who, b, t))
            t += np_len(cs.clean(raw)) / RATE * 60
    return rows, t


def sentences(cuts):
    out = []
    for cid, _, ls in cuts:
        buf, who0 = "", None
        for raw in ls:
            star = bool(cs.STAR_RE.match(raw))
            who = speaker.is_q(raw)
            txt = cs.clean(raw)
            if buf and (star or who != who0):
                out.append((cid, buf)); buf = ""
            who0 = who
            for piece in re.split(r"(?<=[。？！])", txt):
                if not piece:
                    continue
                buf += piece
                if re.search(r"[。？！]$", buf):
                    out.append((cid, buf)); buf = ""
            if star and buf:
                out.append((cid, buf)); buf = ""
        if buf:
            out.append((cid, buf))
    return out


def analyze(path, roles_path=None):
    T = Path(path).read_text(encoding="utf-8")
    cuts = cs.parse(T)
    lines = [(cid, l) for cid, _, ls in cuts for l in ls]
    chars = sum(len(cs.clean(l)) for _, l in lines)
    npc = sum(np_len(cs.clean(l)) for _, l in lines)
    yk = npc / RATE * 60
    m = cs.measure(cuts)
    print(f"== {path}")
    print(f"  カット {len(cuts)} ／ 行 {len(lines)} ／ 本文 {chars}字（句読点こみ・印を除く）／ 句読点なし {npc}字（kousei {KOUSEI_NP} の {100 * npc / KOUSEI_NP:.1f}%）")
    print(f"  🔴 ゆっくりの式 句読点なし÷380 = {mmss(yk)}（{yk / 60:.2f}分）・目標 36:00〜37:00 ＝ 句読点なし {int(BAND[0] / 60 * RATE)}〜{int(BAND[1] / 60 * RATE)}字"
          f"（{'内' if BAND[0] <= yk <= BAND[1] else '🔴 外'}）")
    print(f"  （参考・既知の誤り）門番の判定 {mmss(m['jud'])}＝ElevenLabs の定数")

    # 1 タイトル
    print("\n## 1 タイトル案")
    pub = {}
    tp = Path(__file__).resolve().parent / "titles16.json"
    if tp.exists():
        pub = json.loads(tp.read_text(encoding="utf-8"))
    L = [len(v) for v in pub.values() if not v.startswith("ERR")]
    if L:
        print(f"  公開ずみ {len(L)}本＝{min(L)}〜{max(L)}字・中央値 {statistics.median(L)}・全部「の真相【事故検証】」を含む {sum('の真相【事故検証】' in v for v in pub.values())}本")
    sec1 = T.split("### 1-1.", 1)[1].split("\n### ", 1)[0] if "### 1-1." in T else ""
    for ln in sec1.splitlines():
        mm = re.match(r"^\|\s*\**([^|*]+?)\**\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|", ln)
        if not mm or "タイトル" in mm.group(2):
            continue
        t = mm.group(2).strip()
        n = len(t)
        bad = []
        if not t.endswith("の真相【事故検証】"):
            bad.append("末尾が「の真相【事故検証】」でない")
        if not re.search(r"\d[\d,]*人が亡くなった", t):
            bad.append("「N人が亡くなった」が無い")
        if not 67 <= n <= 94:
            bad.append("67〜94字の外")
        for w in ["死亡", "決壊", "崩壊", "即死", "世界一"]:
            if w in t:
                bad.append(f"「{w}」")
        if n != int(mm.group(3)):
            bad.append(f"表の字数 {mm.group(3)} と違う")
        if t in pub.values():
            bad.append("公開ずみと同じ")
        print(f"  {mm.group(1).strip()} {n}字 {'✓' if not bad else '⚠️ ' + '・'.join(bad)}｜{t}")

    # 2 出典の札
    print("\n## 2 出典の札")
    RANGE = {"S1": (1, 248), "S8": (41, 52), "S9": (1, 19), "S10": (1, 25)}
    cnt, bad, odd, dash = collections.Counter(), [], [], []
    body4 = T.split("## 4. 台本", 1)[1].split("\n## 5.", 1)[0]
    for cid, pic, ls in cuts:
        # 🔴 行頭のカット見出しだけを読む（§2 の表にも **c104** が太字で出る）
        mh = re.search(r"^\*\*" + cid + r"\*\*[^\n]*", body4, re.M)
        src = mh.group(0).split("／")[-1].strip() if mh else ""
        if src in ("—", "-", ""):
            dash.append(cid)
            continue
        if not re.match(r"(S\d+|一般の事実|報道)", src):
            odd.append(cid)
        for doc, pg in re.findall(r"\b(S\d+)\s*(?:PDF|p\.?)\s*(\d+)", src):
            cnt[doc] += 1
            if doc in RANGE and not RANGE[doc][0] <= int(pg) <= RANGE[doc][1]:
                bad.append(f"{cid} {doc} {pg}")
    print(f"  文書ごとの札の延べ {dict(cnt)}")
    print(f"  範囲外の頁 {bad}")
    print(f"  略号で始まらない札 {odd}")
    print(f"  札が「—」のカット {len(dash)}：{' '.join(dash)}")

    # 3 ★
    print("\n## 3 ★の位置と字数")
    nq = 0
    for cid, pic, ls in cuts:
        for i, l in enumerate(ls):
            if cs.STAR_RE.match(l):
                nq += 1
                s = cs.clean(l)
                flag = []
                if len(s) > 20:
                    flag.append("🔴 20字超")
                if i != len(ls) - 1:
                    flag.append("🔴 最後の行でない")
                if kind(pic) != "決め所":
                    flag.append("⚠️ 画の欄が quote でない")
                if flag:
                    print(f"  {cid} {len(s)}字 {'・'.join(flag)}｜{s}")
    print(f"  ★ {nq}行")

    # 4 文・行
    print("\n## 4 文と行")
    ss = sentences(cuts)
    SL = [len(s) for _, s in ss]
    print(f"  文 {len(ss)}・中央値 {statistics.median(SL)}字・最長 {max(SL)}字・40字超 {sum(x > 40 for x in SL)}")
    for cid, s in ss:
        if len(s) > 40:
            print(f"    {cid} {len(s)}字｜{s}")
    ll = [(cid, len(cs.clean(l)), len(l)) for cid, l in lines]
    print(f"  1行（印を除く）中央値 {statistics.median([x for _, x, _ in ll])}字・最長 {max(x for _, x, _ in ll)}字・41字超 {[(c, x) for c, x, _ in ll if x > 41]}・40字超 {[(c, x) for c, x, _ in ll if x > 40]}")
    badn = [cid for cid, _, ls in cuts if not 1 <= len(ls) <= 3]
    print(f"  行数が1〜3の外 {badn}")
    tta = [s.endswith("った。") for _, s in ss]
    n3 = sum(1 for i in range(len(tta) - 2) if tta[i] and tta[i + 1] and tta[i + 2])
    print(f"  「った。」の3連続 {n3}か所")

    # 5 内部の数字
    print("\n## 5 内部の数字の grep（§0 を除く）")
    on, hit = True, []
    for n, ln in enumerate(T.splitlines(), 1):
        if ln.startswith("## "):
            on = not ln.startswith("## 0.")
        if on and re.search(r"維持|再生回数|再生数|視聴|クリック率|CTR|インプレ|チャンネル登録|登録者", ln):
            hit.append(f"L{n}: {ln[:80]}")
    print("  " + ("\n  ".join(hit) if hit else "0件"))

    # 6 使わない言い方（本文だけ）
    print("\n## 6 使わない言い方（本文の字幕の行だけ）")
    NG = [(r"決壊", "決壊（sources §3）＝越流の説明の否定形だけ可"), (r"崩壊", "崩壊"), (r"M字", "M字"), (r"世界一", "世界一"),
          (r"250メートル", "天端から250m"), (r"2,?500人", "犠牲者2,500人"), (r"100秒", "100秒"), (r"ポンテセイ", "ポンテセイ"),
          (r"国有化の前", "国有化の前に高く売る"), (r"腐った", "Toc＝腐った"), (r"無視", "警告を無視（断定）"),
          (r"死亡|即死|絶命|死者", "死の語（§B2-4）"), (r"〜", "波ダッシュ（4-13）"), (r"仕事帰り|事故調査ノート", "チャンネル名"),
          (r"隠蔽|悲劇|戦慄|驚愕|地獄", "煽り語")]
    for cid, l in lines:
        s = cs.clean(l)
        for rx, why in NG:
            if re.search(rx, s):
                print(f"  {cid}｜{why}｜{s}")

    # 7 聞き役
    print("\n## 7 聞き役（check_listener.judge・秒は ÷380）")
    rows, total = rows_of(cuts)
    roles = None
    rp = Path(roles_path) if roles_path else None
    if rp and rp.exists():
        roles = {}
        for ln in rp.read_text(encoding="utf-8").splitlines():
            if ln.strip() and not ln.startswith("#"):
                c, r, tx = ln.split("\t")
                roles[(c.strip(), tx.strip())] = r.strip()
    E, W, info = cl.judge(rows, total, roles)
    if info.get("q"):
        print(f"  聞き役 {info['q']}／{info['lines']}行＝{100 * info['ratio']:.1f}%・1分あたり {info['per_min']:.2f}回・最初 {info['first']:.1f}秒・"
              f"最長の空き {info['max_gap']:.0f}秒（最後→終わり {info['tail']:.0f}秒）")
        try:
            rps = rp.resolve().relative_to(ROOT).as_posix()
        except (ValueError, AttributeError):
            rps = str(rp)
        print(f"  役割 {info.get('roles', {})}（{rps if roles is not None else 'roles.tsv 無し'}）")
    for x in E:
        print("  🔴 E", x)
    for x in W:
        print("  ⚠️ W", x)
    # 空きの大きい所（上位5）
    qt = [(r[0], r[4]) for r in rows if r[2] == speaker.WHO_Q]
    gaps = sorted(((b[1] - a[1], a[0], b[0]) for a, b in zip(qt, qt[1:])), reverse=True)[:5]
    print("  空きの上位 " + " ／ ".join(f"{g:.0f}秒 {a}→{b}" for g, a, b in gaps))

    # 8 冒頭
    print("\n## 8 冒頭の秒（÷380 を1カットずつ足す）")
    t, out = 0.0, []
    for cid, _, ls in cuts[:8]:
        t += sum(np_len(cs.clean(l)) for l in ls) / RATE * 60
        out.append(f"{cid}={t:.1f}s")
    print("  " + " ".join(out))

    # 9 章ごと・3通り
    print("\n## 9 章ごと")
    chap = collections.OrderedDict()
    for cid, pic, ls in cuts:
        c = chap.setdefault(cid[:2], collections.Counter())
        c["n"] += 1; c["lines"] += len(ls); c["np"] += sum(np_len(cs.clean(l)) for l in ls)
        kd = kind(pic)
        c[kd] += 1
        c["文字だけ"] += kd in ("決め所", "パネル", "頁")
        c["★"] += any(cs.STAR_RE.match(l) for l in ls)
        c["Q"] += sum(1 for l in ls if speaker.is_q(l))
    print("  章 | カット | 行 | 句読点なし | 分 | 写真 | 頁 | 再現 | 図解 | 文字だけ | ★ | 聞き役")
    for k, c in chap.items():
        print(f"  {k} | {c['n']} | {c['lines']} | {c['np']} | {c['np'] / RATE:.2f} | {c['写真']} | {c['頁']} | {c['再現イラスト']} | {c['図解']} | {c['文字だけ']} | {c['★']} | {c['Q']}")
    S_ = lambda k: sum(c[k] for c in chap.values())  # noqa: E731
    n = len(cuts)
    print(f"  計 | {n} | {S_('lines')} | {S_('np')} | {S_('np') / RATE:.2f} | 写真 {S_('写真')}（{100 * S_('写真') / n:.1f}%）| 頁 {S_('頁')} | 再現 {S_('再現イラスト')} | 図解 {S_('図解')} | 文字だけ {S_('文字だけ')}（{100 * S_('文字だけ') / n:.1f}%）| ★ {S_('★')} | 聞き役 {S_('Q')}")
    unk = [cid for cid, pic, _ in cuts if kind(pic) == "?"]
    if unk:
        print(f"  🔴 画の欄が読めない {unk}")
    d1 = n * 2190.0 / 242
    d3 = sum(c["np"] for c in chap.values()) / RATE * 60
    print(f"  3通り：① カット×9.05秒 {mmss(d1)} ／ ② 句読点なし÷380 {mmss(yk)} ／ ③ 章ごとの合計 {mmss(d3)} ／ 開き {mmss(max(d1, yk, d3) - min(d1, yk, d3))}")

    # 10 文字だけの連続
    print("\n## 10 文字だけの連続")
    run = best = runs = 0
    span = ""
    ids = [c[0] for c in cuts]
    for i, (cid, pic, _) in enumerate(cuts):
        if kind(pic) in ("決め所", "パネル", "頁"):
            run += 1
            if run > best:
                best, span = run, ids[i - run + 1] + "〜" + cid
        else:
            runs += run >= 3; run = 0
    runs += run >= 3
    print(f"  最長 {best}（{span}）・3以上 {runs}か所")

    # 11 見る向き
    print("\n## 11 見る向き（ルール 5b-80：高さは横から・場所は上から・替わるとき合図）")
    seq = [(cid, view(pic), "合図" in pic) for cid, pic, _ in cuts if view(pic)]
    prev = {}
    nsw = nmiss = nguess = 0
    for cid, v, cue in seq:
        ch = cid[:2]
        p = prev.get(ch)
        if v.endswith("?"):
            nguess += 1
        if p and p[1].rstrip("?") != v.rstrip("?"):
            nsw += 1
            ok = cue
            nmiss += not ok
            print(f"  {p[0]}（{p[1]}）→ {cid}（{v}）{'合図あり' if ok else '⚠️ 合図なし'}")
        prev[ch] = (cid, v)
    print(f"  向きの付いた画 {len(seq)}（推し量り {nguess}）・同じ章の中の切り替え {nsw}・合図なし {nmiss}")
    return E


def selftest():
    import tempfile
    s = ("### 1-1. タイトル\n\n| | タイトル | 字数 |\n|---|---|---:|\n| **推奨A** | あ | 1 |\n\n## 4. 台本\n\n### 第1章　テスト（3カット）\n\n"
         "**c101** ／ 実写 #002 ／ S1 PDF171\n> あいう、えお。\n> Q: なに？\n\n"
         "**c102** ／ quote ／ S1 PDF171\n> そう。かきくけこ。\n> ★さしすせそ\n\n"
         "**c103** ／ 図 再現イラスト 場面5【上から】 ／ S1 PDF144\n> たちつてと。\n\n"
         "**c104** ／ 図 再現イラスト 場面5【横から】合図 ／ S1 PDF146\n> なにぬねの。\n\n## 5. おわり\n")
    p = os.path.join(tempfile.gettempdir(), "mech16_selftest.md")
    open(p, "w", encoding="utf-8").write(s)
    cuts = cs.parse(open(p, encoding="utf-8").read())
    got = sum(np_len(cs.clean(l)) for _, _, ls in cuts for l in ls)
    assert got == 29, got   # あいうえお5＋なに2＋そうかきくけこ7＋さしすせそ5＋たちつてと5＋なにぬねの5
    assert kind("実写 #002") == "写真" and kind("quote") == "決め所" and kind("図 p171（頁）") == "頁"
    assert kind("図 再現イラスト 場面1") == "再現イラスト" and kind("panel 年表") == "パネル" and kind("図 年表") == "図解"
    assert view("図 再現イラスト 場面5【上から】") == "上" and view("図 断面 ダム") == "横?" and view("実写 #083 ダムの上から見た湖") is None
    rows, total = rows_of(cuts)
    assert [r[2] for r in rows].count(speaker.WHO_Q) == 1 and rows[1][3] == "なに？"
    E, W, info = cl.judge(rows, total, {("c101", "なに？"): "質問"})
    assert not E, E
    E, W, info = cl.judge(rows, total, {})
    assert any("roles.tsv に無い" in e for e in E), E        # 陽性対照＝表に無い行は E
    print("selftest ok（句読点なし29字・画の種類6つ・向き3つ・聞き役の判定と陽性対照）")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        selftest(); sys.exit(0)
    rp = a[a.index("--roles") + 1] if "--roles" in a else None
    paths = [x for x in a if not x.startswith("--") and x != rp]
    bad = 0
    for x in paths:
        bad += len(analyze(x, rp) or [])
    sys.exit(1 if bad else 0)
