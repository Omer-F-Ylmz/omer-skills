"""ÖĞREN-4 d1 (video-medya): ÖĞREN-1 d14 hattı yeniden (kaynak çözümü d14.metin · sert d13.sert · Claude yazar); yalnız
kalem kümesi = katalog-son video-medya kanonik kurulu, `mekanizma` kapalı listesi = video rolü (ROL).
  python -X utf8 .claude/ogren4/v1.py hazirla      → kaynak/<ad>.txt + v1-ornek.tsv + v1-paket-N.md (paket başına ~12 kalem)
  python -X utf8 .claude/ogren4/v1.py birlestir    → v1-yazar-*.jsonl → .kos/kopru/ogren/ozet-video-v1.jsonl + hakem-video-v1.jsonl + video-disi-geri.tsv"""
import json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "ogren1"))
import d14, ozet3, ozet_kaynak
from d13 import A, O, sert
from ozet3 import BASLIK, adlari, kaynaksiz
from son import oku

ROL = ["indirme", "dönüştürme", "transkript", "kare analizi", "özetleme", "kurgu", "render üretimi", "ses", "görsel üretim", "rehber", "video-dışı"]
ozet3.MEKANIZMA = ROL  # gecerli_b modül globalini okur
B = Path(__file__).parent
K = B / "kaynak"
PAKET = 12
YOL = {"whisper-cli": r"C:\Projeler\.tmp-video\whisper.cpp\v1.8.0\Release\whisper-cli.exe"}  # katalogda yol boş


def dosya(ad):
    return K / (re.sub(r"[^\w.-]", "_", ad) + ".txt")


def metin(ad, yol):
    """d14.metin + video kalemleri: ikili CLI → kendi --help çıktısı; model kataloğu → yalnız kalemin girdisi"""
    p = Path(yol)
    if p.suffix.lower() == ".exe":
        y = subprocess.run([yol, "-h" if ad in ("ffmpeg", "ffprobe") else "--help"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        return f"=== {ad} yardım: {yol} ===\n{y.stdout}{y.stderr}"
    if p.name == "omni_models_api.json":
        return "\n".join(f"=== model kaydı: {p} · {ad} ===\n" + json.dumps(m, ensure_ascii=False, indent=2)
                         for m in json.loads(p.read_text(encoding="utf-8")) if m["id"] == ad) + "\n"
    return d14.metin(ad, yol)


def D():
    return dict(s.split("\t")[::3] for s in (B / "v1-ornek.tsv").read_text(encoding="utf-8").splitlines())


def hazirla():
    t = [json.loads(x) for x in (O / "katalog-son.jsonl").read_text(encoding="utf-8").splitlines()]
    k = {r["ad"]: r for r in reversed(t) if r["kategori_son"] == "video-medya" and r["tur"] != "aday" and r["kanonik"] == r["id"]}  # aynı adlı kopya: ilk kalır
    K.mkdir(exist_ok=True)
    sec, bos = [], []
    for ad, r in sorted(k.items()):
        r["yol"] = YOL.get(ad, r["yol"])
        m = metin(ad, r["yol"])
        (bos if kaynaksiz(adlari(ad, r["yol"]), m) else sec).append([ad, r["tur"], str(r["bayt"]), r["yol"]])
        if sec and sec[-1][0] == ad:
            dosya(ad).write_text(m, encoding="utf-8")
    (B / "v1-ornek.tsv").write_text("".join("\t".join(s) + "\n" for s in sec), encoding="utf-8")
    (B / "v1-kaynaksiz.tsv").write_text("".join("\t".join(s) + "\n" for s in bos), encoding="utf-8")
    ozet_kaynak.D = D()
    n = -(-len(sec) // PAKET)
    for i in range(n):
        parca = []
        for ad, _, _, kaynak in sec[i::n]:  # şeritli dağıtım: büyük/küçük kaynaklar paketlere yayılır
            m, an = dosya(ad).read_text(encoding="utf-8"), sorted(adlari(ad, kaynak))
            parca += [f"## {ad}", f"kaynak: {dosya(ad)} (çözülmüş; özgün: {kaynak}) · {len(m.splitlines())} satır · araç adları ({len(an)}): {' · '.join(an[:30])}",
                      "BAŞLIKLAR: " + " · ".join(p.split("\n", 1)[0].strip()[:60] for p in BASLIK.split(m)[1:])[:1500], ""]
        (B / f"v1-paket-{i + 1}.md").write_text("\n".join(parca), encoding="utf-8")
    print(f"kaynaklı {len(sec)} · kaynaksız {len(bos)} · paket {n}")


def birlestir():
    ozet_kaynak.D = D()
    c = {}
    for p in sorted(B.glob("v1-yazar-*.jsonl")):
        c.update(oku(p))
    son, ret = {}, {}
    for ad, kaynak in D().items():
        if ad not in c:
            ret[ad] = "yazar satırı yok"
            continue
        m, y = dosya(ad).read_text(encoding="utf-8"), c[ad]
        r = {"ad": ad, "kaynak": str(dosya(ad)), "ozgun": kaynak, **{a: y[a]["deger"] for a in A}, "alinti": {a: y[a].get("alinti", "") for a in A},
             "mekanizma": y["mekanizma"], "kanit": y.get("kanit", ""), "dogrulandi": "claude-yazar"}
        neden, r["uyari"] = sert(r, m, adlari(ad, kaynak))
        if neden:
            ret[ad] = neden
        son[ad] = r
    for ad, h in ret.items():
        print("RET", ad, h, sep="\t")
    for ad, r in son.items():
        for u in r["uyari"]:
            print("UYARI", ad, u, sep="\t")
    (O / "ozet-video-v1.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in son.values()), encoding="utf-8")
    (O / "hakem-video-v1.jsonl").write_text("".join(json.dumps({k: r[k] for k in ["ad", "kaynak", "ozgun"] + A + ["mekanizma"]}, ensure_ascii=False) + "\n"
                                                for r in son.values()), encoding="utf-8")
    disi = [r for r in son.values() if "video-dışı" in r["mekanizma"]]  # ÖĞREN-0b'ye kategori hatası geri bildirimi
    (O / "video-disi-geri.tsv").write_text("".join(f"{r['ad']}\t{r['ozgun']}\t{r['ne_yapar']}\t{r['kanit']}\n" for r in disi), encoding="utf-8")
    print(f"son {len(son)} · RET {len(ret)} · UYARI {sum(len(r['uyari']) for r in son.values())} · video-dışı {len(disi)}")


if __name__ == "__main__":
    {"hazirla": hazirla, "birlestir": birlestir}[sys.argv[1]]()
