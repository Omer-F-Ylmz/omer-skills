# KURULUM-11b — Desktop eşitleme (kapanış) · 20 Eyl 2026

Commit: `f9bb0af` (+ temizlik `1010248`). Bu belge 11b'nin kapanışıdır; docs bölümü
dalganın kendi bütçesinde düşmüştü, 11c'de yazıldı.

## Yapılanlar

- **K0 omniroute kaldırıldı** — Desktop ve CC config'lerinden çıkarıldı, 44 `omni-*`/`cli-*`
  skill `skillOverrides` ile kapatıldı. Yedek alındı.
- **K1 üç MCP teşhisi** — puppeteer · brave-search için dört hipotez de **elendi**:
  npx yolu (`cmd /c npx --version` → 11.17.0), eşzamanlı oturum (iki örnek de 8 araç),
  Chromium indirme (`puppeteer_navigate` → 200, isError:false), tırnaklı PATH (ikisi de çalıştı).
  Kök neden bulunamadı; karar satırı uydurulmadı — doğru davranış.
- **K3** slack tek deneme; jdk-17 tırnağı ayrı PATH-FIX oturumuna devredildi.
- **K4** frontend-craft 1.5.4 (Design varsayılanları), web-sahne description netleştirildi.
- **K5** claude-mem korpus katmanı: `omer-skills` 335 gözlemle kuruldu ve sorgulanabilir.
- **K6** kütüphane rafı: 2 kırık jsDelivr URL'i ESM uç noktasıyla düzeltildi, 3 paket üretildi.

## Sapmalar

1. **docs düştü** — bütçe bitti, belgeler yazılmadı. 11c'de kapatıldı (bu dosya).
2. **K2 hiç yapılmadı** — 7 CLI için Desktop paketi kararı 11c'ye devredildi.
3. **K5b boş korpus** — `divisima` ve `corvano` korpusları 0 gözlemle kuruldu.
   11c'de silindi; kök neden orada.
4. **Anahtar sızıntısı** — dalga sırasında `reg query` ortam değişkeni **değerlerini**
   transkripte yazdırdı. 11b kendi `dalga.md`'sine uyarı olarak düştü; temizlik 11c/K7.
5. `~/.claude.json` hash'i beklenmedik değişti (KABUL #6); sunucu listesi aynı kaldı,
   değişim iyi huylu sayıldı.
