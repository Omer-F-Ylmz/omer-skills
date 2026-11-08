"""DENKLIK-1 (22 Eki): ücretsiz katman Opus referansına denk mi? Claude jetonu 0.
  python tools/denklik.py altin [--gun 14] [--adet 5]   → tools/denklik/altin.jsonl (tür başına Opus oturumu: girdi + referans)
  python tools/denklik.py olc [--tur T] [--adet N]      → ücretsiz katman vakaları çözer, 2 aileli kör hakem puanlar → sonuc.jsonl
  python tools/denklik.py tablo                         → tür × katman denklik tablosu (+ yonlendir-kayit) ve denklik_eksik.jsonl kayıtları
Denklik = hakem puanı ≥ 0,98 × referans puanı (referans 100). Kabul vekili: Ömer'in onay işareti transkriptte aranmaz; oturum
bitiş raporunda *_EKSIK/DUR işareti yoksa ve araç kullanılmışsa kabul sayılır (vekil; kanıt değil)."""
import argparse
import collections
import glob
import json
import os
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
DIZIN = Path(__file__).with_name("denklik")
ALTIN, SONUC, EKSIK = DIZIN / "altin.jsonl", DIZIN / "sonuc.jsonl", Path(__file__).with_name("denklik_eksik.jsonl")
OTURUM = Path(os.path.expanduser("~/.claude/projects/C--Projeler-omer-skills"))
TURLER = {
    "kod-backend": r"pytest|\.py\b|fonksiyon|\btest\b|refactor|\bhata\b|\bbug\b|regex|\.cs\b|dotnet",
    "site-3d": r"three\.?js|\bglb\b|landing|\bsite\b|shader|scroll|r3f|\bhero\b|webgl",
    "logo-gorsel": r"\blogo\b|\bsvg\b|görsel|render|blender|\bpng\b|ikon",
    "video": r"video|ffmpeg|whisper|reel|altyazı|premiere|kare",
    "araştırma": r"araştır|karşılaştır|inceleme|rapor|kaynak|benchmark",
    "kurulum": r"\bkur\b|kurulum|install|plugin|\bmcp\b|marketplace|eklenti",
    "belge": r"belge|docx|pptx|\bpdf\b|sunum|\.md\b|dokuman|döküman",
}
KUSUR = re.compile(r"ARAC_EKSIK|KANIT_EKSIK|OGRENME_EKSIK|\bDUR\b|başarısız|yapılmadı", re.I)


def _metin(c):
    if isinstance(c, str):
        return c
    return "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")


def _oku(f):
    """→ (ilk kullanıcı istemi, son asistan metni, opus payı, araç sayısı) ya da None."""
    ilk, son, mod, arac = None, "", collections.Counter(), 0
    for l in open(f, encoding="utf-8", errors="ignore"):
        try:
            o = json.loads(l)
        except ValueError:
            continue
        m = o.get("message") or {}
        if o.get("type") == "user" and ilk is None and not o.get("isSidechain"):
            t = _metin(m.get("content"))
            if t.strip() and "<system-reminder>" not in t[:40]:
                ilk = t
        elif o.get("type") == "assistant" and not o.get("isSidechain"):
            mod[m.get("model", "")] += 1
            c = m.get("content")
            arac += sum(1 for b in c if isinstance(b, dict) and b.get("type") == "tool_use") if isinstance(c, list) else 0
            t = _metin(c)
            if t.strip():
                son = t
    n = sum(mod.values())
    return (ilk, son, mod["claude-opus-5-5"] / n, arac) if ilk and n else None


def tur_bul(metin):
    s = {t: len(re.findall(r, metin.lower())) for t, r in TURLER.items()}
    t = max(s, key=s.get)
    return t if s[t] >= 2 else None


def altin(gun, adet):
    aday = collections.defaultdict(list)
    for f in glob.glob(str(OTURUM / "*.jsonl")):
        if time.time() - os.path.getmtime(f) > gun * 86400:
            continue
        r = _oku(f)
        if not r:
            continue
        ilk, son, opus, arac = r
        if opus < 0.8 or arac < 1 or len(son) < 200 or KUSUR.search(son) or not 300 < len(ilk) < 6000:
            continue
        for y in re.findall(r"C:/Projeler/omer-skills/[^\s'\"`)\]]+?\.md", ilk):  # istem görev dosyasına yönlendiriyor: içeriği ekle ki vaka tek başına çözülsün
            p = Path(y)
            if p.is_file() and "DEVAM-KURALI" not in y:
                ilk = ilk[:600] + "\n\n[GÖREV DOSYASI " + p.name + "]\n" + p.read_text(encoding="utf-8", errors="ignore")[:2400]
                break
        else:
            if re.search(r"(?i)görev dosyası|DEVAM-KURALI", ilk):
                continue  # çözülemeyen yönlendirme: vaka tek başına anlaşılmaz
        t = tur_bul(ilk)
        if t:
            aday[t].append({"id": Path(f).stem[:8], "tur": t, "girdi": ilk[:3000], "referans": son[:3000], "arac": arac})
    DIZIN.mkdir(exist_ok=True)
    cikti = []
    for t, l in aday.items():  # küçükten büyüğe sırala, eşit aralıklı seç: ucuz çözülebilir vakalar öne
        l.sort(key=lambda x: x["arac"])
        cikti += [l[i * len(l) // adet] for i in range(min(adet, len(l)))]
    ALTIN.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in cikti) + "\n", encoding="utf-8")
    return {t: min(adet, len(l)) for t, l in aday.items()}, {t: len(l) for t, l in aday.items()}


PUAN = re.compile(r"PUAN\s*[:=]\s*(\d{1,3})")


def olc(tur, adet):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ucretsiz_havuz as uh
    vakalar = [json.loads(l) for l in ALTIN.read_text(encoding="utf-8").splitlines() if l.strip()]
    sayac, yazilan = collections.Counter(), 0
    for v in vakalar:
        if tur and v["tur"] != tur or sayac[v["tur"]] >= adet:
            continue
        sayac[v["tur"]] += 1
        for _ in range(2):  # durum.json os.replace Windows'ta eşzamanlı süreçle çakışabiliyor (PermissionError); tek tekrar
            try:
                y, kaynak, _l = uh.cagir("yazim", "Aşağıdaki görevi tek yanıtta, somut ve eksiksiz çöz (araç çağıramazsın; ne yapacağını ve çıktıyı yaz).\n\n" + v["girdi"], max_tokens=2500)
                break
            except PermissionError:
                time.sleep(2)
                y = None
        if not y:
            continue
        istem = ("Kör hakem: görev, REFERANS yanıt (puan 100 kabul edilir) ve ADAY yanıt var. Adayı kabul ölçütleri açısından 0-100 puanla "
                 "(referansın kapsamını ve doğruluğunu karşılıyorsa 100). Son satır yalnız: PUAN: <sayı>\n\nGÖREV:\n" + v["girdi"][:2000] +
                 "\n\nREFERANS:\n" + v["referans"][:2000] + "\n\nADAY:\n" + y[:3000])
        pl = []
        try:
            hl = uh.iki_aile("hakem", istem, max_tokens=600)
        except PermissionError:
            time.sleep(2)
            hl = uh.iki_aile("hakem", istem, max_tokens=600)
        for h, hk, aile in hl:
            m = PUAN.findall(h)
            if m:
                pl.append((int(m[-1]), aile))
        puan = sum(p for p, _ in pl) / len(pl) if pl else None
        kay = {"id": v["id"], "tur": v["tur"], "katman": "ucretsiz", "aday": kaynak, "puan": puan, "hakemler": pl,
               "anlasmazlik": (max(p for p, _ in pl) - min(p for p, _ in pl)) if len(pl) > 1 else None, "denk": bool(puan and puan >= 98)}
        with SONUC.open("a", encoding="utf-8") as f:
            f.write(json.dumps(kay, ensure_ascii=False) + "\n")
        if puan is not None and puan < 98:
            with EKSIK.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"id": v["id"], "tur": v["tur"], "adim": "belirsiz", "puan": puan, "kapatma": "ders-dongu / egitim-1 / kombin (elle ayrıştır)", "durum": "acik"}, ensure_ascii=False) + "\n")
        yazilan += 1
    return yazilan


def tablo():
    sat = [json.loads(l) for l in SONUC.read_text(encoding="utf-8").splitlines()] if SONUC.exists() else []
    t = collections.defaultdict(list)
    for s in sat:
        t[s["tur"]].append(s)
    print("tür | ücretsiz denk/ölçülen | ort. puan | hakem anlaşmazlık ort.")
    for k, l in sorted(t.items()):
        p = [x["puan"] for x in l if x["puan"] is not None]
        a = [x["anlasmazlik"] for x in l if x["anlasmazlik"] is not None]
        print(f"{k} | {sum(x['denk'] for x in l)}/{len(l)} | {sum(p) / len(p):.0f}" if p else f"{k} | 0/{len(l)} | -", f"| {sum(a) / len(a):.0f}" if a else "| -")
    kayit = KOK / ".kos/kopru/yonlendir-kayit.jsonl"
    if kayit.exists():
        c = collections.defaultdict(collections.Counter)
        for l in kayit.read_text(encoding="utf-8").splitlines():
            r = json.loads(l)
            c[r["kademe"]][r["sonuc"]] += 1
        print("yönlendirme kaydı (kademe: geçti/kaldı):", {k: f"{v['gecti']}/{v['kaldi']}" for k, v in sorted(c.items())})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", choices=["altin", "olc", "tablo"])
    ap.add_argument("--gun", type=int, default=14)
    ap.add_argument("--adet", type=int, default=5)
    ap.add_argument("--tur")
    a = ap.parse_args()
    if a.komut == "altin":
        print(altin(a.gun, a.adet))
    elif a.komut == "olc":
        print("ölçülen:", olc(a.tur, a.adet))
    else:
        tablo()
