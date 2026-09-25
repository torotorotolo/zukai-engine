# -*- coding: utf-8 -*-
"""15本目④：台本の機械の数え（読むだけ）。14本目④'の ref/ep14/v2_build/mech.py を15本目用に写して足した。
    python ref/ep15/v1_build/mech15.py ref/ep15/daihon_v1.md [titles.json]
1 タイトル案の字数・句点（公開ずみの題は titles.json＝oEmbed で取った今の題）
2 出典の札の数え（文書ごと・範囲外の頁・文書名で始まらない札）
3 ★の位置（最後の行か）と字数（20字以内か）
4 文の長さ（句点で割る・40字超）と語尾の連続（「った。」3連続・同じ語尾3字の3連続）
5 内部の数字の grep（% 維持 再生 チャンネル 登録 視聴）＝ルール 4'-17
6 語りの中の問いかけ（？・のか。・だろうか）＝聞き役へ移す候補
7 聞き役（行頭 `Q: `）の数・割合・1分あたり・最長の空き・数字を言う行・キャラ語尾・役割
8 🆕 冒頭の秒（行間と決め所の余白まで数えた式＝7 と同じ式。check_script の `冒頭:` は行間と余白を数えない）
9 🆕 章ごとの配分（カット・行・字・写真映像・決め所・聞き役）＝台本 §3 の表
10 🆕 行の長さ（1行41字の上限に近い行）
   秒は check_script.py の③と同じ式（字数÷話速＋行間 GAP＋カット頭尻＋決め所の余白＋章の扉）。⚠️ `Q: ` の3字は数えない
"""
import re, sys, json, collections
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(ROOT / "tools"))
import check_script as CS

MD = Path(sys.argv[1])
T = MD.read_text(encoding="utf-8")
Q_RE = re.compile(r"^Q:\s")          # 聞き役の印（`> Q: ` の `> ` を外したあと）
cuts = CS.parse(T)                    # [(cid, 画, [行…])]
CPS = CS.CPS_FALLBACK


def bare(l):
    """音と字幕になる文（★と ** と聞き役の印を外す）"""
    return Q_RE.sub("", CS.clean(l))


# ── 1 タイトル ───────────────────────────────
print("## 1 タイトル案")
for m in re.finditer(r"^> (?:\*\*)?(推奨A|控えB|控えC)[^\n]*\n> (.+)$", T, re.M):
    t = m.group(2).strip()
    print(f"  {m.group(1)} {len(t)}字 句点{t.count('。')} 末尾【事故検証】{'○' if t.endswith('【事故検証】') else '×'} 【映像あり】{'有' if '映像あり' in t else '無'} 死の語{'有' if re.search('死|亡くな(?!った)', t) else '無'} | {t}")
if len(sys.argv) > 2:
    pub = json.load(open(sys.argv[2], encoding="utf-8"))
    L = [len(t) for t in pub.values()]
    print(f"  公開ずみ {len(pub)}本＝{min(L)}〜{max(L)}字・末尾【事故検証】{sum(t.endswith('【事故検証】') for t in pub.values())}本・「亡くなった」{sum('亡くなった' in t for t in pub.values())}本")

# ── 2 出典の札 ───────────────────────────────
print("\n## 2 出典の札")
body = T.split("## 4. 台本", 1)[1].split("\n## 5.", 1)[0]
heads = re.findall(r"^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／\s*([^／\n]*)／\s*(.*)$", body, re.M)
DOC = ["AAB", "#40", "#33", "#14", "#53", "#17", "CAROL", "勧告書", "報道", "RARA", "Commons"]
RANGE = {"AAB": (1, 52), "#40": (1, 61), "#33": (1, 22), "#14": (1, 40), "#53": (1, 60), "#17": (1, 29)}
cnt = collections.Counter(); odd = []; bad = []
for cid, pic, src in heads:
    s = src.strip()
    doc = None
    for seg in [x.strip() for x in s.split("・")]:
        if seg in ("—", "-", ""):
            continue
        d = next((x for x in DOC if seg.startswith(x)), None)
        if d:
            doc = d
        elif re.match(r"^p\d+", seg) or seg.startswith("A-12") or seg.startswith("注"):
            pass                      # 直前の文書の続き
        else:
            odd.append((cid, seg)); continue
        cnt[doc] += 1
        for a in re.findall(r"p(\d+)", seg):
            if doc in RANGE and not (RANGE[doc][0] <= int(a) <= RANGE[doc][1]):
                bad.append((cid, doc, a))
print("  文書ごとの札の延べ", dict(cnt))
print("  範囲外の頁", bad)
print("  文書名で始まらない札", odd)

# ── 3 ★ ────────────────────────────────────
print("\n## 3 ★の位置と字数")
for cid, pic, ls in cuts:
    st = [i for i, l in enumerate(ls) if l.startswith("★")]
    if "quote" in pic or st:
        s = CS.clean(ls[st[0]]) if st else ""
        flag = ([] if st else ["★なし"]) + (["★が最後の行でない"] if st and st[0] != len(ls) - 1 else []) \
            + ([f"{len(s)}字>20"] if len(s) > 20 else [])
        print(f"  {cid} {len(s)}字 {s} {' '.join(flag)}")

# ── 4 文の長さと語尾 ─────────────────────────
print("\n## 4 文（カットの中で行をつなぎ、句点・？・！で割る。★の行と話者の替わり目も文の切れ目）")
sents = []                          # (cid, 行番号, 話者, 文)＝行番号は文の終わる行
for cid, pic, ls in cuts:
    buf, who0 = "", None
    for i, l in enumerate(ls, 1):
        who = "Q" if Q_RE.match(CS.clean(l)) else "N"
        if buf and who != who0:
            sents.append((cid, i - 1, who0, buf)); buf = ""
        who0 = who
        b = bare(l)
        for p in re.findall(r"[^。？！]+[。？！]?", b):
            buf += p
            if re.search(r"[。？！]$", p):
                sents.append((cid, i, who, buf.strip())); buf = ""
        if CS.STAR_RE.match(l) and buf:
            sents.append((cid, i, who, buf.strip())); buf = ""
    if buf.strip():
        sents.append((cid, len(ls), who0, buf.strip()))
L = [len(s) for *_, s in sents]
print(f"  文 {len(sents)}・中央値 {sorted(L)[len(L)//2]}字・最長 {max(L)}字・40字超 {sum(x > 40 for x in L)}")
for cid, i, who, s in sents:
    if len(s) > 40:
        print(f"   >40 {cid}-{i} {len(s)}字 {s}")
end_tta = [s.endswith("った。") for *_, s in sents]
print(f"  「った。」で終わる文 {sum(end_tta)}")
runs = []; k = 0
while k < len(sents):
    j = k
    while j < len(sents) and end_tta[j]:
        j += 1
    if j - k >= 3:
        runs.append((k, j))
    k = j + 1 if j == k else j
for a, b in runs:
    print(f"   った。×{b - a} " + " ／ ".join(f"{sents[x][0]}-{sents[x][1]}「…{sents[x][3][-10:]}」" for x in range(a, b)))
k = 0; n3 = 0
while k < len(sents):
    e = sents[k][3][-3:]; j = k
    while j < len(sents) and sents[j][3][-3:] == e:
        j += 1
    if j - k >= 3 and e != "った。":
        n3 += 1
        print(f"   同じ語尾「{e}」×{j - k} " + " ／ ".join(f"{sents[x][0]}-{sents[x][1]}" for x in range(k, j)))
    k = j if j > k else k + 1
print(f"  同じ語尾3字の3連続（った。以外） {n3}")

# ── 5 内部の数字 ─────────────────────────────
print("\n## 5 内部の数字の grep（§0 を除くファイル全体）")
sect = "頭"
for line in T.split("\n"):
    if line.startswith("## "):
        sect = line[3:20]
    if sect.startswith("0."):
        continue
    if re.search(r"%|％|維持|再生|チャンネル|登録者|視聴|離脱|CTR|インプレ", line):
        print(f"  [{sect}] {line[:150]}")

# ── 6 語りの中の問いかけ ──────────────────────
print("\n## 6 語りの中の問いかけ（聞き役へ移す候補）")
for cid, i, who, s in sents:
    if who == "N" and re.search(r"[？?]|のか。|だろうか|どうして|どれほど|どこで", s):
        print(f"  {cid}-{i} {s}")

# ── 7 聞き役 ─────────────────────────────────
print("\n## 7 聞き役（行頭 `Q: `）")
t = 0.0; qtimes = []; qlines = []; total_lines = 0; qchars = 0; allchars = 0
prev_ch = None; cut_end = {}
for cid, pic, ls in cuts:
    ch = cid[:2]
    if prev_ch is not None and ch != prev_ch:
        t += CS.CARD_SEC
    prev_ch = ch
    t += CS.LEAD
    for i, l in enumerate(ls):
        b = bare(l); allchars += len(b); total_lines += 1
        if i:
            t += CS.GAP
        if Q_RE.match(CS.clean(l)):
            qtimes.append(t); qlines.append((cid, b)); qchars += len(b)
        t += len(b) / CPS
    t += CS.TAIL + (CS.TAIL_EXTRA_QUOTE if any(CS.STAR_RE.match(l) for l in ls) else 0)
    cut_end[cid] = t
print(f"  尺（この式・印を除く・扉{len({c[:2] for c, _, _ in cuts}) - 1}枚）{int(t)//60}分{int(t)%60:02d}秒（{t:.1f}秒） ／ 本文 {allchars}字（印を除く） ／ 行 {total_lines}")
if qtimes:
    gaps = [qtimes[0]] + [b - a for a, b in zip(qtimes, qtimes[1:])] + [t - qtimes[-1]]
    inner = [b - a for a, b in zip(qtimes, qtimes[1:])]
    print(f"  聞き役の行 {len(qlines)}／{total_lines}＝{100 * len(qlines) / total_lines:.1f}%（字 {qchars}＝{100 * qchars / allchars:.1f}%）"
          f"・1分あたり {len(qlines) / (t / 60):.2f}回")
    print(f"  最初の1回 {qtimes[0]:.1f}秒 ・ 間の中央値 {sorted(inner)[len(inner)//2] if inner else 0:.0f}秒 ・ 最長の空き {max(inner) if inner else 0:.0f}秒"
          f"（最後の聞き役→終わり {gaps[-1]:.0f}秒）")
    over = [(qlines[k][0], qlines[k + 1][0], round(inner[k])) for k in range(len(inner)) if inner[k] > 90]
    print(f"  90秒を超える空き {len(over)} {over}")
    top = sorted(((round(inner[k]), qlines[k][0], qlines[k + 1][0]) for k in range(len(inner))), reverse=True)[:5]
    print(f"  長い空きの上位5 {top}")
    print(f"  数字を含む聞き役の行 {[c for c, b in qlines if re.search(r'[0-9０-９一二三四五六七八九十百千万]', b)]}")
    print(f"  キャラ語尾（ぜ・わ・かしら）の聞き役の行 {[c for c, b in qlines if re.search(r'(ぜ|わ|かしら)[。！？…]*$', b)]}")
    rp = Path(__file__).resolve().parent / "roles.tsv"
    role = {}
    if rp.exists():
        for ln in rp.read_text(encoding="utf-8").splitlines():
            if ln.strip() and not ln.startswith("#"):
                c, r, tx = ln.split("\t")
                role[(c, tx.strip())] = r
    got = collections.Counter(role.get((c, b), "表に無い") for c, b in qlines)
    n = len(qlines)
    print(f"  役割 {dict(got)}（質問 {100 * got['質問'] / n:.0f}%・まとめ {100 * got['まとめ'] / n:.0f}%・反応 {100 * got['反応'] / n:.0f}%）")
    miss = [k for k in role if k not in set(qlines)]
    if miss:
        print(f"  ⚠️ roles.tsv にあって台本に無い {miss}")
    # まとめの次の語りは「そう。」で受ける（ルール 4-15）
    flat = [(cid, CS.clean(l)) for cid, _, ls in cuts for l in ls]
    for k2, (cid, l) in enumerate(flat):
        if Q_RE.match(l) and role.get((cid, Q_RE.sub("", l)), "") == "まとめ":
            nxt = flat[k2 + 1][1] if k2 + 1 < len(flat) else ""
            if not nxt.startswith("そう。"):
                print(f"  ⚠️ まとめの次が「そう。」で始まらない: {cid} {l} → {nxt[:20]}")
    for cid, b in qlines:
        print(f"   Q {cid} [{role.get((cid, b), '?')}] {b}")
else:
    print("  聞き役の行 0")

# ── 8 冒頭の秒 ───────────────────────────────
print("\n## 8 冒頭の秒（7 と同じ式＝行間と決め所の余白を数える）")
print("  " + " ".join(f"{c}={cut_end[c]:.1f}s" for c, _, _ in cuts[:7]))

# ── 9 章ごとの配分 ───────────────────────────
print("\n## 9 章ごと（カット／行／字（印を除く）／写真映像／決め所／聞き役）")
agg = collections.OrderedDict()
for cid, pic, ls in cuts:
    k = cid[:2]
    a = agg.setdefault(k, [0, 0, 0, 0, 0, 0])
    a[0] += 1; a[1] += len(ls); a[2] += sum(len(bare(l)) for l in ls)
    a[3] += CS.pic_kind(pic) in ("A", "B")
    a[4] += any(CS.STAR_RE.match(l) for l in ls)
    a[5] += sum(1 for l in ls if Q_RE.match(CS.clean(l)))
tot = [sum(v[i] for v in agg.values()) for i in range(6)]
for k, v in agg.items():
    print(f"  {k} {v[0]:3d} {v[1]:3d} {v[2]:5d} {v[3]:3d}（{100 * v[3] / v[0]:.0f}%） {v[4]} {v[5]}")
print(f"  計 {tot[0]} {tot[1]} {tot[2]} {tot[3]}（{100 * tot[3] / tot[0]:.1f}%） {tot[4]} {tot[5]}")

# ── 10 行の長さ ──────────────────────────────
print("\n## 10 行の長さ（生の字数＝check_script と同じく印も数える）")
raw = [(cid, CS.clean(l)) for cid, _, ls in cuts for l in ls]
print(f"  最長 {max(len(l) for _, l in raw)}字 ・ 39字以上 {[(c, len(l)) for c, l in raw if len(l) >= 39]}")
