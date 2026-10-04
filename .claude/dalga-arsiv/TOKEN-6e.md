# TOKEN-6e — Enjeksiyon daraltma
Tur ≤35 (5'te bir sayaç, 30'da commit+push+DUR) · claude -p ≤24 (sayaç aşağıda) · her madde commit, push sonda · okuma işi okuyucu (sonnet) · Workflow/doğrulayıcı yok.

## KARAR
- Kurulu skill/plugin/MCP silinmez, kapatılmaz, dosyası düzenlenmez. Daraltma yalnız aracın kendi ayarı/env'i ya da CC ayarıyla; yoksa "dokunulmaz". Global ayar DEĞİŞMEZ: kollar `claude -p --settings <geçici>` (plugin kapatma yalnız K2 ölçüm kolu, kaldıraç sayılmaz).
- Kendi dosyalarımız (global CLAUDE.md, RTK.md, graphify bölümü): kapatılmaz, token metin uzunluğundan "tahmin"; A/B'ye girmez, raporda "ayrı aday".
- K1 Mühür (ayrı satırlar): headroom_yama --durum · Headroom /health pid · runtime_env sha8 · settings özeti (opus effort high, awaySummaryEnabled true) · skill/plugin/MCP sayıları. Sonda aynı, eşit olmalı.
- K2 Envanter: SessionStart vb. her enjeksiyon → kaynak · gerçek input_tokens farkı (boş görev, taban vs kaynak kapalı, kaynak başına ≤1 kol; /context kullanılmaz) · her oturum/koşullu · kendi kaldıracı (ayar + kanıt satırı) ya da "kaldıraç yok".
- K3 A/B: yalnız kaldıraçlılar. 6d düzeneği (rtk-ab kısa + kur.py orta; ≤3 görev), n≥2. Kollar: taban · hepsi birden (önce) · kaynak başına. Ölçü: ağırlıklı token + $ · kör puan + başarı · KEŞİF KAPISI araç çağrısı + alt ajan ≤ taban +%10.
- K4: 24 Eyl kalite takası tablosuyla AL/SOR/RED (kapıyı aşan RED). docs/token-6e.md: envanter · A/B · kararlar · uygulanacak ayar satırları (UYGULANMAZ).

## Kabul
Kod değiştiyse kırmızı-önce · eski test değişmez · kod varsa ilgili suite (pipefail); yalnız doküman → suite yok (sapma değil) · mühür eşit · gitleaks · commit yalnız dalga dosyaları (parti/, adaylar/, video-tarama/, .kos/ hariç) · arşiv .claude/dalga-arsiv/TOKEN-6e.md · push · graphify update . ön planda.

## Durum
- tur 1/35: onay + 3 ek. claude -p 0/24.
- Mühür bas (scratchpad 722d16ff…/muhur-6e-bas.json, betik muhur6e.py): headroom_yama 2 dosya yamalı · /health config.pid 28372 · runtime_env sha8 c0e45d55 · settings özet awaySummary true, opus-5/5-5 high, fable medium, max max · settings f132b748 · mcpServers 23452893 · hooks a0801fdf · plugin 47/53 · mcp 19 · skill 1054.
- tur 20/35 (5,10,15'te sayaç yazılmadı — sapma; tur = araç turu sayılıyor). K2a envanter bitti: enjektörler claude-mem (SessionStart, kaldıraç ~/.claude-mem/settings.json = global dosya, -p env worker'a ulaşmaz → bu dalgada kol yok), superpowers (kaldıraç yok), ponytail (env PONYTAIL_DEFAULT_MODE, off=kural basmaz; config.js:3-10, activate.js:28-35), security-guidance (env SECURITY_GUIDANCE_DISABLE; hook.py:40-41,164-171), ECC (bağlam basmıyor, 6a +17), hookify/headroom/guard ~0, jev-skill koşullu, kendi dosyalar tahmin. 6a ölçümü docs/token-6a.md:76-96. 24 Eyl tablo omer-kurallar.md:23.
- Koşucu scratchpad 722d16ff…/k6e.py (kol = --settings ayar-<kol>.json; sayaç k6e-sayac.txt tavan 24; orta base 33b2bd5, rtk-ab base d0af0b5). K2 arka planda (5 çağrı). K3 planı: taban → hepsi (pt off + sg disable) → pt → sg; her kol kısa×2 + orta×2 = 16 → toplam 21/24.
- tur 25/35: K2 bitti (claude -p 5/24; ham scratchpad k6e-k2-*.jsonl). İlk ctx: taban 72,367 · cmem0 69,254 · sp0 72,681 · pt0 72,296 · sg0 74,821. Gürültü: claude-mem SessionStart çıktısı 21,198 (taban) ↔ 31,956 kr (diğerleri). Hook çıktısı kr (SessionStart): cmem 21.2–32.0k(+160) · ponytail 10,720(+252) · superpowers 7,528 · security-guidance 2×284 · diğerleri ≤571. Fit 0.162 tok/kr (Δctx~Δkr, 4 kol en küçük kareler) → cmem ~3.4–5.2k · pt ~1.8k · sp ~1.2k · sg ~0.1k (ölçülen Δ pozitif) · UserPromptSubmit çıktıları ≤40 kr. Kendi dosyalar (tahmin, bayt/3.5): global CLAUDE.md 3089B ~0.9k · RTK 460B ~0.13k · proje CLAUDE.md 1203B ~0.34k · MEMORY 2510B ~0.7k.
- K3 kapsamı: sg kolu yok (enjeksiyon ~0.1k < gürültü, güvenlik aracı → RED gerekçesi); cmem kaldıracı global dosya → bu dalgada kol yok (ayrı aday); sp kaldıraç yok. Hepsi birden = pt off. K3 arka planda: taban↔pt iç içe, kısa×3 + orta×3 (12 çağrı → 17/24).
- tur 30/35 — DUR (30. tur kuralı). claude -p 17/24. K3 bitti (olcum/token-6e-k3.json): başarı 6/6 · 6/6. pt−taban: rtk $ −7.7 · ağırlıklı −7.4 · çıktı +9.1 · araç −7.1 · ilk ctx −1.8 (−1.7k) % ; orta $ −1.1 · ağırlıklı −0.4 · çıktı +14.1 · araç +11.5 (8.7→9.7, taban aralığı 7–10) · ilk −2.5 (−1.8k) % ; toplam $ −4.8 · ağırlıklı −4.4 · araç 0.0 %. Alt ajan 0 her kolda.
KALAN (sonraki oturum, hepsi scratchpad 722d16ff…/):
1. Kör puan: okuyucu, kor/ (rtk-A..F.diff, orta-A..F.diff, gorev-rtk.txt, gorev-orta.md), 0–3 × doğruluk·eksiksizlik·kalite; eşleme gizli/eslesme.json puanlamadan SONRA açılır → olcum/token-6e-kor.json commit.
2. Karar (omer-kurallar madde 21 + kapı): pt tasarruf ~%4–5 (<%25) → kalite düşüşü bant içindeyse "her tasarruf AL", değilse RED. Kapı: kol toplamı araç +0% (geçer), orta görevde +%11.5 (n=3, taban içi aralık ±%35) — raporda ayrıca yaz. sg RED (enjeksiyon ~0.1k, güvenlik aracı); cmem kaldıracı global dosya → ayrı aday (SOR); sp/ECC dokunulmaz; kendi dosyalar ayrı aday.
3. docs/token-6e.md (envanter · A/B · kararlar · ayar satırları, UYGULANMAZ; AL ise satır: settings.json env PONYTAIL_DEFAULT_MODE=off ya da %APPDATA%\ponytail\config.json defaultMode) commit.
4. Kapanış: muhur6e.py muhur-6e-bas.json ile (EŞİT) · gitleaks · arşiv → .claude/dalga-arsiv/TOKEN-6e.md · push · graphify update . ön planda. Kod değişmedi → suite yok.
- tur 5/15 (yeni oturum; 5. turda yazılmadı, 9'da yazıldı — sapma): kör puan + cmem araştırma okuyucuda; takas = kur.py:348 (d=0 → s≥%25 AL yoksa RED(token)); pt s=%4.8 → RED(token).
- tur 10/15: kör puan bitti (olcum/token-6e-kor.json); cmem: env yolu worker sürecinde, -p/--settings env workera ulaşmaz → oturum başına geçersiz kılma yok.
- tur 13/15 KAPANIŞ: kör puan taban 8.67 · pt 8.83 (başarı 6/6·6/6) · kapı geçer (araç ±0, orta +%11.5 taban aralığı içinde) · pt RED(token) s=%4.8<%25 · cmem oturum başına geçersiz kılma yok → 6e-2 · mühür EŞİT · gitleaks temiz · suite yok (yalnız doküman/ölçüm). docs/token-6e.md.
