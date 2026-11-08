"""VIDEO-KAYNAK (b): 'Ek kaynak satırları' -> sınıf (kur / ogren-uygula / kurulu-kanitli) -> ek-kaynak-sinif.tsv.
Kanıt: kurulu skill/plugin/araç adı ~/.claude/skills, plugins/cache ve repo skills/ içinde aranır."""
import json, os, pathlib, re, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "rapor/yarim-tara-27eki.md"
OUT = ROOT / "docs/kaynak-kutuphane/ek-kaynak-sinif.tsv"
KEY = os.environ.get("GROQ_API_KEY")
HOME = pathlib.Path.home() / ".claude"
INSTALLED = {p.name.lower() for d in (HOME / "skills", ROOT / "skills") if d.exists() for p in d.iterdir()}
INSTALLED |= {p.name.lower() for p in (HOME / "plugins/cache").glob("*/*")} if (HOME / "plugins/cache").exists() else set()

PROMPT = """Her satır bir iş/not satırı. Her satır için JSON dizisi döndür: [{"i":<no>,"sinif":"kur|ogren-uygula|kurulu|kaynak-degil","ad":"satırdaki araç/skill/repo adı (yoksa '')","not":"<=12 kelime"}].
kur = henüz kurulmamış araç/skill/MCP/site kurulacak; ogren-uygula = yöntem/kural/bilgi uygulanacak; kurulu = satır zaten kurulu/yapıldı ([x], tamam, kuruldu) diyor; kaynak-degil = durum/yol haritası notu, kurulacak/öğrenilecek kaynak yok. Yalnız JSON."""


def chat(lines):
    body = json.dumps({"model": "qwen/qwen3.8-27b", "temperature": 0, "max_tokens": 3500,
                       "messages": [{"role": "user", "content": PROMPT + "\n\n" + "\n".join(f"{i}: {l[:300]}" for i, l in lines)}]}).encode()
    req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", body,
                                 {"Content-Type": "application/json", "Authorization": f"Bearer {KEY}", "User-Agent": "curl/8"})
    t = json.loads(urllib.request.urlopen(req, timeout=180).read())["choices"][0]["message"]["content"]
    return json.loads(re.search(r"\[.*\]", t, re.S).group(0))


def main():
    txt = SRC.read_text(encoding="utf-8").splitlines()
    a = next(i for i, l in enumerate(txt) if l.startswith("## Ek kaynak satırları"))
    b = next(i for i in range(a + 1, len(txt)) if txt[i].startswith("## "))
    rows = [l[2:] for l in txt[a:b] if l.startswith("- ")]
    res = {}
    if OUT.exists():
        for ln in OUT.read_text(encoding="utf-8").splitlines()[1:]:
            f = ln.split("	")
            if len(f) >= 6 and f[1] not in ("SINIFLANMADI", "sinif") and f[0].isdigit():
                res[int(f[0])] = {"sinif": f[1], "ad": f[2], "not": f[4]}
    for k in range(0, len(rows), 8):
        chunk = [c for c in list(enumerate(rows))[k:k + 8] if c[0] not in res]
        if not chunk:
            continue
        for deneme in range(3):
            try:
                for r in chat(chunk):
                    res[r["i"]] = r
                break
            except Exception as e:
                print("parti hata", k, type(e).__name__, getattr(e, "code", ""), str(e)[:80], flush=True)
                time.sleep(20)
    out = ["no\tsinif\tad\tkanit\tnot\tkaynak_satir"]
    for i, l in enumerate(rows):
        r = res.get(i, {"sinif": "SINIFLANMADI", "ad": "", "not": ""})
        ad, sinif = r.get("ad", ""), r.get("sinif", "")
        kanit = ""
        if ad and ad.lower() in INSTALLED:
            kanit = "kurulu:" + ad.lower()
            if sinif == "kur":
                sinif = "kurulu"
        out.append("\t".join([str(i), sinif, ad, kanit, r.get("not", ""), l.replace("\t", " ")[:200]]))
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    from collections import Counter
    print(len(rows), Counter(x.split("\t")[1] for x in out[1:]))


main()
