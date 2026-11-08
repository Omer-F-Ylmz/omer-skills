"""OLLAMA-1 A/B: kacan-karar-3.tsv'den 120 rastgele satÄ±r, karar gizli â†’ sonnet vs ollama modelleri."""
import csv, json, random, subprocess, sys, time
sys.path.insert(0, "video")
from video.ucuz import SISTEM, siniflandir

satir = list(csv.DictReader(open("../../docs/kurulumlar/kacan-karar-3.tsv", encoding="utf-8"), delimiter="\t"))
random.Random(1).shuffle(satir)
satir = satir[:120]
terim = [s["terim"] for s in satir]
gercek = [s["karar"] for s in satir]
PARCA = 40


def sonnet(t):
    p = SISTEM + "\n\nTerimler:\n" + json.dumps(t, ensure_ascii=False)
    r = subprocess.run(["claude", "-p", "--model", "sonnet", "--output-format", "json"], input=p,
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    j = json.loads(r.stdout)
    k = json.loads(j["result"][j["result"].index("{"):j["result"].rindex("}") + 1])["kararlar"]
    return k, j.get("total_cost_usd", 0)


def ollama(m):
    def f(t):
        return siniflandir(t, model=m)[0], 0
    return f


yollar = {"gpt-oss:120b-cloud": ollama("gpt-oss:120b-cloud"),
          "gemma4:cloud": ollama("gemma4:cloud"), "qwen3.5:4b(yerel)": ollama("qwen3.5:4b")}
for ad, fn in yollar.items():
    t0, dogru, usd, hata = time.time(), 0, 0.0, 0
    for i in range(0, 120, PARCA):
        try:
            k, c = fn(terim[i:i + PARCA])
            usd += c
            dogru += sum(a == b for a, b in zip(k, gercek[i:i + PARCA]))
        except Exception as e:
            hata += 1
            print(ad, "hata", str(e)[:120])
    print(f"{ad} | doÄŸru {dogru}/120 ({dogru/1.2:.1f}%) | {time.time()-t0:.0f}s | ${usd:.4f} | hatalÄ± parÃ§a {hata}")

