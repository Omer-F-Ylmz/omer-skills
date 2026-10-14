"""ATLAS-1: araç kullanım atlası — katalogun (docs/katalog/yetenek.jsonl) veri kaynağı genişlemesi, ikinci katalog değil.
  python tools/atlas.py envanter          → .claude/atlas/envanter.jsonl (betik, LLM yok): katalog + claude.ai adları + video adayları + site incelemeleri
  python tools/atlas.py kart [--parti 8]  → docs/atlas/kart.jsonl: öncelik kümesi (site/3D/animasyon/Blender) için ucuz model kartı (tools/ucuz_alt.py, Claude-dışı)
Kart alanları: ad tur ne ne_zaman asama nasil token kalite cakisma kanit (+ Opus kararı: karar kosul). katalog_yenile karar/asama'yı satıra taşır."""
import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import ucuz_alt  # noqa: E402

ENV = KOK / ".claude" / "atlas" / "envanter.jsonl"
KART = KOK / "docs" / "atlas" / "kart.jsonl"
# d1 öncelik kümesi: site + 3D/animasyon + Blender (TELVE); yalnız ad+alan'da aranır (açıklamada 947 öğeye şişiyordu → 207)
ONCELIK = re.compile(r"3d|three|webgl|blender|glb|gltf|animasyon|animation|motion|gsap|scroll|lenis|r3f|shader|playwright|screenshot|"
                     r"image-to-code|21st|design-extractor|design-dna|landing|hero|parallax|ui-ux|frontend-craft|impeccable|taste|"
                     r"web-sahne|telve|polyhaven|objaverse|sketchfab|hunyuan|trellis", re.I)
ASAMA = "kesif|referans|tasarim|varlik|yapim|dogrulama|yayin"


def norm(ad):
    return re.sub(r"[^a-z0-9]+", "-", ad.split(":")[-1].lower()).strip("-")


def envanter():
    web = json.loads((KOK / ".kos/kopru/claudeai_adlar.json").read_text(encoding="utf-8"))
    web = {norm(a) for v in web.values() for a in v}
    out = {}
    for s in (KOK / "docs/katalog/yetenek.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(s)
        k = (norm(r["ad"]), r["tur"])
        if k in out:  # aynı ad+tür farklı kaynaktan: kaynakları birleştir
            out[k]["kaynak"] += f" | {r['kaynak']}"
            continue
        out[k] = dict(ad=r["ad"], tur=r["tur"], kaynak=r["kaynak"], alan=r.get("alan", ""),
                      cc=r["durum"] in ("CC", "ikisi", "repo"), claude_ai=r["durum"] == "ikisi" or k[0] in web,
                      aciklama=r["metin"][:300])
    for s in (KOK / "docs/video-tarama/kayit.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(s)
        for a in r.get("adaylar") or []:
            k = (norm(a), "video-aday")
            if k not in out:
                out[k] = dict(ad=a, tur="video-aday", kaynak=f"docs/video-tarama/{r['rapor']}", alan=r.get("konu", ""),
                              cc=False, claude_ai=False, aciklama="", ele=a in (r.get("ele") or []))
    incele = [*(KOK / ".kos/kopru").glob("site-incele-*.md"), *(KOK / "docs/site-inceleme").glob("*.md")]
    for p in sorted(p for p in incele if p.name != "README.md"):
        out[(p.stem, "site-inceleme")] = dict(ad=p.stem, tur="site-inceleme", kaynak=p.relative_to(KOK).as_posix(), alan="site",
                                              cc=False, claude_ai=False, aciklama=p.read_text(encoding="utf-8")[:300])
    ENV.parent.mkdir(parents=True, exist_ok=True)
    ENV.write_bytes("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out.values()).encode("utf-8"))
    print(f"{ENV.relative_to(KOK)}: {len(out)} öğe", {t: sum(r['tur'] == t for r in out.values()) for t in {r['tur'] for r in out.values()}})


def oncelik(r):
    if r["tur"] in ("video-aday", "site-inceleme"):
        return False  # d1: video/site kartı ayrı küme (d4 video yeniden izleme); site incelemeleri oyun kitabında doğrudan
    return (bool(ONCELIK.search(f"{r['ad']} {r['alan']}")) and (r["cc"] or r["claude_ai"])
            and (r["tur"] != "ajan" or r["ad"].startswith("bl-")))  # ajanlar: yalnız Blender ajanları (diğerleri d2)


def kaynak_dizini():
    d = {}
    for kok in (KOK / "skills", Path.home() / ".claude/skills", Path.home() / ".claude/plugins"):
        for md in kok.rglob("SKILL.md"):
            d.setdefault(norm(md.parent.name), md)
    for md in (Path.home() / ".claude/agents").glob("*.md"):
        d.setdefault(norm(md.stem), md)
    return d


def kaynak_metni(r, dz):
    md = dz.get(norm(r["ad"]))
    if not md:
        return f"(kaynak dosya yok; katalog açıklaması) {r['aciklama']}"
    satirlar = md.read_text(encoding="utf-8", errors="ignore").splitlines()[:90]
    return f"yol: {md}\n" + "\n".join(f"{i}: {s[:200]}" for i, s in enumerate(satirlar, 1))[:3500]


ISTEM = f"""Aşağıdaki her araç için kanıta dayalı bir kullanım kartı yaz. YALNIZ verilen metinde yazanı kullan; metinde yoksa "bilinmiyor" yaz, uydurma.
Her araç için tek satır JSON (JSON Lines, başka metin yok), alanlar:
{{"ad": "<verilen ad aynen>", "ne": "ne işe yarar (≤20 kelime)", "ne_zaman": "iş türü + koşul (≤20 kelime)", "asama": "<{ASAMA} birinden>",
"nasil": "çağrı/komut örneği (≤15 kelime)", "token": "azaltır|artırır|nötr: neden (≤12 kelime)", "kalite": "kaliteye etkisi (≤12 kelime)",
"cakisma": "aynı işi yapan benzer araç adları ya da yok", "kanit": "yol:satır (metindeki satır numarası)"}}
Toplam kart ≤120 kelime. Türkçe yaz.
"""


def kart(parti=8):
    hazir = {json.loads(s)["ad"] for s in KART.read_text(encoding="utf-8").splitlines()} if KART.exists() else set()
    rs = [r for r in map(json.loads, ENV.read_text(encoding="utf-8").splitlines()) if oncelik(r) and r["ad"] not in hazir]
    dz, cagri, basarisiz = kaynak_dizini(), 0, []
    KART.parent.mkdir(parents=True, exist_ok=True)
    for i in range(0, len(rs), parti):
        grup = rs[i:i + parti]
        istem = ISTEM + "".join(f"\n### ad: {r['ad']} (tür: {r['tur']})\n{kaynak_metni(r, dz)}\n" for r in grup)
        bulunan = {}
        for deneme in range(3):  # kesilen/boş yanıt yeniden denenir
            cagri += 1
            try:
                c = ucuz_alt.iste(ucuz_alt.govde(istem, []))["choices"][0]
                for s in (c["message"].get("content") or "").splitlines():
                    s = s.strip().strip(",")
                    if s.startswith("{"):
                        try:
                            j = json.loads(s)
                            bulunan[j["ad"]] = j
                        except (ValueError, KeyError):
                            pass
            except Exception as e:  # anahtar hata metnine girmez
                print(f"HATA {type(e).__name__} {getattr(e, 'code', '')}", flush=True)
                time.sleep(20)
            if all(r["ad"] in bulunan for r in grup):
                break
        with KART.open("ab") as f:
            for r in grup:
                if r["ad"] in bulunan:
                    f.write((json.dumps({**bulunan[r["ad"]], "ad": r["ad"], "tur": r["tur"]}, ensure_ascii=False) + "\n").encode("utf-8"))
                else:
                    basarisiz.append(r["ad"])
        print(f"{min(i + parti, len(rs))}/{len(rs)} · çağrı {cagri} · başarısız {len(basarisiz)}", flush=True)
    print("BITTI", json.dumps({"cagri": cagri, "basarisiz": basarisiz}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "envanter":
        envanter()
    elif a and a[0] == "kart":
        kart(int(a[a.index("--parti") + 1]) if "--parti" in a else 8)
    else:
        print(__doc__)
