# llama.cpp

- tür: arac · durum: KURULMADI-SIRADA · videolar: DZ5CcdsjRHW,DavMnS4M1ql,Dd1jV3AgDiG,Dd4UPS4gD8Z,DdRd8uijAER,DeD8sC4gqrO,DehErZxDfkE,DekBdvcCXgG,DerqV7PEkKn,DeyxY_PS4JW
- bizde: yok

## Özellikler
- Videoda GLM-5.2 (744B parametre, 1M bağlam penceresi) yerelde çalıştırılıyor; Mac Studio örneği var
- Toplam sistem RAM gereksinimi: 1-bit 223GB, 2-bit 245GB, 4-bit 475GB, 8-bit 810GB
- Mac'te Metal desteği varsayılan açık, ek bayrak gerekmiyor; NVIDIA için CUDA derleme bayrağı var
- ProjectN.O.M.A, Ollama yerine OpenAI API uyumlu llama.cpp'yi kullanabiliyor (DavMnS4M1ql)

## Videoda yapılış
git clone https://github.com/ggml-org/llama.cpp; cmake llama.cpp -B llama.cpp/build -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON; cmake --build llama.cpp/build --co... (transkript burada kesik; model indirme ve çalıştırma adımları yok)

## Bizdeki karşılık ve fark
Envanterde karşılığı yok (BIZDE: yok).

## Al
Modeli kendi donanımında yerelde çalıştırma; Mac'te Metal varsayılan açık

## At
Donanım gereksinimi çok yüksek: en düşük 1-bit için 223GB RAM. Videonun kendisi 'laptop projesi değil' diyor
