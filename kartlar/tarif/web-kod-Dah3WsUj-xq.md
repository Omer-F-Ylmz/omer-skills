# web-kod (Dah3WsUj-xq)

**Amaç:** Web sitesini tamamen yerel ortamda kullanmak için offline indirme.
**Araçlar:** wget, archiver, socket channel

**Adımlar**
1. [] wget komutu kullanılarak web sitesinin kaynak kodları ve varlıkları indirilir.
2. [] İndirilen veriler sıkıştırılır ve socket kanalından kullanıcıya gönderilir.
3. [] wget parametreleri kullanılarak indirme işlemi yapılır: --mirror, --convert-links, --page-requisites, --no-parent, --adjust-extension.

**Prompt/kod/ayar:** --mirror --convert-links --page-requisites --no-parent --adjust-extension
**Sonuç:** Web sitesinin tamamen offline kullanımına uygun bir kopyası oluşturulur.
**Bizde (öneri, modelden):** Kurulu araçlarla nasıl wget ve socket kanalı kullanılarak offline web indirme yapılır?
**Daha iyi (öneri):** Sıkıştırma ve dosya yönetimi için daha hızlı bir yöntem aranabilir.
