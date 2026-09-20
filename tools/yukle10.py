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
def p_cli_anything(stage, ad, rapor):
    md = (CLI_MK / "openclaw-skill/SKILL.md").read_text(encoding="utf-8").replace(
        "`../cli-anything-plugin/HARNESS.md`", "`references/HARNESS.md`")
    md += ("\n## Paket icerigi\n\n"
           "- `references/HARNESS.md` - CLI-Anything metodolojisinin tam kaynagi.\n"
           "- `references/commands/` - plugin komutlarinin (cli-anything, list, refine,\n"
           "  test, validate) metinleri.\n")
    yaz(stage / "SKILL.md", md)
    fm_lf(stage / "SKILL.md", ad, rapor)
    plug = CLI_MK / "cli-anything-plugin"
    yaz(stage / "references/HARNESS.md", (plug / "HARNESS.md").read_text(encoding="utf-8"))
    for c in sorted((plug / "commands").glob("*.md")):
        yaz(stage / "references/commands" / c.name, c.read_text(encoding="utf-8"))
    yaz(stage / "LICENSE", (plug / "LICENSE").read_text(encoding="utf-8"))


def p_pdev(altyol, ekler=()):
    """ekler: (zip icindeki yol, plugin icindeki kaynak) — SKILL.md'nin cagirdigi betikler."""
    def f(stage, ad, rapor):
        kok = kurulu("plugin-dev@claude-plugins-official")
        md_skill(stage, ad, (kok / altyol).read_text(encoding="utf-8"), rapor)
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

- Playwright bu pakette **yok**; sandbox'in global kurulumu (playwright 1.56.0) kullanilir.
- Yalniz `--provider mock` calisir: ag erisimi ve API anahtari yok. `anthropic`, `openai`,
  `claude-code`, `codex` saglayicilari sandbox'ta denenmemeli.
- Deterministik kontroller (kontrast, mobil tasma, dokunma hedefi, kucuk metin,
  slop desenleri) mock ile tam calisir; yalniz gorsel puanlama modele baglidir.

## Calistirma

```bash
SKILL=$(ls -d /mnt/skills/*/pixeljury | head -1)
export NODE_PATH=$(npm root -g)
node "$SKILL/bin/pixeljury.js" review "file:///mnt/user-data/uploads/index.html" \\
  --provider mock --out /mnt/user-data/outputs/pixeljury
```

Yerel bir sunucu varsa adres dogrudan verilir:

```bash
node "$SKILL/bin/pixeljury.js" review "http://localhost:3000" --provider mock --out ./pixeljury
```

`--out` verilmezse cikti calisma dizinindeki `pixeljury/` klasorune yazilir.

## Puanlama olcutu

Tam rubric: `references/rubric.md`. Sert hatalar (hard fail) puani tavanlar;
problemler puan dusurur. Once `fix-prompt.md` uygulanir, sonra tekrar calistirilir.
"""

HEADROOM_MD = """---
name: headroom-compress
description: Buyuk JSON, log ya da arac ciktisini yapiyi koruyarak sikistirir ve ozetini basar. Uzun bir dosyayi baglama sigdirmak, arac ciktisini kisaltmak ya da sikistirma oranini olcmek gerektiginde kullan.
---

# headroom-compress

headroom-ai 0.37.0'in `headroom/compression/` alt agaci gomulu (Apache-2.0).
Icerik turunu tespit eder, yapiyi (anahtarlar, imzalar, sablon) korur, geri kalani sikistirir.

## Sinirlar (claude.ai sandbox)

- `magika` (ML tespit) ve `tree_sitter` **yok**; her ikisi de `ImportError` ile yedek yola
  duser (`FallbackDetector`, satir tabanli kod ozeti). Cikti biraz daha kaba olur,
  calisma bozulmaz.
- CCR deposu (`ccr_enabled`) kapali: sikistirilan metnin aslini saklamaz.
- Saf Python; derlenmis uzanti, model dosyasi ya da ag cagrisi yok.

## Calistirma

```bash
SKILL=$(ls -d /mnt/skills/*/headroom-compress | head -1)
python3 "$SKILL/scripts/compress.py" buyuk.json --oran 0.3
```

`--cikti dosya.txt` verilirse sikistirilmis metin dosyaya yazilir; verilmezse stdout'a
basilir. Istatistik (oran, tahmini token) her zaman stderr'e gider.

Kutuphane olarak:

```bash
SKILL=$(ls -d /mnt/skills/*/headroom-compress | head -1)
PYTHONPATH="$SKILL" python3 -c "from headroom.compression import compress; print(compress(open('buyuk.json').read()).compressed[:500])"
```

Ornek cikti ve tipik oranlar: `references/ornek.md`.
"""

HEADROOM_CLI = '''#!/usr/bin/env python3
"""Buyuk bir JSON/log/arac ciktisini sikistirip basar (headroom-ai compression)."""
import argparse
import pathlib
import sys

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

HEADROOM_ORNEK = """# Ornek

`scripts/compress.py` bir dosyayi okur, icerik turunu tespit eder, yapiyi koruyarak
sikistirir ve istatistigi stderr'e basar.

```bash
SKILL=$(ls -d /mnt/skills/*/headroom-compress | head -1)
python3 "$SKILL/scripts/compress.py" buyuk.json --cikti kisa.txt
```

stderr ornegi:

```text
girdi 1483210 kr . cikti 512044 kr . oran 0.345 . token 370802 -> 128011 (%65.5 tasarruf)
```

Notlar:

- `--oran` hedeftir, garanti degil; cok tekrarli JSON'da asilir, yogun metinde tutmaz.
- magika yoksa tur tespiti `FallbackDetector`'a duser (uzanti + basit desen).
  JSON ve duz log icin sonuc pratikte ayni; kaynak kodda ozet biraz daha kaba olur.
- Cok kucuk girdilerde (`min_content_length` 100 karakterin altinda) sikistirma yapilmaz,
  metin oldugu gibi doner.
"""


def p_pixeljury(stage, ad, rapor):
    src = Path(kabuk("npm", "root", "-g")) / "pixeljury"
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


PAKETLER = [
    ("cli-anything", "yeni", p_cli_anything),
    ("plugin-dev-create-plugin", "yeni", p_pdev("commands/create-plugin.md")),
    ("plugin-dev-agent-creator", "yeni", p_pdev(
        "agents/agent-creator.md",
        [("scripts/validate-agent.sh", "skills/agent-development/scripts/validate-agent.sh")])),
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
    for ad, hedef, kur in PAKETLER:
        if argv and ad not in argv:
            continue
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
