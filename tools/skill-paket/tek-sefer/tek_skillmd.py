"""claude.ai paket zip'inde tek SKILL.md kuralı: alt skill SKILL.md → TALIMAT.md, daha derindeki SKILL.md → SKILL-ornek.md.
Kullanım: python tek_skillmd.py <girdi_dizini> <cikti_dizini>"""
import re, sys, zipfile, pathlib

gir, cik = map(pathlib.Path, sys.argv[1:3])
cik.mkdir(parents=True, exist_ok=True)
NOT = ("\n> Not: claude.ai bir pakette yalnız tek SKILL.md kabul ettiği için alt skill'lerin talimat dosyası "
       "`skills/<ad>/TALIMAT.md` adını taşır (içerik orijinal SKILL.md ile aynı). Alt skill içinde \"SKILL.md\" geçen yerler kendi TALIMAT.md'sini kasteder.\n")
for zp in sorted(gir.glob("*.zip")):
    src = zipfile.ZipFile(zp)
    pk = src.namelist()[0].split("/")[0]
    ana, alt, ornek = 0, 0, 0
    with zipfile.ZipFile(cik / zp.name, "w", zipfile.ZIP_DEFLATED) as z:
        for n in src.namelist():
            if n.endswith("/"):
                continue
            veri = src.read(n)
            p = n.split("/")
            yeni = n
            if n == f"{pk}/SKILL.md":
                t = veri.decode("utf-8")
                t = t.replace("uygun alt skill'in SKILL.md'sini oku", "uygun alt skill'in dosyasını oku")
                t = t.replace("İlgili alt skill'in SKILL.md'sini oku", "İlgili alt skill'in dosyasını oku")
                t = re.sub(r"`skills/([^/`]+)/SKILL\.md`", r"`skills/\1/TALIMAT.md`", t)
                bas = t.find("\n| skill |")
                t = t[:bas] + NOT + t[bas:] if bas > 0 else t + NOT
                veri, ana = t.encode("utf-8"), ana + 1
            elif p[-1].lower() == "skill.md":
                if len(p) == 4 and p[1] == "skills":
                    yeni, alt = "/".join(p[:-1] + ["TALIMAT.md"]), alt + 1
                else:
                    yeni, ornek = "/".join(p[:-1] + ["SKILL-ornek.md"]), ornek + 1
            z.writestr(yeni, veri)
    kalan = sum(1 for n in zipfile.ZipFile(cik / zp.name).namelist() if n.split("/")[-1].lower() == "skill.md")
    print(f"{zp.name}: ana {ana} · alt {alt} · ornek {ornek} · kalan SKILL.md {kalan}")
    assert ana == 1 and kalan == 1, zp.name
