"""LAYA-1 d2: jev_tum.jsonl'in etiketsiz 209 öğesi + tutarlılık için JEV-1 etiketli 10 öğe → Opus KÖR puan (0-5, jev_yargic.SORU rubriği).
Jev/Laya puanı istemde YOK; öğeler karışık sırada, çağrı başına ≤10 öğe, toplam ≤25 claude -p (cagri.jsonl sayacı, yeniden koşuda kalan partiler).
Plan limitiyle: ANTHROPIC_API_KEY/BASE_URL/AUTH_TOKEN alt sürece verilmez. Ortak sıradan koş: olcum_sira.py kor.py"""
import hashlib
import json
import os
import random
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).parent
K = D / "kor"
J1 = Path("C:/Projeler/omer-skills-wt/jev/.claude/jev1")
TAVAN, PARTI = 25, 10
SEVIYE = ["Hiç karşılamıyor / alakasız", "Çok zayıf", "Kısmen, önemli eksik", "Çoğunlukla, küçük eksik", "Tam karşılıyor",
          "Tam ve örnek nitelikte"]  # jev_yargic.SEVIYE
ISTEM = ("Aşağıda {n} örnek var; her biri bir GOREV, KABUL ölçütü ve bir YANIT içerir. Her YANIT'ı, GOREV isteğini KABUL ölçütüne göre "
         "ne kadar karşıladığına göre 0-5 tamsayıyla puanla. Yalnız yanıtın içeriğini yargıla; biçim/uzunluk değil, doğruluk ve kabul ölçütü.\n"
         + "\n".join(f"{i} = {s}" for i, s in enumerate(SEVIYE)) +
         "\nÖrnekleri birbirinden bağımsız puanla. Araç kullanma. Yalnız tek satır JSON döndür: {{\"<örnek no>\": <0-5>, ...}}\n\n")


def ogeler():
    tum = {k["dosya"]: k["state"] for k in map(json.loads, open(J1 / "jev_tum.jsonl", encoding="utf-8"))}
    etiketli = json.load(open(J1 / "ornek_sira.json"))
    tekrar = sorted(etiketli, key=lambda d: hashlib.sha256(d.encode()).hexdigest())[:10]
    secim = [d for d in tum if d not in etiketli] + tekrar
    random.Random(13).shuffle(secim)
    return tum, secim, tekrar


def main():
    tum, secim, tekrar = ogeler()
    K.mkdir(exist_ok=True)
    (K / "tekrar.json").write_text(json.dumps(tekrar), encoding="utf-8")
    sonuc = json.loads((K / "sonuc.json").read_text(encoding="utf-8")) if (K / "sonuc.json").exists() else {}
    cagri = len((K / "cagri.jsonl").read_text(encoding="utf-8").splitlines()) if (K / "cagri.jsonl").exists() else 0
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
    for p in range(0, len(secim), PARTI):
        parti = [d for d in secim[p:p + PARTI] if d not in sonuc]
        if not parti:
            continue
        if cagri >= TAVAN:
            print(f"TAVAN {TAVAN} çağrı doldu; eksik {len(secim) - len(sonuc)}", flush=True)
            break
        govde = "".join(f"######## ORNEK {i}\n## GOREV\n{tum[d]['gorev']}\n## KABUL\n{tum[d]['kabul']}\n## YANIT\n{tum[d]['yanit']}\n\n"
                        for i, d in enumerate(parti, 1))
        r = subprocess.run(["claude", "-p", "--model", "opus", "--output-format", "json", "--max-turns", "1", "--max-budget-usd", "1.50",
                            "--setting-sources", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
                            "--disable-slash-commands", "--no-session-persistence"],
                           input=ISTEM.format(n=len(parti)) + govde, env=env, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=900, creationflags=0x08000000, cwd=K)
        cagri += 1
        try:
            j = json.loads(r.stdout or "{}")
            ham = j.get("result", "")
            puan = json.loads(ham[ham.index("{"):ham.rindex("}") + 1])
            yeni = {d: int(puan[str(i)]) for i, d in enumerate(parti, 1) if 0 <= int(puan.get(str(i), -1)) <= 5}
        except (ValueError, KeyError, TypeError) as e:
            yeni, j = {}, {"hata": f"{type(e).__name__}: {(r.stdout or r.stderr)[-300:]}"}
        with open(K / "cagri.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"parti": p // PARTI, "n": len(parti), "ok": len(yeni), "usd": j.get("total_cost_usd"),
                                "hata": j.get("hata")}, ensure_ascii=False) + "\n")
        sonuc.update(yeni)
        (K / "sonuc.json").write_text(json.dumps(sonuc, ensure_ascii=False), encoding="utf-8")
        print(f"parti {p // PARTI}: {len(yeni)}/{len(parti)} · çağrı {cagri} · usd {j.get('total_cost_usd')} {j.get('hata') or ''}", flush=True)
        if not yeni:  # plan limiti düz metin döner (API Error değil) ya da biçim bozuk → boşa çağrı yakma
            print("DUR: parti boş döndü", flush=True)
            break
    print(f"BITTI sonuc {len(sonuc)}/{len(secim)} çağrı {cagri}", flush=True)


if __name__ == "__main__":
    main()
