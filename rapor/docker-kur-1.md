# docker-kur-1 — DURDU (yönetici yetkisi yok)
- PARÇA 1: C: boş 140 GB (≥86 ✓) · RAM %84,4 · WSL yüklü değil (`wsl --status` → "Linux için Windows Alt Sistemi yüklü değil") · docker yok · .wslconfig yok.
- Engel: oturum yönetici değil (IsInRole(Administrator)=False). `wsl --install --no-distribution` ve Docker Desktop kurulumu UAC + büyük olasılıkla yeniden başlatma ister; UAC'ı arka planda onaylayamam (ekran kuralı).
- PARÇA 2-4 yapılmadı (kurulum yok → .wslconfig/STRIX anlamsız).
- ÖMER: yönetici PowerShell'de: `wsl --install --no-distribution` → makineyi yeniden başlat → `winget install Docker.DockerDesktop` → bana "docker-kur-1 devam" de.
- Devam planı: .wslconfig [wsl2] memory=3GB processors=2 swap=2GB, `wsl --shutdown`, boşta RAM ölç (>2.5GB → memory=2GB), sonra STRIX_LLM (var/yok boolean) + tools/strix_yerel.py.
