"""Yüklü 357 tekil (ecc dışı) skill'i aile paketlerine çevirir. Kaynak: y12 zip'leri. Çıktı: y12/p5/"""
import sys, zipfile, pathlib, shutil
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import paketle as P

Y = pathlib.Path("/mnt/user-data/uploads/y12")
ACIK = pathlib.Path("/tmp/claude-0/aile"); shutil.rmtree(ACIK, ignore_errors=True); ACIK.mkdir(parents=True)
yollar = [l for l in open("/tmp/claude-0/yuklu.txt").read().split() if "/ecc-" not in l]
aile = {}
for z, satir in zip(yollar, open("/tmp/claude-0/diger357.txt").read().splitlines()):
    fam, ad = satir.split()
    zipfile.ZipFile(Y / z).extractall(ACIK / fam)
    aile.setdefault(fam, []).append(ACIK / fam / ad)

PLAN = [
 ("mattpocock-paket", "Matt Pocock iş akışları: TDD, grill-me, spec/plan/handoff, kod tabanı mimarisi, PR, araştırma, yazım", ["mattpocock-skills"]),
 ("android-paket", "Android: Compose, Navigation 3, CameraX, Media3, Wear/TV, Play Billing, güvenlik, profiler, AGP 9, R8", ["android-skills"]),
 ("tasarim-etkilesim-ui-paket", "Etkileşim ve UI: UX yasaları (Fitts/Hick/Miller), form, navigasyon, mikro etkileşim, renk, tipografi, grid, hiyerarşi", ["interaction-design", "ui-design"]),
 ("tasarim-arastirma-strateji-paket", "Tasarım araştırması ve strateji: persona, yolculuk, görüşme, anket, JTBD, UX stratejisi, design ops", ["design-research", "ux-strategy", "design-strategy", "design-ops"]),
 ("tasarim-sistem-prototip-paket", "Tasarım sistemi ve prototip: token, bileşen spec, kalıp kütüphanesi, A/B ve kullanılabilirlik testi, görsel eleştiri", ["design-systems", "prototyping-testing", "visual-critique", "designer-toolkit"]),
 ("arayuz-iyilestirme-paket", "Arayüz iyileştirme: better-ui/colors/layout/typography/writing/accessibility, arayüz inceleme, durum makinesi", ["interfaces"]),
 ("erisilebilirlik-paket", "Erişilebilirlik ve kapsayıcı tasarım: bilişsel yük, uyarlanabilir arayüz, erişilebilir içerik, klavye, dokunma, ses", ["inclusive-personas", "inclusive-interaction", "cognitive-accessibility", "adaptive-interfaces", "accessible-content", "accessibility-decisions"]),
 ("ai-etkilesim-tasarim-paket", "AI ürün etkileşimi: konuşma kalıpları, ses tonu/persona, ajan rolleri, hata kişiliği, insan-döngüde, önyargı, onay", ["model-interaction-design", "system-behavior-shaping", "design-agent-orchestration", "ai-alignment-reasoning"]),
 ("daymade-gelistirici-paket", "Geliştirici araçları: CC/Codex geçmişini okuma ve sürdürme, kota/kullanım, statusline, Codex çalıştırma, skill yönetimi", ["daymade-claude-code", "daymade-codex", "daymade-skill", "codex"]),
 ("daymade-belge-finans-macos-paket", "Belge, finans, macOS: PDF/PPT/Excel/Markdown dönüşümü, mermaid, finans veri ve rapor, macOS izin/yük/temizlik bakımı", ["daymade-financial", "daymade-docs", "daymade-macos"]),
 ("daymade-ses-paket", "Ses ve konuşma: ASR yazıya dökme, StepFun TTS/ASR, ses yönlendirme, transkript düzeltme", ["daymade-audio"]),
 ("adobe-paket", "Adobe yaratıcı araçlar: PDF/Word/Excel/PPT, fotoğraf düzenleme/rötuş, sosyal varyasyon, şablondan tasarım, font, video", ["adobe-for-creativity"]),
 ("hyperframes-paket", "HyperFrames video/animasyon: core, registry, animasyon, yaratıcı efektler, medya kullanımı, konuşan kafa kurgusu, Figma", ["hyperframes/hyperframes-core", "hyperframes/hyperframes-registry", "hyperframes/hyperframes-animation", "hyperframes/hyperframes-creative", "hyperframes/talking-head-recut", "hyperframes/figma", "hyperframes/media-use"]),
 ("hareket-altyazi-3d-paket", "Hareket ve 3D: GSAP (core, ScrollTrigger, timeline, React, plugin, performans), gömülü altyazı, WebGPU Three.js TSL", ["gsap-skills", "hyperframes/embedded-captions", "webgpu-threejs-tsl"]),
 ("chrome-devtools-paket", "Chrome DevTools: erişilebilirlik ve LCP hata ayıklama, bellek sızıntısı, çerez, DevTools CLI, sorun giderme", ["chrome-devtools-mcp"]),
]
kullanilan = set()
toplam = 0
for ad, konu, fams in PLAN:
    kaynak = [d for f in fams for d in (aile[f] if "/" not in f else [x for x in aile[f.split("/")[0]] if x.name == f.split("/")[1]])]
    assert all(kaynak), fams
    kullanilan |= {f.split("/")[0] for f in fams}
    zp, n = P.paketle(ad, konu, kaynak, Y / "p5")
    toplam += len(kaynak)
    print(f"{ad}: {len(kaynak)} skill · {n} dosya · {zp.stat().st_size // 1024} KB")
secilen = {str(d) for ad, konu, fams in PLAN for f in fams for d in (aile[f] if "/" not in f else [x for x in aile[f.split("/")[0]] if x.name == f.split("/")[1]])}
kalan = {f: [d.name for d in v if str(d) not in secilen] for f, v in aile.items()}
kalan = {f: v for f, v in kalan.items() if v}
print("paketlenen", toplam, "· tekil kalan", sum(len(v) for v in kalan.values()), kalan)
