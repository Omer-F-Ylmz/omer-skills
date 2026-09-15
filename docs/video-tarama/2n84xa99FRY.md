# Yapay Zekayı Böyle Çalıştırıyorum. Kullandığım Skill'i Paylaşıyorum.
kanal: Avenox · süre: 56 dk · altyazı: tr manuel
ana iddia: En zeki/pahalı modeli (Fable) yalnız mimar olarak kullanıp araştırma ve kodu ucuz alt-ajanlara (Codex/Opus) dağıtmak, git takibi ve ölçüm kapılı "iskelet" sistemiyle birleşince vibe coding yerine denetimli ajan mühendisliği sağlar.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| avenox.lol/codex.md skill (Claude Code → Codex köprüsü) | YENİ | ELENDİ | Claude Code'a Codex alt-ajanı çalıştırma + Codex ile görsel üretim ekliyor; ücretli Codex üyeliği + login şart, ajana doğrulanmamış URL'den kendini entegre ettiriyor, repo yok |
| model kademesi (zeki model mimar, ucuz alt-ajan araştırma/kod; effort işe göre) | YENİ | BİLGİ | Fable yalnız mimari karar ve rapor sentezinde, Opus alt-ajanlar ayrı limitten okuyup özet döndürüyor; effort medium/high, max gereksiz; CLAUDE.md'de model/effort kuralı yok |
| ölçüm kapılı iyileştirme ("iskelet": skaler skor = başarı − ağırlıklı token maliyeti) | YENİ | BİLGİ | her commit'te deterministik benchmark; hipotez → değiştir → ölç → iyiyse commit, değilse geri al; spec/test dondurulmuş; pass/fail değil puan |
| iş takibi (alan bazlı commit + gerekçe notu + backlog) | YENİ | BİLGİ | ilgili değişiklikler birlikte commit (frontend ayrı, backend ayrı) ki ajanlar git geçmişinden izlesin; yarım kalan iş backlog'a yazılıp sonra %100'e tamamlanıyor |
| diğer: upstash/context7, codebase mimari haritası, alt-ajanla token tasarrufu, çok-ajanlı commit review (parçala + çapraz doğrulayan 3. ajan), paralel ajanı alan/worktree'ye ayırma, mimariden önce modele soru sordurma, custom guard / approval gate, ajanlarla güvenlik taraması, davranış bazlı test, eksiği "not implemented" diye beyan, git/GitHub kullanımı | ZATEN VAR | ELENDİ | context7 MCP kurulu; graphify; CLAUDE.md CONTEXT DİSİPLİNİ; /code-review + superpowers:dispatching-parallel-agents; using-git-worktrees; brainstorming; hooks yerleşik; /security-review; test-driven-development; CLAUDE.md "kanıtsız bitti yok"; repo zaten git |
| diğer: openai/codex (CLI, "Codex: /goal" dahil), Claude Cowork, beyin.md ikinci beyin (Obsidian benzeri) | ÇİFT | ELENDİ | Codex Claude Code ile aynı iş, /goal (bitene kadar sürdür) kısmen loop skill self-pace + CLAUDE.md "kanıtsız bitti yok"; Cowork videoda da Claude Code'un sadeleşmiş hali; beyin.md = auto-memory + graphify |
| diğer: Serai (kişisel hub), Gemini Embedding, caffeinate (macOS), Hermes?, "modeli uçlara çek" / görevi ilginç çerçeveleme istemi, Claude Code ile video kurgu hazırlığı | YENİ | ELENDİ | Serai kapalı, erişilemez; Gemini Embedding ürün içi RAG bileşeni, API anahtarı; caffeinate macOS'a özgü (ortam Windows); Hermes'in ne olduğu belirsiz; istem tekniği kanıtsız; kurgu akışında araç adı yok |
## ölçütler (YENİ)
- avenox.lol/codex.md skill + diğer YENİ: bakım=hepsi bilinmiyor (repo belirtilmedi; codex skill tek md dosyası) · çift=codex skill kısmen Claude Code alt-ajanları (aynı delegasyon, farklı model), görsel üretimde örtüşme yok; diğerleri örtüşme yok · izin=codex skill: ücretli Codex üyeliği + Codex kurulu ve login + ajanın harici URL'den skill'i indirip sistemine entegre etmesi (içerik doğrulanmadı); Serai erişim yok; Gemini Embedding Google API anahtarı + ücretli kullanım; caffeinate yalnız macOS · context=codex skill her oturum skill açıklaması + Codex çağrılınca; diğerleri kurulmadı, sıfır · kurulum: —
- teknikler (model kademesi, ölçüm kapısı, iş takibi): bakım=yok (teknik) · çift=model kademesi örtüşme yok (subagent model alanı yalnız araç, kural yok); ölçüm kapısı kısmen skill-creator benchmark (pass_rate/süre/token delta ölçer, tek skor ve kabul kapısı yok); iş takibi örtüşme yok · izin=yok · context=CLAUDE.md'ye birer satır, her oturum · kurulum: —
## hedefler (BİLGİ)
- zeki model yalnız plan/mimari karar ve rapor sentezinde, keşif/araştırma/mekanik kod ucuz model alt-ajanda; effort işe göre, max varsayılan değil → CLAUDE.md (CONTEXT DİSİPLİNİ: delege edilen işte model/effort seçimi)
- skill/context değişikliğini tek skaler skorla kabul et (başarı − ağırlıklı token maliyeti; skill-creator benchmark delta'sı iyileşmiyorsa geri al) → CLAUDE.md (Hedef-güdümlü: ölçüm kapısı)
- commit'leri alan bazında grupla ve gerekçeyi yaz; yarım kalan işi backlog'a kaydedip sonra kapat → CLAUDE.md (git / iş takibi)
---
## ek: somut
- ayar: Claude Code modeli Fable, effort medium (önemsiz görev) / high (mimari karar); Opus low thinking modunda bile Hermes'i kapatmanın diğer ajanları kıracağını sorup uyardı
- ayar: alt-ajanlar Opus seçiliyor çünkü Fable'ın ayrı limitinden yemiyor; Codex alt-ajanları GPT modellerinin talimat takibi için tercih ediliyor
- ayar: avenox.lol/codex.md kurulumu ajana istemle: "bu adresi aç, buradaki skill'i oku, benim kendi sistemimi entegre et"; önkoşul Codex üyeliği + bilgisayarda Codex kurulu + üye girişi + Claude Code
- ayar: uzun koşuda uyku engelleme Claude Code'da yapılmalı; Codex kendi sandbox'ında çalıştığı için caffeinate orada özel olarak söylenmezse çalışmaz
- ayar: paralel ajanlar farklı alanlara (database / frontend / backend) ve ayrı worktree'lere; commit'ler tek parça değil alan bazında (frontend ayrı, backend ayrı)
- ayar: Serai'ye tanıtılmamış codebase'de her işlem için onay isteniyor (izin codebase bazında tanımlanıyor)
- ayar: Codex'ten saldırı testi nedeniyle uyarı alındı, kimlik onayı yapılınca çözüldü; Claude serisiyle kendi altyapısına saldırı testi şimdilik yapılamıyor (iddia)
- ayar: benchmark skorunda enjekte token maliyeti ağırlığı bilerek 1.0 (0.1 seçilirse skor artıya döner); spec/test frozen, ajan ucuz istemlerle kendini onaylayamıyor; her gece replay, haftada bir gerçek ajanlarla uçtan uca test
- ayar: Claude Cowork promosyonu: kullanım normal limitin yarısı kadar sayılıyor, ayın 5'ine kadar
- ayar: Gemini Embedding metin, görsel, video ve sesi aynı şekilde vektörlüyor (ayrı ayrı vektörleme gerekmiyor)
- komut: Codex: /goal (görev tamamen bitene kadar bitirmeyi engelliyor) + "son 72 saatteki commitleri detaylı incele"
- komut: caffeinate (Claude Code'a doğal dille: "önümüzdeki 12 saat boyunca bilgisayarımın kapanmasını istemiyorum, 12 saat caffeinate yap")
- komut: istem "bana birkaç soru sor ki aynı yerde olduğumuzu anlayabilelim"; istem "alttan bir agent yolla, Opus gitsin, veriyi raporlarıma lokale çeksin"
- dosya: avenox.lol/codex.md; beyin.md; codebase mimari dosyası (adı gösterilmedi); hub ledger (sabah okunan kayıt, ASR "leger"); hub backlog bölümü
- sayı: alt-ajan 132.000 token harcadı, ana modele ~1.500 token döndü (~150.000 token avantaj) — gösterildi (132 bin ekranda; 1.500 tahmin)
- sayı: 100 commit 10 parçaya bölünüp 10 Codex ajanıyla paralel review; 1 haftalık review 1 günde — yalnız iddia
- sayı: arka planda aynı anda 6-8 ajan; araştırma ajanları (2 geldi, 4 daha bekleniyor), "10 ana parça" örneği — gösterildi (ekranda ajanlar; 10 parça örnek)
- sayı: Claude 5 saatlik + haftalık limit; Fable ek limiti haftalık limitin yarısı — gösterildi (limit ekranı)
- sayı: Fable erişimi 1 hafta — yalnız iddia
- sayı: Fable haftalık limiti video başında %25, sonra %34 — gösterildi
- sayı: codebase 400-450 bin satır; 500 bin satırlık vibe coding codebase'inin temiz olma ihtimali sıfır — yalnız iddia
- sayı: son 3 günde 74 + 67 + 43 ≈ 180 commit — gösterildi (GitHub)
- sayı: Fable review'u: 6,5 haftada 1.856 commit, 457 (başka yerde 450) test dosyası, 9.700 satırlık god object + 2 god file, 4 Opus ajanı bağımsız aynı sonuç, not 10 üzerinden 8,5-9 (A) — gösterildi (model çıktısı, bağımsız doğrulama yok)
- sayı: otomatik loop 60 kabul edilmiş commit üretti, 18 ajan ayrı worktree'de; 148 knob'un 30'u frozen (ASR belirsiz) — yalnız iddia (model raporu)
- sayı: hub benchmark skoru -11 (net negatif); token olmadan %90 → token ile %99 başarı örneği — yalnız iddia (örnek)
- sayı: uygulama %60-70 hazır; %70'te 1 aylık verim 2 haftada, %80'de 2 haftalık verim 1 haftada; 20 özellik 5-6 ana özelliğe indirilecek — yalnız iddia (plan)
- sayı: backlog'daki iş %80-90'dan %100'e tamamlanıyor — yalnız iddia
- sayı: GPT 5.6 bir hafta sonra geliyor (god file refactor'ü ona bırakılıyor) — yalnız iddia
- sayı: ham kayıt ~80-90 dk, kurgu 5-6 saat, izleyici odak süresi 30 sn, 40 dk videoda ortalama izlenme "67 dk" (muhtemelen 6-7 dk, ASR) — yalnız iddia
- sayı: influencer'ların %90-95'i dışarıdan içerik çevirip kurs satıyor — yalnız iddia
- sayı: şakalar: skill için 25 $; Fable'ın kurs önerisi 4 saatlik kurs 200 $ (99 $ değil), Skool? topluluğu aylık 49 $ — yalnız iddia (şaka)
- sayı: 18 sn'dir cevap bekleyen karar; 30 dosyada değişiklik / 6 alan — gösterildi (18 sn ekranda; 30/6 örnek)
