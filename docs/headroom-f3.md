# Headroom F3 (27 Eki)
Önce (ölçüldü): CLI/MCP kopyası `~/.local/bin/headroom` 0.37.0 (uv tool `headroom-ai[all]`); masaüstü/proxy 0.39.0; proxy süreci (python, port 6768) ~1415 MB; PyPI 0.42.0.
Kilit: `headroom mcp serve` (pid 12428 → uv python 1476 → 31344; üst süreç python `tools/ram/mcp_koprusu.py` zinciri) `headroom.exe`'yi tutuyor; kendi başlatmadığım süreç öldürülmedi.
Çözüm: `tools/headroom_guncelle.ps1` (kilit varsa ertelenir; yoksa `uv tool install "headroom-ai[all]==0.39.0" --force` + sürüm doğrulaması, başarıda görevi siler; günlük `.kos/kopru/headroom-guncelle.log`). Kayıt: HKCU Run `omer-headroom-guncelle` (oturum açılışında bir kez, başarıda kendini siler). Görev Zamanlayıcı `schtasks /sc onlogon` yönetici ister (Erişim engellendi), bu yüzden Run anahtarı.
Proxy RAM: ayar yüzeyi yok (launch-profile.json'da argüman yok; `--no-cache`/`--max-connections` yalnız elle `headroom proxy` ile). Değiştirilmedi.
Ölçüm komutu (önce/sonra): `headroom --version; Get-Process python | ? { $_.Path -like '*Headroom*' } | % { "{0} MB" -f [int]($_.WS/1MB) }`
