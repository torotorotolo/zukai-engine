// 27本目 ⑥'（2026-10-30）：YouTube の動画の声の帯域を、内蔵ブラウザの中で数える（音は外に出さない・音のデータは保存しない）。
// なぜ：競合の音は yt-dlp だと配信の側が 403＝取り方を替えて回り込まない。見る人と同じ形で再生し、ページの中で qa_out/ep27_r01_voiceq.py と同じ式で数える。
// 使い方（内蔵ブラウザの javascript_tool で2回）：
//   ① https://www.youtube.com/watch?v=<id>&t=300s を開いて START を実行（広告は ad-showing の間だけ飛ばす・見る人がスキップを押すのは可）
//   ② 60秒たまったら ANALYZE を実行（42秒待っても終わらなければもう一度）→ 帯域（全体に対する dB）・クレスト・声の秒・切れ目の数
// 物差し合わせ：26本目（3NTJQrd2Vm0）の同じ60秒で、手元の mp4（Python）と 0〜8kHz の帯が 0.1dB 以内で一致（qa_out/ep27_r02/voiceq_rivals.tsv）

// ── START ─────────────────────────────────────────
(async () => {
  const v = document.querySelector('video');
  if (!v) return 'no video';
  const mp = document.querySelector('#movie_player');
  if (window.__vq) return JSON.stringify({already: window.__vq.state});
  const ctx = new AudioContext();
  const src = ctx.createMediaElementSource(v);
  const BS = 16384;
  const sp = ctx.createScriptProcessor(BS, 2, 1);
  const g = ctx.createGain(); g.gain.value = 0;                 // 音は外に出さない
  src.connect(sp); sp.connect(g); g.connect(ctx.destination);
  const q = window.__vq = {state: 'arm', runs: [[]], n: 0, sr: ctx.sampleRate, skipAd: 0, skipPause: 0, breaks: 0, lastVt: null, t0: null};
  const target = ctx.sampleRate * 60, dur = BS / ctx.sampleRate;
  sp.onaudioprocess = (e) => {
    if (q.state !== 'rec') return;
    const ad = mp && mp.classList.contains('ad-showing');
    const vt = v.currentTime;
    if (ad) { q.skipAd++; q.lastVt = null; return; }
    if (v.paused || vt < 299) { q.skipPause++; q.lastVt = null; return; }
    // 動画の時刻が塊の長さどおりに進んでいなければ、そこで切る（切れ目をまたぐ窓を作らない）
    if (q.lastVt === null || Math.abs((vt - q.lastVt) - dur) > 0.15) { if (q.runs[q.runs.length - 1].length) { q.runs.push([]); q.breaks++; } }
    q.lastVt = vt;
    const a = e.inputBuffer.getChannelData(0), b = e.inputBuffer.numberOfChannels > 1 ? e.inputBuffer.getChannelData(1) : a;
    const m = new Float32Array(a.length);
    for (let i = 0; i < a.length; i++) m[i] = (a[i] + b[i]) / 2;   // ffmpeg -ac 1 と同じ（左右の平均）
    if (q.t0 === null) q.t0 = vt;
    q.runs[q.runs.length - 1].push(m); q.n += m.length;
    if (q.n >= target) { q.state = 'done'; q.t1 = vt; v.pause(); }
  };
  v.muted = false; v.volume = 1;
  const info = {};
  try { await ctx.resume(); } catch (e) { info.resumeErr = String(e); }
  try { await v.play(); } catch (e) { info.playErr = String(e); }
  q.state = 'rec';
  await new Promise(r => setTimeout(r, 3000));
  return JSON.stringify({id: new URL(location.href).searchParams.get('v'), sr: ctx.sampleRate, ctx: ctx.state, paused: v.paused, t: v.currentTime, n: q.n, ad: !!(mp && mp.classList.contains('ad-showing')), info});
})();

// ── ANALYZE ───────────────────────────────────────
(async () => {
  const q = window.__vq; if (!q) return 'no vq';
  for (let i = 0; i < 42 && q.state !== 'done'; i++) await new Promise(r => setTimeout(r, 1000));
  if (q.state !== 'done') return JSON.stringify({state: q.state, sec: q.n / q.sr, skipAd: q.skipAd, breaks: q.breaks});
  function fft(re, im) {
    const n = re.length;
    for (let i = 1, j = 0; i < n; i++) { let bit = n >> 1; for (; j & bit; bit >>= 1) j ^= bit; j ^= bit; if (i < j) { let t = re[i]; re[i] = re[j]; re[j] = t; t = im[i]; im[i] = im[j]; im[j] = t; } }
    for (let len = 2; len <= n; len <<= 1) { const h = len >> 1; for (let j = 0; j < h; j++) { const ang = -2 * Math.PI * j / len, cr = Math.cos(ang), ci = Math.sin(ang); for (let i = 0; i < n; i += len) { const a = i + j, b = a + h; const vr = re[b] * cr - im[b] * ci, vi = re[b] * ci + im[b] * cr; re[b] = re[a] - vr; im[b] = im[a] - vi; re[a] += vr; im[a] += vi; } } }
  }
  const sr = q.sr, NFFT = 4096, hop = Math.round(sr * 0.05);
  const win = new Float64Array(NFFT); for (let i = 0; i < NFFT; i++) win[i] = 0.5 - 0.5 * Math.cos(2 * Math.PI * i / (NFFT - 1));   // np.hanning
  const acc = new Float64Array(NFFT / 2 + 1), re = new Float64Array(NFFT), im = new Float64Array(NFFT);
  let kk = 0, nvTot = 0, vs2 = 0, vc = 0, vmax = 0, clip = 0, amax = 0, Ntot = 0; const vaList = [];
  for (const run of q.runs) {
    const N = run.reduce((s, b) => s + b.length, 0); if (N < NFFT) continue; Ntot += N;
    const x = new Float32Array(N); let o = 0; for (const b of run) { x.set(b, o); o += b.length; }
    for (let i = 0; i < N; i++) { const a = Math.abs(x[i]); if (a >= 0.96) clip++; if (a > amax) amax = a; }
    const nf = Math.floor(N / hop), on = new Uint8Array(nf);
    for (let k = 0; k < nf; k++) { let s = 0; for (let i = k * hop; i < (k + 1) * hop; i++) s += x[i] * x[i]; on[k] = 20 * Math.log10(Math.sqrt(s / hop + 1e-20)) > -35 ? 1 : 0; if (on[k]) { nvTot++; const va = new Float32Array(hop); for (let i = 0; i < hop; i++) { const a = Math.abs(x[k * hop + i]); va[i] = a; vs2 += x[k * hop + i] ** 2; vc++; if (a > vmax) vmax = a; } vaList.push(va); } }
    for (let i = 0; i < N - NFFT; i += NFFT / 2) {
      if (!on[Math.min(nf - 1, Math.floor((i + NFFT / 2) / hop))]) continue;
      for (let j = 0; j < NFFT; j++) { re[j] = x[i + j] * win[j]; im[j] = 0; }
      fft(re, im); for (let j = 0; j <= NFFT / 2; j++) acc[j] += re[j] * re[j] + im[j] * im[j]; kk++;
    }
  }
  const all = new Float32Array(vc); let p = 0; for (const va of vaList) { all.set(va, p); p += va.length; } all.sort();
  const vrms = Math.sqrt(vs2 / Math.max(vc, 1)), p999 = all[Math.min(all.length - 1, Math.floor(0.999 * (all.length - 1)))];
  const BANDS = [[0, 500], [500, 1000], [1000, 2000], [2000, 4000], [4000, 8000], [8000, 12000], [12000, 16000], [16000, 22050]];
  let tot = 0; for (let j = 0; j <= NFFT / 2; j++) if (j * sr / NFFT < 22050) tot += acc[j];
  const bd = BANDS.map(([lo, hi]) => { let s = 0; for (let j = 0; j <= NFFT / 2; j++) { const f = j * sr / NFFT; if (f >= lo && f < hi) s += acc[j]; } return +(10 * Math.log10(s / tot + 1e-30)).toFixed(1); });
  const r = {id: new URL(location.href).searchParams.get('v'), sr, sec: +(Ntot / sr).toFixed(2), t0: q.t0, t1: q.t1, runs: q.runs.length, breaks: q.breaks, skipAd: q.skipAd, voicedSec: +(nvTot * 0.05).toFixed(1), windows: kk, bands: bd, crestMax: +(20 * Math.log10(vmax / vrms)).toFixed(1), crest999: +(20 * Math.log10(p999 / vrms)).toFixed(1), voicedRmsDb: +(20 * Math.log10(vrms)).toFixed(1), clip096: clip, absMax: +amax.toFixed(3)};
  q.runs = null;
  return JSON.stringify(r);
})();
