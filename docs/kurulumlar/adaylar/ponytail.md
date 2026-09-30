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
### Ponytail daha az kod satırı üretip çıktı tokenı, maliyet ve inceleme süresini azaltıyor (video g89FJiNAlEs, 8:16)
video: g89FJiNAlEs · iddia: Ponytail daha az kod satırı üretip çıktı tokenı, maliyet ve inceleme süresini azaltıyor.
sonuc: doğrulandı
arastirma: README'ye göre Ponytail bir CLI değil, ajana verilen skill/kural seti (.claude-plugin, .cursor/rules, .clinerules, AGENTS.md vb.). Ajan kod yazmadan önce 7 basamaklı merdiveni uygular: gerekli mi (YAGNI), kod tabanında var mı, stdlib, yerel platform özelliği, kurulu bağımlılık, tek satır, en son minimum çalışan kod. Önce ilgili kodu okur. Doğrulama, hata yönetimi, güvenlik ve erişilebilirlik kesilmez. Yazarın ölçümü, gerçek Claude Code oturumları ve FastAPI+React deposu üzerinde, 12 görev, n=4, Haiku 4.5, kod yokken baz alınarak: kod satırı -%54 (en fazla %94, tarih seçici gibi aşırı-inşa görevlerinde), token -%22, maliyet -%20, süre -%27, güvenlik %100. Süre, yani iş bitirme hızı da düştü. README'deki tek yeni belge "inceleme süresi" değil, süre (-%27) ve diff küçülmesidir. Diff küçüldüğü için incelemenin kolaylaşması makul bir çıkarımdır ama README bunu doğrudan ölçmüyor. Eski tek atışlık %80-94 rakamı yazar tarafından düzeltildi. Sınırlar: ölçümler yazarın kendisine ait ve bağımsız doğrulanmadı. Akıl yürütme ağırlıklı modellerde (GPT-5.5) tersine çalışabildiği belirtiliyor. Videoyu ve transkripti görmedim, aracın videodaki araçla aynı olduğu başlık ve konu uyumuna dayanıyor. Aynı adlı başka bir repo da var.
kaynak: https://github.com/DietrichGebert/ponytail
## Destek
- klDiYMzW0o0 · 0:30 · Dördüncü araç; işlevi videoda açıklanmıyor. · kanıt: Sonuncusu Ponytail.
- g89FJiNAlEs · 8:16 · Ajanı 'en tembel kıdemli mühendis' gibi düşündüren skill/plugin. Aynı uygulamayı daha az satır ve dosyayla üretir, çıktı tokenı ve inceleme süresi azalır. · kanıt: Anlatıcı çıktı tokenlarını azaltmak için ilk araç olarak Ponytail'i tanıtıyor; marketplace'e ekleyip kuruyor. · iddia: Ponytail daha az kod satırı üretip çıktı tokenı, maliyet ve inceleme süresini azaltıyor.
- V0XbuApxlhg · 17:33 · Claude'un yazdığı kod miktarını azaltıp maliyeti düşüren popüler skill; Fable ile benchmark sayıları tuttu. · kanıt: It reduces the amount of code Claude writes while maintaining its effectiveness.
- V2RIVnGCy74 · 5:31 · Claude Code'a kod yazmadan önce 'bu gerekli mi, kod tabanında/standart kütüphanede var mı' diye sordurup daha az kod, token ve maliyetle aynı çıktıyı hedefleyen repo. · kanıt: README tablosunda ponytail satırı: LOC -54%, tokens -22%, cost -20%, time -27%, safe 100%. (karede: github.com/DietrichGebert/ponytail README: baseline'a göre çubuk grafikler (LOC, tokens, cost, time) ve tablo; ponytail satırı -54% LOC, -22% tokens, -20% cost, -27% time, safe 100%; caveman ve 'YAGNI + one-liners' satırları da var; sağ altta konuşmacı.)
- PWRWO749oro · 0:00 · Kod yazmadan önce Claude'a kodun gerçekten gerekli olup olmadığını sorduran verimlilik katmanı. · kanıt: Before writing a single line, it forces Claude to ask whether the code even needs to exist.
