"""TASARIM-3 (4) kör yargı: brief başına 4 sayfa (taban ×2 / vitrin ×2) rastgele harfle, tek claude -p (opus, yalnız Read) 1-10 puan.
    python tools/tasarim/kor3.py <kanit_dizini> [--kuru]
4 brief = 4 claude -p, çağrı başına --max-budget-usd 0.75; eşleme kor/<brief>/eslesme.json'da, yargıç görmez.
"""
import json
import os
import pathlib
import random
import subprocess
import sys

BURA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BURA))
import kanit3  # noqa: E402
from kor import ISTEM  # noqa: E402


def main(argv):
    kok = pathlib.Path(argv[0]).resolve()
    sonuc = {}
    for brief, metin in kanit3.kanit.BRIEF.items():
        sayfalar = [(kol, kok / f"{brief}-{kol}-{t}") for kol in ("taban", "vitrin") for t in (1, 2)]
        sayfalar = [s for s in sayfalar if (s[1] / "index.html").exists()]
        random.Random(brief).shuffle(sayfalar)
        cikti = kok / "kor" / brief
        cikti.mkdir(parents=True, exist_ok=True)
        eslesme = {chr(65 + i): [kol, d.name] for i, (kol, d) in enumerate(sayfalar)}
        (cikti / "eslesme.json").write_text(json.dumps(eslesme, ensure_ascii=False), encoding="utf-8")
        resim = [cikti / f"{h}.png" for h in eslesme]
        if "--kuru" in argv:
            print(brief, {h: v[0] for h, v in eslesme.items()})
            continue
        subprocess.run(["node", str(BURA / "kor.mjs"), *[str(x) for d, p in zip(sayfalar, resim) for x in (d[1] / "index.html", p)]],
                       cwd=BURA, check=True, timeout=600, creationflags=0x08000000)
        env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
        r = subprocess.run(["claude", "-p", ISTEM.format(n=len(resim), brief=metin) + "\n".join(p.name for p in resim),
                            "--model", "opus", "--output-format", "json", "--max-budget-usd", "0.75", "--setting-sources", "",
                            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands",
                            "--tools", "Read", "--allowedTools", "Read"], cwd=cikti, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=900, creationflags=0x08000000)
        j = json.loads(r.stdout or "{}")
        ham = j.get("result", "")
        try:
            puan = json.loads(ham[ham.index("{"):ham.rindex("}") + 1])
        except ValueError:  # plan limiti yanıtı düz metin gelir (claude-p-plan-limiti-metin)
            print(brief, "YARGI YOK", ham[:120], flush=True)
            continue
        ort = {kol: round(sum(puan[h] for h, v in eslesme.items() if v[0] == kol) / max(1, sum(v[0] == kol for v in eslesme.values())), 2)
               for kol in ("taban", "vitrin")}
        sonuc[brief] = {"puan": puan, "ort": ort, "usd": j.get("total_cost_usd")}
        print(brief, ort, "usd", j.get("total_cost_usd"), flush=True)
    if sonuc:
        (kok / "kor" / "sonuc.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("BITTI", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
