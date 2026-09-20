"""KURULUM-8 K1: aday envanteri + claude.ai zip'leri -> dist/yukle-8/parti-N."""
import json, os, posixpath, re, shutil, sys, zipfile
from pathlib import Path

H = Path(os.path.expanduser("~/.claude"))
OUT = Path(os.environ.get("YUKLE_OUT") or r"C:\Projeler\omer-skills\dist\yukle-8")
# yalniz bu adlar uretilsin (yama partisi); bos = hepsi
SADECE = {a for a in os.environ.get("YUKLE_SADECE", "").split(",") if a}
# claude.ai "reserved word 'claude'" reddi: zip ici ad + klasor degisir, CC plugin/kaynak skill degismez
YENI_AD = {"claude-api": "messages-api-sdk",
           "claude-md-improver": "memory-md-improver",
           "claude-opus-4-5-migration": "opus-4-5-migration"}
SYNC = H / "skills/synced/924f0f64-fcbf-4e91-8e2f-e62bad8245c0_5bf6859c-713e-459a-9126-5fb1dcc493b6"
YERLESIK = set("""docx pdf pptx xlsx frontend-design skill-creator mcp-builder theme-factory canvas-design
web-artifacts-builder algorithmic-art brand-guidelines doc-coauthoring internal-comms slack-gif-creator""".split())
PERSONAL = {"agent-reach", "graphify", "pia-generation", "policy-monitor", "ui-ux-pro-max",
            "use-case-triage", "learned", "hetzner-deploy", "roblox-game-development-lifecycle",
            "wpf-rule-mvvm-constraints"}
ATLA_DIR = {".git", "node_modules", "__pycache__", ".pytest_cache", ".venv"}
YASAK = re.compile(r'[\x00-\x1f\x7f\\:*?"<>|@]')
SH_EXT = {".sh", ".bash"}
SHEBANG_SH = re.compile(rb"^#![^\n]*\b(ba)?sh\b")
TEXT_EXT = {".md", ".txt", ".py", ".js", ".mjs", ".cjs", ".ts", ".json", ".yaml", ".yml",
            ".sh", ".bash", ".ps1", ".html", ".css", ".csv", ".toml"}


def skill_adi(d):
    """Skill kimligi = SKILL.md frontmatter'indaki name; taste-skill'de klasor adindan farkli."""
    try:
        md = (d / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^﻿?---\s*\r?\n(.*?)\r?\n---", md, re.S)
        n = re.search(r"^name:[ \t]*(.+)$", m.group(1), re.M) if m else None
        if n:
            v = n.group(1).strip().strip("'\"")
            # slug degilse (hookify: "Writing Hookify Rules") klasor adi gecerli kimlik
            if v and re.fullmatch(r"[a-z0-9][a-z0-9-]*", v):
                return v
    except Exception:
        pass
    return d.name


def envanter():
    inst = json.loads((H / "plugins/installed_plugins.json").read_text(encoding="utf-8"))["plugins"]
    decl = {}
    for mk in (H / "plugins/marketplaces").iterdir():
        f = mk / ".claude-plugin/marketplace.json"
        if not f.exists():
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for pl in d.get("plugins", []):
            if pl.get("skills") is not None:
                decl[(mk.name, pl.get("name"))] = pl["skills"]
    cand = {}
    for key, ents in inst.items():
        pname, _, mname = key.partition("@")
        ip = Path(ents[0]["installPath"])
        sk = decl.get((mname, pname))
        dirs = []
        if sk is not None:
            for s in sk:
                d = (ip / s.lstrip("./")).resolve()
                if (d / "SKILL.md").exists():
                    dirs.append(d)
        elif (ip / "skills").is_dir():
            dirs = [p.parent for p in sorted((ip / "skills").rglob("SKILL.md"))]
        for d in dirs:
            cand.setdefault(skill_adi(d), []).append((pname, d))
    loc = {skill_adi(d): ("", d) for d in (H / "skills").iterdir()
           if d.is_dir() and d.name != "synced" and (d / "SKILL.md").exists()}
    syn = {skill_adi(d) for d in SYNC.iterdir() if d.is_dir()} | {d.name for d in SYNC.iterdir() if d.is_dir()}
    gstack = set(loc) - PERSONAL - {"gstack"}
    cowork = {n for n, ps in cand.items() if {p for p, _ in ps} == {"claude-mem-cowork"}}
    secili = {}
    for ad, ps in cand.items():
        if ad in syn or ad in YERLESIK or ad == "gstack" or ad in gstack or ad in cowork:
            continue
        secili[ad] = [(p, d) for p, d in ps if p != "claude-mem-cowork"]
    for ad, (p, d) in loc.items():
        if ad in syn or ad in YERLESIK or ad == "gstack" or ad in gstack or ad in secili:
            continue
        secili[ad] = [(p, d)]
    return secili, {"syn": len(syn), "gstack": len(gstack) + 1, "cowork": sorted(cowork)}


def duzelt_metin(s, ad):
    port = "$(ls -d /mnt/skills/*/" + ad + " | head -1)"
    s = s.replace("${CLAUDE_PLUGIN_ROOT}", port).replace("$CLAUDE_PLUGIN_ROOT", port)
    return s.replace("%CLAUDE_PLUGIN_ROOT%", port)


def kopyala(src, dst, ad, rapor):
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in ATLA_DIR and d != ".claude-plugin"]
        for f in files:
            sp = Path(root) / f
            rel = sp.relative_to(src)
            if f == "plugin.json" or sp.suffix.lower() == ".zip":
                rapor.append(ad + ": cikarildi " + rel.as_posix())
                continue
            if YASAK.search(rel.as_posix()):
                rapor.append(ad + ": YASAK-KARAKTER atlandi " + rel.as_posix())
                continue
            dp = dst / rel
            dp.parent.mkdir(parents=True, exist_ok=True)
            b = sp.read_bytes()
            ext = sp.suffix.lower()
            if ext in TEXT_EXT or b.startswith(b"#!"):
                try:
                    t = b.decode("utf-8")
                except UnicodeDecodeError:
                    dp.write_bytes(b)
                    continue
                t2 = duzelt_metin(t, ad)
                if ext in SH_EXT or b.startswith(b"#!"):
                    t2 = t2.replace("\r\n", "\n").replace("\r", "\n")
                dp.write_bytes(t2.encode("utf-8"))
            else:
                dp.write_bytes(b)


def frontmatter(p, ad, rapor):
    md = p.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^(\ufeff?---\s*\r?\n)(.*?)(\r?\n---)", md, re.S)
    if not m:
        # frontmatter'siz dosya (everything-claude-code'un 3 dokumani): H1 + ilk paragraftan uret
        h1 = re.search(r"^#\s+(.+)$", md, re.M)
        par = next((l.strip() for l in md.splitlines()
                    if l.strip() and not l.startswith(("#", "```", "-", "|", ">"))), "")
        desc = " ".join((((h1.group(1).strip() + ". ") if h1 else "") + par).split())[:200] or ad
        p.write_text("---\nname: " + ad + "\ndescription: " + json.dumps(desc, ensure_ascii=False)
                     + "\n---\n\n" + md, encoding="utf-8")
        rapor.append(ad + ": frontmatter uretildi")
        return
    fm = m.group(2)
    satirlar = fm.split("\n")
    # anahtar bloklarini topla: (indeks, kac satir, anahtar, ham deger)
    i, bloklar = 0, []
    while i < len(satirlar):
        km = re.match(r"^([A-Za-z_][\w-]*):[ \t]*(.*)$", satirlar[i])
        if not km:
            i += 1
            continue
        anahtar, deger, j = km.group(1), km.group(2), i + 1
        if deger.strip() in ("", ">", ">-", "|", "|-"):
            while j < len(satirlar) and (satirlar[j].startswith((" ", "\t")) or not satirlar[j].strip()):
                deger += " " + satirlar[j].strip()
                j += 1
        bloklar.append([i, j - i, anahtar, " ".join(deger.split())])
        i = j
    yeni, degisti = list(satirlar), False
    for bas, uzun, anahtar, deger in reversed(bloklar):
        if anahtar == "name":
            if deger.strip("'\"") != ad:
                yeni[bas:bas + uzun] = ["name: " + ad]
                rapor.append(ad + ": name duzeltildi")
                degisti = True
        elif anahtar == "description":
            val = deger.lstrip(">|-").strip().strip("'\"")
            # claude.ai "description cannot contain XML tags": <...> ve ok isaretleri acili parantezsiz
            temiz = re.sub(r"<([^<>]*)>", r"\1", val).replace("->", "→").replace("<-", "←")
            if temiz != val:
                rapor.append(ad + ": description acili parantez temizlendi")
                val = temiz
            if len(val) > 200:
                val = val[:197].rsplit(" ", 1)[0] + "..."
                rapor.append(ad + ": description " + str(len(deger)) + "->" + str(len(val)))
            if uzun > 1 or val != deger:
                yeni[bas:bas + uzun] = ["description: " + json.dumps(val, ensure_ascii=False)]
                degisti = True
    if not any(b[2] == "name" for b in bloklar):
        yeni.insert(0, "name: " + ad)
        rapor.append(ad + ": name eklendi")
        degisti = True
    if not any(b[2] == "description" for b in bloklar):
        rapor.append(ad + ": DESCRIPTION YOK")
    if degisti:
        p.write_text(m.group(1) + "\n".join(yeni).strip("\n") + m.group(3) + md[m.end():], encoding="utf-8")


def referans_getir(stage, src, ad, rapor):
    """SKILL.md'nin skill disina isaret eden gecerli referanslarini _ref/ altina kopyala."""
    sys.path.insert(0, r"C:\Projeler\omer-skills\tools")
    from skill_denetim import yollar
    sp = stage / "SKILL.md"
    md = sp.read_text(encoding="utf-8", errors="replace")
    degis = False
    for t in sorted(set(yollar(md)), key=len, reverse=True):
        icerde = (stage / t.lstrip("./")).exists() if ".." not in t else False
        if icerde:
            continue
        kaynak = Path(os.path.normpath(str(src / t)))
        if not kaynak.exists() or src in kaynak.parents:
            continue
        yeni = "_ref/" + re.sub(r"^(\.\./)+", "", t).lstrip("/")
        hedef = stage / yeni
        hedef.parent.mkdir(parents=True, exist_ok=True)
        if kaynak.is_dir():
            if not hedef.exists():
                shutil.copytree(kaynak, hedef, ignore=shutil.ignore_patterns(*ATLA_DIR))
        else:
            shutil.copy2(kaynak, hedef)
        md = md.replace(t, yeni)
        rapor.append(ad + ": referans _ref/ " + t)
        degis = True
    if degis:
        sp.write_text(md, encoding="utf-8")


def ref_skillmd(stage, ad, rapor):
    """claude.ai: zip'te tam olarak bir SKILL.md. Kok disindakiler SKILL.ref.md olur, baglantilar guncellenir."""
    esle = set()
    for p in sorted(stage.rglob("SKILL.md")):
        if p.parent == stage:
            continue
        p.rename(p.with_name("SKILL.ref.md"))
        esle.add(p.relative_to(stage).as_posix())
        rapor.append(ad + ": SKILL.ref.md " + p.relative_to(stage).as_posix())
    if not esle:
        return
    for f in sorted(stage.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in TEXT_EXT:
            continue
        try:
            t = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        kok = f.parent.relative_to(stage).as_posix()
        # yalniz yeniden adlandirilan bir dosyaya gercekten cozulen basvuru degisir
        def yenile(m):
            hedef = posixpath.normpath(posixpath.join(kok, m.group(0)))
            return m.group(0)[:-len("SKILL.md")] + "SKILL.ref.md" if hedef in esle else m.group(0)
        t2 = re.sub(r"(?:\.{1,2}/|[\w.-]+/)+SKILL\.md\b", yenile, t)
        if t2 != t:
            f.write_text(t2, encoding="utf-8")


def main():
    secili, ist = envanter()
    tmp = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\pc\AppData\Local\Temp\yukle8tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    if OUT.exists():
        shutil.rmtree(OUT)
    rapor, satir = [], []
    adlar = [a for a in sorted(secili) if not SADECE or a in SADECE]
    for i, kaynak_ad in enumerate(adlar):
        parti = i // 20 + 1
        ad = YENI_AD.get(kaynak_ad, kaynak_ad)
        plugin, src = secili[kaynak_ad][0]
        zad = (plugin + "-" + ad + ".zip") if plugin else (ad + ".zip")
        stage = tmp / ad / ad
        stage.mkdir(parents=True)
        kopyala(src, stage, ad, rapor)
        frontmatter(stage / "SKILL.md", ad, rapor)
        referans_getir(stage, src, ad, rapor)
        ref_skillmd(stage, ad, rapor)
        acik = sum(f.stat().st_size for f in stage.rglob("*") if f.is_file())
        d = OUT / ("parti-" + str(parti))
        d.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(d / zad, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted((tmp / ad).rglob("*")):
                z.write(f, f.relative_to(tmp / ad).as_posix())
        satir.append("\t".join([str(parti), plugin or "(yerel)", ad, zad, str(acik)]))
        if acik > 30 * 10**6:
            rapor.append(ad + ": BOYUT " + str(round(acik / 10**6, 1)) + " MB > 30")
    (tmp / "_satirlar.tsv").write_text("\n".join(satir), encoding="utf-8")
    (tmp / "_rapor.txt").write_text("\n".join(rapor), encoding="utf-8")
    print("aday", len(adlar), "parti", (len(adlar) - 1) // 20 + 1, "synced", ist["syn"],
          "gstack-cikti", ist["gstack"], "cowork", ist["cowork"])
    print("rapor", len(rapor), "->", str(tmp / "_rapor.txt"))


main()
