# -*- coding: utf-8 -*-
"""illu_preview.py — 案C の再現イラストを**ブラウザで下見する**ページを書き出す（2026-09-28 新設・14本目 ⑤b-2）。

■ なぜ要るか（ルール §5b-76）
  レンダはローカルでやらない（§6-1）。案C の見た目の試しだけは、ブラウザで SVG を直接開いてよい。
  このページは**本番と同じ層の SVG**（`scene_jiko.build_layers`）を1枚の SVG に並べ、`build_jiko.illu_frame` と同じ
  段の鍵（rot・sc・dx・dy・a・音の輪・人の影の道・波・カメラ）を JS で再生する＝Chrome を焼かずに動きが見える。
  ⚠️ 下見は SVG の transform で動かす（本番は PIL の補間）＝ふちの滑らかさは違う。**本番の確認は Actions**（`at` で途中のコマ）

■ 使い方
    python tools/illu_preview.py c101 c103 --out "<Vault>/Resources/事故検証ch-案C見本/ep14"
    → <out>/<cid>.html（下の帯で時刻を動かせる・URL の #t=秒 で止めて開く＝hashchange で読み直す）
  Vault の `.claude/launch.json` の `jiko-anc-mock`（python http.server）で開く（file:// は静止画の写しになる）。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J  # noqa: E402
import scene_jiko as S  # noqa: E402

JS = r"""
const ease = u => 0.5 - 0.5 * Math.cos(Math.PI * Math.min(1, Math.max(0, u)));
const DEF = {rot: 0, sc: 1, dx: 0, dy: 0, a: 1};
function tk(st, dl, times) { return (st < times.length ? times[st][0] : 0) + (dl || 0); }
function state(keys, t, times, dflt) {
  dflt = dflt || DEF;
  let j = 0; const tks = keys.map(k => tk(k.stage, k.delay, times));
  tks.forEach((v, i) => { if (t >= v) j = i; });
  const cur = keys[j], out = {};
  if (j === 0) { for (const k in dflt) out[k] = (cur[k] ?? dflt[k]); return out; }
  const prev = keys[j - 1], u = ease((t - tks[j]) / Math.max(0.01, cur.dur ?? 1.1));
  for (const k in dflt) { const a = prev[k] ?? dflt[k], b = cur[k] ?? dflt[k]; out[k] = a + (b - a) * u; }
  return out;
}
function tf(st, piv) {
  return `translate(${st.dx} ${st.dy}) translate(${piv[0]} ${piv[1]}) rotate(${st.rot}) scale(${st.sc}) translate(${-piv[0]} ${-piv[1]})`;
}
function path(p, dt, speed) {
  speed = speed || 190;
  for (let i = 0; i + 1 < p.length; i++) {
    const a = p[i], b = p[i + 1], d = Math.max(0.3, Math.hypot(b[0] - a[0], b[1] - a[1]) / speed);
    if (dt < d) { const u = ease(dt / d); return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]; }
    dt -= d;
  }
  return p[p.length - 1];
}
function drawScene(sc, t, times) {
  for (const p of sc.parts) {
    const el = document.getElementById(p.name);
    if (!el && (p.drift || (p.kind || 'layer') === 'layer')) continue;
    if (p.drift) { const d = ((t * p.drift) % 1920 + 1920) % 1920; el.setAttribute('transform', `translate(${d} 0)`);
      const e2 = document.getElementById(p.name + '_w'); if (e2) e2.setAttribute('transform', `translate(${d - 1920} 0)`); continue; }
    if ((p.kind || 'layer') === 'layer') { const st = state(p.keys, t, times); el.setAttribute('transform', tf(st, p.pivot)); el.setAttribute('opacity', st.a); }
    else if (p.kind === 'ring') {
      let k = 0;
      for (const ev of p.pulse) { const t0 = tk(ev.stage, ev.delay, times);
        for (let j = 0; j < ev.n; j++) { const u = (t - t0 - j * ev.gap) / ev.dur, e = document.getElementById(p.name + '_' + (k++));
          if (!e) continue;
          if (u >= 0 && u < 1) { const st = {rot: 0, dx: 0, dy: 0, sc: ev.s0 + (ev.s1 - ev.s0) * ease(u)}; e.setAttribute('transform', tf(st, p.pivot)); e.setAttribute('opacity', Math.pow(1 - u, 1.2)); }
          else e.setAttribute('opacity', 0); } }
    } else if (p.kind === 'sprite') {
      p.inst.forEach((ins, j) => { const e = document.getElementById(p.name + '_' + j); const t0 = tk(ins.stage, ins.delay, times);
        if (t < t0) { e.setAttribute('opacity', 0); return; }
        const xy = path(ins.path, t - t0); e.setAttribute('transform', `translate(${xy[0] - p.foot[0]} ${xy[1] - p.foot[1]})`);
        e.setAttribute('opacity', Math.min(1, (t - t0) / 0.25)); });
    }
  }
}
function frame(t) {
  const C = window.CUT, times = C.times;
  if (C.full) {
    const sc = C.scenes[0]; drawScene(sc, t, times);
    C.tagIds.forEach((id, i) => { const el = document.getElementById(id); if (!el) return; const info = sc.tags[i] || {};
      let a = ease((t - times[i][0] - (info.delay ?? 0.35)) / 0.45);
      if (!info.keep && i + 1 < times.length) a *= 1 - ease((t - times[i + 1][0]) / 0.45);
      el.setAttribute('opacity', a); });
    const z = sc.cam ? state(sc.cam, t, times, {z: 1}).z : 1, c = sc.camc;
    document.getElementById('cam').setAttribute('transform', `translate(${c[0]} ${c[1]}) scale(${z}) translate(${-c[0]} ${-c[1]})`);
  } else if (C.intro) {
    const sc = C.intro; drawScene(sc, t, sc.times);
    document.getElementById('introwrap').setAttribute('opacity', t < C.introSec ? 1 : Math.max(0, 1 - (t - C.introSec) / 0.6));
    const z = sc.cam ? state(sc.cam, t, sc.times, {z: 1}).z : 1, c = sc.camc;
    document.getElementById('cam').setAttribute('transform', `translate(${c[0]} ${c[1]}) scale(${z}) translate(${-c[0]} ${-c[1]})`);
  } else {
    C.scenes.forEach((sc, k) => { drawScene(sc, t, times); const a = ease((t - (sc.show < times.length ? times[sc.show][0] : 0)) / 0.45);
      document.getElementById('mini' + k).setAttribute('opacity', a); });
    C.tagIds.forEach((id, i) => { const el = document.getElementById(id); if (el) el.setAttribute('opacity', ease((t - times[i][0]) / 0.6)); });
  }
  const r = C.subs.find(x => t >= x.t && t < x.t + x.d + 0.43) || null;
  const s1 = document.getElementById('s1'), s2 = document.getElementById('s2');
  if (r) { const L = r.lines; s1.textContent = L[0]; s2.textContent = L[1] || ''; const col = r.who === 'q' ? '#8fb6c9' : '#eaf2f6';
    s1.setAttribute('fill', col); s2.setAttribute('fill', col); s1.setAttribute('y', L[1] ? 968 : 1000); }
  else { s1.textContent = ''; s2.textContent = ''; }
}
(() => {
  const sl = document.getElementById('sl'), tt = document.getElementById('tt'), pp = document.getElementById('pp');
  let playing = true, base = performance.now(), off = 0;
  function readHash() { const m = location.hash.match(/t=([\d.]+)/); if (m) { playing = false; off = +m[1]; pp.textContent = '再生'; } }
  readHash(); window.addEventListener('hashchange', () => { readHash(); frame(off); sl.value = off; tt.textContent = off.toFixed(2) + ' 秒'; });
  pp.onclick = () => { playing = !playing; pp.textContent = playing ? '一時停止' : '再生'; base = performance.now(); off = +sl.value; };
  sl.oninput = () => { playing = false; pp.textContent = '再生'; off = +sl.value; };
  (function loop(now) { const D = window.CUT.dur; const t = playing ? (off + (now - base) / 1000) % D : off;
    frame(t); sl.value = t; tt.textContent = t.toFixed(2) + ' 秒'; requestAnimationFrame(loop); })(performance.now());
})();
"""


def _ns(svg, pre):
    """層の中の id を層ごとに付け替える（1枚の SVG に並べるとぶつかる）。"""
    svg = re.sub(r'id="([^"]+)"', lambda m: f'id="{pre}{m.group(1)}"', svg)
    return re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{pre}{m.group(1)})', svg)


def _parts_svg(cid, sc, jobs):
    g = []
    for p in sc["parts"]:
        name = p["name"]
        inner = _ns(S.J.remap(jobs[name], S.pal_of_layer(name)), name + "_")
        if p.get("drift"):
            g.append(f'<g id="{name}">{inner}</g><g id="{name}_w">{inner}</g>')
        elif p.get("kind") == "ring":
            k = sum(int(ev["n"]) for ev in p["pulse"])
            g += [f'<g id="{name}_{j}" opacity="0">{_ns(jobs[name], f"{name}_{j}_")}</g>' for j in range(k)]
        elif p.get("kind") == "sprite":
            g += [f'<g id="{name}_{j}" opacity="0">{_ns(jobs[name], f"{name}_{j}_")}</g>' for j in range(len(p["inst"]))]
        else:
            g.append(f'<g id="{name}">{inner}</g>')
    return "".join(g)


def page(cid, idx, jobs, css_href):
    v = idx[cid]
    meta_times = S.stage_times(cid, v["stages"], v.get("holds"))
    il, intro = v.get("illu"), v.get("intro")
    L = lambda k: S.J.remap(jobs[k], S.pal_of_layer(k)) if k in jobs else ""  # noqa: E731
    tag_ids = [f"{cid}_a{i + 1}" for i in range(v["stages"])]
    body = []
    data = dict(dur=round(S.content_sec(cid), 3), times=meta_times, tagIds=tag_ids,
                subs=[dict(t=r["t"] + S.LEAD, d=r["d"], who=r.get("who", "n")[:1],
                           lines=S.wrap2(r["text"]) if hasattr(S, "wrap2") else [r["text"]])
                      for r in S.SUBS.get(cid, [])])
    if il and il.get("full"):
        sc = il["scenes"][0]
        body.append('<g id="cam">' + _parts_svg(cid, sc, jobs)
                    + "".join(f'<g id="{k}" opacity="0">{L(k)}</g>' for k in tag_ids) + "</g>")
        body.append(L(f"{cid}_base"))
        data.update(full=True, scenes=[sc])
    elif intro and intro.get("illu"):
        sc = intro["illu"]
        body.append(L(f"{cid}_base") + L(f"{cid}_lab") + "".join(L(k) for k in tag_ids))
        body.append('<g id="introwrap"><rect width="1920" height="1080" fill="#000"/><g id="cam">'
                    + _parts_svg(cid, sc, jobs) + "</g>" + L(f"{cid}_ilab") + "</g>")
        data.update(full=False, intro=sc, introSec=intro["sec"], scenes=[])
    else:
        body.append(L(f"{cid}_base") + L(f"{cid}_lab"))
        for k, sc in enumerate((il or {}).get("scenes") or []):
            x, y, w, h = sc["box"]
            body.append(f'<g id="mini{k}" opacity="0"><svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 1920 1080">'
                        f'<rect width="1920" height="1080" fill="#000"/>{_parts_svg(cid, sc, jobs)}</svg></g>')
        body.append("".join(f'<g id="{k}" opacity="0">{L(k)}</g>' for k in tag_ids))
        data.update(full=False, scenes=(il or {}).get("scenes") or [])
    band = '<rect x="0" y="900" width="1920" height="180" fill="#000"/>'
    sub = ('<g font-family="Noto" font-size="56" text-anchor="middle" stroke="#000" stroke-width="10" '
           'stroke-linejoin="round" paint-order="stroke fill"><text id="s1" x="960" y="1000"></text>'
           '<text id="s2" x="960" y="1044"></text></g>')
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>下見 {cid}</title>'
            f'<link rel="stylesheet" href="{css_href}"><style>html,body{{margin:0;background:#16181a;color:#dfe6ea;'
            f'font:14px sans-serif}} svg{{display:block;width:100%;height:auto}} .bar{{display:flex;gap:12px;padding:8px 16px}}'
            f' .bar input{{flex:1}}</style></head><body><svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">'
            + "".join(body) + band + sub
            + '</svg><div class="bar"><button id="pp">一時停止</button><input id="sl" type="range" min="0" '
            f'max="{data["dur"]}" step="0.02" value="0"><span id="tt"></span></div>'
            f'<script>window.CUT={json.dumps(data, ensure_ascii=False)};</script><script>{JS}</script></body></html>')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = Path(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), "out/illu_preview"))
    out.mkdir(parents=True, exist_ok=True)
    css = out / "fonts.css"
    if not css.exists():
        S.ensure_css()
        css.write_text(S.CSS, encoding="utf-8")
    idx, jobs = S.layer_index(allow_missing=True)
    for cid in args:
        (out / f"{cid}.html").write_text(page(cid, idx, jobs, "fonts.css"), encoding="utf-8")
        print(f"✓ {out / (cid + '.html')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
