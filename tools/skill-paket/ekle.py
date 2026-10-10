"""Var olan paket zip'ine yeni skill dizinleri ekler, aynı adla yeni zip üretir (claude.ai'de Replace ile güncellemek için).
Mevcut alt skill'ler bayt bayt aynı kalır. Aynı adlı alt skill varsa ValueError; --uzerine ile değiştirilir.
Sınır (200 dosya) aşılırsa hangi skill'lerin yeni pakete gitmesi gerektiği hata metninde yazar.
Kullanım: python ekle.py [--uzerine] <mevcut.zip> <cikti_dizini> <skill_dizini>..."""
import re, sys, zipfile, pathlib
import paketle as P


def _oku_paket(zp):
    z = zipfile.ZipFile(zp)
    ad = z.namelist()[0].split("/")[0]
    md = z.read(f"{ad}/SKILL.md").decode("utf-8")
    dosyalar = {n[len(ad) + 1:]: z.read(n) for n in z.namelist() if not n.endswith("/") and n != f"{ad}/SKILL.md"}
    return ad, md, dosyalar


def _alt_adlar(dosyalar):
    return {k.split("/")[1] for k in dosyalar if k.startswith("skills/")}


def ekle(zip_yolu, kaynaklar, cikti, uzerine=False):
    ad, md, dosyalar = _oku_paket(zip_yolu)
    yeni = [P._oku_skill(k) for k in kaynaklar]
    mevcut = _alt_adlar(dosyalar)
    cakisan = sorted(a for a, *_ in yeni if a in mevcut)
    if cakisan and not uzerine:
        raise ValueError(f"{ad}: zaten var: {', '.join(cakisan)} (değiştirmek için --uzerine)")
    for a in cakisan:
        dosyalar = {k: v for k, v in dosyalar.items() if not k.startswith(f"skills/{a}/")}
        md = "\n".join(l for l in md.split("\n") if f"`skills/{a}/TALIMAT.md`" not in l)

    def say(ekler):
        return 1 + len(dosyalar) + sum(len(d) for *_, d in ekler)

    birlesik = False
    if say(yeni) > P.SINIR:
        yeni_b = [(a, b, c, P._birlestir(d)) for a, b, c, d in yeni]
        birlesik = True
        sigan, tasan = [], []
        for s in yeni_b:
            (sigan if say(sigan + [s]) <= P.SINIR and not tasan else tasan).append(s)
        if tasan:
            raise ValueError(f"{ad}: {say(yeni_b)} dosya > {P.SINIR}; yeni pakete gitmesi gerekenler: "
                             + ", ".join(a for a, *_ in tasan))
        yeni = yeni_b
    for a, _, _, d in yeni:
        dosyalar.update({f"skills/{a}/{k}": v for k, v in d.items()})
    n = len(_alt_adlar(dosyalar))
    konu = re.search(r"^description:.*?paket \((.*?)\)\.", md, re.M)
    md = re.sub(r"^description:.*$", lambda m: f'description: "{P.aciklama(konu.group(1) if konu else ad, n)}"', md, count=1, flags=re.M)
    md = re.sub(r"\d+ skill'i tek girişte", f"{n} skill'i tek girişte", md, count=1)
    if birlesik and "> Not 2:" not in md:
        md = md.replace("\n| skill |", P.NOT2 + "\n| skill |", 1)
    md = md.rstrip("\n") + "\n" + "\n".join(P.satir(a, b, c) for a, b, c, _ in yeni) + "\n"
    zp = P.yaz(ad, md, dosyalar, cikti)
    return zp, 1 + len(dosyalar)


def main(argv):
    uzerine = "--uzerine" in argv
    a = [x for x in argv if x != "--uzerine"]
    if len(a) < 3:
        print(__doc__); return 2
    zp, n = ekle(a[0], a[2:], a[1], uzerine)
    print(f"{zp} · {n} dosya · {zp.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
