# -*- coding: utf-8 -*-
"""⑤c 検品【見る】2周目 3/3 の物差し（2026-09-10）。2つを1本にまとめた。

  credit … そのカットに実際に出る出典行を作り、**丸括弧が2つ以上**続く形を数える
           （§S-13-4 は「その素材は画面に出ない」で閉じたが、ep01 で目に見えた）
  para   … 並列のはずの項目（fig=panel の blocks / people の nodes）の**実際の級数**。
           `fm.fit` の戻りで測る。1枚の中でいちばん開いた組を出す。

陽性対照:
  credit … ep01 が 2組（（NTSB）（Key Bridge Response 2024））で必ず挙がること
  para   … ca12 が 4項目で級数が割れること（目で見て 72 対 58 くらい）
使い方: python qa_out/kb_look2_final.py credit
        python qa_out/kb_look2_final.py para
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "tools")

import scene_jiko as S  # noqa: E402
from cuts import SPEC  # noqa: E402

fm = S.fm
PAREN = re.compile(r"（[^（）]*）\s*（[^（）]*）")


def credits():
    rows = []
    for cid, spec in SPEC.items():
        if "photo" not in spec:      # 図だけのカットは出典行を出さない
            continue
        try:
            cr = S.credit_of(cid, spec)
        except Exception as e:                           # noqa: BLE001
            rows.append((cid, "!! " + type(e).__name__, str(e)[:60]))
            continue
        if not cr:
            continue
        m = PAREN.search(cr)
        if m:
            rows.append((cid, m.group(0), cr))
    print(f"出典行に丸括弧が2つ続くカット: {len(rows)}")
    seen = {}
    for cid, hit, cr in rows:
        seen.setdefault(hit, []).append(cid)
    for hit, ids in sorted(seen.items(), key=lambda kv: -len(kv[1])):
        print(f"  {len(ids):3d}枚  {hit}")
        print(f"          {' '.join(ids)}")


def para():
    """並列項目の実際の級数。**描画関数を本当に回して** txt/para の size を拾う。

    再導出しない（自分で幅と上限を写すと必ずどこか違う＝S-14 の2件目・3件目）。
    """
    import titan_fig as TF
    rec = []
    o_txt, o_para = TF.txt, TF.para

    def w_txt(x, y, t, size=32, *a, **k):
        rec.append((str(t), round(float(size), 1)))
        return o_txt(x, y, t, size, *a, **k)

    def w_para(x, y, t, cols=28, size=34, *a, **k):
        rec.append((str(t), round(float(size), 1)))
        return o_para(x, y, t, cols, size, *a, **k)

    out = []
    for cid, spec in SPEC.items():
        fig = spec.get("fig")
        if not fig:
            continue
        kind, d = fig
        if kind not in ("panel", "people"):
            continue
        items = ([b.get("t", "") for b in d.get("blocks", [])] if kind == "panel"
                 else [n.get("t", "") for n in d.get("nodes", [])])
        if len(items) < 2:
            continue
        rec.clear()
        TF.txt, TF.para = w_txt, w_para
        try:
            (TF.panel if kind == "panel" else TF.people)(**d)
        except Exception as e:                           # noqa: BLE001
            print(f"  !! {cid} {type(e).__name__}: {e}")
            continue
        finally:
            TF.txt, TF.para = o_txt, o_para
        got = {}
        for t, sz in rec:
            if t in items and t not in got:
                got[t] = sz
        sz = [got.get(t) for t in items]
        if any(v is None for v in sz):
            print(f"  !! {cid} 級数が拾えなかった欄がある: "
                  f"{[t for t, v in zip(items, sz) if v is None]}")
            continue
        out.append((round(max(sz) - min(sz), 1), cid, kind,
                    list(zip(items, sz))))
    out.sort(reverse=True)
    print(f"並列項目が2つ以上ある fig: {len(out)}"
          f"／開きが 12px 以上: {sum(1 for o in out if o[0] >= 12)}")
    import os
    lim = int(os.environ.get("N", "14"))
    for diff, cid, kind, pairs in out[:lim]:
        print(f"  {cid} ({kind}) 開き {diff}px")
        for t, s in pairs:
            print(f"      {s:6.1f}  {t}")


def num():
    """数字の書き方のゆれ。**同じカットの画面と字幕で、同じ数が別の形**になっていないか。

    陽性対照: pr01 が「2,769（画面）／2769（字幕）」で必ず挙がること。
    """
    import re as _re
    from narration import SCRIPT

    say = {}
    for cid, lines in SCRIPT:
        say.setdefault(cid, []).extend(lines)

    def strs(spec):
        o = [str(spec.get("t", "")), str(spec.get("s", ""))]
        for a in spec.get("ann", []) or []:
            o += [str(a.get(k, "")) for k in ("t", "v", "d")]
        fig = spec.get("fig")
        if fig:
            _, d = fig
            for b in (d.get("blocks") or []) + (d.get("nodes") or []):
                o += [str(b.get(k, "")) for k in ("k", "t", "v", "d")]
            for e in d.get("edges") or []:
                o.append(str(e.get("t", "")))
            o.append(str(d.get("note", "")))
            o.append(str(d.get("lead", "")))
        return [x for x in o if x]

    NUM = _re.compile(r"[0-9][0-9,]*")
    # 🔴 1版目は「5万5671トン」を 5671 と読み、c303 を取りこぼした。
    #    万・千の混じった書き方も同じ数として並べる。
    JP = _re.compile(r"(?:([0-9]+)万)?(?:([0-9]+)千)?([0-9]*)")

    def canon(bag):
        """その文字列に出てくる数を、カンマも万千も外した形の集合にする。"""
        o = {}
        for s_ in bag:
            for m in _re.finditer(r"(?:[0-9][0-9,]*)(?:万[0-9]*)?(?:千[0-9]*)?", s_):
                raw = m.group(0)
                w = _re.match(r"([0-9][0-9,]*)万([0-9]*)", raw)
                t_ = _re.match(r"([0-9][0-9,]*)千([0-9]*)", raw)
                if w:
                    v = int(w.group(1).replace(",", "")) * 10000
                    v += int(w.group(2) or 0) * (10 ** (4 - len(w.group(2)))
                                                 if w.group(2) else 0)
                    v = (int(w.group(1).replace(",", "")) * 10000
                         + (int(w.group(2)) * 10 ** (4 - len(w.group(2)))
                            if w.group(2) else 0))
                elif t_:
                    v = (int(t_.group(1).replace(",", "")) * 1000
                         + (int(t_.group(2)) * 10 ** (3 - len(t_.group(2)))
                            if t_.group(2) else 0))
                else:
                    v = int(raw.replace(",", ""))
                o.setdefault(str(v), set()).add(raw)
        return o
    hit, scr_c, scr_p, nar_c, nar_p = [], set(), set(), set(), set()
    for cid, spec in SPEC.items():
        on = {n for s in strs(spec) for n in NUM.findall(s)}
        sd = {n for s in say.get(cid, []) for n in NUM.findall(s)}
        for bag, cs, ps in ((on, scr_c, scr_p), (sd, nar_c, nar_p)):
            for n in bag:
                (cs if "," in n else ps).add(n.replace(",", ""))
        con, csd = canon(strs(spec)), canon(say.get(cid, []))
        for v in set(con) & set(csd):
            if int(v) < 1000:
                continue
            forms = con[v] | csd[v]
            if len(forms) > 1:
                hit.append((cid, v, " / ".join(sorted(con[v])),
                            " / ".join(sorted(csd[v]))))
    print(f"同じカットで、画面と字幕の数字の形が違う: {len(hit)}件")
    for cid, v, a, b in sorted(hit):
        print(f"  {cid}  {v:>7} … 画面「{a}」／ 字幕「{b}」")
    print(f"\n画面の4桁以上: カンマ有 {sorted(n for n in scr_c if len(n) >= 4)}")
    print(f"            カンマ無 {sorted(n for n in scr_p if len(n) >= 4)}")
    print(f"字幕の4桁以上: カンマ有 {sorted(n for n in nar_c if len(n) >= 4)}")
    print(f"            カンマ無 {sorted(n for n in nar_p if len(n) >= 4)}")


def era():
    """副題が名乗る年 と、出典行の撮影年 が食い違っていないか。

    副題は**その絵の説明**なので、絵の撮影年と違う年を名乗ったら画面が自分と矛盾する。
    ⚠️ ひかえの静止画は手元に無いので `credit_of` が別の枝に落ちる。
      ここで見るのは **年の数字だけ**なので、どちらの枝でも同じ年が出る。
    陽性対照: c201（副題「南行き右車線の閉鎖　2024年3月25日」対 出典「2005年6月30日」）
    """
    import re as _re
    Y = _re.compile(r"(19[0-9]{2}|20[0-9]{2})年")
    hit = []
    for cid, spec in SPEC.items():
        if "photo" not in spec:
            continue
        sub = str(spec.get("s", ""))
        ys = set(Y.findall(sub))
        if not ys:
            continue
        try:
            cr = S.credit_of(cid, spec)
        except Exception:                                # noqa: BLE001
            continue
        cy = set(Y.findall(cr or ""))
        if cy and not (ys & cy):
            hit.append((cid, sub, sorted(ys), sorted(cy)))
    print(f"副題の年と、出典の年が食い違うカット: {len(hit)}")
    for cid, sub, a, b in sorted(hit):
        print(f"  🔴 {cid}  副題「{sub}」= {'/'.join(a)}年 ／ 出典 = {'/'.join(b)}年")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "credit"
    {"credit": credits, "para": para, "num": num, "era": era}[which]()


