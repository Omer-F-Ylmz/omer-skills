"""MOTOR-M4c birleşim simülasyonu: iki bağımsız okumanın birleşimi mevcut .kos verisinden (yeni tarama yok).

Kollar: (i) m3b-1 ∪ m3b-2 · (ii) m3b-1 ∪ luna-m3b · (iii)/(iv) aynıları, B'nin yalnız kendisinde olan kalemi doğrulamadan geçerse.
Tekilleştirme mevcut eşleme mantığıyla: B kalemi A'yla `anahtarlar` kesişiyorsa ya da A'nın da yakaladığı altın kaleme eşleşiyorsa kopya.
Doğrulama: M3b Jev k3 hükmü (+ k3_duzelt) ve kare kalemde görsel yargıç; eksik görsel hüküm video başına tek hafif çağrı (≤6, ≤$0,2).
"""
import json
import os
from pathlib import Path

import olcum_m3b as o3
import olcum_m4 as o4
import olcum_m4b as o4b
from video import hafif
from video import parti as pt

ANA, B = o4b.ANA, o4b.B
C = ANA / ".kos" / "m4c"
GORSEL_TAVAN = (6, 0.20)  # görsel yargıç (çağrı, $)
KOLLAR = {"(i) m3b-1 ∪ m3b-2": ("m3b2", False), "(ii) m3b-1 ∪ luna-m3b": ("luna", False),
          "(iii) m3b-1 ∪ luna-m3b doğrulamalı": ("luna", True), "(iv) m3b-1 ∪ m3b-2 doğrulamalı": ("m3b2", True)}


def birlesim(a, b, dogrula):
    """a, b: {"esl": {altın i: motor j}, "sinif": [..], "anah": [set]} → (kapsanan altın i'ler, birleşik sınıflar, eklenen B j'leri)."""
    ak, ae = set().union(*a["anah"]), set(a["esl"])
    ters = {j: i for i, j in b["esl"].items()}
    ekl = [j for j, s in enumerate(b["sinif"])
           if not (b["anah"][j] & ak or ters.get(j) in ae) and (not dogrula or s == "dayanıyor")]
    return ae | {i for i, j in b["esl"].items() if j in ekl}, a["sinif"] + [b["sinif"][j] for j in ekl], ekl


def kol(kv, paket, g):
    """Bir kolun bir videosu → esl/sınıf/anahtar + görsel hükmü eksik kare kalemleri {j: (metin, zaman)}."""
    motor = kv["motor"] or []
    esl = {int(i): j for i, j in {**kv["det"], **(kv.get("jev") or {})}.items()}
    sinif, eksik = [], {}
    for j, m in enumerate(motor):
        x = (kv.get("k3") or {}).get(str(j))
        v = "dayanıyor" if j in set(esl.values()) else o3.k3_duzelt(m, x, paket) if x else "ölçülemedi"
        if v == "kare-doğrulanamadı":
            v = g.get(m["metin"], "ölçülemedi")
            if v == "ölçülemedi":
                eksik[j] = (m["metin"], m["zaman"])
        sinif.append(v)
    return {"esl": esl, "sinif": sinif, "anah": [o3.anahtarlar(m["metin"], m["ad"]) for m in motor], "eksik": eksik}


def _maliyet(tara, on):
    xs = [x for k, x in (tara or {}).items() if k.startswith(on + "-")]
    return sum(x["cagri"] for x in xs), sum(x["usd"] for x in xs)


def _veri():
    e1, e2 = o4b._j(ANA / ".kos" / "m3b" / "esle.json")["veri"], o4b._j(B / "m3b2" / "esle.json")["veri"]
    g4, g42 = o4b._j(ANA / ".kos" / "m4" / "gorsel.json"), o4b._j(B / "m42" / "gorsel.json")
    G = o4b._j(C / "gorsel.json", {"m3b2": {}, "luna": {}, "cagri": 0, "usd": 0.0, "usd_kol": {"m3b2": 0.0, "luna": 0.0}})
    out = {}
    for vid, v in e1.items():
        p1 = (o4b.ANA_CACHE / vid / "paket-m3b.md").read_text(encoding="utf-8")
        p2 = (o4b.CACHE3 / vid / "paket.md").read_text(encoding="utf-8")
        out[vid] = {"altin": v["altin"],
                    "m3b-1": kol(v["kollar"]["sonnet"], p1, g4["m3b"].get(vid, {})),
                    "m3b2": kol(e2[vid]["kollar"]["sonnet"], p2, {**g42["m3b"].get(vid, {}), **G["m3b2"].get(vid, {})}),
                    "luna": kol(v["kollar"]["luna"], p1, G["luna"].get(vid, {}))}
    return out, G


def gorsel():
    """Eklenebilecek (kopya olmayan) B kalemlerinin eksik görsel hükmü: video başına tek çağrı, iki kol birlikte."""
    veri, G = _veri()
    env = dict(os.environ)
    for vid, d in veri.items():
        ist = [(k, *d[k]["eksik"][j]) for k in ("m3b2", "luna") for j in birlesim(d["m3b-1"], d[k], False)[2] if j in d[k]["eksik"]][:40]
        if not ist:
            continue
        if G["cagri"] >= GORSEL_TAVAN[0] or G["usd"] >= GORSEL_TAVAN[1] - .02:
            print(f"gorsel: tavan ({G['cagri']} çağrı / ${G['usd']:.3f}), {vid} ölçülemedi", flush=True)
            continue
        p = pt.paket_oku(o4b.ANA_CACHE / vid / "paket-m3b.md")
        kz = [(k, t) for k, t in zip(p["kareler"], p["kare_zaman"]) if Path(k).is_file()]
        zs = [z for *_, z in ist]
        sec = {min(kz, key=lambda k: abs((k[1] or 0) - z))[0] for z in zs if z is not None} if kz else set()
        sec = sorted(sec | ({k for k, _ in kz} if None in zs else set()))[:8]
        et, usd = o4.gorsel_yargi([m for _, m, _ in ist], sec, hafif.cagir, butce=min(.05, GORSEL_TAVAN[1] - G["usd"]), env=env)
        for (k, m, _), e in zip(ist, et):
            G[k].setdefault(vid, {})[m] = e
            G["usd_kol"][k] += usd / len(ist)
        G["cagri"], G["usd"] = G["cagri"] + 1, G["usd"] + usd
        print(f"gorsel {vid}: {len(ist)} kalem · {len(sec)} kare · {dict((e, et.count(e)) for e in set(et))} · ${usd:.3f}", flush=True)
        o4b._jy(C / "gorsel.json", G)
    o4b._jy(C / "gorsel.json", G)


def olc(veri, bk, dogrula):
    tum, esl, sinif = [], set(), []
    for d in veri.values():
        k, s, _ = birlesim(d["m3b-1"], d[bk], dogrula) if bk else (set(d["m3b-1"]["esl"]), d["m3b-1"]["sinif"], [])
        esl |= {len(tum) + i for i in k}
        tum += d["altin"]
        sinif += s
    m = o3.metrik(tum, esl)
    say = {e: sinif.count(e) for e in set(sinif)}
    return {"yuksek": m["yuksek"], "genel": m["genel"], "dayanmayan": (say.get("dayanmıyor", 0), len(sinif)), "sinif": say,
            "ol": o3.olcut(m, (say.get("dayanmıyor", 0), len(sinif)))}


def rapor():
    veri, G = _veri()
    t1, t2 = o4b._j(ANA / ".kos" / "m3b" / "tara.json"), o4b._j(B / "m3b2" / "tara.json")
    mal = {"m3b-1": _maliyet(t1, "sonnet"), "m3b2": _maliyet(t2, "sonnet"), "luna": _maliyet(t1, "luna")}
    out = {"m3b-1 (tek)": {**olc(veri, None, False), "usd": mal["m3b-1"][1], "sonnet_cagri": mal["m3b-1"][0]}}
    for ad, (bk, dg) in KOLLAR.items():
        dog = G["usd_kol"][bk] if dg else 0.0
        out[ad] = {**olc(veri, bk, dg), "usd": mal["m3b-1"][1] + mal[bk][1] + dog, "dogrulama_usd": dog,
                   "sonnet_cagri": mal["m3b-1"][0] + (mal[bk][0] if bk == "m3b2" else 0), "luna_cagri": mal[bk][0] if bk == "luna" else 0}
    out["_gorsel"] = {"cagri": G["cagri"], "usd": G["usd"], "jev": 0}
    o4b._jy(C / "sonuc.json", out)
    for ad, r in out.items():
        if not ad.startswith("_"):
            print(f"{ad}: yüksek {o3._pct(r['yuksek'])} · genel {o3._pct(r['genel'])} · dayanmayan {o3._pct(r['dayanmayan'])} · "
                  f"${r['usd']:.3f} · sonnet {r['sonnet_cagri']} · {r['sinif']} · {r['ol']}", flush=True)
    print("görsel:", out["_gorsel"], flush=True)


if __name__ == "__main__":
    gorsel()
    rapor()
