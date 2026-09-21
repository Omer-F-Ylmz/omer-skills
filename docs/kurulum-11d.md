# KURULUM-11d — Desktop MCP ortam sorunu + 11c kalanı

21 Eyl 2026. Taban: 7e8ed97.

## K1 — kök neden, tahmin değil: ikiliden okundu

### Canlı kurulum tek ve MSIX (11e yan notu TERS çıktı)

- Tek Desktop: `C:\Program Files\WindowsApps\Claude_2.2553.1.0_x64__pzs8sxrjxfjjc\app\Claude.exe`
- **Canlı config:** `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json`
  — `%APPDATA%\Claude` **hiç yok**.
- **Canlı log:** `%LOCALAPPDATA%\Claude\logs`
- `…\LocalCache\Roaming\Claude\logs` (mcp.log 0 B / 18 Ağu) **kalıntı**.
- ⇒ İkinci kurulum yok. 11e kalemi olarak yazılacak not yanlış yöndeydi: MSIX olan
  **asıl** kurulum, eski Roaming log klasörü kalıntı.

### Beyaz liste — brave-search'ün kök nedeni

`app.asar` ofset **3899305** (ayrıca 16928127), MCP TypeScript SDK'nın
`DEFAULT_INHERITED_ENV_VARS` listesi birebir:

```
APPDATA HOMEDRIVE HOMEPATH LOCALAPPDATA PATH PROCESSOR_ARCHITECTURE
SYSTEMDRIVE SYSTEMROOT TEMP USERNAME USERPROFILE PROGRAMFILES
```

Özel anahtarlar (`BRAVE_API_KEY`, `STITCH_API_KEY`, `CONTEXT7_API_KEY`) sunucu
sürecine **hiç ulaşmıyor**. `cmd /c` sarmalayıcısı çözmez: cmd de aynı 12
değişkenle başlar, `%VAR%` genişlemez.

**11b/11c'deki kuru testler bu yüzden yanıltıcıydı** — `mcp_kurutest.py` tam
`os.environ` ile koşuyordu, yani Desktop'ın çalıştırdığı programı değil başka bir
programı test ediyordu. `--desktop-env` bayrağı bu boşluğu kapatır.

### Üreme testi (K1a)

`python tools/mcp_kurutest.py --desktop-env` — 15 sunucunun 15'i koşturuldu:

| Sonuç | Sunucu |
|---|---|
| OK (13) | binlog 44 · claude-mem 15 · code-review 12 · context7 2 · headroom 3 · mcp-fetch 1 · mcp-filesystem 14 · mcp-git 12 · mcp-memory 9 · mcp-sequential-thinking 1 · mcp-time 2 · playwright 25 · **puppeteer 8** |
| INIT-YOK (2) | **brave-search** — "A Brave API key is required…" · **stitch** — "StitchProxy requires an API key (STITCH_API_KEY)…" |

Düşen iki sunucu, tam olarak anahtar isteyen iki sunucu. Model doğrulandı.

### puppeteer: model bu sunucuyu AÇIKLAMIYOR — ayrı kök neden

puppeteer kısıtlı ortamda sorunsuz: initialize + 8 araç + **gerçek `navigate`**
(`https://example.com`, Status 200), stderr 0 bayt, 3.9 s.

Desktop'ta düşmesinin sebebi ortam değil **eşzamanlılık**: Desktop sunucuyu iki
tüketici için başlatıyor (sohbet + "Cowork and Code sessions" shared-pool).
İki örnek aynı anda koşturulunca `initialize` **26–28 s** sürüyor (tek örnekte
3.9 s) — `npx -y` paket çözümlemesinin yarışması. Desktop açılış zaman aşımı
~24 s'de süreci öldürüyor; log'daki 09:06:46 → 09:07:10 penceresi tam bu.

Düzeltme: `"startupTimeoutSec": 120` (ikilide desteklenen stdio alanı).

### envHelper — belgesiz ama ürünün kendi mekanizması

`app.asar` ofset 3045914 / 4537803, `[custom3p-mcp-env]`. Ürünün kendi metni:

> "Absolute path to an executable that prints a single JSON object of environment
> variables to stdout… The app runs it before spawning the server and merges the
> result over `env` (helper wins on conflict). **Use it to pull secrets from a
> secrets manager instead of storing them inline in `env`.**"

| Kalem | Değer |
|---|---|
| Alanlar | `envHelper` (mutlak yol) · `envHelperTtlSec` (varsayılan 300 s) |
| Sürüm | `availableInVersion 1.21459.0` · kurulu 2.2553.1.0 |
| `.cmd` başlatma | `cmd.exe /d /s /c` · `.ps1` → `powershell -NoProfile -NonInteractive -ExecutionPolicy Bypass -File` |
| Helper'ın ortamı | `{...process.env}` — beyaz liste helper'a uygulanmaz |
| Çıktı | stdout'ta tek JSON · ad `^[A-Za-z_][A-Za-z0-9_]*$` · ≤64 değişken · değer ≤32768 |
| Sınırlar | 30 s · 256 KB · exit 0 ve boş olmayan stdout zorunlu |
| Hata | Helper düşerse **sunucu başlamaz** |
| Argüman | **YOK** — helper'a argüman da sunucu adı da geçilmiyor (`envHelperArgs` alanı yok) |

**UYARI:** Bu alan belgesiz; app.asar'dan çıkarıldı. Desktop güncellemesinde
yeniden doğrula.

### Yazılan config değişiklikleri

Yedek: `claude_desktop_config.json.bak11d`. JSON doğrulandı. 15 → **14 sunucu**.

| Sunucu | Değişiklik |
|---|---|
| brave-search | `envHelper` + `envHelperTtlSec: 300` |
| stitch | `envHelper` + `envHelperTtlSec: 300` |
| puppeteer | `startupTimeoutSec: 120` |
| context7 | **kaldırıldı** — hesap bağlayıcısı `context7-c1492263` var (çift kayıt) |

CC `~/.claude.json` mcpServers: 17 adet, sha256 değişmedi (öncesi = sonrası).
*Not: 11c'deki `874d34b9…` özeti başka bir yöntemle alınmış; burada öncesi/sonrası
aynı yöntemle karşılaştırıldı.*

### Başlatıcı: tools/mcp-launch/mcp-env.cmd

Tek betik, `BRAVE_API_KEY` + `STITCH_API_KEY` adlarını HKCU'dan okur, stdout'a tek
JSON nesnesi basar. Değer başka hiçbir yere yazılmaz. **Anahtar hijyeni kuralının
tek istisnası bu HKCU okumasıdır.**

Anahtar **helper her çalıştığında** okunur (TTL 300 s) → yenilenen anahtar bir
sonraki Desktop açılışında kendiliğinden geçer, config'e dokunmaya gerek yok.

Bilinen sınırlar: değerde `"` ya da ters bölü olursa JSON bozulur; ünlem karakteri
gecikmeli genişletmede yenir. İki anahtar da ASCII ve bu karakterleri içermiyor
(boru testiyle doğrulandı).

**Yan etki, bilinerek kabul:** helper argüman almadığı için tek betik iki anahtarı
da döndürür; brave'in süreci `STITCH_API_KEY`'i de alır. İkisi de aynı kullanıcının
anahtarı, config'e ve log'a düşmüyor.

### Kabul durumu

| Ölçüt | Durum |
|---|---|
| `--desktop-env` brave initialize + tools/list | ⏳ Desktop yeniden başlatması bekleniyor |
| `--desktop-env` puppeteer initialize + tools/list + navigate | ✅ 8 araç, navigate Status 200 |
| Config'te anahtar değeri yok | ✅ gitleaks 0 bulgu |
| `tools/mcp-launch` değer içermiyor | ✅ gitleaks 0 bulgu |

## K2b — gitleaks (a)-aday, rtk (b)

| Kontrol | gitleaks 8.30.1 |
|---|---|
| ELF | ELF64 LSB, `e_machine 0x3e` (x86-64), `e_type EXEC` |
| Bağlama | **statik** — dinamik yükleyici izi yok, GLIBC_ sembolü yok → sandbox glibc'sinden bağımsız |
| sha256 | release `gitleaks_8.30.1_checksums.txt` ile **eşleşti** |
| Boyut | açık 20.9 MB (limit 30) · zip 7.7 MB |
| `skill_denetim.py` | 0 hata |

Paket: `dist/yukle-11d/replace/gitleaks-desktop.zip` — `bin/gitleaks` + SKILL.md.
SKILL.md ikiliyi `/home/claude` altına kopyalatıp `chmod +x` yaptırır (sandbox 644 yazar).

**Yürütme kanıtı claude.ai'de bekliyor.** Yükleme sonrası yeni chat'te "skill
kontrol" → `gitleaks version`. Geçmezse karar (b)'ye döner. **(a) o kanıt gelene
kadar kesin değildir.**

**rtk → (b).** Yerel `rtk.exe` 0.49.0 bir Windows PE; `--help` çıktısında kaynak
URL yok, uv/pip kaydı yok → public linux-amd64 release tespit edilemedi.

`duman_claudeai.py` kapısı **koşulmadı**: bu makinede Linux çalıştırma ortamı yok
(WSL dağıtımı kurulu değil, Docker yok). Kapı bash bloklarını yerel Git Bash'te
koşturuyor, ELF çalıştıramaz.

## K7b — tools/redakte-transkript.ps1

gitleaks JSON raporundaki **eşleşme dizesine** göre maskeler, HKCU'daki güncel
değere göre değil (anahtar yenilenirse eşleşme kaybolur, eski transkriptteki eski
değer maskesiz kalırdı). Yedek `.bak11d`, ekrana yalnız dosya adı + sayı.

Kuru çalışma: **6 eşleşme, 1 dosya** (kural: `github-oauth`).
CC yalnız `-WhatIf` ile koştu; gerçek koşu Ömer'de.

## Sapmalar

1. K1b yöntemi: tarif `.cmd` sarmalayıcı istiyordu; ikilide yerleşik `envHelper`
   bulundu, Ömer "önce envHelper, düşerse .cmd" dedi. Sarmalayıcı yedeği gerekmedi.
2. "Tek betik, yalnız istenen adları döndürür" — adlar kürlendi, ama sunucu başına
   filtreleme imkânsız (helper argüman almıyor).
3. puppeteer'ın kök nedeni ortam değil eşzamanlılık; tarifteki model bu sunucu için
   yanlıştı.
4. K2b kapısı koşulmadı (yerel Linux yok); statik doğrulama + claude.ai kanıtı.
5. `desktop-eslesme.md:63-68` ("Miras" + "%VAR% genişletmesi") tümden yanlıştı.
6. K5 kalemleri (K5b/c/e/g) bütçe dolduğu için yapılmadı — 11e'ye devreder.
