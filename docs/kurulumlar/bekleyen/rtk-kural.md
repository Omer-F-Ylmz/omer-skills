# ONAY rtk-kural (21a K4) — KOŞULMAZ, Ömer onaylar

Repo filtresi `.rtk/filters.toml` (cc-kopru-suit) yazıldı ve test edildi (tests/test_21a.py). RTK proje filtrelerini yalnızca güven verildikten sonra uygular. `rtk verify` şu an "untrusted project filters skipped" diyor. Güven kaydı kullanıcı deposuna yazıldığı için bu adım onaya bırakıldı.

```powershell
Set-Location C:\Projeler\omer-skills
rtk trust --yes                                 # .rtk/filters.toml'a güven
rtk verify --filter cc-kopru-suit               # satır içi test: 1/1
# geri alma
rtk untrust
```

## Kullanıcı filters.toml önerisi (repo dışı komutlar; %APPDATA%\rtk\filters.toml)
İlk 10 listesinde süzülmeden geçenler `rtk proxy` (125×, ~91k tok) ve `graphify query` (34×, ~37k tok). `rtk proxy` bilerek süzülmeyen çıktıdır, kural yazılmaz. graphify için öneri (hata satırlarına dokunmaz):
```toml
[filters.graphify-query]
description = "graphify query: boş satır süz, 120 satır tavan"
match_command = "^graphify\\s+(query|path|explain)\\b"
strip_lines_matching = ["^\\s*$"]
max_lines = 120
```
