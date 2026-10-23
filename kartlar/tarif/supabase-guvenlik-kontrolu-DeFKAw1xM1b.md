# supabase-guvenlik-kontrolu (DeFKAw1xM1b)

**Amaç:** Veritabanı sızıntılarını önlemek ve güvenliği sağlamak
**Araçlar:** Supabase Dashboard

**Adımlar**
1. [0:15] RLS (Satır Güvenliği) ayarlarını Security Advisor ile kontrol edin.
2. [0:22] Kural policy'sini 'herkes okuyabilir'den 'sadece kendi verisi'ne çevirin.
3. [0:30] Secret key'in tarayıcı kodunda (client-side) bulunmadığından emin olun.
4. [0:37] Depolama (Storage) klasörlerinin erişim izinlerini denetleyin.
5. [0:44] Şifreleri düz metin saklamayın, Supabase Auth sistemini kullanın.

**Prompt/kod/ayar:** alter policy "sadece kendi verisi" using(auth.uid() = user_id)
**Sonuç:** Güvenli Supabase konfigürasyonu
**Bizde (öneri, modelden):** kurulu araçlarla nasıl
**Daha iyi (öneri):** Security Advisor kullanımı
