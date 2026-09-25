# -*- coding: utf-8 -*-
"""14本目④'：台本の機械の数え（読むだけ）。第1版にも第2版にも当てる。
    python ref/ep14/v2_build/mech.py ref/ep14/daihon_v1.md [titles.json]
1 タイトル案の字数・句点（公開ずみの題は titles.json＝oEmbed で取った今の題）
2 出典の札の数え（1カットだけの頁・範囲外の頁）
3 ★の位置（最後の行か）と字数（20字以内か）
4 文の長さ（句点で割る・40字超）と語尾の連続（「った。」3連続・同じ語尾3字の3連続）
5 内部の数字の grep（% 維持 再生 チャンネル 登録 視聴）＝ルール 4'-17
6 語りの中の問いかけ（？・のか。・だろうか）＝聞き役へ移す候補
7 聞き役（行頭 `Q: `）の数・割合・1分あたり・最長の空き・数字を言う行
   秒は check_script.py の③と同じ式（字数÷話速＋行間 GAP＋カット頭尻＋決め所の余白＋章の扉）。
   ⚠️ `Q: ` の3字は数えない（音にしない印）。⚠️ ca〜cd の扉も数える（check_script は数えない）
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


def bare(l):
    """音と字幕になる文（★と ** と聞き役の印を外す）"""
    return Q_RE.sub("", CS.clean(l))


# ── 1 タイトル ───────────────────────────────
print("## 1 タイトル案")
for m in re.finditer(r"^> (?:\*\*)?(推奨A|控えB|控えC)[^\n]*\n> (.+)$", T, re.M):
    t = m.group(2).strip()
    print(f"  {m.group(1)} {len(t)}字 句点{t.count('。')} 【映像あり】{'有' if '映像あり' in t else '無'} | {t}")
if len(sys.argv) > 2:
    pub = json.load(open(sys.argv[2], encoding="utf-8"))
    print("  公開ずみ（oEmbed の今の題）")
    for vid, t in pub.items():
        print(f"   {vid} {len(t)}字 句点{t.count('。')} 読点{t.count('、')} 末尾【事故検証】{'○' if t.endswith('【事故検証】') else '×'} 先頭【映像あり】{'○' if t.startswith('【映像あり】') else '-'} | {t}")

# ── 2 出典の札 ───────────────────────────────
print("\n## 2 出典の札")
body = T.split("## 4. 台本", 1)[1].split("\n## 5.", 1)[0]
heads = re.findall(r"^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／\s*([^／\n]*)／\s*(.*)$", body, re.M)
DOC = ["艇長の大法院", "艇長の判決", "幹部の判決", "会社の判決", "船員2審", "船員1審", "特調委", "判決", "海審", "裁決"]
RANGE = {"判決": (1, 81), "海審": (1001, 1138), "裁決": (2001, 2174), "特調委": (3001, 4486),
         "艇長の大法院": (5001, 5001), "艇長の判決": (5002, 5002), "幹部の判決": (5003, 5004),
         "会社の判決": (5005, 5005), "船員1審": (5006, 5006), "船員2審": (5007, 5007)}
cnt = collections.Counter(); where = collections.defaultdict(list); odd = []
for cid, pic, src in heads:
    s = src.strip()
    for seg in re.split(r"・(?=[^\dp〜])", s):
        seg = seg.strip()
        doc = next((d for d in DOC if seg.startswith(d)), None)
        if doc is None:
            if seg not in ("—", "-", ""):
                odd.append((cid, seg))
            continue
        for a, b in re.findall(r"p(\d+)(?:〜p?(\d+))?", seg):
            for p in ([int(a)] if not b else range(int(a), int(b) + 1)):
                cnt[(doc, p)] += 1; where[(doc, p)].append(cid)
    # 「・p60」の続き（文書名なしの頁）は直前の文書に付く＝上の split で拾えないので数える
    for doc, rest in re.findall(r"(" + "|".join(DOC) + r") p\d+(?:〜p?\d+)?((?:・p\d+(?:〜p?\d+)?)+)", s):
        for a, b in re.findall(r"p(\d+)(?:〜p?(\d+))?", rest):
            for p in ([int(a)] if not b else range(int(a), int(b) + 1)):
                cnt[(doc, p)] += 1; where[(doc, p)].append(cid)
print("  文書ごとの札の延べ", dict(collections.Counter(d for d, p in cnt.elements())))
bad = [(d, p, where[(d, p)]) for (d, p) in cnt if not (RANGE[d][0] <= p <= RANGE[d][1])]
print("  範囲外の頁", bad)
once = sorted(k for k, v in cnt.items() if v == 1)
print("  1カットだけの頁", len(once), " ".join(f"{d}p{p}({where[(d, p)][0]})" for d, p in once))
print("  文書名で始まらない札", odd[:30])

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
# 同じ語尾（最後の3字）の3連続（「った。」は上で見た）
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
print("\n## 5 内部の数字の grep（§0 を除くファイル全体＝§0 は門番の出力を差すので自分を拾わない。位置は節の名で出す）")
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
    if who == "N" and re.search(r"[？?]|のか。|だろうか|なぜ|どうして|どれほど|どこで|何が", s):
        print(f"  {cid}-{i} {s}")

# ── 7 聞き役 ─────────────────────────────────
print("\n## 7 聞き役（行頭 `Q: `）")
CPS = CS.CPS_FALLBACK
t = 0.0; qtimes = []; qlines = []; total_lines = 0; qchars = 0; allchars = 0
prev_ch = None
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
print(f"  尺（この式・印を除く・扉{len({c[:2] for c, _, _ in cuts}) - 1}枚）{int(t)//60}分{int(t)%60:02d}秒 ／ 本文 {allchars}字（印を除く）")
if qtimes:
    gaps = [qtimes[0]] + [b - a for a, b in zip(qtimes, qtimes[1:])] + [t - qtimes[-1]]
    inner = [b - a for a, b in zip(qtimes, qtimes[1:])]
    mx = max(range(len(gaps)), key=lambda k: gaps[k])
    print(f"  聞き役の行 {len(qlines)}／{total_lines}＝{100 * len(qlines) / total_lines:.1f}%（字 {qchars}＝{100 * qchars / allchars:.1f}%）"
          f"・1分あたり {len(qlines) / (t / 60):.2f}回")
    print(f"  最初の1回 {qtimes[0]:.1f}秒 ・ 間の中央値 {sorted(inner)[len(inner)//2] if inner else 0:.0f}秒 ・ 最長の空き {max(inner) if inner else 0:.0f}秒"
          f"（最後の聞き役→終わり {gaps[-1]:.0f}秒）")
    over = [(qlines[k][0], qlines[k + 1][0], round(inner[k])) for k in range(len(inner)) if inner[k] > 90]
    print(f"  90秒を超える空き {len(over)} {over}")
    print(f"  数字を含む聞き役の行 {[c for c, b in qlines if re.search(r'[0-9０-９一二三四五六七八九十百千万]', b)]}")
    # 役割＝roles.tsv（cid<TAB>役割<TAB>聞き役の文）。1行ずつ台本と突き合わせる（表に無い・台本に無いを出す）
    rp = Path(__file__).resolve().parent / "roles.tsv"
    role = {}
    if rp.exists():
        for ln in rp.read_text(encoding="utf-8").splitlines():
            if ln.strip() and not ln.startswith("#"):
                c, r, tx = ln.split("\t")
                role[(c, tx.strip())] = r
    got = collections.Counter(role.get((c, b), "表に無い") for c, b in qlines)
    print(f"  役割 {dict(got)}（質問 {100 * got['質問'] / len(qlines):.0f}%・まとめ {100 * got['まとめ'] / len(qlines):.0f}%・反応 {100 * got['反応'] / len(qlines):.0f}%）")
    miss = [k for k in role if k not in set(qlines)]
    if miss:
        print(f"  ⚠️ roles.tsv にあって台本に無い {miss}")
    for cid, b in qlines:
        print(f"   Q {cid} [{role.get((cid, b), '?')}] {b}")
else:
    print("  聞き役の行 0")
