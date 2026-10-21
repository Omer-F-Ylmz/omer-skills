"""MAKARA SLEEP-3 dönüş yolu: bulut gece koşusunun artefaktı → PC. `gh run download` (CLI önce) → öneriler .kos/makara/kum/ (KUM; gerçek skill'e asla),
bulut uyku raporu Obsidian'a '-bulut' notu. Aynı kid = aynı dosya (çift yok); bir koşu bir kez işlenir. Kabul yine yalnız onay/makara_onay.py <id>.
Repo: --repo, sonra ortam MAKARA_BULUT_REPO, sonra .kos/makara.json (bulut_repo) (sahip/ad); hiçbiri yoksa sessiz çıkar.
  python tools/makara_cek.py [--repo sahip/ad] | kur | kaldir     # kur: saatlik, pencere yok (conhost --headless; ONLOGON yönetici ister)"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import makara_ders  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
M = KOK / ".kos/makara"
KASA = makara_ders.KASA
AD = "omer-makara-cek"
WORKFLOW = "gece.yml"
KID = re.compile(r"m[0-9a-f]{6}")
NW = 0x08000000  # CREATE_NO_WINDOW
KOK_USTU = {"omer-kurallar.md": Path(r"C:\Projeler\omer-kurallar.md")}


def yerel_hedef(h, kok=KOK):
    """Runner yolu (.../hedefler/<göreli>) → bu PC'deki dosya; yoksa ya da kök dışına çıkıyorsa None."""
    p = h.replace("\\", "/")
    if "/hedefler/" not in "/" + p:
        return None
    rel = ("/" + p).split("/hedefler/", 1)[1]
    if ".." in rel.split("/"):
        return None
    y = KOK_USTU.get(rel) or Path(kok) / rel
    return y if y.is_file() else None


def birlestir(dizin, m=M, kok=KOK):
    """indirilen artefakt dizini → m/kum. (yeni, zaten var, atlanan)."""
    kum = m / "kum"
    kum.mkdir(parents=True, exist_ok=True)
    yeni = var = atla = 0
    for p in sorted(Path(dizin).rglob("kum/*.json")):
        try:
            r = json.loads(p.read_text(encoding="utf-8"))
            hedef = yerel_hedef(r["hedef"], kok)
        except (ValueError, KeyError, TypeError):
            atla += 1; continue
        if not KID.fullmatch(str(r.get("id"))) or r.get("durum") != "bekliyor" or not hedef or not r.get("kural"):
            atla += 1; continue
        if (kum / f"{r['id']}.json").exists():
            var += 1; continue
        r.update(hedef=str(hedef), kaynak="bulut")
        (kum / f"{r['id']}.json").write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
        yeni += 1
    return yeni, var, atla


def rapor_not(dizin, kasa=KASA):
    """Bulut uyku notu (rapor/90-log/uyku-<gün>.md) → Obsidian uyku-<gün>-bulut.md; aynı ad = üzerine yazar, çift not yok."""
    n = 0
    for p in sorted(Path(dizin).rglob("90-log/uyku-*.md")):
        if "ozet" in p.name or "kuru" in p.name:
            continue
        y = Path(kasa) / "90-log" / f"{p.stem}-bulut.md"
        y.parent.mkdir(parents=True, exist_ok=True)
        y.write_bytes(p.read_bytes()); n += 1
    return n


def bulut_repo(kok=KOK):
    """MAKARA_BULUT_REPO → .kos/makara.json (bulut_repo) sırasıyla; ikisi de yoksa None."""
    if os.environ.get("MAKARA_BULUT_REPO"):
        return os.environ["MAKARA_BULUT_REPO"]
    y = Path(kok) / ".kos/makara.json"
    return json.loads(y.read_text(encoding="utf-8")).get("bulut_repo") if y.exists() else None


def gh(*a):
    return subprocess.run(["gh", *a], capture_output=True, text=True, creationflags=NW if os.name == "nt" else 0, timeout=300)


def cek(repo, m=M, kasa=KASA, kok=KOK):
    """En son başarılı, işlenmemiş koşuyu çeker. Çıktı tek satır."""
    durum_y = m / "cek.json"
    durum = json.loads(durum_y.read_text(encoding="utf-8")) if durum_y.exists() else {"islenen": []}
    r = gh("run", "list", "-R", repo, "--workflow", WORKFLOW, "--status", "success", "--limit", "5", "--json", "databaseId")
    if r.returncode:
        return f"gh run list başarısız ({r.returncode})"
    yeni = [i["databaseId"] for i in json.loads(r.stdout or "[]") if i["databaseId"] not in durum["islenen"]]
    toplam = [0, 0, 0]
    for rid in reversed(yeni):
        tmp = tempfile.mkdtemp(prefix="makara-cek-")
        try:
            r = gh("run", "download", str(rid), "-R", repo, "-D", tmp)
            if r.returncode:
                return f"gh run download {rid} başarısız ({r.returncode})"
            for i, v in enumerate(birlestir(tmp, m, kok)):
                toplam[i] += v
            rapor_not(tmp, kasa)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)  # kendi geçici dizinimiz
        durum["islenen"].append(rid)
        m.mkdir(parents=True, exist_ok=True)
        durum_y.write_text(json.dumps(durum), encoding="utf-8")
    return f"bulut: {len(yeni)} koşu · yeni öneri {toplam[0]} · zaten var {toplam[1]} · atlanan {toplam[2]}"


def kur(sil=False):
    if sil:
        return subprocess.run(["schtasks", "/Delete", "/TN", AD, "/F"], capture_output=True, text=True).returncode
    tr = f'conhost.exe --headless "{sys.executable}" "{Path(__file__).resolve()}"'
    r = subprocess.run(["schtasks", "/Create", "/TN", AD, "/SC", "HOURLY", "/TR", tr, "/F"], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    return r.returncode


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", nargs="?", choices=["kur", "kaldir"])
    ap.add_argument("--repo")
    a = ap.parse_args(argv)
    if a.komut:
        return kur(a.komut == "kaldir")
    a.repo = a.repo or bulut_repo()
    if not a.repo:
        return print("bulut repo ayarlı değil (MAKARA_BULUT_REPO / --repo)")
    s = cek(a.repo)
    if "yeni öneri 0" not in s and s.startswith("bulut"):
        import makara_gece
        makara_gece.onay_listesi()
    print(s)


if __name__ == "__main__":
    sys.exit(main())
