"""PAKET sistemi: skill klasörlerinden claude.ai uyumlu tek-giriş paket zip'i üretir. Hiçbir içerik atılmaz.
Kurallar: tek SKILL.md (alt → TALIMAT.md, daha derin → SKILL-ornek.md) · ≤200 dosya (gerekirse ek .md'ler REFERANS.md'de birleşir,
yine sığmazsa ValueError: çağıran böler) · adda 'claude' yok · açıklama ≤200.
Kullanım (modül): paketle(ad, konu, [kaynak_dizin...], cikti_dizini, onsoz=None) → (zip_yolu, dosya_sayisi); kural ihlali ValueError.
Kullanım (CLI): python paketle.py <paket-adi> "<konu>" <cikti_dizini> <skill_dizini>...
BÜYÜK mod (çok skill'li tema): alt skill başına en çok TALIMAT.md · REFERANS.md (ek .md'ler + ikili listesi) · KAYNAK-n.md
(diğer metinler, parça başına ~PARCA); tema taşarsa <ad>-1, -2… dengeli bölünür (≤200 dosya, zip ≤ BUYUK_BOYUT).
Kullanım: buyuk(ad, konu, [kaynak_dizin...], cikti_dizini) → [(zip, dosya_sayisi)...] · CLI: python paketle.py --buyuk <ad> "<konu>" <cikti> <dizin>..."""
import re, sys, zlib, zipfile, pathlib

SINIR = 200
BOYUT = 9_500_000
BUYUK_BOYUT = 9_000_000
PARCA = 1_200_000
METIN = 1_048_576
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


def yaz(ad, md, dosyalar, cikti, sinir=BOYUT):
    """dosyalar: {zip içi yol (paket adı önekisiz): bayt}. SKILL.md sayısı ve boyut denetlenir."""
    cikti = pathlib.Path(cikti); cikti.mkdir(parents=True, exist_ok=True)
    zp = cikti / f"{ad}.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{ad}/SKILL.md", md)
        for k, v in dosyalar.items():
            z.writestr(f"{ad}/{k}", v)
    skm = sum(1 for x in zipfile.ZipFile(zp).namelist() if x.split("/")[-1].lower() == "skill.md")
    if skm != 1 or zp.stat().st_size >= sinir:
        raise ValueError(f"{ad}: SKILL.md={skm}, boyut={zp.stat().st_size} (en fazla 1 ve < {sinir})")
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


NOT_BUYUK = ("> Not: claude.ai paket başına tek SKILL.md ve en çok 200 dosya kabul ediyor. Bu yüzden her alt skill en çok üç tür dosyaya "
             "sıkıştırıldı: `TALIMAT.md` (orijinal SKILL.md), `REFERANS.md` (tüm ek .md dosyaları `## [yol]` başlıklarıyla) ve "
             "`KAYNAK-n.md` (betik, json, css gibi diğer metin dosyaları `### yol` başlığı + kod bloğu olarak). Bir dosya gerekirse "
             "ilgili başlıktan aynen çıkarılıp yazılabilir. Resim/font gibi ikili (ya da 1 MB üstü) dosyalar alınmadı; listesi "
             "REFERANS.md sonunda, asılları Claude Code kurulumunda duruyor.\n")
NOT_TAL_B = ("\n> Paket notu: bu skill'in ek dosyaları aynı klasörde `REFERANS.md` (ek .md'ler) ve `KAYNAK-n.md` (diğer metin "
             "dosyaları) içinde yol başlıklarıyla duruyor. Metinde bir dosya yolu geçince o başlığı ara.\n")


def metin_mi(b):
    """Metin sayılan dosya: ≤1 MB, NUL baytsız, UTF-8."""
    if len(b) > METIN or b"\x00" in b:
        return False
    try:
        b.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def _buyuk_skill(d):
    """→ (dizin adı, ad, açıklama, {paket içi dosya: metin})."""
    d = pathlib.Path(d)
    ana = d / "SKILL.md" if (d / "SKILL.md").is_file() else d / "TALIMAT.md"
    tam = {f.relative_to(d).as_posix(): f.read_bytes() for f in sorted(d.rglob("*"))
           if f.is_file() and not {"node_modules", ".git"} & set(f.relative_to(d).parts)}
    tal = tam.pop(ana.relative_to(d).as_posix()).decode("utf-8", "replace")
    ad = (re.search(r"^name:\s*\"?([^\"\n]+)", tal, re.M) or [None, d.name])[1].strip()
    acik = (re.search(r"^description:\s*\"?(.*?)\"?\s*$", tal, re.M) or [None, ""])[1].strip()
    ikili = [(k, len(v)) for k, v in tam.items() if not metin_mi(v)]
    md = sorted(k for k, v in tam.items() if k.lower().endswith(".md") and metin_mi(v))
    diger = sorted(k for k, v in tam.items() if k not in md and metin_mi(v))
    out = {}
    ref = [f"\n\n---\n\n## [{k}]\n\n{tam[k].decode()}" for k in md]
    if ikili:
        ref.append("\n\n---\n\n## [ikili/büyük dosyalar — pakete alınmadı]\n\n"
                   + "\n".join(f"- `{k}` ({b // 1024} KB)" for k, b in ikili) + f"\n\nAsıl konum: `{d}`\n")
    if ref:
        out["REFERANS.md"] = f"# REFERANS — {ad}: birleştirilmiş ek .md dosyaları\n" + "".join(ref)
    parcalar, cur = [], ""
    for k in diger:
        m = tam[k].decode()
        cit = "`" * max(4, max((len(x) for x in re.findall(r"`+", m)), default=0) + 1)  # içerikteki çit kodu bloğu kırmasın
        blok = f"\n\n### {k}\n\n{cit}\n{m}\n{cit}\n"
        if cur and len(cur) + len(blok) > PARCA:
            parcalar.append(cur); cur = ""
        cur += blok
    if cur:
        parcalar.append(cur)
    for i, p in enumerate(parcalar, 1):
        out[f"KAYNAK-{i}.md"] = f"# KAYNAK {i}/{len(parcalar)} — {ad}: metin dosyaları (yol başlıklı)\n" + p
    if out:
        mm = re.match(r"﻿?---\r?\n.*?\r?\n---\r?\n", tal, re.S)
        tal = tal[:mm.end()] + NOT_TAL_B + tal[mm.end():] if mm else NOT_TAL_B + tal
    out["TALIMAT.md"] = tal
    return d.name, ad, acik, out


def _bol(sk, agirlik):
    """Skill'leri paketlere dağıtır: önce açgözlü (paket sayısı k), sonra ağırlığa göre dengeli; dengeli sınırı aşarsa açgözlü."""
    def sigar(cur):
        return 1 + sum(len(x[3]) for x in cur) <= SINIR and 3000 + sum(agirlik[x[0]] for x in cur) <= BUYUK_BOYUT  # 3000: SKILL.md dizini
    acgozlu, cur = [], []
    for s in sk:
        if cur and not sigar(cur + [s]):
            acgozlu.append(cur); cur = []
        cur.append(s)
    acgozlu.append(cur)
    k = len(acgozlu)
    if k == 1:
        return acgozlu
    w = lambda s: max(len(s[3]) / SINIR, agirlik[s[0]] / BUYUK_BOYUT)
    hedef = sum(w(s) for s in sk) / k
    dengeli, cur, a = [], [], 0.0
    for s in sk:
        if cur and len(dengeli) < k - 1 and a >= hedef - 1e-9:
            dengeli.append(cur); cur, a = [], 0.0
        cur.append(s); a += w(s)
    dengeli.append(cur)
    return dengeli if all(sigar(p) for p in dengeli) else acgozlu


def buyuk(ad, konu, kaynaklar, cikti):
    if "claude" in ad.lower() or "anthropic" in ad.lower():
        raise ValueError(f"paket adında claude/anthropic olamaz: {ad}")
    sk = sorted((_buyuk_skill(k) for k in kaynaklar), key=lambda s: s[1])
    if len({s[0] for s in sk}) != len(sk):
        raise ValueError("aynı dizin adı iki kez")
    aciklama(konu, len(sk))  # erken doğrulama
    agirlik = {s[0]: sum(len(zlib.compress(v.encode("utf-8"))) + 150 for v in s[3].values()) for s in sk}  # 150: zip başlığı
    for s in sk:
        if 1 + len(s[3]) > SINIR or 3000 + agirlik[s[0]] > BUYUK_BOYUT:
            raise ValueError(f"{s[0]}: tek başına sığmıyor ({len(s[3])} dosya, {agirlik[s[0]]} bayt)")
    paketler = _bol(sk, agirlik)
    sonuc = []
    for i, pk in enumerate(paketler, 1):
        pad = ad + (f"-{i}" if len(paketler) > 1 else "")
        pk_konu = konu + (f" (bölüm {i}/{len(paketler)})" if len(paketler) > 1 else "")
        md = (f"---\nname: {pad}\ndescription: \"{aciklama(pk_konu, len(pk))}\"\n---\n\n# {pad}\n\n"
              f"Bu paket {len(pk)} skill'i tek girişte toplar. Kullanım: aşağıdan işe uyan alt skill'i seç, `TALIMAT.md` dosyasını "
              "oku ve uygula; gerekirse aynı klasördeki REFERANS/KAYNAK dosyalarına bak.\n\n"
              + NOT_BUYUK + "\n| skill | ne zaman | dosya |\n|---|---|---|\n" + "\n".join(satir(a, b, c) for a, b, c, _ in pk) + "\n")
        dosyalar = {f"skills/{a}/{k}": v.encode("utf-8") for a, _, _, d in pk for k, v in d.items()}
        sonuc.append((yaz(pad, md, dosyalar, cikti, BUYUK_BOYUT), 1 + len(dosyalar)))
    return sonuc


def main(argv):
    if argv and argv[0] == "--buyuk":
        if len(argv) < 5:
            print(__doc__); return 2
        for zp, n in buyuk(argv[1], argv[2], argv[4:], argv[3]):
            print(f"{zp} · {n} dosya · {zp.stat().st_size // 1024} KB")
        return 0
    if len(argv) < 4:
        print(__doc__); return 2
    zp, n = paketle(argv[0], argv[1], argv[3:], argv[2])
    print(f"{zp} · {n} dosya · {zp.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
