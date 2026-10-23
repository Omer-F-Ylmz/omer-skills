# otomasyon (Ded7ZFWRGmP)

**Amaç:** Claude'in tekrar eden görevleri otomatik olarak pratik yaparak, test sonuçlarına göre yetenek/kurallarını sürekli iyileştirme
**Araçlar:** GitHub repo (SkillOpt), Claude Code plugin (SkillOptSleep), Git komutları (clone, plugin yükleme), Test sonucu analiz sistemi

**Adımlar**
1. [0:31-0:38] Geçmiş Claude oturumlarını okuma (read-only)
2. [0:38-0:41] Tekrar eden görevleri tespit etme ve pratik yapma
3. [0:41-0:46] Kuralların taslak halini oluşturma
4. [0:43-0:50] Değişiklikleri test etme (geri tutulan görevler kullanılarak)
5. [0:50-0:54] Kullanıcı onayı ile değişiklikleri canlıya alma

**Prompt/kod/ayar:** /skillopt-sleep dry run (ön izleme) /skillopt-sleep adopt (onay)
**Sonuç:** Claude'in tekrar eden görevleri otomatik olarak pratik yaparak, test sonuçlarına göre yetenek/kurallarını sürekli iyileştirme
**Bizde (öneri, modelden):** Kurulu araçlarla, geçmiş Claude oturumlarını analiz ederek, tekrar eden görevleri tespit edip, test sonucu doğrultusunda kuralların otomatik olarak güncellenmesini sağlayan bir sistem oluşturmak.
**Daha iyi (öneri):** Microsoft'un test sonuçlarına göre otomatik olarak değişiklikleri test eden ve onaylanana kadar bekleyen sistemine benzer bir yapıyı, daha hızlı ve kullanıcı dostu bir arayüzle entegre etmek.
