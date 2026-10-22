"""EGITIM-1 OGREN kapisi: is turu basina 20 gorev (kod · cikarim · mantik), 3 kol: ucretsiz duz · ucretsiz+sablon · Haiku duz.
Dogrulama betikle (hakem yok): kod = birim testler, cikarim = tam JSON esitligi, mantik = 'CEVAP: <sayi>'.
Kabul: ucretsiz+sablon dogru orani >= %92 (tur basina, sonucsuz yanlis sayilir) VEYA >= Haiku orani (ucretsiz-once gecer).
python tools/ogret/kapi.py [--haiku=60] [--tavan=200] [--tur=kod,cikarim,mantik] → .kos/kopru/ogret/kapi.json
Dis cagri tavani: ucretsiz kol <= tavan, Haiku <= --haiku (varsayilan 60)."""
import concurrent.futures as cf, json, random, re, subprocess, sys, tempfile, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import ucretsiz_havuz as H  # noqa: E402

arg = lambda ad, v: next((a.split("=", 1)[1] for a in sys.argv if a.startswith(f"--{ad}=")), v)  # noqa: E731
HAIKU_TAVAN, DIS_TAVAN, TURLER = int(arg("haiku", 60)), int(arg("tavan", 200)), arg("tur", "kod,cikarim,mantik").split(",")
CIKTI = KOK / ".kos/kopru/ogret/kapi.json"

KOD = [("liste_tekrarsiz", "liste_tekrarsiz(l): sırayı koruyarak tekrarları at", [(([3, 1, 3, 2, 1],), [3, 1, 2]), (([],), [])]),
       ("ters_kelime", "ters_kelime(s): cümledeki kelimelerin sırasını ters çevir (boşlukla ayrılmış)", [(("a b c",), "c b a"), (("tek",), "tek")]),
       ("asal_mi", "asal_mi(n): n asal ise True", [((1,), False), ((2,), True), ((15,), False), ((17,), True)]),
       ("fib", "fib(n): n. Fibonacci (fib(0)=0, fib(1)=1)", [((0,), 0), ((1,), 1), ((10,), 55)]),
       ("palindrom", "palindrom(s): harf/rakam dışını ve büyük-küçük farkını yok sayarak palindrom mu", [(("A man, a plan, a canal: Panama",), True), (("abc",), False)]),
       ("toplam_cift", "toplam_cift(l): listedeki çift sayıların toplamı", [(([1, 2, 3, 4],), 6), (([],), 0)]),
       ("en_uzun", "en_uzun(l): kelime listesinde en uzun kelime; eşitse ilki; boşsa None", [((["a", "abc", "xyz"],), "abc"), (([],), None)]),
       ("sikistir", "sikistir(s): ardışık tekrar eden harfleri harf+sayı yap ('aaabcc' -> 'a3b1c2')", [(("aaabcc",), "a3b1c2"), (("",), "")]),
       ("anagram", "anagram(a, b): büyük-küçük harf ve boşluk yok sayılarak anagram mı", [(("Listen", "Silent"), True), (("ab", "abc"), False)]),
       ("kesisim", "kesisim(a, b): iki listenin ortak elemanları, sıralı ve tekrarsız liste", [(([1, 2, 2, 3], [2, 3, 4]), [2, 3]), (([1], [2]), [])]),
       ("ikili", "ikili(n): negatif olmayan n'nin ikilik tabandaki yazımı (str), ikili(0)='0'", [((5,), "101"), ((0,), "0")]),
       ("ort", "ort(l): sayıların ortalaması, boş liste için 0", [(([1, 2, 3],), 2), (([],), 0)]),
       ("dilimle", "dilimle(l, n): listeyi n'er elemanlı parçalara böl (liste listesi)", [(([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]), (([], 3), [])]),
       ("sayac", "sayac(s): harf sıklığı sözlüğü (boşluk hariç)", [(("aab b",), {"a": 2, "b": 2})]),
       ("gun_say", "gun_say(ay, yil): ayın gün sayısı (artık yıl dahil)", [((2, 2024), 29), ((2, 2023), 28), ((4, 2023), 30)]),
       ("roma", "roma(n): 1-3999 arası n'i Roma rakamına çevir", [((4,), "IV"), ((1994,), "MCMXCIV")]),
       ("duzlestir", "duzlestir(l): iç içe listeyi tek düz listeye çevir", [(([1, [2, [3, 4]], 5],), [1, 2, 3, 4, 5])]),
       ("medyan", "medyan(l): sayıların medyanı (çift sayıda elemanda iki ortanın ortalaması)", [(([3, 1, 2],), 2), (([1, 2, 3, 4],), 2.5)]),
       ("ebob", "ebob(a, b): en büyük ortak bölen", [((12, 18), 6), ((7, 5), 1)]),
       ("ilk_tekrar", "ilk_tekrar(l): listede ikinci kez görülen ilk eleman; yoksa None", [(([1, 2, 3, 2, 1],), 2), (([1, 2],), None)])]


def kod_gorevleri():
    return [dict(id=f"kod{i}", tur="kod", istem=f"Python 3 ile tek bir fonksiyon yaz: {t}. Yalnızca ```python bloğu ver, açıklama ekleme.", ad=ad, testler=tt)
            for i, (ad, t, tt) in enumerate(KOD)]


def cikarim_gorevleri():
    r, ad, soy = random.Random(7), ["Ayşe", "Mehmet", "Zeynep", "Can", "Elif", "Burak", "Selin", "Deniz"], ["Demir", "Kaya", "Yılmaz", "Çelik", "Aksoy"]
    out = []
    for i in range(20):
        a, t = f"{r.choice(ad)} {r.choice(soy)}", r.choice([250, 1250, 9800, 15400, 320, 48500])
        g, ay, y = r.randint(1, 28), r.randint(1, 12), r.choice([2025, 2026])
        ts = f"{t:,}".replace(",", ".")
        m = r.choice([f"{a} {ts} TL ödedi, tarih {g:02d}.{ay:02d}.{y}.", f"Tarih: {g:02d}/{ay:02d}/{y}. Müşteri {a}, tutar {ts} TL.", f"{g}.{ay}.{y} günü {a} adlı kişi {ts} TL'lik fatura kesti."])
        out.append(dict(id=f"cik{i}", tur="cikarim", istem=f"Metinden JSON çıkar: {{\"ad\": str, \"tutar_tl\": int, \"tarih\": \"YYYY-AA-GG\"}}. Yalnız JSON ver.\nMetin: '{m}'",
                        beklenen=dict(ad=a, tutar_tl=t, tarih=f"{y}-{ay:02d}-{g:02d}")))
    return out


def mantik_gorevleri():
    r, out = random.Random(11), []
    for i in range(20):
        k = i % 4
        if k == 0:
            a, b, c = r.randint(3, 9), r.randint(5, 15), r.randint(1, 20); s, c = f"Bir kutuda {b} kalem var; {a} kutu alınıp {c} kalem hediye edildi. Kaç kalem kaldı?", c; v = a * b - c
        elif k == 1:
            h, t = r.randint(40, 90), r.randint(2, 6); s = f"Bir araç saatte {h} km gider. {t} saat gittikten sonra yolun {r.randint(10, 30)} km'si kalıyor; toplam yol, gidilen yolun {t*h} km olduğu bilgisiyle kalan 25 km ile birlikte kaç km?"; v = t * h + 25
            s = f"Bir araç saatte {h} km gider, {t} saat gittikten sonra gidecek 25 km daha kalıyor. Toplam yol kaç km?"
        elif k == 2:
            n, p = r.randint(4, 12), r.choice([5, 10, 20, 25]); f = r.choice([200, 400, 800]); s = f"{n} kişilik grup kişi başı {f} TL öder; toplama %{p} indirim uygulanır. Ödenecek toplam kaç TL?"; v = round(n * f * (100 - p) / 100)
            if (n * f * (100 - p)) % 100:
                s = f"{n} kişilik grup kişi başı {f} TL öder; toplama %20 indirim uygulanır. Ödenecek toplam kaç TL?"; v = round(n * f * 0.8)
        else:
            a, b = r.randint(12, 30), r.randint(2, 5); s = f"Ali'nin {a} bilyesi var; arkadaşı ona kendi bilyelerinin yarısı kadar ({a*b} bilyesi olan arkadaş) değil, Ali'nin {b} katı kadar bilye verirse Ali'nin kaç bilyesi olur?"; v = a + a * b
            s = f"Ali'nin {a} bilyesi var. Arkadaşı ona Ali'nin bilye sayısının {b} katı kadar bilye verirse Ali'nin kaç bilyesi olur?"
        out.append(dict(id=f"man{i}", tur="mantik", istem=f"{s} Adım adım hesapla. Son satır tam olarak: CEVAP: <sayı>", beklenen=int(v)))
    return out


def kod_dogru(g, y):
    m = re.search(r"```(?:python)?\s*(.*?)```", y, re.S)
    kod = (m.group(1) if m else y).strip()
    prog = kod + "\n" + "\n".join(f"assert {g['ad']}(*{a!r}) == {e!r}, {a!r}" for a, e in g["testler"]) + "\nprint('OK')"
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "t.py").write_text(prog, encoding="utf-8")
        try:
            p = subprocess.run([sys.executable, "-I", "t.py"], cwd=d, capture_output=True, text=True, timeout=10, creationflags=H.NW)
        except subprocess.TimeoutExpired:
            return False
    return "OK" in p.stdout


def cikarim_dogru(g, y):
    m = re.search(r"\{.*\}", y, re.S)
    try:
        return json.loads(m.group(0)) == g["beklenen"]
    except (AttributeError, ValueError):
        return False


def mantik_dogru(g, y):
    m = re.findall(r"CEVAP:\s*\**\s*(-?[\d.,]+)", y)
    try:
        return bool(m) and float(m[-1].replace(".", "").replace(",", ".") if m[-1].count(".") > 1 or "," in m[-1] else m[-1]) == g["beklenen"]
    except ValueError:
        return False


DOGRU = dict(kod=kod_dogru, cikarim=cikarim_dogru, mantik=mantik_dogru)
GOREV = dict(kod=kod_gorevleri, cikarim=cikarim_gorevleri, mantik=mantik_gorevleri)


def kos(g, kol):
    try:
        if kol == "haiku":
            y, model = H._haiku(g["istem"]), "haiku"
        else:
            y, model, _ = H.cagir("yazim", g["istem"], max_tokens=2500, zaman=70, sablon=g["tur"] if kol == "sablon" else None)
    except Exception as x:  # noqa: BLE001 — kapi tek gorevde dusmesin
        return dict(id=g["id"], kol=kol, ok=None, model=type(x).__name__)
    if y is None:
        return dict(id=g["id"], kol=kol, ok=None, model=None)
    ok = DOGRU[g["tur"]](g, y)
    if ok and kol == "sablon":  # katman 1b: dogrulanmis basari -> sablon havuzu
        from ogret.sarmal import kaydet
        kaydet(g["tur"], g["istem"], y)
    return dict(id=g["id"], kol=kol, ok=ok, model=model)


def main():
    gorevler = [g for t in TURLER for g in GOREV[t]()]
    isler = [(g, "duz") for g in gorevler] + [(g, "sablon") for g in gorevler]
    if HAIKU_TAVAN:
        isler += [(g, "haiku") for g in gorevler[:HAIKU_TAVAN]]
    assert sum(1 for _, k in isler if k != "haiku") <= DIS_TAVAN, "dis cagri tavani"
    t0, sonuc = time.time(), []
    with cf.ThreadPoolExecutor(4) as ex:
        for s in ex.map(lambda a: kos(*a), isler):
            sonuc.append(s)
    ozet = {}
    for t in TURLER:
        for kol in ("duz", "sablon", "haiku"):
            r = [s for s in sonuc if s["id"].startswith({"kod": "kod", "cikarim": "cik", "mantik": "man"}[t]) and s["kol"] == kol]
            if r:
                ozet[f"{t}/{kol}"] = dict(n=len(r), dogru=sum(1 for s in r if s["ok"]), sonucsuz=sum(1 for s in r if s["ok"] is None))
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    CIKTI.write_text(json.dumps(dict(ozet=ozet, sonuc=sonuc, sn=round(time.time() - t0)), ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in ozet.items():
        print(k, v)


if __name__ == "__main__":
    main()
