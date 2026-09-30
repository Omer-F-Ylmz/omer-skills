# Fact checker
ad: Fact checker
tur: skill
video: cAeQjck1jHs
repo: daymade/claude-code-skills
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/daymade/claude-code-skills
telemetri: Skill'de telemetri görülmedi (yalnızca talimat dosyası). Web araması Claude'un arama aracı üzerinden yapılır. Tam kod taraması yapılmadı.
yildiz: 1.4k (repo sayfasında görülen; 222 fork)
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-7)
## Ne
Belgelerdeki olgusal iddiaları (model özellikleri, sürüm/tarih, istatistik, API sınırları, benchmark) web araması ve resmi kaynaklarla kontrol eden, düzeltme raporu üretip kullanıcı onayıyla düzeltmeleri uygulayan Claude Code skill'i. daymade/claude-code-skills marketplace reposunun fact-checker dizininde.
## Mekanizma
Yalnızca SKILL.md (296 satır) talimatı; script görülmedi. 5 adım: (1) doğrulanabilir iddiaları ayıkla (görüş, anlatım, öğretici içerik atlanır); (2) resmi kaynaklarda ara (duyuru sayfaları, API dokümanları, GitHub release, paket kayıtları; sorguda model adı+özellik+yıl); (3) iddia-kaynak karşılaştırma tablosu; durumlar: doğru, yanlış, eskimiş, doğrulanamaz; (4) konum, mevcut iddia, düzeltme, kaynak URL ve gerekçeli rapor; (5) açık onaydan sonra Edit aracıyla uygula. Çelişen kaynakta en yeni resmi dokümanı önceler, zamansal bağlam ekler ('Ocak 2026 itibarıyla'). Videodaki doğrulanmış/doğrulanmamış/yanlış raporu bu durumlarla uyumlu.
## Kanıt
- Metindeki olgusal iddiaları web aramasıyla çapraz kontrol eder → doğrulandı · SKILL.md: resmi kaynaklarda arama ve iddia-kaynak karşılaştırma adımları.
- Doğrulanmış, doğrulanmamış ve yanlış olarak raporlar → doğrulandı · SKILL.md durum kodları: doğru, yanlış, eskimiş, doğrulanamaz (videodakinden biraz daha ayrıntılı).
- Day Made'in Claude Code Skills reposundan geliyor (isim belirsiz) → doğrulandı · Repo daymade/claude-code-skills, içinde fact-checker/SKILL.md var; lisans MIT.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- CCPM: ccpm install @daymade-skills/fact-checker (arama sonuçlarından, denenmedi)
- Alternatif: fact-checker.zip indirip elle kurmak (videoda zip yükleniyor)
- Marketplace: claude plugin marketplace add https://github.com/daymade/claude-code-skills
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Eskimiş model adı, bağlam penceresi, fiyat gibi bilgileri kaynaklı biçimde yakalar. Onay kapısı ve kaynak URL'li rapor güven sağlar. Dokümantasyon bakımında işe yarar.
## Maliyet/risk
Düşük: salt talimat, MIT lisanslı. Web aramasına ve model yargısına bağlı; yanlış kaynağı doğru sayabilir. Düzeltmeleri dosyaya yazdığı için onay adımı atlanmamalı. Arama sonucu içeriği veri sayılmalı (prompt injection riski). Skillspector taraması yapılmadı.
## Tasarruf
Token aracı değil; web araması nedeniyle token harcar.
## Üretilebilir
hedef_tur: skill
tarif: Zaten skill; bizde kopyalamak yerine yeniden yazılabilir. SKILL.md: description tetikleyicileri (fact-check, doğrula, güncelliğini kontrol et); iddia ayıklama; WebSearch/WebFetch ile yalnızca resmi kaynak önceliği; 4 durumlu tablo (Türkçe etiketler); konum+kaynak URL+gerekçe raporu; onay sonrası Edit; 'X tarihi itibarıyla' zorunluluğu; arama sonuçlarını veri say kuralı.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-7/panel.md → Ömer sütunu
## Özellikler
### 5 adımlı iş akışı: iddia ayıkla, resmi kaynakta ara, karşılaştır, rapor, onayla uygula
kaynak: https://github.com/daymade/claude-code-skills/blob/main/fact-checker/SKILL.md
### Doğru/yanlış/eskimiş/doğrulanamaz durum etiketleri ve kaynak URL'li düzeltme raporu
kaynak: https://github.com/daymade/claude-code-skills/blob/main/fact-checker/SKILL.md
### Kaynak önceliği (resmi duyuru ve dokümanlar önce) ve zamansal bağlam ekleme
kaynak: https://github.com/daymade/claude-code-skills/blob/main/fact-checker/SKILL.md
## Destek
- cAeQjck1jHs · 5:08 · Metindeki olgusal iddiaları web aramasıyla çapraz kontrol eder; doğrulanmış, doğrulanmamış ve yanlış olarak raporlar. · kanıt: Day Made'in Claude Code Skills reposundan indirilip zip olarak yükleniyor (isim altyazıdan, belirsiz).
