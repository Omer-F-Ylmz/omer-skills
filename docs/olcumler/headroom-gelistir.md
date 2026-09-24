# Headroom/RTK geliştirme (22)

## K1 önbellek ömrü
- Yakalama ($0, kaydedici 400): CC→kaydedici ve CC→ikinci Headroom (8792, v0.37)→kaydedici. İki gövdede de 3 `cache_control` kırılımı aynı yerde duruyor (system[1], system[2], messages[1].content[0]) ve hepsi `{"type":"ephemeral","ttl":"1h"}`. Headroom TTL'yi düşürmüyor.
- Üst akış kanıtı: K3 koşularında 6767 üzerinden dönen `usage.cache_creation` her istekte `ephemeral_1h_input_tokens` = tüm yazım, `ephemeral_5m_input_tokens` = 0. `outbound_headers` stripped_count=0.
- Günlük (proxy.log*, 22.09 18:46 – 24.09 13:37, 99 oturum, `x-claude-code-session-id`): aynı oturumda önceki isteğe göre aralık
  | aralık | istek | read oranı | tam kayıp (read≈0) |
  |---|---|---|---|
  | <5 dk | 4484 | 0.95 | 172 |
  | 5–60 dk | 40 | 0.39 | ~%80 (46'nın 37'si, >60 dk dahil) |
  | >60 dk | 6 | 0.38 | — |
  5–60 dk aralığında isabet 7 istekte var (22, 51 ve 55. dakikalar dahil). Yani 1 saatlik önbellek bazen tutuyor. Tam kayıpların nedeni TTL değil: TTL gövdede ve üst akışta 1h. Neden ölçülmedi: model değişimi, oturum içi sıkıştırma ve istek eşleme (FIFO, 453 kayıt eşlenemedi) ayrıştırılamadı. Headroom ayarıyla düzelecek bir aşama bulunmadı, bekleyen/headroom-ttl.md yazılmadı.
- Betikler: scratchpad k1_bosluk.py, k1_sinif.py (repo dışı).

## K2 RTK kapsamı
`rtk discover --since 3`: 6760 Bash komutunun %30.2'si RTK'dan geçiyor. audit-reads (440 oturum): Bash %51.1, Read %38.3, PowerShell %2.5. Repo filtresi: cc-kopru-suit artık `node --test`'i de eşliyor (75 çağrı). Filtre kazancı: fixture'da %89. Ayrıntı ve PowerShell sonucu: bekleyen/rtk-kural-2.md. Koruma testi tüm filtrelere genişledi (tests/test_21a.py). Mutasyonda `(?i)fail` eklenince 2 test kırmızıya döndü, sonra geri alındı.

## K3 bayat okuma
Read lifecycle v0.37'de varsayılan açık. Denenen özellikler: `--read-maturation` (beta) ve `--intercept-tool-results` (canary). A/B sonucu (docs/denemeler/headroom-okuma-sonuc.md, 16 claude -p, $5.47) **RED**: girdi +%17 (233k → 273k), sıcak $ +%19, kalite 2.69 → 2.63, süre 15.8 → 18.7 sn. Okuma görevleri düzenleme içermiyor, maturation taze Read'i önek dışında tutarak girdiyi büyütüyor. `headroom evals adversarial` ($0, çevrim dışı): payload hayatta kalma %93–100. `fake_system_tag` 15 hücrede sıkıştırmayı bastırıyor (bağışıklık bayrağı). Bu değerlendirme varsayılan hattı ölçüyor, iki özelliği değil.

## K4 hız
`headroom perf --hours 72`: total_pre_upstream p95 2135 ms. Bunun ~%95'i compression_first_stage (p50 18 ms, p95 2032 ms, maks 30.2 s). read_request_json p95 24 ms, kuyruk ~0. Günlükte 348 "Kompress slow" satırı var: ONNX inference p50 1.65 s, p95 5.9 s, maks 14.2 s. Makinede 24 çekirdek var; worker (24) ve concurrency (8) sınırı darboğaz değil. 30 s uçları 67–94k tokluk ardışık patlamalarda görülüyor. A/B `--disable-kompress` (docs/denemeler/headroom-hiz-sonuc.md, 8 yeni claude -p, temel kol K3 önbelleğinden) **RED**: girdi +%33 (233k → 311k), süre 15.8 → 17.6 sn, sıcak $ +%35, kalite 2.68 → 2.71. Kompress'i kapatmak kazanç getirmiyor.
