# Am I missing anything this time?
## Künye
Am I missing anything this time? · millee.md · süre: 0:26 · ? · https://www.instagram.com/reel/DcCT3UfpFAn/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-12 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 32240 tk · claude-haiku-5-5: claude-haiku-5-5 · 13974 tk
## Özet
Kısa bir Instagram reel'i: konuşmacı, uygulamayı yayınlamadan önce Claude'a yaptırılacak 20 güvenlik maddesini 27 saniyede sayıyor (2. bölüm). Maddeler HSTS, CSRF belirteçleri, oturum sıfırlama, hız sınırı, prompt injection engelleme, güvenli çerezler ve veritabanı izinlerini kapsıyor. Açıklamada bunun sızma testinin yerini tutmadığı belirtiliyor.
## Bölümler
- 0:00 Giriş ve madde 1: HSTS
- 0:05 Madde 2-8: CSRF, oturum, bağlantı, yükleme, ödeme, fiyat
- 0:15 Madde 9-12: prompt injection, AI sınırı, istek boyutu, hız sınırı
- 0:20 Madde 13-16: temizleme, dizin listeleme, yönetici rotaları
- 0:26 Madde 17-20: hesap kilitleme, günlük, çerezler, veritabanı izinleri
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude | yok | CLI | yok | Güvenlik maddelerini uygulatmak için kullanılan yapay zekâ asistanı | 0:00 | Başlıkta Claude'a yaptırılacak 20 şey yazıyor. (karede: Başlık: 20 things to have Claude do before launching your app (in under 27 seconds) pt.2) |
| HSTS | yok | teknik | yok | HTTPS'i zorunlu kılan güvenlik başlığı | 0:00 | Madde 1 'Add HSTS'. (karede: Listede '1. Add HSTS', altyazıda 'add HSTS,') |
| CSRF tokens | yok | teknik | yok | Siteler arası istek sahteciliğine karşı belirteçler | 0:10 | Madde 2 'Add CSRF tokens'. (karede: '2. Add CSRF tokens' listede görünüyor) |
| Rate limiting | yok | teknik | yok | Parola sıfırlama isteklerini sınırlama | 0:15 | Madde 12 'Rate limit password resets'. · kanıt: kare (karede: '12. Rate limit password resets' sağ sütunda) |
| Prompt injection engelleme | yok | teknik | yok | Yapay zekâ girdisine karşı koruma | 0:15 | Madde 9 'Block prompt injection'. · kanıt: kare (karede: '9. Block prompt injection' sol sütunda) |
| Secure cookies | yok | teknik | yok | Çerezlere güvenlik bayrakları ekleme | 0:00 | Altyazıda 'Set secure cookies' geçiyor. |
## Açıklama bağlantıları
- yok
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Yayından önce Claude'a yaptırılacak 20 güvenlik maddesi 27 saniyede sayılıyor. | 0:00 | öneri |
| Liste sızma testinin yerini tutmaz. | açıklama | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | Claude | Claude | Başlıkta adı geçiyor. |
| konuşma 0:00 | HSTS | HSTS | Altyazı 'add HSTS,'. |
| kare 0:10 | CSRF tokens | CSRF tokens | Madde 2. |
| kare 0:15 | Rate limit password resets | Rate limiting | Madde 12. |
| kare 0:15 | Block prompt injection | Prompt injection engelleme | Madde 9. |
| konuşma 0:26 | Set secure cookies | Secure cookies | Altyazı maddesi. |
| kare 0:15 | Cap AI usage | aday değil: genel kavram | Madde 10, genel öneri. |
| açıklama | Pen-test notu | aday değil: genel kavram | P.S. sızma testi yerine geçmez. |
## Kareden okunanlar
- 0:00: Başlık, 1. Add HSTS, boş 2-20 numaraları, sayaç 00:00.46, altyazı 'add HSTS,'
- 0:10: 1-8. maddeler: HSTS, CSRF tokens, Reset sessions, Expire reset links, Prevent user enumeration, Whitelist upload types, Verify payment webhooks, Set prices server-side
- 0:15: 9. Block prompt injection, 10. Cap AI usage, 11. Limit request size, 12. Rate limit password resets
## Belirsizlikler
- Konuşmacı ve kanal adı belli değil.
- 13-20. maddeler kare olmadan yalnız altyazı ve OCR'dan alındı; 'Lock down cores' büyük olasılıkla 'Lock down CORS' (OCR/altyazı hatası).
- Yorumlar girişsiz alınamadı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- yok
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
