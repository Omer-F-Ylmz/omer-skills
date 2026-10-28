"""OMNİ-AYIR-DÜZELT: held-out README özet ölçümü (ücretsiz havuz) + ücretsiz hakem.
  python duzelt_olc.py <etiket> <ofset> <adet>   -> duzelt-<etiket>.jsonl (yeniden başlatılabilir)
Held-out: olc.py'nin seçtiği 25 dışındaki README'ler (ofset kaydırır)."""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(Path(__file__).parent))
import ucuz_alt  # noqa: E402
import ucretsiz_havuz  # noqa: E402

D = Path(__file__).parent
etiket, ofset, adet = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
kul = {json.loads(l)['yol'] for l in (D / 'olcum.jsonl').read_text(encoding='utf-8').splitlines()}
EV = Path.home() / '.claude'
OZET_ISTEM = ("Bu README'den tam 4 madde çıkar, her biri tek cümle, '1) … 2) … 3) … 4) …' biçiminde ozet alanında: "
              "1) Ne yapar 2) Nasıl kurulur/çalıştırılır (komut varsa birebir) 3) Gereksinim/platform "
              "4) Lisans. README'de olmayan bilgi için o maddeye 'README'de yok' yaz; tahmin etme.")
tum = sorted(p for k in (EV / "plugins/marketplaces", EV / "skills") for d in (1, 2) for p in k.glob("/".join(["*"] * d) + "/README.md")
             if p.is_file() and 3_000 < p.stat().st_size < 12_000 and str(p) not in kul)
secili = tum[ofset::max(1, len(tum) // adet)][:adet]
cikti = D / f"duzelt-{etiket}.jsonl"
bitti = {json.loads(s)["yol"] for s in cikti.read_text(encoding="utf-8").splitlines()} if cikti.is_file() else set()

HAKEM = ("Sen kör hakemsin. README ve onun 4 maddelik özeti verilmiş (1 Ne yapar, 2 Kurulum/çalıştırma, 3 Gereksinim/platform, 4 Lisans). "
         "Her madde için karar ver: DOGRU (README ile tutarlı; README'de gerçekten yoksa 'README'de yok' da DOGRU), "
         "YANLIS (README'de bilgi VAR ama madde 'yok' diyor, eksik/parça parça anlamsız ya da çelişiyor), UYDURMA (README'de olmayan bilgi). "
         "Dikkat: README'yi tam tara (başlıklar, rozetler, 'License', 'Requirements', 'Prerequisites', kod blokları). "
         'YALNIZ JSON: {"m1":"DOGRU|YANLIS|UYDURMA","m2":"..","m3":"..","m4":"..","not":"yanlışların kısa nedeni"}\n\n')


def hakemle(readme, ozet):
    y, _, _ = ucretsiz_havuz.cagir("hakem", HAKEM + f"<README>\n{readme}\n</README>\n\n<OZET>\n{ozet}\n</OZET>", max_tokens=1500)
    return ucuz_alt.json_al(y) if y else None


with cikti.open("a", encoding="utf-8") as f:
    for p in secili:
        if str(p) in bitti:
            continue
        try:
            o, model, deneme, _, _ = ucuz_alt.coz("ozet", OZET_ISTEM, [p])
        except Exception as e:
            o, model, deneme = None, f"HATA {type(e).__name__}", 1
        h = hakemle(p.read_text(encoding="utf-8", errors="ignore"), o["ozet"]) if o else None
        f.write(json.dumps({"yol": str(p), "ozet": o["ozet"] if o else None, "model": model, "deneme": deneme, "hakem": h},
                           ensure_ascii=False) + "\n")
        f.flush()
        print(p.parent.name, model, deneme, h and [h.get(k) for k in ("m1", "m2", "m3", "m4")], flush=True)
