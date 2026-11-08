"""KATEGORI-KAPSAM adim 4: docs/envanter/kategori.tsv -> docs/envanter/kategori-ozet.md (yeniden uretir).
Her kategori: (a) bir cumle ne ise yarar, (b) toplam + tur grubuna dagilim, (c) en onemli 15 oge, (d) cok-yonlu listesi ayri baslik.
NOT: kategori_sinifla.py da kategori-ozet.md yazar; ondan SONRA bu betik calistirilmali (python tools/kapsam_sinifla.py && python tools/kategori_ozet_kapsam.py)."""
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import kategori_sinifla as S  # noqa: E402

csv.field_size_limit(10**9)
KAT = KOK / "docs/envanter/kategori.tsv"
OZET = KOK / "docs/envanter/kategori-ozet.md"
CUMLE = {
    "arastirma": "Web/akademik araştırma, kaynak tarama, doğrulama ve bilgi toplama araçları.",
    "backend-dotnet": "Sunucu tarafi .NET/C# kodu: ASP.NET Core, EF Core, MSBuild, NuGet ve .NET API gelistirme.",
    "backend-genel": "Sunucu tarafi kod (.NET disi): Java, Go, Rust, Python, Node backend kaliplari, API tasarimi ve mimari desenler.",
    "belge": "Doküman üretimi/okuma: docx, pdf, pptx, xlsx, yazım ve metin düzeltme.",
    "bilim": "Bilimsel hesap, biyoloji/kimya/fizik paketleri ve laboratuvar iş akışları.",
    "bulut-devops": "Bulut, CI/CD, konteyner, altyapı ve dağıtım işleri.",
    "frontend-ui": "Arayüz, tasarım sistemi, animasyon ve web ön yüz geliştirme.",
    "git-yayin": "Git, PR, sürüm/yayın ve depo yönetimi.",
    "gorsel": "Görsel üretim/düzenleme: görüntü modelleri, logo, illüstrasyon, tasarım araçları.",
    "guvenlik": "Güvenlik testi, zafiyet tarama, savunma ve gizli anahtar denetimi.",
    "inceleme": "Kod/PR/tasarım inceleme ve denetim.",
    "is-finans-hukuk": "İş, finans, hukuk, satış ve operasyon süreçleri.",
    "ml-ai": "Model eğitimi/çıkarımı, LLM, ajan modelleri ve yapay zekâ kütüphaneleri.",
    "mobil": "Mobil uygulama geliştirme: Android, iOS, Expo, Flutter.",
    "oyun": "Oyun geliştirme, motorlar, mod yapımı ve oyun varlıkları.",
    "pazarlama-reklam": "Pazarlama, SEO, reklam, sosyal medya ve içerik stratejisi.",
    "surec-plan": "Planlama, karar, kural ve iş akışı süreçleri.",
    "test-qa": "Test, kalite güvencesi ve doğrulama araçları.",
    "veri-db": "Veritabanı, veri analizi ve veri hattı araçları.",
    "verimlilik": "Token/bağlam tasarrufu, hafıza ve oturum verimliliği araçları.",
    "video": "Video üretim/kurgu/altyazı/ses ve medya işleme.",
    "3d-blender": "3B modelleme, Blender, sahne ve render araçları.",
    "ajan-arac": "Ajan, MCP, CLI, eklenti ve genel geliştirici araç altyapısı.",
    "diger-genel": "Hiçbir özel kategoriye girmeyen genel öğeler.",
}
GRUP = {"skill": "skill", "plugin-skill": "skill", "plugin": "plugin", "mcp": "MCP", "baglayici": "MCP/bağlayıcı", "cli": "CLI",
        "klon": "repo", "kalem": "paket", "betik": "paket", "uygulama": "uygulama", "model": "model", "site": "site", "hesap": "hesap"}
ONEM = {"skill": 6, "plugin": 7, "mcp": 8, "cli": 7, "uygulama": 7, "model": 6, "klon": 5, "hesap": 6, "baglayici": 5, "plugin-skill": 4,
        "eklenti": 5, "arac": 5, "site": 4, "kart": 2}
GUVEN = {"yuksek": 3, "orta": 2, "dusuk": 0}


def main():
    with open(KAT, encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f, delimiter="\t") if r.get("ad")]
    kat = defaultdict(list)
    cy = defaultdict(list)
    for r in rows:
        kat[r["birincil"]].append(r)
        if r["cok_yonlu"]:
            cy[r["cok_yonlu"]].append(r)
    def puan(r):
        return ONEM.get(r["tur"], 1) + GUVEN.get(r["guven"], 0) + (2 if r["cok_yonlu"] else 0) + (1 if 3 < len(r["ad"]) < 40 else 0)
    cikti = ["# Kategori özeti (KATEGORI-1 + KATEGORI-KAPSAM)", "",
             f"Tekil kalem: {len(rows)} · kategori: {len(kat)} · çok-yönlü etiketli: {sum(len(v) for v in cy.values())}.",
             "Kategoriler: " + ", ".join(f"{k} ({len(kat.get(k, []))})" for k in S.KATEGORILER), ""]
    for k in S.KATEGORILER:
        L = kat.get(k, [])
        dag = Counter(GRUP.get(r["tur"], r["tur"]) for r in L)
        gor, top = set(), []
        for r in sorted(L, key=lambda r: (-puan(r), r["ad"])):
            n = S._norm(r["ad"])
            if n not in gor and not r["ad"].startswith("kapsam:"):
                gor.add(n)
                top.append(r)
            if len(top) == 15:
                break
        cikti += [f"## {k} — {len(L)}", "", f"**Ne işe yarar:** {CUMLE[k]}", "",
                  "**Dağılım:** " + ", ".join(f"{a}={b}" for a, b in dag.most_common()), "", "**En önemli 15:**"]
        cikti += [f"{i}. {re.sub(r'[|`]', ' ', r['ad'])[:70]} ({r['tur']})" for i, r in enumerate(top, 1)]
        cikti.append("")
    cikti += ["## çok-yönlü (NİHAİ 0 çok amaçlı araçlar)", ""]
    cy_say = Counter()
    for r in rows:
        for e in filter(None, r["cok_yonlu"].split(",")):
            cy_say[e] += 1
    cikti.append("Etiket sayıları: " + ", ".join(f"{a}={b}" for a, b in cy_say.most_common()))
    cikti.append("")
    for e, n in cy_say.most_common():
        ornek = [r["ad"] for r in rows if e in r["cok_yonlu"].split(",") and not r["ad"].startswith("kapsam:")][:8]
        cikti.append(f"- **{e}** ({n}): " + "; ".join(re.sub(r"[|`]", " ", a)[:50] for a in ornek))
    OZET.write_text("\n".join(cikti) + "\n", encoding="utf-8", newline="\n")
    print("yazildi", len(rows), "kalem", len(cikti), "satir")


if __name__ == "__main__":
    main()
