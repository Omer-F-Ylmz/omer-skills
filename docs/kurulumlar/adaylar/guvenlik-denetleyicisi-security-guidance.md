# Güvenlik denetleyicisi (security-guidance)
ad: Güvenlik denetleyicisi (security-guidance)
tur: plugin
video: I0ADpAN2qT0
repo: anthropics/claude-code
lisans: bilinmiyor
son_commit: 2026-05-26
arsiv: bilinmiyor
kaynak: https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance
telemetri: Plugin kendi başına ağ çağrısı yapmaz (hatırlanan bilgi, kod okunmadı); yerel Python betiği çalışır. Claude Code'un kendi veri toplaması (README: kullanım verisi, geri bildirim) ayrıca geçerli.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı: SkillSpector raporu yok
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Claude dosya yazarken/düzenlerken riskli kod kalıplarını (komut enjeksiyonu, eval, XSS, pickle vb.) yakalayıp Claude'a güvenlik hatırlatması veren Anthropic resmi plugin'i.
## Mekanizma
Hatırladığım kadarıyla: plugins/security-guidance altında hooks.json ile PreToolUse hook'u tanımlı (Edit/Write/MultiEdit). Hook bir Python betiği (security_reminder_hook.py) çalıştırır; yazılacak içerik/dosya yolunu önceden tanımlı desen listesiyle (ör. GitHub Actions workflow enjeksiyonu, child_process.exec, eval, new Function, dangerouslySetInnerHTML, innerHTML, document.write, pickle, os.system) eşler. Eşleşirse uyarıyı stderr'e yazıp engelleme koduyla çıkar; Claude uyarıyı görüp kodu güvenli biçimde yeniden yazar. Aynı dosya+kural uyarısı oturum başına bir kez verilir (durum dosyası). Yani LLM tabanlı tarama değil, statik regex/alt dizgi eşleşmesi. Bu dosyaları bu çalışmada okuyamadım (yalnız README ve ağaç vardı), bu yüzden ayrıntılar doğrulanmadı.
## Kanıt
- Claude'un yazdığı kodu aynı oturumda tarayıp güvenlik açıklarını bulan ve çözen eklenti → sınanamadı · Plugin dosyaları (hook betiği, hooks.json) elimdeki veride yoktu; yalnız ağaçta plugins/security-guidance klasörü görüldü. Hatırlanan bilgiye göre mekanizma desen tabanlı uyarıdır; 'çözme' işini Claude yapar, plugin yapmaz.
- Eklenti adı 'security-guidance' ve anthropics/claude-code deposunda → doğrulandı · Depo ağacında plugins/security-guidance dizini var.
- güvenlik ön taraması: koşmadı: SkillSpector raporu yok
## Kurulum
- Claude Code içinde: /plugin marketplace add anthropics/claude-code
- /plugin install security-guidance@claude-code-plugins (marketplace adı doğrulanmadı)
- Python 3 kurulu olmalı (hook betiği için)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Claude'un yazdığı kodda bilinen tehlikeli kalıplar yazılmadan önce yakalanır; ek kurulum ve model maliyeti olmadan oturum içinde anlık geri bildirim sağlar.
## Maliyet/risk
Videodaki "kodu tarayıp açıkları bulup çözer" ifadesi abartılı olabilir: statik desen hatırlatıcısıdır, gerçek açık analizi yapmaz; yanlış pozitif/negatif çıkar. Lisans açık kaynak değil gibi görünüyor, yeniden dağıtım/fork için doğrulanmalı. Python bağımlılığı. SkillSpector raporu yok, güvenlik ön taraması yapılmadı.
## Tasarruf
Token aracı değil; tersine her uyarı bağlama az miktarda metin ekler. Dolaylı kazanç: sonradan güvenlik düzeltme turlarını azaltabilir.
## Üretilebilir
hedef_tur: hook
tarif: PreToolUse hook (matcher: Edit/Write/MultiEdit) yaz. Betik stdin'den tool_input JSON'unu okur (file_path, content/new_string). Kendi kural listeni (eval, exec/os.system, innerHTML, dangerouslySetInnerHTML, pickle.loads, SQL string birleştirme, workflow'da ${{ github.event.* }} enjeksiyonu, sabit sır kalıpları) regex ile eşle. Eşleşirse mesajı stderr'e yazıp exit 2 ile çık; oturum ve dosya+kural anahtarlı küçük bir durum dosyasıyla aynı uyarıyı tekrarlama. Plugin olarak .claude-plugin/plugin.json + hooks/hooks.json ile paketle. Kaynak kodu kopyalama; lisansı belirsiz, kendi kurallarını yaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### Resmi Anthropic plugin'i olarak aynı depoda bulunur (plugins/security-guidance)
kaynak: https://github.com/anthropics/claude-code/tree/main/plugins
### PreToolUse hook ile Edit/Write sırasında riskli kalıp uyarısı (hatırlanan bilgi, doğrulanmadı)
kaynak: https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance
## Destek
- I0ADpAN2qT0 · 0:04 · Claude'un yazdığı kodu aynı oturumda tarayıp güvenlik açıklarını bulan ve çözen eklenti. · kanıt: Altyazıda 'adı güvenlik' görünürken ekranda 'security-guidance' başlıklı README. (karede: GitHub dosya listesi ve 'security-guidance' başlığı; altında 'Security reminder for Claude-generated code' benzeri metin.)
