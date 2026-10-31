# Kubernetes

- tür: arac · durum: KURULMADI-SIRADA · videolar: DZ3PUfYlK6z,DcBuc3XuVif,DcDfnzsM2wL,DcNGpmXOR42,Dd5YSAqFaHd,DdRd0SNkrW-,DdSaxEKjhg_,DdVVF0_DcmB,Ddt16ilkRGB,De1oJR3Ea4F,De68AiWSiMp,DeChw05s6ID,DePQ2O3ElPy,DeQmfMeCIAu,DeUMgFpkz2y,DefTRngy4bF,DezcE_BMmrJ
- bizde: yok

## Özellikler
- Docker + Kubernetes + gVisor/Kata/Firecracker ile izolasyon desteği (OpenSandbox tanıtımı, DcBuc3XuVif)
- Kubernetes-ready probe'lar (DZ3PUfYlK6z)

## Videoda yapılış
Docker yerine Podman rootless: systemctl --user start podman.socket; systemctl --user enable podman.socket; export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock; ardından repo klonlanıp docker-compose ile başlatılıyor; dashboard, API ve docs localhost üzerinde açılıyor. Transkript bozuk; compose dosya adı ve port tam okunamadı.

## Bizdeki karşılık ve fark
yok

## Al
Rootless Podman için soket servisini etkinleştirip DOCKER_HOST ile bağlanma yöntemi

## At
Podman rootless kurulumunda soket servisi çalışır durumda olmalı; değilse bağlantı kurulamaz
