# Claude Desktop eşleşme belgesi · KURULUM-11 · 20 Eyl 2026

Kaynak: `claude mcp list` + `~/.claude.json` + `claude plugin list` + K3 kuru testi
(`tools/mcp_kurutest.py`, initialize + tools/list, Desktop kapalıyken CC tarafında).
Her hücre kanıta dayanır; kanıtı olmayan satır "doğrulanmadı" olarak işaretlidir.

Taban: CC'de 30 MCP sunucusu (nano-banana-2 kapsam dışı ama sayımda görünür).
Desktop config dalga öncesi 10 tanım, dalga sonrası **16** tanım.

## 1. Katman tablosu

| Yetenek | CC | Desktop Chat | Desktop Cowork | Desktop Code |
|---|---|---|---|---|
| Yerel stdio MCP (16 tanım) | ✅ 16/16 tools/list | ✅ config'te tanımlı | ⛔ VM yok | ⛔ VM yok |
| Uzak http MCP (hesap bağlayıcısı) | ✅ 6 bağlı | ✅ Connectors | ⛔ VM yok | ⛔ VM yok |
| Skill (sohbet) | ✅ | ✅ | ⛔ VM yok | ⛔ VM yok |
| Plugin komutu (`/ad`) | ✅ 53 komut | ⛔ Desktop plugin komutu çalıştırmaz | ⛔ | ⛔ |
| Subagent (161) | ✅ | ⛔ | ⛔ | ⛔ |
| Yerel CLI aracı (9) | ✅ | ⛔ sandbox'ta yerel makine yok | ⛔ | ⛔ |
| Hook / statusline | ✅ | ⛔ Desktop'ta karşılığı yok | ⛔ | ⛔ |

**Cowork/Code sütunlarının kanıtı** — `logs/cowork_vm_node.log`:
`[cleanupVMBundleIfUnsupported] yukonSilver not supported (status=unsupported)` ve
`[Bundle:status] rootfs.vhdx missing / vmlinuz missing / initrd missing`.
Cowork ve Code oturumları bu VM paketine bağlıdır; bu makinede paket yok.
Kaydın son satırı 20 Ağu tarihli → **Ömer'den ekran kanıtı istenir** (K3).

## 2. MCP tablosu

Kuru test: Desktop kapalıyken, gerçek Windows PATH'i ile, CC tarafında bağımsız çalıştırma.

| Ad | Desktop'ta kaynak | Komut | Anahtar kaynağı | Önkoşul | Araç | Sekme |
|---|---|---|---|---|---|---|
| headroom | config (**düzeltildi**) | `.local\bin\headroom.EXE mcp serve` | yok (env: HEADROOM_PROXY_URL) | 127.0.0.1:6767 ayakta | 3 | Chat |
| puppeteer | config (mevcut) | `cmd /c npx -y puppeteer-mcp-server@0.7.2` | yok (`startupTimeoutSec: 120` eklendi) | — | 8 | Chat |
| mcp-sequential-thinking | config (mevcut) | `cmd /c npx -y @modelcontextprotocol/server-sequential-thinking@0.6.2` | yok | — | 1 | Chat |
| mcp-memory | config (mevcut) | `cmd /c npx -y @modelcontextprotocol/server-memory@2026.8.31` | yok | — | 9 | Chat |
| mcp-filesystem | config (mevcut) | `cmd /c npx -y @modelcontextprotocol/server-filesystem@2026.8.31 C:/Users/pc/Desktop C:/Projeler` | yok | kökler CC ile aynı | 14 | Chat |
| mcp-fetch | config (mevcut) | `uvx mcp-server-fetch@2026.8.18` | yok | — | 1 | Chat |
| mcp-git | config (mevcut) | `uvx mcp-server-git@2026.8.18` | yok | — | 12 | Chat |
| mcp-time | config (mevcut) | `uvx mcp-server-time@2026.8.18` | yok | — | 2 | Chat |
| binlog | config (mevcut) | `dotnet dnx Microsoft.AITools.BinlogMcp --yes --prerelease` | yok | .NET SDK | 44 | Chat |
| playwright | config (mevcut) | `cmd /c npx -y @playwright/mcp@latest` | yok | — | 25 | Chat |
| brave-search | config (**eklendi**) | `cmd /c npx -y @brave/brave-search-mcp-server` | **envHelper** → `tools/mcp-launch/mcp-env.cmd` | — | 8 | Chat |
| context7 | ~~config~~ → **hesap bağlayıcısı** | Desktop config'inden **kaldırıldı** (11d) | bağlayıcı `context7-c1492263` | — | 2 | Chat |
| stitch | config (**eklendi**) | `cmd /c npx -y @_davideast/stitch-mcp@0.9.0 proxy` | miras (STITCH_API_KEY) | — | 16 | Chat |
| omniroute | config (**eklendi**) | `cmd /c omniroute --mcp` | yok | — | 110 | Chat |
| code-review | config (**eklendi**) | `cmd /c uvx code-review-mcp@2.0.0` | miras (GITHUB_TOKEN) | GITLAB_TOKEN tanımsız (CC'de de uyarı) | 12 | Chat |
| claude-mem | config (**eklendi**) | `node ...\claude-mem\13.25.2\scripts\mcp-server.cjs` | yok | yerel claude-mem worker | 15 | Chat |
| mslearn | hesap bağlayıcısı | `https://learn.microsoft.com/api/mcp` | auth yok | — | — | Chat |
| claude-design | hesap bağlayıcısı | `https://api.anthropic.com/v1/design/mcp` | OAuth | — | — | Chat |
| 21st | hesap bağlayıcısı | `https://21st.dev/api/mcp` | header x-api-key | — | — | Chat |
| github | hesap bağlayıcısı | `https://api.githubcopilot.com/mcp/` | header Bearer | — | — | Chat |
| figma | hesap bağlayıcısı | `https://mcp.figma.com/mcp` | OAuth | — | — | Chat |
| supabase | hesap bağlayıcısı | `https://mcp.supabase.com/mcp` | OAuth | Desktop'ta ayrı OAuth | — | Chat |
| design:{slack,linear,asana,atlassian,notion,intercom,gmail} | hesap bağlayıcısı | uzak http | OAuth | **CC'de de doğrulanmamış** — bu dalgada bağlanmadı (karar 6) | — | — |
| nano-banana-2 | — | — | — | **kapsam dışı** (karar 1) | — | — |

Uzak sunucular config'e **ikinci kez yazılmadı**: Desktop'ta hesap bağlayıcısı olarak gelir.

### Anahtar politikası

> **DÜZELTME · 21 Eyl 2026 (KURULUM-11d).** Aşağıdaki iki madde **yanlıştı** ve
> kaldırıldı. İkisinin de "kanıt"ı Claude Code'da **tam ortamla** koşan kuru testti;
> Desktop o programı çalıştırmıyor.
>
> - ~~**Miras** — süreç kullanıcı ortam değişkenlerini devralır.~~ Devralmıyor.
> - ~~**`%VAR%` genişletmesi** — `cmd /c` sarmalayıcısı genişletmeyi yapar.~~ Yapmıyor;
>   cmd de aynı kısıtlı ortamla başlar, değişken orada olmadığı için `%VAR%` literal kalır.

Desktop yerel MCP sunucularını **tam kullanıcı ortamıyla değil**, MCP TypeScript SDK'nın
`DEFAULT_INHERITED_ENV_VARS` beyaz listesiyle başlatır. Kaynak: `app.asar` ofset **3899305**
(Claude 2.2553.1.0). win32'de tam 12 değişken:

```
APPDATA HOMEDRIVE HOMEPATH LOCALAPPDATA PATH PROCESSOR_ARCHITECTURE
SYSTEMDRIVE SYSTEMROOT TEMP USERNAME USERPROFILE PROGRAMFILES
```

Özel anahtarlar bu listede olmadığı için sunucu sürecine **hiç ulaşmaz**.

**Doğru mekanizma: `envHelper`** (belgesiz, `app.asar` ofset 3045914). Config'te sunucuya
mutlak bir betik yolu yazılır; betik stdout'a tek JSON nesnesi basar, uygulama sunucuyu
başlatmadan önce çalıştırıp `env` üzerine birleştirir. Helper **tam uygulama ortamıyla**
koşar, beyaz liste ona uygulanmaz. `envHelperTtlSec` varsayılanı 300 s.
Helper'a argüman ya da sunucu adı **geçilmez**.

Bu repoda: `tools/mcp-launch/mcp-env.cmd` — `BRAVE_API_KEY` + `STITCH_API_KEY` adlarını
HKCU'dan okur, değeri yalnız stdout'taki JSON'a koyar. Anahtar helper her çalıştığında
okunduğu için **yenilenen anahtar bir sonraki Desktop açılışında kendiliğinden geçer**.

Config'te düz anahtar yok (gitleaks 0 bulgu).

⚠️ `envHelper` belgesiz bir alandır, app.asar'dan çıkarılmıştır. **Desktop güncellemesinde
yeniden doğrula.**

## 3. puppeteer (K2) — kök neden

Belirti: Desktop "Couldn't start for Cowork and Code sessions".

Elenen hipotezler (her biri çalıştırılıp kanıtla elendi):

| Hipotez | Test | Sonuç |
|---|---|---|
| npx yolu | gerçek Windows PATH ile `cmd /c npx --version` | ✅ 11.17.0 — elendi |
| eşzamanlı oturum | iki puppeteer örneği aynı anda | ✅ ikisi de 8 araç — elendi |
| Chromium indirme | `puppeteer_navigate https://example.com` | ✅ Status 200, isError:false — elendi |
| cmd sarmalayıcı / tırnaklı PATH | PATH tırnaklı ve tırnaksız | ✅ ikisi de çalıştı — elendi |

**Kök neden puppeteer değil.** Sunucu sağlıklı; başarılı araç çağrısı kanıtı yukarıda.
Hata mesajı özellikle *Cowork ve Code* oturumlarını adlandırıyor ve bu iki oturum türü
`cowork_vm_node.log`'da `status=unsupported` olan VM paketine bağlı. Yani yerel MCP'lerin
hiçbiri Cowork/Code'da görünmez; Chat'te görünür. Düzeltme puppeteer tanımında değil.

Not: `mcp.log` 0 bayt, `main.log`'da puppeteer geçmiyor → Desktop tarafında doğrudan
hata kaydı yok. VM kaydının son satırı 20 Ağu; **güncel doğrulama için ekran kanıtı gerekir**.

## 4. Sohbet eşdeğerliği (K4)

Envanter: **53 plugin komutu** (dedup; 68 dosya) + **161 subagent** + **9 CLI aracı** = 223 kalem.
Tam komut listesi: `docs/kurulum-11-komut-envanteri.txt`.

| Kova | Tanım | Sayı |
|---|---|---|
| (a) sohbette zaten skill olarak var | plugin skill'leri Desktop'ta doğrudan yüklü | 53 komut + 161 subagent = 214 |
| (b) sandbox'ta koşturulabilir → paket üretilir | 9 CLI aracı | 9 |
| (c) yapısal olarak imkânsız | — | 0 |

(c) kovası boş: karar 7 gereği kanıtsız satır yazılmaz ve elimizdeki her kalem için
çalıştırılmış bir kanıt var. claude-mem'in "imkânsız" sayılması karar 4 ile reddedildi ve
kuru test onu doğruladı (15 araç) — config'e girdi.

### (b) kovası — 9 CLI aracı, paketler bu dalgada ÜRETİLMEDİ

| CLI | Yol | Durum | Tahmini iş |
|---|---|---|---|
| graphify | `.local/bin/graphify` | (b) — üretilmedi | grafik verisi gömülmeli, büyük |
| agent-reach | `.local/bin/agent-reach` | (b) — üretilmedi | undici bağımlılığı (hafıza notu) |
| skill-ui | WinGet node | (b) — üretilmedi | orta |
| playwright-cli | WinGet node | (b) — üretilmedi | tarayıcı indirmesi gerekir |
| rtk | `.local/bin/rtk` | (b) — üretilmedi | orta |
| semgrep | `.local/bin/semgrep` | (b) — üretilmedi | kural tabanı büyük |
| gitleaks | WinGet Links | (b) — üretilmedi | tek ikili, kolay |
| headroom | `.local/bin/headroom` | (b) — yukle-10'da üretildi (headroom-compress) | tamam |
| pixeljury | WinGet node | (b) — yukle-10'da üretildi | tamam |

Gerekçe: dalga tur bütçesi (35) K1–K3 kök neden araştırması ve K5 ile doldu.
Sessizce düşen kalem yok; 7 paket **KURULUM-11b**'ye devreder (karar 3).

---

## §3 DÜZELTME · 21 Eyl 2026 (KURULUM-11c)

Bu bölüm §3'ün eski içeriğini **geçersiz kılar**. Eski kök neden ("yerel MCP'ler yalnız
Chat'te; Cowork/Code VM `status=unsupported`") **chat oturumundaki eksikliği açıklamıyor**:
eksik sunucular zaten Chat sekmesinde aranıyordu.

**11b'de elenen dört hipotez** (hiçbiri kök neden değil):

| Hipotez | Test | Sonuç |
|---|---|---|
| npx yolu | `cmd /c npx --version` (gerçek Windows PATH) | 11.17.0 — elendi |
| eşzamanlı oturum | iki puppeteer örneği aynı anda | ikisi de 8 araç — elendi |
| Chromium indirme | `puppeteer_navigate https://example.com` | Status 200, isError:false — elendi |
| cmd sarmalayıcı / tırnaklı PATH | PATH tırnaklı ve tırnaksız | ikisi de çalıştı — elendi |

Ölçüm süreleri: kuru testler sunucu başına 0.3–3 sn arası tamamlandı; hiçbirinde
zaman aşımı görülmedi — "açılış zaman aşımı" açıklaması da bu yüzden düşüyor.

**11c'deki yeni kanıt (K1):** 20 Eyl'de Desktop **yeniden başlatılmadan** açılan yeni
sohbette sayım 22 ve `omniroute` listede **yok**. omniroute 11b/K0'da config'ten
silinmişti; liste uygulama açılışında donsaydı hâlâ görünecekti. Yani araç listesi
config yazımından **sonra** tazeleniyor → "bayat liste" hipotezi de zayıf.

**Durum:** `puppeteer` ve `brave-search` Desktop chat'e gerçekten gelmiyor; kök neden
hâlâ bulunamadı. 11c'de yeni teşhis denemesi yapılmadı (tarif gereği). Sonraki adım 11d.


## 5. KURULUM-11d düzeltmeleri · 21 Eyl 2026

### §3'ün sonucu yanlıştı — puppeteer'ın kök nedeni bulundu

§3 "eşzamanlı oturum" hipotezini **araç sayısına bakarak** eledi (iki örnek de 8 araç
döndürdü). Ölçülmeyen şey **süreydi**. 11d'de aynı test `--desktop-env` tabanıyla ve
süre ölçülerek tekrarlandı:

| Senaryo | `initialize` süresi | Sonuç |
|---|---|---|
| Tek örnek | **3.9 s** | OK, 8 araç, navigate Status 200 |
| İki eşzamanlı örnek | **26–28 s** | ikisi de OK — ama Desktop çoktan öldürmüş olur |

Desktop sunucuyu iki tüketici için başlatıyor (sohbet + "Cowork and Code sessions"
shared-pool). `npx -y` paket çözümlemesi yarışınca açılış 24 s'lik zaman aşımını aşıyor;
log'daki 09:06:46 (`initialize`) → 09:07:10 (süreç öldü) penceresi tam bu.

§3'teki "kuru testler 0.3–3 sn sürdü, zaman aşımı açıklaması düşüyor" cümlesi de bu
yüzden geçersiz: o süreler **tek örnek** süreleriydi.

**Düzeltme:** `"startupTimeoutSec": 120`.

### Yol düzeltmeleri

Önceki dalgalarda `%APPDATA%\Claude` varsayılmıştı. Doğrusu:

| Ne | Yol |
|---|---|
| Canlı config | `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json` |
| Canlı log | `%LOCALAPPDATA%\Claude\logs` |
| Uygulama | `C:\Program Files\WindowsApps\Claude_2.2553.1.0_x64__pzs8sxrjxfjjcpp\Claude.exe` (MSIX) |

`%APPDATA%\Claude` **yok**. `…\LocalCache\Roaming\Claude\logs` (mcp.log 0 B / 18 Ağu)
kalıntı klasördür.

**11e kalemi olarak yazılacak "ikinci (MSIX) kurulum izi" notu ters yöndeydi:** ikinci
kurulum yok; MSIX olan **asıl ve tek** kurulumdur.

### K2b paketi

`dist/yukle-11d/replace/gitleaks-desktop.zip` — gitleaks 8.30.1, statik ELF64 x86-64,
sha256 release checksums ile eşleşti, açık 20.9 MB. **Yürütme kanıtı claude.ai'de
bekliyor**; (a) kararı o kanıt gelene kadar kesin değildir.

## 6. KURULUM-11e · 21 Eyl 2026 — sunucu komutu anahtarı kendisi okur

### 11d'nin iki düzeltmesi canlıda etkisizdi (K0 kanıtı)

| Kanıt | Saat |
|---|---|
| Canlı config yazıldı (`envHelper` + `startupTimeoutSec: 120` içinde) | **10:28:36Z** |
| Desktop açılışı, 3 log'da `Initializing server` | **10:48:00Z / 10:48:04Z** |

Config açılıştan **20 dakika önce** yazılmıştı; yani her iki alan da canlıydı. Sonuç:

- `brave-search` → `A Brave API key is required … BRAVE_API_KEY` + `Invalid configuration`, 10:48:21Z'de düştü
- `stitch` → `✖ Proxy server error: StitchProxy requires an API key (STITCH_API_KEY) …`, 10:48:20Z'de düştü
- `puppeteer` → initialize 10:48:04.474Z → `transport closed` 10:48:28.326Z (**23.9 s**), stderr boş

**Desktop `envHelper`, `envHelperTtlSec` ve `startupTimeoutSec` alanlarını okumuyor.**
Bunlar belgesiz alanlardı; 11d'de config şemasında görünmeleri okunmalarına delil sayılmıştı.
Kural: **belgesiz config alanına dayanılmaz.**

### Yeni mekanizma

`npx` açılıştan çıkarıldı, paketler pinli global kuruldu, araya `cmd` wrapper girdi:

| Sunucu | Paket (pinli) | Wrapper |
|---|---|---|
| puppeteer | `puppeteer-mcp-server@0.7.2` (MIT) | `tools/mcp-launch/puppeteer.cmd` |
| brave-search | `@brave/brave-search-mcp-server@2.1.4` (MIT) | `tools/mcp-launch/brave-search.cmd` |
| stitch | `@_davideast/stitch-mcp@0.9.0` (Apache-2.0) | `tools/mcp-launch/stitch.cmd` |

Config tarafı artık yalnız `{"command":"cmd","args":["/c","<mutlak wrapper>"]}`.
Anahtarı **wrapper** `reg query HKCU\Environment` ile okur; değer `for /f`'e girer,
ekrana/log'a hiç çıkmaz. Config'te düz anahtar yok.

#### İki tuzak (ikisi de bu dalgada bulundu)

1. **`npx` = puppeteer'ın 24 s'si.** Global kurulumdan sonra kuru testte açılış
   **23.9 s → 0.6 s**. Zaman aşımı hastalık değil, semptomdu; `startupTimeoutSec`
   okunsaydı bile yanlış tedavi olurdu.
2. **Wrapper'da `setlocal` OLMAZ.** Son satır `call`'suz başka bir `.cmd`'ye geçer;
   cmd.exe batch bağlamını değiştirirken **örtük `endlocal`** uygular. npm shim'inin
   kendi `endLocal`'ı da bizim kapsamı açar ve anahtar node başlamadan silinir.
   Kanıtlandı: `setlocal` ile `Invalid configuration`, `setlocal` olmadan 8 araç.

### Sonuç — 2/3 çalışıyor, puppeteer DUR

Kuru test (`mcp_kurutest.py --desktop-env`, canlı config):

| Sunucu | Araç | Tek örnek | 2 eşzamanlı örnek |
|---|---|---|---|
| puppeteer | 8 | 0.4 s | 0.4 s / 0.4 s |
| brave-search | 8 | 0.5 s | 0.5 s / 0.5 s |
| stitch | 16 | 1.1 s | 1.4 s / 1.6 s |

11d tabanı 2 eşzamanlı örnekte 26–28 s idi. `brave_web_search` ile **1 gerçek çağrı**
yapıldı (tavan 1): 621 karakter sonuç → anahtar yalnız mevcut değil, geçerli.

Canlı Desktop (11:44Z açılışı):

- **brave-search — GEÇTİ.** `initialize` → sonuç → `tools/list` → sonuç. Anahtar hatası yok, kapanma yok.
- **stitch — GEÇTİ.** `[stitch-proxy] Connected to Stitch, discovered 15 tools`. Anahtar hatası yok, kapanma yok.
- **puppeteer — DUR.** 11:44:03.551Z `initialize` id=0 → **sunucu hiç yanıt vermedi** →
  11:44:05.160Z shared-pool `Couldn't start for Cowork and Code sessions` →
  11:44:06.946Z `transport closed` (**3.4 s**). **stderr tamamen boş.**

**Puppeteer'ın kalan kök nedeni kanıtlanmamıştır.** Bilinen: `npx` gecikmesi gitti
(23.9 s → 3.4 s) ama süreç yine de `initialize`'ı yanıtlamadan kendiliğinden çıkıyor.
Aynı wrapper, aynı 12 değişkenlik ortamla kuru testte 0.4 s'de 8 araç döndürüyor.
Yani **12 değişkenlik beyaz liste taklidi Desktop'ın gerçek spawn'ını tam modellemiyor**;
fark (cwd, stdio tutamak tipi, ikinci eşzamanlı tüketici yarışı) henüz ölçülmedi.
Sonraki dalga buradan başlamalı — ölçüm gerekiyor, tahmin değil.

### Desktop güncellemesinde yeniden doğrula

Wrapper'lar npm global prefix'ine mutlak yolla bağlı:
`…\WinGet\Packages\OpenJS.NodeJS.LTS_…\node-v24.19.0-win-x64`. Node sürümü yükselirse
bu yol değişir. Desktop veya Node güncellemesinden sonra K4 kuru testi tekrar çalıştırılmalı.

`tools/mcp-launch/mcp-env.cmd` (11d envHelper betiği) bu dalgada **silindi** — referanssız kaldı.

## 7. KURULUM-11f · 21 Eyl 2026 — puppeteer kök nedeni kanıtlandı

**Kök neden (tek cümle):** Claude Desktop yerel MCP sunucularını
cwd = `C:\Windows\System32` ile başlatır; `puppeteer-mcp-server` günlük dosyasını
`<cwd>\logs` altına açtığı ve orada yazma izni olmadığı için düşer, hatayı da yalnız
açamadığı o dosyaya yazmaya çalıştığından stderr boş kalır ve süreç sessizce ölür.

**Kanıt satırı** (`_trace.cjs`, 12:15Z açılışı, 6 sürecin altısında da aynı):

```json
{"olay":"acilis","cwd0":"C:\Windows\System32","cwd":"C:\Users\pc\AppData\Local\Temp"}
```

`cwd0` = wrapper düzeltmeden **önce** yakaladığı Desktop cwd'si. Kontrol kolu
brave-search aynı `cwd0` ile başlıyor ama cwd'ye yazmadığı için zaten çalışıyordu —
fark tek başına cwd'ye göreli yazma.

### Paketin sessizliği nereden geliyor

`puppeteer-mcp-server@0.7.2 · dist/src/config/logger.js`:

```js
const logsDir = path.join(process.cwd(), 'logs');            // cwd'ye GÖRELİ
if (!fs.existsSync(logsDir)) fs.mkdirSync(logsDir, {recursive:true});
// transports: SADECE DailyRotateFile -- "to avoid interfering with MCP protocol"
process.on('uncaughtException', e => { logger.error(...); process.exit(1); });
```

Tüm hatalar stderr'e değil bu dosyaya gider. Dosya açılamazsa hata da kaybolur.

### Ayrıştırıcılar (`mcp_kurutest.py --cwd` / `--spawner`)

| Koşu | Sonuç |
|---|---|
| `--cwd C:\Windows\System32` | `INIT-YOK`, çıkış **1**, stderr **boş** — Desktop imzasının aynısı |
| `--cwd <WindowsApps\Claude…>` | `INIT-YOK`, stderr'de `logger.js:8` + `errno -4048` (EPERM) |
| `--spawner node`, cwd = repo | **OK, 8 araç** → suçlu spawner katmanı değil |
| `--spawner node` + WindowsApps cwd | `INIT-YOK`, aynı `logger.js:8` → **suçlu cwd** |

İlk iki satırın farkı imzayı da açıklıyor: `System32\logs` **var** olduğu için
`mkdirSync` hiç denenmez, hata winston dosyayı açarken — yani `uncaughtException`
dinleyicisi kaydolduktan **sonra** — oluşur ve yutulur. `WindowsApps\…\logs` ise
yok, `mkdirSync` modül yüklenirken patlar, dinleyici henüz yok, stderr'e düşer.
Desktop'ın gördüğü ilk durumdur.

### Düzeltme

`tools/mcp-launch/puppeteer.cmd` içinde tek satır, shim çağrısından önce:

```cmd
cd /d "%TEMP%"
```

`TEMP` 12 değişkenlik beyaz listede ve yazılabilir; günlük artık
`%TEMP%\logs\mcp-puppeteer-*.log`. Config'e belgesiz alan **eklenmedi**; üç tanım da
yalnız `command` + `args` içeriyor, diğer 11 tanım değişmedi.

**Doğrulama** — canlı Desktop 12:15Z açılışı, `mcp-server-puppeteer.log`:
`initialize` → sonuç → `tools/list` 8 araç → `resources/list` → sonuç; ardından
iki `tools/call` (navigate + screenshot) sonuç döndürdü. Kapanma satırı yok.
12:14Z'den sonra **mcp.log'da hiç `[error]` satırı yok** (14 sunucunun tamamı).

### "Couldn't start for Cowork and Code sessions" tostu — VM ile ilgisi yoktu

Bu satır bir VM teşhisi değildi: shared-pool MCP tüketicisinin ölmüş sunucuya
bağlanamamasıydı. Sunucu ayakta kaldığı için 12:14Z'den sonra **0 tane** üretildi.
Cowork VM'i ayrı bir katman ve hâlâ kurulu değil — `cowork_vm_node.log`
`rootfs.vhdx missing` / `vmlinuz missing` / `initrd missing` diyor — ama bu satırlar
MCP tostu üretmez. İki olgu birbirinden bağımsız; çelişki yok.

### Kalıcı iz aracı

`tools/mcp-launch/_trace.cjs` — `node --require` ile takılan geçici iz. Bu dalgada
wrapper'lardan çıkarıldı, ileride Desktop spawn davranışı yine ölçülmek gerekirse
diye dosya `tools/` altında bırakıldı. Ortam değişkenlerinin yalnız **adlarını**
kaydeder, değerlerini asla.
