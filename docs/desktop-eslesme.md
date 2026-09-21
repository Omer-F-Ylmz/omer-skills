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
