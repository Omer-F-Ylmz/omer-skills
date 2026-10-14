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
    # d3 (Desktop 22:06): kancanın tetiklendiği 2. görev, TELVE'de (src/sahne/fincan.js 872 satır)
    "telve": "Bu repoda src/sahne/fincan.js'teki kahve yüzeyi dalga simülasyonunda ızgara çözünürlüğü N neye göre "
             "seçiliyor, zaman adımı DTS hangi kararlılık koşulundan ve hangi frekans formülünden geliyor, gecis() "
             "fonksiyonu ne yapıyor? Kısa yanıt, dosya:satır ile.",
}
CWD = {"telve": Path("C:/Users/pc/Desktop/TELVE")}
BAYRAK = ["-p", "--output-format", "json", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
          "--disable-slash-commands", "--no-session-persistence"]


SOR = "C:/Projeler/omer-skills/.kos/kopru"
# d5 (Desktop 23:55): C = B + is-akisi keşif sırası (harita → graphify_sor → aralıklı Read); A tabanı d3 satırları
KESIF = (f"Keşif sırası: önce {SOR}/harita/<proje>.md (proje = cwd klasör adı); sonra Bash `python {SOR}/graphify_sor.py "
         "\"<sembol ya da dosya adı>\" --kok <cwd>` (sembol · dosya:satır · çağıranlar); dosyayı yalnız kanıt satırı için "
         "Read offset/limit (~20-40 satır) ile oku, bütün dosyayı açma. Bağımsız çağrıları aynı turda paralel yap.")


def kos(istem, ayar, cwd=KOK, ek=()):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(ayar, f)
    t = time.time()
    r = subprocess.run(["claude", *BAYRAK, "--settings", f.name, *ek], input=istem, capture_output=True, text=True,
                       encoding="utf-8", cwd=cwd, timeout=900, creationflags=0x08000000)
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
    plan = [a.split(":") for a in sys.argv[1:] if a != "--c"] or [[ad, "1"] for ad in GOREVLER]  # örn. profil:1 telve:2
    for ad, n in plan:
        for _ in range(int(n)):  # A/B sırayla, tekrar başına bir çift → kayma iki kola eşit düşer
          kollar = [("C", {"hooks": KANCA}, ["--append-system-prompt", KESIF])] if "--c" in sys.argv else \
                   [("A", {}, []), ("B", {"hooks": KANCA}, [])]
          for kol, ayar, ek in kollar:
            s = kos(GOREVLER[ad], ayar, CWD.get(ad, KOK), ek)
            with out.open("a", encoding="utf-8") as f:
                f.write(f"{ad}\t{kol}\t{json.dumps(s, ensure_ascii=False)}\n")
            print(ad, kol, {k: v for k, v in s.items() if k != "yanit"}, flush=True)
    print("BITTI")
