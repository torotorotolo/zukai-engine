# -*- coding: utf-8 -*-
"""カットごとの「読む負荷」を測る（2026-08-01 追加）。

■ なぜ `check_echo.py` と別に要るか
  カズヤくんの試写指摘（2026-08-01）:
  **「画面上の情報量が多いのに画面の切り替えが早く理解が追い付かない」**

  `check_echo` が見ているのは「図がナレーションの**複写**か」で、しかも
  **見出し（t）と副題（s）は「話題を出す場所だから寄って当然」として、
  丸ごと同一のときしか咎めない**。だから `pr10` の副題
  「事故から2年　どちらも2025年の最終報告書」は素通りした。
  ナレーションは「2025年、2つの最終報告書が出た」「事故から2年たって」なので、
  **言い換えではあっても、視聴者にとっては同じ情報を耳と目で二度処理させられている。**

  つまり複写か否かは問題ではない。**総量と、そのうちの重複量**が問題。

■ 測るもの（すべて「実際に画面に出る <text>」から）
  字数     … そのカットで読ませる文字の総数
  重複     … ナレーションと 4字以上つながって一致する部分が覆う文字数
  字/秒    … 字数 ÷ カット尺。**読み切れるかの指標**
  削れる   … 重複ぶん。ここを削っても図が持つ情報（数値・関係・出どころ）は減らない

  ⚠️ 重複の測り方は **4字以上の連続一致**。`check_echo` の教訓どおり
     飛び飛びの部分列では測らない（日本語は助詞と常用漢字が共通で誤検出しかしない）。
     ただし 12字では言い換えを取り逃がすので、**節でなく語の長さ**で切る。

■ 使い方
    python tools/check_load.py                … 重い順に出す
    python tools/check_load.py --only=pr      … 章をしぼる
    python tools/check_load.py --detail=pr10  … そのカットの内訳を全部出す
    python tools/check_load.py --csv          … 表として出す

🔴 これは**目安であって合否ではない**。どれを削るかは中身を見て決める。
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S

TEXT = re.compile(r'<text\s[^>]*>([^<]*)</text>')
UNESC = {"&amp;": "&", "&lt;": "<", "&gt;": ">"}
NGRAM = 4          # 一致と見なす最短の連続長。語の長さで切る
DROP = re.compile(r"[、。，．\s「」『』（）()【】・…　]")


def unesc(t):
    for k, v in UNESC.items():
        t = t.replace(k, v)
    return t


def norm(s):
    return DROP.sub("", str(s))


def covered(fig, narr):
    """fig のうち、narr と NGRAM 字以上つながって一致する文字の個数。

    位置を集合で持つので、同じ場所を二重に数えない。
    """
    if len(fig) < NGRAM or not narr:
        return 0
    hit = set()
    for i in range(len(fig) - NGRAM + 1):
        # i から始まる最長一致を伸ばす
        j = NGRAM
        while i + j <= len(fig) and fig[i:i + j] in narr:
            j += 1
        if j > NGRAM:
            hit.update(range(i, i + j - 1))
    return len(hit)


def collect():
    """カット → [(レイヤー名, 画面に出る文字列)]。実写カットの見出しも拾える。"""
    jobs, _ = S.build_layers(allow_missing=True)
    by = defaultdict(list)
    for k, svg in jobs.items():
        cid = k.rsplit("_", 1)[0]
        for m in TEXT.finditer(svg):
            t = unesc(m.group(1)).strip()
            if t:
                by[cid].append((k, t))
    return by


def measure(only=None):
    by = collect()
    secs = dict(S.CUTS)
    rows = []
    for cid in S.ORDER:
        if cid not in by or (only and not cid.startswith(only)):
            continue
        narr = norm("".join(r["text"] for r in S.SUBS.get(cid, [])))
        items = []
        for layer, t in by[cid]:
            n = norm(t)
            if not n:
                continue
            items.append((layer, t, len(n), covered(n, narr)))
        chars = sum(x[2] for x in items)
        dup = sum(x[3] for x in items)
        sec = secs[cid]
        rows.append({"cid": cid, "sec": sec, "chars": chars, "dup": dup,
                     "cps": chars / sec if sec else 0,
                     "ratio": dup / chars if chars else 0, "items": items,
                     "narr": len(narr)})
    return rows


def main():
    only = next((a.split("=")[1] for a in sys.argv if a.startswith("--only=")), None)
    detail = next((a.split("=")[1] for a in sys.argv if a.startswith("--detail=")), None)
    rows = measure(only)
    if detail:
        r = next((x for x in rows if x["cid"] == detail), None)
        if not r:
            print(f"🔴 {detail} が無い")
            return 1
        print(f"■ {r['cid']}  尺 {r['sec']:.1f}秒 ／ 図 {r['chars']}字"
              f"（うち重複 {r['dup']}字 = {r['ratio']:.0%}）／ 字幕 {r['narr']}字")
        print(f"  ナレーション: {' / '.join(x['text'] for x in S.SUBS.get(detail, []))}\n")
        print(f"  {'重複':>4}{'字数':>5}  レイヤー / 画面に出る文字")
        for layer, t, ln, cv in sorted(r["items"], key=lambda x: -x[3]):
            mark = "🔴" if cv >= 4 else "  "
            print(f"{mark}{cv:>4}{ln:>5}  {layer:<14}「{t}」")
        return 0

    if "--csv" in sys.argv:
        print("cid,sec,chars,dup,ratio,cps")
        for r in sorted(rows, key=lambda x: -x["dup"]):
            print(f"{r['cid']},{r['sec']:.2f},{r['chars']},{r['dup']},"
                  f"{r['ratio']:.3f},{r['cps']:.2f}")
        return 0

    tot_c = sum(r["chars"] for r in rows)
    tot_d = sum(r["dup"] for r in rows)
    print(f"■ {len(rows)}カット ／ 図の総字数 {tot_c:,}字 ／ "
          f"うちナレーションと重複 {tot_d:,}字（{tot_d / max(tot_c,1):.0%}）\n")

    cps = sorted(r["cps"] for r in rows)
    n = len(cps)
    print(f"字/秒  中央 {cps[n//2]:.2f} ／ 上位1割 {cps[-max(1,n//10)]:.2f} "
          f"／ 最大 {cps[-1]:.2f}\n")

    print("── 削れる字数が多い順（重複＝耳で聞いている情報） ──")
    print(f"{'カット':<8}{'尺':>6}{'字数':>6}{'重複':>6}{'割合':>6}{'字/秒':>7}")
    for r in sorted(rows, key=lambda x: -x["dup"])[:25]:
        print(f"{r['cid']:<8}{r['sec']:>6.1f}{r['chars']:>6}{r['dup']:>6}"
              f"{r['ratio']:>5.0%}{r['cps']:>7.2f}")

    print("\n── 字/秒 が高い順（重複が無くても読み切れない） ──")
    print(f"{'カット':<8}{'尺':>6}{'字数':>6}{'重複':>6}{'割合':>6}{'字/秒':>7}")
    for r in sorted(rows, key=lambda x: -x["cps"])[:15]:
        print(f"{r['cid']:<8}{r['sec']:>6.1f}{r['chars']:>6}{r['dup']:>6}"
              f"{r['ratio']:>5.0%}{r['cps']:>7.2f}")
    print("\n内訳は --detail=カットID で出る。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
