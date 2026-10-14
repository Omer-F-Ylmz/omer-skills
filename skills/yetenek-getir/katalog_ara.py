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
    "odeme": "payment checkout billing", "kapora": "payment deposit", "abonelik": "subscription billing",
    "kirili": "flaky intermittent", "flaky": "flaky intermittent", "jwt": "jwt token", "dokum": "transcript", "pdf": "pdf document",
}
ORAN, GENIS, UZUN, ILK = 0.3, 0.5, 30, 5
KAVRAM, SIRA, BAYAG = 0.5, 3, 0.05
# d8 ızgarası (altın küme ayar 20 iş): ilk 80 + tür tabanı 10 → aşama-1 geri çağırma ayar 0.993 / sınama 1.000, ~3.8k jeton
ADAY, TABAN, TAVAN = 80, 10, 300
DURAK = set("ile ve veya icin bir bu su da de mi ne gibi olarak the and or with for to of in on an my is are how".split())
GRUP = {"skill": "skill", "ajan": "ajan", "mcp": "mcp", "plugin": "plugin", "cli": "cli",
        "kutuphane": "kütüphane", "arac": "bizim betik", "ogrenim": "öğrenim"}
_OGR = Path(__file__).resolve().parent / "ogrenim.jsonl"
OGRENIM = _OGR if _OGR.exists() else Path(__file__).resolve().parents[1] / "docs" / "katalog" / "ogrenim.jsonl"
OGR_N = 8  # varsayılan çıktıda öğrenim grubu tavanı (kompakt)
# katalog_yenile'nin standart cagri kalıbı: satırda ad tekrarı yerine grup başlığında bir kez yazılır
CAGRI = {"skill": "Skill {ad}", "ajan": "Agent {ad} (listede yoksa Skill ajan-getir)", "mcp": "ToolSearch '{ad}' → mcp__{ad}__*",
         "cli": "Bash: {ad} --help", "arac": "python tools/{ad}.py"}
TR = str.maketrans("çğıöşüÇĞİÖŞÜâî", "cgiosucgiosuai")
# PLAN-KUR-2 yığın süzgeci: ad → (aile, desen). Aynı ailede projenin yığınında olmayan teknolojiye bağlı araç elenir
# (ENVANTER-3: Astro işine React gerektiren araç önerildi); ailesiz (three) yalnız tanınır.
YIGIN = {
    "react": ("fe", r"\breact\b|next\.?js|\bjsx\b|\bremix\b"), "vue": ("fe", r"\bvue|\bnuxt"), "svelte": ("fe", r"svelte"),
    "angular": ("fe", r"\bangular"), "astro": ("fe", r"\bastro\b"), "solid": ("fe", r"solid\.?js"), "qwik": ("fe", r"\bqwik"),
    "django": ("be", r"django"), "flask": ("be", r"\bflask"), "fastapi": ("be", r"fastapi"),
    "node": ("be", r"\bexpress\b|express\.js|node\.?js|nestjs|next\.?js"),
    "aspnet": ("be", r"asp\.?net|\.net\b|dotnet|\bc#|blazor|ef ?core|^dn-|\bdn-"), "rails": ("be", r"\brails\b"),
    "laravel": ("be", r"laravel"), "spring": ("be", r"spring ?boot"),
    "flutter": ("mobil", r"flutter|\bdart\b"), "rn": ("mobil", r"react native"), "ios": ("mobil", r"swiftui|\bswift\b"),
    "android": ("mobil", r"kotlin|jetpack compose"),
    "unity": ("motor", r"\bunity\b"), "godot": ("motor", r"godot"), "unreal": ("motor", r"unreal"), "roblox": ("motor", r"roblox|luau"),
    "three": ("", r"three\.?js|\bthree\b"),
}
YIGIN_IZ = (("astro.config.*", "astro"), ("*.csproj", "asp.net"), ("pubspec.yaml", "flutter"), ("project.godot", "godot"),
            ("ProjectSettings", "unity"))


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


def yigin(q, cwd="."):
    """İş metni + cwd proje dosyalarından (package.json bağımlılıkları, işaret dosyaları) yığın adları."""
    d, t = Path(cwd), q.lower()
    try:
        p = json.loads((d / "package.json").read_text(encoding="utf8"))
        t += " " + " ".join({**p.get("dependencies", {}), **p.get("devDependencies", {})})
    except (OSError, ValueError):
        pass
    t += "".join(f" {ad}" for desen, ad in YIGIN_IZ if any(d.glob(desen)))
    for f in ("pyproject.toml", "requirements.txt", "Gemfile", "composer.json"):
        try:
            t += " " + (d / f).read_text(encoding="utf8", errors="ignore").lower()
        except OSError:
            pass
    return [k for k, (_, r) in YIGIN.items() if re.search(r, t)]


def kurulu(o):
    """Bu makinede çağrılabilir: CC/ikisi/kurulu (kapalı değil) ya da cwd'de dosyası olan bizim betik."""
    d = o["durum"]
    if d == "repo":
        return Path("tools", f"{o['ad']}.py").exists()
    return "kapal" not in d and (d.startswith(("CC", "ikisi")) or d == "kurulu")


def suz(rows, yg):
    """(kalan, yığınla elenen sayısı, kurulu olmayanlar). Yığın bilinmiyorsa yığın elemesi yok."""
    aile = {YIGIN[k][0] for k in yg} - {""}
    kal, elen, yok = [], 0, []
    for o in rows:
        if not kurulu(o):
            yok.append(o)
            continue
        m, ad = f"{o['ad']} {o['is']}".lower(), o["ad"].lower()
        # adında yığın dışı teknoloji (ecc:fastapi-reviewer) ya da açıklamasında aynı aileden yabancı teknoloji
        yab = any(k not in yg and re.search(r, ad) for k, (_, r) in YIGIN.items()) if yg else False
        if (yab or any(f == a and k not in yg and re.search(r, m) for a in aile for k, (f, r) in YIGIN.items())) and \
                not any(re.search(YIGIN[k][1], m) for k in yg):
            elen += 1
            continue
        kal.append(o)
    return kal, elen, yok


def ogrenimler():
    """Öğrenim satırları katalog kaydı biçiminde; ayrı derlem (araç sıralamasının BM25 istatistiği değişmesin)."""
    if not OGRENIM.exists():
        return []
    return [{"ad": "", "tur": "ogrenim", "is": o["is"], "metin": f"{o['ne']} {o.get('araclar', '')} {o.get('alan', '')}",
             "cagri": o["kaynak"], "durum": "", "ne": o["ne"]}
            for o in map(json.loads, filter(str.strip, OGRENIM.read_text(encoding="utf8").splitlines()))]


def ogrenim_ara(q, n=OGR_N):
    ogr = ogrenimler()
    return ara(q, None, ORAN, ogr)[:n] if ogr else []


def main():
    a = sys.argv[1:]
    tur = a[a.index("--tur") + 1] if "--tur" in a else None
    oran = float(a[a.index("--oran") + 1]) if "--oran" in a else ORAN
    n = int(a[a.index("--aday") + 1]) if "--aday" in a else ADAY
    q = " ".join(x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--tur", "--oran", "--aday")))
    if tur == "ogrenim":
        sonuc = ogrenim_ara(q, n if "--aday" in a else 3 * OGR_N)
    else:
        # PLAN-KUR-2 (Ömer 14 Eki 06:38): kurulu olmayan araç listelenmez; yığınla uyumsuz araç elenir
        sonuc, elen, yok = suz(ara(q, tur, oran) if "--esik" in a else aday(q, n, tur), yigin(q))
        bas = f"elendi: {elen} (yığın) · {len(yok)} kurulu değil\n"
        sonuc += [] if tur else ogrenim_ara(q)
    listele(sonuc, len(sonuc) > UZUN and "--esik" in a and "--tam" not in a, bas if tur != "ogrenim" else "")


def listele(sonuc, uzun=False, bas=""):
    # Headroom tag_protector etiketli bloğu sıkıştırmaz; ```text çiti, ERROR/DEBUG'lı açıklamalarda içeriğin
    # LOG sayılıp (etiket korumasız yol) kırpılmasını önler (karma yol önce etiketi korur)
    print(f"<aday-listesi>\n{bas}{metin(sonuc, uzun)}\n</aday-listesi>")


def metin(sonuc, uzun=False):
    """Türe göre gruplu ```text çitli liste (katalog_kanca da kullanır)."""
    gruplar = {t: [o for o in sonuc if o["tur"] == t] for t in GRUP if any(o["tur"] == t for o in sonuc)}
    s = ["```text", f"{len(sonuc)} kayıt · " + " · ".join(f"{GRUP[t]} {len(v)}" for t, v in gruplar.items())]
    no = 0  # sıra no öneki: önceki çıktıyla aynı satır dizisi Headroom'da "[↑NL same as msg]" diye katlanmasın
    for t, v in gruplar.items():
        s.append(f"## {GRUP[t]} ({len(v)})" + (f" · çağrı: {CAGRI[t].format(ad='<ad>')}" if t in CAGRI else ""))
        if t == "ogrenim":
            for o in v:
                no += 1
                s.append(f"{no}. {o['ne']} · iş: {o['is']} · {o['cagri']}")
            continue
        satir = {}  # aynı açıklamalı kayıtlar tek satır: tekrar satırı okuyucuda gizlenmesin
        for o in v[:ILK if uzun else None]:
            c = "" if o["cagri"] == CAGRI.get(t, "").format(ad=o["ad"]) else f" · {o['cagri'][:60]}"
            satir.setdefault(f"{(o['is'] or o['metin'])[:110]}{c}", []).append(o["ad"])
        for m, adlar in satir.items():
            no += 1
            s.append(f"{no}. {', '.join(adlar)} · {m}")
    if uzun:
        s.append(f"… grup başına ilk {ILK}; hepsi için --tam")
    return "\n".join(s + ["```"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
