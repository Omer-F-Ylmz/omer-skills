"""TOKEN-11 skill listesi ölçümü. `envanter` (çağrısız): CC'nin son skill_listing eki + SKILL.md açıklama uzunlukları,
sahiplik ve B (bizim açıklamalar ≤90 kr) kr farkı. `tel` (2 claude -p, sonnet): A = mevcut, Z = listelenen her skill 'off'
(geçici CLAUDE_CONFIG_DIR, settings.json kopyası) → listenin wire jeton bedeli ve kr→jeton oranı. Canlı ~/.claude'a yazılmaz."""
import json, os, re, shutil, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf8")
EV = Path.home() / ".claude"
WT = Path("C:/Projeler/omer-skills-wt/token11")
TABAN = ["-p", "--output-format", "json", "--model", "sonnet", "--settings", json.dumps({"promptCacheTtl": "5m"})]
KIRP = 90


def son_liste():
    for f in sorted((EV / "projects").glob("*/*.jsonl"), key=os.path.getmtime, reverse=True):
        for s in f.read_text(encoding="utf8", errors="ignore").splitlines():
            if '"skill_listing"' in s:
                at = json.loads(s).get("attachment") or {}
                if at.get("type") == "skill_listing":
                    return at["content"]


def aciklama(md):
    m = re.search(r"^---\s*\n(.*?)\n---", md.read_text(encoding="utf8", errors="ignore"), re.S)
    if not m:
        return ""
    d = re.search(r"^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", m.group(1), re.S | re.M)
    return " ".join(d.group(1).strip().strip("\"'>|").split()) if d else ""


def aciklamalar():
    """ad → açıklama: yerel skills, kurulu plugin'ler (installPath), claude.ai senkron kopyaları."""
    d = {}
    for md in (EV / "skills").glob("*/SKILL.md"):
        d[md.parent.name] = aciklama(md)
    ip = json.loads((EV / "plugins" / "installed_plugins.json").read_text(encoding="utf8"))
    for anahtar, kayitlar in (ip.get("plugins") or {}).items():
        for k in kayitlar[:1]:
            for md in Path(k["installPath"]).glob("**/skills/*/SKILL.md"):
                d.setdefault(f"{anahtar.split('@')[0]}:{md.parent.name}", aciklama(md))
    for md in (EV / "plugins" / "synced").glob("**/SKILL.md"):
        d.setdefault(f"anthropic-skills:{md.parent.name}", aciklama(md))
    return d


def envanter():
    liste = son_liste().splitlines()
    adlar = [l[2:].split(": ", 1)[0] for l in liste]
    aciklamali = {l[2:].split(": ", 1)[0]: l for l in liste if ": " in l}
    repo = {Path(p).parent.name for p in subprocess.run(["git", "ls-files", "*SKILL.md"], cwd=WT, capture_output=True,
                                                         text=True, encoding="utf8").stdout.split() if p.startswith(("skills/", "plugins/"))}
    ov = json.loads((EV / "settings.json").read_text(encoding="utf8")).get("skillOverrides") or {}
    acs = aciklamalar()

    def sahip(ad):
        on, _, kok = ad.rpartition(":")
        if on == "anthropic-skills":
            return "claudeai-bizim" if kok in repo else "claudeai-diger"
        if on:
            return "plugin-bizim" if kok in repo and on in ("omer-skills", "blender") else "plugin"
        return "yerel-bizim" if ad in repo else "yerel-diger"

    print(f"liste: {len(liste)} satır · {sum(len(l) + 1 for l in liste)} kr · açıklamalı {len(aciklamali)} · override {Counter(ov.values())}")
    s = Counter(); kr = Counter(); acik_bulunan = 0
    for ad in adlar:
        k = sahip(ad); s[k] += 1
        a = acs.get(ad)
        if a is not None:
            acik_bulunan += 1; kr[k] += len(a)
    print("sahiplik (n · tam açıklama kr toplamı, listede değil):", {k: (s[k], kr[k]) for k in s}, "· açıklaması bulunan", acik_bulunan)
    print("tümü açıklamalı olsaydı ≈", sum(len(ad) + 4 + len(acs.get(ad, "")) for ad in adlar), "kr")
    b_fark = 0
    for ad, l in sorted(aciklamali.items()):
        a = l.split(": ", 1)[1]
        kazanc = max(0, len(a) - KIRP) if sahip(ad).endswith("bizim") else 0
        b_fark += kazanc
        print(f"  {ad} · {sahip(ad)} · {ov.get(ad, '-')} · {len(a)} kr · B kazanç {kazanc}")
    print(f"B (bizim açıklamalı satırlar ≤{KIRP} kr) fark: {b_fark} kr")


def kur(kok, kapali):
    kok.mkdir()
    for p in EV.iterdir():
        if p.is_dir():
            subprocess.run(["cmd", "/c", "mklink", "/J", str(kok / p.name), str(p)], capture_output=True, check=True)
        else:
            shutil.copy2(p, kok / p.name)
    shutil.copy2(Path.home() / ".claude.json", kok / ".claude.json")
    if kapali:
        ay = json.loads((kok / "settings.json").read_text(encoding="utf8"))
        ay["skillOverrides"] = {**ay.get("skillOverrides", {}), **{l[2:].split(": ", 1)[0]: "off" for l in son_liste().splitlines()}}
        (kok / "settings.json").write_bytes(json.dumps(ay, ensure_ascii=False, indent=2).encode("utf8"))


def sok(kok):
    for p in kok.iterdir():
        if p.is_junction():
            os.rmdir(p)  # junction: yalnız bağ silinir
    shutil.rmtree(kok)


def liste_eki(sid):
    for f in (EV / "projects").glob(f"*/{sid}.jsonl"):
        for s in f.read_text(encoding="utf8").splitlines():
            at = json.loads(s).get("attachment") or {}
            if at.get("type") == "skill_listing":
                return {"n": at.get("skillCount"), "kr": len(at.get("content") or "")}
        return {"n": 0, "kr": 0}


def tel():
    tmp = Path(tempfile.mkdtemp(prefix="t11skill_"))
    try:
        kur(tmp / "A", False); kur(tmp / "Z", True)
        for kol in ("A", "Z"):
            env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}  # api-kredi.kapali
            env["CLAUDE_CONFIG_DIR"] = str(tmp / kol)
            r = subprocess.run(["claude", *TABAN], input="tamam", capture_output=True, text=True, encoding="utf8",
                               cwd=WT, env=env, timeout=300, creationflags=0x08000000)
            try:
                j = json.loads(r.stdout)
            except ValueError:
                print(kol, "rc", r.returncode, r.stdout[:200], r.stderr[:200]); continue
            u = j.get("usage", {})
            top = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
            print(json.dumps({"kol": kol, "girdi": top, "liste": liste_eki(j.get("session_id"))}, ensure_ascii=False), flush=True)
    finally:
        for k in ("A", "Z"):
            if (tmp / k).exists():
                sok(tmp / k)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    {"envanter": envanter, "tel": tel}[sys.argv[1]]()
