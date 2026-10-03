# TOKEN-6f — Headroom sıcak önbellek kırılması

KARAR: Headroom'a yalnız yama betiğiyle dokunulur; ayar/hook'a dokunulmaz; claude -p 0; API 0. ≤16 tur, 14'te DUR; 5/10/15'te "tur N/16".
Ekler: K2 sentetik dizi gerçek away_summary yapısından (içerik maskeli), iki biçim (ayrı mesaj / son user'a ekli). K3 ikinci test: soğuk önekte kompress_background+read_maturation hâlâ tetiklenir. Kök CC tarafındaysa (önceki tur gerçekten değişiyorsa) yama yok, DUR.

Kabul:
- K1 mühür (settings·hooks·mcp sha, sayım, fark; Headroom 0.37.0; yamalı dosya sha16; SHAPER/HOLDOUT/VERBOSITY dosya:satır)
- K2 kök neden dosya:satır + scratchpad yeniden üretim
- K3 iki test, yamasız kırmızı (sıcak) gösterildi
- K4 tools/headroom_yama.py: sürüm kilidi, idempotent, yedek, --durum/--geri-al; testler yeşil
- K5 kazanç öncesi/sonrası; düşüşte madde 21 tablosu
- K6 mühür eşit (yamalı sha hariç) · diff-filter=D boş · gitleaks · push

Durum:
- K1 1a659e5: proxy 0.39.0 runtime venv (uv 0.37 yalnız CLI) · yamalı sha16 anthropic a01ca804 · prefix_tracker 6ffca9b3 · cold_prefix 0a027998.
- K2 ce50d78: mod token (desktop env). Kök: (i) recap yan isteği lineage'ı eziyor → prefix_tracker.py:1488 yeni lineage → frozen 0; (iii) tracker TTL 600 < 1h. (ii) red. CC değil → yama.
- tur 5/16 (K3 başlıyor). Yama planı: resolve_tracker çatal geri dönüşü (ortak önek ≥ zincir−1 → tracker'ı yeniden kullan, frozen ortak öneke kısılır) + is_expired max(600, istek cache TTL ipucu); ipucu anthropic.py:1612 _cc_ttl'den.
- tur 10/16: K3 4d8ec82 (yamasız 4 kırmızı / 3 yeşil) · K4 88dfab7 (kök düzeltme, kuruluma uygulandı, 20/20) · K5 3915eb6 (kazanç +%5–8.5, ağırlıklı −%17.9).
- kapanış: mühür eşit (yamalı 2 sha hariç) · diff-filter=D boş · gitleaks temiz · suit 1131/1131 · push. Restart + awaySummaryEnabled true Ömer'de.
