"""ENVANTER-2: yetenek kataloğunda iş tarifiyle arama — iki aşama: geniş aday listesi (bu betik) → seçimi okuyan model yapar.
python tools/katalog_ara.py "<iş tarifi>" [--aday N] [--tur skill|ajan|mcp|cli|kutuphane|arac|plugin]
  varsayılan: BM25 ilk ADAY + her türden en az TABAN aday, türe göre gruplu kompakt satır (ad · ne işe yarar · nasıl çağrılır)
  --esik [--oran 0.3] [--tam]: eski eşik listesi (tek aşama, kısa ama geri çağırması düşük)
BM25 (ad alanı 2x, 5 harf önek) + TR/EN eş anlam sözlüğü; kapalı (override off) skill'ler sona itilir.
"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

_YAN = Path(__file__).resolve().parent / "yetenek.jsonl"  # yetenek-getir skill klasöründeki kopya
KATALOG = _YAN if _YAN.exists() else Path(__file__).resolve().parents[1] / "docs" / "katalog" / "yetenek.jsonl"
# TR → EN (ve tersi) eş anlamlar; sorgu genişletmesi için. Kayıp örneklerle büyür.
ES = {
    "hata": "bug error debug hata", "guvenlik": "security vulnerability guvenlik",
    "acik": "vulnerability security", "veritabani": "database db sql", "sorgu": "query sql",
    "yavas": "slow performance", "performans": "performance profiling", "dagitim": "deploy deployment release",
    "gorsel": "image visual screenshot", "resim": "image", "video": "video ffmpeg", "ses": "audio voice",
    "belge": "document docx pdf", "rapor": "report", "sunum": "presentation slides pptx", "tablo": "table xlsx spreadsheet",
    "cevir": "translate translation convert", "donustur": "convert", "markdown": "markdown markitdown",
    "karanlik": "dark theme", "hizlandir": "optimize slow index", "mesaj": "message messages",
    "deney": "experiment ab testing","ozet": "summary summarize", "ozetle": "summarize summary",
    "arama": "search", "ara": "search find", "kazi": "scrape crawl", "tarayici": "browser playwright",
    "tasarim": "design ui", "arayuz": "ui interface frontend", "bilesen": "component", "renk": "color palette",
    "yazi": "font typography text", "animasyon": "animation motion", "oyun": "game", "mod": "mod modding",
    "model": "model 3d mesh", "kimlik": "auth identity login", "giris": "login auth", "oturum": "session",
    "sir": "secret credential", "sifre": "password secret", "lisans": "license", "bagimlilik": "dependency package",
    "paket": "package", "kurulum": "install setup", "yapilandirma": "config configuration settings",
    "kanca": "hook hooks", "ajan": "agent subagent", "beceri": "skill", "eklenti": "plugin",
    "zamanla": "schedule cron", "otomasyon": "automation workflow n8n", "eposta": "email mail",
    "bildirim": "notification alert", "log": "log logging logs", "gunluk": "log logs", "izle": "monitor observability",
    "maliyet": "cost spend token", "jeton": "token tokens cost", "baglam": "context", "bellek": "memory",
    "hafiza": "memory", "grafik": "chart graph", "harita": "map graph", "kod": "code", "inceleme": "review",
    "incele": "review audit", "denetim": "audit", "birlestir": "merge", "cakisma": "conflict merge",
    "dal": "branch git", "surum": "version release", "web": "web website", "site": "website web",
    "mobil": "mobile ios android", "sozlesme": "contract legal", "hukuk": "legal law", "reklam": "ads advertising",
    "pazarlama": "marketing", "fiyat": "pricing price", "musteri": "customer", "yuk": "load",
    "erisilebilirlik": "accessibility a11y", "seo": "seo meta", "kutuphane": "library", "indir": "download",
    "altyazi": "subtitle caption transcript", "kilit": "deadlock lock", "deadlock": "kilitlenme lock",
    "dogrula": "validation validate verify", "uctan": "e2e end-to-end", "orneklem": "sample size statistics experiment testing",
    "kirili": "flaky intermittent", "flaky": "flaky intermittent", "jwt": "jwt token", "dokum": "transcript", "pdf": "pdf document",
}
ORAN, GENIS, UZUN, ILK = 0.3, 0.5, 30, 5
KAVRAM, SIRA, BAYAG = 0.5, 3, 0.05
# d8 ızgarası (altın küme ayar 20 iş): ilk 80 + tür tabanı 10 → aşama-1 geri çağırma ayar 0.993 / sınama 1.000, ~3.8k jeton
ADAY, TABAN, TAVAN = 80, 10, 300
DURAK = set("ile ve veya icin bir bu su da de mi ne gibi olarak the and or with for to of in on an my is are how".split())
GRUP = {"skill": "skill", "ajan": "ajan", "mcp": "mcp", "plugin": "plugin", "cli": "cli",
        "kutuphane": "kütüphane", "arac": "bizim betik"}
# katalog_yenile'nin standart cagri kalıbı: satırda ad tekrarı yerine grup başlığında bir kez yazılır
CAGRI = {"skill": "Skill {ad}", "ajan": "Agent {ad} (listede yoksa Skill ajan-getir)", "mcp": "ToolSearch '{ad}' → mcp__{ad}__*",
         "cli": "Bash: {ad} --help", "arac": "python tools/{ad}.py"}
TR = str.maketrans("çğıöşüÇĞİÖŞÜâî", "cgiosucgiosuai")


def kelimeler(s):
    s = re.sub(r"\ba/b\b", "ab", s.lower())  # "A/B test" tek harflere bölünüp kaybolmasın
    t = [w for w in re.split(r"[^a-z0-9]+", s.translate(TR)) if len(w) > 1]
    # 5 harf önek: TR ekleri ve EN çoğul/çekim (tablosunda/tablo, deadlocks/deadlock) için kaba kök
    return t + [w[:5] + "~" for w in t if len(w) >= 5]


def ileri(t):
    return [e for w in t for k, v in ES.items() if w.startswith(k) and len(w) - len(k) <= 4 for e in v.split()]


def genislet(q):
    """Sorgu terimi → ağırlık: kullanıcının kelimesi 1, ES açılımı GENIS (açılımlar tepe puanı şişirmesin)."""
    t = kelimeler(q)
    return {w: GENIS for w in kelimeler(" ".join(ileri(t)))} | {w: 1.0 for w in t}


def tetik(metin, n=120):
    """Boş tetik için deterministik TR+EN anahtar: ES ileri (TR→EN) + geri (EN→TR) eşleşmeleri."""
    t = [w for w in kelimeler(metin) if not w.endswith("~")]
    ek = ileri(t) + [k for k, v in ES.items() if set(v.split()) & set(t)]
    return " ".join(dict.fromkeys(e for e in ek if e not in t))[:n].rsplit(" ", 1)[0] if ek else ""


def puanla(q, tur=None, satirlar=None):
    """BM25 sıralı tüm eşleşmeler [(puan, kavram kapsama, kayıt)] + gereken kavram sayısı."""
    rows = satirlar or [json.loads(s) for s in KATALOG.read_text(encoding="utf8").splitlines()]
    if tur:
        rows = [o for o in rows if o["tur"] == tur]
    docs = [kelimeler(o["ad"]) * 2 + kelimeler(f"{o['is']} {o.get('tetik', '')} {o['metin']}") for o in rows]
    N, ort = len(docs), sum(map(len, docs)) / max(len(docs), 1)
    df = Counter(w for d in docs for w in set(d))
    sorgu = {w: v for w, v in genislet(q).items() if w not in DURAK}
    # kavram = kullanıcının her kelimesi (+önek, +ES açılımı); belgelerin >%5'inde geçen kelime kavram sayılmaz
    kavram = [set(kelimeler(w) + kelimeler(" ".join(ileri([w])))) for w in kelimeler(q)
              if not w.endswith("~") and df[w] < BAYAG * N and w not in DURAK]
    gerek = math.ceil(KAVRAM * len(kavram))
    puan = []
    for o, d in zip(rows, docs):
        tf, s = Counter(d), 0.0
        for w, qn in sorgu.items():
            if tf[w]:
                idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
                s += qn * idf * tf[w] * 2.2 / (tf[w] + 1.2 * (0.25 + 0.75 * len(d) / ort))
        if "kapal" in o["durum"]:
            s *= 0.5
        if s > 0:
            # kapsama tetik HARİÇ sayılır: deterministik tetik ES açılımı taşır ("video" → "ffmpeg"), her kaydı kavramlı gösterir
            ham = set(kelimeler(f"{o['ad']} {o['is']} {o['metin']}"))
            puan.append((s, sum(1 for c in kavram if ham & c), o))
    puan.sort(key=lambda x: -x[0])
    return puan, gerek


def ara(q, tur=None, oran=ORAN, satirlar=None):
    """İlgili sayılan HER kayıt: puanı en iyinin `oran` katını geçenler (sabit ilk-N değil; Ömer 21:33)."""
    puan, gerek = puanla(q, tur, satirlar)
    tepe = puan[0][0] if puan else 0
    # tek ortak kelimeyle gelen gürültü ("video", "hata") elenir: ilk SIRA kayıt ya da ham metinde kavramların ≥KAVRAM oranı
    return [o for i, (s, kap, o) in enumerate(puan) if s >= oran * tepe and (i < SIRA or kap >= gerek)]


def aday(q, n=ADAY, tur=None, satirlar=None, taban=TABAN):
    """Aşama-1: BM25 ilk n + ilk TAVAN içinden her türe en az `taban` kayıt (plugin/cli gibi az puanlı türler kaybolmasın)."""
    p = [o for _, _, o in puanla(q, tur, satirlar)[0]]
    sec, say = p[:n], Counter(o["tur"] for o in p[:n])
    for o in p[n:TAVAN]:
        if say[o["tur"]] < taban:
            sec.append(o)
            say[o["tur"]] += 1
    return sec


def main():
    a = sys.argv[1:]
    tur = a[a.index("--tur") + 1] if "--tur" in a else None
    oran = float(a[a.index("--oran") + 1]) if "--oran" in a else ORAN
    n = int(a[a.index("--aday") + 1]) if "--aday" in a else ADAY
    q = " ".join(x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--tur", "--oran", "--aday")))
    sonuc = ara(q, tur, oran) if "--esik" in a else aday(q, n, tur)
    gruplar = {t: [o for o in sonuc if o["tur"] == t] for t in GRUP if any(o["tur"] == t for o in sonuc)}
    uzun = len(sonuc) > UZUN and "--esik" in a and "--tam" not in a
    print("<aday-listesi>")  # Headroom tag_protector özel etiketli bloğu sıkıştırmaz: liste tam görünür
    print(f"{len(sonuc)} kayıt · " + " · ".join(f"{GRUP[t]} {len(v)}" for t, v in gruplar.items()))
    for t, v in gruplar.items():
        print(f"## {GRUP[t]} ({len(v)})" + (f" · çağrı: {CAGRI[t].format(ad='<ad>')}" if t in CAGRI else ""))
        satir = {}  # aynı açıklamalı kayıtlar tek satır: tekrar satırı okuyucuda gizlenmesin
        for o in v[:ILK if uzun else None]:
            c = "" if o["cagri"] == CAGRI.get(t, "").format(ad=o["ad"]) else f" · {o['cagri'][:60]}"
            satir.setdefault(f"{(o['is'] or o['metin'])[:110]}{c}", []).append(o["ad"])
        for m, adlar in satir.items():
            print(f"{', '.join(adlar)} · {m}")
    if uzun:
        print(f"… grup başına ilk {ILK}; hepsi için --tam")
    print("</aday-listesi>")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
