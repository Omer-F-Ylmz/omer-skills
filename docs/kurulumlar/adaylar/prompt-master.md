# Prompt Master
ad: Prompt Master
tur: skill
video: cAeQjck1jHs
repo: nidhinjs/prompt-master
lisans: bilinmiyor (repoda LICENSE dosyası var ama türü okunamadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/nidhinjs/prompt-master
telemetri: Yok görünüyor: yalnız markdown talimat ve referans dosyaları içeriyor, çalıştırılabilir kod ya da ağ çağrısı listelenmiyor. Kaynak kodu tam okunmadı; README'ye ve dosya ağacına dayanıyor.
yildiz: 10.000+ (arama sonucu özeti; ~1.200 fork)
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-7)
## Ne
Dağınık isteği, hedef AI aracına (Claude, Cursor, Claude Code, Midjourney, GPT, Gemini vb.) uygun, yapılandırılmış ve kısa tek bir prompt bloğuna çeviren Claude skill'i. Kötü prompt onarma (repair) ve prompt'u başka araca uyarlama (decompiler) modları da var.
## Mekanizma
SKILL.md içinde sekiz adımlı bir boru hattı var. (1) Hedef aracı tespit eder. (2) 9 boyutta niyet çıkarır: görev, girdi, çıktı, kısıtlar, bağlam, kitle, hafıza, başarı ölçütü, örnekler. (3) Kritik bilgi eksikse en fazla 3 soru sorar. (4) Uygun prompt çerçevesini kullanıcıya göstermeden seçer. (5) Yalnız güvenli teknikleri uygular: rol atama, few-shot, XML yapı, dayanak noktaları, hafıza bloğu. (6) "En güncel" gerektiren isteklerde model bilgisini resmi dokümanla doğrular. (7) Çıktıyı değiştirmeyen her kelimeyi atan bir token verimlilik denetimi yapar. (8) Tek kopyalanabilir blok ve tek satır strateji notu verir. Dosyalar: SKILL.md, references/patterns.md, references/templates.md.
## Kanıt
- Dağınık prompt'ları yapılandırılmış, optimize prompt'a çeviriyor → doğrulandı · README'deki 8 adımlı boru hattı ve örnek çıktılar bunu anlatıyor. Gerçek çalıştırma yapılmadı.
- Hedef aracı tespit ediyor → doğrulandı · README adım 1: hedef aracı tespit edip uygun yaklaşıma yönlendirir.
- En fazla üç soru soruyor → doğrulandı · README adım 3: kritik bilgi eksikse en fazla 3 soru.
- 30+ araçla çalışıyor → sınanamadı · README yaklaşık 25 araç adı sayıyor ve 'any AI tool' diyor. 30+ rakamı sayılamadı, çalışma da denenmedi.
- Repo GitHub'da 'prompt master' aramasıyla bulunup zip ile yükleniyor → doğrulandı · Repo nidhinjs/prompt-master. README'de ZIP indirip Customize > Skills > Upload yolu öneriliyor. Videonun transkripti alınamadı, video içeriği doğrulanamadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Önerilen (claude.ai): repoyu ZIP indir → Sidebar → Customize → Skills → Upload a Skill (videodaki yol da bu).
- Claude Code: mkdir -p ~/.claude/skills && git clone https://github.com/nidhinjs/prompt-master.git ~/.claude/skills/prompt-master (README 'önerilmez' diyor).
- Kullanım: doğal dille ('Cursor için şu prompt'u yaz') ya da /prompt-master ile.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Hangi araca hangi biçimde prompt yazılacağını bilmeden hızlı ve tutarlı prompt üretir. Belirsiz isteklerde en fazla 3 soru sorar. Görsel, kod ve otomasyon araçlarını kapsar. Yanlış çıktı yüzünden yeniden deneme sayısını azaltır.
## Maliyet/risk
Düşük: sadece talimat dosyası. Dikkat edilecekler: aynı metnin çok sayıda fork'u var, yalnız nidhinjs/prompt-master kaynak alınmalı. "Zero tokens wasted" iddiası pazarlama dili ve ölçülmemiş. Lisans türü doğrulanmadı, kopyalayıp dağıtmadan önce LICENSE okunmalı. Model/araç bilgileri zamanla eskiyebilir.
## Tasarruf
Doğrudan token sıkıştırma aracı değil. Amaç, ilk denemede doğru çıktı alıp tekrar prompt yazma turlarını azaltmak. Prompt'tan gereksiz kelimeleri atan bir denetim adımı var. Ölçülmüş bir tasarruf rakamı bulunamadı. Skill'in kendi talimatı da her çağrıda bağlama yüklenir, bu küçük bir maliyet.
## Üretilebilir
hedef_tur: skill
tarif: Zaten skill olduğu için doğrudan alınabilir, ama lisansı doğrulayıp kendi sürümümüzü yazmak daha güvenli. Tarif: SKILL.md'de (1) hedef araç tespiti, (2) 9 boyutlu niyet kontrol listesi, (3) en fazla 3 soru kuralı, (4) araç başına şablonlar (references/templates.md: kod ajanı, görsel, sohbet modeli), (5) gereksiz kelime silme denetimi, (6) çıktı biçimi: tek blok ve tek satır strateji notu. Tetikleyici açıklamasına 'X için prompt yaz' ve 'bu prompt'u düzelt' ifadeleri konur. Bizim araç setine (Claude Code, Cursor) göre kısaltılır.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-7/panel.md → Ömer sütunu
## Özellikler
### Hedef araç tespiti ve araca özel yönlendirme (Claude, Cursor, Midjourney, Claude Code vb.)
kaynak: https://github.com/nidhinjs/prompt-master
### 9 boyutlu niyet çıkarımı ve en fazla 3 netleştirme sorusu
kaynak: https://github.com/nidhinjs/prompt-master
### Token verimlilik denetimi: çıktıyı değiştirmeyen kelimeleri atar
kaynak: https://github.com/nidhinjs/prompt-master
### Repair modu (kötü prompt onarma) ve decompiler modu (başka araca uyarlama)
kaynak: https://vibewithrashid.com/prompt-master-the-free-claude-skill-that-writes-better-prompts-for-any-ai-tool/
### Prompt Master (skill): 30'dan fazla araçla çalışma, 9 boyutta niyet çıkarımı, en fazla 3 soru
video: cAeQjck1jHs · iddia: Prompt Master 30'dan fazla araçla çalışır, dokuz boyutta niyet çıkarır, en fazla üç soru sorar.
sonuc: sınanamadı
arastirma: Repo README'si okundu (SKILL.md ve references dosyaları okunmadı). Dosya ağacı: LICENSE, README.md, SKILL.md, references/patterns.md, references/templates.md. (1) Dokuz boyut: README'nin "How It Works" adım 2'sinde yazıyor: görev, girdi, çıktı, kısıtlar, bağlam, kitle, hafıza, başarı ölçütü, örnekler. Doğrulandı. (2) En fazla üç soru: adım 3'te "max 3 questions if critical info is missing, never more" yazıyor. Doğrulandı. (3) 30'dan fazla araç: "Works with" listesini saydım, 25 ad çıkıyor (o1/o3 ayrı sayılırsa 26): Claude, ChatGPT, Codex, Grok, Gemini, o1/o3, MiniMax, Cursor, Claude Code, GitHub Copilot, Windsurf, Bolt, v0, Lovable, Devin, Perplexity, Midjourney, DALL-E, Stable Diffusion, ComfyUI, Sora, Runway, ElevenLabs, Zapier, Make. Ardından "any AI tool you throw at it" ekleniyor. "30+" rakamı README'de geçmiyor, listede de 30'a ulaşılmıyor. Belge bu sayıyı desteklemiyor, çürütmüyor da. Gerçek çalıştırma yapılmadı; çalışıp çalışmadığı bilinmiyor. Sonuç: iki parça doğrulandı, "30+" parçası doğrulanamadı. İddia tek cümle olduğu için genel sonuç "sınanamadı". Lisans türü okunmadı: bilinmiyor.
kaynak: https://github.com/nidhinjs/prompt-master
## Destek
- cAeQjck1jHs · 3:18 · Dağınık prompt'ları yapılandırılmış, optimize prompt'a çevirir; hedef aracı tespit eder, en fazla üç soru sorar, 30+ araçla çalışır. · kanıt: GitHub'da 'prompt master' aranıyor, repo zip indirilip Customize > Skills > Upload ile yükleniyor. · iddia: Prompt Master 30'dan fazla araçla çalışır, dokuz boyutta niyet çıkarır, en fazla üç soru sorar.
