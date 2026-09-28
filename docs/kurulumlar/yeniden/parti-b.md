# Parti B — ilk 15'in 5-7'si (2026-09-28)

Hat: SERTİFİKA-1 (tarama → toplu → on → araştırıcı → bizde → katman → teknik → brief). Karar kaynağı: docs/kurulumlar/kayit.jsonl satır 99+ (ad başına son satır). Toplu: docs/video-tarama/2026-09-28-toplu-parti-b.md · rapor: docs/kurulumlar/2026-09-28-uygula.md Koşu 3-5 · brief: docs/kurulumlar/yeniden/parti-b-brief.md. Etiket: `yeniden:parti-b`.

## 2n84xa99FRY (Avenox · Serai hub + codex.md skill)
- karar dağılımı: ÖĞREN 10 · KUR 3 · RED 1 · ZATEN VAR 1 · departman surec-ajan-arac / verimlilik / surec-git-yayin / surec-inceleme
- Site/UI: yok (frontend içerik değil)
- prompt kalıbı: 0
- ÜRETİLEBİLİR: 0
- ayrıştırma: 0 (codex-exec-genel token hipotezli ama araştırma yarım → ÖĞREN, DENE yok)
- araştırıcı: codex-skill 91.5k token · 10 çağrı · web 1 · **yarım** (SkillSpector için yerel klon yapılmadı). Bulgu: avenox.lol/codex.md kaynağına (avenoxai/avenoxskills, MIT) göre bayat (kaldırılmış model + bayrak). Serai özel repo (gh 404) → araştırılmadı.
- tarayıcı: 81.8k token · 22 çağrı · kare 10

## XemheY_aM1g (Burhan KOCABIYIK · MiniMax M3 → Claude Code)
- karar dağılımı: KUR 5 · ÖĞREN 3 · RED 1 · departman surec-ajan-arac / diger / belge / frontend / verimlilik
- Site/UI: yok (görselden arayüz testi var, teknik gösterilmedi)
- prompt kalıbı: 0
- ÜRETİLEBİLİR: 0
- ayrıştırma: 0 (claude-mm token özelliği RED(lisans: yok · güvenlik: --bare OAuth atlama + veri 3. tarafa); takas ölçümü yok, claude -p 0)
- araştırıcı: claude-mm 58.5k token · 10 çağrı · tam (MG-Cafe/claudecode-minimax-stack, lisanssız)
- tarayıcı: 79.4k token · 13 çağrı · kare 6

## 4cE9t4rE0-0 (Yıldız Dikme · ChatLLM ile scroll-scrub yat sitesi)
- karar dağılımı: ÖĞREN 11 · KUR 2 · UYARLA 1 · departman frontend / surec-ajan-arac / arastirma-ogrenme / diger / surec-git-yayin / verimlilik
- Site/UI: UYARLA 1 özellik (4ce9-yat-sitesi-promptu/scroll-scrub-hero-video) + teknik UYARLA 5 (bekleyen/teknik-*) · ÖĞREN 0
- prompt kalıbı: 1 (4ce9-yat-sitesi-promptu → frontend-promptlar.md; ZATEN VAR 1). Anatomi alanları doğrulanamadı: 7:22 karesi site promptunu değil Kling video promptunu gösteriyor; altyazıda prompt metni yok.
- ÜRETİLEBİLİR: 0
- ayrıştırma: 0
- araştırıcı: 4ce9-yat-sitesi-promptu 36.4k token · 8 çağrı · tam. ChatLLM ELE listesinde (sözlük 0.94) → araştırılmadı; platforma bağlı 5 aday ÖĞREN kartı.
- tarayıcı: 94.7k token · 20 çağrı · kare 8

## Ölçüm (K3)
- araştırıcı: 3 · toplam 186.3k token · 28 çağrı · yarım 1/3 (Parti A 2/4). Hedef yarım 0 tutmadı: codex-skill SkillSpector klonunu tur disiplini için atladı.
- Jev: paket 98 · toplu 68 · bizde 6 · katman 128+1+6 = 307 (tavan 450) · claude -p 0 · web ≤3/aday (codex-skill 1).

## Düzeltme / kusur (sonraki dalga, kod değişmedi)
- `kanit()` (tools/video/video/uygula.py:192): gerekçenin yalnız ilk önekini okur ve lisansı özellik alanıyla tam alt dize arar → claude-mm'nin `güvenlik:`+`lisans:` kanıtlı RED'i Koşu 3-4'te DENE oldu. Veri biçimiyle düzeltildi (özellik `lisans: yok`, kanıt sırası lisans önce); Koşu 5 RED. Kırmızı test: çok önekli gerekçe + `yok (açıklama)` lisansı.
- `video toplu` çıktısı sabit `<bugün>-toplu.md` → Parti A dosyasını ezer; parti-b'ye taşındı, Parti A git'ten geri alındı.
- `red:` alanlı T0 adayları (serai-hub, caffeinate, ChatLLM'e bağlılar, indirim kodu) katmanda ÖĞREN oldu (24a K4: araç değil → ÖĞREN); RED gerekçesi aday.md'de duruyor.
- 4ce9-yat-sitesi-promptu departmanı Jev 0.49 surec-ajan-arac → elle.json ile frontend.

## YÜKLENECEK ZIP
- yok (skills/ değişmedi)
