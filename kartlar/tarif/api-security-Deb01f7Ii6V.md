# api-security (Deb01f7Ii6V)

**Amaç:** API erişim kontrolü bozukluklarını tespit etme ve raporlama
**Araçlar:** Python, Playwright, HTTPX, FastAPI

**Adımlar**
1. [] İki farklı rolle kullanıcı hesabı oluştur. Örneğin, bir admin ve bir normal kullanıcı.
2. [] Kullanıcıların erişim izni olmayan nesneleri ve işlemleri hedefleyerek isteği yeniden oynat. Örneğin, bir admin hesabıyla normal kullanıcıya ait bir nesneye erişim isteği.
3. [] Erişim izni olmayan nesneler ve işlemler için farklılıkları manuel olarak doğrulayarak potansiyel güvenlik açıklarını tespit et.
4. [] Tespit edilen açıklar ve delilleri geliştirici dostu bir rapora dönüştür.

**Prompt/kod/ayar:** Create two accounts with different roles, replay captured requests with swapped object IDs, roles, and HTTP methods, flag suspicious differences for manual verification, generate evidence and developer-friendly report.
**Sonuç:** API erişim kontrolü bozukluklarının tespit edilmesi ve raporlanması.
**Bizde (öneri, modelden):** Kurulu araçlarla nasıl yapılır: FastAPI ve Playwright kullanarak API isteğini yakalayarak, farklı roller ve nesne ID'leriyle yeniden oynatma, farklılıkları manuel olarak doğrulama ve raporlama.
**Daha iyi (öneri):** Bilgisayar görü ile otomatik farklılık tespiti ve daha detaylı raporlama.
