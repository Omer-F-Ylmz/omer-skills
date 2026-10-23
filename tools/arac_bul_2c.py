"""ARAC-BUL-2 adım 1c: 221 'bulunamadı' adının hepsini arac-bul-2.tsv'de tek satıra oturt (yedekteki 192 + 2. geçiş güncellemesi + elle doğrulanmış 29 eksik/8 kalan).
Elle girişler `gh repo view` ile doğrulandı (23 Eki). Kullanım: python tools/arac_bul_2c.py"""
import collections, csv, os

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".kos", "kopru", "rapor")
BASLIK = ["ad", "sinif", "aday", "link", "durum", "boyut", "tarama", "kanit", "video"]
GH = "https://github.com/"
# ad → (sinif, aday, kanit); sinif bulundu için aday = owner/repo
EL = {
    "apity-mcp-server": ("bulundu", "apify/apify-mcp-server", "OCR 'apity'→apify; gh view ok"),
    "@apify/actors-mcp-server": ("bulundu", "apify/apify-mcp-server", "npm @apify/actors-mcp-server = apify-mcp-server"),
    "htipsms-go": ("bulundu", "evolution-foundation/evolution-go", "OCR; evolution-go ailesi (OCR varyantı)"),
    "evolut1en": ("bulundu", "evolution-foundation/evolution-go", "OCR 'evolut1en'→evolution; gh view ok"),
    "evolton-go": ("bulundu", "evolution-foundation/evolution-go", "OCR 'evolton-go'→evolution-go; gh view ok"),
    "@nvidia/openshell-sdk": ("bulundu", "NVIDIA/OpenShell", "npm @nvidia/openshell-sdk; gh view NVIDIA/OpenShell ok"),
    "openshipreadme": ("ocr", "", "'openship'+README artığı"),
    "pentest-agentsfreadme": ("ocr", "", "'pentest-agents'+README artığı"),
    "plexottreadme": ("ocr", "", "'plexott'+README artığı"),
    "hyerfre": ("bulundu", "heygen-com/hyperframes", "OCR hyperframes"),
    "hyerfrmes": ("bulundu", "heygen-com/hyperframes", "OCR hyperframes"),
    "bperframes": ("bulundu", "heygen-com/hyperframes", "OCR hyperframes"),
    "hypetframes-all": ("bulundu", "heygen-com/hyperframes", "OCR hyperframes"),
    "hyperfrans": ("bulundu", "heygen-com/hyperframes", "OCR hyperframes"),
    "releses": ("ocr", "", "'releases' OCR artığı"),
    "relases": ("ocr", "", "'releases' OCR artığı"),
    "rekases": ("ocr", "", "'releases' OCR artığı"),
    "releass": ("ocr", "", "'releases' OCR artığı"),
    "lightpanda-io/beowser/lightpanda": ("bulundu", "lightpanda-io/browser", "OCR 'beowser'→browser; gh view ok"),
    "lighapanda-io/beowsicr/lighrpanda": ("bulundu", "lightpanda-io/browser", "OCR; gh view ok"),
    "browserlightpnda": ("bulundu", "lightpanda-io/browser", "OCR; gh view ok"),
    "lowsint": ("bulundu", "reconurge/flowsint", "OCR 'lowsint'→flowsint; gh view ok"),
    "skillsaddhttps://github.com/latent-spaces/brag": ("bulundu", "latent-spaces/brag", "komut 'skills add' + repo; gh view ok"),
    "context7@claude-plugins-official": ("komut", "", "claude plugin install context7@claude-plugins-official (marketplace eklentisi)"),
    "github@claude-plugins-official": ("komut", "", "claude plugin install github@claude-plugins-official"),
    "figma@claude-plugins-official": ("komut", "", "claude plugin install figma@claude-plugins-official"),
    "vercel@claude-plugins-official": ("komut", "", "claude plugin install vercel@claude-plugins-official"),
    "car-rental-system": ("uygulama", "", "öğretici videodaki örnek proje (repo yok)"),
    "POS-System": ("uygulama", "", "öğretici videodaki örnek proje (repo yok)"),
    "reddit-clone-mern-stack": ("uygulama", "", "öğretici videodaki örnek proje (repo yok)"),
    "note-taking-app": ("uygulama", "", "FaisalST32/note-taking-app gh'de yok (silinmiş); öğretici örnek"),
    "enguin-harmess": ("bulundu", "Prism-Shadow/penguin-harness", "OCR hamess→harness; gh view ok"),
    "penguin-hamess": ("bulundu", "Prism-Shadow/penguin-harness", "OCR hamess→harness; gh view ok"),
    "TrauingAgents.AnalystIeam": ("bulundu", "TauricResearch/TradingAgents", "OCR; gh view ok"),
    "skillsaddmorlutorea-skill": ("bulundu", "morluto/rea", "'npx skills add morluto/rea-skill'; rea-skill repo yok, morluto/rea var"),
}


def oku(ad):
    with open(os.path.join(R, ad), encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main():
    girdi = [r for r in oku("arac-indir-2.tsv") if r["durum"] == "bulunamadi"]
    yedek = {r["ad"]: r for r in oku("arac-bul-2.yedek.tsv")}
    simdi = {r["ad"]: r for r in oku("arac-bul-2.tsv")}
    cikti = []
    for g in girdi:
        ad = g["ad"]
        r = dict(simdi.get(ad) or yedek.get(ad) or {k: "-" for k in BASLIK})
        r.update(ad=ad, video=g["video"])
        if ad in EL:
            s, a, k = EL[ad]
            r.update(sinif=s, aday=a, kanit=k)
            if s == "bulundu":
                r.update(link=GH + a, durum="indirilmedi", boyut="-")
        cikti.append(r)
    with open(os.path.join(R, "arac-bul-2.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, BASLIK, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(cikti)
    print(len(cikti), collections.Counter(r["sinif"] for r in cikti), "tekil repo", len({r["aday"].lower() for r in cikti if r["sinif"] == "bulundu"}))


if __name__ == "__main__":
    main()
