"""MOTOR-M4 ölçüm (M3c): aynı altın sete karşı M4 motoru — sonnet-m4 · luna-m4 · karma-m4 + K5b görsel yargıç (M3b kolları dahil).

Kullanım (tools/video'da): uv run python olcum_m4.py [hazirla|tara|esle|gorsel|rapor|hepsi]
olcum_m3b adımlarını KOS=.kos/m4 ile yeniden kullanır; M3b verisi .kos/m3b'den yalnız okunur. Ölçütler ve altın set değişmez.
karma-m4 bileşiktir: site/kod videolarında sonnet-m4, diğerlerinde luna-m4 koşusunun raporu (ek çağrı yok).
"""
import json
import os
import sys
from pathlib import Path

import olcum_m3b as o3
from video import hafif, kur
from video import parti as pt
from video import tarama as tr

REPO, CACHE = o3.REPO, o3.CACHE
M3B, KOS = REPO / ".kos" / "m3b", REPO / ".kos" / "m4"
KARMA_SONNET = {"86HM0RUWhCk", "JfmAm3sxCSc"}  # site/kod videoları (kuyruk notu/başlık: site_mu); diğerleri luna
# grup başına (hafif çağrı, $); dilim çağrıları dahil — sonnet Σ 10 / $1,2 · luna Σ 10 / $0,1
KOLLAR = {"sonnet": (None, [(2, .15), (5, .70), (3, .35)]),
          "luna": ("openai/gpt-6-luna-pro", [(2, .015), (5, .055), (3, .03)])}
GORSEL_TAVAN = (12, 0.4)
SISTEM_G = ("Görsel yargıçsın. Ekli kareler bir videodan. Numaralı her kalem için bu bilgi bu karelerde görülüyor mu karar ver: "
            "evet (karede açıkça görülüyor), hayır (karelerde yok ya da çelişiyor), okunamıyor (ilgili kare var ama çözünürlük/bulanıklık yüzünden okunamıyor).")
SEMA_G = {"type": "object", "required": ["kararlar"], "additionalProperties": False, "properties": {"kararlar": {"type": "array", "items": {
    "type": "object", "required": ["no", "karar"], "additionalProperties": False,
    "properties": {"no": {"type": "integer"}, "karar": {"type": "string", "enum": ["evet", "hayır", "okunamıyor"]}}}}}}
ETIKET = {"evet": "dayanıyor", "hayır": "dayanmıyor", "okunamıyor": "okunamıyor"}


def gorsel_yargi(kalemler, kareler, cagir, butce=.08, env=None):
    """K5b: video başına tek hafif çağrı → ([dayanıyor|dayanmıyor|okunamıyor|ölçülemedi], $)."""
    y = cagir(SISTEM_G, "Kalemler:\n" + "\n".join(f"{i + 1}. {k}" for i, k in enumerate(kalemler)), SEMA_G,
              kareler=list(kareler), model=hafif.MODEL, butce=butce, env=env)
    k = {x.get("no"): x.get("karar") for x in ((y.get("form") or {}).get("kararlar") or []) if isinstance(x, dict)}
    return [ETIKET.get(k.get(i + 1), "ölçülemedi") for i in range(len(kalemler))], y.get("usd") or 0.0


def _j(y, bos=None):
    return json.loads(y.read_text(encoding="utf-8")) if y.is_file() else bos


def hazirla():
    """M3b paketi paket-m3b.md olarak saklanır (görsel yargıç M3b karelerini görsün); paket.md M4 motoruyla yeniden üretilir."""
    for vid in o3.VIDEOLAR:
        p = CACHE / vid / "paket.md"
        if p.is_file() and "· paket: m4" not in p.read_text(encoding="utf-8").splitlines()[0]:
            if not (y := CACHE / vid / "paket-m3b.md").is_file():
                y.write_bytes(p.read_bytes())
            p.unlink()
            print(f"hazirla {vid}: paket-m3b.md saklandı, paket.md M4'te yeniden")


def gorsel():
    g = _j(KOS / "gorsel.json", {"m3b": {}, "m4": {}, "cagri": 0, "usd": 0.0})
    env = dict(os.environ)
    for ver, kok, pad in (("m3b", M3B, "paket-m3b.md"), ("m4", KOS, "paket.md")):
        for vid, v in _j(kok / "esle.json")["veri"].items():
            if vid in g[ver]:
                continue
            paket = (CACHE / vid / pad).read_text(encoding="utf-8")
            kal = {}
            for kv in v["kollar"].values():
                for j, x in (kv.get("k3") or {}).items():
                    if o3.k3_duzelt(m := kv["motor"][int(j)], x, paket) == "kare-doğrulanamadı":
                        kal[m["metin"]] = m["zaman"]
            if kal and (g["cagri"] >= GORSEL_TAVAN[0] or g["usd"] >= GORSEL_TAVAN[1] - .02):
                print(f"gorsel: tavan ({g['cagri']} çağrı / ${g['usd']:.3f}), {ver} {vid} ölçülemedi")
                continue
            if kal:
                p = pt.paket_oku(CACHE / vid / pad)
                kz = [(k, t) for k, t in zip(p["kareler"], p["kare_zaman"]) if Path(k).is_file()]
                sec = {min(kz, key=lambda k: abs((k[1] or 0) - z))[0] for z in kal.values() if z is not None} if kz else set()
                sec = sorted(sec | ({k for k, _ in kz} if None in kal.values() else set()))[:8]
                ad = list(kal)[:40]
                et, usd = gorsel_yargi(ad, sec, hafif.cagir, butce=min(.08, GORSEL_TAVAN[1] - g["usd"]), env=env)
                g[ver][vid], g["cagri"], g["usd"] = dict(zip(ad, et)), g["cagri"] + 1, g["usd"] + usd
                print(f"gorsel {ver} {vid}: {len(ad)} kalem · {len(sec)} kare · {dict((e, et.count(e)) for e in set(et))} · ${usd:.3f}")
            else:
                g[ver][vid] = {}
            KOS.mkdir(parents=True, exist_ok=True)
            (KOS / "gorsel.json").write_text(json.dumps(g, ensure_ascii=False, indent=1), encoding="utf-8")


def olc(veri, secim, g, pad):
    """Tek kol metriği; kare-doğrulanamadı → görsel yargıç kararı (yoksa ölçülemedi). Dayanmayan tek değer, okunamıyor ayrı."""
    tum, esl, say, seb, n, dus = [], set(), dict.fromkeys(("dayanıyor", "dayanmıyor", "okunamıyor", "ölçülemedi"), 0), {}, 0, 0
    for vid, v in veri.items():
        kv = v["kollar"][secim(vid)]
        if kv["motor"] is None:
            dus += 1
            continue
        paket = (CACHE / vid / pad).read_text(encoding="utf-8")
        esli = {int(i) for i in kv["det"]} | {int(i) for i in kv.get("jev", {})}
        for i, a in enumerate(v["altin"]):
            tum.append({**a, "vid": vid})
            if i in esli:
                esl.add(len(tum) - 1)
            elif a["onem"] in ("yüksek", "orta"):
                seb[s] = seb.get(s := o3.sebep(a, paket), 0) + 1
        n += len(kv["motor"])
        for j, x in kv.get("k3", {}).items():
            m = kv["motor"][int(j)]
            if (x := o3.k3_duzelt(m, x, paket)) == "kare-doğrulanamadı":
                x = g.get(vid, {}).get(m["metin"], "ölçülemedi")
            say[x] += 1
    m = o3.metrik(tum, esl)
    return {"m": m, "tum": tum, "esl": esl, "say": say, "seb": seb, "n": n, "dus": dus, "day": (say["dayanmıyor"], n), "ol": o3.olcut(m, (say["dayanmıyor"], n))}


def maliyet(kok):
    """(kol, video) → [usd, girdi jeton, çıktı jeton, çağrı]; grup çağrısı videolara eşit bölünür, dilim çağrıları sayılır."""
    out = {}
    for anah, x in (_j(kok / "tara.json") or {}).items():
        for e in tr.kayit_oku(REPO / ".kos" / x["pid"] / "defter.jsonl"):
            k = len(e["videolar"])
            for vid in e["videolar"]:
                o = out.setdefault((anah.rsplit("-", 1)[0], vid), [0.0, 0, 0, 0])
                o[0] += e["usd"] / k
                o[1] += (e["girdi"] + e["onb_okuma"] + e["onb_yazma"]) / k
                o[2] += e["cikti"] / k
                o[3] += e.get("dilim", 1) / k
    return out


def _alt(z, f):
    ix = [n for n, a in enumerate(z["tum"]) if f(a)]
    return o3._pct(o3.metrik([z["tum"][n] for n in ix], {k for k, n in enumerate(ix) if n in z["esl"]})["genel"]) if ix else "—"


def rapor():
    e3, e4, g = _j(M3B / "esle.json")["veri"], _j(KOS / "esle.json")["veri"], _j(KOS / "gorsel.json", {"m3b": {}, "m4": {}, "cagri": 0, "usd": 0.0})
    c3, c4 = maliyet(M3B), maliyet(KOS)
    kollar = {"sonnet (M3b)": (e3, lambda v: "sonnet", g["m3b"], "paket-m3b.md", c3, lambda v: "sonnet"),
              "luna (M3b)": (e3, lambda v: "luna", g["m3b"], "paket-m3b.md", c3, lambda v: "luna"),
              "qwen (M3b)": (e3, lambda v: "qwen", g["m3b"], "paket-m3b.md", c3, lambda v: "qwen"),
              "sonnet-m4": (e4, lambda v: "sonnet", g["m4"], "paket.md", c4, lambda v: "sonnet"),
              "luna-m4": (e4, lambda v: "luna", g["m4"], "paket.md", c4, lambda v: "luna"),
              "karma-m4": (e4, lambda v: "sonnet" if v in KARMA_SONNET else "luna", g["m4"], "paket.md", c4,
                           lambda v: "sonnet" if v in KARMA_SONNET else "luna")}
    oz = {}
    for ad, (veri, sec, gg, pad, c, ck) in kollar.items():
        z = oz[ad] = olc(veri, sec, gg, pad)
        z["c"] = [sum(c.get((ck(v), v), [0, 0, 0, 0])[i] for v in veri) for i in range(4)]
    s3, s4 = oz["sonnet (M3b)"], oz["sonnet-m4"]
    gk = lambda b: "GEÇTİ" if b else "KALDI"
    L = ["# M4 — altın set ölçümü (M3c: M4 motoru, M3b ile yan yana)", "",
         "Ölçütler ve altın set M3b ile aynı. Dayanmayan = K3 'dayanmıyor' + görsel yargıcın 'hayır' dediği kare kalemleri; 'okunamıyor' ayrı sayılır (K5b).",
         "M3b satırları aynı görsel yargıçla yeniden hesaplandı (m3b-altin-olcum.md'deki alt/üst sınır yerine tek değer).", "",
         "| kol | yüksek-önem | genel | dayanmayan | okunamıyor | ölçülemedi | motor kalem | hafif çağrı | girdi jeton | çıktı jeton | $ |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {k} | {o3._pct(z['m']['yuksek'])} | {o3._pct(z['m']['genel'])} | {o3._pct(z['day'])} | {z['say']['okunamıyor']} | {z['say']['ölçülemedi']} | "
          f"{z['n']} | {z['c'][3]:.0f} | {z['c'][1]:.0f} | {z['c'][2]:.0f} | {z['c'][0]:.4f} |" for k, z in oz.items()]
    L += ["", "## Ölçütler (sonnet-m4 = M4 motoru)",
          f"- yüksek-önem ≥%90: {gk(s4['ol']['yuksek'])} ({o3._pct(s4['m']['yuksek'])}) · M3b {o3._pct(s3['m']['yuksek'])}",
          f"- tüm kalemler ≥%75: {gk(s4['ol']['genel'])} ({o3._pct(s4['m']['genel'])}) · M3b {o3._pct(s3['m']['genel'])}",
          f"- dayanmayan ≤%5: {gk(s4['ol']['dayanmayan'])} ({o3._pct(s4['day'])}; okunamıyor {s4['say']['okunamıyor']}) · M3b {o3._pct(s3['day'])} (okunamıyor {s3['say']['okunamıyor']})",
          f"- sonuç: motor {'MÜKEMMEL' if all(s4['ol'].values()) else 'mükemmel DEĞİL'}", "",
          "## Kategori yakalama (sonnet)", "| kategori | M3b | M4 |", "|---|---|---|"]
    L += [f"| {k} | {_alt(s3, lambda a: a['kat'] == k)} | {_alt(s4, lambda a: a['kat'] == k)} |" for k in sorted({a["kat"] for a in s4["tum"]})]
    L += ["", "## Kategori × önem (sonnet)", "| kategori | önem | M3b | M4 |", "|---|---|---|---|"]
    L += [f"| {k[0]} | {k[1]} | {o3._pct(s3['m']['kirilim'].get(k, (0, 0)))} | {o3._pct(t)} |" for k, t in sorted(s4["m"]["kirilim"].items())]
    L += ["", "## Video yakalama (genel)", "| video | " + " | ".join(oz) + " |", "|---|" + "---|" * len(oz)]
    L += [f"| {vid} | " + " | ".join(_alt(z, lambda a: a["vid"] == vid) for z in oz.values()) + " |" for vid in e4]
    ad = {"a": "kaynak motora gitmedi", "b": "formda alan/kategori yok", "c": "model atladı"}
    L += ["", "## Kaçırma sebepleri (yüksek/orta, sonnet)", "| sebep | M3b | M4 |", "|---|---|---|"]
    L += [f"| ({k}) {ad[k]} | {s3['seb'].get(k, 0)} | {s4['seb'].get(k, 0)} |" for k in ad]
    art = lambda i: 100 * (s4["c"][i] / s3["c"][i] - 1) if s3["c"][i] else 0.0
    L += ["", "## Maliyet / jeton (K6: kural 21 kendi değişikliğimize)",
          f"- sonnet girdi jetonu M3b {s3['c'][1]:.0f} → M4 {s4['c'][1]:.0f} (%{art(1):+.0f}; K2 tam altyazı + yoğun kare 1568 px + K3 form alanları + K4 dilim çağrıları) · "
          f"çıktı %{art(2):+.0f} · çağrı {s3['c'][3]:.0f} → {s4['c'][3]:.0f} · $ {s3['c'][0]:.4f} → {s4['c'][0]:.4f} (%{art(0):+.0f})",
          f"- görsel yargıç (ayrı satır, sonnet tavanına dahil değil): {g['cagri']} hafif çağrı · ${g['usd']:.4f} · tavan {GORSEL_TAVAN[0]} / ${GORSEL_TAVAN[1]}", "",
          "## Kural 21 takası (kur.takas)", "| kol | taban | yakalama düşüşü | tasarruf | ölçütler | karar |", "|---|---|---|---|---|---|"]
    for k, taban in (("sonnet-m4", "sonnet (M3b)"), ("luna-m4", "sonnet-m4"), ("karma-m4", "sonnet-m4")):
        z, t = oz[k], oz[taban]
        dus = max(0.0, 100 * (o3.oran(t["m"]["genel"]) - o3.oran(z["m"]["genel"])) / (o3.oran(t["m"]["genel"]) or 1), 100 * z["dus"] / len(e4))
        tas = 100 * (1 - z["c"][0] / t["c"][0]) if t["c"][0] else 0.0
        L.append(f"| {k} | {taban} | %{dus:.0f} | %{tas:.0f} | {gk(all(z['ol'].values()))} | {' — '.join(kur.takas(tas, dus, all(z['ol'].values())))} |")
    ta = _j(KOS / "tara.json") or {}
    L += ["", "Tarama (M4): " + " · ".join(f"{k} {x['pid']} {x['videolar']}" for k, x in ta.items()),
          f"karma-m4 bileşik: {', '.join(sorted(KARMA_SONNET))} sonnet-m4, diğerleri luna-m4 raporu (ek çağrı yok; tek örnek, yeniden koşu değil)."]
    (REPO / "docs" / "olcumler" / "m4-altin-olcum.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("rapor: docs/olcumler/m4-altin-olcum.md")
    for k, z in oz.items():
        print(f"{k}: yüksek {o3._pct(z['m']['yuksek'])} · genel {o3._pct(z['m']['genel'])} · dayanmayan {o3._pct(z['day'])} · okunamıyor {z['say']['okunamıyor']}"
              f" · kare {_alt(z, lambda a: a['kat'] == 'Kareden bilgi')} · Jfm {_alt(z, lambda a: a['vid'] == 'JfmAm3sxCSc')} · sebep {z['seb']} · ${z['c'][0]:.4f} · girdi {z['c'][1]:.0f}")


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    sys.path.insert(0, str(REPO / "tools" / "jev"))
    o3.KOS, o3.KOLLAR, o3.AD = KOS, KOLLAR, "m4"
    adim = sys.argv[1] if len(sys.argv) > 1 else "hepsi"
    for ad, f in (("hazirla", hazirla), ("tara", o3.tara), ("esle", o3.esle), ("gorsel", gorsel), ("rapor", rapor)):
        if adim in (ad, "hepsi"):
            f()
