"""FABLE-AJAN hook kolu: plugin alt ajanı (dosyası değiştirilmez) üst `claude -p` oturumunca Task ile çağrılır;
taban = hook yok, proto = SubagentStart hook'u (tools/fable_ajan_hook.py) protokolü verir. Satırlar fable_ajan_olc ile aynı
TSV biçiminde (aile=plugin, ajan=görev adı) → fable_ajan_tablo aynen karar verir. Tavan 16 çağrı.
  python tools/olcum/fable_ajan_hook_olc.py <cikti_dizin> [--protokol SKILL.md] [--tekrar 2]"""
import argparse, json, os, random, subprocess, sys, tempfile, time
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
sys.path.insert(0, str(DIZIN))
import kosucu  # noqa: E402
from fable_ajan_olc import BASLIK, protokol_govde, yapilanlar  # noqa: E402

KOK = DIZIN.parents[1]
HOOK = KOK / "tools" / "fable_ajan_hook.py"
TAVAN = 16
# plugin ajanı → kalite3 görevi (rubrik oradan); hepsi sonnet
CIFTLER = [("ecc:security-reviewer", "sec-injection-denetci"), ("pr-review-toolkit:code-reviewer", "fe-react-bilesen-inceleme"),
           ("feature-dev:code-reviewer", "sec-api-guvenlik"), ("pr-review-toolkit:pr-test-analyzer", "qa-birim-test-yazar")]


def istem(ajan, gorev):
    return (f"Delegate the task below to the `{ajan}` subagent with the Task tool (subagent_type exactly `{ajan}`) and reply with "
            f"its answer verbatim, nothing else.\n\nTASK:\n{gorev}")


def kos(metin, ayar, timeout=600):
    t = time.time()
    k = ["claude", "-p", metin, "--model", "sonnet", "--output-format", "json", "--settings", str(ayar),
         "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--max-budget-usd", "1.0"]
    try:
        p = subprocess.run(k, capture_output=True, text=True, encoding="utf-8", timeout=timeout, creationflags=0x08000000)
        j = json.loads(p.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return {"metin": "", "out": 0, "usd": 0.0, "sure": round(time.time() - t), "tur": 0, "rc": 1}
    out = sum(m.get("outputTokens", 0) for m in (j.get("modelUsage") or {}).values())
    return {"metin": j.get("result") or "", "out": out, "usd": j.get("total_cost_usd") or 0.0, "sure": round(time.time() - t),
            "tur": j.get("num_turns", 0), "rc": p.returncode, "usage": j.get("usage") or {}}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cikti")
    ap.add_argument("--protokol", default=str(KOK / "skills" / "calisma-protokolu" / "SKILL.md"))
    ap.add_argument("--tekrar", type=int, default=2)
    ns = ap.parse_args(argv)
    os.environ["OLCUM_MCP_HAFIF"] = "1"
    gorev = {g["ajan"]: g for g in json.loads((KOK / "ajanlar" / "kalite3" / "gorevler.json").read_text(encoding="utf-8"))}
    cikti = Path(ns.cikti)
    (cikti / "metin").mkdir(parents=True, exist_ok=True)
    tsv = cikti / "olcum.tsv"
    yapildi = yapilanlar(tsv) if tsv.exists() else set()
    if not tsv.exists():
        tsv.write_text(BASLIK, encoding="utf-8")
    harita = cikti / "harita.json"
    harita.write_text(json.dumps({"metin": {"sonnet": protokol_govde(ns.protokol)}, "ajan": {a: "sonnet" for a, _ in CIFTLER}},
                                 ensure_ascii=False), encoding="utf-8")
    hook = {"hooks": {"SubagentStart": [{"matcher": ".*", "hooks": [{"type": "command", "command": f'python "{HOOK}" "{harita}"'}]}]}}
    sayi = 0
    with tempfile.TemporaryDirectory() as d:
        ayar = {"taban": Path(d) / "taban.json", "proto": Path(d) / "proto.json"}
        ayar["taban"].write_text("{}", encoding="utf-8")
        ayar["proto"].write_text(json.dumps(hook), encoding="utf-8")
        for r in range(1, ns.tekrar + 1):
            for ajan, g in CIFTLER:
                for kol in random.Random(r).sample(["taban", "proto"], 2):
                    if (g, kol, str(r)) in yapildi:
                        continue
                    if sayi >= TAVAN:
                        print("tavan", sayi, flush=True); return
                    o = kos(istem(ajan, gorev[g]["istem"]), ayar[kol])
                    sayi += 1
                    (cikti / "metin" / f"{g}__{kol}__{r}.md").write_text(o["metin"], encoding="utf-8")
                    i, cc, cr, _ = kosucu.jeton(o.get("usage") or {})
                    with tsv.open("a", encoding="utf-8") as f:
                        f.write("\t".join(map(str, [g, "plugin", "sonnet", kol, r, i, cc, cr, o["out"], round(o["usd"], 4), o["sure"],
                                                    kosucu.puanla(o["metin"], gorev[g]["rubrik"]), o["tur"], o["rc"]])) + "\n")
                    print(ajan, kol, r, "out", o["out"], "$", round(o["usd"], 4), flush=True)
    print("bitti: çağrı", sayi, flush=True)


if __name__ == "__main__":
    main()
