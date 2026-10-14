# GRAPHIFY-ULTRA-1 — ARA (d2, 14 Eki)
Katalog: kullanılan [graphify extract/_is_ignored, cc-kopru ajan profili, rtk] · atlanan [plan-kur/katalog (rutin tek alan), alt ajan (kural 0)]
| ölçü | önce | sonra |
|---|---|---|
| artımlı update süre / tepe RSS | 48 sn / 829 MB | 3.8 sn / 332 MB (graphify_hizli, 3 dosya) |
| büyük dosya tam Read (sunucu.mjs 28 KB) | ~7k jeton | 1.4 KB iskelet (24 satır) + aralık |
| A/B profil (kanca tetiklenir) girdi · tur · sn | 334k · 5 · 57 | 199k · 3 · 46 (0.60×), yanıt ikisinde doğru |
| A/B hafif (kontrol, kanca tetiklenmez) | 198k · 3 · 47 | 334k · 5 · 56 → n=1 gürültüsü ±%70 |
- G4: tools/oku_yonlendir.py — Read PreToolUse; >300 satır + offset/limit yok → ilk istek red + gerekçede regex iskelet (py/js/ts/mjs/cs/md), aynı oturumda 2. istek geçer. Köprü ajan profiline (profiller/cc-arka.json ajan.ayar.hooks) bağlandı → tüm köprü ajanlarında aktif; global CC değil. Öz-sınama 5/5, ajan-argv 12/12.
- G2: .kos/kopru/graphify_hizli.py — graphify'ın extract()'ı yalnız değişen dosyalara, graf tek yükleme; graphify_hafif artımlı dalı buna bağlandı. Yeni semboller query'de çıkıyor; kapı oku AYNI, sorgu farkı yalnız eklenen düğümler.
- G5 kapısı (≤0.5×) KARAR VERİLEMEDİ: tetiklenen görevde 0.60×, ama kontrol görevi aynı gürültüyü gösterdi; n=1 ile kanıt yok. TELVE görevleri ve tekrar için claude -p izni gerekli (d2: 4/4 kullanıldı).
- Yapılmadı: G1 20 soru, G3 harita/kompakt, G6 paket, TELVE/Desktop grafları. Devir: devir/graphify-ultra-1-devam.md
- graphify update koşmadı: RAM %78 ≥ %75 kapısı (hafif reddetti).
