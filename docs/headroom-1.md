# HEADROOM-1 — headroom-ai güncelleme hazırlığı: DUR (13 Eki 2026)

Karar: onay betiği (onay/headroom_1_guncelle.py) YAZILMADI. Görev madde 3: kırıcı değişiklik var + planlanan yöntem proxy'ye uymuyor.

## İki ayrı kurulum
- Proxy (6768): `headroom-desktop.exe --autostart` (HKCU Run "Headroom", sürüm 0.9.30) → `headroom.exe proxy --port 6768 --no-http2 --no-rate-limit --log-messages`; çalışan PID 27472 (zincir 27432 → 27480 → 27472, başlangıç 13 Eki 10:21). Runtime kendi kendine yeten venv: `%LOCALAPPDATA%\Headroom\headroom\runtime\venv`, bootstrap-receipt `managedBy: Headroom`; headroom-ai **0.39.0** (/health "version":"0.39.0").
- uv aracı: `~/.local/bin/headroom` = headroom-ai **0.37.0** (`uv tool install --python 3.13 "headroom-ai[all]"`). Kullananlar: headroom eklenti kancaları (`headroom init hook ensure`, SessionStart/PreToolUse) ve `headroom mcp serve` (CC oturumları + 47800 paylaşım merkezi alt süreci; ölçüm anında 3 süreç ağacı).
- `uv tool upgrade headroom-ai` proxy venv'ine DOKUNMAZ; IG-41-KUR'daki "proxy venv'i bozulur" kaygısı yersizdi. Proxy'yi güncellemenin yolu masaüstü uygulamasının kendi güncelleyicisi (log'da 0.9.40 görünüyor; runtime yükseltmesini `last_runtime_upgrade_failure` ile kendisi izliyor). Yönetilen venv'e elle pip yapmak yöneticiyi atlar.

## Sürümler / kırıcı değişiklik
- PyPI son: 0.40.0 (6 Eki). Arada 0.38.0, 0.39.0, 0.39.1.
- v0.40.0 "⚠ BREAKING CHANGES": (1) proxy HEADROOM_LICENSE okur, kullanım raporlaması opt-in olur; (2) `crewai` extra'sı kaldırıldı (chromadb lockfile'dan çıktı) — uv aracı `[all]` ile kurulu.
- 0.38.0–0.39.1 notlarında kırıcı satır yok; proxy bayrakları (--port/--no-http2/--no-rate-limit/--log-messages) için kaldırma/yeniden adlandırma görülmedi.

## Ortam değişkeni ADLARI (değer yazılmadı)
- headroom MCP: `type http`, url 127.0.0.1:47800, env yok. Masaüstü uygulaması `~/.bashrc` ve `~/.bash_profile`'ı yönetiyor (client-setup.json managedShellFiles). 0.40.0'la gelen yeni ad: HEADROOM_LICENSE.

## Seçenekler (karar Ömer'in)
1. uv aracını 0.39.1'e sabitle (kırıcı değişiklik yok): `uv tool install --force --python 3.13 "headroom-ai[all]==0.39.1"`; açık `headroom mcp serve` süreçleri exe'yi kilitler → tüm CC oturumları ve 47800 merkezinin headroom alt süreci kapalıyken yapılmalı; proxy durdurulmaz.
2. Proxy için headroom-desktop güncellemesi (0.9.30 → 0.9.40) masaüstü arayüzünden; runtime sürümünü uygulama seçer.
3. 0.40.0'a geçiş: HEADROOM_LICENSE davranışı ve [all] içeriği ayrıca doğrulanmalı.
