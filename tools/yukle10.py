"""KURULUM-10 C: claude.ai paketleri -> dist/yukle-10/{yeni,replace}.

Kaynaklar yerel kurulumdan okunur (plugin cache, npm -g, uv tool, synced skill, dist zip).
Ortak kapi (kapi()): name == zip kok klasoru . name'de claude/anthropic yok .
description <= 200 . LF . nokta dosyasi yok . <= 30 MB . ic ice zip/plugin manifest yok .
synced adlariyla cakisma 0 (replace haric).
"""
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yukle8 import ATLA_DIR, TEXT_EXT, duzelt_metin, frontmatter  # noqa: E402

H = Path(os.path.expanduser("~/.claude"))
REPO = Path(r"C:\Projeler\omer-skills")
OUT = Path(os.environ.get("YUKLE10_OUT") or REPO / "dist/yukle-10")
TMP = Path(os.environ.get("YUKLE10_TMP") or r"C:\Users\pc\AppData\Local\Temp\yukle10tmp")
SYNC = H / "skills/synced/924f0f64-fcbf-4e91-8e2f-e62bad8245c0_5bf6859c-713e-459a-9126-5fb1dcc493b6"
CLI_MK = H / "plugins/marketplaces/cli-anything"
# 10c: CC marketplace klonu KitJacky fork'undan, upstream'den 716 commit geri.
# Kaynak upstream klonu; yoksa p_cli_anything acikca durur.
CLI_UP = Path(os.environ.get("CLI_ANYTHING_KLON") or r"C:\Projeler\.tmp-kurulum6\HKUDS__CLI-Anything")
FC_SKILL = REPO / "plugins/frontend-craft/skills/frontend-craft"
PJ_KLON = Path(r"C:\Projeler\.tmp-kurulum6\pixeljury")
WIG_REPO = "vercel-labs/web-interface-guidelines"
YASAK = re.compile(r'[\x00-\x1f\x7f\\:*?"<>|@]')


def kurulu(ad):
    d = json.loads((H / "plugins/installed_plugins.json").read_text(encoding="utf-8"))["plugins"]
    return Path(d[ad][0]["installPath"])


def kabuk(*args):
    # shell=True yok: Git Bash PATH'i cmd.exe'ye gecmiyor, .cmd shim'i which ile cozulur
    exe = shutil.which(args[0])
    if not exe:
        raise SystemExit("bulunamadi: " + args[0])
    return subprocess.run((exe,) + args[1:], capture_output=True, text=True,
                          check=True).stdout.strip()


def yaz(p, metin):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(metin.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))


def kopyala(src, dst, ad, rapor):
    """Kaynak agaci stage'e kopyalar; nokta dosyasi / manifest / zip disarida kalir."""
    for kok, dirs, files in os.walk(src):
        dirs[:] = sorted(d for d in dirs if d not in ATLA_DIR and not d.startswith("."))
        for f in sorted(files):
            sp = Path(kok) / f
            rel = sp.relative_to(src)
            if f.startswith(".") or f == "plugin.json" or sp.suffix.lower() == ".zip":
                continue
            if YASAK.search(rel.as_posix()):
                rapor.append(ad + ": YASAK-KARAKTER atlandi " + rel.as_posix())
                continue
            b = sp.read_bytes()
            if sp.suffix.lower() in TEXT_EXT or b.startswith(b"#!"):
                try:
                    yaz(dst / rel, duzelt_metin(b.decode("utf-8"), ad))
                    continue
                except UnicodeDecodeError:
                    pass
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            (dst / rel).write_bytes(b)


def fm_lf(p, ad, rapor):
    """yukle8.frontmatter write_text kullaniyor; Windows'ta CRLF yaziyor -> LF'e cevir."""
    frontmatter(p, ad, rapor)
    yaz(p, p.read_text(encoding="utf-8"))


def md_skill(stage, ad, kaynak_md, rapor):
    """Komut/agent markdown'ini SKILL.md'ye cevirir (frontmatter yukle8 kalibi)."""
    yaz(stage / "SKILL.md", duzelt_metin(kaynak_md, ad))
    fm_lf(stage / "SKILL.md", ad, rapor)


# --------------------------------------------------------------- paketler
# 10c: kaynak upstream (HKUDS). KitJacky fork'u 0 ileri / 716 geri -> icerik farki yok,
# ama CC marketplace klonu o fork'tan geldigi icin HARNESS.md 503 satir eski.
# Govde codex-skill kaliba dayanir; platform adi gecmez (claude.ai ile CC ortak metin).
CLI_MD = '''---
name: cli-anything
description: "GUI uygulamasini ya da kaynak deposunu durum tutan, --json konusan bir komut satirina ceviren CLI-Anything harness yontemi: kurma, gelistirme, test, dogrulama."
---

# CLI-Anything

Insan icin yazilmis bir yazilimi, ekransiz bir ajanin kullanabilecegi durum tutan bir
CLI'a cevirme yontemi. Uretilen harness Python + Click'tir: `cli_anything.<yazilim>` ad
alani paketi, alt komut yokken REPL, her komutta `--json`, destekleyen yazilimda
undo/redo.

## Nerede ne yapilir

| Ortam | Yapilabilen | Yapilamayan |
| --- | --- | --- |
| claude.ai / Desktop | plan, mimari karari, `references/HARNESS.md` incelemesi, mevcut harness'in kod okumasi, bosluk analizi | hedef yazilim kurulu degil: kurma, kosma, test, render |
| Claude Code | uretim ve kosu: `/cli-anything:cli-anything`, `/cli-anything:refine`, `/cli-anything:test`, `/cli-anything:validate`, `/cli-anything:list` | - |

claude.ai/Desktop'ta bu skill **yalniz plan ve HARNESS incelemesi** icindir. "Harness kur"
istegi geldiginde cikti bir plandir; uretim ve kosu CC'deki komutlara havale edilir.

## Kaynak sirasi

1. `references/HARNESS.md` - yontemin tam kaynagi, uygulamadan once okunur.
2. `references/commands/` altindaki calisilan modun sartnamesi.
3. `references/guides/` altindaki konu dosyasi - yalniz o konuya dokunuluyorsa.
4. Hicbiri okunamiyorsa asagidaki ozet kurallar.

## Yontem - 7 faz

1. **Kod tabani analizi** - arka uc motoru bul (Shotcut icin MLT, GIMP icin ImageMagick),
   GUI eylemlerini API cagrilarina esle, veri modelini ve proje dosya bicimini cikar,
   yazilimin kendi CLI'larini (`melt`, `ffmpeg`, `convert`) envantere al, undo/redo
   komut sistemini katalogla.
2. **CLI mimarisi** - etkilesim modeli (durum tutan REPL + tek atislik alt komut, ikisi
   birden), komut gruplari (proje, cekirdek islem, ice/disa aktarim, ayar, oturum),
   durum modeli ve ciktinin insan/makine (`--json`) ikiligi.
3. **Uygulama** - once veri katmani, sonra `info`/`list`/`status` gozlem komutlari, sonra
   mutasyon komutlari, sonra `utils/<yazilim>_backend.py` ile gercek yazilim cagrisi,
   sonra render/export, sonra kilitli oturum yazimi, en son REPL.
4. **Test plani** - kod yazmadan once `TEST.md`: dosya basina planlanan test sayisi,
   birim plani, E2E plani, gercekci is akisi senaryolari.
5. **Test uygulamasi** - `test_core.py` birim, `test_full_e2e.py` gercek dosya + gercek
   arka uc; kurulu `cli-anything-<yazilim>` komutu subprocess ile de kosulur.
6. **Test dokumani** - `TEST.md`'nin ikinci yarisi: kapsam, senaryolar, gercek kosu
   ciktisi. (6.5: pakete giren CLI'a ozel `SKILL.md` uretimi.)
7. **Paketleme** - `find_namespace_packages(include=["cli_anything.*"])`, `cli_anything/`
   altinda `__init__.py` yok, `console_scripts` ile `cli-anything-<yazilim>`.

## HARNESS.md dersleri

- **Gercek yazilimi cagir, yeniden yazma.** Pillow ile GIMP taklidi, Blender cagirmadan
   bpy uretimi oyuncaktir. Dogru yol: `libreoffice --headless --convert-to`,
   `blender --background --python`, `inkscape --actions`, `melt`, `sox`.
- **Yazilim sert bagimliliktir.** Kurulu degilse CLI net hatayla durur; yedek kutuphaneye
   sessizce dusmez.
- **Render bosluguna dikkat.** Cogu GUI efekti render aninda motorda uygulanir; proje
   dosyasini degistirmek yetmez, ciktinin kendisi programatik olarak dogrulanir.
   "Hatasiz kostu" yeterli degildir.
- **Yerel bicimi dogrudan isle** (MLT XML, ODF, SVG); ara dosyayi uret, render'i yazilima
   birak.
- **Yuksek sesle hata ver** - ajan kendini duzeltecekse mesaj belirsiz olamaz.
- **Idempotent ol, gozlem komutu ver** (`info`, `list`, `status`); ajan degistirmeden once
   bakar.
- **Oturum dosyasini kilitle.** `open("w")` kilit alinmadan dosyayi kirpar; `"r+"` ile ac,
   kilidi al, kirpmayi kilidin icinde yap.

## Modlar

- **Build** - yeni harness. `references/commands/cli-anything.md`.
- **Refine** - mevcut harness; once komut/test envanteri, sonra hedef yazilima karsi
  bosluk analizi. Kullanici acikca istemedikce komut silinmez.
  `references/commands/refine.md`.
- **Test** - testler once planlanir, sonra yazilir. `references/commands/test.md`.
- **Validate** - ad alani duzeni, kurulabilir giris noktasi, `--json`, REPL varsayilani,
  dokuman ve test. `references/commands/validate.md`.
- **List** - kurulu/uretilmis harness kesfi. `references/commands/list.md`.

## API setini tek CLI'da toplamak

Yontem yalniz masaustu GUI'si icin degil; bir web servis ailesini tek harness altinda
toplamak da ayni kaliptir. Servisin HTTP API'si "arka uc" yerine gecer:

- Komut gruplari API kaynaklarina esler (proje/kaynak/is/cikti).
- Kimlik tek yerde: ortam degiskeni (`ANYGEN_API_KEY`, `NOVITA_API_KEY`, `EXA_API_KEY`
  gibi), CLI icine gomulmez.
- Oturum dosyasi cagrilar arasi baglami tutar; boylece ajan her komutta butun girdiyi
  yeniden gondermez.
- Her komut `--json` doner; zincirleme `jq`/pipe ile yapilir.
- Ag hatasi sessizce yutulmaz; hiz siniri ve yeniden deneme tek yerde toplanir.

Tek CLI'da birden cok servis gerekiyorsa her servis ayri komut grubu olur; ad alani
paketi sayesinde `cli-anything-<ad>` paketleri ayni ortamda yan yana kurulur.

## Hazir CLI tetikleyicileri (CLI-Hub)

Yeni harness kurmadan once hazir olani var mi diye bakilir:

| Proje ihtiyaci | Hazir CLI |
| --- | --- |
| diyagram, akis semasi | `cli-anything-drawio` - `cli-anything-mermaid` |
| belge, PDF, sunum, tablo | `cli-anything-libreoffice` |
| SVG, vektor | `cli-anything-inkscape` |
| gorsel duzenleme, raster | `cli-anything-gimp` |

Kurulum kalibi (`<ad>` = drawio, mermaid, libreoffice, inkscape, gimp):

```text
pip install git+https://github.com/HKUDS/CLI-Anything.git#subdirectory=<ad>/agent-harness
```

`drawio`, `libreoffice`, `inkscape`, `gimp` hedef yazilimin kurulu olmasini ister;
`mermaid` istemez (durum dosyasi + mermaid.ink render URL'si). Tam liste depodaki
`registry.json`.

## Windows (olculmus)

Ortam: Windows 11, Git Bash, Python 3.12.10, pip 25.0.1. Asagidakiler kosulmus ve
ciktilari alinmistir; claude.ai kum havuzunda kosturulacak adim degildir.

Klon (CRLF bozmasin diye acikca kapatilir) ve tek harness kurulumu:

```text
git clone -c core.autocrlf=false https://github.com/HKUDS/CLI-Anything.git <klon>
cd <klon>/mermaid/agent-harness && python -m pip install -e .
  -> Successfully installed cli-anything-mermaid-1.0.0 click-8.5.0
     prompt-toolkit-3.0.53 wcwidth-0.8.4
```

Giris noktasi PATH'e kendiliginden girer; Git Bash'te ayri bir sarmalayici gerekmez:

```text
$ command -v cli-anything-mermaid
/c/Users/<kullanici>/AppData/Local/Programs/Python/Python312/Scripts/cli-anything-mermaid

$ cli-anything-mermaid --help
Usage: cli-anything-mermaid [OPTIONS] [COMMAND] [ARGS]...
  CLI harness for Mermaid Live Editor state files and renderer URLs.
Options:
  --json          Emit machine-readable JSON
  --project TEXT  Open a Mermaid project file
  --dry-run       Run command without saving changes to disk
Commands:
  diagram  export  project  repl  session
```

Ag gerektirmeyen `--json` komutu (`export render` mermaid.ink'e cikar, bu cikmaz):

```text
$ cli-anything-mermaid --json project samples
{"flowchart":"flowchart TD\\n  A[Start] --> B{Ready?}\\n ...",
 "sequence":"sequenceDiagram\\n  participant U as User\\n ...",
 "er":"erDiagram\\n  USER ||--o{ ORDER : places\\n ..."}
```

Yol donusumu: Git Bash argumandaki POSIX yolu MSYS katmaninda Windows yoluna cevirir,
`--output /tmp/m.json` dosyayi `C:\\Users\\<kullanici>\\AppData\\Local\\Temp\\m.json`
altina yazar - `cygpath -w` ile acikca cevirmek ayni sonucu verir. Betik Windows
Python'u oldugu icin POSIX yolunu kendisi cozmez; donusumu yapan kabuktur.

## Paket icerigi

- `references/HARNESS.md` - yontemin tam kaynagi.
- `references/commands/` - build, refine, test, validate, list sartnameleri.
- `references/guides/` - oturum kilitleme, auto-save/dry-run, MCP arka uc, onizleme,
  filtre cevirisi, zaman kodu, PyPI, SKILL.md uretimi.
- `LICENSE` - Apache-2.0 (HKUDS/CLI-Anything).
'''


def p_cli_anything(stage, ad, rapor):
    plug = CLI_UP / "cli-anything-plugin"
    if not (plug / "HARNESS.md").is_file():
        raise SystemExit("cli-anything: upstream klon yok -> " + str(CLI_UP)
                         + "  (git clone -c core.autocrlf=false https://github.com/HKUDS/CLI-Anything.git)")
    yaz(stage / "SKILL.md", CLI_MD)
    fm_lf(stage / "SKILL.md", ad, rapor)
    yaz(stage / "references/HARNESS.md", (plug / "HARNESS.md").read_text(encoding="utf-8"))
    for alt, hedef in (("commands", "references/commands"), ("guides", "references/guides")):
        for c in sorted((plug / alt).glob("*.md")):
            yaz(stage / hedef / c.name, c.read_text(encoding="utf-8"))
    yaz(stage / "LICENSE", (plug / "LICENSE").read_text(encoding="utf-8"))
    sha = kabuk("git", "-C", str(CLI_UP), "log", "-1", "--format=%h %cs")
    rapor.append(ad + ": HKUDS/CLI-Anything " + sha)


def p_frontend_craft(stage, ad, rapor):
    """Repodaki skill dizini oldugu gibi paketlenir (node_modules/nokta dosyasi disarida)."""
    kopyala(FC_SKILL, stage, ad, rapor)
    fm_lf(stage / "SKILL.md", ad, rapor)
    surum = json.loads((REPO / "plugins/frontend-craft/.claude-plugin/plugin.json")
                       .read_text(encoding="utf-8"))["version"]
    rapor.append(ad + ": surum " + surum)


def p_pdev(altyol, ekler=(), degis=()):
    """ekler: (zip icindeki yol, plugin icindeki kaynak) — SKILL.md'nin cagirdigi betikler.
    degis: (eski, yeni) — kaynak metindeki sandbox'ta calismayan cagrilarin duzeltmesi."""
    def f(stage, ad, rapor):
        kok = kurulu("plugin-dev@claude-plugins-official")
        md = (kok / altyol).read_text(encoding="utf-8")
        for a, b in degis:
            if a not in md:
                raise SystemExit(ad + ": degis deseni kaynakta yok -> " + a)
            md = md.replace(a, b)
        md_skill(stage, ad, md, rapor)
        for hedef, kaynak in ekler:
            yaz(stage / hedef, (kok / kaynak).read_text(encoding="utf-8"))
        yaz(stage / "LICENSE", (kok / "LICENSE").read_text(encoding="utf-8"))
    return f


def p_memory_md(stage, ad, rapor):
    kok = kurulu("claude-md-management@claude-plugins-official")
    md_skill(stage, ad, (kok / "commands/revise-claude-md.md").read_text(encoding="utf-8"), rapor)
    yaz(stage / "LICENSE", (kok / "LICENSE").read_text(encoding="utf-8"))


PIXELJURY_MD = """---
name: pixeljury
description: Rendered web sayfasi icin gorsel QA - Chromium'da acar; kontrast, 390px mobil tasma, dokunma hedefi ve AI-slop desenlerini bulur, ajana verilebilir fix-prompt yazar. Yerel dosya ya da localhost adresi icin kullan.
---

# PixelJury (claude.ai paketi)

Sayfayi gercekten Chromium'da acip inceler; kaynak koddan tahmin etmez.
Cikti: `critique.md`, `fix-prompt.md`, `score.json`, ekran goruntuleri.

## Sinirlar (claude.ai sandbox)

- Playwright bu pakette **yok**; sandbox'in global kurulumu kullanilir. ESM `import()`
  `NODE_PATH`'i yok sayar, bu yuzden asagidaki blok global playwright'i calisma
  kopyasinin `node_modules/` dizinine baglar.
- `/mnt/skills` salt okunur; skill once `/tmp/pixeljury-run` altina kopyalanir.
- Yalniz `--provider mock` calisir: ag erisimi ve API anahtari yok. `anthropic`, `openai`,
  `claude-code`, `codex` saglayicilari sandbox'ta denenmemeli.
- Deterministik kontroller (kontrast, mobil tasma, dokunma hedefi, kucuk metin,
  slop desenleri) mock ile tam calisir; yalniz gorsel puanlama modele baglidir.

## Calistirma

Bash bloklari arasinda kabuk durumu korunmaz: asagisi **tek blok** olarak calistirilir.

```bash
SKILL=$(ls -d /mnt/skills/*/pixeljury | head -1)
URL=${URL:-file:///mnt/user-data/uploads/index.html}   # ya da http://localhost:3000
OUT=${OUT:-/mnt/user-data/outputs/pixeljury}
mkdir -p /tmp/pixeljury-run && cp -rf "$SKILL/." /tmp/pixeljury-run/
ln -sfn "$(npm root -g)/playwright" /tmp/pixeljury-run/node_modules/playwright
export PIXELJURY_RUBRIC=/tmp/pixeljury-run/references/rubric.md
node /tmp/pixeljury-run/bin/pixeljury.js review "$URL" --provider mock --out "$OUT"
```

Baska bir sayfa icin yalniz `URL` degisir: yerel dosya `file:///mnt/user-data/uploads/x.html`,
calisan sunucu `http://localhost:3000`. `--out` dizini yoksa olusturulur.

## Puanlama olcutu

Tam rubric: `references/rubric.md` (blokta `PIXELJURY_RUBRIC` ile gosterilir; rubric-loader
onu kendiliginden bulmaz). Sert hatalar (hard fail) puani tavanlar; problemler puan dusurur.
Once `fix-prompt.md` uygulanir, sonra tekrar calistirilir.
"""

HEADROOM_MD = """---
name: headroom-compress
description: Buyuk log, arac ciktisi ya da uzun metinli JSON'u yapiyi koruyarak sikistirir ve ozetini basar. Uzun bir dosyayi baglama sigdirmak ya da sikistirma oranini olcmek gerektiginde kullan.
---

# headroom-compress

headroom-ai 0.37.0'in `headroom/compression/` alt agaci gomulu (Apache-2.0).
Icerik turunu tespit eder, yapiyi (anahtarlar, imzalar, sablon) korur, geri kalani sikistirir.

## Sinirlar (claude.ai sandbox)

- **Kisa degerli JSON'da kazanc yok.** Sikistirma yalnizca **50 karakterden uzun**
  yapisal-olmayan parcalara uygulanir; JSON isleyicisi anahtarlari, parantezleri,
  bool/null degerleri, kisa sayilari ve 20 karaktere kadar metin degerlerini yapisal
  sayip korur. Olculen (400 kayitlik dizi, alanlar id / e-posta / sehir / durum / tarih):
  indent=2 252 KB -> **oran 1.000, %0**; kompakt 140 KB -> **%0**. Ayni dizide kayit
  basina tek metin degeri uzatilinca: 40 kr %0 . 50 kr %23.7 . 80 kr %35.4 . 200 kr %52.8.
  Yani **%30'u asmak icin metin degerlerinin ~80 karakterden uzun olmasi gerekir**;
  kayit dizisi bicimindeki disa aktarimlar bu paketin isi degil.
- **Seviye etiketi garanti degil.** Sikistirma her parcanin **ortasini** atar
  (bas 2/3 + `...[compressed]...` + son 1/3) ve kesme noktasi karakter sayisina gore
  belirlenir; log seviyesi ozel olarak korunmaz. Kesilen bolgeye denk gelen bir
  `ERROR`/`WARN` etiketi kaybolur. Seviye saymak icin sikistirilmis cikti degil asil
  dosya kullanilir. (Olculen 3000 satirlik log ornegi: %29.7 tasarruf, ERROR 60 -> 60.)
- `magika` (ML tespit) ve `tree_sitter` **yok**; her ikisi de `ImportError` ile yedek yola
  duser (`FallbackDetector`, satir tabanli kod ozeti). Cikti biraz daha kaba olur,
  calisma bozulmaz.
- Ust akisin guclu sikistiricilari (`transforms/kompress_compressor.py`,
  `transforms/smart_crusher.py`) gomulemez: ilki torch + transformers + onnxruntime ve
  model indirmesi ister, ikincisi derlenmis `headroom._core` uzantisina baglidir.
- CCR deposu (`ccr_enabled`) kapali: sikistirilan metnin aslini saklamaz.
- Saf Python; derlenmis uzanti, model dosyasi ya da ag cagrisi yok.

## Calistirma

```bash
SKILL=$(ls -d /mnt/skills/*/headroom-compress | head -1)
GIRDI=${GIRDI:-buyuk.log}
python3 "$SKILL/scripts/compress.py" "$GIRDI" --oran 0.3
```

`--cikti dosya.txt` verilirse sikistirilmis metin dosyaya yazilir; verilmezse stdout'a
basilir. Istatistik (oran, tahmini token) her zaman stderr'e gider.

Kutuphane olarak:

```bash
SKILL=$(ls -d /mnt/skills/*/headroom-compress | head -1)
GIRDI=${GIRDI:-buyuk.log}
PYTHONPATH="$SKILL" python3 -B -c "import sys; from headroom.compression import compress; print(compress(open(sys.argv[1], encoding='utf-8').read()).compressed[:500])" "$GIRDI"
```

Olculen ornekler ve tipik oranlar: `references/ornek.md`.
"""

HEADROOM_CLI = '''#!/usr/bin/env python3
"""Buyuk bir JSON/log/arac ciktisini sikistirip basar (headroom-ai compression)."""
import argparse
import pathlib
import sys

# /mnt/skills salt okunur: import sirasinda __pycache__ yazmaya calisilmasin
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from headroom.compression import UniversalCompressor, UniversalCompressorConfig


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dosya", help="sikistirilacak metin/JSON/log dosyasi")
    ap.add_argument("--oran", type=float, default=0.3,
                    help="hedef sikistirma orani (0-1, varsayilan 0.3)")
    ap.add_argument("--cikti", help="sonucun yazilacagi dosya; yoksa stdout")
    a = ap.parse_args(argv)

    metin = pathlib.Path(a.dosya).read_text(encoding="utf-8", errors="replace")
    # magika/CCR sandbox'ta yok: acikca kapatilir ki yedek yol sessizce secilsin
    cfg = UniversalCompressorConfig(use_magika=False, ccr_enabled=False,
                                    compression_ratio_target=a.oran)
    r = UniversalCompressor(config=cfg).compress(metin)

    if a.cikti:
        pathlib.Path(a.cikti).write_text(r.compressed, encoding="utf-8")
    else:
        sys.stdout.write(r.compressed)
    print("girdi {} kr . cikti {} kr . oran {:.3f} . token {} -> {} (%{:.1f} tasarruf)".format(
        len(r.original), len(r.compressed), r.compression_ratio,
        r.tokens_before, r.tokens_after, r.savings_percentage), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

HEADROOM_ORNEK = """# Ornek ve olculen sinirlar

`scripts/compress.py` bir dosyayi okur, icerik turunu tespit eder, yapiyi koruyarak
sikistirir ve istatistigi stderr'e basar.

```bash
SKILL=$(ls -d /mnt/skills/*/headroom-compress | head -1)
GIRDI=${GIRDI:-buyuk.log}
python3 "$SKILL/scripts/compress.py" "$GIRDI" --cikti kisa.txt
```

stderr ornegi:

```text
girdi 266679 kr . cikti 187455 kr . oran 0.703 . token 66669 -> 46863 (%29.7 tasarruf)
```

## Olculen sonuclar

| girdi | boyut | oran | tasarruf |
| --- | --- | --- | --- |
| 3000 satirlik uygulama logu (60 ERROR) | 260 KB | 0.703 | %29.7 |
| 400 kayitlik JSON dizisi, kisa alanlar, indent=2 | 252 KB | 1.000 | **%0** |
| 400 kayitlik JSON dizisi, kisa alanlar, kompakt | 140 KB | 1.000 | **%0** |
| ayni dizi, kayit basina 50 karakterlik metin degeri | - | 0.763 | %23.7 |
| ayni dizi, kayit basina 80 karakterlik metin degeri | - | 0.646 | %35.4 |
| ayni dizi, kayit basina 200 karakterlik metin degeri | - | 0.472 | %52.8 |

## JSON siniri

Sikistirma yalnizca **50 karakterden uzun** yapisal-olmayan parcalara uygulanir.
JSON isleyicisi anahtarlari, parantez/virgul/iki noktayi, bool ve null degerleri,
kisa sayilari ve **20 karaktere kadar** metin degerlerini yapisal sayip korur.
Bu yuzden alanlari kisa olan bir kayit dizisinde (id, e-posta, sehir, durum, tarih)
sikistirilabilir parca kalmaz ve oran 1.000 cikar -- girdi ne kadar tekrarli olursa
olsun. Tekrar tabanli kazanc ust akistaki `transforms/` sikistiricilarinda; onlar
torch/transformers/onnxruntime ya da derlenmis `headroom._core` istedigi icin bu
pakette yok.

Pratik kural: **metin degerleri ~80 karakteri gectiginde %30 ve ustu tasarruf gelir.**

## Notlar

- `--oran` hedeftir, garanti degil.
- Sikistirma her parcanin ortasini atar (bas 2/3 + `...[compressed]...` + son 1/3).
  Kesme noktasi karakter sayisina gore belirlenir; log seviyesi (`ERROR`, `WARN`) ozel
  olarak korunmaz, kesilen bolgeye denk gelen bir etiket kaybolur. Yukaridaki 3000
  satirlik ornekte 60 ERROR satirinin 60'i korundu, ama bu bicime bagli bir sonuc:
  seviye saymak icin asil dosya kullanilir.
- magika yoksa tur tespiti `FallbackDetector`'a duser (uzanti + basit desen).
  JSON ve duz log icin sonuc pratikte ayni; kaynak kodda ozet biraz daha kaba olur.
- Cok kucuk girdilerde (`min_content_length` 100 karakterin altinda) sikistirma yapilmaz,
  metin oldugu gibi doner.
"""


def p_pixeljury(stage, ad, rapor):
    src = Path(kabuk("npm", "root", "-g")) / "pixeljury"
    # kok package.json: kopyala() yalniz alt agaclari geziyordu, kok dosyalar disarida
    # kaliyordu -- bin/pixeljury.js "../package.json" okuyor (surum) ve "type": "module"
    # ESM cozumlemesi icin gerekli. Ikisi de bu dosyada.
    yaz(stage / "package.json", (src / "package.json").read_text(encoding="utf-8"))
    for alt in ("bin", "src"):
        kopyala(src / alt, stage / alt, ad, rapor)
    for m in ("pixeljury-core", "pixeljury-vision"):  # playwright/playwright-core HARIC
        kopyala(src / "node_modules" / m, stage / "node_modules" / m, ad, rapor)
    yaz(stage / "references/rubric.md", (src / "rubric.md").read_text(encoding="utf-8"))
    yaz(stage / "SKILL.md", PIXELJURY_MD)
    yaz(stage / "LICENSE", (PJ_KLON / "LICENSE").read_text(encoding="utf-8"))
    fm_lf(stage / "SKILL.md", ad, rapor)


def p_headroom(stage, ad, rapor):
    hr = Path(kabuk("uvx", "--from", "headroom-ai==0.37.0", "python", "-c",
                    "import headroom,os;print(os.path.dirname(headroom.__file__))"))
    # headroom/ paket yolu korunur: alt agac mutlak "from headroom.compression.X" import eder
    yaz(stage / "headroom/__init__.py",
        '"""headroom-ai 0.37.0 compression alt agaci (Apache-2.0)."""\n')
    kopyala(hr / "compression", stage / "headroom/compression", ad, rapor)
    yaz(stage / "scripts/compress.py", HEADROOM_CLI)
    yaz(stage / "references/ornek.md", HEADROOM_ORNEK)
    yaz(stage / "SKILL.md", HEADROOM_MD)
    lic = next(hr.parent.glob("headroom_ai-*.dist-info/licenses/LICENSE*"))
    yaz(stage / "LICENSE", lic.read_text(encoding="utf-8"))
    yaz(stage / "NOTICE",
        "headroom-compress\n\n"
        "Bu paket headroom-ai 0.37.0 (Apache License 2.0) surumunun\n"
        "headroom/compression/ alt agacini degistirmeden icerir.\n"
        "Kaynak: https://github.com/headroomlabs-ai/headroom\n\n"
        "Degisiklikler: yalniz compression alt agaci alindi; ust paketin geri kalani\n"
        "(_core uzantisi, onnx modelleri, cache ve transforms modulleri) cikarildi.\n"
        "scripts/compress.py, references/ornek.md ve SKILL.md bu paket icin yazilmistir.\n")
    fm_lf(stage / "SKILL.md", ad, rapor)


WDG_MD = """---
name: web-design-guidelines
description: Web Interface Guidelines uyumu icin UI kodunu gozden gecirir. "arayuzumu incele", "erisilebilirlik kontrolu", "tasarim denetimi" ya da "siteyi en iyi uygulamalara gore kontrol et" istendiginde kullan.
---

# Web Interface Guidelines

Dosyalari Web Interface Guidelines kurallarina gore inceler.

## Kural kaynagi

1. **Once yerel kopya:** `references/command.md` - paketin icinde, ag olmadan calisir.
   Basligindaki cekilis tarihi ve commit SHA'si hangi surum oldugunu soyler.
2. **Ag varsa tazele:** su adresi cek ve yerel kopyanin yerine kullan:
   `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
   Cekilemezse (sandbox'ta ag kapali olabilir) sessizce yerel kopyayla devam et.

## Akis

1. Kurallari yukle (yukaridaki sira).
2. Verilen dosyalari ya da deseni oku; verilmediyse kullaniciya sor.
3. Kurallarin hepsini uygula.
4. Bulgulari kurallarin tarif ettigi kisa `dosya:satir` bicimiyle yaz.
"""


def p_wdg(stage, ad, rapor):
    j = json.loads(kabuk("gh", "api", "repos/" + WIG_REPO + "/commits?path=command.md&per_page=1"))
    sha, tarih = j[0]["sha"], j[0]["commit"]["committer"]["date"][:10]
    icerik = json.loads(kabuk("gh", "api", "repos/" + WIG_REPO + "/contents/command.md"))["content"]
    govde = base64.b64decode(icerik).decode("utf-8")
    bas = ("> Kaynak: " + WIG_REPO + " . command.md . MIT\n"
           "> Cekilis: " + os.environ.get("YUKLE10_TARIH", "2026-09-20")
           + " . commit " + sha + " (" + tarih + ")\n\n")
    yaz(stage / "references/command.md", bas + govde)
    yaz(stage / "SKILL.md", WDG_MD)
    fm_lf(stage / "SKILL.md", ad, rapor)
    rapor.append(ad + ": command.md commit " + sha[:12] + " (" + tarih + ")")


DIVISIMA = ("Yalniz Divisima reposunda (C:\\Users\\pc\\Desktop\\smart\\Divisima.Solution) "
            "kullanilir; baska repoda tetiklenmez. ")


def p_zipten(zad):
    """dist/<zad> icindeki paketi acar; yalniz description onekini degistirir, govde aynen kalir."""
    def f(stage, ad, rapor):
        with zipfile.ZipFile(REPO / "dist" / zad) as z:
            for i in z.infolist():
                if i.is_dir():
                    continue
                rel = i.filename.split("/", 1)[1]
                b = z.read(i)
                if Path(rel).suffix.lower() in TEXT_EXT:
                    yaz(stage / rel, b.decode("utf-8"))
                else:
                    (stage / rel).parent.mkdir(parents=True, exist_ok=True)
                    (stage / rel).write_bytes(b)
        p = stage / "SKILL.md"
        md = p.read_text(encoding="utf-8")
        m = re.search(r"^description:[ \t]*(.+)$", md, re.M)
        eski = m.group(1).strip().strip("'\"")
        yeni = (DIVISIMA + eski)[:200]
        yaz(p, md[:m.start()] + "description: " + json.dumps(yeni, ensure_ascii=False)
            + md[m.end():])
        rapor.append(ad + ": description Divisima oneki (" + str(len(yeni)) + " kr)")
    return f


# claude.ai: dosyalar 644 -> betigi dogrudan cagirmak "Permission denied" verir;
# ayrica cwd skill koku degil. Cagri bash ile ve mutlak yolla yapilir.
AGENT_CREATOR_ESKI = (
    "Validate with: `scripts/validate-agent.sh agents/[identifier].md`")
AGENT_CREATOR_YENI = '''Dogrulama (betik pakette: `scripts/validate-agent.sh`;
claude.ai'da dosyalar 644 oldugu icin dogrudan degil `bash` ile cagrilir):

```bash
SKILL=$(ls -d /mnt/skills/*/plugin-dev-agent-creator | head -1)
bash "$SKILL/scripts/validate-agent.sh" agents/[identifier].md
```'''


PAKETLER = [
    # 10c: cli-anything synced'de var -> "replace"; frontend-craft claude.ai'de kurulu.
    ("cli-anything", "replace", p_cli_anything),
    ("frontend-craft", "replace", p_frontend_craft),
    ("plugin-dev-create-plugin", "yeni", p_pdev("commands/create-plugin.md")),
    ("plugin-dev-agent-creator", "yeni", p_pdev(
        "agents/agent-creator.md",
        [("scripts/validate-agent.sh", "skills/agent-development/scripts/validate-agent.sh")],
        [(AGENT_CREATOR_ESKI, AGENT_CREATOR_YENI)])),
    ("plugin-dev-plugin-validator", "yeni", p_pdev("agents/plugin-validator.md")),
    ("plugin-dev-skill-reviewer", "yeni", p_pdev("agents/skill-reviewer.md")),
    ("memory-md-management-revise-memory-md", "yeni", p_memory_md),
    ("pixeljury", "yeni", p_pixeljury),
    ("headroom-compress", "yeni", p_headroom),
    ("web-design-guidelines", "replace", p_wdg),
    ("sdp", "replace", p_zipten("sdp-claudeai.zip")),
    ("surec", "replace", p_zipten("surec-claudeai.zip")),
]


def kapi(stage, ad, hedef, synced):
    """Ortak kapi: claude.ai Add ekraninin reddettigi her sey burada yakalanir."""
    h = []
    md = (stage / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^\ufeff?---\s*\r?\n(.*?)\r?\n---", md, re.S)
    fm = yaml.safe_load(m.group(1)) if m else {}
    if not isinstance(fm, dict):
        return 0, ["frontmatter YAML okunamadi"]
    if fm.get("name") != ad:
        h.append("name=" + repr(fm.get("name")) + " != kok " + repr(ad))
    for k in ("claude", "anthropic"):
        if k in ad.lower():
            h.append("ayrilmis sozcuk: " + k)
    d = str(fm.get("description") or "").strip()
    if not 1 <= len(d) <= 200:
        h.append("description " + str(len(d)) + " karakter")
    if re.search(r"[<>]", d) or re.search(r"[<>]", str(fm.get("name") or "")):
        h.append("name/description acili parantez")
    if hedef != "replace" and ad in synced:
        h.append("synced ile cakisma: " + ad)
    skillmd, toplam = 0, 0
    for f in sorted(stage.rglob("*")):
        rel = f.relative_to(stage).as_posix()
        if any(par.startswith(".") for par in rel.split("/")):
            h.append("nokta dosyasi: " + rel)
        if not f.is_file():
            continue
        toplam += f.stat().st_size
        if f.name.lower() == "skill.md":
            skillmd += 1
        if f.suffix.lower() == ".zip":
            h.append("ic ice zip: " + rel)
        if f.name == "plugin.json" or ".claude-plugin" in rel.split("/"):
            h.append("plugin manifest: " + rel)
        if YASAK.search(rel):
            h.append("yasak karakter: " + rel)
        if f.suffix.lower() in TEXT_EXT and b"\r" in f.read_bytes():
            h.append("CRLF: " + rel)
    if skillmd != 1:
        h.append("SKILL.md sayisi " + str(skillmd))
    if toplam > 30 * 10**6:
        h.append("boyut " + str(round(toplam / 10**6, 1)) + " MB > 30")
    return toplam, h


def main(argv):
    synced = {d.name for d in SYNC.iterdir() if d.is_dir()}
    if TMP.exists():
        shutil.rmtree(TMP)
    if OUT.exists():
        shutil.rmtree(OUT)
    rapor, satir, hata = [], [], []
    zorla = os.environ.get("YUKLE10_HEDEF")  # 10b: eski surumun yerine gecen parti
    for ad, hedef, kur in PAKETLER:
        if argv and ad not in argv:
            continue
        hedef = zorla or hedef
        stage = TMP / ad / ad
        stage.mkdir(parents=True)
        kur(stage, ad, rapor)
        acik, h = kapi(stage, ad, hedef, synced)
        hata += [ad + ": " + x for x in h]
        d = OUT / hedef
        d.mkdir(parents=True, exist_ok=True)
        zp = d / (ad + ".zip")
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted((TMP / ad).rglob("*")):
                z.write(f, f.relative_to(TMP / ad).as_posix())
        satir.append("\t".join([hedef, ad, str(acik), str(zp.stat().st_size)]))
    print("hedef\tad\tacik\tzip")
    print("\n".join(satir))
    print("\npaket " + str(len(satir)) + " . rapor " + str(len(rapor))
          + " . KAPI HATASI " + str(len(hata)))
    for r in rapor:
        print("  .", r)
    for x in hata:
        print("  !", x)
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
