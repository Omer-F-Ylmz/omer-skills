# You Should Know
ad: you-should-know
tur: plugin
video: _0NSNY7n5lE
repo: yok
lisans: yok
son_commit: yok
arsiv: hayır
kaynak: yok
telemetri: açık
arastirma: tam
karar: ÖĞREN (yerleşik, Kurulum satırı yok → video onay hattına girmez; `video dene` claude -p ile ölçer, mod claude -p'de koşmaz → DENE ölçülemez; "maliyet artırmaz" iddiası yanlış → kullanım kartı)
## Ne
Claude Code v2.1.287 (2026-10-01) yerleşik "mod": uzun görevlerde yan ajan Claude çıktısını izler, kaçırılabilecek şey bulursa istemin üstüne kısa not düşer. Varsayılan kapalı.
## Kanıt
- ön getirme: C:/Projeler/omer-skills/.kos/_0NSNY7n5lE/you-should-know/on.md
- yıldız: yok (repo yok; kaynak public mods klasöründe değil) · son commit: yok · lisans: yok (Claude Code içinde, Anthropic ticari)
- SkillSpector: koşmadı (on.md; skill değil)
- https://fixter.dev/blog/cc-plugin-you-should-know — tetik kuralı, yan ajan modeli, kullanım sıklığı yayımlanmamış; mod kullanımı harcayabilir.
## Kurulum
Yerleşik; Kurulum satırı yok (`/plugin enable cc-plugin-you-should-know@builtin` yalnız etkileşimli oturumda, claude -p'de çalışmaz).
## İzinler
Mod sandbox'sız: her istemi, her araç çağrısını, dosya ve ortamı görür (Fixter/Anthropic mods docs). --safe-mode, --bare, disableAllHooks yerleşik modu durdurmaz. Telemetri açık birinci taraf oturum gerekir. Serbest komut yok; elle etkinleştirme.
## Duman testi
- komut: claude --version
- cikis: 0
- desen: \d+\.\d+\.\d+
## Geri alma
Kaldırılamaz, yalnız kapatılır: `/plugin disable cc-plugin-you-should-know@builtin` (elle).
## Köprü izni
- arac: claude
- altIzin: --version
## Önerilen katman
T2 (çalıştırılabilir, oturum içi yan ajan; elle etkinleştirme, otomatik onay hattı yok)
## Telemetri kapatma
- /plugin disable cc-plugin-you-should-know@builtin (özellik telemetri açık oturum şartlı; telemetriyi kapatmak özelliği de kapatır)
## Özellikler
### yan-ajan-notu
ne: Uzun görevde yan ajan çıktıyı tarar, kaçırılabilecek karar/varsayım/atlanan adım için istem üstüne not düşer.
kurulum: `/plugin enable cc-plugin-you-should-know@builtin` (v2.1.287+, etkileşimli oturum).
lisans: yok (Anthropic ticari, yerleşik)
etiket: -
karar: DENE
gerekce: yalnız birkaç uzun görevde aç, kullanım farkını ölç; maliyeti yayımlanmamış.
## Bağımsız kanıt
- https://fixter.dev/blog/cc-plugin-you-should-know — yan ajan model çağırır, ek kullanım yayımlanmamış; kısa görev ve sıkı limitte önerilmez.
- https://nerdschalk.com/claude-code-you-should-know-plugin/ — varsayılan kapalı, birinci taraf + telemetri açık oturumla sınırlı.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Token/süre maliyeti artırmaz (4:03) | https://fixter.dev/blog/cc-plugin-you-should-know | yanlış | Mod model çağırabilir; yan ajan ek kullanım harcar, miktar yayımlanmamış. | - |
| Claude çıktısındaki önemli detayları hatırlatır | https://nerdschalk.com/claude-code-you-should-know-plugin/ | doğru | Yan ajan not düşer. | - |
## Kötü yan + onarım + güçlendirme
- token · yan ajan ek model çağrısı, miktar belirsiz · neden: https://fixter.dev/blog/cc-plugin-you-should-know · tahmin · onarım: yalnız uzun görevlerde aç, kullanımı aç/kapa karşılaştır, bitince /plugin disable · kaynak: aynı
- güvenlik · mod sandbox'sız, tüm oturumu görür; kaynağı kapalı · neden: aynı · tahmin · onarım: gizli bilgi içeren oturumda kapalı tut · kaynak: aynı
- kalite · tetik kuralı bilinmiyor; "doğruluk kanıtı değil" · neden: https://www.dmssolution.co.kr/en/works/claude-code-you-should-know · tahmin · onarım: notları doğrulama yerine ipucu say · kaynak: aynı
güçlendirme: graphify ve Headroom ile oturum bağlamı küçüldüğünden yan ajan girdisi de küçülür; departman skill'lerinin kapanış raporuyla notlar çapraz kontrol edilir.
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): yok
