# prd-to-issues
ad: prd-to-issues
tur: skill
video: EJyuu6zlQCg
repo: mattpocock/skills
lisans: bilinmiyor (repoda LICENSE dosyası var ama türü okunamadı; MIT olması muhtemel, doğrulanmadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/mattpocock/skills
telemetri: Skill'in kendisi metin dosyası olduğu için telemetri yok gibi görünüyor, ama kodunu incelemedim. skills.sh yükleyicisinin (npx skills) kendi telemetrisi olup olmadığı bilinmiyor.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-4)
## Ne
Bir PRD'yi/planı, tracer-bullet mantığıyla dikey dilimlere bölüp proje issue tracker'ında (GitHub, Linear ya da yerel dosya) bağımsız alınabilir issue'lar olarak yayınlayan agent skill'i. Matt Pocock'un skills reposunun parçası. Videoda (EJyuu6zlQCg, "5 Claude Code skills I use every single day") PRD'yi bir Kanban tahtasına çevirdiği söyleniyor.
## Mekanizma
Saf prompt (SKILL.md) tabanlı. Ajan planı okur ve şema, API, UI, test gibi tüm katmanları uçtan uca kesen ince dikey dilimlere böler. Yatay katman bazlı bölme yapmaz. Her dilimi HITL (insan kararı/incelemesi gerekir) ya da AFK (insansız uygulanıp merge edilebilir) diye sınıflar ve AFK'yı tercih eder. Önerilen dökümü kullanıcıya gösterip düzeltme alır. Onaydan sonra issue'ları bağımlılık sırasına göre, blocked-by ilişkileriyle tracker'a açar. Tracker seçimi `/setup-matt-pocock-skills` ile yapılır. Bu bilgiler web arama özetlerinden geliyor; SKILL.md'yi doğrudan okuyamadım.
## Kanıt
- PRD'yi tracer-bullet dikey dilimlere böler → doğrulandı · Web arama özetleri (skills.sh, mcpservers.org, hackernoon sayfaları) tracer-bullet dikey dilimleri anlatıyor; SKILL.md'nin kendisini okumadım.
- Bloklama ilişkili bağımsız issue'lar üretir → doğrulandı · Arama özeti: issue'lar bağımlılık sırasıyla yayınlanıyor. Blocked-by alanının açıkça geçtiğini görmedim.
- Kanban tahtasına çevirir (video) → sınanamadı · Yalnızca video alıntısı var; transkripti getir çıktısı vermedi (sadece sayfa iskeleti geldi).
- Skill adı prd-to-issues → çürütüldü · Güncel repoda yol skills/engineering/to-issues; prd-to-issues eski ad olarak görünüyor (skills.lc ve SkillsMP'de eski adla listeli).
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- claude plugins install mattpocock-skills (ya da oturum içinden /plugin install mattpocock-skills)
- Alternatif, düzenlenebilir kopya: npx skills@latest add mattpocock/skills (to-issues ve setup-matt-pocock-skills seçilmeli)
- Repo başına bir kez /setup-matt-pocock-skills çalıştırıp issue tracker, etiketler ve doküman konumunu seç
- Not: videodaki ad 'prd-to-issues', güncel repoda 'skills/engineering/to-issues' olarak geçiyor (yeniden adlandırılmış görünüyor)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Büyük bir PRD'yi paralel yürütülebilir, uçtan uca test edilebilir küçük işlere çevirir. HITL/AFK ayrımı hangi işin insansız yapılabileceğini gösterir. Bağımlılık sırası ve bloklama ilişkisi net olur.
## Maliyet/risk
Repo doğrudan doğrulanamadı: aday adı repoda geçmiyor, yeniden adlandırma web aramasına dayanıyor. Lisans türü bilinmiyor. Plugin kurulumu salt okunur ve otomatik güncellenir, yani yukarı akış değişikliği davranışı sessizce değiştirebilir. Issue açma, tracker'a yazma yetkisi gerektirir; onay adımı atlanmamalı.
## Tasarruf
Token aracı değil. Dolaylı fayda: küçük, bağımsız dilimler her ajan oturumunun bağlamını küçük tutar.
## Üretilebilir
hedef_tur: skill
tarif: Tek bir SKILL.md yeterli. Adımlar: 1) PRD/planı oku. 2) Katmanları uçtan uca kesen ince dikey dilimlere böl. 3) Her dilim için başlık, kabul ölçütü, blocked-by ve HITL/AFK etiketi yaz. 4) Dökümü kullanıcıya göster ve onay al. 5) `gh issue create` ile bağımlılık sırasına göre aç. Sonraki issue'lara önceki issue numaralarını 'Blocked by #N' olarak yaz. Tracker seçimini repo yapılandırma dosyasından oku. Kod gerekmez. Bir kez yazılınca yukarı akışa bağımlılık kalmaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-4/panel.md → Ömer sütunu
## Özellikler
### Tracer-bullet dikey dilimleme: her issue tüm katmanları uçtan uca keser
kaynak: https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md
### HITL/AFK sınıflaması, AFK öncelikli
kaynak: https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md
### Yayından önce döküm kullanıcıya gösterilip yinelenir
kaynak: https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md
### Issue'lar bağımlılık sırasında tracker'a açılır (GitHub, Linear ya da yerel dosya)
kaynak: https://github.com/mattpocock/skills
## Destek
- EJyuu6zlQCg · 6:00 · PRD'yi tracer-bullet mantığıyla dikey dilimlere, bloklama ilişkili bağımsız GitHub issue'larına böler. · kanıt: it takes a PRD, takes the destination, and it turns it into a Kanban board
