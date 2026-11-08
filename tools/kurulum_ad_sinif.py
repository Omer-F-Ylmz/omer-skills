"""KURULUM-AD-1: ana-liste'deki linksiz (AD) kalemleri ücretsiz havuzla kurulum türüne ayırır.
Çıktı docs/video-tarama/kurulum-ad.tsv (kalem, sinif, ad, kaynak, gb, model). Yeniden koşulunca biten kalemler atlanır."""
import csv, json, re, sys, io, threading, os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ucretsiz_havuz as H  # noqa: E402

KOK = Path(__file__).resolve().parents[1] / "docs/video-tarama"
MOD = sys.argv[1] if len(sys.argv) > 1 else "AD"
CIK = KOK / ("kurulum-ad.tsv" if MOD == "AD" else "kurulum-url.tsv")
SINIF = {"GENEL", "UYGULAMA", "HIZMET", "PAKET", "CLI", "SKILL", "MODEL", "BELIRSIZ"}
ALAN = ["kalem", "sinif", "ad", "kaynak", "gb", "model"]
KIL = threading.Lock()

ISTEM = """Sen bir yazılım envanter uzmanısın. Aşağıdaki kalemler kısa videolarda (AI/Claude Code/tasarım/video/3D) geçen araç adlarıdır.
Her kalemi TEK sınıfa koy:
GENEL = işletim sistemi, programlama dili, dosya biçimi, genel kavram/özellik, donanım, platform/marka adı (ayrıca kurulacak bir şey değil: Windows, CSS, Markdown, Android, Excel özelliği)
UYGULAMA = Windows'a kurulabilen masaüstü uygulaması (Aseprite, Sublime Text, OBS)
HIZMET = web SaaS, barındırılan AI modeli/servisi, API hizmeti (yerelde kurulmaz; hesapla kullanılır: Runway Gen-2.5, ERNIE 4.5, VirusTotal, NextDNS)
PAKET = programlama kütüphanesi/paketi (pip/npm/cargo/nuget: HTTPX, huggingface_hub, Scanpy)
CLI = komut satırı aracı / geliştirici aracı / açık kaynak repo-uygulama (Bazel, Baserow, Eigent, RIFE)
SKILL = Claude/ajan skill'i, slash komutu, plugin, MCP sunucusu, prompt paketi (blender-lighting-lookdev, offensive-ssrf, design-system skill)
MODEL = yerelde indirilebilen açık ağırlıklı model (Qwen, FLUX, Wan 2.2)
BELIRSIZ = tanınmıyor/anlamsız
Her kalem için kurulum kaynağını bildiğin kadar yaz: winget:<Id> | pip:<ad> | npm:<ad> | cargo:<ad> | gh:<sahip/repo> | hf:<repo> | url:<site> | boş.
gb = yerel kurulum yaklaşık GB (1'den küçükse 0). Bilmiyorsan kaynak boş bırak, UYDURMA.
YALNIZ JSON dizi döndür: [{"i":0,"s":"SINIF","ad":"kanonik ad","k":"kaynak","gb":0}, ...] — her i tam bir kez.
Kalemler:
"""


def oku_bitmis():
    if not CIK.exists():
        return {}
    return {r["kalem"]: r for r in csv.DictReader(open(CIK, encoding="utf-8"), delimiter="\t")}


def parti_isle(parti):
    istem = ISTEM + "\n".join(f"{i}: {k}" for i, k in enumerate(parti))

    def dogru(m):
        try:
            j = json.loads(re.search(r"\[.*\]", m, re.S).group(0))
        except Exception:
            return False
        ii = {x.get("i") for x in j if isinstance(x, dict) and x.get("s") in SINIF}
        return ii == set(range(len(parti)))

    m = mdl = None
    for tur in ("orta", "kolay", "orta"):
        m, mdl, _ = H.cagir(tur, istem, max_tokens=4000, zaman=120, etiket="kurulum-ad", haiku_tavan=60)
        if m and dogru(m):
            break
    else:
        return []
    j = json.loads(re.search(r"\[.*\]", m, re.S).group(0))
    return [{"kalem": parti[x["i"]], "sinif": x["s"], "ad": str(x.get("ad", ""))[:80].replace("\t", " "),
             "kaynak": str(x.get("k", ""))[:120].replace("\t", " "), "gb": x.get("gb", 0), "model": mdl} for x in j]


def main():
    rows = list(csv.DictReader(open(KOK / "kurulum-sinif.tsv", encoding="utf-8"), delimiter="\t"))
    if MOD == "AD":
        adlar = {r["kalem"] for r in rows if r["sinif"] == "AD"}
    else:
        adlar = {f'{r["kalem"]} <{r["repo_link"][:90]}>' for r in rows if r["sinif"] in ("URL-URUN", "KISA-LINK")}
    bitmis = oku_bitmis()
    kalan = sorted(adlar - set(bitmis))
    print("toplam", len(rows), "kalan", len(kalan), flush=True)
    yeni = not CIK.exists()
    f = open(CIK, "a", encoding="utf-8", newline="")
    w = csv.DictWriter(f, fieldnames=ALAN, delimiter="\t")
    if yeni:
        w.writeheader()
    partiler = [kalan[i:i + 40] for i in range(0, len(kalan), 40)]
    tamam = 0
    with ThreadPoolExecutor(4) as ex:
        for sonuc in ex.map(parti_isle, partiler):
            with KIL:
                w.writerows(sonuc); f.flush()
                tamam += len(sonuc)
                (KOK / (CIK.stem + ".ilerleme")).write_text(f"{tamam}/{len(kalan)}")
    f.close()
    print("BITTI", tamam, "/", len(kalan), flush=True)


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
