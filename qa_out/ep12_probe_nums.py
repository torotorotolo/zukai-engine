# -*- coding: utf-8 -*-
"""12本目⑤a：数の読みの別案を `el_probe_words --text` で鳴らして聞き取る（2026-09-23）。

  python qa_out/ep12_probe_nums.py        … 下の CAND を全部（1行ずつ el_probe_words を呼ぶ）

🔴 なぜ el_ab_yomi でないか: el_ab_yomi は鍵を**台本の元の字**で照合する＝EL_YOMI でかなに変えた所
   （「ろっキロ」など）は「台本に当たりません」で試せない（9本目の記憶どおり・⑤aで実際に19件はじかれた）。
⭐ el_probe_words は候補の送信文をそのまま合成し、**送信文を鍵にキャッシュへ置く**
   ＝あとで EL_YOMI をこの送信文になるよう直せば、焼き直しは 0クレジット。
出力: audio/el_qa/probe_nums_ep12.log（全文）と、画面に「行・案・聞取」の要約
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES  # noqa: E402

# (行ID, いまの送信文の中の句, 別案)
CAND = [
    ("c110-1", "ろっキロ", "ろくキロ"),
    ("c414-2", "ろっキロ", "ろくキロ"),
    ("c422-2", "ろっキロ", "ろくキロ"),
    ("c915-2", "ろっキロ", "ろくキロ"),
    ("c108-2", "住民 にひゃくさんじゅうきゅうにん", "住民二百三十九人"),
    ("c721-2", "住民 にひゃくさんじゅうきゅうにん", "住民二百三十九人"),
    ("c402-3", "アメリカ兵 にじゅうはちにん", "アメリカ兵二十八人"),
    ("c701-2", "アメリカ兵 にじゅうはちにん", "アメリカ兵二十八人"),
    ("c401-3", "縦 にひゃくななじゅうはちキロ", "縦二百七十八キロ"),
    ("c112-3", "標準時で にがつ にじゅうはちにち", "標準時で二月二十八日"),
    ("c512-1", "さんじゅっぷんご", "さんじっぷんご"),
    ("c512-1", "さんじゅっぷんご", "三十分後"),
    ("c804-1", "さんがつの下旬", "三月の下旬"),
    ("c623-1", "なな、ようかたつと", "なな、ようか たつと"),
    ("c623-1", "なな、ようかたつと", "七、八日たつと"),
    ("c819-3", "ななおく にせんまんえん", "ななおくにせんまんえん"),
    ("c819-3", "ななおく にせんまんえん", "七億二千万円"),
    ("c708-1", "いっセンチ", "いっせんち"),
    ("c708-1", "いっセンチ", "一センチ"),
]
LOG = ROOT / "audio" / "el_qa" / "probe_nums_ep12.log"


def main():
    text = {l.lid: l.text for l in ES.lines()}
    with LOG.open("a", encoding="utf-8") as log:
        for lid, old, new in CAND:
            sent = ES.el_text(text[lid])
            if old not in sent:
                print(f"🔴 {lid}: 送信文に「{old}」が無い＝止める（送信文: {sent}）")
                return 1
            cand = sent.replace(old, new)
            p = subprocess.run([sys.executable, "tools/el_probe_words.py", ES.SLUG, "--ids", lid, "--text", cand],
                               cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
            out = p.stdout + p.stderr
            log.write(f"\n##### {lid} 「{old}」→「{new}」\n{out}")
            log.flush()
            m = re.findall(r"聞取: (.+)", out)
            print(f"{lid:7s} {new:18s} → {m[-1].strip() if m else f'?（exit {p.returncode}）'}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
