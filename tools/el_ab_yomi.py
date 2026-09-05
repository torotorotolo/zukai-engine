# -*- coding: utf-8 -*-
r"""el_ab_yomi.py — 読みの直し候補を「いまの音」と**文字起こしで比べる**（耳の代わり）。

  python tools\el_ab_yomi.py ep008 --plan tools\ep008_yomi_plan.json

plan の形（JSON）:
  [ {"id":"s014", "key":"2006年", "val":"にせんろくねん", "why":"西暦が2004に聞こえる"} , ... ]
    key/val … EL_YOMI に入れる予定の1件。その行に対してだけ当てて候補文を作る

やること:
  ① いまキャッシュにある音を文字起こし（すでに焼いた音・追加費用は STT のみ）
  ② key→val を当てた候補文を合成して文字起こし
  ③ 台本との一致率を before / after で並べる

🔴 これは門番ではありません。**採否を決めるのは一致率だけではない**ので、
   出力を読んで人（Claude）が決めます。ただし「直したのに悪くなった」は機械で捕まります。

⚠️ 一致率が上がっても、**別の語が崩れていないか**必ず聞取の全文を見ること
   （ep005「測り方を直したら同じ行の『定義』が『重力』に化けた」）。
⚠️ key は必ず台本の実文に当たることを確かめる。当たらないキーは黙って素通りします。

出力: out/<slug>_yomi_ab.tsv（場面 / key / val / before一致率 / after一致率 / 両方の聞取）
"""
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_tts                                    # noqa: E402
import el_script as ES                           # noqa: E402  行の列挙・EL_YOMI・キャッシュの場所
from el_check_yomi import stt, norm              # noqa: E402
import difflib                                   # noqa: E402
el_text = ES.el_text


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    slug = ES.SLUG
    plan_path = arg("--plan")
    if not plan_path:
        print(__doc__)
        print("[FATAL] --plan で計画ファイルを指定してください（id は行ID＝c112-2 の形）", file=sys.stderr)
        return 2
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    by_id = ES.by_id()

    out, bad = [], []
    for item in plan:
        sid, key, val = item["id"], item["key"], item["val"]
        ln = by_id.get(sid)
        if ln is None:
            print(f"[FATAL] 無い行ID: {sid}（行ID＝カットID-行番号）", file=sys.stderr)
            return 1
        text = ln.text
        if key not in text:                       # fail closed: 当たらないキーを黙って通さない
            bad.append(f"{sid}: キー「{key}」が台本に当たりません")
            continue
        before_sent = el_text(text)
        after_sent = before_sent.replace(key, val)
        if after_sent == before_sent:
            bad.append(f"{sid}: 置換後が置換前と同じです（key={key}）")
            continue

        cache = ES.cache_path(before_sent)
        if not cache.exists():
            bad.append(f"{sid}: 合成キャッシュがありません")
            continue
        heard_b = stt(cache.read_bytes())
        pcm_a = el_tts.synth(after_sent, sid, slug=slug, settings=ES.SETTINGS)   # 候補側（キャッシュされる）
        heard_a = stt(pcm_a)

        rb = difflib.SequenceMatcher(None, norm(text), norm(heard_b)).ratio()
        ra = difflib.SequenceMatcher(None, norm(text), norm(heard_a)).ratio()
        mark = "⭐良化" if ra > rb + 0.005 else ("▲悪化" if ra < rb - 0.005 else "＝変わらず")
        print(f"\n=== {sid}  「{key}」→「{val}」  {mark}  {rb*100:.1f}% → {ra*100:.1f}% ===")
        print(f"  理由: {item.get('why','')}")
        print(f"  台本  : {text}")
        print(f"  前の聞取: {heard_b}")
        print(f"  後の聞取: {heard_a}")
        out.append((sid, key, val, rb, ra, heard_b, heard_a))

    p = ES.qa_path("yomi_ab.tsv")
    old = p.read_text(encoding="utf-8").splitlines()[1:] if p.exists() else []
    p.write_text("行\tkey\tval\t前\t後\t前の聞取\t後の聞取\n" +
                 "\n".join(old + [f"{a}\t{b}\t{c}\t{d:.3f}\t{e:.3f}\t{f}\t{g}" for a, b, c, d, e, f, g in out]) + "\n",
                 encoding="utf-8")
    print(f"\n{len(out)}件 -> {p.name}")
    if bad:
        print("🔴 試せなかったもの:", file=sys.stderr)
        for b in bad:
            print("   " + b, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
