# -*- coding: utf-8 -*-
r"""el_ledger.py — ⑤a の**行ごとの検査台帳**を audio/el_qa/ の記録から機械で組む（2026-09-05 新設）。

  python tools/el_ledger.py            → audio/el_qa/<SLUG>_ledger.md（全行）＋ 要耳一覧の下書き

列: 行ID／台本／送信（EL_YOMI 後）／聞取／一致率／数の照合／所見（heard_flags・dup・artifacts・take2・ab・retakes）／扱い
  「扱い」は el_qa/<SLUG>_verdicts.tsv（行ID\t扱い\t理由。人＝Claude が書く）から差し込む。無ければ空欄＝**未判定**として数える。
⚠️ 台帳は「全部OK」を言うための表ではない。未判定が0で、疑いの行に扱いが付いていることを確かめる表。
"""
import csv
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_script as ES                                  # noqa: E402
# 🔴 2026-09-23（12本目⑤a）: 数の照合（カンマ・万億の合成・漢数字の小数）は check_numbers_heard に1本化した。
#    ここに独自の版（_expand_kanji_units）を持っていたため、10本目に塞いだ「7万1,136」「228億」の穴が
#    check_numbers_heard 側に効かず、12本目で「1500万トン」の15行が鳴りっぱなしになった。
#    numbers_missing は el_retake・qa_out/ep10_* が `from el_ledger import numbers_missing` で使うので名前は残す。
from check_numbers_heard import numbers_missing, _selftest as _numbers_selftest  # noqa: E402


def _tsv(path, key=0):
    if not path.exists():
        return {}
    rows = list(csv.reader(path.open(encoding="utf-8"), delimiter="\t"))
    out = {}
    for r in rows[1:]:
        if r:
            out.setdefault(r[key], []).append(r)
    return out


def main():
    _numbers_selftest()          # 🔴 数の物差しが壊れていたら、台帳の「数」の列を信用できないので止める
    yomi = _tsv(ES.qa_path("el_yomi.tsv"))
    flags = _tsv(ES.qa_path("heard_flags.tsv"))
    arts = _tsv(ES.qa_path("el_artifacts.tsv"))
    take2 = _tsv(ES.qa_path("take2.tsv"))
    ab = _tsv(ES.qa_path("yomi_ab.tsv"))
    retakes = _tsv(ES.qa_path("el_retakes.tsv"))
    # 🔴 2026-09-16（9本目）: el_reading_diff の「読みが違う」も疑いに入れる。
    #    8本目 c212-2「離陸から」→『陸から』は **2周とも崩れていたのに一致率 91.9%** で、
    #    「90%未満か所見あり」の網の外にいた（頭の1字が落ちても残りが全部合うと率は高い）。
    #    8本目はこの足し算を qa_out/ep8_verdicts.py（その回専用）にだけ入れたので、次の回に効いていなかった
    #    （feedback-gates-blind-spot-is-the-scan-direction）。
    #    ⚠️ reading_diff.tsv が無い回は足せない＝**黙って0で埋めず、台帳の頭に「無い」と書く**
    rdiff = _tsv(ES.qa_path("reading_diff.tsv"))
    verdicts = {r[0]: r for r in sum(_tsv(ES.qa_path("verdicts.tsv")).values(), [])}
    dup_hits = set()
    try:
        from el_check_dup import find_dup
        for lid, rs in yomi.items():
            if find_dup(rs[-1][3]):
                dup_hits.add(lid)
    except Exception:
        pass

    lines = ES.lines()
    out = ["# ⑤a 検査台帳（機械生成。`python tools/el_ledger.py`）", "",
           f"台本 {len(lines)}行／文字起こし {len(yomi)}行／扱いの記録 {len(verdicts)}行", "",
           "| 行 | 台本 | 送信 | 聞取 | 一致率 | 数 | 所見 | 扱い |", "|---|---|---|---|---:|---|---|---|"]
    n_sus = n_unj = 0
    for ln in lines:
        sent = ES.el_text(ln.text)
        y = yomi.get(ln.lid, [None])[-1]
        heard = y[3] if y else "（未検査）"
        ratio = f"{float(y[1])*100:.0f}%" if y else "—"
        miss = numbers_missing(ln.text, heard) if y else []
        obs = []
        if miss:
            obs.append("数:" + ",".join(miss))
        for f in flags.get(ln.lid, []):
            obs.append(f"{f[1]}:{f[2]}")
        if ln.lid in dup_hits:
            obs.append("重複読み")
        for a in arts.get(ln.lid, []):
            obs.append("異音:" + a[1][:18])
        for t in take2.get(ln.lid, []):
            obs.append("2テイク:" + t[7])
        for a in ab.get(ln.lid, []):
            obs.append(f"A/B:{a[1]}→{a[2]}")
        for r in retakes.get(ln.lid, []):
            if r[1] != "clean":
                obs.append(f"振り直し:{r[1]}")
        for r in rdiff.get(ln.lid, [])[-1:]:
            if len(r) > 1 and r[1] == "読みが違う":
                obs.append("読み:" + (r[2][:24] if len(r) > 2 and r[2] else "違う"))
        v = verdicts.get(ln.lid)
        sus = bool(obs) or (y and float(y[1]) < 0.9)
        if sus:
            n_sus += 1
            if not v:
                n_unj += 1
        verdict = (v[1] + (f"（{v[2]}）" if len(v) > 2 and v[2] else "")) if v else ("**未判定**" if sus else "")
        sent_cell = sent if sent != ln.text else "＝"
        out.append(f"| {ln.lid} | {ln.text} | {sent_cell} | {heard} | {ratio} | {'🔴' if miss else ''} | {'／'.join(obs)} | {verdict} |")
    out.insert(3, f"疑いの行 {n_sus}（一致率90%未満か所見あり・所見には el_reading_diff の「読みが違う」を含む）／うち扱い未判定 **{n_unj}**"
               + ("" if rdiff else "　🔴 reading_diff.tsv が無い＝読みの照合は疑いに入っていない"))
    p = ES.qa_path("ledger.md")
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"台帳 {len(lines)}行 → {p}")
    print(f"文字起こし {len(yomi)}行／疑い {n_sus}／未判定 {n_unj}")

    # ── 要耳一覧（試写パッケージ用）：扱いが「要耳」で始まる行を、本編の秒つきで並べる ──────
    # 本編の秒＝audio/narration.json の durations を LEAD 0.35＋TAIL 0.50（quote は＋2.0）で積んだ見込み。
    # ⚠️ 正確な秒は ⑤b の scene_jiko が決める（章マーカー等が入れば少し動く）。当たりとして使う。
    import json
    jp = ROOT / "audio" / "narration.json"
    d = json.loads(jp.read_text(encoding="utf-8")) if jp.exists() else {}
    # 🔴 2026-09-08: ここは **4本目サーフサイドの決め所IDが直書き**されていた（12件）。
    #    6本目キー橋の決め所 22件と重なるのは c426 / c722 の2件だけ＝残り20カットで
    #    「+2.0秒」が誤って入る／抜けるまま、要耳一覧の頭出しの秒が黙ってずれていた。
    #    台本の md から機械で取る（ES.quote_cuts は数が EXPECT と食い違えば止まる）。
    Q = ES.quote_cuts()
    t, start = 0.0, {}
    for cid, sec in d.get("durations", {}).items():
        start[cid] = t
        t += sec + 0.35 + 0.50 + (2.0 if cid in Q else 0.0)
    rows = []
    for ln in lines:
        v = verdicts.get(ln.lid)
        if not v or not v[1].startswith("要耳"):
            continue
        off = 0.0
        for r in d.get("subtitles", {}).get(ln.cid, []):
            if r["text"] == ln.text:
                off = r["t"]
                break
        s = start.get(ln.cid, 0.0) + 0.35 + off
        rows.append(f"| {ln.lid} | {int(s//60)}:{int(s%60):02d} | {ln.text} | {v[2] if len(v) > 2 else ''} |")
    yp = ES.qa_path("youmimi.md")
    yp.write_text("# 要耳一覧（試写で、この秒だけ注意して聴く）\n\n"
                  f"機械の網（Scribe 照合・数の照合・同形異音語・2テイク合議・A/B・取り直し）で決着しなかった行。{len(rows)}行。\n"
                  "秒は narration.json から積んだ見込み（⑤b で章マーカー等が入ると数秒動く）。\n\n"
                  "| 行 | 本編の秒 | 台本 | 疑いの中身 |\n|---|---:|---|---|\n" + "\n".join(rows) + "\n",
                  encoding="utf-8")
    print(f"要耳一覧 {len(rows)}行 → {yp}")
    return 1 if n_unj else 0


if __name__ == "__main__":
    sys.exit(main())
