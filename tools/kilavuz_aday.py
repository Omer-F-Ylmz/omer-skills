"""ENVANTER-4 d3: tarif/aile kılavuzu için aday dökümü + aile JSON → md + ad denetimi.

python tools/kilavuz_aday.py tarif        → <AD>/tarif-<iş>.txt (iş başına katalog adayları)
python tools/kilavuz_aday.py aile         → <AD>/aile-<k>.txt (≥4 üyeli aileler, 3 dilim)
python tools/kilavuz_aday.py isle <jsonl> → docs/katalog/kilavuz/<aile>.md (+ kucuk-aileler.md)
python tools/kilavuz_aday.py denetle      → tarif/kılavuzda `ad` olup katalogda olmayanlar
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import katalog_ara
from kilavuz_ara import derin_tablo

KOK = Path(__file__).resolve().parents[1]
KAT = KOK / "docs" / "katalog"
AD = Path("C:/Projeler/omer-skills/.kos/kopru/envanter4/aday")
ISLER = {
    "pazarlama-kurumsal-site": ["landing page marketing website", "seo meta copywriting", "kurumsal site tasarım", "conversion cro"],
    "awwwards-3d-scroll-site": ["three.js webgl 3d hero", "scroll animation gsap", "awwwards motion design", "shader"],
    "e-ticaret": ["e-commerce checkout cart", "stripe payment", "product catalog shop", "woocommerce shopify"],
    "dotnet-api-backend": ["asp.net core api", "ef core migration", "dotnet test xunit", "backend api design"],
    "guvenlik-testi": ["penetration test", "security audit owasp", "semgrep sast", "secret scan gitleaks", "threat model"],
    "oyun-web-roblox": ["game three.js browser", "roblox lua", "game design balance", "unity godot"],
    "blender-3d-varlik": ["blender bpy", "glb export model", "3d asset material uv", "render turntable"],
    "video-uretim-kurgu": ["video edit ffmpeg", "remotion hyperframes", "subtitle transcript", "short reels clip"],
    "sosyal-medya-otomasyonu": ["social media post", "instagram tiktok", "content calendar", "scheduling automation"],
    "otomasyon-satisi-prototip": ["n8n workflow automation", "prototype mvp", "proposal pricing", "api integration webhook"],
    "belge-sunum": ["pdf docx report", "pptx slides presentation", "xlsx spreadsheet", "documentation writing"],
    "veri-db": ["postgres schema query", "database migration", "data analysis pandas", "sql optimize index"],
    "mobil": ["react native expo", "ios android app", "mobile release store", "push notification"],
    "ajan-skill-gelistirme": ["skill creator", "subagent agent definition", "mcp server", "hook plugin", "eval prompt"],
    "arastirma": ["research web search", "deep research sources", "youtube reddit read", "library docs"],
    "tasarim-sistemi": ["design system tokens", "ui component library", "typography color", "design review"],
    "performans-token-optimizasyonu": ["token context compression", "performance profiling", "web vitals", "cost usage"],
    "mod": ["game mod 3dmigoto", "mod repair package", "lua script mod", "texture model mod"],
}


def kayitlar():
    R = [json.loads(s) for s in open(KAT / "yetenek.jsonl", encoding="utf8")]
    aile = {f"{r['tur']}:{r['ad']}": r["aile"] for r in csv.DictReader(open(KAT / "tekil.tsv", encoding="utf8"), delimiter="\t")}
    return R, aile


def satir(o, aile, derin):
    d = o["durum"]
    bay = "ADAY" if d in ("repo", "yok") or d.startswith("lisans") else "KAPALI" if "kapal" in d else ""
    s = f"- `{o['ad']}` [{o['tur']}{'|' + bay if bay else ''}] {aile.get(o['tur'] + ':' + o['ad'], '?')} · {(o['metin'] or o['is'])[:180]}"
    j = derin(o)
    if j and j.get("dogrulandi", True):
        s += f" ‖ nasıl: {j['nasil'][:110]} ‖ birlikte: {j['birlikte'][:90]} ‖ tuzak: {j['tuzak'][:90]}"
    return s


def tarif():
    R, aile = kayitlar()
    derin = derin_tablo()
    AD.mkdir(parents=True, exist_ok=True)
    for ad, qs in ISLER.items():
        gor, out = set(), []
        for q in qs:
            for o in katalog_ara.ara(q)[:18]:
                k = o["tur"] + ":" + o["ad"]
                if k not in gor:
                    gor.add(k)
                    out.append(satir(o, aile, derin))
        (AD / f"tarif-{ad}.txt").write_text(f"# {ad} · sorgular: {qs}\n" + "\n".join(out[:70]) + "\n", encoding="utf8")
        print(ad, len(out))


def uyeler():
    R, aile = kayitlar()
    tem = {f"{r['tur']}:{r['ad']}" for r in csv.DictReader(open(KAT / "tekil.tsv", encoding="utf8"), delimiter="\t") if r["ad"] == r["temsilci"]}
    g = defaultdict(list)
    for o in R:
        if o["tur"] + ":" + o["ad"] in tem:
            g[aile.get(o["tur"] + ":" + o["ad"], "?")].append(o)
    return g


def aile_dokum():
    g = uyeler()
    buyuk = sorted((a for a in g if len(g[a]) >= 4), key=lambda a: -len(g[a]))
    for k in range(3):
        blok = [f"## {a} ({len(g[a])})\n" + "\n".join(f"- {o['ad']} [{o['tur']}] {(o['metin'] or o['is'])[:120]}" for o in g[a][:80])
                for a in buyuk[k::3]]
        (AD / f"aile-{k}.txt").write_text("\n\n".join(blok) + "\n", encoding="utf8")
        print(k, len(blok), sum(len(b) for b in blok))


def dosya_adi(aile):
    # claude.ai zip'te tek SKILL.md ister, adı büyük/küçük harf duyarsız eşler
    return f"{aile}-aile.md" if aile.lower() == "skill" else f"{aile}.md"


def isle(yol):
    g = uyeler()
    hedef = KAT / "kilavuz"
    hedef.mkdir(exist_ok=True)
    for j in map(json.loads, open(yol, encoding="utf8")):
        u = g[j["aile"]]
        adlar = {o["ad"] for o in u}
        guclu = [x for x in j["guclu"] if x["ad"] in adlar]  # katalogda olmayan ad düşer
        tur = defaultdict(list)
        for o in u:
            tur[o["tur"]].append(o["ad"])
        md = [f"# {j['aile']} — {len(u)} benzersiz kayıt", "", f"**Amaç:** {j['amac']}", "", f"**İç yapı:** {j['yapi']}", "",
              "## En güçlü parçalar"] + [f"- `{x['ad']}` — {x['neden']}" for x in guclu] + \
             ["", "## Birlikte kullanım"] + [f"- {x}" for x in j["birlikte"]] + ["", "## Tuzaklar"] + [f"- {x}" for x in j["tuzak"]] + \
             ["", "## Üyeler"] + [f"- {t} ({len(a)}): " + ", ".join(sorted(a)[:40]) + (" …" if len(a) > 40 else "") for t, a in tur.items()]
        (hedef / dosya_adi(j["aile"])).write_text("\n".join(md) + "\n", encoding="utf8")
        print(j["aile"], len(guclu), "/", len(j["guclu"]))
    kucuk = sorted(a for a in g if len(g[a]) < 4)
    (hedef / "kucuk-aileler.md").write_text("# Küçük aileler (<4 kayıt) — katalog metniyle\n\n" + "\n".join(
        f"- **{a}**: " + " · ".join(f"`{o['ad']}` [{o['tur']}] {(o['metin'] or o['is'])[:90]}" for o in g[a]) for a in kucuk) + "\n", encoding="utf8")


def denetle():
    R, _ = kayitlar()
    adlar = {o["ad"] for o in R}
    bilinmez = defaultdict(set)
    for p in list((KAT / "tarifler").glob("*.md")) + list((KAT / "kilavuz").glob("*.md")):
        for x in re.findall(r"`([^`\s]+)`", p.read_text(encoding="utf8")):
            if x not in adlar:
                bilinmez[p.name].add(x)
    for k, v in sorted(bilinmez.items()):
        print(k, sorted(v))
    return bilinmez


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    m = sys.argv[1]
    {"tarif": tarif, "aile": aile_dokum, "denetle": denetle}.get(m, lambda: isle(sys.argv[2]))()
