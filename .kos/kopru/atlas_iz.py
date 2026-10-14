"""ATLAS kullanım izi (salt-okur): python atlas_iz.py <kitap> [--gun N] [--proje DİZİN]
Kitaptaki (docs/atlas/<kitap>.md) VARSAYILAN araç adlarının son N gündeki CC transkriptlerinde tool_use girdisinde
(Skill adı, Agent subagent_type, Bash komutu, MCP aracı) kaç oturumda kullanıldığını sayar. Dosya yazmaz."""
import json, re, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
a = sys.argv[1:]
kitap = a[0]
gun = float(a[a.index("--gun") + 1]) if "--gun" in a else 7
proje = Path(a[a.index("--proje") + 1]) if "--proje" in a else Path.home() / ".claude" / "projects"

metin = (KOK / "docs" / "atlas" / f"{kitap}.md").read_text(encoding="utf-8")
adlar = {k["ad"] for k in map(json.loads, (KOK / "docs" / "atlas" / "kart.jsonl").read_text(encoding="utf-8").splitlines())
         if k.get("karar") == "VARSAYILAN" and f"`{k['ad']}`" in metin}
desen = {ad: re.compile(r"(?<![\w-])" + re.escape(ad) + r"(?![\w-])") for ad in adlar}


def girdiler(yol):
    for s in yol.open(encoding="utf-8", errors="replace"):
        if '"tool_use"' not in s:
            continue
        try:
            icerik = json.loads(s).get("message", {}).get("content", [])
        except json.JSONDecodeError:
            continue
        for c in icerik if isinstance(icerik, list) else []:
            if c.get("type") == "tool_use":
                yield c.get("name", "") + " " + json.dumps(c.get("input", {}), ensure_ascii=False)


esik = time.time() - gun * 86400
oturum, sayac = 0, dict.fromkeys(adlar, 0)
for t in proje.rglob("*.jsonl"):
    if t.stat().st_mtime < esik:
        continue
    gorulen = {ad for g in girdiler(t) for ad, d in desen.items() if d.search(g)}
    oturum += bool(gorulen)
    for ad in gorulen:
        sayac[ad] += 1
print(f"{kitap} · son {gun:g} gün · VARSAYILAN {len(adlar)} · kullanan oturum {oturum}")
for ad, n in sorted(sayac.items(), key=lambda x: -x[1]):
    print(f"{n:4d}  {ad}")
