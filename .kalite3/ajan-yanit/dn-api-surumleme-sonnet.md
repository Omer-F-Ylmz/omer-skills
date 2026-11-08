Kapsam: C:\Users\pc\AppData\Local\Temp\olcum-pl8ltmgs içinde API sözleşmesi ya da endpoint kodu yok (*.cs, *.csproj, *.json, *.yaml, *.proto, *.graphql için Glob sonucu boş). Bu yüzden dosya:satır kanıtı veremiyorum. Aşağıdakiler genel API tasarım pratiğidir, repo bulgusu değildir.

KIRICI değişiklikler:
1. Alan, endpoint, parametre ya da enum değeri silmek veya yeniden adlandırmak. Öneri: önce kullanımdan kaldır, sonra sil.
2. Alanın tipini, biçimini veya null olabilirliğini değiştirmek (string yerine number, isteğe bağlı alanı zorunlu yapmak). Öneri: yeni alan ekle, eskisini koru.
3. Var olan istekte yeni zorunlu alan, daha sıkı doğrulama ya da yeni auth/scope şartı. Öneri: yeni alanı isteğe bağlı ve varsayılanlı ekle.
4. HTTP durum kodu, hata gövdesi veya hata kodu semantiğini, sıralamayı, sayfalama varsayılanlarını değiştirmek (Hyrum Yasası). Öneri: bunları sözleşmenin parçası say.
5. Gövde, yanıt veya alan uyumsuzluğu üreten serileştirme ayarı değişiklikleri (örneğin System.Text.Json adlandırma politikası). Öneri: yeni davranışı yeni sürümde aç.

KIRICI OLMAYAN: yeni isteğe bağlı alan, yeni endpoint, yeni isteğe bağlı sorgu parametresi. Tüketici bilinmeyen alanları yok saymalı (tolerant reader).

Sürümleme yolu (ASP.NET Core): Asp.Versioning ile URL segmenti (/v1/...). Genel API'de en açık yöntem budur. Dahili API'de başlık ya da media type da olur. Sürüm yalnızca kırıcı değişiklikte artar. Tek sürüm kuralı: mümkünse genişlet, çatallama. OpenAPI diff'ini (oasdiff) CI'a ekle, kırıcı değişiklik PR'ı kırmızı yapsın.

Kaldırma takvimi önerisi:
- T0: v2 yayında, v1 yanıtlarına Deprecation ve Sunset başlıkları eklenir.
- T+3 ay: tüketicilere ikinci duyuru, v1 kullanım metriği izlenir.
- T+6 ay: v1 salt-okunur veya uyarılı moda alınır.
- T+9 ay: kullanım yaklaşık %0 ise v1 kaldırılır ve 410 döner. Genel API için 12 ay.

Not: Gerçek kod verilirse bulgular dosya:satır kanıtıyla yeniden doğrulanmalı. Hiçbir dosya değiştirilmedi.