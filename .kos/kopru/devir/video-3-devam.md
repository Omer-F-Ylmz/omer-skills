# VİDEO-3 devam (d2 → d3), 14 Eki ~19:25
DURUM: V2 Gemini kolu 5/6 puanlandı (aday 0.51, kapı 0.95 uzak; HYMD 2400/3600 aralığı 429). V3 carousel 3 koşuldu (v3/karusel.json önbellekte): 1.0 / 1.0 / 0.667 araç. claude -p 0/6 kullanıldı.
SIRADAKİ (d3):
1. HYMD: `cd tools/video && PYTHONPATH=. .venv/Scripts/python.exe ../../.kos/kopru/arka.py --cwd <tools/video> .kos/kopru/video/v3_kos3.log <.kos/kopru/video/v3.py> kos` (aralık önbelleği → yalnız eksik 2 aralık), sonra `v3.py puan`.
2. Uzun kol yakalama düşük: kos'ta metin_gec+birlestir (kisa'daki 2. geçiş) uzun videoya uygulanıyor mu bak; uygulanmıyorsa ekle, yeniden puanla. Sonra Claude adımı (kisa.calistir oturum(), claude -p ≤6) → ağır jeton.
3. YDAK süresi 33→110 sn: uzun.izle aralıkları ThreadPool ile paralelle (oran sınırına uygun 2–3 iş parçacığı).
4. Carousel yp (20/4/5) denetimi: yeni adlar pakette kanıtlı mı (kisa_m4._kanit) → kanıtlıysa referans kaçağı, kanıtsızsa gerçek yp. Dd7W (slayt videolu) kaçaklarına bak.
5. Ayrı sınama kümesi (uzun 2 + carousel 2, ayarlanmamış) — kapı geçerlilik şartı. V4 `video hat`, V5 başlanmadı.
DOSYALAR: .kos/kopru/video/v3.py (olc/taban/kos/puan/karusel), v3/kos.json, v3/karusel.json, rapor/video-3.md, tools/video/video/uzun.py.
DİKKAT: kisa.py / kisa_m4.py (VİDEO-KISA-TOKEN-1) değiştirilmedi, yalnız içe aktarılıyor. Ücretsiz Gemini kotası tek anahtar; kisa hattıyla aynı anda koşturma.
