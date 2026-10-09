# Ruflo (videoda 'Rufflow')
ad: Ruflo (videoda 'Rufflow')
tur: plugin
video: DuDrHzaBQ3k
repo: ruvnet/ruflo
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/ruvnet/ruflo
telemetri: bilinmiyor. README'nin görünen kısmında telemetri açıklaması yok ve kod incelenmedi. Federasyon özelliği makineler arası iletişim kurar; ağa çıkışı kurulumdan önce doğrulanmalı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: atlandı (repo 591 MB olduğu için güvenlik ön taraması yapılmadı)
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Claude Code ve Codex için "ajan meta-harness": 100+ uzman ajan, koordineli sürüler (swarm), kendi kendine öğrenen hafıza, makineler arası federasyon ve güvenlik korumaları ekleyen bir yürütme katmanı. README'ye göre 314 MCP aracı, 26 CLI komutu ve 35 plugin var.
## Mekanizma
İki kurulum yolu var. (A) Claude Code plugin marketplace: `/plugin marketplace add ruvnet/ruflo`, ardından tek tek plugin kurulur (ruflo-core, ruflo-swarm, ruflo-rag-memory vb.). Bu yol çalışma alanına dosya yazmaz ve yalnızca slash komutları, ajan tanımları ve birkaç skill ekler. Yalnızca ruflo-core kendi MCP sunucusunu kaydeder. (B) `npx ruflo init`: `.claude/`, `.claude-flow/`, `CLAUDE.md`, yardımcı betikler ve settings dosyalarını yazar. Ayrıca MCP sunucusu, hook'lar ve daemon kurar. README'deki akış şeması: Kullanıcı → Ruflo (CLI/MCP) → Router → Swarm → Ajanlar → Hafıza → LLM sağlayıcıları, bir öğrenme döngüsü geri besler. Hook'lar görevleri otomatik yönlendirir, başarılı kalıplardan öğrenir ve ajanları arka planda koordine eder. Hafıza vektör veritabanına (agentdb/ruvector, RVF dosyaları) dayanır. Çekirdek Rust tabanlı (Cargo.toml, crates). Bunlar yalnızca README özetinden okundu, kodu incelenmedi.
## Kanıt
- Açık kaynak ve ücretsiz → doğrulandı · README MIT lisans rozeti gösteriyor ve repoda LICENSE dosyası var. Lisans metni okunmadı.
- 60+ ajanı koordine ediyor → doğrulandı · README 100+ ajandan söz ediyor (kurulum tablosunda 98 ajan). Bu sayı video iddiasını aşıyor ama ajanların çalışıp çalışmadığı denenmedi.
- Ortak hafıza ve model yönlendirmesi var → sınanamadı · README'de 'self-learning memory' ve 'Router' var, ancak çalışması denenmedi ve kodu incelenmedi.
- Token tasarrufu sağlıyor → sınanamadı · Görünen README kısmında ölçülmüş bir tasarruf verisi yok.
- güvenlik ön taraması: atlandı (repo 591 MB)
## Kurulum
- Hafif yol (Claude Code içinde): /plugin marketplace add ruvnet/ruflo
- /plugin install ruflo-core@ruflo (isteğe bağlı: ruflo-swarm@ruflo, ruflo-rag-memory@ruflo)
- Konsol/mod'lar için (Claude Code 2.1.287+): /plugin install ruflo-console@ruflo ; /plugin install ruflo-mods@ruflo ; /reload-plugins
- Tam yol: npx ruflo init → Claude Code'u yeniden başlat → /ruflo
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Çok ajanlı orkestrasyonu, oturumlar arası kalıcı hafızayı ve görev yönlendirmesini tek kurulumla sağlar. Plugin'ler ayrı ayrı kurulabildiği için yalnızca gereken parça alınabilir (örneğin sadece swarm ya da rag-memory).
## Maliyet/risk
Yüzey çok geniş: 314 MCP aracı, hook'lar, daemon ve CLAUDE.md/settings değişiklikleri. README mod'ların hesap izinleriyle çalıştığını, sandbox'a alınmadığını ve önce kodun okunması gerektiğini kendisi söylüyor. `npx ruflo init` çalışma alanına çok sayıda dosya yazar. Repo 591 MB olduğundan güvenlik ön taraması atlandı. Pazarlama dili (8.1M+ indirme, "self-learning") bağımsız doğrulanmadı. Federasyon, verinin makine dışına gitmesi riskini doğurur. Videoda "Completely free" deniyor ama bu yalnızca bir kare görüntüsüne dayanıyor.
## Tasarruf
Videoda "model yönlendirmesi" geçiyor. README'de görünen kısımda token tasarrufu iddiası ya da ölçümü yok. Router'ın görevi uygun modele yönlendirmesi maliyeti düşürebilir ama bu doğrulanmadı. Ayrıca 60+ ajan ve swarm koordinasyonu token tüketimini artırabilir.
## Üretilebilir
hedef_tur: hook
tarif: Tamamını kopyalamak yerine iki parça yapılabilir. (1) UserPromptSubmit hook'u: istemi sınıflandırıp (basit / orta / karmaşık) uygun alt ajanı ya da modeli öneren bir yönlendirici. (2) Basit bir SQLite/JSON hafıza skill'i: tamamlanan görevlerin özetini ve etiketlerini yazar, yeni oturumda SessionStart hook'u ile ilgili kayıtları bağlama ekler. Swarm koordinasyonu için Claude Code'un yerel alt ajan (Task) özelliği yeterli olabilir. Ruflo'nun swarm, federasyon ve vektör hafızası kapsamının tamamı karşılanmaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### 35 plugin'lik marketplace: core, swarm, autopilot, loop-workers, workflows, federation, agentdb, rag-memory, rvf, ruvector, knowledge-graph vb.
kaynak: https://github.com/ruvnet/ruflo
### `npx ruflo init` ile ajanlar, komutlar, skill'ler, MCP sunucusu, hook'lar ve daemon kurulumu
kaynak: https://github.com/ruvnet/ruflo
### /ruflo konsolu: Claude Code içinde 26 sayfalık kokpit ve Plugin Catalog (kur/etkinleştir/güncelle)
kaynak: https://github.com/ruvnet/ruflo
### Hook tabanlı otomatik görev yönlendirme ve başarılı kalıplardan öğrenme
kaynak: https://github.com/ruvnet/ruflo
### Federasyon: farklı makinelerdeki ajanların güvenli iş birliği
kaynak: https://github.com/ruvnet/ruflo
## Destek
- DuDrHzaBQ3k · 0:03 · 60+ ajanı koordine eden, ortak hafıza ve model yönlendirmesi olan açık kaynak Claude Code çoklu ajan aracı. · kanıt: Karede GitHub deposu ruvnet / ruflo ve 'Completely free' görülüyor. (karede: Kare 0:03: GitHub sayfası 'ruvnet / ruflo' Public, taç ve GitHub logosu, 'Completely free' yazısı.)
