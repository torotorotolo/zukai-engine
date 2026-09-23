# -*- coding: utf-8 -*-
"""④' の機械の数え（台本 第1版・読むだけ）。
1 公開ずみの題（qa_out/ep*_meta.py の TITLE）と ④ のタイトル案の型・字数
2 出典の札（仏 pN 等）の数え：1カットしか使わない札・台本の表に無い札
3 ★の位置（最後の行か）と字数（20字以内か）
4 語の初出（ウィンザー 等）
5 章名と本文の語の重なり
"""
import re, sys, glob, ast, collections
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/Users/konar/Desktop/zukai-engine/"
T = open(R + "ref/ep13/daihon_v1.md", encoding="utf-8").read()

print("## 1 公開ずみの題")
for f in sorted(glob.glob(R + "qa_out/ep*_meta.py")):
    s = open(f, encoding="utf-8").read()
    m = re.search(r"^TITLE\s*=\s*(\(.*?\)|\".*?\")\s*$", s, re.S | re.M)
    if m:
        try:
            t = ast.literal_eval(m.group(1))
        except Exception as e:
            t = "?" + str(e)
        print(f.split("/")[-1], len(t), t)
    m = re.search(r"^TITLES\s*=\s*(\{.*?\n\})", s, re.S | re.M)
    if m:
        try:
            d = ast.literal_eval(m.group(1))
            pk = re.search(r'TITLE_PICK\s*=\s*"(\w)"', s).group(1)
            print(f.split("/")[-1], "pick", pk, len(d[pk]), d[pk])
        except Exception as e:
            print(f, "TITLES ?", e)
for lab, t in re.findall(r"> \*\*推奨A.*?\n> (.+)|> 控え(B|C).*?\n> (.+)", T) and []:
    pass
for m in re.finditer(r"^> (?:\*\*)?(推奨A|控えB|控えC).*\n> (.+)$", T, re.M):
    t = m.group(2)
    print("④案", m.group(1), len(t), "句点", t.count("。"), t)

# 本体
body = T.split("## 4. 台本", 1)[1].split("## 5.", 1)[0]
cuts = re.findall(r"^\*\*(c\d{3})\*\* ／ (.*?) ／ (.*?)\n((?:> .*\n)+)", body, re.M)
print("\n## カット数", len(cuts))

print("\n## 2 出典の札")
cnt = collections.Counter()
where = collections.defaultdict(list)
for cid, kind, src, lines in cuts:
    for doc, rng in re.findall(r"(仏|英|上院|NTSB|AD|SB|国会) (p\d+(?:〜p\d+)?)", src):
        for p in re.findall(r"p(\d+)", rng):
            cnt[(doc, int(p))] += 1
            where[(doc, int(p))].append(cid)
    # 「・p60」のような続き
    for doc, rest in re.findall(r"(仏|英|上院|NTSB|AD|SB|国会) ((?:p\d+(?:〜p\d+)?・?)+)", src):
        pass
docs = collections.Counter(d for d, p in cnt.elements())
print("文書ごとの札の延べ", dict(docs))
once = sorted([k for k, v in cnt.items() if v == 1])
print("1カットだけの頁", len(once), " ".join(f"{d}p{p}({where[(d,p)][0]})" for d, p in once))
rng = {"仏": (1, 158), "英": (1001, 1055), "上院": (2001, 2062), "NTSB": (3001, 3045), "AD": (4001, 4308), "SB": (5001, 5111), "国会": (6001, 6351)}
bad = [(d, p, where[(d, p)]) for (d, p) in cnt if not (rng[d][0] <= p <= rng[d][1])]
print("範囲外の札", bad)
# 出典欄の頁の後ろに付いた「・p60」形式の拾い漏れ確認
for cid, kind, src, lines in cuts:
    raw = re.findall(r"p\d+", src)
    got = sum(1 for (d, p) in cnt for c in where[(d, p)] if c == cid)
    if len(raw) != len(set(raw)) and False:
        pass
nosrc = [cid for cid, kind, src, lines in cuts if src.strip() in ("—", "-")]
print("出典なし（—）", len(nosrc), nosrc)

print("\n## 3 ★の位置と字数")
for cid, kind, src, lines in cuts:
    ls = [l[2:] for l in lines.strip("\n").split("\n")]
    stars = [i for i, l in enumerate(ls) if l.startswith("★")]
    if "quote" in kind or stars:
        s = ls[stars[0]][1:] if stars else ""
        flag = []
        if not stars: flag.append("★なし")
        elif stars[0] != len(ls) - 1: flag.append("★が最後の行でない")
        if len(s) > 20: flag.append(f"{len(s)}字>20")
        print(cid, len(s), s, " ".join(flag))

print("\n## 4 語の初出")
for w in ["ウィンザー", "N103AA", "SB", "AD", "FAA", "NTSB", "与圧", "減圧", "通気扉", "ロックピン", "フック", "のぞき窓", "航空機関士", "紳士協定", "52-37", "29号機", "TC-JAV", "世界時", "登録記号", "ロッキード", "全日空", "三井物産", "レーカー", "支えの板", "表示板", "昇降舵", "西部地域局", "副長官", "公聴会", "立会人", "オルリー", "DC-10", "サン・パテュス", "エルムノンヴィル", "付属書", "官報"]:
    hits = [cid for cid, kind, src, lines in cuts if w in lines]
    print(f"{w}: 初出 {hits[0] if hits else '-'}  延べ {len(hits)}")

print("\n## 行数ごとのカット")
c = collections.Counter(len(lines.strip().split("\n")) for _, _, _, lines in cuts)
print(dict(c))
long_lines = [(cid, l) for cid, _, _, lines in cuts for l in lines.strip().split("\n") if len(l) - 2 > 38]
print("38字を超える行", len(long_lines))
for cid, l in long_lines:
    print(" ", cid, len(l) - 2, l[2:])

print("\n## 型の連続（panel が4つ以上続く所）")
run = []
for cid, kind, src, lines in cuts:
    k = kind.split()[0]
    run.append((cid, k))
i = 0
while i < len(run):
    j = i
    while j < len(run) and run[j][1] == run[i][1]:
        j += 1
    if j - i >= 4:
        print(run[i][1], run[i][0], "〜", run[j - 1][0], j - i)
    i = j
