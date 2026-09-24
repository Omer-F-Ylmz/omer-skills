---
iddia: RTK Bash komutlarının %30'unu kapsıyor; kalan büyük aileler (cat, sed, echo, python) içerik çıktısı olduğundan süzülmez. PowerShell kancası işlevsiz.
kaynak: rtk discover --since 3, headroom audit-reads, rtk hook claude'a PowerShell girdisi
guven: yuksek
dogrulama: docs/olcumler/headroom-gelistir.md
tarih: 2026-09-24
bayatlama: 2026-12-23
etiketler: token, headroom, rtk, olcum
---
RTK Bash komutlarının %30'unu kapsıyor; kalan büyük aileler (cat, sed, echo, python) içerik çıktısı olduğundan süzülmez. PowerShell kancası işlevsiz.
- Repo filtresi cc-kopru-suit node --test'i de eşliyor (75 çağrı, fixture %89); etkinlik rtk trust'a bağlı.
- graphify query boş satır süzme ~%3; 21a max_lines önerisi geri çekildi (TRUNCATED uyarısını keser).
- PowerShell: settings eşleyicisi var, rtk hook PowerShell girdisine boş döner, RTK'da PowerShell desteği yok.
