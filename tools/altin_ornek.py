"""TARA-KOD-1 aşama 3: ana oturumun son seçimini kaydet; sonraki taramalar bundan öğrenir.
  python tools/altin_ornek.py kaydet "<iş>" <seçim dosyası>   satır biçimi: adım · araç · neden  (araç = 2. alan; tek alan varsa o)
  python tools/altin_ornek.py olc                              kayıtlı örnekler için aday kümesinin seçimi kapsama oranı
Kayıt: .kos/kopru/altin-ornek/ornekler.jsonl {is, secim[], kacirilan[], gun}. kacirilan = seçimde olup aday kümesinde olmayan →
sonraki benzer taramada 'ALTIN!' grubunda öne çıkar. Kaçıranlar için `beyin kaydet` ile 2. beyne tek satır ders yazılır (beyin yoksa atlanır)."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
DOSYA = KOK / ".kos" / "kopru" / "altin-ornek" / "ornekler.jsonl"
SATIR = 130
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import envanter_tara as et  # noqa: E402


def ad_say(s):
    return re.sub(r"^(skill|ajan|mcp):", "", s.strip().strip("`*"))


def secim_oku(yol):
    out = []
    for s in Path(yol).read_text(encoding="utf-8").splitlines():
        s = s.strip()
        if not s or s.startswith("#"):
            continue
        k = s.split(" · ")
        a = ad_say(k[1] if len(k) > 2 else re.sub(r"^[-*\d.)\s]+", "", k[0]))
        for p in re.split(r"\s*\+\s*|\s*,\s*", a):  # "a + b" → iki araç
            if p:
                out.append(p)
    return out


def kume_adlari(is_):
    metin = "\n".join(et.birlestir(is_, SATIR))
    return {duz for duz in (et.duz(x) for x in re.findall(r"^([^ ·]+(?: \([^)]*\))?)(?= ·)", metin, re.M))} | {et.duz(metin)}


def kapsama(is_, secim):
    metin = et.duz("\n".join(et.birlestir(is_, SATIR)))
    # ana paket listedeyse alt skill'i (ana:alt) kapsanmış sayılır
    kac = [a for a in secim if et.duz(a) not in metin and not (":" in a and et.duz(a.split(":")[0]) in metin)]
    return kac


def kaydet(is_, yol):
    secim = secim_oku(yol)
    kac = kapsama(is_, secim)
    DOSYA.parent.mkdir(parents=True, exist_ok=True)
    kayit = {"is": is_, "secim": secim, "kacirilan": kac, "gun": sys.argv[0] and ""}
    with DOSYA.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
    print(f"kaydedildi: {len(secim)} seçim, kaçırılan {len(kac)}: {', '.join(kac) or '-'}")
    if kac and shutil.which("beyin"):
        ders = f"envanter taraması '{is_}' için şunları kaçırdı: {', '.join(kac)}; aday kümesine ekle"
        try:
            subprocess.run(["beyin", "kaydet", ders], capture_output=True, timeout=30, cwd=KOK)
        except Exception:
            pass
    return 0


def olc():
    top = kac = 0
    for s in DOSYA.read_text(encoding="utf-8").splitlines() if DOSYA.exists() else []:
        o = json.loads(s)
        k = kapsama(o["is"], o["secim"])
        top += len(o["secim"])
        kac += len(k)
        print(f"{o['is']}: {len(o['secim']) - len(k)}/{len(o['secim'])} kaçırılan: {', '.join(k) or '-'}")
    print(f"recall {100 * (top - kac) / top:.1f}%" if top else "kayıt yok")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["kaydet"] and len(a) == 3:
        sys.exit(kaydet(a[1], a[2]))
    if a[:1] == ["olc"]:
        sys.exit(olc())
    print(__doc__)
    sys.exit(2)
