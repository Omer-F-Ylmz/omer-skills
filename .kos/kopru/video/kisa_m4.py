"""VİDEO-KISA-TOKEN-1 ölçüm: m0 (taban, .kos/v16 kayıtlarından, claude -p yok) · kos (yeni hat, 1 claude -p) · puan (altın kümede kapı).
python .kos/kopru/video/kisa_m4.py m0|kos|puan    (tools/video/.venv python'u; PYTHONPATH=tools/video)
"""
import json
import re
import shutil
import subprocess
import sys
import time
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
SINAMA = ("ig-DYKSh1iv8nP", "ig-DbG_xa3y_d6", "ig-DeXK9x7jQfb", "ig-Ddx-cbVNEva", "ig-Ddg8Mqnv0R5", "ig-DcDfnzsM2wL")  # 14 Eki d9: linkler-14eki.txt'teki ilk 6 önbelleksiz reel (seçimde ayar yok)
SADE = ("ipucu", "iş akışı", "is akisi", "prompt", "teknik")  # 14 Eki 19:15 Desktop: teknik ayrı alan, araç sayımına/yp'ye girmez


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
    yl = len(rln & ln) / len(rln) if rln else None  # referansta link yoksa (DeW7) 0/0 ortalamaya girmez
    yp = sum(1 for a in ad if not esit(a, rad) and not any(tr.normal(b) in metin for b in re.split(r"[()]", a) if tr.normal(b)))  # "OpenAI Luna (GPT-6 Luna)": parçalardan biri metinde yeter
    tem = {u for u in rln if not re.search(r"\(|…|\.\.\.", u)}  # referansın kendisinin "ocr bozuk/kırpık" dediği adresler link değil (tüm kollara eşit)
    return ya, yl, yp, len(tem & ln) / len(tem) if tem else None


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


def hazirla():
    """Sınama kümesi paketleri (hat indirir: meta + Groq konuşma + OCR); ağır iş, seri."""
    for v in SINAMA:
        if not (ONB / v / "paket.md").is_file():
            t = time.monotonic()
            for adim in ("ozet", "paket"):
                r = subprocess.run([str(Path(sys.executable).parent / "video.exe"), adim, v], capture_output=True, text=True, encoding="utf-8", errors="replace")
                print(v, adim, r.returncode, round(time.monotonic() - t, 1), (r.stdout + r.stderr)[-300:].replace("\n", " | "), flush=True)
                if r.returncode:
                    break
    print("BITTI")


def kos():
    """IG medyası hat tarafından CIK/medya'ya yeniden indirilir (önbellekte mp4 silinmiş); video-cache'e dokunulmaz."""
    CIK.mkdir(parents=True, exist_ok=True)
    ids, ad = (SINAMA, "oturum-sinama.json") if "sinama" in sys.argv[3:] else (ALTIN + EK, "oturum.json")
    for v in ids:  # süre ölçümü taze izlemeyle: Gemini önbelleği yedeğe (araştırma önbelleği M2 gereği kalır)
        for a in ("gemini.json", "gemini-metin.json"):
            if (ONB / v / a).is_file():
                (ONB / v / a).replace(ONB / v / a.replace(".json", f"-{sys.argv[2] if sys.argv[2:] else 'eski'}.json"))
    if "claudesiz" in sys.argv[3:]:  # d12: Claude öncesi deterministik liste, medya tekrar için kalır (claude -p 0)
        ad = ad.replace(".json", f"-{sys.argv[2]}.json")
    iz, y = kisa.calistir(ids, ONB, CIK, claude="claudesiz" not in sys.argv[3:], sil="claudesiz" not in sys.argv[3:])
    (CIK / ad).write_text(json.dumps({"iz": iz, "sonuc": y}, ensure_ascii=False, indent=1), encoding="utf-8")
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
            rln -= {u for u in rln if any(w.startswith(u + "…") for w in rln)}  # TOKEN-2 M7d: ref'in kendisi "u… kırpık" diyorsa u OCR kırpığı (DeHMM altın link 0.85'in kökü), tüm kollara eşit
            if "temiz" in sys.argv[3:]:  # yalnız denetimde kanıtlı kalemler (Desktop onayı bekleyen liste)
                d = json.loads((CIK / "altin-denetim.json").read_text(encoding="utf-8"))[v]
                rad, rln = {a for a in rad if d["arac"].get(a)}, {u for u in rln if d["link"].get(u)}
            metin = tr.normal((ONB / v / "paket.md").read_text(encoding="utf-8"))
            if k == "yeni":
                f = yeni[v]
                ad, ln = {x["ad"] for x in f["araclar"] if (x.get("tur") or "").lower() != "teknik"}, {_url(x) for x in f["linkler"] + [x["link"] for x in f["araclar"] if x["link"]]}
                g = o["iz"][v]
                gs = g["gemini"].get("sure") or json.loads((ONB / v / "gemini.json").read_text(encoding="utf-8"))["_iz"]["sure"]  # önbellek dönüşünde süre kayıtta
                sure = max(gs, (g.get("metin") or {}).get("sure", 0)) + g["arastir"] + o["sonuc"]["sure"] / n  # metin geçişi izlemeye paralel
                sure = o["sonuc"].get("duvar", sure * n) / n  # d7+: videolar paralel → toplu duvar saati / video
                ag = y_agir
            else:
                ad, ln = ogeler(_kol(k)[v]["form"], v)
                s = next(z for z in t0[k] if z["v"] == v)
                sure, ag = s["sure"], s["agir"]
            a.append((*olc(ad, ln, rad, rln, metin), ag, sure))
            print(k, v, *[x if x is None else round(x, 3) for x in a[-1][:4]], sep="\t", file=sys.stderr)
        sat.append((k, *[round(sum(z[i] for z in a if z[i] is not None) / max(sum(1 for z in a if z[i] is not None), 1), 3) for i in range(6)]))
    print("kol\taraç_yak\tlink_yak\typ/video\tlink_temiz\tağır_tk/video\tsn/video")
    for s in sat:
        print(*s, sep="\t")


def kacak():
    """Kaçak analizi: altın videolarda yeni hattın kaçırdığı referans araçları + paket metninde (transkript+OCR+açıklama) geçip geçmediği."""
    o = json.loads((CIK / (sys.argv[2:] or ["oturum.json"])[0]).read_text(encoding="utf-8"))
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


def _kanit(ad, satirlar):
    """Paket.md'de (açıklama/transkript/OCR) adın geçtiği ilk yer: 'bölüm [zaman] …kesit…' ya da None."""
    adlar = {tr.normal(b) for b in (ad, re.split(r"\s*[(,]|\s+powered by\s+", ad)[0], ad.split("/")[-1]) if len(tr.normal(b)) >= 2}
    bol = ""
    for s in satirlar:
        if s.startswith("## "):
            bol = s[3:].strip()
            continue
        if any(a in tr.normal(s) for a in adlar):
            z = re.findall(r"\[[\d:.]+\]", s)
            return f"{bol} {z[0] if z else ''} {s[:90].strip()}"
    return None


def denetle():
    """Geçerlilik (a): altın referansın her kalemi pakette kanıtlanır; kanıtsızlar ayrı listede (silinmez, Desktop onaylar) → kisa/altin-denetim.json."""
    out = {}
    for v in ALTIN:
        sat = (ONB / v / "paket.md").read_text(encoding="utf-8").splitlines()
        rad = set().union(*(ogeler(_kol(r)[v]["form"], v)[0] for r in REF))
        rln = set().union(*(ogeler(_kol(r)[v]["form"], v)[1] for r in REF))
        ar = {a: _kanit(a, sat) for a in sorted(rad)}
        ln = {}
        for u in sorted(rln):
            k = next((f"pakette: {s[:90].strip()}" for s in sat if u in s.lower()), None)
            gh = re.match(r"github\.com/([\w.-]+/[\w.-]+)$", u)
            ln[u] = k or (f"araştırma: gh repos/{gh[1]} var" if gh and kisa._repo_var(gh[1]) else None)
        out[v] = {"arac": ar, "link": ln}
        print(f"{v}\taraç {sum(1 for x in ar.values() if x)}/{len(ar)} kanıtlı\tlink {sum(1 for x in ln.values() if x)}/{len(ln)} kanıtlı")
        for k, d in (("araç", ar), ("link", ln)):
            for a, x in d.items():
                if not x:
                    print(f"  KANITSIZ {k}\t{a}")
    (CIK / "altin-denetim.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


REF_SISTEM = ("Kısa video paket metinlerinden (açıklama, konuşma dökümü, ekran OCR'ı, linkler) referans listesi çıkarıyorsun. Her VIDEO için: "
              "araclar = metinde ADI GEÇEN her araç/repo/model/kütüphane/servis/site/uygulama/dil/platform (eksiksiz; kişi adı, arayüz düğmesi, sıradan kelime değil); "
              "teknikler = adı konmuş yöntem/kavramlar; linkler = metinde geçen her URL ve github sahip/repo (aynen). Uydurma yok, metinde olmayanı yazma.")
REF_SEMA = {"type": "object", "required": ["videolar"], "properties": {"videolar": {"type": "array", "items": {"type": "object", "required": ["id", "araclar", "teknikler", "linkler"],
            "properties": {"id": {"type": "string"}, "araclar": {"type": "array", "items": {"type": "string"}},
                           "teknikler": {"type": "array", "items": {"type": "string"}}, "linkler": {"type": "array", "items": {"type": "string"}}}}}}}


def sinama_ref():
    """Geçerlilik (b): referans = yeni hat ∪ bağımsız Claude paket okuması (1 claude -p); her kalem pakette kanıtlanır, kanıtsızlar ayrı (silinmez)."""
    o = json.loads((CIK / "oturum-sinama.json").read_text(encoding="utf-8"))
    hat = {x["id"]: x for x in o["sonuc"]["form"]["videolar"]}
    y = kisa.hafif.cagir(REF_SISTEM, "\n\n".join(f"VIDEO {v}\n{(ONB / v / 'paket.md').read_text(encoding='utf-8')}" for v in SINAMA), REF_SEMA, efor="medium", butce=1.0)
    cl = {x["id"]: x for x in (y["form"] or {}).get("videolar", [])}
    out = {"_claude": {k: y.get(k) for k in ("sure", "usd", "usage", "hata")}}
    for v in SINAMA:
        sat = (ONB / v / "paket.md").read_text(encoding="utf-8").splitlines()
        h, c = hat.get(v, {"araclar": [], "linkler": []}), cl.get(v, {"araclar": [], "teknikler": [], "linkler": []})
        ar = {a["ad"]: "hat" for a in h["araclar"] if (a.get("tur") or "").lower() != "teknik"}
        for a in c["araclar"]:
            if not esit(a, ar):
                ar[a] = "claude"
        ln = {_url(u): "hat" for u in h["linkler"]} | {_url(u): "claude" for u in c["linkler"] if _url(u) not in {_url(x) for x in h["linkler"]}}
        ham = "\n".join(sat).lower()
        out[v] = {"arac": {a: [k, _kanit(a, sat)] for a, k in ar.items()},
                  "link": {u: [k, next((s[:90] for s in sat if u in s.lower()), None) or (u.split("/")[-1] in ham and "pakette ad")] for u, k in ln.items() if u and v[3:].lower() not in u},
                  "teknik": c["teknikler"] + [a["ad"] for a in h["araclar"] if (a.get("tur") or "").lower() == "teknik"]}
        print(v, "araç", sum(1 for x in out[v]["arac"].values() if x[1]), "/", len(out[v]["arac"]), "link", sum(1 for x in out[v]["link"].values() if x[1]), "/", len(out[v]["link"]))
    (CIK / "sinama-ref.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("claude", out["_claude"])


def sinama_puan():
    """Sınama kümesi: kanıtlı referansa karşı yeni hattın araç/link yakalaması + yp (kanıtlı ref dışı ve pakette geçmeyen)."""
    o = json.loads((CIK / (sys.argv[2:] or ["oturum-sinama.json"])[0]).read_text(encoding="utf-8"))
    ref = json.loads((CIK / "sinama-ref.json").read_text(encoding="utf-8"))
    yeni, n, a = {x["id"]: x for x in o["sonuc"]["form"]["videolar"]}, len(o["iz"]), []
    for v in SINAMA:
        f = yeni[v]
        ad = {x["ad"] for x in f["araclar"] if (x.get("tur") or "").lower() != "teknik"}
        ln = {_url(x) for x in f["linkler"] + [x["link"] for x in f["araclar"] if x["link"]]}
        rad = {k for k, x in ref[v]["arac"].items() if x[1] and k not in GURULTU}
        rln = {k for k, x in ref[v]["link"].items() if x[1]}
        ya, yl, yp, _ = olc(ad, ln, rad, rln, tr.normal((ONB / v / "paket.md").read_text(encoding="utf-8")))
        a.append((ya, yl, yp))
        print(v, len(rad), len(rln), round(ya, 3), yl if yl is None else round(yl, 3), yp, sep="\t")
        for r in sorted(r for r in rad if not esit(r, ad)) + sorted(rln - ln):
            print("  kaçan", r)
    s = o["sonuc"]
    print("ort araç", round(sum(x[0] for x in a) / len(a), 3), "link", round(sum(x[1] for x in a if x[1] is not None) / max(sum(1 for x in a if x[1] is not None), 1), 3),
          "yp/video", round(sum(x[2] for x in a) / len(a), 2), "| sn/video", round(s["duvar"] / n, 1), "hazır", round(s["hazir_sure"] / n, 1), "claude", s["sure"],
          "| ağır_tk/video", round(agir(s["usage"].get("input_tokens", 0), s["usage"].get("cache_read_input_tokens", 0), s["usage"].get("cache_creation_input_tokens", 0), s["usage"].get("output_tokens", 0)) / n))


GURULTU = ("CLI", "Skills", "Mac", "Bytebase")  # 14 Eki 20:30 Desktop: ref'teki genel kelimeler araç değil → referanstan çıkar, raporda ayrı satır · TOKEN-2 M7e: Bytebase = star-history sponsor linki


def gemini_puan():
    """Claude'suz kararlılık (claude -p 0): SINAMA taze Gemini (izle + metin geçişi) → birleşik araç listesinin (Claude öncesi) kanıtlı ref yakalaması.
    Medya kisa/medya'da kalır (tekrar koşu yeniden indirmez); çıktılar <id>/gemini-<etiket>.json."""
    from video import instagram
    ref, et, a = json.loads((CIK / "sinama-ref.json").read_text(encoding="utf-8")), sys.argv[2], []
    for v in SINAMA:
        d, m = ONB / v, CIK / "medya" / v
        video = json.loads((d / "meta.json").read_text(encoding="utf-8")).get("video")
        if video and not (m / "goz-video.mp4").is_file():
            instagram.getir(m)
        g, gi = kisa.izle(d, m if video else None, yeniden=True)
        mg = kisa.metin_gec(d, yeniden=True)
        for f in ("gemini.json", "gemini-metin.json"):
            shutil.copy(d / f, d / f.replace(".json", f"-{et}.json"))
        ad = {x["ad"] for x in kisa.birlestir(g, mg)["araclar"]}
        rad = {k for k, x in ref[v]["arac"].items() if x[1] and k not in GURULTU}
        kac = sorted(r for r in rad if not esit(r, ad))
        a.append(1 - len(kac) / max(len(rad), 1))
        print(v, gi.get("model"), gi.get("sure"), len(rad), round(a[-1], 3), "kaçan:", kac, flush=True)
    print(et, "ort araç (Claude öncesi)", round(sum(a) / len(a), 3))


if __name__ == "__main__":
    {"m0": lambda: print(json.dumps(m0(), ensure_ascii=False, indent=0)), "kos": kos, "puan": puan, "kacak": kacak, "denetle": denetle, "hazirla": hazirla, "sinama_ref": sinama_ref, "sinama_puan": sinama_puan,
     "gemini_puan": gemini_puan}[sys.argv[1]]()
