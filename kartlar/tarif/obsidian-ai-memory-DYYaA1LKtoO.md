# obsidian-ai-memory (DYYaA1LKtoO)

**Amaç:** Kişisel proje belleğini AI ile yönetmek için bir sistem oluşturmak.
**Araçlar:** Obsidian (desktop app), Claude Cowork (veya başka AI araçları), Markdown dosyaları (README.md, STATUS.md, progress.md, decisions.md)

**Adımlar**
1. [0:17-0:26] Obsidian uygulaması indir ve yeni bir vault oluştur. Bu, bilgisayarınızdaki bir klasör gibidir.
2. [0:26-0:39] Proje için Obsidian vault içinde bir klasör oluştur ve bu klasörü AI araçlarına bağla. AI'ye klasörün okuma/yazma erişimine sahip olması gerekir.
3. [0:49-1:25] Başlangıç prompt'ini kullanarak AI'ye proje için 4 ana dosya oluşturmasını söyle. Bu dosyalar şunlardır: README.md (proje açıklaması), STATUS.md (şu anki durum), progress.md (gelişme takibi), decisions.md (kararlar). AI'ye proje kontekstini ve geçmişini dikkate alarak bu dosyaları oluşturmasını söyle.
4. [1:32-1:37] Eğer proje konteksti AI'de (örn. Claude Cowork) ise, AI'ye bu 4 dosyayı doğrudan yazmasını söyle ve ardından manuel olarak Obsidian'a kopyala.
5. [1:50-2:03] Her çalışma oturumunun sonunda AI'ye bellek dosyalarını güncellemesini söyle. Bu prompt, STATUS.md güncellemesi, yeni progress.md girişleri, yeni kararlar ve README.md güncellemeleri gibi işlemleri içerir.

**Prompt/kod/ayar:** Başlangıç prompt: AI'ye proje için 4 dosya oluşturmasını söyle. Güncelleme prompt: STATUS.md, progress.md, decisions.md ve README.md güncellemeleri için AI'ye talimat ver.
**Sonuç:** Proje için AI ile yönetilen bir bellek sistemi oluşturulur. Bu sistem, AI araçlarının proje kontekstini anlayabilmesi için 4 ana dosyayı kullanır ve her çalışma oturumunun sonunda güncellenir.
**Bizde (öneri, modelden):** Kurulu araçlarla (Obsidian + AI araçları) benzer bir sistem oluşturmak için, başlangıçta proje klasörü oluşturulur, ardından AI'ye proje kontekstini anlatmak için başlangıç prompt'leri verilir. Güncellemeler için de benzer prompt'ler kullanılabilir.
**Daha iyi (öneri):** AI'nin proje kontekstini daha iyi anlayabilmesi için, proje dosyalarının düzenli olarak güncellenmesi ve AI'ye daha detaylı prompt'ler verilebilir. Ayrıca, AI araçlarının proje klasörüne erişimi kolaylaştırılabilir.
