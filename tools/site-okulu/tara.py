"""SİTE-OKULU-1: cek.py çıktısını Claude'suz özetler.
  python tools/site-okulu/tara.py kod  <slug...>  → <slug>/kod.json (kütüphane imzası+sürüm, GLSL efekt sınıfı, varlık bütçesi)
  python tools/site-okulu/tara.py izle <slug...>  → <slug>/gemini.json (kayıt + 2 mobil kare → yapılandırılmış sahne JSON'u; ücretsiz Gemini)"""
import base64, json, re, sys, time
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2] / ".kos" / "site-okulu"
IMZA = {  # ad: desen (ilk grup varsa sürüm)
    "three": r"REVISION\s*=\s*[\"'](\d{3})", "ogl": r"\bogl\b|new \w+\(\{[^}]{0,40}dpr:", "babylon": r"BABYLON\.", "r3f": r"__r3f|react-three-fiber",
    "drei": r"useGLTF|@react-three/drei", "pmndrs-post": r"BlendFunction|EffectPass", "three-composer": r"EffectComposer|UnrealBloomPass",
    "gsap": r"GreenSock|gsap", "scrolltrigger": r"ScrollTrigger", "splittext": r"SplitText", "lenis": r"[Ll]enis", "theatre": r"@theatre|theatrejs",
    "barba": r"barba", "swup": r"swup", "howler": r"[Hh]owler|new Howl\(", "tone": r"Tone\.Transport|ToneAudioNode", "ktx2": r"KTX2Loader|basis_transcoder",
    "draco": r"DRACOLoader|draco_decoder|dracoworker", "meshopt": r"MeshoptDecoder|meshopt", "webgpu": r"navigator\.gpu|WebGPURenderer", "tsl": r"\bTSL\b|NodeMaterial",
    "rapier": r"rapier", "rive": r"@rive-app|rive\.wasm", "lottie": r"lottie|bodymovin", "spline": r"@splinetool", "svelte": r"svelte", "react": r"react-dom|__REACT",
    "vue": r"__VUE__|createApp\(", "astro": r"astro-island", "gltf": r"GLTFLoader|glTF", "gpgpu": r"GPUComputationRenderer|texturePosition|textureVelocity",
    "splat": r"\.sog\b|splat|SplatMesh", "image-seq": r"image-sequence|frameCount|imageSequence|\.webp`|sequence",
}
GLSL = {  # efekt sınıfı: desen (shader penceresi başına sayılır)
    "noise": r"snoise|cnoise|fbm\(|simplex|perlin", "curl": r"curl", "fresnel": r"fresnel", "kromatik/dispersiyon": r"chromatic|aberration|dispersion|rgbShift",
    "bloom": r"bloom|luminosityHighPass|mipmapBlur", "dof": r"bokeh|depthOfField|\bcoc\b|circleOfConfusion", "gren": r"grain|filmGrain",
    "akiskan": r"advect|divergence|vorticity|pressure", "raymarch": r"raymarch|sdBox|sdSphere|MAX_STEPS", "gecis/maske": r"uProgress|transition|dissolve|uMask|reveal",
    "gpgpu": r"texturePosition|textureVelocity|uPositions|positionTexture", "matcap": r"matcap", "kirilma": r"refract\(|transmission", "dither": r"dither|bayer",
    "aa": r"fxaa|smaa|FXAA|SMAA", "tonemap": r"ACESFilmic|toneMapping|AgX", "vinyet": r"vignette", "glitch": r"glitch|scanline", "blur": r"gaussian|kawase|blur",
    "instancing": r"instanceMatrix|INSTANCED", "parcacik": r"gl_PointSize", "golge": r"shadowMap|SHADOWMAP", "kaydirma-uniform": r"uScroll|scrollProgress|uProgress",
}


def kod(slug):
    d = KOK / slug
    o = json.loads((d / "olcum.json").read_text(encoding="utf-8"))
    metin = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in sorted((d / "js").glob("*")))
    imza = {}
    for ad, des in IMZA.items():
        m = re.findall(des, metin)
        if m:
            imza[ad] = next((x for x in m if x), True) if isinstance(m[0], str) and re.fullmatch(r"\d+", m[0] or "") else len(m)
    gsap_v = sorted(set(re.findall(r"version:\s*\"(3\.\d{1,2}\.\d{1,2})\"", metin))) if "gsap" in imza else []
    # shader pencereleri: her 'void main' çevresi (string literal ayrıştırmadan; sınıflama sayımı için yeterli)
    pencere = [metin[max(0, m.start() - 2500): m.start() + 2500] for m in re.finditer(r"void\s+main\s*\(", metin)]
    sinif = Counter(k for p in pencere for k, des in GLSL.items() if re.search(des, p))
    (d / "glsl.txt").write_text("\n/*----*/\n".join(pencere), encoding="utf-8")
    tur = Counter()
    for ad, b, _ in o["masa"]["kaynak"]:
        u = re.search(r"\.(\w{2,5})$", ad)
        tur[u.group(1).lower() if u else "diger"] += b
    sonuc = {"imza": imza, "gsap": gsap_v, "shaderSayisi": len(pencere), "glsl": dict(sinif.most_common()),
             "butceMB": round(sum(tur.values()) / 1e6, 2), "istek": len(o["masa"]["kaynak"]), "turKB": {k: round(v / 1e3) for k, v in tur.most_common(8)},
             "jsKB": round(sum(x[1] for x in o["masa"]["kod"]) / 1e3), "mobilMB": round(o["mobilBayt"] / 1e6, 2), "sayfa": o["masa"]["sayfa"], "yukMs": o["masa"]["yukMs"],
             "buyuk": sorted(o["masa"]["kaynak"], key=lambda x: -x[1])[:6]}
    (d / "kod.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(slug, sonuc["butceMB"], "MB", list(imza)[:14], dict(sinif.most_common(6)))


ISTEM = """Bu, ödüllü bir web sitesinin masaüstü ekran kaydı (yükleme + 8 kaydırma adımı) ve 2 mobil kare. Bir front-end/WebGL uzmanı olarak YALNIZ gördüğünü raporla, tahminini 'tahmin' diye işaretle.
JSON döndür, alanlar: {"sahneler":[{"t":"mm:ss","tanim":"..."}], "kamera":"sürekli yol mu, bölüm başına poz mu, sabit mi; hareket türü",
"gecisler":["bölümler arası geçiş türü: kesme/solma/noise-maske/RT kompozit/dönüşüm..."], "post_efektler":["bloom/DoF/gren/kromatik/vinyet..."],
"tipografi":"dev başlık, satır/harf bölme animasyonu, 3B ile katmanlama", "yukleyici":"% sayacı, süre, tasarımı", "ses":"görünür ses düğmesi vb.",
"etkilesimler":["imleç takibi, hover, sürükleme, tık kapısı..."], "mobil":"mobil karelerde 3B var mı, sadeleşme nasıl", "renk_isik":"palet ve ışık karakteri",
"one_cikan_teknikler":["en fazla 6 madde, taklit etmeye değer mekanizma"], "zorluk_1_5":0}"""


def izle(slug):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "video"))
    from video.kisa import anahtar, yukle, _uret
    d, key = KOK / slug, anahtar()
    parca = [{"text": ISTEM}, yukle(d / "kayit.webm", key)]
    for i in (0, 4):
        parca.append({"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode((d / f"m-{i}.jpg").read_bytes()).decode()}})
    j, iz = _uret({"contents": [{"parts": parca}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}}, key, time.monotonic())
    (d / "gemini.json").write_text(json.dumps({**j, "_iz": iz}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(slug, "gemini", iz, flush=True)


HAZIR = {  # imza/GLSL sınıfı → teknikler.md madde no
    "scrolltrigger": 1, "theatre": 1, "gecis/maske": 4, "akiskan": 5, "gpgpu": 6, "parcacik": 6, "bloom": 7, "dof": 7, "gren": 7, "kromatik/dispersiyon": 7,
    "pmndrs-post": 7, "three-composer": 7, "dither": 8, "splittext": 9, "howler": 12, "r3f": 13, "ktx2": 15, "meshopt": 15, "draco": 15, "splat": 18,
    "rapier": 20, "webgpu": 21, "tsl": 21, "rive": 22, "noise": 4, "fresnel": 7, "kirilma": 7, "matcap": 7,
}


def kart(slug):
    """docs/site-okulu/<slug>.md: görülen (Gemini) → kod kanıtı → hazır karşılığı → zorluk. Sayılar ham JSON'dan, yorum yok."""
    d = KOK / slug
    g, k = (json.loads((d / f).read_text(encoding="utf-8")) for f in ("gemini.json", "kod.json"))
    j = lambda x: "; ".join(map(str, x)) if isinstance(x, list) else str(x)
    imza = [f"{a}={b}" if a == "three" else a for a, b in k["imza"].items() if a not in ("image-seq", "gltf")]
    no = sorted({HAZIR[x] for x in [*k["imza"], *list(k["glsl"])[:8]] if x in HAZIR})
    satir = [f"# {slug} — mekanizma kartı (SİTE-OKULU-1)", f"Ham: `.kos/site-okulu/{slug}/` (yerel). Gemini {g['_iz']['model']}, {g['_iz']['jeton']} jeton; Claude görüntü okumadı.", "",
             "## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)"]
    satir += [f"- {t['t']} {t['tanim']}" for t in g.get("sahneler", [])[:6]]
    for e, a in (("Kamera", "kamera"), ("Geçiş", "gecisler"), ("Post", "post_efektler"), ("Tipografi", "tipografi"), ("Yükleyici", "yukleyici"), ("Ses", "ses"), ("Etkileşim", "etkilesimler"), ("Mobil", "mobil")):
        satir.append(f"- **{e}:** {j(g.get(a, '—'))[:220]}")
    # Gemini 'tahmin'lerinin kodla çaprazı; ✗ = imza/GLSL eşleşmesi yok (çalışma anında derlenen shader'ı göremez, yokluk kanıtı değil)
    cap = {"bloom": "bloom" in k["glsl"], "DoF/blur": "blur" in k["glsl"], "kromatik": "kromatik/dispersiyon" in k["glsl"],
           "gren/dither": "dither" in k["glsl"], "maske geçiş": "gecis/maske" in k["glsl"], "scroll uniform": "kaydirma-uniform" in k["glsl"] or "scrolltrigger" in k["imza"],
           "SplitText": "splittext" in k["imza"], "ses kütüphanesi": bool({"howler", "tone"} & set(k["imza"]))}
    satir.append("- **Kod çapraz:** " + " · ".join(f"{a} {'✓' if v else '✗'}" for a, v in cap.items()))
    satir += ["", "## Nasıl yapılmış (kod kanıtı)", f"- İmza: {', '.join(imza) or '—'}" + (f" · gsap {', '.join(k['gsap'])}" if k["gsap"] else ""),
              f"- Shader: {k['shaderSayisi']} `void main` penceresi; sınıf: {', '.join(f'{a} {b}' for a, b in list(k['glsl'].items())[:8]) or '—'}",
              f"- JS {k['jsKB']} KB · sayfa docH {k['sayfa']['docH']} · canvas {', '.join(k['sayfa']['canv'][:2]) or 'yok/iframe'} · yük {k['yukMs']} ms",
              f"- Bütçe (perf API, çapraz kökende eksik sayar): {k['butceMB']} MB / {k['istek']} istek · mobil {k['mobilMB']} MB · tür KB {k['turKB']}",
              "", "## Öne çıkan teknikler (Gemini)"] + [f"- {t}" for t in g.get("one_cikan_teknikler", [])[:6]]
    satir += ["", "## Hazır karşılığı", f"- `teknikler.md` maddeleri: {', '.join(map(str, no)) or '—'} (kaynak + lisans orada)",
              "", f"## Zorluk: {g.get('zorluk_1_5', '?')}/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)"]
    (Path(__file__).resolve().parents[2] / "docs" / "site-okulu" / f"{slug}.md").write_text("\n".join(satir[:40]) + "\n", encoding="utf-8")
    print(slug, "kart", len(satir))


if __name__ == "__main__":
    kip, *adlar = sys.argv[1:]
    for s in adlar:
        try:
            {"kod": kod, "izle": izle, "kart": kart}[kip](s)
        except Exception as e:
            print(s, "DÜŞTÜ", type(e).__name__, str(e)[:300], flush=True)
    print("BITTI", flush=True)
