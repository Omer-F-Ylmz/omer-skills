# tersine-muhendislik (WTMd9fNloT0)

**Amaç:** Kompilasyon sonrası kodları analiz edip yapay zeka için erişilebilir hale getirme.
**Araçlar:** REA (Cloud'a entegre edilmiş araç), Ghidra (NSA tarafından geliştirilmiş açık kaynaklı araç), Hopper (Mac için tasarlanmış decompiler), IDA (endüstri standardı, pahalı araç)

**Adımlar**
1. [1:16-2:02] Programlama dillerini iki gruba ayırarak (kompilasyon sonrası ve yorumlanmış) REA'nın gerekliliğini açıklıyor.
2. [2:09-2:59] Kompilasyon sonrası kodun orijinal koddan nasıl farklılaştığını ve decompiling'in nasıl çalıştığını anlatıyor.
3. [3:07-4:25] REA'nın Ghidra, Hopper ve IDA gibi araçları Cloud'a entegre ederek kullanıcı dostu bir arayüz sağladığını açıklıyor.
4. [4:54-5:01] REA'nın Electron uygulamalarındaki gizli şifreyi bulma sürecini test ediyor.
5. [7:20-8:36] REA ile ve REA olmadan Cloud'a aynı görev için prompt vererek sonuçları karşılaştırıyor.

**Prompt/kod/ayar:** Opus 5.5 (yüksek seviye), REA kullanımı/olmaması
**Sonuç:** REA ile 200 dakika daha hızlı ve daha doğru sonuçlar elde edildi.
**Bizde (öneri, modelden):** kurulu araçlarla (Ghidra/Hopper/IDA) nasıl yapılırsa, REA'nın Cloud'a entegre edilmiş versiyonu ile daha hızlı ve kullanıcı dostu bir şekilde yapılır.
**Daha iyi (öneri):** REA, Ghidra/Hopper/IDA gibi araçların kullanımını kolaylaştırır ve Cloud'a entegre edilerek daha hızlı analiz sağlar.
