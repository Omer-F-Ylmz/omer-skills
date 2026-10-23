# video-kurgu (DdY6e4Rsm0o)

**Amaç:** Referans görsel ve ses klipinden lip-sync video üretilmesi
**Araçlar:** LongCat-Video-Avatar 1.5 (Meituan, INT8DiT+DMD28-step distilled), ZeroGPUSpaces (yerel otomasyonlu platform)

**Adımlar**
1. [] Referans görsel (resim) ve ses klipini yükle
2. [] Kısa bir metin prompt'i gir (örneğin: 'Bu bir test video'dur')
3. [] Teknoloji tarafından otomatik olarak lip-sync video üretsin (5 saniye civarı)
4. [] Yerel bilgisayarda ZeroGPUSpaces üzerinden çalıştırılabilir

**Prompt/kod/ayar:** Uploadareferenceimage+audioclip+ashorttextprompt
**Sonuç:** Lip-sync video (5 saniye)
**Bizde (öneri, modelden):** Kurulu araçlarla referans görsel/ses klipini kullanarak lip-sync video üretebilmek için ZeroGPUSpaces veya benzer yerel platformlar kurmak gerekiyor.
**Daha iyi (öneri):** Meituan'ın LongCat-Video-Avatar 1.5 teknolojisinin yerel çalıştırılabilir versiyonunu kullanmak, Heygen gibi alternatiflere göre daha hızlı ve maliyet etkin olabilir.
