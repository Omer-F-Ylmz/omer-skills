"""LAYA-2 ücretsiz öğretmen kurulu: her öğeyi farklı sağlayıcılar 0-5 puanlar (Claude $0, tools/ucretsiz_havuz.cagir).
  python kurul.py <girdi.jsonl> <cikti.jsonl> [k=3] [işçi=6] [sınır]   girdi: {id, state:{gorev,kabul,yanit}}
Çıktı satırı: {id, puan:{sağlayıcı: 0-5}}; yeniden koşunca biten id'ler atlanır (kota dolunca devam). Sağlayıcı yanıtlamazsa sıradakine geçilir."""
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import puan  # noqa: E402
import ucretsiz_havuz as uh  # noqa: E402

SAG = ["gemini", "groq", "openrouter", "mistral", "nvidia", "cloudflare", "ollama", "omniroute"]
SEVIYE = ["Hiç karşılamıyor / alakasız", "Çok zayıf", "Kısmen, önemli eksik", "Çoğunlukla, küçük eksik", "Tam karşılıyor",
          "Tam ve örnek nitelikte"]
ISTEM = ("Bir yanıtı kabul ölçütüne göre puanla. Yalnızca yanıtın içeriğini yargıla (doğruluk, ölçütün karşılanması); biçim ve uzunluk değil.\n"
         "Düzeyler: " + "; ".join(f"{i}={s}" for i, s in enumerate(SEVIYE)) + ".\n\n"
         "GÖREV:\n{gorev}\n\nKABUL ÖLÇÜTÜ:\n{kabul}\n\nYANIT:\n{yanit}\n\n"
         'Yalnızca JSON ver, başka metin yok: {{"score": <0-5 tam sayı>}}')
KILIT = threading.Lock()
_yaz, YKILIT = uh._yaz, threading.Lock()


def _kilitli_yaz(d):  # havuz durum tmp'si süreç başı: iş parçacıkları çakışmasın (WinError 5)
    with YKILIT:
        _yaz(d)


uh._yaz = _kilitli_yaz


def istem(s):
    return ISTEM.format(gorev=s["gorev"][:1500], kabul=s.get("kabul", "")[:600], yanit=s["yanit"][:3000])


def ayikla(m):
    p = puan.ayikla(m)
    return None if p is None else int(p)


def puanla(k, ag, sag):
    p, i = {}, hash(k["id"]) % len(sag)
    for j in range(len(sag)):
        pr = sag[(i + j) % len(sag)]
        m, _, _ = uh.cagir("hakem", istem(k["state"]), max_tokens=1500, saglayici=pr, dogrula=lambda y: None if ayikla(y) is not None else "puan yok", zaman=60)
        if m is not None:
            p[pr] = ayikla(m)
        if len(p) >= ag:
            break
    return {"id": k["id"], "puan": p}


def main():
    gir, cik = Path(sys.argv[1]), Path(sys.argv[2])
    ag = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    isci = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    sinir = int(sys.argv[5]) if len(sys.argv) > 5 else 10**9
    tum = [json.loads(x) for x in open(gir, encoding="utf-8")]
    n, bos = 0, 0

    def is_(k):
        nonlocal n
        r = puanla(k, ag, SAG)
        with KILIT:
            if len(r["puan"]) >= 2:  # <2 öğretmen: kota dolu, sonraki turda yeniden denenir
                open(cik, "a", encoding="utf-8").write(json.dumps(r) + chr(10))
                n += 1
    while bos < 3:  # ilerleme yoksa 3 tur sonra dur (kotalar dolu); beklemek yok = tur arası kısa soğuma
        bitti = {json.loads(x)["id"] for x in open(cik, encoding="utf-8")} if cik.exists() else set()
        bekle = [k for k in tum if k["id"] not in bitti][:sinir]
        print(f"bekleyen {len(bekle)}", flush=True)
        if not bekle:
            break
        onceki = n
        with ThreadPoolExecutor(isci) as ex:
            list(ex.map(is_, bekle))
        bos = 0 if n > onceki else bos + 1
        if n == onceki:
            time.sleep(120)
    print("KURUL BITTI", n)


if __name__ == "__main__":
    main()
