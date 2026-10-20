"""Tek soru teşhisi: python tani.py <id> — dönen parçalar (kaynak:satır, ilk satır) ve cevap/kaynak."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import beyin  # noqa: E402

for s in (Path(__file__).parent.parent / "beyin2/sorular.jsonl").read_text(encoding="utf-8").splitlines():
    q = json.loads(s) if s.strip() else None
    if q and str(q["id"]) in sys.argv[1:]:
        print(q["id"], q["soru"], "=>", q["cevap"], "|", q["kaynak"].replace("C:/Projeler/omer-skills/", ""))
        print(" ids:", beyin.kimlikler(q["soru"]))
        for k, no, sat in beyin.ara(q["soru"], 3):
            print("  ", Path(k).name[:30], no, "|", " / ".join(sat)[:90])
