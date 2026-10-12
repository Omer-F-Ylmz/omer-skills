"""KALİTE-3 Faz 1: bütün skill filosunun statik denetimi (API'siz, salt okuma).

Kaynaklar: ~/.claude/skills (gevşek + iç içe alt skill'ler), installed_plugins.json installPath'leri,
~/.claude/skills/synced (claude.ai kopyası: giriş SKILL.md + skills/*/TALIMAT.md).
python tools/skill_filo_denetim.py [--tsv docs/kutuphane/skill-denetim.tsv] [--ozet docs/kutuphane/skill-denetim-ozet.md]
"""
import argparse, collections, hashlib, json, posixpath, re, sys
from pathlib import Path

ATLA = {".trash", "synced"}
TETIK = re.compile(r"use when|use this|use for|when the user|when you|trigger|invoke|proactively|kullan|tetikle|zaman|durumda|için"
                   r"|[时時]使用|時に使用|何[时時]|때 사용|사용할 때|usar cuando|úsal[oa]", re.I)
BAG = re.compile(r"\]\(([^)#\s]+)\)|`((?:references|scripts|assets|reference|docs)/[^`\s]+)`")
MCP = re.compile(r"mcp__([A-Za-z0-9_.-]+?)__")
EMIR = re.compile(r"\b(ALWAYS|NEVER|MUST NOT|MUST|DO NOT|HER ZAMAN|ASLA)\b\s+((?:\w+\s+){2}\w+)", re.I)
OLUMSUZ = {"never", "must not", "do not", "asla"}
SORUNLAR = ("aciklama_yok", "aciklama_kisa", "aciklama_uzun", "tetik_yok", "kirik_bag", "cift", "eski_arac", "celiski", "pd_yok")
PD_SINIR = 2000
ALANLAR = ("ad", "kaynak", "aile", "yol", "aciklama_uzunluk", "tetik", "govde_jeton", "dosya", "kirik", "cift", "kopya", "eski_arac", "celiski", "sorunlar")


def ayir(metin):
    """frontmatter (name, description) + gövde; YAML kütüphanesi olmadan, katlanmış açıklamayı da toplar."""
    m = re.match(r"\ufeff?---\r?\n(.*?)\r?\n---\r?\n?(.*)", metin, re.S)
    if not m:
        return {}, metin
    fm, alan = {}, None
    for satir in m.group(1).splitlines():
        k = re.match(r"([A-Za-z_-]+):\s*(.*)", satir)
        if k:
            alan = k.group(1)
            fm[alan] = k.group(2).strip().strip("'\"").lstrip(">|").strip()
        elif alan and satir.startswith((" ", "\t")):
            fm[alan] = (fm[alan] + " " + satir.strip()).strip()
    return fm, m.group(2)


def jeton(metin):
    # ponytail: karakter/4 yaklaşığı; gerçek sayım gerekirse count_tokens API ile örnekle
    return len(metin) // 4


def _dosya_kaydi(md, kok, kaynak, aile, mevcut):
    fm, govde = ayir(md.read_text(encoding="utf-8", errors="replace"))
    return {"ad": fm.get("name") or md.parent.name, "aciklama": fm.get("description", ""), "govde": govde,
            "kaynak": kaynak, "aile": aile, "yol": str(md), "dizin": md.parent.relative_to(kok).as_posix(), "mevcut": mevcut}


def _pazar_skills(ev, anahtar):
    """marketplace.json'da plugin girdisinin "skills" yolları (daymade paketleri plugin.json'suz bunu kullanır)."""
    ad, _, pazar = anahtar.partition("@")
    m = ev / ".claude/plugins/marketplaces" / pazar / ".claude-plugin/marketplace.json"
    try:
        girdi = next((p for p in json.loads(m.read_text(encoding="utf-8")).get("plugins", []) if p.get("name") == ad), {})
    except (OSError, ValueError):
        return []
    s = girdi.get("skills") or []
    return [s] if isinstance(s, str) else s


def _plugin_yuklenen(kok, ek=()):
    """CC'nin plugin sürüm kökünden yüklediği SKILL.md'ler: kök SKILL.md, skills/<ad>/, plugin.json ve marketplace.json
    "skills" yolları (ek; yol skill dizini ya da skill dizinlerinin üstü). docs/<dil>, .kiro, .agents vb. kopyalar yüklenmez."""
    yollar = ["skills", *ek]
    pj = kok / ".claude-plugin/plugin.json"
    if pj.exists():
        try:
            s = json.loads(pj.read_text(encoding="utf-8")).get("skills") or []
        except ValueError:
            s = []
        yollar += [s] if isinstance(s, str) else s
    out = {kok / "SKILL.md"}
    for y in yollar:
        d = kok / y
        out |= {d / "SKILL.md"} if (d / "SKILL.md").exists() else set(d.glob("*/SKILL.md"))
    return out


def _haric_sinif(parts):
    for p in parts[:-1]:
        if p == "docs" or p.startswith("."):
            return p
    return "skills/<kat>/<ad>" if parts[0] == "skills" else parts[0]


def _dizin_kayitlari(kok, kaynak, aile_adi, yuklenen=None, haric=None):
    """yuklenen verilmezse (gevşek) gizli dizin ve docs/ altındaki kopyalar atlanır; atlananlar haric'e sayılır."""
    for md in sorted(kok.rglob("SKILL.md")):
        parts = md.relative_to(kok).parts
        if ATLA & set(parts):
            continue
        if (md not in yuklenen if yuklenen is not None
                else any(p == "docs" or p.startswith(".") for p in parts[:-1])):
            if haric is not None:
                haric[_haric_sinif(parts)] += 1
            continue
        d = md.parent
        mevcut = {p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file()}
        aile = aile_adi or md.relative_to(kok).parts[0]
        yield _dosya_kaydi(md, kok, kaynak, aile, mevcut)


def _synced_kayitlari(kok):
    """claude.ai senkron kopyası: giriş SKILL.md + aile paketinin skills/*/TALIMAT.md alt skill'leri."""
    for giris in sorted(kok.glob("*/*/SKILL.md")):
        aile = None
        for md in [giris] + sorted(giris.parent.glob("skills/*/TALIMAT.md")):
            d = md.parent
            mevcut = {p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file()}
            k = _dosya_kaydi(md, kok, "claude.ai", aile, mevcut)
            aile = aile or k["ad"]
            k["aile"] = aile
            if "REFERANS.md" in mevcut:
                k["referans"] = (d / "REFERANS.md").read_text(encoding="utf-8", errors="replace")
            yield k


def topla(ev, haric=None):
    kayit = list(_dizin_kayitlari(ev / ".claude/skills", "gevşek", None, haric=haric))
    ip = ev / ".claude/plugins/installed_plugins.json"
    if ip.exists():
        for anahtar, liste in json.loads(ip.read_text(encoding="utf-8")).get("plugins", {}).items():
            for x in liste[:1]:
                p = Path(x.get("installPath", ""))
                if p.is_dir():
                    kayit += _dizin_kayitlari(p, "plugin", anahtar.split("@")[0], _plugin_yuklenen(p, _pazar_skills(ev, anahtar)), haric)
    return kayit + list(_synced_kayitlari(ev / ".claude/skills/synced"))


def mcp_adlari(ev):
    """Kurulu MCP sunucu adları (CC araç önekindeki biçimiyle); değer/komut okunmaz."""
    d = json.loads((ev / ".claude.json").read_text(encoding="utf-8"))
    adlar = set(d.get("mcpServers") or {})
    for p in (d.get("projects") or {}).values():
        adlar |= set(p.get("mcpServers") or {})
    ip = ev / ".claude/plugins/installed_plugins.json"
    if ip.exists():
        for anahtar, liste in json.loads(ip.read_text(encoding="utf-8")).get("plugins", {}).items():
            pl = anahtar.split("@")[0]
            for x in liste[:1]:
                m = Path(x.get("installPath", "")) / ".mcp.json"
                if m.exists():
                    try:
                        j = json.loads(m.read_text(encoding="utf-8"))
                    except ValueError:
                        continue
                    adlar |= {f"plugin_{pl}_{s}" for s in (j.get("mcpServers", j) or {})}
    return adlar


def _kirik(k):
    kirik = []
    for m in BAG.finditer(k["govde"]):
        h = m.group(1) or m.group(2)
        h = h[1:-1] if h.startswith("<") and h.endswith(">") else h
        if re.match(r"[a-z]+:|/|~|\$", h) or re.search(r"[*<{]", h) or not re.search(r"\.\w+$", h):
            continue
        if h.startswith("..") and "!" not in k["yol"] and (Path(k["yol"]).parent / h).exists():
            continue
        hedef = posixpath.normpath(h.lstrip("./") if not h.startswith("..") else h)
        if (hedef not in k["mevcut"] and posixpath.basename(hedef) not in {posixpath.basename(x) for x in k["mevcut"]}
                and posixpath.basename(hedef) not in k.get("referans", "")):
            kirik.append(h)
    return sorted(set(kirik))


def _celiski(govde):
    olumlu, olumsuz = set(), set()
    for m in EMIR.finditer(govde):
        (olumsuz if m.group(1).lower() in OLUMSUZ else olumlu).add(m.group(2).lower())
    return sorted(olumlu & olumsuz)


def denetle(kayit, mcp):
    imza, govdeler = collections.Counter(), collections.defaultdict(set)
    for k in kayit:
        imza[k["ad"].lower()] += 1
        govdeler[k["ad"].lower()].add(hashlib.sha1(re.sub(r"\s+", " ", k["govde"]).strip().encode()).hexdigest())
    satirlar = []
    for k in kayit:
        acik, gj = k["aciklama"], jeton(k["govde"])
        kirik = _kirik(k)
        eski = sorted({"mcp__" + s for s in MCP.findall(k["govde"] + " " + acik)
                       if s not in mcp and not s.startswith("claude_ai_")})
        cel = _celiski(k["govde"])
        mdler = [x for x in k["mevcut"] if x.endswith(".md") and posixpath.basename(x) not in ("SKILL.md", "TALIMAT.md")]
        s = []
        if not acik:
            s.append("aciklama_yok")
        elif len(acik) < 40:
            s.append("aciklama_kisa")
        if len(acik) > (200 if k["kaynak"] == "claude.ai" and k["dizin"].count("/") == 0 else 1024):
            s.append("aciklama_uzun")
        if acik and not TETIK.search(acik):
            s.append("tetik_yok")
        if kirik:
            s.append("kirik_bag")
        if len(govdeler[k["ad"].lower()]) > 1:
            s.append("cift")
        if eski:
            s.append("eski_arac")
        if cel:
            s.append("celiski")
        if gj > PD_SINIR and not mdler:
            s.append("pd_yok")
        satirlar.append({"ad": k["ad"], "kaynak": k["kaynak"], "aile": k["aile"], "yol": k["yol"],
                         "aciklama_uzunluk": len(acik), "tetik": int(bool(TETIK.search(acik))), "govde_jeton": gj,
                         "dosya": len(k["mevcut"]), "kirik": ";".join(kirik), "cift": len(govdeler[k["ad"].lower()]) - 1, "kopya": imza[k["ad"].lower()] - 1,
                         "eski_arac": ";".join(eski), "celiski": ";".join(cel), "sorunlar": ",".join(s)})
    return satirlar


def ozet(satirlar):
    """(sorun sınıfı → sayı, aile → puan). Puan: skill başına 100 − 15 × sorun sınıfı (taban 0), aile ortalaması."""
    sayi = collections.Counter(x for r in satirlar for x in r["sorunlar"].split(",") if x)
    puan = collections.defaultdict(list)
    for r in satirlar:
        puan[r["aile"]].append(max(0, 100 - 15 * len([x for x in r["sorunlar"].split(",") if x])))
    return sayi, {a: round(sum(v) / len(v)) for a, v in puan.items()}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--ev", default=str(Path.home()))
    ap.add_argument("--tsv", default="docs/kutuphane/skill-denetim.tsv")
    ap.add_argument("--ozet", default="docs/kutuphane/skill-denetim-ozet.md")
    a = ap.parse_args()
    ev = Path(a.ev)
    haric = collections.Counter()
    kayit = topla(ev, haric)
    satirlar = denetle(kayit, mcp_adlari(ev))
    with open(a.tsv, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(ALANLAR) + "\n")
        for r in sorted(satirlar, key=lambda r: (r["aile"], r["ad"], r["kaynak"])):
            f.write("\t".join(str(r[x]).replace("\t", " ") for x in ALANLAR) + "\n")
    sayi, aile = ozet(satirlar)
    kaynak = collections.Counter(r["kaynak"] for r in satirlar)
    gj = sorted(r["govde_jeton"] for r in satirlar)
    satir = [f"# Skill filosu statik denetimi (KALİTE-3 Faz 1)", "",
             f"Kayıt {len(satirlar)} · " + " · ".join(f"{k} {v}" for k, v in kaynak.most_common())
             + f" · aile {len(aile)}",
             f"Yüklenmeyen kopya (hariç) {sum(haric.values())}: " + " · ".join(f"{k} {v}" for k, v in haric.most_common()),
             f"Gövde jetonu (≈karakter/4): toplam {sum(gj)} · ortanca {gj[len(gj) // 2]} · >{PD_SINIR}: {sum(1 for x in gj if x > PD_SINIR)}", "",
             "## Sorun sınıfı başına", ""] + [f"- {s}: {sayi.get(s, 0)}" for s in SORUNLAR] + [
             "", "## En düşük puanlı 30 aile (puan · skill sayısı)", ""]
    adet = collections.Counter(r["aile"] for r in satirlar)
    satir += [f"- {a_} {p} · {adet[a_]}" for a_, p in sorted(aile.items(), key=lambda x: (x[1], x[0]))[:30]]
    satir.append("")
    Path(a.ozet).write_text("\n".join(satir), encoding="utf-8", newline="\n")
    print("\n".join(satir[:4 + len(SORUNLAR) + 4]))


if __name__ == "__main__":
    main()
