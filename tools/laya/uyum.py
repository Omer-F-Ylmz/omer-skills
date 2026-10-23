"""LAYA-2 kurul↔Opus uyumu: kurul.jsonl'deki Opus etiketli öğelerde sağlayıcı başına ve kurul (ortalama / ağırlıklı) Spearman ρ.
  python uyum.py [kurul.jsonl] [opus.jsonl]  → sağlayıcı ρ tablosu; ağırlık = max(ρ,0) (uyum.json'a yazılır, kurul etiketi bunu kullanır)"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK.parent / "omer-skills-wt/jev/.claude/jev1"))
from karsilastir_ab import spearman  # noqa: E402

D = KOK / ".claude/laya2"


def yukle(kurul, opus):
    op = {k["id"]: k for k in map(json.loads, open(opus, encoding="utf-8"))}
    return [(op[r["id"]], r["puan"]) for r in map(json.loads, open(kurul, encoding="utf-8")) if r["id"] in op]


def kurul_puan(p, w=None):
    w = w or {}
    t = sum(w.get(k, 1) for k in p)
    return sum(v * w.get(k, 1) for k, v in p.items()) / t if t else None


def main():
    kurul = sys.argv[1] if len(sys.argv) > 1 else D / "kurul.jsonl"
    opus = sys.argv[2] if len(sys.argv) > 2 else D / "opus.jsonl"
    v = yukle(kurul, opus)
    o = [k["opus"] / 2 for k, _ in v]
    print(f"n={len(v)} (Opus etiketli, kurulda)")
    w = {}
    for pr in sorted({p for _, ps in v for p in ps}):
        a = [(ps[pr], k["opus"] / 2) for k, ps in v if pr in ps]
        r = spearman([x for x, _ in a], [y for _, y in a]) if len(a) > 5 else None
        w[pr] = max(r or 0, 0.05)
        print(f"  {pr}: n={len(a)} ρ={r} MAE={sum(abs(x - y) for x, y in a) / len(a):.2f}")
    for ad, ww in (("ortalama", None), ("ağırlıklı", w)):
        c = [kurul_puan(ps, ww) for _, ps in v]
        print(f"kurul {ad}: ρ={spearman(c, o)} MAE={sum(abs(x - y) for x, y in zip(c, o)) / len(o):.2f}")
    (D / "uyum.json").write_text(json.dumps(w), encoding="utf-8")


if __name__ == "__main__":
    main()
