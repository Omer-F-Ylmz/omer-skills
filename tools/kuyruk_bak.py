import re
from pathlib import Path

kok = Path(r"C:\Projeler\omer-skills")
cikti = kok / ".kos" / "kopru" / "log" / "kuyruk_bak.out.txt"
atla = {"node_modules", ".git", "graphify-out", "ana-liste-npm", "ana-liste-npm-2", ".venv", "dist", "site-packages"}
adaylar = []
for alt in (kok / ".kos", kok / "tools", kok / "data", kok / "docs"):
    if not alt.exists():
        continue
    for p in alt.rglob("*"):
        if atla & set(p.parts):
            continue
        if p.is_file() and p.suffix in (".md", ".txt", ".json", ".jsonl", ".csv", ".tsv") and p.stat().st_size < 50_000_000:
            t = p.read_text(encoding="utf-8", errors="ignore")
            n = len(set(re.findall(r"instagram\.com/(?:reel|p)/([A-Za-z0-9_-]+)", t)))
            y = len(set(re.findall(r"(?:youtu\.be/|v=|shorts/)([A-Za-z0-9_-]{11})", t)))
            if n + y >= 300:
                adaylar.append((n + y, n, y, str(p.relative_to(kok)), p.stat().st_size, round(p.stat().st_mtime)))
satirlar = [str(a) for a in sorted(adaylar, reverse=True)[:25]]
cikti.write_text("\n".join(satirlar) + "\nBITTI2\n", encoding="utf-8")
