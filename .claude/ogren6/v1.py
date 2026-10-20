"""ÖĞREN-6 d1 (G4: test-qa + güvenlik + backend-dotnet + veri-db): ÖĞREN-4 v1 hattı (d14.metin · d13.sert · Claude yazar) +
★ 11:27 katmanı: A = kanonik kurulu ∩ (kullanim_30g>0 ∪ Odak ∪ müdür skill'de anılan), ≤150, kullanım sırası; B = geri kalan → betik kartı.
  python -X utf8 .claude/ogren6/v1.py hazirla      → kaynak/<ad>.txt + v1-ornek.tsv + v1-paket-N.md + kart-b-g4.jsonl
  python -X utf8 .claude/ogren6/v1.py birlestir    → v1-yazar-*.jsonl → .kos/kopru/ogren/ozet-g4-v1.jsonl + hakem-g4-v1.jsonl"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "ogren1"))
import d14, ozet3, ozet_kaynak
from d13 import A, O, sert
from ozet3 import BASLIK, adlari, kaynaksiz
from son import oku

ROL = ["birim test", "e2e/tarayıcı", "kalite ölçümü", "LLM değerlendirme", "statik analiz", "sır/bağımlılık taraması", "sızma/DAST",
       "uyumluluk", "derleme/teşhis", "backend/API", "veri/şema", "sorgu/analiz", "rehber", "G4-dışı"]
ozet3.MEKANIZMA = ROL  # gecerli_b modül globalini okur
B = Path(__file__).parent
K = B / "kaynak"
PAKET = 12
KAT = {"test-qa": "departman-test-qa", "güvenlik": "departman-guvenlik", "backend-dotnet": "departman-backend-dotnet", "veri-db": "departman-veri-db"}
ODAK = """writing-mstest-tests coverage-analysis crap-score test-gap-analysis assertion-quality test-smell-detection tdd superpowers-tdd
test-driven-development tdd-guard playwright-cli playwright puppeteer webapp-testing gstack-qa qa qa-only verification-loop eval-harness jev
grade-tests run-tests semgrep gitleaks strix zap opengrep-rule-generator 0day-scanner tm-security-review threat-modeling security-review
security-reviewer owasp-top-10-testing api-penetration-testing web-app-penetration-testing policy-monitor pia-generation use-case-triage
agentshield guvenlik-paket dotnet-data aspnetcore nuget msbuild csharp-lsp binlog mslearn dotnet-webapi optimizing-ef-core-queries
minimal-api-file-upload configuring-opentelemetry-dotnet convert-to-cpm wpf-rule-mvvm ecc-backend backend-patterns api-and-interface-design
dotnet-format supabase postgres-best-practices supabase-postgres-best-practices clickhouse drizzle-docs airtable convex pinecone pocketbase
sql-queries write-query mcp-memory memory dataviz""".split()
ONEK = ("build-perf-", "msbuild-", "data:", "mukul975-")  # Odak'taki joker aileler


def dosya(ad):
    return K / (re.sub(r"[^\w.-]", "_", ad) + ".txt")


def D():
    return dict(s.split("\t")[::3] for s in (B / "v1-ornek.tsv").read_text(encoding="utf-8").splitlines())


def katman(k):
    """→ (A listesi, B listesi); A ≤150 kullanım sırasıyla, taşan B'ye"""
    mudur = "\n".join((Path("skills") / d / "SKILL.md").read_text(encoding="utf-8") for d in KAT.values())
    anilan = lambda ad: len(ad) >= 4 and re.search(rf"(?<![\w-]){re.escape(ad)}(?![\w-])", mudur)
    a = [r for r in k.values() if r["kullanim_30g"] > 0 or r["ad"] in ODAK or r["ad"].startswith(ONEK[:2]) or anilan(r["ad"])]
    a.sort(key=lambda r: (-r["kullanim_30g"], r["ad"] not in ODAK, r["ad"]))
    sec = {r["ad"] for r in a[:150]}
    return [r for r in a[:150]], [r for r in k.values() if r["ad"] not in sec]


def hazirla():
    t = [json.loads(x) for x in (O / "katalog-son.jsonl").read_text(encoding="utf-8").splitlines()]
    k = {r["ad"]: r for r in reversed(t) if r["kategori_son"] in KAT and r["tur"] != "aday" and r["kanonik"] == r["id"]}  # aynı adlı kopya: ilk kalır
    ka, kb = katman(k)
    (O / "kart-b-g4.jsonl").write_text("".join(json.dumps({"ad": r["ad"], "katman": "B", "ne": r["aciklama"], "nasil": "", "tur": r["tur"], "yol": r["yol"],
                                                          "kategori": r["kategori_son"]}, ensure_ascii=False) + "\n" for r in kb), encoding="utf-8")
    K.mkdir(exist_ok=True)
    sec, bos = [], []
    for r in sorted(ka, key=lambda r: r["ad"]):
        try:
            m = d14.metin(r["ad"], r["yol"])
        except OSError:  # katalogdaki yol artık yok (ör. Desktop MCP ayar dosyası) → kaynaksız
            m = ""
        (bos if kaynaksiz(adlari(r["ad"], r["yol"]), m) else sec).append([r["ad"], r["tur"], str(r["bayt"]), r["yol"]])
        if sec and sec[-1][0] == r["ad"]:
            dosya(r["ad"]).write_text(m, encoding="utf-8")
    (B / "v1-ornek.tsv").write_text("".join("\t".join(s) + "\n" for s in sec), encoding="utf-8")
    (B / "v1-kaynaksiz.tsv").write_text("".join("\t".join(s) + "\n" for s in bos), encoding="utf-8")
    (B / "a-liste.tsv").write_text("".join(f"{r['ad']}\t{r['kategori_son']}\t{r['kullanim_30g']}\t{r['tur']}\n" for r in ka), encoding="utf-8")
    ozet_kaynak.D = D()
    n = -(-len(sec) // PAKET)
    for i in range(n):
        parca = []
        for ad, _, _, kaynak in sec[i::n]:  # şeritli dağıtım: büyük/küçük kaynaklar paketlere yayılır
            m, an = dosya(ad).read_text(encoding="utf-8"), sorted(adlari(ad, kaynak))
            parca += [f"## {ad}", f"kaynak: {dosya(ad)} (çözülmüş; özgün: {kaynak}) · {len(m.splitlines())} satır · araç adları ({len(an)}): {' · '.join(an[:30])}",
                      "BAŞLIKLAR: " + " · ".join(p.split("\n", 1)[0].strip()[:60] for p in BASLIK.split(m)[1:])[:1500], ""]
        (B / f"v1-paket-{i + 1}.md").write_text("\n".join(parca), encoding="utf-8")
    print(f"toplam {len(k)} · A {len(ka)} (kaynaklı {len(sec)} · kaynaksız {len(bos)}) · B {len(kb)} · paket {n}")


def birlestir():
    ozet_kaynak.D = D()
    c = {}
    for p in sorted(B.glob("v1-yazar-*.jsonl")):
        c.update(oku(p))
    son, ret = {}, {}
    for ad, kaynak in D().items():
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
    (O / "ozet-g4-v1.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in son.values()), encoding="utf-8")
    (O / "hakem-g4-v1.jsonl").write_text("".join(json.dumps({k: r[k] for k in ["ad", "kaynak", "ozgun"] + A + ["mekanizma"]}, ensure_ascii=False) + "\n"
                                                for r in son.values()), encoding="utf-8")
    print(f"son {len(son)} · RET {len(ret)} · UYARI {sum(len(r['uyari']) for r in son.values())} · G4-dışı {sum('G4-dışı' in r['mekanizma'] for r in son.values())}")


if __name__ == "__main__":
    {"hazirla": hazirla, "birlestir": birlestir}[sys.argv[1]]()
