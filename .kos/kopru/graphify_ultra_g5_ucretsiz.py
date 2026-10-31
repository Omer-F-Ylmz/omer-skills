"""KARAR-30 m2: GRAPHIFY-ULTRA-1 G5 kapi tekrar olcumu ucretsiz modelle (OmniRoute), claude -p ABONELIK/PARA yok.
A = kancasiz, C = kanca + KESIF istemi. 2 gorev x 2 kol = 4 kosu (tavan). Cikti: graphify-ultra-g5-ucretsiz.tsv.
Kapi: C girdi (girdi+cr+cw) / A <= 0.5."""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path
sys.path.insert(0, "C:/Projeler/omer-skills/.kos/kopru"); sys.path.insert(0, "C:/Projeler/omer-skills/tools")
import graphify_ultra_ab as ab
import ucretsiz_motor as m

def kos(istem, ayar, ek):
    ayar = {**ayar, "env": m.ayar_env()}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(ayar, f)
    t = time.time()
    try:
      r = subprocess.run(["claude", "--model", m.model(), *ab.BAYRAK, "--setting-sources", "project", "--settings", f.name, *ek], input=istem, capture_output=True,
                       text=True, encoding="utf-8", cwd=ab.KOK, timeout=int(os.environ.get("G5_TIMEOUT", 300)), creationflags=0x08000000, env=m.env_kur(dict(os.environ)))
    except subprocess.TimeoutExpired:
        return {"hata": "zaman-asimi-300sn"}
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"hata": (r.stdout or r.stderr)[:200]}
    u = d.get("usage", {})
    return {"sure": round(time.time() - t), "tur": d.get("num_turns"), "girdi": u.get("input_tokens", 0),
            "cr": u.get("cache_read_input_tokens", 0), "cw": u.get("cache_creation_input_tokens", 0),
            "cikti": u.get("output_tokens", 0), "yanit": (d.get("result") or "")[:300]}

if __name__ == "__main__":
    out = ab.KOK / ".kos/kopru/graphify-ultra-g5-ucretsiz.tsv"
    for ad in (sys.argv[1:] or ["profil"]):
        for kol, ayar, ek in (("A", {}, []), ("C", {"hooks": ab.KANCA}, ["--append-system-prompt", ab.KESIF])):
            s = kos(ab.GOREVLER[ad], ayar, ek)
            with out.open("a", encoding="utf-8") as f:
                f.write(f"{ad}\t{kol}\t{json.dumps(s, ensure_ascii=False)}\n")
            print(ad, kol, {k: v for k, v in s.items() if k != "yanit"}, flush=True)
    print("BITTI")
