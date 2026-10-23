# security-audit (DeJxR3-hR5b)

**Amaç:** Kodlama agentlerinin güvenlik denetimi yapabilmesi için bir araç sağlamak.
**Araçlar:** Cloudflare security-audit-skill, Skills CLI (npx), GitHub (kaynak kodu)

**Adımlar**
1. [0:17-0:18] Beceri eklemek için komutu çalıştırın.
2. [0:19-0:21] Kod tabanını, giriş, veritabanı ve API'yi taratın.
3. [0:25-0:27] Hunters, güvenlik açıklarını tespit etmek için sistemde delikler arar.
4. [0:27-0:29] Sonuç olarak, detaylı bir rapor üretilir.
5. [0:29-0:33] Validatorlar, çoğu bulguyu çözer, ancak bazı küçük sorunlar kalır.

**Prompt/kod/ayar:** npx skills add https://github.com/cloudflare/ --skill security-audit
**Sonuç:** Güvenlik denetimi raporu (örneğin: kritik veya yüksek öncelikli sorunlar yok, ancak küçük sorunlar kalabilir).
**Bizde (öneri, modelden):** Kurulu araçlarla nasıl bir güvenlik denetimi yapılır: Cloudflare security-audit-skill kullanarak kod tabanını taratın, hunters ve validators ile test edin, raporu inceleyin.
**Daha iyi (öneri):** Kodlama sürecinde daha erken aşamalarda güvenlik denetimini uygulamak ve raporları otomatikleştirmek.
