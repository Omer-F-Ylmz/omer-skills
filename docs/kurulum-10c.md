# KURULUM-10c — Vercel kılavuzu + CLI-Anything + 21st, iki tarafa

21 Eyl 2026. Taban: b53d37a.

Üç dış kaynak global `CLAUDE.md`'ye satır eklemeden skill'lere indi. Kural iki yerde
yazılmadı: çift olan tek yerde durur, öbürü atıf yapar.

## K1 · Vercel Web Interface Guidelines → frontend-craft referansı

`plugins/frontend-craft/skills/frontend-craft/references/vercel-web-interface.md` (164 satır).
Kaynak `vercel.com/design/guidelines` → "Download AGENTS.md" →
`vercel-labs/web-interface-guidelines` `AGENTS.md`, MIT, commit `e3d624ba` (18 Ağu 2026).

`web-design-guidelines` skill'inin `references/command.md` dosyası aynı depodan, aynı
commit'ten üretiliyor. 107 maddenin **6'sı birebir çift** çıktı (normalize edip
`comm -12`); o 6 madde referanstan çıkarıldı, başlıkta adlarıyla ve atıfla duruyor:
placeholder `…` · `prefers-reduced-motion` · flex/grid vs JS ölçümü · `&nbsp;` ·
kritik font preload · `theme-color`. Kalan 101 madde referansta.

1.5.3'ün 5 Forms/touch kabul kuralı (Bölüm 4) olduğu gibi kaldı; kabul kriterine yeni
kural eklenmedi. ÇEKİRDEK'e tek satır girdi.

## K2 · CLI-Anything → platformdan bağımsız claude.ai skill'i

**Kaynak sorusu kapandı.** `gh api repos/HKUDS/CLI-Anything/compare/main...KitJacky:cli-anything:main`
→ `ahead_by 0, behind_by 716`. *KitJacky fork'u upstream'den 0 commit ileride, 716 commit
geride — içerik farkı yok, yalnız eskimiş ayna; kaynak HKUDS/CLI-Anything kalır.*

Bu önemliydi: CC'deki marketplace klonu o fork'tan geldiği için `HARNESS.md` 503 satır,
`codex-skill/SKILL.md` 164 satır eskiydi, `registry.json` 18 CLI gösteriyordu (upstream 79).
`tools/yukle10.py` artık upstream klonundan okuyor (`CLI_UP`, env `CLI_ANYTHING_KLON`);
klon yoksa paket üretimi açık hatayla durur.

SKILL.md gövdesi codex-skill kalıbına dayanıyor ama platform adı geçmiyor (claude.ai ile
CC ortak metin). Bölümler: nerede ne yapılır · kaynak sırası · 7 faz · HARNESS dersleri ·
modlar · API setini tek CLI'da toplama · CLI-Hub tetikleyicileri · Windows ölçümü.

Platform sınırı metne girdi: claude.ai/Desktop'ta hedef yazılım yok → yalnız plan ve
HARNESS incelemesi; üretim ve koşu CC'de `/cli-anything:cli-anything`, `:refine`,
`:test`, `:validate`, `:list`.

Tetikleyici tablosu: diyagram → `drawio`/`mermaid` · belge-PDF → `libreoffice` ·
SVG → `inkscape` · görsel → `gimp`.

### Windows ölçümü (tahmin değil)

```text
git clone -c core.autocrlf=false https://github.com/HKUDS/CLI-Anything.git \
  C:\Projeler\.tmp-kurulum6\HKUDS__CLI-Anything          # 810c18b, 21 Ağu 2026
cd mermaid/agent-harness && python -m pip install -e .
  -> Successfully installed cli-anything-mermaid-1.0.0 click-8.5.0
     prompt-toolkit-3.0.53 wcwidth-0.8.4

$ command -v cli-anything-mermaid
/c/Users/pc/AppData/Local/Programs/Python/Python312/Scripts/cli-anything-mermaid

$ cli-anything-mermaid --help        -> Usage + 5 komut (diagram export project repl session)
$ cli-anything-mermaid --json project samples
{"flowchart":"flowchart TD\n  A[Start] --> B{Ready?}...","sequence":...,"er":...}
```

- Python 3.12.10, pip 25.0.1. Giriş noktası `Python312/Scripts`'e kuruluyor ve Git Bash
  PATH'inde çözülüyor; sarmalayıcı gerekmedi.
- Yol dönüşümü: `--output /tmp/m.json` dosyayı `%TEMP%\m.json` altına yazdı — POSIX yolu
  MSYS katmanı çeviriyor, `cygpath -w` ile açık çevirmek aynı sonucu veriyor. Betik
  Windows Python'u; dönüşümü yapan kabuk.
- `export render` mermaid.ink'e çıkar, ölçümde kullanılmadı. Kurulan mermaid harness'ı
  kaldı; başka hazır CLI kurulmadı.

## K3 · 21st akışı → frontend-craft referansı

`references/21st-akis.md` (31 satır). Adımlar: referans çıkarma `get_inspiration` →
`record_inspiration_feedback` · bileşen `search`/`search_picker` → `get_component` ·
tema `get_theme` · logo `search_logo` · taslak `iterate_generation` →
`get_generation_job`/`get_generation`/`get_take` · kayıt `bookmark`/`add_to_list` ·
kota `get_usage`.

**Sapma:** tarifteki `iterate_generation` canlı `tools/list`'te **yok** — `generate` de
yok. İkisi de uydurma değil: `get_usage` ve `get_generation_job` araçlarının kendi
şemalarında adları geçiyor, `aiGenerationEnabled` doğru olduğunda listeye giriyorlar.
Referansta ikisi de "AI-kapılı" olarak işaretli. 16 ad denetlendi, listede olmayan 0.

`21st-ui` skill'ine dokunulmadı. frontend-craft'ta Bölüm 10 (bileşen) ve Bölüm 11 (yön
keşfi) birer satırlık atıf aldı.

## K4 · Paket

`frontend-craft` **1.5.5**. Yan bulgu: `plugin.json` 1.5.4, `marketplace.json` 1.5.3
idi — 11b'de plugin bump'ı marketplace'e yansımamış; ikisi hizalandı.

`dist/yukle-10c/replace/`: `frontend-craft.zip` (24 KB) · `cli-anything.zip` (45 KB).
Üretim: `YUKLE10_OUT=dist/yukle-10c python tools/yukle10.py frontend-craft cli-anything`.
İkisi de `replace`; `cli-anything` synced'de kayıtlı, `kapi()` başka türlü reddeder.

| Kapı | Sonuç |
| --- | --- |
| `skill_denetim.py dist/yukle-10c` | 2 zip · **0 hata** · 0 CRLF · 0 `~/.claude` uyarısı |
| `duman_claudeai.py dist/yukle-10c/replace` | 2 zip · **0 sorunlu** (0 bash blok) |
| `cli-anything.zip` içinde "OpenClaw" | **0** |
| description | `cli-anything` 159 · `frontend-craft` 195 (sınır 200) |
| 21st araç adları | 16/16 gerçek listede |
| frontend-craft SKILL.md | +3 −2 → **net +1 satır** (tavan 10) |
| gitleaks (git modu, 84 commit) | **0 bulgu** |

**sync-off:** `tools/sync-off-10.ps1 -Dist dist/yukle-10c` (-WhatIf) →
`eklenecek (N) : 0`. `anthropic-skills:frontend-craft` ve `anthropic-skills:cli-anything`
zaten off (toplam 328). `-Apply` gerekmedi. Betik `cli-anything`'i "açık kalan"
sayıyor çünkü CC'deki plugin skill değil **komut** sağlıyor (`cli-anything` adlı SKILL.md
dizini yok); override elle konmuş ve doğru.

## Yükleme

claude.ai → Customize → Skills → Add → **Replace**, sırayla:
`dist/yukle-10c/replace/frontend-craft.zip`, `dist/yukle-10c/replace/cli-anything.zip`.
Kök dizindeki eski `dist/frontend-craft.zip` bayat (1.5.4'ün iki ÇEKİRDEK satırı yok),
kullanılmaz.

## Yan bulgular

- `gitleaks detect --no-git` 1 bulgu veriyor: `generic-api-key`,
  `graphify-out/cache/stat-index.json:1`. Dosya `.gitignore`'da, git'te takip edilmiyor,
  graphify'ın ürettiği önbellek. Git modu taraması temiz.
- `HARNESS.md` içinde "Codex" 1 kez geçiyor — upstream metninde ajan örneği
  ("Claude Code, Codex, etc."), skill'in platform bağı değil.
- `duman_claudeai.py` SKILL.md'deki her ` ```bash ` bloğunu ağsız sandbox'ta koşuyor.
  Windows ölçüm dökümü bu yüzden ` ```text ` çitinde: koşulacak adım değil, kanıt.
