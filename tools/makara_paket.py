"""MAKARA SLEEP-3 giden paket (PC → özel bulut repo). Model yok. Kasadan YALNIZ ders notları + tasks-v2.json (intent<900 + reference) + şerit hedefleri;
ham transkript, is-kaydi.tsv, devir/, 60-ajanlar, ~/.claude/CLAUDE.md ASLA girmez. Veri dosyaları redakte edilir (anahtar/e-posta/yol/IP/kişi adı), sonra
gitleaks + kendi taraması; TEK bulgu varsa paket çıkmaz (hedef dizine dokunulmaz). Kod (tools/*.py) olduğu gibi gider, yalnız gitleaks'e girer.
  python tools/makara_paket.py [--cikis .kos/makara/paket]     # push ayrı Ömer onayı; bu betik push etmez"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import makara_ders  # noqa: E402
import makara_gece  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
KASA = makara_ders.KASA
GOREV = makara_gece.GOREV
KOD = ("makara_gece.py", "makara_ders.py", "ucretsiz_havuz.py")  # runner'ın çalıştırdığı betikler (tools/ altına aynı adla)
KOK_USTU = {"omer-kurallar.md": Path(r"C:\Projeler\omer-kurallar.md")}  # ana repo dışındaki hedef
GUN, KES = 14, 4000  # ders notu penceresi; hedef dosyadan alınan en çok karakter (gece yalnız ilk 1500'ünü okur)
ANAHTAR = re.compile(r"sk-[\w-]{20,}|gh[pousr]_\w{20,}|github_pat_\w{20,}|AIza[\w-]{30,}|xox[a-z]-[\w-]{10,}|gsk_\w{20,}|nvapi-[\w-]{20,}|Bearer\s+[\w.-]{20,}")
EPOSTA = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
ATAMA = re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\b(\s*[=:]\s*)\S+")
YOL = re.compile(r"[A-Za-z]:[\\/](?:Users|Projeler)[\\/][^\s\"'`)>\]]*|/(?:c/)?(?:Users|home)/\w+[^\s\"'`)>\]]*")
IP = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
KISI = re.compile(r"Omer-F-Ylmz|omery3899|Ömer|Omer|Yılmaz|Yilmaz")
REDAKSIYON = [(ANAHTAR, "<gizli>"), (ATAMA, r"\1\2<gizli>"), (EPOSTA, "<eposta>"), (YOL, "<yol>"), (IP, "<ip>"), (KISI, "<kişi>")]


def redakte(s):
    for r, y in REDAKSIYON:
        s = r.sub(y, s)
    return s


def kalan(s):
    """Redaksiyondan sonra kalmaması gereken desenler (anahtar, e-posta, değer atanmış gizli)."""
    return [m[0][:12] for r in (ANAHTAR, EPOSTA) for m in r.finditer(s)] + [m[0][:12] for m in ATAMA.finditer(s) if not m[0].endswith("<gizli>")]


def gitleaks(dizin):
    """(temiz mi, kısa not). Bulunamazsa temiz SAYILMAZ."""
    try:
        r = subprocess.run(["gitleaks", "dir", str(dizin), "--no-banner", "--redact"], capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.SubprocessError) as x:
        return False, f"gitleaks çalışmadı: {type(x).__name__}"
    return r.returncode == 0, "" if r.returncode == 0 else f"gitleaks bulgu (çıkış {r.returncode})"


def hedefler(kok):
    for _, desenler, _ in makara_gece.BULUT_SERIT:
        for d in desenler:
            if d in KOK_USTU:
                if KOK_USTU[d].exists():
                    yield d, KOK_USTU[d]
            else:
                for p in sorted(Path(kok).glob(d)):
                    yield p.relative_to(kok).as_posix(), p


def derle(hedef, kok, kasa, gorev, gun):
    """hedef dizinine veri + kodu yazar; {göreli yol: sha256} döner."""
    kok, hedef = Path(kok), Path(hedef)

    def yaz(rel, metin, ham=False):
        y = hedef / rel
        y.parent.mkdir(parents=True, exist_ok=True)
        y.write_bytes(metin.encode("utf-8") if not ham else metin)
    t = json.loads(Path(gorev).read_text(encoding="utf-8"))
    gor = [{k: redakte(str(g[k])) if k != "split" else g[k] for k in ("id", "split", "intent", "reference")} for g in t["tasks"] if len(g["intent"]) < 900 and g["reference"]]
    yaz("tasks-v2.json", json.dumps({"tasks": gor}, ensure_ascii=False))
    sinir = time.strftime("%Y-%m-%d", time.localtime(time.time() - gun * 86400))
    for p in sorted((Path(kasa) / "50-dersler").glob("ders-*.md")):
        if p.stem[5:] >= sinir:
            yaz(f"dersler/{p.name}", redakte(p.read_text(encoding="utf-8")))
    for rel, p in hedefler(kok):
        yaz(f"hedefler/{rel}", redakte(p.read_text(encoding="utf-8", errors="replace")[:KES]))
    for ad in KOD:
        yaz(f"tools/{ad}", (Path(__file__).parent / ad).read_bytes(), ham=True)
    return {p.relative_to(hedef).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(hedef.rglob("*")) if p.is_file()}


def kur(cikis, kok=KOK, kasa=KASA, gorev=GOREV, tarayici=gitleaks, gun=GUN):
    """(tamam, mesaj). Bulgu varsa cikis'e dokunulmaz."""
    cikis = Path(cikis)
    gec = cikis.with_name(cikis.name + ".tmp")
    if gec.exists():
        shutil.rmtree(gec)  # kendi yarım çıktımız
    man = derle(gec, kok, kasa, gorev, gun)
    veri = [p for p in man if not p.startswith("tools/")]
    bulgu = [f"{p}: {b}" for p in veri for b in kalan((gec / p).read_text(encoding="utf-8"))]
    ok, not_ = tarayici(gec)
    if bulgu or not ok:
        shutil.rmtree(gec)
        return False, "REDDEDİLDİ: " + "; ".join(bulgu[:3] + ([not_] if not_ else []))
    (gec / "manifest.json").write_text(json.dumps({"gun": time.strftime("%Y-%m-%d"), "dosyalar": man}, indent=1), encoding="utf-8")
    if cikis.exists():
        if not (cikis / "manifest.json").exists():
            shutil.rmtree(gec)
            return False, f"REDDEDİLDİ: {cikis} bizim paket değil (manifest yok), silinmedi"
        shutil.rmtree(cikis)  # önceki paketimiz
    gec.rename(cikis)
    return True, f"paket: {len(man)} dosya · gitleaks temiz · {cikis}"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cikis", default=str(KOK / ".kos/makara/paket"))
    ok, m = kur(ap.parse_args(argv).cikis)
    print(m)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
