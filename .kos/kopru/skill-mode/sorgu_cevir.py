"""Sorgu genişletme (Code Mode M3 öncesi): TR/EN iş tarifi → İngilizce yeniden yazım + 6-10 teknik anahtar sözcük.
Ücretsiz havuzla (Claude token 0). Çıktı: sorgu-cevir.json {sorgu: "en metin | anahtarlar"}. Önbellekli; çalışma anında da aynı fonksiyon kullanılır."""
import json, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / "tools"))
import ucretsiz_havuz as uh

D = Path(__file__).resolve().parent
CIK = D / "sorgu-cevir.json"
PAKET = 25
ISTEM = ("Each line is a user's task request (Turkish or English) for a developer/creator assistant. For each, write ONE English line: "
         "a plain rewrite of the task, then ' | ', then 6-10 technical keywords/synonyms a tool description for this task would contain "
         "(e.g. 'deploy, release, ci, production checklist'). Do not invent tool names. Return ONLY a JSON array: [{\"i\":0,\"e\":\"...\"}, ...]\n\n")


def dogrula(m):
    try:
        j = json.loads(re.search(r"\[.*\]", m, re.S).group(0))
        return None if isinstance(j, list) and j else "liste yok"
    except Exception:
        return "json değil"


def cevir(sorgular, onbellek):
    eksik = [q for q in dict.fromkeys(sorgular) if q not in onbellek]
    for i in range(0, len(eksik), PAKET):
        p = eksik[i:i + PAKET]
        m, kay, _ = uh.cagir("kolay", ISTEM + "\n".join(f"{k}. {q}" for k, q in enumerate(p)), max_tokens=3000, dogrula=dogrula, etiket="skill-mode-cevir")
        if not m:
            continue
        for o in json.loads(re.search(r"\[.*\]", m, re.S).group(0)):
            try:
                onbellek[p[int(o["i"])]] = str(o["e"])
            except (KeyError, ValueError, IndexError, TypeError):
                pass
    return onbellek


if __name__ == "__main__":
    tet = [json.loads(s) for s in (D / "tetik.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    ob = json.loads(CIK.read_text(encoding="utf-8")) if CIK.exists() else {}
    t = time.time()
    ob = cevir([q for x in tet for q in x["sorgular"]], ob)
    CIK.write_text(json.dumps(ob, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"çevrilen {len(ob)} · {time.time() - t:.0f}s")
