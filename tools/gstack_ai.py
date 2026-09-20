#!/usr/bin/env python3
"""gstack alt skill'lerini claude.ai paketine cevirir.

Kaynak ~/.claude/skills/gstack SALT OKUNUR. Cikti dist/yukle-9/gstack/parti-N.
Idempotent: gstack guncellenince yeniden kosulur.

Kullanim:
  python tools/gstack_ai.py            # uret
  python tools/gstack_ai.py --rapor    # uretilen paketi olc/denetle
"""
import json
import os
import re
import shutil
import sys
import zipfile
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
KAYNAK = Path(os.environ.get("GSTACK_KAYNAK") or (Path.home() / ".claude" / "skills" / "gstack"))
CIKTI = KOK / "dist" / "yukle-9b" / "replace"
SAHNE = KOK / ".tmp" / "gstack-ai"
SHIM = KOK / "tools" / "gstack_browse.py"
ENV_KAYNAK = KOK / "tools" / "gstack_env.sh"
# claude.ai kabuk durumunu cagrilar arasinda korumaz: GS/B/D her blogun ilk satirindan
ENV_SATIR = ('. "${GSTACK_CORE_RO:-$(ls -d /mnt/skills/*/gstack-core '
             '2>/dev/null | head -1)}/bin/gstack-env"')
PARTI_BOY = 20

# tools/gstack_browse.py KAPSAM listesiyle ayni tutulmali.
BROWSE_KAPSAM = set(
    "goto snapshot click fill press text js eval console screenshot wait viewport "
    "reload back url links html status closetab pdf responsive perf stop".split())

# Elle gerekcelendirilmis "claude.ai'de calismaz" listesi (regex'ten daha okunur/denetlenebilir).
HAYIR = {
    "ios-clean": "xcrun / iOS arac zinciri yok",
    "ios-design-review": "gercek iOS cihazi + xcrun yok",
    "ios-fix": "xcrun / iOS arac zinciri yok",
    "ios-qa": "tailnet daemon + gercek iOS cihazi yok",
    "ios-sync": "xcrun / iOS arac zinciri yok",
    "cso": "derlenmis gstack-cso-launcher + container yok",
    "setup-gbrain": "gbrain/Supabase kurulumu ag ister",
    "sync-gbrain": "gbrain senkronu ag ister",
    "codex": "harici codex CLI yok",
    "gstack-upgrade": "git pull / ag ister",
    "canary": "canli dagitim izleme, ag ister",
    "scrape": "gercek internet sayfasi ister",
    "land-and-deploy": "dagitim saglayicisi agi ister",
    "benchmark-models": "model API cagrisi ister",
    "open-gstack-browser": "gercek Chromium + eklenti baslatir",
    "setup-browser-cookies": "gercek tarayici profili okur",
    "pair-agent": "uzak ajan eslemesi, ag ister",
    "design-shotgun": "$D (gorsel uretim API) cekirdek",
}

# 200 karakteri asan tek aciklama; kor truncate yerine anlami koruyan elle kisaltma.
OZEL_ACIKLAMA = {
    "design-consultation": (
        "Design consultation: understands your product, researches the landscape, proposes a "
        "complete design system (aesthetic, typography, color, layout, spacing, motion). (gstack)"),
}

UYARLAMA = """> **claude.ai uyarlamasi**
> - Skill tool yok: `/x` gecen yerde `gstack-x` SKILL.md'sini oku ve uygula.
> - AskUserQuestion yok: `ask_user_input_v0` kullan, o da yoksa duz soru sor.
> - `$B` = gstack-env ayarlar (`python3 $GS/bin/browse`, Python+playwright shim); kapsam disi komut exit 2 doner.
> - `$D` desteklenmez; gorsel uretim adimlarini atla.
> - Kabuk durumu bash cagrilari arasinda korunmaz: GS/B/D her blogun ilk satirindaki
>   gstack-env'den gelir; preamble'in diger degiskenlerini (SLUG, _BRANCH ...) gereken
>   blokta yeniden hesapla.
> - Pakette yok (bun/.ts): gstack-decision-search/-log, gstack-brain-cache,
>   gstack-egress-lib ... - bos donerse atla.
> - `~/.gstack` oturumluk: oturum bitince silinir, kalici sayma.
> - Ag kapali: yalnizca sandbox icindeki dosyalar ve localhost sunuculari kullanilabilir.
"""

CEKIRDEK_SKILL = """---
name: gstack-core
description: Shared gstack runtime for the claude.ai package - bash helper tools plus the
  browse shim that other gstack-* skills call. Not invoked directly. (gstack)
---

# gstack-core

Bu skill dogrudan calistirilmaz. Diger `gstack-*` skill'lerinin cagirdigi paylasilan
arac takimini tasir.

- `bin/browse` - `$B` yerine gecen Python 3 + playwright shim. Arka planda tek bir
  tarayici sunucusu tutar, sayfa durumu cagrilar arasinda korunur, 15 dk boslukta kapanir.
  Kapsam: `{kapsam}`. Kapsam disi komut "desteklenmez" basip exit 2 doner.
  `snapshot [-i] [-a [-o <yol>]] [-D]`: her cagri ref'leri isaretler; `-i` listeyi
  etkilesimli elemanlara daraltir, `-a` ref kutularini cizip full_page PNG yazar
  (`-o` yoksa `annotated.png`), `-D` onceki snapshot ile farki verir. Bilinmeyen
  bayrak exit 2. `viewport 375x812` ve `viewport 375 812` ayni kapiya cikar.
- `bin/gstack-env` - her bash blogunun ilk satirinda source edilir: salt okunur
  kaynagi `$HOME/.gstack/core` altina +x'li kopyalar (claude.ai dosyalari 644 yazar),
  sonra `GS`, `B`, `D` disari verir. Ikinci source kopyalamaz.
- `bin/gstack-skill-start` - preamble shim'i; telemetri ve artifacts-sync kapali.
- `bin/gstack-skill-end`, `bin/gstack-telemetry-log` - no-op.
- `bin/gstack-*` - ust kaynaktan alinan saf bash yardimcilar (bun/.ts araclar disarida).

Diger skill'ler her bash blogunun ilk satirinda soyle baglanir:

```bash
. "${{GSTACK_CORE_RO:-$(ls -d /mnt/skills/*/gstack-core 2>/dev/null | head -1)}}/bin/gstack-env"
$B goto file:///tmp/x.html
```

Ust kaynak: gstack {surum}, MIT (Copyright (c) 2026 Garry Tan).
"""

SKILL_START = """#!/usr/bin/env bash
# claude.ai shim: gercek gstack-skill-start yerine gecer. Telemetri ve artifacts-sync kapali.
set -u
mkdir -p "${HOME}/.gstack" 2>/dev/null || true
_SID="${GSTACK_SESSION_ID:-gs-$$-$(date +%s 2>/dev/null || echo 0)}"
echo "SKILL_START_PROTO: 1"
echo "SESSION_KIND: interactive"
echo "PROACTIVE: true"
echo "PROACTIVE_PROMPTED: true"
echo "ACTIVATED: true"
echo "FIRST_LOOP_SHOWN: true"
echo "TELEMETRY: off"
echo "TEL_PROMPTED: true"
echo "SESSION_ID: ${_SID}"
echo "TEL_START: $(date +%s 2>/dev/null || echo 0)"
echo "ARTIFACTS_SYNC: off"
echo "UPDATE_CHECK: off"
echo "QUESTION_TUNING: off"
echo "LEARNINGS: 0"
echo "REPO_MODE: ${GSTACK_REPO_MODE:-repo}"
echo "BRANCH: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
echo "GSTACK_PLAN_MODE: ${GSTACK_PLAN_MODE:-false}"
echo "HAS_ROUTING: false"
echo "ROUTING_DECLINED: true"
echo "VENDORED_GSTACK: false"
echo "CHECKPOINT_MODE: off"
echo "SANDBOX: claude.ai"
exit 0
"""

NOOP = """#!/usr/bin/env bash
# claude.ai shim: no-op (telemetri claude.ai paketinde kapali).
exit 0
"""


# --------------------------------------------------------------------- yardimcilar

def hedef_ad(ad):
    """Adinda 'gstack' geceni oldugu gibi birak, digerine gstack- oneki ekle."""
    return ad if "gstack" in ad else "gstack-" + ad


def frontmatter_ayir(metin):
    m = re.match(r"^---\n(.*?)\n---\n", metin, re.S)
    if not m:
        return None, metin
    return m.group(1), metin[m.end():]


def fm_degeri(fm, anahtar):
    m = re.search(r"^%s:[ \t]*(.*(?:\n[ \t]+\S.*)*)" % anahtar, fm, re.M)
    if not m:
        return None
    return re.sub(r"\s+", " ", m.group(1)).strip().strip("'\"")


def bash_araci_mi(p):
    if p.suffix in (".ts", ".exe", ".js", ".c", ".md") or p.is_dir():
        return False
    try:
        bas = p.open("rb").readline()
    except OSError:
        return False
    return bas.startswith(b"#!") and b"bun" not in bas and b"node" not in bas


def bash_araclari_topla(metinler):
    """SKILL.md'lerde gecen gstack-* bash araclari + gecisli bagimliliklari."""
    bind = KAYNAK / "bin"
    mevcut = {p.name: p for p in bind.iterdir() if p.is_file() and bash_araci_mi(p)}
    kuyruk = set()
    for m in metinler:
        kuyruk |= {a for a in re.findall(r"\bgstack-[a-z0-9-]+(?:\.sh)?\b", m) if a in mevcut}
    secili = {}
    while kuyruk:
        ad = kuyruk.pop()
        if ad in secili:
            continue
        secili[ad] = mevcut[ad]
        govde = mevcut[ad].read_text(encoding="utf-8", errors="replace")
        kuyruk |= {a for a in re.findall(r"\bgstack-[a-z0-9-]+(?:\.sh)?\b", govde)
                   if a in mevcut and a not in secili}
    return secili


def skillmd_donustur(metin, ad, yeni_ad, sinif, gerekce):
    """Frontmatter adini duzelt, yollari $GS'e cevir, uyarlama basligini ekle."""
    fm, govde = frontmatter_ayir(metin)
    if fm is None:
        raise ValueError(ad + ": frontmatter yok")

    fm = re.sub(r"^name:.*$", "name: " + yeni_ad, fm, count=1, flags=re.M)
    aciklama = OZEL_ACIKLAMA.get(ad) or fm_degeri(fm, "description") or (ad + " (gstack)")
    aciklama = aciklama.replace("<", "").replace(">", "")
    if len(aciklama) > 200:
        aciklama = aciklama[:197].rsplit(" ", 1)[0] + "..."
    # json.dumps -> gecerli YAML cift tirnakli skaler; aciklamadaki ':' YAML'i bozmasin
    fm = re.sub(r"^description:[ \t]*(?:.*(?:\n[ \t]+\S.*)*)$",
                lambda _: "description: " + json.dumps(aciklama, ensure_ascii=False),
                fm, count=1, flags=re.M)
    # allowed-tools icindeki Bash(...) izinleri de kurulum yolu tasiyor
    fm = re.sub(r"(?:~|\$HOME|\$\{HOME\})/\.claude/skills/gstack", "$GS", fm)

    # Ust kaynagin bun ile yeniden uretim banner'i claude.ai paketinde anlamsiz
    govde = re.sub(r"^<!-- (?:AUTO-GENERATED|Regenerate:).*-->\n", "", govde, flags=re.M)

    # gstack kurulum yollari -> $GS
    govde = re.sub(r"(?:~|\$HOME|\$\{HOME\})/\.claude/skills/gstack", "$GS", govde)
    govde = re.sub(r"(?:~|\$HOME|\$\{HOME\})/\.claude(?=/|\b)", "$HOME/.claude", govde)

    # bun / .ts arac cagrilarini yorumla
    def ts_yorumla(satir):
        s = satir.lstrip()
        if not s or s.startswith("#"):
            return satir
        if re.search(r"\.ts\b|(?<![\w-])bun\s", satir):
            return "# claude.ai'de yok (bun/.ts gerekiyor): " + satir.strip()
        # $B/$D gstack-env'den gelir; ust kaynagin yol taramasi claude.ai'de ikisini de bosaltir
        if re.match(r'(B|D)=("|\s*$)', s) or re.search(r'\]\s*&&\s*(B|D)="', s):
            return "# claude.ai: $B/$D gstack-env'den gelir -- " + satir.strip()
        return satir

    parcalar = re.split(r"(```[a-z]*\n.*?```)", govde, flags=re.S)
    for i, p in enumerate(parcalar):
        if p.startswith("```bash") or p.startswith("```sh"):
            parcalar[i] = "\n".join(ts_yorumla(s) for s in p.split("\n"))
    govde = "".join(parcalar)

    # $GS/$B/$D gecen her blok kendi kabugunu kurar (durum cagrilar arasi korunmaz)
    def env_ekle(m):
        if not re.search(r"\$GS|\$B\b|\$D\b", m.group(2)):
            return m.group(0)
        return m.group(1) + ENV_SATIR + "\n" + m.group(2) + m.group(3)
    govde = re.sub(r"(```bash\n)(.*?)(```)", env_ekle, govde, flags=re.S)

    bas = UYARLAMA
    if sinif == "hayir":
        bas += ">\n> **Bu skill claude.ai'de calismaz:** " + gerekce + "\n"
    return "---\n" + fm + "\n---\n\n" + bas + "\n" + govde.lstrip("\n")


def siniflandir(ad, metin):
    if ad in HAYIR:
        return "hayir", HAYIR[ad]
    # "bun run gen:skill-docs" banner'i her dosyada var, gercek arac cagrisi degil
    metin = re.sub(r"^<!-- (?:AUTO-GENERATED|Regenerate:).*-->$", "", metin, flags=re.M)
    if (re.search(r"gstack-[a-z-]+\.ts|(?<![\w-])bun\s", metin)
            or len(re.findall(r"\$D\s+[a-z]", metin)) > 2):
        return "kismen", "bun/.ts araci veya $D adimlari atlanir"
    return "evet", "yalnizca bash + $B + sandbox ici dosya/localhost"


def zip_yaz(dizin, ad):
    hedef = dizin / (ad + ".zip")
    kaynak = SAHNE / ad
    with zipfile.ZipFile(hedef, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(kaynak.rglob("*")):
            if f.is_file():
                z.write(f, (Path(ad) / f.relative_to(kaynak)).as_posix())
    return hedef


def yaz_lf(p, metin, calistirilabilir=False):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(metin.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))
    if calistirilabilir:
        os.chmod(p, 0o755)


# --------------------------------------------------------------------------- uretim

def uret():
    if not KAYNAK.is_dir():
        sys.exit("kaynak yok: " + str(KAYNAK))
    surum = (KAYNAK / "VERSION").read_text(encoding="utf-8").strip()

    kaynaklar = [(KAYNAK, "gstack-router")]
    for d in sorted(KAYNAK.iterdir()):
        if d.is_dir() and (d / "SKILL.md").is_file() and d.name != "node_modules":
            kaynaklar.append((d, None))

    gorulen, skiller, atlanan, rapor = {}, [], [], []
    for d, zorla in kaynaklar:
        metin = (d / "SKILL.md").read_text(encoding="utf-8")
        fm, _ = frontmatter_ayir(metin)
        ad = fm_degeri(fm or "", "name") or d.name
        yeni = zorla or hedef_ad(ad)
        if yeni in gorulen and gorulen[yeni] == ad:
            atlanan.append((d.name, yeni, gorulen[yeni]))
            continue
        if yeni in gorulen:  # onceki aday adiyla eslesmiyordu, bunu tercih et
            atlanan.append((gorulen[yeni], yeni, d.name))
            skiller[:] = [x for x in skiller if x["yeni"] != yeni]
        gorulen[yeni] = d.name
        sinif, gerekce = siniflandir(ad, metin)
        skiller.append({"dizin": d.name, "ad": ad, "yeni": yeni,
                        "sinif": sinif, "gerekce": gerekce,
                        "icerik": skillmd_donustur(metin, ad, yeni, sinif, gerekce)})

    if SAHNE.exists():
        shutil.rmtree(SAHNE)
    SAHNE.mkdir(parents=True)
    for s in skiller:
        yaz_lf(SAHNE / s["yeni"] / "SKILL.md", s["icerik"])

    # gstack-core
    araclar = bash_araclari_topla([s["icerik"] for s in skiller])
    cek = SAHNE / "gstack-core"
    yaz_lf(cek / "SKILL.md", CEKIRDEK_SKILL.format(
        kapsam=" ".join(sorted(BROWSE_KAPSAM)), surum=surum))
    for ad, p in sorted(araclar.items()):
        if ad in ("gstack-skill-start", "gstack-skill-end", "gstack-telemetry-log"):
            continue
        yaz_lf(cek / "bin" / ad, p.read_text(encoding="utf-8", errors="replace"), True)
    yaz_lf(cek / "bin" / "gstack-skill-start", SKILL_START, True)
    yaz_lf(cek / "bin" / "gstack-skill-end", NOOP, True)
    yaz_lf(cek / "bin" / "gstack-telemetry-log", NOOP, True)
    yaz_lf(cek / "bin" / "browse", SHIM.read_text(encoding="utf-8"), True)
    yaz_lf(cek / "bin" / "gstack-env", ENV_KAYNAK.read_text(encoding="utf-8"), True)

    # zip'ler: gstack-core once, sonra alfabetik
    adlar = ["gstack-core"] + sorted(s["yeni"] for s in skiller)
    if CIKTI.exists():
        shutil.rmtree(CIKTI)
    boyutlar = {}
    for i, ad in enumerate(adlar):
        d = CIKTI / ("parti-" + str(i // PARTI_BOY + 1))
        d.mkdir(parents=True, exist_ok=True)
        boyutlar[ad] = zip_yaz(d, ad).stat().st_size

    (KOK / ".tmp" / "gstack-ai-envanter.json").write_text(json.dumps(
        {"surum": surum, "atlanan": atlanan, "bash_arac": len(araclar),
         "skiller": [{k: s[k] for k in ("dizin", "ad", "yeni", "sinif", "gerekce")}
                     for s in skiller]}, ensure_ascii=False, indent=1), encoding="utf-8")

    sayim = Counter(s["sinif"] for s in skiller)
    enbuyuk = max(boyutlar.items(), key=lambda kv: kv[1])
    print("%d zip (%d skill + gstack-core) -> %s" % (len(adlar), len(skiller), CIKTI))
    print("siniflar: evet %d . kismen %d . hayir %d" % (
        sayim["evet"], sayim["kismen"], sayim["hayir"]))
    print("gstack-core bash arac: %d . en buyuk zip: %s %.1f KB" % (
        len(araclar), enbuyuk[0], enbuyuk[1] / 1024))
    for dizin, yeni, sahip in atlanan:
        print("atlandi: %s -> %s (ayni ad, sahibi %s)" % (dizin, yeni, sahip))
    rapor.extend(adlar)
    return 0


# ---------------------------------------------------------------------------- rapor

def rapor():
    if not SAHNE.exists():
        sys.exit("once `python tools/gstack_ai.py` kosun")
    mds = sorted(SAHNE.glob("*/SKILL.md"))
    hist, ciplak, bun_kalan = Counter(), [], []
    for p in mds:
        m = p.read_text(encoding="utf-8")
        hist.update(re.findall(r"\$B\s+([a-z][a-z0-9-]*)", m))
        if re.search(r"~/\.claude/skills/gstack", m):
            ciplak.append(p.parent.name)
        # bun cagrisi yalnizca bash cercevelerinde anlamli
        for cerceve in re.findall(r"```(?:bash|sh)\n(.*?)```", m, re.S):
            for satir in cerceve.split("\n"):
                if re.search(r"(?<![\w-])bun\s", satir) and not satir.lstrip().startswith("#"):
                    bun_kalan.append(p.parent.name + ": " + satir.strip()[:70])
    # @ ve yasak karakter denetimi gercek zip girdi yollari uzerinde yapilir
    at_yol = []
    for z in sorted(CIKTI.rglob("*.zip")):
        with zipfile.ZipFile(z) as zf:
            if any(re.search(r'[\x00-\x1f\x7f\\:*?"<>|@]', e) for e in zf.namelist()):
                at_yol.append(z.name)

    toplam = sum(hist.values())
    kapsanan = sum(n for k, n in hist.items() if k in BROWSE_KAPSAM)
    print("SKILL.md: %d" % len(mds))
    print("$B kapsami: %d/%d = %%%.1f" % (kapsanan, toplam, 100.0 * kapsanan / max(toplam, 1)))
    print("kapsam disi komutlar: " + ", ".join(
        "%s=%d" % (k, n) for k, n in hist.most_common() if k not in BROWSE_KAPSAM) or "(yok)")
    print("ciplak ~/.claude/skills/gstack: %d %s" % (len(ciplak), ciplak or ""))
    print("yasak karakterli zip yolu: %d %s" % (len(at_yol), at_yol or ""))
    print("yorumlanmamis bun cagrisi: %d" % len(bun_kalan))
    for s in bun_kalan[:5]:
        print("  " + s)
    return 0


def main(argv):
    return rapor() if "--rapor" in argv else uret()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
