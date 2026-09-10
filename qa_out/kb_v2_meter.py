# -*- coding: utf-8 -*-
"""⑤c 検品【見る】3周目 2/2（r04・残り39枚）で使った物差しを1本にまとめたもの。

⚠️ 式を書き写さない。`titan_fig` を**本当に回して** SVG の属性を読む／SPEC の値をそのまま数える。
⚠️ 読んだファイルを必ず印字する（[[feedback-verify-your-own-instrument]]）。
⚠️ 陽性対照は「件数が増える」ことだけを見ない。**もともと全件が該当する指標では件数は動かない**ので、
   その場合は「値が変わったか」を見る（`people` がこれに当たる。2026-09-10 に踏んだ）。

  python -u qa_out/kb_v2_meter.py <部>  [--pos]

    people    people 図の節見出しの級数が1カットの中で割れるか   （対照＝値が落ちるか）
    fontmix   panel の答え（v）の書体が1カットの中で割れるか      （対照＝件数が増えるか）
    units     画面に「フィート」を書いてメートル換算が無いカット   （対照＝件数が減るか）
    paren     photo_ann の問い・答えに括弧／句点が混ざるカット     （対照＝件数が増えるか）
    vgeo      panel の中身が縦にどこからどこまで在るか（段数ごと）
    reuse     同じ素材ファイルを何カットで使っているか
    field     fig の欄・答えが空のブロック・段ラベルの中身
    color     SPEC が使っている色の数え上げ
    all       上を順に全部（⚠️ 門番を同時に2本回さないこと）
"""
import collections
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import titan_fig as T                                      # noqa: E402
from cuts import SPEC                                      # noqa: E402

TEXT = re.compile(r'<text([^>]*)>([^<]*)</text>')
SIZE = re.compile(r'font-size="([0-9.]+)"')
FAM = re.compile(r'font-family="([^"]*)"')
YS = re.compile(r'\b(?:y|y1|y2|cy)="(-?[0-9.]+)"')
HEX = re.compile(r"#[0-9a-fA-F]{6}")
GAP = 8.0


def head(part, pos):
    print(f"■ 読んだファイル: {Path(T.__file__).resolve()}")
    print(f"■ cuts: {Path(sys.modules['cuts'].__file__).resolve()}／SPEC {len(SPEC)} カット")
    print(f"■ 部: {part}／モード: {'陽性対照' if pos else '実測'}")


def figs(kind):
    for cid, sp in SPEC.items():
        f = sp.get("fig")
        if f and f[0] == kind:
            yield cid, dict(f[1])


def attrs(svg):
    """SVG の <text> を {字面: (級数, 書体)} で返す。"""
    out = {}
    for m in TEXT.finditer(svg):
        t = m.group(2)
        if not t.strip():
            continue
        s = SIZE.search(m.group(1))
        f = FAM.search(m.group(1))
        out[t] = (float(s.group(1)) if s else None, f.group(1) if f else None)
    return out


# ── people ────────────────────────────────────────────────────────────────
def part_people(pos):
    rows = []
    for cid, kw in figs("people"):
        nd = [dict(n) for n in kw["nodes"]]
        if pos and nd:
            nd[0]["t"] = str(nd[0].get("t", "")) + "永" * 14
        kw = dict(kw, nodes=nd)
        fig = T.people(**kw)
        svg = "".join(fig.stages) if getattr(fig, "stages", None) else str(fig)
        a = attrs(svg)
        got = [(a[str(n.get("t", "")).strip()][0], str(n.get("t", "")).strip())
               for n in nd if str(n.get("t", "")).strip() in a]
        got = [(s, t) for s, t in got if s is not None]
        if len(got) >= 2:
            rows.append((cid, max(s for s, _ in got) - min(s for s, _ in got), got))
    rows.sort(key=lambda r: -r[1])
    bad = [r for r in rows if r[1] >= GAP]
    print(f"\n🔴 people の節見出しの級数が {GAP:.0f}px 以上割れる ＝ {len(bad)} カット"
          f"（節が2つ以上の people は 全 {len(rows)}）")
    for cid, g, got in bad:
        print(f"  {cid}  開き{g:6.1f}px  " + "／".join(f"{s:.0f}「{t[:16]}」" for s, t in got))
    print("⚠️ この指標は実測でも 11/11 が該当するので、**件数では対照が鳴らない**。"
          "対照は『injectした節の級数が落ちるか』で見る（例＝c414 65→20px・c711 29→20px）。")


# ── fontmix ───────────────────────────────────────────────────────────────
def part_fontmix(pos):
    bad, tot = [], 0
    for cid, kw in figs("panel"):
        bl = [dict(b) for b in kw["blocks"]]
        if pos:
            for b in bl:
                if str(b.get("v", "")).strip():
                    b["v"] = "あいうえおかきくけこさしすせそ"      # かな主体の長い語
                    break
        a = attrs("".join(T.panel(**dict(kw, blocks=bl)).stages))
        vs = [(str(b.get("v", "")).strip(), a[str(b.get("v", "")).strip()][1])
              for b in bl if str(b.get("v", "")).strip() in a]
        vs = [(t, f) for t, f in vs if f]
        if len(vs) < 2:
            continue
        tot += 1
        if len({f for _, f in vs}) > 1:
            bad.append((cid, vs))
    print(f"\n🔴 1カットの中で答え（v）の書体が割れる ＝ {len(bad)} カット"
          f"（答えが2つ以上ある panel は 全 {tot}）")
    for cid, vs in bad:
        print(f"  {cid}  " + "／".join(f"{f}「{t[:14]}」" for t, f in vs))


# ── units ─────────────────────────────────────────────────────────────────
def _texts(sp):
    """⚠️ repr 全文を検索しない（"ft" が "left"/"shift" に当たる）。欄の値だけを集める。"""
    out = []
    for k in ("t", "s"):
        if sp.get(k):
            out.append(str(sp[k]))
    for a in sp.get("ann", []) or []:
        for k in ("t", "v", "d"):
            if a.get(k):
                out.append(str(a[k]))
    f = sp.get("fig")
    if f:
        def walk(o):
            if isinstance(o, dict):
                for v in o.values():
                    walk(v)
            elif isinstance(o, (list, tuple)):
                for v in o:
                    walk(v)
            elif isinstance(o, str):
                out.append(o)
        walk(f[1])
    return out


def part_units(pos):
    bad, ok = [], []
    for cid, sp in SPEC.items():
        ts = _texts(sp)
        if pos:
            ts = ts + ["およそ0メートル"]                       # 対照＝全件に換算を足すと 0 件になるか
        # ⚠️ 2026-09-10（⑤c' 3巡目）：**「20フィート換算」は長さではなく単位の名前**
        #    （TEU ＝ 20フィートコンテナ何個ぶん）。メートルに直すものが無いので数えない。
        #    ⚠️ 除外は「多いから」ではなく**中身が違うから**。ここに書いて理由を残す。
        ts = [t for t in ts if "フィート換算" not in t]
        s = "／".join(ts)
        if "フィート" in s:
            (ok if "メートル" in s else bad).append((cid, [t for t in ts if "フィート" in t]))
    print(f"\n🔴 画面に「フィート」を書いていて、同じ画面にメートル換算が無い ＝ {len(bad)} カット"
          f"（フィートを書くのは 全 {len(bad) + len(ok)}）")
    for cid, t in bad:
        print(f"  {cid}  " + "／".join(t))
    print("✅ 併記あり ＝ " + " ".join(c for c, _ in ok))


# ── paren ─────────────────────────────────────────────────────────────────
def part_paren(pos):
    pk, pv, dots = [], [], []
    first = True
    for cid, sp in SPEC.items():
        for a in sp.get("ann", []) or []:
            t = str(a.get("t", ""))
            v = str(a.get("v", "") or a.get("d", ""))
            if pos and first and t:
                t, first = t + "（試）", False
            if "（" in t or "(" in t:
                pk.append((cid, t))
            if "（" in v or "(" in v:
                pv.append((cid, v))
            if "。" in v:
                dots.append((cid, v))
    for name, rows in (("問い（t）に括弧", pk), ("答え（v/d）に括弧", pv), ("答え（v/d）に句点", dots)):
        print(f"\n🔴 {name} ＝ {len(rows)} 件")
        for cid, t in rows:
            print(f"   {cid}  「{t}」")


# ── vgeo ──────────────────────────────────────────────────────────────────
def part_vgeo(pos):
    rows = []
    for cid, kw in figs("panel"):
        ys = [float(v) for v in YS.findall("".join(T.panel(**kw).stages))]
        if ys:
            rows.append((len(kw["blocks"]), cid, min(ys), max(ys)))
    rows.sort()
    print(f"\n■ panel {len(rows)} カット ／ 段数・カット・中身の上端 y・下端 y"
          "（出典行は y≈878 に固定なので、下端が高いほど下が空く）")
    for n, cid, lo, hi in rows:
        print(f"  段{n}  {cid}  上 {lo:7.1f}  下 {hi:7.1f}")


# ── reuse ─────────────────────────────────────────────────────────────────
def part_reuse(pos):
    use = collections.defaultdict(list)
    for cid, sp in SPEC.items():
        if sp.get("photo"):
            use[sp["photo"]].append(cid)
    multi = {k: v for k, v in use.items() if len(v) >= 2}
    print(f"\n🔴 同じ素材を2カット以上で使っている ＝ {len(multi)} 件"
          f"（素材つきカットは 全 {sum(len(v) for v in use.values())}）")
    for k, v in sorted(multi.items(), key=lambda kv: -len(kv[1])):
        print(f"  {len(v)}カット  {k}  ← " + " ".join(v))


# ── field ─────────────────────────────────────────────────────────────────
def part_field(pos):
    kw_cnt = collections.defaultdict(set)
    kcnt, kwhere, novc = collections.Counter(), collections.defaultdict(set), []
    for cid, sp in SPEC.items():
        f = sp.get("fig")
        if not f:
            continue
        kind, kw = f[0], f[1]
        for k in kw:
            kw_cnt[f"{kind}.{k}"].add(cid)
        if kind == "panel":
            blanks = [b for b in kw.get("blocks", []) if not str(b.get("v", "")).strip()]
            if blanks:
                novc.append((cid, len(blanks), len(kw.get("blocks", []))))
            for b in kw.get("blocks", []):
                kk = str(b.get("k", ""))
                kcnt[kk] += 1
                kwhere[kk].add(cid)
    print("\n■ fig の欄が何カットに出るか")
    for k in sorted(kw_cnt, key=lambda k: -len(kw_cnt[k])):
        s = sorted(kw_cnt[k])
        print(f"  {k:22s} {len(s):3d}カット" + ("  " + " ".join(s) if len(s) <= 8 else ""))
    print(f"\n■ panel で答え（v）が空のブロックを持つカット ＝ {len(novc)}")
    for cid, b, t in novc:
        print(f"  {cid}  空 {b}／全 {t} ブロック")
    print("\n■ panel の段ラベル（k）の中身")
    for k, n in kcnt.most_common():
        s = sorted(kwhere[k])
        print(f"  「{k}」 のべ{n:4d} ／ {len(s):3d}カット" + ("  " + " ".join(s) if len(s) <= 8 else ""))


# ── color ─────────────────────────────────────────────────────────────────
def part_color(pos):
    cnt, where = collections.Counter(), collections.defaultdict(set)
    for cid, sp in SPEC.items():
        for m in HEX.findall(repr(sp)):
            cnt[m.lower()] += 1
            where[m.lower()].add(cid)
    print(f"\n■ SPEC が使っている色 ＝ {len(cnt)} 種")
    for c, n in cnt.most_common():
        ws = sorted(where[c])
        print(f"  {c}  のべ{n:4d}回 ／ {len(ws):3d}カット" + ("  " + " ".join(ws) if len(ws) <= 6 else ""))


PARTS = {
    "people": part_people, "fontmix": part_fontmix, "units": part_units,
    "paren": part_paren, "vgeo": part_vgeo, "reuse": part_reuse,
    "field": part_field, "color": part_color,
}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pos = "--pos" in sys.argv
    part = args[0] if args else "all"
    if part == "all":
        for name, fn in PARTS.items():
            head(name, pos)
            fn(pos)
            print()
        return 0
    if part not in PARTS:
        print(f"⚠️ 部が違う: {part}／使えるのは " + " ".join(PARTS) + " all")
        return 2
    head(part, pos)
    PARTS[part](pos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
