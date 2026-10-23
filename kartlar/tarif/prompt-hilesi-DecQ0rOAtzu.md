# prompt-hilesi (DecQ0rOAtzu)

**Amaç:** AI yazılarının insan yazılarından ayırt edilebilir özniteliklerini (tells) kaldırmak ve doğal bir yazı tarzı elde etmek.
**Araçlar:** markdown dosyası (tells listesi), GitHub repo (humanizer skill), Claude modeli (veya diğer destekleyen AI modelleri)

**Adımlar**
1. [0:00-0:32] AI yazılarında kullanılan özniteliklerin (tells) bir listesini oluştur. Bu liste, Wikipedia'nın 'Signs of AI writing' rehberine dayanarak hazırlanmalıdır.
2. [0:24-0:32] Oluşturulan markdown dosyasını bir prompt ile AI modeline yükleyerek, modelin bu öznitelikleri kullanmasını engelle. Bu işlem, modelin 'Skills' özelliği aracılığıyla yapılır.
3. [0:11-0:13] AI'nin yazdığı metinlerdeki özniteliklerin kaldırıldığını doğrulayarak, doğal bir yazı tarzının elde edildiğini test et.

**Prompt/kod/ayar:** comment human and i will send you the repo
**Sonuç:** AI yazılarının insan yazılarından ayırt edilebilir özniteliklerinin kaldırılması ve doğal bir yazı tarzının elde edilmesi.
**Bizde (öneri, modelden):** kurulu araçlarla nasıl bir 'tells' listesi oluşturulur ve AI modeline nasıl entegre edilir?
**Daha iyi (öneri):** Bu yöntemin daha geniş bir AI modeli kütüphanesine entegre edilmesi ve kullanıcıların kendi 'tells' listelerini oluşturabilmesi için bir arayüz sağlanması.
