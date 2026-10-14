# GRAPHIFY-ULTRA-1 — ARA (d5, 15 Eki 00:05)
Katalog: kullanılan [graphify_sor, graphify_ultra_g1 --sor, graphify_ultra_ab --c (yeni kol), olcum_sira, arka, bekle, rtk pytest] · atlanan [plan-kur/katalog (rutin tek alan), alt ajan (kural 0), G6 paket (çağrı 40 sınırı → devir)]
| ölçü | önce | sonra |
|---|---|---|
| artımlı update süre / tepe RSS | 48 sn / 829 MB | 3.8 sn / 332 MB (omer-skills, d2) · 3.1 sn / 74 MB (TELVE, d4) |
| G1 isabet, d4 seti | 15/20 (query --budget 400) | 18/20 (graphify_sor) |
| G1 isabet, d5 seti (yeni dosyalarla değişti, daha zor) | 11/20 (d4 graphify_sor) | 14/20 (d5 graphify_sor), 3.35 satır/yanıt |
| proje haritası | yok | omer-skills ~568 · TELVE ~596 jeton (≤800 ✓) |
| A/B keşif girdi jetonu (girdi+cr+cw) | A d3 ort. 1× | B d3 0.75×/0.87× · C d5 (kanca+keşif istemi) profil 1.00× · telve 0.74× |
- G5 kapısı (≤0.5×) GEÇMEDİ, iki denemede de. Doğruluk aynı (C yanıtları A ile aynı dosya:satır). Süre profil 70 sn (A 48–57), telve 55 sn (A 49–59). Kök: tur başına ~60k sabit bağlam (sistem istemi + araçlar), keşif 3–5 tur → harita/graphify_sor turu kısaltmıyor; 0.5× yalnız tur sayısı yarıya inerse olur.
- Desktop 23:55 kararı uygulandı: is-akisi keşif satırı DEĞİŞMEDİ (denendi, geri alındı); graphify_sor köprü profilinde kalır; global kanca önerisi yok.
- d5 graphify_sor düzeltmeleri: (1) aynı ad çoklu dosyada → soruda yolu geçen önce, sonra sığ yol (TELVE `_ham` kopyaları); (2) grafta düğümü olmayan dış sembol (QueryValueEx, geturl) → git grep tanım + çağrı yeri; (3) yedek belirteç ASCII (çağırıyor → "ağırıyor" sahte belirteci). Test tests/test_graphify_sor.py 3/3 (sentetik graf + git).
- graphify_hafif başarıyla bitince graphify_harita'yı çağırır (G3 tazelik).
- Kalan kaçaklar: md başlık sorusu (tanımlayıcısız, 2), TELVE `_ham` kopyalarında genel ad (2), belirsiz ad sıralaması (2).
- Yapılmadı: G6 paket (graphify skill 0.9.57→0.9.88, zip_denetle, atlas kartı), G0 izleme koşusu, BİTTİ. Devir: devir/graphify-ultra-1-devam.md
- claude -p: d5 2/2 (profil:1, telve:1), $1.15.
