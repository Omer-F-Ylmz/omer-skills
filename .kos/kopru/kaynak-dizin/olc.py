"""KAYNAK-DIZIN-1 ölçümü: 5 örnek iş · altın küme recall · süre · çıktı jetonu (yeni/eski). Jeton ≈ UTF-8 bayt/3.6 (tiktoken yok)."""
import subprocess, sys, time, re
ISLER = {
    "İLİK 3D": ("parfüm şişesi 3D sahne blender render shader", ["shadergradient", "3d-model-anything", "onmars3d.com", "blender", "kurulum-blender-arastirma--1", "BlenderOlcum", "blender-kum", "parfum-yaris", "3dicons.co"]),
    "video hattı": ("video hattı remotion altyazı kurgu klip render", ["remotion.dev", "ffmpeg", "whisper-cli", "kids-shorts-sablon", "oktan-film"]),
    "site arka plan videosu": ("site arka plan videosu scroll hero gsap", ["4ce9-yat-sitesi-promptu-scroll-scrub-hero-video", "scrolltide.co", "scrollhaus.ai", "gsap.com", "madewithgsap.com", "threejs-spiral-gallery-gsap-scroll-reveal-hmr"]),
    "borsa botu": ("borsa botu al sat strateji backtest kripto trading", ["condor.hummingbot.org", "devir-desktop-devir-23eki-1021--6", "algoritmik"]),
    "logo": ("logo tasarımı marka logo", ["brandlogo.co", "liquid-logo", "pixeljury", "omer-logo", "omer-logo-2", "omer-logo-3", "omer-logo-final"]),
}


def calis(py, q, ek=()):
    t = time.time()
    r = subprocess.run([sys.executable, py, *ek, q], capture_output=True, encoding="utf-8", errors="replace")
    return r.stdout, time.time() - t


import tiktoken
_e = tiktoken.get_encoding("cl100k_base")
tj = lambda s: len(_e.encode(s))
t15 = ozet = hepsi = tum = 0
for ad, (q, gold) in ISLER.items():
    y, sn = calis("tools/envanter_tara.py", q, ["--yenile"])
    y2, sn2 = calis("tools/envanter_tara.py", q)
    b, bsn = calis("tools/envanter_tara.py", q, ["--brief", "--yenile"])
    e, _ = calis("tools/_eski_envanter.py", q, ["--yenile"])
    kay = y.split("## kaynaklar")[1].split("## ")[0].splitlines()[1:] if "## kaynaklar" in y else []
    ilk = [k for k in kay if k.strip() and not k.startswith("  (") and not k.startswith("+")]
    o15 = [g for g in gold if any(g in k for k in ilk)]
    oz = [g for g in gold if any(g in k for k in kay)]
    tum_k, _ = calis("tools/envanter_tara.py", q, ["--kaynak", "--hepsi"])
    oh = [g for g in gold if any(g in k for k in tum_k.splitlines())]
    print(f"{ad}: top15 {len(o15)}/{len(gold)} özet+kuyruk {len(oz)}/{len(gold)} hepsi {len(oh)}/{len(gold)} eksik(özet)={[g for g in gold if g not in oz]} | jeton tam {tj(y)} brief {tj(b)} eski {tj(e)} | süre ilk {sn:.1f}s brief-ilk {bsn:.1f}s önbellekli {sn2:.2f}s")
    t15 += len(o15); ozet += len(oz); hepsi += len(oh); tum += len(gold)
print(f"recall top15 {t15/tum:.0%} · özet+kuyruk {ozet/tum:.0%} · --hepsi {hepsi/tum:.0%}")
