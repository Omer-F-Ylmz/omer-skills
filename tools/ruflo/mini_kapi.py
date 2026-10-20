"""RUFLO-2 d4 mini kapı: derssiz / bizim / Ruflo / KOMBO, 2 aile (kod5, rapor5 held-out) × 4 kol. Aynı blok → tek koşu.
Tohum: kod0+rapor0 derssiz koşu → haiku damıtma (≤4 çağrı) + temizlenmiş gerçek aktif banka (gürültü). Tavan: 11 claude -p.
  python mini_kapi.py [--kuru]   → --kuru: yalnız ücretsiz kapsam/getirme ölçümü (gerçek banka, çağrı yok)"""
import json
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(KOK / "tools" / "olcum"), str(KOK / "tools" / "ogrenme"), str(KOK / "tools" / "ruflo")]
import os  # noqa: E402

TS = time.strftime("%Y%m%d-%H%M%S")
BANKA = KOK / ".kos" / "ruflo" / "kapi" / TS
os.environ["OGRENME_DIZIN"] = str(BANKA)
BANKA.mkdir(parents=True)
import ab_olc  # noqa: E402
import ders  # noqa: E402
import kosucu  # noqa: E402
import mcp_dene  # noqa: E402

GERCEK = KOK / ".kos" / "ogrenme" / "dersler.jsonl"
TSV = KOK / "docs" / "kutuphane" / "olcum" / "ruflo-2-kapi.tsv"
TAVAN, ESIK = 11, 0.5  # claude -p tavanı; Ruflo benzerlik eşiği (bizim getir de en iyinin yarısı eşiğini kullanır)
NS = f"kapi-{TS}"
HELDOUT = [("kod", 5), ("rapor", 5)]
cagri = 0


def gorev_metni(aile, i):
    with tempfile.TemporaryDirectory() as d:
        return ab_olc.kur(aile, i, d)


def blok(secilen):
    """ders.getir ile aynı biçim/jeton payı."""
    s = ["Dersler (uymuyorsa yok say). Dersteki proje kuralını doğrudan uygula, kural belgesi arama; girdiyi ilk turda oku, tek yazımla bitir:"]
    pay = (ders.JETON * 4 - len(s[0])) // len(secilen) - 1
    for x in secilen:
        s.append(f"- [{x['id']}·{'kaçın' if x['tur'] == 'basarisizlik' else '✓'}] {x['baslik']} — {x['kosul']}: "
                 f"{re.split(r'(?<=[.!?])\s', x['icerik'])[0]}"[:pay])
    return "\n".join(s)


def ruflo(sorgular):
    """tek MCP oturumu: tüm aktif dersleri yaz + her sorgu için ara → (sorgu başına [(id, benzerlik)], süre sn)"""
    akt = [x for x in ders.oku() if x["durum"] == "aktif"]
    c = [("tools/call", {"name": "memory_store", "arguments": {"key": x["id"], "namespace": NS, "value": f"{x['baslik']} — {x['kosul']}"}}) for x in akt]
    c += [("tools/call", {"name": "memory_search", "arguments": {"query": q[:300], "namespace": NS, "limit": 3}}) for q in sorgular]
    t = time.perf_counter()
    o, _ = mcp_dene.kos(c)
    sure = time.perf_counter() - t
    sonuc = []
    for k in range(len(akt) + 2, len(akt) + 2 + len(sorgular)):
        try:
            r = json.loads(o[k]["result"]["content"][0]["text"])["results"]
            sonuc.append([(h["key"], round(h["similarity"], 2)) for h in r])
        except (KeyError, ValueError, TypeError):
            sonuc.append(None)
    return sonuc, sure


def kapsam(gercek):
    """ücretsiz: 25 görev metni için bizim vs Ruflo blok doluluğu + gecikme"""
    gorevler = [(a, i, gorev_metni(a, i)) for a, n in (("kod", 10), ("rapor", 10), ("video", 5)) for i in range(n)]
    t = time.perf_counter()
    bizim = [ders.getir(ab_olc.AJAN[a], g)[1] for a, _, g in gorevler]
    bsure = (time.perf_counter() - t) / len(gorevler) * 1000
    rf, rsure = ruflo([g for _, _, g in gorevler])
    rd = [[k for k, s in (h or []) if s >= ESIK][:2] for h in rf]
    print(f"KAPSAM ({'gerçek banka' if gercek else 'tohumlu'}, n={len(gorevler)}): bizim dolu {sum(map(bool, bizim))} · Ruflo dolu {sum(map(bool, rd))} "
          f"· getirme bizim {bsure:.0f} ms/sorgu · Ruflo {rsure / len(gorevler):.1f} s/sorgu (tek oturum {rsure:.0f} s, {len(ders.oku())} ders yazımı dahil)")
    return bizim, rd


def kos(istem, aile, i, d, model="sonnet", butce=0.6):
    global cagri
    cagri += 1
    return kosucu.kos(istem, ek=ab_olc.EK, cwd=d, model=model, butce=butce)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    shutil.copy(GERCEK, BANKA / "dersler.jsonl")
    ders._yaz([x for x in ders.oku() if x["durum"] == "aktif"])
    print(f"gürültü bankası: {len(ders.oku())} aktif gerçek ders ({BANKA})")
    if "--kuru" in sys.argv:
        kapsam(True)
        sys.exit()
    # 1) tohum: derssiz koşu → haiku damıtma
    for aile in ("kod", "rapor"):
        d = tempfile.mkdtemp(prefix=f"kapi-tohum-{aile}-")
        g = ab_olc.kur(aile, 0, d)
        o = kos(g, aile, 0, d)
        puan, gizli, notlar = ab_olc.yargic(aile, 0, d)
        dm = kosucu.kos(ab_olc.DAMIT % (g, puan, o["tur"], "; ".join(notlar) or "hepsi geçti", o["metin"][-1500:],
                                        (Path(d) / "KURALLAR.md").read_text(encoding="utf-8")),
                        ek=["--strict-mcp-config", "--max-turns", "1"], model="haiku", butce=0.2)
        cagri += 1
        try:
            m = dm["metin"]
            for x in json.loads(m[m.index("["):m.rindex("]") + 1])[:3]:
                ders.ekle(ab_olc.AJAN[aile], x["baslik"], x["kosul"], x["icerik"], "basari" if puan >= 1.0 else "basarisizlik",
                          f"kapi-tohum-{aile}0", f"puan {puan}", g)
        except (ValueError, KeyError, TypeError) as e:
            print("damıtma ayrışmadı", aile, e)
        print(f"tohum {aile}0: puan {puan} tur {o['tur']} · bankada {len(ders.oku())} ders · Σ{cagri}", flush=True)
    kapsam(False)
    # 2) held-out: blok kolları
    gorevler = {a: gorev_metni(a, i) for a, i in HELDOUT}
    rf, _ = ruflo([gorevler[a] for a, _ in HELDOUT])
    bank = {x["id"]: x for x in ders.oku()}
    TSV.write_text("zaman\taile\tkol\tblok_ids\tpuan\ttur\tjeton_in_cc_out\tusd\tsure_sn\tnot\n", encoding="utf-8", newline="\n") if not TSV.exists() else None
    for (aile, i), hits in zip(HELDOUT, rf):
        ajan = ab_olc.AJAN[aile]
        _, b_ids = ders.getir(ajan, gorevler[aile])
        r_ids = [k for k, s in (hits or []) if s >= ESIK and k in bank][:2]
        k_ids = (b_ids[:1] + [k for k in r_ids if bank[k]["ajan"] in (ajan, "*") and k not in b_ids])[:2]
        kollar = {"derssiz": [], "bizim": b_ids, "ruflo": r_ids, "kombo": k_ids}
        print(aile, "hits", hits, "kollar", kollar, flush=True)
        yapilan = {}
        for kol, ids in kollar.items():
            anahtar = tuple(ids)
            if anahtar in yapilan:
                satir = yapilan[anahtar]
                not_ = f"= {satir[0]} (aynı blok, koşu paylaşıldı)"
            else:
                if cagri >= TAVAN or kosucu.bos_ram_gb() < 1.6:
                    print("TAVAN/RAM — durdu", kol, cagri, flush=True)
                    continue
                d = tempfile.mkdtemp(prefix=f"kapi-{aile}-{kol}-")
                g = ab_olc.kur(aile, i, d)
                o = kos((blok([bank[k] for k in ids]) + "\n\n" + g) if ids else g, aile, i, d)
                puan, gizli, notlar = ab_olc.yargic(aile, i, d)
                satir = (kol, puan, o["tur"], kosucu.jeton(o["usage"]), round(o["usd"], 3), o["sure"])
                yapilan[anahtar] = satir
                not_ = " | ".join(notlar)[:120]
            with open(TSV, "a", encoding="utf-8", newline="\n") as f:
                f.write("\t".join(map(str, [time.strftime("%H:%M:%S"), aile, kol, ",".join(ids), *satir[1:], not_])) + "\n")
            print(aile, kol, satir[1:], f"Σ{cagri}", flush=True)
    print(f"BİTTİ Σ{cagri} claude -p · {TSV}")
