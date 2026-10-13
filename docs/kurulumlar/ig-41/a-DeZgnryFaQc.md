# DeZgnryFaQc · insiderforce · reel · https://www.instagram.com/reel/DeZgnryFaQc/
## Özet
"5 ücretsiz Claude Code eklentisi" listesi: OmniRoute, Claude Mem, Headroom, Claude Code Setup, Claude Security.
Sonda "HUMAN" yorumuyla e-kitap çağrısı (insiderforce.io; reklam, kalem değil).
## Kalemler
| ad | tür | link | karar | ölçütler (bakım · çift · izin · context) | gerekçe |
|---|---|---|---|---|---|
| OmniRoute | CLI/ağ geçidi | https://github.com/diegosouzapw/OmniRoute | RED | ★75812 push:2026-10-11 arşiv:h · kurulu:omniroute · ağ, hesap token'ı · - | gönderide: limit dolunca ücretsiz sağlayıcılara otomatik geçen tek uç / bizde: npm omniroute kurulu, kol/omniroute1 ile bağlandı → fark yok |
| claude-mem | plugin | https://github.com/thedotmack/claude-mem | RED | ★100158 push:2026-10-13 arşiv:h · kurulu:thedotmack/claude-mem · dosya yazma, shell · SessionStart enjeksiyonu (gözlem sayısıyla ayarlı) | gönderide: oturum kapanınca bağlamı saklayıp sonraki oturumda geri yükleme / bizde: plugin kurulu, CLAUDE_MEM_CONTEXT_OBSERVATIONS ile sınırlı enjeksiyon → fark yok |
| headroom | plugin + MCP | https://github.com/headroomlabs-ai/headroom | RED | ★75154 push:2026-10-13 arşiv:h · kurulu:headroom (MCP + plugin) · ağ (vekil), shell · küçük (retrieve aracı) | gönderide: log/araç çıktısını modele gitmeden sıkıştırma / bizde: headroom vekil + MCP + plugin kurulu, headroom_retrieve kullanılıyor → fark yok (gönderideki %95 iddiası repo açıklamasındaki ~%20 ile uyuşmuyor) |
| claude-code-setup | plugin (resmi) | https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup | KUR | ★37764 push:2026-10-12 arşiv:h · önceki-karar:karar.tsv:KUR / karar-a.tsv:KUR (envanterde yok) · dosya okuma · çağrılınca | Apache-2.0 resmi Anthropic; kod tabanını tarayıp gereken hook/skill/MCP/alt ajanı öneriyor; pazar ekli, henüz kurulmamış |
| Claude Security | plugin (resmi) | https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-security | KUR | ★37764 push:2026-10-12 arşiv:h · önceki-karar:karar-b.tsv:KUR (kısmen: security-review, security-guidance) · dosya okuma, yama önerisi (onayla) · 1 skill + 9 ajan + hooks | Resmi Anthropic (eklenti lisansı Anthropic koşulları, karar-b ile tutarlı); ajan ekibi mimariyi haritalayıp bulguyu doğrulayarak yama öneriyor |
