"""ÖĞREN-3 (ajan-orkestrasyon) d1: ÖĞREN-1 d14 hattı (Claude yazar + sert denetim + kaynak çözümü) aynen; tek fark
kapalı liste: token "mekanizma" yerine orkestrasyon "rol" (ozet3.MEKANIZMA yerinde değiştirilir → gecerli_b aynı kodla denetler).
  python -X utf8 .claude/ogren3/o3.py hazirla     → kaynak çöz (o3-kaynak/), o3-kalem.tsv, o3-paket-NN.md (~15 kalem)
  python -X utf8 .claude/ogren3/o3.py birlestir   → ozet-ajan-o3.jsonl + hakem-o3.jsonl, RET/UYARI listesi"""
import collections, json, random, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "ogren1"))
import ozet3  # noqa: E402
from d13 import A, O, sert  # noqa: E402
from d14 import metin  # noqa: E402
from ozet3 import BASLIK, adlari  # noqa: E402
from son import oku  # noqa: E402
from komut import doldur  # noqa: E402

ROL = ["orkestrasyon", "delegasyon", "paralel dağıtım", "planlama", "zamanlama", "izleme", "bellek", "yönlendirme",
       "koruma", "model sağlayıcı", "ajan tanımı", "inceleme", "orkestrasyon-dışı"]
ozet3.MEKANIZMA[:] = ROL
B = Path(__file__).parent
K = B / "o3-kaynak"
PARTI = 15


def kalemler():
    """kopya grubu başına tek kalem (kanonik öncelikli); aday ve model hariç (model → modeller())"""
    t = [json.loads(x) for x in (O / "katalog-son.jsonl").read_text(encoding="utf-8").splitlines()]
    g = {}
    for r in t:
        if r["kategori_son"] == "ajan-orkestrasyon" and r["tur"] not in ("aday", "model"):
            k = r.get("kopya_grubu") or r["id"]
            if k not in g or r["kanonik"] == r["id"]:
                g[k] = r
    return list(g.values())


def dosya(r):
    return K / (r["id"] + "_" + re.sub(r"[^\w.-]", "_", r["ad"])[:60] + ".txt")


def hazirla():
    K.mkdir(exist_ok=True)
    satir, say = [], collections.Counter()
    for r in kalemler():
        try:
            if r["yol"].lower().endswith(".exe"):  # ikili dosya metin değil: kaynak = --help çıktısı
                h = subprocess.run([r["yol"], "--help"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                m = f"=== {r['yol']} --help ===\n{h.stdout}{h.stderr}"
            else:
                m = metin(r["ad"], r["yol"])
        except Exception as e:  # noqa: BLE001
            m, say[f"açılmıyor {type(e).__name__}"] = "", say[f"açılmıyor {type(e).__name__}"] + 1
        dosya(r).write_text(m, encoding="utf-8")
        satir.append([r["id"], r["ad"], r["tur"], r["katman"], r["yol"], str(len(m.splitlines()))])
    satir.sort(key=lambda s: -int(s[5]))
    (B / "o3-kalem.tsv").write_text("".join("\t".join(s) + "\n" for s in satir), encoding="utf-8")
    partiler = []
    for kat in ("A", "B", "C"):  # A partileri önce (oturum çağrı tavanında çekirdek önce yazılır)
        ks = [s for s in satir if s[3] == kat]
        n = -(-len(ks) // PARTI)
        partiler += [ks[i::n] for i in range(n)]  # büyükten küçüğe sıralı listeden dönüşümlü dağıtım → satır yükü dengeli
    for i, ps in enumerate(partiler):
        parca = []
        for s in ps:
            p = K / dosya({"id": s[0], "ad": s[1]}).name
            m = p.read_text(encoding="utf-8")
            an = sorted(adlari(s[1], s[4]))
            parca += [f"## {s[1]}", f"id: {s[0]} · tür: {s[2]} · katman: {s[3]} · kaynak: {p} (özgün: {s[4]}) · {s[5]} satır · araç adları ({len(an)}): {' · '.join(an[:30])}",
                      "BAŞLIKLAR: " + " · ".join(x.split("\n", 1)[0].strip()[:60] for x in BASLIK.split(m)[1:])[:1500], ""]
        (B / f"o3-paket-{i + 1:02d}.md").write_text("\n".join(parca), encoding="utf-8")
    assert sum(map(len, partiler)) == len(satir)
    print(f"kalem {len(satir)} · parti {len(partiler)} (A {sum(p[0][3] == 'A' for p in partiler)}) · satır toplam {sum(int(s[5]) for s in satir)} · boş {sum(s[5] == '0' for s in satir)} · {dict(say)}")


G2 = ("ajan-orkestrasyon", "araştırma", "bilim", "diğer")
ODAK = set("""cc-kopru OmniRoute superpowers gstack subagent-driven-development dispatching-parallel-agents plan-kur is-akisi ajan-getir
brave-search context7 context7-cli context7-mcp mcp-fetch agent-reach deep-research find-docs awesome-rehber yetenek-getir video-tarama graphify
ecc ecc-ml-bilim-saglik-paket davila7-scientific-paket-1 davila7-scientific-paket-2 kdense-scientific-paket-1 kdense-scientific-paket-2
mslearn arxiv last30days claude-mem""".split())
MUDUR = ("departman-surec-ajan-arac", "departman-surec-plan", "departman-arastirma-ogrenme")


def a2():
    """d2 (★ 11:27 C): G2 A ≤150 = d1'de yazılmış 30 + kullanım sırası + Odak + müdür skill'de anılan; geri kalan kanonik → B betik kartı"""
    t = [json.loads(x) for x in (O / "katalog-son.jsonl").read_text(encoding="utf-8").splitlines()]
    k = [r for r in t if r["kategori_son"] in G2 and r["tur"] != "aday" and r["kanonik"] == r["id"] and r["yol"]]  # yol "" = PATH'te yok, kurulu değil
    yazili = {i for p in ("01", "02") for i in re.findall(r"^id: (\S+)", (B / f"o3-paket-{p}.md").read_text(encoding="utf-8"), re.M)}
    mudur = "\n".join((Path("skills") / d / "SKILL.md").read_text(encoding="utf-8") for d in MUDUR)
    anilan = lambda ad: len(ad) >= 4 and re.search(rf"(?<![\w-]){re.escape(ad)}(?![\w-])", mudur)
    aday = [r for r in k if r["tur"] != "model" and (r["id"] in yazili or r["kullanim_30g"] > 0 or r["ad"] in ODAK or r["ad"].startswith("phoenix-") or anilan(r["ad"]))]
    aday.sort(key=lambda r: (r["id"] not in yazili, -r["kullanim_30g"], r["ad"] not in ODAK, r["ad"]))
    a = aday[:150]
    sec = {r["id"] for r in a}
    kb = [r for r in k if r["id"] not in sec]
    # docs/atlas/kart.jsonl B şeması (G1 ile aynı): komut = çağrı adı, kanit = özgün yol; uydurma alan yok
    (O / "kart-b-g2.jsonl").write_text("".join(json.dumps({"ad": r["ad"], "ne": r["aciklama"], "komut": r["ad"], "kanit": r["yol"], "kategori": r["kategori_son"],
                                                          "tur": r["tur"], "katman": "B"}, ensure_ascii=False) + "\n" for r in kb), encoding="utf-8")
    satir = []
    for r in a:
        p = dosya(r)
        cmd = r["yol"].lower().endswith((".exe", ".cmd"))  # .CMD npm kabuğu da ikili gibi: kaynak = --help
        if not p.exists() or cmd and not p.read_text(encoding="utf-8").startswith("==="):  # d1 hazirla yalnız ajan-orkestrasyon'u çözdü
            try:
                if cmd:
                    h = subprocess.run([r["yol"], "--help"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                    p.write_text(f"=== {r['yol']} --help ===\n{h.stdout}{h.stderr}", encoding="utf-8")
                else:
                    p.write_text(metin(r["ad"], r["yol"]), encoding="utf-8")
            except (OSError, subprocess.SubprocessError):  # yolu kaybolan kaynak → kaynaksız
                p.write_text("", encoding="utf-8")
        satir.append([r["id"], r["ad"], r["tur"], "A", r["yol"], str(len(p.read_text(encoding="utf-8").splitlines())), r["kategori_son"], str(r["kullanim_30g"])])
    (B / "o3-kalem.tsv").write_text("".join("\t".join(s) + "\n" for s in satir), encoding="utf-8")
    # 6 büyük kaynak d1'de parçalı tam okunmadı → yeniden yazılır (o3-yazar-aNN, birlestir'de 01/02'nin üstüne yazar)
    buyuk = {"ecc", "office-hours", "claude-api", "plan-ceo-review", "OmniRoute", "setup-deploy"}
    yeni = sorted((s for s in satir if s[0] not in yazili or s[1] in buyuk), key=lambda s: -int(s[5]))
    var = sorted(B.glob("o3-paket-a*.md"))
    if var:  # yazım başladıysa paketler değişmez; yeni giren + kaynağı --help'e dönen kalemler ek partiye
        once = {i for p in var for i in re.findall(r"^id: (\S+)", p.read_text(encoding="utf-8"), re.M)}
        yeni = [s for s in yeni if s[0] not in once or s[4].lower().endswith(".cmd")]
    n, i0 = -(-len(yeni) // PARTI), len(var)
    for i in range(i0, i0 + n):
        parca = []
        for s in yeni[i - i0::n]:
            p, m = dosya({"id": s[0], "ad": s[1]}), dosya({"id": s[0], "ad": s[1]}).read_text(encoding="utf-8")
            an = sorted(adlari(s[1], s[4]))
            parca += [f"## {s[1]}", f"id: {s[0]} · tür: {s[2]} · katman: A · kategori: {s[6]} · kaynak: {p} (özgün: {s[4]}) · {s[5]} satır · araç adları ({len(an)}): {' · '.join(an[:30])}",
                      "BAŞLIKLAR: " + " · ".join(x.split("\n", 1)[0].strip()[:60] for x in BASLIK.split(m)[1:])[:1500], ""]
        (B / f"o3-paket-a{i + 1:02d}.md").write_text("\n".join(parca), encoding="utf-8")
    js = [s for s in satir if s[4].lower().endswith(".json") and Path(s[4]).name not in ("hooks.json", "settings.json", ".claude.json")]
    print(f"G2 kanonik {len(k)} · A aday {len(aday)} → A {len(a)} ({collections.Counter(s[6] for s in satir)}) · B {len(kb)} "
          f"(model {sum(r['tur'] == 'model' for r in kb)}) · kopya dışı {sum(r['kategori_son'] in G2 and r['tur'] != 'aday' and r['kanonik'] != r['id'] for r in t)}"
          f" · yeni yazım {len(yeni)} → parti {n} · boş {sum(s[5] == '0' for s in satir)} · .json kaynak {[(s[1], Path(s[4]).name) for s in js]}")


def birlestir():
    c = {}
    for p in sorted(B.glob("o3-yazar-*.jsonl")):  # aynı ad farklı kopya gruplarında geçer → yazar satırı kendi partisinin id'sine bağlanır
        ids = dict(re.findall(r"^## (.+)\nid: (\S+)", (B / p.name.replace("yazar", "paket").replace(".jsonl", ".md")).read_text(encoding="utf-8"), re.M))
        c.update({ids[ad]: y for ad, y in oku(p).items() if ad in ids})
    son, ret = {}, {}
    satirlar = [x.split("\t") for x in (B / "o3-kalem.tsv").read_text(encoding="utf-8").splitlines()]
    yazili_ad = {s[1] for s in satirlar if s[0] in c}
    for s in satirlar:
        i, ad, tur, katman, yol = s[:5]
        if i not in c and ad in yazili_ad:  # d3: aynı adlı zip sürüm kopyası → kanonik tek kart (kopya sayılır, RET değil)
            print("KOPYA", i, ad, yol[-50:], sep="\t")
            continue
        if i not in c:
            ret[i] = "yazar satırı yok"
            continue
        p = K / dosya({"id": i, "ad": ad}).name
        m, y = p.read_text(encoding="utf-8"), c[i]
        r = {"ad": ad, "id": i, "tur": tur, "katman": katman, "kaynak": str(p), "ozgun": yol, **{a: y[a]["deger"] for a in A},
             "alinti": {a: y[a].get("alinti", "") for a in A}, "ne_zaman": y.get("ne_zaman", ""), "mekanizma": y["rol"], "kanit": y.get("kanit", ""),
             "dogrulandi": "claude-yazar"}
        r = doldur(r, m)  # d3: komut belirsiz → kaynaktaki birebir satır (betik)
        neden, r["uyari"] = sert(r, m, adlari(ad, yol))
        if neden:
            ret[i] = neden
        son[i] = r
    for i, h in ret.items():
        if h != "yazar satırı yok":
            print("RET", i, son[i]["ad"], h, sep="\t")
    (O / "ozet-ajan-o3.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in son.values()), encoding="utf-8")
    (O / "hakem-o3.jsonl").write_text("".join(json.dumps({k: r[k] for k in ["ad", "kaynak", "ozgun"] + A + ["mekanizma"]}, ensure_ascii=False) + "\n"
                                             for i, r in son.items() if i not in ret), encoding="utf-8")
    print(f"son {len(son)} · RET {len(ret)} (yazar yok {sum(v == 'yazar satırı yok' for v in ret.values())}) · UYARI {sum(len(r['uyari']) for r in son.values())}"
          f" · rol {collections.Counter(x for r in son.values() for x in ([r['mekanizma']] if isinstance(r['mekanizma'], str) else r['mekanizma'])).most_common()}")


def kapi(tohum):
    """iki yeni tohum (★ 11:27): yalnız A'dan, sert denetimden geçmiş kalemlerden 25 kalem × 4 alan = 100 alan"""
    h = [json.loads(x) for x in (O / "hakem-o3.jsonl").read_text(encoding="utf-8").splitlines()]
    sec = random.Random(int(tohum)).sample(h, 25)
    (O / f"hakem-o3-t{tohum}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sec), encoding="utf-8")
    print(tohum, [r["ad"] for r in sec])


def puan(tohum):
    """iki kör hakem: ikisi D → D, ikisi Y → Y, ayrışan → AYRI (Claude kaynağa bakıp karar verir, karar.tsv: ad<TAB>alan<TAB>D|Y)"""
    alan = A + ["mekanizma"]
    hs = [{r["ad"]: r for r in map(json.loads, (B / f"hakem-t{tohum}-{n}.jsonl").read_text(encoding="utf-8").splitlines())} for n in (1, 2)
          if (B / f"hakem-t{tohum}-{n}.jsonl").exists()]
    hs += hs[:1] * (2 - len(hs))  # tohum başı tek hakem: Y'ler karar-t<tohum>.tsv'de Claude kaynağa bakıp onaylar/reddeder
    assert hs, "hakem dosyası yok"
    adlar = [json.loads(x)["ad"] for x in (O / f"hakem-o3-t{tohum}.jsonl").read_text(encoding="utf-8").splitlines()]
    assert all(h.keys() == set(adlar) for h in hs), "hakem satırı eksik"
    kp = B / f"karar-t{tohum}.tsv"
    kr = {(a, b): c for a, b, c in (s.split("\t") for s in kp.read_text(encoding="utf-8").splitlines())} if kp.exists() else {}
    y = []
    for ad in adlar:
        for a in alan:
            k = {hs[0][ad][a], hs[1][ad][a]}
            v = k.pop() if len(k) == 1 else kr.get((ad, a), "AYRI")
            if v != "D":
                y.append((ad, a, v))
                print(v, ad, a, hs[0][ad].get("gerekce", {}).get(a, ""), hs[1][ad].get("gerekce", {}).get(a, ""), sep="\t")
    n = len(adlar) * len(alan)
    print(f"tohum {tohum} · alan {n} · Y {sum(v == 'Y' for *_, v in y)} · AYRI {sum(v == 'AYRI' for *_, v in y)} · doğru %{100 * (n - len(y)) / n:.1f}")


if __name__ == "__main__":
    {"hazirla": hazirla, "a2": a2, "birlestir": birlestir, "kapi": lambda: kapi(sys.argv[2]), "puan": lambda: puan(sys.argv[2])}[sys.argv[1]]()
