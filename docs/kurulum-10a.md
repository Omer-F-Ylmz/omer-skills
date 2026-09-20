# KURULUM-10a — CC tarafi (B) ve claude.ai paketleri (C)

64 kalemlik denetim tablosu ayri dosyada: `docs/kurulum-10.md`.
Olcum tarihi: 2026-09-20. Butun kanit komut ciktisindan.

## B. Claude Code

### B2-B3 · plugin durumu

| plugin | once | sonra |
| --- | --- | --- |
| `design@synced` | disabled | **loaded** |
| `plugin-dev@claude-plugins-official` | disabled | **enabled** |
| `claude-md-management@claude-plugins-official` | disabled | **enabled** |
| `engineering@synced` · `product-management@synced` · `data@synced` | disabled | disabled (dokunulmadi) |

Komut: `claude plugin enable <ad>` (settings.json'a dogrudan yazilmadi).

Plugin icerigi (kanit: dosya agaci):

- **plugin-dev**: 1 komut (`create-plugin`) · 3 agent (`agent-creator`, `plugin-validator`,
  `skill-reviewer`) · 7 skill · hook yok.
- **claude-md-management**: 1 komut (`revise-claude-md`) · 1 skill (`claude-md-improver`) · hook yok.

### B3 · tools/sync-off-10.ps1

sync-off-9 yontemi birebir: `-WhatIf` varsayilan · yalniz `anthropic-skills:<ad>` anahtari ·
bare-ad uretirse `throw` · idempotent · yedek `settings.json.bak10s` ·
yazim sonrasi skillOverrides disi fark dogrulanir.

**Mod a (varsayilan)** — iki plugin acilinca synced ile ciftlenen 8 ad, kosulsuz off:

```
hedef kume      : 8 ad (kural 1: 8 . kural 2: 0)
synced'de eksik : 0
eklenecek (N)   : 8  -> off (sonra): 276
bare-ad anahtar : 0
```

Anahtarlar: `anthropic-skills:` + agent-development · command-development · hook-development ·
mcp-integration · memory-md-improver · plugin-settings · plugin-structure · skill-development.

Uygulandi: `off: 268 -> 276 (+8)` · `skillOverrides disi fark: 0` ·
ikinci `-Apply` "degisiklik yok" dedi (idempotent).

**Mod b (`-Dist dist\yukle-10`)** — claude.ai yuklemesinden **sonra** kosulacak, simdilik yalniz -WhatIf:

```
hedef kume      : 11 ad (kural 1: 8 . kural 2: 3)
synced'de eksik : 8  (yeni/ paketleri henuz claude.ai'ye yuklenmedi — beklenen)
eklenecek (N)   : 8  -> off (sonra): 276
acik kalan      : 3  sdp, surec, web-design-guidelines
bare-ad anahtar : 0
```

`yeni/` 8 paket kosulsuz off (CC karsiliklari var); `replace/` 3 paket CC'de baska aktif
kopya olmadigi icin acik kaliyor.

### B4 · cli-anything

Kurulum tekrarlanmadi. Kanit:

```
cli-anything@cli-anything   Version: b1e9d53e9d0d   Scope: user   Status: ✔ enabled
$ cygpath -w /usr/bin/cygpath
C:\Program Files\Git\usr\bin\cygpath.exe
```

### B5 · headroom-desktop v0.9.16

`C:\Users\pc\Downloads` altina indirildi (kurulum Omer'de):

| dosya | boyut | sha256 | release digest |
| --- | --- | --- | --- |
| `Headroom_0.9.16_x64-setup.exe` | 8 613 288 | `4c9d4aa2…766b8b` | **ayni** |
| `Headroom_0.9.16_x64-setup.exe.sig` | 420 | `edecd8d4…4cf5840` | **ayni** |

- `Get-AuthenticodeSignature` → **Valid**, imzalayan `CN=Garm Tech BV, O=Garm Tech BV, L=Amsterdam, NL`.
- `.sig` turu: Authenticode degil — base64 govdesi `untrusted comment:` ile basliyor,
  yani Tauri updater'in minisign imzasi. Authenticode dogrulamasi exe'nin kendi imzasindan gelir.

**Port / ayar cakismasi (Omer'e uyari):** headroom-desktop sabit `127.0.0.1:6767` intercept
proxy'si acar (ikinci hop 6768, dolu ise 6768-6790 arasi), **ve kurulumda
`~/.claude/settings.json` icine `ANTHROPIC_BASE_URL=http://127.0.0.1:6767` env blogu yazar** —
yani Claude Code'u kendi proxy'sine yonlendirir. CC'deki `headroom` MCP'si
(`uvx --from headroom-ai[mcp]==0.37.0 headroom mcp serve`) stdio uzerinden calisir, port
kullanmaz; masaustu uygulamasi da kendi ~3 GB Python calisma zamanini ayri app-data dizinine
indirir. Yani **port cakismasi yok, ama settings.json env blogu CC'nin trafigini degistirir** —
kurulumdan once settings.json yedegi alinmali.

## C. claude.ai paketleri — `dist/yukle-10`

Uretim: `python tools/yukle10.py` (yukle8.py kalibi, `main()` `if __name__` altinda).
Ortak kapi her pakette kosuyor: name == zip kok klasoru · name'de claude/anthropic yok ·
description ≤ 200 · LF · nokta dosyasi yok · ≤ 30 MB · ic ice zip ve plugin manifest yok ·
synced adlariyla cakisma 0 (replace haric). **KAPI HATASI 0.**

| hedef | ad | acik bayt | zip bayt | kaynak |
| --- | --- | --- | --- | --- |
| yeni | `cli-anything` | 74 548 | 30 000 | cli-anything `openclaw-skill` + plugin HARNESS/commands |
| yeni | `plugin-dev-create-plugin` | 27 388 | 10 169 | plugin-dev `commands/create-plugin.md` |
| yeni | `plugin-dev-agent-creator` | 17 844 | 7 166 | plugin-dev `agents/agent-creator.md` + `validate-agent.sh` |
| yeni | `plugin-dev-plugin-validator` | 17 096 | 6 768 | plugin-dev `agents/plugin-validator.md` |
| yeni | `plugin-dev-skill-reviewer` | 16 491 | 6 612 | plugin-dev `agents/skill-reviewer.md` |
| yeni | `memory-md-management-revise-memory-md` | 12 759 | 5 234 | claude-md-management `commands/revise-claude-md.md` |
| yeni | `pixeljury` | 90 507 | 44 852 | npm -g pixeljury 0.1.5 (playwright HARIC) |
| yeni | `headroom-compress` | 101 883 | 33 083 | headroom-ai 0.37.0 `headroom/compression/` |
| replace | `web-design-guidelines` | 8 897 | 5 024 | synced SKILL.md + vercel-labs `command.md` |
| replace | `sdp` | 23 233 | 11 516 | `dist/sdp-claudeai.zip` |
| replace | `surec` | 13 233 | 6 975 | `dist/surec-claudeai.zip` |

Denetim: `python tools/skill_denetim.py dist/yukle-10` → **0 hata** (8 yanlis alarm).
Tam dist: `python tools/skill_denetim.py dist` → **387 zip · 0 hata** (gerileme yok).

### Paket notlari

- **cli-anything**: SKILL.md'deki `../cli-anything-plugin/HARNESS.md` yolu `references/HARNESS.md`
  olarak yeniden yazildi; 5 komut metni `references/commands/`'e, plugin LICENSE'i koke kondu.
  description 237 → 194 karakter.
- **plugin-dev / memory-md**: frontmatter yukle8 kalibiyla uretildi. Agent metinlerinin
  description'i `<example>` etiketleri iceriyordu — acili parantezler temizlendi, ~1170 karakter
  ≤ 200'e kisaltildi. claude.ai `name` icinde "claude" kelimesini reddettigi icin
  `revise-claude-md` → `memory-md-management-revise-memory-md` (8b'deki claude-md → memory-md ikamesi).
  `hook-development` skill'i claude.ai'de **yapisal** (hook CC'ye ozgu), paketlenmedi.
- **pixeljury**: `bin/`, `src/`, `node_modules/{pixeljury-core,pixeljury-vision}` gomulu;
  `playwright` ve `playwright-core` HARIC (18,5 MB). `rubric.md` → `references/rubric.md`.
  SKILL.md sandbox'in global playwright'ini `NODE_PATH=$(npm root -g)` ile kullanir,
  yalniz `--provider mock`, file:/// ve localhost ornegi var. MIT.
- **headroom-compress**: `headroom/compression/` alt agaci + bos `headroom/__init__.py`.
  `scripts/compress.py` CLI + `references/ornek.md` + LICENSE (Apache-2.0) + NOTICE.
- **web-design-guidelines**: `references/command.md` gomuldu, basliginda cekilis tarihi
  (2026-09-20) ve commit `e3d624baaf29dc1fc645aff3e38f03e564d2d6b1` (2026-08-18, MIT).
  SKILL.md artik "once yerel kopya, ag varsa tazele" diyor. CRLF → LF.
- **sdp / surec**: govde degismedi; yalniz description onu
  `Yalniz Divisima reposunda (C:\Users\pc\Desktop\smart\Divisima.Solution) kullanilir;
  baska repoda tetiklenmez.` onekiyle basliyor, 200 karaktere kirpildi. Bu iki skill
  **bu repoya kurulmadi** (Divisima'ya ozgu), yalniz claude.ai paketi olarak uretildi.

### Yerel duman testleri

**pixeljury** — repo klonu `C:\Projeler\.tmp-kurulum6\pixeljury`, gecici klasorde playwright
1.56.0 pinli (chromium build 1194), `examples/sloppy-saas/index.html`, `--provider mock`:

```
PIXELJURY_EXIT=0
  PixelJury  ·  rubric v0.1
  Design score: 30/100   — Broken or pure slop
  Hard fails
    ✗ Page is 1146px wider than the 390px viewport (horizontal scroll on mobile).  caps at 70
    ✗ Text contrast 1.0:1 (needs 4.5:1) — e.g. "✨ AI-powered productivity".  caps at 65
```

30 MB asilmadi (90 KB) ve chromium surum uyusmazligi cikmadi → REF'e dusulmedi, tam skill uretildi.

**headroom-compress** — zip gecici klasore acildi, gomulu agac import edildi:

```
$ python scripts/compress.py graphify-out/graph.json --cikti kisa.txt
girdi 495961 kr . cikti 477273 kr . oran 0.962 . token 123990 -> 119318 (%3.8 tasarruf)
HEADROOM_EXIT=0
```

Ek olcumler: `docs/kurulum-7.md` %27,9 · `tools/skill_denetim.py` %32,4 tasarruf.
Tespit yolu dogrulandi: `FallbackDetector → ContentType.JSON → JSONStructureHandler`
(magika yok, `tree_sitter` yok, ikisi de `ImportError` ile yedege dustu).
`_core.pyd`, onnx modeli ya da ag cagrisi **olmadi** → DUR kosulu tetiklenmedi.

Dogrudan olcum: yogun/benzersiz JSON'da kazanc dusuk (%3,8), markdown ve Python'da %28-32.
Kompress motoru pakette olmadigi icin `_simple_compress` yedegi devrede.

## Sapmalar

1. **headroom "duzlestirme"**: `headroom/compression/` alt agaci duz bir klasore tasinmadi;
   `headroom/compression/` paket yolu korundu (bos bir `headroom/__init__.py` ile). Neden:
   alt agac kendi icinde `from headroom.compression.X import ...` mutlak import kullaniyor;
   duzlestirmek 20'den fazla import satirini yeniden yazmayi gerektirirdi. Etki yok —
   zip'te yalniz compression alt agaci var, ust paketin geri kalani cikarildi.
2. **`sync-off-10.ps1` mod a uygulandi** (yalniz -WhatIf degil): iki plugin bu dalgada acildi,
   ciftlenme hemen olustu. Mod b claude.ai yuklemesinden sonra Omer'de.
3. **pixeljury `--out`**: SKILL.md'de sandbox ciktisi `/mnt/user-data/outputs/pixeljury`
   olarak ornekleniyor; paket bunu zorlamaz, `--out` verilmezse calisma dizinine yazar.

## Omer'e dusen komutlar

```powershell
# 1) headroom-desktop kurulumu (once settings.json yedegi al — kurulum env blogu yazar)
Copy-Item "$env:USERPROFILE\.claude\settings.json" "$env:USERPROFILE\.claude\settings.json.bakHD" -Force
Start-Process "C:\Users\pc\Downloads\Headroom_0.9.16_x64-setup.exe"

# 2) dist\yukle-10\yeni (8 zip) ve dist\yukle-10\replace (3 zip) claude.ai'ye yuklendikten sonra
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Projeler\omer-skills\tools\sync-off-10.ps1" -Dist "C:\Projeler\omer-skills\dist\yukle-10"
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Projeler\omer-skills\tools\sync-off-10.ps1" -Dist "C:\Projeler\omer-skills\dist\yukle-10" -Apply
```

---

# KURULUM-10a-FIX — claude.ai denetim bulgulari

claude.ai sandbox'ta (Node 22.22.2, global playwright 1.56.0, `/mnt/skills` salt okunur,
dosyalar 644, bash bloklari arasi kabuk durumu yok) uc paket dustu. Uc kok neden, uc
duzeltme, bir de bundan sonraki her partide kosulacak duman testi araci.

Yeni surumler `dist/yukle-10b/replace/`; dusen surumler `C:\Projeler\.tmp-kurulum6\eski-10a`.

## F1 · pixeljury — uc ayri kusur

| # | Belirti | Kok neden | Duzeltme |
| --- | --- | --- | --- |
| a | `bin/pixeljury.js:15` ENOENT | `yukle10.py` `p_pixeljury` yalniz `bin/` ve `src/` alt agaclarini geziyordu; kok dosyalar hic kopyalanmiyordu. `bin/pixeljury.js` surumu `../package.json`'dan okuyor, ayrica `"type": "module"` ESM cozumlemesi icin bu dosyada. | Kok `package.json` (ozgun, 0.1.5) zip'e eklendi. |
| b | "Playwright is not installed" | `pixeljury-core/src/render.js:46` `await import("playwright")` — ESM `NODE_PATH`'i yok sayar, yalnizca dizin yurur. | SKILL.md blogu skill'i `/tmp/pixeljury-run`'a kopyalayip global playwright'i `node_modules/playwright` olarak bagliyor. |
| c | rubric bulunamiyor | `src/rubric-loader.js` sirasi `$PIXELJURY_RUBRIC` -> `cwd/rubric.md` -> modul dizininden yukari; paket rubric'i `references/` altinda tuttugu icin ucunde de yok. | Blok `PIXELJURY_RUBRIC=/tmp/pixeljury-run/references/rubric.md` veriyor. |

Calistirma artik **tek blok** (kabuk durumu korunmuyor) ve `URL`/`OUT` ile disaridan
parametrelenebiliyor, bu sayede duman testi blogu birebir kosabiliyor.

Duman sonucu: exit 0 . `score.json` `critique.md` `fix-prompt.md` `screenshot.png`
`screenshot-390.png` . `examples/sloppy-saas` icin **3 hard fail**, skor 30/100.
(Tarifin elle olcumu 49/100 idi; fark playwright surumunden — yerelde 1.63.0,
sandbox'ta 1.56.0. Kabul olcutu exit 0 + cikti + hard-fail >= 1, ucu de saglandi.)

## F2 · headroom-compress — JSON dizisinde %0

**Kok neden ust akista, pakette degil.** `headroom/compression/universal.py`
`_compress_with_mask` yalnizca **50 karakterden uzun** yapisal-olmayan parcalari
sikistiriyor; `json_handler.py` anahtarlari, parantez/virgul/iki noktayi, bool ve null
degerleri, kisa sayilari ve **20 karaktere kadar** metin degerlerini yapisal sayip
koruyor. Alanlari kisa olan bir kayit dizisinde sikistirilabilir parca kalmiyor.

Olculen (400 kayit x 3 order + meta, `random.seed(1)`):

| girdi | boyut | oran | tasarruf |
| --- | --- | --- | --- |
| JSON dizisi, kisa alanlar, indent=2 | 252 KB | 1.000 | %0 |
| JSON dizisi, kisa alanlar, kompakt | 140 KB | 1.000 | %0 |
| ayni dizi, kayit basina 40 kr metin degeri | - | 1.000 | %0 |
| ayni dizi, 50 kr | - | 0.763 | %23.7 |
| ayni dizi, 80 kr | - | 0.646 | %35.4 |
| ayni dizi, 200 kr | - | 0.472 | %52.8 |
| 3000 satirlik uygulama logu (60 ERROR) | 260 KB | 0.703 | %29.7 |

**Gomme denendi, olmuyor.** `compression/` disindaki tekrar tabanli sikistiricilar saf
Python degil: `transforms/kompress_compressor.py` torch + transformers + onnxruntime +
safetensors + huggingface_hub istiyor ve model indiriyor (olcumde 20 s zaman asimina
girip kalani aynen birakti, %35.6); `transforms/smart_crusher.py` derlenmis
`headroom._core` uzantisina bagli. Ikisi de 30 MB sinirini ve "ag yok" kisitini asiyor.
Karar: **gomulmedi**, olculen sinir `SKILL.md` "Sinirlar" ve `references/ornek.md`
"JSON siniri" bolumlerine yazildi; paketin description'i da "uzun metinli JSON" diyecek
sekilde daraltildi.

**ERROR satiri.** Olculen 3000 satirlik ornekte **60 -> 60**, kesilme olmadi. Ama
mekanizma tarifin gordugu kesilmeyi aciklyor: sikistirma her parcanin **ortasini**
atiyor (bas 2/3 + `...[compressed]...` + son 1/3) ve kesme noktasi karakter sayisina
gore belirleniyor; LOG icin isleyici `noop`, log seviyesi ozel olarak korunmuyor.
Seviye etiketinin kurtulmasi satir bicimine bagli — upstream davranisi, `SKILL.md`
"Sinirlar"a ve `ornek.md` "Notlar"a birer satir eklendi.

Ek olarak `scripts/compress.py` artik `sys.dont_write_bytecode = True` ile basliyor:
duman testi salt okunur kopyaya `__pycache__` yazildigini yakaladi.

## F3 · plugin-dev-agent-creator — Permission denied

Kaynak metin `scripts/validate-agent.sh agents/[identifier].md` diye dogrudan cagiriyordu;
644'te calismaz, ayrica cwd skill koku degil. `p_pdev`'e `degis` parametresi eklendi
(desen kaynakta yoksa `SystemExit` — upstream metni degisirse sessizce gecmesin), cagri:

```bash
SKILL=$(ls -d /mnt/skills/*/plugin-dev-agent-creator | head -1)
bash "$SKILL/scripts/validate-agent.sh" agents/[identifier].md
```

644 kopyada `bash "$SKILL/scripts/validate-agent.sh"` usage basiyor (exit 1, kullanim
metni). Blok sablon oldugu icin duman testinde beklenen exit kodu 1
(`--bekle plugin-dev-agent-creator=1`).

## F4 · tools/duman_claudeai.py

yukle-N zip'ini gecici dizine acar, dosyalari 644 / dizinleri salt okunur yapar,
`SKILL.md`'deki her ```bash blogunu **ayri kabukta** kosar, sonra salt okunur kopyaya
yazilip yazilmadigini karsilastirir. `/mnt/skills/*/` deseni acilan kopyaya cevrilir.

Windows'un sandbox'tan ayrildigi yerler ve ne yapildigi:

| fark | cozum |
| --- | --- |
| `chmod 644` exec bitini kaldirmiyor, Git Bash shebang'e bakip calistiriyor | dogrudan betik cagrilari ayrica **statik** denetleniyor (`statik_denetim`) |
| dizin salt okunur zorlanmiyor | blok oncesi/sonrasi dosya listesi karsilastirmasi |
| Git Bash `ln -s` dizin hedefini POSIX yola cevirip yaziyor, Node cozemiyor | PATH'e `ln` shim'i (Python `os.symlink`) |
| yerelde playwright global kokte degil, `pixeljury/node_modules` altinda | PATH'e `npm` shim'i: `npm root -g` taklit global koku basiyor, oraya symlink kurulur |

Kullanim:

```bash
python tools/duman_claudeai.py dist/yukle-10b/replace \
  --bekle plugin-dev-agent-creator=1 \
  --env "URL=file:///C:/Projeler/.tmp-kurulum6/pixeljury/examples/sloppy-saas/index.html" \
  --env "OUT=/tmp/pj" --env "GIRDI=/tmp/buyuk.log"
```

Sonuc: `3 zip . 0 sorunlu`.

## Sapmalar

1. **644 exec biti yerelde dogrulanamadi.** Windows'ta `chmod 644` calistirma yetkisini
   kaldirmiyor, bu yuzden F3'un asil belirtisi (Permission denied) yerelde uretilemez.
   Dogrulanan: yeni cagri bicimi exec bitine ve cwd'ye bagli degil, `bash` ile usage
   basiyor. Asil belirti sandbox'ta kapanmis sayilir.
2. **JSON ureticisi birebir degil.** Tarif indent=2 icin 227 KB / kompakt 122 KB veriyor,
   yeniden uretilen ayni yapidaki dosya 252 KB / 140 KB. Sonuc degismiyor: iki bicimde de
   oran 1.000. Sinir sayilari yeniden uretilen dosyayla olculdu.
3. **Log ornegi farkli.** Tarif %68.7 gormus, yeniden uretilen 3000 satirlik log %29.7.
   Tasarruf satir uzunluguna ve tekrara bagli; ikisi de "%30 civari ve ustu" bandinda.
   ERROR kesilmesi bu ornekte olusmadi (60 -> 60), mekanizma yine de belgelendi.
4. **`headroom-compress` ve `pixeljury` SKILL.md bloklarina `${VAR:-varsayilan}`
   parametreleri eklendi.** Gerekce: duman testinin blogu *birebir* kosabilmesi icin
   girdi yolunun disaridan verilebilmesi gerekiyordu. Kullanici icin davranis degismiyor,
   varsayilanlar sandbox yollari.
