"""VİDEO-KISA-TOKEN-1 ölçüm: m0 (taban, .kos/v16 kayıtlarından, claude -p yok) · kos (yeni hat, 1 claude -p) · puan (altın kümede kapı).
python .kos/kopru/video/kisa_m4.py m0|kos|puan    (tools/video/.venv python'u; PYTHONPATH=tools/video)
"""
import json
import re
import sys
from pathlib import Path

from video import kisa
from video import tarama as tr

ANA = Path(r"C:\Projeler\omer-skills")
ONB = Path(r"C:\Projeler\.video-cache")
V16 = ANA / ".kos" / "v16"
CIK = ANA / ".kos" / "kopru" / "video" / "kisa"
ALTIN = ("ig-DeW7JHrgsXb", "ig-DeV9nZPtSsC", "ig-DeHMM45NaFt")  # VİDEO-16 short altın kümesi (aynı videolar)
EK = ("ig-DeZdb5pNQSB", "ig-DeZdAxovI1G", "ig-DdupQchgt8X", "ig-DcGy07ZMh5D", "ig-DeRC-BJoA5H")  # oturumu 8'e tamamlar; sonuncusu carousel
REF, TABAN = ("taban-1", "taban-2"), ("low-ssb-1", "low-ssb-2")  # referans = eski varsayılan (sonnet+haiku) ×2 · taban = güncel varsayılan ssb
SADE = ("ipucu", "iş akışı", "is akisi", "prompt")


def agir(g, oy, oz, c):
    return g + 0.1 * oy + 1.25 * oz + 5 * c  # k0_olc AG ile aynı


def _kol(k):
    return json.loads((V16 / f"{k}.json").read_text(encoding="utf-8"))


def _url(u):
    u = re.sub(r"^https?://(www\.)?", "", u.strip().lower()).rstrip("/")
    return re.sub(r"[?#].*$", "", u)


def ogeler(form, vid):
    """(araç adları, linkler) — ipucu/iş akışı/prompt adayları ve videonun kendi adresi dışarıda."""
    ad = {a["ad"] for a in form.get("adaylar", []) if (a.get("tur") or "").lower() not in SADE}
    ln = {_url(x["url"]) for x in form.get("urller", [])} | {_url(x.get("url") or "") for x in form.get("aciklama_baglantilari", [])}
    ln |= {_url(a["repo_url"]) for a in form.get("adaylar", []) if a.get("repo_url")}
    return ad, {u for u in ln if u and vid[3:].lower() not in u}


def esit(a, havuz):
    """Ad normalleştirme (tüm kollara eşit): "jev (GliFormer)" / "jev, powered by GliFormer" → çekirdek ad "jev" da denenir."""
    h = [(x, "") for x in havuz] + [(re.split(r"\s*[(,]|\s+powered by\s+", x)[0], "") for x in havuz]
    return any(tr.eslestir(b, h) is not None for b in {a, re.split(r"\s*[(,]|\s+powered by\s+", a)[0]} if b)


def olc(ad, ln, rad, rln, metin):
    """→ (araç yakalama, link yakalama, yanlış pozitif); YP = referansta yok VE paket metninde (transkript+OCR+açıklama) geçmiyor."""
    ya = sum(esit(r, ad) for r in rad) / max(len(rad), 1)
    yl = len(rln & ln) / max(len(rln), 1)
    yp = sum(1 for a in ad if not esit(a, rad) and tr.normal(a) not in metin)
    tem = {u for u in rln if not re.search(r"\(|…|\.\.\.", u)}  # referansın kendisinin "ocr bozuk/kırpık" dediği adresler link değil (tüm kollara eşit)
    return ya, yl, yp, len(tem & ln) / max(len(tem), 1)


def m0():
    """Taban: video başı ağırlıklı jeton · süre · kategori (paket.md metni, kare, sabit istem, rapor yazımı)."""
    sabit = len(kisa.hafif.FABLE_VIDEO.get("C", "")) // 4 + 2500  # FABLE öneki + SISTEM+şema (~2.5k, VİDEO-16 sonda)
    out = {}
    for k in REF + TABAN:
        j = _kol(k)
        for v in ALTIN:
            s = j[v]
            metin = len((ONB / v / "paket.md").read_text(encoding="utf-8")) // 3
            cagri = s["cagri"]
            girdi = s["girdi"] + s["onb_okuma"] + s["onb_yazma"]
            out.setdefault(k, []).append({"v": v, "agir": agir(s["girdi"], s["onb_okuma"], s["onb_yazma"], s["cikti"]), "sure": s["duvar"],
                                          "adim": cagri, "rapor_yazimi": 5 * s["cikti"], "metin": metin * cagri, "sabit": sabit * cagri,
                                          "kare": max(girdi - (metin + sabit) * cagri, 0), "arastirma": 0})
    return out


def kos():
    """IG medyası hat tarafından CIK/medya'ya yeniden indirilir (önbellekte mp4 silinmiş); video-cache'e dokunulmaz."""
    CIK.mkdir(parents=True, exist_ok=True)
    iz, y = kisa.calistir(ALTIN + EK, ONB, CIK)
    (CIK / "oturum.json").write_text(json.dumps({"iz": iz, "sonuc": y}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("claude", y["hata"], y["sure"], y["usd"], y["usage"])


def puan():
    o = json.loads((CIK / (sys.argv[2:] or ["oturum.json"])[0]).read_text(encoding="utf-8"))
    yeni = {x["id"]: x for x in o["sonuc"]["form"]["videolar"]}
    u, n = o["sonuc"]["usage"], len(o["iz"])
    y_agir = agir(u.get("input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("output_tokens", 0)) / n
    t0 = {k: v for k, v in m0().items()}
    sat = []
    for k in REF + TABAN + ("yeni",):
        a = []
        for v in ALTIN:
            rad, rln = set(), set()
            for r in REF:
                x, y = ogeler(_kol(r)[v]["form"], v)
                rad |= x
                rln |= y
            metin = tr.normal((ONB / v / "paket.md").read_text(encoding="utf-8"))
            if k == "yeni":
                f = yeni[v]
                ad, ln = {x["ad"] for x in f["araclar"]}, {_url(x) for x in f["linkler"] + [x["link"] for x in f["araclar"] if x["link"]]}
                g = o["iz"][v]
                gs = g["gemini"].get("sure") or json.loads((ONB / v / "gemini.json").read_text(encoding="utf-8"))["_iz"]["sure"]  # önbellek dönüşünde süre kayıtta
                sure = max(gs, (g.get("metin") or {}).get("sure", 0)) + g["arastir"] + o["sonuc"]["sure"] / n  # metin geçişi izlemeye paralel
                ag = y_agir
            else:
                ad, ln = ogeler(_kol(k)[v]["form"], v)
                s = next(z for z in t0[k] if z["v"] == v)
                sure, ag = s["sure"], s["agir"]
            a.append((*olc(ad, ln, rad, rln, metin), ag, sure))
            print(k, v, *[round(x, 3) for x in a[-1][:4]], sep="\t", file=sys.stderr)
        sat.append((k, *[round(sum(z[i] for z in a) / len(a), 3) for i in range(6)]))
    print("kol\taraç_yak\tlink_yak\typ/video\tlink_temiz\tağır_tk/video\tsn/video")
    for s in sat:
        print(*s, sep="\t")


def kacak():
    """Kaçak analizi: altın videolarda yeni hattın kaçırdığı referans araçları + paket metninde (transkript+OCR+açıklama) geçip geçmediği."""
    o = json.loads((CIK / "oturum.json").read_text(encoding="utf-8"))
    yeni = {x["id"]: x for x in o["sonuc"]["form"]["videolar"]}
    for v in ALTIN:
        rad = set().union(*(ogeler(_kol(r)[v]["form"], v)[0] for r in REF))
        ad = {x["ad"] for x in yeni[v]["araclar"]}
        metin = tr.normal((ONB / v / "paket.md").read_text(encoding="utf-8"))
        kac = sorted(r for r in rad if not esit(r, ad))
        print(f"{v}\tref {len(rad)}\tkaçan {len(kac)}")
        for r in kac:
            print(f"  {'METİNDE' if tr.normal(r) in metin else 'yok    '}\t{r}")
        rln = set().union(*(ogeler(_kol(r)[v]["form"], v)[1] for r in REF))
        ln = {_url(x) for x in yeni[v]["linkler"] + [x["link"] for x in yeni[v]["araclar"] if x["link"]]}
        ham = (ONB / v / "paket.md").read_text(encoding="utf-8").lower()
        print(f"  link ref {len(rln)}\tkaçan {len(rln - ln)}")
        for r in sorted(rln - ln):
            print(f"  {'PAKETTE' if r in ham else 'yok    '}\t{r}")


if __name__ == "__main__":
    {"m0": lambda: print(json.dumps(m0(), ensure_ascii=False, indent=0)), "kos": kos, "puan": puan, "kacak": kacak}[sys.argv[1]]()
