# dil — 26 benzersiz kayıt

**Amaç:** Programlama diline/çalışma zamanına özel uzman ajanlar: Go, Python, Rust (Actix), TypeScript, JVM dilleri, fonksiyonel diller, Bash/C ile CLI, API sözleşmesi, regex, derleyici tasarımı.

**İç yapı:** Tümü [ajan], dil-<dil/konu>; dil başına yazım/inceleme, bazıları profilleme (go-pprof, python-profil) ve eşzamanlılık (go-eszamanlilik, asyncio) alt uzmanlığı.

## En güçlü parçalar
- `dil-ts-tip-daraltma` — Narrowing, discriminated union, any yerine unknown, exhaustive check ile TS güvenliği.
- `dil-go-eszamanlilik` — Goroutine sızıntısı, kanal, context iptali, yarış; yalnız belirti verilse de çalışır.
- `dil-asyncio` — Coroutine içinde bloklayan çağrı, unutulan task, iptal ve timeout hataları.
- `dil-regex-denetci` — Felaket geri izleme, eksik çapa, Unicode sorunları; yapıştırılan kalıp yeterli.
- `dil-bash-betik` — Strict mode, güvenli tırnaklama, cleanup trap ve CI statik kontrolüyle Bash sertleştirme.
- `dil-python-profil` — cProfile, py-spy ve bellek araçlarıyla yavaş işlerde sıcak nokta düzeltme.
- `dil-openapi-sozlesme` — Yeniden kullanılır şema, hata, sürümleme ile contract-first OpenAPI 3.
- `dil-uv-proje` — uv ile lockfile, Python sürümü, araç kurulumu ve CI önbelleği.
- `dil-nodejs` — Event loop bloklanması, async hata, stream ve bağımlılık riski.
- `dil-cli-araci` — Alt komut, bayrak, çıkış kodu ve yardım çıktısı tasarımı.

## Birlikte kullanım
- dil-go + dil-go-eszamanlilik + dil-go-pprof: yazım, eşzamanlılık, profilleme.
- dil-python-tip-guvenligi + dil-asyncio + dil-python-profil: Python kalite hattı.
- dil-openapi-sozlesme + dil-graphql: API sözleşme tasarımında iki model.
- dil-cli-araci + dil-bash-betik + dil-yapilandirma: komut satırı aracı ve ortam yapılandırması.

## Tuzaklar
- Ajanlar dil başına; aynı projede birden çok dil için birden çok ajan gerekir.
- dil-flask/dil-nodejs/dil-actix-web sunucu düzeltir, be ailesiyle kapsam örtüşebilir.
- dil-yapilandirma sır ayrımı önerir ama sır yönetim aracı değil; araç katalog metninde belirtilmemiş.

## Üyeler
- ajan (26): dil-actix-web, dil-asyncio, dil-bash-betik, dil-c-sistem, dil-cli-araci, dil-clojure, dil-derleyici-tasarimi, dil-flask, dil-go, dil-go-eszamanlilik, dil-go-pprof, dil-graphql, dil-haskell, dil-java-modern, dil-nodejs, dil-ocaml, dil-openapi-sozlesme, dil-python-profil, dil-python-tip-guvenligi, dil-regex-denetci, dil-ruby-metaprog, dil-scala, dil-ts-tip-daraltma, dil-uv-proje, dil-websocket, dil-yapilandirma
