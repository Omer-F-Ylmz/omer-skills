# AJAN-TAM-YETKI-1 — kısmi (envanter + skill + profil + Skill aracı bitti; canlı doğrulama kaldı)
- Fark: skill 2890 satır (docs/envanter/yetenek-fark.tsv, tools/yetenek_fark.py); CC'de YOK 2141 (çoğu dist-geçmiş sürüm/claude.ai-özel adlar).
- Aktarılan (CC ~/.claude/skills, hiçbiri ezilmedi): video-tarama, video-izle, video-uygula, headroom-compress, pixeljury, remotion-video-paket, hyperframes-paket (bu oturumun skill listesinde göründü).
- Atlandı: threejs-awesome-graphics (lisanssız), domain-modeling, grill-with-dogs (kaynak yok).
- Kök neden "skill kapalı": skillOverrides değil — yönetici `--disable-slash-commands` ile açıyor (departman-* hiçbir override'da yok). Düzeltme: `python onay/slash_ac.py uygula` → .kos/kopru/ajan-sira.slash yazıldı (tam küme; geri: --geri). settings.json'a dokunulmadı. 'off' olan anthropic-skills:headroom-compress/pixeljury claude.ai kopyaları; yeni yerel kopyalar etkilenmiyor.
- MCP profili: tools/mcp_profil.py TEMEL = ruflo, rea, playwright, headroom, context7, brave-search, stalemap (rea 15, playwright 12 araçla KEEP'li; kalanı kapı `ara/cagir` arkasında). Test: tools/test_mcp_profil_temel.py + stalemap testi (eski "dotnet'te stalemap yok" iddiası bilerek tersine çevrildi) — 5/5 yeşil.
- YAPILMADI (45 tur sınırı): adım 5 Desktop bağlayıcıları (figma/canva OAuth zaten doğrudan; github MCP http var; gh+vercel CLI PATH'te, supabase CLI yok), adım 6 zorunlu_arac süzgeci, adım 7 3 canlı ajan oturumu + RAM tepe, claude-mem (eklenti MCP'si KAYNAK dışı).
- ERİŞİM YOK: claude-mem, code-mode-MCP (cm.py Bash üzerinden var), supabase CLI, miro. 
- ÖMER: canva ve claude-design OAuth girişi gerekli (claude-design 403: /design-login). Yönetici runner'ı slash bayrağı için yenilenmeli.
