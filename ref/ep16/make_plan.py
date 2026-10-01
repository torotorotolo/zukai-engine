# -*- coding: utf-8 -*-
"""make_plan.py — 16本目の章ファイル（tools/cuts/c1〜c9・ca・cb）の**骨組み PLAN** を作る（2026-10-01 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（14本目・15本目の `ref/ep1x/make_plan.py` と同じ作り）。
  ① 台本 `ref/ep16/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典`（242カット・11章＝c1〜c9・ca・cb）
  ② 承認ずみの映像方針 Vault `Projects/事故検証-16本目-映像方針-絵コンテ-20261001.md`（10-01 カズヤくん承認＝§12）
     §1-3（冒頭の絵コンテ）／§3（置き場と使うカット）／§4-2（見る向きの合図13）／§5-1〜§5-4（案C の画と動き）／
     §6（図表）／§8（替える画）
画面の種類（kind）は Vault `Resources/事故検証ch-案C見本/count_text_screens.py` の数え方（preset なし＝画の欄のまま）を
土台に、映像方針 §3 の案C 33カット（§9⑦ の混ざり3＝c104・c408・c807）を上書きして決める。書く前に照合する（違えば止まる）：
  道具の数え方（画の欄のまま）＝写真87・文字だけ29（12.0%）・続く最長2
  → 映像方針 §8 のあと＝**写真85・文字だけ28（11.6%）・続く最長2・3カット以上続く所0**（文字だけ＝決め所 c104 が混ざりへ）

    python ref/ep16/make_plan.py          # 照合して数を出すだけ（書かない）
    python ref/ep16/make_plan.py --write  # 章ファイル 11本を書く（🔴 16本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 映像方針の秒（÷365 の見込み）は書き写さない＝冒頭の絵は narration.json の実測の秒で組む（⑤a-2 引き継ぎ §2-4：
   c105 の終わり 39.0秒＝見込みより2.7秒遅い）。
"""
import importlib.util
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
SCRIPT = HERE / "ref" / "ep16" / "daihon_v2.md"
VAULT = Path(r"C:\Users\konar\Documents\Obsidian Vault")
POLICY = VAULT / "Projects" / "事故検証-16本目-映像方針-絵コンテ-20261001.md"
COUNTER = VAULT / "Resources" / "事故検証ch-案C見本" / "count_text_screens.py"
CUTS = HERE / "tools" / "cuts"
N_CUTS = 242
BASE_WANT = (29, 2, 87)    # 道具の数え方（画の欄のまま）＝文字だけ・続く最長・写真（映像方針 §8 の「いま」）
WANT = (28, 2, 0)          # 文字だけ・続く最長・3カット以上続く所（映像方針 §8 のあと＝10-01 承認）
WANT_PHOTO = 85            # 写真・実写 87 → 85（§8）
WANT_C = 33                # 案C（再現イラスト・混ざり）のカット（§3）

KINDS = ("写真", "図・写真の頁", "再現イラスト", "図解", "混ざり", "文字の頁", "パネル", "決め所")
TEXT = ("パネル", "決め所", "文字の頁")
CHAPTER_OF = dict({f"c{i}": i for i in range(1, 10)}, ca=10, cb=11)
CID = r"c[1-9ab]\d{2}"

# §3 の置き場の名 → 記号
PLACE_TAG = (("VA", "【案C VA 上から見た谷】"), ("VB", "【案C VB 谷を横切る断面】"),
             ("VC", "【案C VC 谷に沿う断面（ダム）】"), ("VD", "【案C VD 正面から見た斜面】"))
# §6 の種類の名 → 記号（＝図解として作る型）
TAG6 = (("場面1", "【線の図】"), ("場面4", "【帯】"), ("断面の図解", "【断面の図解】"), ("地図 drift", "【地図】"))
WANT6 = {"【線の図】": 20, "【帯】": 9, "【断面の図解】": 7, "【地図】": 2}
# 1つの画面の中で種類が入れ替わる・絵と図解が並ぶカット＝映像方針 §9⑦「混ざりは c104・c408・c807 だけ」
#   （門番 check_text_screens は illu_pair と「冒頭の絵 → 決め所」を「混ざり」と見る）
MIXED = {
    "c104": "【混ざり：案C VC → 決め所】",
    "c408": "【混ざり：案C VD＋図解の断面を小さく戻す】",
    "c807": "【混ざり：illu_pair＝模型の想定と実際を並べる】",
}
# 映像方針・④'・⑤a のカットごとの注意（plan の末尾に「⚠️」で足す）
PEOPLE = ("⚠️ 人は顔の無い影・数えない群れなら水が届く瞬間まで描いてよい（10-01 カズヤくん・ルール §5b-111）。"
          "ただし記録にある所だけ＝22時39分に町の人がどこにいたかは S1・S8・S9 に無い＝いまは人を置かない（映像方針 §2）")
NOTES = {
    "c102": PEOPLE,
    "c814": "⚠️ 本編でも町に届くまで描く（10-01 カズヤくん・映像方針 §2）＝集落の建物の面が消えるまで｜" + PEOPLE,
    "c823": ("⚠️ 台本の画の欄の「峡谷の出口で止める＝この先は描かない」は映像方針 §2 で上書き（10-01 カズヤくん＝"
             "本編でも町に届くまで描く）＝町の建物の面が消える・2行目で夜明けの色へ｜" + PEOPLE),
    "c720": "⚠️ 電話は案C にしない（時刻が割れる・私人の交換手＝映像方針 §5 の「使わない場面」）",
    "c312": "⚠️ 1960年の崩落の場所（ダムの約500m上流＝PDF81〈抽〉）は ⑤b で原文に当ててから（当たらなければ模式）",
}
# ④'・映像方針の申し送り＝⑤b で原寸を見る写真（記憶 project-jiko-ep16-vajont「⑤b で原寸」）
FULLSIZE = ("#031", "#029", "#076", "#083", "#028")


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
    """表の行（`|` で割った列）。見出しの行と区切り行は外す。"""
    out = []
    for ln in lines:
        if not ln.startswith("|") or set(ln.replace("|", "").strip()) <= set("-: "):
            continue
        out.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return out[1:]      # 1行目＝見出し


def cuts_in(col):
    """列の中のカットID（「c710〜c713」は間も足す・章をまたぐ範囲は止める）。"""
    col = col.replace("`", "")
    out = []
    for m in re.finditer(rf"({CID})(?:\s*〜\s*({CID}))?", col):
        a, b = m.group(1), m.group(2)
        if b:
            if a[:2] != b[:2] or int(b[2:]) < int(a[2:]):
                raise SystemExit(f"🔴 範囲の書き方が読めない: {a}〜{b}")
            out += [f"{a[:2]}{i:02d}" for i in range(int(a[2:]), int(b[2:]) + 1)]
        else:
            out.append(a)
    return out


def first_cut(col):
    m = re.match(rf"\W*`?({CID})`?", col)
    return m.group(1) if m else None


def clean(s):
    return re.sub(r"\s+", " ", s.replace("**", "").replace("`", "").replace("🆕 ", "").replace("🆕", "")).strip()


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
        m = re.match(rf"^\*\*({CID})\*\*", ln)
        if m:
            parts = ln.split(" ／ ")
            pic[m.group(1)], src[m.group(1)] = clean(parts[1]), clean(" ／ ".join(parts[2:]))
    if set(pic) != set(cuts):
        raise SystemExit(f"🔴 見出し行の読み方が2つで食い違う: {sorted(set(pic) ^ set(cuts))}")
    base = {k: ct.base(k, c["pic"], None) for k, c in cuts.items()}

    # §3 置き場と使うカット（置き場｜見る向き｜中身｜使うカット）→ 案C の33カット
    place = {}
    for cols in table(section(POLICY, r"^## 3\.", r"^## 4\.")):
        tag = tag_of(cols[0], PLACE_TAG)
        if not tag:
            continue
        for k in cuts_in(cols[3]):
            if k in place:
                raise SystemExit(f"🔴 {k} が2つの置き場にある")
            place[k] = tag
    if len(place) != WANT_C:
        raise SystemExit(f"🔴 案C のカットが {len(place)}（§3＝{WANT_C} のはず）")
    kind = dict(base)
    for k in place:
        kind[k] = "混ざり" if k in MIXED else "再現イラスト"
    bad = {k: v for k, v in kind.items() if v not in KINDS}
    if bad:
        raise SystemExit(f"🔴 種類が決まらないカット: {bad}")

    plan = {k: "台本の画：" + pic[k] for k in cuts}
    used = Counter()
    # §6 図表（種類｜中身｜カット）＝図解として作る型（場面1・場面4 の「再現イラスト」の札は出さない）
    got6 = Counter()
    for cols in table(section(POLICY, r"^## 6\.", r"^## 7\.")):
        tag = tag_of(clean(cols[0]), TAG6)
        if not tag:
            continue
        for k in cuts_in(cols[2]):
            if kind[k] != "図解":
                raise SystemExit(f"🔴 §6 の {tag} に図解でないカット {k}（{kind[k]}）")
            plan[k] = f"{tag}{clean(cols[0])}：{clean(cols[1])}（映像方針 §6）｜台本の画：{pic[k]}"
            got6[tag] += 1
    if dict(got6) != WANT6:
        raise SystemExit(f"🔴 §6 の数が違う: {dict(got6)}（{WANT6} のはず）")
    used["§6"] = sum(got6.values())
    # §5-1〜§5-4 案C（カット｜台本の要点｜画と動き｜⚠️）
    for cols in table(section(POLICY, r"^## 5\.", r"^## 6\.")):
        k = first_cut(cols[0])
        if not k:
            continue
        if k not in place:
            raise SystemExit(f"🔴 §5 の {k} が §3 の置き場に無い")
        warn = clean(cols[3]) if len(cols) > 3 else ""
        plan[k] = (f"{place[k]}{clean(cols[2])}（映像方針 §5）"
                   + (f"｜⚠️ {warn}" if warn not in ("", "—") else ""))
        used["§5"] += 1
    # §1-3 冒頭（カット（秒）｜台本｜いまの画｜変えたあとの画と動き｜人｜出典）＝行ごとの画を1つにまとめる（秒は写さない）
    rows = OrderedDict()
    for cols in table(section(POLICY, r"^### 1-3\.", r"^### 1-4\.")):
        k = first_cut(cols[0])
        if not k:
            continue
        line = re.sub(r"（[^）]*）", "", clean(cols[0]).replace(k, "", 1)).strip()
        rows.setdefault(k, []).append((line, clean(cols[3]), clean(cols[4]), clean(cols[5])))
    for k, rs in rows.items():
        if rs[0][1].startswith("そのまま"):
            plan[k] = f"【冒頭】台本の画：{pic[k]}（映像方針 §1-3：{rs[0][1]}）"
        else:
            body = "／".join(f"{ln or '全体'}＝{b}" for ln, b, _, _ in rs)
            hum = "・".join(sorted({h for _, _, h, _ in rs if h not in ("", "—")}))
            rec = "・".join(dict.fromkeys(r for _, _, _, r in rs if r not in ("", "—")))
            plan[k] = f"【冒頭】{place.get(k, '')}{body}｜人：{hum or '—'}｜rec：{rec}（映像方針 §1-3・秒は narration.json の実測で）"
        used["§1-3"] += 1
    # §8 替える画（カット｜台本の文｜いまの画｜替えたあと｜理由｜写真・実写）＝末尾に足す
    for cols in table(section(POLICY, r"^## 8\.", r"^## 9\.")):
        k = first_cut(cols[0])
        if k:
            plan[k] += f"｜替える画（映像方針 §8）：いま＝{clean(cols[2])}・理由＝{clean(cols[4])}"
            used["§8"] += 1
    # §4-2 見る向きの合図（#｜前 → 後｜合図）＝後のカットに足す
    for cols in table(section(POLICY, r"^### 4-2\.", r"^## 5\.")):
        ks = cuts_in(cols[1])
        if len(ks) < 2:
            continue
        plan[ks[-1]] += f"｜合図（映像方針 §4-2 #{clean(cols[0])}・{ks[0]} から）：{clean(cols[2])}"
        used["§4-2"] += 1
    for k, head in MIXED.items():
        plan[k] = head + plan[k]
    for k, v in NOTES.items():
        plan[k] += "｜" + v
    for k in cuts:
        hit = [h for h in FULLSIZE if re.search(re.escape(h) + r"(?!\d)", pic[k])]
        if hit:
            plan[k] += f"｜⚠️ {'・'.join(hit)} は ⑤b で原寸を見てから（④'・映像方針の申し送り）"
            used["原寸"] += 1
    unknown = sorted(set(plan) - set(cuts))
    if unknown:
        raise SystemExit(f"🔴 台本に無いカット: {unknown}")
    # 案C（再現イラスト・混ざり）なのに映像方針の行（§5・§1-3）が1つも当たっていないカットは止める（写し漏れ）
    lost = [k for k in cuts if kind[k] in ("再現イラスト", "混ざり")
            and "（映像方針 §5）" not in plan[k] and "（映像方針 §1-3" not in plan[k]]
    if lost:
        raise SystemExit(f"🔴 案C の種類なのに映像方針の予定が無い: {sorted(set(lost))}")
    if used["§4-2"] != 13:
        raise SystemExit(f"🔴 見る向きの合図が {used['§4-2']}（13 のはず）")
    return cuts, base, kind, plan, src, used


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
    if ch in ("ca", "cb"):
        was = ("■ 🔴 2026-10-01（⑤b-1）：新しく作った（15本目は9章）。14本目の同じ名前の章ファイル（第10・11章＝別の中身）は"
               f"\n  git の `dc6ecf4`（`git show dc6ecf4:tools/cuts/{ch}.py`）。")
    else:
        was = ("■ 🔴 2026-10-01（⑤b-1）：15本目（リノ・エアレース2011）の中身を空にした＝git の `c646174`"
               f"（`git show c646174:tools/cuts/{ch}.py`）。")
    return f'''# -*- coding: utf-8 -*-
"""第{n}章　{name} {ids[0]}–{ids[-1]}（{len(ids)}カット）。16本目（バイオントダム災害）。

{was}
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep16/make_plan.py` で
  台本 §4・承認ずみの映像方針（§1-3 冒頭・§3 置き場・§4-2 合図・§5 案C・§6 図表・§8 替える画）から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所（ルール §5b-79）
  記号＝【案C VA】上から見た谷・【案C VB】谷を横切る断面・【案C VC】谷に沿う断面（ダム）・【案C VD】正面から見た斜面（§3）・
        【冒頭】（§1-3）・【線の図】場面1・【帯】場面4 時間の帯・【断面の図解】・【地図】drift（§6）・【混ざり】（§9⑦）
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
    cuts, base, kind, plan, src, used = build()
    ids = list(cuts)
    ct = load_counter()
    # 照合①：道具の数え方（画の欄のまま）＝映像方針 §8 の「いま」
    b_tc, b_best, _ = count(ids, base)
    b_ph = sum(v == "写真" for v in base.values())
    ratio0, best0 = ct.report(cuts, {}, None, "照合①：count_text_screens（画の欄のまま）")
    if (b_tc, b_best, b_ph) != BASE_WANT or (b_tc, b_best) != (round(ratio0 * len(ids)), best0):
        raise SystemExit(f"🔴 画の欄のままの数が違う（{b_tc}・{b_best}・写真{b_ph} ／ 見込み {BASE_WANT}）＝台本が変わった？")
    # 照合②：案C を上書きした数＝道具の report に同じ上書きを渡して同じ答えか
    over = {k: v for k, v in kind.items() if v != base[k]}
    ratio, best_ct = ct.report(cuts, over, None, "照合②：count_text_screens（映像方針 §3・§8 を当てた）")
    tc, best, runs = count(ids, kind)
    ph = sum(v == "写真" for v in kind.values())
    nc = sum(v in ("再現イラスト", "混ざり") for v in kind.values())
    print(f"■ PLAN：{len(ids)}カット・映像方針の行 {dict(used)}・文字だけ {tc}（{tc / len(ids) * 100:.1f}%）"
          f"・続く最長 {best}・3カット以上続く所 {runs}・写真 {ph}・案C {nc}")
    print("  種類: " + "・".join(f"{k} {v}" for k, v in Counter(kind.values()).most_common()))
    if ((tc, best) != (round(ratio * len(ids)), best_ct) or (tc, best, runs) != WANT or ph != WANT_PHOTO
            or nc != WANT_C):
        raise SystemExit(f"🔴 数え直しの道具・承認の数と合わない（PLAN {tc}・{best}・{runs}・写真{ph}・案C{nc} ／ 道具 "
                         f"{round(ratio * len(ids))}・{best_ct} ／ 承認 {WANT}・写真{WANT_PHOTO}・案C{WANT_C}）")
    print(f"✓ 数え直しの道具・映像方針（§8＝文字だけ{WANT[0]}・最長{WANT[1]}・3連続以上{WANT[2]}か所・写真{WANT_PHOTO}・"
          f"案C{WANT_C}）と同じ")
    rest = Counter(re.match(r"図\s*([^\s（(【]+)", plan[k].split("台本の画：")[-1]).group(1)
                   for k in ids if kind[k] == "図解" and plan[k].startswith("台本の画：図"))
    print("  §6 の外の図解（⑤b の割り振り用・画の欄の2語目）: " + "・".join(f"{k} {v}" for k, v in rest.most_common()))
    names = {}
    for ln in SCRIPT.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^###\s*第(\d+)章[　\s]+(.+?)（\d+カット）", ln)
        if m:
            names[int(m.group(1))] = m.group(2).strip()
    if len(names) != 11:
        raise SystemExit(f"🔴 台本の章見出しが {len(names)}（11 のはず）")
    groups = OrderedDict()
    for k in ids:
        groups.setdefault(k[:2], []).append(k)
    if list(groups) != list(CHAPTER_OF):
        raise SystemExit(f"🔴 章の並びが違う: {list(groups)}")
    for ch, cids in groups.items():
        n = CHAPTER_OF[ch]
        print(f"  {ch}.py 第{n}章　{names[n]}　{cids[0]}–{cids[-1]}（{len(cids)}）"
              f" 文字だけ {sum(kind[k] in TEXT for k in cids)}・案C {sum(k in plan and kind[k] in ('再現イラスト', '混ざり') for k in cids)}")
    if not write:
        print("（書いていない。書くなら --write）")
        return
    for ch, cids in groups.items():
        p = CUTS / f"{ch}.py"
        if p.exists():
            old = p.read_text(encoding="utf-8")
            m = re.search(r"^SPEC = \{(.*?)^\}", old, re.S | re.M)
            if "16本目（バイオント" in old and m and m.group(1).strip() and "--force" not in sys.argv:
                print(f"  ⚠️ {ch}.py は16本目の SPEC が入っている＝上書きしない（--force で上書き）")
                continue
        p.write_text(chapter_file(ch, cids, kind, plan, src, names[CHAPTER_OF[ch]], CHAPTER_OF[ch]),
                     encoding="utf-8", newline="\n")
        print(f"  ✓ 書いた {p.relative_to(HERE)}")


if __name__ == "__main__":
    main(write="--write" in sys.argv)
