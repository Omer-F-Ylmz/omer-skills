"""HAVUZ-GENİŞ-1B: G (görsel) rolü olan her model 3 bilinen test görseliyle doğrulanır (renk · OCR · sahne).
3/3 geçen model G'de kalır; yanlış bilen ya da ulaşılamayan model G rolünü kaybeder (kapalı).
Kullanım: python tools/gorsel_dogrula.py   → .kos/kopru/ucretsiz/gorsel-dogrula.json + envanter G sütunu + docs halka satırı"""
import base64, io, json, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import havuz_envanter as E  # noqa: E402
import ucretsiz_havuz as H  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
ENVANTER = KOK / ".kos/kopru/havuz-envanter.tsv"
RAPOR = KOK / ".kos/kopru/ucretsiz/gorsel-dogrula.json"
DOKUMAN = KOK / "docs/ucretsiz-havuz.md"


def _png(im):
    b = io.BytesIO()
    im.save(b, "PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


def _yazi(metin, boy):
    try:
        return ImageFont.truetype("arial.ttf", boy)
    except OSError:
        return ImageFont.load_default(size=boy)


def testler():
    renk = Image.new("RGB", (256, 256), (0, 0, 255))  # saf mavi
    ocr = Image.new("RGB", (512, 160), (255, 255, 255))
    ImageDraw.Draw(ocr).text((30, 40), "HAVUZ 42", fill=(0, 0, 0), font=_yazi("HAVUZ 42", 72))
    sahne = Image.new("RGB", (400, 300), (135, 206, 235))  # gökyüzü
    d = ImageDraw.Draw(sahne)
    d.rectangle([0, 200, 400, 300], fill=(34, 139, 34))  # çimen
    d.ellipse([150, 40, 250, 140], fill=(255, 215, 0))  # sarı daire
    return [
        ("renk", _png(renk), "Bu görselin ana rengi nedir? Yalnız tek kelime yaz.", ["mavi", "blue"], None, "son"),
        ("ocr", _png(ocr), "Görseldeki yazıyı aynen yaz. Yalnız yazıyı yaz, başka hiçbir şey yazma.", ["havuz42"], None, "son"),
        ("sahne", _png(sahne), "Bu görselde ne var? Şeklin ve rengini kısaca yaz.", ["sarı", "sari", "yellow"],
         ["daire", "çember", "cember", "güneş", "gunes", "circle", "sun", "disk"], "tum"),
    ]


def _norm(s):
    return "".join(ch for ch in s.lower().replace("ı", "i") if ch.isalnum())


def _kontrol(yanit, grup_a, grup_b, kapsam):
    # "son": yalnız son dolu satır (düşünme metni cevap sayılmaz); "tum": tüm yanıt
    metin = yanit.strip().splitlines()[-1] if kapsam == "son" and yanit.strip() else yanit
    y = _norm(metin) if kapsam == "son" else metin.lower().replace("ı", "i")
    ok = any(_norm(k) in y for k in grup_a)
    return ok and (grup_b is None or any(_norm(k) in y for k in grup_b))


def dene(prov, model):
    sonuc = []
    for ad, png, soru, a, b, kapsam in testler():
        icerik = [{"type": "text", "text": soru}, {"type": "image_url", "image_url": {"url": png}}]
        m, kod, not_, _ = E._gonder(prov, model, icerik, 1500, 60)
        if m is None and kod in (429, 503, 599, 502):  # geçici: bir kez bekle, tekrar dene
            time.sleep(20)
            m, kod, not_, _ = E._gonder(prov, model, icerik, 1500, 60)
        if m is None:
            sonuc.append({"test": ad, "durum": "erisilemedi", "kod": kod, "not": not_})
        else:
            sonuc.append({"test": ad, "durum": "gecti" if _kontrol(m, a, b, kapsam) else "yanlis", "yanit": m[-80:]})
    if all(s["durum"] == "gecti" for s in sonuc):
        karar = "G"
    elif any(s["durum"] == "yanlis" for s in sonuc):
        karar = "KAPALI-YANLIS"
    else:
        karar = "KAPALI-ERISILEMEDI"
    return {"prov": prov, "model": model, "karar": karar, "testler": sonuc}


def main():
    satirlar = [l.split("\t") for l in ENVANTER.read_text(encoding="utf-8").splitlines()]
    baslik, gov = satirlar[0], satirlar[1:]
    # aday: tek görsel probunda "kırmızı" diyen her model (G rolü önceden düşmüş olabilir)
    adaylar = [s for s in gov if "kırmız" in s[6].lower()]
    print(f"G adayı: {len(adaylar)}")
    with ThreadPoolExecutor(max_workers=min(9, len(adaylar)) or 1) as ex:
        sonuc = list(ex.map(lambda s: dene(s[0], s[1]), adaylar))
    for r in sonuc:
        print(r["prov"], r["model"], r["karar"], [t["durum"] for t in r["testler"]])
    RAPOR.parent.mkdir(parents=True, exist_ok=True)
    RAPOR.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    karar = {(r["prov"], r["model"]): r["karar"] == "G" for r in sonuc}
    for s in gov:
        if (s[0], s[1]) in karar:
            rol = [x for x in s[7].split(",") if x not in ("G", "-")]
            if karar[(s[0], s[1])]:
                rol.insert(1 if rol[:1] == ["M"] else 0, "G")
            s[7] = ",".join(rol) or "-"
    ENVANTER.write_text("\n".join("\t".join(s) for s in [baslik] + gov) + "\n", encoding="utf-8")
    print("G kalan:", sum(karar.values()), "· kapatılan:", len(karar) - sum(karar.values()))


if __name__ == "__main__":
    main()
