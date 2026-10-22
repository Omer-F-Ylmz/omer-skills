"""DERS-DONGU-1: hatalardan ders döngüsü (Claude jetonu 0). Tek kaynak tools/dersler.jsonl {id, tur, tetik, hata, dogru, kanit, tarih, destek}.
  topla  → DUR/RED/ARAC_EKSIK/KANIT_EKSIK satırlarını kanıt yoluyla ders_aday'a yazar (betik)
  onayla [N≤10] → adayı ücretsiz havuzla {tur,tetik,hata,dogru}'ya damıtır, ekle() (kanıtsız/sırlı ders reddedilir)
  yansit → Obsidian 50-dersler/ders-dongu-<id>.md (tek_banka → ruflo ders bankası); tohum → BHS5 dersi
  getir <görev> → ≤5 ders, ≤150 jeton (enjeksiyon: ajan_sira.on_ek_kur, ucretsiz_havuz.cagir)
  olc → tools/ders_test/vakalar.json: ücretsiz modelle derssiz/dersli uygulama oranı (≤2×vaka çağrı)"""
import hashlib
import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "tools/ogrenme"))
import ders  # noqa: E402  sır süzgeci + kök eşleme (kelimeler)

DOSYA = KOK / "tools/dersler.jsonl"
ADAY = KOK / ".kos/ogrenme/ders_aday.jsonl"
OBSIDIAN = Path(r"C:\Users\pc\Desktop\Obsidian\50-dersler")
KAYNAK = [KOK / ".kos/kopru/rapor", KOK / ".kos/kopru/devir", KOK / ".kos/kopru/gorev"]
ISARET = re.compile(r"\b(DUR|RED|ARAC_EKSIK|KANIT_EKSIK)\b")
K, JETON = 5, 150


def oku(yol=None):
    yol = yol or DOSYA
    return [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines() if s.strip()] if yol.exists() else []


def _yaz(yol, kayitlar):
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_bytes("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in kayitlar).encode("utf-8"))  # CRLF'siz


def _anahtar(x):
    return set(ders.kelimeler(x["tetik"] + " " + x["hata"]))


def ekle(tur, tetik, hata, dogru, kanit):
    if not kanit.strip():
        raise ValueError("kanıtsız ders yazılmaz")
    if ders.sir_var(" ".join([tur, tetik, hata, dogru, kanit])):
        raise ValueError("ders sır/kişisel veri içeriyor")
    dersler, yeni = oku(), {"tur": tur, "tetik": tetik[:160], "hata": hata[:200], "dogru": dogru[:240]}
    a = _anahtar(yeni)
    for x in dersler:
        b = _anahtar(x)
        if x["tur"] == tur and a and len(a & b) / len(a | b) >= 0.8:  # benzer ders birleşir (kelime-kök Jaccard)
            x["destek"] += 1
            x["kanit"] = x["kanit"] if kanit in x["kanit"] else (x["kanit"] + " | " + kanit)[-200:]
            _yaz(DOSYA, dersler)
            return {"id": x["id"], "durum": "birlesti"}
    yeni.update(id=hashlib.sha1(f"{tur}|{tetik}".encode()).hexdigest()[:6], kanit=kanit[:200], destek=1, tarih=time.strftime("%Y-%m-%d"))
    _yaz(DOSYA, dersler + [yeni])
    return {"id": yeni["id"], "durum": "yeni"}


def tohum():
    """Ömer'in BHS5 D1 reddi: ders-dongu-1.md satır 4 (a)."""
    return ekle("video", "Ömer referans (ses, site, video, logo) verdi",
                "referans yerine benzer üretildi (BHS5 D1: referans ses yerine Kokoro)",
                "Referansı birebir kullan, benzer üretme; sapma kararını yalnız Ömer verir",
                ".kos/kopru/gorev/ders-dongu-1.md:4")


def getir(tur, gorev, k=K, jeton=JETON):
    """→ (blok, ids). ≥2 ortak kelime-kökü; tur verilirse yalnız o tür + genel. Sıra: ortak × (1+0.1·destek), sonra yenilik."""
    sorgu, puan = set(ders.kelimeler(gorev)), []
    for x in oku():
        if tur and x["tur"] not in (tur, "genel"):
            continue
        ortak = sorgu & set(ders.kelimeler(" ".join([x["tetik"], x["hata"], x["dogru"]])))
        if len(ortak) >= 2:
            puan.append((len(ortak) * (1 + 0.1 * min(x["destek"], 5)), x["tarih"], x))
    secilen = [p[2] for p in sorted(puan, key=lambda p: (-p[0], p[1]))[:k]]
    if not secilen:
        return "", []
    pay = jeton * 3 // len(secilen) - 1  # jeton ≈ karakter/3 (ucretsiz_havuz ile aynı)
    return "\n".join(f"- [{x['id']}] {x['tetik']} → {x['dogru']} (kaçın: {x['hata']})"[:pay] for x in secilen), [x["id"] for x in secilen]


def onek(gorev, tur=None):
    """İstem önüne ders bloğu; ders yok/hata → '' (0 jeton)."""
    try:
        blok = getir(tur, gorev[:600])[0]
    except Exception:
        return ""
    return "Dersler (uymuyorsa yok say):\n" + blok + "\n\n" if blok else ""


def topla(dizinler=None):
    """Hata işaretli satırları kanıt yoluyla döndürür (≥40 karakter); aday dosyada olan kanıt tekrarlanmaz."""
    var, bulunan = {a["kanit"] for a in oku(ADAY)}, []
    for d in dizinler or KAYNAK:
        for p in sorted(Path(d).glob("*.*")) if Path(d).is_dir() else []:
            if p.suffix not in (".md", ".log", ".tsv", ".txt"):
                continue
            for n, s in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                kanit = f"{p.relative_to(KOK) if KOK in p.parents else p}:{n}".replace("\\", "/")
                if ISARET.search(s) and len(s.strip()) >= 40 and kanit not in var:
                    bulunan.append({"kanit": kanit, "satir": s.strip()[:300]})
    return bulunan


ISTEM = ('Aşağıdaki hata/ret satırından tek bir genellenebilir ders çıkar. Yalnız JSON: {"tur":"video|site|kod|belge|araç|genel",'
         '"tetik":"hangi durumda","hata":"ne yanlış gitti","dogru":"doğru davranış"}. Satırda ders yoksa {"tur":""}.\nSatır: ')


def onayla(n=10):
    """≤n aday → ücretsiz havuz → ekle(). Havuz yoksa aday bekler (ders uydurulmaz)."""
    sys.path.insert(0, str(KOK / "tools"))
    import ucretsiz_havuz
    adaylar, yazilan, bitti = oku(ADAY), [], 0
    for a in adaylar[:min(n, 10)]:
        try:
            m, _, _ = ucretsiz_havuz.cagir("ozet", ISTEM + a["satir"], max_tokens=300, zaman=60)
        except OSError:  # havuz durum.json başka süreçte kilitli → aday bekler
            break
        if not m or "{" not in m:
            continue
        try:
            j = json.loads(m[m.index("{"):m.rindex("}") + 1])
            if j.get("tur"):
                yazilan.append(ekle(j["tur"], j["tetik"], j["hata"], j["dogru"], a["kanit"]))
            bitti += 1
            a["bitti"] = True
        except (ValueError, KeyError, TypeError):
            a["bitti"] = True  # bozuk/sırlı → tekrar denenmez
    _yaz(ADAY, [a for a in adaylar if not a.get("bitti")])
    return yazilan


def yansit():
    """Obsidian 50-dersler'e yeni dersleri yazar (tek_banka.py → ruflo ders bankası; claude-mem Obsidian'ı okur). → yeni dosya sayısı."""
    OBSIDIAN.mkdir(parents=True, exist_ok=True)
    yeni = 0
    for x in oku():
        p = OBSIDIAN / f"ders-dongu-{x['id']}.md"
        if not p.exists():
            p.write_bytes((f"# ders-dongu {x['id']} ({x['tur']})\n\n- Ders: {x['tetik']} → {x['dogru']}\n- Kök neden: {x['hata']}\n"
                           f"- Kanıt: {x['kanit']}\n- Tarih: {x['tarih']}\n").encode("utf-8"))
            yeni += 1
    return yeni


def olc():
    """vakalar.json: her vaka derssiz + dersli bir kez ücretsiz modele; yanıtta `uygula` regex'i varsa ders uygulandı sayılır."""
    sys.path.insert(0, str(KOK / "tools"))
    import ucretsiz_havuz
    vakalar, say = json.loads((KOK / "tools/ders_test/vakalar.json").read_text(encoding="utf-8")), {"derssiz": 0, "dersli": 0}
    for v in vakalar:
        for ad, on in (("derssiz", ""), ("dersli", onek(v["gorev"], v["tur"]))):
            m, _, _ = ucretsiz_havuz.cagir("ozet", on + v["gorev"] + "\nKısa yanıtla: hangi adımları atarsın?", max_tokens=400, zaman=60)
            say[ad] += bool(m and re.search(v["uygula"], m, re.I))
    return {"vaka": len(vakalar), **say}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    kmt, arg = (sys.argv[1] if len(sys.argv) > 1 else ""), " ".join(sys.argv[2:])
    if kmt == "topla":
        a = topla()
        _yaz(ADAY, oku(ADAY) + a)
        print(f"{len(a)} yeni aday")
    elif kmt == "onayla":
        print(onayla(int(arg or 10)))
    elif kmt == "yansit":
        print(yansit(), "dosya")
    elif kmt == "tohum":
        print(tohum())
    elif kmt == "getir":
        print(getir(None, arg)[0])
    elif kmt == "olc":
        print(olc())
    else:
        print(__doc__)
