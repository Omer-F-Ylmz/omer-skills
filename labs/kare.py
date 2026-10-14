"""SİTE-OKULU-2 lab kıyası: labs/<teknik> headless kareleri + fps/boşta kare ölçümü → Gemini ETKİ eşleşme puanı (referans site kareleriyle) → dist/site-okulu/<teknik>-kiyas.jpg + labs/<teknik>/olcum.json.
Kullanım: python labs/kare.py <teknik>... (Gemini çağrısı teknik başı 1, koşu başı en fazla TAVAN)."""
import asyncio, base64, functools, http.server, io, json, statistics, sys, threading, time
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "tools" / "video"), str(KOK / "tools" / "jev"), str(KOK / "tools")]
from video import kisa  # noqa: E402
import ucuz_alt  # noqa: E402

TAVAN = 12  # Gemini çağrısı / koşu (teknik başı KOSU)
REF = KOK / ".kos" / "site-okulu"
CIKTI = KOK / "dist" / "site-okulu"
# teknik: (referans site, konu, [(sorgu, p)])
LAB = {
    "kamera-yolu": ("igloo", "scroll'a bağlı tek sürekli kamera yolu (spline), sis içinden dalış ve nesneler arasından geçiş", [("", 0), ("", .3), ("", .6), ("", .95)]),
    "post": ("lusion", "post-processing yığını: bloom, alan derinliği (rack focus), kromatik sapma, film greni, vinyet; mobil kademe düşüşü", [("", 0), ("", 1), ("?kademe=dusuk", 1)]),
    "gecis": ("activetheory", "iki 3B sahne arasında render-target kompozit gürültü maskeli geçiş (kenar ışımalı)", [("", .2), ("", .45), ("", .55), ("", .85)]),
    "metin": ("lando", "dev tipografi + 3B nesne katmanlama (tip nesnenin arkasında) + SplitText maskeli satır girişleri", [("", 0), ("", .45), ("", .8)]),
    "yukleyici": ("lando", "yükleme yüzde sayacı (000-100) + perde açılışı + kamera dolly + başlık harf girişi koreografisi", [("", .1), ("", .45), ("", .7), ("", 1)]),
    "parcacik": ("activetheory", "GPGPU parçacık bulutu (buhar), derinlik solması ve sis", [("", 0), ("?kademe=dusuk", 0)]),
}
ISTEM = """Sen bir WebGL/yaratıcı geliştirme jürisisin. A0..A7 = ödüllü referans sitenin kaydırma kareleri; B0.. = bizim lab demomuzun kareleri (sırayla zaman/kaydırma ilerler).
Teknik: {konu}. İçerik, marka, metin, renk paleti eşleşmesi ARANMAZ (kendi varlıklarımız); yalnız tekniğin ETKİSİ ve kalite çıtası karşılaştırılır.
İki ayrı puan ver: "mekanizma" = tekniğin kendisi (hareket, ışık/post, zamanlama, geçiş eğrisi) referans çıtasında mı; "icerik" = referansın kendi 3B/parçacık/sahne içeriğinin zenginliği bizde ne kadar (içerik kopyalanmaz; mekanizma puanını ETKİLEMEZ).
Yalnız JSON dön: {{"ref_kareler":[tekniği en iyi gösteren ≤3 A indeksi], "hareket":0-10, "isik_post":0-10, "kalite":0-10, "mekanizma":0-10, "icerik":0-10, "eslesme":0-10, "farklar":[≤3 kısa madde], "oneriler":[≤3 somut kod/ayar önerisi]}}"""
KOSU = 3  # d3: tek Gemini koşusu ±3 oynuyordu → temp 0, 3 koşu medyanı
IKINCI = ("openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free", "openrouter/google/gemma-4-31b-it:free", "openrouter/google/gemma-4-26b-a4b-it:free")  # Gemini dışı ücretsiz görsel; cfp/* çift jeton döndürüyor


def sunucu():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(KOK))
    http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
    # Windows kayıt defteri .js'i text/plain eşleyebiliyor → modül betiği reddedilir
    http.server.SimpleHTTPRequestHandler.extensions_map |= {".js": "text/javascript", ".mjs": "text/javascript"}
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]


def jpg(im, w=640):
    b = io.BytesIO()
    im.convert("RGB").resize((w, int(im.height * w / im.width))).save(b, "JPEG", quality=80)
    return b.getvalue()


async def cek(br, port, ad, adimlar):
    kareler, olcum, hatalar = [], {}, []
    for sorgu, p in adimlar:
        pg = await br.new_page(viewport={"width": 1440, "height": 900})
        pg.on("pageerror", lambda e: hatalar.append(str(e)[:200]))
        pg.on("console", lambda m: m.type == "error" and hatalar.append(m.text[:200]))
        await pg.goto(f"http://127.0.0.1:{port}/labs/{ad}/{sorgu}")
        try:
            await pg.wait_for_function("window.lab && lab.hazir", timeout=20000)
        except Exception:
            print(ad, sorgu, "hazır değil:", sorted(set(hatalar))[:3], flush=True)
            await pg.close()
            continue
        await pg.evaluate(f"lab.git({p})")
        k0 = await pg.evaluate("lab.kare")
        await pg.wait_for_timeout(1000)
        anahtar = f"{sorgu or 'varsayilan'}@{p}"
        olcum[anahtar] = {"kare_1sn": await pg.evaluate("lab.kare") - k0}
        kareler.append(Image.open(io.BytesIO(await pg.screenshot(type="jpeg", quality=85))))
        if not olcum.get("gpu"):
            olcum["gpu"] = await pg.evaluate("(()=>{const g=document.createElement('canvas').getContext('webgl2');const e=g&&g.getExtension('WEBGL_debug_renderer_info');return e?g.getParameter(e.UNMASKED_RENDERER_WEBGL):'?'})()")
        await pg.close()
    olcum["hatalar"] = sorted(set(hatalar))[:5]
    return kareler, olcum


def puanla(ref, konu, bizim, key):
    parca = [{"text": ISTEM.format(konu=konu)}]
    refs = [Image.open(REF / ref / f"d-{i}.jpg") for i in range(8)]
    for ad, ims in (("A", refs), ("B", bizim)):
        for i, im in enumerate(ims):
            parca += [{"text": f"{ad}{i}:"}, {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(jpg(im)).decode()}}]
    govde = {"contents": [{"parts": parca}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    kosular = [kisa._uret(govde, key, time.monotonic()) for _ in range(KOSU)]
    j, iz = kosular[0]
    for alan in ("hareket", "isik_post", "kalite", "mekanizma", "icerik", "eslesme"):
        v = [k[0].get(alan) for k in kosular if isinstance(k[0].get(alan), (int, float))]
        j[alan] = statistics.median(v) if v else None
        j[alan + "_kosular"] = v
    return j, iz, refs


def izgara(ims, w=360):
    h = int(900 * w / 1440)
    t = Image.new("RGB", (4 * w, -(-len(ims) // 4) * h))
    for i, im in enumerate(ims):
        t.paste(im.convert("RGB").resize((w, h)), (i % 4 * w, i // 4 * h))
    return "data:image/jpeg;base64," + base64.b64encode(jpg(t, 1440)).decode()


def ikinci(refs, konu, bizim):
    """Bağımsız yargıç: aynı istem, A ve B ızgarası iki görsel; ilk yanıt veren model."""
    icerik = [{"type": "text", "text": ISTEM.format(konu=konu) + "\nGörsel 1 = A ızgarası (soldan sağa, yukarıdan aşağı A0..), görsel 2 = B ızgarası."},
              {"type": "image_url", "image_url": {"url": izgara(refs)}}, {"type": "image_url", "image_url": {"url": izgara(bizim)}}]
    for m in IKINCI:
        try:
            j = ucuz_alt.iste({"model": m, "max_tokens": 4000, "temperature": 0, "messages": [{"role": "user", "content": icerik}]}, 180)
            metin = j["choices"][0]["message"]["content"] or ""
            return {"model": m, **json.loads(metin[metin.index("{"):metin.rindex("}") + 1])}
        except Exception as e:
            hata = f"{m}: {str(e)[:120]}"
    return {"hata": hata}


def kiyas(refs, secim, bizim, yol, w=480):
    sec = [int(str(i).lstrip("Aa")) for i in (secim or [0]) if str(i).lstrip("Aa").isdigit()]
    ust = [refs[i] for i in sec[:3] if 0 <= i < 8] or refs[:1]
    n = max(len(ust), len(bizim))
    h = int(900 * w / 1440)
    tuval = Image.new("RGB", (n * w, 2 * h), (12, 8, 6))
    for sira, ims in enumerate((ust, bizim)):
        for i, im in enumerate(ims):
            tuval.paste(im.convert("RGB").resize((w, h)), (i * w, sira * h))
    tuval.save(yol, "JPEG", quality=82)


async def main(adlar):
    assert all(a in LAB for a in adlar), f"bilinmeyen teknik; seçenekler: {list(LAB)}"
    assert len(adlar) * KOSU <= TAVAN, f"koşu başı en fazla {TAVAN} Gemini çağrısı"
    key = kisa.anahtar()
    port = sunucu()
    CIKTI.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch(args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-gpu"])
        for ad in adlar:
            ref, konu, adimlar = LAB[ad]
            bizim, olcum = await cek(br, port, ad, adimlar)
            try:
                j, iz, refs = puanla(ref, konu, bizim, key)
            except RuntimeError as e:
                j, iz, refs = {"hata": str(e)[:300]}, {}, [Image.open(REF / ref / f"d-{i}.jpg") for i in range(8)]
            kiyas(refs, j.get("ref_kareler"), bizim, CIKTI / f"{ad}-kiyas.jpg")
            j2 = ikinci(refs, konu, bizim) if bizim else {}
            (KOK / "labs" / ad / "olcum.json").write_text(json.dumps({"ref": ref, "olcum": olcum, "gemini": j, "ikinci": j2, "iz": iz}, ensure_ascii=False, indent=1), encoding="utf-8")
            print(ad, json.dumps({"gemini": {a: j.get(a + "_kosular") for a in ("mekanizma", "icerik", "eslesme")}, "ikinci": {a: j2.get(a) for a in ("model", "mekanizma", "icerik", "eslesme", "hata")}, "farklar": j.get("farklar"), "olcum": olcum}, ensure_ascii=False))
        await br.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or list(LAB)))
