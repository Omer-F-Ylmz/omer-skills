"""MAKARA döngü 2 (boşta, PC açık): gece şerit rotasyonu. Ücretsiz havuz kural önerisi üretir → held-out görevlerde mekanik + İKİ FARKLI AİLE hakem
(ayrışırsa ya da biri yoksa at) → kabul yalnız KUM HAVUZUNA (.kos/makara/kum), gerçek dosyaya yalnız onay/makara_onay.py. Claude token 0, Haiku yok.
Zamanlanmış görev (30 dk'da bir): conhost --headless python.exe makara_gece.py (pencere yok); şart: RAM <%80, GetLastInputInfo ≥10 dk (her öneride yeniden), günde 1 gece (5 şerit × en fazla 3 öneri, çağrı tavanı 150).
  python tools/makara_gece.py [--kuru --serit skill --n 3] [--zorla] | kur | kaldir
  python tools/makara_gece.py --bulut --girdi paket --cikti out [--sure 1380]   # SLEEP-3: Actions runner (PC kapalı), girdi tools/makara_paket.py çıktısı"""
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
TAVAN = 150  # gece başına havuz çağrısı üst sınırı (yeniden denemeler dahil, gün içi tick'ler toplamı)
RAM_ES, BOSTA, T, N_SERIT = 80, 600, 3, 3  # %, sn, held-out görev sayısı/öneri, şerit başı en fazla öneri
HAKEM_AILE = ("mistral", "alibaba", "openai", "minimax", "google", "nvidia", "meta")  # hızlı yanıt verenler önce; görev başına ilk İKİ YANIT VEREN alınır (21 Eki canlı: meta yanıtsız)
HAKEM_MT = {"nvidia": 8000}  # nemotron düşünme jetonu 1500'ü yer, boş yanıt döner
TABAN = {}  # görev kimliği → eski (kuralsız) yanıt; şeritler arası paylaşılır
OZET, HAFTA = KOK / ".kos/kopru/uyku-ozet.txt", KOK / ".kos/kopru/makara-hafta-ozet.txt"  # Desktop sabah yalnız bunları okur
GOREV = KOK / ".kos/sleep/lanes/omer-skills/tasks-v2.json"
HOME = Path.home()
SERITLER = [  # (ad, glob'lar, gece başına hedef)
    ("skill", [str(KOK / "skills/*/SKILL.md")], 2),
    ("ogren", [str(KOK / "docs/ogren/**/*.md")], 2),
    ("router", [str(KOK / "tools/yonlendir-kurallar.json")], 1),
    ("kural", [r"C:\Projeler\omer-kurallar.md", str(HOME / ".claude/CLAUDE.md")], 1),
    ("ters", [str(KOK / "skills/tersine*/SKILL.md"), str(KOK / "docs/**/ters*.md")], 1),
]
BULUT, GIRDI = False, None  # --bulut: Linux runner ya da yerel simülasyon; GIRDI = makara_paket çıktısı
BULUT_SERIT = [  # paket kökünde hedefler/ altına aynı göreli yolla girer (omer-kurallar.md yalnız ana repo kökünün bir üstünde); ~/.claude/CLAUDE.md HİÇ gitmez
    ("skill", ["skills/*/SKILL.md"], 2),
    ("ogren", ["docs/ogren/**/*.md"], 2),
    ("router", ["tools/yonlendir-kurallar.json"], 1),
    ("kural", ["omer-kurallar.md"], 1),
    ("ters", ["skills/tersine*/SKILL.md", "docs/**/ters*.md"], 1),
]
GIZLI = re.compile(r"sk-[\w-]{20,}|gh[ps]_\w{20,}|AIza[\w-]{30,}|Bearer\s+[\w.-]{20,}|(?i:api[_-]?key|secret|password)\s*[=:]")
SONUC = re.compile(r"SONUC:\s*(A|B|EQ)\b")


class Say:  # çağrı sayacı: tavan aşılınca None döner; claude = Haiku/Claude'dan gelen yanıt sayısı (kanıt: hep 0)
    n = claude = ert = 0
    bitis = float("inf")  # yalnız --bulut: duvar saati sınırı (job timeout'u artefakt yüklemesini kesmesin)
    olu = set()  # bu gece yanıt vermeyen hakem aileleri (tekrar çağrılmaz)
    durdu = False  # RAM/boşta/tavan yüzünden şerit yarıda kaldı
    bos = False  # son çağrı havuzdan yanıt alamadı (tükenme) → öneri atılmaz, ertelenir
    kaz = {}


def cagri(tur, istem, **kw):
    if Say.n >= TAVAN:
        Say.bos = True
        return None
    y, k, log = H.cagir(tur, istem, haiku_tavan=0, **kw)  # SABİT 0: kw ile açılamaz (çift anahtar TypeError); Claude/Haiku halkası kapalı
    Say.n += 1 + len(log)
    Say.claude += (k or "").startswith("haiku")
    Say.bos = Say.bos or y is None
    return y


def ertele(h):
    """Havuz tükendi: hedef atılmaz, ertelenen.jsonl'e 'makara:' kimlikle yazılır; sonraki gece ertelenenler() alır (H.tekrar bu kimlikleri çalıştırmaz)."""
    H._ertele("makara:" + h, dict(tur="yazim", istem=h, max_tokens=0, aile=None, haric_aile=None, haiku_tavan=0, etiket="makara", zaman=90))
    Say.ert += 1


def ertelenenler():
    # shortcut: dosya kilidi yok; aynı anda serve yazarsa bir satır kaybolabilir, sık paralel süreçte H.KILIT kullan
    if not H.ERT.exists():
        return []
    ent = [json.loads(s) for s in H.ERT.read_text(encoding="utf-8").splitlines() if s.strip()]
    H.ERT.write_bytes("".join(json.dumps(i, ensure_ascii=False) + "\n" for i in ent if not i["id"].startswith("makara:")).encode("utf-8"))
    return [i["id"][7:] for i in ent if i["id"].startswith("makara:") and Path(i["id"][7:]).exists()]


def ram():
    if BULUT:
        return 0
    class MS(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(f"x{i}", ctypes.c_ulonglong) for i in range(7)]
    m = MS(); m.l = ctypes.sizeof(MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.yuk


def bosta_sn():
    if BULUT:
        return 10**9
    class LI(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_uint), ("t", ctypes.c_uint)]
    li = LI(); li.cb = ctypes.sizeof(LI)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(li))
    return (ctypes.windll.kernel32.GetTickCount() - li.t) / 1000


def sartlar(durum, bugun, zorla=False):  # zorla: günde-1-koşu ve boşta şartı atlanır, RAM/çakışma kalır
    if durum.get("son_gun") == bugun and not zorla:
        return "bugün koşuldu"
    if time.time() - durum.get("calisiyor", 0) < 7200:
        return "başka koşu sürüyor"
    if ram() >= RAM_ES:
        return f"RAM %{ram()}"
    if bosta_sn() < BOSTA and not zorla:
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
    if aile in Say.olu:
        return None
    r = cagri("hakem", ist, max_tokens=HAKEM_MT.get(aile, 1500), aile=aile, dogrula=lambda t: None if SONUC.search(t) else "sonuç satırı yok")
    if not r:
        if Say.n < TAVAN:  # tavan yüzünden değil, aile gerçekten yanıt vermedi
            Say.olu.add(aile)
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
        bulunan = []  # görev başına yanıt veren ilk iki FARKLI aile (kota/soğuma düşebilir)
        for aile in HAKEM_AILE:
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


def gece(serit, n, kuru=False, devam=False, zorla=False):
    t0, durum = time.time(), json.loads((M / "durum.json").read_text(encoding="utf-8")) if (M / "durum.json").exists() else {}
    bugun = time.strftime("%Y-%m-%d")
    durum["calisiyor"] = t0
    M.mkdir(parents=True, exist_ok=True); (M / "kum").mkdir(exist_ok=True)
    (M / "durum.json").write_text(json.dumps(durum), encoding="utf-8")
    imlec0 = dict(durum.get("imlec", {}))
    dersler = (bulut_dersler() if BULUT else [e["metin"] for e in sorted(makara_ders.yukle()["dersler"].values(), key=lambda e: -e["sayac"])[:5]]) or ["(henüz ders yok)"]
    gor = [g for g in json.loads(GOREV.read_text(encoding="utf-8"))["tasks"] if len(g["intent"]) < 900 and g["reference"]]
    gor = sorted(gor, key=lambda g: g["split"] != "val")[:T]  # val önce; öneri üretiminde görevler görülmez
    for g in gor:
        if not TABAN.get(g["id"]):
            TABAN[g["id"]] = cagri("yazim", g["intent"][:2500], max_tokens=1200)
    taban = {g["id"]: TABAN[g["id"]] for g in gor}
    kayit = []
    Say.durdu = False
    if not devam:
        Say.claude = Say.ert = 0; Say.kaz = {}
    devir = [] if kuru else ertelenenler()  # önceki gecenin ertelenenleri önce
    for p in devir[n:]:
        ertele(p)
    liste = devir[:n] + hedefler(serit, n - len(devir[:n]), durum.setdefault("imlec", {}))
    for j, h in enumerate(liste):
        if (not kuru and (ram() >= RAM_ES or (bosta_sn() < BOSTA and not zorla))) or Say.n >= TAVAN or (BULUT and time.time() > Say.bitis):  # kuru koşu yalnız raporlar; gerçek koşu her öneride RAM/boşta/tavanı yeniden sınar
            for r in liste[j:]:
                ertele(r)
            Say.durdu = True
            kayit.append((h, None, "ertelendi: durdu (RAM/boşta/tavan)")); break
        metin = Path(h).read_text(encoding="utf-8", errors="replace")
        Say.bos = False
        kural = oner(h, metin, dersler)
        if not kural:
            if Say.bos:
                ertele(h)
            kayit.append((h, None, "ertelendi: havuz tükendi" if Say.bos else "öneri üretilemedi")); continue
        oy, me, mn, fam = degerlendir(kural, gor, taban)
        ok, neden = karar(oy, me, mn)
        if not ok and neden in ("tek hakem ailesi", "hakem yanıtı eksik"):  # hakem havuzu tükendi: öneri atılmaz
            ertele(h)
            kayit.append((h, kural, "ertelendi: " + neden)); continue
        kid = "m" + hashlib.sha1((h + kural).encode()).hexdigest()[:6]
        olcum = {"mekanik_eski": me, "mekanik_yeni": mn, "oy": oy, "aileler": fam}
        if ok:
            Say.kaz[kid] = sum(1 for vs in oy.values() for v in vs if v == "B") - sum(1 for vs in oy.values() for v in vs if v == "A")
            (M / "kum" / f"{kid}.json").write_text(json.dumps(dict(id=kid, gun=bugun, serit=serit, hedef=h, kural=kural, olcum=olcum, durum="bekliyor"), ensure_ascii=False), encoding="utf-8")
        kayit.append((h, kural, f"{'KABUL ' + kid if ok else 'ret'}: {neden}"))
    if kuru:
        durum["imlec"] = imlec0  # kuru koşu rotasyonu ilerletmez
    durum["calisiyor"] = 0
    (M / "durum.json").write_text(json.dumps(durum), encoding="utf-8")
    if not kuru:
        serit, kayit, sn = gun_birlestir(bugun, serit, kayit, time.time() - t0)
    else:
        sn = time.time() - t0
    return rapor(bugun, serit, kayit, sn, kuru)


def gun_birlestir(bugun, serit, kayit, sn):
    """Aynı günün şerit koşuları tek uyku notunda toplanır (gun.json); aynı hedef yeniden işlenirse eski satırı düşer. (şerit etiketi, birleşik kayıt, toplam sn)."""
    y = M / "gun.json"
    g = json.loads(y.read_text(encoding="utf-8")) if y.exists() else {}
    if g.get("gun") != bugun:
        g = {"gun": bugun, "serit": {}, "kaz": {}, "ert": 0, "sn": 0}
    yeni = {h for h, _, _ in kayit}
    g["serit"][serit] = [k for k in g["serit"].get(serit, []) if k[0] not in yeni] + [list(k) for k in kayit]
    g["kaz"].update(Say.kaz); g["ert"] += Say.ert; g["sn"] += sn
    y.write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
    Say.kaz, Say.ert = dict(g["kaz"]), g["ert"]
    return "+".join(g["serit"]), [tuple(k) for v in g["serit"].values() for k in v], g["sn"]


def rapor(bugun, serit, kayit, sn, kuru):
    kabul = sum(1 for _, _, s in kayit if s.startswith("KABUL"))
    sat = [f"- `{Path(h).name}` · {k or '-'} → {s}" for h, k, s in kayit]
    y = KASA / "90-log" / f"uyku-{bugun}{'-kuru' if kuru else ''}.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_bytes((f"---\ntur: uyku\nguncellenme: {bugun}\netiket: [uyku, makara]\n---\n# uyku {bugun}{' (kuru)' if kuru else ''}\n"
                   f"- şerit: {serit} · öneri: {len(kayit)} · kabul: {kabul} · ret: {len(kayit) - kabul - sum(1 for _, _, s in kayit if s.startswith('ertelendi'))} · ertelenen {Say.ert}\n"
                   f"- ölçüm: havuz çağrısı {Say.n}/{TAVAN} · {sn:.0f} sn · RAM %{ram()} · Claude token 0 · Haiku 0 · pencere 0\n"
                   "- hakem: iki farklı aile (görev başına yanıt veren ilk iki farklı: mistral · alibaba · openai · minimax · google · nvidia · meta; ikisi de net yeni-lehine değilse ret); mekanik: rubrikteki sayısal tavanlar\n## Öneriler\n" + "\n".join(sat) + "\n").encode("utf-8"))
    ozet(bugun, serit, kayit, kuru)
    onay_listesi()
    return kabul, len(kayit), str(y)


def ozet(bugun, serit, kayit, kuru):
    """≤12 satır sabit biçim; betik yazar (model yok). Desktop sabah yalnız bunu okur."""
    kab = [(s.split()[1].rstrip(":"), h) for h, _, s in kayit if s.startswith("KABUL")]
    ert = sum(1 for _, _, s in kayit if s.startswith("ertelendi"))
    sat = [f"uyku {bugun}{' (kuru)' if kuru else ''} · şerit {serit}",
           f"öneri {len(kayit)} · kabul {len(kab)} · ret {len(kayit) - len(kab) - ert} · ertelenen {Say.ert}"]
    sat += [f"{k} · {Path(h).name} · +{Say.kaz.get(k, 0)}" for k, h in kab[:7]]
    if len(kab) > 7:
        sat.append(f"+{len(kab) - 7} kabul daha")
    if any("durdu" in s for _, _, s in kayit):
        sat.append("hata: durdu (RAM/tavan)")
    sat.append(f"Claude çağrısı={Say.claude} (haiku_tavan=0)")
    m = ("\n".join(x[:120] for x in sat) + "\n").encode("utf-8")
    if not kuru:
        OZET.parent.mkdir(parents=True, exist_ok=True); OZET.write_bytes(m)
    (KASA / "90-log" / f"uyku-ozet-{bugun}{'-kuru' if kuru else ''}.md").write_bytes(m)


def onay_listesi():
    bek = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((M / "kum").glob("*.json"))]
    bek = [r for r in bek if r["durum"] == "bekliyor"]
    y = KASA / "90-log" / f"onay-listesi-{time.strftime('%G-W%V')}.md"
    y.write_bytes(("---\ntur: onay\netiket: [onay, makara]\n---\n# Makara onay listesi\nKabul: `python onay/makara_onay.py <id>` (yedekli) · geri: `--geri`\n"
                   + "\n".join(f"- **{r['id']}** [{r['serit']}] `{Path(r['hedef']).name}`: {r['kural']} (oy {r['olcum']['oy']})" for r in bek) + ("" if bek else "bekleyen yok") + "\n").encode("utf-8"))
    sat = [f"onay bekleyen {len(bek)} · hafta {time.strftime('%G-W%V')}"] + [f"{r['id']} · {r['serit']} · {Path(r['hedef']).name} · {r['kural']}"[:140] for r in bek[:11]]
    if len(bek) > 11:
        sat.append(f"+{len(bek) - 11} daha (tam liste Obsidian onay-listesi)")
    sat.append("kabul: python onay/makara_onay.py <id> · geri: --geri")
    HAFTA.parent.mkdir(parents=True, exist_ok=True); HAFTA.write_bytes(("\n".join(sat) + "\n").encode("utf-8"))


def hepsi(bugun, zorla=False):
    """Boş pencerede bugünün şerit sırasıyla her şeritte en fazla N_SERIT öneri; tavan/boşta/RAM dolunca durur, bitmeyen şerit sonraki tick'te sürer."""
    durum = json.loads((M / "durum.json").read_text(encoding="utf-8")) if (M / "durum.json").exists() else {}
    devam = durum.get("bitenler_gun") == bugun and not zorla
    bit = list(durum.get("bitenler", [])) if devam else []
    Say.n = durum["cagri"][1] if devam and durum.get("cagri", [None])[0] == bugun else 0
    Say.olu = set()
    i0 = time.localtime().tm_yday % len(SERITLER)
    sira = [s[0] for s in SERITLER[i0:] + SERITLER[:i0]]
    for s in sira:
        if s in bit:
            continue
        gece(s, N_SERIT, devam=True, zorla=zorla)
        if Say.durdu or Say.n >= TAVAN:
            break
        bit.append(s)
    durum = json.loads((M / "durum.json").read_text(encoding="utf-8"))
    durum.update(bitenler=[s[0] for s in SERITLER if s[0] in bit], bitenler_gun=bugun, cagri=[bugun, Say.n])
    durum.pop("son_gun", None)  # yarım kalan gece sonraki tick'te sürer (zorla koşu eski bir son_gun'u da açar)
    if len(bit) == len(SERITLER) or Say.n >= TAVAN:
        durum["son_gun"] = bugun
    (M / "durum.json").write_text(json.dumps(durum), encoding="utf-8")
    return bit


def bulut_dersler():
    """Pakete giren ders notlarından en sık tekrarlanan 5 satır (sayaç = '(×n, ...)')."""
    sat = [s[2:] for p in sorted((GIRDI / "dersler").glob("ders-*.md")) for s in p.read_text(encoding="utf-8").splitlines() if s.startswith("- ")]
    return sorted(sat, key=lambda s: -int((re.search(r"×(\d+)", s) or [0, 1])[1]))[:5]


def bulut(girdi, cikti, sure=1380):
    """--bulut: ctypes/Obsidian/~/.claude yok. girdi = makara_paket çıktısı; cikti = artefakt dizini (makara/kum/*.json, uyku-ozet.txt, rapor/, havuz/ertelenen.jsonl)."""
    global BULUT, GIRDI, M, KASA, OZET, HAFTA, GOREV, SERITLER
    BULUT, GIRDI, cikti = True, Path(girdi), Path(cikti)
    M, KASA, GOREV = cikti / "makara", cikti / "rapor", GIRDI / "tasks-v2.json"
    OZET, HAFTA = cikti / "uyku-ozet.txt", cikti / "makara-hafta-ozet.txt"
    SERITLER = [(ad, [str(GIRDI / "hedefler" / d) for d in g], n) for ad, g, n in BULUT_SERIT]
    H.DIZIN = cikti / "havuz"
    H.DURUM, H.ERT, H.SONUC = H.DIZIN / "durum.json", H.DIZIN / "ertelenen.jsonl", H.DIZIN / "ertelenen-sonuc.jsonl"
    H.ENT = [e for e in H.ENT if e.prov not in ("omniroute", "github")]  # yerel köprü/gh oturumu bulutta yok
    Say.bitis = time.time() + sure
    return hepsi(time.strftime("%Y-%m-%d"))


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
    ap.add_argument("--kuru", action="store_true"); ap.add_argument("--serit", choices=[s[0] for s in SERITLER]); ap.add_argument("--n", type=int); ap.add_argument("--zorla", action="store_true")
    ap.add_argument("--bulut", action="store_true"); ap.add_argument("--girdi", default="paket"); ap.add_argument("--cikti", default="out"); ap.add_argument("--sure", type=int, default=1380)
    a = ap.parse_args(argv)
    if a.bulut:
        return print("tamam:", bulut(a.girdi, a.cikti, a.sure))
    if a.komut:
        return kur(a.komut == "kaldir")
    durum = json.loads((M / "durum.json").read_text(encoding="utf-8")) if (M / "durum.json").exists() else {}
    bugun = time.strftime("%Y-%m-%d")
    if not a.kuru and (neden := sartlar(durum, bugun, a.zorla)):
        return print("atlandı:", neden)
    makara_ders.main()
    if not (a.kuru or a.serit):
        return print("tamam:", hepsi(bugun, a.zorla))
    sirada = a.serit or SERITLER[time.localtime().tm_yday % len(SERITLER)][0]
    n = a.n or next(s[2] for s in SERITLER if s[0] == sirada)
    print("tamam:", gece(sirada, min(n, 3), a.kuru, zorla=a.zorla))


if __name__ == "__main__":
    main()
