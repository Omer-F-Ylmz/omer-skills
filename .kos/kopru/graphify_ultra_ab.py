"""GRAPHIFY-ULTRA-1 G5: keşif A/B — A = köprü profili kancasız (mevcut), B = oku_yonlendir kancalı.
2 görev × 2 kol = 4 claude -p (tavan), sırayla, MCP'siz hafif bayraklar. Çıktı: graphify-ultra-ab.tsv."""
import json, subprocess, sys, tempfile, time
from pathlib import Path

KOK = Path("C:/Projeler/omer-skills")
KANCA = json.loads((KOK / "profiller/cc-arka.json").read_text(encoding="utf-8"))["ajan"]["ayar"]["hooks"]
GOREVLER = {
    "profil": "Bu repoda cc-kopru köprüsünün `ajan` aracı alt claude sürecine verdiği --settings profil dosyasını hangi "
              "fonksiyon kuruyor, hangi kaynak JSON'un hangi alanlarını okuyor ve dosyayı nereye yazıyor? "
              "Kısa yanıt: fonksiyon adı, dosya:satır, alan adları, yazılan yol.",
    "hafif": "Bu repoda .kos/kopru/graphify_hafif.py artımlı modda değişen dosyaları nasıl belirliyor ve hangi RAM "
             "eşiğinde çalışmayı reddediyor? graphify'ın hangi iç fonksiyonunu çağırıyor? Kısa yanıt, dosya:satır ile.",
}
BAYRAK = ["-p", "--output-format", "json", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
          "--disable-slash-commands", "--no-session-persistence"]


def kos(istem, ayar):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(ayar, f)
    t = time.time()
    r = subprocess.run(["claude", *BAYRAK, "--settings", f.name], input=istem, capture_output=True, text=True,
                       encoding="utf-8", cwd=KOK, timeout=900, creationflags=0x08000000)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"hata": (r.stdout or r.stderr)[:200]}
    u = d.get("usage", {})
    return {"sure": round(time.time() - t), "tur": d.get("num_turns"), "girdi": u.get("input_tokens", 0),
            "cr": u.get("cache_read_input_tokens", 0), "cw": u.get("cache_creation_input_tokens", 0),
            "cikti": u.get("output_tokens", 0), "usd": d.get("total_cost_usd"), "yanit": (d.get("result") or "")[:600]}


if __name__ == "__main__":
    out = KOK / ".kos/kopru/graphify-ultra-ab.tsv"
    for ad, istem in GOREVLER.items():
        for kol, ayar in (("A", {}), ("B", {"hooks": KANCA})):
            s = kos(istem, ayar)
            with out.open("a", encoding="utf-8") as f:
                f.write(f"{ad}\t{kol}\t{json.dumps(s, ensure_ascii=False)}\n")
            print(ad, kol, {k: v for k, v in s.items() if k != "yanit"}, flush=True)
    print("BITTI")
