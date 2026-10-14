"""ozet.py'nin kaynak yarısı (D = yollar.tsv + ekler, metin()) — ozet.py import'ta özet döngüsünü koştuğu için döngüden önceki kısım exec edilir."""
from pathlib import Path

_k = (Path(__file__).parent / "ozet.py").read_text(encoding="utf-8")
exec(_k[:_k.index("\nfor ad, kaynak in D.items():")])
