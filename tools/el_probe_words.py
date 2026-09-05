# -*- coding: utf-8 -*-
r"""el_probe_words.py — 合成音を「語ごとの時刻つき」で文字起こしし、読みを**秒数で**測る。

  python tools\el_probe_words.py ep008 --ids s116,s118
  python tools\el_probe_words.py ep008 --ids s116 --focus 間     … その字だけ抜き出す
  python tools\el_probe_words.py ep008 --ids s116 --text "同じ論文はこれを、あいだを…"
        … 台本ではなく指定した文を合成して測る（A/B の候補側を試すとき）

🔴 なぜ要るか（2026-08-31）:
    ElevenLabs は読みを返さないので、これまで読みの可否は耳だけが頼りでした。
    ところが文字起こしは**漢字**を返すので、「間」が「ま」か「あいだ」かは字では分かりません。
    ⭐ ですが **モーラ数がちがえば秒数がちがう**ので、語の時間幅で読み分けられます。
       実測（ep008 s116）: 「間」=0.120秒。同じ行の1モーラの助詞「を」0.120秒・「て」0.100秒と同幅
       ＝「ま」（1モーラ）。「あいだ」（3モーラ）なら 0.36秒前後になるはず。

⚠️ これも門番ではありません。**当たりを付けて、直したあとに差が出たかを見る**道具です。
⚠️ 幅は前後の音や句末の伸びに引きずられます。**同じ行の中の1モーラの助詞と比べる**こと。
   行をまたいで秒数を比べない（話速が行ごとに違います）。

出力: 語・開始・終了・幅、および行の「1モーラあたりの目安」（助詞から推定）
"""
import json
import struct
import sys
import urllib.request
import uuid
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_tts                                   # noqa: E402
import el_script as ES                          # noqa: E402  行の列挙・EL_YOMI・キャッシュの場所
el_text = ES.el_text

# 1モーラの目安を取るのに使う語（ほぼ確実に1モーラ）
ONE_MORA = set("をがはにでとへもねよか")


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def stt_words(pcm: bytes):
    n = len(pcm)
    hdr = struct.pack("<4sI4s4sIHHIIHH4sI", b"RIFF", 36 + n, b"WAVE", b"fmt ",
                      16, 1, 1, el_tts.SR, el_tts.SR * 2, 2, 16, b"data", n)
    wav = hdr + pcm
    bd = "----" + uuid.uuid4().hex

    def part(k, v):
        return (f'--{bd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n').encode()

    body = (part("model_id", "scribe_v1") + part("language_code", "jpn")
            + part("timestamps_granularity", "word"))
    body += (f'--{bd}\r\nContent-Disposition: form-data; name="file"; filename="a.wav"\r\n'
             f'Content-Type: audio/wav\r\n\r\n').encode() + wav + b"\r\n"
    body += f"--{bd}--\r\n".encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text",
                                 data=body, method="POST",
                                 headers={"xi-api-key": el_tts.key(),
                                          "Content-Type": "multipart/form-data; boundary=" + bd})
    with urllib.request.urlopen(req, timeout=300) as res:
        r = json.load(res)
    return r.get("text", ""), [w for w in r.get("words", []) if w.get("type") == "word"]


def main():
    slug = ES.SLUG
    ids = ES.resolve_ids(arg("--ids"))          # 行ID（c112-2）かカットID（c112＝全行）。無いIDは止まる
    focus = arg("--focus")
    override = arg("--text")
    if not ids:
        print(__doc__)
        print("[FATAL] --ids で行IDを指定してください", file=sys.stderr)
        return 2
    if override and len(ids) != 1:
        print("[FATAL] --text は行1つのときだけ使えます", file=sys.stderr)
        return 2

    by_id = ES.by_id()
    rc = 0
    for sid in ids:
        ln = by_id[sid]
        sent = override if override else el_text(ln.text)
        cache = ES.cache_path(sent)
        if cache.exists():
            pcm = cache.read_bytes()
            src = "キャッシュ"
        elif override:
            pcm = el_tts.synth(sent, sid, slug=slug, settings=ES.SETTINGS)      # 候補側は無ければ合成する
            src = "新規合成"
        else:
            print(f"[FATAL] 合成キャッシュがありません: {sid}", file=sys.stderr)
            rc = 1
            continue
        text, ws = stt_words(pcm)
        one = [w["end"] - w["start"] for w in ws if w["text"] in ONE_MORA]
        unit = sum(one) / len(one) if one else None
        print(f"\n=== {sid}（{src}） ===")
        print(f"  送信: {sent}")
        print(f"  聞取: {text}")
        if unit:
            print(f"  1モーラの目安: {unit:.3f}秒（この行の助詞 {len(one)}個の平均）")
        for w in ws:
            if focus and w["text"] not in focus:
                continue
            d = w["end"] - w["start"]
            mora = f"≒{d/unit:.1f}モーラ" if unit else ""
            print(f"    {w['text']:<3} {w['start']:6.3f}〜{w['end']:6.3f}  幅{d:.3f}秒  {mora}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
