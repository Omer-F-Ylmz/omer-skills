---
type: report
status: done
tags: [ucretsiz-motor-1, ajan_sira, omniroute]
relatedTo: [ajan_sira, maliyet_defter]
---
# UCRETSIZ-MOTOR-1 (24 Eki)

- Motor: `tools/ucretsiz_motor.py` + `ajan_sira.py` (`motor=ucretsiz` sütunu, MERDIVEN 0. basamak `("ucretsiz","high")`, eski basamaklar +1 kaydı). claude CLI aynı bayraklar; ANTHROPIC_BASE_URL=OmniRoute (`/v1/messages`, Anthropic uyumlu), model `ucretsiz-ozet2`.
- Kimlik: alt süreç env'inden `ANTHROPIC_*`, `CLAUDE_CODE_OAUTH*`, `OMNIROUTE_KEY` temizlenir; tek kimlik `ANTHROPIC_AUTH_TOKEN`; `--settings` kopyası anahtarsız. Kanıt: gerçek claude süreci sahte uca istek attı, başlıklarda `sk-ant` yok, yalnız proxy anahtarı (test_kanit_abonelik_kimligi_proxy_surecine_gecmez).
- Model seçimi (araç çağrısı ölçümü, /v1/messages): ozet2, ozet, groq, auto/coding:free, auto/best-free hepsi `tool_use` döndü. Canlı Write+Read+Bash görevi: ozet2 KABUL (4 tur, 243 sn, Claude $0); groq aynı görevde 429 rate limit.
- Sınıflayıcı: görev ilk satırı+ad; zor işaret ezer, kolay işaret yoksa Haiku'dan başlar. Türde son 7 gün ücretsiz başarı <%80 → doğrudan haiku (`ucretsiz_zayif`, `ucretsiz_oran`). Anahtar yoksa 0. basamak atlanır.
- Başarısızlık: rc≠0 ya da görevde `KABUL` satırı varken raporda yok → üst basamak. Defter $ = 0 (claude'un uydurma fiyatı yazılmaz).
- Test: yeni 9 (test_ucretsiz_motor) + test_ajan_sira güncel = 70 yeşil. Tam suit: jev 85, mcp/jev 40, jev-dotnet 22, tools/tests 379 yeşil; tests 937/941, 3 kırmızı bu işle ilgisiz (test_katalog_ek rea_oto, test_blender_uretim kontur, test_ucretsiz_havuz jeton kovası; hiçbiri ajan_sira/ucretsiz_motor/maliyet_defter'e dokunmuyor). tools/video ve tools/cc-kopru çıktısı kesildi, sonuç doğrulanamadı.
- Maliyet: son 20 iş ort. $0.79 (toplam $15.81, 379 kayıtlı iş). "Sonra" ölçümü YAPILMADI: kuyrukta henüz motor=ucretsiz ile koşan gerçek iş yok; ≥%60 düşüş hedefi doğrulanmadı.
- Yapılmadı: madde 4 (ordu-on 10 iş ölçümü; ücretsiz işler birikmeden ölçülemez), madde 5 (Hermes kurulu değil), kolay işlere varsayılan olarak motor=ucretsiz atamak main() içinde `basamak_sec` ile bağlı ama canlı kuyrukta sınanmadı.
- Devam: kolay bir işi `motor=ucretsiz` sütunuyla kuyruğa ekle, `maliyet.tsv` ucretsiz-high satırını ve KABUL'ü izle.
