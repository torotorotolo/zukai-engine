# -*- coding: utf-8 -*-
"""make_plan.py — 15本目の章ファイル（tools/cuts/c1〜c9）の**骨組み PLAN** を作る（2026-09-30 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（14本目の `ref/ep14/make_plan.py` と同じ作り）。
  ① 台本 `ref/ep15/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典`（192カット）
  ② 承認ずみの映像方針 Vault `Projects/事故検証-15本目-映像方針-絵コンテ-20260926.md`（09-26 カズヤくん承認）
     §3-1・§3-2（案C の画と動き・人・出典）／§4（動く模式図と地図）／§5（替える画）／§11-2（案B＝パネルを替える42カット）
画面の種類（kind）は Vault `Resources/事故検証ch-案C見本/count_text_screens.py` の preset `ep15B`（案B で承認＝59/192・最長5）と
**同じ関数**で決める（書く前にここで照合する＝違えば止まる）。

    python ref/ep15/make_plan.py          # 照合して数を出すだけ（書かない）
    python ref/ep15/make_plan.py --write  # 章ファイル 9本を書く（🔴 15本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 承認ずみの文書の範囲の書き方はゆるい（§4 の「`c607`〜`c609`」に文字の頁 c608 が入る）＝§4 の予定は種類が図解のカットにだけ付ける。
"""
import importlib.util
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
SCRIPT = HERE / "ref" / "ep15" / "daihon_v2.md"
VAULT = Path(r"C:\Users\konar\Documents\Obsidian Vault")
POLICY = VAULT / "Projects" / "事故検証-15本目-映像方針-絵コンテ-20260926.md"
COUNTER = VAULT / "Resources" / "事故検証ch-案C見本" / "count_text_screens.py"
CUTS = HERE / "tools" / "cuts"
PRESET = "ep15B"
WANT = (59, 5, 4)          # 文字だけ・続く最長・3カット以上続く所（映像方針 §11-1 の案B＝09-26 承認）
N_CUTS = 192

KINDS = ("写真", "図・写真の頁", "再現イラスト", "図解", "混ざり", "文字の頁", "パネル", "決め所")
TEXT = ("パネル", "決め所", "文字の頁")
CHAPTER_OF = {f"c{i}": i for i in range(1, 10)}

# §4 の種類の名 → 記号（plan の頭）
TAG4 = (("尾翼", "【尾翼】"), ("ねじ", "【ねじ】"), ("改造", "【改造】"), ("時間の帯", "【帯】"), ("地図", "【地図】"))
# §11-2 の型の名 → 記号
TAG11 = (("年表", "【年表】"), ("数の比べ", "【棒】"), ("書類", "【書類】"), ("時間の帯", "【帯】"),
         ("承認ずみの図", "【使い回し】"), ("絵（案C）を戻す", "【案C 戻り】"))
# 1つの画面の中で種類が入れ替わるカット（§3・§5 の文を読んだ）
MIXED = {
    "c104": "【混ざり：案C B → 決め所】",
    "c904": "【混ざり：頁 p46 → 地図 drift】",
    "c302": "【案C D → 尾翼の模式図】",
    "c312": "【案C A → 時間の帯】",
    "c109": "【案C を小さく戻す（3つの問い）】",
}
# 映像方針のカットごとの注意（§1 の線・§3・§11-2・④' の申し送り）。plan の末尾に「⚠️」で足す
COURTESY = "⚠️ 報告書の courtesy の写真＝紙面の引用のまま（頁ごと・額装・無加工）。描いた物を重ねない・なぞらない・絵と同じ画面に並べない（映像方針 §1 線3）"
NOTES = {c: COURTESY for c in "c103 c301 c306 c309 c310 c311 c520 c521".split()}
NOTES.update({
    "c313": "⚠️ 絵にしない＝崩れた姿勢（苦しむ瞬間）は描かない（映像方針 §1 線2）",
    "c316": "⚠️ 絵にしない＝観客の「避けようとしたように見えた」は支えられない・私人の言葉は絵に出さない（映像方針 §1 線2）",
    "c802": "⚠️ A の×を動かさずに出すだけ（人数を絵で名乗らない・数は字幕だけ）（映像方針 §11-2）",
    "c107": "⚠️ パイロットの実名（09-26 承認）＝人の形は描かない（D の機体に名前と歳の札だけ）（映像方針 §11-2・§1 線2）",
    "c408": "⚠️ パイロットの実名（09-26 承認）＝人の形は描かない（映像方針 §1 線2）",
    "c105": "⚠️ AAB 図14 を c105 と c708 で2回使う（④' の申し送り）",
    "c708": "⚠️ AAB 図14 を c105 と c708 で2回使う（④' の申し送り）",
    "c710": "⚠️ ドケット #40 図7（黄色の塗装）は ④' も未見＝原寸で見てから。色が証拠＝章の色に置き換えない（color=1.0）",
})
for _c in "c318 c319 c320 c321 c322 c323".split():
    NOTES.setdefault(_c, "⚠️ 横転のきっかけ（後方乱気流／リンクが先に折れた）は未確定＝場面にしない（映像方針 §1 線3）")


def load_counter():
    spec = importlib.util.spec_from_file_location("count_text_screens", COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def section(path, start_pat, stop_pat):
    lines = path.read_text(encoding="utf-8").split("\n")
    s = next(i for i, ln in enumerate(lines) if re.match(start_pat, ln))
    e = next((i for i in range(s + 1, len(lines)) if re.match(stop_pat, lines[i])), len(lines))
    return lines[s:e]


def table(lines):
    """表の行（`|` で割った列）。見出しの区切り行は外す。"""
    out = []
    for ln in lines:
        if not ln.startswith("|") or set(ln.replace("|", "").strip()) <= set("-: "):
            continue
        out.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return out


def first_cut(col):
    m = re.match(r"`?(c\d{3})`?", col)
    return m.group(1) if m else None


def cuts_in(col):
    return re.findall(r"c\d{3}", col)


def clean(s):
    return re.sub(r"\s+", " ", s.replace("**", "").replace("`", "")).strip()


def tag_of(name, tags):
    return next((t for k, t in tags if k in name), "")


def build():
    ct = load_counter()
    cuts = ct.parse(str(SCRIPT))
    if len(cuts) != N_CUTS:
        raise SystemExit(f"🔴 台本のカットが {len(cuts)}（{N_CUTS} のはず）")
    # 画と出典は「 ／ 」（前後に空白）で割る（画の中に空白の無い「／」がある）
    src, pic = {}, {}
    for ln in SCRIPT.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^\*\*(c\d{3})\*\*", ln)
        if m:
            parts = ln.split(" ／ ")
            pic[m.group(1)], src[m.group(1)] = clean(parts[1]), clean(" ／ ".join(parts[2:]))
    if set(pic) != set(cuts):
        raise SystemExit(f"🔴 見出し行の読み方が2つで食い違う: {sorted(set(pic) ^ set(cuts))}")
    over, tp = ct.PRESETS[PRESET]
    kind = {k: over.get(k, ct.base(k, c["pic"], tp)) for k, c in cuts.items()}
    bad = {k: v for k, v in kind.items() if v not in KINDS}
    if bad:
        raise SystemExit(f"🔴 種類が決まらないカット: {bad}")

    plan = {k: "台本の画：" + pic[k] for k in cuts}
    used = Counter()
    # §4 動く模式図と地図（種類｜中身｜カット）＝種類が図解のカットにだけ（範囲の書き方がゆるい）
    for cols in table(section(POLICY, r"^## 4\.", r"^## 5\.")):
        tag = tag_of(cols[0], TAG4)
        if not tag:
            continue
        for k in cuts_in(cols[2]):
            if kind.get(k) == "図解":
                plan[k] = f"{tag}{clean(cols[0])}：{clean(cols[1])}（映像方針 §4）｜台本の画：{pic[k]}"
                used["§4"] += 1
    # §5 替える画（カット｜いま｜替えたあと｜実写の数）
    for cols in table(section(POLICY, r"^## 5\.", r"^## 6\.")):
        k = first_cut(cols[0])
        if k:
            plan[k] = f"{clean(cols[2])}（映像方針 §5＝いまの画：{clean(cols[1])}）"
            used["§5"] += 1
    # §3-1 冒頭（カット（秒）｜台本｜いまの画｜案C の画と動き｜人｜出典）
    for cols in table(section(POLICY, r"^### 3-1\.", r"^### 3-2\.")):
        k = first_cut(cols[0])
        if not k:
            continue
        body = clean(cols[3])
        if body.startswith("そのまま"):
            plan[k] = f"台本の画：{pic[k]}（映像方針 §3-1：{body}）"
        else:
            plan[k] = f"【案C】{body}｜人：{clean(cols[4])}｜rec：{clean(cols[5])}（映像方針 §3-1）"
        used["§3-1"] += 1
    # §3-2 要所（カット｜台本の要点｜いまの画｜案C の画と動き｜人｜⚠️）
    for cols in table(section(POLICY, r"^### 3-2\.", r"^## 4\.")):
        k = first_cut(cols[0])
        if not k:
            continue
        head = "【案C】" if kind[k] in ("再現イラスト", "混ざり") else ""
        warn = clean(cols[5]) if len(cols) > 5 else ""
        plan[k] = (f"{head}{clean(cols[3])}｜人：{clean(cols[4])}（映像方針 §3-2）"
                   + (f"｜⚠️ {warn}" if warn not in ("", "—") else ""))
        used["§3-2"] += 1
    # §11-2 案B（型｜何を見せるか｜カット）＝最も新しい決め（09-26）＝勝つ
    for cols in table(section(POLICY, r"^### 11-2\.", r"^### 11-3\.")):
        tag = tag_of(clean(cols[0]), TAG11)
        if not tag:
            continue
        for k in cuts_in(cols[2]):
            plan[k] = f"{tag}{clean(cols[0])}：{clean(cols[1])}（映像方針 §11-2＝案B）｜台本の画：{pic[k]}"
            used["§11-2"] += 1
    for k, head in MIXED.items():
        plan[k] = head + plan[k]
    for k, v in NOTES.items():
        plan[k] += "｜" + v
    unknown = sorted(set(plan) - set(cuts))
    if unknown:
        raise SystemExit(f"🔴 台本に無いカット: {unknown}")
    # 案C（再現イラスト・混ざり）なのに映像方針の行が1つも当たっていないカットは止める（写し漏れ）
    lost = sorted(k for k in cuts if kind[k] in ("再現イラスト", "混ざり") and plan[k].startswith("台本の画："))
    if lost:
        raise SystemExit(f"🔴 案C の種類なのに映像方針の予定が無い: {lost}")
    return cuts, kind, plan, src, used


def count(ids, kind):
    """数え直しの道具と同じ数え方（文字だけの数・続く最長・3カット以上続く所）。"""
    tc = sum(kind[k] in TEXT for k in ids)
    run = best = runs = 0
    for k in ids:
        if kind[k] in TEXT:
            run += 1
            best = max(best, run)
        else:
            runs += run >= 3
            run = 0
    runs += run >= 3
    return tc, best, runs


def chapter_file(ch, ids, kind, plan, src, name, n):
    rows = "\n".join(f'    "{k}": dict(kind={kind[k]!r},\n'
                     f'               plan={plan[k]!r},\n'
                     f'               src={src.get(k, "")!r}),' for k in ids)
    return f'''# -*- coding: utf-8 -*-
"""第{n}章　{name} {ids[0]}–{ids[-1]}（{len(ids)}カット）。15本目（リノ・エアレース2011）。

■ 🔴 2026-09-30（⑤b-1）：14本目（セウォル号）の中身を空にした＝git の `dc6ecf4`（`git show dc6ecf4:tools/cuts/{ch}.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep15/make_plan.py` で
  台本 §4・承認ずみの映像方針（§3 案C・§4 動く模式図と地図・§5 替える画・§11-2 案B）から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所（ルール §5b-79）
  記号＝【案C】再現イラスト（置き場 A 上から見た空港・B 空の中の事故機・C ボックス席とピット・D ピットの事故機）・
        【尾翼】【ねじ】【改造】【帯】【地図】（映像方針 §4）・【年表】【棒】【書類】【帯】【使い回し】【案C 戻り】（§11-2＝案B）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {{
{rows}
}}

SPEC = {{
}}
'''


def main(write=False):
    cuts, kind, plan, src, used = build()
    ids = list(cuts)
    tc, best, runs = count(ids, kind)
    ct = load_counter()
    ratio, best_ct = ct.report(cuts, ct.PRESETS[PRESET][0], ct.PRESETS[PRESET][1], f"照合：count_text_screens {PRESET}")
    print(f"■ PLAN：{len(ids)}カット・映像方針の行 {dict(used)}・文字だけ {tc}（{tc / len(ids) * 100:.1f}%）"
          f"・続く最長 {best}・3カット以上続く所 {runs}")
    print("  種類: " + "・".join(f"{k} {v}" for k, v in Counter(kind.values()).most_common()))
    if (tc, best) != (round(ratio * len(ids)), best_ct) or (tc, best, runs) != WANT:
        raise SystemExit(f"🔴 数え直しの道具・承認の数と合わない（PLAN {tc}・{best}・{runs} ／ 道具 {round(ratio * len(ids))}・{best_ct}"
                         f" ／ 承認 {WANT}）")
    print(f"✓ 数え直しの道具（案B で承認＝{WANT[0]}・最長{WANT[1]}・3連続以上{WANT[2]}か所）と同じ")
    names = {}
    for ln in SCRIPT.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^###\s*第(\d+)章[　\s]+(.+?)（\d+カット）", ln)
        if m:
            names[int(m.group(1))] = m.group(2).strip()
    if len(names) != 9:
        raise SystemExit(f"🔴 台本の章見出しが {len(names)}（9 のはず）")
    groups = OrderedDict()
    for k in ids:
        groups.setdefault(k[:2], []).append(k)
    if list(groups) != list(CHAPTER_OF):
        raise SystemExit(f"🔴 章の並びが違う: {list(groups)}")
    for ch, cids in groups.items():
        n = CHAPTER_OF[ch]
        print(f"  {ch}.py 第{n}章　{names[n]}　{cids[0]}–{cids[-1]}（{len(cids)}）"
              f" 文字だけ {sum(kind[k] in TEXT for k in cids)}")
    if not write:
        print("（書いていない。書くなら --write）")
        return
    for ch, cids in groups.items():
        p = CUTS / f"{ch}.py"
        if p.exists():
            old = p.read_text(encoding="utf-8")
            m = re.search(r"^SPEC = \{(.*?)^\}", old, re.S | re.M)
            if "15本目（リノ" in old and m and m.group(1).strip() and "--force" not in sys.argv:
                print(f"  ⚠️ {ch}.py は15本目の SPEC が入っている＝上書きしない（--force で上書き）")
                continue
        p.write_text(chapter_file(ch, cids, kind, plan, src, names[CHAPTER_OF[ch]], CHAPTER_OF[ch]),
                     encoding="utf-8", newline="\n")
        print(f"  ✓ 書いた {p.relative_to(HERE)}")


if __name__ == "__main__":
    main("--write" in sys.argv)
