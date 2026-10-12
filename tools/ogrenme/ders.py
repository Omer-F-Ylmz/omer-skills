"""RUFLO-1 ders bankası: ReasoningBank döngüsünün bizdeki karşılığı (Ruflo kodu kopyalanmadı; mekanizma uyarlandı).

Döngü: koşu sonu ajan ≤3 ders adayı yazar (damıtma) → yargıç (test/ölçüt/jev sonucu) sonuc=basari|basarisizlik verir →
ekle(): sır süzgeci + birleştirme (yinelenen ders destek++ alır) → getir(): görev başında ajan kapsamı + BM25 ile top-k ≤3,
≤300 jeton blok → geri_bildir(): kullanılan dersin görevi başarısızsa güveni düşer, 3 kullanımda güven <0.34 → dusuk (çağrılmaz).
Depo: $OGRENME_DIZIN ya da C:/Projeler/omer-skills/.kos/ogrenme (dersler.jsonl + getirme.jsonl).
python ders.py getir --ajan kod --gorev "..." | ekle --ajan kod --sonuc basari --dosya aday.json --kaynak <koşu>
              | geri --id a1b2,c3d4 --sonuc basarisizlik | liste
"""
import argparse, hashlib, json, math, os, re, sys, time
from pathlib import Path

VARSAYILAN = Path("C:/Projeler/omer-skills/.kos/ogrenme")
K, JETON, EN_FAZLA_ADAY = 3, 300, 3
SIR = [r"sk-ant-[\w-]{10,}", r"\bsk-[A-Za-z0-9]{20,}", r"\bgh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_\w{20,}",
       r"\bAKIA[0-9A-Z]{16}\b", r"\bxox[abps]-[\w-]{10,}", r"-----BEGIN [A-Z ]*KEY-----", r"\bBearer\s+[\w.-]{20,}",
       r"(?i)\b(parola|password|şifre|sifre|secret|token|api[_-]?key)\s*[:=]\s*\S+", r"[\w.+-]+@[\w-]+\.[\w.]+",
       r"(?i)[a-z]:[\\/]+users[\\/]+[^\\/\s]+", r"\b[0-9a-f]{32,}\b", r"\b[A-Za-z0-9+/]{40,}={0,2}"]


def dizin():
    d = Path(os.environ.get("OGRENME_DIZIN") or VARSAYILAN)
    d.mkdir(parents=True, exist_ok=True)
    return d


def kelimeler(metin):
    return [w for w in re.findall(r"\w+", metin.replace("İ", "i").replace("I", "ı").lower()) if len(w) > 1]


def oku():
    p = dizin() / "dersler.jsonl"
    return [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()] if p.exists() else []


def _yaz(dersler):
    p = dizin() / "dersler.jsonl"
    gecici = p.with_suffix(".tmp")
    gecici.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in dersler), encoding="utf-8", newline="\n")
    os.replace(gecici, p)


class _Kilit:
    """Filo ajanları aynı anda yazabilir: O_EXCL kilit dosyası, ≤10 sn bekler, 60 sn'den eski kilit bayat sayılır."""
    def __enter__(self):
        self.yol = dizin() / "kilit"
        for _ in range(100):
            try:
                os.close(os.open(self.yol, os.O_CREAT | os.O_EXCL))
                return self
            except FileExistsError:
                if time.time() - self.yol.stat().st_mtime > 60:
                    self.yol.unlink(missing_ok=True)
                time.sleep(0.1)
        raise TimeoutError("ders bankası kilidi alınamadı")

    def __exit__(self, *_):
        self.yol.unlink(missing_ok=True)


def sir_var(metin):
    return any(re.search(k, metin) for k in SIR)


def _guven(x):
    return (x["yardim"] + 1) / (x["kullanim"] + 2)


def ekle(ajan, baslik, kosul, icerik, sonuc, kaynak, kanit=""):
    """Sırlı ders reddedilir (ValueError). Aynı ajan + baslik/kosul Jaccard ≥0.8 → birleşir (destek++)."""
    if sir_var(" ".join([baslik, kosul, icerik, kanit])):
        raise ValueError("ders sır/kişisel veri içeriyor — reddedildi")
    if sonuc not in ("basari", "basarisizlik"):
        raise ValueError("sonuc basari|basarisizlik olmalı")
    with _Kilit():
        dersler, anahtar = oku(), set(kelimeler(baslik + " " + kosul))
        for x in dersler:
            k2 = set(kelimeler(x["baslik"] + " " + x["kosul"]))
            ayni = (x["baslik"], x["kosul"]) == (baslik[:120], kosul[:200])
            if x["ajan"] == ajan and (ayni or anahtar and len(anahtar & k2) / len(anahtar | k2) >= 0.8):
                x["destek"] += 1
                x["kaynaklar"] = (x["kaynaklar"] + [kaynak])[-10:]
                x["son"] = time.strftime("%Y-%m-%d")
                if sonuc == "basari" and x["tur"] == "basarisizlik":
                    x["icerik"] = icerik[:600]  # başarılı koşu, aynı tuzağın çözümünü verir
                _yaz(dersler)
                return {"id": x["id"], "durum": "birlesti"}
        x = {"id": hashlib.sha1(f"{ajan}|{baslik}|{kosul}".encode()).hexdigest()[:6], "ajan": ajan, "baslik": baslik[:120],
             "kosul": kosul[:200], "icerik": icerik[:600], "tur": sonuc, "kanit": kanit[:200], "kaynaklar": [kaynak],
             "destek": 1, "kullanim": 0, "yardim": 0, "durum": "aktif", "tarih": time.strftime("%Y-%m-%d"),
             "son": time.strftime("%Y-%m-%d")}
        _yaz(dersler + [x])
        return {"id": x["id"], "durum": "yeni"}


def getir(ajan, gorev, k=K, kosu=""):
    """→ (blok, ids). Ajan kapsamı (kendi + '*'), BM25 ≥2 ortak terim, en iyinin yarısı eşiği, güven × eskime ağırlığı."""
    aday = [x for x in oku() if x["durum"] == "aktif" and x["ajan"] in (ajan, "*")]
    sorgu = set(kelimeler(gorev))
    if not aday or not sorgu:
        return "", []
    belgeler = [kelimeler(" ".join([x["baslik"], x["kosul"], x["icerik"]])) for x in aday]
    ort = sum(map(len, belgeler)) / len(belgeler)
    df = {w: sum(w in set(b) for b in belgeler) for w in sorgu}
    puanlar = []
    for x, b in zip(aday, belgeler):
        ortak = sorgu & set(b)
        if len(ortak) < 2:
            continue
        bm = sum(math.log(1 + (len(belgeler) - df[w] + 0.5) / (df[w] + 0.5)) * b.count(w) * 2.2
                 / (b.count(w) + 1.2 * (0.25 + 0.75 * len(b) / ort)) for w in ortak)
        yas = (time.time() - time.mktime(time.strptime(x["son"], "%Y-%m-%d"))) / 86400
        puanlar.append((bm * _guven(x) * 0.5 ** (yas / 60) * (1 + 0.1 * min(x["destek"], 5)), x))
    puanlar.sort(key=lambda p: -p[0])
    secilen = [x for p, x in puanlar[:k] if p >= puanlar[0][0] * 0.5]
    if not secilen:
        return "", []
    satirlar, pay = ["İlgili dersler (önceki koşulardan; göreve uymuyorsa yok say):"], (JETON * 4 - 70) // len(secilen)
    for x in secilen:
        s = f"- [{x['id']} · {'kaçın' if x['tur'] == 'basarisizlik' else '✓'}] {x['baslik']} — ne zaman: {x['kosul']}. {x['icerik']}"
        satirlar.append(s[:pay])
    ids = [x["id"] for x in secilen]
    with open(dizin() / "getirme.jsonl", "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "ajan": ajan, "kosu": kosu, "ids": ids}) + "\n")
    return "\n".join(satirlar), ids


def geri_bildir(ids, basari):
    with _Kilit():
        dersler = oku()
        for x in dersler:
            if x["id"] in ids:
                x["kullanim"] += 1
                x["yardim"] += int(basari)
                if x["kullanim"] >= 3 and _guven(x) < 0.34:
                    x["durum"] = "dusuk"
        _yaz(dersler)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    alt = ap.add_subparsers(dest="komut", required=True)
    g = alt.add_parser("getir")
    g.add_argument("--ajan", required=True)
    g.add_argument("--gorev", required=True)
    g.add_argument("--k", type=int, default=K)
    g.add_argument("--kosu", default="")
    e = alt.add_parser("ekle")
    e.add_argument("--ajan", required=True)
    e.add_argument("--sonuc", required=True, choices=["basari", "basarisizlik"])
    e.add_argument("--kaynak", required=True)
    e.add_argument("--kanit", default="")
    e.add_argument("--dosya", help="JSON liste: [{baslik, kosul, icerik}] (ilk 3 alınır)")
    for a in ("--baslik", "--kosul", "--icerik"):
        e.add_argument(a, default="")
    r = alt.add_parser("geri")
    r.add_argument("--id", required=True)
    r.add_argument("--sonuc", required=True, choices=["basari", "basarisizlik"])
    alt.add_parser("liste")
    a = ap.parse_args(argv)
    if a.komut == "getir":
        blok, _ = getir(a.ajan, a.gorev, min(a.k, K), a.kosu)
        if blok:
            print(blok)
    elif a.komut == "ekle":
        adaylar = json.loads(Path(a.dosya).read_text(encoding="utf-8")) if a.dosya else [vars(a)]
        for d in adaylar[:EN_FAZLA_ADAY]:
            try:
                print(ekle(a.ajan, str(d.get("baslik", "")), str(d.get("kosul", "")), str(d.get("icerik", "")), a.sonuc,
                           a.kaynak, a.kanit))
            except ValueError as h:
                print(f"RET: {h}", file=sys.stderr)
    elif a.komut == "geri":
        geri_bildir(a.id.split(","), a.sonuc == "basari")
    else:
        for x in oku():
            print(f"{x['id']}\t{x['ajan']}\t{x['tur']}\t{x['durum']}\tdestek={x['destek']}\tguven={_guven(x):.2f}\t{x['baslik']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
