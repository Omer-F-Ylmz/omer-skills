"""TOKEN-3b proje profili: skillOverrides/enabledPlugins proje .claude/settings.json'a, router'lara "Profil dışı üyeler".

Kullanım: python tools/profil.py                 # profilleri uygula (yedek .bakT3b)
          python tools/profil.py --geri <proje>  # yedekten bayt-eşit geri
          python tools/profil.py --kontrol       # sapma + router ezilmesi
          python tools/profil.py --routerlar     # router bloğu: repo skills/ + synced CC kopyası
          python tools/profil.py --zip           # dist/token-3b/departman-*.zip (claude.ai Replace)
Kural (dalga KARAR): kullanıcı aileleri 14 günde ≥1 çağrı → name-only, 0 → off + router; plugin skill anahtarı
skillOverrides'ta etkisiz (K1) → plugin 0 çağrıysa enabledPlugins:false, G/H hook ya da kullanılmış MCP/ajan varsa açık.
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
VERI = KOK / "profiller/proje-profilleri.json"
BLOK_BAS = "<!-- profil-disi:bas -->"
BLOK_SON = "<!-- profil-disi:son -->"
GSTACK_EK = {"gstack", "_gstack-command", "gstack-upgrade"}


def _json(p):
    return json.loads(Path(p).read_bytes().decode("utf-8-sig"))


def _desc(md):
    m = re.match(r"---\s*\n(.*?)\n---", md.read_bytes().decode("utf-8", "replace"), re.S)
    d = re.search(r"^description:\s*(.+)$", m.group(1), re.M) if m else None
    t = d.group(1).strip().strip("\"'") if d else ""
    return (t.split(". ")[0].rstrip(".") or "—")[:110]


def envanter(home):
    c = Path(home) / ".claude"
    plugins = {}
    for key, kayit in _json(c / "plugins/installed_plugins.json")["plugins"].items():
        ad, market = key.split("@")
        p = Path(kayit[0]["installPath"])
        mj = c / "plugins/marketplaces" / market / ".claude-plugin/marketplace.json"
        ent = next((e for e in _json(mj).get("plugins", []) if e.get("name") == ad), {}) if mj.exists() else {}
        mdler = [(p / x / "SKILL.md") for x in ent["skills"]] if ent.get("skills") else sorted(p.glob("skills/*/SKILL.md"))
        pj = p / ".claude-plugin/plugin.json"
        hook = (p / "hooks/hooks.json").exists() or (pj.exists() and "hooks" in _json(pj))
        plugins[ad] = {"anahtar": key, "skills": {m.parent.name: m for m in mdler if m.exists()}, "hook": hook}
    sk = c / "skills"
    gstack = GSTACK_EK | {d.name for d in (sk / "gstack").glob("*") if (d / "SKILL.md").exists()}
    kullanici = {}
    for d in sorted(sk.iterdir()) if sk.exists() else []:
        if (d / "SKILL.md").exists():
            aile = "threejs" if d.name.startswith("threejs-") else "gstack" if d.name in gstack else d.name
            kullanici.setdefault(aile, {})[d.name] = d / "SKILL.md"
    return {"plugins": plugins, "kullanici": kullanici}


def kapat_dogrula(ad, veri):
    if veri["hook_sinif"].get(ad) in ("G", "H"):
        raise ValueError(f"{ad}: G/H hook sağlıyor — kapatılmaz")
    if veri["mcp14"].get(ad) or veri["ajan14"].get(ad):
        raise ValueError(f"{ad}: 14 günde kullanılmış MCP/ajan sağlıyor — kapatılmaz")


def hesapla(profil_ad, veri, env):
    pr = veri["profiller"][profil_ad]
    acik = set(veri["her_zaman"]) | set(pr["acik"])
    name_only = set(pr["name_only"])
    bilinen = set(env["plugins"]) | set(env["kullanici"]) | {"anthropic-skills"}
    for a in sorted((acik | name_only) - bilinen):
        raise ValueError(f"bilinmeyen aile/skill: {a}")
    so, ep, atlanan = {}, {}, []
    for aile, sks in env["kullanici"].items():
        if aile in acik:
            continue
        deger = "name-only" if aile in name_only or veri["cagri14"].get(aile, 0) >= 1 else "off"
        if deger == "off" and aile not in veri["router"]:
            raise ValueError(f"kapalı aileye router eşlemesi yok: {aile}")
        so.update({s: deger for s in sks})
    for ad, p in env["plugins"].items():
        if ad in acik or ad in veri.get("kucuk_500kr", []) or not p["skills"]:
            continue
        if p["hook"] and ad not in veri["hook_sinif"]:
            raise ValueError(f"sınıfsız hook: {ad}")
        try:
            if veri["cagri14"].get(ad, 0) >= 1:
                raise ValueError("çağrılmış")  # plugin'de name-only mekanizması yok (K1) → açık kalır
            kapat_dogrula(ad, veri)
        except ValueError:
            atlanan.append(ad)
            continue
        if ad not in veri["router"]:
            raise ValueError(f"kapalı plugin'e router eşlemesi yok: {ad}")
        ep[p["anahtar"]] = False
    return {"skillOverrides": so, "enabledPlugins": ep, "atlanan": sorted(atlanan)}


def _dosyalar(proje):
    f = Path(proje) / ".claude/settings.json"
    return f, f.with_name("settings.json.bakT3b"), f.with_name("settings.json.yokT3b")


def uygula(proje, h, home):
    f, bak, yok = _dosyalar(proje)
    globaller = {(Path(x) / ".claude/settings.json").resolve() for x in (home, Path.home())}
    if f.resolve() in globaller:
        raise ValueError("global settings'e yazılmaz")
    f.parent.mkdir(parents=True, exist_ok=True)
    if not bak.exists() and not yok.exists():
        (bak.write_bytes(f.read_bytes()) if f.exists() else yok.write_bytes(b""))
    d = _json(f) if f.exists() else {}
    for k in ("skillOverrides", "enabledPlugins"):
        d.setdefault(k, {}).update(h[k])
    yeni = (json.dumps(d, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if not f.exists() or f.read_bytes() != yeni:
        f.write_bytes(yeni)


def geri(proje):
    f, bak, yok = _dosyalar(proje)
    if bak.exists():
        f.write_bytes(bak.read_bytes())
    elif yok.exists():
        if f.exists():
            f.replace(f.with_name("settings.json.geriT3b"))  # silme yok: kenara al
    else:
        raise ValueError(f"yedek yok: {bak}")


def router_bloklari(veri, env):
    kapali = {}
    for pad in sorted(set(veri["projeler"].values())):
        h = hesapla(pad, veri, env)
        for aile, sks in env["kullanici"].items():
            if any(h["skillOverrides"].get(s) == "off" for s in sks):
                kapali[aile] = sks
        for ad, p in env["plugins"].items():
            if p["anahtar"] in h["enabledPlugins"]:
                kapali[ad] = {f"{ad}:{s}": m for s, m in p["skills"].items()}
    satirlar = {}
    for aile in sorted(kapali):
        for s, m in sorted(kapali[aile].items()):
            satirlar.setdefault(veri["router"][aile], []).append(f"- `{s}` · {_desc(m)} · `{m.as_posix()}`")
    return {dep: "\n".join([BLOK_BAS, "## Profil dışı üyeler (yalnız CC)",
                            "Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa SKILL.md'yi Read ile aç; "
                            "references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. "
                            "claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.", *sat, BLOK_SON])
            for dep, sat in satirlar.items()}


def blok_yollari(metin):
    return re.findall(r"`([^`]+/SKILL\.md)`", metin)


def router_yaz(f, blok):
    t = f.read_bytes().decode("utf-8")
    if BLOK_BAS in t:
        yeni = t[:t.index(BLOK_BAS)] + blok + t[t.index(BLOK_SON) + len(BLOK_SON):]
    else:
        yeni = t.rstrip("\n") + "\n\n" + blok + "\n"
    if yeni == t:
        return False
    f.write_bytes(yeni.encode("utf-8"))
    return True


def kontrol(veri, env, router_kokleri):
    u = []
    for proje, pad in veri["projeler"].items():
        h = hesapla(pad, veri, env)
        f = Path(proje) / ".claude/settings.json"
        d = _json(f) if f.exists() else {}
        for k in ("skillOverrides", "enabledPlugins"):
            for a, v in h[k].items():
                if d.get(k, {}).get(a) != v:
                    u.append(f"SAPMA {proje} {k}.{a}: {d.get(k, {}).get(a)!r} != {v!r}")
    for kok in router_kokleri:
        for dep, blok in router_bloklari(veri, env).items():
            rf = Path(kok) / f"departman-{dep}/SKILL.md"
            t = rf.read_bytes().decode("utf-8") if rf.exists() else ""
            if BLOK_BAS not in t:
                u.append(f"ROUTER bloğu yok (senkron ezmiş olabilir): {rf}")
            elif blok not in t:
                u.append(f"ROUTER bloğu güncel değil: {rf}")
            u += [f"ROUTER yol yok: {y}" for y in blok_yollari(t) if not Path(y).exists()]
    return u


def router_kokleri(home):
    return [KOK / "skills"] + sorted(d for d in (Path(home) / ".claude/skills/synced").glob("*_*") if d.is_dir())


def zip_routerlar(kaynak, dist):
    dist.mkdir(parents=True, exist_ok=True)
    for d in sorted(kaynak.glob("departman-*")):
        with zipfile.ZipFile(dist / f"{d.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(x for x in d.rglob("*") if x.is_file()):
                z.write(f, f"{d.name}/{f.relative_to(d).as_posix()}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--geri", metavar="PROJE")
    ap.add_argument("--kontrol", action="store_true")
    ap.add_argument("--routerlar", action="store_true")
    ap.add_argument("--zip", action="store_true")
    a = ap.parse_args()
    home = Path.home()
    if a.geri:
        return geri(a.geri) or print("geri:", a.geri)
    veri, env = _json(VERI), envanter(home)
    if a.kontrol:
        u = kontrol(veri, env, router_kokleri(home))
        print("\n".join(u) or "kontrol temiz")
        return 1 if u else 0
    if a.routerlar:
        for kok in router_kokleri(home):
            for dep, blok in router_bloklari(veri, env).items():
                print(dep, kok.name, router_yaz(kok / f"departman-{dep}/SKILL.md", blok))
        return 0
    if a.zip:
        return zip_routerlar(KOK / "skills", KOK / "dist/token-3b") or print("dist/token-3b yazıldı")
    for proje, pad in veri["projeler"].items():
        h = hesapla(pad, veri, env)
        uygula(proje, h, home)
        print(f"{pad} {proje}: skillOverrides {len(h['skillOverrides'])} · enabledPlugins:false {sorted(h['enabledPlugins'])} · açık kalan {h['atlanan']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
