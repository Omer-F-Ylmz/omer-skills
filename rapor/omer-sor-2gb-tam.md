# 2 GB üstü kalemler — birleşik liste (7 Kas 17:45)
Kaynaklar: rapor/omer-sor-2gb.md (kur-hepsi-1), rapor/gurultu-kur-1.md, rapor/omer-sor-1107.md. Ömer her satıra EVET/HAYIR der; EVET olanlar ayrı betikle kurulur. 2 GB altı her şey kur_hepsi.ps1 içinde, soru yok.

| # | ad | boyut | kaynak | ne işe yarar | not |
|---|---|---|---|---|---|
| 1 | clef | 51,2 GiB | HF Cloudflare/clef (Apache-2.0) | model ağırlığı | GitHub'da kod yok, yalnız ağırlık |
| 2 | clef-flash | 17,8 GiB | HF Cloudflare/clef-flash (Apache-2.0) | clef'in hızlı sürümü | |
| 3 | MegaTTS3 | 3,98 GiB | HF ByteDance/MegaTTS3 (Apache-2.0) | açık ağırlıklı TTS, Seed-TTS muadili | ses turu adayı |
| 4 | laya | 2,2 GiB | HF convaiinnovations/laya (Apache-2.0) | model ağırlığı | |
| 5 | ClickHouse | 14,9 GB | clickhouse | analitik veritabanı | önceden HARİÇ/İLERİDE |
| 6 | Clawdbot | 13 GB | — | ajan uygulaması | önceden HARİÇ/İLERİDE |
| 7 | twenty | 2,5 GB | twentyhq/twenty | açık kaynak CRM | önceden HARİÇ/İLERİDE |
| 8 | Stable Diffusion Forge | repo 0,05 GB + model ağırlıkları >2 GB | lllyasviel/stable-diffusion-webui-forge (AGPL-3.0) | SD görsel üretim arayüzü | ComfyUI zaten var |
| 9 | CUDA / CUDA 12.8 | >2 GB | winget Nvidia.CUDA (NVIDIA EULA) | GPU derleme araç seti | iki satır tek kalem |
| 10 | DaVinci Resolve | >2 GB | Blackmagic (ticari, ücretsiz sürüm) | video kurgu | |
| 11 | xelatex (MiKTeX) | >2 GB olası | winget MiKTeX.MiKTeX (doğrulanmadı) | LaTeX/PDF dizgi | |
| 12 | Swift | toolchain ölçülemedi (repo 1,35 GB) | swiftlang/swift (Apache-2.0) | Swift dili, Windows araç zinciri | VS 2022 zaten kurulu, ek bağımlılık yok |
| 13 | Chromium (kaynak) | 64,9 GB | chromium/chromium (BSD-3) | tarayıcı kaynak ağacı | Chrome kurulu; kaynak yalnız derleme için |
| 14 | WebKit (kaynak) | 12,7 GB | WebKit/WebKit | tarayıcı motoru kaynağı | kurulabilir ürün değil, kaynak |

Listeden çıkarılan: MSVC Build Tools — VS 2022 Community + VC araçları zaten kurulu (link.exe 14.44 doğrulandı, 7 Kas 17:40).
