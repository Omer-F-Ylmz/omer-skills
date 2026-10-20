"""ÖĞREN-2 d2 (G1 = frontend-tasarım + 3d + oyun-mod): ÖĞREN-4 v1.py hattı aynen (d14.metin · d13.sert · Claude yazar);
fark: kalem kümesi = G1 kanonik kurulu, A seçimi ★ 11:27 C (kullanım>0 ∪ odak ∪ departman-frontend anışı, ≤150), `mekanizma` = G1 ROL,
geri kalan her kanonik kalem → betik B kartı (model yok).
  python -X utf8 .claude/ogren2/g1.py secim       → g1-a.tsv (A) + g1-b.tsv (B)
  python -X utf8 .claude/ogren2/g1.py hazirla     → kaynak/<ad>.txt + g1-ornek.tsv + g1-paket-N.md
  python -X utf8 .claude/ogren2/g1.py birlestir   → g1-yazar-*.jsonl → ozet-g1.jsonl + hakem-g1.jsonl + g1-disi-geri.tsv
  python -X utf8 .claude/ogren2/g1.py b           → docs/atlas/kart.jsonl'a "katman":"B" satırları (frontmatter/katalogdan, uydurma yok)"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "ogren1"))
import d14, ozet3, ozet_kaynak
from d13 import A, O, sert
from ozet3 import BASLIK, adlari, kaynaksiz
from son import oku

ROL = ["referans çıkarma", "tasarım yönü", "kod üretimi", "bileşen kaynağı", "animasyon", "3d sahne", "görsel üretim",
       "görsel doğrulama", "erişilebilirlik-performans", "oyun-mod", "rehber", "G1-dışı"]
ozet3.MEKANIZMA[:] = ROL  # gecerli_b modül globalini okur
B = Path(__file__).parent
K = B / "kaynak"
KOK = Path(__file__).parents[2]
KART = KOK / "docs" / "atlas" / "kart.jsonl"
G1 = {"frontend-tasarım", "3d", "oyun-mod"}
TAVAN, PAKET = 150, 12
ODAK = ["frontend-craft", "impeccable", "taste", "ui-ux-pro-max", "design-dna", "scroll-craft", "web-sahne", "gsap", "lenis",
        "threejs", "three-", "r3f", "react-three", "motion-foundations", "motion-patterns", "motion-advanced", "animasyon-scroll",
        "web-stil-sayfa", "21st", "magic", "stitch", "figma", "claude-design", "pixeljury", "playwright", "puppeteer", "axe",
        "create-design-md", "tasarim-katalog", "fixing-motion",
        "blender", "godot", "unity", "comfyui", "rembg", "gorsel-uret", "generate-image", "banana", "ideagram", "illustrasyon-logo",
        "mod-atolyesi", "oyun-mod", "3dmigoto", "xxmi", "oyun-gelistirme", "roblox", "gmod"]


def dosya(ad):
    return K / (re.sub(r"[^\w.-]", "_", ad) + ".txt")


def metin(ad, yol):
    """d14.metin + model kataloğu: dosyanın tamamı değil yalnız kalemin girdisi"""
    p = Path(yol)
    if p.name == "claudeai_adlar.json":  # yalnız ad listesi, aracı anlatan metin yok → kaynaksız (d2: yazarlar addan mekanizma tahmin etti)
        return ""
    if p.name == "omni_models_api.json":
        j = json.loads((KOK / yol if not p.is_absolute() else p).read_text(encoding="utf-8"))
        g = j.items() if isinstance(j, dict) else enumerate(j)
        return "".join(f"=== kayıt: {p.name} · {ad} ===\n" + json.dumps(v, ensure_ascii=False, indent=2) + "\n"
                       for _, v in g if ad in json.dumps(v, ensure_ascii=False))
    return d14.metin(ad, yol)


def kanonik():
    t = [json.loads(x) for x in (O / "katalog-son.jsonl").read_text(encoding="utf-8").splitlines()]
    k = sorted((r for r in t if r["kategori_son"] in G1 and r["tur"] != "aday" and r["kanonik"] == r["id"]), key=lambda r: r["kullanim_30g"])
    return list({r["ad"]: r for r in k}.values())  # aynı adlı kopya: en çok kullanılan kalır


def secim():
    mudur = (KOK / "skills" / "departman-frontend" / "SKILL.md").read_text(encoding="utf-8").lower()
    k = kanonik()
    def a_mi(r):
        ad = r["ad"].lower()
        return r["kullanim_30g"] > 0 or any(o in ad for o in ODAK) or (len(ad) >= 4 and re.search(rf"(?<![\w-]){re.escape(ad)}(?![\w-])", mudur))
    a = sorted((r for r in k if a_mi(r)), key=lambda r: (-r["kullanim_30g"], r["katman"] != "A", r["ad"]))
    a, kes = a[:TAVAN], a[TAVAN:]
    ai = {r["id"] for r in a}
    satir = lambda rs: "".join("\t".join([r["id"], r["ad"], r["tur"], r["kategori_son"], str(r["kullanim_30g"]), r["yol"]]) + "\n" for r in rs)
    (B / "g1-a.tsv").write_text(satir(a), encoding="utf-8")
    (B / "g1-b.tsv").write_text(satir(r for r in k if r["id"] not in ai), encoding="utf-8")
    print(f"kanonik {len(k)} · A {len(a)} (kesilen {len(kes)} → B) · B {len(k) - len(a)}")


def D():
    return dict(s.split("\t")[::3] for s in (B / "g1-ornek.tsv").read_text(encoding="utf-8").splitlines())


def hazirla():
    K.mkdir(exist_ok=True)
    sec, bos = [], []
    for s in (B / "g1-a.tsv").read_text(encoding="utf-8").splitlines():
        _, ad, tur, _, _, yol = s.split("\t")
        try:
            m = metin(ad, yol)
        except (OSError, ValueError, KeyError) as e:  # açılmayan kaynak → kaynaksız listesine, hat durmaz
            m = f"(açılamadı: {e})"
        if kaynaksiz(adlari(ad, yol), m):
            bos.append([ad, tur, "0", yol])
            continue
        dosya(ad).write_text(m, encoding="utf-8")
        sec.append([ad, tur, str(len(m)), yol])
    (B / "g1-ornek.tsv").write_text("".join("\t".join(s) + "\n" for s in sec), encoding="utf-8")
    (B / "g1-kaynaksiz.tsv").write_text("".join("\t".join(s) + "\n" for s in bos), encoding="utf-8")
    ozet_kaynak.D = D()
    n = -(-len(sec) // PAKET)
    for i in range(n):
        parca = []
        for ad, _, _, kaynak in sec[i::n]:  # şeritli dağıtım: büyük/küçük kaynaklar paketlere yayılır
            m, an = dosya(ad).read_text(encoding="utf-8"), sorted(adlari(ad, kaynak))
            parca += [f"## {ad}", f"kaynak: {dosya(ad)} (çözülmüş; özgün: {kaynak}) · {len(m.splitlines())} satır · araç adları ({len(an)}): {' · '.join(an[:30])}",
                      "BAŞLIKLAR: " + " · ".join(p.split("\n", 1)[0].strip()[:60] for p in BASLIK.split(m)[1:])[:1500], ""]
        (B / f"g1-paket-{i + 1}.md").write_text("\n".join(parca), encoding="utf-8")
    print(f"kaynaklı {len(sec)} · kaynaksız {len(bos)} · paket {n}")


def birlestir():
    ozet_kaynak.D = D()
    c = {}
    for p in sorted(B.glob("g1-yazar-*.jsonl")):
        c.update(oku(p))
    son, ret = {}, {}
    for ad, kaynak in D().items():
        if ad not in c:
            ret[ad] = "yazar satırı yok"
            continue
        m, y = dosya(ad).read_text(encoding="utf-8"), c[ad]
        r = {"ad": ad, "kaynak": str(dosya(ad)), "ozgun": kaynak, **{a: y[a]["deger"] for a in A}, "alinti": {a: y[a].get("alinti", "") for a in A},
             "ne_zaman": y.get("ne_zaman", ""), "mekanizma": y["mekanizma"], "kanit": y.get("kanit", ""), "dogrulandi": "claude-yazar"}
        neden, r["uyari"] = sert(r, m, adlari(ad, kaynak))
        if neden:
            ret[ad] = neden
        son[ad] = r
    for ad, h in ret.items():
        print("RET", ad, h, sep="\t")
    for ad, r in son.items():
        for u in r["uyari"]:
            print("UYARI", ad, u, sep="\t")
    (O / "ozet-g1.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in son.values()), encoding="utf-8")
    (O / "hakem-g1.jsonl").write_text("".join(json.dumps({k: r[k] for k in ["ad", "kaynak", "ozgun"] + A + ["mekanizma"]}, ensure_ascii=False) + "\n"
                                              for r in son.values()), encoding="utf-8")
    disi = [r for r in son.values() if "G1-dışı" in r["mekanizma"]]  # ÖĞREN-0b'ye kategori hatası geri bildirimi
    (O / "g1-disi-geri.tsv").write_text("".join(f"{r['ad']}\t{r['ozgun']}\t{r['ne_yapar']}\t{r['kanit']}\n" for r in disi), encoding="utf-8")
    print(f"son {len(son)} · RET {len(ret)} · UYARI {sum(len(r['uyari']) for r in son.values())} · G1-dışı {len(disi)}")


def onyuz(yol):
    """SKILL.md/komut/ajan .md frontmatter'ı → {anahtar: değer}; yoksa {}"""
    p = Path(yol)
    p = p / "SKILL.md" if p.is_dir() else p
    if p.suffix != ".md" or not p.is_file():
        return {}
    m = re.match(r"---\r?\n(.*?)\r?\n---", p.read_text(encoding="utf-8", errors="replace"), re.S)
    return dict(re.findall(r"^(\w[\w-]*):\s*(.+?)\s*$", m.group(1), re.M)) if m else {}


def komut(r, f):
    """birebir çağrı adı: skill/ajan frontmatter name · slash komutu /dosya-adı · cli/mcp kendi adı; yoksa boş"""
    if r["tur"] == "komut":
        return "/" + Path(r["yol"]).stem
    if r["tur"] in ("cli", "mcp", "model"):
        return r["ad"]
    return f.get("name", "").strip("'\"") or "kaynak yetersiz — frontmatter name yok"


def b():
    eski = {json.loads(x)["ad"] for x in KART.read_text(encoding="utf-8").splitlines() if json.loads(x).get("katman") == "B"}
    yeni, kat_ne = [], {r["id"]: r["aciklama"] for r in kanonik()}
    for s in (B / "g1-b.tsv").read_text(encoding="utf-8").splitlines():
        i, ad, tur, kat, _, yol = s.split("\t")
        if ad in eski:
            continue
        f = onyuz(yol)
        yeni.append({"ad": ad, "ne": f.get("description", "").strip("'\"") or kat_ne.get(i) or "kaynak yetersiz — açıklama yok",
                     "komut": komut({"ad": ad, "tur": tur, "yol": yol}, f), "kanit": yol, "kategori": kat, "tur": tur, "katman": "B"})
    with KART.open("ab") as h:  # bayt olarak ekle: write_text CRLF'ye çevirir
        h.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in yeni).encode("utf-8"))
    print(f"B kartı +{len(yeni)} · boş ne {sum(not r['ne'] for r in yeni)} · boş komut {sum(not r['komut'] for r in yeni)}")


if __name__ == "__main__":
    {"secim": secim, "hazirla": hazirla, "birlestir": birlestir, "b": b}[sys.argv[1]]()
