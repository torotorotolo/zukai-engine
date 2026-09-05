# -*- coding: utf-8 -*-
r"""el_retake.py — **文字起こしで確かめながら**振り直し、台本と合うテイクだけを採用する（2026-09-05 新設）。

  python tools/el_retake.py --ids c214-1,c210-2          … 最大 4 テイク
  python tools/el_retake.py --ids c214-1 --max 6

なぜ要るか（2026-09-05 ⑤a サーフサイドで実測）:
  eleven_v3 は同じ本文でも**テイクごとに文頭の子音が弱くなる**ことがある。「隙間だった」は7テイク中1回だけ
  聞取が「暇だった」になり、その1回が本番のキャッシュに入っていた。書き方（EL_YOMI）では直らない型なので、
  取り直して、**文字起こしが台本と合うテイクだけ**を採用する。
  ⚠️ 切る前（raw）と切った後（trim）を同じテイクで文字起こしして一致することを確かめたので、原因は _trim ではない。
  ⚠️ v3 の出力は行の6割で声が 0ms から始まる（先頭に無音が無い）。これ自体は欠けの証拠ではない
     （0ms 始まりの7テイクが全部正しく聞き取れた）。振幅で頭欠けは判定できない＝文字起こしで見る。

合格（＝採用）の条件（どちらも機械）:
  ① check_numbers_heard：台本の数が聞取に全部ある
  ② el_check_heard.check_row：同形異音語・頭欠け・字の欠けの所見が 0
  全テイク落ちたら、所見が最少のテイクを採用して「要耳」に記録（黙って通さない）。
⚠️ 本番のキャッシュを差し替える（採用した1テイクだけ）。差し替えた行は `el_build.py --dry --cuts <cid>` で wav と json に反映すること。
出力: audio/el_qa/<SLUG>_retake_gate.tsv（行 / テイク数 / 判定 / 各テイクの聞取 / 本文）。el_yomi.tsv の該当行も更新する。
"""
import difflib
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_tts                                            # noqa: E402
import el_script as ES                                   # noqa: E402
from el_check_yomi import stt, norm, load_tsv            # noqa: E402
from el_check_heard import check_row                     # noqa: E402
from el_ledger import numbers_missing                    # noqa: E402


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


# 文頭に足す無音のための接頭辞。2026-09-05 実測（「門を載せている…」9テイク）：
#   接頭辞なし＝先頭の無音 0〜20ms が7/7 → 「門」が7回とも別の語に聞こえた
#   「　、」（全角空白＋読点）＝先頭に 70ms の無音が 2/3 → その2回は「門」と聞こえた
#   <break time> は v3 で効かず（0ms が3/3）、previous_text は v3 未対応（HTTP 400 unsupported_model）
# 足した分は無音なので el_tts._trim が切る。字幕（台本）は変えない。--noprefix で外せる。
PREFIX = "　、"


def judge(text, heard):
    flags = [f"{k}:{w}" for k, w in check_row(text, heard)]
    miss = numbers_missing(text, heard)
    if miss:
        flags.append("数:" + ",".join(miss))
    return flags


def update_yomi_tsv(lid, text, heard, sent):
    p = ES.qa_path("el_yomi.tsv")
    d = load_tsv(p)
    r = difflib.SequenceMatcher(None, norm(text), norm(heard)).ratio()
    d[lid] = (text, heard, r, sent)
    order = [l.lid for l in ES.lines()]
    p.write_text("場面\t一致率\t送った文\t聞こえた文\t送信文\n" +
                 "\n".join(f"{i}\t{d[i][2]:.3f}\t{d[i][0]}\t{d[i][1]}\t{d[i][3]}" for i in order if i in d) + "\n",
                 encoding="utf-8")


def main():
    ids = ES.resolve_ids(arg("--ids"))
    mx = int(arg("--max", "4"))
    prefix = "" if "--noprefix" in sys.argv else PREFIX
    if not ids:
        print(__doc__)
        return 2
    by_id = ES.by_id()
    out = ES.qa_path("retake_gate.tsv")
    old = {l.split("\t")[0]: l for l in out.read_text(encoding="utf-8").splitlines()[1:]} if out.exists() else {}
    unsure = 0
    for lid in ids:
        ln = by_id[lid]
        sent = ES.el_text(ln.text)
        cache = ES.cache_path(sent)
        takes = []           # (pcm, heard, flags)
        for t in range(1, mx + 1):
            pcm = el_tts.synth(sent, lid, slug=ES.SLUG, settings=ES.SETTINGS, refresh=True,
                               send_text=(prefix + sent) if prefix else None)
            heard = stt(pcm)
            flags = judge(ln.text, heard)
            takes.append((pcm, heard, flags))
            print(f"  {lid} take{t}: {'✓' if not flags else '／'.join(flags)}  {heard[:44]}", flush=True)
            if not flags:
                break
        best = min(range(len(takes)), key=lambda i: len(takes[i][2]))
        pcm, heard, flags = takes[best]
        if best != len(takes) - 1:              # 採用テイクをキャッシュに戻す（最後のテイクが書かれている）
            cache.write_bytes(pcm)
            meta = cache.with_suffix(".json")
            if meta.exists():
                m = json.loads(meta.read_text(encoding="utf-8"))
                m["sec"] = round(len(pcm) / 2 / el_tts.SR, 3)
                m["note"] = f"el_retake: take{best+1}/{len(takes)} を採用"
                meta.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
        verdict = "採用（文字起こしが台本と合う）" if not flags else "要耳（全テイク落ち・所見最少を採用）"
        if flags:
            unsure += 1
        update_yomi_tsv(lid, ln.text, heard, sent)
        old[lid] = f"{lid}\t{len(takes)}\t{verdict}\t" + " || ".join(f"take{i+1}: {h}" for i, (_, h, _) in enumerate(takes)) + f"\t{ln.text}"
        print(f"{lid}: {len(takes)}テイク → {verdict}")
    order = [l.lid for l in ES.lines()]
    out.write_text("行\tテイク数\t判定\t各テイクの聞取\t本文\n" + "\n".join(old[i] for i in order if i in old) + "\n",
                   encoding="utf-8")
    print(f"\n{len(ids)}行 → 要耳 {unsure} -> {out}")
    print("⚠️ 差し替えた行のカットは `python tools/el_build.py --dry --cuts <cid>` で wav と json に反映すること")
    return 1 if unsure else 0


if __name__ == "__main__":
    sys.exit(main())
