# -*- coding: utf-8 -*-
r"""check_listener.py — 「最小限の聞き役」の門番（2026-09-25・14本目⑤a 新設・ルール §4-15）。

  python tools/check_listener.py              … 門番（E があれば exit 1）
  python tools/check_listener.py --list       … 聞き役の行を秒つきで全部出す
  python tools/check_listener.py --selftest   … 答えの分かっている入力で検算

■ なぜ要るか
  14本目から、1人の語りに聞き役の一言を差す（ルール §4-15・カズヤくん決定 09-25）。数の決まり
  （行の10〜15%・1分に1.5〜2回・空きは最長90秒・質問5割／まとめ2〜3割／反応2割まで・聞き役に数字を言わせない）は
  ④'の `ref/ep14/v2_build/mech.py` §7 が**数えるだけ**だった＝⑤以降に行を直すと黙って崩れる
  （[[feedback-rules-need-gates]]）。15本目以降も同じ規則なので tools/ に置く。

■ 重さ
  E（止める）＝聞き役の行に数字／聞き役どうしの空きが90秒超／roles.tsv と台本の食い違い（表に無い行・台本に無い行）／
              キャラ語尾（〜ぜ・〜わ・〜かしら）／聞き役の行があるのに roles.tsv が無い
  W（見る）  ＝行の割合 10〜15% の外／1分あたり 1.5〜2回 の外／最初の1問が 15〜45秒 の外／役割の内訳が目安の外／
              「まとめ」のすぐあとの語りが「そう」で受けていない（§4-15 ⚠️）
  ⚠️ 割合と回数は目安＝音の長さで少し動く。止めると鳴りすぎて本物が埋もれる（[[feedback-gates-blind-spot-is-the-scan-direction]]）

■ 秒
  audio/narration.json が**この台本の音**なら実測（カットの尺＋字幕の t）。違えば check_script の式（③と同じ）。
  どちらで出したかを必ず表に出す。
■ 対象外
  聞き役の行が1つも無く roles.tsv も無い回（13本目まで）は「対象外」で exit 0。
"""
import collections
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import speaker  # noqa: E402

RATIO = (0.10, 0.15)
PER_MIN = (1.5, 2.0)
FIRST = (15.0, 45.0)
MAX_GAP = 90.0
ROLE_TARGET = {"質問": (0.0, 0.60), "まとめ": (0.20, 0.30), "反応": (0.0, 0.20)}   # 質問は「5割」＝上だけ緩めに見る
NUM_RE = re.compile(r"[0-9０-９一二三四五六七八九十百千万]")
CHARA_RE = re.compile(r"(?:ぜ|わ|かしら)[。？！?!]?$")


def load_roles(slug):
    p = ROOT / "ref" / slug / "v2_build" / "roles.tsv"
    if not p.exists():
        return None, p
    out = {}
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.strip() and not ln.startswith("#"):
            c, r, tx = ln.split("\t")
            out[(c.strip(), tx.strip())] = r.strip()
    return out, p


def timeline(script, cs):
    """[(cid, 行番号, 話者, 文, 開始秒)] と 全体の秒・出どころ。cs＝check_script（定数と式）。"""
    cuts = [(cid, "", ls) for cid, ls in script]
    subs, src = None, "check_script の式（音がまだ無い）"
    p = ROOT / "audio" / "narration.json"
    if p.exists():
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            s = d.get("subtitles", {})
            same = all(cid in s and [x.get("text") for x in s[cid]] == [speaker.bare(t) for t in ls]
                       for cid, ls in script)
            if same:
                subs, src = s, "narration.json の実測"
            else:
                src = "check_script の式（narration.json は別の台本の音）"
        except Exception as e:                       # noqa: BLE001
            src = f"check_script の式（narration.json を読めない {type(e).__name__}）"
    if subs is None:
        cs.use_measured_cps([(cid, pic, [speaker.bare(t) for t in ls]) for cid, pic, ls in cuts])
    rows, t, prev = [], 0.0, None
    for cid, ls in script:
        key = cid[:2] if cs.CHAPTER_CUT_RE.match(cid) else None
        if key is not None:
            if prev is not None and key != prev:
                t += cs.CARD_SEC
            prev = key
        t += cs.LEAD
        if subs is not None:
            for i, (x, raw) in enumerate(zip(subs[cid], ls), 1):
                rows.append((cid, i, speaker.split(raw)[0], speaker.bare(raw), t + float(x["t"])))
            last = subs[cid][-1]
            t += float(last["t"]) + float(last["d"])
        else:
            for i, raw in enumerate(ls, 1):
                if i > 1:
                    t += cs.GAP
                rows.append((cid, i, speaker.split(raw)[0], speaker.bare(raw), t))
                t += len(speaker.bare(raw)) / cs.CPS
        t += cs.TAIL + (cs.TAIL_EXTRA_QUOTE if any(cs.STAR_RE.match(l) for l in ls) else 0.0)
    return rows, t, src


def judge(rows, total, roles):
    """rows＝timeline の行。戻り値＝(E, W, 数の辞書)。"""
    E, W = [], []
    q = [r for r in rows if r[2] == speaker.WHO_Q]
    info = {"lines": len(rows), "q": len(q)}
    if not q:
        return E, W, info
    ratio = len(q) / len(rows)
    per_min = len(q) / (total / 60.0)
    times = [r[4] for r in q]
    inner = [b - a for a, b in zip(times, times[1:])]
    info.update(ratio=ratio, per_min=per_min, first=times[0],
                max_gap=max(inner) if inner else 0.0, tail=total - times[-1])
    for cid, i, _, b, _ in q:
        if NUM_RE.search(b):
            E.append(f"{cid}-{i} 聞き役が数字を言っている（§4-15）: {b}")
        if CHARA_RE.search(b):
            E.append(f"{cid}-{i} 聞き役にキャラ語尾（〜ぜ・〜わ・〜かしら）: {b}")
    for k, g in enumerate(inner):
        if g > MAX_GAP:
            E.append(f"聞き役の空きが {g:.0f}秒（{q[k][0]} → {q[k + 1][0]}・上限 {MAX_GAP:.0f}秒）")
    if roles is None:
        E.append("聞き役の行があるのに roles.tsv が無い（役割の正本・ルール §4-15）")
        got = collections.Counter()
    else:
        keys = [(cid, b) for cid, _, _, b, _ in q]
        for cid, b in keys:
            if (cid, b) not in roles:
                E.append(f"{cid} roles.tsv に無い聞き役の行: {b}")
        for (cid, b) in sorted(set(roles) - set(keys)):
            E.append(f"{cid} roles.tsv にあって台本に無い行: {b}")
        got = collections.Counter(roles.get(k, "表に無い") for k in keys)
        for role, (lo, hi) in ROLE_TARGET.items():
            share = got[role] / len(q)
            if not lo <= share <= hi:
                W.append(f"役割「{role}」が {100 * share:.0f}%（目安 {100 * lo:.0f}〜{100 * hi:.0f}%）")
        # まとめのすぐあとの語りは「そう」で受ける（先回りを防ぐ）。⚠️ 1行の W にまとめる
        #    （14本目の第2版は11行中7行が「つまり〜？」の確かめの問いで、語りが根拠で答える形＝行ごとに鳴らすと埋もれる）
        idx = {(r[0], r[1]): n for n, r in enumerate(rows)}
        nos, nq = [], 0
        for cid, i, _, b, _ in q:
            if roles.get((cid, b)) == "まとめ":
                nq += 1
                n = idx[(cid, i)]
                nxt = next((r for r in rows[n + 1:] if r[2] != speaker.WHO_Q), None)
                if nxt and not nxt[3].startswith("そう"):
                    nos.append(cid)
        if nos:
            W.append(f"まとめ {nq}行のうち {len(nos)}行は、すぐあとの語りが「そう」で受けていない（{'・'.join(nos)}）")
    info["roles"] = dict(got)
    if not RATIO[0] <= ratio <= RATIO[1]:
        W.append(f"聞き役の行が {100 * ratio:.1f}%（目安 {100 * RATIO[0]:.0f}〜{100 * RATIO[1]:.0f}%）")
    if not PER_MIN[0] <= per_min <= PER_MIN[1]:
        W.append(f"聞き役が1分あたり {per_min:.2f}回（目安 {PER_MIN[0]}〜{PER_MIN[1]}回）")
    if not FIRST[0] <= times[0] <= FIRST[1]:
        W.append(f"最初の聞き役が {times[0]:.1f}秒（目安 {FIRST[0]:.0f}〜{FIRST[1]:.0f}秒）")
    return E, W, info


def run(listing=False):
    import check_script as CS
    import el_script
    import narration
    script = [(cid, ls) for cid, ls in narration.SCRIPT if cid not in el_script.COMMON_TAIL]
    roles, rp = load_roles(el_script.SLUG)
    rows, total, src = timeline(script, CS)
    if not any(r[2] == speaker.WHO_Q for r in rows) and roles is None:
        print(f"聞き役なし（{el_script.SLUG}＝この回は対象外・roles.tsv も無い）")
        return 0
    E, W, info = judge(rows, total, roles)
    print(f"秒の出どころ：{src}／尺 {int(total) // 60}分{int(total) % 60:02d}秒")
    if info["q"]:
        print(f"聞き役 {info['q']}／{info['lines']}行＝{100 * info['ratio']:.1f}%・1分あたり {info['per_min']:.2f}回・"
              f"最初 {info['first']:.1f}秒・最長の空き {info['max_gap']:.0f}秒（最後→終わり {info['tail']:.0f}秒）")
        print(f"役割 {info.get('roles', {})}（{rp.relative_to(ROOT) if roles is not None else 'roles.tsv 無し'}）")
    if listing:
        for cid, i, who, b, t in rows:
            if who == speaker.WHO_Q:
                print(f"  {int(t) // 60:2d}:{t % 60:04.1f} {cid}-{i} {b}")
    for x in E:
        print("🔴 E", x)
    for x in W:
        print("⚠️ W", x)
    print(f"E {len(E)}件 / W {len(W)}件")
    return 1 if E else 0


def selftest():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %s %-34s 期待 %-10r 実際 %r" % ("OK " if good else "🔴NG", name, want, got))

    def rows_of(spec):
        """spec＝[(秒, 話者, 文)]。カットは1行1カット。"""
        return [(f"c{n + 101}", 1, w, b, t) for n, (t, w, b) in enumerate(spec)]

    base = [(0, None, "語り。"), (20, "q", "船長たちは？"), (30, None, "そう。先に離れた。"),
            (60, "q", "つまり、待てと？"), (70, None, "そう。待てだ。"), (100, "q", "なんで？"), (110, None, "理由はこうだ。")]
    roles = {("c102", "船長たちは？"): "質問", ("c104", "つまり、待てと？"): "まとめ", ("c106", "なんで？"): "質問"}
    E, W, info = judge(rows_of(base), 120.0, roles)
    chk("きれいな見本は E 0", len(E), 0)
    chk("聞き役3行を数える", info["q"], 3)
    def swap(old, new):
        """役割の表の1行を差し替える（元の行を残すと「台本に無い行」の E も出る＝差が2になる）。"""
        r = {k: v for k, v in roles.items() if k != old}
        r[new] = roles[old]
        return r

    bad = list(base)
    bad[1] = (20, "q", "船長たち3人は？")
    chk("🔴聞き役の数字は E", len(judge(rows_of(bad), 120.0, swap(("c102", "船長たちは？"), ("c102", "船長たち3人は？")))[0]), 1)
    gap = [(0, None, "語り。"), (20, "q", "船長たちは？"), (130, "q", "なんで？")]
    chk("🔴空き90秒超は E", len(judge(rows_of(gap), 140.0, {("c102", "船長たちは？"): "質問", ("c103", "なんで？"): "質問"})[0]), 1)
    chk("🔴roles.tsv に無い行は E", len(judge(rows_of(base), 120.0, {k: v for k, v in roles.items() if k[0] != "c106"})[0]), 1)
    chk("🔴roles.tsv が無ければ E", any("roles.tsv が無い" in e for e in judge(rows_of(base), 120.0, None)[0]), True)
    chara = list(base)
    chara[5] = (100, "q", "なんでだぜ？")
    chk("🔴キャラ語尾は E", len(judge(rows_of(chara), 120.0, swap(("c106", "なんで？"), ("c106", "なんでだぜ？")))[0]), 1)
    nosou = list(base)
    nosou[4] = (70, None, "待てだ。")
    chk("まとめのあと「そう」が無ければ W", any("そう" in w for w in judge(rows_of(nosou), 120.0, roles)[1]), True)
    chk("聞き役0行なら何も言わない", judge(rows_of([(0, None, "語り。")]), 10.0, None)[:2], ([], []))
    print("check_listener selftest:", "PASS" if ok else "🔴FAIL")
    return ok


def main():
    if "--selftest" in sys.argv:
        return 0 if selftest() else 1
    return run(listing="--list" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
