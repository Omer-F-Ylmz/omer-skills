# web-kod (DbIz3rdFF3T)

**Amaç:** Birden fazla bulut depolama sağlayıcısını tek bir arayüzle birleştirmek.
**Araçlar:** Vue.js (frontend), Express.js (backend API), Node.js (runtime), TailwindCSS (styling), SQLite (veritabanı), WebSocket (gerçek zamanlı iletişim)

**Adımlar**
1. [] OmniCloud'u yerel olarak kur veya Docker kullanarak çalıştır.
2. [] Her bulut sağlayıcı hesabını OAuth veya giriş bilgileriyle bağla.
3. [] Tek bir arayüzden tüm depolama hesaplarını tarayarak dosyaları yönet.
4. [] Yükleme işlemleri gerçek zamanlı ilerleme gösterir.
5. [] Dosyaları yeniden adlandır, sil veya yıldızdan çıkart.

**Prompt/kod/ayar:** OAuth/hesap-anahtar tabanlı bağlama, adapter katmanı ile sağlayıcı uyumlaştırması
**Sonuç:** Tek bir arayüzle 7+ bulut sağlayıcısını yöneten, gerçek zamanlı dosya işlemleri sunan bir platform.
**Bizde (öneri, modelden):** Kurulu araçlarla (Node.js, Express.js, Vue.js) benzer bir platform oluşturmak için adapter katmanı tasarlayabilirsiniz.
**Daha iyi (öneri):** Sağlayıcı uyumluluğunu artırmak için daha fazla API entegrasyonu ekleyebilirsiniz.
