"""claude.ai sınırları: paket başına ≤200 dosya, adda 'claude' yasak.
azure → 2 paket, marketing → 1 paket (alt .md referansları skill başına REFERANS.md'de birleşir; betik/yaml/json olduğu gibi kalır),
claude-ads → reklam-ads-paket. Çıktı: /mnt/user-data/uploads/y12/p3/"""
import re, zipfile, pathlib, collections

GIR = pathlib.Path("/mnt/user-data/uploads/y12/p2/diger")
CIK = pathlib.Path("/mnt/user-data/uploads/y12/p3"); CIK.mkdir(parents=True, exist_ok=True)
NOT_TAL = ("\n> Paket notu: bu skill'in ek .md dosyaları (ör. references/*.md) claude.ai'nin 200 dosya sınırı yüzünden tek dosyada "
           "birleştirildi: aynı klasördeki `REFERANS.md`. Her biri `## [yol]` başlığı altında, içerik aynen. Metinde bir .md yolu "
           "geçince REFERANS.md'de o başlığı ara. Betik/yaml/json dosyaları yerinde.\n")
NOT_KOK = ("\n> Not 2: alt skill'lerin ek .md dosyaları (references/ vb.) skill klasöründeki `REFERANS.md`'de `## [yol]` başlıklarıyla "
           "birleşiktir (claude.ai paket başına 200 dosya sınırı); betik/yaml/json dosyaları olduğu gibi duruyor.\n")


def oku(zp):
    z = zipfile.ZipFile(zp)
    pk = z.namelist()[0].split("/")[0]
    kok = z.read(f"{pk}/SKILL.md").decode("utf-8")
    alt = collections.defaultdict(dict)
    for i in z.infolist():
        if i.is_dir() or i.filename == f"{pk}/SKILL.md":
            continue
        p = i.filename.split("/")
        alt[p[2]]["/".join(p[3:])] = z.read(i)
    return pk, kok, alt


def birlestir(dosyalar):
    """TALIMAT.md + diğer .md → REFERANS.md; diğerleri aynen."""
    refs = sorted(k for k in dosyalar if k.lower().endswith(".md") and k != "TALIMAT.md")
    if not refs:
        return dict(dosyalar)
    out = {k: v for k, v in dosyalar.items() if not (k.lower().endswith(".md") and k != "TALIMAT.md")}
    parca = ["# REFERANS — bu skill'in birleştirilmiş ek .md dosyaları\n"]
    for k in refs:
        parca.append(f"\n\n---\n\n## [{k}]\n\n" + dosyalar[k].decode("utf-8", "replace"))
    out["REFERANS.md"] = "".join(parca).encode("utf-8")
    t = dosyalar["TALIMAT.md"].decode("utf-8", "replace")
    m = re.match(r"---\n.*?\n---\n", t, re.S)
    t = t[:m.end()] + NOT_TAL + t[m.end():] if m else NOT_TAL + t
    out["TALIMAT.md"] = t.encode("utf-8")
    return out


def yaz(ad, acik, kok_govde, satirlar, alt, ekle_not=True):
    assert "claude" not in ad.lower() and len(acik) <= 200, (ad, len(acik))
    g = re.sub(r"^---\n.*?\n---\n", f'---\nname: {ad}\ndescription: "{acik}"\n---\n', kok_govde, flags=re.S)
    g = re.sub(r"^# .*$", f"# {ad}", g, count=1, flags=re.M)
    g = re.sub(r"Bu paket \d+ skill'i", f"Bu paket {len(satirlar)} skill'i", g)
    bas = g.find("\n| skill |")
    tablo = "\n| skill | ne zaman | dosya |\n|---|---|---|\n" + "\n".join(satirlar) + "\n"
    g = g[:bas] + (NOT_KOK if ekle_not else "") + tablo
    n = 1
    with zipfile.ZipFile(CIK / f"{ad}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{ad}/SKILL.md", g)
        for d, fs in alt.items():
            for k, v in fs.items():
                z.writestr(f"{ad}/skills/{d}/{k}", v); n += 1
    skm = sum(1 for x in zipfile.ZipFile(CIK / f"{ad}.zip").namelist() if x.split("/")[-1].lower() == "skill.md")
    print(f"{ad}: {len(satirlar)} skill · {n} dosya · SKILL.md {skm} · açıklama {len(acik)}")
    assert n <= 200 and skm == 1


def satirlar_(kok):
    return [l for l in kok.splitlines() if l.startswith("| ") and "`skills/" in l]


def dizin(l):
    return re.search(r"`skills/([^/`]+)/TALIMAT\.md`", l).group(1)


# azure → 2
pk, kok, alt = oku(GIR / "azure-paket.zip")
alt = {d: birlestir(f) for d, f in alt.items()}
B = {"azure--microsoft-foundry", "foundry-iq-skills--foundry-iq", "azure--finetuning", "azure--deploy-model", "azure--azure-ai",
     "azure--azure-aigateway", "azure--azure-app-onboard", "azure--azure-app-onboard-prereq", "azure--azure-deploy", "azure--azure-prepare",
     "azure--azure-validate", "azure--deploy", "azure--prepare", "azure--preset", "azure--scaffold", "azure--customize",
     "azure--python-appservice-deploy", "azure--discover-azure-skills"}
S = satirlar_(kok)
assert {dizin(l) for l in S} == set(alt), "tablo/dizin uyuşmazlığı"
sa = [l for l in S if dizin(l) not in B]; sb = [l for l in S if dizin(l) in B]
yaz("azure-altyapi-paket", f"{len(sa)} skill'lik paket (Azure altyapı: AKS/Kubernetes, işlem, depolama, kota, güvenilirlik, maliyet, Kusto, Entra, Azure Local, tanılama). İlgili alt skill'in dosyasını oku ve uygula.",
    kok, sa, {d: alt[d] for d in alt if d not in B})
yaz("azure-uygulama-ai-paket", f"{len(sb)} skill'lik paket (Azure uygulama ve AI: Foundry, model dağıtımı, fine-tuning, AI gateway, onboarding, hazırla/doğrula/dağıt, App Service). İlgili alt skill'in dosyasını oku ve uygula.",
    kok, sb, {d: alt[d] for d in alt if d in B})

# marketing → 1
pk, kok, alt = oku(GIR / "marketing-skills-paket.zip")
alt = {d: birlestir(f) for d, f in alt.items()}
S = satirlar_(kok)
assert {dizin(l) for l in S} == set(alt)
yaz("marketing-skills-paket", re.search(r'description: "([^"]+)"', kok).group(1), kok, S, alt)

# claude-ads → reklam-ads-paket (dosyalar aynen)
pk, kok, alt = oku(GIR / "claude-ads-paket.zip")
S = satirlar_(kok)
yaz("reklam-ads-paket", re.search(r'description: "([^"]+)"', kok).group(1), kok, S, alt, ekle_not=False)
