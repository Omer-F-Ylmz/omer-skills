"""ARKA-OTO-1 testi: geçici dizinde sahte iş json'u + log; KABUL, DUR, belirsiz, ölü iş, tekrar bildirimi yok.
  python tools/test_arka_oto.py"""
import json
import os
import sys
import tempfile

os.environ["ARKA_OTO_TEST"] = "1"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arka_oto
import arka_sira

T = tempfile.mkdtemp(prefix="arka-oto-test-")
arka_oto.ARKA = arka_sira.ARKA = T
arka_sira.SIRA = os.path.join(T, "_sira.txt")
arka_sira.LOG = os.path.join(T, "_sira.log")


def is_(ad, sonuc, kapi=None, sonraki=None, bitti=True, kilit=False):
    j = {"gorev": "x", "cwd": T}
    if kapi:
        j["kapi"] = {"tur": kapi}
    if sonraki:
        j["sonraki"] = sonraki
    json.dump(j, open(os.path.join(T, ad + ".json"), "w", encoding="utf-8"))
    log = "BASLADI 10:00\n"
    if sonuc is not None:
        log += json.dumps({"type": "result", "result": sonuc, "total_cost_usd": 0.42}, separators=(",", ":")) + "\n"
    if bitti:
        log += "\nBITTI 10:30 kod 0\n"
    open(os.path.join(T, ad + ".log"), "w", encoding="utf-8").write(log)
    if kilit:
        open(os.path.join(T, ad + ".kilit"), "w").write("99999999")


def havuz(v):
    arka_oto.havuz_karar = lambda k, m: v


ok = []
def kontrol(ad, kosul):
    ok.append(bool(kosul)); print(("OK  " if kosul else "FAIL"), ad)


is_("a-kabul", "Bitti. hakem %92, commit abc1234f.", "hakem >= %87", ["ikinci yon"])
is_("b-dur", "hakem %60 commit deadbee1", "hakem >= %87", ["x"])
is_("c-belirsiz", "hakem %95 commit 1234abcd", "hakem >= %87", ["x"])
is_("d-olu", None, kilit=True, bitti=False)
is_("e-sayisiz", "sayi yok", "hakem >= %87")
arka_oto.havuz_karar = lambda kp, m: "DUR" if ("%60" in m or "1234abcd" in m) else "KABUL"
arka_oto.tara(canli=[])
kontrol("ilk kosu taban cizgisi: olay/kuyruk yok", not arka_sira.kuyruk() and not arka_oto.SIZINTI)
os.remove(os.path.join(T, "_oto.json")) if False else None
d0 = arka_oto._durum(); d0["islenen"] = {}; d0["yeniden"] = {}; arka_oto._yaz(d0)
arka_oto.tara(canli=[])
d = arka_oto._durum()
oz = open(os.path.join(T, "gece-ozeti.md"), encoding="utf-8").read()
k = arka_sira.kuyruk()
kontrol("KABUL: kuyruga girdi + yon yazildi", "a-kabul" in k and json.load(open(os.path.join(T, "a-kabul.json"), encoding="utf-8"))["devam_notu"] == "ikinci yon")
kontrol("DUR: regex+havuz DUR -> karar-bekliyor, kuyrukta yok", "b-dur" in d["karar"] and "b-dur" not in k)
kontrol("belirsiz: regex KABUL havuz DUR -> cakisma, kuyrukta yok", "c-belirsiz" in d["karar"] and "c-belirsiz" not in k)
kontrol("kapi sayisiz: regex None -> karar-bekliyor", "e-sayisiz" in d["karar"])
kontrol("olu: bir kez yeniden kuyruk", "d-olu" in k and d["yeniden"]["d-olu"] == 1)
kontrol("gece-ozeti 5 satir, maliyet+commit", len(oz.strip().splitlines()) == 5 and "$0.42" in oz and "abc1234f" in oz)
n = len(arka_oto.SIZINTI)
arka_oto.tara(canli=[])
kontrol("ayni olay tekrar bildirilmez / islenmez", len(arka_oto.SIZINTI) == n and len(open(os.path.join(T, "gece-ozeti.md"), encoding="utf-8").read().strip().splitlines()) == 5)
havuz(None)
is_("f-havuzyok", "hakem %99 commit 1a2b3c4d", "hakem >= %87")
arka_oto.tara(canli=[])
kontrol("havuz basarisiz -> yalniz regex + karar-bekliyor", "f-havuzyok" in arka_oto._durum()["karar"])
# olu is ikinci kez: yeniden kuyruk yok
is_("d-olu", None, kilit=True, bitti=False)
os.utime(os.path.join(T, "d-olu.log"), (1, 2))
arka_oto.tara(canli=[])
kontrol("olu ikinci kez kuyruga alinmaz", arka_oto._durum()["yeniden"]["d-olu"] == 1)
ds = open(os.path.join(T, "_desktop.md"), encoding="utf-8").read()
kontrol("_desktop.md <=40 satir ve karar bekleyen listeli", len(ds.splitlines()) <= 40 and "b-dur" in ds)
# arka_sira mevcut davranisi
arka_sira.yaz_kuyruk([])
arka_sira.tur()
kontrol("arka_sira.tur bos kuyrukta calisir (oto cagrisi dahil)", True)
print("SONUC", sum(ok), "/", len(ok))
sys.exit(0 if all(ok) else 1)
