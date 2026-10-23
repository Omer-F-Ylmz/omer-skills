"""LAYA-2 kurul istemi denemesi: Opus etiketli alt kümede istem varyantı × sağlayıcı → Spearman ρ (Claude $0).
  python istem_dene.py <varyant> [sağlayıcılar,] [n=100] [işçi=6]   çıktı: .claude/laya2/dene-<varyant>.jsonl (yeniden koşunca devam)
  python istem_dene.py rapor <varyant,...>                         varyant×sağlayıcı ρ tablosu"""
import functools
import json
import random
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(KOK.parent / "omer-skills-wt/jev/.claude/jev1"))
import puan  # noqa: E402
import ucretsiz_havuz as uh  # noqa: E402

D = KOK / ".claude/laya2"
YK = threading.Lock()
_y = uh._yaz
uh._yaz = lambda d: (YK.acquire(), _y(d), YK.release())  # noqa: E731

GOVDE = "GÖREV:\n{gorev}\n\nKABUL ÖLÇÜTÜ:\n{kabul}\n\nYANIT:\n{yanit}\n\n"
IST = {
    "v1": ("Bir yanıtı kabul ölçütüne göre 0-10 puanla. Yalnızca içeriği yargıla (doğruluk, ölçütün her parçasının karşılanması, gereksiz/yanlış iddia yok); biçim ve uzunluk değil.\n"
           "Çapalar: 10=ölçütün her parçası doğru ve eksiksiz; 8=ölçüt karşılanmış ama küçük eksik/belirsizlik; 6=önemli bir parça eksik ya da kısmen yanlış; 4=ölçütün yarısından azı; 2=çoğunlukla yanlış/alakasız; 0=boş/alakasız.\n"
           "Önce en çok iki cümleyle neyin karşılandığını/eksik olduğunu yaz, sonra son satırda yalnızca şunu ver: {{\"score\": <0-10>}}\n\n" + GOVDE),
    "v2": ("Bir yanıtı kabul ölçütüne göre denetle. Önce ölçütü 2-4 somut maddeye ayır; her madde için yanıtta KARŞILANDI / KISMEN / YOK yaz (tek satır, kanıt kelimesiyle). "
           "Yanıtta ölçütte olmayan yanlış teknik iddia varsa ekle: YANLIŞ İDDİA. Sonra son satırda yalnızca şunu ver: {{\"score\": <0-10>}} "
           "(10=tüm maddeler KARŞILANDI ve yanlış iddia yok; her KISMEN ~-1.5, her YOK ~-3, her YANLIŞ İDDİA ~-2).\n\n" + GOVDE),
}


def ayikla(m):
    return puan.ayikla(m, 10)


@functools.lru_cache(maxsize=None)
def altin():
    """v3 kalibrasyon örnekleri: yalnız eğitim yarısından, Opus düzeyi başına en kısa yanıtlar; altkume'ye girmez."""
    op = [k for k in map(json.loads, open(D / "opus.jsonl", encoding="utf-8")) if not k["test"]]
    return [k for d, adet in ((4, 1), (6, 1), (8, 2), (10, 2)) for k in sorted((k for k in op if k["opus"] == d), key=lambda k: len(k["state"]["yanit"]))[:adet]]


def ornek_blok():
    return "USTA PUANLI ÖRNEKLER (aynı ölçek; bu örneklerin puanını ölçek çapası al):\n" + "".join(
        f"- GÖREV: {k['state']['gorev'][:250]} | ÖLÇÜT: {k['state'].get('kabul', '')[:250]} | YANIT: {k['state']['yanit'][:450]} => {{\"score\": {k['opus']}}}\n"
        for k in altin()) + "\n"


def istem(v, s):
    p = IST["v2" if v == "v3" else v].format(gorev=s["gorev"][:1500], kabul=s.get("kabul", "")[:600], yanit=s["yanit"][:3000])
    if v == "v3":
        bas, son = p.split("GÖREV:\n", 1)
        p = bas + ornek_blok() + "GÖREV:\n" + son
    return p


def altkume(n):
    ay = {k["id"] for k in altin()}
    op = [k for k in map(json.loads, open(D / "opus.jsonl", encoding="utf-8")) if k["id"] not in ay]
    dusuk = [k for k in op if k["opus"] <= 6]
    diger = [k for k in op if k["opus"] > 6]
    random.Random(7).shuffle(diger)
    return dusuk + diger[: max(n - len(dusuk), 0)]


def main():
    v, sag = sys.argv[1], (sys.argv[2].split(",") if len(sys.argv) > 2 else ["mistral", "groq", "nvidia", "openrouter"])
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    isci = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    cik = D / f"dene-{v}.jsonl"
    var = {(r["id"], r["pr"]) for r in map(json.loads, open(cik, encoding="utf-8"))} if cik.exists() else set()
    is_ = [(k, p) for k in altkume(n) for p in sag if (k["id"], p) not in var]
    print(f"{v}: {len(is_)} çağrı", flush=True)
    kl = threading.Lock()

    def calis(a):
        k, p = a
        m, _, _ = uh.cagir("hakem", istem(v, k["state"]), max_tokens=2500, saglayici=p, dogrula=lambda y: None if ayikla(y) is not None else "puan yok", zaman=70)
        if m is not None:
            with kl:
                open(cik, "a", encoding="utf-8").write(json.dumps({"id": k["id"], "pr": p, "s": ayikla(m)}) + chr(10))

    with ThreadPoolExecutor(isci) as ex:
        list(ex.map(calis, is_))
    print("BITTI", flush=True)


def rapor(vs):
    from karsilastir_ab import spearman
    op = {k["id"]: k["opus"] for k in map(json.loads, open(D / "opus.jsonl", encoding="utf-8"))}
    for v in vs:
        pu = {}
        for r in map(json.loads, open(D / f"dene-{v}.jsonl", encoding="utf-8")):
            pu.setdefault(r["id"], {})[r["pr"]] = r["s"]
        for pr in sorted({p for d in pu.values() for p in d}) + ["ORT"]:
            a = [((sum(d.values()) / len(d)) if pr == "ORT" else d[pr], op[i]) for i, d in pu.items() if pr == "ORT" or pr in d]
            print(f"{v} {pr}: n={len(a)} ρ={spearman([x for x, _ in a], [y for _, y in a])}")


if __name__ == "__main__":
    rapor(sys.argv[2].split(",")) if sys.argv[1] == "rapor" else main()
