"""İKİ TARAF: /ajan-getir claude.ai paketi. Katalogdaki yerel `yol` istemleri zip içine gömülür (claude.ai'de ~/.claude yok).
claude.ai zip başına en çok 200 dosya kabul eder → istemler plugin başına tek dosyada birleşir (references/ajanlar/<grup>.md);
katalog yolu `references/ajanlar/<grup>.md#L<bas>-<bit>` olur, skill yalnız o satırları okur (az token).
  python tools/ajan_getir_zip.py   → dist/kalite-3/ajan-getir.zip"""
import re
import sys
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EN_COK_DOSYA = 200  # claude.ai: "Zip contains too many files (maximum 200)"
EN_BUYUK_BAYT = 400_000  # tek grup dosyası tavanı; aşan grup <grup>-2.md, -3.md … diye bölünür


def _slug(s):
    return re.sub(r"[^a-z0-9._-]+", "-", s.lower()).strip("-") or "x"


def _gruplar(ajanlar, sinir):
    """Plugin öneki (ad'daki ilk ':' öncesi; öneksiz = kullanıcı ajanı) → grup; grup sayısı sınırı aşarsa baş harfe göre kovalar."""
    anahtar = [_slug(ad.split(":")[0]) if ":" in ad else "kullanici" for ad, *_ in ajanlar]
    if len(set(anahtar)) > sinir:
        anahtar = [f"harf-{k[0]}" for k in anahtar]
    return anahtar


def paketle(skill, cikti):
    satirlar = skill.joinpath("katalog.tsv").read_text(encoding="utf-8").splitlines()
    ajanlar = [s.split("\t") for s in satirlar[1:] if s.strip()]
    gruplar = _gruplar(ajanlar, EN_COK_DOSYA - 2)  # SKILL.md + katalog.tsv
    icerik, bayt, parca, yeni = {}, {}, {}, [satirlar[0]]
    for (ad, model, tek, yol), grup in zip(ajanlar, gruplar):
        metin = Path(yol).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").rstrip("\n")
        boy = len(metin.encode("utf-8"))
        if bayt.get(grup, 0) and bayt[grup] + boy > EN_BUYUK_BAYT:
            parca[grup] = parca.get(grup, 1) + 1
            bayt[grup] = 0
        bayt[grup] = bayt.get(grup, 0) + boy
        grup = grup if parca.get(grup, 1) == 1 else f"{grup}-{parca[grup]}"
        dosya = icerik.setdefault(grup, [f"# {grup} ajanları (ajan-getir; katalog.tsv satır aralığıyla okunur)", ""])
        dosya += ["", f"<!-- ajan: {ad} -->"]
        bas = len(dosya) + 1
        dosya += metin.split("\n")
        yeni.append("\t".join((ad, model, tek, f"references/ajanlar/{grup}.md#L{bas}-{len(dosya)}")))
    cikti.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(cikti, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(skill / "SKILL.md", "ajan-getir/SKILL.md")
        for grup, dosya in sorted(icerik.items()):
            z.writestr(f"ajan-getir/references/ajanlar/{grup}.md", "\n".join(dosya) + "\n")
        z.writestr("ajan-getir/katalog.tsv", "\n".join(yeni) + "\n")
        assert len(z.namelist()) <= EN_COK_DOSYA, f"{len(z.namelist())} dosya > {EN_COK_DOSYA}"
    return cikti


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(paketle(KOK / "skills/ajan-getir", KOK / "dist/kalite-3/ajan-getir.zip"))
