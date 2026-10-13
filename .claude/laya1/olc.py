"""LAYA-1 ölçüm: etiketli yargı verisi (Opus ref + Jev puanı) üzerinde Laya sıfır-atış / ince ayarlı ↔ Jev, ayrılmış test kümesinde.
  python olc.py veri            → veri.jsonl (id, kaynak, state, soru, opus 0-10, jev 0-10) + bölme (sha(id) → %50 test)
  python olc.py puanla <kol> [model] → <kol>.json (Laya puanları, jev_yargic önbelleği ayrı dosya)
  python olc.py rapor <kol>...  → test ρ/MAE (Opus'a karşı), jeton/$, karma %20
claude -p 0, Jev çağrısı 0 (Jev puanları kayıtlı veriden). Laya yerel, $0."""
import hashlib
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
WT = Path(__file__).resolve().parents[2]
J1 = Path("C:/Projeler/omer-skills-wt/jev/.claude/jev1")
sys.path[:0] = [str(WT / "tools" / "olcum"), str(WT / "tools" / "jev"), str(J1)]
import jev_yargic  # noqa: E402
from karsilastir_ab import spearman  # noqa: E402
from laya_tasiyici import LayaTasiyici  # noqa: E402

D = Path(__file__).parent
JEV_TL_M = 0.042  # $/M girdi jetonu (jev_yargic başlığı)
SORULAR = {"SORU": jev_yargic.SORU,  # JEV-1 (a) yanıt kalitesi, score 0-5 → 0-10
           "ESLES": {"kalite": {"type": "noul", "instructions": "Does the report line `satir` state the same tool, "
                                "claim or item as the gold item `altin` (same thing, possibly paraphrased)?"}}}


def test_mi(i):
    return int(hashlib.sha256(i.encode()).hexdigest(), 16) % 2 == 0


def veri():
    out = []
    jev1 = {k["dosya"]: k for k in map(json.loads, open(J1 / "jev_tum.jsonl", encoding="utf-8"))}
    dos, opus = json.load(open(J1 / "ornek_sira.json")), json.load(open(J1 / "opus_ref.json"))
    for i, d in enumerate(dos):
        out.append({"id": "jev1:" + d, "kaynak": "jev1", "soru": "SORU", "state": jev1[d]["state"],
                    "opus": opus[str(i)] * 2, "jev": jev1[d]["jev"]})
    jb, ob = [json.loads(x) for x in open(J1 / "jev_b.jsonl", encoding="utf-8")], json.load(open(J1 / "opus_b.json"))
    for i, b in enumerate(jb):  # JEV-1 (b) video altın↔rapor eşleşmesi, Opus evet/hayır → 10/0, Jev noul p → 0-10
        out.append({"id": f"video:{i}", "kaynak": "video", "soru": "ESLES", "state": {"altin": b["altin"], "satir": b["satir"]},
                    "opus": 10 * ob[str(i)], "jev": round(10 * b["jev_ham"]["noul"], 2)})
    for k in out:
        k["test"] = test_mi(k["id"])
    with open(D / "veri.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(k, ensure_ascii=False) + "\n" for k in out)
    print(f"veri: n={len(out)} test={sum(k['test'] for k in out)}")


def yukle():
    return [json.loads(x) for x in open(D / "veri.jsonl", encoding="utf-8")]


def puanla(kol, model="multilingual"):
    v, t = yukle(), LayaTasiyici(model=model)
    t0, out = time.perf_counter(), {}
    for soru in sorted({k["soru"] for k in v}):
        ks = [k for k in v if k["soru"] == soru]
        c = jev_yargic.yargila([k["state"] for k in ks], SORULAR[soru], t, D / f"ob-{kol}.json")
        out.update({k["id"]: (None if x is None else round(x["kalite"]["score"] * 2, 2)
                                          if "score" in x["kalite"] else round(10 * x["kalite"]["noul"], 2)) for k, x in zip(ks, c)})
    jeton = sum(u["input_tokens"] for u in t.kullanim)
    json.dump({"puan": out, "jeton": jeton, "sn": round(time.perf_counter() - t0, 1)}, open(D / f"{kol}.json", "w"))
    print(f"{kol}: n={len(out)} jeton {jeton} süre {time.perf_counter() - t0:.1f}s")


def rapor(*kollar):
    for kaynak in ("jev1", "video"):
        _rapor(kaynak, kollar)


def _rapor(kaynak, kollar):
    v = [k for k in yukle() if k["test"] and k["kaynak"] == kaynak]
    o = [k["opus"] for k in v]
    dogru = lambda a: sum((x >= 5) == (y >= 5) for x, y in zip(a, o))  # noqa: E731
    mae = lambda a: round(sum(abs(x - y) for x, y in zip(a, o)) / len(o), 2)  # noqa: E731
    jv = [k["jev"] for k in v]
    print(f"[{kaynak}] test n={len(v)} · Jev: ρ {spearman(jv, o)} MAE {mae(jv)} doğru(≥5) {dogru(jv)}")
    for kol in kollar:
        r = json.load(open(D / f"{kol}.json"))
        lv = [r["puan"][k["id"]] for k in v]
        sec = set(jev_yargic.belirsiz(lv))
        karma = [o[i] if i in sec else x for i, x in enumerate(lv)]
        print(f"{kol}: ρ {spearman(lv, o)} MAE {mae(lv)} doğru(≥5) {dogru(lv)} · karma%20 ρ {spearman(karma, o)} · jeton(tüm) {r['jeton']} "
              f"(Jev ödemesi ≈ ${r['jeton'] * JEV_TL_M / 1e6:.4f}, Laya $0) · {r['sn']}s")


if __name__ == "__main__":
    {"veri": veri, "puanla": puanla, "rapor": rapor}[sys.argv[1]](*sys.argv[2:])
