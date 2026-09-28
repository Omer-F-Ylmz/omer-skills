# global-okuma-kurali

hedef: ~/.claude/CLAUDE.md (1.3k tavanı; yeni satır açılmaz, birleştirilir)
karar: Ömer onayı bekler — KOŞULMAZ
uygulandı: 2026-09-28 (Ömer onayı, VİDEO-PARTİ-D-DEVAM-3) — "Exploration" satırına eklendi; yedek CLAUDE.md.bak-okuma; ~971 → ~1005 token (karakter/3.53 tahmini, /context ölçülmedi: claude -p 0).

## Önerilen birleşme
CONTEXT DISCIPLINE altındaki "Exploration: …" satırının sonuna eklenir:

> Exploration: graphify query first, then `jev ilgili`; big logs/scans: `jev log|triage <file>` first; open only evidence lines, Escalate/top-k rows; file content only via Read with a narrow line range (~20 lines), never Bash cat/sed/head/tail/awk or grep -A/-B/-C dumps.

Ek uzunluk: ~120 karakter.

## Gerekçe
- headroom Bash çıktısını sıkıştırır → okuma başına ~3 çağrı (döküm → okuma → headroom_retrieve); VİDEO-PARTİ-D-DEVAM 45 turu buna harcadı.
- 28 Eyl ölçümü: Read de sıkışıyor (574 kelime → 432, 271 → 191, 224 → 177 kelimede işaretli); ~14-20 satırlık Read sıkışmadı. Yani kural "Read + dar aralık"tır, "Read sıkışmaz" değil.
- Önceki oturumun "okumaları tek dosyada topla" dersi geçersiz: toplu Bash çıktısı yine sıkışır.

## Proje karşılığı
omer-skills/CLAUDE.md'ye aynı kural tek satır olarak eklendi (VİDEO-PARTİ-D-DEVAM-2).
