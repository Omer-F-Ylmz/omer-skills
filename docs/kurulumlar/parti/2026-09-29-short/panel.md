# Karar paneli — 2026-09-29-short

Ömer sütununa AL / RED / ERTELE ya da karar (DENE · ÖĞREN · UYARLA · ZATEN VAR) yaz; boş satır dokunulmaz → `video panel uygula <bu dosya>`.

| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |
|---|---|---|---|---|---|---|---|
| ucretsiz-llm-api-deposu-adi-belirtilmemi | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | |
| jcode | CLI | 1 | MIT | koşmadı: kurulu | ZATEN VAR | eşdeğer: codex p 0.75 | UYARLA |
| harness-katmani-ajan-ara-katmani | teknik | 1 | — | koşmadı: servis | ÖĞREN | teknik: kurulabilir araç değil | |
| graphify | CLI | 2 | Apache-2.0 (README rozeti; depoda ayrıca LICENSE-MIT dosyası var, bir web sonucu MIT diyor. Çift lisans olabilir, doğrulanmadı) | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | ZATEN VAR |
| webcmd | CLI | 1 | Apache-2.0 | koşmadı: SkillSpector raporu yok | SOR | eksik: son_commit | UYARLA |
| headroom | CLI | 1 | Apache-2.0 | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | ZATEN VAR |
| codeburn | CLI | 1 | bilinmiyor (repoda LICENSE dosyası var, içeriği okunamadı) | koşmadı: servis | SOR | servis: koşullar · ücretsiz katman · gizlilik · eksik: kullanim_kosullari, ucretsiz_katman, veri_gizliligi | ERTELE |
| ponytail | CLI | 1 | MIT | koşmadı: kurulu | ZATEN VAR | kurulu: ponytail | ZATEN VAR |
| find-skills | skill | 1 | — | koşmadı: repo yok | SOR | araştırılmadı (tavan) | |
| superpowers | skill | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: superpowers | ZATEN VAR |
| claude-mem | plugin | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: claude-mem | ZATEN VAR |
| impeccable | skill | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: impeccable | ZATEN VAR |
| task-observer | skill | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: anthropic-skills:task-observer | |

## form_red
- NogIRR1B6gY: ['NogIRR1B6gY.adaylar[0].karede_gorulen: kare gönderildi, karede görülen boş olamaz']
- M9qgd_KJkWc: ['M9qgd_KJkWc.adaylar[1].karede_gorulen: kare gönderildi, karede görülen boş olamaz', 'M9qgd_KJkWc rapor: kanıt zamansız: Framer Motion (m:ss + kare yolu ya da altyazı)', 'M9qgd_KJkWc rapor: kanıt zam
## Belirsiz birleşmeler (ad benzer, repo farklı)
- yok
## ÜRETİLEBİLİR / yapım tarifleri
- jcode: hedef_tur: hook tarif: JCode'un tamamı üretilemez, ama bağlam tasarrufu fikirleri Claude Code hook'u olarak yapılabilir. PostToolUse hook'u yaz. Grep/Read çıktısını oturumdaki görülmüş satır/dosya karma listesiyle karşılaştır ve tekrar eden içeriği 'daha önce görüldü' özetiyle kısalt. Ayrıca grep sonuçlarına dosya başına sembol/yapı özeti ekleyen küçük bir CLI (ctags veya tree-sitter tabanlı) yaz. Oturum hafızası için yerel bir gömme dizini kullanan bir MCP sunucusu düşünülebilir. Swarm modu kapsam dışı.
- graphify: hedef_tur: CLI tarif: Graphify zaten kurulabilir bir CLI+skill olduğundan kopyalamak yerine doğrudan kullanmak daha mantıklı. Hafif bir sürüm için: Python CLI yaz, tree-sitter ile dosyalardan sembol, import ve call kenarlarını çıkar, networkx ile graph.json üret, query/path/explain alt komutları ekle. Ardından bir SKILL.md ile Claude'a 'önce graph.json'ı sorgula' talimatı ver ve isteğe bağlı bir PreToolUse hook'u ile ilk ham Read'i grafiğe yönlendir.
- webcmd: hedef_tur: skill tarif: Kendi 'site-hafizasi' skill'imiz: ajan bir siteyi gezdikten sonra alan adı başına bir markdown dosyası (~/.claude/site-memory/<domain>.md) yazsın: giriş/arama URL'leri, çalışan seçiciler, bulunan iç API uçları, tuzaklar, yedek yollar. Görev başında skill o alan adı dosyasını okur, yoksa normal keşfeder; bitince yalnız doğrulanmış yeni bilgiyi ekler (canlı sayfa esas kabul edilir). Tarayıcı kontrolü için mevcut Playwright/Chrome MCP kullanılır; ek olarak SessionEnd/Stop hook'u ile öğrenme notu hatırlatılabilir. Bulut seed ve stealth kısmı yapılmaz.
- headroom: hedef_tur: hook tarif: Tam proxy yerine hafif bir Claude Code PostToolUse hook'u: Bash/Read çıktısı eşiği (örn. >8k token) aşarsa (1) JSON'u alan/dizi örnekleyerek özetle, (2) log'ları tekrarlayan satırları grupla ama ERROR/FATAL/stack trace satırlarını aynen koru, (3) tam çıktıyı yerel bir dosyaya (.cache/ccr/<hash>.txt) yaz ve özetin sonuna 'tam çıktı: <yol>' referansı ekle; modele bu dosyayı Read ile geri çağırma imkanı ver. İstenirse ek olarak `retrieve`/`stats` için küçük bir MCP sunucusu. Kompress benzeri ML modeli gerektirmez; kural tabanlı başla, ölçüm için önce/sonra token sayısını logla.
- codeburn: hedef_tur: skill tarif: Kendi skill'imiz `codeburn` CLI'ını çağırsın. Örneğin `npx codeburn` ve `codeburn optimize` çıktısını özetlesin. Bağımsız bir sürüm için Claude Code oturum JSONL dosyalarını (~/.claude/projects) okuyan küçük bir Node veya Python betiği yazılabilir. Betik usage alanlarını toplayıp model fiyat tablosuyla çarpar, proje ve gün bazında tablo verir. Bunu bir SessionEnd hook'una da bağlayabiliriz. Optimize benzeri bulgular için CLAUDE.md boyutunu ve kullanılmayan MCP'leri kontrol eden ek kurallar eklenebilir.
- ponytail: hedef_tur: skill tarif: Bir SKILL.md yaz. Ajana kod yazmadan önce 7 basamaklı merdiveni (gerekli mi, kod tabanında var mı, stdlib, native özellik, mevcut bağımlılık, tek satır, minimum) uygulamasını söyle. Önce ilgili kodu okumayı ve doğrulama, hata yönetimi, güvenlik ve erişilebilirliği asla kesmemeyi şart koş. Önce/sonra örnekleri ekle. Etkiyi kendi ortamımızda 5-10 görevle git diff satırı ve token ölçerek sına. Kopyalamak yerine MIT lisansına atıf vererek sıfırdan yazmak daha temiz.
## Kural önerileri (T0)
- ucretsiz-llm-api-deposu-adi-belirtilmemi: Ücretsiz API sunan sağlayıcılardan (Open Router, Groq, Nvidia NIM) anahtar üretip Claude Code veya Cursor'a vermek.
## OLASI EŞDEĞER (Jev p 0.5–0.75)
- yok
## OLASI TEKRAR
- yok
## Araştırılmadı
- find-skills: tavan parti tavanı
## Defter
28 çağrı · $1.8325 · 427929 jeton
