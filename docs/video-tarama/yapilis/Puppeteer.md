# Puppeteer

- tür: kutuphane · durum: KURULU-KANITSIZ · videolar: DbOI3-zOv0J,DdBlwBIFGvC,Ddw2K7_CtrK,De2kpfnCFeH,De3VNywBzBu,De6jpQyDAhc,De8XjQVhbzW,De9D5Z9kx9a,DeXAMs2Eqgh,Deg346vDphY,DeuOHMjFGBI,DeuZ4BnhCqA,DeupYVwjRiu,Deyws1vlXq5,Dez9ehLmdNZ
- bizde: docs/envanter/envanter.tsv; site:.kos\kopru\kaynak-dizin\dizin.tsv; kaynak-kutuphane/site:docs/kaynak-kutuphane/site/pptr.dev.md; yontem:.kos\kopru\kaynak-dizin\dizin.tsv; ~/.claude.json:docs\katalog\yetenek.tsv

## Özellikler
- Alıntıda Puppeteer, Lightpanda'nın CDP (port 9222) üzerinden bağlandığı istemci olarak geçiyor (alıntı: 'Works with Playwright, Puppeteer & Chromedp')
- Lightpanda: Zig ile sıfırdan yazılmış, Chromium fork değil (alıntı)
- Chrome'dan 11x hızlı, 9x az bellek iddiası (alıntı, ölçüm yöntemi yok)
- Tek satır Docker kurulumu (alıntı)
- Windows'ta native binary yok, WSL gerekiyor (alıntı)
- AGPL-3.0 lisans, 11.8k yıldız (alıntı)

## Videoda yapılış
Alıntıda Linux/macOS'ta release binary'sini curl ile indirip chmod a+x ile çalıştırma, Docker imajı ve Windows'ta WSL içinde kurup istemciyi localhost:9222'ye bağlama anlatılıyor. Puppeteer'ın kendi kurulum veya kod adımı alıntıda yok.

## Bizdeki karşılık ve fark
Kayıtlı yerler: docs/envanter/envanter.tsv; .kos/kopru/kaynak-dizin/dizin.tsv; docs/kaynak-kutuphane/site/pptr.dev.md; ~/.claude.json, docs/katalog/yetenek.tsv. Dosya içerikleri okunmadı. Alıntılar Puppeteer'ı değil Lightpanda'yı anlatıyor; fark belirlenemedi.

## Al
Chromium'a bağımlı olmayan hafif tarayıcının CDP üzerinden Puppeteer'a bağlanması. Hız ve bellek farkı kendi ölçümümüzle doğrulanırsa değerlendirilebilir.

## At
11x ve 9x iddiaları ölçüm yöntemi olmadan verilmiş. AGPL-3.0 lisansı. Windows'ta native binary yok (WSL gerekli). Linux binary'si glibc gerektiriyor; glibc olmayan imajlarda çalışmıyor (alıntı).
