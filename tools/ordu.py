"""ORDU-1: iş → zorluk sınıfı (kolay/orta/zor/imkansiz, LLM yok) → ROUTER-1 kademesi. Ücretsiz çıktı mekanik denetimi geçemezse
yonlendir.kos bir üst kademeye çıkarır (≤2) ve kayda yazar; ikinci bir yönlendirici yok.
kolay=T1 (tek ücretsiz aile) · orta=T1 + iki aile çapraz (ucretsiz_havuz.iki_aile; havuz yoksa T1 zincirinin sonu Haiku) · zor=T2 Sonnet medium · imkansiz=T4 Opus medium
Kaskad (Ömer 21 Eki, kesin): ücretsiz → Haiku medium/high → Sonnet medium/high → Opus medium/high; başarılı basamak türe kaydedilir (basla).
  python tools/ordu.py sinif "<iş>" [--boyut kucuk|orta|buyuk] [--risk a,b]   → karar (JSON)
  python tools/ordu.py heldout                                                 → 20 işlik kapı kümesi: dağılım + sınıf doğruluğu
  python tools/ordu.py kapi A.json B.json                                      → A/B kapısı ({claude_token, kalite, basarisiz})
d3 kapısı kapi3: {claude_is, agirlikli_token, kalite}"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yonlendir  # noqa: E402

SINIF = ["kolay", "orta", "zor", "imkansiz"]
KADEME = {"kolay": ("T1", False), "orta": ("T1", True), "zor": ("T2", False), "imkansiz": ("T4", False)}
_K = yonlendir.kurallar()["kademe"]
MERDIVEN = [{"ad": "ucretsiz", **_K["T1"]}] + [{"ad": f"{m}-{e}", "model": mod, "effort": e} for m, mod in (
    ("haiku", yonlendir.HAIKU), ("sonnet", _K["T2"]["model"]), ("opus", _K["T4"]["model"])) for e in ("medium", "high")]
BASLA = {"kolay": 0, "orta": 0, "zor": 3, "imkansiz": 5}
# shortcut: anahtar kelime + boyut + risk; geçmiş başarı (yonlendir-kayit) sınıfa katılmıyor, ≥30 koşu birikince ekle
ANAHTAR = [("imkansiz", ("mimari", "tasarım kararı", "inatçı", "iki kez başarısız", "çok dosyalı")),
           ("zor", ("refactor", "bug", "düzelt", "test yaz", "kod yaz", "uygula", "yargı", "skill yaz")),
           ("orta", ("özet", "araştır", "çevir", "etiket", "sınıfla", "rapor", "alan çıkar", "incele", "regex")),
           ("kolay", ("sayım", "kaç satır", "listele", "biçim", "dönüştür", "birleştir", "taşı", "yeniden adlandır", "kopyala"))]
# kapı kümesi: anahtar listesi bu işlere bakılarak ayarlanmadı; etiketler elle (gerçek repo iş türleri)
HELDOUT = [
    ("tools/ klasöründeki .py dosyalarının satır sayımını TSV'ye yaz", "kolay"),
    ("iki devir notunu birleştir, tekrar eden satırları at", "kolay"),
    ("docs/ altındaki .md dosyalarını listele, boyuta göre sırala", "kolay"),
    ("eski rapor dosyalarını arşiv klasörüne taşı", "kolay"),
    ("JSON çıktıyı TSV biçimine dönüştür", "kolay"),
    ("tests/ dosya adlarını yeni önek ile yeniden adlandır", "kolay"),
    ("ucuz_alt.py ne yapar, kısaca özet", "orta"),
    ("OmniRoute kota davranışını araştır, tek paragraf", "orta"),
    ("README'deki kurulum bölümünü İngilizceye çevir", "orta"),
    ("video raporlarını konuya göre etiketle", "orta"),
    ("devir notundan karar ve tarih alanlarını çıkar", "orta"),
    ("tarih biçimini yakalayan regex yaz ve örneklerle dene", "orta"),
    ("yonlendir.sec için sınır durumlarını kapsayan test yaz", "zor"),
    ("ajan_sira.kuyruk içindeki küçük bug'ı düzelt", "zor"),
    ("ucretsiz_havuz._sec fonksiyonunu refactor et, davranış aynı kalsın", "zor"),
    ("iki skill taslağı arasında rubrikle yargı ver", "zor"),
    ("yeni bir yardımcı için kod yaz ve testini koştur", "zor"),
    ("onay betiği için skill yaz ve KALİTE kapısından geçir", "zor"),
    ("çok dosyalı köprü mimarisi için tasarım kararı ver", "imkansiz"),
    ("iki kez başarısız olan inatçı yarış durumunu çöz", "imkansiz"),
]


def sinif(tanim, boyut="kucuk", risk=()):
    """Anahtar kelime sınıfı (hiçbiri eşleşmezse zor); büyük boyut ve geri dönülmez/güvenlik riski +1 (zor'a kadar; imkansiz yalnız anahtarla)."""
    t = tanim.lower()
    i = SINIF.index(next((c for c, ks in ANAHTAR if any(k in t for k in ks)), "zor"))
    if i < 2:
        i = min(i + (boyut == "buyuk") + any(r in ("geri-donulmez", "guvenlik") for r in risk), 2)
    kd, capraz = KADEME[SINIF[i]]
    return {"sinif": SINIF[i], **yonlendir.karar(kd, "full" if risk else "light", None, "ordu"), "capraz": capraz}


def basla(tur, sinif_):
    """Türün kayıtlı (≥2) koşusuna göre başlangıç basamağı: en alt geçen basamak (orada kalma payı geçmeden fazlaysa +1; hiç geçen yoksa en yüksek denenenin üstü); kayıt yoksa sınıf başlangıcı."""
    ks = [s for s in yonlendir.satirlar() if s.get("tur") == tur and "basamak" in s]
    if len(ks) < 2:
        return BASLA[sinif_]
    gecen = [s["basamak"] for s in ks if s["sonuc"] == "gecti"]
    if not gecen:
        return min(max(s["basamak"] for s in ks) + 1, len(MERDIVEN) - 1)
    b = min(gecen)
    return min(b + (sum(1 for s in ks if s["basamak"] == b and s["sonuc"] == "kaldi") > gecen.count(b)), len(MERDIVEN) - 1)


def merdiven_kos(tur, sinif_, calistir, denetle, ad=""):
    """calistir(basamak) → (çıktı, usage{giris,cikis}); denetle(çıktı, basamak) → bool. Geçmeyen iş bir üst basamağa; her basamak
    yonlendir kaydına yazılır (öğrenme girdisi); tükenirse SIRA satırı. Döner (çıktı|None, geçen/son basamak indeksi)."""
    for i in range(basla(tur, sinif_), len(MERDIVEN)):
        b = MERDIVEN[i]
        cikti, u = calistir(b)
        ok = bool(denetle(cikti, b))
        yonlendir.kaydet({"tur": tur, "kademe": b["ad"], "model": b["model"], "effort": b["effort"], "dogrulama": "light"},
                         "gecti" if ok else "kaldi", u, i, {"basamak": i, **({"ad": ad} if ad else {})})
        if ok:
            return cikti, i
    with yonlendir.SIRA.open("ab") as f:
        f.write(f"- {time.strftime('%H:%M')} ORDU-1 MERDİVEN TÜKENDİ: {ad or tur} · Desktop bakmalı\n".encode("utf-8"))
    return None, len(MERDIVEN) - 1


def kapi(a, b):
    """B (ordu) Claude token ≤ A'nın %50'si VE kalite ≥ A VE başarısızlık ≤ A."""
    return b["claude_token"] <= a["claude_token"] * 0.5 and b["kalite"] >= a["kalite"] and b["basarisiz"] <= a["basarisiz"]


AGIRLIK = {"haiku": 1 / 3, "sonnet": 1.0, "opus": 5 / 3}  # plan kotası ağırlığı: liste fiyat oranı varsayımı (Sonnet=1)


def kapi3(a, b):
    """d3 kapısı: Claude'a giden alt iş ≤%50 VE Claude ağırlıklı token ≤%60 VE kalite ≥ A."""
    return b["claude_is"] <= a["claude_is"] * 0.5 and b["agirlikli_token"] <= a["agirlikli_token"] * 0.6 and b["kalite"] >= a["kalite"]


KABUL_BAYRAK = Path(__file__).resolve().parents[1] / ".kos/kopru/ajan-sira.ordu-kabul"  # onay/ordu_1.py kabul · --geri


def norm(y):
    """JSON dizgesi/çitli blok → nesne; dizge → boşluk daraltılmış, küçük harf, sondaki noktalama atılmış."""
    if isinstance(y, str):
        s = y.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        if s[:1] in "{[":
            try:
                return norm(json.loads(s))
            except ValueError:
                pass
        return " ".join(s.lower().split()).rstrip(".")
    if isinstance(y, dict):
        return {str(k): norm(v) for k, v in y.items()}
    return [norm(v) for v in y] if isinstance(y, list) else y


def hakem(istem, a, b, aileler):
    """Üçüncü ücretsiz aile: iki yanıt anlamca aynı mı (sayı/ad/tarih farkı → AYRI). Yanıt veren üçüncü aile yoksa None (ret sayılır)."""
    import ucretsiz_havuz as h
    for uc in sorted({e.aile for e in h.ENT} - set(aileler) - {"karma", "anthropic"}):
        y, _, _ = h.cagir("ozet", f"İş:\n{istem}\n\nYanıt 1:\n{a}\n\nYanıt 2:\n{b}\n\nİki yanıt anlamca aynı mı (aynı sayılar, adlar, tarihler, karar)? Yalnız AYNI ya da AYRI yaz.", max_tokens=1500, aile=uc)
        if y:
            return y.strip().upper().startswith("AYNI")
    return None


def kabul(yanitlar, test=None, hakem_=None, gevsek=None):
    """Orta işte iki aile yanıtı → kabul edilen (normalize) yanıt | None. Bayrak kapalı: birebir aynı. Açık: mekanik test varsa testi geçen;
    yoksa normalize eşitlik, o da yoksa hakem_(a, b) (üçüncü aile) 'aynı' derse birinci yanıt."""
    if not (KABUL_BAYRAK.exists() if gevsek is None else gevsek):
        return yanitlar[0] if len(yanitlar) == 2 and yanitlar[0] is not None and yanitlar[0] == yanitlar[1] else None
    ys = [norm(y) for y in yanitlar if y is not None]
    if test:
        return next((y for y in ys if test(y)), None)
    if len(ys) == 2 and (ys[0] == ys[1] or (hakem_ and hakem_(*ys))):
        return ys[0]
    return None


if __name__ == "__main__":
    a = sys.argv[1:]
    al = lambda b, v: a[a.index(b) + 1] if b in a else v
    if a[0] == "sinif":
        print(json.dumps(sinif(a[1], al("--boyut", "kucuk"), [r for r in al("--risk", "").split(",") if r]), ensure_ascii=False))
    elif a[0] == "heldout":
        sonuc = [(sinif(t)["sinif"], e) for t, e in HELDOUT]
        print(json.dumps({"is": len(HELDOUT), "dagilim": {s: sum(1 for _, e in HELDOUT if e == s) for s in SINIF},
                          "dogru": sum(1 for g, e in sonuc if g == e), "yanlis": [(t, g, e) for (t, e), (g, _) in zip(HELDOUT, sonuc) if g != e]},
                         ensure_ascii=False, indent=1))
    elif a[0] == "kapi":
        A, B = (json.loads(Path(p).read_text(encoding="utf-8")) for p in a[1:3])
        print(json.dumps({"gecti": kapi(A, B), "A": A, "B": B}, ensure_ascii=False))
