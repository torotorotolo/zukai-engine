# -*- coding: utf-8 -*-
"""台帳の 🔴／🔴🔴 の全項目を機械で拾い、「決着の記載」と突き合わせる（⑤c' 5巡目の手順0）。

なぜ：追認（「r08 にも残っている」）だけして決着の無い 🔴 を、目で拾うと取りこぼした
（§AB-2 で13件・§AC-2 で3件）。拾う側を機械にする。

項目の4つの形
  1. 所見の表の行   `| 72 | `c509` | 🔴 … |`（§P より前・2列目にカット番号）   → #72
     ⚠️ 印は3列目とは限らない（`fb_*` の表は4列目）＝行の中で**最初に出る印**で決める
  2. 表の行（1列目が番号）`| **V-11** | `c201` … | 🔴🔴 … |`                     → §V-11
  3. 箇条／小見出し `- **#217** 🔴🔴 …`／`### 🔴 #302 …`                        → #217
  4. 節の見出し     `## R-3. 🔴🔴 …`／`### 🔴🔴 Z-6b-1. …`                       → §R-3

決着の判定（言及ごと）
  - 言及の行に「のまま・まだ・持ち越し・追認・直していない・記載が無い…」→ 持ち越し
  - 言及の行に「直した・閉じる・決着・解消・直さない・粗ではない・⚠️ として…」→ 決着
  - どちらも無ければ、言及の行が属する節の見出しで決める
  - 5巡目の束（§AB-2・§AC-2・§AC-5）で名指しされた項目 → 束5（この巡で直す）
  ⚠️ 古い番号（#1〜#262）は**型でまとめて直した**ので番号で書かれていないことが多い。
     「未決」には手がかり（型の番号・そのカットがあとで出てくる行）を添える＝裁くのは人

⚠️ 出るのは**候補**。最後は人（原文照合）が決める（台帳 §AD-1）：
  `#117` は直したあとも「決着」と出る（別カットの行に強い語がある）／`#384` は ✅ の行にカットが無いので「未決」に落ちる。
  2026-09-11 は「未決・持ち越し」252件をサブエージェント3本で照合した（`qa_out/kb_ad_verdict_{A,B,C}.md`）。

使い方
  python -u qa_out/kb_ad_settle.py                     # 全行
  python -u qa_out/kb_ad_settle.py --upto 3040         # 陽性対照＝§AB より前だけで回す
出力：qa_out/kb_ad_settle.txt（--out で変更）
"""
import re
import sys
import argparse
from pathlib import Path

LEDGER = Path(__file__).with_name("kb_qa_look1.md")

CUT = r"(?:c\d{3}|pr\d{2}|ep\d{2}|ca\d{2}|fb_\w+)"
RE_CUT = re.compile(r"`(" + CUT + r")`")
RE_ROW = re.compile(r"^\|\s*\**(\d{1,3})\**\s*\|([^|]*)\|(.*)$")
RE_IDROW = re.compile(r"^\|\s*\**(§?[A-Z]{1,2}-\d+(?:-\d+)?[a-z]?)\**\s*\|(.*)$")
RE_HASHDEF = re.compile(r"^(?:-\s*\*\*#(\d{1,3})\*\*|#{2,4}\s+(?:\S+\s+)?#(\d{1,3})\b)")
RE_HEAD = re.compile(r"^(#{1,4})\s+(.*)$")
RE_SECID = re.compile(r"(?<![A-Za-z0-9§])§?([A-Z]{1,2}-\d+(?:-\d+)?[a-z]?)(?![\d])")
RE_TYPE = re.compile(r"型\s*([①-⑯])|([①-⑯])\s*の型")
SEV = re.compile(r"🔴+")
MARK = re.compile(r"🔴+|✅|⚪|⚠️")

CARRY = re.compile(r"のまま|まだ|持ち越|追認|直していない|直っていない|未決|未処理|未見|次の巡|次回|"
                   r"残る|残って|残った|宿題|取りこぼ|閉じていない|記載が無|決着の無|決着が無")
SETTLE = re.compile(r"直した|直して|直しずみ|直っ|閉じる|閉じた|決着|解消|取り下げ|撤回|粗ではない|粗でない|"
                    r"直さない|⚠️\s*として|⚠️ で閉|杞憂|誤りではない|変更なし|→\s*⚠️|✅")
HEAD_SETTLE = re.compile(r"直した|直して|直さない|決着|閉じ|粗ではない|粗でなかった|直っている|確かめた|検算して")
HEAD_CARRY = re.compile(r"直していない|持ち越|追認|次 ──|次の|宿題|渡す")
# 所見でない見出し（直した記録・道具・物差し・次への申し送り）
HEAD_NOT_FINDING = re.compile(r"直した|直して|直せた|直さない|決めた|道具|物差し|門番を|測り違い|確かめ|検算|次 ──|次の|束|"
                              r"まとめ|畳み方|版と帳|見た枚|宿題|打ち切り|ひとこと|焼く前|焼き直し|risk")


def load(upto):
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    if upto:
        lines = lines[:upto]
    return lines


def section_map(lines):
    """各行が属する見出しの列（上位→下位）。"""
    cur = [None] * 5
    out = []
    for i, s in enumerate(lines, 1):
        m = RE_HEAD.match(s)
        if m:
            lv = len(m.group(1))
            cur[lv] = (i, lv, m.group(2))
            for k in range(lv + 1, 5):
                cur[k] = None
        out.append([c for c in cur[1:] if c])
    return out


def body_end(lines, i, lv):
    return next((j for j in range(i + 1, len(lines) + 1)
                 if RE_HEAD.match(lines[j - 1]) and len(RE_HEAD.match(lines[j - 1]).group(1)) <= lv),
                len(lines) + 1) - 1


def first_mark(s):
    m = MARK.search(s)
    return m.group(0) if m else ""


def find_items(lines):
    items = {}
    p_start = next((i for i, s in enumerate(lines, 1) if s.startswith("# P.")), len(lines))

    def add(key, i, sev, cuts, text, own, types):
        items.setdefault(key, []).append(dict(line=i, sev=sev, cuts=cuts, text=text, own=own, types=types))

    def types_of(s):
        return sorted(set(a or b for a, b in RE_TYPE.findall(s)))

    for i, s in enumerate(lines, 1):
        # 1. 所見の表の行（§P より前・2列目にカット番号）
        m = RE_ROW.match(s)
        if m and i < p_start and RE_CUT.search(m.group(2)):
            mk = first_mark(m.group(3))
            if mk.startswith("🔴"):
                add(f"#{int(m.group(1))}", i, mk, RE_CUT.findall(s), s, (i, i), types_of(s))
            continue
        # 2. 1列目が節の番号の表の行
        m = RE_IDROW.match(s)
        if m:
            mk = first_mark(m.group(2))
            if mk.startswith("🔴"):
                add("§" + m.group(1).lstrip("§"), i, mk, RE_CUT.findall(s), s, (i, i), types_of(s))
            continue
        # 3. 箇条／小見出しの #N
        m = RE_HASHDEF.match(s)
        if m:
            n = int(m.group(1) or m.group(2))
            mk = first_mark(s[:80])
            if mk.startswith("🔴"):
                own_end = body_end(lines, i, len(s) - len(s.lstrip("#"))) if s.startswith("#") else i
                body = "\n".join(lines[i - 1:own_end])
                add(f"#{n}", i, mk, sorted(set(RE_CUT.findall(body))), s, (i, own_end), types_of(body[:600]))
            continue
        # 4. 節の見出し
        m = RE_HEAD.match(s)
        if m and len(m.group(1)) >= 2:
            t = m.group(2)
            sid = RE_SECID.search(t[:30])
            sv = SEV.search(t)
            if sid and sv and not HEAD_NOT_FINDING.search(t):
                own_end = body_end(lines, i, len(m.group(1)))
                body = "\n".join(lines[i - 1:own_end])
                add(f"§{sid.group(1)}", i, sv.group(0), sorted(set(RE_CUT.findall(body))), s, (i, own_end),
                    types_of(body[:600]))
    return items


def key_regex(key):
    if key.startswith("#"):
        return re.compile(re.escape(key) + r"(?!\d)")
    sid = key[1:]
    return re.compile(r"(?<![A-Za-z0-9])§?" + re.escape(sid) + r"(?![\d-])")


def bundle5_ranges(lines):
    """5巡目の束＝§AB-2・§AC-2・§AC-5 の本文の行範囲。"""
    rng = []
    for i, s in enumerate(lines, 1):
        m = RE_HEAD.match(s)
        if m and re.match(r"(AB-2|AC-2|AC-5)\.", m.group(2)):
            rng.append((i, body_end(lines, i, len(m.group(1)))))
    return rng


STRONG = re.compile(r"直した|直しずみ|閉じる|閉じた|決着ずみ|解消|取り下げ|撤回|直さない|粗ではない|粗でない|⚠️\s*として")


RE_VERDICT = re.compile(r"^\|\s*\**(#\d{1,3}|§[A-Z]{1,2}-\d+(?:-\d+)?[a-z]?)\**\s*\|([^|]*)\|")
RE_VKIND = re.compile(r"NOT-FINDING|NOT-FIX|SUPERSEDED|FIXED\?|FIXED|OPEN")
VERDICT_DONE = ("FIXED", "NOT-FIX", "SUPERSEDED", "NOT-FINDING")


def load_verdicts():
    """サブエージェントの判定（`kb_ad_verdict_{A,B,C}.md`）＝ {キー: (判定, ファイル名)}。"""
    out = {}
    for p in sorted(LEDGER.parent.glob("kb_ad_verdict_*.md")):
        for s in p.read_text(encoding="utf-8").splitlines():
            m = RE_VERDICT.match(s)
            if m:
                k = RE_VKIND.search(m.group(2))
                if k:
                    out[m.group(1)] = (k.group(0), p.name)
    return out


def sec_range(lines, name_re):
    """見出しの名前が name_re に合う節の本文の行範囲。"""
    rng = []
    for i, s in enumerate(lines, 1):
        m = RE_HEAD.match(s)
        if m and re.match(name_re, m.group(2)):
            rng.append((i, body_end(lines, i, len(m.group(1)))))
    return rng


def classify(line_txt, sec_list):
    if CARRY.search(line_txt):
        return "持ち越し"
    if STRONG.search(line_txt):
        return "決着"
    for (_, _, h) in reversed(sec_list):
        if HEAD_CARRY.search(h):
            return "持ち越し"
        if HEAD_SETTLE.search(h):
            return "決着"
    # ⚠️ 最初の印が 🔴 の行は所見そのもの（中に ✅ があっても決着の記載ではない）
    if first_mark(line_txt).startswith("🔴"):
        return "言及"
    if SETTLE.search(line_txt):
        return "決着"
    return "言及"


def sec_label(sec_list):
    for (_, _, h) in reversed(sec_list):
        m = RE_SECID.search(h[:30])
        if m:
            return "§" + m.group(1)
    return "§" + (sec_list[-1][2][:6] if sec_list else "?")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--upto", type=int, default=0, help="台帳をこの行までで切る（陽性対照）")
    ap.add_argument("--out", default=str(Path(__file__).with_name("kb_ad_settle.txt")))
    a = ap.parse_args()

    lines = load(a.upto)
    secs = section_map(lines)
    items = find_items(lines)
    b5 = bundle5_ranges(lines)
    in_b5 = lambda i: any(r0 <= i <= r1 for (r0, r1) in b5)
    ac5 = b5[-1] if b5 and "AC-5" in lines[b5[-1][0] - 1] else (0, -1)
    in_ac5 = lambda i: ac5[0] <= i <= ac5[1]
    # §AD-2（直した）・§AD-3（直さない・理由つき）での言及は決着。
    # §AD-4（絵で決める名簿）は 2026-09-11 カズヤくん決定の終わりの決まり（§AD-7）で**見ずに閉じた**＝決着。
    ad23 = sec_range(lines, r"(AD-2|AD-3|AD-4)\.")
    ad4 = []
    in_ad23 = lambda i: any(r0 <= i <= r1 for (r0, r1) in ad23)
    in_ad4 = lambda i: any(r0 <= i <= r1 for (r0, r1) in ad4)
    ad_start = next((i for i, s in enumerate(lines, 1) if s.startswith("# §AD.")), len(lines) + 1)
    # ⚠️ 判定ファイルは §AC までの台帳を照合したもの。陽性対照（--upto）では読まない。
    verdict = {} if a.upto else load_verdicts()

    # 節の見出しの番号（`## V-11. ✅ …`）。表の行の番号（`| **V-11** |`）と**ぶつかる**ことがある
    head_id = {}
    for i, s in enumerate(lines, 1):
        m = RE_HEAD.match(s)
        if m:
            sid = RE_SECID.search(m.group(2)[:30])
            if sid:
                head_id[i] = "§" + sid.group(1)

    rows = []
    for key, defs in items.items():
        rx = key_regex(key)
        owns = [d["own"] for d in defs]
        own = lambda i: any(o0 <= i <= o1 for (o0, o1) in owns)
        # ⚠️ 番号の衝突：同じ番号の「別の節」がある項目は、決着の行にその項目のカットが無ければ数えない
        clash = any(v == key and not own(i) for i, v in head_id.items())
        icuts = [re.compile("`" + re.escape(c) + "`") for c in set(c for d in defs for c in d["cuts"])]
        ments = []
        for i, s in enumerate(lines, 1):
            if own(i) or not rx.search(s):
                continue
            if head_id.get(i) == key:
                continue                   # 同じ番号の別の節の見出しそのもの
            if in_ad23(i):
                ments.append((i, "決着", s))
                continue
            if in_ad4(i):
                ments.append((i, "持ち越し", s))
                continue
            if clash and not any(r.search(s) for r in icuts):
                ments.append((i, "言及(衝突)", s))
                continue
            if in_b5(i):
                # ⚠️ §AC-5 の「#1〜#15」は束の表の自分の行番号＝台帳の #N ではない
                if key.startswith("#") and int(key[1:]) <= 15 and in_ac5(i):
                    continue
                # 束の節の中でも「閉じた・決着ずみ」と書いた行は決着
                k = "決着" if (SETTLE.search(s) and not CARRY.search(s)) else "束5"
            else:
                k = classify(s, secs[i - 1])
                # ⚠️ #N の項目は、弱い決着（✅・節の見出し）なら**その項目のカットが同じ行に在る**ときだけ数える。
                #    #117 #122 を、別のカットの ✅ 行（L393「absent 型は絵に出典を出す」）で決着と読み違えた。
                if k == "決着" and key.startswith("#") and not STRONG.search(s) \
                        and icuts and not any(r.search(s) for r in icuts):
                    k = "言及(カット無し)"
            ments.append((i, k, s))
        # 判定ファイルの決着は §AD の直前に置く＝あとの §AD-4（持ち越し）・§AD-2/3（決着）が勝つ
        v = verdict.get(key)
        if v and v[0] in VERDICT_DONE:
            ments.append((ad_start - 0.5, "決着", f"{v[1]}：{v[0]}"))
            ments.sort(key=lambda m: m[0])
        kinds = [k for (_, k, _) in ments]
        last_def = max(d["line"] for d in defs)
        if "束5" in kinds:
            st = "束5"
        else:
            later = [(i, k) for (i, k, _) in ments if i > last_def and k in ("決着", "持ち越し")]
            if later and later[-1][1] == "決着":
                st = "決着"
            elif later:
                st = "持ち越し"
            elif "決着" in kinds:
                st = "決着?"          # 決着の言及が定義より前（まとめ節など）
            else:
                st = "未決"
        sev = max((d["sev"] for d in defs), key=len)
        cuts = sorted(set(c for d in defs for c in d["cuts"]))
        types = sorted(set(t for d in defs for t in d["types"]))
        # 手がかり：定義より後ろで、そのカット／型が出てくる行（決着の行を先に）
        hints = []
        if st in ("未決", "持ち越し", "決着?"):
            crx = [re.compile("`" + re.escape(c) + "`") for c in cuts[:6]]
            trx = [re.compile("型\\s*" + t + "|" + t + "\\s*の型") for t in types]
            for i in range(last_def + 1, len(lines) + 1):
                if own(i):
                    continue
                s = lines[i - 1]
                hit = [c for c, r in zip(cuts, crx) if r.search(s)] + [t for t, r in zip(types, trx) if r.search(s)]
                if hit:
                    k = "束5" if in_b5(i) else classify(s, secs[i - 1])
                    hints.append((0 if k in ("決着", "束5") else 1, i, k, sec_label(secs[i - 1]), hit, s))
            hints.sort(key=lambda h: (h[0], -h[1]))
        rows.append(dict(key=key, sev=sev, st=st, defs=defs, ments=ments, cuts=cuts, types=types, hints=hints))

    order = {"未決": 0, "持ち越し": 1, "決着?": 2, "束5": 3, "決着": 4}

    def sk(r):
        k = r["key"]
        return (order[r["st"]], k[0], int(k[1:]) if k[0] == "#" else r["defs"][0]["line"])

    rows.sort(key=sk)
    cnt = {}
    for r in rows:
        cnt[r["st"]] = cnt.get(r["st"], 0) + 1

    out = []
    out.append(f"# kb_ad_settle  台帳={LEDGER.name}  行数={len(lines)}  upto={a.upto or '全行'}")
    out.append(f"# 🔴 項目 {len(rows)}件  " + "  ".join(f"{k}={cnt.get(k, 0)}" for k in order))
    dup = [r["key"] for r in rows if len(r["defs"]) > 1]
    out.append(f"# 定義が2か所以上: {' '.join(dup) if dup else 'なし'}")
    out.append("")
    for r in rows:
        d0 = r["defs"][0]
        out.append(f"## [{r['st']}] {r['key']} {r['sev']}  L{','.join(str(d['line']) for d in r['defs'])}  "
                   f"{' '.join(r['cuts'][:8])}{' …' if len(r['cuts']) > 8 else ''}"
                   f"{'  型' + ''.join(r['types']) if r['types'] else ''}")
        out.append("   定義: " + d0["text"].strip()[:170])
        for (i, k, s) in r["ments"]:
            out.append(f"   L{i} [{k}] " + s.strip()[:150])
        for (_, i, k, sl, hit, s) in r["hints"][:5]:
            out.append(f"   ・手がかり L{i} {sl} [{k}] {'/'.join(hit)}: " + s.strip()[:130])
        out.append("")
    Path(a.out).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {a.out}")
    print(out[1])
    print(out[2])
    for st in ("未決", "持ち越し", "決着?", "束5"):
        ks = [r["key"] for r in rows if r["st"] == st]
        print(f"{st} {len(ks)}: {' '.join(ks)}")


if __name__ == "__main__":
    sys.exit(main())
