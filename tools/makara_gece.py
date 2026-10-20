"""MAKARA döngü 2 (boşta, PC açık): gece şerit rotasyonu. Ücretsiz havuz kural önerisi üretir → held-out görevlerde mekanik + İKİ FARKLI AİLE hakem
(ayrışırsa ya da biri yoksa at) → kabul yalnız KUM HAVUZUNA (.kos/makara/kum), gerçek dosyaya yalnız onay/makara_onay.py. Claude token 0, Haiku yok.
Zamanlanmış görev: conhost --headless python.exe makara_gece.py (pencere yok); şart: RAM <%80, GetLastInputInfo ≥10 dk, günde 1 koşu.
  python tools/makara_gece.py [--kuru --serit skill --n 3] | kur | kaldir"""
import argparse
import ctypes
import glob
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import makara_ders  # noqa: E402
import ucretsiz_havuz as H  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
M = KOK / ".kos/makara"
KASA = makara_ders.KASA
AD = "omer-makara-gece"
TAVAN = 120  # gece başına havuz çağrısı üst sınırı (yeniden denemeler dahil)
RAM_ES, BOSTA, T = 80, 600, 3  # %, sn, held-out görev sayısı/öneri
GOREV = KOK / ".kos/sleep/lanes/omer-skills/tasks-v2.json"
HOME = Path.home()
SERITLER = [  # (ad, glob'lar, gece başına hedef)
    ("skill", [str(KOK / "skills/*/SKILL.md")], 2),
    ("ogren", [str(KOK / "docs/ogren/**/*.md")], 2),
    ("router", [str(KOK / "tools/yonlendir-kurallar.json")], 1),
    ("kural", [r"C:\Projeler\omer-kurallar.md", str(HOME / ".claude/CLAUDE.md")], 1),
    ("ters", [str(KOK / "skills/tersine*/SKILL.md"), str(KOK / "docs/**/ters*.md")], 1),
]
GIZLI = re.compile(r"sk-[\w-]{20,}|gh[ps]_\w{20,}|AIza[\w-]{30,}|Bearer\s+[\w.-]{20,}|(?i:api[_-]?key|secret|password)\s*[=:]")
SONUC = re.compile(r"SONUC:\s*(A|B|EQ)\b")


class Say:  # çağrı sayacı: tavan aşılınca None döner
    n = 0


def cagri(tur, istem, **kw):
    if Say.n >= TAVAN:
        return None
    y, k, log = H.cagir(tur, istem, haiku_tavan=0, **kw)
    Say.n += 1 + len(log)
    return y


def ram():
    class MS(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(f"x{i}", ctypes.c_ulonglong) for i in range(7)]
    m = MS(); m.l = ctypes.sizeof(MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.yuk


def bosta_sn():
    class LI(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_uint), ("t", ctypes.c_uint)]
    li = LI(); li.cb = ctypes.sizeof(LI)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(li))
    return (ctypes.windll.kernel32.GetTickCount() - li.t) / 1000


def sartlar(durum, bugun):
    if durum.get("son_gun") == bugun:
        return "bugün koşuldu"
    if time.time() - durum.get("calisiyor", 0) < 7200:
        return "başka koşu sürüyor"
    if ram() >= RAM_ES:
        return f"RAM %{ram()}"
    if bosta_sn() < BOSTA:
        return "kullanıcı boşta değil"


def mekanik(cikti, ref):
    """Rubrikteki sayısal tavanlar (En fazla N satır/cümle/madde, Tam N madde); denetlenecek şey yoksa None."""
    c = cikti.strip()
    m = re.search(r"[Ee]n fazla (\d+) (satır|cümle|madde)", ref) or re.search(r"Tam (\d+) (madde)", ref)
    if not c:
        return False
    if not m:
        return None
    n, tur = int(m[1]), m[2]
    say = len([s for s in c.splitlines() if s.strip()]) if tur != "cümle" else len(re.findall(r"[.!?](\s|$)", c))
    return say == n if m[0].startswith("Tam") else say <= n


def hakem(aile, gorev, a, b):
    """'A'|'B'|'EQ'|None. Sıra görev kimliğiyle deterministik çevrilir (konum yanlılığı)."""
    ters = int(hashlib.sha1((gorev["id"] + aile).encode()).hexdigest(), 16) % 2
    x, y = (b, a) if ters else (a, b)
    ist = (f"Ölçüt: {gorev['reference']}\n\nGörev: {gorev['intent'][:1500]}\n\n=== Yanıt A ===\n{x[:1500]}\n\n=== Yanıt B ===\n{y[:1500]}\n\n"
           "Ölçüte hangi yanıt daha iyi uyuyor? Son satır tam olarak `SONUC: A`, `SONUC: B` ya da `SONUC: EQ` olsun.")
    r = cagri("hakem", ist, max_tokens=1500, aile=aile, dogrula=lambda t: None if SONUC.search(t) else "sonuç satırı yok")
    if not r:
        return None
    v = SONUC.findall(r)[-1]
    return v if v == "EQ" else ("A" if (v == "B") == bool(ters) else "B")  # A=eski(a), B=yeni(b) uzayına çevir


def karar(oy, mek_eski, mek_yeni):
    """oy: {aile: [hakem sonuçları]}; ikisi de net yeni-lehine ve mekanik kötüleşmediyse True."""
    if len(oy) < 2:
        return False, "tek hakem ailesi"
    net = {a: sum(1 for v in vs if v == "B") - sum(1 for v in vs if v == "A") for a, vs in oy.items()}
    if any(not vs or None in vs for vs in oy.values()):
        return False, "hakem yanıtı eksik"
    if mek_yeni < mek_eski:
        return False, "mekanik kötüleşti"
    if all(n > 0 for n in net.values()):
        return True, "kabul"
    return False, "hakemler ayrıştı/eşit " + str(net)


def oner(hedef, metin, dersler):
    ist = ("Aşağıdaki hedef metni ve son derslere bakarak TEK bir kural satırı öner: ≤200 karakter, emir kipi, somut; Claude'un yanıt kalitesini "
           "ya da token tasarrufunu artıran genel bir davranış kuralı olsun. Yalnız kuralı yaz, başka metin yok.\n\n"
           f"Hedef: {hedef}\n{metin[:1500]}\n\nSon dersler:\n" + "\n".join("- " + s for s in dersler))
    r = cagri("yazim", ist, max_tokens=1500)
    k = next((re.sub(r"^[\s\-*•\d.)\"]+|[\s\"]+$", "", s) for s in (r or "").splitlines() if s.strip()), "")
    return k if 15 <= len(k) <= 240 and not GIZLI.search(k) else None


def degerlendir(kural, gorevler, taban):
    oy, me, mn, mec, fam = {}, 0, 0, [], {}
    for g in gorevler:
        yeni = cagri("yazim", f"Kural: {kural}\n\n{g['intent'][:2500]}", max_tokens=1200)
        eski = taban.get(g["id"])
        if not yeni or not eski:
            oy.setdefault("eksik", []).append(None); continue
        for a, c in mec_pairs(g, eski, yeni):
            mec.append((a, c))
        bulunan = []  # görev başına açık ilk iki FARKLI aile (gemini günlük kotası düşebilir)
        for aile in ("google", "mistral", "meta", "nvidia", "minimax", "alibaba"):
            if len(bulunan) < 2 and (v := hakem(aile, g, eski, yeni)):
                bulunan.append(aile); oy.setdefault(f"h{len(bulunan)}", []).append(v); fam.setdefault(f"h{len(bulunan)}", []).append(aile)
        for i in range(len(bulunan) + 1, 3):
            oy.setdefault(f"h{i}", []).append(None)
    me = sum(1 for a, c in mec if a is True); mn = sum(1 for a, c in mec if c is True)
    return oy, me, mn, fam


def mec_pairs(g, eski, yeni):
    a, c = mekanik(eski, g["reference"]), mekanik(yeni, g["reference"])
    return [(a, c)] if a is not None and c is not None else []


def hedefler(serit, n, imleç):
    ad, desenler, _ = next(s for s in SERITLER if s[0] == serit)
    yollar = sorted({p for d in desenler for p in glob.glob(d, recursive=True)})
    if not yollar:
        return []
    i = imleç.get(serit, 0) % len(yollar)
    imleç[serit] = i + n
    return [yollar[(i + j) % len(yollar)] for j in range(min(n, len(yollar)))]


def gece(serit, n, kuru=False):
    t0, durum = time.time(), json.loads((M / "durum.json").read_text(encoding="utf-8")) if (M / "durum.json").exists() else {}
    bugun = time.strftime("%Y-%m-%d")
    durum["calisiyor"] = t0
    M.mkdir(parents=True, exist_ok=True); (M / "kum").mkdir(exist_ok=True)
    (M / "durum.json").write_text(json.dumps(durum), encoding="utf-8")
    imlec0 = dict(durum.get("imlec", {}))
    d = makara_ders.yukle()
    dersler = [e["metin"] for e in sorted(d["dersler"].values(), key=lambda e: -e["sayac"])[:5]] or ["(henüz ders yok)"]
    gor = [g for g in json.loads(GOREV.read_text(encoding="utf-8"))["tasks"] if len(g["intent"]) < 900 and g["reference"]]
    gor = sorted(gor, key=lambda g: g["split"] != "val")[:T]  # val önce; öneri üretiminde görevler görülmez
    taban = {g["id"]: cagri("yazim", g["intent"][:2500], max_tokens=1200) for g in gor}
    kayit = []
    for h in hedefler(serit, n, durum.setdefault("imlec", {})):
        if (ram() >= RAM_ES and not kuru) or Say.n >= TAVAN:  # kuru koşu RAM'i yalnız raporlar, gerçek koşu durur
            kayit.append((h, None, "durdu (RAM/tavan)")); break
        metin = Path(h).read_text(encoding="utf-8", errors="replace")
        kural = oner(h, metin, dersler)
        if not kural:
            kayit.append((h, None, "öneri üretilemedi")); continue
        oy, me, mn, fam = degerlendir(kural, gor, taban)
        ok, neden = karar(oy, me, mn)
        kid = "m" + hashlib.sha1((h + kural).encode()).hexdigest()[:6]
        olcum = {"mekanik_eski": me, "mekanik_yeni": mn, "oy": oy, "aileler": fam}
        if ok:
            (M / "kum" / f"{kid}.json").write_text(json.dumps(dict(id=kid, gun=bugun, serit=serit, hedef=h, kural=kural, olcum=olcum, durum="bekliyor"), ensure_ascii=False), encoding="utf-8")
        kayit.append((h, kural, f"{'KABUL ' + kid if ok else 'ret'}: {neden}"))
    if kuru:
        durum["imlec"] = imlec0  # kuru koşu rotasyonu ilerletmez
    else:
        durum["son_gun"] = bugun
    durum["calisiyor"] = 0
    (M / "durum.json").write_text(json.dumps(durum), encoding="utf-8")
    return rapor(bugun, serit, kayit, time.time() - t0, kuru)


def rapor(bugun, serit, kayit, sn, kuru):
    kabul = sum(1 for _, _, s in kayit if s.startswith("KABUL"))
    sat = [f"- `{Path(h).name}` · {k or '-'} → {s}" for h, k, s in kayit]
    y = KASA / "90-log" / f"uyku-{bugun}{'-kuru' if kuru else ''}.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_bytes((f"---\ntur: uyku\nguncellenme: {bugun}\netiket: [uyku, makara]\n---\n# uyku {bugun}{' (kuru)' if kuru else ''}\n"
                   f"- şerit: {serit} · öneri: {len(kayit)} · kabul: {kabul} · ret: {len(kayit) - kabul}\n"
                   f"- ölçüm: havuz çağrısı {Say.n}/{TAVAN} · {sn:.0f} sn · RAM %{ram()} · Claude token 0 · Haiku 0 · pencere 0\n"
                   "- hakem: iki farklı aile (görev başına açık ilk iki farklı: google · mistral · meta · nvidia · minimax · alibaba; ikisi de net yeni-lehine değilse ret); mekanik: rubrikteki sayısal tavanlar\n## Öneriler\n" + "\n".join(sat) + "\n").encode("utf-8"))
    onay_listesi()
    return kabul, len(kayit), str(y)


def onay_listesi():
    bek = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((M / "kum").glob("*.json"))]
    bek = [r for r in bek if r["durum"] == "bekliyor"]
    y = KASA / "90-log" / f"onay-listesi-{time.strftime('%G-W%V')}.md"
    y.write_bytes(("---\ntur: onay\netiket: [onay, makara]\n---\n# Makara onay listesi\nKabul: `python onay/makara_onay.py <id>` (yedekli) · geri: `--geri`\n"
                   + "\n".join(f"- **{r['id']}** [{r['serit']}] `{Path(r['hedef']).name}`: {r['kural']} (oy {r['olcum']['oy']})" for r in bek) + ("" if bek else "bekleyen yok") + "\n").encode("utf-8"))


def kur(sil=False):
    if sil:
        return subprocess.run(["schtasks", "/Delete", "/TN", AD, "/F"], capture_output=True, text=True).returncode
    tr = f'conhost.exe --headless "{sys.executable}" "{Path(__file__).resolve()}"'
    r = subprocess.run(["schtasks", "/Create", "/TN", AD, "/SC", "MINUTE", "/MO", "30", "/TR", tr, "/F"], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    return r.returncode


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", nargs="?", choices=["kur", "kaldir"])
    ap.add_argument("--kuru", action="store_true"); ap.add_argument("--serit", choices=[s[0] for s in SERITLER]); ap.add_argument("--n", type=int)
    a = ap.parse_args(argv)
    if a.komut:
        return kur(a.komut == "kaldir")
    durum = json.loads((M / "durum.json").read_text(encoding="utf-8")) if (M / "durum.json").exists() else {}
    bugun = time.strftime("%Y-%m-%d")
    if not a.kuru and (neden := sartlar(durum, bugun)):
        return print("atlandı:", neden)
    makara_ders.main()
    sirada = a.serit or SERITLER[time.localtime().tm_yday % len(SERITLER)][0]
    n = a.n or next(s[2] for s in SERITLER if s[0] == sirada)
    print("tamam:", gece(sirada, min(n, 3), a.kuru))


if __name__ == "__main__":
    main()
