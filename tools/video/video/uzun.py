"""VİDEO-3 V2: uzun YouTube videosu Gemini-önce — ≥PARCA sn ise zaman aralıklı istekler (videoMetadata) + birleştirme; kısa olan kisa.izle'ye gider.
Çıktı kisa.izle ile aynı gemini.json şeması, böylece kisa.calistir (katalog → araştırma → tek Claude oturumu) önbellekten devam eder."""
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import kisa
from . import tarama as tr

PARCA = 1200  # sn; 20 dk aralık, düşük çözünürlükte ~120k jeton (ücretsiz flash TPM 250k)
ESZAMAN = 2  # aynı anda aralık isteği; TPM sınırı yüzünden 2
ISTEM = kisa.ISTEM.replace("Bu kısa videoyu (ya da carousel slaytlarını) baştan sona izle",
                           "Bu uzun videonun YALNIZ verilen zaman aralığını izle (zamanları videonun başından say)")
LISTE = ("araclar", "adlar", "linkler", "komutlar", "iddialar")


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
    j["araclar"] += [{"ad": a, "ne_dedi": "(yalnız adı geçiyor)", "zaman": "paket"} for a in j.pop("adlar")
                     if tr.normal(a) not in var and not kisa.KOD.search(a)]
    iz = {"model": sorted({s[1]["model"] for s in sonuc}), "sure": round(time.monotonic() - t, 1),
          "jeton": sum(s[1]["jeton"] or 0 for s in sonuc), "aralik": len(sonuc)}
    hedef.write_text(json.dumps({**j, "_iz": iz}, ensure_ascii=False, indent=1), encoding="utf-8")
    return j, iz


def rapor_md(adlar, aciklama_link, urller, komutlar):
    """altin.puan'ın okuduğu en küçük rapor (Adaylar · Açıklama bağlantıları · URL'ler · Kurulum/komutlar); iki kola eşit uygulanır."""
    h = lambda s: str(s).replace("|", "/").replace("\n", " ")  # noqa: E731
    return "\n".join(["## Adaylar", "| ad | tür |", "|---|---|", *[f"| {h(a)} | araç |" for a in adlar],
                      "## Açıklama bağlantıları", *[f"- {u}" for u in aciklama_link],
                      "## URL'ler", "| url |", "|---|", *[f"| {h(u)} |" for u in urller],
                      "## Kurulum/komutlar", "| komut |", "|---|", *[f"| {h(k)} |" for k in komutlar], ""])
