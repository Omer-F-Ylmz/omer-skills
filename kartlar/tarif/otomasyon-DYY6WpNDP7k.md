# otomasyon (DYY6WpNDP7k)

**Amaç:** Uzaktan kod çalıştırmak ve test otomasyonu yapmak için mesajlaşma aracılığıyla Claude Code Channels kullanımı.
**Araçlar:** Telegram, Discord, iMessage

**Adımlar**
1. [00:00-00:02] Kullanıcı Claude'a mesaj gönderir ve istek verir.
2. [00:02-00:03] Claude, kullanıcı isteklerini doğrudan kodlamaya ve test etmeye başlar.
3. [00:03-00:04] Claude, kod değişikliklerini depolara yansıtır ve test sonuçlarını kullanıcıya geri döndürür.
4. [00:04-00:05] Kullanıcı yeni bir istek gönderir ve bu istekler de aynı şekilde yerine getirilir.
5. [00:05-00:06] Claude, kod refaktörleme ve değişiklikleri kullanıcıya diff özeti ile iletir.
6. [00:06-00:07] Kullanıcı Claude Code Channels'ı kurar ve ayarlar.
7. [00:07-00:07] Kullanıcı herhangi bir mesajla kod işlemlerini uzaktan yapar.

**Prompt/kod/ayar:** /plugin install telegram@claude-plugins-official
/telegram:configure YOUR_BOT_TOKEN
claude --channels plugin:telegram
/telegram:access pair CODE_FROM_BOT
**Sonuç:** Kullanıcı herhangi bir mesajla kod değişiklikleri yapar, testler çalıştırılır ve değişiklikler depolara yansıtılır.
**Bizde (öneri, modelden):** Kurulu araçlarla uzaktan kod çalıştırmak için Claude Code Channels'ı kullanarak, mesajlaşma aracılığıyla kod değişikliklerini ve testleri otomatikleştirmek.
**Daha iyi (öneri):** Kullanıcıların herhangi bir yerden ve herhangi bir zaman kod değişiklikleri yapabilmeleri için daha hızlı ve kolay bir kurulum süreci sağlanabilir.
