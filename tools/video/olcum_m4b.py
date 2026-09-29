"""MOTOR-M4b ölçüm: gürültü (koşu-2) + kalem düzeyi + K4 kare-luna. Motor koduna ve altın sete dokunmaz.

Kullanım (tools/video'da): uv run python olcum_m4b.py <adim>...  (k1 · m42 · m3b2 · kare · esle · gorsel · rapor)
m3b2 kendini 7a550e3 worktree'sinin koduyla (M4B_KOD, VIDEO_CACHE=.kos/m4b/cache-m3b) yeniden çağırır; ana ağaç değişmez.
Koşu-2 tavanı = koşu-1'in gerçek (çağrı, $) toplamı ×1,2, gruplara koşu-1 oranıyla bölünür; tavanlar .kos/m4b/tavan.json'da.
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

if os.environ.get("M4B_KOD"):  # m3b2 alt süreci: M3b motoru (7a550e3) önce gelir
    sys.path.insert(0, os.environ["M4B_KOD"])
import olcum_m3b as o3
from video import cli, hafif
from video import parti as pt

ANA = Path(__file__).resolve().parents[2]
ANA_CACHE = o3.CACHE
B = ANA / ".kos" / "m4b"
WT = ANA.parent / "omer-skills-m3b"
CACHE3 = B / "cache-m3b"
LUNA = "openai/gpt-6-luna-pro"
K4_TAVAN = (20, 0.15)   # luna kare okuma (çağrı, $)
KG_TAVAN = (5, 0.20)    # kare-luna kolunun görsel yargıcı (sonnet)
SISTEM_K = ("Video karelerinden somut bilgi çıkarıcısın. Ekli kareler sırayla verilen zamanlara ait. Her kare için ekranda OKUNAN somut bilgiyi yaz: "
            "araç/site/repo adı, URL, komut, ayar/değer, kod, arayüz öğesi ve ne işe yaradığı. Kurulum/terminal komutu → Kurulum/komutlar; "
            "yöntem/ipucu/iş akışı → Teknikler; diğer her şey → Kareden bilgi. Karede okunmayanı yazma; somut bilgi yoksa o kareyi atla. "
            "zaman alanına listedeki zamanı aynen yaz.")
SEMA_K = {"type": "object", "required": ["kareler"], "properties": {"kareler": {"type": "array", "items": {
    "type": "object", "required": ["zaman", "bilgi", "bolum"], "properties": {
        "zaman": {"type": "string"}, "bilgi": {"type": "string"},
        "bolum": {"type": "string", "enum": ["Kareden bilgi", "Kurulum/komutlar", "Teknikler"]}}}}}}


def k4_zamanlar(sure_dk):
    """Altın setin kare aralığı: short (≤1 dk) 5 sn · uzun max(30 sn, süre/45); aralık ortaları."""
    sure = sure_dk * 60
    ar = 5 if sure_dk <= 1 else max(30, sure / 45)
    return [ar / 2 + i * ar for i in range(int(sure / ar + 1e-9))]


def tavan_bol(gercek, oran=1.2):
    """Koşu-1 grup başına gerçek (çağrı, $) → Σ×oran, gruplara aynı oranla; çağrı yukarı yuvarlanır, fark en büyük gruba."""
    C, U = math.ceil(sum(c for c, _ in gercek) * oran - 1e-9), sum(u for _, u in gercek) * oran
    cs = [max(1, round(c * oran)) for c, _ in gercek]
    b = max(range(len(cs)), key=lambda i: gercek[i][0])
    cs[b] += C - sum(cs)
    return [(c, round(u * oran, 4)) for c, (_, u) in zip(cs, gercek)]


def durum_sinifi(xs):
    v = [x for x in xs if x is not None]
    return "ölçülemedi" if not v else "hep yakaladı" if all(v) else "hep kaçtı" if not any(v) else "bazen"


def gurultu(a, b):
    """(isabet, toplam) × 2 koşu → (fark puan, havuz ortalama, ± yarı fark)."""
    r1, r2 = o3.oran(a), o3.oran(b)
    return 100 * abs(r1 - r2), (a[0] + b[0]) / ((a[1] + b[1]) or 1), abs(r1 - r2) / 2


def luna_ekle(md, kalemler):
    """Kare-luna kalemleri rapora bölüm başlığıyla madde olarak eklenir; 'karede' işareti K3'te kare-doğrulanamadı yoluna sokar."""
    bol = {}
    for k in kalemler:
        if (b := " ".join(str(k.get("bilgi") or "").split())):
            bol.setdefault(k.get("bolum") or "Kareden bilgi", []).append(f"- {k.get('zaman', '')} · karede: {b}")
    return md.rstrip("\n") + "\n" + "".join(f"\n## {b} (kare-luna)\n" + "\n".join(x) + "\n" for b, x in bol.items())


def _j(p, bos=None):
    return json.loads(p.read_text(encoding="utf-8")) if p and p.is_file() else bos


def _jy(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")


def _ss(t):
    return f"{int(t) // 60:02d}:{int(t) % 60:02d}" if t is not None else "—"


def _gercek(tara):
    return [(x["cagri"], x["usd"]) for k, x in sorted(tara.items()) if k.startswith("sonnet-")]


def _toplam(tara):
    x = [y for k, y in (tara or {}).items() if k.startswith("sonnet-")]
    return [sum(y["cagri"] for y in x), sum(y["usd"] for y in x), sum(y["jeton"] or 0 for y in x)]


def _tavan_yaz(ad, t):
    d = _j(B / "tavan.json", {})
    d[ad] = t
    _jy(B / "tavan.json", d)
    print(f"{ad} tavan: {t}", flush=True)


def _bitti(d, ad):
    du = {v: s for x in d.values() for v, s in x["videolar"].items()}
    eksik = [v for v, s in du.items() if not s.startswith("tamam")]
    print(f"{ad}: {du}" + (f" · DUR: {eksik} tamamlanmadı" if eksik else " · 5/5 tamam"), flush=True)


def _durum(x):
    pdir = o3.REPO / ".kos" / x["pid"]
    x["cagri"], x["usd"], x["jeton"] = pt._defter(pdir)
    x["videolar"] = {v: s["tarama"]["durum"] for v, s in _j(pdir / "durum.json")["videolar"].items()}


def _m4():
    import olcum_m4 as m4
    sys.path.insert(0, str(ANA / "tools" / "jev"))
    o3.KOS, o3.KOLLAR, o3.AD, o3.CACHE = m4.KOS, m4.KOLLAR, "m4", ANA_CACHE
    return m4


def k1():
    """86HM0RUWhCk: M4 sonnet/luna uzun grubu parti devam; kol başı ≤3 ek çağrı, Σ$ ≤0,35 (0,32 + 0,03). Sonra M4 esle/gorsel/rapor."""
    m4 = _m4()
    d = o3._oku("tara")
    for kol, hedef in (("sonnet", .32), ("luna", .03)):
        x = d[f"{kol}-1"]
        if "tavan" not in x["videolar"].values():
            continue
        pdir = ANA / ".kos" / x["pid"]
        ta = _j(pdir / "durum.json")["tavan"]
        n, usd, _ = pt._defter(pdir)
        ek = (max(0, n + 3 - ta["cagri"]), max(0.0, round(usd + hedef - ta["usd"], 4)))
        _tavan_yaz(f"k1-{kol}", {"onceki": ta, "harcanan": [n, round(usd, 4)], "ek": ek, "hedef_usd": hedef})
        env = {**os.environ, "VIDEO_TARAMA_DIZIN": str(m4.KOS / kol / "rapor"), "PYTHONIOENCODING": "utf-8"}
        asil = hafif.cagir
        if kol == "luna":
            hafif.cagir = o3.or_cagir(LUNA, env)
        try:
            x["rc"] = cli.main(["parti", "devam", x["pid"], "--cagri-ek", str(ek[0]), "--usd-ek", f"{ek[1]:.4f}"], env=env)
        finally:
            hafif.cagir = asil
        _durum(x)
        o3._yaz("tara", d)
        print(f"k1 {kol}: {x}", flush=True)
    o3.esle()
    m4.gorsel()
    m4.rapor()


def m42():
    tav = tavan_bol(_gercek(_j(ANA / ".kos" / "m4" / "tara.json")))
    _tavan_yaz("m42", {"gruplar": tav, "toplam": [sum(c for c, _ in tav), round(sum(u for _, u in tav), 4)], "kaynak": "M4-1 (K1 dahil) ×1,2"})
    o3.KOS, o3.KOLLAR, o3.AD = B / "m42", {"sonnet": (None, tav)}, "m4b2m4"
    _bitti(o3.tara(), "m42")


def m3b2():
    if not os.environ.get("M4B_KOD"):
        for vid in o3.VIDEOLAR:
            if not (h := CACHE3 / vid).is_dir():
                shutil.copytree(ANA_CACHE / vid, h)
                (h / "paket.md").write_bytes((ANA_CACHE / vid / "paket-m3b.md").read_bytes())
        env = {**os.environ, "M4B_KOD": str(WT / "tools" / "video"), "VIDEO_CACHE": str(CACHE3), "PYTHONIOENCODING": "utf-8"}
        sys.exit(subprocess.run([sys.executable, __file__, "m3b2"], env=env, cwd=WT / "tools" / "video").returncode)
    tav = tavan_bol(_gercek(_j(ANA / ".kos" / "m3b" / "tara.json")))
    C, U = sum(c for c, _ in tav), sum(u for _, u in tav)
    _tavan_yaz("m3b2", {"gruplar": tav, "toplam": [C, round(U, 4)], "kaynak": "M3b-1 (onar dahil) ×1,2", "motor": "7a550e3"})
    o3.KOS, o3.KOLLAR, o3.AD = B / "m3b2", {"sonnet": (None, tav)}, "m4b2m3b"
    d = o3.tara()
    for anah, x in d.items():  # M3b protokolü: form_red bir kez yeniden (o3.onar), Σ C / $U içinde
        n, u = sum(y["cagri"] for y in d.values()), sum(y["usd"] for y in d.values())
        if "form_red" not in x["videolar"].values() or n + 1 > C:
            continue
        env = {**os.environ, "VIDEO_TARAMA_DIZIN": str(o3.KOS / "sonnet" / "rapor"), "PYTHONIOENCODING": "utf-8"}
        cli.main(["parti", "devam", x["pid"], "--form-red-yeniden", "--cagri-ek", "1", "--usd-ek", f"{max(0.0, U - u - .005):.3f}"], env=env)
        _durum(x)
        o3._yaz("tara", d)
        print(f"onar {anah}: {x}", flush=True)
    _bitti(d, "m3b2")


def _kare_cek(vid, zs, d):
    url = subprocess.run(["yt-dlp", "-g", "--no-warnings", "-f", "bv*[height<=720][vcodec!=none]/b", vid],
                         capture_output=True, text=True, timeout=180).stdout.split()[0]

    def bir(t):
        y = d / f"k{int(t):05d}.jpg"
        try:
            if not y.is_file():
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-rw_timeout", "15000000", "-ss", f"{t:g}", "-i", url, "-vf",
                                "scale='min(1024,iw)':-2,format=yuvj420p", "-frames:v", "1", "-q:v", "4", str(y)], capture_output=True, timeout=120)
        except subprocess.TimeoutExpired:
            pass
        return (y, t) if y.is_file() else None

    with ThreadPoolExecutor(6) as ex:
        return [k for k in ex.map(bir, zs) if k]


def kare():
    """K4: altın set aralığında YALNIZ kare okuma (luna, ≤15 kare/çağrı); sonuç sonnet-m3b koşu-1 raporuna eklenir → m3b+kare-luna kolu."""
    k = _j(B / "kare" / "luna.json", {"cagri": 0, "usd": 0.0, "veri": {}})
    env = dict(os.environ)
    cagir = o3.or_cagir(LUNA, env)
    for vid, (dk, _) in o3.VIDEOLAR.items():
        if vid in k["veri"]:
            continue
        (d := B / "kare" / vid).mkdir(parents=True, exist_ok=True)
        kz = _kare_cek(vid, k4_zamanlar(dk), d)
        out = []
        for i in range(0, len(kz), 15):
            if k["cagri"] >= K4_TAVAN[0] or k["usd"] >= K4_TAVAN[1] - .01:
                print(f"kare: tavan {K4_TAVAN} — DUR ({vid} yarım, kaydedilmedi)", flush=True)
                return
            p = kz[i:i + 15]
            y = cagir(SISTEM_K, "Kare zamanları (ekler sırayla):\n" + "\n".join(f"{j + 1}. {_ss(t)}" for j, (_, t) in enumerate(p)), SEMA_K,
                      kareler=[str(a) for a, _ in p], butce=.02)
            k["cagri"], k["usd"] = k["cagri"] + 1, k["usd"] + (y.get("usd") or 0.0)
            b = [x for x in ((y.get("form") or {}).get("kareler") or []) if isinstance(x, dict)]
            out += b
            print(f"kare {vid} {i // 15 + 1}: {len(p)} kare · {len(b)} bilgi · ${y.get('usd') or 0:.4f} · hata {y.get('hata')}", flush=True)
        k["veri"][vid] = {"kareler": [[str(a), t] for a, t in kz], "bilgi": out}
        _jy(B / "kare" / "luna.json", k)
    rd = B / "kare" / "sonnet" / "rapor"
    rd.mkdir(parents=True, exist_ok=True)
    for vid, v in k["veri"].items():
        r = sorted((ANA / ".kos" / "m3b" / "sonnet" / "rapor").glob(f"*-{vid}.md"))[-1]
        (rd / r.name).write_text(luna_ekle(r.read_text(encoding="utf-8"), v["bilgi"]), encoding="utf-8")
    print(f"kare: Σ {k['cagri']} çağrı · ${k['usd']:.4f} (tavan {K4_TAVAN}) · {sum(len(v['kareler']) for v in k['veri'].values())} kare", flush=True)


def esle():
    sys.path.insert(0, str(ANA / "tools" / "jev"))
    for ad, cache in (("m42", ANA_CACHE), ("m3b2", CACHE3), ("kare", CACHE3)):
        kos = B / ad
        if (kos / "esle.json").is_file() or not (kos / "sonnet" / "rapor").is_dir():
            continue
        o3.KOS, o3.KOLLAR, o3.CACHE = kos, {"sonnet": (None, [])}, cache
        o3.esle()
        print(f"esle {ad} tamam", flush=True)


def gorsel():
    m4 = _m4()
    m4.M3B, m4.KOS = B / "m3b2", B / "m42"
    m4.gorsel()
    g1 = _j(ANA / ".kos" / "m4" / "gorsel.json")["m3b"]
    kg = _j(B / "kare" / "gorsel.json", {"g": {}, "cagri": 0, "usd": 0.0})
    lk = _j(B / "kare" / "luna.json")["veri"]
    for vid, v in _j(B / "kare" / "esle.json")["veri"].items():
        kv = v["kollar"]["sonnet"]
        if vid in kg["g"] or kv["motor"] is None:
            continue
        paket = (CACHE3 / vid / "paket.md").read_text(encoding="utf-8")
        kal = {m["metin"]: m["zaman"] for j, x in (kv.get("k3") or {}).items()
               if o3.k3_duzelt(m := kv["motor"][int(j)], x, paket) == "kare-doğrulanamadı" and m["metin"] not in g1.get(vid, {})}
        h = dict(g1.get(vid, {}))
        if kal:
            if kg["cagri"] >= KG_TAVAN[0] or kg["usd"] >= KG_TAVAN[1] - .02:
                print(f"gorsel kare {vid}: tavan {KG_TAVAN} — ölçülemedi", flush=True)
                continue
            kz = [(Path(p), t) for p, t in lk.get(vid, {}).get("kareler", [])]
            sec = sorted({min(kz, key=lambda k: abs(k[1] - z))[0] for z in kal.values() if z is not None})[:8] if kz else []
            ad = list(kal)[:40]
            et, usd = m4.gorsel_yargi(ad, sec, hafif.cagir, butce=min(.08, KG_TAVAN[1] - kg["usd"]), env=dict(os.environ))
            h.update(zip(ad, et))
            kg["cagri"], kg["usd"] = kg["cagri"] + 1, kg["usd"] + usd
            print(f"gorsel kare {vid}: {len(ad)} kalem · {len(sec)} kare · {dict((e, et.count(e)) for e in set(et))} · ${usd:.3f}", flush=True)
        kg["g"][vid] = h
        _jy(B / "kare" / "gorsel.json", kg)


def _kat(m):
    out = {}
    for (kat, _), t in m["kirilim"].items():
        o = out.setdefault(kat, [0, 0])
        o[0], o[1] = o[0] + t[0], o[1] + t[1]
    return {k: tuple(v) for k, v in out.items()}


def _isabet(veri):
    """(vid, altın i) → True/False; motor yoksa video ölçülemedi (None)."""
    out = {}
    for vid, v in veri.items():
        kv = v["kollar"]["sonnet"]
        es = {int(i) for i in kv["det"]} | {int(i) for i in kv.get("jev", {})}
        for i in range(len(v["altin"])):
            out[(vid, i)] = None if kv["motor"] is None else i in es
    return out


def _yakin(t, xs):
    return min(xs, key=lambda x: abs(x - t)) if xs and t is not None else None


def rapor():
    m4 = _m4()
    g4, g42, kg = _j(ANA / ".kos" / "m4" / "gorsel.json"), _j(B / "m42" / "gorsel.json"), _j(B / "kare" / "gorsel.json")
    lk = _j(B / "kare" / "luna.json")
    t3 = _toplam(_j(ANA / ".kos" / "m3b" / "tara.json"))
    KOSU = {"m3b-1": (ANA / ".kos" / "m3b", g4["m3b"], "paket-m3b.md", ANA_CACHE, t3),
            "m3b-2": (B / "m3b2", g42["m3b"], "paket.md", CACHE3, _toplam(_j(B / "m3b2" / "tara.json"))),
            "m4-1": (ANA / ".kos" / "m4", g4["m4"], "paket.md", ANA_CACHE, _toplam(_j(ANA / ".kos" / "m4" / "tara.json"))),
            "m4-2": (B / "m42", g42["m4"], "paket.md", ANA_CACHE, _toplam(_j(B / "m42" / "tara.json"))),
            "m3b+kare-luna": (B / "kare", kg["g"], "paket.md", CACHE3, [t3[0] + lk["cagri"] + kg["cagri"], t3[1] + lk["usd"] + kg["usd"], t3[2]])}
    oz = {}
    for ad, (kok, g, pad, cache, c) in KOSU.items():
        m4.CACHE = cache
        veri = _j(kok / "esle.json")["veri"]
        oz[ad] = {**m4.olc(veri, lambda v: "sonnet", g, pad), "c": c, "veri": veri, "is": _isabet(veri)}
    m4.CACHE = ANA_CACHE
    P, tav = o3._pct, _j(B / "tavan.json", {})
    L = ["# M4b — gürültü + kare-luna ölçümü", "",
         "Ölçütler (yüksek ≥%90 · genel ≥%75 · dayanmayan ≤%5) ve altın set değişmedi. Dört sonnet koşusu aynı eşleme (det + Jev K2/K3) ve görsel yargıçla ölçüldü.",
         "Koşu-2: aynı motor, aynı paket; m3b-2 7a550e3 worktree'sinde. Gürültü = |koşu-1 − koşu-2|; ortalama iki koşunun havuzu, ± yarı fark.", "",
         "## Koşular", "| koşu | yüksek | genel | dayanmayan | okunamıyor | ölçülemedi | düşen video | motor kalem | çağrı | $ | jeton |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {a} | {P(z['m']['yuksek'])} | {P(z['m']['genel'])} | {P(z['day'])} | {z['say']['okunamıyor']} | {z['say']['ölçülemedi']} | {z['dus']} | {z['n']} | "
          f"{z['c'][0]} | {z['c'][1]:.3f} | {z['c'][2]} |" for a, z in oz.items()]
    L += ["", "## Tavanlar (koşu-2 = koşu-1 gerçek ×1,2)"] + [f"- {k}: {json.dumps(v, ensure_ascii=False)}" for k, v in tav.items()]
    L += [f"- kare-luna: luna {lk['cagri']} çağrı ${lk['usd']:.4f} (tavan {K4_TAVAN}) · görsel yargıç {kg['cagri']} çağrı ${kg['usd']:.3f} (tavan {KG_TAVAN})"]
    L += ["", "## Gürültü ve ortalamalar (ölçütlere ortalama ile)", "| motor | metrik | koşu-1 | koşu-2 | fark (puan) | ortalama ± gürültü | ölçüt |", "|---|---|---|---|---|---|---|"]
    ort = {}
    for mo in ("m3b", "m4"):
        a, b = oz[f"{mo}-1"], oz[f"{mo}-2"]
        for mt, x, y, esik, ust in (("yüksek", a["m"]["yuksek"], b["m"]["yuksek"], .9, True), ("genel", a["m"]["genel"], b["m"]["genel"], .75, True),
                                    ("dayanmayan", a["day"], b["day"], .05, False)):
            f, o, pm = gurultu(x, y)
            ort[(mo, mt)] = (o, pm, f)
            L.append(f"| {mo} | {mt} | {P(x)} | {P(y)} | {f:.1f} | %{100 * o:.1f} ± {100 * pm:.1f} | {'GEÇTİ' if (o >= esik if ust else o <= esik) else 'KALDI'} |")
    ortak = [v for v in o3.VIDEOLAR if all(any(x is not None for (w, _), x in z["is"].items() if w == v) for z in oz.values())]
    ay = lambda z, y: (sum(1 for (w, i), x in z["is"].items() if w in ortak and x and (not y or z["veri"][w]["altin"][i]["onem"] == "yüksek")),
                       sum(1 for (w, i), x in z["is"].items() if w in ortak and x is not None and (not y or z["veri"][w]["altin"][i]["onem"] == "yüksek")))
    L += ["", f"## Ortak videolar ({len(ortak)}: {', '.join(ortak)}) — eşit kıyas", "| koşu | yüksek | genel |", "|---|---|---|"]
    L += [f"| {a} | {P(ay(z, True))} | {P(ay(z, False))} |" for a, z in oz.items()]
    L += ["", "## Kategori (genel yakalama)", "| kategori | m3b-1 | m3b-2 | m4-1 | m4-2 | m3b fark | m4 fark | m4−m3b ort (puan) | kare-luna |", "|---|---|---|---|---|---|---|---|---|"]
    kk = {a: _kat(z["m"]) for a, z in oz.items()}
    for kat in sorted(kk["m3b-1"]):
        g_ = [kk[a].get(kat, (0, 0)) for a in ("m3b-1", "m3b-2", "m4-1", "m4-2")]
        f3, o3_, _ = gurultu(g_[0], g_[1])
        f4, o4, _ = gurultu(g_[2], g_[3])
        L.append(f"| {kat} | " + " | ".join(P(x) for x in g_) + f" | {f3:.0f} | {f4:.0f} | {100 * (o4 - o3_):+.0f} | {P(kk['m3b+kare-luna'].get(kat, (0, 0)))} |")
    L += ["", "## Kategori × önem (iki koşu havuzu)", "| kategori | önem | m3b | m4 | m3b+kare-luna |", "|---|---|---|---|---|"]
    kir = lambda a, k: oz[a]["m"]["kirilim"].get(k, (0, 0))
    hav = lambda a, b, k: (kir(a, k)[0] + kir(b, k)[0], kir(a, k)[1] + kir(b, k)[1])
    for k in sorted(oz["m3b-1"]["m"]["kirilim"], key=lambda k: (k[0], o3.ONEM.index(k[1]) if k[1] in o3.ONEM else 9)):
        L.append(f"| {k[0]} | {k[1]} | {P(hav('m3b-1', 'm3b-2', k))} | {P(hav('m4-1', 'm4-2', k))} | {P(kir('m3b+kare-luna', k))} |")
    L += ["", "## Video (genel)", "| video | " + " | ".join(oz) + " |", "|---|" + "---|" * len(oz)]
    for vid in o3.VIDEOLAR:
        L.append(f"| {vid} | " + " | ".join(P((sum(1 for (v, _), x in z['is'].items() if v == vid and x), sum(1 for (v, _), x in z['is'].items() if v == vid and x is not None)))
                                          for z in oz.values()) + " |")
    L += ["", "## Kaçırma sebepleri (yüksek/orta)", "| sebep | " + " | ".join(oz) + " |", "|---|" + "---|" * len(oz)]
    L += [f"| ({s}) | " + " | ".join(str(z["seb"].get(s, 0)) for z in oz.values()) + " |" for s in "abcd"]
    # kare-luna eki: yakalanan ek altın kalem + eklenen kalemlerin dayanaklığı
    z, b = oz["m3b+kare-luna"], oz["m3b-1"]
    ek = dict.fromkeys(("eşleşti", "dayanıyor", "dayanmıyor", "okunamıyor", "kare-doğrulanamadı", "ölçülemedi"), 0)
    for vid, v in z["veri"].items():
        kv = v["kollar"]["sonnet"]
        if kv["motor"] is None:
            continue
        es = set(kv["det"].values()) | set(kv.get("jev", {}).values())
        paket = (CACHE3 / vid / "paket.md").read_text(encoding="utf-8")
        for j, m in enumerate(kv["motor"]):
            if not m["bolum"].endswith("(kare-luna)"):
                continue
            if j in es:
                ek["eşleşti"] += 1
                continue
            x = o3.k3_duzelt(m, (kv.get("k3") or {}).get(str(j), "ölçülemedi"), paket)
            ek[kg["g"].get(vid, {}).get(m["metin"], "ölçülemedi") if x == "kare-doğrulanamadı" else x] += 1
    yeni = sum(1 for k, x in z["is"].items() if x and not b["is"].get(k))
    kay = sum(1 for k, x in z["is"].items() if b["is"].get(k) and x is False)
    L += ["", "## K4 — m3b+kare-luna (sonnet-m3b koşu-1 + luna kare okuma)",
          f"- eklenen kalem {sum(ek.values())}: {ek}",
          f"- altın isabet: +{yeni} yeni yakalanan · −{kay} (eşleme gürültüsüyle kaybolan) · yüksek {P(b['m']['yuksek'])} → {P(z['m']['yuksek'])} · genel {P(b['m']['genel'])} → {P(z['m']['genel'])} · "
          f"dayanmayan {P(b['day'])} → {P(z['day'])}",
          f"- ek maliyet: luna ${lk['usd']:.4f} + görsel yargıç ${kg['usd']:.3f} (sonnet-m3b koşu-1 ${t3[1]:.3f} üstüne %{100 * (lk['usd'] + kg['usd']) / (t3[1] or 1):.0f})"]
    c3 = [(oz["m3b-1"]["c"][i] + oz["m3b-2"]["c"][i]) / 2 for i in range(3)]
    c4 = [(oz["m4-1"]["c"][i] + oz["m4-2"]["c"][i]) / 2 for i in range(3)]
    gd = ort[("m4", "genel")][0] - ort[("m3b", "genel")][0]
    L += ["", "## Kural 21 takası (iki koşu ortalaması)",
          f"- m4 / m3b: çağrı {c3[0]:.1f} → {c4[0]:.1f} · $ {c3[1]:.3f} → {c4[1]:.3f} (%{100 * (c4[1] / (c3[1] or 1) - 1):+.0f}) · jeton {c3[2]:.0f} → {c4[2]:.0f} "
          f"(%{100 * (c4[2] / (c3[2] or 1) - 1):+.0f}) · genel {100 * gd:+.1f} puan (gürültü m3b ±{100 * ort[('m3b', 'genel')][1]:.1f}, m4 ±{100 * ort[('m4', 'genel')][1]:.1f})",
          "", "## M4 özellik önerileri", "(aşağıda elle; dayanak yukarıdaki tablolar)"]
    (ANA / "docs" / "olcumler" / "m4b-olcum.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    # K3 kalem düzeyi
    ad4 = ("m3b-1", "m3b-2", "m4-1", "m4-2")
    K = ["# M4b — kalem düzeyi analiz (yüksek önem, 4 sonnet koşusu)", "",
         "Durum: hep kaçtı (gerçek) · bazen (gürültü) · hep yakaladı; ölçülemeyen koşu sayılmaz. Kök neden `olcum_m3b.sebep`: (a) kaynak motora gitmedi · (b) formda yeri yok · (c) model atladı · (d) panel düşürdü.", ""]
    sat, sinif = [], {}
    for vid, v in oz["m4-1"]["veri"].items():
        p3, p4 = (ANA_CACHE / vid / "paket-m3b.md").read_text(encoding="utf-8"), (ANA_CACHE / vid / "paket.md").read_text(encoding="utf-8")
        kz = {n: [t for t in pt.paket_oku(ANA_CACHE / vid / f)["kare_zaman"] if t is not None] for n, f in (("m3b", "paket-m3b.md"), ("m4", "paket.md"))}
        sg = {n: [o3.sn(x) for x in re.findall(r"^\[(\d+:\d\d(?::\d\d)?)\]", p, re.M)] for n, p in (("m3b", p3), ("m4", p4))}
        for i, a in enumerate(v["altin"]):
            if a["onem"] != "yüksek":
                continue
            xs = [oz[k]["is"].get((vid, i)) for k in ad4]
            if all(x is not False for x in xs):
                continue
            s = durum_sinifi(xs)
            sinif[s] = sinif.get(s, 0) + 1
            if s != "hep kaçtı":
                sat.append(f"| {s} | {vid} | {a['ad'][:60]} | " + " ".join("✓" if x else "✗" if x is False else "–" for x in xs) + " | | |")
                continue
            t = a["zaman"]
            ac = [f"altın {_ss(t)}" if t is not None else "zamansız (açıklama/kaynak)"] + [
                f"{n}: kare {_ss(k)} (Δ{abs(k - t):.0f}s) · segment {_ss(g)} (Δ{abs(g - t):.0f}s)" for n in ("m3b", "m4")
                if t is not None and (k := _yakin(t, kz[n])) is not None and (g := _yakin(t, sg[n])) is not None]
            sat.append(f"| hep kaçtı | {vid} | {a['ad'][:60]} | ✗✗✗✗ | {o3.sebep(a, p3)}/{o3.sebep(a, p4)} | {' · '.join(ac)} · formda: {a['kat']} |")
    kok = {}
    for s in sat:
        if s.startswith("| hep kaçtı"):
            for x in s.split(" | ")[4].split("/"):
                kok[x] = kok.get(x, 0) + 1
    K += [f"Özet: {sinif} · gerçek kaçırmaların kök nedeni (m3b/m4 paketi, toplam): {kok}", "",
          "| durum | video | kalem | m3b-1 m3b-2 m4-1 m4-2 | kök (m3b/m4) | açıklama |", "|---|---|---|---|---|---|"]
    K += sorted(sat, key=lambda s: (not s.startswith("| hep"), s))
    (ANA / "docs" / "olcumler" / "m4b-kalem-analizi.md").write_text("\n".join(K) + "\n", encoding="utf-8")
    print("yazıldı: docs/olcumler/m4b-olcum.md · m4b-kalem-analizi.md", flush=True)
    for a, z in oz.items():
        print(f"{a}: yüksek {P(z['m']['yuksek'])} · genel {P(z['m']['genel'])} · dayanmayan {P(z['day'])} · seb {z['seb']} · ${z['c'][1]:.3f}", flush=True)
    print(f"ortalama±gürültü: { {f'{k[0]}-{k[1]}': f'%{100 * o:.1f}±{100 * pm:.1f} (fark {f:.1f})' for k, (o, pm, f) in ort.items()} }", flush=True)
    print(f"kalem: {sinif} · kök {kok} · kare-luna ek {ek} · +{yeni}/−{kay}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    ADIM = {"k1": k1, "m42": m42, "m3b2": m3b2, "kare": kare, "esle": esle, "gorsel": gorsel, "rapor": rapor}
    for a in sys.argv[1:]:
        ADIM[a]()
