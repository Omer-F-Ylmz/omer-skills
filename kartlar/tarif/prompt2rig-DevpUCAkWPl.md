# prompt2rig (DevpUCAkWPl)

**Amaç:** Metin prompt'inden canlı 3D hareket ve parmak izlemeyi çıkarmak.
**Araçlar:** GPU (video model analizi için), Fast video model (klip üretimi için), Mixamo karakteri veya diğer rigged karakterler (canlı performans için)

**Adımlar**
1. [] Kullanıcı metin prompt'ini girer.
2. [] GPU, video model tarafından üretilen klipteki 3D hareketleri ve el hareketlerini analiz eder.
3. [] Canlı olarak Mixamo karakteri veya diğer rigged karakterler tarafından hareketler canlandırılır.
4. [] Hareketler Blender veya Unity'ye doğrudan aktarılabilir.

**Prompt/kod/ayar:** Metin prompt'i (örn: 'el kaldır, parmakları bük')
**Sonuç:** Canlı 3D animasyon ve parmak izlemeyi içeren rigged karakterler.
**Bizde (öneri, modelden):** Kurulu araçlarla nasıl GPU analizi yapılırsa, prompt2rig bu işlemi otomatikleştirir.
**Daha iyi (öneri):** Hızlı video modeli ve GPU analizi ile manuel keyframing gerektirmeden 3D animasyon oluşturma.
