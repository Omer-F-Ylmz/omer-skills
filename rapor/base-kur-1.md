# BASE-KUR-1 — base v0.16.0 kuruldu (FSL-1.1-ALv2, iç kullanım)

1. **Güvenlik:** zip sha256 `013a49b2…74d6` = sürüm sayfası. install.ps1 yalnız zip indirir → `base.exe install` koşar → `base`'i `base.exe` olarak kopyalar (boru yok, elle koştum). gitleaks 3 bulgu = test fixture sahte anahtarları (scrub.rs:321, match_log_test.rs:361/366); semgrep (p/default+p/rust; ilk `--config auto` metrics-off hatasıyla düştü) 22 bulgu: temp_dir/current_exe/unsafe/urllib, kritik yok.
2. **Kurulum:** `base install --starter-commands --no-corrections-line`, `base scaffold`, `base doctor` = HEALTHY. CLAUDE.md'ye BASE CLI bölümü eklendi (yedek: .kos/kopru/yedek/CLAUDE-oncesi-base-20261024.md).
3. **Kancalar:** settings.json'a 6 `base hook <olay>` girdisi eklendi (21→27), 0 silinen, tüm olaylarda eski sıra korunmuş, üst düzey anahtar farkı yok (ara/base-diff.txt). Yedek: yedek/settings-oncesi-base-20261024-105944.json.
4. **Gecikme (sentetik girdi, 5 koşu medyan):** session-start 0.12 sn (maks 0.76 soğuk), diğerleri 0.03–0.06 sn → 2 sn eşiğinin çok altında.
5. **A/B (claude -p haiku, 3 iş × 2 kol, n=1, $0.02 toplam):** bağlam (in+cache) bul 23.9k/22.1k, düzelt 37.2k/34.9k, devir 214k/123k (acik/kapali; devir'de tur 10 vs 7). Oturum başı sabit fark ≈ +0.9k jeton (cache_w 5701/4821). Doğruluk: bul ✓✓, düzelt ✓✓ (betik denetçisi `-I` yüzünden yanlış ✗ yazdı, elle yeniden koşuda ikisi OK), devir ✓✓. Süre acik/kapali: 8.7/7.1, 19.2/15.2, 27.0/21.7 sn; fark tur sayısı ve kanca (≤0.12 sn/çağrı) ile açıklanamayacak kadar gürültülü, ajan başlangıcı belirgin yavaşlamadı.
6. **Kısıt:** `claude -p` kullanıcı ayarlarında `enabledPlugins` varken asılıyor (kanca-sız ve base-sız ayarla da yeniden üretildi → base kaynaklı değil, önceden var). A/B bu yüzden eklentisiz ayarla (`--setting-sources project --settings`) koşuldu; CLAUDE.md'deki BASE bölümü iki kolda da yüklü (kapalı kol tam base-siz değil).
7. **Katalog:** yetenek-tam.jsonl'e `base` (cli) ve `base-hook` (hook) eklendi. Push yok.
8. **Ömer'e:** `base tune` bekleyen kural geçişi var; eklenti asılma sorunu ayrı bir işe konu olmalı.

Olcum betikleri/sonuclar: rapor/base-kur-1-olcum/. Katalog satirlari .kos (gitignore) altinda yetenek-tam.jsonl icinde, commit disi.
