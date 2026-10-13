"""ENVANTER-2: yetenek kataloğunda iş tarifiyle arama → en iyi 8 araç, tek satır/sonuç (≤1.5k kr).
python tools/katalog_ara.py "<iş tarifi>" [--tur skill|ajan|mcp|cli|kutuphane|arac|plugin] [--n 8]
BM25 (ad alanı 2x, 5 harf önek) + TR/EN eş anlam sözlüğü; kapalı (override off) skill'ler sona itilir.
"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

KATALOG = Path(__file__).resolve().parents[1] / "docs" / "katalog" / "yetenek.jsonl"
# TR → EN (ve tersi) eş anlamlar; sorgu genişletmesi için. Kayıp örneklerle büyür.
ES = {
    "hata": "bug error debug hata", "guvenlik": "security vulnerability guvenlik",
    "acik": "vulnerability security", "veritabani": "database db sql", "sorgu": "query sql",
    "yavas": "slow performance", "performans": "performance profiling", "dagitim": "deploy deployment release",
    "gorsel": "image visual screenshot", "resim": "image", "video": "video ffmpeg", "ses": "audio voice",
    "belge": "document docx pdf", "rapor": "report", "sunum": "presentation slides pptx", "tablo": "table xlsx spreadsheet",
    "cevir": "translate translation", "ozet": "summary summarize", "ozetle": "summarize summary",
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
    "dogrula": "validation validate verify", "uctan": "e2e end-to-end", "orneklem": "sample size statistics",
    "kirili": "flaky intermittent", "flaky": "flaky intermittent", "jwt": "jwt token", "dokum": "transcript", "pdf": "pdf document",
}
TR = str.maketrans("çğıöşüÇĞİÖŞÜâî", "cgiosucgiosuai")


def kelimeler(s):
    t = [w for w in re.split(r"[^a-z0-9]+", s.lower().translate(TR)) if len(w) > 1]
    # 5 harf önek: TR ekleri ve EN çoğul/çekim (tablosunda/tablo, deadlocks/deadlock) için kaba kök
    return t + [w[:5] + "~" for w in t if len(w) > 5]


def genislet(q):
    t = kelimeler(q)
    return t + [e for w in t for k, v in ES.items() if w.startswith(k) and len(w) - len(k) <= 4 for e in v.split()]


def ara(q, tur=None, n=8, satirlar=None):
    rows = satirlar or [json.loads(s) for s in KATALOG.read_text(encoding="utf8").splitlines()]
    if tur:
        rows = [o for o in rows if o["tur"] == tur]
    docs = [kelimeler(o["ad"]) * 2 + kelimeler(f"{o['is']} {o.get('tetik', '')} {o['metin']}") for o in rows]
    N, ort = len(docs), sum(map(len, docs)) / max(len(docs), 1)
    df = Counter(w for d in docs for w in set(d))
    sorgu = Counter(genislet(q))
    puan = []
    for o, d in zip(rows, docs):
        tf, s = Counter(d), 0.0
        for w, qn in sorgu.items():
            if tf[w]:
                idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
                s += qn * idf * tf[w] * 2.2 / (tf[w] + 1.2 * (0.25 + 0.75 * len(d) / ort))
        if "kapal" in o["durum"]:
            s *= 0.5
        puan.append((s, o))
    return [o for s, o in sorted(puan, key=lambda x: -x[0])[:n] if s > 0]


def main():
    a = sys.argv[1:]
    tur = a[a.index("--tur") + 1] if "--tur" in a else None
    n = int(a[a.index("--n") + 1]) if "--n" in a else 8
    q = " ".join(x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--tur", "--n")))
    for o in ara(q, tur, n):
        print(f"{o['tur']} · {o['ad']} · {(o['is'] or o['metin'])[:110]} · {o['cagri'][:50]}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
