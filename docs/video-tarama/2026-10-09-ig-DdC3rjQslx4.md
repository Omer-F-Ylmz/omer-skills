# Yapay zeka maliyetini 0 TL ye indirdim. Elinizdeki sistemi kullanarak siz de yap
## Künye
Yapay zeka maliyetini 0 TL ye indirdim. Elinizdeki sistemi kullanarak siz de yap · bunyamin.dev · süre: 1:08 · ? · https://www.instagram.com/reel/DdC3rjQslx4/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-26 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 30131 tk · claude-haiku-5-5: claude-haiku-5-5 · 17430 tk
## Özet
Konuşmacı, aylık yapay zekâ faturasını sıfırlamak için bulut ve lokal modelleri ayırıyor. Planlama ve dokümantasyonu Claude gibi bulut modellerine, kodlama ve analiz gibi mekanik işleri kendi GPU'sunda çalışan açık kaynak lokal modellere yaptırıyor. Lokal modelde VRAM önemli. Detaylı kurulum rehberi için yorum istiyor.
## Bölümler
- 0:00 Bulut ve lokal yapay zekâ farkı
- 0:22 Lokal modeller ve donanım (VRAM)
- 0:46 Hibrit kullanım: planlama bulutta, kodlama lokalde
- 1:02 Rehber videosu için yorum çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude | yok | teknik | yok | Planlama, mimari ve dokümantasyon için kullanılan bulut tabanlı güçlü model. | 0:48 | Ekranda '1. Planlama & Mimari → Claude (Bulut)' yazıyor; konuşmada da geçiyor. (karede: 0:48 OCR metni: '1. Planlama & Mimari → Claude (Bulut)' (bu an gönderilen karelerde yok).) |
| ChatGPT | yok | teknik | yok | Bulut tabanlı yapay zekâ servisi örneği olarak anılıyor. | 0:07 | Ekran metni: 'Yani Claude, ChatGPT'. (karede: 0:07 OCR metni: 'Yani Claude, ChatGPT' (gönderilen karelerde yok).) |
| DeepSeek | yok | teknik | yok | Lokal çalıştırılabilen açık kaynak model örneği. | 0:22 | Karede DeepSeek logosu ve adı görünüyor. (karede: Üç uygulama simgesinden solda mavi balina logolu DeepSeek yazısı.) |
| Llama.cpp | yok | CLI | yok | Modelleri lokal çalıştırmak için gösterilen çalıştırma kütüphanesi. | 0:22 | Karede Llama.cpp logosu ve adı görünüyor. (karede: Ortadaki turuncu logolu simge altında 'Llama.cpp' yazısı.) |
| Qwen | yok | teknik | yok | Lokal çalıştırılabilen açık kaynak model örneği. | 0:22 | Karede Qwen logosu ve adı görünüyor. (karede: Sağdaki simgede 'Qwen' görseli ve altında 'Qwen' yazısı.) |
| Lokal modeller | yok | iş akışı | yok | Kodlama ve analiz gibi tekrarlı işleri kendi GPU'sunda çalışan açık kaynak modellere yaptırma. | 0:54 | Ekranda '2. Kodlama & Analiz → Lokal Modeller' yazıyor. (karede: 0:54 OCR metni: '2. Kodlama & Analiz → Lokal Modeller' (gönderilen karelerde yok).) |
## Açıklama bağlantıları
- yok
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Açık kaynak modeller bulut tabanlı modeller kadar iyi performans vermiyor. | 0:40 | karşılaştırma |
| Büyük model için gereken ekran kartı gücü VRAM ile doğru orantılıdır. | 0:36 | özellik |
| Planlama ve dokümantasyon bulut modeline, kodlama ve analiz lokal modellere yaptırılmalı. | 0:48 | öneri |
| Lokal kurulum bir kez yapılıyor, sonrası ücretsiz. | 0:22 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Bulutta çalışan modeller | Claude | Şirket sunucularında çalışan modeller anlatılıyor. |
| kare 0:07 | ChatGPT | ChatGPT | Ekran metni: Yani Claude, ChatGPT. |
| kare 0:11 | Bulut API ve dev GPU sunucusu şeması | aday değil: genel kavram | Bulut iletişimi şeması. |
| kare 0:18 | Lokal ve çevrimdışı çalışma şeması | Lokal modeller | Model cihazda yüklü, internet yok. |
| kare 0:22 | DeepSeek | DeepSeek | Logo ve ad görünüyor. |
| kare 0:22 | Llama.cpp | Llama.cpp | Logo ve ad görünüyor. |
| kare 0:22 | Qwen | Qwen | Logo ve ad görünüyor. |
| konuşma 0:30 | GPU / ekran kartı | aday değil: genel kavram | Donanım yatırımı anlatılıyor. |
| kare 0:36 | VRAM | aday değil: genel kavram | 'VRAM İLE DOĞRU ORANTILI' yazıyor. |
| kare 0:48 | Planlama ve mimari için Claude (Bulut) | Claude | Ekran metni. |
| kare 0:54 | Kodlama ve analiz için lokal modeller | Lokal modeller | Ekran metni. |
| açıklama | Rehber isteği | aday değil: konu dışı | Açıklamada 'Rehber gelsin mi?' yazıyor. |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı. |
## Kareden okunanlar
- 0:11: Bulut yapay zekâ iletişimi (Cloud API): Senin Cihazın (Prompt Gönderir), 'İstek' düğmesi, Dev GPU Sunucusu (Bulut Veri Merkezi).
- 0:18: Lokal & çevrimdışı çalışma mantığı: Kendi Bilgisayarın (Model Cihazında Yüklü), İnternet Bağlantısı Yok, Verilerin Güvende.
- 0:22: DeepSeek, Llama.cpp ve Qwen simgeleri; altyazıda 'Kurulumu bir kez'.
## Belirsizlikler
- Altyazıda 'Cloudy, ChetCity, Pity' geçiyor; muhtemelen Claude, ChatGPT ve başka bir servis ama kesin değil.
- Sözlükteki Inter ve Geist eşleşmeleri ses kaynaklı hatalı eşleşme gibi; font kullanımı doğrulanamadı.
- Kullanılan lokal model, ekran kartı ve kurulum adımları anlatılmıyor; kurulum komutu yok.
- Yorumlar girişsiz alınamadı.
- Video dili belirtilmemiş; içerik Türkçe.
- 0:36 ve 0:40 zamanları yaklaşık; 0:07, 0:36, 0:48 ve 0:54 bilgileri OCR'dan, gönderilen üç karede yok.
- Altyazıda 'GPU'ya ekstra yatırım yaptım' cümlesi bozuk; ne kadar yatırım yapıldığı belli değil.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/reel/DdC3rjQslx4/ | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Bulut yapay zekâ çalışma mantığını anlatma: istek dev GPU sunucusuna gidiyor. — araçlar: Claude, ChatGPT
- 2. adım — Lokal çalışma mantığını anlatma: model kendi bilgisayarında internetsiz çalışıyor. — araçlar: Lokal modeller
- 3. adım — Açık kaynak lokal model örneklerini gösterme. — araçlar: DeepSeek, Llama.cpp, Qwen
- 4. adım — Ekran kartı ve VRAM ihtiyacını açıklama. — araçlar: Lokal modeller
- 5. adım — Planlama, mimari ve dokümantasyonu bulut modeline yaptırma. — araçlar: Claude
- 6. adım — Kodlama ve analiz gibi mekanik işleri lokal modellere yaptırma. — araçlar: Lokal modeller
- 7. adım — İzleyiciden yorumla rehber isteme. — araçlar: yok
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
