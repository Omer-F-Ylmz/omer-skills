# TOKEN-REA — token + hafıza araçlarımızın daha iyi sürümleri (REA + tersine)

★ d1 İLK VE BAĞLAYICI (Desktop 20 Eki 16:40; Ömer onayı 16:36 "başlayabiliriz")
Kaynak: gorev/SIRA.md "SIRA SONU-2" satırı (tek kaynak, tekrar edilmez). Ortak kurallar: ogren-ortak.md ★'ları + model-politikasi.md (betik → ücretsiz bulut → Haiku → Sonnet → Opus; YEREL MODEL YOK) geçerli.

★ KAPSAM KURALI (Ömer 20 Eki 16:50, kalıcı): TOKEN-REA kapalı liste değildir. video-764 hattından (ve sonraki her kaynaktan) çıkıp KURULAN her yeni araç önce ÖĞREN kapısından geçer (güncel sürümle; ≥%92, hedef %98), sonra token/hafıza etkisi varsa TOKEN-REA envanterine eklenir ve aynı 4 eksen taban + kendi sürüm akışına girer. envanter.tsv'ye `kaynak` sütunu (kurulu · video-764 · diğer) ve `durum` (bekliyor · öğren · taban · iyileştirme · kapı) ekle; yeni gelen satır otomatik `bekliyor` olur.

## Kapsam (araç listesi)
Token: RTK · Headroom · graphify · context-mode · ROUTER/OmniRoute · CC ayarları (promptCacheTtl, tool search, statusline) · videolardan çıkan token araçları (ogren/ kartlarında "token" etiketli UYARLA/ÖĞREN).
Hafıza: claude-mem · BEYİN/Obsidian · NotebookLM (nblm.py) · mcp-memory · CLAUDE.md/dalga.md + SessionStart hook.

## d1 — hazırlık + taban (≤1 oturum, en fazla 40 tur)
0. REA SAĞLIK: REA'nın bu oturumda araç olarak çağrılabildiğini kanıtla (bir gerçek REA çağrısı, örn. Headroom'un bir modülü üzerinde). Çağrılamıyorsa nedeni + düzeltme (MCP config) — düzeltemezsen `tersine` skill'inin REA'sız yolu (DevTools/graphify/kaynak okuma) ile devam, raporda yaz. Native ikili (ör. RTK .exe) için Ghidra GEREKİRSE kurma; yalnız gerekçe + kurulum adımı raporla (Java 17 var). Önce açık kaynak kodu tercih et — kaynak varken ikili analizi yok.
1. ENVANTER: her araç için tek satır — sürüm · kaynak (repo/yerel yol) · dil · bizdeki kullanım noktası · ölçüm betiği var mı. `.kos/kopru/token-rea/envanter.tsv`.
2. TABAN ÖLÇÜMÜ (her araç tek tek, betikle, Claude token'ı minimum): 4 eksen — performans (süre/RAM) · kalite (mevcut kapı/test seti; yoksa ≥10 maddelik tohumlu set yaz, held-out ayrı) · kullanışlılık (adım sayısı, hata oranı) · token katkısı (gerçek API girdi token'ı, araç açık/kapalı A/B; /context Skills satırı KULLANILMAZ). Toplam taban: tipik 3 iş profilinde (kod dalgası · araştırma · köprü kontrolü) toplam girdi+çıktı token. `.kos/kopru/token-rea/taban.md`.
3. MEKANİZMA ÇIKARMA (REA + tersine): en büyük token katkılı 3 araçla başla; her biri için "ne yapıyor · nerede kaybediyor · neyi daha iyi yapabiliriz" ≤15 satır. Kod kopyalanmaz, mekanizma alınır.
4. PLAN: araç başına "kendi sürümümüz" tasarımı + beklenen kazanç + kapı (taban üstü 4 eksende de; %98 kuralı) — `.kos/kopru/token-rea/plan.md`. Toplam hedef: tabana göre ≥%50-60 ek tasarruf, kalite eşit/üstü.

## Kurallar
- Kurulu araç kaldırılmaz/budanmaz; kendi sürümümüz yanında kurulur, A/B ile kazanırsa varsayılan olur (Ömer onayıyla).
- Ücretli çağrı yok; Claude çağrıları plan kotasından, ölçüm çağrıları "en fazla 30".
- RAM ≤%88 (runner eşiği); ağır ölçümler sırayla. Pencere açma yok (CREATE_NO_WINDOW). rm yok, push yok, güvenlik ayarı onaysız değişmez.
- Alt ajan katmanı: kolay → Haiku/ücretsiz, zor → Sonnet high, çok zor → Opus 5.5 medium.
- Commit: tek konu tek commit, mesaj "token-rea d1: ...".
- RAPOR ≤15 satır (commit · ölçülen araç sayısı · taban toplamı · REA sağlık · ilk 3 aracın mekanizma özeti tek satır · d2 önerisi · Ömer'e gereken adım). d2 bölümünü bu dosyanın sonuna ★ d2 TASLAK olarak yaz (Desktop onaylar).

## ★ d2 TASLAK (d1 sonrası; Desktop onaylar)
Kanıt: `.kos/kopru/token-rea/` (envanter.tsv · taban.md/json/py · mekanizma.md · plan.md). d1 bulgusu: ağırlıklı taban 497.6M'nin %75'i cache okuma+yazma; araç-çıktısı sıkıştırma tek başına ≈%14-15 verir, "ek %50-60" için iş deseni de değişmeli (Ömer kararı gerekir).
1. d2a (ayar/enjeksiyon, kod az): bağlam-diyeti (hook enjeksiyonu 14.6k → ≤6k) + önbellek disiplini (ttl-sim) → count_tokens ve taban.py profil ile A/B; kapı: sabit bağlam ≤22k, görev testi eşit.
2. d2b: rtk2 sinyal-koruma sarmalayıcı (held-out 4 komut) + sor2 graphify hibrit (held-out 5 soru, isabet ≥9/10, ≤1.5k token, <0.5 sn); kapı %98.
3. d2c: bekleyen 6 aracın tabanı (context-mode, OmniRoute, jev, qmd, NotebookLM, mcp-memory) → envanter durum `taban`; sonra hr2 (CC tool search ile şema ertelemesi çakışması) ve çıktı-diyeti.
Tavan: ölçüm Claude çağrısı ≤30/oturum; kurulu araç silinmez; varsayılan geçişi Ömer onayıyla.
