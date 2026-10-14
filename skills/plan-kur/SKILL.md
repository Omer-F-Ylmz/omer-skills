---
name: plan-kur
description: Builds a robust plan for hard or multi-domain work in ONE catalog call - work-type gates (test, security, a11y/SEO, KVKK), review agents, council point, phase token budget, catalog tools and learnings. Use when the task spans 2+ domains, is out of domain, or the right tools are unknown. Not for routine single-domain tasks (zero gain, extra cost).
---

> DENEYSEL — kapı RET (rapor/envanter-3.md), kurulmaz. Otomatik kurulum/zip dışında; onay/envanter_3_uygula.py koşulmaz.

# plan-kur — zor işte sağlam plan (tek çağrı)

yetenek-getir'in üstünde. Rutin tek alanlı işte ÇAĞIRMA (ENVANTER-6: kazanç 0, her ek tur ~100k önbellek okuma).

## Ne zaman
- İş ≥2 alana yayılıyor (ör. pazarlama sitesi = tasarım + güvenlik + SEO + KVKK), alan dışı ya da aracın adını bilmiyorsun.
- Kritik/geri dönüşü zor karar içeren iş (konsey noktası gerekir).

## Nasıl
1. TEK komut (birden çok iş varsa hepsi aynı komutta):
   `python ~/.claude/skills/plan-kur/plan_kur.py "<iş tarifi>" ["<iş 2>" ...]`
   Çıktı (~≤5k jeton): iş türü kapıları · inceleme ajanları (hangi aşamada) · konsey seçenekleri · faz jeton bütçesi ·
   katalog adayları (türe göre) · ilgili öğrenimler (`ne · iş · kaynak`). Katalog: kardeş `yetenek-getir` klasörü.
2. Listeyi bir kez oku; EK SORGU YOK. Kısaltma notu (`compressed … hash=…`) varsa önce `headroom_retrieve`.
3. Planı ≤40 satır yaz: faz · adım · araç (skill/ajan/MCP/CLI, hangi adımda) · kapı · inceleme ajanı · konsey noktası (en çok 1) ·
   faz jeton bütçesi. İlgili olup kullanılmayan araç için tek satır gerekçe; öğrenimlerden işe uyanları adımlara göm.

## Kurallar
- Kurulu olmayan (`durum` aday) aracı kurma; planda "aday" diye an. `kapalı(override off)` olanı kullanıcıya söyle.
- Betik çıktısı ≤30k karakter kalır: CC satır içi sınırını aşan çıktı dosyaya düşer + ek Read turu (ENVANTER-3 d1: 5 tur/374k → d3: 3 tur/223k).
- Konsey varsayılan YOK: yalnız geri dönüşsüz ya da çok seçenekli kararda (yoksa planda "konsey: yok — gerekçe"; varsayılan konsey her zor işe ~70k ekledi, kör kapıda kaliteyi artırmadı); ücretli API 0 — harici model yalnız ücretsizse (OmniRoute), Claude aboneliği OmniRoute'tan geçmez.
- claude.ai (betik çalışmazsa): `yetenek-getir/yetenek.tsv` ve `yetenek-getir/ogrenim.jsonl` içinde iş sözcüklerini (TR+EN) geniş grep'le,
  kapıları şu sırayla yaz: test → güvenlik (semgrep · gitleaks · OWASP paketleri) → a11y/SEO → KVKK → kapanış listesi.
