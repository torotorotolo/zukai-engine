# -*- coding: utf-8 -*-
r"""el_take2.py — 2テイク合議。疑いの行を**同じ送信文でもう1回**合成し、2本の文字起こしを比べる（2026-09-05 新設）。

  python tools/el_take2.py --ids c112-2,c116-1
  python tools/el_take2.py --ids c112       … カットIDなら全行

なぜ要るか:
  1テイクの文字起こしが台本と食い違っても、それが「声の読み」なのか「Scribe の癖」なのか「本文が誘発する崩れ」なのか
  は1本では分からない。同じ送信文で振り直したテイクをもう1本文字起こしして、
    - 2本が**割れる** → 読みが安定していない＝本文が誘発している。書き方を変える候補（EL_YOMI）
    - 2本が**そろって台本と違う** → 毎回そう読む。Scribe の同音別字か、本物の誤読。el_probe_words で秒数を測る
    - 2本が**そろって台本どおり** → 1テイク目の聞取が Scribe の揺れ。直さない
  ⚠️ 2テイク目は audio/el_cache/<SLUG>_take2/ に置く＝**本番のキャッシュには触らない**（採用音は変えない）。
  ⚠️ 費用＝その行の文字数×0.55クレジット（本番と同じ）。疑いの行だけに使う。

出力: audio/el_qa/<SLUG>_take2.tsv（行 / 台本 / 聞取1 / 聞取2 / 一致率1 / 一致率2 / 2本の一致率 / 判定）
"""
import difflib
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_tts                                   # noqa: E402
import el_script as ES                          # noqa: E402
from el_check_yomi import stt, norm, load_tsv   # noqa: E402


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    ids = ES.resolve_ids(arg("--ids"))
    if not ids:
        print(__doc__)
        return 2
    by_id = ES.by_id()
    prev = load_tsv(ES.qa_path("el_yomi.tsv"))          # 1テイク目の聞取があれば STT を節約
    out = ES.qa_path("take2.tsv")
    old = {l.split("\t")[0]: l for l in out.read_text(encoding="utf-8").splitlines()[1:]} if out.exists() else {}
    rows, split = [], 0
    for lid in ids:
        ln = by_id[lid]
        sent = ES.el_text(ln.text)
        c1 = ES.cache_path(sent)
        if not c1.exists():
            print(f"🔴 {lid}: 本番のキャッシュが無い（el_build を先に）")
            return 1
        heard1 = prev[lid][1] if lid in prev and prev[lid][3] == sent else stt(c1.read_bytes())
        pcm2 = el_tts.synth(sent, lid, slug=ES.SLUG + "_take2", settings=ES.SETTINGS)
        heard2 = stt(pcm2)
        r1 = difflib.SequenceMatcher(None, norm(ln.text), norm(heard1)).ratio()
        r2 = difflib.SequenceMatcher(None, norm(ln.text), norm(heard2)).ratio()
        r12 = difflib.SequenceMatcher(None, norm(heard1), norm(heard2)).ratio()
        if norm(heard1) == norm(heard2):
            verdict = "そろう（台本どおり）" if norm(heard1) == norm(ln.text) else "そろう（台本と違う＝毎回そう読む）"
        else:
            verdict = "割れる（本文が誘発の疑い）"
            split += 1
        print(f"\n{lid}  {verdict}  1:{r1*100:.1f}% 2:{r2*100:.1f}% 1↔2:{r12*100:.1f}%")
        print(f"  台本: {ln.text}")
        if sent != ln.text:
            print(f"  送信: {sent}")
        print(f"  聞取1: {heard1}")
        print(f"  聞取2: {heard2}")
        old[lid] = f"{lid}\t{ln.text}\t{heard1}\t{heard2}\t{r1:.3f}\t{r2:.3f}\t{r12:.3f}\t{verdict}"
        rows.append(lid)
    order = [l.lid for l in ES.lines()]
    out.write_text("行\t台本\t聞取1\t聞取2\t一致率1\t一致率2\t1↔2\t判定\n" +
                   "\n".join(old[i] for i in order if i in old) + "\n", encoding="utf-8")
    print(f"\n{len(rows)}行 → 割れた行 {split} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
