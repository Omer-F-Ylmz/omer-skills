"""MCP-HAFIF-1 KABUL: 12 temsilci kalite3 ajanı (6 MCP anan + 6 anmayan) × 2 tekrar, model_olc ajan kolu; kol başına ayrı süreç
(OLCUM_MCP_HAFIF süreç geneli): eski = tam user MCP, yeni = mcp_sec. Koşu sürerken claude'un torunları CIM ile örneklenir
(en çok süreç / toplam RAM). Kol başına en fazla 24 claude -p (+ boş yanıtta 1 yeniden deneme); jev: en fazla 2 Jev batch.
  python tools/olcum/mcp_hafif_kabul.py kol eski|yeni      # iki kol ayrı arka süreçte, aynı anda
  python tools/olcum/mcp_hafif_kabul.py agac eski|yeni     # ÖLÇ: tek "OK" çağrısı (haiku)
  python tools/olcum/mcp_hafif_kabul.py jev                # Jev puanı + özet"""
import csv
import json
import os
import re
import subprocess
import sys
import threading
import time
from collections import Counter
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
KOK = DIZIN.parents[1]
sys.path.insert(0, str(DIZIN.parent))
import model_olc  # noqa: E402
from olcum import kosucu  # noqa: E402

AJANLAR = ["bl-isik-kurulumu", "bl-glb-disa-aktar", "ajn-mcp-kurulum-denetci", "qa-e2e-playwright", "otm-tarayici-otomasyon",
           "ara-kutuphane-dokuman", "db-migration-planlayici", "fe-css-hata-bulucu", "oyn-mod-onarim", "sec-docker-guvenlik",
           "vrm-log-ozetleyici", "ajn-migrasyon-model"]
OLCUM = KOK / "docs/kutuphane/olcum"
YANIT = KOK / ".kalite3/mcphafif-yanit"
BASLIK = ["ajan", "kol", "tekrar", "puan", "usd", "sure", "surec", "ram_mb", "adlar"]


def anlik():
    """Win32_Process (salt okur) → {pid: (ppid, ad, ram_bayt)}."""
    ps = "Get-CimInstance Win32_Process | ForEach-Object { \"$($_.ProcessId)`t$($_.ParentProcessId)`t$($_.Name)`t$($_.WorkingSetSize)\" }"
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], capture_output=True, text=True,
                       creationflags=kosucu.PENCERESIZ, timeout=60)
    d = {}
    for s in r.stdout.splitlines():
        p = s.split("\t")
        if len(p) == 4 and p[0].isdigit():
            d[int(p[0])] = (int(p[1]), p[2], int(p[3] or 0))
    return d


def torunlar(d, kok):
    cocuk = {}
    for pid, (pp, _, _) in d.items():
        cocuk.setdefault(pp, []).append(pid)
    out, yigin = [], list(cocuk.get(kok, []))
    while yigin:
        p = yigin.pop()
        out.append(p)
        yigin += cocuk.get(p, [])
    return out


class Ornekle(threading.Thread):
    """Bu sürecin claude çocuklarının torunları: en çok süreç sayısı, en çok toplam RAM, o andaki ad sayımı."""
    def __init__(self):
        super().__init__(daemon=True)
        self.dur, self.n, self.ram, self.adlar = threading.Event(), 0, 0, Counter()

    def run(self):
        while not self.dur.wait(4):
            d = anlik()
            ben = [p for p, (pp, ad, _) in d.items() if pp == os.getpid() and ad.lower().startswith("claude")]
            t = [p for c in ben for p in torunlar(d, c)]
            ram = sum(d[p][2] for p in t)
            if len(t) > self.n:
                self.n, self.adlar = len(t), Counter(d[p][1] for p in t)
            self.ram = max(self.ram, ram)

    def sonuc(self):
        self.dur.set()
        self.join()
        return self.n, round(self.ram / 2**20), ",".join(f"{a}:{n}" for a, n in self.adlar.most_common(8))


def bayrak(kol):
    if kol == "yeni":
        os.environ["OLCUM_MCP_HAFIF"] = "1"
    else:
        os.environ.pop("OLCUM_MCP_HAFIF", None)


def yaz(tsv, satir):
    yeni = not tsv.exists()
    with tsv.open("a", encoding="utf-8", newline="\n") as f:
        f.write(("\t".join(BASLIK) + "\n" if yeni else "") + "\t".join(map(str, satir)) + "\n")


def kol_kos(kol):
    bayrak(kol)
    gorevler = {g["ajan"]: g for g in json.loads((model_olc.AJAN / "gorevler.json").read_text(encoding="utf-8"))}
    tsv = OLCUM / f"mcp-hafif-1-{kol}.tsv"
    bitti = {(s["ajan"], s["tekrar"]) for s in csv.DictReader(tsv.open(encoding="utf-8"), delimiter="\t")} if tsv.exists() else set()
    YANIT.mkdir(parents=True, exist_ok=True)
    for tekrar in ("1", "2"):
        for ad in AJANLAR:
            if (ad, tekrar) in bitti:
                continue
            while kosucu.bos_ram_gb() < kosucu.RAM_ALT_GB:
                time.sleep(30)
            g = gorevler[ad]
            yol = next(model_olc.AJAN.glob(f"*/{ad}.md"))
            _, t = model_olc.tanim(yol, g["model"])
            o_ = Ornekle()
            o_.start()
            o = model_olc.kos(ad, t, g["model"], g["istem"])
            n, ram, adlar = o_.sonuc()
            (YANIT / f"{ad}-{kol}-{tekrar}.md").write_text(o["metin"], encoding="utf-8", newline="\n")
            yaz(tsv, [ad, kol, tekrar, model_olc.puan(o, g["rubrik"]), round(o["usd"], 4), o["sure"], n, ram, adlar])
            print(ad, kol, tekrar, o["sure"], n, ram, flush=True)


def agac(kol):
    bayrak(kol)
    o_ = Ornekle()
    o_.start()
    o = kosucu.kos("Reply with exactly: OK", model="haiku", butce=0.2, timeout=300)
    n, ram, adlar = o_.sonuc()
    print("\t".join(map(str, [kol, o["sure"], o["rc"], n, ram, adlar])), flush=True)


def jev():
    sys.path.insert(0, str(KOK / ".kalite3"))
    import ajan_jev
    from jev.cekirdek import Tasiyici
    gorevler = {g["ajan"]: g for g in json.loads((model_olc.AJAN / "gorevler.json").read_text(encoding="utf-8"))}
    satir = [s for k in ("eski", "yeni") for s in csv.DictReader((OLCUM / f"mcp-hafif-1-{k}.tsv").open(encoding="utf-8"), delimiter="\t")]
    state = []
    for s in satir:
        g = gorevler[s["ajan"]]
        kabul = "Yanıt şunları kapsamalı: " + "; ".join(
            f"{re.sub(r'^[(][?]i[)]', '', r['regex'])} ({r['puan']} puan)" for r in g["rubrik"])
        yanit = (YANIT / f"{s['ajan']}-{s['kol']}-{s['tekrar']}.md").read_text(encoding="utf-8", errors="replace")
        state.append({"gorev": g["istem"], "kabul": kabul, "yanit": yanit})
    for s, c in zip(satir, Tasiyici(env=ajan_jev.ortam(), en_fazla=2, istek_tavan=len(state) + 10).yargila(state, ajan_jev.SORU)):
        s["jev"] = round(c["kalite"]["score"] * 2, 1) if c else ""
    cikti = OLCUM / "mcp-hafif-1.tsv"
    with cikti.open("w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=BASLIK + ["jev"], delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(satir)
    ozet(satir)


def ort(x):
    x = [float(v) for v in x if v not in ("", "hata")]
    return round(sum(x) / len(x), 2) if x else None


def ozet(satir):
    """Gürültü = aynı kol·ajanın iki tekrarı arasındaki ortalama mutlak fark; kalite eşit ⇔ |Δ kol ortalaması| ≤ gürültü."""
    for m in ("puan", "jev", "sure", "surec", "ram_mb", "usd"):
        k = {kol: ort(s[m] for s in satir if s["kol"] == kol) for kol in ("eski", "yeni")}
        ikili = [(s["ajan"], s["kol"]) for s in satir if s["tekrar"] == "1"]
        fark = [abs(float(a[m]) - float(b[m])) for aj, kol in ikili
                for a in satir if (a["ajan"], a["kol"], a["tekrar"]) == (aj, kol, "1")
                for b in satir if (b["ajan"], b["kol"], b["tekrar"]) == (aj, kol, "2")
                if a[m] not in ("", "hata") and b[m] not in ("", "hata")]
        gurultu = ort(fark)
        esit = None if None in k.values() or gurultu is None else abs(k["yeni"] - k["eski"]) <= gurultu
        print(f"{m}\teski {k['eski']}\tyeni {k['yeni']}\tgürültü {gurultu}\t{'eşit' if esit else 'FARK' if esit is False else '-'}")
    # karar uyuşması (d3, sonuçtan önce yazıldı): ajan·kol ortalama rubrik puanı ≥5 = geçti; eski↔yeni aynı karar ≥10/12 → eşit
    gecti = {(s["ajan"], s["kol"]): ort(a["puan"] for a in satir if (a["ajan"], a["kol"]) == (s["ajan"], s["kol"])) for s in satir}
    ajanlar = {a for a, _ in gecti}
    uy = sum(((gecti.get((a, "eski")) or 0) >= 5) == ((gecti.get((a, "yeni")) or 0) >= 5) for a in ajanlar)
    print(f"karar uyuşması {uy}/{len(ajanlar)}\t{'eşit' if uy >= len(ajanlar) - 2 else 'FARK'}")
    hata = Counter(s["kol"] for s in satir if s["puan"] == "hata")
    print("hata", dict(hata), "satır", Counter(s["kol"] for s in satir))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"kol": kol_kos, "agac": agac, "jev": lambda: jev(), "ozet": lambda: ozet(
        list(csv.DictReader((OLCUM / "mcp-hafif-1.tsv").open(encoding="utf-8"), delimiter="\t")))}[sys.argv[1]](*sys.argv[2:])
