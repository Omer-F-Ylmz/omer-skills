# 📱 A half-gigabyte AI model now runs real agents on your phone, no cloud.
## Künye
📱 A half-gigabyte AI model now runs real agents on your phone, no cloud. · fullstackparody · süre: 0:00 · ? · https://www.instagram.com/p/DeMyQ4PjZlr/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-31 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (7)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 32427 tk · claude-haiku-5-5: claude-haiku-5-5 · 125104 tk
## Özet
Instagram görsel gönderisi (carousel, 7 kare): OpenBMB'nin 1 milyar parametreli cihaz içi modeli MiniCPM5 tanıtılıyor. Model telefonda bulutsuz çalışıyor, MCP ve yerel araç çağırmayı destekliyor, 128K bağlam sunuyor, ajan ve akıl yürütme kıyaslarında ortalama 42.57 ile bir sonraki en iyi 1B modeli (35.61) geride bırakıyor. Ağırlıklar Apache 2.0 ile Hugging Face'te; vLLM, SGLang ve Transformers ile çalıştırılıyor. Kare 2'de GitHub deposu, kare 6'da Python kurulum ve çalıştırma kodu gösteriliyor.
## Bölümler
- 0:00 Kapak: 0.5GB, ajan çalıştırır
- 0:00 Kaynak: GitHub OpenBMB/MiniCPM deposu
- 0:00 Nedir: minicpm5, telefonda 1B model
- 0:00 Bellek: 128k token bağlam
- 0:00 Skor: kıyas tablosu
- 0:00 Nasıl çalıştırılır: açık ağırlıklar ve kod
- 0:00 Kapanış: takip çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| MiniCPM5 | yok | teknik | https://github.com/OpenBMB/MiniCPM | OpenBMB'nin 1B parametreli, cihaz içi, 128K bağlamlı, yerel araç çağıran dil modeli | 0:00 | Kare 3'te 'minicpm5' ve 'A 1-billion-parameter model that runs entirely on your phone' yazıyor. (karede: Turuncu kutuda 'minicpm5', telefonda MiniCPM5 sohbeti, sağda 1B parametre açıklaması) |
| OpenBMB | yok | teknik | https://github.com/OpenBMB/MiniCPM | MiniCPM modelini geliştiren kuruluş ve GitHub organizasyonu | 0:00 | Kapakta 'OPENBMB - MINICPM5' ve kare 2'de OpenBMB / MiniCPM deposu görünüyor. (karede: Üstte 'OPENBMB - MINICPM5'; GitHub'da OpenBMB / MiniCPM) |
| GitHub | yok | teknik | yok | MiniCPM kaynak deposunu barındıran servis | 0:00 | Kare 2'de tarayıcıda github.com/OpenBMB/MiniCPM sayfası açık. (karede: Tarayıcı adres çubuğunda github.com/OpenBMB/MiniCPM, depo dosya listesi) |
| Hugging Face | yok | teknik | yok | Model ağırlıklarının yayımlandığı platform | 0:00 | Kare 6'da 'live on Hugging Face' yazıyor; açıklamada da geçiyor. (karede: Sağ kartta 'The weights are open under Apache 2.0 and live on Hugging Face.') |
| vLLM | yok | CLI | yok | Modeli sunmak için çıkarım motoru; 'vllm serve' komutu gösteriliyor | 0:00 | Kare 6 kodunda 'pip install vllm' ve 'vllm serve OpenBMB/MiniCPM5-1B --dtype bfloat16' var. (karede: Kod penceresinin altında '# Or run with vLLM' ve vllm serve komutu) |
| SGLang | yok | teknik | yok | Modeli çalıştırmak için anılan çıkarım çerçevesi | 0:00 | Kare 6 açıklamasında 'Run it with vLLM, SGLang or Transformers' yazıyor. (karede: Sağ kartta 'Run it with vLLM, SGLang or Transformers') |
| Transformers | yok | teknik | yok | Hugging Face Transformers kütüphanesi; AutoModelForCausalLM ile model yükleme | 0:00 | Kare 6 kodunda 'pip install transformers torch' ve 'from transformers import AutoModelForCausalLM' var. (karede: Kod penceresinde 'from transformers import AutoModelForCausalLM,' ve AutoTokenizer) |
| PyTorch | yok | teknik | yok | Kodda torch, bfloat16 ve device_map ile model yüklemede kullanılan kütüphane | 0:00 | Kare 6'da 'import torch' ve 'torch_dtype=torch.bfloat16' görünüyor. · kanıt: kare (karede: Kodda 'import torch' ve 'torch_dtype=torch.bfloat16') |
| MCP | yok | MCP | yok | Model Context Protocol; modelin araç çağırma için desteklediği protokol | 0:00 | Kare 3 ve 6'da modelin MCP'yi desteklediği yazıyor. (karede: Kare 3'te 'It supports MCP and native tool calling'; kare 6'da 'speaks MCP for tool calling') |
| Qwen2.5-1.5B | yok | teknik | yok | Kıyas tablosunda karşılaştırılan model (34.12) | 0:00 | Kare 5 tablosunda Qwen2.5-1.5B satırı 34.12 ile listeleniyor. (karede: Tabloda 'Qwen2.5-1.5B / 34.12') |
| Phi-3-mini | yok | teknik | yok | Kıyas tablosunda karşılaştırılan model (32.08) | 0:00 | Kare 5 tablosunda Phi-3-mini satırı var. (karede: Tabloda 'Phi-3-mini / 32.08') |
| Gemma-2B | yok | teknik | yok | Kıyas tablosunda karşılaştırılan model (31.46) | 0:00 | Kare 5 tablosunda Gemma-2B satırı var. (karede: Tabloda 'Gemma-2B / 31.46') |
| Llama-3.2-1B | yok | teknik | yok | Kıyas tablosunda karşılaştırılan model (30.91) | 0:00 | Kare 5 tablosunda Llama-3.2-1B satırı var. (karede: Tabloda 'Llama-3.2-1B / 30.91') |
| SmolLM2-1.7B | yok | teknik | yok | Kıyas tablosunda karşılaştırılan model (29.87) | 0:00 | Kare 5 tablosunda SmolLM2-1.7B satırı var. (karede: Tabloda 'SmolLM2-1.7B / 29.87') |
| MobileLLM-1.4B | yok | teknik | yok | Kıyas tablosunda karşılaştırılan model (28.21) | 0:00 | Kare 5 tablosunda MobileLLM-1.4B satırı var. (karede: Tabloda 'MobileLLM-1.4B / 28.21') |
| TinyLlama-1.1B | yok | teknik | yok | Kıyas tablosunda karşılaştırılan model (25.63) | 0:00 | Kare 5 tablosunda TinyLlama-1.1B satırı var. (karede: Tabloda 'TinyLlama-1.1B / 25.63') |
| BeautifulSoup | yok | teknik | yok | Telefondaki örnek kod özetinde geçen HTML ayrıştırma kütüphanesi | 0:00 | Kare 3'te kodda 'from bs4 import BeautifulSoup' görünüyor. (karede: Telefon ekranında 'from bs4 import BeautifulSoup' ve 'BeautifulSoup(response.text') |
| Python requests | yok | teknik | yok | Telefondaki örnek kodda HTTP isteği için kullanılan kütüphane | 0:00 | Kare 3 kodunda 'import requests' ve 'requests.get(url)' var. · kanıt: kare (karede: Telefon ekranında 'import requests' ve 'response = requests.get(url)') |
| Apache-2.0 | yok | teknik | yok | Modelin ve deponun lisansı | 0:00 | Kare 2'de 'Apache-2.0 license', kare 6'da 'Apache 2.0, open weights' yazıyor. (karede: Depo sayfasında 'Apache-2.0 license'; kare 6'da 'Apache 2.0, open weights') |
| Telefonda yerel model ile kod özetleme | yok | prompt | yok | Kullanıcı modelden bir kodu özetlemesini ve ne yaptığını açıklamasını istiyor (web kazıyıcı Python betiği örneği). | 0:00 | kaynak: kare |
| 128K bağlamla uzun belge özetleme | yok | prompt | yok | Kullanıcı ai_research_paper.pdf (112 sayfa) dosyasını okumasını ve ana bulgularla ayrıntılı özet vermesini istiyor. | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| pip install transformers torch | Transformers ve PyTorch kütüphanelerini kurar (karede: Kare 6'da run_minicpm5.py içinde 'pip install transformers torch') | 0:00 | kare |
| pip install vllm | İsteğe bağlı olarak vLLM çıkarım motorunu kurar (karede: Kare 6'da 'pip install vllm # (optional, for vLLM)') | 0:00 | kare |
| vllm serve OpenBMB/MiniCPM5-1B --dtype bfloat16 | MiniCPM5-1B modelini vLLM ile bfloat16 hassasiyetinde sunar (karede: Kare 6 altında '# Or run with vLLM' ve vllm serve komutu) | 0:00 | kare |
| pip install vllm # (optional, for vLLM) | İsteğe bağlı olarak vLLM kütüphanesini kurar. (karede: İkinci pip satırında 'pip install vllm' ve yanında '(optional, for vLLM)' yorumu.) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| MiniCPM5 1 milyar parametreli ve tamamen telefonda, bulut arka ucu olmadan çalışıyor. | 0:00 | özellik |
| Model MCP ve yerel araç çağırmayı destekliyor, çevrimdışı ajan işi yapabiliyor. | 0:00 | özellik |
| 128.000 token bağlam, yaklaşık 96.000 kelime, cihaz içinde. | 0:00 | sayısal |
| Ajan ve akıl yürütme kıyaslarında ortalama 42.57; sonraki en iyi 1B model 35.61. | 0:00 | karşılaştırma |
| Kodlama, matematik, mantık ve ajan görevlerinde önde. | 0:00 | karşılaştırma |
| Ağırlıklar Apache 2.0 ile açık, Hugging Face'te; vLLM, SGLang veya Transformers ile çalışıyor. | 0:00 | özellik |
| Yarım gigabaytlık model telefonda gerçek ajanları çalıştırıyor. | açıklama | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 1 · 0:00 | OpenBMB | OpenBMB | 'OPENBMB - MINICPM5' başlığı |
| kare 1 · 0:00 | MiniCPM5 | MiniCPM5 | Kapakta MINICPM5 |
| kare 1 · 0:00 | 0.5GB boyut iddiası | aday değil: genel kavram | '0.5GB.' başlığı |
| kare 2 · 0:00 | GitHub deposu | GitHub | github.com/OpenBMB/MiniCPM |
| kare 2 · 0:00 | openbmb.github.io/MiniCPM/ | aday değil: başka adayın parçası (MiniCPM5) | Hakkında bölümündeki bağlantı |
| kare 2 · 0:00 | MiniCPM-o 2.6 | aday değil: başka adayın parçası (MiniCPM5) | Releases bölümünde Latest etiketi |
| kare 2 · 0:00 | Apache-2.0 lisansı | Apache-2.0 | README sekmesinde Apache-2.0 license |
| kare 2 · 0:00 | Konu etiketleri (llm, multimodal, edge-ai, on-device, vla) | aday değil: genel kavram | Depo konu etiketleri |
| kare 3 · 0:00 | MCP | MCP | 'It supports MCP and native tool calling' |
| kare 3 · 0:00 | Yerel araç çağırma | aday değil: genel kavram | native tool calling |
| kare 3 · 0:00 | BeautifulSoup | BeautifulSoup | Telefon ekranındaki kodda |
| kare 3 · 0:00 | requests | Python requests | import requests |
| kare 3 · 0:00 | csv modülü | aday değil: genel kavram | import csv, standart kütüphane |
| kare 4 · 0:00 | 128k token bağlam | aday değil: genel kavram | '128k tokens' başlığı |
| kare 4 · 0:00 | ai_research_paper.pdf | aday değil: genel kavram | Örnek dosya, araç değil |
| kare 5 · 0:00 | benchmark.py | aday değil: genel kavram | Kıyas betiği penceresi |
| kare 5 · 0:00 | Qwen2.5-1.5B | Qwen2.5-1.5B | Tablo satırı 34.12 |
| kare 5 · 0:00 | Phi-3-mini | Phi-3-mini | Tablo satırı 32.08 |
| kare 5 · 0:00 | Gemma-2B | Gemma-2B | Tablo satırı 31.46 |
| kare 5 · 0:00 | Llama-3.2-1B | Llama-3.2-1B | Tablo satırı 30.91 |
| kare 5 · 0:00 | SmolLM2-1.7B | SmolLM2-1.7B | Tablo satırı 29.87 |
| kare 5 · 0:00 | MobileLLM-1.4B | MobileLLM-1.4B | Tablo satırı 28.21 |
| kare 5 · 0:00 | TinyLlama-1.1B | TinyLlama-1.1B | Tablo satırı 25.63 |
| kare 6 · 0:00 | Hugging Face | Hugging Face | 'live on Hugging Face' |
| kare 6 · 0:00 | vLLM | vLLM | vllm serve komutu |
| kare 6 · 0:00 | SGLang | SGLang | Açıklama metninde |
| kare 6 · 0:00 | Transformers | Transformers | pip install transformers torch |
| kare 6 · 0:00 | torch | PyTorch | import torch |
| kare 6 · 0:00 | pip | aday değil: genel kavram | Python paket yöneticisi komutları |
| kare 6 · 0:00 | run_minicpm5.py | aday değil: başka adayın parçası (MiniCPM5) | Örnek betik dosyası |
| kare 7 · 0:00 | @fullstackparody | aday değil: konu dışı | Hesap takip çağrısı |
| açıklama | Next.js (sözlük eşleşmesi) | aday değil: konu dışı | Açıklamada geçmiyor |
| açıklama | Claude (sözlük eşleşmesi) | aday değil: konu dışı | Açıklamada geçmiyor |
| açıklama | Hashtag'ler (#minicpm #ondeviceai #edgeai #llm #aiagents) | aday değil: genel kavram | Açıklama sonu etiketleri |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 1 · 0:00: 'OPENBMB - MINICPM5', '0.5GB.', 'runs agents.', elde iPhone.
- 2 · 0:00: github.com/OpenBMB/MiniCPM; 17.5k yıldız, 1.4k fork, 315 commit, Apache-2.0, Python %98.1; açıklama 'MiniCPM5: SOTA on-device LLMs, small yet powerful'; son sürüm MiniCPM-o 2.6.
- 3 · 0:00: 'minicpm5', 1B parametre telefonda; MCP ve yerel araç çağırma; kod özetleme sohbeti (BeautifulSoup, requests, csv).
- 4 · 0:00: '128k tokens', ~96.000 kelime; ai_research_paper.pdf 112 sayfa 2.3 MB özetleme sohbeti.
- 5 · 0:00: benchmark.py tablosu: MiniCPM5-1B 42.57, next-best 1B 35.61, Qwen2.5-1.5B 34.12, Phi-3-mini 32.08, Gemma-2B 31.46, Llama-3.2-1B 30.91, SmolLM2-1.7B 29.87, MobileLLM-1.4B 28.21, TinyLlama-1.1B 25.63.
- 6 · 0:00: run_minicpm5.py: pip install transformers torch, pip install vllm, AutoModelForCausalLM ile OpenBMB/MiniCPM5-1B yükleme, vllm serve komutu.
- 7 · 0:00: 'follow for more.' ve '@fullstackparody / coding + ai tools'.
## Belirsizlikler
- Video yok, görsel gönderi; tüm zamanlar 0:00 olarak verildi, kareler 1-7 sırasıyla.
- Kare 2'deki GitHub sayfası MiniCPM-o 2.6'yı son sürüm gösteriyor, MiniCPM5 sürümü orada görünmüyor; depo içeriği ile gönderi iddiası tam örtüşmüyor.
- Kare 5'teki 'next-best 1B' satırı adsız; hangi modelin kastedildiği belli değil.
- Kıyas tablosu görsel olarak üretilmiş/stilize görünüyor; sayıların resmi kaynağı doğrulanamadı.
- Açıklamadaki '0.5 GB' boyutu için kayıt formatı (nicemleme) belirtilmiyor.
- Kare 6'daki kod fiilen çalıştırılmıyor, yalnız gösteriliyor; kare 3 örnek kod da kesik.
- Sözlük eşleşmeleri Next.js ve Claude açıklamada geçmiyor; gönderiyle ilgisiz kabul edildi.
- Yorumlar girişsiz alınamadı.
- Hashtag'lerde 'aitools' ve 'opensource' etiketleri; araç değil.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/p/DeMyQ4PjZlr/ | açıklama | açıklama | hayır |
| github.com/OpenBMB/MiniCPM | 0:00 | ekran | evet |
| openbmb.github.io/MiniCPM/ | 0:00 | ekran | hayır |
## İş akışı
- 1. adım — Gönderi kapağı: MiniCPM5'in 0.5GB ile telefonda ajan çalıştırdığı duyuruluyor — araçlar: MiniCPM5, OpenBMB
- 2. adım — Kaynak gösteriliyor: GitHub'daki OpenBMB/MiniCPM deposu — araçlar: GitHub, MiniCPM5
- 3. adım — Model tanıtılıyor: telefonda 1B yerel model, MCP ve araç çağırma, kod özetleme örneği — araçlar: MiniCPM5, MCP, BeautifulSoup
- 4. adım — Bellek gösteriliyor: 128k token ile 112 sayfalık PDF özeti — araçlar: MiniCPM5
- 5. adım — Skor gösteriliyor: 1B sınıfı modellerle kıyas tablosu — araçlar: MiniCPM5, Qwen2.5-1.5B, Phi-3-mini, Gemma-2B, Llama-3.2-1B, SmolLM2-1.7B, MobileLLM-1.4B, TinyLlama-1.1B
- 6. adım — Kurulum: pip ile Transformers ve torch kurulumu, isteğe bağlı vLLM — araçlar: pip, Transformers, PyTorch, vLLM
- 7. adım — Modeli Transformers ile yükleyip sohbet üretme kodu gösteriliyor — araçlar: Transformers, PyTorch, Hugging Face
- 8. adım — Alternatif olarak vllm serve ile sunma ve SGLang anılıyor — araçlar: vLLM, SGLang
- 9. adım — Kapanış: takip çağrısı — araçlar: yok
## Promptlar
- Telefonda yerel model ile kod özetleme — Kullanıcı modelden bir kodu özetlemesini ve ne yaptığını açıklamasını istiyor (web kazıyıcı Python betiği örneği).
- 128K bağlamla uzun belge özetleme — Kullanıcı ai_research_paper.pdf (112 sayfa) dosyasını okumasını ve ana bulgularla ayrıntılı özet vermesini istiyor.
