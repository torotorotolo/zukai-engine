# -*- coding: utf-8 -*-
"""音素の網（再発防止策1の試作）── 送信文の読みと、合成した音の音素を突き合わせる（API 不使用・2026-09-24）。

  python qa_out/phon_check.py ep13 [--top 40] [--ids c101,c203-2]
  python qa_out/phon_check.py ep12r04 --pos c311-1,c409-2,…    … 陽性対照を捕まえるか・陰性でどれだけ鳴るか

入力（git の外）: out/phon/<tag>_lp.npz・_g2p.json（qa_out/phon_asr_modal.py）・_texts.json・_wav16.npz（qa_out/phon_prep.py）
出力: out/phon/<tag>_check.tsv（全行）
物差し（3つ）:
  ① 差分＝音から自由に起こした音素列（CTC の貪欲デコード）と、送信文の読み（pyopenjtalk）の食い違い
  ② GOP＝送信文の読みを音に無理に当てた（CTC 強制整列）ときの「その音素の対数確率 − その枠の最大」の最良値。
     0 に近いほど音がその読みを支持する。語の GOP＝語の中でいちばん悪い音素
  ③ 間＝行の中の無音（SIL_DB 未満が SIL_MIN 秒以上）のうち、句読点の無い所にあるもの（空白＝辞書の半角空白は別に印）
⚠️ 物差しの正しさは陽性対照（12本目 r04 の試写の指摘）で測ってから使う（再発防止策1）。読み（pyopenjtalk）も誤る＝最後は人が読む。
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "out" / "phon"
FR = 0.02                  # HuBERT の1枠＝20ms（16kHz で 320サンプル）
PUNCT = set("、。，．？！?!…「」『』（）()・：:")
SIL_DB = -40.0             # 無音とみなす RMS（dBFS）
SIL_MIN = 0.12             # これ以上続く無音を「間」とみなす（秒）
PAD = 8000                 # phon_asr_modal.PAD と同じ（前後 0.5秒の無音）。音の枠をモデルの枠にそろえるため同じだけ足す
VOW = set("aiueo")


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def nph(p):
    return p.lower() if p in ("I", "U") else p


def expected(tokens):
    """[[表層, 読み, "音素 …"]] → 音素列 E・各音素の語番号・句読点の位置・空白の位置（音素の境目の番号）"""
    E, tok, punct, space = [], [], set(), set()
    for i, (surf, pron, ph) in enumerate(tokens):
        phs = [nph(p) for p in ph.split() if p not in ("pau", "sil")]
        if not phs:
            if surf.strip() == "":
                space.add(len(E))
            elif any(c in PUNCT for c in surf):
                punct.add(len(E))
            continue
        for p in phs:
            E.append(p)
            tok.append(i)
    return E, tok, punct, space


def greedy(lp, id2, blank):
    ids = lp.argmax(1)
    R, Rf, prev = [], [], -1
    for t, i in enumerate(ids):
        i = int(i)
        if i != prev and i != blank:
            s = id2.get(i, "?")
            if s not in ("pau", "sil", "SOS", "EOS", "UNK", "PAD", "?"):
                R.append(nph(s))
                Rf.append(t)
        prev = i
    return R, Rf


def lev_align(a, b):
    n, m = len(a), len(b)
    D = np.zeros((n + 1, m + 1), dtype=np.int32)
    D[:, 0] = np.arange(n + 1)
    D[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        ai, row, up = a[i - 1], D[i], D[i - 1]
        for j in range(1, m + 1):
            row[j] = min(up[j] + 1, row[j - 1] + 1, up[j - 1] + (ai != b[j - 1]))
    ops, i, j = [], n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i, j] == D[i - 1, j - 1] + (a[i - 1] != b[j - 1]):
            ops.append(("=" if a[i - 1] == b[j - 1] else "s", i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i > 0 and D[i, j] == D[i - 1, j] + 1:
            ops.append(("d", i - 1, None))
            i -= 1
        else:
            ops.append(("i", None, j - 1))
            j -= 1
    return int(D[n, m]), ops[::-1]


def kind_of(cur, E, R):
    """差分の種類: 長音（同じ母音の足し引きだけ）／促音（cl の足し引きだけ）／音（それ以外＝読みが違う疑い）"""
    only_len, only_cl = True, True
    for op, e, r in cur:
        if op == "s":
            return "音"
        p = E[e] if op == "d" else R[r]
        seq, k = (E, e) if op == "d" else (R, r)
        near = {seq[k - 1] if k > 0 else None, seq[k + 1] if k + 1 < len(seq) else None}
        if not (p in VOW and p in near):
            only_len = False
        if p != "cl":
            only_cl = False
    return "長音" if only_len else ("促音" if only_cl else "音")


def hunks(E, R, ops, tok):
    out, cur, e_prev = [], [], -1
    for op in ops + [("=", None, None)]:
        if op[0] != "=":
            cur.append(op)
            continue
        if cur:
            es = [o[1] for o in cur if o[1] is not None]
            rs = [o[2] for o in cur if o[2] is not None]
            e0 = es[0] if es else e_prev + 1
            e1 = es[-1] + 1 if es else e_prev + 1
            tks = sorted({tok[e] for e in es}) if es else [tok[min(max(e_prev, 0), len(tok) - 1)]] if tok else []
            pos = "頭" if e0 <= 1 else ("尾" if e1 >= len(E) - 1 else "")
            out.append({"e0": e0, "e1": e1, "exp": "".join(E[e0:e1]),
                        "rec": "".join(R[rs[0]:rs[-1] + 1]) if rs else "", "tok": tks, "pos": pos,
                        "kind": kind_of(cur, E, R)})
            cur = []
        if op[1] is not None:
            e_prev = op[1]
    return out


def ctc_align(lp, lab, blank):
    """CTC 強制整列（ビタビ）。各枠の状態（偶数＝空白・奇数＝ラベル 2j+1）を返す。整列できなければ None。"""
    T, L = lp.shape[0], len(lab)
    S = 2 * L + 1
    ext = np.full(S, blank, dtype=np.int64)
    ext[1::2] = lab
    NEG = -1e9
    skip = np.zeros(S, dtype=bool)
    skip[2:] = (ext[2:] != blank) & (ext[2:] != ext[:-2])
    dp = np.full(S, NEG, dtype=np.float64)
    dp[0] = lp[0, blank]
    if S > 1:
        dp[1] = lp[0, ext[1]]
    bp = np.zeros((T, S), dtype=np.int8)
    for t in range(1, T):
        c1 = np.concatenate(([NEG], dp[:-1]))
        c2 = np.where(skip, np.concatenate(([NEG, NEG], dp[:-2])), NEG)
        st = np.stack([dp, c1, c2])
        a = st.argmax(0)
        dp = st[a, np.arange(S)] + lp[t, ext]
        bp[t] = a
    s = S - 2 if S > 1 and dp[S - 2] > dp[S - 1] else S - 1
    if dp[s] <= NEG / 2:
        return None
    path = np.zeros(T, dtype=np.int64)
    for t in range(T - 1, -1, -1):
        path[t] = s
        s -= int(bp[t, s])            # int8 のまま引くと numpy 2 の型規則で 127 を超えてあふれる
    return path


def gop(lp, E, sym, blank):
    lab = np.array([sym[p] for p in E], dtype=np.int64)
    path = ctc_align(lp, lab, blank) if len(E) and len(E) * 1 <= lp.shape[0] else None
    if path is None:
        return None, None
    mx = lp.max(1)
    g = np.full(len(E), -99.0)
    fr = np.zeros(len(E), dtype=np.int64)
    for t, s in enumerate(path):
        if s % 2:
            j = s // 2
            d = float(lp[t, lab[j]] - mx[t])
            if d > g[j]:
                g[j], fr[j] = d, t
    return g, fr


def pauses(wav, fr, E, punct, space):
    """行の中の無音（声の最初と最後の間）→ [(秒, 長さ, 境目の番号, 印)]。印＝句読点/空白/「」（何も無い所）"""
    x = np.concatenate([np.zeros(PAD), wav.astype(np.float64), np.zeros(PAD)])
    n = len(x) // 320
    if n < 3 or fr is None:
        return []
    rms = np.sqrt((x[:n * 320].reshape(n, 320) ** 2).mean(1) + 1e-9)
    db = 20 * np.log10(rms / 32768.0)
    voiced = np.where(db >= SIL_DB)[0]
    if len(voiced) < 2:
        return []
    out, t = [], voiced[0]
    while t < voiced[-1]:
        if db[t] < SIL_DB:
            u = t
            while u < voiced[-1] and db[u] < SIL_DB:
                u += 1
            if (u - t) * FR >= SIL_MIN:
                k = int(np.searchsorted(fr, t))          # 無音より前にある音素の数＝境目の番号
                mark = "句読点" if k in punct else ("空白" if k in space else "")
                out.append((round(t * FR - PAD / 16000, 2), round((u - t) * FR, 2), k, mark))
            t = u
        else:
            t += 1
    return out


def analyse(tag):
    lp_z = np.load(BASE / f"{tag}_lp.npz")
    g = json.loads((BASE / f"{tag}_g2p.json").read_text(encoding="utf-8"))
    tx = json.loads((BASE / f"{tag}_texts.json").read_text(encoding="utf-8"))
    wz = np.load(BASE / f"{tag}_wav16.npz")
    sym, blank = g["vocab"], int(g["blank"])
    id2 = {v: k for k, v in sym.items()}
    rows = []
    for lid in tx:
        lp = lp_z[lid].astype(np.float32)
        toks = g["lines"][lid]["tokens"]
        E, tok, punct, space = expected(toks)
        R, _ = greedy(lp, id2, blank)
        dist, ops = lev_align(E, R)
        hs = hunks(E, R, ops, tok)
        gp, fr = gop(lp, E, sym, blank)
        tg = {}
        if gp is not None:
            for j, v in enumerate(gp):
                tg[tok[j]] = min(tg.get(tok[j], 0.0), float(v))
        ps = pauses(wz[lid], fr, E, punct, space)
        bad = [h for h in hs if h["kind"] == "音"]
        worst = min(tg.items(), key=lambda kv: kv[1]) if tg else (None, 0.0)
        rows.append({"lid": lid, "n": len(E), "per": dist / max(len(E), 1), "hunks": hs, "bad": bad,
                     "tg": tg, "worst": worst, "pauses": ps, "toks": toks, "text": tx[lid]["text"],
                     "sent": tx[lid]["sent"], "E": "".join(E), "R": "".join(R), "aligned": gp is not None,
                     "El": E, "tok": tok, "Rl": R, "ops": ops})
    return rows


def surf(r, ids):
    return "".join(r["toks"][i][0] for i in ids)


def fmt(r, gthr=-3.0):
    parts = [f"{r['lid']}  PER {r['per']:.2f}  GOP最小 {r['worst'][1]:.1f}「{surf(r, [r['worst'][0]]) if r['worst'][0] is not None else ''}」"]
    for h in r["bad"]:
        parts.append(f"    差分{('[' + h['pos'] + ']') if h['pos'] else ''}「{surf(r, h['tok'])}」 {h['exp'] or '∅'} → {h['rec'] or '∅'}")
    low = sorted([(v, i) for i, v in r["tg"].items() if v < gthr])
    if low:
        parts.append("    GOP低: " + "／".join(f"「{r['toks'][i][0]}」{v:.1f}" for v, i in low[:6]))
    odd = [p for p in r["pauses"] if p[3] != "句読点"]
    if odd:
        parts.append("    間: " + "／".join(f"{p[0]:.2f}秒 {p[1]:.2f}s {p[3] or '無印'}" for p in odd))
    parts.append(f"    送信: {r['sent']}")
    return "\n".join(parts)


def score(r):
    return len(r["bad"]) * 2 + max(0.0, -r["worst"][1] - 2.0) + sum(1 for p in r["pauses"] if p[3] != "句読点")


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "ep13"
    rows = analyse(tag)
    with open(BASE / f"{tag}_check.tsv", "w", encoding="utf-8") as f:
        f.write("lid\tscore\tper\tgop_min\tgop_tok\tbad\tlen\tcl\tpauses\tsent\n")
        for r in rows:
            f.write("\t".join([r["lid"], f"{score(r):.2f}", f"{r['per']:.3f}", f"{r['worst'][1]:.2f}",
                               surf(r, [r["worst"][0]]) if r["worst"][0] is not None else "",
                               " | ".join(f"{surf(r, h['tok'])}:{h['exp']}>{h['rec']}{h['pos']}" for h in r["bad"]),
                               str(sum(1 for h in r["hunks"] if h["kind"] == "長音")),
                               str(sum(1 for h in r["hunks"] if h["kind"] == "促音")),
                               " | ".join(f"{p[0]}+{p[1]}{p[3]}" for p in r["pauses"]), r["sent"]]) + "\n")
    na = sum(1 for r in rows if not r["aligned"])
    print(f"■ {tag}: {len(rows)}行（整列できない行 {na}）→ {BASE / (tag + '_check.tsv')}")
    pos = [x for x in (arg("--pos", "") or "").split(",") if x]
    if pos:
        rank = {r["lid"]: k for k, r in enumerate(sorted(rows, key=score, reverse=True), 1)}
        neg = [r for r in rows if r["lid"] not in pos]
        print("\n── 陽性対照（試写で指摘された行）──")
        for r in rows:
            if r["lid"] in pos:
                print(f"[順位 {rank[r['lid']]}/{len(rows)}] " + fmt(r))
        per = np.array([r["per"] for r in neg])
        gm = np.array([r["worst"][1] for r in neg])
        nb = np.array([len(r["bad"]) for r in neg])
        print(f"\n── 陰性（指摘の無い {len(neg)}行）── PER 中央値 {np.median(per):.3f}・90%点 {np.percentile(per, 90):.3f}"
              f"／「音」の差分がある行 {int((nb > 0).sum())}（{(nb > 0).mean():.0%}）"
              f"／GOP最小 中央値 {np.median(gm):.1f}・10%点 {np.percentile(gm, 10):.1f}・<-5 {int((gm < -5).sum())}行・<-8 {int((gm < -8).sum())}行")
        return 0
    ids = [x for x in (arg("--ids", "") or "").split(",") if x]
    if ids:
        for r in rows:
            if any(r["lid"] == i or r["lid"].startswith(i + "-") for i in ids):
                print(fmt(r) + f"\n    読み: {r['E']}\n    音  : {r['R']}")
        return 0
    top = int(arg("--top", "40"))
    for r in sorted(rows, key=score, reverse=True)[:top]:
        print(fmt(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
