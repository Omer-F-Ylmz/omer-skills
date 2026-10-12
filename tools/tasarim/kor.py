"""TASARIM-2 (3) kör yargı: brief başına 8 sayfa (1.6.0 ×4 / 1.7.0 ×4) rastgele harfle etiketlenir, ekran görüntüsü alınır,
tek claude -p (opus, yalnız Read) 1-10 puanlar; eşleme kor/<brief>/eslesme.json'da, yargıç görmez.
    python tools/tasarim/kor.py <kopru_dizini> [--kuru]
Toplam 2 claude -p, çağrı başına --max-budget-usd 1.5 (Σ ≤ $3).
"""
import json
import os
import pathlib
import random
import subprocess
import sys

BURA = pathlib.Path(__file__).resolve().parent
ISTEM = ("Aşağıdaki {n} dosya aynı brief için üretilmiş web sayfalarının ekran görüntüsü (1440 genişlik, üst 2700px). "
         "Brief: {brief}\nHer birini Read ile aç. Her sayfayı 1-10 puanla: görsel kalite, tipografi, hiyerarşi, markaya özgünlük "
         "(şablon/AI-slop gibi duruyorsa düşük). Yalnız tek satır JSON döndür: {{\"A\": puan, ...}}.\nDosyalar:\n")


def dizinler(kok, brief):
    return ([kok / f"tasarim-kanit/{brief}-yeni-{t}" for t in (1, 2)] + [kok / f"tasarim2-kanit/{brief}-160-{t}" for t in (3, 4)],
            [kok / f"tasarim2-kanit/{brief}-170-{t}" for t in (1, 2, 3, 4)])


def main(argv):
    sys.path.insert(0, str(BURA))
    import kanit
    kok = pathlib.Path(argv[0]).resolve()
    sonuc = {}
    for brief, metin in kanit.BRIEF.items():
        d160, d170 = dizinler(kok, brief)
        sayfalar = [("160", d) for d in d160] + [("170", d) for d in d170]
        random.Random(brief).shuffle(sayfalar)
        cikti = kok / "tasarim2-kanit/kor" / brief
        cikti.mkdir(parents=True, exist_ok=True)
        eslesme = {chr(65 + i): [kol, d.name] for i, (kol, d) in enumerate(sayfalar)}
        (cikti / "eslesme.json").write_text(json.dumps(eslesme, ensure_ascii=False), encoding="utf-8")
        resim = [cikti / f"{h}.png" for h in eslesme]
        if "--kuru" in argv:
            print(brief, {h: v[0] for h, v in eslesme.items()})
            continue
        subprocess.run(["node", str(BURA / "kor.mjs"), *[str(x) for d, p in zip(sayfalar, resim) for x in (d[1] / "index.html", p)]],
                       cwd=BURA, check=True, timeout=600, creationflags=0x08000000)
        env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_BASE_URL"}
        r = subprocess.run(["claude", "-p", ISTEM.format(n=len(resim), brief=metin) + "\n".join(p.name for p in resim),
                            "--model", "opus", "--output-format", "json", "--max-budget-usd", "1.5", "--setting-sources", "",
                            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands",
                            "--tools", "Read", "--allowedTools", "Read"], cwd=cikti, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=900, creationflags=0x08000000)
        j = json.loads(r.stdout or "{}")
        ham = j.get("result", "")
        puan = json.loads(ham[ham.index("{"):ham.rindex("}") + 1])
        ort = {kol: round(sum(puan[h] for h, v in eslesme.items() if v[0] == kol) / 4, 2) for kol in ("160", "170")}
        sonuc[brief] = {"puan": puan, "ort": ort, "usd": j.get("total_cost_usd")}
        print(brief, ort, "usd", j.get("total_cost_usd"), flush=True)
    if sonuc:
        (kok / "tasarim2-kanit/kor/sonuc.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("BITTI", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
