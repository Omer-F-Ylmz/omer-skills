"""kapi3_<k1>.json + kapi3_<k2>.json → kapi3_kor.md (görev başına X/Y karışık, yalnız ajan adı) + kapi3_anahtar.json.
  python kor3.py A V1"""
import json, random, re, sys
from pathlib import Path

BURA = Path(__file__).parent
sys.path.insert(0, str(BURA))
from kapi3 import GOREV


def secimler(k):
    j = json.loads((BURA / f"kapi3_{k}.json").read_text(encoding="utf8"))
    m = re.search(r"\[.*\]", j["result"], re.S)
    return {d["no"]: d["ajan"] for d in json.loads(m.group(0))}, j.get("num_turns")


if __name__ == "__main__":
    k1, k2 = sys.argv[1:3]
    (s1, t1), (s2, t2) = secimler(k1), secimler(k2)
    rnd, anahtar, md = random.Random(813), {}, []
    for i, g in enumerate(GOREV, 1):
        x, y = (k1, k2) if rnd.random() < 0.5 else (k2, k1)
        anahtar[i] = {"X": x, "Y": y}
        sec = {k1: s1.get(i, "-"), k2: s2.get(i, "-")}
        md.append(f"## {i}. {g}\n- X: {sec[x]}\n- Y: {sec[y]}\n")
    (BURA / "kapi3_kor.md").write_text("\n".join(md), encoding="utf8")
    (BURA / "kapi3_anahtar.json").write_text(json.dumps({"anahtar": anahtar, "tur": {k1: t1, k2: t2}}), encoding="utf8")
    print("görev", len(GOREV), "seçim", len(s1), len(s2), "tur", {k1: t1, k2: t2})
