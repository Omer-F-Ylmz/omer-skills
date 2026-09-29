# Ponytail
ad: Ponytail
tur: CLI
video: klDiYMzW0o0
repo: dietrichgebert/ponytail
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/DietrichGebert/ponytail
telemetri: Bilinmiyor. README'nin okunan kısmında telemetri beyanı yok. Kural/prompt dosyası olduğu için ağ çağrısı beklenmez. Repoda .env.example ve yalnızca kıyaslama amaçlı benchmark betikleri var. README'de bir "waitlist" bağlantısı (ponytail.dev) bulunuyor. Kurulumdan önce npm paketini kontrol edin.
yildiz: bilinmiyor (üçüncü taraf site 131K diyor, GitHub'dan doğrulanmadı)
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
AI kodlama ajanını "en tembel kıdemli geliştirici" gibi davranmaya iten bir kural seti/skill. Amaç gereksiz kod yazdırmamak, daha küçük ve basit çözümler üretmek. Claude Code, Codex, Cursor, Windsurf, Cline, Gemini CLI, OpenCode gibi yaklaşık 20 ajanı destekliyor. Videoda yalnızca "Sonuncusu Ponytail" diye geçiyor, işlevi anlatılmıyor. Aynı adı taşıyan başka bir repo da var (mikrammullah/PonyTail), bu yüzden videodaki aracın bu repo olduğu varsayımdır ve doğrulanmadı.
## Mekanizma
Ajan kod yazmadan önce bir karar merdiveninde ilk tutan basamakta durur: 1) Bu gerekli mi (YAGNI)? 2) Kod tabanında zaten var mı? 3) Stdlib yapıyor mu? 4) Yerel platform özelliği var mı? 5) Kurulu bağımlılık var mı? 6) Tek satır mı? 7) Ancak sonra çalışan minimum. Önce problemi anlar ve ilgili kodu okur. Doğrulama, hata yönetimi, güvenlik ve erişilebilirliği kesmez. Talimatlar skill ve kural dosyalarıyla (.claude-plugin, .cursor/rules, .clinerules, AGENTS.md vb.) ajanın bağlamına verilir. Çalışan bir çalıştırma kodu yok, prompt mühendisliği.
## Kanıt
- Ponytail bir CLI aracıdır → çürütüldü · Repo yapısı ve README skill/plugin/kural seti olduğunu gösteriyor; ayrı bir çalıştırılabilir CLI görünmüyor (npm paketi kurulum içindir).
- Claude token harcamasını yarıya indirir (video başlığı) → çürütüldü · README'deki yazar ölçümü token -%22, maliyet -%20, kod satırı -%54. Yarıya inen kod satırıdır, token değil.
- Kod satırını %80-94 azaltır → çürütüldü · Yazar bunu eski tek atışlık kıyaslama artefaktı olarak düzeltmiş; ortalama %54, %94 yalnızca en kötü aşırı-inşa görevinde.
- Videodaki dördüncü araç bu repodur → sınanamadı · Video sayfası yalnızca başlığı verdi; transkript alınamadı. Eşleşme başlık ve konu uyumuna dayanıyor.
- Lisans MIT → doğrulandı · README rozeti ve arama sonuçları MIT diyor; repoda LICENSE dosyası var.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code için repodaki .claude-plugin/marketplace.json üzerinden plugin marketplace ile eklenir (tam komut doğrulanmadı, README'ye bakın)
- npm paketi var: @dietrichgebert/ponytail
- Cursor/Windsurf gibi editörlerde repodaki kural dosyaları kopyalanır (.cursor/rules, .windsurf/rules)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Aşırı mühendisliği (gereksiz bağımlılık, sarmalayıcı bileşen, stil dosyası) önler. Örneğin tarih seçici için flatpickr yerine `<input type="date">` önerir. Diff küçülür, gözden geçirme kolaylaşır, maliyet biraz düşer. Güvenlik korumalarını korur.
## Maliyet/risk
Düşük. Kod çalıştırmayan bir prompt/kural paketi. Riskler: ajanı aşırı minimalist yapıp gerekli kodu atlatması, reasoning modellerde maliyeti artırması, videodaki adayla repo eşleşmesinin doğrulanmamış olması, ad benzerliği olan başka repo, ileride ticari (waitlist) yön değişikliği. Kurulumdan önce npm paketi ve eklenti dosyaları incelenmeli.
## Tasarruf
Kod satırını azaltarak dolaylı token ve maliyet tasarrufu sağlar. Yazarın kendi ölçümü (Haiku 4.5, 12 görev, n=4, FastAPI+React deposu): kod satırı -%54, token -%22, maliyet -%20, süre -%27, güvenlik %100. Eski tek atışlık %80-94 rakamını yazar kendisi düzeltmiş. Videodaki "yarıya indirir" başlığı bu araç için token tarafında doğrulanmıyor. Akıl yürütme ağırlıklı modellerde (GPT-5.5) tersine çalışabildiği belirtiliyor. Ölçümler bağımsız doğrulanmadı.
## Üretilebilir
hedef_tur: skill
tarif: Bir SKILL.md yaz. Ajana kod yazmadan önce 7 basamaklı merdiveni (gerekli mi, kod tabanında var mı, stdlib, native özellik, mevcut bağımlılık, tek satır, minimum) uygulamasını söyle. Önce ilgili kodu okumayı ve doğrulama, hata yönetimi, güvenlik ve erişilebilirliği asla kesmemeyi şart koş. Önce/sonra örnekleri ekle. Etkiyi kendi ortamımızda 5-10 görevle git diff satırı ve token ölçerek sına. Kopyalamak yerine MIT lisansına atıf vererek sıfırdan yazmak daha temiz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### 7 basamaklı karar merdiveni (YAGNI, yeniden kullan, stdlib, native, mevcut bağımlılık, tek satır, minimum)
kaynak: https://github.com/DietrichGebert/ponytail
### Yaklaşık 20 ajan için kural/eklenti dosyaları (Claude Code, Codex, Cursor, Windsurf, Cline, Kiro, Qoder, Devin, Grok vb.)
kaynak: https://github.com/DietrichGebert/ponytail
### Tekrarlanabilir ajan tabanlı benchmark (benchmarks/ klasörü)
kaynak: https://github.com/DietrichGebert/ponytail
### Güvenlik korumaları (doğrulama, hata yönetimi, erişilebilirlik) korunur
kaynak: https://github.com/DietrichGebert/ponytail
## Destek
- klDiYMzW0o0 · 0:30 · Dördüncü araç; işlevi videoda açıklanmıyor. · kanıt: Sonuncusu Ponytail.
