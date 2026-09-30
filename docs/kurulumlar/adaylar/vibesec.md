# VibeSec
ad: VibeSec
tur: skill
video: ZSvcxjNZdxk
repo: behisecc/vibesec-skill
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/BehiSecc/VibeSec-Skill
telemetri: Yok. Repoda yalnızca markdown dosyaları var, çalışan kod olmadığı için ağ çağrısı veya telemetri beklenmiyor. SKILL.md'yi satır satır doğrulamadım.
yildiz: bilinmiyor
alt_tur: bilinmiyor
skillspector: SkillSpector --no-llm: 6 HIGH/CRITICAL bulgu. Ayrıntılar elimde yok, yanlış pozitif olabilir, elle incelenmeli.
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-6)
## Ne
Yapay zeka kodlama ajanına (Claude Code, Cursor, Codex, Copilot, Antigravity) güvenli kod yazmayı öğreten bir güvenlik skill'i. Bug bounty avcısı bakış açısıyla yazılmış güvenlik rehberi içerir. Amaç, API anahtarının istemci koduna gömülmesi, IDOR ve kimlik doğrulamasız hassas sayfalar gibi açıkların üretime girmeden engellenmesidir.
## Mekanizma
Repoda yalnızca LICENSE, README.md ve SKILL.md var. Çalıştırılabilir kod yok. SKILL.md'yi ajan skill olarak yükler. Model kod yazarken veya incelerken bu talimat ve kontrol listelerini bağlamına alır. README'ye göre kapsam şöyle: erişim kontrolü (IDOR, yetki yükseltme, mass assignment, token iptali), istemci tarafı (XSS, CSRF, gizli anahtar sızıntısı, open redirect), sunucu tarafı (SSRF, SQLi, XXE, path traversal, güvensiz dosya yükleme), kimlik doğrulama (zayıf parola, oturum, JWT) ve API/GraphQL. Atlatma teknikleri, uç durumlar, çerçeve ve bulut farkındalığı ile doğrulama kontrol listeleri de var. SKILL.md içeriğini doğrudan okuyamadım, bu yüzden bu bilgiler README'ye dayanıyor.
## Kanıt
- Skill, Claude'a güvenli kod yazmayı öğretir; build öncesi kurulursa açıkları önler → sınanamadı · Etkiyi ölçen bir test yapmadım. Repoda yalnızca SKILL.md ve README var, yani mekanizma talimat tabanlı. Gerçek azaltma oranı bilinmiyor.
- Yaygın açıkların %60-70'ini kapsar → sınanamadı · README'deki yazar beyanı. Bağımsız ölçüm yok.
- Kapsam IDOR, XSS, SSRF, SQLi, JWT, GraphQL vb. sınıflarını içerir → doğrulandı · README'deki kapsam tablosunda bu sınıflar listeli. SKILL.md içeriğini doğrudan okumadım.
- Repo güvenlik ön taramasından temiz geçer → çürütüldü · SkillSpector --no-llm taraması 6 HIGH/CRITICAL bulgu verdi. Bulguların yanlış pozitif olup olmadığı incelenmedi.
- güvenlik ön taraması: SkillSpector --no-llm HIGH/CRITICAL 6
## Kurulum
- git clone https://github.com/BehiSecc/VibeSec-Skill
- Claude Code için klasörü ~/.claude/skills (global) veya proje içindeki .claude/skills altına kopyala
- Cursor: ~/.cursor/skills veya .cursor/skills; Codex: ~/.agents/skills veya .agents/skills; Copilot: ~/.copilot/skills veya .github/skills
- İstem örneği: "I'm building a [web app description]. Please follow secure coding practices."
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Kod üretimi sırasında güvenli desenleri ajanın bağlamına koyar ve yaygın açık sınıflarını önceden azaltır. Kurulumu tek klasör kopyalamaktan ibarettir. Birçok ajan platformunda çalışır. README, kapsamın yaygın açıkların yalnızca %60-70'ini karşıladığını kendisi söylüyor. Daha kapsamlı sürüm ücretli/ayrı olan vibesec.sh'de.
## Maliyet/risk
Skill statik talimat olduğu için güvenlik garantisi vermez. Model talimatı atlayabilir veya yanlış uygulayabilir. Kapsam kısmi (%60-70). Lisans türünü doğrulayamadım, LICENSE dosyası var ama içeriği okunmadı. Ön tarama SkillSpector --no-llm ile 6 HIGH/CRITICAL bulgu verdi. Bulguların ayrıntısı elimde yok. Muhtemelen SKILL.md'deki saldırı örnekleri veya payload metinleri yanlış pozitif üretiyor, ama bunu doğrulamadım. Kurmadan önce SKILL.md elle incelenmeli. Video iddiaları ajansın kendi anlatımı, bağımsız doğrulanmadı.
## Tasarruf
Token aracı değil. Tam tersine skill bağlama ek token yükler.
## Üretilebilir
hedef_tur: skill
tarif: Kendi güvenlik skill'imizi yazmak kolaydır. Bir SKILL.md oluştur. Frontmatter'a ad ve tetikleyici açıklama (web uygulaması/API/auth kodu yazılırken kullan) ekle. Gövdeyi açık sınıfına göre bölümle: IDOR, XSS, SSRF, SQLi, JWT, gizli anahtar yönetimi. Her bölüme 'yapma / yap' örnekleri ve bir doğrulama kontrol listesi koy. Uzun ayrıntıları ayrı referans dosyalarına al ve gerektiğinde yüklet, böylece token tüketimi düşük kalır. İsteğe bağlı olarak bir PreToolUse hook'u ile koddaki sabit gizli anahtarları tarayan basit bir regex denetimi eklenebilir. Bu repodaki metni kopyalamadan önce lisansı kontrol et.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-6/panel.md → Ömer sütunu
## Özellikler
### Erişim kontrolü, istemci, sunucu, kimlik doğrulama ve API güvenliği sınıflarını kapsayan güvenli kodlama rehberi
kaynak: https://github.com/BehiSecc/VibeSec-Skill
### Her açık sınıfı için kontrol listeleri ve atlatma tekniği bilgisi
kaynak: https://github.com/BehiSecc/VibeSec-Skill
### Claude Code, Cursor, Codex, Copilot ve Antigravity için klasör kopyalama ile kurulum
kaynak: https://github.com/BehiSecc/VibeSec-Skill
## Destek
- ZSvcxjNZdxk · 17:01 · Kod tabanında güvenlik açıklarını denetler; build öncesi kurulursa Claude'a güvenli kod yazmayı öğretir. · kanıt: stop vibe coding vulnerabilities into production
