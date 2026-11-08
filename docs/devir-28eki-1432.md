# Devir — 28 Eki 2026 14:32 (TR)

## Kurallar (değişmedi)
- CC'yi Ömer gibi kullan: iş başına tek oturum, blok blok (--resume), gereksiz yeni oturum yok.
- Uzun işler: .kos/kopru/arka/<ad>.json yaz (mcp-filesystem write_file) → `python C:/Projeler/omer-skills/tools/arka_ajan.py baslat <ad>` (cc-kopru komut). Kısa (<60 sn) işler köprüden. vercel deploy/link ve git remote köprüde yasak → CC ajanına ver.
- arka_ajan.py ARKA-FIX-1 (ab99d29b): sonuç sonrası süreç ağacını kapatır, bayat kilidi .kilit-eski yapar. TOKEN-ACILIS-1 (3baa186d): json'da "eklenti": [], "mcp": [], "hafif": true|false → açılış 350–440k → ~38k (hafif) / ~68k (skill açık). Kalite A/B henüz ölçülmedi (varsayılan kol dönmedi) — ilk fırsatta jev ile ölç.
- Durum okuma: .log satır sayısı (cc-kopru oku aralik bas=1 bit=1); 5 satır = bitti, sonuç JSON'unda "TUR BITTI" → aynı adla yeniden baslat; "<İŞ> BITTI" → başlatma, özetle.
- Kontrol 20–25 dk'da bir; aynı anda en fazla 4–5 iş; RAM ≤%89.

## Çalışan işler (14:30 itibarıyla)
1. ilik-v2 (13:40, Opus medium) — İLİK yeniden yapım: performans (kasma), gerçekçi çiçekler (Sketchfab + PBR), awwwards tasarım, kapanış; push → Vercel otomatik. Canlı: https://ilik-yaka-cicegi.vercel.app (repo Omer-F-Ylmz/ilik-yaka-cicegi, Vercel projesi ilik-yaka-cicegi, team omer-a4de). Bitince linki doğrula, Ömer'e at.
2. derin-hiz (13:44) — derin video hattını hızlandırma + GPU TDR teşhisi; 897 linklik toplu koşuyu BAŞLATMAZ, planı getirir.
3. karar-14b TUR 2 (14:20) — kalan ogren-3-d1 + ters-2-d8 (suit-kirmizi-2 ve yarim-g7 bitti).
4. video-kaynak (14:20, orta profil) — 178 video + 275 kaynak.
5. ret-kur-1b (14:30) — 8 servis kurulumu: Meta Ads MCP, Oxylabs (OXYLABS_API_KEY, kullanıcı adı yok), Apify, fal.ai, Modal (ID+SECRET), Higgsfield+Kling, Composio, Telegram bot. Anahtarlar HKCU\Environment'ta. Bitince Desktop yeniden başlatma gerekebilir. Meta token 27 Ara 2026'da biter — Ömer'e 20 Ara civarı hatırlat (Graph API Explorer → Generate → Extend).

## Sıradakiler
- video-764-1.json hazır (para işi 1/4, tavan $3, orta profil). Boş yer açılınca başlat; sonra token-2-d3 → graphify-ultra-1-d2 → token-8-f2d (sabit tur sınırı yok, az oturum, json'ları hafif/orta profille yaz). Biri bitmeden sonraki başlamaz. Ömer onayladı.
- 20:55 TR: HF ZeroGPU kotası sıfırlanınca yaka-3d-4t.json başlat (ilik-v2 çalışıyorsa çakışmasın).

## Bitenler (bugün)
- ARKA-FIX + TOKEN-ACILIS (yukarıda). strix: kritik 0, yüksek 0, orta 2 (rapor/strix-2.md). yarim-onay: kurulum/indirmeler zaten yapılmış. guvenlik-yama: PHP/Node/Java yamalı; Ömer'de: eski kullanıcı Node 24.19 kopyası — bir sonraki yeniden başlatmada Desktop açılmadan `winget upgrade OpenJS.NodeJS.LTS --scope user`. kalan-6: ram-opt-1-d3 bitti (Desktop yeniden başlatınca etkin, doğrulanmadı); omni-ayir/slash-ogren/video-13/gorev-usta-blender-1 ENGEL. hic-122: 109/123 (kalanlar ENGEL/N-A/ERTELİ). yarim-216: 178/216 (kalanlar yarim-onay'a taşındı, yeniden başlatma).

## Ömer'de bekleyen sorular
- skill-paket-2: claude.ai 932 kayıt — hedef 1000'e mi çıksın, 82 kopya mı silinsin (öneri: kopyalar silinsin, Ömer siler, liste Claude'dan).

## Vercel siteleri
İLİK https://ilik-yaka-cicegi.vercel.app · TELVE https://telve-xi.vercel.app · TELVE mini https://telve-mini.vercel.app · NEFFEX https://neffex-omer.vercel.app · OKTAN https://oktan-deneme.vercel.app · Mıhlama https://mihlama.vercel.app

## Not
Eski sohbette 14:43'e kurulu "Arka ajan kontrolü 19" görevi var; yeni sohbet kendi kontrolünü kursun (iki kontrol aynı işi yapabilir, zararı yok).
