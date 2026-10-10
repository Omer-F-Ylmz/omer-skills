"""KÜTÜPHANE-3a: oturum başı bağlam dökümü. Boş klasörde 4 tek turlu `claude -p "tamam yaz"`:
  tam · mcpsiz (--strict-mcp-config) · skillsiz (--disable-slash-commands) · runner (hafif.py A1 bayrakları).
init olayından skill/komut/ajan/araç/MCP sayıları, hook olaylarından hook çıktı boyutu. Sonuç: docs/kutuphane/olcum/bilesen-<tarih>.json"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kosucu as k  # noqa: E402

KOLLAR = {
    "tam": [],
    "mcpsiz": ["--strict-mcp-config"],
    "skillsiz": ["--disable-slash-commands"],
    "runner": ["--tools", "", "--setting-sources", "", "--strict-mcp-config", "--safe-mode", "--disable-slash-commands"],
}


def main():
    tarih = time.strftime("%Y-%m-%d")
    sonuc = {}
    for ad, ek in KOLLAR.items():
        o = k.kos("tamam yaz", ek, butce=3.0, timeout=300)
        i, cc, cr, out = k.jeton(o["usage"])
        init = o["init"]
        hook_bayt = sum(len(json.dumps(h, ensure_ascii=False)) for h in o["hook"])
        sonuc[ad] = {"input": i, "cache_creation": cc, "cache_read": cr, "output": out, "toplam_baglam": i + cc + cr, "sure": o["sure"], "usd": round(o["usd"], 4),
                     "rc": o["rc"], "hata": o["hata"],
                     "n": {a: len(init.get(a) or []) for a in ("tools", "mcp_servers", "slash_commands", "agents", "skills", "plugins")},
                     "hook_olay": len(o["hook"]), "hook_bayt": hook_bayt,
                     "hook_adlar": sorted({str(h.get("hook_name") or h.get("hook_event")) for h in o["hook"]})[:40]}
        if ad == "tam":
            sonuc["_init_tam"] = {a: init.get(a) for a in ("tools", "slash_commands", "agents", "skills")}
        print(ad, sonuc[ad]["toplam_baglam"], sonuc[ad]["n"], "hook", sonuc[ad]["hook_olay"], sonuc[ad]["hook_bayt"], flush=True)
    yol = k.CIKTI / f"bilesen-{tarih}.json"
    k.CIKTI.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("->", yol)


if __name__ == "__main__":
    main()
