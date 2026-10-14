"""ÖĞREN-1 adım 1: token araçlarının özgün metni → ücretsiz model (OmniRoute openrouter :free, düşerse ollama yerel) sabit şemalı özet
→ .kos/kopru/ogren/ozet-token.jsonl. Tavan: en fazla 90 model çağrısı (kalem başına ≤2 kol). Claude bu metinleri okumaz.
  python -X utf8 .claude/ogren1/ozet.py"""
import json, subprocess, sys, time, urllib.request, zipfile
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / ".claude/omniroute1"))
from pilot import env_oku  # noqa: E402

CIKTI = KOK / ".kos/kopru/ogren/ozet-token.jsonl"
TAVAN, CAGRI = 90, 0
KOLLAR = [("omni", "openrouter/nvidia/nemotron-3-super-120b-a12b:free"), ("ollama", "gpt-oss:20b-cloud"), ("ollama", "qwen3.5:4b")]
SEMA = ("Aşağıdaki araç belgesini oku ve YALNIZ şu JSON nesnesini döndür (Türkçe, alan başına ≤2 cümle, uydurma yok; belgede yoksa \"belirsiz\"): "
        '{"ad":"","ne_yapar":"","mekanizma":"sıkıştırma|önbellek|bağlam dışı depolama|delegasyon|özetleme|tur azaltma|ölçüm|diğer + 1 cümle",'
        '"ne_zaman":"","komut":"en tipik 1-2 komut/çağrı","girdi_cikti":"","sinirlar":"","cakistigi_arac":"belgede adı geçen benzer/çakışan araçlar"}')
D = {k: str(v) for k, v in [(l.split("\t")[0], l.split("\t")[2]) for l in (KOK / ".claude/ogren1/yollar.tsv").read_text(encoding="utf-8").splitlines()] if v != "-"}
Z = "C:/Projeler/omer-skills/dist/"
D.update({
    "rtk": "cmd:rtk --help", "headroom": "cmd:headroom --help", "graphify": "cmd:graphify --help", "qmd": "cmd:qmd --help",
    "headroom-compress": Z + "yukle-10b/replace/headroom-compress.zip", "omni-cache": Z + "yukle-7/omniroute-omni-cache.zip",
    "omni-compression": Z + "yukle-7/omniroute-omni-compression.zip", "omni-context-rtk": Z + "omniroute-omni-context-rtk.zip",
    "cli-compression": Z + "omniroute-cli-compression.zip", "cli-contexts": Z + "omniroute-cli-contexts.zip",
    "cli-cost-usage": Z + "omniroute-cli-cost-usage.zip",
})


def metin(kaynak):
    if kaynak.startswith("cmd:"):
        p = subprocess.run(kaynak[4:], shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        return p.stdout + p.stderr
    y = Path(kaynak)
    if y.suffix == ".zip":
        with zipfile.ZipFile(y) as z:
            return z.read(next(n for n in z.namelist() if n.endswith("SKILL.md"))).decode("utf-8", "replace")
    if y.is_dir():
        y = next((y / n for n in ("SKILL.md", "README.md", "readme.md") if (y / n).is_file()), None) or next(y.rglob("SKILL.md"))
    return y.read_text(encoding="utf-8", errors="replace")


def sor(kol, model, istem):
    global CAGRI
    assert CAGRI < TAVAN, "çağrı tavanı"
    CAGRI += 1
    if kol == "omni":
        url, h = "http://127.0.0.1:20128/v1/chat/completions", {"authorization": f"Bearer {env_oku('OMNIROUTE_KEY')}", "user-agent": "curl/8.4"}
    else:
        url, h = "http://127.0.0.1:11434/v1/chat/completions", {}
    q = urllib.request.Request(url, method="POST", headers={"content-type": "application/json", **h},
                               data=json.dumps({"model": model, "max_tokens": 4000, "temperature": 0,
                                                "messages": [{"role": "user", "content": istem}]}).encode())
    y = json.load(urllib.request.urlopen(q, timeout=240))["choices"][0]["message"].get("content") or ""
    return json.loads(y[y.index("{"):y.rindex("}") + 1])


bitti = {json.loads(s)["ad"] for s in CIKTI.read_text(encoding="utf-8").splitlines()} if CIKTI.exists() else set()
for ad, kaynak in D.items():
    if ad in bitti:
        continue
    try:
        m = metin(kaynak)[:9000]
    except Exception as e:
        print(ad, "KAYNAK-YOK", type(e).__name__, flush=True)
        continue
    for kol, model in KOLLAR:
        t = time.time()
        try:
            o = sor(kol, model, f"{SEMA}\n\nAraç adı: {ad}\n---\n{m}")
        except AssertionError:
            sys.exit("TAVAN")
        except Exception as e:
            print(ad, model, "HATA", type(e).__name__, str(e)[:80], flush=True)
            continue
        o.update(ad=ad, kaynak=kaynak, model=model, sn=round(time.time() - t))
        with CIKTI.open("a", encoding="utf-8") as f:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
        print(ad, model, "ok", o["sn"], flush=True)
        break
print("BITTI cagri", CAGRI, flush=True)
