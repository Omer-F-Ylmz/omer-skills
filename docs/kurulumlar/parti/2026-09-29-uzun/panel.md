# Karar paneli — 2026-09-29-uzun

Ömer sütununa AL / RED / ERTELE ya da karar (DENE · ÖĞREN · UYARLA · ZATEN VAR) yaz; boş satır dokunulmaz → `video panel uygula <bu dosya>`.

| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |
|---|---|---|---|---|---|---|---|
| token-kullanim-denetim-promptu | prompt | 1 | — | koşmadı: repo yok | ÖĞREN | prompt: kurulabilir araç değil || ÖĞREN |
| clear | ipucu | 1 | — | koşmadı: kurulu | SOR | eşdeğer doğrulanmadı: learn || ZATEN VAR |
| model-effort-u-oturum-basinda-sabitle | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) || ZATEN VAR |
| cikti-filtreleme-hook-dosyasi | teknik | 1 | — | koşmadı: repo yok | ÖĞREN | teknik: kurulabilir araç değil || ÖĞREN |
| mcp-sunucu-listesi-ile-kullanilmayanlari | MCP | 1 | yok | koşmadı: repo yok | SOR | eksik: son_commit || RED |
| subagent-i-haiku-ya-ayarlama | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) || DENE |
| rewind | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) || ZATEN VAR |
| context-usage-cost-ve-yanma-hizi-gosterg | CLI | 1 | — | koşmadı: kurulu | SOR | servis: koşullar · ücretsiz katman · gizlilik · eksik: kullanim_kosullari, ucretsiz_katman, veri_gizliligi || ERTELE |
| claude-code-yapilandirmasini-token-tuket | prompt | 1 | — | koşmadı: servis | ÖĞREN | prompt: kurulabilir araç değil || ÖĞREN |
| arac-ciktisini-ajan-gormeden-once-filtre | prompt | 1 | — | koşmadı: repo yok | ÖĞREN | prompt: kurulabilir araç değil || ÖĞREN |
| token-dashboard | teknik | 1 | — | koşmadı: repo yok | ÖĞREN | teknik: kurulabilir araç değil || ÖĞREN |
| session-handoff-skill | skill | 1 | bilinmiyor | koşmadı: repo yok | SOR | eksik: lisans, son_commit || UYARLA |
| clear-ve-compact-ile-temiz-baslangic | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) || ZATEN VAR |
| claude-projelerine-belge-koymak | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) || ÖĞREN |
| oturum-ortasinda-claude-md-duzenleme | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) || ÖĞREN |
| github-reposundaki-token-dashboard-u-cla | prompt | 1 | — | koşmadı: repo yok | ÖĞREN | prompt: kurulabilir araç değil || ÖĞREN |
| rtk | CLI | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız || ZATEN VAR |
| headroom | CLI | 1 | Apache-2.0 | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız || ZATEN VAR |
| ponytail | skill | 1 | MIT | koşmadı: kurulu | ZATEN VAR | kurulu: ponytail || ZATEN VAR |
| graphify | skill | 1 | Apache-2.0 (README rozeti; depoda ayrıca LICENSE-MIT dosyası var, bir web sonucu MIT diyor. Çift lisans olabilir, doğrulanmadı) | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız || ZATEN VAR |
| rtk-etkinken-claude-code-a-commit-ve-pus | prompt | 1 | — | koşmadı: servis | ÖĞREN | prompt: kurulabilir araç değil || ÖĞREN |
| headroom-sarmali-oturumda-simplify-skill | prompt | 1 | — | koşmadı: ürün | ÖĞREN | prompt: kurulabilir araç değil || ÖĞREN |

## form_red
- yok
## Belirsiz birleşmeler (ad benzer, repo farklı)
- yok
## ÜRETİLEBİLİR / yapım tarifleri
- mcp-sunucu-listesi-ile-kullanilmayanlari: hedef_tur: skill tarif: 'mcp-temizlik' skill'i: adımlar olarak /mcp listesini al, her sunucunun son 30 gündeki kullanımını (oturum kayıtlarından/kullanıcıdan) sor, kullanılmayanları kapatmayı öner, ardından /context ile tools satırını kontrol ettir. Kod gerektirmez; salt talimat metni yeterli.
- session-handoff-skill: hedef_tur: skill tarif: ~/.claude/skills/session-handoff/SKILL.md oluştur. Frontmatter: name: session-handoff, description: 'Oturumu /clear öncesi devretmek için özet üret'. Gövde: modele şu başlıklarla kısa bir Markdown üretmesini söyle: 1) Hedef, 2) Yapılanlar, 3) Değişen/önemli dosyalar (yol + tek satır neden), 4) Açık kararlar ve engeller, 5) Sonraki adım (ilk yapılacak komut). Kurallar: en fazla ~300 kelime, sır/anahtar yazma, git status/diff'e bakarak dosya listesini doğrula, çıktıyı tek kod bloğunda ver ki kopyalanabilsin. İsteğe bağlı: özeti HANDOFF.md dosyasına yaz ve yeni oturumda okut.
- headroom: hedef_tur: hook tarif: Tam proxy yerine hafif bir Claude Code PostToolUse hook'u: Bash/Read çıktısı eşiği (örn. >8k token) aşarsa (1) JSON'u alan/dizi örnekleyerek özetle, (2) log'ları tekrarlayan satırları grupla ama ERROR/FATAL/stack trace satırlarını aynen koru, (3) tam çıktıyı yerel bir dosyaya (.cache/ccr/<hash>.txt) yaz ve özetin sonuna 'tam çıktı: <yol>' referansı ekle; modele bu dosyayı Read ile geri çağırma imkanı ver. İstenirse ek olarak `retrieve`/`stats` için küçük bir MCP sunucusu. Kompress benzeri ML modeli gerektirmez; kural tabanlı başla, ölçüm için önce/sonra token sayısını logla.
- ponytail: hedef_tur: skill tarif: Bir SKILL.md yaz. Ajana kod yazmadan önce 7 basamaklı merdiveni (gerekli mi, kod tabanında var mı, stdlib, native özellik, mevcut bağımlılık, tek satır, minimum) uygulamasını söyle. Önce ilgili kodu okumayı ve doğrulama, hata yönetimi, güvenlik ve erişilebilirliği asla kesmemeyi şart koş. Önce/sonra örnekleri ekle. Etkiyi kendi ortamımızda 5-10 görevle git diff satırı ve token ölçerek sına. Kopyalamak yerine MIT lisansına atıf vererek sıfırdan yazmak daha temiz.
- graphify: hedef_tur: CLI tarif: Graphify zaten kurulabilir bir CLI+skill olduğundan kopyalamak yerine doğrudan kullanmak daha mantıklı. Hafif bir sürüm için: Python CLI yaz, tree-sitter ile dosyalardan sembol, import ve call kenarlarını çıkar, networkx ile graph.json üret, query/path/explain alt komutları ekle. Ardından bir SKILL.md ile Claude'a 'önce graph.json'ı sorgula' talimatı ver ve isteğe bağlı bir PreToolUse hook'u ile ilk ham Read'i grafiğe yönlendir.
## Kural önerileri (T0)
- model-effort-u-oturum-basinda-sabitle: Model, effort veya fast mode değişimi cache'i geçersiz kılar; baştan seçip dokunmamak gerekir.
- subagent-i-haiku-ya-ayarlama: Yüksek hacimli izole işlerde subagent modelini Haiku yapmak ana oturum cache'ine dokunmadan maliyeti düşürür.
- rewind: Birkaç turu geri almak için compact yerine kullanılır; cache'in bildiği noktaya döner.
- clear-ve-compact-ile-temiz-baslangic: Görev değiştirirken /clear veya /compact ile yeni başla; uzun beklemeden sonra oturumu devret.
- claude-projelerine-belge-koymak: Claude chat'te büyük belgeleri sohbete yapıştırmak yerine proje içine koymak; dosyalar farklı önbelleklenir (belgelenmemiş, tahmin).
- oturum-ortasinda-claude-md-duzenleme: CLAUDE.md oturum ortasında düzenlenebilir; değişiklik oturum yeniden başlayana dek uygulanmadığı için önbellek bozulmaz.
## OLASI EŞDEĞER (Jev p 0.5–0.75)
- yok
## OLASI TEKRAR
- yok
## Araştırılmadı
- yok
## Defter
8 çağrı · $0.5325 · 129735 jeton
