"""Desktop kontrol özeti: son kontrolden beri BAŞLAT/BİTTİ + biten işlerin ücretsiz modelle 4 satırlık özeti + RAM + kuyruk. ≤15 satır.
python kontrol_ozet.py [--sifirla-yok]   (varsayılan: kontrol-son.txt'yi şimdiye ilerletir)"""
import ctypes
import json
import re
import sys
from pathlib import Path

K = Path(__file__).resolve().parent
sys.path.insert(0, str(K.parents[1] / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
LOG, SIRA, SON, TSV = K / "ajan-sira.log", K / "ajan-sira", K / "kontrol-son.txt", K / "ajan-sira.tsv"
SATIR = 15
SAY = re.compile(r"\d+")
SOZ = re.compile(r"commit|test|kapı|★|sapma|geçti|kırmızı|passed|failed", re.I)
ISTEM = """Aşağıdaki ajan çıktısını TAM 4 satırda özetle, Türkçe, yalnız olgu, her satır ≤110 karakter, başka metin yok:
commit: <hash/mesaj veya yok>
test: <geçen/toplam sayılar>; kapı: <sonuç>
★: <sonraki taslak veya yok>
sapma: <sapma veya yok>
Sayıları kaynaktan birebir al, uydurma; kaynakta yoksa 'yok' yaz.

ÇIKTI:
"""


def ram():
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in "abcdefg"]
    m = M()
    m.l = ctypes.sizeof(M)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.yuk


def canli(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
    if not h:
        return False
    kod = ctypes.c_ulong()
    ok = ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(kod))
    ctypes.windll.kernel32.CloseHandle(h)
    return bool(ok) and kod.value == 259


def yeni_satirlar():
    satir = [s for s in LOG.read_text(encoding="utf-8", errors="replace").splitlines() if re.match(r"\d\d:\d\d:\d\d ", s)]
    son = SON.read_text(encoding="utf-8").strip() if SON.exists() else ""
    if not satir:
        return [], son
    if not son:
        return satir[-10:], satir[-1][:8]  # ilk koşu: son 10 olay
    d = 0  # gün dönümü: damga log sonundan büyükse son geriye sarımdan beri
    if son > satir[-1][:8]:
        d = max((i for i in range(1, len(satir)) if satir[i][:8] < satir[i - 1][:8]), default=0)
        return satir[d:], satir[-1][:8]
    return [s for s in satir if s[:8] > son], satir[-1][:8]


def ham(res):
    """Özet güvenilmezse: sonuçtan anahtar sözcüklü ilk 4 satır, ham."""
    s = [x.strip()[:150] for x in res.splitlines() if x.strip() and SOZ.search(x)]
    return (s or [x.strip()[:150] for x in res.splitlines() if x.strip()])[:4]


def ozet(ad):
    try:
        res = json.load(open(SIRA / f"{ad}.json", encoding="utf-8")).get("result") or ""
    except (OSError, ValueError):
        return ["json okunamadı/yok"]
    if not res.strip():
        return ["sonuç boş"]
    try:
        import ucretsiz_havuz as h
        y, _, _ = h.cagir("ozet", ISTEM + res[:6000], max_tokens=600, etiket="kontrol_ozet")
    except Exception:
        y = None
    if y:
        satir = [x.strip() for x in y.splitlines() if x.strip()]
        if len(satir) == 4 and all(n in set(SAY.findall(res)) for n in SAY.findall(y)):
            return [x[:130] for x in satir]
    return ["(ham) " + ham(res)[0]] + ham(res)[1:] if ham(res) else ["(ham) yok"]


def kuyruk():
    bas = {f.stem for f in SIRA.glob("*.basladi")}
    cal = 0
    for f in SIRA.glob("*.basladi"):
        p = f.read_text(encoding="utf-8", errors="replace").split()
        cal += len(p) >= 3 and p[1] == "pid" and p[2].isdigit() and canli(p[2])
    bek = sum(1 for s in TSV.read_text(encoding="utf-8").splitlines() if s.strip() and not s.startswith("#") and s.split("\t")[0] not in bas)
    return cal, bek


def main():
    yeni, son = yeni_satirlar()
    biten = [s.split()[2] for s in yeni if s[9:14] == "BİTTİ"]
    basl = [s.split()[2] for s in yeni if s[9:15] == "BAŞLAT"]
    cal, bek = kuyruk()
    cikti = [f"RAM %{ram()} · çalışan {cal} · bekleyen {bek} · yeni: {len(basl)} başladı, {len(biten)} bitti (son {son or '-'})"]
    if basl:
        cikti.append("başladı: " + ", ".join(basl))
    kalan = SATIR - len(cikti)
    gosterilen = biten[: max(kalan // 4, 0)] if len(biten) * 4 > kalan else biten
    for ad in gosterilen:
        o = ozet(ad)[:4]
        cikti.append(f"[{ad}] {o[0]}")
        cikti += o[1:]
    if len(gosterilen) < len(biten):
        cikti.append("+ " + ", ".join(biten[len(gosterilen):]) + " (python sonuc_kisa.py --kisa <ad>)")
    print("\n".join(cikti[:SATIR]))
    if son:
        SON.write_text(son, encoding="utf-8")


main()
