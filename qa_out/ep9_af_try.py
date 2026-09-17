# -*- coding: utf-8 -*-
"""9本目 ⑥ 試写の指摘の直し候補を、**送る文ごと**に合成して聞取で比べる（2026-09-17）。

なぜ `el_ab_yomi.py` を使わないか：あちらは「辞書を当てたあとの文」に key→val を重ねる作りで、
**すでにキーが入っている行（pr01-1 など）は候補が作れない**（置換前と同じ、で止まる）。

    python qa_out/ep9_af_try.py <plan.json>
    plan＝[{"id": "pr01-1", "sent": "候補の送る文", "prefix": false}, ...]

- prefix … `el_retake.PREFIX`（「　、」）を API にだけ足す（行頭の音が落ちる型の手当て。字幕は変わらない）
- ⚠️ 課金（合成＋聞取）。候補はキャッシュに入る＝`EL_YOMI` で**同じ送る文**になるようにすれば、
  `el_build.py` は API を叩かず、**ここで聞いたテイクがそのまま入る**
- ⚠️ 聞取（Scribe）は「すべそうろ→滑走路」のように**正しい字に直して書く**ことがある＝合格の証明ではない。
  見るのは「別の語に化けていないか」
"""
import difflib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import el_tts  # noqa: E402
import el_script as ES  # noqa: E402
from el_check_yomi import stt, norm  # noqa: E402
from el_retake import PREFIX  # noqa: E402


def main():
    ES.gate_args(set())                      # 🔴 知らない旗で有料の本番に落ちない
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not files:
        raise SystemExit(__doc__)
    plan = json.loads(Path(files[0]).read_text(encoding="utf-8"))
    by_id = ES.by_id()
    for it in plan:
        ln = by_id.get(it["id"])
        if ln is None:
            raise SystemExit(f"🔴 無い行ID: {it['id']}")
        sent = it["sent"]
        had = ES.cache_path(sent).exists()
        pcm = el_tts.synth(sent, it["id"], slug=ES.SLUG, settings=ES.SETTINGS,
                           send_text=(PREFIX + sent) if it.get("prefix") else None)
        heard = stt(ES.shipped(pcm))
        r = difflib.SequenceMatcher(None, norm(ln.text), norm(heard)).ratio()
        print(f"\n=== {it['id']}{'（キャッシュ）' if had else ''}{'（頭に「　、」）' if it.get('prefix') else ''}  "
              f"{r * 100:.1f}%", flush=True)
        print(f"  台本: {ln.text}\n  送る: {sent}\n  聞取: {heard}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
