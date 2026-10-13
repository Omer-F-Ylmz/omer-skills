"""TOKEN-8 f2b iş 3 ayrımı: kalibre3 ile aynı 8 öğe/4 çift, ama pilot.opus_yargila'nın Türkçe özgün istemi
+ yalnız hafif bayraklar (--setting-sources "" --tools ""). Kapı: eşik 7 uyumu ≥%95, ort |Δ| ≤0.25."""
import json, re, subprocess, sys
from pathlib import Path

OMNI = Path("C:/Projeler/omer-skills-wt/omniroute1/.claude/omniroute1")
sys.path.insert(0, str(OMNI))
import pilot  # noqa: E402  (argv'siz → EK="", varsayılan önbellek anahtarları)

ob = {json.loads(s)["anahtar"]: json.loads(s) for s in pilot.OB.read_text(encoding="utf-8").splitlines()}
satir = [{"gorev": pilot.ISTEM + m, **ob[f"{y}:{ad}"]} for ad, m in pilot.ornekler() for y in (pilot.YOL, "claude")]
eski = {int(k): v for k, v in ob["opus"]["puan"].items()}
sec = list(eski)
ENV = {k: v for k, v in __import__("os").environ.items() if k != "ANTHROPIC_API_KEY"
       and not re.match(r"CLAUDECODE|CLAUDE_CODE_(CHILD|MESSAGING|SESSION|ENTRYPOINT|EXECPATH)|CLAUDE_PID", k)}

yeni, jeton = {}, []
for k in range(0, len(sec), 2):
    pilot.ram_bekle()
    metin = "Her öğe için özeti, kabul ölçütüne göre 0-10 puanla. Yalnız satır başına `<id> <puan>` yaz.\nKabul: " + pilot.KABUL + "\n\n"
    metin += "\n\n".join(f"### id={i}\nTRANSKRİPT: {satir[i]['gorev'][len(pilot.ISTEM):]}\nÖZET:\n{satir[i]['yanit']}" for i in sec[k:k + 2])
    p = subprocess.run([pilot.CLAUDE, "-p", "--output-format", "json", "--model", "opus", "--disable-slash-commands",
                        "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--setting-sources", "", "--tools", ""],
                       input=metin, env=ENV, capture_output=True, text=True, encoding="utf-8", timeout=300, creationflags=0x08000000)
    j = json.loads(p.stdout)
    if j.get("is_error") or re.search(r"usage limit|limit reached|resets? at", str(j.get("result")), re.I):
        sys.exit("limit/hata: " + str(j.get("result"))[:120])
    u = j.get("usage", {})
    jeton.append(u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0))
    yeni.update({int(a): float(b) for a, b in re.findall(r"^\s*(\d+)\s+(\d+(?:\.\d+)?)", j["result"], re.M)})

ort = [i for i in sec if i in yeni]
uyum = sum((eski[i] >= 7) == (yeni[i] >= 7) for i in ort) / max(len(ort), 1)
d = sum(abs(eski[i] - yeni[i]) for i in ort) / max(len(ort), 1)
print(json.dumps({"eski": eski, "yeni": yeni, "n": len(ort), "uyum7": round(uyum, 3), "ort_fark": round(d, 3),
                  "girdi_jeton": jeton, "kapi": uyum >= 0.95 and d <= 0.25 and len(ort) == len(sec)}, ensure_ascii=False))
