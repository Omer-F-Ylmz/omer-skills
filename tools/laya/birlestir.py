"""LAYA-2 kurul birleştirici: sağlayıcı puanlarından Opus'a ridge (eğitim yarısı test=False; ρ yalnız test=True'da).
  python birlestir.py [kurul.jsonl ...]   → test ρ/MAE (ortalama · ağırlıklı · ridge), ağırlıkları birlestir.json'a yazar"""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK.parent / "omer-skills-wt/jev/.claude/jev1"))
from karsilastir_ab import spearman  # noqa: E402

D = KOK / ".claude/laya2"
SAG = ["gemini", "groq", "openrouter", "mistral", "nvidia", "omniroute"]


def yukle(dosyalar):
    op = {k["id"]: k for k in map(json.loads, open(D / "opus.jsonl", encoding="utf-8"))}
    p = {}
    for f in dosyalar:
        for r in map(json.loads, open(f, encoding="utf-8")):
            if r["id"] in op:
                p.setdefault(r["id"], {}).update(r["puan"])
    return [(op[i], p[i]) for i in p]


def ozellik(k, ps):  # sağlayıcı puanı (yoksa kurul ortalaması) + eksiklik göstergesi + uzunluk
    m = sum(ps.values()) / len(ps)
    x = [ps.get(s, m) for s in SAG] + [m, len(ps), np.log1p(len(k["state"]["yanit"]))]
    return x


def ridge(X, y, a):
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.c_[(X - mu) / sd, np.ones(len(X))]
    w = np.linalg.solve(Z.T @ Z + a * np.eye(Z.shape[1]), Z.T @ y)
    return lambda Q: np.c_[(Q - mu) / sd, np.ones(len(Q))] @ w


def main():
    v = yukle([Path(a) for a in sys.argv[1:]] or [D / "kurul.jsonl", D / "kurul-opus.jsonl"])
    tr = [(k, p) for k, p in v if not k["test"]]
    te = [(k, p) for k, p in v if k["test"]]
    print(f"n={len(v)} eğitim={len(tr)} test={len(te)}")
    X = lambda s: np.array([ozellik(k, p) for k, p in s], float)  # noqa: E731
    y = lambda s: np.array([k["opus"] / 2 for k, _ in s], float)  # noqa: E731
    ort = [sum(p.values()) / len(p) for _, p in te]
    print(f"test ortalama ρ={spearman(ort, list(y(te)))}")
    for a in (1, 10, 30, 100):
        f = ridge(X(tr), y(tr), a)
        c = f(X(te))
        print(f"ridge a={a}: test ρ={spearman(list(c), list(y(te)))} MAE={np.abs(c - y(te)).mean():.2f}")


if __name__ == "__main__":
    main()
