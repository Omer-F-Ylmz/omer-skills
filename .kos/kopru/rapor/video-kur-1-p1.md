# VIDEO-KUR-1 PARÇA 1, sınıflama (kurulum yok)

- 808 aday satırı → 652 ham terim → **223 tekil aday** (URL'ler repo/alan adına indirgendi). Sonuç: `video-kur-1-p1.tsv`
- Karar: **kurulu 73** (envanter kanıtlı) · **KUR 98** · **KUR-sonra 14** (VS Code önkoşullu eklentiler + OmniCopilot/Cline) · **gürültü 37** (genel terim/kırık metin) · **atla-güvenlik 1** (`1inkedin-agent` typosquat görünümlü).
- Envanter: ~/.claude skill+eklenti, MCP, npm -g, pip, uv tool, StartApps, winget, PATH ikilileri (3867 ad); `kurulu` satırlarının kanıt adı envanterde doğrulandı (0 eksik).
- Ücretsiz modeller (cloudflare llama, mistral) sınıflamada bozuk/uydurma çıktı verdi (sekme yerine "TAB>", anlamsız gerekçe) → doğrulanamayan çıktı atıldı; sınıflama Claude'da, kural+envanter ile yapıldı.
- Disk: C: boş 146 GB (≥80 kapısı geçti).

## PARÇA 2 kurulum sırası önerisi
1. Güvenlik kapısı: her dış repo için `gitleaks` + `semgrep` (kurulu), kod çalıştıran/yüklenen için `strix`/agentshield; `nvidia/skillspector`, `affaan-m/ecc`, `christopherkahler/base`, `zk/claude-mods` ilk taranır.
2. Düşük risk, yüksek getiri: skill/plugin/CLI (`code-modernization`, `lua-lsp`, `nvidia/skillspector`, `vercel` CLI, `router-for-me/cliproxyapi`, `freeflow`, `9router`, `ecc`).
3. Kütüphaneler proje başı (crawlee, impit, litellm, tailwind, framer-motion): global kurulum yok, ihtiyaç doğunca.
4. Masaüstü uygulamalar (winget): stirling-pdf, kdenlive, insomnia, msty, meetily, actual; AGPL olanlar (vaultwarden, documenso, dub, immich) yalnız self-host, kodları projeye gömülmez; immich/kali Docker/WSL + disk ister, sona.
5. API-servis/SaaS (hesap gerekir; ücretli → bütçe tavanı yazılmadan çağrı yok): nvidia-nim, mistral (ücretsiz katman) önce; higgsfield, photoroom, serpapi, SEO SaaS'lar en son.
6. VS Code: önce VS Code kurulumu kararı; MS lisanslı eklentiler yalnız resmî VS Code'da → işlevsel muadil (Visual Studio 2022 kurulu).
7. Site/dizinler (land-book, muz.li, skillry, claudepluginhub, banger.show): kurulum değil, `docs/site-inceleme` / katalog kaynağına eklenir.
- Lisans notu: remotion (≤3 kişi ücretsiz), cursor/postman/highlight/augment kapalı kaynak; `calesthio/OpenMontage` ve rivecn lisansı okunmadan kurulmaz.

## Bekleyen 135 link için derin izleme sırası → `video-kur-1-p1-bekleyen.tsv`
1. ig-reel 2 → 2. yt-shorts 1 indirilebilir → 3. ig-post 122 indirilebilir (log izi yok; ilk 1-2 deneme sonucu gelmeden tüm partiyi başlatma, bkz. ig-karusel-2.md: /p/ sayfasında DOM'da video=0).
- Ayrı liste (indirilemeyen): yt-shorts 6 silinmiş/özel · ig-post 2 foto/karusel (kare+OCR yolu) · 1 giriş duvarı (çerez) · 1 diğer hata.
