---
iddia: 28 dk'lık suite koşusunun sebebi kök tests/'in uv izole ortamında koşması (playwright yok → test_browse_shim test başına 120 sn); ortam python'u ile 16 sn
kaynak: docs/olcumler/suite-suresi.md
guven: yüksek
dogrulama: https://github.com/Omer-F-Ylmz/omer-skills/blob/main/docs/olcumler/suite-suresi.md
tarih: 2026-09-24
bayatlama: 2026-12-23
etiketler: test, sure, olcum
---
Suite'ler yavaşlamadı (video 11 s, jev 1 s). Kök suite `python -m pytest tests` ile koşulmalı; suite-kosucu bunu sabitliyor.
