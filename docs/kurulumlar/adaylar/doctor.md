# /doctor
ad: /doctor
tur: CLI
video: V0XbuApxlhg
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor. Komutun kendine özgü bir telemetrisi doğrulanmadı. Claude Code'un genel telemetri ayarları geçerli.
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Claude Code'a yerleşik olduğu için zaten bizde var. Kurulum gerekmiyor.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun)
## Ne
Claude Code içinde yerleşik bir slash komutu. Kurulum ve ayar sağlığını denetler. Video, bağlam şişkinliği uyarılarını (büyük CLAUDE.md, çok yer kaplayan MCP araçları) gösterdiği için bunu bir budama rehberi olarak öneriyor.
## Mekanizma
Oturumda /doctor yazılınca Claude Code yerel kurulumu, ayarları ve bağlamı tarar, sorunları listeler. Kendi bilgime göre bağlam uyarıları da veriyor: çok büyük CLAUDE.md dosyaları, büyük MCP araç tanımları, erişilemeyen izin kuralları. Kendisi dosya budamaz. Kısaltma işini kullanıcı ya da model yapar. Bu ayrıntıları bu oturumda doğrulayamadım. Video sayfasından yalnızca başlık geldi, transkript gelmedi. Videoda geçen "forward/doctor" büyük olasılıkla "/doctor" komutunun yanlış duyulmuş hali.
## Kanıt
- /doctor CLAUDE.md'yi kısaltır, kullanılmayan skill ve MCP'leri budar. → sınanamadı · Video sayfasından yalnızca başlık geldi, transkript gelmedi. Komutu bu ortamda çalıştırmadım. /doctor'un tanı koyduğunu biliyorum, otomatik budadığını doğrulayamadım. Budama muhtemelen elle yapılıyor.
- Anthropic'e 20 kat fazla ödeniyor. → sınanamadı · Yalnızca video başlığında geçiyor, ölçüm ya da kaynak yok.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Ayrı kurulum gerekmez. Claude Code kuruluysa oturumda /doctor yazın.
- Çıktıdaki bağlam uyarılarına göre CLAUDE.md'yi kısaltın, kullanılmayan MCP sunucularını ve skill'leri kaldırın.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Bağlamı şişiren kaynakları bulmayı ve budamayı kolaylaştırır. Yerleşik olduğu için maliyeti sıfır.
## Maliyet/risk
Düşük. Aşırı kısaltılmış CLAUDE.md ya da kaldırılmış MCP, ihtiyaç duyulan talimatı ya da aracı kaybettirebilir. Video kanıtı zayıf: yalnızca başlık alındı, komut adı da yanlış yazılmış.
## Tasarruf
Dolaylı tasarruf sağlar. /doctor budamayı kendisi yapmaz, şişkinliği görünür kılar. Küçük CLAUDE.md ve az sayıda MCP aracı, her istekte gönderilen sabit bağlam token'ını azaltır. Videodaki "20 kat" iddiası doğrulanmadı.
## Üretilebilir
hedef_tur: skill
tarif: 'bağlam-diyeti' adında bir skill yazılabilir. Adımlar: (1) CLAUDE.md ve ~/.claude/CLAUDE.md boyutunu ölç. (2) settings ve .mcp.json içindeki MCP sunucularını ile skill klasörlerini listele. (3) Son oturumlarda kullanılmayanları işaretle. (4) Kaldırma ve kısaltma önerilerini onay isteyerek sun. /doctor çıktısı ek girdi olarak kullanılabilir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun/panel.md → Ömer sütunu
## Özellikler
### Yerleşik tanı komutu: kurulum ve ayar sorunlarını listeler. Bağlam uyarıları da veriyor (doğrulanmadı).
kaynak: https://www.youtube.com/watch?v=V0XbuApxlhg
## Destek
- V0XbuApxlhg · 14:54 · CLAUDE.md'yi kısaltır, kullanılmayan skill ve MCP'leri budayıp bağlam şişkinliğini azaltır. · kanıt: Run the forward/doctor command... trim your claude.md down.
