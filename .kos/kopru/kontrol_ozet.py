"""Desktop kontrol özeti: son kontrolden beri BAŞLAT/BİTTİ + biten işlerin ücretsiz modelle 4 satırlık özeti + RAM + kuyruk. ≤15 satır.
python kontrol_ozet.py [--sifirla-yok]   (varsayılan: kontrol-son.txt'yi şimdiye ilerletir)"""
import contextlib
import ctypes
import json
import re
import sys
import threading
import time
from pathlib import Path

import maliyet_defter  # günlük toplam + Haiku-zayıf türler (son satır)

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


def _saat(s):
    return int(s[0:2]) * 3600 + int(s[3:5]) * 60 + int(s[6:8])


def yeni_satirlar():
    """kontrol-son.txt = log BAYT ofseti; yalnız o ofsetten sonrası okunur (saat damgası gün sınırını bilmez).
    Dosya yok / ofset geçersiz / log küçülmüş: son 2 saat (geriye giderken saat artarsa gün sınırı)."""
    ham_b = LOG.read_bytes()
    boy = len(ham_b)
    try:
        ofs = int(SON.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        ofs = -1
    sat = lambda b: [s for s in b.decode("utf-8", errors="replace").splitlines() if re.match(r"\d\d:\d\d:\d\d ", s)]
    if 0 <= ofs <= boy:
        return sat(ham_b[ofs:]), boy
    satir = sat(ham_b)
    secilen = []
    for s in reversed(satir):
        if secilen and _saat(s) > _saat(secilen[0]):
            break  # gün sınırı
        if (_saat(satir[-1]) - _saat(s)) % 86400 > 7200:
            break
        secilen.insert(0, s)
    return secilen, boy


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
        with contextlib.redirect_stdout(sys.stderr):  # havuz/claude-mem gürültüsü stderr'e, özet stdout temiz
            y, _, _ = h.cagir("ozet", ISTEM + res[:6000], max_tokens=600, etiket="kontrol_ozet")
    except Exception:
        y = None
    if y:
        satir = [x.strip() for x in y.splitlines() if x.strip()]
        if len(satir) == 4 and all(n in set(SAY.findall(res)) for n in SAY.findall(y)):
            return [x[:130] for x in satir]
    return ["(ham) " + ham(res)[0]] + ham(res)[1:] if ham(res) else ["(ham) yok"]


def ozetle(adlar, sure=7):
    """Biten işlerin özetleri tek daemon iş parçacığında; toplam ≤ sure sn (≤10 sn hedefi). Yetişmeyen → zaman aşımı satırı."""
    sonuc = {}

    def calis():
        for ad in adlar:
            sonuc[ad] = ozet(ad)

    t = threading.Thread(target=calis, daemon=True)
    t.start()
    t.join(sure)
    return [sonuc.get(ad, ["(özet zaman aşımı) python sonuc_kisa.py --kisa " + ad]) for ad in adlar]


def kuyruk():
    """(runner'ın kendi canlı oturumları, dış canlı oturumlar, bekleyen). Dış = son 'başladı' satırındaki 'önceden başlamış' listesi."""
    bas = {f.stem for f in SIRA.glob("*.basladi")}
    onceki = set()
    for s in reversed(LOG.read_text(encoding="utf-8", errors="replace").splitlines()):
        if "başladı · tavan" in s:
            onceki = set(re.findall(r"'([^']+)'", s.split("önceden başlamış", 1)[-1].split("]")[0]))
            break
    cal = dis = 0
    for f in SIRA.glob("*.basladi"):
        p = f.read_text(encoding="utf-8", errors="replace").split()
        if len(p) >= 3 and p[1] == "pid" and p[2].isdigit() and canli(p[2]):
            if f.stem in onceki:
                dis += 1
            else:
                cal += 1
    bek = sum(1 for s in TSV.read_text(encoding="utf-8").splitlines() if s.strip() and not s.startswith("#") and s.split("	")[0] not in bas)
    return cal, dis, bek


def main():
    if not LOG.exists():
        print("log yok")
        return
    yeni, son = yeni_satirlar()
    biten = [s.split()[2] for s in yeni if s[9:14] == "BİTTİ"]
    basl = [s.split()[2] for s in yeni if s[9:15] == "BAŞLAT"]
    cal, dis, bek = kuyruk()
    cikti = [f"RAM %{ram()} · çalışan {cal} (+{dis} dış) · bekleyen {bek} · yeni: {len(basl)} başladı, {len(biten)} bitti (ofset {son})"]
    if basl:
        cikti.append("başladı: " + ", ".join(basl))
    kalan = SATIR - len(cikti) - 2  # 1: "+ …" satırı, 1: defter satırı
    gosterilen = biten[: max(kalan // 4, 0)] if len(biten) * 4 > kalan else biten
    for ad, o in zip(gosterilen, ozetle(gosterilen)):
        o = o[:4]
        cikti.append(f"[{ad}] {o[0]}")
        cikti += o[1:]
    if len(gosterilen) < len(biten):
        cikti.append("+ " + ", ".join(biten[len(gosterilen):]) + " (python sonuc_kisa.py --kisa <ad>)")
    top, en_pahali = maliyet_defter.gunluk(maliyet_defter.oku(), time.strftime("%Y-%m-%d"))
    zayif = ", ".join(sorted(maliyet_defter.haiku_zayif(maliyet_defter.oku()))) or "yok"
    cikti.append(f"bugün ${top:.2f} · en pahalı: " + ", ".join(f"{r['ad']} ${r['usd']:.2f}" for r in en_pahali)
                 + f" · Haiku-zayıf (7g): {zayif}")
    print("\n".join(cikti[:SATIR]), file=sys.__stdout__)  # özet stdout'ta; ozet() havuz gürültüsünü stderr'e yönlendirir
    SON.write_text(str(son), encoding="utf-8")


if __name__ == "__main__":
    main()
