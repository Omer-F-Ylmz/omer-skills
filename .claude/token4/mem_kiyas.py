"""TOKEN-4 A3: claude-mem gözlemcisi haiku ↔ Gemini çevrimdışı kalite kıyası (0 Anthropic çağrısı).
Bugünkü gözlemci oturumlarından N (girdi, haiku çıktısı) çifti; aynı girdi OmniRoute'ta Gemini'ye; kör yargıç (başka aile) 1-10 puanlar.
Not: gözlemcinin sistem istemi transkriptte yok → Gemini yalnız kullanıcı metnini görür (Gemini aleyhine).
  python mem_kiyas.py [N=20]"""
import json, random, re, sys, time
from pathlib import Path

sys.path.insert(0, r"C:\Projeler\omer-skills\tools")
import ucuz_alt

# OmniRoute dva/gemini 500 verdi (14 Eki 22:58); claude-mem gemini sağlayıcısı da doğrudan Google API'ye gider
GEMINI, YARGIC = "gemini-flash-latest", "cc-yedek-dis"
DIZ = Path(__file__).parent


def gemini(istem):
    import urllib.request, winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k: key = winreg.QueryValueEx(k, "GEMINI_API_KEY")[0]
    for _ in range(3):
        try:
            r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI}:generateContent",
                                       json.dumps({"contents": [{"parts": [{"text": istem}]}]}).encode(),
                                       {"Content-Type": "application/json", "x-goog-api-key": key})
            j = json.load(urllib.request.urlopen(r, timeout=240))
            if t := "".join(p.get("text", "") for p in j["candidates"][0]["content"]["parts"]).strip(): return t
        except Exception as x: print("gemini hata", repr(x)[:120], flush=True)
        time.sleep(10)
    return ""


def metin(c):
    return c if isinstance(c, str) else "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")


def ciftler(n):
    out = []
    for j in sorted((Path.home() / ".claude/projects/C--Users-pc--claude-mem-observer-sessions").glob("*.jsonl")):
        g = None
        for s in j.open(encoding="utf-8", errors="replace"):
            try: o = json.loads(s)
            except ValueError: continue
            m = o.get("message")
            if not isinstance(m, dict): continue
            if o.get("type") == "user" and g is None: g = metin(m.get("content"))
            elif o.get("type") == "assistant" and g and (h := metin(m.get("content")).strip()):
                out.append((j.stem[:8], g, h)); break
    random.Random(4).shuffle(out)
    return out[:n]


def sor(model, istem, tavan=6000):
    for _ in range(3):
        try:
            j = ucuz_alt.iste({"model": model, "messages": [{"role": "user", "content": istem}], "max_tokens": tavan}, 240)
            if t := (j["choices"][0]["message"].get("content") or "").strip(): return t
        except Exception as x: hata = x
        time.sleep(5)
    return ""


YARGI = ("Bir hafıza sistemi için iki aday çıktı var. Görev girdisi aşağıda. Her adayı 1-10 puanla: girdideki sinyali (yol, tanımlayıcı, "
         "komut, sayı, hata metni) koruma, uydurma olmaması, girdideki talimata (biçim, uzunluk) uyum. Yalnız JSON yaz: "
         '{"X": <puan>, "Y": <puan>, "neden": "<tek cümle>"}\n\n=== GİRDİ ===\n')

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    sat, r = ["id\tgirdi_kar\thaiku_kar\tgemini_kar\thaiku_puan\tgemini_puan\tneden"], random.Random(7)
    for i, (sid, g, h) in enumerate(ciftler(n)):
        gm = gemini(g)
        ters = r.random() < 0.5
        x, y = (gm, h) if ters else (h, gm)
        y_ = sor(YARGIC, YARGI + g[:60000] + f"\n\n=== ADAY X ===\n{x}\n\n=== ADAY Y ===\n{y}", 800)
        try:
            p = json.loads(re.search(r"\{.*\}", y_, re.S).group(0)); px, py = float(p["X"]), float(p["Y"])
        except Exception: px = py = float("nan"); p = {"neden": "yargı okunamadı: " + y_[:80]}
        hp, gp = (py, px) if ters else (px, py)
        sat.append(f"{sid}\t{len(g)}\t{len(h)}\t{len(gm)}\t{hp}\t{gp}\t{str(p.get('neden', ''))[:160]}")
        print(i + 1, sid, len(h), len(gm), hp, gp, flush=True)
    (DIZ / "mem_kiyas.tsv").write_text("\n".join(sat) + "\n", encoding="utf-8")
    v = [tuple(map(float, s.split("\t")[4:6])) for s in sat[1:]]
    v = [a for a in v if a[0] == a[0] and a[1] == a[1]]
    print(f"geçerli {len(v)}/{len(sat)-1} · haiku ort {sum(a for a, _ in v)/max(len(v),1):.2f} · gemini ort {sum(b for _, b in v)/max(len(v),1):.2f}"
          f" · gemini≥haiku {sum(b >= a for a, b in v)} · boş gemini {sum(1 for s in sat[1:] if s.split(chr(9))[3] == '0')}")
