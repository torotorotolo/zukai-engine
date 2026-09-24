# -*- coding: utf-8 -*-
"""音素の網（再発防止策1の試作）── Modal で「音 → 音素の確率」と「送信文 → 読みの音素」を出す（2026-09-24）。

  PYTHONIOENCODING=utf-8 modal run qa_out/phon_asr_modal.py --tag ep13
  → out/phon/<tag>_lp.npz（行ID → [枠×記号] float16 の log-softmax・1枠 20ms）
    out/phon/<tag>_g2p.json（{"vocab", "blank", "lines": {行ID: {"g2p", "tokens": [[表層, 読み, 音素]]}}}）

入力は qa_out/phon_prep.py の out/phon/<tag>_wav16.npz・<tag>_texts.json（音は PC で切ってから送る）。
モデル＝prj-beatrice/japanese-hubert-base-phoneme-ctc-v4（Hugging Face・Apache-2.0・378MB）。
🔴 カズヤくんの許可（2026-09-24）＝**Modal の中だけ**に落とす。PC には torch も辞書も入れない（コミットの空きが細い）。
🔴 読み（g2p）は pyopenjtalk-plus＝モデルの学習ラベルと同じ体系の音素（a i u e o・無声化 I U・N・cl・pau）。
"""
import io
import json
from pathlib import Path

import modal

MODEL = "prj-beatrice/japanese-hubert-base-phoneme-ctc-v4"
PAD = 8000           # 🔴 前後に 0.5秒の無音を足す（2026-09-24 実測）。合成音は無音なしでいきなり始まるので、
                     #    足さないとモデルが最初の 0.3〜0.6秒を空白にして行頭の語を落とす（陰性 425行中 424行で「頭」が鳴った）。
                     #    本番でも行の前には GAP 0.40／LEAD 0.35 の無音がある＝聞く条件にそろえる。phon_check も同じ値で足す
app = modal.App("phon-asr")


def _bake():
    from transformers import AutoModelForCTC, AutoProcessor
    AutoProcessor.from_pretrained(MODEL)
    AutoModelForCTC.from_pretrained(MODEL)
    import pyopenjtalk
    pyopenjtalk.g2p("テスト")          # 辞書を image に焼き込む（実行のたびに取りに行かない）


image = (modal.Image.debian_slim(python_version="3.11")
         .apt_install("build-essential", "cmake")
         .pip_install("torch==2.4.1", index_url="https://download.pytorch.org/whl/cpu")
         .pip_install("transformers==4.44.2", "numpy<2", "pyopenjtalk-plus")
         .run_function(_bake))


@app.function(image=image, cpu=4.0, memory=4096, timeout=1500)
def logprobs(blob: bytes) -> bytes:
    import numpy as np
    import torch
    from transformers import AutoModelForCTC
    torch.set_num_threads(4)
    model = AutoModelForCTC.from_pretrained(MODEL).eval()
    d = np.load(io.BytesIO(blob))
    out = {}
    with torch.inference_mode():
        for k in d.files:
            z = np.zeros(PAD, dtype=np.float32)
            x = torch.from_numpy(np.concatenate([z, d[k].astype(np.float32) / 32768.0, z]))[None]
            lg = model(x).logits[0].float()
            out[k] = torch.log_softmax(lg, -1).numpy().astype(np.float16)
    buf = io.BytesIO()
    np.savez_compressed(buf, **out)
    return buf.getvalue()


@app.function(image=image, timeout=900)
def g2p(texts: dict) -> dict:
    import re
    import pyopenjtalk
    from transformers import AutoConfig, AutoProcessor
    kana = re.compile(r"[ぁ-ゟ゠-ヿ]")
    proc = AutoProcessor.from_pretrained(MODEL)
    cfg = AutoConfig.from_pretrained(MODEL)
    lines = {}
    for k, t in texts.items():
        toks = []
        for n in pyopenjtalk.run_frontend(t):
            surf = n.get("string", "")
            pron = (n.get("pron") or "").replace("’", "")
            ph = pyopenjtalk.g2p(pron) if kana.search(pron) else ""
            toks.append([surf, pron, ph])
        lines[k] = {"g2p": pyopenjtalk.g2p(t), "tokens": toks}
    return {"vocab": proc.tokenizer.get_vocab(), "blank": cfg.pad_token_id, "lines": lines}


@app.local_entrypoint()
def main(tag: str = "ep13", chunk: int = 40):
    import numpy as np
    base = Path(__file__).resolve().parent.parent / "out" / "phon"
    d = np.load(base / f"{tag}_wav16.npz")
    texts = json.loads((base / f"{tag}_texts.json").read_text(encoding="utf-8"))
    keys = list(d.files)
    blobs = []
    for i in range(0, len(keys), chunk):
        buf = io.BytesIO()
        np.savez(buf, **{k: d[k] for k in keys[i:i + chunk]})
        blobs.append(buf.getvalue())
    merged = {}
    for b in logprobs.map(blobs):
        z = np.load(io.BytesIO(b))
        merged.update({k: z[k] for k in z.files})
    if set(merged) != set(keys):
        raise SystemExit(f"🔴 音素の確率が返らなかった行: {sorted(set(keys) - set(merged))[:10]}")
    np.savez_compressed(base / f"{tag}_lp.npz", **merged)
    g = g2p.remote({k: v["sent"] for k, v in texts.items()})
    (base / f"{tag}_g2p.json").write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
    print(f"✓ {tag}: 音素の確率 {len(merged)}行／読み {len(g['lines'])}行／記号 {len(g['vocab'])}（空白 id {g['blank']}）")
