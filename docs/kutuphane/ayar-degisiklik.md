# Ayar değişiklikleri (ölçümle)

Kural: her değişiklik önce A/B (tools/olcum, 12 görev), kalite ≥ taban ve jeton azalıyorsa uygulanır; yedek alınır, geri alma komutu yazılır.

## 2026-10-10 14:22 — skill listesi: name-only + bütçe 75000 (KÜTÜPHANE-4)

Değişen (~/.claude/settings.json, yalnız iki anahtar):
- `skillOverrides`: 1511 → 2355 anahtar (+844 `name-only`; mevcut 1511 değer ezilmedi). Açıklamalı kalanlar: 13 departman-* yönlendirici, frontend-craft · impeccable · frontend-design · ui-ux-pro-max · graphify · blender · pdf/docx/pptx/xlsx · omer-kutuphaneler · web-sahne-desenleri · sdp · surec · video-* · *-desktop ve diğer 42 çekirdek (tools/olcum/profil_uret.py KORU listesi).
- `env.SLASH_COMMAND_TOOL_CHAR_BUDGET`: 150000 → 75000.

Neden ikisi birlikte: CC listede her skill'in ADINI her zaman tutar; bütçe yalnız açıklamaları keser (en az kullanılandan başlayarak). 150k'da liste tavana dayalıydı (Skills 49.3k), name-only tek başına jeton düşürmedi. Bütçe düşünce name-only, açıklama payını yönlendiricilere ve çekirdeğe bırakıyor.

| ölçü | önce (tam) | sonra (nameonly75) | fark |
|---|---|---|---|
| /context Skills | 49.3k | 24.3k | −25.0k |
| /context toplam (boş klasör) | 91.4k | 67.4k | −26% |
| tek turlu görevde gerçek API bağlamı (ort., 6 görev) | 137.7k | 110.2k | −20% |
| 11 görev USD | 11.99 | 9.80 | −18% |
| kalite (rubrik, 11 görev toplamı /110) | 104 | 110 | ≥ taban |
| doğru araç isabeti (/11) | 9 | 10 | ≥ taban |

Karşılaştırma kolu `tam75` (yalnız bütçe): bağlam −20%, USD −14%, kalite 106, isabet 9 → name-only ile birlikte daha iyi. Ayrıntı: `docs/kutuphane/olcum/2026-10-10-karsilastirma.md`.

Uygulama: `python tools/olcum/ayar_uygula.py profil-nameonly-75k.json` (profil önce `profil_uret.py` + `profil_varyant.py` ile üretilir). Doğrulama: canlı ayarla `/context` → Skills 24.3k.
Geri alma: `python tools/olcum/ayar_uygula.py --geri` (yedek `~/.claude/settings.json.bak-k4-20261010-142258`).
Etkisiz: video runner'ın `claude -p` çağrıları (`--setting-sources ""`), claude.ai/Desktop sohbeti.

Not: rubrik regex tabanlı ve görev başına 1 koşu; fark gürültü içinde olabilir, ama düşüş yok. Sonraki koşular yanıt metnini `docs/kutuphane/olcum/<tarih>-<profil>/` altına yazar (jev ile yargıç karşılaştırması için).

## 2026-10-10 17:43 — ajan listesi: kullanılmayan 141 plugin ajanı gizlendi (KÜTÜPHANE-5, Ömer onayı)

Değişen: `permissions.deny` 7 → 148 (+141 `Agent(<plugin>:<ajan>)`; mevcut 7 kural aynen). Seçim `tools/olcum/ajan_kullanim.py`: CC transcript'lerinde son 60 günde 273 ajandan yalnız 1'i çağrılmış (feature-dev:code-explorer); 186 plugin ajanının 141'i gizlendi, adında code-reviewer · security · test · explore · plan · debug · build-error · csharp · dotnet · msbuild · frontend · a11y · performance geçen 45 plugin ajanı ve 87 kullanıcı/proje ajanının hepsi açık. Hiçbir plugin/ajan dosyası silinmedi; kural kaldırılınca ajan geri gelir.

| ölçü | taban (tam, sabah) | nameonly75 (canlı) | + ajan | fark (tabana göre) |
|---|---|---|---|---|
| tek turlu görevde gerçek API bağlamı (ort.) | 137.7k | 110.2k | 92.0k | −33% |
| 11 görev USD | 11.99 | 9.80 | 8.31 | −31% |
| kalite (rubrik /110) | 104 | 110 | 106 | ≥ taban |
| araç isabeti (/11) | 9 | 10 | 9 | = taban |

Gürültü kontrolü (aynı görev tekrarı): G01 rubrik canlı 10,10,8,8,10,8 · ajan 8,8,8,8,10,10,8; G10 canlı 10,10,8 · ajan 8,10,8; G06 isabeti iki kolda da çoğunlukla 0 (Bash ile npm/curl). LLM yargıç (jev-1.13, G01 4+4 yanıt, 1–10): ajan ort. 8.17 · canlı 8.27 (fark 0.10, tekil sapma ~0.15) → kalite eşit, düşüş yok.

Geri alma: `python tools/olcum/ayar_uygula.py --geri` (yedek `~/.claude/settings.json.bak-k4-20261010-174306`; bu yedek nameonly75'li hâli tutar).
