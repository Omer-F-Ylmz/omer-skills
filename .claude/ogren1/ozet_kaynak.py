"""ozet.py'nin kaynak yarısı (D = yollar.tsv + ekler, metin()) — ozet.py import'ta özet döngüsünü koştuğu için döngüden önceki kısım exec edilir."""
from pathlib import Path

_k = (Path(__file__).parent / "ozet.py").read_text(encoding="utf-8")
exec(_k[:_k.index("\nfor ad, kaynak in D.items():")])
# d4/d7: qmd sınırları README'de (Requirements), `qmd --help`te yok — ozet3 ve son.py aynı belgeyi görsün (hakem de)
import os  # noqa: E402
D["qmd"] = str(Path(os.environ["LOCALAPPDATA"]) / "Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe"
               / "node-v24.19.0-win-x64/node_modules/@tobilu/qmd/README.md")
