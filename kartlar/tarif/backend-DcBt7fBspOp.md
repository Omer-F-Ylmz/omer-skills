# backend (DcBt7fBspOp)

**Amaç:** Aynı ödeme isteğinin tekrar gönderilmesi durumunda kullanıcıdan tekrarlı ödeme alınmasını önlemek.
**Araçlar:** Idempotency key, Backend/Odeme Servisi (API)

**Adımlar**
1. [0:59-1:08] Her ödeme isteği ile birlikte benzersiz bir Idempotency key gönderilir.
2. [1:08-1:13] Sunucu Idempotency key'ini kontrol eder ve ilk kez gördüğü key için ödemeyi gerçekleştirir.
3. [1:13-1:17] Aynı Idempotency key ile tekrar gelen isteği reddederek önceki sonucu döndürür.

**Prompt/kod/ayar:** Idempotency-Key: 123
**Sonuç:** Kullanıcıdan ödeme yalnızca bir kez alındı.
**Bizde (öneri, modelden):** Backend servisimizde idempotency key'i kullanarak aynı ödeme isteğinin tekrarlanmasını önleyebiliriz.
**Daha iyi (öneri):** Idempotency key'ini daha uzun ve karmaşık yapmak, güvenliği artırabilir.
