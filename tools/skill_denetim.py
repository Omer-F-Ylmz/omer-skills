"""claude.ai skill zip denetimi.

Kullanım: python tools/skill_denetim.py <dist> [--rapor docs/x.md]
Kapsam: <dist>/*.zip + <dist>/yukle-6c/**/*.zip (_yerlesik hariç). Yalnız özet basar; ayrıntı rapora gider.
Çıkış kodu: hata varsa 1.
"""
import argparse, fnmatch, hashlib, posixpath, re, subprocess, sys, zipfile
from collections import Counter
from pathlib import Path
import yaml

BSDTAR = r"C:\Windows\System32\tar.exe" if sys.platform == "win32" else "bsdtar"
YERLESIK = set("""algorithmic-art brand-guidelines canvas-design internal-comms slack-gif-creator web-artifacts-builder
theme-factory mcp-builder skill-creator docs import-memory morning docx pdf pptx xlsx product-self-knowledge
frontend-design file-reading pdf-reading""".split())
# (zip deseni, tür, öğe deseni, gerekçe) — tür "yol": SKILL.md'deki göreli yol; "claude": "dosya: satır" metni; "manifest": zip öğesi
YANLIS_ALARM = [
    ("one-skill-to-rule-them-all-task-observer.zip", "manifest", r"/\.tessl-plugin/plugin\.json$", "tessl manifest'i; claude.ai kurulum-7'de reddetmedi"),
    ("claude-design-skills-ux-research.zip", "claude", r"`~/\.claude/skills/` for local skills", "Obsidian/kişisel kurulum bölümü; repo dışı olarak belgelenmiş"),
    ("policy-monitor.zip", "claude", r"~/\.claude/plugins/config/claude-for-legal/privacy-legal/CLAUDE\.md", "isteğe bağlı profil; dosya yoksa profilsiz çalışır"),
    ("use-case-triage.zip", "claude", r"~/\.claude/plugins/config/claude-for-legal/privacy-legal/CLAUDE\.md", "isteğe bağlı profil; dosya yoksa profilsiz çalışır"),
    ("context7-context7-cli.zip", "claude", r"^[^:]+/references/setup\.md: .*# Claude Code \(~/\.claude/skills\)", "ctx7 kurulum hedefini anlatan yorum"),
]
LINK = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
TOKEN = re.compile(r"(?<![\w./~-])((?:\.\./)*(?:references|reference|scripts|assets|templates|examples)/[^\s)`'\"\],;*<>|]+|(?:\.\./)+[\w.-][^\s)`'\"\],;*<>|]*)")
TEXT_EXT = {".md", ".txt", ".py", ".js", ".mjs", ".ts", ".json", ".yaml", ".yml", ".sh", ".ps1", ".html", ".css", ".csv", ".toml"}


def alarm(zname, tur, oge, uygulanan):
    for zdes, t, odes, why in YANLIS_ALARM:
        if t == tur and fnmatch.fnmatch(zname, zdes) and re.search(odes, oge):
            uygulanan[(zdes, t, why)] += 1
            return True
    return False


def yollar(md):
    for m in LINK.finditer(md):
        t = m.group(1)
        if re.match(r"^(https?:|mailto:|#|/|~|[a-zA-Z]:\\)", t) or "://" in t or "{" in t or "<" in t:
            continue
        t = t.split("#")[0].split("?")[0]
        if t and ("/" in t or "." in t):
            yield t
    for m in TOKEN.finditer(md):
        t = m.group(1).split("#")[0].rstrip(".:,;!?")
        if t and "*" not in t:
            yield t


def denetle(z, dist, uygulanan):
    hatalar, zname = [], z.name
    p = subprocess.run([BSDTAR, "-tf", str(z)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ents = [e for e in p.stdout.splitlines() if e.strip()]
    if p.returncode != 0 or not ents:
        return None, [("tar -tf", "açılmıyor")]
    kok = {e.split("/")[0] for e in ents}
    if len(kok) != 1:
        return None, [("yapı", f"kökte {len(kok)} öğe: {sorted(kok)[:3]}")]
    ad = kok.pop()
    if f"{ad}/SKILL.md" not in ents:
        return ad, [("yapı", f"{ad}/SKILL.md yok")]
    files = {e.rstrip("/") for e in ents}
    zf = zipfile.ZipFile(z)
    # claude.ai Add ekranı ret kuralları
    ic_zip = [e for e in ents if e.lower().endswith(".zip")]
    if ic_zip:
        hatalar.append(("iç içe zip", ", ".join(ic_zip)))
    manifest = [e for e in ents if (".claude-plugin" in e.split("/") or e.endswith("/plugin.json"))
                and not alarm(zname, "manifest", e, uygulanan)]
    if manifest:
        hatalar.append(("plugin manifest", f"{len(manifest)} öğe: {manifest[0]}"))
    acik = sum(i.file_size for i in zf.infolist())
    if acik > 30 * 10**6:
        hatalar.append(("açık boyut", f"{acik / 10**6:.1f} MB > 30 MB"))
    md = zf.read(f"{ad}/SKILL.md").decode("utf-8", errors="replace")
    m = re.match(r"^\ufeff?---\s*\r?\n(.*?)\r?\n---", md, re.S)
    try:
        fm = yaml.safe_load(m.group(1)) if m else None
        assert isinstance(fm, dict)
    except Exception:
        return ad, [("frontmatter", "YAML okunamadı")]
    if fm.get("name") != ad:
        hatalar.append(("name", f"name={fm.get('name')!r} ≠ klasör {ad!r}"))
    dl = len(str(fm.get("description") or "").strip())
    if not 1 <= dl <= 200:
        hatalar.append(("description", f"{dl} karakter"))
    for t in sorted(set(yollar(md))):
        hedef = posixpath.normpath(posixpath.join(ad, t))
        if hedef in files or any(f.startswith(hedef + "/") for f in files):
            continue
        if not alarm(zname, "yol", t, uygulanan):
            hatalar.append(("yol", f"{t} zip'te yok"))
    for e in ents:
        if e.endswith("/") or Path(e).suffix.lower() not in TEXT_EXT:
            continue
        for i, line in enumerate(zf.read(e).decode("utf-8", errors="replace").splitlines(), 1):
            if "~/.claude" in line and not alarm(zname, "claude", f"{e}: {line.strip()}", uygulanan):
                hatalar.append(("~/.claude", f"{e}:{i}"))
    return ad, hatalar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dist")
    ap.add_argument("--rapor")
    a = ap.parse_args()
    dist = Path(a.dist)
    kok_zip = sorted(dist.glob("*.zip"))
    yukle = sorted((dist / "yukle-6c").rglob("*.zip")) if (dist / "yukle-6c").exists() else []
    uygulanan, sonuc, adlar = Counter(), [], {}
    for z in kok_zip + yukle:
        ad, h = denetle(z, dist, uygulanan)
        rel = z.relative_to(dist).as_posix()
        sonuc += [(rel, k, d) for k, d in h]
        if z.parent == dist and ad:
            adlar.setdefault(ad, []).append(rel)
    for ad, zs in adlar.items():
        if len(zs) > 1:
            sonuc += [(z, "ad tekil", f"{ad} {len(zs)} zip'te") for z in zs]
        if ad in YERLESIK:
            sonuc += [(zs[0], "yerleşik ad", ad)]
    sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
    for z in yukle:
        k = dist / z.name
        if not k.exists() or sha(k) != sha(z):
            sonuc.append((z.relative_to(dist).as_posix(), "kopya", "dist kökündeki eşiyle aynı değil"))
    ozet = f"{len(kok_zip) + len(yukle)} zip denetlendi (kök {len(kok_zip)}, yukle-6c {len(yukle)}) · {len(sonuc)} hata · {sum(uygulanan.values())} yanlış alarm uygulandı"
    print(ozet)
    for k, v in Counter(k for _, k, _ in sonuc).items():
        print(f"  {k}: {v}")
    if a.rapor:
        L = ["# KURULUM-6c skill zip denetimi", "", f"`python tools/skill_denetim.py {a.dist}` · _yerlesik hariç", "", ozet, ""]
        if sonuc:
            L += ["## Hatalar", ""] + [f"- {z} · {k} · {d}" for z, k, d in sonuc] + [""]
        L += ["## Uygulanan yanlış alarmlar", ""] + [f"- {zd} · {t} · {n} kez · {why}" for (zd, t, why), n in uygulanan.items()]
        Path(a.rapor).write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.exit(1 if sonuc else 0)


if __name__ == "__main__":
    main()
