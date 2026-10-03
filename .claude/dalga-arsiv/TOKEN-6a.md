# TOKEN-6a — Headroom + oturum başı enjeksiyonları: teşhis ve ölçüm

KARAR
- Ayar/hook/skill/plugin/MCP/Headroom değişmez; silme yok; env değeri yazılmaz (varlık bool).
- K2 günlük tahmini: kol başına ilk istemin toplam ağırlıklı maliyeti farkı × oturum/gün; plan modu çekincesi docs'ta.
- okuyucu.md'ye env sorgu yasağı satırı (ajan dosyası ayar sayılmaz).

Kabul
- claude -p 7/7 · iş 21. turda kapandı.
- Mühür başla eşit (Headroom 3 alan ayrı satır) · kurulum eşit (skill 1054 · mcp 19 · plugin 47/53) · diff-filter=D boş · gitleaks · kod değişmedi → suite yok.

Durum
- Taban HEAD 1dc7272 · mühür scratchpad/muhur-6a.json.
- [x] okuyucu kuralı a01c75a · [x] K1 fc16dbf · [x] K3 b81573a · [x] K4 67cf07a · [x] K2 · [x] K5 · [x] kapanış (hash'ler git log'da).

Sonuç
- K1: Headroom Desktop siler/geri yazar (çıkış · pause · auto-pause · çökme bekçisi); guard yalnız okur; 14 gün kapalı-dönem payı cli+sdk-cli 0/6102 (600 sn).
- K2: ilk ctx'te en pahalı claude-mem (−3.8k) ama kapalıyken Explore → +%180; dördü kapalı −%40 (−1.2 M/gün @14 oturum); b/c/d tek tek bant içinde.
- K3: HOLDOUT=0/1 iki kol, rtk-ab 2+2 + orta 1+1, madde 21.

Sapmalar
- Plan aşaması: okuyucu HKCU HEADROOM_OUTPUT_SHAPER uzunluk/truthy bilgisi çıkardı; bulgu kullanılmadı; okuyucu.md'ye yasak eklendi.
- K2 n=1/kol; c ve g error_max_turns (tavan 10); SessionStart karakterleri output+stdout toplamı, yalnız oran kullanıldı.
- docs/token-6a.md'de bölüm sırası K1·K3·K4·K2·K5 (K2 koşusu sürerken K3/K4 commit edildi).
