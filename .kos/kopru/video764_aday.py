"""VIDEO-764-4 adım 3: karar-v2 UYARLA/AL → aday listesi, ÖĞREN → öğrenme özeti. Kurulum yok.
python video764_aday.py cikar | ogren | yaz     (cikar/ogren Sonnet çağrısı, devam edebilir; yaz yerel)"""
import csv, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import video764_karar2 as K  # noqa: E402

HAM = K.OG / "video-764-aday-ham.json"; TSV = K.OG / "video-764-aday.tsv"; MD = K.OG / "video-764-ogren.md"
KATALOG = [K.V.R / "docs/katalog/yetenek.tsv", K.V.R / "skills/yetenek-getir/yetenek.tsv"]
ISTEM = ("Aşağıdaki video özetlerinde geçen kurulabilir aracı/repoyu/skill'i/MCP'yi çıkar. Video başına YALNIZ bir JSON dizisi öğesi: "
         '{"id":..., "ad":"aracın kendi adı (video başlığı değil)", "tur":"skill|mcp|repo|arac", "kaynak":"özette geçen repo/site linki, yoksa \\"\\"", '
         '"ne":"≤90 karakter ne yapar", "cc_cift":"evet|hayir|belki (Claude Code yerleşiği ya da yaygın skill/plugin ile çift mi)", '
         '"context":"dusuk|orta|yuksek (kurulunca bağlam maliyeti: MCP/çok araçlı yuksek, tek komut dusuk)", '
         '"token_hafiza":"evet|hayir (token tasarrufu, bağlam ya da hafıza aracı mı)", "kategori":"≤3 kelime"}. Başka metin yazma.\n\n')
OGREN = ("Aşağıda ÖĞREN sınıfı video kararlarının gerekçeleri var (satır: id | gerekçe). Tekrarları birleştirip öğrenilecek TEKNİK/PRATİKLERİ konuya göre grupla: "
         "markdown, her grup `## konu` + 2-6 madde (`- teknik — ne öğrenilir (id, id)`), toplam ≤120 satır. Araç listesi/haber gürültüsünü at. Başka metin yazma.\n\n")


def v2():
    with K.V2.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))


def cikar(n=25):
    ham = json.loads(HAM.read_text(encoding="utf-8")) if HAM.exists() else {}
    d = K.veri(); bekle = [d[r["id"]] for r in v2() if r["karar-v2"] in ("UYARLA", "AL") and r["id"] not in ham and r["id"] in d]
    for i in range(0, len(bekle), n):
        b = bekle[i:i + n]
        for o in K.json_oku(K.claude("claude-sonnet-5-5", ISTEM + K.metin(b))):
            ham[o["id"]] = o
        HAM.write_text(json.dumps(ham, ensure_ascii=False), encoding="utf-8"); print("aday parti", i // n + 1, len(b), flush=True)


def ogren():
    s = "\n".join(f"{r['id']} | {r['gerekçe']}" for r in v2() if r["karar-v2"] == "ÖĞREN")
    MD.write_text("# VIDEO-764 ÖĞREN özeti (karar-v2 ÖĞREN gerekçelerinden; kurulum yok, ÖĞREN 2. turun girdisi)\n\n" + K.claude("claude-sonnet-5-5", OGREN + s).strip() + "\n", encoding="utf-8")


def bizde():
    ad = set()
    for f in KATALOG:
        if f.exists():
            ad |= {ln.split("\t")[0].lower() for ln in f.read_text(encoding="utf-8").splitlines()[1:] if ln}
    ad |= {p.name.lower() for p in (Path.home() / ".claude/skills").iterdir()}
    return ad


def karsilik(a, ad):
    k = re.sub(r"[^a-z0-9]+", "-", a.lower()).strip("-")
    return ", ".join(sorted(x for x in ad if len(k) >= 4 and (k in x or (len(x) >= 4 and x in k)))[:3]) or "yok"


def yaz(ad=None):
    ham = json.loads(HAM.read_text(encoding="utf-8")); ad = ad if ad is not None else bizde(); kar = {r["id"]: r for r in v2()}
    gruplar = {}
    for i, o in ham.items():
        if i in kar:
            g = gruplar.setdefault(re.sub(r"[^a-z0-9]+", "", o.get("ad", "").lower()) or i, dict(o=o, v=[]))
            g["v"].append(kar[i])
    duz = lambda s: str(s).replace("\t", " ").replace("\n", " ")  # noqa: E731
    sat = ["ad\ttür\tkaynak\tne\tbizdeki karşılık\tbakım\tCC'de çift\tizin kapsamı\tcontext maliyeti\ttoken/hafıza\tkategori\tvideo sayısı\tvideo link\tkarar\tdoğrulanmadı"]
    for g in sorted(gruplar.values(), key=lambda g: -len(g["v"])):
        o, v = g["o"], g["v"]; k = "AL" if any(r["karar-v2"] == "AL" for r in v) else "UYARLA"
        bz = karsilik(o["ad"], ad)
        sat.append("\t".join(duz(x) for x in (o["ad"], o.get("tur", ""), o.get("kaynak", ""), o.get("ne", ""),
                                               ("UYARLA: bizdekiyle karşılaştır → " + bz) if bz != "yok" else "yok", "?", o.get("cc_cift", ""), "?",
                                               o.get("context", ""), o.get("token_hafiza", ""), o.get("kategori", ""), len(v), " ".join(r["link"] for r in v[:3]), k,
                                               "evet" if k == "AL" else "")))
    TSV.write_text("\n".join(sat) + "\n", encoding="utf-8", newline="\n"); print(len(sat) - 1, "aday")


if __name__ == "__main__":
    {"cikar": cikar, "ogren": ogren, "yaz": yaz}[sys.argv[1]]()
