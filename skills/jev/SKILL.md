---
name: jev
description: "Jev (TypeSafe) tipli yargı: çok öğeli sınıflandırma/puanlama, kalibre olasılık, ikinci görüş. jev_* araçları, soru yazımı, güven bantları."
---

# Jev — tipli yargı aracı

Jev metin üretmez; `state` (yargılanan malzeme) + `questions` alır, her soruya tipli cevap döner:
`noul` (evet olasılığı 0-1) · `choice` (seçenek + `probabilities` + `confidence`) · `score` (seviyeler arası ağırlıklı değer + `legend` + `confidence`).

## Ne zaman çağır
- Çok öğeli sınıflandırma/puanlama (ticket, yorum, kayıt listesi) → `jev_batch` (≤200 state, aynı sorular).
- Kararın kalibre olasılığı gerekiyorsa (eşikle yönlendirme, sıralama).
- Kendi cevabına ikinci görüş / guardrail: "bu yanıt politikayı ihlal ediyor mu?" gibi dar evet/hayır.

## Ne zaman çağırma
- Tek seferlik muhakeme, açıklama, metin/kod üretimi — Jev üretmez.
- Sayma, aritmetik, tarih hesabı — kodla yap (Jev'in zayıf alanı, docs: model-jaggedness).
- Sır, anahtar, kişisel veri (KVKK): state üçüncü tarafa gider; ZDR yalnız kurumsal planda.
- Araç (jev_*) bağlı değilse: kendin karar ver, Jev'i taklit etme.

## Soru yazımı
- `state` = yargılanan malzeme. Soru yalnız `questions`'ta; state'e yazılan soru malzeme sayılır.
- Atomik ve literal: bir soru tek özelliği yargılar; geniş soruyu birkaç dar soruya böl, birleştirmeyi sen yap.
- State alanına backtick ile işaret et: "Does `message` ask for a refund?"
- Sınır durumlar `criteria`'da: noul `{true, false}`; choice `{seçenek: açıklama|null}` (≤255); score seviye dizisi (2-10).
- Bağımsız soruları tek istekte topla (paralel değerlendirilir).

## Güven (choice/score `confidence`; noul'da max(p, 1-p))
- ≥0.85 → Act: doğrudan uygula.
- 0.60-0.85 → Flag: uygula ama işaretle / ikinci soruyla doğrula.
- <0.60 → Escalate: kullanıcıya sor ya da kendin gerekçeli karar ver.
Kanıt (`jev kalibre`, n=40 sentetik TR, jev-1.13): Act 51 yargı · isabet 1.00 · Flag 22 · 0.86 · Escalate 7 · 0.43; doygunluk (≥0.999) 0.29, sınır durumda 0.21. CLI bantları `~/.config/jev/bantlar.json`'dan okur. Yalnız en iyi seçenek lazımsa eşik koyma, `choice`'u al.

## Ömer haritası
- CC: `jev log <dosya> [--diff a,b]` (test/derleme hatası sınıfı) · `jev ilgili "<soru>" <yol...>` (graphify adaylarından ilk-k aralık) · `jev triage <json>` (semgrep/gitleaks/SARIF/SkillSpector/axe).
- Desktop (cc-kopru `komut`): `jev kanit <rapor> <kanit...>` (iddia-kanıt denetimi) · `jev tarama <aday.json>` (çift/izin/bakım sıralaması) · tek seferlik soru için `jev_evaluate`.
- Yalnız Escalate satırları ve ilk-k aralıklar açılır, gerisi context'e girmez.
- Ne zaman değil: malzeme zaten context'teyse, kod doğruluğu sorusunda, final KABUL/DUR kararında. Jev işaretler, karar ajanda kalır.

## Türkçe
Canlı ölçüm (2026-09-22, jev-1.13, 3 Türkçe müşteri mesajı, choice/3 seçenek): Türkçe soru+criteria 3/3 isabet, ort. güven 1.00; İngilizce soru+criteria 3/3, ort. güven 1.00.
Soru dili fark yaratmadı; Türkçe state güvenle yargılanıyor. Örnek küçük — kritik akışta kendi etiketli setinle eşik ayarla.

## Referanslar
- `references/api.md` — iki backend tel biçimi, sınırlar, hatalar.
- `references/kaliplar.md` — fan-out · confidence routing · composite scoring · intent routing.
- `references/cli.md` — `jev` alt komutları, birer örnek satır.
- `references/dotnet.md` — .NET HttpClient örneği.
