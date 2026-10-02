# TOKEN-3a — skill listesi tetik ölçümü + profil tasarımı (AYAR DEĞİŞMEZ)

KARAR
- Plan kabul (velvet-churning-snail.md) + 2 düzeltme:
  1. .claude/agents/okuyucu.md (model: sonnet, salt-okuma); K1/K2 bu ajanla 2 paralel Agent çağrısı. Ajan dosyası ayar sayılmaz.
  2. K4 gerçek ortamda (Headroom açık). Pilot init'te Skill yoksa: bulgu → TOKEN-6 kritik; 1 teşhis pilotu BASE_URL'siz; kalan 28 BASE_URL'siz, "gerçek ortam değil".
- Skill/plugin/MCP/çalışma silinmez; hiçbir ayar dosyası değişmez.

KABUL
- Testler ≥8 yeşil; kırmızı-önce commit; mutasyon (alternatif eşleşme) kırmızı.
- claude -p toplam ≤35 (K4 ≤30 + pilot).
- Mühür eşit: settings.json · mcpServers · hooks · proje .claude/settings*.json; sayılar eşit; diff-filter=D boş.
- gitleaks temiz; suite 3 yeşil (pipefail).
- docs/token-3a.md; dalga → .claude/dalga-arsiv/TOKEN-3a.md; commit + push.

DURUM
- Tur 10: mühür tabanı scratchpad (bas 2695783 öncesi HEAD 2695783→K0 6f37311). K0 commit ✓ (gitleaks 0).
- okuyucu Agent'ta "not found" ×2 → K1/K2 `claude -p --agent okuyucu --model sonnet` (BASE_URL'siz, arka plan). SAPMA.
- K3 veri: 14 gün Skill çağrısı az (omer-skills 13 tür, mod-atolyesi ×14, sdp/surec, TELVE web-sahne/frontend-craft).
- Tur 15: K3 kırmızı 82a243c · yeşil 10/10 · mutasyon ([:1] kabul) → 1 kırmızı ✓. tetik-seti.json 30 (26+4 neg).
- K1/K2 ilk başlatma argüman hatası (API yok) → yeniden başlatıldı.
- Pilot bl1 Headroom AÇIK: Skill aracı var, isabet (blender-oturum+uretim), ilk ctx 99.1k, $0.89 → 30'u gerçek ortam.
- claude -p sayacı: 3 (K1, K2, bl1) + K4 kalan 29 arka planda → 32
- Tur 25: K1 ✓ ($0.32, sebep: referans rehberleri okunmadı → ışık −2). K2 ✓ ($0.68): skillOverrides on/name-only/user-invocable-only/off; plugin skill'leri etkilenmez → enabledPlugins. K4 sürüyor. docs/token-3a.md §1 yazıldı.
- Tur 20: liste 140.3k kr (init: 393 skill · 490 komut · 51 plugin). Aile payı scratchpad/liste_aile.py. K1/K2/K4 bekleniyor; sonra K5.
- Tur 30: K4 bitti; kapanış betiği (suite 3 · mühür · D · gitleaks) → commit+push. claude -p: 32 API (K1·K2·30 istem) + 2 başlatma hatası (API yok).
