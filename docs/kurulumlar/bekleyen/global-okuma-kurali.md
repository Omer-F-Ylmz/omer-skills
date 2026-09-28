# global-okuma-kurali

hedef: ~/.claude/CLAUDE.md (1.3k tavanı; yeni satır açılmaz, birleştirilir)
karar: Ömer onayı bekler — KOŞULMAZ

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
