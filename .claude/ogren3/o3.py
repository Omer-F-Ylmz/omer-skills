"""ÖĞREN-3 (ajan-orkestrasyon) d1: ÖĞREN-1 d14 hattı (Claude yazar + sert denetim + kaynak çözümü) aynen; tek fark
kapalı liste: token "mekanizma" yerine orkestrasyon "rol" (ozet3.MEKANIZMA yerinde değiştirilir → gecerli_b aynı kodla denetler).
  python -X utf8 .claude/ogren3/o3.py hazirla     → kaynak çöz (o3-kaynak/), o3-kalem.tsv, o3-paket-NN.md (~15 kalem)
  python -X utf8 .claude/ogren3/o3.py birlestir   → ozet-ajan-o3.jsonl + hakem-o3.jsonl, RET/UYARI listesi"""
import collections, json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "ogren1"))
import ozet3  # noqa: E402
from d13 import A, O, sert  # noqa: E402
from d14 import metin  # noqa: E402
from ozet3 import BASLIK, adlari  # noqa: E402
from son import oku  # noqa: E402

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


def birlestir():
    c = {}
    for p in sorted(B.glob("o3-yazar-*.jsonl")):  # aynı ad farklı kopya gruplarında geçer → yazar satırı kendi partisinin id'sine bağlanır
        ids = dict(re.findall(r"^## (.+)\nid: (\S+)", (B / p.name.replace("yazar", "paket").replace(".jsonl", ".md")).read_text(encoding="utf-8"), re.M))
        c.update({ids[ad]: y for ad, y in oku(p).items() if ad in ids})
    son, ret = {}, {}
    for s in (x.split("\t") for x in (B / "o3-kalem.tsv").read_text(encoding="utf-8").splitlines()):
        i, ad, tur, katman, yol = s[:5]
        if i not in c:
            ret[i] = "yazar satırı yok"
            continue
        p = K / dosya({"id": i, "ad": ad}).name
        m, y = p.read_text(encoding="utf-8"), c[i]
        r = {"ad": ad, "id": i, "tur": tur, "katman": katman, "kaynak": str(p), "ozgun": yol, **{a: y[a]["deger"] for a in A},
             "alinti": {a: y[a].get("alinti", "") for a in A}, "ne_zaman": y.get("ne_zaman", ""), "mekanizma": y["rol"], "kanit": y.get("kanit", ""),
             "dogrulandi": "claude-yazar"}
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
          f" · rol {collections.Counter(x for r in son.values() for x in r['mekanizma']).most_common()}")


if __name__ == "__main__":
    {"hazirla": hazirla, "birlestir": birlestir}[sys.argv[1]]()
