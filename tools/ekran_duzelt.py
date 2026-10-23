"""ASR düzeltici: ekranda yazılı araç/komut adı ASR'de başka duyulduysa ekrandakini alır (yalnız düzeltme; initial_prompt'a değil).

Aday = atlas kart adları (tek parça, ≥5 karakter) ∩ aynı videonun ekran metni. Videoda hiç görünmeyen ad hiçbir kelimeyi değiştiremez.
Kullanım: import ekran_duzelt as ed; ed.duzelt(metin, ekran_metni)
"""
import difflib
import json
import re
from functools import lru_cache
from pathlib import Path

from ekran_yazi import kat

KART = Path(__file__).resolve().parent.parent / "docs/atlas/kart.jsonl"
DERIN = Path(__file__).resolve().parent.parent / "docs/video-tarama/derin"
ESIK = 0.8  # kat() sonrası benzerlik; ≥5 karakterli adlarda 1 harf farkı kabul, 2 harf farkı değil


@lru_cache(1)
def sozluk():
    """{katlanmış ad: yazılış}; yalnız harf/rakam/tire içeren, tek parça adlar."""
    s = {}
    for satir in KART.read_text(encoding="utf-8").splitlines():
        try:
            ad = json.loads(satir)["ad"]
        except (ValueError, KeyError):
            continue
        k = kat(ad)
        if len(k) >= 5 and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.\-]*", ad):
            s.setdefault(k, ad)
    return s


def adaylar(ekran_metni):
    """Ekranda geçen sözlük adları {katlanmış: yazılış}. Tire/boşlukla bölünen adlar için bitişik kelime çifti de denenir."""
    jetonlar = re.findall(r"[A-Za-z0-9ÇĞİÖŞÜçğıöşü]+(?:[-.][A-Za-z0-9]+)*", ekran_metni)
    kum = {kat(j) for j in jetonlar} | {kat(a + b) for a, b in zip(jetonlar, jetonlar[1:])}
    return {k: ad for k, ad in sozluk().items() if k in kum}


@lru_cache(1)
def yaygin(min_video=3):
    """Derin dökümlerde ≥min_video videoda geçen katlanmış kelimeler: gerçek kelime sayılır, ad diye değiştirilmez (project, quick, usage)."""
    sayac = {}
    for p in DERIN.glob("*.json"):
        try:
            seg = json.loads(p.read_text(encoding="utf-8")).get("transkript") or []
        except ValueError:
            continue
        for w in {kat(x) for x in re.findall(r"\w+", " ".join(s["t"] for s in seg))}:
            sayac[w] = sayac.get(w, 0) + 1
    return {w for w, n in sayac.items() if n >= min_video}


def en_yakin(k, cand):
    en, oran = None, 0.0
    for c in cand:
        r = difflib.SequenceMatcher(None, k, c).ratio()
        if r > oran:
            en, oran = c, r
    return en, oran


def duzelt(metin, ekran_metni):
    """(düzeltilmiş metin, [(eski, yeni)]). Kelime ya da bitişik iki kelime, ekran adına ≥ESIK benziyor ama eşit değilse değişir."""
    cand = adaylar(ekran_metni)
    if not cand:
        return metin, []
    kelimeler = list(re.finditer(r"[\w]+(?:'[\w]+)?", metin))
    yg = yaygin()
    degisim, ops, i = [], [], 0
    while i < len(kelimeler):
        yeni = None
        if kat(kelimeler[i].group().split("'")[0]) in cand:  # ad zaten doğru
            i += 1
            continue
        for n in (2, 1):  # önce iki kelime ("agent reach" → agent-reach)
            if i + n > len(kelimeler):
                continue
            parca = [kelimeler[i + j].group().split("'")[0] for j in range(n)]
            k = kat("".join(parca))
            if len(k) < 5 or k in cand or all(kat(p) in yg for p in parca):  # her parça yaygın kelimeyse gerçek konuşmadır
                continue
            if n == 2 and any(len(kat(p)) < 3 for p in parca):
                continue
            c, oran = en_yakin(k, cand)
            # önek ilişkisi ek/çoğul (agent/agents, Claude/Claude'un): düzeltme değil; uzunluk farkı 1'i aşarsa başka kelimedir
            if c and oran >= ESIK and abs(len(c) - len(k)) <= 1 and not (c.startswith(k) or k.startswith(c)):
                yeni = (n, cand[c], " ".join(kelimeler[i + j].group() for j in range(n)))
                break
        if yeni:
            n, ad, eski = yeni
            son = kelimeler[i + n - 1]
            sonek = son.group().partition("'")[1:]  # Claude'un → ad + 'un
            degisim.append((kelimeler[i].start(), son.end(), ad + "".join(sonek)))
            ops.append((eski, ad))
            i += n
        else:
            i += 1
    for bas, son, yz in reversed(degisim):
        metin = metin[:bas] + yz + metin[son:]
    return metin, ops
