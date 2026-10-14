# VİDEO-3 devam (d1 → d2), 14 Eki ~18:50
DURUM: V1 ölçüldü, V2 kod + taban hazır, V2 Gemini koşusu 4/6 video önbellekte; HYMD (6 aralık) ve YDAK ücretsiz kota 429 ile düştü (iki flash + lite tükendi).
SIRADAKİ (d2):
1. Kota yenilenince (Gemini günlük sıfırlama ~10:00 TSİ): `cd tools/video && PYTHONPATH=. .venv/Scripts/python.exe ../../.kos/kopru/video/v3.py kos` (aralık önbelleği gemini-<sn>.json → kaldığı yerden; kos.json artımlı), sonra `... v3.py puan`.
2. Puan: yeni kol araç yakalama ≥0.90 değilse eksik kalemlere bak (taban `v3/taban.json`: 1nGx 12/18, aZe5 14/22, d_UE 3/13, FaCh 8/16, HYMD 39/39, YDAK 5/27).
3. Yeni kolun Claude adımı: kisa.calistir'in oturum() adımına uzun JSON'ları ver (claude -p ≤6 toplam; d1'de 0 kullanıldı) → ağır jeton ölç; hedef ≤0.30× taban (uzun taban video başı ~383k ağır; altın 6'da 60k–635k).
4. V3 carousel (ig- carousel: kisa_m4 EK sonuncusu ig-DcGy07ZMh5D gibi), V4 `video hat`, V5 — başlanmadı.
DOSYALAR: tools/video/video/uzun.py (araliklar/birlestir/izle/rapor_md) · tests/test_uzun.py 3/3 · .kos/kopru/video/v3.py (olc/taban/kos/puan) · rapor/video-3.md.
DİKKAT: kisa.py (VİDEO-KISA-TOKEN-1) değiştirilmedi, yalnız içe aktarılıyor. Ücretsiz kota tek anahtar; kisa hattıyla aynı anda koşturma.
