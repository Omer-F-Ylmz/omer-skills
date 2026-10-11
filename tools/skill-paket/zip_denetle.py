"""claude.ai'ye yüklemeden ÖNCE skill zip denetimi (yükleme reddini ve çöp dosyayı önceden yakalar).
  python tools/skill-paket/zip_denetle.py <zip ya da klasör> [...]   → sorun yoksa rc 0
Kontrol: SKILL.md var · name ve description var · description ≤ 1024 karakter ve XML/açılı ayraç (< >) yok
(claude.ai reddeder) · __pycache__/.pyc/.DS_Store yok · gizli anahtar deseni yok (değer yazdırılmaz)."""
import re
import sys
import zipfile
from pathlib import Path

GIZLI = re.compile(rb"sk-ant-[A-Za-z0-9_-]{8}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30}"
                   rb"|-----BEGIN [A-Z ]*PRIVATE KEY-----\s+[A-Za-z0-9+/=]{40}")  # PEM: gövdesi olan anahtar, tablo sözü değil
ORNEK = re.compile(rb"EXAMPLE|XXXX|EXPOSED|FAKE|DUMMY|\.\.\.", re.I)  # belge örneği/yer tutucu (AWS: AKIAIOSFODNN7EXAMPLE)
COP = re.compile(r"(^|/)(__pycache__/|\.DS_Store$|Thumbs\.db$)|\.pyc$")


def _on_bilgi(metin):
    m = re.match(r"^---\s*\n(.*?)\n---", metin, re.S)
    if not m:
        return {}
    alan, son = {}, None
    for satir in m.group(1).splitlines():
        k = re.match(r"^([A-Za-z_-]+):\s*(.*)$", satir)
        if k:
            son = k.group(1)
            alan[son] = k.group(2).strip().strip('"').strip("'")
        elif son and satir.startswith((" ", "\t")):
            alan[son] += " " + satir.strip()
    return alan


def denetle(zp):
    sorun = []
    with zipfile.ZipFile(zp) as z:
        adlar = z.namelist()
        skill = [a for a in adlar if a.split("/")[-1] == "SKILL.md"]
        if not skill:
            return [f"{Path(zp).name}: SKILL.md yok"]
        on = _on_bilgi(z.read(min(skill, key=len)).decode("utf-8", "replace"))
        acik = on.get("description", "")
        if not on.get("name"):
            sorun.append("frontmatter name yok")
        if not acik:
            sorun.append("frontmatter description yok")
        if len(acik) > 1024:
            sorun.append(f"description {len(acik)} karakter > 1024")
        if re.search(r"[<>]", acik):
            sorun.append("description XML/açılı ayraç içeriyor (claude.ai reddeder)")
        cop = [a for a in adlar if COP.search(a)]
        if cop:
            sorun.append(f"çöp dosya {len(cop)} (ör. {cop[0]}; __pycache__/.pyc)")
        gizli = [a for a in adlar if not a.endswith("/") and any(
            not ORNEK.search(b[m.start():m.end() + 24]) for b in [z.read(a)] for m in GIZLI.finditer(b))]
        if gizli:
            sorun.append(f"gizli anahtar deseni {len(gizli)} dosyada (ör. {gizli[0]})")
    return [f"{Path(zp).name}: {s}" for s in sorun]


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    zipler = [p for a in argv for p in (sorted(Path(a).glob("*.zip")) if Path(a).is_dir() else [Path(a)])]
    sorunlar = [s for z in zipler for s in denetle(z)]
    print("\n".join(sorunlar) or f"TEMİZ: {len(zipler)} zip")
    return 1 if sorunlar else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
