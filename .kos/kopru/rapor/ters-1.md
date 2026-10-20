# TERS-1 d1 raporu
- REA = morluto/rea (npm rea-agents 6.7.0, MCP+CLI+skill). MIT, aktif (son push 20 Eki, sürüm 18 Eki), arşivli değil. Kaynak: docs/video-tarama/2026-10-09-ig-DeKHggujqWf.md.
- Tarama (repo temp'te, kurulum YOK): gitleaks 217 bulgu, hepsi docs/tests/experiments içinde `ownership_token`/fixture, kaynakta 0 (yanlış pozitif sayıldı, tek tek açılmadı). semgrep 32 (16 ERROR: detect-child-process build betikleri + src/process, 3 python defused-xml; araç Ghidra vb. süreç başlattığı için beklenen), HIGH gerçek bulgu yok.
- SkillSpector --no-llm (yalnız `.agents/skills/reverse-engineer-anything`): 16 MEDIUM, 0 HIGH madde (Prompt Injection 6, MCP Rug Pull 5, Rogue Agent 3, Excessive Agency 1, Memory Poisoning 1) ama toplam karar HIGH/skor 53/DO_NOT_INSTALL. Maddeleri tek tek doğrulamadım.
- KARAR: REA kurulmadı, onay betiği yazılmadı. Toplam karar DO_NOT_INSTALL; Ömer'in kuralı "HIGH → kurma". d2 için seçenek: 16 maddeyi okuyup gerçek/yanlış pozitif ayır, sonra `onay/ters_1_uygula.py`.
- Yazıldı: skills/tersine/SKILL.md (taslak, 3 ek kombin; departman skill'ine bağlanmadı), docs/ters/kapi-tasarim.md.
- YAPILMADI: mini denemeler (docs/ters/ornek-*.md), departman bağlantısı, zip/CC teslimi (iki taraf kuralı), test yok. Neden: 45 tur bütçesi taramalarda (clone/semgrep/SkillSpector zaman aşımı, ikisi yeniden koşuldu) bitti.
- RAM: %84 → %80 (eşik %85, tarayıcı hiç açılmadı). Tarama kalıntısı: %TEMP%\rea-tarama (silinmedi).
- Sapma: SkillSpector tüm repoda asılı kaldı, durdurup yalnız skill klasöründe koştum.

## d2
- SkillSpector 16 MEDIUM tek tek okundu: 2 gerçek (RP1 @latest ×5 satır, EA2 DMG mount), 10 yanlış pozitif; sınır tersine SKILL.md'de → docs/ters/rea-tarama.md.
- Mini denemeler: scroll-demo (kendi; TELVE/Portale bulunamadı) tam, yeniden kurulum farkı 0.041 (docs/ters/ornek-scroll-demo.md). thinking-orbs KISMİ: canlı prob boş, fark ölçülmedi (ornek-thinking-orbs.md).
- Bağlandı: departman-arastirma-ogrenme adım 4b → tersine.
- KAPI KOŞULMADI/BİTMEDİ: tur bütçesi (45) bitti. Hazır: tools/ters/probe.py, tools/ters/kapi_kos.py (skill vs zemin, hakem nemotron + groq llama/gemini, çağrı tavanı 60, önbellekli). Ground truth (10 hedef: 6 labs sayfası, 2 JS, 2 .NET Fiyat) alt ajanda `docs/ters/kapi/hedefler.json`'a yazılıyor; arka plan işi bitince kapi_kos.py'yi kendisi koşar → docs/ters/kapi/sonuc.md; günlük %TEMP%	ers-kapi2.log. Kapı SONUCU YOK, sayı yok.
- d3 ilk iş: hedefler.json'u doğrula (alıntılar dosyada var mı), sonuc.md varsa oku/yoksa kapi_kos.py'yi koş; karar eşiği kapi-tasarim.md. Zemin kolu aynı koşuda.
- Sapma: hedeflerin çoğu kendi repomuz (açık kaynak 0 hedef) → held-out ama tek kaynaklı; kanıt bileşeni skill kolunda prob çıktısını da korpus sayar. Yeniden kurulum bileşeni yalnız site hedeflerinde (6), diğerlerinde puan = ortalama(c1,c2). Lighthouse yok. Test/CI yok.
- Commit yalnız d2 dosyaları; push yok; %TEMP%ea-tarama silinmedi.
SIRA: TERS-1 d2 (kapı bekliyor)

## d3 (kapı BİTMEDİ — kapanış yapılmadı)
- Düzeltildi: statik sunucu kökü KOK + `/labs` önekiyle 404 yok (parcacik/metin/yukleyici Playwright headless: hata listesi boş). Eski `%TEMP%\ters-kapi` → `ters-kapi-eski-170403` (silme yok), sayaç/önbellek sıfırlandı.
- Zincir: OpenRouter :free → Groq → Haiku (tavan 30; havuz modülü başka oturumdan). OpenRouter günlük kota 429, Groq TPD 429, gemini 404/429/503; hakem ailesi google→minimax (OpenRouter), openai (Groq). Hakemsiz hedef artık 0 değil "ATLANDI" (puana girmez, kapı GEÇMEZ).
- Koşu 8. hedefte KeyError 'derlenmis' ile düştü (dotnet hedefin hedefler.json kaydında alan yok) → sonuc.md/json YAZILMADI; docs/ters/kapi/sonuc.md eski kuru deneme (1 hedef), geçersiz. Ham satırlar %TEMP%\ters-kapi6.log: 6 site hedefi puanlı; skill ort ~0.65, zemin ~0.69 (elle hesap, resmi değil); metin + markdown-table ATLANDI.
- Bulut çağrı 39/60, Haiku 12/30. Skill zip/departman/SIRA kapanışı YAPILMADI (kapı geçmedi/bitmedi).
- Öneri: hedefler.json dotnet kayıtlarına `derlenmis` ekle, kota sıfırlanınca (OpenRouter 00:00 UTC) tam koşu; skill kolu şu an zemini geçmiyor → SKILL.md kanıt bölümü gözden geçirilmeli.
SIRA: TERS-1 d3 (kapı geçmedi/bitmedi)

## d4 (20 Eki, kapanış denemesi)
- Düzeltme: `hedefler.json` dotnet kayıtlarına `derlenmis` eklendi; `kapi_kos.py` döngü gövdesi `hedef_kos()`'a alındı, hedef hatası koşuyu çökertmez (`hatalar` + atlanan) · test `tools/tests/test_ters_kapi_kos.py` 2/2. Zincir `ucretsiz_havuz` (1 hedef kuru deneme çalıştı). SKILL.md'ye "Kanıt satırı kuralı" (birebir alıntı) eklendi.
- KAPI GEÇMEDİ (tam koşu, 43/60 bulut çağrı, Haiku 0): skill 0.534 · zemin 0.527 (eşik ≥0.92). 2/10 hedef ATLANDI (gecis, Fiyat.Tests: model/tavan).
- Ölçülen kayıp sınıfları: (1) yazar fiilen ministral-8b (19/21 not; nvidia gpt-oss-20b 2) — zayıf yazar; (2) kanıt (alıntı birebir bulunur): skill 0.47 < zemin 0.70, yani kanıt eki alıntı tutarlılığını artırmadı; (3) mekanizma: skill 0.48, zemin 0.35; dotnet Fiyat skill 0.0/0.0; kamera-yolu skill 0.40/0.00; (4) atlanan hedef kuralı: 2 atlama tek başına kapıyı geçirmez.
- Neden kanıtı yok: yazar/hakem model gücü ile skill etkisi ayrışmıyor (fark skill−zemin +0.007, tek koşu). Kapanış (zip/departman/SIRA kapanışı) YAPILMADI.
- Öneri: yazar zincirinde ministral-8b yerine daha güçlü model (kota açılınca openrouter nemotron/gemma-4 ya da Haiku tavanı) ve atlanan 2 hedefi yeniden koşmak; eşik 0.92 bu zincirle ulaşılabilir görünmüyor — Ömer kararı.
SIRA: TERS-1 d4 (kapı geçmedi)
