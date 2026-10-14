"""PLAN-KUR-3 plan-kur v3: iş tarifinden TEK koşuda kompakt plan girdisi (zor işte ≤6k karakter, katalog_ara listesinin YERİNE).
katalog_ara sırasıyla ilk K KURULU ve yığınla uyumlu aday (alan uzmanı önde, fazsız; seçimi model yapar) · faz başına sayısal kapı · inceleme ajanı · konsey (varsayılan yok) · ≤3 öğrenim.
python tools/plan_kur.py "<iş 1>" ["<iş 2>" ...]   (birden çok iş tek komutta)
python tools/plan_kur.py --ac <ad>                 (tek aracın ayrıntısı; çoğu işte gerekmez)
Rutin tek alanlı işte tek satır: ENVANTER-6'da rutin işte katalog kazancı 0, maliyeti var.
Çıktı deterministik (aynı iş → bayt bayt aynı), sabit başlık en üstte: önbellek dostu.
"""
import json
import re
from collections import Counter
from functools import cache
import sys
from pathlib import Path

B = Path(__file__).resolve().parent
for _p in (B, B.parent / "yetenek-getir", B.parent / "tools"):  # skill kurulumu (~/.claude/skills/plan-kur) + repo
    sys.path.insert(0, str(_p))
import katalog_ara as ka  # noqa: E402

K = 43  # aday sayısı: uzman@43 ≈ 0.9×havuz tavanı, zor işte ≤6k kr (PLAN-KUR-3 K eğrisi: .claude/plankur3/k_egrisi.py)
VARLIK_DF = 8  # bir sözcük en çok bu kadar kaydın adında geçiyorsa alan/teknoloji adıdır
GENEL = set("uygulama uygulamasi sunucu sunucusu tasarim tasarimi tasarla design app server sistem sistemi kur kurulum "
            "yap ekle yeni mevcut olustur gelistir site sayfa proje araci arac hizmet servis".split())
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
              "araç seçimi (kurulu video skill'leri / ffmpeg)","brief 5k · üretim 30k · kontrol 8k · kapanış 3k"),
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
# araç → faz (ad + iş metninde ilk eşleşen; hiçbiri değilse uygulama). Sıra: test önce (tasarım kelimesi taşıyan test araçları)
FAZ_AD = {1: "faz 1 tasarım", 2: "faz 2 uygulama", 3: "faz 3 test+güvenlik", 4: "faz 4 yayın+kapanış"}
# sayısal kapılar: (iş deseni, faz, kapı). ENVANTER-3 kör yargıç: sayısal kapı yoksa sağlamlık en çok 1
KAPI = (
    (r"tasi|gecis|migration|kademeli|geriye donuk", 1,
     "geçiş: her adım geri alınabilir · eski/yeni paralel, parite testi %100 · sözleşme testi kırmızıysa yayın yok"),
    (r"odeme|payment|stripe|iyzico|kapora|fatura|abonelik|checkout|billing", 2,
     "ödeme: idempotency anahtarı her ödeme/iade isteğinde · 3DS/SCA · PCI SAQ-A (kart verisi sunucuya değmez, barındırılan alan) · "
     "webhook imza doğrulama + olay kimliğiyle tekil işleme · yeniden deneme tavanı 3, üstel bekleme"),
    (r"kvkk|gdpr|riza|kisisel veri|aydinlatma", 2,
     "KVKK: aydınlatma metni + ayrı, önceden işaretsiz açık rıza kutusu · saklama süresi yazılı · silme talebi ≤30 gün"),
    (r"auth|kimlik|giris|login|jwt|oturum|firebase", 2,
     "auth: erişim jetonu ≤15 dk + yenileme jetonu döndürme · giriş hız sınırı 5 deneme/dk · sırlar ortam değişkeninde"),
    (r"graphql|\brest\b|\bapi\b|endpoint", 2,
     "API: p95 ≤300 ms · hız sınırı 100 istek/dk/anahtar · GraphQL derinlik ≤7 + karmaşıklık tavanı · istek başına DB sorgusu sabit (N+1 yok)"),
    (r"sms|e-?posta|email|bildirim|push|hatirlatma", 2,
     "ücretli gönderim: günlük tavan (sayı yaz) + tekrar önleme anahtarı · gönderim günlüğü"),
    (r"site|web|sayfa|frontend|dashboard|panel|landing|vue|react|astro|svelte|htmx|lighthouse", 3,
     "web: LCP ≤2.5 s · CLS ≤0.1 · INP ≤200 ms · ilk yük JS ≤170 KB gz · qa-erisilebilirlik-testi 0 ciddi ihlal"),
    (r"flutter|mobil|android|\bios\b|cevrimdisi|offline|senkron", 3,
     "mobil: çevrimdışı→çevrimiçi çakışma testi (2 cihaz eşzamanlı yazım) · soğuk açılış ≤2 s · izin reddinde zarif düşüş"),
    (r"\brag\b|llm|vektor|embedding|soru-cevap|chatbot|\bbot\b", 3,
     "LLM: değerlendirme seti ≥50 soru · kaynak gösterim doğruluğu ≥%90 · yanıt p95 ≤5 s · bağlam/VRAM tavanı yazılı"),
    (r"oyun|game|unity|godot|unreal", 3,
     "oyun: 60 fps (kare ≤16.7 ms) · kaydet→yükle tur testi aynı durum · hedef platform yapısı uyarısız derlenir"),
    (r"regresyon|\bci\b|kapisi", 4, "CI kapısı: bütçe aşımı kırmızı (paket +%5, LCP +%10)"),
    (r"yayin|deploy|vps|docker|canli|production|steam|magaza|\bstore", 4,
     "yayın: staging/önizleme önce · sağlık kontrolü · geri alma ≤5 dk ve adımı yazılı"),
)
SABIT = {3: "test yeşil · semgrep 0 yüksek · gitleaks 0 bulgu", 4: "Kapanış (6): test · semgrep · gitleaks · a11y · kanıt · rapor commit·test·CI·sapma"}
INCELE = re.compile(r"review|incele|denetci")
KONSEY = ("Konsey: yok — adımlar geri alınabilir; yalnız geri dönüşsüz VE iki makul seçenekli (veri yok) kararda "
          "ecc:council 1 kez (~60-90k)")
BASLIK = ("plan-kur v3: planı ≤30 satır yaz — faz · adım · araç · sayısal kapı · inceleme ajanı · konsey · faz jetonu. "
          "Araçları aşağıdaki adaylardan işe uyanlarla SEN seç (hepsi kurulu, yığınla uyumlu, alan uzmanı önde; ilgisizi kullanma); listede yoksa yalnız kurulu bildiğin aracı ekle; kurulmamışı/kurulumu önerme, ek sorgu yapma; kurulmamış kayıtla aynı adlı çerçeveyi araç diye yazma, kurulu sarmalayıcıyı yaz. "
          "Çağrı: skill → Skill <ad> · ajan → Agent <ad> · mcp → ToolSearch · cli → Bash. Ayrıntı nadiren: plan_kur.py --ac <ad>")


def kayitlar():
    return [json.loads(s) for s in ka.KATALOG.read_text(encoding="utf8").splitlines()]


def kurulu_disi_adlar():
    """Kurulu olmayan kayıtların (kurulu bir adla çakışmayan) ad sözcükleri: öğrenim metninde geçerse öğrenim gösterilmez."""
    rows = kayitlar()
    var = {w for o in rows if ka.kurulu(o) for w in re.findall(r"[a-z0-9][a-z0-9.+-]{3,}", o["ad"].lower())}
    return {w for o in rows if not ka.kurulu(o) for w in re.findall(r"[a-z0-9][a-z0-9.+-]{4,}", o["ad"].lower())} - var


@cache
def tam_ad_re():
    """Kurulu olmayan TAM katalog adları (kurulu adla çakışmayan; tek sözcüklü ≤4 harf gürültü): PLAN-KUR-3 sert kapısıyla aynı tanım."""
    rows = kayitlar()
    kur = {o["ad"].lower() for o in rows if ka.kurulu(o)}
    yok = {o["ad"].lower() for o in rows if not ka.kurulu(o) and (len(o["ad"]) > 4 or "-" in o["ad"] or ":" in o["ad"])} - kur
    return re.compile(r"(?<![\w:-])(" + "|".join(map(re.escape, sorted(yok, key=len, reverse=True))) + r")(?![\w-])", re.I)


def kisa(o, n=60):
    # kurulu aday açıklamasındaki kurulmamış kayıt adı (ör. "Export a <çerçeve> video") modele araç adı olarak sızmasın
    m = " ".join(tam_ad_re().sub("", o["is"] or o["metin"]).split())
    return m if len(m) <= n else m[:n].rsplit(" ", 1)[0] + "…"


def ad_sozcukleri(ad):
    return set(re.split(r"[^a-z0-9]+", ad.lower()))


def varliklar(q):
    """İş metnindeki teknoloji/alan adları: katalogda az kaydın ADINDA geçen, genel olmayan sözcük (graphql, jwt, unity)."""
    df = Counter(w for o in kayitlar() for w in ad_sozcukleri(o["ad"]))
    return {w for w in re.findall(r"[a-z0-9]{2,}", q.lower().translate(ka.TR))
            if w not in GENEL and w not in ka.DURAK and 0 < df[w] <= VARLIK_DF}


def adaylar(q, kal, k=K):
    """katalog_ara sırası (A ile aynı BM25 + tür tabanı) → alan uzmanı (ad varlık eşleşmesi) öne → ilk k, fazsız; seçimi model yapar."""
    vr, gor, tek = varliklar(q), set(), []
    for o in kal:
        if not o["ad"].endswith("-paket") and kisa(o) not in gor:  # şemsiye paketler ve aynı açıklamalı kopyalar dışarıda
            gor.add(kisa(o))
            tek.append(o)
    return sorted(tek, key=lambda o: not (ad_sozcukleri(o["ad"]) & vr))[:k]  # sorted kararlı: grup içinde BM25 sırası


def havuz(q, yg):
    """katalog_ara A listesi (ADAY + tür tabanı) + adı iş varlığıyla eşleşen kurulu kayıtlar → tür/yığın/kurulu süzgeci."""
    p = ka.aday(q)
    vr, var = varliklar(q), {o["ad"] for o in p}
    p += [o for o in kayitlar() if o["ad"] not in var and ka.kurulu(o) and ad_sozcukleri(o["ad"]) & vr]
    return ka.suz([o for o in p if o["tur"] in ("skill", "ajan", "mcp", "cli")], yg)


def plan_girdisi(q, k=K):
    t = q.lower().translate(ka.TR)
    tr = [k for k, v in TUR.items() if re.search(v[0], t)]
    if len(tr) <= 1 and not ZOR.search(t) and len(t.split()) < 20:
        k = TUR[tr[0]][1].split(" · ")[0] if tr else "test yeşil"
        print(f"RUTİN ({tr[0] if tr else 'genel'}): plan-kur gereksiz — doğrudan uygula; kapı: {k}; kapanış raporu commit·test·sapma.")
        return
    yg = ka.yigin(q)
    kal, elen, yok = havuz(q, yg)
    secim = adaylar(q, kal, k)
    ince =["ecc:code-reviewer (her faz sonu)", "ecc:security-reviewer (faz 3)"]
    ince += [o["ad"] for o in kal if o["tur"] == "ajan" and INCELE.search(o["ad"]) and not any(o["ad"] in i for i in ince)][:1]
    kapi = {n: [k for d, f, k in KAPI if f == n and re.search(d, t)] for n in FAZ_AD}
    for n, k in SABIT.items():
        kapi[n].append(k)
    yasak = kurulu_disi_adlar()
    ogr = [o for o in ka.ogrenim_ara(q) if not any(re.search(rf"\b{re.escape(w)}\b", o["ne"].lower()) for w in yasak)][:3]
    print(f"yığın: {', '.join(yg) or 'bilinmiyor'} · elendi: {elen} (yığın) · {len(yok)} kurulu değil (gösterilmez)")
    if adlar := sorted({m.lower() for m in tam_ad_re().findall(q)}):  # iş metni kurulmamış kaydı adlandırıyor: sarmalayıcıyı göster
        print(f"kurulu değil (iş metninde): {', '.join(adlar)} → planda bu adı tek başına yazma; kurulu sarmalayıcı: "
              + (" · ".join(o["ad"] for o in secim if any(w in o["ad"].lower() for w in adlar)) or "—"))
    print("<aday-listesi>\n```text")
    for o in secim:
        print(f"{o['ad']} · {o['tur']} · {kisa(o)}")
    print("```\n</aday-listesi>\nkapılar:")
    for n, v in kapi.items():
        print(f"  {FAZ_AD[n]}: " + (" ; ".join(v) or "—"))
    print("inceleme ajanları: " + " · ".join(ince))
    print(KONSEY)
    for o in ogr:
        print(f"öğrenim: {o['ne'][:160]} ({o['cagri']})")
    print(f"jeton (tahmini): {TUR[tr[0]][4] if tr else 'tasarım 8k · uygulama 35k · test+güvenlik 12k · kapanış 3k'}")


def ac(ad):
    r = [o for o in kayitlar() if ka.kurulu(o) and ad.lower() in o["ad"].lower()][:3]
    for o in r:
        print(f"{o['ad']} ({ka.GRUP[o['tur']]}) · {o['durum'][:40]} · çağrı: {o['cagri']}\n  {o['is']}\n  {o['metin'][:600]}")
    if not r:
        print(f"kurulu kayıt yok: {ad}")


def main():
    if "--ac" in sys.argv:
        return ac(sys.argv[sys.argv.index("--ac") + 1])
    isler = [a for a in sys.argv[1:] if not a.startswith("--")]
    print(BASLIK)
    for n, q in enumerate(isler, 1):
        print(f"\n# İŞ {n}: {q}")
        plan_girdisi(q)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
