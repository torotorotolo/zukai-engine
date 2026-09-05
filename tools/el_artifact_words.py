# -*- coding: utf-8 -*-
r"""el_artifact_words.py — 異音の門番が「要耳（unsure）／本物（real）」と判定した行を、語の時刻で見分ける（2026-09-05 新設）。

  python tools/el_artifact_words.py --ids pr07-1,c426-2
  python tools/el_artifact_words.py --retakes        … audio/el_qa/<SLUG>_el_retakes.tsv の unsure/real を全部

なぜ要るか:
  el_artifacts の物差しは「無音に挟まれた短い大きな塊」。ところが日本語の**促音**（いっ・だっ・かっ）は
  「短い音→無音→音」の形をしているので、同じ形に見える。⑤a サーフサイドでは unsure 12行のうち
  調べた11行が全部 促音か語頭の破裂音（だっ|た・いっかしょ・かっこ・は、決定的）だった。
  Scribe の語ごとの時刻（words[].start/end）で、異音の時刻に重なる語を並べれば、字で判定できる。
  ⚠️ 判定は人（Claude）。「っ」「た」「か行」が重なれば促音＝本物。語が無い（語なし）なら本物の異音の疑い。
出力: 標準出力（台帳には「所見」として写す）
"""
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_script as ES              # noqa: E402
import el_artifacts as ART          # noqa: E402
from el_probe_words import stt_words  # noqa: E402


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    if "--retakes" in sys.argv:
        p = ES.qa_path("el_retakes.tsv")
        rows = [l.split("\t") for l in p.read_text(encoding="utf-8").splitlines()[1:]]
        ids = sorted({r[0] for r in rows if len(r) > 1 and r[1] in ("unsure", "real")},
                     key=[l.lid for l in ES.lines()].index)
    else:
        ids = ES.resolve_ids(arg("--ids"))
    if not ids:
        print(__doc__)
        return 2
    by = ES.by_id()
    for lid in ids:
        ln = by[lid]
        p = ES.cache_path(ES.el_text(ln.text))
        if not p.exists():
            print(f"{lid}: キャッシュ無し")
            continue
        pcm = p.read_bytes()
        items = ART.blips(ART.inspect_struct(pcm))
        text, ws = stt_words(pcm)
        print(f"\n=== {lid} 「{ln.text}」\n  聞取: {text}")
        if not items:
            print("  （いまのテイクに異音の所見なし）")
        for it in items:
            t0, t1 = it["at_ms"] / 1000, (it["at_ms"] + it["ms"]) / 1000
            near = [f"{w['text']}({w['start']:.2f}-{w['end']:.2f})" for w in ws
                    if w["end"] >= t0 - 0.12 and w["start"] <= t1 + 0.12]
            print(f"  ⚠️ {it['kind']} {t0:.2f}-{t1:.2f}s 振幅比{it['ratio']:.1f} → 重なる語: {' '.join(near) or '（語なし）'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
