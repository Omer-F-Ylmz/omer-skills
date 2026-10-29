"""USTA-KART-1: kurulu her kalem için ustalık kartı (3 kullanım · tuzak · jeton ipucu · kombin · örnek çağrı). Üretim YALNIZ ücretsiz havuz.
  python -I tools/usta_kart.py say                      envanter: kartlı / kartsız / eski (>30 gün), türe göre
  python -I tools/usta_kart.py uret [--n 50] [--is 3]   öncelik sırasıyla (boşta → kullanılan → kalan) kart üretir, docs/usta-kart/usta.jsonl'e ekler
  python -I tools/usta_kart.py hakem [--n 20]           rastgele kartları Haiku hakemle puanlar (doğru+yararlı oranı)
  python -I tools/usta_kart.py obsidian                 kart dizinini 30-araclar/usta-kart-dizin.md'ye yazar
Kaynak: aracın kendi SKILL.md/README (ilk ~900 karakter) → Claude bağlamına girmez, doğrudan ücretsiz modele gider."""
import csv, json, os, random, re, subprocess, sys, time, unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
KART = KOK / "docs/arac-kart/kart.jsonl"
USTA = KOK / "docs/usta-kart/usta.jsonl"
BOSTA = KOK / ".kos/kopru/rapor/bosta-arac-1-liste.tsv"
ENV = KOK / "docs/envanter/envanter.tsv"
ILERLEME = KOK / ".kos/kopru/usta-kart-ilerleme.json"
KASA = Path(r"C:\Users\pc\Desktop\Obsidian") / "30-araclar"
GUN30 = 30 * 86400
ALANLAR = ["kullanim", "tuzak", "token_ipucu", "kombin", "ornek"]
GRUP = 4
SURE = int(os.environ.get("USTA_SURE", "540"))  # dongu üst süre (sn)
ISTEM = """Sen araç dokümanı damıtıcısın. Aşağıdaki {n} kalemin HER biri için YALNIZ verilen kaynak metne dayanarak Türkçe ustalık kartı yaz.
Uydurma yok: kaynakta olmayan şeyi yazma; bilgi yetmiyorsa kısa ve genel kal.
Çıktı: YALNIZ geçerli JSON dizisi, kalem sırasıyla, her eleman:
{{"ad":"<aynen>","kullanim":["en iyi kullanım 1","2","3"],"tuzak":"en sık hata/tuzak (1 cümle)","token_ipucu":"jeton tasarrufu ipucu (1 cümle)","kombin":["birlikte kullanılan araç adları, en çok 3"],"ornek":"kaynakta AYNEN geçen bir komut/çağrı; yoksa boş string"}}
Kural: kaynakta olmayan komut, bayrak, CLI, API adı ya da parametre YAZMA (uydurma örnek en sık hatadır); kombin yalnız kaynakta adı geçen araçlar, yoksa boş liste; kaynak başka bir şeyden söz ediyorsa kısa ve genel kal.
Her metin ≤140 karakter.

{kalemler}"""


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower().split(":")[-1])


def oku_usta():
    d = {}
    if USTA.exists():
        for l in USTA.read_text(encoding="utf-8").splitlines():
            if l.strip():
                k = json.loads(l); d[k["ad"]] = k
    return d


def kartlar():
    return [json.loads(l) for l in KART.read_text(encoding="utf-8").splitlines() if l.strip()]


def bosta_kumesi():
    s = set()
    if BOSTA.exists():
        for l in BOSTA.read_text(encoding="utf-8").splitlines()[1:]:
            p = l.split("\t")
            if len(p) > 1 and p[1] != ".trash":
                s.add(norm(p[1]))
    return s


def kullanilan_kumesi():
    s = set()
    with open(ENV, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r.get("son_kullanim"):
                s.add(norm(r["ad"]))
    return s


def sirali(K, U):
    bos, kul = bosta_kumesi(), kullanilan_kumesi()
    simdi = time.time()
    adaylar = [k for k in K if not (k["ad"] in U and simdi - U[k["ad"]]["tarih"] < GUN30)]
    def anahtar(k):
        n = norm(k["ad"])
        return 0 if n in bos else (1 if n in kul else 2)
    return sorted(adaylar, key=anahtar)


def kaynak(k, lim=900):
    yol = k.get("yol") or ""
    if yol and os.path.exists(yol):
        try:
            t = Path(yol).read_text(encoding="utf-8", errors="replace")
            m = re.match(r"^---\s*(.*?)\n---\s*", t, flags=re.S)
            fm = ""
            if m:
                fm = " ".join(l.strip() for l in m.group(1).splitlines() if re.match(r"\s*(name|description|triggers):|\s*- ", l))[:350]
                t = t[m.end():]
            t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
            parcalar = re.split(r"(?m)^(?=#{1,3} )", t)
            govde = "".join(x for x in parcalar if not re.match(r"#{1,3} .*(preamble|telemetry|upgrade check)", x, flags=re.I))
            return re.sub(r"\s+", " ", fm + " " + govde)[:lim]
        except OSError:
            pass
    return re.sub(r"\s+", " ", f"{k.get('ne','')} {k.get('ba','')} {k.get('etiket','')}")[:600]


def dogrula_fabrika(adlar):
    def d(m):
        try:
            a = json.loads(m[m.index("["):m.rindex("]") + 1])
        except (ValueError, json.JSONDecodeError):
            return "json"
        if not isinstance(a, list) or len(a) != len(adlar):
            return "sayi"
        for e, ad in zip(a, adlar):
            if not isinstance(e, dict) or any(not e.get(x) for x in ALANLAR if x not in ("ornek", "kombin")) or len(e["kullanim"]) < 3:
                return "alan"
        return None
    return d


def temiz(x):
    x = unicodedata.normalize("NFC", str(x)).replace(chr(0xfffd), "")
    return "".join(c for c in x if ord(c) >= 32 and not (0x200b <= ord(c) <= 0x200f or 0x3000 <= ord(c) <= 0x9fff or 0xac00 <= ord(c) <= 0xd7af)).strip()


DOGRU_ISTEM = """Denetçisin. Her kartın her satırı kaynak metinle DESTEKLENİYOR mu (kaynakta geçen ya da doğrudan çıkarılabilen)? Kaynakla çelişen ya da kaynakta olmayan iddia = false.
YALNIZ JSON dizisi, kart sırasıyla: [{{"kullanim":[b,b,b],"tuzak":b,"token_ipucu":b}}] (b = true/false).

{kalemler}"""


def ikinci_goz(out, grup):
    """Her iddia satiri kaynaga karsi: desteklenmeyen satir silinmez, 'dogrulanamadi' alanina tasinir."""
    import ucretsiz_havuz as H
    NLC = chr(10)
    kal = NLC.join(f"### {i+1}. {k['ad']}" + NLC + f"KAYNAK: {kaynak(k)}" + NLC + "KART: " + json.dumps({x: c[x] for x in ("kullanim", "tuzak", "token_ipucu")}, ensure_ascii=False) for i, (c, k) in enumerate(zip(out, grup)))

    def d(m):
        try:
            a = json.loads(m[m.index("["):m.rindex("]") + 1])
        except (ValueError, json.JSONDecodeError):
            return "json"
        return None if isinstance(a, list) and len(a) == len(out) and all(isinstance(e, dict) for e in a) else "sayi"
    m, _, _ = H.cagir("ozet", DOGRU_ISTEM.format(kalemler=kal), max_tokens=1500, haric_aile="anthropic", dogrula=d, etiket="usta-kart-dogrula")
    if not m:
        for c in out:
            c["dogrulanamadi"] = ["(denetlenemedi)"]
        return
    a = json.loads(m[m.index("["):m.rindex("]") + 1])
    for c, v in zip(out, a):
        bad = []
        ku = v.get("kullanim") if isinstance(v.get("kullanim"), list) else []
        keep = [x for i, x in enumerate(c["kullanim"]) if i >= len(ku) or ku[i] is not False]
        bad += [x for x in c["kullanim"] if x not in keep]
        c["kullanim"] = keep
        for f in ("tuzak", "token_ipucu"):
            if v.get(f) is False:
                bad.append(c[f])
                c[f] = ""
        if bad:
            c["dogrulanamadi"] = bad


def grup_uret(grup):
    import ucretsiz_havuz as H
    adlar = [k["ad"] for k in grup]
    kal = "\n".join(f"### {i+1}. {k['ad']} ({k['tur']})\n{kaynak(k)}" for i, k in enumerate(grup))
    m, kol, log = H.cagir("ozet", ISTEM.format(n=len(grup), kalemler=kal), max_tokens=2200,
                          haric_aile="anthropic", dogrula=dogrula_fabrika(adlar), etiket="usta-kart")
    if not m:
        return [], None, log
    a = json.loads(m[m.index("["):m.rindex("]") + 1])
    out = []
    for e, k in zip(a, grup):
        src = kaynak(k)
        o = str(e.get("ornek") or "").strip()
        e["ornek"] = o if o and o in src else (f"Skill {k['ad']}" if "skill" in str(k["tur"]) else k["ad"])  # uydurma komut kalıbı: örnek kaynakta yoksa çağrı adı
        e["kombin"] = [x for x in (e.get("kombin") if isinstance(e.get("kombin"), list) else []) if str(x).lower() in src.lower()]
        out.append({"ad": k["ad"], "tur": k["tur"], "kullanim": [temiz(x)[:200] for x in e["kullanim"][:3]], "tuzak": temiz(e["tuzak"])[:220],
                    "token_ipucu": temiz(e["token_ipucu"])[:220], "kombin": [str(x)[:60] for x in (e["kombin"] if isinstance(e["kombin"], list) else [e["kombin"]])[:3]],
                    "ornek": str(e["ornek"])[:220], "model": kol, "tarih": int(time.time())})
    ikinci_goz(out, grup)
    return out, kol, log


def say():
    K, U = kartlar(), oku_usta()
    simdi = time.time()
    sat = {}
    for k in K:
        s = sat.setdefault(k["tur"], [0, 0, 0])
        s[0] += 1
        u = U.get(k["ad"])
        if not u: s[1] += 1
        elif simdi - u["tarih"] > GUN30: s[2] += 1
    for t, (n, yok, eski) in sorted(sat.items()):
        print(f"{t}\ttoplam {n}\tkartsiz {yok}\teski {eski}")
    tp = sum(v[0] for v in sat.values())
    print(f"TOPLAM {tp}\tkartli {len(U)}\tkartsiz/eski {sum(v[1]+v[2] for v in sat.values())}")
    with open(ENV, encoding="utf-8", newline="") as f:
        import collections
        print("envanter.tsv:", dict(collections.Counter(r["tur"] for r in csv.DictReader(f, delimiter="\t"))))


def uret(n, is_):
    K, U = kartlar(), oku_usta()
    S = sirali(K, U)[:n]
    gruplar = [S[i:i + GRUP] for i in range(0, len(S), GRUP)]
    USTA.parent.mkdir(parents=True, exist_ok=True)
    yeni, bos = 0, 0
    with ThreadPoolExecutor(is_) as ex:
        for out, kol, log in ex.map(grup_uret, gruplar):
            if not out:
                bos += 1; print("BOS", log[-3:], flush=True); continue
            with open(USTA, "a", encoding="utf-8", newline="\n") as f:
                for c in out:
                    f.write(json.dumps(c, ensure_ascii=False) + "\n")
            yeni += len(out)
    ILERLEME.write_text(json.dumps({"yeni": yeni, "bos_grup": bos, "toplam_kart": len(oku_usta())}), encoding="utf-8")
    print(f"yeni {yeni} bos_grup {bos} toplam {len(oku_usta())}")


def dongu(hedef, is_):
    """Arka plan: 50'şer kartlık dilimler; havuz boşsa 3 dk bekler (halkalar soğuma/kota); hedef kart sayısına ya da 6 ardışık boş dilime kadar."""
    bos, son = 0, time.time() + SURE
    while len(oku_usta()) < hedef and bos < 20 and time.time() < son:
        once = len(oku_usta())
        uret(12, is_)
        if len(oku_usta()) == once:
            bos += 1; time.sleep(60)
        else:
            bos = 0
    print("dongu bitti", len(oku_usta()), flush=True)


def hakem(n):
    U = list(oku_usta().values())
    ornek = random.sample(U, min(n, len(U)))
    K = {k["ad"]: k for k in kartlar()}
    par = "\n".join(f"[{i}] {c['ad']} | kaynak: {kaynak(K[c['ad']])}\n kart: {json.dumps({x: c[x] for x in ALANLAR}, ensure_ascii=False)}" for i, c in enumerate(ornek))
    ist = ("Hakemsin. Her kart için: kaynak metne göre DOĞRU (uydurma/yanlış yok) ve YARARLI (somut, genel geçer değil) mi? "
           'YALNIZ JSON dizisi: [{"i":0,"dogru":true,"yararli":true,"neden":"≤10 kelime"}...]\n\n' + par)
    r = subprocess.run(["claude", "-p", "--model", "claude-haiku-5-5", "--no-session-persistence"], input=ist, capture_output=True, text=True, encoding="utf-8", timeout=300, env=dict(os.environ), creationflags=0x08000000)
    m = r.stdout
    a = json.loads(m[m.index("["):m.rindex("]") + 1])
    ok = sum(1 for e in a if e.get("dogru") and e.get("yararli"))
    print(f"hakem {ok}/{len(a)} = {ok/len(a):.0%}")
    for e in a:
        if not (e.get("dogru") and e.get("yararli")):
            print(" RED", ornek[e["i"]]["ad"], e.get("neden"))


def hazirla(grup_n, n=50):
    """Haiku kolu: kartı olmayan/eski ilk n kalemi (öncelik sırasıyla) grup_n'lik istem dosyalarına yazar; sıra manifest.json'da (alt ajan g<i>.txt okur, g<i>.json yazar)."""
    U = oku_usta()
    if "--zayif" in sys.argv:  # ornek/kombin boş kalan kartları yeniden üret
        Z = {a for a, c in U.items() if not c["kombin"] or c["ornek"] in (a, "Skill " + a)}
        S = [k for k in kartlar() if k["ad"] in Z][:n]
    else:
        S = sirali(kartlar(), U)[:n]
    d = KOK / ".kos/kopru/usta-haiku/ileri"
    d.mkdir(parents=True, exist_ok=True)
    (d / "manifest.json").write_text(json.dumps([k["ad"] for k in S], ensure_ascii=False), encoding="utf-8")
    for i in range(0, len(S), grup_n):
        g = S[i:i + grup_n]
        kd = d / "kaynak"; kd.mkdir(exist_ok=True)
        pr = []
        for j, k in enumerate(g):
            src = kaynak(k, 6000); f = kd / f"{i+j}.txt"
            f.write_text(src, encoding="utf-8")
            assert len(f.read_text(encoding="utf-8")) == len(src) <= 6000
            pr.append(f"### {j+1}. {k['ad']} ({k['tur']}) kaynak dosyası (TAMAMINI Read ile oku, {len(src)} karakter): {f}")
        kal = "\n".join(pr)
        (d / f"g{i//grup_n}.txt").write_text(ISTEM.format(n=len(g), kalemler=kal), encoding="utf-8")
    print("istem", -(-len(S) // grup_n), "kalem", len(S))


def isle(grup_n):
    """Haiku çıktısı g<i>.json'u aynı süzgeçle ileri/haiku.jsonl'e yazar (manifest sırasıyla)."""
    d = KOK / ".kos/kopru/usta-haiku/ileri"
    K = {k["ad"]: k for k in kartlar()}
    S = [K[a] for a in json.loads((d / "manifest.json").read_text(encoding="utf-8"))]
    out = []
    for i in range(0, len(S), grup_n):
        f = d / f"g{i//grup_n}.json"
        if not f.exists():
            print("YOK", f.name); continue
        m = f.read_text(encoding="utf-8")
        a = json.loads(m[m.index("["):m.rindex("]") + 1])
        for e, k in zip(a, S[i:i + grup_n]):
            src = kaynak(k, 6000)
            o = str(e.get("ornek") or "").strip()
            ko = [x for x in (e.get("kombin") if isinstance(e.get("kombin"), list) else []) if str(x).lower() in src.lower()]
            out.append({"ad": k["ad"], "tur": k["tur"], "kullanim": [temiz(x)[:200] for x in e["kullanim"][:3]], "tuzak": temiz(e["tuzak"])[:220],
                        "token_ipucu": temiz(e["token_ipucu"])[:220], "kombin": [str(x)[:60] for x in ko[:3]],
                        "ornek": (o if o and o in src else (f"Skill {k['ad']}" if "skill" in str(k["tur"]) else k["ad"]))[:220], "model": "haiku-high", "tarih": int(time.time())})
    (d / "haiku.jsonl").write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in out) + "\n", encoding="utf-8")
    print("kart", len(out))


def birlestir(yol):
    """yol'daki jsonl kartlarını usta.jsonl'e ekler/değiştirir (aynı ad → yenisi); eskiyi usta.jsonl.bak'a yedekler."""
    U = oku_usta()
    if USTA.exists():
        (USTA.parent / "usta.jsonl.bak").write_bytes(USTA.read_bytes())
    for l in Path(yol).read_text(encoding="utf-8").splitlines():
        if l.strip():
            c = json.loads(l); U[c["ad"]] = c
    USTA.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in U.values()), encoding="utf-8", newline="\n")
    print("usta", len(U))


def obsidian():
    U = oku_usta()
    KASA.mkdir(parents=True, exist_ok=True)
    sat = ["---", "type: dizin", "status: aktif", "tags: [usta-kart]", "relatedTo: [ustalik-1]", "---", "# Ustalık kartı dizini", f"{len(U)} kart · kaynak docs/usta-kart/usta.jsonl", ""]
    for ad, c in sorted(U.items()):
        sat.append(f"- **{ad}** ({c['tur']}) — {c['kullanim'][0]} · `{c['ornek']}`")
    (KASA / "usta-kart-dizin.md").write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("yazildi", len(U))


if __name__ == "__main__":
    a = sys.argv[1:]
    g = lambda b, v: int(a[a.index(b) + 1]) if b in a else v
    {"say": say, "uret": lambda: uret(g("--n", 50), g("--is", 3)), "dongu": lambda: dongu(g("--hedef", 400), g("--is", 3)), "hakem": lambda: hakem(g("--n", 20)), "obsidian": obsidian, "hazirla": lambda: hazirla(g("--g", 8), g("--n", 50)), "birlestir": lambda: birlestir(a[1]), "isle": lambda: isle(g("--g", 8))}[a[0]]()
