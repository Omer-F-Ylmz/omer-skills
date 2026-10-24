"""M3: katalog kayıtlarına TR+EN etiket/eşanlam (ücretsiz havuz, Claude jetonu 0). Çıktı etiket.json {ad|imza: "anahtarlar"}.
Sıra: açıklaması en zayıf (kısa) kayıt önce; önbellekli, süre sınırlı, tekrar koşulabilir. python etiket_uret.py <saniye> [is_parcasi]"""
import json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, r"C:\Projeler\omer-skills\tools")
import ucretsiz_havuz as uh

D = Path(__file__).resolve().parent
CIK = D / "etiket.json"
PAKET, IS = 25, 6
ISTEM = ("Each line is a tool/skill/agent: 'name :: description'. For each, write 8-12 search keywords/synonyms that a user might use "
         "to ask for it, mixing ENGLISH and TURKISH (e.g. 'deploy, release, yayınla, canlıya al, ci, checklist'). Concrete task words, no tool names, "
         "no generic words like 'tool' or 'skill'. Return ONLY a JSON array: [{\"i\":0,\"t\":\"kw1, kw2, ...\"}, ...]\n\n")
anahtar = lambda o: f"{o['ad']}|{o.get('imza', '')}"


def dogrula(m):
    try:
        j = json.loads(re.search(r"\[.*\]", m, re.S).group(0))
        return None if isinstance(j, list) and j else "liste yok"
    except Exception:
        return "json değil"


def paket(p):
    m, _, _ = uh.cagir("kolay", ISTEM + "\n".join(f"{k}. {o['ad']} :: {(o.get('is') or o.get('metin') or '')[:160]}" for k, o in enumerate(p)),
                       max_tokens=4000, dogrula=dogrula, etiket="skill-mode-etiket")
    s = {}
    if m:
        for o in json.loads(re.search(r"\[.*\]", m, re.S).group(0)):
            try:
                s[anahtar(p[int(o["i"])])] = str(o["t"])
            except (KeyError, ValueError, IndexError, TypeError):
                pass
    return s


if __name__ == "__main__":
    sure = float(sys.argv[1]) if len(sys.argv) > 1 else 480
    rows = [json.loads(s) for s in (D / "yetenek-tam.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    ob = json.loads(CIK.read_text(encoding="utf-8")) if CIK.exists() else {}
    eksik = [o for o in rows if anahtar(o) not in ob and o["tur"] != "motion-prompt"]
    eksik.sort(key=lambda o: len(o.get("is") or ""))
    parcalar = [eksik[i:i + PAKET] for i in range(0, len(eksik), PAKET)]
    t0 = time.time()
    print("eksik", len(eksik), "paket", len(parcalar), flush=True)
    with ThreadPoolExecutor(IS) as ex:
        i, bos = 0, 0
        while i < len(parcalar) and time.time() - t0 < sure:
            ilk = len(ob)
            for s_ in ex.map(paket, parcalar[i:i + IS]):
                ob.update(s_)
            if len(ob) == ilk:  # havuz soğuma/kota: bekle, aynı grubu tekrar dene
                bos += 1
                time.sleep(min(30 * bos, 120))
                continue
            bos, i = 0, i + IS
            CIK.write_text(json.dumps(ob, ensure_ascii=False), encoding="utf-8")
            print(f"{len(ob)} kayıt · {time.time() - t0:.0f}s", flush=True)
