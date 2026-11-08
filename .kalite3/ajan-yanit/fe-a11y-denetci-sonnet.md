Not: Çalışma dizininde (C:\Users\pc\AppData\Local\Temp\olcum-m3ox6ms1) denetlenecek html/tsx/jsx/vue/razor/cshtml/svelte dosyası yok. Bu yüzden dosya:satır kanıtı verilemedi. Aşağıdakiler genel kontrol listesidir, gerçek bulgu değildir. Dosya yolu verilirse kanıtlı rapor çıkarırım. Skill: fixing-accessibility yüklendi, hiçbir dosya değiştirilmedi.

Giriş formu için en önemli kontroller (önem sırasıyla):
1. Etiket: her input görünür `<label for>` ile bağlı olmalı, placeholder tek başına etiket sayılmaz · WCAG 1.3.1, 3.3.2, 4.1.2 · öneri: `<label for="email">` + `id="email"`.
2. Klavye: Tab sırası mantıklı olmalı, gönder düğmesi gerçek `<button type="submit">` olmalı (div/span değil), Enter ile gönderilmeli, tabindex>0 olmamalı · WCAG 2.1.1, 2.4.3 · öneri: yerel elemanlar kullan.
3. Odak görünürlüğü: `outline:none` kaldırılmışsa yerine görünür bir odak stili olmalı · WCAG 2.4.7, 2.4.11 · öneri: `:focus-visible` ile en az 3:1 kontrastlı halka.
4. Hata yönetimi: hatalar `aria-describedby` ile alana bağlanmalı, `aria-invalid="true"` set edilmeli, hata özeti `role="alert"` / aria-live ile duyurulmalı, yalnızca renkle belirtilmemeli · WCAG 3.3.1, 3.3.3, 4.1.3, 1.4.1 · öneri: "E-posta geçersiz" gibi metin + ikon.
5. Otomatik doldurma: `autocomplete="username"` / `"current-password"`, doğru `type` (email, password) · WCAG 1.3.5, 3.3.8 · öneri: bu öznitelikleri ekle; parola yapıştırmayı ve parola yöneticisini engelleme.
6. Kontrast: metin 4.5:1, input kenarlığı ve ikonlar 3:1 · WCAG 1.4.3, 1.4.11 · öneri: açık gri placeholder/kenarlığı koyulaştır.
7. Parola göster/gizle düğmesi: `aria-label` ve `aria-pressed` taşımalı, klavyeyle erişilebilmeli · WCAG 4.1.2 · öneri: `<button type="button" aria-pressed="false" aria-label="Parolayı göster">`.
8. Zorunlu alan ve yapı: `required` / `aria-required` duyurulmalı, `<form>` + tek `<h1>` ve `<main>` landmark'ı olmalı, devre dışı gönder düğmesi nedenini açıklamalı · WCAG 3.3.2, 1.3.1, 2.4.6 · öneri: yerel `required` ve anlamlı başlık.
9. Durum bildirimi: yükleniyor / başarısız giriş mesajı `aria-live` ile duyurulmalı, yalnızca toast olmamalı; odak hatalı alana veya hata özetine taşınmalı · WCAG 4.1.3, 3.2.2.
10. Büyütme ve dokunma hedefi: 200% zoom ve 320px genişlikte yatay kaydırma olmamalı, hedefler en az 24x24 px · WCAG 1.4.4, 1.4.10, 2.5.8.

Atladığım şey: kodu çalıştırıp axe/ekran okuyucu ile doğrulama yapmadım. Elde dosya yok.