"""30 yeni rastgele skill (seed 31, tur4 seti hariç) → girdi31.tsv: ad \t açıklama."""
import json, random
from pathlib import Path
K = Path(__file__).parent
d = json.loads(Path("C:/Users/pc/.claude/ertele-dizin.json").read_text(encoding="utf-8"))
eski = {l.split("\t")[0] for l in (K.parents[0] / "ertele9/girdi.tsv").read_text(encoding="utf-8").splitlines()}
aday = sorted(a for a, v in d.items() if v["tur"] == "skill" and not a.startswith("departman-") and a not in eski and Path(v["yol"]).is_file())
random.seed(31)
sec = random.sample(aday, 30)
(K / "girdi31.tsv").write_text("".join(f"{a}\t{d[a]['acik'][:200]}\n" for a in sec), encoding="utf-8")
print(len(aday))
