# web-kod (DeuLXZXtkGH)

**Amaç:** Canlı tarayıcıda modül ekleme işlemini test etme
**Araçlar:** Claude Code, Anthropic webapp-testing skill, Playwright, Chrome

**Adımlar**
1. [0:16-0:23] webapp-testing klasörünü .claude/skills içine kopyala.
2. [0:23-0:27] Claude Code'da `/webapp-testing` komutunu yaz ve test promptunu ver: modül ekleme, adı değiştirme, yenileme kontrolü.
3. [0:34-0:37] Claude tarafından Playwright testinin otomatik olarak hazırlanması ve çalıştırılması.
4. [0:45-0:51] Test sonuçlarını doğrulama: modül eklendi, adı değiştirildi, yenileme sonrası yeni adı kaldı.
5. [0:52-0:53] Ekran görüntüleri ve test dosyalarını kaydet.
6. [0:56-0:57] Testi sakla ve tekrar çalıştırılabilir hale getir.

**Prompt/kod/ayar:** /webapp-testing Modul eklemeyi canlı tarayıcında test et. Web Gelistirme'de "Yeni modul ekle" ile "Playwright Deneme" adında, açıklaması "Tarayıcı testi" olan 2 saatlik bir modül ekle; listede aorundaki kontrol et. Sonra adını "Playwright Deneme 2" yap ve kaydet. Sayfayı yenileyin; yeni adı durduğunu kontrol et. Her adımda ekran görüntüsü al, sonucu raporla, testi tekrar çalıştırabilir dosya olarak kaydet.
**Sonuç:** 8 kontrolü geçti (modül eklendi, adı değiştirildi, yenileme sonrası yeni adı kaldı).
**Bizde (öneri, modelden):** Kendi projede denemek için: webapp-testing klasörünü .claude/skills içine kopyala ve test veritabanı kullan.
**Daha iyi (öneri):** Test veritabanı kullanarak daha gerçekçi bir ortamda test etme.
