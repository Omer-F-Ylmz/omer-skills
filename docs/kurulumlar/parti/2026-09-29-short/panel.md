# Karar paneli — 2026-09-29-short

Ömer sütununa AL / RED / ERTELE ya da karar (DENE · ÖĞREN · UYARLA · ZATEN VAR) yaz; boş satır dokunulmaz → `video panel uygula <bu dosya>`.

| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |
|---|---|---|---|---|---|---|---|
| ucretsiz-llm-api-listesi-reposu | teknik | 1 | — | koşmadı: repo yok | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| openrouter | CLI | 1 | yok | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | ZATEN VAR |
| groq | CLI | 1 | yok | koşmadı: servis | SOR | servis: koşullar · ücretsiz katman · gizlilik · eksik: kullanim_kosullari, ucretsiz_katman, veri_gizliligi | DENE |
| nvidia-nim | CLI | 1 | bilinmiyor | koşmadı: servis | SOR | servis: koşullar · ücretsiz katman · gizlilik · eksik: kullanim_kosullari, ucretsiz_katman, veri_gizliligi | DENE |
| kimi-deepseek-gemini-ucretsiz-erisim | teknik | 1 | — | koşmadı: servis | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| saglayici-api-anahtarini-claude-code-cur | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | RED |
| claude-code | CLI | 1 | bilinmiyor | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | ZATEN VAR |
| cursor | CLI | 1 | yok | koşmadı: servis | SOR | servis: koşullar · ücretsiz katman · gizlilik · eksik: kullanim_kosullari, ucretsiz_katman, veri_gizliligi | ÖĞREN |
| basit-uygulama-islerini-ucretsiz-modele- | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| jcode | CLI | 1 | MIT | koşmadı: kurulu | ZATEN VAR | eşdeğer: codex p 0.75 | UYARLA |
| otomatik-hafiza | teknik | 1 | — | koşmadı: ürün | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| coklu-paralel-oturum | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | RED |
| ajan-yardimci-ajan-orkestrasyonu | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| harness-kavrami | teknik | 1 | — | koşmadı: servis | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| graphify | CLI | 2 | Apache-2.0 (README rozeti; depoda ayrıca LICENSE-MIT dosyası var, bir web sonucu MIT diyor. Çift lisans olabilir, doğrulanmadı) | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | ZATEN VAR |
| webcmd | skill | 1 | Apache-2.0 | koşmadı: SkillSpector raporu yok | SOR | eksik: son_commit | UYARLA |
| markitdown-microsoft | CLI | 1 | MIT | koşmadı: SkillSpector raporu yok | SOR | eksik: son_commit | DENE |
| headroom | CLI | 1 | Apache-2.0 | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | ZATEN VAR |
| codeburn | CLI | 1 | bilinmiyor (repoda LICENSE dosyası var, içeriği okunamadı) | koşmadı: servis | SOR | servis: koşullar · ücretsiz katman · gizlilik · eksik: kullanim_kosullari, ucretsiz_katman, veri_gizliligi | ERTELE |
| ponytail | CLI | 1 | MIT | koşmadı: kurulu | ZATEN VAR | kurulu: ponytail | ZATEN VAR |
| find-skills | skill | 1 | — | koşmadı: repo yok | SOR | araştırılmadı (tavan) | |
| superpowers | skill | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: superpowers | ZATEN VAR |
| claude-mem | plugin | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: claude-mem | ZATEN VAR |
| impeccable | skill | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: impeccable | ZATEN VAR |
| task-observer | skill | 1 | — | koşmadı: kurulu | SOR | olası eşdeğer: anthropic-skills:task-observer p 0.73 | |

## form_red
- M9qgd_KJkWc: ['M9qgd_KJkWc.aciklama_baglantilari: karar yok: https://www.skool.com/buildroom/', 'M9qgd_KJkWc.iddialar[2].karede_gorulen: kare gönderildi, karede görülen boş olamaz', 'M9qgd_KJkWc rapor: kanıt zaman
## Belirsiz birleşmeler (ad benzer, repo farklı)
- yok
## ÜRETİLEBİLİR / yapım tarifleri
- groq: hedef_tur: CLI tarif: Ucuz alt görevler için ince bir 'groq-ask' CLI/skill: GROQ_API_KEY ortam değişkenini okur, https://api.groq.com/openai/v1/chat/completions adresine model (örn. openai/gpt-oss-20b) ve prompt gönderir, çıktıyı stdout'a yazar. 429 durumunda geri çekilip tekrar dener. Anahtar koda gömülmez.
- nvidia-nim: hedef_tur: skill tarif: NIM'i kopyalamak mümkün değil, ama onu kullanan bir skill yazılabilir. Skill; NVIDIA_API_KEY ortam değişkenini okuyup integrate.api.nvidia.com/v1'e OpenAI uyumlu istek atar. Ucuz veya toplu görevleri (özetleme, sınıflandırma) ücretsiz modele yönlendirir. 429 gelirse geri çekilip yeniden dener, 40 RPM üstüne çıkmaz. Anahtar dosyaya yazılmaz.
- jcode: hedef_tur: hook tarif: JCode'un tamamı üretilemez, ama bağlam tasarrufu fikirleri Claude Code hook'u olarak yapılabilir. PostToolUse hook'u yaz. Grep/Read çıktısını oturumdaki görülmüş satır/dosya karma listesiyle karşılaştır ve tekrar eden içeriği 'daha önce görüldü' özetiyle kısalt. Ayrıca grep sonuçlarına dosya başına sembol/yapı özeti ekleyen küçük bir CLI (ctags veya tree-sitter tabanlı) yaz. Oturum hafızası için yerel bir gömme dizini kullanan bir MCP sunucusu düşünülebilir. Swarm modu kapsam dışı.
- graphify: hedef_tur: CLI tarif: Graphify zaten kurulabilir bir CLI+skill olduğundan kopyalamak yerine doğrudan kullanmak daha mantıklı. Hafif bir sürüm için: Python CLI yaz, tree-sitter ile dosyalardan sembol, import ve call kenarlarını çıkar, networkx ile graph.json üret, query/path/explain alt komutları ekle. Ardından bir SKILL.md ile Claude'a 'önce graph.json'ı sorgula' talimatı ver ve isteğe bağlı bir PreToolUse hook'u ile ilk ham Read'i grafiğe yönlendir.
- webcmd: hedef_tur: skill tarif: Kendi 'site-hafizasi' skill'imiz: ajan bir siteyi gezdikten sonra alan adı başına bir markdown dosyası (~/.claude/site-memory/<domain>.md) yazsın: giriş/arama URL'leri, çalışan seçiciler, bulunan iç API uçları, tuzaklar, yedek yollar. Görev başında skill o alan adı dosyasını okur, yoksa normal keşfeder; bitince yalnız doğrulanmış yeni bilgiyi ekler (canlı sayfa esas kabul edilir). Tarayıcı kontrolü için mevcut Playwright/Chrome MCP kullanılır; ek olarak SessionEnd/Stop hook'u ile öğrenme notu hatırlatılabilir. Bulut seed ve stealth kısmı yapılmaz.
- markitdown-microsoft: hedef_tur: skill tarif: Ayrı bir araç yazmaya gerek yok, markitdown'ı sarmalayan bir skill yeterli. Skill, kullanıcı PDF/DOCX/XLSX/PPTX verdiğinde önce `markitdown <dosya> -o <dosya>.md` komutunu çalıştırır. Sonra ham dosyayı değil .md çıktısını okur. Kurulum adımı olarak `pip install 'markitdown[pdf,docx,pptx,xlsx]'` eklenir. Güvenilmeyen kaynaklar için dosya yolunu doğrulama kuralı konur. İstenirse `markitdown-mcp` paketi MCP olarak bağlanır. Token tasarrufunu, dönüşümden önce ve sonra karakter sayısını karşılaştırarak ölçen bir adım da eklenebilir.
- headroom: hedef_tur: hook tarif: Tam proxy yerine hafif bir Claude Code PostToolUse hook'u: Bash/Read çıktısı eşiği (örn. >8k token) aşarsa (1) JSON'u alan/dizi örnekleyerek özetle, (2) log'ları tekrarlayan satırları grupla ama ERROR/FATAL/stack trace satırlarını aynen koru, (3) tam çıktıyı yerel bir dosyaya (.cache/ccr/<hash>.txt) yaz ve özetin sonuna 'tam çıktı: <yol>' referansı ekle; modele bu dosyayı Read ile geri çağırma imkanı ver. İstenirse ek olarak `retrieve`/`stats` için küçük bir MCP sunucusu. Kompress benzeri ML modeli gerektirmez; kural tabanlı başla, ölçüm için önce/sonra token sayısını logla.
- codeburn: hedef_tur: skill tarif: Kendi skill'imiz `codeburn` CLI'ını çağırsın. Örneğin `npx codeburn` ve `codeburn optimize` çıktısını özetlesin. Bağımsız bir sürüm için Claude Code oturum JSONL dosyalarını (~/.claude/projects) okuyan küçük bir Node veya Python betiği yazılabilir. Betik usage alanlarını toplayıp model fiyat tablosuyla çarpar, proje ve gün bazında tablo verir. Bunu bir SessionEnd hook'una da bağlayabiliriz. Optimize benzeri bulgular için CLAUDE.md boyutunu ve kullanılmayan MCP'leri kontrol eden ek kurallar eklenebilir.
- ponytail: hedef_tur: skill tarif: Bir SKILL.md yaz. Ajana kod yazmadan önce 7 basamaklı merdiveni (gerekli mi, kod tabanında var mı, stdlib, native özellik, mevcut bağımlılık, tek satır, minimum) uygulamasını söyle. Önce ilgili kodu okumayı ve doğrulama, hata yönetimi, güvenlik ve erişilebilirliği asla kesmemeyi şart koş. Önce/sonra örnekleri ekle. Etkiyi kendi ortamımızda 5-10 görevle git diff satırı ve token ölçerek sına. Kopyalamak yerine MIT lisansına atıf vererek sıfırdan yazmak daha temiz.
## Kural önerileri (T0)
- saglayici-api-anahtarini-claude-code-cur: Üçüncü taraf anahtarla ajanı ücretsiz modelle çalıştırma
- basit-uygulama-islerini-ucretsiz-modele-: Ajan Claude'da kalırken uygulamadaki basit işlemler ücretsiz modelle yapılır
- coklu-paralel-oturum: Yavaşlama olmadan birden çok oturumu aynı anda çalıştırma
- ajan-yardimci-ajan-orkestrasyonu: Bir ajan yönetir, diğerleri aynı kod tabanında çakışmadan çalışır
## OLASI EŞDEĞER (Jev p 0.5–0.75)
- task-observer ≈ anthropic-skills:task-observer p 0.73
## OLASI TEKRAR
- yok
## Araştırılmadı
- find-skills: tavan parti tavanı
## Defter
21 çağrı · $1.3104 · 331015 jeton
