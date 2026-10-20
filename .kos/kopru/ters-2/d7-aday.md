# TERS-2 d7 — held-out ADAY listesi + ground truth TASLAĞI

Durum: ADAY. hedefler.json'a yazılmadı, koşu yok. d6'da kullanılan 13 hedef (7 site, ink-puppet, markdown-table, ortak-js, Fiyat, Fiyat.Tests, Halka) listede yok.
Not: `rea analyze-javascript-application` tek dosya kabul etmiyor (unsupported_target; yalnız dizin/.asar) → js adayları için `yol` dizin olmalı ya da js REA'sız koşulmalı; düzeltilmiş koşucu bunu hata sayıp durur.

## 5 js (ayrıca dizin/kaynak seçimi gerekir)
1. `uygulamalar/openmontage/ink-theater/ink-theater.js` (15.8K; ink-puppet'ın üst modülü)
2. `tools/cc-kopru/hook.mjs` (17.2K)
3. `tools/cc-kopru/sunucu.mjs` (27.4K)
4. `uygulamalar/colibri/web/src/lib/cortex.ts` (9.6K)
5. `uygulamalar/colibri/web/src/lib/transcript.ts` (2.3K) — küçük/kolay; yerine `images.ts` (5.2K) olabilir

## 4 .NET
1. `templates/jev-dotnet/Jev/bin/Debug/net10.0/Jev.dll` — derlenmiş, TASLAK aşağıda
2. `templates/jev-dotnet/Jev.Tests/bin/Debug/net10.0/Jev.Tests.dll` — derlenmiş
3. `.tmp-kurulum6c/openclaw-windows-node/src/OpenClaw.Shared` (81 .cs) — dll YOK, önce derlemek gerek; LICENSE MIT/Apache geçer (başlıkta eşleşti, doğrulanmalı)
4. `.tmp-kurulum6c/openclaw-windows-node/src/OpenClaw.Connection` (56 .cs) — dll YOK, derleme gerek
Kod tabanında derlenmiş yalnız 2 yeni dll var; 3-4 derleme (build) onayı ister, yoksa yedek: `rea/tests/fixtures/nativeaot` (1 .cs).

## 3 site (prob karesi std ≥ 10 HENÜZ doğrulanmadı)
1. `labs/cok-sahne/index.html`
2. `skills/animasyon-atolyesi/tarifler/giris-scroll.html`
3. `skills/animasyon-atolyesi/tarifler/sayfa-gecisi.html`
Koşucunun sunucusu `/labs` altından sunuyor; 2-3 için `sayfa` yolu/kök ayarı gerekir. Önce prob ile kare std'sini ölç (çağrısız); düz çıkan yerine `parcacik-three.html`.

## Ground truth TASLAĞI — Jev.dll (dotnet; kaynak: templates/jev-dotnet/Jev/*.cs, hepsi Read ile doğrulandı)
Kaynak yolları `C:/Projeler/omer-skills/templates/jev-dotnet/Jev/` altında. Soru: "Jev istemci kütüphanesi redaksiyon, tavan ve güven bantlarını nasıl uyguluyor?"

1. **İstek yolu tek boğaz noktası: önce tavan kontrolü, sonra TR redaksiyonu, sonra ek redactor'lar.** `JevClient.cs` satır 60-61: `state = TurkishRedactor.Instance.Redact(state);` / `foreach (var r in _extra) state = r.Redact(state);` (tavan: satır 38-41 `JevLimitException`).
2. **Tavanlar JevOptions varsayılanlarında sabit:** MaxBatches 5, MaxRequests 250 (tekrarlar dahil), ChunkSize 200, MaxConcurrency 8, Retries 2. `Models.cs` satır 18-22: `public int MaxBatches { get; set; } = 5;` … `public int MaxConcurrency { get; set; } = 8;`
3. **Yeniden deneme yalnız 408/429/≥500'de, üstel geri çekilmeyle (Retry-After öncelikli); anahtar yalnız Authorization başlığında.** `JevClient.cs` satır 73: `var retryable = response.StatusCode is HttpStatusCode.RequestTimeout or HttpStatusCode.TooManyRequests || code >= 500;` satır 76: `TimeSpan.FromMilliseconds(500 * Math.Pow(2, attempt))`.
4. **TurkishRedactor 6 örüntü sırayla maskeler (anahtar, iban, kart, tckn, telefon, e-posta); kart yalnız Luhn doğrulanırsa.** `Redaction.cs` satır 18: `("anahtar", Key()), ("iban", Iban()), ("kart", Card()), ("tckn", Tckn()), ("telefon", Phone()), ("e-posta", Email()),` ; satır 24: `m => kind != "kart" || Luhn(m.Value) ? $"[REDAKTE:{kind}]" : m.Value`.
5. **Güven bantları: Act ≥0.85, Flag ≥0.60, altı Escalate; noul tipinde kesinlik max(p, 1−p).** `JevBands.cs` satır 11: `a.Type == "noul" ? Math.Max(a.Noul ?? 0, 1 - (a.Noul ?? 0)) : a.Confidence ?? 0;` satır 13: `certainty >= act ? Band.Act : certainty >= flag ? Band.Flag : Band.Escalate`.

Bileşen ayrımı: (1) akış sırası · (2) sabit/veri tablosu · (3) dış bağımlılık/HTTP davranışı · (4) tür/örüntü envanteri · (5) sınır/eşik durumu. Dondurma: skill değişikliğinden önce; yeni hedeflerin geri kalan 11'i için aynı Read-doğrulama gerekir (bu taslak yalnız 1/12).
