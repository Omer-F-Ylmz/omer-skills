# CC kullanım kuralı (Ömer 27 Eki 18:39)

Desktop ve ajanlar Claude Code'u Ömer'in kullandığı gibi kullanır:

1. Tek oturum: proje başına kalıcı oturum. cc-kopru `ajan` ilk çağrıda `session_id`'yi `.kos/kopru/oturumlar/<proje>.json`'a yazar, sonrakilerde `--resume` ile aynı oturuma gönderir (önbellek ısınık kalır). Taze oturum: `yeni_oturum: true`. Girdi bağlamı 120k'yı (≈%60) geçince kayıt silinir, sonraki çağrı yeni oturum açar. Kapatmak: `kopru.json` → `oturumKalici: false`; klasör: `oturumDizin`.
2. Blok halinde iş: tek çağrıya birden çok madde; her küçük adım için ayrı oturum açma.
3. `/clear` yalnız iş değişince; gereksiz yeni oturum yok.
4. Küçük, tek seferlik iş = haiku, tek blok (`ajan_sira.py` kuyruğunda modelsiz satır zaten haiku/medium ile başlar).
5. Alt ajan kuyruğu (`ajan_sira.py`): her paralel işçi proje başına kendi kalıcı oturumunu kullanır (`oturumlar/<proje>-<n>.json`, `isci_oturum()`); çalışan bir işin işçi no'su başkasına verilmez, aynı oturuma eşzamanlı resume yok. Önceki işin girdi bağlamı 120k'yı aşar ya da hata verdiyse taze oturum. Kapatma: env `CC_ISCI_OTURUM_KAPALI=1`. Yalnız opus/sonnet/haiku işleri.

Doğrulama: `tools/cc-kopru/test/ajan-argv.test.mjs` (sahte claude ile kayıt, `--resume`, `yeni_oturum`). 2. çağrıda cache_read ≥%90 ölçümü gerçek (ücretli) çağrı ister, koşulmadı.
6. Oturumlar arası mesaj (F9): `python tools/oturum_mesaj.py gonder <alici> "<metin>"` / `al <alici>` (dosya kuyruğu `.kos/kopru/mesaj/`, self-check `test` 3/3). Basit/küçük iş yönlendirmesi: modelsiz kuyruk satırı haiku/medium (madde 4); Hermes (`motor=hermes`) ücretsiz modelle kuyruğu `al` ile okuyabilir, bağlanmadı.

## ARKA-AJAN (28 Eki 00:48, Ömer onayı — 21 Eki "detached yok" kuralına istisna)
- Desktop köprü çağrısı 60 sn sonra kesiliyor, cc-kopru yeniden başlıyor, Windows iş nesnesi çocuk claude -p süreçlerini öldürüyor (00:41 kanıt: yeni cc-kopru PID + 2 ajan aynı saniye).
- Uzun ajanlar: .kos/kopru/arka/<isim>.json yaz → `python tools/arka_ajan.py baslat <isim>` (Görev Zamanlayıcı, pythonw, pencere yok, kilit dosyası, log .kos/kopru/arka/<isim>.log, iş bitince görev silinir).
- Kısa (<60 sn) işler köprüden. Ölü oturum --resume edilmez (sarkık tool_use), devir brief ile taze oturum.
- ERTELE-1 (29 Eki): Desktop/ajanların CC işinde iş json'una `"ertele": true` verirse `tools/arka_ajan.py` oturumu skill listesi olmadan açar (`--disable-slash-commands` + `tools/ertele_istem.md` + 285 özel ajan reddi `tools/ertele_ayar.json`); skill/ajan `python tools/ertele_katalog.py ara|tam` ile o an yüklenir. Varsayılan kapalı; ölçüm `.kos/kopru/rapor/ertele-1.md`.
