"""PAKET sistemi: skill klasörlerinden claude.ai uyumlu tek-giriş paket zip'i üretir. Hiçbir içerik atılmaz.
Kurallar: tek SKILL.md (alt → TALIMAT.md, daha derin → SKILL-ornek.md) · ≤200 dosya (gerekirse ek .md'ler REFERANS.md'de birleşir,
yine sığmazsa ValueError: çağıran böler) · adda 'claude' yok · açıklama ≤200.
Kullanım (modül): paketle(ad, konu, [kaynak_dizin...], cikti_dizini, onsoz=None) → (zip_yolu, dosya_sayisi); kural ihlali ValueError.
Kullanım (CLI): python paketle.py <paket-adi> "<konu>" <cikti_dizini> <skill_dizini>..."""
import re, sys, zipfile, pathlib

SINIR = 200
BOYUT = 9_500_000
NOT1 = ("> Not: claude.ai bir pakette yalnız tek SKILL.md kabul ettiği için alt skill'lerin talimat dosyası "
        "`skills/<ad>/TALIMAT.md` adını taşır (içerik orijinal SKILL.md ile aynı). Alt skill içinde \"SKILL.md\" geçen yerler kendi TALIMAT.md'sini kasteder.\n")
NOT2 = ("\n> Not 2: alt skill'lerin ek .md dosyaları (references/ vb.) skill klasöründeki `REFERANS.md`'de `## [yol]` başlıklarıyla "
        "birleşiktir (claude.ai paket başına 200 dosya sınırı); betik/yaml/json dosyaları olduğu gibi duruyor.\n")
NOT_TAL = ("\n> Paket notu: bu skill'in ek .md dosyaları claude.ai'nin 200 dosya sınırı yüzünden aynı klasördeki `REFERANS.md`'de "
           "`## [yol]` başlıklarıyla birleşti, içerik aynen. Metinde bir .md yolu geçince REFERANS.md'de o başlığı ara.\n")


def _oku_skill(d):
    d = pathlib.Path(d)
    ana = d / "SKILL.md" if (d / "SKILL.md").is_file() else d / "TALIMAT.md"
    dosyalar = {}
    for f in sorted(d.rglob("*")):
        if f.is_file():
            r = f.relative_to(d).as_posix()
            dosyalar["TALIMAT.md" if f == ana else r] = f.read_bytes()
    t = dosyalar["TALIMAT.md"].decode("utf-8", "replace")
    ad = (re.search(r"^name:\s*\"?([^\"\n]+)", t, re.M) or [None, d.name])[1].strip()
    acik = (re.search(r"^description:\s*\"?(.*?)\"?\s*$", t, re.M) or [None, ""])[1].strip()
    for k in list(dosyalar):
        if k != "TALIMAT.md" and k.split("/")[-1].lower() == "skill.md":
            dosyalar[k.rsplit("/", 1)[0] + "/SKILL-ornek.md" if "/" in k else "SKILL-ornek.md"] = dosyalar.pop(k)
    return d.name, ad, acik, dosyalar


def _birlestir(dosyalar):
    refs = sorted(k for k in dosyalar if k.lower().endswith(".md") and k != "TALIMAT.md")
    if not refs:
        return dosyalar
    out = {k: v for k, v in dosyalar.items() if k not in refs}
    out["REFERANS.md"] = ("# REFERANS — bu skill'in birleştirilmiş ek .md dosyaları\n" + "".join(
        f"\n\n---\n\n## [{k}]\n\n" + dosyalar[k].decode("utf-8", "replace") for k in refs)).encode("utf-8")
    t = dosyalar["TALIMAT.md"].decode("utf-8", "replace")
    m = re.match(r"---\n.*?\n---\n", t, re.S)
    out["TALIMAT.md"] = (t[:m.end()] + NOT_TAL + t[m.end():] if m else NOT_TAL + t).encode("utf-8")
    return out


def aciklama(konu, n):
    acik = f"{n} skill'lik paket ({konu}). İlgili alt skill'in dosyasını oku ve uygula."
    if len(acik) > 200:
        raise ValueError(f"açıklama {len(acik)} > 200 karakter; konuyu kısalt")
    return acik


def satir(a, b, c):
    return f"| {b} | {(c or '-').replace('|', '/')[:160]} | `skills/{a}/TALIMAT.md` |"


def yaz(ad, md, dosyalar, cikti):
    """dosyalar: {zip içi yol (paket adı önekisiz): bayt}. SKILL.md sayısı ve boyut denetlenir."""
    cikti = pathlib.Path(cikti); cikti.mkdir(parents=True, exist_ok=True)
    zp = cikti / f"{ad}.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{ad}/SKILL.md", md)
        for k, v in dosyalar.items():
            z.writestr(f"{ad}/{k}", v)
    skm = sum(1 for x in zipfile.ZipFile(zp).namelist() if x.split("/")[-1].lower() == "skill.md")
    if skm != 1 or zp.stat().st_size >= BOYUT:
        raise ValueError(f"{ad}: SKILL.md={skm}, boyut={zp.stat().st_size} (en fazla 1 ve < {BOYUT})")
    return zp


def paketle(ad, konu, kaynaklar, cikti, onsoz=None):
    if "claude" in ad.lower() or "anthropic" in ad.lower():
        raise ValueError(f"paket adında claude/anthropic olamaz: {ad}")
    sk = [_oku_skill(k) for k in kaynaklar]
    if len({s[0] for s in sk}) != len(sk):
        raise ValueError("aynı dizin adı iki kez")
    birlesik = False
    if 1 + sum(len(s[3]) for s in sk) > SINIR:
        sk = [(a, b, c, _birlestir(d)) for a, b, c, d in sk]
        birlesik = True
    n = 1 + sum(len(s[3]) for s in sk)
    if n > SINIR:
        raise ValueError(f"{ad}: {n} dosya > {SINIR}; böl")
    acik = aciklama(konu, len(sk))
    md = (f"---\nname: {ad}\ndescription: \"{acik}\"\n---\n\n# {ad}\n\n"
          + (onsoz or f"Bu paket {len(sk)} skill'i tek girişte toplar (claude.ai skill sınırı ve jeton tasarrufu). "
             "Kullanım: aşağıdan işe uyan alt skill'i seç, dosyasını oku, talimatını uygula. Birden çok alt skill gerekebilir.") + "\n\n"
          + NOT1 + (NOT2 if birlesik else "") + "\n| skill | ne zaman | dosya |\n|---|---|---|\n"
          + "\n".join(satir(a, b, c) for a, b, c, _ in sk) + "\n")
    dosyalar = {f"skills/{a}/{k}": v for a, _, _, d in sk for k, v in d.items()}
    return yaz(ad, md, dosyalar, cikti), n


def main(argv):
    if len(argv) < 4:
        print(__doc__); return 2
    zp, n = paketle(argv[0], argv[1], argv[3:], argv[2])
    print(f"{zp} · {n} dosya · {zp.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
