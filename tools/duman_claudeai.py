"""claude.ai sandbox duman testi: yukle-N zip'ini acip SKILL.md bash bloklarini kosar.

Taklit edilen kisitlar (KURULUM-10a olcumu):
  . skill /mnt/skills/<parti>/<ad> altinda, dosyalar 644, dizin salt okunur
  . playwright yalniz global node_modules'te (paketin icinde degil)
  . bash bloklari arasinda kabuk durumu korunmaz -> her blok ayri kabukta
  . ag yok: bloklar ag isteyen bir sey yapmamali

Kullanim:
    python tools/duman_claudeai.py dist/yukle-10b/replace
    python tools/duman_claudeai.py dist/yukle-10b/replace/pixeljury.zip --env URL=file:///...

Windows farklari (sandbox Linux):
  . 644 exec bitini kaldirmaz -> betik cagrilari ayrica statik olarak denetlenir
  . dizin salt okunur zorlanmaz -> blok sonrasi dosya listesi karsilastirilir
  . Git Bash `ln -s` dizine POSIX yol yaziyor, Node cozemiyor -> PATH'e `ln` shim'i
  . `npm root -g` sandbox'takinden farkli -> PATH'e `npm` shim'i (taklit global kok)
"""
import argparse
import os
import re
import shutil
import stat
import subprocess
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WIN = os.name == "nt"
BASH = shutil.which("bash") or r"C:\Program Files\Git\bin\bash.exe"
# sandbox'ta global olmasi gereken moduller; yerelde nerede olursa olsun tek yere baglanir
GLOBAL_MODULLER = ("playwright", "playwright-core")


def npm_kok():
    exe = shutil.which("npm") or shutil.which("npm.cmd")
    if not exe:
        raise SystemExit("npm bulunamadi")
    return Path(subprocess.run([exe, "root", "-g"], capture_output=True, text=True,
                               check=True).stdout.strip())


def modul_bul(kok, ad):
    """Modulu once global kokte, sonra global paketlerin node_modules'unda arar."""
    d = kok / ad
    if d.is_dir():
        return d
    for p in sorted(kok.glob("*/node_modules/" + ad)):
        if p.is_dir():
            return p
    return None


def sim_global(tmp):
    """Sandbox'in global node_modules'unu taklit eden kok; eksik modul raporlanir."""
    sim = tmp / "npm-global"
    sim.mkdir(parents=True, exist_ok=True)
    kok, eksik = npm_kok(), []
    for m in GLOBAL_MODULLER:
        kaynak = modul_bul(kok, m)
        if kaynak is None:
            eksik.append(m)
            continue
        hedef = sim / m
        if hedef.is_symlink() or hedef.exists():
            hedef.unlink()
        os.symlink(kaynak, hedef, target_is_directory=True)
    return sim, eksik


def shim_yaz(tmp, sim):
    """PATH onune konan npm/ln shim'leri: sandbox davranisini Windows'ta uretir."""
    d = tmp / "shim"
    d.mkdir(parents=True, exist_ok=True)
    gercek_npm = (shutil.which("npm") or "npm").replace("\\", "/")
    (d / "npm").write_text(
        '#!/bin/sh\n'
        '# sandbox: global kok tek dizin. Oteki alt komutlar gercek npm\'e gider.\n'
        'if [ "$1" = "root" ] && [ "$2" = "-g" ]; then\n'
        '  echo "' + str(sim).replace("\\", "/") + '"\n'
        '  exit 0\n'
        'fi\n'
        'exec "' + gercek_npm + '" "$@"\n',
        encoding="utf-8", newline="\n")
    if WIN:
        # Git Bash `ln -s` hedefi POSIX yola cevirip yaziyor; Node bunu cozemiyor.
        # Sandbox'ta gercek symlink var, burada Windows yerel symlink'i uretilir.
        (d / "ln").write_text(
            '#!/bin/sh\n'
            'for a in "$@"; do\n'
            '  case "$a" in -*) ;; *) set -- "$@" "$a" ;; esac\n'
            'done\n'
            'exec python "' + str(Path(__file__).resolve()).replace("\\", "/")
            + '" --ln "$@"\n',
            encoding="utf-8", newline="\n")
    for f in d.iterdir():
        f.chmod(0o755)
    return d


def ln_shim(argv):
    """`ln [-s|-f|-n|-sfn...] HEDEF LINK` -> Windows yerel symlink."""
    yol = [a for a in argv if not a.startswith("-")]
    if len(yol) < 2:
        print("ln shim: hedef/link eksik", file=sys.stderr)
        return 1
    hedef, link = Path(yol[-2]), Path(yol[-1])
    if link.is_dir() and not link.is_symlink():
        link = link / hedef.name
    if link.is_symlink() or link.exists():
        link.unlink()
    os.symlink(hedef.resolve(), link, target_is_directory=hedef.is_dir())
    return 0


def kur_644(kok):
    """Sandbox kopyasi: dosyalar 644, dizinler salt okunur (Windows'ta bilgi amacli)."""
    for p in sorted(kok.rglob("*"), reverse=True):
        p.chmod(0o644 if p.is_file() else 0o555)
    kok.chmod(0o555)


def ac_644(kok):
    for p in sorted(kok.rglob("*")) + [kok]:
        if p.is_dir():
            p.chmod(stat.S_IRWXU)


def agac(kok):
    return {p.relative_to(kok).as_posix() for p in kok.rglob("*")}


def bloklar(md):
    return re.findall(r"```bash\n(.*?)```", md, re.S)


def statik_denetim(md, kok, ad):
    """644'te dusecek cagrilar: SKILL.md'nin dogrudan calistirdigi paket betikleri."""
    h = []
    for b in bloklar(md):
        for m in re.finditer(r'(?m)^\s*(?:"?\$\w+/)?([\w./-]+\.(?:sh|py|js))\b', b):
            aday = m.group(1).lstrip("./")
            if (kok / aday).is_file():
                h.append("644'te calismaz, yorumlayiciyla cagir: " + m.group(0).strip())
    # kod blogu disinda kalan dogrudan betik cagrisi (ornek: `scripts/x.sh arg`).
    # Argumansiz anma (`scripts/x.sh`) cagri degil, dosya adi -- sayilmaz.
    govde = re.sub(r"```.*?```", "", md, flags=re.S)
    for m in re.finditer(r"`((?:scripts|bin)/[\w./-]+\.(?:sh|py|js))[ 	]+[^`]+`", govde):
        if (kok / m.group(1)).is_file():
            h.append("metinde dogrudan cagri (644'te duser): " + m.group(0))
    return h


def kos(zp, tmp, sim, shim, ortam):
    ad = zp.stem
    parti = tmp / "mnt-skills" / zp.parent.name
    kok = parti / ad
    with zipfile.ZipFile(zp) as z:
        z.extractall(parti.parent / "_ac")
    shutil.move(str(parti.parent / "_ac" / ad), str(kok))
    shutil.rmtree(parti.parent / "_ac", ignore_errors=True)

    md = (kok / "SKILL.md").read_text(encoding="utf-8")
    bl = bloklar(md)
    statik = statik_denetim(md, kok, ad)
    kur_644(kok)
    once = agac(kok)

    cevre = dict(os.environ)
    cevre["PATH"] = str(shim) + os.pathsep + cevre["PATH"]
    cevre["NODE_PATH"] = str(sim)
    cevre["MSYS"] = "winsymlinks:nativestrict"
    cevre.update(ortam)
    is_dizin = tmp / "cwd" / ad
    is_dizin.mkdir(parents=True, exist_ok=True)

    sonuc = []
    for i, b in enumerate(bl, 1):
        # /mnt/skills/<x>/<ad> desenini bu kopyaya cevir: sandbox yolu yerelde yok
        kosulacak = b.replace("/mnt/skills/*/", parti.as_posix() + "/")
        p = subprocess.run([BASH, "-c", kosulacak], cwd=is_dizin, env=cevre,
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        sonuc.append((i, p.returncode, (p.stdout + p.stderr).strip()))
    ac_644(kok)
    yazildi = sorted(agac(kok) - once)
    return ad, bl, sonuc, statik, yazildi, is_dizin


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("hedef", nargs="?", help="zip ya da zip iceren dizin")
    ap.add_argument("--env", action="append", default=[], metavar="AD=DEGER",
                    help="bloklara verilecek degisken (ornek: URL=file:///...)")
    ap.add_argument("--bekle", action="append", default=[], metavar="AD=RC",
                    help="beklenen exit kodu; sablon blok icin (ornek: x=1)")
    ap.add_argument("--tmp", help="calisma dizini (varsayilan: sistem gecici dizini)")
    ap.add_argument("--ln", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if a.ln is not None:
        return ln_shim(a.ln)
    if not a.hedef:
        ap.error("hedef gerekli")

    hedef = Path(a.hedef)
    zipler = sorted(hedef.rglob("*.zip")) if hedef.is_dir() else [hedef]
    tmp = Path(a.tmp or (Path(os.environ.get("TEMP", "/tmp")) / "duman-claudeai"))
    if tmp.exists():
        for p in sorted(tmp.rglob("*"), reverse=True):
            if p.is_dir() and not p.is_symlink():
                p.chmod(stat.S_IRWXU)
        shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)

    sim, eksik = sim_global(tmp)
    shim = shim_yaz(tmp, sim)
    if eksik:
        print("! global modul yerelde yok: " + ", ".join(eksik))
    ortam = dict(kv.split("=", 1) for kv in a.env)
    bekle = {k: int(v) for k, v in (kv.split("=", 1) for kv in a.bekle)}

    hatali = 0
    for zp in zipler:
        ad, bl, sonuc, statik, yazildi, cwd = kos(zp, tmp, sim, shim, ortam)
        b = bekle.get(ad, 0)
        kotu = [s for s in sonuc if s[1] != b]
        durum = "HATA" if (kotu or statik or yazildi) else "tamam"
        hatali += bool(kotu or statik or yazildi)
        print("\n=== %s . %d bash blok . %s" % (ad, len(bl), durum))
        for i, rc, cikti in sonuc:
            bas = cikti.splitlines()
            print("  blok %d . exit %d%s" % (
                i, rc, "" if rc == b else "  <-- DUSTU",))
            for line in (bas[:12] if rc != b else bas[:4]):
                print("      " + line[:160])
        for x in statik:
            print("  ! statik: " + x)
        for x in yazildi:
            print("  ! salt okunur kopyaya yazildi: " + x)
        print("  cikti dizini: " + cwd.as_posix())
    print("\n%d zip . %d sorunlu" % (len(zipler), hatali))
    return 1 if hatali else 0


if __name__ == "__main__":
    sys.exit(main())
