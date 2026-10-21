# makara-bulut (SLEEP-3 şablonu)

PC kapalıyken gece koşusu: GitHub Actions, ücretsiz havuz, Claude 0. Bu klasör ayrı ÖZEL repoya kopyalanır (omer-skills'e bağlı değil).

Ömer'in adımları:
1. Özel repo aç (öneri: `omer-makara-bulut`), bu klasörün içeriğini köke koy (`.github/workflows/gece.yml`).
2. Actions secret ekle (değerler yalnız GitHub'da): `GEMINI_API_KEY` · `GROQ_API_KEY` · `OPENROUTER_API_KEY` · `MISTRAL_API_KEY` · `NVIDIA_API_KEY` (en az 2 farklı aile yeter).
3. PC'de `python tools/makara_paket.py` → `.kos/makara/paket/` içeriğini repo köküne kopyala, commit + push (push onayı sende). Dönüş: `MAKARA_BULUT_REPO=sahip/ad` ortam değişkeni, `python tools/makara_cek.py kur` (saatlik, pencere yok; yeni artefaktı çeker).
