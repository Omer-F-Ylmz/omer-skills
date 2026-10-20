"""ÖĞREN-6 d2 yazım yardımcısı: paketteki her kalem için numaralı aday satırlar (okuma amaçlı; alıntıyı yaz.py birebir çeker).
  python -X utf8 .claude/ogren6/goster.py N"""
import re, sys
from pathlib import Path

B = Path(__file__).parent
SINIR = re.compile(r"\b(never|must|only|warning|requires?|required|do not|don't|limit|avoid|caution|authori[sz]ed|permission|yalnız|dikkat|not |gerek)\b", re.I)
KOD = re.compile(r"^\s*(`[^`]+`|\$ |python|npx|uvx|dotnet|pip|npm|semgrep|gitleaks|docker|curl|strix|/[\w-]+)")
Y = 120


def goster(p):
    for blok in ("\n" + (B / f"v1-paket-{p}.md").read_text(encoding="utf-8")).split("\n## ")[1:]:
        ad = blok.split("\n", 1)[0].strip()
        yol = re.search(r"kaynak: (\S+)", blok).group(1)
        m = Path(yol).read_text(encoding="utf-8", errors="replace").splitlines()
        print(f"## {ad} · {len(m)}")
        i = next((j for j, x in enumerate(m) if x.lstrip().startswith("description:")), None)
        if i is not None:
            print(f"{i + 1}|{m[i].strip()[:Y]}")
            if m[i].rstrip().endswith((">", "|", ">-", "|-")):
                print(f"{i + 2}|{m[i + 1].strip()[:Y]}")
        if len(m) <= 12 and i is None:
            for j, x in enumerate(m):
                print(f"{j + 1}|{x.strip()[:Y]}")
            continue
        for j, x in [(j, x) for j, x in enumerate(m) if KOD.match(x) and len(x.strip()) >= 10 and x.isascii()][:3]:
            print(f"K{j + 1}|{x.strip()[:Y]}")
        for j, x in [(j, x) for j, x in enumerate(m) if SINIR.search(x) and len(x.strip()) >= 20 and x.isascii() and not x.lstrip().startswith("description:")][:3]:
            print(f"S{j + 1}|{x.strip()[:Y]}")


goster(sys.argv[1])
