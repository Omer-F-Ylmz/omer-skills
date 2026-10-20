"""ÖĞREN-4 d2 (G3 = video-medya + belge + pazarlama): v1 hattı + ★ 11:27 katmanı + ★ 11:58 (v) kaynak kuralı.
A = kanonik kurulu ∩ (d1'de yazılmış ∪ kullanim_30g>0 ∪ Odak ∪ müdür skill'de anılan), ≤150; B = geri kalan → betik kartı.
Ad listesi kalemi (claudeai_adlar.json) → dist zip'teki gerçek SKILL.md/TALIMAT; .mcp.json → eklenti kökü (README + plugin.json).
  python -X utf8 .claude/ogren4/v2.py hazirla      → kaynak/<ad>.txt + v2-ornek.tsv + v2-paket-N.md (yazılmamış A) + kart-b-g3.jsonl
  python -X utf8 .claude/ogren4/v2.py birlestir    → v1/v2-yazar-*.jsonl → .kos/kopru/ogren/ozet-g3-v2.jsonl + hakem-g3-v2.jsonl"""
import json, re, sys, zipfile
from functools import lru_cache
from glob import glob
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import v1
from v1 import B, O, A, adlari, dosya, kaynaksiz, oku, ozet3, ozet_kaynak, sert

ROL = v1.ROL[:-1] + ["belge üretimi", "belge okuma", "yazım", "bilgi tabanı", "pazarlama içeriği", "SEO", "marka", "video-dışı"]
ozet3.MEKANIZMA = ROL
KAT = {"video-medya": "departman-diger", "belge": "departman-belge", "pazarlama": "departman-diger"}
ODAK = set("""whisper-cli mcp-video-analyzer rapidocr tesseract ffmpeg ffprobe yt-dlp qwen3.5:4b video video-tarama video-uygula video-izle watch
remotion remotion-video-paket hyperframes hyperframes-paket motion-studio motion-os autoclip moneyprinter daymade-ses-paket premiere-mcp summarize crv
docx pptx xlsx pdf markitdown doc-coauthoring beautiful-article humanizer project-documenter documentation-and-adrs frontend-slides wowerpoint
teklif-kutusu fatura-kutusu prd-yaz prd-generator obsidian notebooklm qmd marketing-skills reklam-ads ecc-icerik-pazarlama linkedin-agent
ootto-content baoyu baoyu-paket brandkit brand-guidelines brand-systems seo fixing-metadata star-history""".split())
ONEK = ("writing-", "gstack-make-pdf", "gstack-document-", "obsidian", "remotion", "hyperframes", "motion-", "marketing", "business-marketing", "seo-")
ZIP = sorted(glob("dist/yukle-12/*/*.zip"), key=lambda z: ("_paket_yuklenen" not in z, "_paket_hazir" not in z, z)) + ["dist/eksik-metin.zip"]


@lru_cache(None)
def adlar_zip(z):
    return zipfile.ZipFile(z).namelist()


def kaynak_ret(yol):
    """★ 11:58 (v): kaynak yalnız ad listesi / .mcp.json / katalog satırı → mekanizma addan tahmin edilir → RET"""
    n = Path(str(yol)).name
    return "kaynak yalnız ad listesi/.mcp.json/katalog" if n in ("claudeai_adlar.json", ".mcp.json") or n.startswith("katalog") else None


def coz(ad):
    """ad listesi kalemi → "<zip>!<paket>/SKILL.md" (paket kalemi) ya da "<zip>!<skill dizini>/" (tüm .md'leri) ya da None"""
    for z in ZIP:
        for n in adlar_zip(z):
            if re.search(rf"(^|/){re.escape(ad)}/(SKILL|TALIMAT|REFERANS)\.md$", n):
                return f"{z}!{n}" if ad.endswith("-paket") else f"{z}!{n.rsplit('/', 1)[0]}/"
    p = Path.home() / ".claude/skills/gstack" / ad.removeprefix("gstack-") / "SKILL.md"  # gstack-* claude.ai adı → CC'deki gstack alt skill'i
    return str(p) if ad.startswith("gstack-") and p.is_file() else None


def metin(ad, yol):
    if ".zip!" in yol and yol.endswith("/"):
        z, i = yol.split("!", 1)
        return "".join(f"=== {n} ===\n" + zipfile.ZipFile(z).read(n).decode("utf-8", "replace") + "\n" for n in adlar_zip(z) if n.startswith(i) and n.endswith(".md"))
    return v1.metin(ad, yol)


def yazilmis():
    """d1 yazar satırları; kaynağı ad listesi/.mcp.json olanlar (addan tahmin) yeniden yazılır → hariç"""
    eski = v1.D()
    c = {}
    for p in sorted(B.glob("v1-yazar-*.jsonl")):
        c.update(oku(p))
    return {ad: y for ad, y in c.items() if not kaynak_ret(eski.get(ad, ""))}


def D():
    return dict(s.split("\t")[::3] for s in (B / "v2-ornek.tsv").read_text(encoding="utf-8").splitlines())


def katman(k, eski):
    mudur = "\n".join((Path("skills") / d / "SKILL.md").read_text(encoding="utf-8") for d in set(KAT.values()))
    anilan = lambda ad: len(ad) >= 4 and re.search(rf"(?<![\w-]){re.escape(ad)}(?![\w-])", mudur)
    a = [r for r in k.values() if r["ad"] in eski or r["kullanim_30g"] > 0 or r["ad"] in ODAK or r["ad"].startswith(ONEK) or anilan(r["ad"])]
    a.sort(key=lambda r: (r["ad"] not in eski, -r["kullanim_30g"], r["ad"] not in ODAK, r["ad"]))
    sec = {r["ad"] for r in a[:150]}
    return a[:150], [r for r in k.values() if r["ad"] not in sec]


def hazirla():
    t = [json.loads(x) for x in (O / "katalog-son.jsonl").read_text(encoding="utf-8").splitlines()]
    k = {r["ad"]: r for r in reversed(t) if r["kategori_son"] in KAT and r["tur"] != "aday" and r["kanonik"] == r["id"]}  # aynı adlı kopya: ilk kalır
    eski = yazilmis()
    ka, kb = katman(k, eski)
    (O / "kart-b-g3.jsonl").write_text("".join(json.dumps({"ad": r["ad"], "katman": "B", "ne": r["aciklama"], "nasil": "", "tur": r["tur"], "yol": r["yol"],
                                                          "kategori": r["kategori_son"]}, ensure_ascii=False) + "\n" for r in kb), encoding="utf-8")
    sec, bos = [], []
    for r in sorted(ka, key=lambda r: r["ad"]):
        y = v1.YOL.get(r["ad"], r["yol"])
        if Path(y).name == "claudeai_adlar.json":
            y = coz(r["ad"]) or y
        elif Path(y).name == ".mcp.json":
            y = str(Path(y).parent)  # eklenti kökü: d14.metin README + plugin.json okur
        try:
            m = "" if kaynak_ret(y) else metin(r["ad"], y)
        except OSError:  # katalogdaki yol artık yok → kaynaksız
            m = ""
        (bos if not m or kaynaksiz(adlari(r["ad"], y), m) else sec).append([r["ad"], r["tur"], str(r["bayt"]), y])
        if sec and sec[-1][0] == r["ad"]:
            dosya(r["ad"]).write_text(m, encoding="utf-8")
    (B / "v2-ornek.tsv").write_text("".join("\t".join(s) + "\n" for s in sec), encoding="utf-8")
    (B / "v2-kaynaksiz.tsv").write_text("".join("\t".join(s) + "\n" for s in bos), encoding="utf-8")
    (B / "a-liste.tsv").write_text("".join(f"{r['ad']}\t{r['kategori_son']}\t{r['kullanim_30g']}\t{r['tur']}\n" for r in ka), encoding="utf-8")
    yeni = [s for s in sec if s[0] not in eski]
    n = -(-len(yeni) // v1.PAKET)
    for i in range(n):
        parca = []
        for ad, _, _, kaynak in yeni[i::n]:  # şeritli dağıtım
            m, an = dosya(ad).read_text(encoding="utf-8"), sorted(adlari(ad, kaynak))
            parca += [f"## {ad}", f"kaynak: {dosya(ad)} (çözülmüş; özgün: {kaynak}) · {len(m.splitlines())} satır · araç adları ({len(an)}): {' · '.join(an[:30])}",
                      "BAŞLIKLAR: " + " · ".join(p.split("\n", 1)[0].strip()[:60] for p in v1.BASLIK.split(m)[1:])[:1500], ""]
        (B / f"v2-paket-{i + 1}.md").write_text("\n".join(parca), encoding="utf-8")
    print(f"A {len(ka)} (kaynaklı {len(sec)} · kaynaksız {len(bos)} · yazılmış {len(sec) - len(yeni)} · yeni {len(yeni)} → paket {n}) · B {len(kb)}")


def birlestir():
    ozet_kaynak.D = D()
    c = yazilmis()
    for p in sorted(B.glob("v2-yazar-*.jsonl")):
        c.update(oku(p))
    son, ret = {}, {}
    for ad, kaynak in D().items():
        if kaynak_ret(kaynak):
            ret[ad] = kaynak_ret(kaynak)
            continue
        if ad not in c:
            ret[ad] = "yazar satırı yok"
            continue
        m, y = dosya(ad).read_text(encoding="utf-8"), c[ad]
        r = {"ad": ad, "kaynak": str(dosya(ad)), "ozgun": kaynak, **{a: y[a]["deger"] for a in A}, "alinti": {a: y[a].get("alinti", "") for a in A},
             "mekanizma": y["mekanizma"], "kanit": y.get("kanit", ""), "dogrulandi": "claude-yazar"}
        neden, r["uyari"] = sert(r, m, adlari(ad, kaynak))
        if neden:
            ret[ad] = neden
        son[ad] = r
    for ad, h in ret.items():
        print("RET", ad, h, sep="\t")
    for ad, r in son.items():
        for u in r["uyari"]:
            print("UYARI", ad, u, sep="\t")
    (O / "ozet-g3-v2.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in son.values()), encoding="utf-8")
    (O / "hakem-g3-v2.jsonl").write_text("".join(json.dumps({k: r[k] for k in ["ad", "kaynak", "ozgun"] + A + ["mekanizma"]}, ensure_ascii=False) + "\n"
                                                for r in son.values()), encoding="utf-8")
    disi = [r for r in son.values() if "video-dışı" in r["mekanizma"]]  # ÖĞREN-0b'ye kategori hatası geri bildirimi
    (O / "g3-disi-geri.tsv").write_text("".join(f"{r['ad']}\t{r['ozgun']}\t{r['ne_yapar']}\t{r['kanit']}\n" for r in disi), encoding="utf-8")
    print(f"son {len(son)} · RET {len(ret)} (yazılmamış {sum(h == 'yazar satırı yok' for h in ret.values())}) · UYARI {sum(len(r['uyari']) for r in son.values())} · dışı {len(disi)}")


def tohum(t):
    """kapı örneklemi: ozet-g3-v2'den (RET'siz son kartlar) tohum t ile 25 kalem → hakem-g3-t<t>.jsonl + v2-t<t>-ornek.tsv"""
    import random
    son = list(oku(O / "ozet-g3-v2.jsonl").values())
    sec = random.Random(int(t)).sample(son, 25)
    (O / f"hakem-g3-t{t}.jsonl").write_text("".join(json.dumps({k: r[k] for k in ["ad", "kaynak", "ozgun"] + A + ["mekanizma"]}, ensure_ascii=False) + "\n"
                                                    for r in sec), encoding="utf-8")
    (B / f"v2-t{t}-ornek.tsv").write_text("".join(f"{r['ad']}\t\t\t{r['ozgun']}\n" for r in sec), encoding="utf-8")
    print(f"tohum {t}: {len(sec)} kalem · {len(sec) * 4} alan")


def puan(t, h1, h2):
    from d9 import puan as p
    ozet_kaynak.D = dict(s.split("\t")[::3] for s in (B / f"v2-t{t}-ornek.tsv").read_text(encoding="utf-8").splitlines())
    p(B / h1, B / h2)


if __name__ == "__main__":
    k = sys.argv[1:]
    {"hazirla": hazirla, "birlestir": birlestir, "tohum": lambda: tohum(k[1]), "puan": lambda: puan(*k[1:4])}[k[0]]()
