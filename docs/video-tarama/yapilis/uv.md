# uv

- tür: arac · durum: KURULMADI-SIRADA · videolar: DXpKuMtj1f5,DcXvWV0z077,Dd0ZDPRjIWA,DdA-QjwAMh_,DdBQrn-jV8v,DdEmizXglN9,DdjEKF4jDso,Ddt16ilkRGB,De-ozuJiHjm,De928DMsmEj,DeYASC1j8Zm,DefTRngy4bF,DelHsxgBq13,DeroxUoiAK_,DerpKungtI1,DesTevqtfX9,DeuUwuSk7da,DevVTopkRwf,DeysPEmgd5g,DezhgNTD5P4,DfA-nQWiPKz,DfE2anKmQGQ
- bizde: yok

## Özellikler
- 'uv sync' ile bağımlılık kurulumu (alıntıda yerel geliştirme komutu)
- Yerel geliştirmede Python 3.11+ ve uv gerekir; Docker dışı çalıştırmada Python 3.11-3.12, uv ve ffmpeg gerekir (alıntı)
- Repolarda uv.lock ve pyproject.toml bulunur (TradingAgents alıntısı)
- Repo Postgres, Redis, Celery veya Ray gerektirmez; durum SQLite ve dosya sisteminde tutulur (alıntı)

## Videoda yapılış
Repo klonlanır; 'uv sync' çalıştırılır; .env.example .env olarak kopyalanır; REST API başlatılır (komut alıntıda kesik). Docker tarafında 'docker compose -f docker-compose.release.yml up -d' kullanılır.

## Bizdeki karşılık ve fark
BIZDE: yok. Envanterde karşılığı verilmemiş; durum KURULMADI-SIRADA.

## Al
'uv sync' ile tek komutta bağımlılık kurulumu

## At
Alıntıda uv'ye dair kötü yan yok; yerel kurulumda Python sürümü ve ffmpeg ön koşulu var
