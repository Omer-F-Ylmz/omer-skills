"""ERTELE-3 TUR4: kör skill tarifi için 30 rastgele skill (seed 30, departman-* hariç, dosyası var)."""
import json, random
from pathlib import Path
d = json.loads(Path("C:/Users/pc/.claude/ertele-dizin.json").read_text(encoding="utf-8"))
aday = sorted(a for a, v in d.items() if v.get("tur") == "skill" and not a.startswith("departman-") and Path(v["yol"]).is_file())
random.seed(30)
sec = random.sample(aday, 30)
Path(__file__).with_name("girdi.tsv").write_text("".join(f"{a}\t{d[a]['yol']}\n" for a in sec), encoding="utf-8")
print(len(aday), "aday;", ", ".join(sec))
