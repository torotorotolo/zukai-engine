# -*- coding: utf-8 -*-
"""old_metrics.json（dump_old.py の出力）から、棚卸しの表を Markdown で書き出す。手で写さないため。

    python ref/ep19/old/tables_from_metrics.py      → ref/ep19/old/old_tables.md
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def mmss(t):
    t = round(t, 1)
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:04.1f}"


def main():
    m = json.loads((HERE / "old_metrics.json").read_text(encoding="utf-8"))
    o = ["---\ntitle: 19本目①棚卸し — 旧版（4本目）の数の表（機械）\ncreated: 2026-10-05\n"
         "tags: [project/jiko-kensho, ep19]\n---\n",
         "# 旧版（4本目サーフサイド）の数の表 ── `old_metrics.json` から機械で\n",
         f"> 版 `{m['rev']}`。{m['n_cuts']}カット／{m['n_lines']}行／完成尺 {m['total_mmss']}"
         f"（声 {mmss(m['speech_sec'])}＋構造 {mmss(m['structure_sec'])}）。\n"]

    o.append("## 章\n")
    o.append("| 章 | カット | 本数 | 開始 | 尺 | 行 | 句読点なしの字 | 字/分 | 写真を持つ | 動く映像 | 文字だけ（狭）| 文字だけ（広）| 台本の見込み（コメント） |")
    o.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for c in m["chapters"]:
        cpm = c["chars_nopunct"] / (c["sec"] / 60)
        o.append(f"| {c['name']} | {c['first']}〜{c['last']} | {c['n_cuts']} | {mmss(c['start'])} | {mmss(c['sec'])} | "
                 f"{c['n_lines']} | {c['chars_nopunct']:,} | {cpm:.1f} | {c['photo']} | {c['footage_moving']} | "
                 f"{c['text_A']} | {c['text_B']} | {c['planned_header']} |")
    o.append("")

    o.append("## 冒頭60秒の行（読み始めの時刻）\n")
    o.append("| 秒 | カット | 行 |")
    o.append("|---:|---|---|")
    for t, c, i, x in m["opening_60s"]:
        o.append(f"| {mmss(t)} | {c}-{i} | {x} |")
    o.append("")

    o.append("## 決め所（quote・★）\n")
    o.append("| # | カット | カット頭 | 句が出はじめる | 決め所の句 | 見出し | 原文の欄 |")
    o.append("|---:|---|---:|---:|---|---|---|")
    for k, q in enumerate(m["quotes"], 1):
        o.append(f"| {k} | {q['cid']} | {mmss(q['cut_start'])} | {mmss(q['appears'])} | {q['phrase']} | "
                 f"{q['heading']} | {q['ctx'].replace('|', '／')} |")
    o.append("")

    o.append("## 図の型（`kind`）\n")
    o.append("| 型 | 本数 |")
    o.append("|---|---:|")
    for k, n in m["fig_kinds"]:
        o.append(f"| {k} | {n} |")
    o.append("")
    o.append("## 写真を持つカットの内訳\n")
    o.append("| 種類 | 本数 |")
    o.append("|---|---:|")
    for k, n in m["photo_source_kinds"]:
        o.append(f"| {k} | {n} |")
    o.append("")
    o.append("## 静止画のファイルごとの使用回数（動く映像のカットを除く）\n")
    o.append("| ファイル | 回数 |")
    o.append("|---|---:|")
    for k, n in m["photo_files_static"]:
        o.append(f"| `{k}` | {n} |")
    o.append("")

    o.append("## 文字だけの画面\n")
    o.append(f"- 狭い数え方＝panel・quote・文字のスライド（p16 の問い・p86・p189・p191）：**{m['text_A']}カット"
             f"（{m['text_A_ratio']*100:.1f}%・{m['text_A_secs']}秒）**")
    o.append(f"- 広い数え方＝狭い＋absent・beforeafter・process：**{m['text_B']}カット"
             f"（{m['text_B_ratio']*100:.1f}%・{m['text_B_secs']}秒）**")
    o.append(f"- 文字の情報だけでは決まらないスライド（p185・どちらにも数えていない）：{' '.join(m['unsure_text_slides'])}")
    o.append("- 3カット以上続く所（狭い）：" + "／".join(f"{r[0]}〜{r[-1]}（{len(r)}）" for r in m["runs_A"]))
    o.append("- 3カット以上続く所（広い）：" + "／".join(f"{r[0]}〜{r[-1]}（{len(r)}）" for r in m["runs_B"]))
    o.append("")

    o.append("## ヤード・ポンド法の単位（ナレーション）\n")
    o.append("| カット-行 | 単位 | 同じ行に換算 | 同じカットに換算 | 次のカットに換算 | 文 |")
    o.append("|---|---|:-:|:-:|:-:|---|")
    for u in m["units_narration"]:
        yn = lambda b: "○" if b else "－"     # noqa: E731
        o.append(f"| {u['cid']}-{u['line']} | {'・'.join(u['units'])} | {yn(u['metric_same_line'])} | "
                 f"{yn(u['metric_same_cut'])} | {yn(u['metric_next_cut'])} | {u['text']} |")
    o.append("")
    o.append("## ヤード・ポンド法の単位（画面の文字・章マーカーを除く）\n")
    o.append("| カット | 単位 | 同じ文字列に換算 | 同じカットの画面に換算 | 文字列 |")
    o.append("|---|---|:-:|:-:|---|")
    n_cm = 0
    for u in m["units_screen"]:
        if u["chapter_marker"]:
            n_cm += 1
            continue
        yn = lambda b: "○" if b else "－"     # noqa: E731
        o.append(f"| {u['cid']} | {'・'.join(u['units'])} | {yn(u['metric_same_text'])} | {yn(u['metric_same_cut'])} | "
                 f"{u['text'].replace('|', '／')} |")
    o.append(f"\n章マーカー（第2章の章名「4インチの隙間」）に出たぶん：{n_cm}カット（c201〜c232 の全部）\n")

    o.append("## 時刻の書き方\n")
    o.append("| 形 | ナレーション | 画面 |")
    o.append("|---|---:|---:|")
    for k in m["time_narration"]:
        o.append(f"| {k} | {len(m['time_narration'][k])} | {len(m['time_screen'][k])} |")
    o.append("")
    for k in m["time_screen"]:
        for h in m["time_screen"][k]:
            o.append(f"- 画面 {h['cid']}：「{h['text']}」（{k}）")
    for k in m["time_narration"]:
        for h in m["time_narration"][k]:
            o.append(f"- 声 {h['cid']}：「{h['text']}」（{k}）")
    o.append("")

    o.append("## 死の語\n")
    o.append("| 語 | ナレーション | 画面 |")
    o.append("|---|---:|---:|")
    for k in m["death_narration"]:
        o.append(f"| {k} | {m['death_narration'][k]} | {m['death_screen'][k]} |")
    o.append("")
    for k, v in m["death_narration_hits"].items():
        for h in v:
            o.append(f"- 声 {h['cid']}：{h['text']}")
    for k, v in m["death_screen_hits"].items():
        for h in v:
            o.append(f"- 画面 {h['cid']}：{h['text']}")
    o.append("")

    o.append("## 噂・説の語が出る行（網：" + "・".join(m["rumor_hits"].keys()) + "）\n")
    seen = set()
    for k, v in m["rumor_hits"].items():
        for h in v:
            key = (h["cid"], h["text"])
            if key in seen:
                continue
            seen.add(key)
            o.append(f"- {h['cid']}：{h['text']}（{k}）")
    o.append("")

    o.append("## 出典の欄が「―」のカット（台本のコメント）\n")
    o.append(f"{len(m['no_source_cuts'])}カット：" + " ".join(m["no_source_cuts"]) + "\n")
    o.append("## 名前の候補（機械）\n")
    o.append("- カタカナの「・」つなぎ：" + "、".join(f"{k}（{n}）" for k, n in m["katakana_names"]))
    o.append("- 画面の英字の大文字の続き：" + "、".join(f"{k}（{n}）" for k, n in m["latin_names"]))
    o.append("")
    (HERE / "old_tables.md").write_text("\n".join(o) + "\n", encoding="utf-8")
    print("✓ old_tables.md")


if __name__ == "__main__":
    main()
