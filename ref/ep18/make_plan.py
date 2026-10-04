# -*- coding: utf-8 -*-
"""make_plan.py — 18本目の章ファイル（tools/cuts/c1〜c9・ca・cb）の**骨組み PLAN** を作る（2026-10-04 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（14〜16本目の `ref/ep1x/make_plan.py` と同じ作り）。
  ① 台本 `ref/ep18/daihon_v2.md` §4 の見出し行 `**c101** 🔧 ／ 画 ／ 出典`（242カット・11章＝c1〜c9・ca・cb）
  ② 承認ずみの映像方針 Vault `Projects/事故検証-18本目-映像方針-絵コンテ-20261001.md`（10-01 カズヤくん承認＝§15・10-04 §16・§17）
     §1-3（冒頭の絵コンテ）／§3（置き場と使うカット）／§4（見る向きの合図5）／§5（案C の画と動き）／§6（前置き c106〜c115）／
     §8（記録映画）／§9（頁の版）／§11（替える画13）
画面の種類（kind）は Vault `Resources/事故検証ch-案C見本/count_text_screens.py` の数え方（preset なし＝画の欄のまま）を
土台に、§3 の案C 24カット（混ざり2＝c102・c103）と §11 の替える画（c105・cb21＝頁、c107＝並べ図）を上書きして決める。
書く前に照合する（違えば止まる）：
  道具の数え方（画の欄のまま）＝写真64・文字だけ38（15.7%）・続く最長2
  → 映像方針 §11 のあと＝**写真57（23.6%）・文字だけ40（16.5%）・続く最長2・3カット以上続く所0・案C 22＋混ざり2**

    python ref/ep18/make_plan.py          # 照合して数を出すだけ（書かない）
    python ref/ep18/make_plan.py --write  # 章ファイル 11本を書く（🔴 18本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 映像方針の秒（÷365 の見込み）は書き写さない＝冒頭の絵は narration.json の実測の秒で組む（⑤a-2 引き継ぎ §2-2：
   実測は見込みより約1秒遅い＝c104-3★ 0:31.8・c105-1 0:36.6・c105 の終わり 45.9秒）。
🆕 フリー素材の映像（映像方針 §17・ルール §2-5c）は ⑤b-7 で替える場面を表にして承認をもらってから、PLAN の種類を
   「フリー素材」に直す（この事故の写真＝20%の数に入れない・別に数える＝門番 check_text_screens・check_cuts）。
   この道具はまだ1カットも「フリー素材」にしない（素材は ⑤b-7 で探す）。
"""
import importlib.util
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
SCRIPT = HERE / "ref" / "ep18" / "daihon_v2.md"
VAULT = Path(r"C:\Users\konar\Documents\Obsidian Vault")
POLICY = VAULT / "Projects" / "事故検証-18本目-映像方針-絵コンテ-20261001.md"
COUNTER = VAULT / "Resources" / "事故検証ch-案C見本" / "count_text_screens.py"
CUTS = HERE / "tools" / "cuts"
N_CUTS = 242
BASE_WANT = (38, 2, 64)    # 道具の数え方（画の欄のまま）＝文字だけ・続く最長・写真（映像方針 §11 の「いま」）
WANT = (40, 2, 0)          # 文字だけ・続く最長・3カット以上続く所（映像方針 §11 のあと＝10-01 承認）
WANT_PHOTO = 57            # 写真・実写 64 → 57（§11）
WANT_C = 24                # 案C（再現イラスト22・混ざり2）のカット（§3）

KINDS = ("写真", "図・写真の頁", "再現イラスト", "図解", "混ざり", "文字の頁", "パネル", "決め所", "フリー素材")
TEXT = ("パネル", "決め所", "文字の頁")
CHAPTER_OF = dict({f"c{i}": i for i in range(1, 10)}, ca=10, cb=11)
CID = r"c[1-9ab]\d{2}"

# §3 の置き場の名（表の1列目の頭）→ 記号
PLACE_TAG = (("SA", "【案C SA 横から見た海】"), ("SB", "【案C SB 上から見た海（北が上）】"),
             ("SC", "【案C SC 上から見た海の底】"), ("SD", "【案C SD 横から見た海の底の捜索】"))
# 1つの画面の中で本物の映像・写真と絵が入れ替わるカット＝映像方針 §12 ⑦「混ざりは冒頭の c102・c103 だけ」
MIXED = {
    "c102": "【混ざり：本物の記録映画 85185 → 案C SA】",
    "c103": "【混ざり：案C SA（推定の札・9時18.1分）→ 本物の写真 thr_t16】",
}
# §11 の替える画のうち、置き場（§3）で決まらない種類＝頁と並べ図。照合＝§11 の「写真・実写」「文字だけ」の列
OVER = {"c105": "文字の頁", "c107": "図解", "cb21": "文字の頁"}
WANT11 = dict(photo_minus={"c101", "c105", "c107", "c318", "cb21"}, to_mixed={"c102", "c103"}, text_plus={"c105", "cb21"})
# 映像方針のカットごとの注意（plan の末尾に「⚠️」で足す）
DEPTH = ("⚠️ 深さの数を幾何で漏らさない（映像方針 §2 ③'・18本目だけの線）＝深さの目盛りのある段に潜水艦を置かない・"
         "試験深度の線は目盛りの切れ目（≈）の向こう")
SUB_CUTS = ("c101", "c102", "c103", "c106", "c310", "c311", "c319", "c405", "c407", "c409", "c411")
NOTES = {
    "c103": ("⚠️ 推定の札は 9:17 から（意見45「the actual hull collapse occurred at 0918.1R」）・壊れる物（check_illu ⑫）と"
             "9時18.1分の音の輪（⑰）は c103 だけ・壊れた船体は数えられる前に暗がりへ（⑮）・光・泡・炎・人・深さは描かない。"
             "艦首の角度は意見45 の Case III を頁の画像で確かめてから（OCR の文字の層は「150 up angle」＝§1-3）"),
    "c104": "⚠️ 頁は見た目の字がある版だけ（§9）＝冒頭の秒は narration.json の実測（★ 0:31.8）",
    "c105": ("🔴 物証の本物＝証拠111（X p.531〜533＝前の艦長の評価書 serial 086・1962-11-16）。第5段落に語りと同時に印"
             "（c105-3 0:41.3〜・c105 の終わり 45.9秒）。cb21 と同じ段落"),
    "c318": "⚠️ 想定の札「少佐の証言（仮定）」（ss.ILLU_ASSUME）・潜水艦なし（縮尺どおり）",
    "c411": "⚠️ ここで艦の絵を止める（本編は 9:17 まで＝check_illu ⑮・kousei §4-1）",
    "c420": "⚠️ 潜水艦は描かない（9:17 より後）",
    "c422": "⚠️ 潜水艦は描かない（9:17 より後）",
    "c502": "⚠️ 潜水艦は描かない（9:17 より後）",
    "c519": "⚠️ 捜索の艦の数は認定34 に合わせる（数えて表に・決まらなければ描かない＝映像方針 §12 ③'）",
    "ca21": "⚠️ 大きな塊は R17 の Plate（形のもと）があるときだけ描く（無ければ円と札だけ＝映像方針 §2①）",
    "cb21": "🔴 証拠111 の第5段落（c105 と同じ段落）→ 勧告20（R08 p.220）＝物証を終章で回収（語りは変えない）",
}
CB23_DROP = "＝c101 と同じ絵に戻す"   # 映像方針 §11 末尾：c101 が絵になるので画の欄の注を外す


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
    """表の行（`|` で割った列）。見出しの行と区切り行は外す（節の中に表が2つあれば両方の見出しを外す）。"""
    out, head = [], True
    for ln in lines:
        if not ln.startswith("|"):
            head = True
            continue
        if set(ln.replace("|", "").strip()) <= set("-: "):
            continue
        if head:
            head = False
            continue
        out.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return out


def cuts_in(col):
    """列の中のカットID（「c710〜c713」は間も足す・章をまたぐ範囲は止める）。「c103 1〜2行目」の行の範囲は拾わない。"""
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
    m = re.search(rf"({CID})", col.replace("`", ""))
    return m.group(1) if m else None


def clean(s):
    return re.sub(r"\s+", " ", s.replace("**", "").replace("`", "").replace("🆕 ", "").replace("🆕", "")).strip()


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
    if pic["cb23"].count(CB23_DROP) != 1 or sum(CB23_DROP in v for v in pic.values()) != 1:
        raise SystemExit(f"🔴 cb23 の画の欄の注「{CB23_DROP}」が見つからない／ほかのカットにもある")
    base = {k: ct.base(k, c["pic"], None) for k, c in cuts.items()}

    # §3 置き場と使うカット（置き場｜見る向き｜中身｜使うカット）→ 案C の24カット
    place = {}
    for cols in table(section(POLICY, r"^## 3\.", r"^## 4\.")):
        tag = next((t for k, t in PLACE_TAG if clean(cols[0]).startswith(k)), "")
        if not tag:
            continue
        for k in cuts_in(cols[3]):
            if k in place:
                raise SystemExit(f"🔴 {k} が2つの置き場にある")
            place[k] = tag
    if len(place) != WANT_C:
        raise SystemExit(f"🔴 案C のカットが {len(place)}（§3＝{WANT_C} のはず）")
    if not set(MIXED) <= set(place):
        raise SystemExit("🔴 混ざりのカットが §3 の置き場に無い")
    # §11 替える画（カット｜いまの画｜替えたあと｜理由｜写真・実写｜文字だけ）＝種類の上書きを照合する
    rows11 = []
    got11 = dict(photo_minus=set(), to_mixed=set(), text_plus=set())
    for cols in table(section(POLICY, r"^## 11\.", r"^## 12\.")):
        ks = cuts_in(cols[0])
        if not ks:
            continue
        rows11.append((ks, cols))
        for k in ks:
            if re.search(r"[−-]1", cols[4]):
                got11["photo_minus"].add(k)
            if "混ざり" in cols[4]:
                got11["to_mixed"].add(k)
            if "+1" in cols[5]:
                got11["text_plus"].add(k)
    if got11 != WANT11:
        raise SystemExit(f"🔴 §11 の替える画の数が違う: {got11}（{WANT11} のはず）")
    kind = dict(base)
    for k in place:
        kind[k] = "混ざり" if k in MIXED else "再現イラスト"
    for k, v in OVER.items():
        if k in place:
            raise SystemExit(f"🔴 {k} は置き場にも上書きにもある")
        kind[k] = v
    bad = {k: v for k, v in kind.items() if v not in KINDS}
    if bad:
        raise SystemExit(f"🔴 種類が決まらないカット: {bad}")

    plan = {k: "台本の画：" + pic[k] for k in cuts}
    plan["cb23"] = ("台本の画：" + pic["cb23"].replace(CB23_DROP, "")
                    + "｜⚠️ 画の欄の注「c101 と同じ絵に戻す」は外した（c101 は SA の絵になった＝映像方針 §11）")
    used = Counter()
    # §1-3 冒頭（カット（秒）｜いまの画｜変えたあとの画と動き｜人｜出典）＝行ごとの画を1つにまとめる（秒は写さない）
    rows = OrderedDict()
    for cols in table(section(POLICY, r"^### 1-3\.", r"^### 1-4\.")):
        k = first_cut(cols[0])
        if not k:
            continue
        line = re.sub(r"（[^）]*）", "", clean(cols[0]).replace(k, "", 1)).strip()
        rows.setdefault(k, []).append((line, clean(cols[2]), clean(cols[3]), clean(cols[4])))
    for k, rs in rows.items():
        body = "／".join(f"{ln or '全体'}＝{b}" for ln, b, _, _ in rs)
        hum = "・".join(sorted({h for _, _, h, _ in rs if h not in ("", "—")}))
        rec = "・".join(dict.fromkeys(r for _, _, _, r in rs if r not in ("", "—")))
        plan[k] = (f"【冒頭】{place.get(k, '')}{body}｜人：{hum or '—'}｜rec：{rec}"
                   f"（映像方針 §1-3・秒は narration.json の実測で）｜台本の画（いま）：{pic[k]}")
        used["§1-3"] += 1
    # §5 案C：§5-1 は表（カット｜動き｜rec）・§5-2／§5-3 は箇条（「／」で区切ったひとまとまりごとに頭のカット）
    sec5 = section(POLICY, r"^## 5\.", r"^## 6\.")
    for cols in table(sec5):
        for k in cuts_in(cols[0]):
            if k in rows:          # c101〜c103 は §1-3
                continue
            if k not in place:
                raise SystemExit(f"🔴 §5 の {k} が §3 の置き場に無い")
            plan[k] = f"{place[k]}{clean(cols[1])}｜rec：{clean(cols[2])}（映像方針 §5）"
            used["§5"] += 1
    for ln in sec5:
        if not ln.startswith("- "):
            continue
        for seg in ln[2:].split("／"):
            k = first_cut(seg)
            if not k or k not in place:
                continue
            if "（映像方針 §5）" in plan[k]:
                raise SystemExit(f"🔴 §5 に {k} が2回ある")
            plan[k] = f"{place[k]}{clean(seg)}（映像方針 §5）"
            used["§5"] += 1
    # §6 前置き（カット｜秒｜いまの画｜推奨）＝推奨を足す（秒は写さない）
    for cols in table(section(POLICY, r"^## 6\.", r"^## 7\.")):
        k = first_cut(cols[0])
        if k:
            plan[k] += f"｜前置き（映像方針 §6）：{clean(cols[3])}"
            used["§6"] += 1
    # §8 記録映画 85185 の12カット（絵｜いま｜推奨）
    for cols in table(section(POLICY, r"^## 8\.", r"^## 9\.")):
        for k in cuts_in(cols[1]):
            plan[k] += (f"｜記録映画（映像方針 §8）：{clean(cols[0])}＝{clean(cols[2])}"
                        "（額装＋地のぼかし・縦1.8倍まで・⑤b-7 で SAR を測る）")
            used["§8"] += 1
    # §9 頁の版（カット｜映す頁｜測った値｜決め）
    for cols in table(section(POLICY, r"^## 9\.", r"^## 10\.")):
        for k in dict.fromkeys(cuts_in(cols[0])):
            plan[k] += f"｜頁の版（映像方針 §9）：{clean(cols[1])}＝{clean(cols[3])}"
            used["§9"] += 1
    # §11 替える画＝末尾に足す
    for ks, cols in rows11:
        for k in ks:
            plan[k] += f"｜替える画（映像方針 §11）：いま＝{clean(cols[1])} → {clean(cols[2])}・理由＝{clean(cols[3])}"
            used["§11"] += 1
    # §4 見る向きの合図（#｜前 → 後｜合図）＝後のカットに足す（#1 は最初の絵＝前が無い）
    for cols in table(section(POLICY, r"^## 4\.", r"^## 5\.")):
        ks = cuts_in(cols[1])
        if not ks:
            continue
        frm = f"・{ks[0]} から" if len(ks) > 1 else ""
        plan[ks[-1]] += f"｜合図（映像方針 §4 #{clean(cols[0])}{frm}）：{clean(cols[2])}"
        used["§4"] += 1
    for k, head in MIXED.items():
        plan[k] = head + plan[k]
    for k in SUB_CUTS:
        plan[k] += "｜" + DEPTH
    for k, v in NOTES.items():
        plan[k] += "｜" + v
    unknown = sorted(set(plan) - set(cuts))
    if unknown:
        raise SystemExit(f"🔴 台本に無いカット: {unknown}")
    # 案C（再現イラスト・混ざり）なのに映像方針の行（§5・§1-3）が1つも当たっていないカットは止める（写し漏れ）
    lost = [k for k in cuts if kind[k] in ("再現イラスト", "混ざり")
            and "（映像方針 §5）" not in plan[k] and "（映像方針 §1-3" not in plan[k]]
    if lost:
        raise SystemExit(f"🔴 案C の種類なのに映像方針の予定が無い: {sorted(set(lost))}")
    want_used = {"§1-3": 5, "§5": WANT_C - 3, "§4": 5, "§11": 13}
    bad_used = {k: (used[k], v) for k, v in want_used.items() if used[k] != v}
    if bad_used:
        raise SystemExit(f"🔴 映像方針の行の数が違う（いま, 見込み）: {bad_used}")
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
    return f'''# -*- coding: utf-8 -*-
"""第{n}章　{name} {ids[0]}–{ids[-1]}（{len(ids)}カット）。18本目（スレッシャー号のリメイク）。

■ 🔴 2026-10-04（⑤b-1）：16本目（バイオントダム災害）の中身を空にした＝git の `b044b56`（`git show b044b56:tools/cuts/{ch}.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep18/make_plan.py` で
  台本 §4・承認ずみの映像方針（§1-3 冒頭・§3 置き場・§4 合図・§5 案C・§6 前置き・§8 記録映画・§9 頁の版・§11 替える画）から
  機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」と「フリー素材」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所／フリー素材（ルール §5b-79・§2-5c）
  記号＝【案C SA】横から見た海・【案C SB】上から見た海（北が上）・【案C SC】上から見た海の底・【案C SD】横から見た海の底の捜索（§3）・
        【冒頭】（§1-3）・【混ざり】（§12 ⑦）
  🆕 フリー素材の映像（映像方針 §17）＝⑤b-7 で替える場面を表にして承認 → その種類を「フリー素材」に（20% と【映像あり】に数えない）
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
    # 照合①：道具の数え方（画の欄のまま）＝映像方針 §11 の「いま」
    b_tc, b_best, _ = count(ids, base)
    b_ph = sum(v == "写真" for v in base.values())
    ratio0, best0 = ct.report(cuts, {}, None, "照合①：count_text_screens（画の欄のまま）")
    if (b_tc, b_best, b_ph) != BASE_WANT or (b_tc, b_best) != (round(ratio0 * len(ids)), best0):
        raise SystemExit(f"🔴 画の欄のままの数が違う（{b_tc}・{b_best}・写真{b_ph} ／ 見込み {BASE_WANT}）＝台本が変わった？")
    # 照合②：案C と替える画を上書きした数＝道具の report に同じ上書きを渡して同じ答えか
    over = {k: v for k, v in kind.items() if v != base[k]}
    ratio, best_ct = ct.report(cuts, over, None, "照合②：count_text_screens（映像方針 §3・§11 を当てた）")
    tc, best, runs = count(ids, kind)
    ph = sum(v == "写真" for v in kind.values())
    nc = sum(v in ("再現イラスト", "混ざり") for v in kind.values())
    print(f"■ PLAN：{len(ids)}カット・映像方針の行 {dict(used)}・文字だけ {tc}（{tc / len(ids) * 100:.1f}%）"
          f"・続く最長 {best}・3カット以上続く所 {runs}・写真 {ph}（{ph / len(ids) * 100:.1f}%）・案C {nc}")
    print("  種類: " + "・".join(f"{k} {v}" for k, v in Counter(kind.values()).most_common()))
    if ((tc, best) != (round(ratio * len(ids)), best_ct) or (tc, best, runs) != WANT or ph != WANT_PHOTO
            or nc != WANT_C):
        raise SystemExit(f"🔴 数え直しの道具・承認の数と合わない（PLAN {tc}・{best}・{runs}・写真{ph}・案C{nc} ／ 道具 "
                         f"{round(ratio * len(ids))}・{best_ct} ／ 承認 {WANT}・写真{WANT_PHOTO}・案C{WANT_C}）")
    print(f"✓ 数え直しの道具・映像方針（§11＝文字だけ{WANT[0]}・最長{WANT[1]}・3連続以上{WANT[2]}か所・写真{WANT_PHOTO}・"
          f"案C{WANT_C}）と同じ")
    # 見る向きの合図（映像方針 §4・16本目 mech16 §11 の数え方）：台本の順で**隣り合う**案C のカットの置き場が変われば、
    #   後のカットに合図が要る（間に写真・図解が挟まれば向きの切り替えではない＝向きの札だけ＝§4 #4 の注）
    place_of = {k: m.group(1) for k in ids for m in [re.search(r"【案C (S[A-D]) ", plan[k])] if m}
    pairs = [(a, b) for a, b in zip(ids, ids[1:]) if a in place_of and b in place_of and place_of[a] != place_of[b]]
    nosig = [f"{a}（{place_of[a]}）→{b}（{place_of[b]}）" for a, b in pairs if "合図（映像方針 §4" not in plan[b]]
    print(f"  見る向き：隣り合って置き場が変わる所 {len(pairs)}（" + "・".join(f"{a}→{b}" for a, b in pairs)
          + f"）・合図なし {len(nosig)}・§4 の合図 {sum('合図（映像方針 §4' in plan[k] for k in ids)}")
    if nosig:
        raise SystemExit(f"🔴 見る向きが変わるのに合図が無い: {nosig}")
    rest = Counter(m.group(1) if m else f"替えた画（{k}）"
                   for k in ids if kind[k] == "図解"
                   for m in [re.match(r"図\s*([^\s（(【]+)", plan[k].split("台本の画：")[-1])])
    print("  図解の内わけ（⑤b の割り振り用・画の欄の2語目）: " + "・".join(f"{k} {v}" for k, v in rest.most_common()))
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
              f" 文字だけ {sum(kind[k] in TEXT for k in cids)}・写真 {sum(kind[k] == '写真' for k in cids)}"
              f"・案C {sum(kind[k] in ('再現イラスト', '混ざり') for k in cids)}")
    if not write:
        print("（書いていない。書くなら --write）")
        return
    for ch, cids in groups.items():
        p = CUTS / f"{ch}.py"
        if p.exists():
            old = p.read_text(encoding="utf-8")
            m = re.search(r"^SPEC = \{(.*?)^\}", old, re.S | re.M)
            if "18本目（スレッシャー" in old and m and m.group(1).strip() and "--force" not in sys.argv:
                print(f"  ⚠️ {ch}.py は18本目の SPEC が入っている＝上書きしない（--force で上書き）")
                continue
        p.write_text(chapter_file(ch, cids, kind, plan, src, names[CHAPTER_OF[ch]], CHAPTER_OF[ch]),
                     encoding="utf-8", newline="\n")
        print(f"  ✓ 書いた {p.relative_to(HERE)}")


if __name__ == "__main__":
    main(write="--write" in sys.argv)
