# Docker Compose

- tür: arac · durum: KURULU-KANITSIZ · videolar: 7tInlFRcTEQ,DZ3PUfYlK6z,DbVGcvfgUsD,DcI8a69AEJq,DcXvWV0z077,Dcd3eY1iOMA,Dd0ZDPRjIWA,Dd4UPS4gD8Z,DdKcLiJgczB,DdRd8uijAER,DdSwfSNgFiJ,DdVWXArCa_T,DdgKOaPDXwD,DdgfJ_mEvPl,DeDrlhWk7Q5,DePQ2O3ElPy,DeXK9x7jQfb,DeYASC1j8Zm,Deau8oUO4i1,DefTRngy4bF,DeloFdYmRuI,DeubpyGFEVp
- bizde: kurulu-tara.json PATH:C:\Program Files\Docker\Docker\resources\bin

## Özellikler
- n8n'i Docker container olarak, Docker Compose seçenekleriyle çalıştırma (alıntı: n8n self-host)
- Docker Compose dosyalarını olduğu gibi deploy etme (alıntı: Openship)
- Otomatik Let's Encrypt SSL, sınırsız domain, zamanlanmış yedekler, canlı build logları (alıntı: Openship)
- Standart Docker container'ları olduğu için sağlayıcılar arasında taşınabilirlik (alıntı: Openship)
- Podman rootless modunda socket'in çalışıyor olması gerekir (alıntı)

## Videoda yapılış
Ön koşul olarak Docker Desktop kurulur. Alıntıda 'git clone ...; cd openA; docker compose -f docker-compose.dev.yml up' (OCR bozuk) ve panel adresi http://localhost:2785 geçiyor.

## Bizdeki karşılık ve fark
BIZDE: kurulu-tara.json içinde PATH kaydı: C:\\Program Files\\Docker\\Docker\\resources\\bin. Kurulu olduğu kanıtlanmamış; BIZDE alanında compose kullanım kaydı verilmemiş.

## Al
Tek compose dosyasıyla servis ayağa kaldırma ve standart container taşınabilirliği

## At
Docker Desktop ön koşulu; Podman için socket gereksinimi; Openship'in 'sıfır yapılandırma' iddiası alıntıda doğrulanmamış
