"""ENVANTER-3 plan-kur: iş tarifinden TEK koşuda plan girdisi — iş türü kapıları + inceleme ajanları + konsey noktası
+ faz jeton bütçesi + katalog adayları + öğrenimler (~≤5k jeton). Model bunu okuyup ≤40 satır planı yazar; ek sorgu yok.
python tools/plan_kur.py "<iş 1>" ["<iş 2>" ...]   (birden çok iş tek komutta)
Rutin tek alanlı işte kısa çıktı: ENVANTER-6'da rutin işte katalog kazancı 0, maliyeti var.
ENVANTER-4 tarifleri (tarifler/*.md) varsa iş türü bölümü tariften gelir, yoksa aşağıdaki TUR tablosundan.
"""
import re
import sys
from pathlib import Path

B = Path(__file__).resolve().parent
for _p in (B, B.parent / "yetenek-getir", B.parent / "tools"):  # skill kurulumu (~/.claude/skills/plan-kur) + repo
    sys.path.insert(0, str(_p))
import katalog_ara as ka  # noqa: E402

TARIF = next((d for d in (B / "tarifler", B.parent / "docs" / "katalog" / "tarifler") if d.is_dir()), None)
N_ADAY, N_TABAN = 50, 5  # ~3k jeton: ENVANTER-6 B' ekinin (80+10) kısası; toplam ≤5k
# ENVANTER-3 3d incelemesi: skill-debate / council-multi-model codex·agy CLI ister (kurulu değil) → önerilmez
KONSEY = ("Konsey VARSAYILAN YOK — yalnız geri dönüşü zor VE belirsiz (iki makul seçenek, veri yok) kararda en çok 1; "
          "değilse planda tek satır 'konsey: yok — <gerekçe>' (kör kapı: gereksiz konsey uygulanabilirlikten düşer). Seçenekler: ecc:council (Skeptic·Pragmatist·Critic alt ajanları + sentez, "
          "Claude personaları, ücretli API 0, ~60-90k); hafif karar: consciousness-council (tek model, ~10-20k); ücretsiz harici görüş: "
          "octo:skill-council --providers claude,openai-compatible --depth quick --max-cost (OmniRoute Gemini; önce --dry-run) — "
          "Claude aboneliği OmniRoute'tan geçmez.")
KAPANIS = ("Kapanış (6): test yeşil · semgrep · gitleaks · a11y (UI: axe-core) · kanıt (UI: 3 genişlik ekran görüntüsü; "
           "diğer: çıktı/log) · rapor commit·test·CI·sapma (docs/kapanis-araclar.md)")
# tür: (tanıma deseni [TR→ASCII küçük harf], kapılar, inceleme ajanları aşama:ajan, konsey kararı, faz jeton bütçesi)
TUR = {
    "web": (r"\bsite|landing|web|sayfa|frontend|arayuz|\bui\b|seo|awwwards|e-?ticaret|magaza",
            "tasarım: frontend-craft > impeccable > ui-ux-pro-max · test: qa-e2e-playwright (Chrome) · a11y: qa-erisilebilirlik-testi · "
            "SEO: fe-meta-seo-duzeltici · güvenlik: semgrep · gitleaks · strix · ZAP · sec-owasp-top10 · sec-guvenlik-baslik · "
            "KVKK (form/çerez): sec-kvkk-gdpr-kontrol · performans: Lighthouse/CWV sayısal bütçe (LCP, JS KB tavanı) · "
            "yayın: önizleme + geri alma adımı",
            "tasarım sonrası: fe-tasarim-incele · UI Finish-Gate Reviewer · kod: ecc:code-reviewer · güvenlik: ecc:security-reviewer",
            "tasarım yönü / yığın seçimi", "araştırma 15k · tasarım+uygulama 50k · test+güvenlik 12k · kapanış 3k"),
    "dotnet": (r"\.net|dotnet|asp\.?net|c#|csharp|ef ?core|blazor|minimal api|\bapi\b|endpoint|backend",
               "test: dn-xunit-test-yazar (rtk dotnet test) · güvenlik: semgrep · gitleaks · sec-api-guvenlik · sec-owasp-top10 · "
               "auth: dn-identity-auth · sec-jwt-denetci · veri: dn-efcore-migration (geri alınabilir) · KVKK (kişisel veri): sec-kvkk-gdpr-kontrol",
               "her PR: ecc:csharp-reviewer · güvenlik: ecc:security-reviewer · mimari: inc-mimari-inceleme",
               "veri modeli / auth yaklaşımı", "tasarım 8k · uygulama 35k · test 12k · güvenlik 8k · kapanış 3k"),
    "oyun": (r"oyun|game|roblox|unity|godot|three\.?js|multiplayer|cok oyunculu|seviye|dusman",
             "test: oynanış senaryosu + qa-e2e-playwright (web oyunu) · denge: oyn-oyun-denge · performans: kare süresi ölçümü · "
             "ağ: oyn-ag-senkronu (çok oyunculuysa) · güvenlik: semgrep · gitleaks",
             "kod: ecc:code-reviewer · tasarım: oyn-oyun-dokuman ile kapsam kontrolü",
             "mekanik / ağ modeli", "tasarım 8k · uygulama 40k · test+denge 12k · kapanış 3k"),
    "blender": (r"blender|3d|glb|gltf|render|mesh|model(leme)?\b|sahne|turntable|doku\b",
                "headless (-b) · doğrulama: tools/blender/lib dogrula · bl-gorsel-ani-kontrol (normal, manifold, doku) · "
                "web ise: bl-glb-disa-aktar + GLB boyut/mesh ölçümü · görsel kanıt: render karesi",
                "sahne: bl-sahne-temizlik · web entegrasyonu: fe-webgl-3d-hero",
                "modelleme yaklaşımı / poly bütçesi", "plan 6k · bpy betik 30k · doğrulama 8k · kapanış 3k"),
    "video": (r"video|reels?|shorts|tiktok|ffmpeg|kurgu|altyazi|youtube|instagram|remotion|hyperframes",
              "teknik: vid-ffmpeg-donusturucu · renk: vid-renk-uzayi · ses: vid-ses-duzeni (loudness) · kare kanıtı: vid-kare-cikarici · "
              "telif/lisans kontrolü · platform biçimi: vid-sosyal-video-bicim",
              "ritim: vid-gecis-ve-ritim · otomasyon kodu: ecc:code-reviewer",
              "araç seçimi (Remotion/HyperFrames/ffmpeg)", "brief 5k · üretim 30k · kontrol 8k · kapanış 3k"),
    "otomasyon": (r"otomasyon|automation|n8n|zamanla|cron|webhook|bot|entegrasyon|pipeline|hatt|toplu|batch|playwright",
                  "kuru koşu (--kuru) + idempotent · hata yolu: otm-n8n-hata-yonetimi / be-dayaniklilik-kaliplari · sır: sec-sir-tarayici · gitleaks · "
                  "zamanlama: otm-zamanlanmis-gorev (kilit + log) · ücretli çağrıya sayısal tavan",
                  "üretim öncesi: inc-uretim-hazirligi · kod: ecc:code-reviewer",
                  "tetik / kuyruk mimarisi", "tasarım 6k · uygulama 25k · kuru koşu+test 10k · kapanış 3k"),
    "guvenlik": (r"guvenlik|pentest|saldiri|zafiyet|owasp|xss|csrf|injection|sizma|security",
                 "SAST: semgrep (sec-sast-kosucu) · sır: gitleaks (sec-gitleaks-gecmis) · DAST: ZAP · ajan pentest: strix · "
                 "bağımlılık: sec-bagimlilik-acik · rapor: sec-guvenlik-raporu · yetkili kapsam: sec-pentest-plani · "
                 "tehdit modeli: sec-tehdit-modelleme · ödeme: sec-pci-dss-kapsam · yetki: sec-yetkilendirme-matrisi · "
                 "yayındaki sitede DAST yalnız yazılı izin + staging ya da hız tavanı",
                 "bulgu triyajı: ecc:security-reviewer · differential-review:adversarial-modeler (yüksek risk)",
                 "risk önceliği / kapsam", "plan 6k · tarama 15k · triyaj 12k · rapor 5k"),
}
ZOR = re.compile(r"guvenlik|odeme|auth|kimlik|giris|kvkk|gdpr|yayin|deploy|canli|production|multiplayer|cok oyunculu|awwwards|"
                 r"migration|gecis|olcek|entegrasyon|bastan|yeniden yap|sifirdan|uctan uca")


def turler(t):
    return [k for k, v in TUR.items() if re.search(v[0], t)]


def tarifler(q):
    """En uygun 1–2 ENVANTER-4 tarifi (ikincisi tepe puanın %60'ını geçerse; çok alanlı iş)."""
    if not TARIF:
        return []
    rows = [{"ad": f.stem, "tur": "tarif", "is": f.read_text(encoding="utf8").split("\n", 2)[1], "tetik": "", "durum": "",
             "metin": f.read_text(encoding="utf8"), "yol": f} for f in sorted(TARIF.glob("*.md"))]
    p = ka.puanla(q, None, rows)[0]
    return [o["yol"] for s, _, o in p[:2] if s >= 0.6 * p[0][0]]


def plan_girdisi(q, n_aday=N_ADAY):
    t = q.lower().translate(ka.TR)
    tr = turler(t)
    if len(tr) <= 1 and not ZOR.search(t) and len(t.split()) < 20:
        k = TUR[tr[0]][1].split(" · ")[0] if tr else "test yeşil"
        print(f"RUTİN ({tr[0] if tr else 'genel'}): plan-kur gereksiz — doğrudan uygula; kapı: {k}; kapanış raporu commit·test·sapma.")
        return
    tf = tarifler(q)
    for f in tf:  # tarif varsa iş türü bölümü ondan (ENVANTER-4)
        print(f"<tarif {f.stem}>\n" + f.read_text(encoding="utf8").split("\n", 1)[1].strip() + "\n</tarif>")
    if not tf:
        for k in tr or ["web"]:
            _, kapi, ajan, karar, butce = TUR[k]
            print(f"## {k}\nkapılar: {kapi}\ninceleme ajanları: {ajan}\nkonsey adayı (yalnız belirsizse): {karar}\njeton (tahmini): {butce}")
    print(KONSEY + "\n" + KAPANIS)
    ka.listele(ka.aday(q, n_aday, taban=N_TABAN) + ka.ogrenim_ara(q))


def main():
    isler = [a for a in sys.argv[1:] if not a.startswith("--")]
    print("plan-kur: planı ≤40 satır yaz — faz · adım · araç · kapı · inceleme ajanı · konsey noktası · faz jetonu; "
          "listede ilgili olup kullanılmayan araca tek satır gerekçe. Ek katalog sorgusu yapma.")
    # CC 30k karakteri aşan Bash çıktısını dosyaya yazar → parça parça Read, her tur ~66k önbellek (ENVANTER-3 B 0: +2 tur)
    n_aday = max(20, N_ADAY * 2 // max(2, len(isler)))
    for n, q in enumerate(isler, 1):
        print(f"\n# İŞ {n}: {q}")
        plan_girdisi(q, n_aday)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
