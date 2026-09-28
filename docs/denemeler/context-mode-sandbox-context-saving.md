# Deneme: context-mode-sandbox-context-saving

video v-vRYtvWDYs · 15 · bu dalgada koşulmaz (14b) · kurulum Ömer ONAY'ı ister (T2; Elastic-2.0: yönetilen hizmet olarak sunulmaz, lisans anahtarı atlatılmaz, telif bildirimleri silinmez)

## Hipotez
RTK + Headroom açıkken context-mode, MCP-ağır görevde (Playwright snapshot, büyük log, gh issue) ek girdi token tasarrufu sağlar; Bash-ağır görevde ek kazanç ~0 (Bash çıktısını RTK zaten kaynağında kısaltıyor).

## Metrik
girdi/çıktı token (K4 zorunlu) · görev başarısı (aynı kabul ölçütü) · geri getirme çağrısı sayısı (headroom_retrieve + FTS5 arama) · hook çakışma hatası sayısı

## Bütçe
en fazla 4 koşu: 2 görev (MCP-ağır · Bash-ağır) × 2 kol (A: RTK+Headroom · B: A + context-mode); toplam ≤200k token

## Geri alma
`claude plugin uninstall context-mode` + marketplace kaydını kaldır · ev dizinindeki context-mode SQLite'ını sil · settings.json hook girdileri kurulum öncesi yedekten

## Başarı eşiği
MCP-ağır görevde ≥%20 ek girdi token tasarrufu VE görev başarısı düşmez VE hook çakışması 0; biri tutmazsa RED

## Takas tablosu
| boyut | RTK | Headroom | context-mode |
|---|---|---|---|
| kapsam | Bash komut çıktısı | API isteğine giren tüm araç çıktıları | hook'ların yakaladığı araç çıktıları + ctx_execute sandbox |
| yer | PreToolUse: komutu `rtk <cmd>`'ye yeniden yazar | ANTHROPIC_BASE_URL vekili (istek anında) | MCP sunucusu + 6 hook (PreToolUse/PostToolUse/UserPromptSubmit/PreCompact/SessionStart/Stop) + SQLite/FTS5 |
| geri getirme | `rtk proxy` / recall | `headroom_retrieve` (hash) | FTS5 arama |
| sabit maliyet | yok | yok (yerel) | MCP araç açıklamaları context'e + SessionStart enjeksiyonu |
| durum | kurulu | kurulu | kurulu değil (T2, ONAY) |
| risk | düşük | alt süreçte araçları gizleyebilir (köprü notu) | sandbox'ta kod çalıştırma (dosya sistemi erişimi); ikinci Bash yeniden yazıcı |

## Headroom/RTK çakışma notu
- Aynı çıktılar mı: kısmen. Bash çıktısı üçünün de yolunda (RTK kaynağında kısaltır, context-mode PostToolUse'ta yakalayabilir, Headroom istekte yeniden sıkıştırır). MCP çıktısında (Playwright vb.) RTK yok; çakışma context-mode ↔ Headroom.
- Zincir sırası: araç → [PreToolUse: RTK yeniden yazma ∥ context-mode yönlendirme] → çıktı → [PostToolUse: context-mode özet] → transkript → Headroom (istek anı). Yani RTK (kaynak) → context-mode (hook/sandbox) → Headroom (taşıma).
- Riskler: iki PreToolUse Bash yeniden yazıcısının sırası tanımsız (RTK `rtk` önekiyle context-mode ctx_execute yönlendirmesi çakışabilir) · çift sıkıştırmada sinyal kaybı · iki ayrı geri getirme yolu (hash vs FTS5) · SessionStart'a yeni enjektör (claude-mem/ponytail/superpowers yanında; cowork aynı gerekçeyle kapatılmıştı).
- Deneme koşulursa: B kolunda context-mode'un Bash hook'u kapalı başlatılır (yalnız MCP çıktısı), çakışma ayrı ölçülür.
