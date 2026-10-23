# otomasyon (Declah_AWHb)

**Amaç:** Claude hesaplarını ve ayarlarını temizleme ve doğrulama yapma
**Araçlar:** macOS/Linux/Windows için Rust+Tauri tabanlı native uygulamalar, Isolated Chromium profile (CCBaga-B), Browser fingerprinting ve sistem ayarları doğrulama, AI-guided network & system checks

**Adımlar**
1. [] Mevcut Claude ayarlarını ve kurulumunu arşivle (kaydet).
2. [] Seçilen bölgeye göre dil, saat dilimi ve ağ ayarlarını ayarla.
3. [] Tarayıcıyı yeniden başlat ve fingerprint doğrulamasını yap.
4. [] Sistem ve ağ okumalarını karşılaştır ve uyumluysa onay ver.
5. [] Kullanıcıya yeni bir Claude kimliği oluşturma veya mevcuttan değiştirme seçeneği sun.

**Prompt/kod/ayar:** CCBaga-A (native) + CCBaga-B (isolated Chromium) çalışır. Ayarlanan değişikliklerin doğrulanması ayrı adımlardır.
**Sonuç:** Kullanıcıya Claude ayarlarını temizleme ve doğrulama imkanı sağlar.
**Bizde (öneri, modelden):** Kurulu araçlarla Claude ayarlarını yönetmek için benzer bir otomasyon yapmak için Rust+Tauri tabanlı bir uygulama geliştirilebilir.
**Daha iyi (öneri):** Kullanıcı deneyimini daha kullanıcı dostu hale getirmek için GUI arayüzü geliştirilebilir.
