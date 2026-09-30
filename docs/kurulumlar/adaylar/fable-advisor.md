# Fable advisor
ad: Fable advisor
tur: skill
video: V0XbuApxlhg
repo: dannymac180/fable-advisor
lisans: bilinmiyor (repoda LICENSE dosyası var, ancak README çıktısında lisans türü kesildi; SPDX doğrulanmadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/DannyMac180/fable-advisor
telemetri: README'de telemetri belirtilmiyor. Eklentinin kendi telemetrisi yok gibi görünüyor ama kod okunmadı: bilinmiyor. Not: spec ve kod Codex CLI üzerinden OpenAI'a, inceleme için Anthropic'e gider.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun)
## Ne
Claude Code oturumunu "mimar" yapıp kod yazma işini OpenAI Codex CLI üzerinden GPT-6 Luna/Sol modellerine devreden, kritik kararlarda ve işin sonunda Fable 5.1 ile temiz bağlamlı, salt-okunur inceleme yaptıran eklenti. Videoda (V0XbuApxlhg, 13:51) yalnızca "Fable advisor gibi repolar var" denmiş, URL verilmemiş; aday adıyla eşleşen repo aramayla bulundu. Aynı adla birçok fork var (IpiggyI, birhantprkc, DannyMac180, timurlain vb.); asıl kaynak hangisi doğrulanamadı, incelenen DannyMac180 sürümü.
## Mekanizma
Claude Code'un alt ajan başına model seçebilme özelliğini kullanır. Üç ajan: luna-implementer (rutin iş, gpt-6-luna, varsayılan effort max), sol-implementer (karmaşık iş, gpt-6-sol, effort high), fable-advisor (model: fable, salt-okunur inceleyici; ship / fix-first / rethink kararı verir). Implementer ajanlar `codex exec` ile Codex CLI'yi çağırır. Orkestrasyon skill'i yönlendirme tablosunu, altı parçalı spec sözleşmesini ve doğrulama kurallarını oturuma öğretir. /fable-advisor:setup seçimleri ~/.claude/fable-advisor/lanes.json dosyasına yazar. Codex yoksa lane "STATUS: unavailable" döner, sessizce Claude'a düşmez; yalnızca advisor moduna inilir. Hafif mod: agents/fable-advisor.md dosyasını ~/.claude/agents/ altına kopyalamak.
## Kanıt
- Fable'ın GPT modellerini danışman/uygulayıcı olarak çağırmasını sağlayan repo var → doğrulandı · README: luna-implementer ve sol-implementer ajanları Codex CLI ile GPT-6 modellerini çağırır; Fable 5.1 inceleyicidir.
- Anthropic'e 20 kat fazla ödüyorsunuz (video başlığı) → sınanamadı · README'de ölçülmüş maliyet karşılaştırması yok; yalnızca 'bir danışma birkaç sent' gibi niteliksel ifade var.
- Depo tek ve asıl kaynak belli → sınanamadı · Aramada aynı ad ve açıklamayla en az 8 farklı kullanıcı reposu çıktı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- claude plugin marketplace add DannyMac180/fable-advisor
- claude plugin install fable-advisor@fable-advisor
- Codex CLI kur ve giriş yap: npm i -g @openai/codex ; codex login
- Bir kez /fable-advisor:setup çalıştır (lane modelleri ve effort seçimi)
- Gereksinim: Claude Code >= 2.1.170; CLAUDE_CODE_SUBAGENT_MODEL ortam değişkenini ayarlama (advisor pinini ezer)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Pahalı modeli yalnızca karar ve inceleme noktalarına ayırarak maliyeti düşürür; farklı model ailesinden implementer ile çapraz-satıcı inceleme sağlar. Bizim için asıl değer, "danışman ajan + yönlendirme doktrini" deseninin kendisi.
## Maliyet/risk
Lisans doğrulanmadı. Çok sayıda fork var, hangisi asıl belirsiz. Codex CLI ve GPT-6 erişimi gerekir, ek ücret ve OpenAI'a veri gönderimi doğurur. Sabitlenmiş Claude modeli hesapta yoksa Claude Code sessizce oturum modeline düşer, inceleme kalitesi fark edilmeden düşer. Kod yazan lane'ler harici süreç çalıştırır; ajan dosyaları kurmadan önce okunmalı. Ürün adları (Fable 5.1, GPT-6) benim bilgi alanımda doğrulanamadı; yalnızca README'ye dayanıyor.
## Tasarruf
Evet, token/maliyet yönlendirmesi: oturum modeli yalnızca yargı ve spec üretir; kodun büyük kısmını daha ucuz GPT lane'leri yazar; pahalı Fable yalnızca mimari karar ve son incelemede kullanılır. Skill ayrıca oturumun bağlamını yalın tutmayı ve geniş keşfi ucuz salt-okunur ajanlara vermeyi söyler. Somut tasarruf oranı ölçülmedi; videodaki "20x" başlığı iddiasına README'de kanıt yok.
## Üretilebilir
hedef_tur: skill
tarif: Kendi skill'imizi yaz: (1) agents/advisor.md: model'i pinlenmiş, yalnızca Read/Grep/Glob araçlı, temiz bağlamda çalışan salt-okunur inceleme ajanı; çıktı ship/fix-first/rethink. (2) skills/orchestration/SKILL.md: hangi işin hangi lane'e gideceği tablosu, altı satırlık spec şablonu (hedef, dosyalar, kısıtlar, doğrulama, REASONING vb.), 'iş bitmeden advisor incelemesi' kuralı. (3) İsteğe bağlı implementer ajanı: `codex exec` çağıran, çıktıyı yapılandırılmış STATUS ile döndüren sarmalayıcı. (4) CLAUDE.md'ye tek satırlık zorunlu-danışma kuralı. Önce yalnızca (1)+(4) ile başla; Codex bağımlılığını sonra ekle.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun/panel.md → Ömer sütunu
## Özellikler
### Mimar deseni: oturum spec yazar, uygulama lane'lere gider, iş sonunda Fable incelemesi zorunlu
kaynak: https://github.com/DannyMac180/fable-advisor
### Lane başına varsayılan reasoning effort ve spec'teki REASONING satırıyla geçersiz kılma
kaynak: https://github.com/DannyMac180/fable-advisor
### Hafif mod: tek dosyalık fable-advisor ajanı ile yalnızca kritik noktalarda danışma
kaynak: https://github.com/DannyMac180/fable-advisor
### /fable-advisor:setup ile lane modeli seçimi, lanes.json'a kayıt
kaynak: https://github.com/DannyMac180/fable-advisor
### Opsiyonel resmi Codex eklentisiyle /codex:adversarial-review ikinci inceleme
kaynak: https://github.com/openai/codex-plugin-cc
## Destek
- V0XbuApxlhg · 13:51 · Fable'ın GPT modellerini danışman olarak çağırmasını sağlayan repo (adı yalnızca söylendi, URL yok). · kanıt: There's other repos like this Fable advisor that do exactly that.
