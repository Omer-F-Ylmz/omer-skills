"""ÖĞREN-6 d2: spec (satır numarası + Türkçe değer) → v1-yazar-N.jsonl; alıntı/komut/kanıt kaynak satırından BİREBİR çekilir.
  python -X utf8 .claude/ogren6/yaz.py N     (girdi: v1-spec-N.jsonl)
spec satırı: {"ad","ne":[satır,"Türkçe"],"k":[satır,"iğne"]|null,"s":[satır,"Türkçe"]|null,"m":["rol"],"kn":satır}
k: iğne = o satırda geçen komut parçası (""=satırın tamamı); komutu kendi adı olan kalem: "k":[satır,"@ad"]"""
import json, sys
from pathlib import Path

B = Path(__file__).parent
K = B / "kaynak"
import re


def dosya(ad):
    return K / (re.sub(r"[^\w.-]", "_", ad) + ".txt")


def al(m, n):
    x = m[n - 1].strip()
    if len(x) < 15:
        raise SystemExit(f"satır {n} çok kısa: {x!r}")
    return x[:190]


def yaz(p):
    cikti = []
    for s in (B / f"v1-spec-{p}.jsonl").read_text(encoding="utf-8").splitlines():
        o = json.loads(s)
        m = dosya(o["ad"]).read_text(encoding="utf-8", errors="replace").splitlines()
        no = lambda x: x if isinstance(x, int) else next(i + 1 for i, l in enumerate(m) if x in l)  # satır no ya da satırda geçen iğne
        o["ne"][0], o["kn"] = no(o["ne"][0]), no(o["kn"])
        k, sn = o.get("k"), o.get("s")
        k, sn = (k and [no(k[0]), k[1]]), (sn and [no(sn[0]), sn[1]])
        if k:
            igne = o["ad"] if k[1] == "@ad" else (k[1] or m[k[0] - 1].strip()[:150])
            if k[1] != "@ad" and igne not in m[k[0] - 1]:
                raise SystemExit(f"{o['ad']}: iğne {igne!r} satır {k[0]}'de yok")
            komut = {"deger": igne, "alinti": al(m, k[0])}
        else:
            komut = {"deger": "belirsiz — kaynakta bu aracın komut şablonu yok", "alinti": ""}
        sinir = {"deger": sn[1], "alinti": al(m, sn[0])} if sn else {"deger": "belirsiz — kaynakta sınır/uyarı yok", "alinti": ""}
        cikti.append({"ad": o["ad"], "ne_yapar": {"deger": o["ne"][1], "alinti": al(m, o["ne"][0])}, "komut": komut, "sinirlar": sinir,
                      "mekanizma": o["m"], "kanit": al(m, o["kn"])})
    (B / f"v1-yazar-{p}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in cikti), encoding="utf-8")
    print(f"paket {p}: {len(cikti)} kalem yazıldı")


yaz(sys.argv[1])
