# CUDA

- tür: arac · durum: KURULMADI-SIRADA · videolar: DZ5CcdsjRHW,DbvGorIgM4q,DcNOMyTCXmO,DcjEHTvyYBS,Dd1jV3AgDiG,DdnQtgBCUZu,De2TJpwjJWX,DeMgL8IDfD5,De_3H65gDSN,DefTRngy4bF,Deidr7QOet0,Dew-EGglUpE,DfAbIv5C8OH,DfAq1txAF-p,DfBSFBwCikQ,DfDQXqrk2bt
- bizde: yok

## Özellikler
- llama.cpp'yi NVIDIA GPU için CUDA desteğiyle derleme
- Mac'te Metal desteği varsayılan olarak açık
- Hugging Face CLI ile model ağırlıklarını indirme
- Unsloth'un 2-bit dinamik kuantizasyonu: videoya göre 1.51 TB modeli 239 GB'a indiriyor, %82 doğruluk korunduğu iddia ediliyor

## Videoda yapılış
1) git clone https://github.com/ggml-org/llama.cpp  2) cmake llama.cpp -B llama.cpp/build -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON  3) cmake --build llama.cpp/build --config Release -j  (Mac kullanıcıları için -DGGML_CUDA=OFF)  4) pip install huggingface_hub, ardından hf download ile Unsloth 2-bit kuantizasyonunu indirme. Videoda kuantizasyona göre toplam sistem RAM'i: 1-bit 223 GB, 2-bit 245 GB, 4-bit 475 GB, 8-bit 810 GB.

## Bizdeki karşılık ve fark
yok

## Al
llama.cpp'yi kendi donanımınızda CUDA ile derleyip büyük modeli yerelde çalıştırma yolu

## At
Videoya göre bu iş laptop için uygun değil; 2-bit için bile yaklaşık 245 GB sistem RAM'i gerekiyor. İndirme çok uzun sürüyor (videoda 'bir kahve al' deniyor).
