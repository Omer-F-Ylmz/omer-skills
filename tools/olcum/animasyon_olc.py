"""ANİMASYON-1 ölçümü: taban (kurulu animasyon skill'leri) ↔ yeni (+ animasyon-atolyesi) — 4 görev × 2 yol × 2 tekrar = 16 `claude -p`.
    python C:\\Projeler\\omer-skills\\.kos\\kopru\\arka.py <log> C:\\Projeler\\omer-skills\\.kos\\kopru\\olcum_sira.py <bu betik>
        [--tekrar 2] [--gorev w1,w2,b1,v1] [--yol taban,yeni] [--yargi-hazirla]
Yeni yol: koşu klasörüne .claude/skills/animasyon-atolyesi kopyalanır (proje skill'i); istem iki yolda aynı. TSV'de olan koşu atlanır.
Nesnel kalite: skills/animasyon-atolyesi/olc.py (headless). --yargi-hazirla: görev başına önizlemeleri kör harflerle _yargi/ altına
kopyalar (yargıyı claude -p değil oturumdaki alt ajan yapar → 16 çağrı tavanı korunur).
Çıktı docs/kutuphane/olcum/animasyon-1.tsv · koşu klasörü ~/AnimasyonOlcum/<gorev>-<yol>-<n>/
"""
import argparse
import json
import random
import shutil
import sys
import time
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
KOK = DIZIN.parents[1]
SKILL = KOK / "skills" / "animasyon-atolyesi"
sys.path[:0] = [str(DIZIN), str(SKILL)]
import kosucu  # noqa: E402
import olc  # noqa: E402

PROJE = Path.home() / "AnimasyonOlcum"
TSV = kosucu.CIKTI / "animasyon-1.tsv"
MODEL, BUTCE, TAVAN_USD = "sonnet", 0.5, 7.5  # Σ$8: tavan aşılınca yeni koşu başlamaz
IZIN = ["--allowedTools", "Bash", "Read", "Write", "Edit", "Glob", "Grep", "Skill"]
BASLIK = "gorev\tyol\ttekrar\tinput\tcache_creation\tcache_read\toutput\ttoplam\ttur\tsure_sn\tusd\tkalite\tkalan\tskill\thata"
PENCERE = " Pencere/tarayıcı açma (start, os.startfile yok); her şey arka planda."
YONLENDIR = "Animasyon/efekt işinde (giriş, scroll, sayfa geçişi, parçacık, 3D exploded, intro video) önce `animasyon-atolyesi` skill'i: tarifi kopyala-uyarla, olc.py ile ölç.\n"

GOREV = {
    "w1": ("index.html", "TELVE kahve markası için tek dosya landing yaz: {d}\\index.html. Hero (başlık 'Telve', alt başlık, CTA) kademeli "
                         "giriş animasyonuyla gelsin; altında 3 bölüm (Kavrum, Öğütüm, Pişirim) scroll'la belirsin; üstte scroll "
                         "ilerleme çubuğu. Hareket erişilebilir ve 60 fps dostu olsun."),
    "w2": ("index.html", "Tek dosya HTML yaz: {d}\\index.html — Three.js ile ~15k parçacıklı, sıcak kahve tonlarında buhar/toz "
                         "benzeri hero arka planı, üstünde 'Telve' başlığı; fareyle etkileşim; mobil ve performans dostu."),
    "b1": ("telve_anim.glb", "Blender'ı yalnız arka planda (-b) kullanarak TELVE Türk kahvesi makinesinin patlatılmış görünüm "
                             "ANİMASYONUNU yap: en az 5 parça (GEO- önekli), kare 1'de birleşik, sonra Z ekseninde yumuşak easing'le "
                             "ayrılsın; kamera yavaş yörünge yapsın. 4 kare PNG render → {d}\\kareler\\, animasyonlu GLB → "
                             "{d}\\telve_anim.glb, son kare önizleme → {d}\\onizleme.png. Blender: "
                             "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe"),
    "v1": ("intro.mp4", "4 saniyelik 1280x720, 30 fps intro videosu üret: {d}\\intro.mp4 — 'TELVE' başlığı ve 'Türk kahvesi atölyesi' "
                        "alt başlığı animasyonla girsin, arka plan degrade, sonda yumuşak kararma."),
}


def kalite(g, d, o):
    """Görev başına nesnel kontroller: [(ad, geçti)] + ölçüm sözlüğü."""
    m = olc.olc(d / GOREV[g][0], d / "_kare")
    if m.get("yok"):
        return [("dosya", False)], m
    if g in ("w1", "w2"):
        k = [("dolu", m["dolu"]), ("konsol_temiz", m["konsol_hata"] == 0), ("reduced_motion", m["reduced_motion"]),
             ("hareket", m["hareket"] > 0.001), ("fps", m["fps"] >= (55 if g == "w1" else 30))]
        k += [("duzen_yok", not m["duzen_animasyonu"]), ("scroll", (m["scroll_hareket"] or 0) > 0.001)] if g == "w1" else []
    elif g == "b1":
        kare = sorted((d / "kareler").glob("*.png")) if (d / "kareler").is_dir() else []
        k = [("glb", m.get("gecerli", False)), ("animasyon", m.get("animasyon", 0) >= 1), ("parca_5", m.get("mesh", 0) >= 5),
             ("kare_4", len(kare) >= 4), ("onizleme", (d / "onizleme.png").is_file() and olc.dolu(d / "onizleme.png"))]
    else:
        k = [("boyut", (m["en"], m["boy"]) == (1280, 720)), ("fps", abs(m["fps"] - 30) < 0.5), ("sure", abs(m["sure_sn"] - 4) < 0.3),
             ("dolu", m["dolu"]), ("hareket", m["hareket"] > 0.01)]
    return k, m


def kos_bir(g, yol, t):
    d = PROJE / f"{g}-{yol}-{t}"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    if yol == "yeni":
        shutil.copytree(SKILL, d / ".claude" / "skills" / "animasyon-atolyesi", ignore=shutil.ignore_patterns("__pycache__"))
        # skill listesi bütçesinde açıklama düşüyor (yalnız ad görünür, yeni0 koşusu skill'i hiç çağırmadı) → yönlendirme satırı
        (d / "CLAUDE.md").write_text(YONLENDIR, encoding="utf-8")
    o = kosucu.kos(GOREV[g][1].format(d=d) + PENCERE, ek=IZIN, cwd=str(d), model=MODEL, timeout=1500, butce=BUTCE)
    k, m = kalite(g, d, o)
    (d / "sonuc.json").write_text(json.dumps({"o": {x: o.get(x) for x in ("metin", "araclar", "usage", "tur", "usd", "sure", "rc", "hata")},
                                              "olcu": m, "kontrol": k}, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    j = kosucu.jeton(o["usage"])
    skill = ",".join(sorted({a for a in o["araclar"] if a.startswith("Skill")})) or "-"
    return [g, yol, t, *j, sum(j), o["tur"], o["sure"], round(o["usd"], 4), round(sum(v for _, v in k) / len(k), 3),
            ",".join(a for a, v in k if not v) or "-", skill, o["hata"] or "-"]


def onizleme(g, d):
    return {"w1": d / "_kare" / "h1.png", "w2": d / "_kare" / "h1.png", "b1": d / "onizleme.png", "v1": d / "_kare" / "v50.png"}[g]


def yargi_hazirla():
    esle = {}
    for g in GOREV:
        aday = [f"{yol}-{t}" for yol in ("taban", "yeni") for t in (1, 2) if onizleme(g, PROJE / f"{g}-{yol}-{t}").is_file()]
        random.shuffle(aday)
        kor = PROJE / "_yargi" / g
        shutil.rmtree(kor, ignore_errors=True)
        kor.mkdir(parents=True)
        for h, a in zip("ABCD", aday):
            shutil.copy(onizleme(g, PROJE / f"{g}-{a}"), kor / f"{h}.png")
        esle[g] = dict(zip("ABCD", aday))
    (PROJE / "_yargi" / "esle.json").write_text(json.dumps(esle, indent=1), encoding="utf-8")
    print("yargı hazır:", PROJE / "_yargi", flush=True)


def satirlar():
    lines = TSV.read_text(encoding="utf-8").splitlines() if TSV.is_file() else []
    return [dict(zip(lines[0].split("\t"), x.split("\t"))) for x in lines[1:] if x.strip()] if lines else []


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--tekrar", type=int, default=2)
    a.add_argument("--gorev", default=",".join(GOREV))
    a.add_argument("--yol", default="taban,yeni")
    a.add_argument("--yargi-hazirla", action="store_true")
    a = a.parse_args(argv)
    if a.yargi_hazirla:
        return yargi_hazirla()
    if not TSV.is_file():
        TSV.parent.mkdir(parents=True, exist_ok=True)
        TSV.write_text(BASLIK + "\n", encoding="utf-8")
    for t in range(1, a.tekrar + 1):
        for g in a.gorev.split(","):
            for yol in a.yol.split(",")[::1 if t % 2 else -1]:  # tekrar başına sıra ters: sıra etkisi dengelenir
                rows = satirlar()
                if any((r["gorev"], r["yol"], r["tekrar"]) == (g, yol, str(t)) for r in rows):
                    continue
                harcanan = sum(float(r["usd"]) for r in rows)
                if harcanan > TAVAN_USD:
                    print(f"DUR: tavan ${harcanan:.2f} > ${TAVAN_USD}", flush=True)
                    return 1
                print(time.strftime("%H:%M:%S"), g, yol, t, flush=True)
                try:
                    s = kos_bir(g, yol, t)
                except Exception as ex:  # tek koşunun çöküşü zinciri düşürmez
                    s = [g, yol, t, *[0] * 9, "-", "-", str(ex)[:150]]
                with TSV.open("a", encoding="utf-8") as f:
                    f.write("\t".join(map(str, s)) + "\n")
                print("\t".join(map(str, s)), flush=True)
    yargi_hazirla()
    return 0


if __name__ == "__main__":
    sys.exit(main())
