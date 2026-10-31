"""BOSTA-ARAC-1 TUR 2: boşta kalemler için 'hangi işte kullanılmalıydı' satırları (ücretsiz havuz, 50'lik parti).
Çıktı: bosta-arac-1-satirlar.tsv (kategori, ad, öneri). Yeniden başlatılabilir: zaten yazılmış ad atlanır."""
import csv, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "tools"))
import ucretsiz_havuz as u

RAPOR = os.path.dirname(os.path.abspath(__file__))
GIRIS = os.path.join(RAPOR, "bosta-arac-1-liste.tsv")
CIKIS = os.path.join(RAPOR, "bosta-arac-1-satirlar.tsv")
PARTI = 50

with open(GIRIS, encoding="utf-8") as f:
    kalemler = [(r["kategori"], r["ad"]) for r in csv.DictReader(f, delimiter="\t")]

yazilan = set()
if os.path.exists(CIKIS):
    with open(CIKIS, encoding="utf-8") as f:
        yazilan = {(r[0], r[1]) for r in csv.reader(f, delimiter="\t") if len(r) >= 3}

bekleyen = [k for k in kalemler if k not in yazilan]
print(f"toplam {len(kalemler)} · yazılı {len(yazilan)} · bekleyen {len(bekleyen)}")

def istem_olustur(parti):
    satirlar = "\n".join(f"{i}. {kat}: {ad}" for i, (kat, ad) in enumerate(parti, 1))
    return (
        "Aşağıdaki Claude Code araçları (skill, agent, plugin, mcp) son 14 günde hiç kullanılmadı. "
        "Her biri için, bu aracın gerçekten işe yarayacağı TEK bir iş türü yaz (Türkçe, en fazla 12 kelime). "
        "Her satır şu biçimde olsun: numara|iş türü. Başka hiçbir şey yazma. Tam olarak "
        f"{len(parti)} satır üret.\n\n{satirlar}"
    )

def dogrula(metin):
    satir = [s for s in metin.strip().splitlines() if re.match(r"^\s*\d+\s*\|", s)]
    return None if len(satir) >= len(PARTI_BU) else f"eksik {len(satir)}/{len(PARTI_BU)}"

with open(CIKIS, "a", encoding="utf-8", newline="") as out:
    w = csv.writer(out, delimiter="\t")
    for b in range(0, len(bekleyen), PARTI):
        parti = bekleyen[b:b + PARTI]
        PARTI_BU = parti
        metin, saglayici, log = u.cagir("kolay", istem_olustur(parti), max_tokens=3000, etiket="bosta-arac-1", zaman=120, dogrula=dogrula)
        if metin is None:
            print(f"parti {b // PARTI + 1}: hiçbir halka yanıtlamadı {log}; kalan {len(bekleyen) - b} kalem yazılmadı")
            break
        cevap = {}
        for s in metin.strip().splitlines():
            m = re.match(r"^\s*(\d+)\s*\|\s*(.+)$", s)
            if m:
                cevap[int(m.group(1))] = m.group(2).strip().replace("\t", " ")
        for i, (kat, ad) in enumerate(parti, 1):
            w.writerow([kat, ad, cevap.get(i, "(üretilemedi)")])
        out.flush()
        print(f"parti {b // PARTI + 1}: {len(parti)} kalem · {saglayici} · {len(cevap)} satır")
