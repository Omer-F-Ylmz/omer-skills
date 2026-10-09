# stop slop
ad: stop slop
tur: skill
video: BiEvvC_66AQ
repo: hardikpandya/stop-slop
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/hardikpandya/stop-slop
telemetri: Yok. Yalnızca markdown dosyaları, ağ çağrısı veya çalıştırılabilir kod içermiyor.
yildiz: bilinmiyor (üçüncü taraf listeleme ~9.8k★ diyor, doğrudan doğrulanmadı)
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Yapay zeka yazımının tipik kalıplarını (klişe cümleler, yapısal tekrarlar, ritim tekdüzeliği) metinden temizleyen, Claude ve diğer LLM'ler için yazılmış salt-dokümantasyon skill'i.
## Mekanizma
Çalıştırılabilir kod yok. SKILL.md çekirdek kuralları verir; references/ altında phrases.md (yasak ifadeler), structures.md (kaçınılacak yapılar) ve examples.md (önce/sonra örnekleri) ihtiyaç halinde yüklenir. Model metni bu kurallara göre yeniden yazar ve 5 boyutta (doğrudanlık, ritim, güven, özgünlük, yoğunluk) 1-10 puanlar; toplam 35/50 altındaysa tekrar revize eder. Kurallar: dolgu ifadeleri at, kalıp yapıları boz, etken çatı, somut ol, zarfları ve em dash'i çıkar, Wh- cümle başlangıcı kullanma.
## Kanıt
- Metinlerdeki yapay zeka kalıplarını temizler → doğrulandı · Repo README: 'A skill for removing AI tells from prose'; phrases.md, structures.md ve puanlama tablosu mevcut.
- Lisans MIT ve kod içermez → doğrulandı · README 'MIT. Use freely' ve ağaçta yalnızca .md dosyaları ile LICENSE var.
- Yıldız sayısı ~9.8k → sınanamadı · Yalnızca skillsllm.com arama özetinde geçiyor; GitHub'dan doğrulanmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Repoyu klonla: git clone https://github.com/hardikpandya/stop-slop
- Klasörü Claude Code skill dizinine kopyala (örn. ~/.claude/skills/stop-slop veya proje içi .claude/skills/stop-slop)
- Claude Projects için SKILL.md ve references dosyalarını proje bilgisine yükle; API için SKILL.md'yi sistem istemine ekle
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Türkçe/İngilizce çıktıda yapay zeka kokan kalıpları azaltır; blog, e-posta, doküman yazımında insan sesine yakın metin üretir. Puanlama döngüsü kaliteyi ölçülebilir kılar. Not: kurallar İngilizce kalıplara göre yazılmış, Türkçe için uyarlama gerekir.
## Maliyet/risk
Düşük: kod yok, MIT. Riskler: kurallar İngilizce'ye özgü (em dash, Wh- başlangıç, "adverb yasağı" Türkçede anlamsız olabilir); aşırı kuralcılık metni bozabilir; "yapay zeka tespitini atlatma" amacıyla kullanılırsa etik/akademik sorun doğar. Video kanıtı yalnızca tek cümlelik tanıtım; repo adı arama sonucuyla eşleştirildi (aynı adlı başka fork'lar var: mohamedgame, drm-collab).
## Tasarruf
Token aracı değil. Tersine skill içeriği bağlama yüklenir (referanslar isteğe bağlı), küçük bir token maliyeti ekler.
## Üretilebilir
hedef_tur: skill
tarif: Türkçe uyarlama: SKILL.md + references/(kaliplar-tr.md, yapilar-tr.md, ornekler-tr.md). Türkçe yapay zeka kalıplarını derle ('Sonuç olarak', 'günümüzde', 'bir yolculuğa çıkalım', 'sadece X değil, aynı zamanda Y', gereksiz edilgenlik, 'önemle belirtmek gerekir'). Aynı 5 boyutlu puanlama ve 35/50 eşiğiyle yeniden yazma döngüsü ekle; em dash/Wh- gibi İngilizce'ye özgü kuralları çıkar. Orijinal MIT lisansına atıf yap.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### Yasak ifade listesi: giriş dolguları, vurgu koltuk değnekleri, iş jargonu, zarflar, belirsiz ifadeler, meta-yorum
kaynak: https://github.com/hardikpandya/stop-slop
### Yapısal klişe tespiti: ikili karşıtlık, olumsuz listeleme, dramatik parçalama, retorik kurulum, sahte özne, edilgen çatı
kaynak: https://github.com/hardikpandya/stop-slop
### 5 boyutlu puanlama (doğrudanlık, ritim, güven, özgünlük, yoğunluk), 35/50 altı revize
kaynak: https://github.com/hardikpandya/stop-slop
### Önce/sonra örnekleri ve isteğe bağlı referans yükleme
kaynak: https://github.com/hardikpandya/stop-slop
## Destek
- BiEvvC_66AQ · 0:00 · Metinlerdeki yapay zeka kalıplarını temizler. · kanıt: stop slop, which strips out any AI-sounding patterns from any text
