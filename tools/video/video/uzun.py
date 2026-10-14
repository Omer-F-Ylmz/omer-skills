"""VİDEO-3 V2: uzun YouTube videosu Gemini-önce — ≥PARCA sn ise zaman aralıklı istekler (videoMetadata) + birleştirme; kısa olan kisa.izle'ye gider.
Çıktı kisa.izle ile aynı gemini.json şeması, böylece kisa.calistir (katalog → araştırma → tek Claude oturumu) önbellekten devam eder."""
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import kisa
from . import tarama as tr

PARCA = 1200  # sn; 20 dk aralık, düşük çözünürlükte ~120k jeton (ücretsiz flash TPM 250k)
ESZAMAN = 2  # aynı anda aralık isteği; TPM sınırı yüzünden 2
ISTEM = kisa.ISTEM.replace("Bu kısa videoyu (ya da carousel slaytlarını) baştan sona izle",
                           "Bu uzun videonun YALNIZ verilen zaman aralığını izle (zamanları videonun başından say)")
LISTE = ("araclar", "adlar", "teknikler", "linkler", "komutlar", "iddialar")
PENCERE = kisa.PAKET_TAVAN * 2  # metin geçişi pencere boyu (kisa.metin_gec'in tek seferde okuduğu kadar)
ORTUSME = 1000  # pencere sınırında bölünen adı kaçırmamak için
METIN_ISTEM = kisa.METIN_ISTEM + (" Videonun adını koyarak anlattığı teknik, desen ve özellik adlarını da (render/animasyon/mimari tekniği, "
                                  "ürün özelliği ya da modu) videodaki yazımıyla al.")  # VİDEO-3 d3: altın kaçanlarının çoğu adlandırılmış teknik


def araliklar(sure, parca=PARCA):
    """[(başlangıç, bitiş)] sn; son aralık kısa kalırsa (<parca/4) bir öncekine katılır."""
    s = list(range(0, int(sure), parca)) or [0]
    if len(s) > 1 and sure - s[-1] < parca / 4:
        s.pop()
    return [(a, s[i + 1] if i + 1 < len(s) else int(sure) + 1) for i, a in enumerate(s)]


def birlestir(js):
    """Aralık JSON'ları → tek JSON: metinler sırayla, listeler tekrarsız (araç adı tarama.normal ile)."""
    metin = lambda x: "\n".join(map(str, x)) if isinstance(x, list) else str(x)  # noqa: E731 — model bazen dizi döndürüyor
    out = {k: "\n".join(metin(j.get(k, "")) for j in js) for k in ("konusma_ozet", "ekran_metni")}
    for k in LISTE:
        gor, out[k] = set(), []
        for j in js:
            for x in j.get(k, []):
                a = tr.normal(x["ad"] if isinstance(x, dict) else str(x))
                if a not in gor:
                    gor.add(a)
                    out[k].append(x)
    return out


def izle(d, env=None, yeniden=False):
    """→ (gemini.json içeriği, iz); kisa.izle ile aynı önbellek dosyası."""
    d = Path(d)
    sure = json.loads((d / "meta.json").read_text(encoding="utf-8")).get("duration") or 0
    if sure < PARCA * 1.25:
        return kisa.izle(d, env=env, yeniden=yeniden)
    hedef = d / "gemini.json"
    if hedef.is_file() and not yeniden:
        return json.loads(hedef.read_text(encoding="utf-8")), {"onbellek": True}
    key, t = kisa.anahtar(env), time.monotonic()
    paket = (d / "paket.md").read_text(encoding="utf-8")[:kisa.PAKET_TAVAN] if (d / "paket.md").is_file() else ""

    def bir(ar):
        ara = d / f"gemini-{ar[0]}.json"  # aralık önbelleği: kota 429'da kaldığı yerden devam
        if ara.is_file() and not yeniden:
            return tuple(json.loads(ara.read_text(encoding="utf-8")))
        govde = {"contents": [{"parts": [{"fileData": {"fileUri": f"https://www.youtube.com/watch?v={d.name}"},
                                          "videoMetadata": {"startOffset": f"{ar[0]}s", "endOffset": f"{ar[1]}s"}},
                                         {"text": f"paket.md:\n{paket}\n\nAralık: {ar[0]}–{ar[1]} sn.\n{ISTEM}"}]}],
                 "generationConfig": {"responseMimeType": "application/json", "responseSchema": kisa.SEMA, "temperature": 0.2,
                                      "mediaResolution": "MEDIA_RESOLUTION_LOW"}}
        s = kisa._uret(govde, key, time.monotonic())
        ara.write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
        return s

    with ThreadPoolExecutor(ESZAMAN) as ex:
        sonuc = list(ex.map(bir, araliklar(sure)))
    j = birlestir([s[0] for s in sonuc])
    var = {tr.normal(a["ad"]) for a in j["araclar"]}  # kisa.izle ile aynı: adlar listesi araçlara tekrarsız katılır
    for a, nd in [(a, "(yalnız adı geçiyor)") for a in j.pop("adlar")] + [(a, "(teknik)") for a in j.pop("teknikler")]:
        if tr.normal(a) not in var and not kisa.KOD.search(a):
            var.add(tr.normal(a))
            j["araclar"].append({"ad": a, "ne_dedi": nd, "zaman": "paket"})
    iz = {"model": sorted({s[1]["model"] for s in sonuc}), "sure": round(time.monotonic() - t, 1),
          "jeton": sum(s[1]["jeton"] or 0 for s in sonuc), "aralik": len(sonuc)}
    hedef.write_text(json.dumps({**j, "_iz": iz}, ensure_ascii=False, indent=1), encoding="utf-8")
    return j, iz


def pencereler(metin, boy=PENCERE, ortusme=ORTUSME):
    return [metin[i:i + boy] for i in range(0, max(len(metin) - ortusme, 1), boy - ortusme)]


def metin_gec(d, env=None, yeniden=False):
    """kisa.metin_gec PENCERE'de kesiyor (uzun videoda paket.md 25–180k): paket pencerelere bölünür, her pencereye aynı istem, adlar birleşir.
    İstem kisa'nınkine ek olarak adlandırılmış teknikleri de ister; önbellek gemini-metin-uzun.json."""
    d = Path(d)
    metin = (d / "paket.md").read_text(encoding="utf-8") if (d / "paket.md").is_file() else ""
    hedef = d / "gemini-metin-uzun.json"
    if hedef.is_file() and not yeniden:
        return json.loads(hedef.read_text(encoding="utf-8"))
    key, t = kisa.anahtar(env), time.monotonic()
    aday = [a["ad"] for a in kisa.sozluk_tara(d, {})]

    def bir(p):  # pencerede geçen adayları ver: istem kısa kalır
        ad = [a for a in aday if a.casefold() in p.casefold()]
        govde = {"contents": [{"parts": [{"text": f"{METIN_ISTEM}\n\nADAYLAR: {', '.join(ad) or 'yok'}\n\n{p}"}]}],
                 "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1,
                                      "responseSchema": {"type": "OBJECT", "required": ["adlar"], "properties": {"adlar": {"type": "ARRAY", "items": {"type": "STRING"}}}}}}
        return kisa._uret(govde, key, time.monotonic())

    with ThreadPoolExecutor(ESZAMAN) as ex:
        sonuc = list(ex.map(bir, pencereler(metin)))
    gor, adlar = set(), []
    for a in (a for s in sonuc for a in s[0]["adlar"]):
        if a.strip() and not kisa.KOD.search(a) and tr.normal(a) not in gor:
            gor.add(tr.normal(a))
            adlar.append(a)
    j = {"adlar": adlar, "aday": len(aday), "_iz": {"model": sorted({s[1]["model"] for s in sonuc}), "sure": round(time.monotonic() - t, 1),
                                                     "jeton": sum(s[1]["jeton"] or 0 for s in sonuc), "pencere": len(sonuc)}}
    hedef.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    return j


def son(d, g):
    """Birleşik Gemini çıktısına son geçiş (yerinde): katalog sözlüğünün pakette bulduğu adlar doğrudan eklenir (kisa d9 deseni) ·
    istem yankısı düşer — VİDEO-3 d4: izleme istemindeki örnek adlar (Python, pip, PyTorch…) pakette geçmeden araç olarak dönüyordu."""
    p = (Path(d) / "paket.md").read_text(encoding="utf-8").casefold() if (Path(d) / "paket.md").is_file() else ""
    ham, istem = tr.normal(p), tr.normal(ISTEM + METIN_ISTEM)
    pakette = lambda a: re.search(rf"\b{re.escape(a.casefold())}\b", p) if len(tr.normal(a)) <= 4 else tr.normal(a) in ham  # noqa: E731 — "pip" ⊂ "pipeline" sayılmaz
    g["araclar"] = [a for a in g["araclar"] + kisa.sozluk_tara(d, g) if not (tr.normal(a["ad"]) in istem and not pakette(a["ad"]))]
    return g


def rapor_md(adlar, aciklama_link, urller, komutlar):
    """altin.puan'ın okuduğu en küçük rapor (Adaylar · Açıklama bağlantıları · URL'ler · Kurulum/komutlar); iki kola eşit uygulanır."""
    h = lambda s: str(s).replace("|", "/").replace("\n", " ")  # noqa: E731
    return "\n".join(["## Adaylar", "| ad | tür |", "|---|---|", *[f"| {h(a)} | araç |" for a in adlar],
                      "## Açıklama bağlantıları", *[f"- {u}" for u in aciklama_link],
                      "## URL'ler", "| url |", "|---|", *[f"| {h(u)} |" for u in urller],
                      "## Kurulum/komutlar", "| komut |", "|---|", *[f"| {h(k)} |" for k in komutlar], ""])
