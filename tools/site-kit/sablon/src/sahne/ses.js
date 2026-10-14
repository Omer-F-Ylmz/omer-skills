// Ses: varsayılan kapalı, AudioContext yalnız düğme tıkında doğar (autoplay kuralı). Sentez Web Audio — dosya/lisans/bağımlılık yok.
// Katmanlar: köz uğultusu (detune testereler → alçak geçiren) + seyrek çıtırtı; ayarla(p) kaydırmayı filtre/düzeye bağlar, tik() etkileşim sesi.
export function ses(dugme, { duzey = 0.4 } = {}) {
  let c, ana, filtre, citir;
  let acik = false;
  const kur = () => {
    c = new AudioContext();
    ana = c.createGain();
    ana.gain.value = 0;
    ana.connect(c.destination);
    filtre = c.createBiquadFilter();
    filtre.type = 'lowpass';
    filtre.frequency.value = 240;
    filtre.Q.value = 3;
    filtre.connect(ana);
    for (const [f, d] of [[55, -9], [55, 9], [82.4, 0]]) {
      const o = c.createOscillator();
      o.type = 'sawtooth';
      o.frequency.value = f;
      o.detune.value = d;
      const g = c.createGain();
      g.gain.value = 0.12;
      o.connect(g).connect(filtre);
      o.start();
    }
    const b = c.createBuffer(1, c.sampleRate * 3, c.sampleRate);
    const v = b.getChannelData(0);
    for (let i = 0; i < v.length; i++) v[i] = Math.random() < 0.0006 ? Math.random() * 2 - 1 : 0;
    const n = c.createBufferSource();
    n.buffer = b;
    n.loop = true;
    citir = c.createGain();
    citir.gain.value = 0.2;
    n.connect(citir).connect(ana);
    n.start();
  };
  const goster = () => {
    dugme.setAttribute('aria-pressed', acik);
    dugme.textContent = acik ? 'Ses: açık' : 'Ses: kapalı';
  };
  dugme.addEventListener('click', async () => {
    if (!c) kur();
    acik = !acik;
    goster();
    if (acik) await c.resume();
    ana.gain.setTargetAtTime(acik ? duzey : 0, c.currentTime, 0.25);
    // kapanışta sönüm bitince askıya al: arka planda DSP harcamasın
    if (!acik) setTimeout(() => !acik && c.suspend(), 1200);
  });
  document.addEventListener('visibilitychange', () => c && acik && (document.hidden ? c.suspend() : c.resume()));
  goster();
  return {
    ayarla(p) {
      if (!c) return;
      filtre.frequency.setTargetAtTime(240 + p * p * 2200, c.currentTime, 0.12);
      citir.gain.setTargetAtTime(0.2 + p * 0.5, c.currentTime, 0.12);
    },
    tik(f = 660) {
      if (!acik) return;
      const o = c.createOscillator();
      const g = c.createGain();
      o.frequency.setValueAtTime(f, c.currentTime);
      o.frequency.exponentialRampToValueAtTime(f / 2, c.currentTime + 0.15);
      g.gain.setValueAtTime(0.15, c.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.2);
      o.connect(g).connect(ana);
      o.start();
      o.stop(c.currentTime + 0.2);
    },
    dugum: () => ana,
  };
}
