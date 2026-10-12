"""BLENDER-1 Faz 5: taban (headless Blender + resmi Blender MCP) ↔ tarif yolu ölçümü. Yalnız ortak sırayla:
    python C:\\Projeler\\omer-skills\\.kos\\kopru\\arka.py <log> C:\\Projeler\\omer-skills\\.kos\\kopru\\olcum_sira.py <bu betik>
        [--tekrar 2] [--gorev g1,g2,g3,g4] [--yol taban,tarif] [--yargi]
Koşu başına `claude -p` (stream-json → jeton/tur/$/süre) + headless nesnel denetim (blender_denetim.py); TSV'de olan koşu atlanır.
--yargi: görev başına önizlemelerin kör karşılaştırması (sonnet, A/B/C/D rastgele, dosya adları gizli).
Çıktı docs/kutuphane/olcum/blender-faz5.tsv · blender-faz5-yargi.json · koşu klasörü Desktop\\BlenderOlcum\\blender\\<gorev>-<yol>-<n>\\
"""
import argparse
import json
import math
import random
import re
import shutil
import struct
import subprocess
import sys
import time
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
KOK = DIZIN.parents[1]
sys.path[:0] = [str(DIZIN), str(KOK / "tools"), str(KOK / "tools" / "blender")]
import blender_cli as bc  # noqa: E402
import yalin  # noqa: E402
import blender_oturum as bo  # noqa: E402
import kosucu  # noqa: E402

PROJE = bo.MASAUSTU / "BlenderOlcum" / "blender"
TSV = kosucu.CIKTI / "blender-faz5.tsv"
YARGI = kosucu.CIKTI / "blender-faz5-yargi.json"
DENETIM = DIZIN / "blender_denetim.py"
TARIF = KOK / "tools" / "blender" / "lib" / "tarif.py"
MODEL, TAVAN_USD = "sonnet", 22.0  # bütçe ≤ $30 (yargı ≤ $4 dahil): tavan aşılınca yeni koşu başlamaz
BUTCE = {"taban": 4.0, "tarif": 1.5, "tek": 0.5}
IZIN = ["--allowedTools", "Bash", "Read", "Write", "Edit", "Glob", "Grep", "mcp__blender"]
BASLIK = "gorev\tyol\ttekrar\tinput\tcache_creation\tcache_read\toutput\ttoplam\ttur\tsure_sn\tusd\tkalite\tkalan\tmcp_n\tbash_n\thata"

GOREV = {
    "g1": (None, "Ürün sahnesi kur: GEO-Fincan (silindir, çap 8 cm, yükseklik 9 cm, parlak beyaz sırlı seramik), GEO-Tabak (çap 14 cm, "
                 "kalınlık 1 cm, aynı seramik, fincanın altında), GEO-Zemin (1×1 m düzlem, açık gri mat). Üç nokta stüdyo ışığı + world "
                 "dolgu; kamera ürünü kadraja alsın. Kaydet: {d}\\sahne.blend; 384 px EEVEE önizleme render: {d}\\onizleme.png."),
    "g2": ("baslangic", "Sahnedeki GEO-Fincan'ı düzenle: 2 mm bevel, subdivision seviye 1, akıllı UV aç, parlak beyaz sırlı seramik "
                        "malzeme ata. Kaydet: {d}\\sahne.blend; 384 px EEVEE önizleme: {d}\\onizleme.png. Sonda GEO-Fincan'ın üçgen ve "
                        "UV katmanı sayısını yaz."),
    "g3": ("baslangic", "Sahnedeki GEO-Fincan kare 1'den 24'e Z ekseninde 360° dönsün; sahne kare aralığı 1–24. Kare 1, 7, 13, 19 için "
                        "256 px EEVEE render al → {d}\\kareler\\ klasörüne PNG. Kaydet: {d}\\sahne.blend; 384 px önizleme (kare 1): "
                        "{d}\\onizleme.png."),
    "g4": (None, "TELVE için patlatılmış görünüm Türk kahvesi makinesi: en az 5 parça (ör. GEO-Taban, GEO-Govde, GEO-Hazne, GEO-Cezve, "
                 "GEO-Kapak), Z ekseninde alttan üste dizili, parçalar arası en az 5 cm boşluk; düşük poli (toplam < 5000 üçgen); her "
                 "parçaya malzeme (gövde koyu, kapak/cezve pirinç gibi). Kaydet: {d}\\sahne.blend; GLB: {d}\\telve.glb; 384 px EEVEE "
                 "önizleme: {d}\\onizleme.png."),
}
YOL = {
    "taban": "Blender headless açık; resmi Blender MCP sunucusu 127.0.0.1:9876'da bağlı ({sahne}). İşi yalnız blender MCP araçlarıyla "
             "yap; blender_cli.py ve tarif.py kullanma, Blender'ı açıp kapatma.",
    "tarif": "{blend}",  # devam-3: blender-oturum'un devrettiği yalın oturum (yalin.bayraklar) — sistem istemi tarifi taşır
}


def glb_mesh(yol):
    """GLB 2.0 başlığı + JSON parçası geçerliyse mesh sayısı, değilse 0."""
    try:
        b = Path(yol).read_bytes()
        sihir, surum, _ = struct.unpack_from("<4sII", b)
        n, tur = struct.unpack_from("<I4s", b, 12)
        return len(json.loads(b[20:20 + n]).get("meshes", [])) if (sihir, surum, tur) == (b"glTF", 2, b"JSON") else 0
    except (OSError, struct.error, ValueError):
        return 0


def kontrol(g, d, den, baz_ucgen=124):
    """Görev başına nesnel kontroller: [(ad, geçti)]."""
    m = {x["ad"]: x for x in den.get("mesh", [])}
    f = m.get("GEO-Fincan")
    k = [("render_dolu", bool(den.get("png")) and all(v > 0.02 for v in den["png"].values())),
         ("malzeme_hepsi", bool(m) and all(x["malzeme"] for x in m.values()))]
    if g == "g1":
        k += [("fincan_olcu", bool(f) and all(abs(a - b) <= 0.15 * b for a, b in zip(f["boyut"], (0.08, 0.08, 0.09)))),
              ("nesne_3", len(m) >= 3), ("isik_3", den.get("isik", 0) >= 3), ("kamera", bool(den.get("kamera")))]
    elif g == "g2":
        k += [("uv", bool(f) and f["uv"] >= 1), ("subdiv", bool(f) and f["ucgen"] > 2 * baz_ucgen)]
    elif g == "g3":
        kare = list((Path(d) / "kareler").glob("*.png"))
        k += [("kareler_4", len(kare) >= 4), ("kare_1_24", den.get("kare") == [1, 24]),
              ("donus_360", bool(f) and abs(abs(f["rz"][1] - f["rz"][0]) - 2 * math.pi) < 0.2)]
    else:
        z = sorted(x["z"] for x in m.values())
        k += [("glb", glb_mesh(Path(d) / "telve.glb") >= 5), ("parca_5", len(m) >= 5),
              ("patlatma_aralik", len(z) >= 2 and all(b[0] - a[1] >= 0.04 for a, b in zip(z, z[1:]))),
              ("dusuk_poli", 0 < sum(x["ucgen"] for x in m.values()) < 5000)]
    return k


def denetle(d):
    if not (d / "sahne.blend").is_file():
        return {"mesh": [], "png": {}, "isik": 0, "kamera": False}
    _, s, _ = bc.calistir(DENETIM, {"png": [str(d / "onizleme.png")]}, d / "sahne.blend", zaman_asimi=180)
    return s or {"mesh": [], "png": {}, "isik": 0, "kamera": False}


def mcp_ac(blend):
    if bo.dinleyenler():
        raise RuntimeError("9876 dolu: başka oturum Blender'ı sürüyor")
    p = subprocess.Popen([bo.BLENDER, "-b", str(blend), "--command", "blender_mcp"], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, creationflags=kosucu.PENCERESIZ)
    for _ in range(60):
        time.sleep(1)
        if any(pid == p.pid for _, pid in bo.dinleyenler()):
            return p
    kapat(p)
    raise RuntimeError("headless MCP 60 sn içinde dinlemedi")


def kapat(p):
    subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)  # yalnız kendi başlattığımız PID


def satirlar():
    if not TSV.is_file():
        return []
    s = TSV.read_text(encoding="utf-8").splitlines()
    return [dict(zip(s[0].split("\t"), x.split("\t"))) for x in s[1:]]


def hazirla():
    PROJE.mkdir(parents=True, exist_ok=True)
    baz = {"bos": PROJE / "_bos.blend", "baslangic": PROJE / "_baslangic.blend"}
    if not baz["bos"].is_file():
        bc.calistir(TARIF, {"kaydet": str(baz["bos"])})
    if not baz["baslangic"].is_file():
        bc.calistir(TARIF, {"nesneler": [{"ad": "GEO-Fincan", "tur": "silindir", "boyut": [0.08, 0.08, 0.09], "konum": [0, 0, 0.045]}],
                            "kaydet": str(baz["baslangic"])})
    baz["ucgen"] = sum(x["ucgen"] for x in denetle_dosya(baz["baslangic"]).get("mesh", []))
    return baz


def denetle_dosya(blend):
    return bc.calistir(DENETIM, {}, blend, zaman_asimi=180)[1] or {}


def kos_bir(g, yol, t, baz):
    d = PROJE / f"{g}-{yol}-{t}"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    kaynak, istem = GOREV[g]
    blend = None
    if kaynak:
        blend = d / "baslangic.blend"
        shutil.copy(baz["baslangic"], blend)
    p = None
    if yol == "taban":
        p = mcp_ac(blend or baz["bos"])
        ek = YOL["taban"].format(sahne=f"açık dosya: {blend}" if blend else "boş sahne")
    else:
        ek = YOL["tarif"].format(blend=f"Başlangıç sahnesi: --blend {blend}" if blend else "")
    try:
        if yol == "tek":  # BLENDER-2: araçsız tek tur, Blender'ı yalin koşar
            o = yalin.tek(istem.format(d=d), blend, kos=lambda i, e: kosucu.kos(i, ek=e, model=MODEL, timeout=1500, butce=BUTCE[yol]))
        else:
            o = kosucu.kos(istem.format(d=d) + "\n\n" + ek, ek=IZIN if yol == "taban" else yalin.bayraklar(), model=MODEL,
                           timeout=1500, butce=BUTCE[yol])
    finally:
        if p:
            kapat(p)
    den = denetle(d)
    k = kontrol(g, d, den, baz["ucgen"])
    (d / "sonuc.json").write_text(json.dumps({"o": {x: o.get(x) for x in ("metin", "araclar", "usage", "tur", "usd", "sure", "rc", "hata")},
                                              "denetim": den, "kontrol": k}, ensure_ascii=False, indent=1), encoding="utf-8")
    j = kosucu.jeton(o["usage"])
    return [g, yol, t, *j, sum(j), o["tur"], o["sure"], round(o["usd"], 4), round(sum(v for _, v in k) / len(k), 3),
            ",".join(a for a, v in k if not v) or "-", sum(a.startswith("mcp__") for a in o["araclar"]),
            sum(a == "Bash" for a in o["araclar"]), o["hata"] or "-"]


def yargi():
    sonuc = json.loads(YARGI.read_text(encoding="utf-8")) if YARGI.is_file() else {}
    for g, (_, istem) in GOREV.items():
        aday = [f"{yol}-{t}" for yol in ("taban", "tarif", "tek") for t in (1, 2) if (PROJE / f"{g}-{yol}-{t}" / "onizleme.png").is_file()]
        if g in sonuc or len(aday) < 2:
            continue
        random.shuffle(aday)
        kor = PROJE / "_yargi" / g
        shutil.rmtree(kor, ignore_errors=True)
        kor.mkdir(parents=True)
        harf = "ABCD"[:len(aday)]
        for h, a in zip(harf, aday):
            shutil.copy(PROJE / f"{g}-{a}" / "onizleme.png", kor / f"{h}.png")
        soru = (f"Kör karşılaştırma. İstek: {istem.format(d='<klasör>')}\nGörseller (Read ile aç): "
                + "; ".join(f"{h}={kor / (h + '.png')}" for h in harf)
                + "\nHer görsele 4 ölçütte 1-10 puan ver: bicim (biçim doğruluğu), isik (malzeme/ışık), kompozisyon, uyum (istek uyumu). "
                  'Yalnız tek satır JSON yaz: {"A": {"bicim": 0, "isik": 0, "kompozisyon": 0, "uyum": 0}, ...}')
        o = kosucu.kos(soru, ek=["--allowedTools", "Read"], model="sonnet", timeout=600, butce=1.0)
        m = re.search(r"\{.*\}", o["metin"], re.S)
        sonuc[g] = {"esle": dict(zip(harf, aday)), "puan": json.loads(m.group(0)) if m else o["metin"][-300:], "usd": o["usd"]}
        YARGI.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
        print("yargı", g, sonuc[g]["esle"], flush=True)


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--tekrar", type=int, default=2)
    a.add_argument("--gorev", default=",".join(GOREV))
    a.add_argument("--yol", default="taban,tarif")
    a.add_argument("--yargi", action="store_true")
    a = a.parse_args(argv)
    baz = hazirla()
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
                    s = kos_bir(g, yol, t, baz)
                except RuntimeError as ex:
                    s = [g, yol, t, *[0] * 12, str(ex)]
                with TSV.open("a", encoding="utf-8") as f:
                    f.write("\t".join(map(str, s)) + "\n")
                print("\t".join(map(str, s)), flush=True)
    if a.yargi:
        yargi()
    return 0


if __name__ == "__main__":
    sys.exit(main())
