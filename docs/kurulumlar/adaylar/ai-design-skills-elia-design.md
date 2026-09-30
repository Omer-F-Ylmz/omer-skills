# AI design skills (Elia Design)
ad: AI design skills (Elia Design)
tur: skill
video: Ysr7oNDajJI
repo: elayadesign/ai-design-skills
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/elayadesign/ai-design-skills
telemetri: Yok. Yalnızca markdown dosyası, çalıştırılan kod ve ağ çağrısı yok. SKILL.md içeriğini ben okumadım.
yildiz: bilinmiyor
alt_tur: araç
skillspector: --no-llm taramasında 2 HIGH/CRITICAL bulgu. Ayrıntı görülmedi, elle inceleme gerekli.
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun)
## Ne
Claude Code, Cursor, Codex, Windsurf gibi AI kodlama araçları için tasarım skill'leri koleksiyonu. Şu an tek skill var: landing-page-design. Sıfırdan landing page kurar: giriş soruları, sayfa yapısı, dönüşüm odaklı metin ve tam görsel sistem (tipografi, boşluk, radius, hareket).
## Mekanizma
Her skill kendi klasöründe duran bir SKILL.md (markdown kural dosyası). Ajan bu dosyayı bağlamına alır ve talimatları izler. Kod ya da çalışan servis yoktur. Tasarım değerleri (font, renk, boşluk, hareket) dosyanın altındaki tek bir bölümde durur. Fork edip o bölümü değiştirince skill'in geri kalanı buna uyar. Video, skill'in sayfayı tek bir eyleme odakladığını söylüyor: "a landing page has one job". SEO'nun skill'de yer aldığı yalnızca videoya dayanıyor. SKILL.md'yi okuyamadım, README'de SEO geçmiyor.
## Kanıt
- Lisans MIT'tir, atıf gerekmez → doğrulandı · README 'License: MIT. Use it, fork it, ship it, sell what you build with it. No attribution needed.' diyor. LICENSE dosyası ağaçta var. İçeriğini okumadım.
- Skill tek dosyalık ve landing page'i tek eyleme odaklar (renk, tipografi, boşluk, SEO) → sınanamadı · Video alıntısı 'a landing page has one job'. Ağaçta skills/landing-page-design klasörü var. SKILL.md içeriğini okumadım. README tipografi, boşluk, radius ve hareketi doğruluyor, SEO'yu doğrulamıyor.
- Birden çok araçta çalışır (Claude Code, Cursor, Codex, Windsurf) → doğrulandı · README bu araçlar için kurulum yollarını veriyor. Fiilen çalıştırmadım. Yalnızca kurulum talimatlarının varlığını doğruladım.
- güvenlik ön taraması: SkillSpector --no-llm HIGH/CRITICAL 2
## Kurulum
- mkdir -p .claude/skills
- git clone https://github.com/elayadesign/ai-design-skills.git /tmp/ai-design-skills
- cp -r /tmp/ai-design-skills/skills/landing-page-design .claude/skills/
- Cursor için: SKILL.md dosyasını .cursor/rules/ altına curl ile indir. Codex için AGENTS.md, Windsurf için .windsurfrules, Cline için .clinerules kullan.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Landing page üretiminde tutarlı bir tasarım sistemi ve dönüşüm odaklı yapı verir. Ajanın jenerik çıktısını azaltır. Araçtan bağımsızdır, MIT lisanslıdır ve değerleri fork ile özelleştirilebilir.
## Maliyet/risk
Düşük. Kod içermeyen markdown. SkillSpector --no-llm taraması 2 HIGH/CRITICAL bulgu verdi, ayrıntıları görmedim. Talimat metnindeki prompt-injection benzeri kalıplar ya da yanlış pozitif olabilir, kurmadan önce SKILL.md elle incelenmeli. Kaynak çok yeni ve küçük görünüyor, yıldız ve commit bilgisi doğrulanamadı.
## Tasarruf
Token aracı değil. Belirgin bir tasarruf mekanizması yok. Tek dosyalık skill bağlama yer kaplar, ama tekrar eden tasarım kararlarını yeniden anlatma ihtiyacını azaltabilir.
## Üretilebilir
hedef_tur: skill
tarif: Kendi landing-page skill'imizi SKILL.md olarak yaz. Bölümler: (1) giriş soruları (hedef eylem, kitle, teklif), (2) sayfa iskeleti (hero, kanıt, fayda, SSS, CTA) ve tek eylem kuralı, (3) dönüşüm metni yönergeleri, (4) SEO kontrol listesi (başlık, meta, başlık hiyerarşisi), (5) en altta değiştirilebilir 'tasarım değerleri' bölümü (font, renk, boşluk ölçeği, radius, hareket). Doğrudan kopyalamak yerine MIT lisansıyla forklayıp Türkçe ve kendi marka değerlerimizle uyarlamak daha hızlı. Önce SKILL.md'yi okuyup SkillSpector'ın 2 bulgusunu incele.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun/panel.md → Ömer sütunu
## Özellikler
### Giriş soruları, sayfa yapısı ve dönüşüm metni ile sıfırdan landing page üretimi
kaynak: https://github.com/elayadesign/ai-design-skills
### Tam görsel sistem: tipografi, boşluk, radius, hareket
kaynak: https://github.com/elayadesign/ai-design-skills
### Tasarım değerleri tek bölümde, fork ile özelleştirilebilir
kaynak: https://github.com/elayadesign/ai-design-skills
### Çoklu araç desteği: Claude Code, Cursor, Codex, Windsurf, Cline, Claude.ai
kaynak: https://github.com/elayadesign/ai-design-skills
## Destek
- Ysr7oNDajJI · 5:24 · Tek dosyalık landing page skill'i; renk, tipografi, boşluk sistemi ve SEO'yu tek eyleme odaklar. · kanıt: a landing page has one job and that's getting people to actually take action
