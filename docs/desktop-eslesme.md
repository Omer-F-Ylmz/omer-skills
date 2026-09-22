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
| obsidian | config (**eklendi**, 11g · 11m-A'da yeniden yazıldı) | `cmd /c tools\mcp-launch\obsidian.cmd` → `node tools/cc-kopru/obsidian.mjs` (SDK SSE istemcisi; mcp-remote katmanı düştü) | yok (eklentide kimlik doğrulama yok; §8 yaması) | Obsidian kapalıyken de açılır; araç çağrısı "Obsidian kapalı — aç ve tekrar dene" der, Obsidian açılınca Desktop yeniden başlatılmadan ilk çağrı bağlanır (11m-A K1) | 7 | Chat |
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

> **ÇÜRÜTÜLDÜ — 11f, §7.** Buradaki *nedensellik* iddiası yanlıştı. puppeteer
> Chat sekmesinde de düşüyordu; kök neden Desktop'ın sunucuyu
> `cwd=C:\Windows\System32` ile başlatması ve paketin oraya günlük yazamaması.
> §1'deki VM paketi kanıtı (satır 22-26) doğru, ama **bağımsız** bir olgu: o
> satırlar MCP tostu üretmez. Kanıt ve düzeltme §7'de.

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

## 8. KURULUM-11g · 21 Eyl 2026 — obsidian köprüsü + eklenti güvenlik yaması

### Köprü

Desktop `claude_desktop_config.json`'da yalnız **stdio** tanımı kabul eder; Obsidian
`claude-code-mcp` eklentisi (v1.1.8) HTTP+SSE konuşur. Arada `mcp-remote@0.14.3`
(global, npm prefix'i diğer wrapper'larla aynı) stdio↔SSE proxy'si duruyor.
CC'nin `/ide` WebSocket bağlantısına dokunulmadı; o eklentinin ayrı kanalı.

`tools/mcp-launch/obsidian.cmd` iki noktada 11e/11f kalıbına ekleme yapar:

- **`http://127.0.0.1:22360/sse`, `localhost` değil.** Eklenti `server.listen(port,
  "127.0.0.1")` ile yalnız IPv4 dinliyor; Node Windows'ta `localhost`'u önce `::1`'e
  çözebilir ve bağlantı reddedilir.
- **`--transport sse-only`.** Eklentide `/mcp` (Streamable HTTP) rotası yok, yalnız
  `GET /sse` + `POST /messages?session_id=…` var. mcp-remote 0.14.x varsayılanı
  `http-first`, yani her açılışta boşa giden bir yoklama demek.

**Obsidian kapalıyken** köprü asılı kalmaz: `ECONNREFUSED 127.0.0.1:22360`,
çıkış kodu 1, **5.6 s**. Desktop üstel geri çekilmeyle yeniden dener. Sıra bu yüzden
önemli: **Obsidian, Desktop'tan önce açılır.**

### Kalıp notu (her yeni wrapper için)

Desktop yerel MCP sunucularını `cwd=C:\Windows\System32` ile başlatır (§7'de
kanıtlandı). Oraya yazmaya çalışan her sunucu sessizce düşer. **Her yeni wrapper
ilk komut olarak `cd /d "%TEMP%"` ile açılır.** `TEMP` 12 değişkenlik beyaz listede
ve yazılabilir. Mevcut `brave-search.cmd` / `stitch.cmd` geriye dönük düzeltilmedi —
cwd'ye yazmıyorlar.

### Güvenlik bulgusu ve yama (K6)

Eklentinin sunucusu hiçbir kimlik doğrulaması yapmıyordu:

- `validateOrigin(req) { return true; }` — saplama, Origin hiç denetlenmiyordu
- `Access-Control-Allow-Origin: "*"` iki yerde (ön ayarlar + SSE yanıtı)
- WS sunucusu `new WebSocketServer({ port: 0 })` — **host yok**, yani `::` (tüm
  arayüzler). Lock dosyasında `authToken` da yok.

Sonuç: Obsidian açıkken ziyaret edilen herhangi bir web sayfası kasayı okuyup
**yazabilirdi**; yazma yolu prompt injection kapısıdır. WS tarafı ayrıca tarayıcıya
hiç gerek kalmadan LAN'dan erişilebilirdi.

**Ölçüm önce:** mcp-remote `Origin` **göndermiyor** (UA `undici`; `sec-fetch-mode: cors`
var ama Origin yok). Tarayıcı ise her cross-origin istekte ve her WS el sıkışmasında
Origin gönderir. Bu yüzden bearer token'a gerek kalmadı.

`tools/obsidian-yama.ps1` altı çapayı değiştirir:

| # | Yer | Önce | Sonra |
|---|---|---|---|
| 1 | logger | — | `__k11gOriginLog` (Origin kaydı) |
| 2 | `setCORSHeaders` | 4 CORS başlığı | boş — CORS başlığı **hiç** yazılmaz |
| 3 | SSE `writeHead` | 2 CORS başlığı | kaldırıldı |
| 4 | `validateOrigin` | `return true` | Origin varsa **403** |
| 5 | WS sunucu | `{ port: 0 }` | `+ host: "127.0.0.1"` · `verifyClient` Origin varsa **401** |
| 6 | WS port | `address().port` | `listening` beklenir (aşağıya bak) |

**6. çapa neden gerekti:** `host` verilince `net.Server.listen` DNS yoluna girer ve
senkron olmaktan çıkar. Eklentinin `this.port = this.wss.address().port;` satırı
`null.port`'a düşer, hata `dual-server.ts`'in `try/catch`'inde yutulur ve
`~/.claude/ide/<port>.lock` **yazılmaz** — yani CC `/ide` keşfi kırılır. Sunucu yine
dinlemeye devam ettiği için belirti sessizdir. Ölçüm: yamasız `{port:0}` →
`address()` anında `{"address":"::"}`; `{port:0,host}` → `address()` **null**.

Betik idempotenttir ve hash'e bağlıdır: yamasız → uygular · yamalı → dokunmaz ·
**bilinmeyen → DUR**. Yama öncesi `main.js.bak11g` alınır; yama sonrası hash
tutmazsa yedek geri yüklenir.

```
yamasiz sha256 784b49d6f243053a2271d1e69c6d0716a3bde407a5dfeda8fbb894eaf87ec043
yamali  sha256 4ee2c5d80b1baf9312d701708feb6adb0eee252ddd95f83d5737788998c0805c
```

> **Eklenti güncellenince yama SİLİNİR.** Güncellemeden sonra
> `powershell -ExecutionPolicy Bypass -File tools\obsidian-yama.ps1` yeniden koşulur.
> Yeni sürümde hash bilinmeyeceği için betik DUR verir; çapalar elle doğrulanıp
> hash sabitleri güncellenmeden yama uygulanmaz.

Origin kaydı: `C:/Projeler/.tmp-mcp-trace/obsidian-origin.jsonl` — yalnız başlık
**adı + değeri**, gövde yok.

### Desktop'ın "araçları say, kapat" deseni

Bu dalgada 15 sunucunun hepsi `initialize` + `tools/list` tamamladı. Sonrasında
çoğunda birkaç saniye içinde `Server transport closed` görülür: bu bir çökme değil,
Desktop'ın araçları sayıp stdio taşımasını kapatması, çağrı gelince yeniden
başlatmasıdır. **Gerileme değildir** — 11f'de kabul edilen 12:15 açılışında da aynı
desen var, üstelik orada `closed unexpectedly` varken bu açılışta yok.
"≥2 dk kapanma yok" ölçütü bu yüzden "tools/list'i tamamlamadan düşme yok ve
sonrasında yeniden deneme döngüsü yok" diye okunmalıdır.

### Köprünün kopma/toparlanma davranışı (K7, ölçüldü)

Belirti: Desktop sohbetinde `obsidian get_workspace_files` iki kez 4'er dakika
**hatasız** askıda kaldı. Beş ölçüm sorunu eklentide de köprüde de üretmedi:

| Senaryo | `tools/call` |
|---|---|
| Eklenti, tek istemci (köprüsüz) | 0.02 s |
| Eklenti, iki tüketici (B listele→kapan, sonra A çağır) | A yanıt aldı |
| Köprü, normal ortam | 6.3 s |
| Köprü + `--desktop-env` + `cwd=System32` | 0.42 s |
| Aynı anda iki köprü örneği | ikisi de OK |

Kök neden `mcp-server-obsidian.log`'da: **tek bir `tools/call` satırı yok** — çağrı
sunucuya hiç ulaşmamış. Buna karşılık **448** üst düzey
`SseError: … ECONNREFUSED 127.0.0.1:22360` var. Desktop açılışta **iki** mcp-remote
örneği başlatır ve bunlar uzun ömürlüdür; Obsidian'ın sunucusu gidince ikisi de
süresiz yeniden deneme döngüsüne girer. Desktop o sırada sunucuyu hazır saymaz,
`tools/call`'ı göndermez ve **hata da üretmez** — çağrı askıda kalır.

Ölçülen davranış:

- **Obsidian kapalıyken:** çağrı hatasız askıda kalır (zaman aşımı yok, izin istemi
  yok). Köprü ilk açılışta bağlanamazsa `ECONNREFUSED`, çıkış kodu 1, **5.6 s**;
  ama bağlantı *kurulduktan sonra* koparsa süresiz yeniden dener.
- **Obsidian açılınca:** köprü kendiliğinden toparlanır. Ölçüm — Obsidian süreci
  14:34:57Z, köprüden ilk sunucu mesajı 14:35:01.6Z → **~4.6 s**. Obsidian
  dinlemeye başladıktan sonra **0** `ECONNREFUSED`.
- **Desktop yeniden başlatmak gerekmedi.** Çağrı, açılışta doğan aynı köprü
  PID'leriyle yanıt verdi.

Elenen iki hipotez: URL ve soket zaten `127.0.0.1` olduğu için `localhost`→`::1`
sapması **mümkün değil**; yeniden deneme beklemesi de suçlu değil (4.6 s).

**Kural:** Obsidian, Desktop'tan **önce** açılır. Obsidian kapanıp açılırsa Desktop'ı
yeniden başlatmak gerekmez, ~5 s beklemek yeterlidir. Kesinti penceresinde yapılan
çağrılar hata vermeden askıda kalır — bu Desktop'ın davranışıdır, köprününki değil.

### Kasaya/projeye sızan `logs\` klasörleri

`puppeteer-mcp-server` günlüğünü `<cwd>\logs\` altına açar (§7'deki mekanizmanın
zararsız hali — cwd yazılabilir olduğu için sessizce başarılı olur). CC user-scope
MCP'leri oturum cwd'sinde başlattığı için her CC oturumu proje köküne `logs\`
yazıyordu. Bulunanlar: `C:\Projeler\omer-skills\logs\` (3 günlük + audit) ve
`C:\Users\pc\Desktop\Obsidian\logs\` (20 Eyl, 3 koşu). **Hiçbiri repoya girmemiş** —
bu repoda `.gitignore`'un `logs/` satırı kapsıyor, `git ls-files logs` boş.
İkisi de `C:\Projeler\.tmp-mcp-trace\` altına taşındı.

Düzeltme: `~/.claude.json` içindeki user-scope `puppeteer` tanımı
`tools\mcp-launch\puppeteer.cmd`'ye yönlendirildi (wrapper zaten `cd /d "%TEMP%"`
ile açılıyor). Yedek `~/.claude.json.bak11g`; diğer 16 sunucunun ve üst ağacın
hash'i değişmedi. Etkisi yeni CC oturumlarında.

## 9. KURULUM-11i · 21 Eyl 2026 — cc-kopru: CC katmanı Desktop sohbetinde

Desktop sohbetine CC'nin CLI · hook · subagent · hafıza katmanını açan yerel stdio MCP:
`tools/cc-kopru` (Node + `@modelcontextprotocol/sdk`). Başlatıcı
`tools/mcp-launch/cc-kopru.cmd`. Desktop `mcpServers` **15 → 16**; yalnız `command` +
`args` yazıldı, `env` bloğu yok. Yedek `claude_desktop_config.json.bak11i`.
CC `~/.claude.json` `mcpServers` alt ağaç hash'i **değişmedi** (`a88f7f99ce829eec`).
Desktop'ın kısıtlı ortam beyaz listesiyle (12 değişken) ve `cwd=System32` ile ayrıca
doğrulandı: initialize + 4 araç + `gitleaks version` exit 0.

### `claude mcp serve` neden kullanılmadı

Ölçüldü (`tools/call`): serve 28 araç veriyor (`Task` yok, karşılığı `Agent`) ama
**ne PreToolUse hook'unu ne `permissions.deny`'ı uyguluyor** — süreç-adla-öldürme komutu
koştu (exit 128), `Read(./graphify-out/**)` deny'ına rağmen dosya okundu. Desktop'a açmak
hook'suz/deny'siz `Bash`+`Edit`+`Write` vermek olurdu. Köprü kendi runner'ını koşuyor.

### Araç tablosu

| araç | ne yapar | kapı |
| --- | --- | --- |
| `komut` | allowlist'teki 12 CLI (graphify · rtk · semgrep · gitleaks · playwright-cli · skill-ui · agent-reach · headroom · pixeljury · dotnet · git · strix) | alt komut ilk jeton · yürütücüye komut geçiren seçenek red · `cwd` yalnız `C:\Projeler` / `Desktop` · `shell:false` |
| `ajan` | gerçek CC oturumu (`claude -p --output-format json`) | istem **stdin**'den, argv'ye girmez · `model`/`ajan_adi`/`devam_id` `[A-Za-z0-9._-]` · izin atlama red · oturum başına 10 çağrı |
| `oturum` | `SessionStart` hook'ları + `CLAUDE.md` + `dalga.md` | 12k kırpma |
| `kaydet` | gitleaks → claude-mem worker `POST :37777/api/memory/save`, kaynak `desktop` | sızıntı varsa yazmaz |

Ortak: tek kuyruk · timeout'ta süreç **ağacı PID ile** kapatılır · 30k üstü çıktı baş 5k
+ son 25k, tamamı `%TEMP%\cc-kopru\*.log` · adında `KEY|TOKEN|SECRET|PAT|PASSWORD`
**segmenti** olan değişkenlerin değeri `***` (segment eşleşmesi; `PATH` bozulmaz).

### Hook envanteri — çalışan / çalışmayan

13 kaynaktan **53 tanım** okunuyor (`~/.claude/settings.json` + 12 açık eklentinin
`hooks/hooks.json`'u + proje ayarı). `kopru.json > kapaliHooklar` **boş** — elle
kapatılan hook yok; elenenler yapısal eleniyor:

| durum | hangileri | sebep |
| --- | --- | --- |
| koşuyor (PreToolUse `Bash`) | block-destructive.ps1 · `rtk hook claude` · hookify · headroom | matcher `Bash`'i kapsıyor |
| koşuyor (SessionStart) | user-settings headroom-guard · explanatory/learning-output-style · security-guidance · superpowers · everything-claude-code · headroom · claude-mem (×2) · claude-mem-cowork | ölçüldü; `oturum` çıktısında listeleniyor |
| atlanıyor | everything-claude-code'un `tool=="Bash" && …` matcher'ları | CC'nin ifade matcher'ı; köprü regex matcher uyguluyor, ifade görürse atlıyor |
| tetiklenmiyor | impeccable (POSIX başlatıcı, Windows'ta şüpheli) · claude-mem `PreToolUse:Read` · claude-mem-cowork `Task\|Agent` · dotnet-format (`Edit\|Write`) | matcher köprünün ürettiği olaylara uymuyor |
| transcript'e bakanlar | claude-mem ailesi · ralph-wiggum `Stop` | her oturum `%TEMP%\cc-kopru\<id>.jsonl` asgari transcript yazıyor, boşa düşmüyorlar |

Kanıt (gerçek `claude -p` içinden): süreç-adla-öldürme komutu denendi, dönen metin aynen
`DUR: süreç adla öldürülmez; yalnız kendi başlattığın PID`.

### `ajan` maliyeti — normal vs `hafif`

`hafif: true` yalnız `claude --help`te doğrulanmış bayrakları ekler:
`--disable-slash-commands` ("Disable all skills") · `--strict-mcp-config` +
`--mcp-config {"mcpServers":{}}`. **Hook'lar ve CLAUDE.md açık kalır.** Bayraklar
sürümde yoksa `hafif` reddedilir; uydurma bayrak yok.

| # | iş | hafif | girdi token | tur | $ |
| --- | --- | --- | --- | --- | --- |
| 1 | dosya yaz / oku / sil (yazma izni kanıtı) | hayır | **167.802** | 2 | 0,3298 |
| 2 | plugin komutu `/ponytail-help` | hayır | **85.084** | 1 | 0,3136 |
| 3 | hook kanıtı (süreç-adla-öldürme) | evet | **58.702** | 2 | 0,1256 |
| 4 | `devam_id` ile sürdürme | evet | **29.671** | 1 | 0,1331 |

Kural: skill / slash komutu ya da MCP gerekiyorsa `hafif: false` (2. satır —
`/ponytail-help` `hafif`te çalışmazdı). Dosya / komut / hook işi ise `hafif: true`;
bağlam ~3× küçülüyor, maliyet ~%60 düşüyor. `devam_id` ile sürdürmede cache okuma
%99'a çıkıyor, girdi 29.671'e iniyor.

### Kalıcı sınırlar

- **`UserPromptSubmit` ve `Stop` yok.** Köprü araç çağrısıyla uyanıyor; Desktop sohbetinin
  istem gönderme ve durma anlarına bağlanamıyor. O olaylara bağlı hook'lar (hookify,
  security-guidance, claude-mem summarize, ralph-wiggum) Desktop tarafında tetiklenmez.
- **Sohbet bağlamı ölçülemez.** Köprü Desktop'ın token kullanımını, geçmişini ya da
  compaction durumunu göremez; `ajan`ın bildirdiği rakamlar yalnız o `claude -p` alt
  oturumuna aittir.
- **Sohbet trafiği proxy'den geçmez.** `ANTHROPIC_BASE_URL` yalnız köprünün başlattığı
  süreçleri etkiler; Desktop'ın kendi istekleri headroom proxy'sine uğramaz.
- Yerel MCP'ler Desktop'ta yalnız **Chat** sekmesinde; Cowork/Code oturumları için geçerli
  değil (§6'daki `status=unsupported` bulgusu).

### 11i-FIX-2 · Desktop'tan köprü kontrolü (21 Eyl)

- Gerçek Desktop çağrısı üç kırık gösterdi ve üçü de kapatıldı: `kaydet` worker'ın strict şemasına takılıyordu (`source` anahtarı yok; "desktop" etiketi artık `metadata.platformSource`), bash hook'ları PATH'inde Git olmayan MCP sürecinde "spawn bash ENOENT" veriyordu (artık mutlak Git Bash yolu, WSL `System32\bash.exe` asla), `;` argüman metakarakteri sayılmıyordu ve hook yeniden yazımı argüman sınırını bozabiliyordu (artık yalnız `["rtk", ...orijinal argv]` biçimi kabul, başkası yok sayılır); gitleaks reddi yalnız "N bulgu (kural adı)" basar, değer ve ANSI yok.

---

## §10 · KURULUM-11k — CC eşdeğerliği: katman katman (21 Eyl 2026)

11k, cc-kopru'nun beş katmanını Claude Code'daki davranışa yaklaştırdı. Her satır
ölçüme dayanır; ölçülemeyen parça "yapısal sınır" olarak yazıldı, tahmin yazılmadı.

| katman | CC'de | Desktop'ta (11k sonrası) | yol | yapısal sınır |
|---|---|---|---|---|
| CLI yüzeyi | Bash + `permissions.allow/deny` | `komut` aracı · 21 araç allowlist'i | `kos.mjs` · `kopru.json` | inline kod (`-e/-c/-p`) ve indirip-çalıştırma kapalı; `npx` yalnız `--no` ile |
| izin reddi | `permissions.deny` | `Bash(...)` komut yüzeyinde, `Read(...)` kanca geçidinde | `denyDenetle` · `okumaDeny` | — |
| hook'lar | PreToolUse/PostToolUse | aynı tanımlar aynen koşar (kopyalanmaz) | `hook.mjs` | ifade matcher'ları (`tool == "Edit" && …`) atlanır |
| MCP araçları | CC'nin kendi izin katmanı | `mcp-filesystem` + `mcp-git` geçit arkasında | `gecit.mjs` | salt okur git araçları eşlenmez (CC'de de Bash değiller) |
| alt oturum | Task/agent | `ajan` (`claude -p`, gerçek CC oturumu) | `sunucu.mjs` | `--max-turns` CLI'da yok; bütçe göreve yazılıp dönüşte doğrulanır |
| katalog | skill/komut/agent listesi | `katalog` aracı (dosya sistemi, API yok) | `hook.mjs:katalogTopla` | — |
| statusline | her turda | `durum` aracı, son `ajan` kullanımıyla | `statuslineGovde` | **Desktop sohbetinin kendi ctx %'si ölçülemiyor** (§9) |
| hafıza | PostToolUse → claude-mem | her `komut`/`ajan`/geçit çağrısı aynı uçtan | `gozlemYaz` | sağlayıcı kotası doluyken kuyrukta bekler |
| oturum özeti | Stop hook | `oturum_ozeti` aracı | `/api/sessions/summarize` | asenkron LLM işi |
| bağlam sıkıştırma | Headroom proxy (6767) | >8 KB çıktı `headroom mcp serve`'e | `ciktiHazirla` | **Desktop sohbet trafiği yerel proxy'ye yönlendirilemiyor** (aşağıda) |
| tasarım MCP'si | `claude-design` (http, OAuth) | `mcp-remote` sarmalayıcısı | `tools/mcp-launch/claude-design.cmd` | ilk kullanımda tarayıcı onayı gerekir |

### K1-ek · `npx` koşulsuz REDden `--no` zorunluluğuna

Faz A'da `npx` tamamen kapatılmıştı (`--no-install` npm 11.17'nin `--help`inde yok).
Kaynak okunduğunda gerçek bayrak bulundu:

- `docs/content/commands/npm-exec.md:28` — istem `--yes` **ya da `--no`** ile bastırılır.
- Aynı dosya `:29` — **stdin TTY değilse `--yes` VARSAYILIR.** Köprü sürecinde TTY yok:
  bayraksız `npx` uzak paketi sessizce indirip koşardı.
- `libnpmexec/lib/index.js:288-291` — `yes === false` ise `npxArb.reify()`'den **önce**
  `npx canceled due to missing packages and no YES option` atılır. `:294-296` ise
  TTY yokken "will be installed" deyip kurar.
- `:298` — `--no-install` deprecated, `--no`ya çevriliyor; köprü kabul etmiyor.

Sonuç: `npx` allowlist'te, `gerekliBayrak: ["--no"]`. Pin: `npx --no node-which node`
gerçekten koşuyor (exit 0), `npx --no <olmayan-paket>` reify'den önce iptal ediliyor.

### K5 · Kanca geçidi

`gecit.mjs` satır tabanlı bir JSON-RPC proxy'dir: Desktop ↔ geçit ↔ gerçek sunucu.
Yalnız `tools/call` yakalanır, kalan her mesaj **ham satır** olarak iletilir (yeniden
serileştirme yok). Eşleme:

- `read_file|read_text_file|read_multiple_files|read_media_file` → `Read`
- `write_file|create_directory|move_file` → `Write`, `edit_file` → `Edit`
- `git_commit|git_add|git_reset|git_checkout|git_create_branch|git_init` → `Bash`
  (`tool_input.command` gerçek git satırına çevrilir, hook'lar onu görür)

Desktop config'de **aynı adlar** sarmalayıcılara döner, sunucular silinmedi, yedek
`claude_desktop_config.json.bak11k`. Kuru test (Desktop env'iyle, Desktop config'inden):
`mcp-filesystem` 14 araç, `mcp-git` 12 araç — sarmalayıcısız sayılarla aynı.

Üç pin yeşil: (1) `git_reset {mode:"hard"}` → `git reset --hard` → block-destructive
exit 2 → istek sunucuya **iletilmiyor**; (2) `.cs` yazımından sonra
`user-settings|PostToolUse|Edit|Write` (dotnet-format) koşuyor; (3) `bin/**` okuma
`permissions.deny` gereği reddediliyor, `README.md` okuması geçiyor.

**Ölçülü sınır:** geçitte okuma yanıtının gövdesi claude-mem'e yazılmaz — her okumada
gitleaks koşmak geçidi kullanılamaz hale getirirdi, gitleaks'siz yazmak da sızıntı
riskidir. Yazan araçların girdisi kapıdan geçer.

### K6 · Headroom

**(a) Proxy kanıtlandı.** `GET /stats` → `agent_usage.agents[].models["-p"]` sayacı bir
`ajan` çağrısıyla +2 arttı → `claude -p` 6767'deki proxy'den geçiyor.

**(b) Sıkıştırma ölçümü** (`headroom mcp serve` → `headroom_compress`; HTTP tarafında
sıkıştırma rotası yok, `/compress` 404):

| içerik | karakter | ham jeton | sıkışmış | kazanç | süre |
|---|---|---|---|---|---|
| `docs/desktop-eslesme.md` (karışık markdown) | 33 480 | 11 755 | 11 754 | **%0** | 12,5 sn |
| tekrarlı worker log'u | 87 189 | 27 006 | 18 915 | **%30** | 4,5 sn |

Headroom **fail-open** çalışıyor: router tek-önbellek-ıskası 20 sn'yi aşınca içeriği
aynen geri veriyor (`ContentRouter single-cache-miss compression exceeded 20.0s;
failing open via PASSTHROUGH`) ve JSON zarfı yüzünden çıktı **büyüyor**. Ayrıca
`headroom mcp serve`in yapılandırılmış proxy'si `http://127.0.0.1:8787` — erişilemiyor
(çalışan proxy 6767'de). Bu yüzden `ciktiHazirla` kazancı ölçüp kazanç yoksa ham metni
kırpıyor; şişmiş zarf hiçbir zaman basılmıyor.

**(c) Desktop sohbet trafiğini yerel proxy'ye yöneltmek — yapısal sınır.** Belgelenen
`HTTPS_PROXY`/`HTTP_PROXY`/`NO_PROXY` desteği **Claude Code'a** aittir
(<https://docs.anthropic.com/en/docs/claude-code/corporate-proxy>); Desktop bağlamında
bile yalnız managed settings ve `~/.claude/settings.json`'dan okunur ve **Code
oturumunu** yönlendirir. Desktop **sohbet** istemcisi için belgelenmiş bir proxy ayarı
yok; Electron olarak işletim sistemi proxy'sini devralması tek yol olurdu ve bu
sistem geneli MITM demektir — tarifte yasak. Dokunulmadı.

### K7 · claude-design Desktop'ta

`tools/mcp-launch/claude-design.cmd` = obsidian kalıbı + `mcp-remote --transport
http-only`. `--transport` olmadan SSE'ye düşüp **405** alıyordu. Şimdi OAuth dinamik
istemci kaydına kadar geliyor ve tarayıcı onayını bekliyor → kuru test `INIT-YOK`.
**Adım Ömer'de:** Desktop yeniden başlatıldıktan sonra ilk `claude-design` çağrısında
açılan tarayıcı sayfasında izin verilecek; jeton `~/.mcp-auth` altında kalır.

### Yeniden başlatma

`claude_desktop_config.json` değişti (3 giriş). Değişikliğin etkili olması için
**Claude Desktop tamamen kapatılıp açılmalı** (tepsi simgesinden çıkış). Geri dönmek
için: `claude_desktop_config.json.bak11k` dosyasını üzerine kopyalamak yeterli.

## 11. KURULUM-11l · 22 Eyl 2026 — köprü kontrol 2 açıkları + claude-design köprüsü

### Köprü kontrol 2 — dört açık ve kök nedenleri

| açık | kök neden | düzeltme |
|---|---|---|
| `npx --no <paket>` paketi değil npx'in kendi bayrağını okuyor | npm'in npx argüman ayrıştırması (rtk'sız çağrıda da aynı: `11.17.0`) | `komutDenetle()` gerekli bayraktan sonra `--` ekler → `0.1.5` |
| katalog YAML blok skalerini açıklama sanıp basıyor | `aciklamaOku()` regex'i göstergeyi metin sayıyor | gösterge görülürse izleyen girintili ilk anlamlı satır alınır |
| `Read(./bin/**)` iç içe `bin/Debug`'ı kaçırıyor | `./` kalıbı proje kökünden çözülüyor | `tools/deny-11l.ps1`: `**/bin/Debug/**` · `**/bin/Release/**` · `**/obj/**` (`**/bin/**` EKLENMEZ — gstack altında 13 `bin` dizini okunamaz olurdu) |
| `durum` günlük satırı UTC gününü veriyor | `toISOString()` | `yerelGun()` — `Intl.DateTimeFormat("sv-SE", { timeZone: "Europe/Istanbul" })` |

### claude-design — yapısal sınır (iki yol da kapalı)

- **mcp-remote:** `claude_desktop_config.json`'daki `claude-design` girişi `mcp-remote --transport http-only` ile uca geliyor ama OAuth **dinamik istemci kaydında (DCR) 405** alıyor; uç kayıt kabul etmiyor, tarayıcı onayı tamamlanamıyor.
- **claude.ai özel bağlayıcı:** özel bağlayıcı (CIMD) uçları emekli; Desktop/claude.ai tarafından eklenebilecek bir adres kalmadı.
- Sonuç: Desktop'ın claude-design'a kendi başına bağlanması **yapısal olarak kapalı**. Açık olan tek kapı CC'nin kendi yetkili oturumu.

### K1 yolu — cc-kopru `tasarim.mjs`

1. 23 JSONSchema gerçek bir `tools/list` yanıtından yakalanıp `tools/cc-kopru/tasarim-semalar.json`'a yazıldı; sunucu bunları **birebir** yayınlar (elle/modelle yazılmadı).
2. Gövde tek ortak aktarıcıya gider: `claude -p --output-format stream-json --setting-sources "" --tools "" --system-prompt … --strict-mcp-config --allowedTools mcp__claude-design__<araç>`; CC'nin OAuth'lu bağlantısı yeniden kullanılır.
3. Sonuç modelin cümlesinden değil stream-json'daki `tool_result` bloğundan alınır. `--max-turns` CC CLI'da yok → ilk `tool_result` görülür görülmez süreç ağacı kapatılır.
4. Açılışta hiç süreç başlatılmaz (Desktop sunucuyu 4 süreçle açıyor); şema geçerliliği ilk çağrının zaten gelen `init` olayından denetlenir.
5. Test tohumu `CC_KOPRU_SAHTE_AKTARICI` yalnız `tools/cc-kopru/test/yardim/` altındaki var olan bir dosyayı kabul eder; başka yol ya da tanımsız değişken yok sayılır ve gerçek aktarıcı koşar (11l K1c).

### B2 kök nedeni — Headroom vekili aktarıcıyı kör ediyor

Gerçek uçta `list_projects` kırmızıydı: akışta hiç `tool_use` yok, model "aracım yok" diyordu.
Kök neden ortamda: **`ANTHROPIC_BASE_URL` Headroom'un yerel vekilini gösteriyor ve vekil isteğin `tools` dizisini tek bir arama aracına (`tool_search_tool_regex`) indiriyor** — model 23 claude-design aracını hiç görmüyor, dolayısıyla çağırmıyor.
Düzeltme: aktarıcı alt sürecinde `ANTHROPIC_BASE_URL` **düşürülür** (`delete ortam.ANTHROPIC_BASE_URL`, `tasarim.mjs`); köprünün kendi süreci ve diğer araçlar etkilenmez. Pin: değişken miras alınırsa `tool_use` gelmez (`tasarim.test.mjs`).

## 9. KURULUM-11m-A · 22 Eyl 2026 — Desktop token katmanı (köprü tarafı)

Ayrıntı: `docs/kurulum-11m.md`. Özet:

| kalem | değişiklik | token etkisi |
|---|---|---|
| K1 obsidian | başlatıcı `obsidian.mjs`'e döndü; açılışta bağlanmaz, şema önbelleğe yazılır | Obsidian kapalıyken 7 araç şeması yine yayınlanır; Desktop yeniden başlatma turu düşer |
| K2 git | `izinli.git` = grep · ls-files · show, önek kısaltmalı yasak bayrak kapısı | `komut` ile git okuması artık köprüden geçiyor — `ajan` alt oturumu açmaya gerek yok |
| K3 `oku` | claude-mem smart_* yerine `graphify-out/graph.json`; iskelet · sembol · aralik | dosyayı tam okumak yerine iskelet + tek sembol |
| K4 çıktı | `ciktiHazirla` sınıf kapısı (log/JSON sıkışır, markdown/kod sıkışmaz), `ham`, tam çıktı log yolunda, LOG_DIZIN'de son 200 dosya | ölçüm tablosu `docs/kurulum-11m.md` K4 |

`smart_*` CC'de de çalışmıyor; onarım = tree-sitter-cli + gramerler + C derleyici, ayrı karar.
