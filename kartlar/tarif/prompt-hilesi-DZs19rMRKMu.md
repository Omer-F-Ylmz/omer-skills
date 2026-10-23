# prompt-hilesi (DZs19rMRKMu)

**Amaç:** AI'ya güvenli kod ürettirmek için 3 temel güvenlik açığını (API anahtarlarını gizleme, rate limiting ve girdi doğrulamasını) tek bir prompt ile çözmek.
**Araçlar:** Cursor, VS Code, Yapay Zeka Kodlama Asistanı

**Adımlar**
1. [] Önerilen prompt'i yapay zeka asistanına veya kod editörüne yapıştırarak çalıştırma.

**Prompt/kod/ayar:** Secret'lar sadece .env'de yaşar. Frontend'e asla sk-... yazma, .gitignore'a .env eklemeyi unutma. Her public endpoint'te rate limiting kur. Kullanıcı girdisine asla güvenme. Doğrulamayı sunucuda yap, Zod ya da Pydantic ile. Auth'u sıfırdan yazma. Hazır kütüphane kullan, parolaları bcrypt ile hashle.
**Sonuç:** Güvenli kod üretilmesi ve 3 güvenlik açığının çözülmesi.
**Bizde (öneri, modelden):** Kurulu araçlarla (Zod/Pydantic, bcrypt, rate limiting middleware) nasıl uygulanır?
**Daha iyi (öneri):** API anahtarlarını .env dosyasına saklamak ve frontend'e göndermeyi tamamen engellemek.
