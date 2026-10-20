"""VIDEO-764-4: altın set + karar verici ölçümü + yeniden karar.
python video764_karar2.py altin | ver <altin|heldout> | tutar | olc <verici> <altin|heldout> | yeniden <verici>
verici: cf (cloudflare llama-3.3-70b) · groq (gpt-oss-120b) · haiku"""
import json, os, random, re, subprocess, sys, time
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import video764_kos as V  # noqa: E402

H = V.HAVUZ; OG = V.R / ".kos/kopru/ogren"
ALTIN = OG / "video-764-altin.json"; SAYAC = OG / "video-764-4-sayac.json"; TAHMIN = OG / "video-764-4-tahmin.json"
TAVAN = {"claude": 120, "havuz": 200}
SINIF = ("AL", "UYARLA", "ÖĞREN", "ELE")
TANIM = ("AL: metinde bir aracın/reponun ADI ve repo/linki açık, açık kaynak, doğrudan kurulur (çok nadir).\n"
         "UYARLA: metinde tek somut araç/repo/skill/MCP adı var; kurmadan önce lisans+kurulum raporu ya da uyarlama gerekir. AL'dan şüphe edersen UYARLA.\n"
         "ÖĞREN: kurulacak tek somut araç yok: fikir/pratik/teknik, araç LİSTESİ, zaten kurulu bir şeyin tanıtımı; ya da adlar eksik ama konu Claude Code/ajan/skill — mevcut kural/skill ile karşılaştırılır. ELE ile ÖĞREN arasında şüphede ÖĞREN: konu AI-ajan/kodlama alanındaysa model/araç HABERİ ya da zayıf/içeriksiz görünen anlatım da ELE değil ÖĞREN.\n"
         "ELE: yalnız konu dışı (Claude Code/ajan/geliştirici araçlarıyla ilgisiz), tamamen içeriksiz ya da ücretli SaaS/hizmet reklamı.")
ALTIN_A = ("Bir Claude Code + skill deposu sahibi için video özetlerini sınıflandır. Sınıflar:\n" + TANIM +
           "\n\nHer video için YALNIZ bir JSON dizisi öğesi: {\"id\":..., \"karar\":\"AL|UYARLA|ÖĞREN|ELE\", \"gerekce\":\"≤150 karakter\", \"kanit\":\"özetten birebir tek cümle\"}. Başka metin yazma.\n\n")
ALTIN_B = ("Aşağıdaki videoları sırayla şu sorularla karara bağla (ilk 'evet' kazanır): "
           "(1) Konu AI-ajan/kodlama alanında mı? Evet ise ELE'ye gitme (model/araç haberi ve zayıf anlatım da ÖĞREN'dir). Alan dışı, tamamen içeriksiz ya da ücretli hizmet reklamı ise → ELE. "
           "(2) Metinde ADI açıkça geçen TEK bir araç/repo/skill/MCP var mı ve kurulması düşünülebilir mi? Evet ve repo/link de açıksa açık kaynak-doğrudan kurulur → AL (çok nadir), yoksa → UYARLA. "
           "(3) Aksi halde (fikir, pratik, araç listesi, tanıtım, adı eksik ama Claude Code/ajan konusu) → ÖĞREN.\n"
           "Çıktı: YALNIZ JSON dizisi, öğe: {\"id\":..., \"karar\":\"AL|UYARLA|ÖĞREN|ELE\", \"gerekce\":\"≤150 karakter\", \"kanit\":\"özetten birebir tek cümle\"}.\n\n")
UCUZ = ("Bir Claude Code + skill deposu sahibi için video özetlerini sınıflandır. Sınıflar:\n" + TANIM +
        "\n\nHer video için TEK satır, sekmeyle ayrılmış: id<TAB>KARAR<TAB>güven (yüksek|düşük)<TAB>neden (≤100 karakter). Başka metin yazma.\n\n")


def sayac(k):
    d = json.loads(SAYAC.read_text()) if SAYAC.exists() else {"claude": 0, "havuz": 0}
    d[k] += 1; SAYAC.write_text(json.dumps(d))
    if d[k] > TAVAN[k]:
        raise SystemExit(f"{k} tavanı aşıldı")


def veri():
    t = {}
    for ln in V.TSV.read_text(encoding="utf-8").splitlines()[1:]:
        c = ln.split("\t"); t[c[0]] = c
    d = {}
    for f in V.O.glob("*.meta.json"):
        vid = f.name[:-10]; m = json.loads(f.read_text(encoding="utf-8"))
        d[vid] = dict(id=vid, url=m["url"], baslik=m["baslik"], sure=m["sure"], eski=t.get(m["url"]),
                      ozet=(V.O / (vid + ".ozet.txt")).read_text(encoding="utf-8")[:900])
    return d


def metin(v):
    return "\n\n".join(f"## id={x['id']} · {x['baslik']} · {x['sure']}\n{x['ozet']}" for x in v)


def claude(model, istem):
    sayac("claude")
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}
    p = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json", "--max-turns", "1", "--tools", "", "--setting-sources", ""],
                       input=istem, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300, creationflags=V.NW, cwd=V.O, env=env)
    j = json.loads(p.stdout); r = j.get("result") or ""
    if j.get("is_error") or not r or (len(r) < 200 and re.search(r"(?i)usage limit|limit reached|resets? (at|in)", r)):
        raise RuntimeError("claude " + r[:100])
    return r


def havuz(prov, model, istem):
    e = next(x for x in H.ENT if x.prov == prov and x.model == model)
    for n in range(3):
        sayac("havuz")
        try:
            return H._istek(e, istem, 3000, 120)
        except H.Hata as h:
            print("havuz hata", h.kod, str(h)[:80]); time.sleep(20 * (n + 1))
    raise RuntimeError("havuz düştü")


VERICI = {"cf": lambda s: havuz("cloudflare", "@cf/meta/llama-3.3-70b-instruct-fp8-fast", s),
          "groq": lambda s: havuz("groq", "openai/gpt-oss-120b", s),
          "haiku": lambda s: claude("haiku", s)}


def json_oku(o):
    return json.loads(o[o.index("["):o.rindex("]") + 1])


def tsv_oku(o):
    d = {}
    for ln in o.splitlines():
        c = [x.strip() for x in ln.strip().lstrip("#").split("\t")]
        if len(c) >= 2:
            k = c[1].upper().replace("OGREN", "ÖĞREN")
            if k in SINIF:
                d[c[0].replace("id=", "")] = dict(karar=k, guven=(c[2] if len(c) > 2 else ""), gerekce=(c[3] if len(c) > 3 else ""))
    return d


def tahmin_al():
    return json.loads(TAHMIN.read_text(encoding="utf-8")) if TAHMIN.exists() else {}


def tahmin_yaz(anahtar, p):
    t = tahmin_al(); t.setdefault(anahtar, {}).update(p); TAHMIN.write_text(json.dumps(t, ensure_ascii=False), encoding="utf-8")


def altin():
    d = veri(); r = random.Random(764)
    hk = lambda x: x["eski"] and "[Haiku" in x["eski"][4]  # noqa: E731
    sinif = lambda k: [x for x in d.values() if hk(x) and x["eski"][3] == k]  # noqa: E731
    pilot = [d[i] for i in ("elOexRIdA4c", "DePEr93jXYd", "DeZa_8yjGbp") if i in d]
    secili = {x["id"]: "sınır-pilot" for x in pilot}
    al = [x for x in sinif("AL") if x["id"] not in secili]
    for x in al:
        secili[x["id"]] = "AL"
    zayif = [x for x in sinif("UYARLA") if x["id"] not in secili and not re.search(r"github|repo|http|\.com|\.io", x["ozet"], re.I)]
    repo = [x for x in sinif("ÖĞREN") if x["id"] not in secili and re.search(r"github\.com|repo", x["ozet"], re.I)]
    for x in r.sample(zayif, 5): secili[x["id"]] = "sınır-zayıf-UYARLA"  # pilot 3 video önbellekte meta'sız, o yüzden rastgele sınır
    for x in r.sample(repo, 6): secili[x["id"]] = "sınır-repolu-ÖĞREN"
    for k, n in (("UYARLA", 9), ("ÖĞREN", 9), ("ELE", 8)):
        for x in r.sample([y for y in sinif(k) if y["id"] not in secili], n):
            secili[x["id"]] = k
    kalan = [x["id"] for x in d.values() if hk(x) and x["id"] not in secili]
    held = r.sample(kalan, 30)
    ALTIN.write_text(json.dumps({"altin": secili, "heldout": held}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(secili), Counter(secili.values()), "heldout", len(held))


def set_(ad):
    a = json.loads(ALTIN.read_text(encoding="utf-8")); d = veri()
    ids = list(a["altin"]) if ad == "altin" else a["heldout"]
    return [d[i] for i in ids]


def ver(ad, istem=ALTIN_A, model="claude-sonnet-5-5", n=5, ids=None, anahtar=None):
    s = set_(ad)
    if ids:
        s = [x for x in s if x["id"] in ids]
    for i in range(0, len(s), n):
        b = s[i:i + n]
        p = {o["id"]: o for o in json_oku(claude(model, istem + metin(b)))}
        tahmin_yaz(anahtar or f"sonnet/{ad}", {k: dict(karar=o["karar"].upper().replace("OGREN", "ÖĞREN"), gerekce=o.get("gerekce", ""), kanit=o.get("kanit", "")) for k, o in p.items()})
        print("parti", i // n + 1, len(p), "/", len(b))


def tutar():
    a = json.loads(ALTIN.read_text(encoding="utf-8"))["altin"]; r = random.Random(7)
    ids = r.sample(list(a), 10)
    ver("altin", ALTIN_B, ids=ids, n=5, anahtar="sonnet-B/altin")
    t = tahmin_al(); A = t["sonnet/altin"]; B = t["sonnet-B/altin"]
    fark = [(i, A[i]["karar"], B[i]["karar"]) for i in ids if i in B and A[i]["karar"] != B[i]["karar"]]
    print("tutarlılık", 10 - len(fark), "/10", fark)


def olc(v, ad, n=5):
    s = set_(ad); gold = tahmin_al()[f"sonnet/{ad}"]; p = {}
    for i in range(0, len(s), n):
        p.update(tsv_oku(VERICI[v](UCUZ + metin(s[i:i + n])))); time.sleep(8 if v != "haiku" else 0)  # groq 7k TPM
    tahmin_yaz(f"{v}/{ad}", p)
    ok = sum(1 for x in s if p.get(x["id"], {}).get("karar") == gold[x["id"]]["karar"])
    fark = [(x["id"], gold[x["id"]]["karar"], p.get(x["id"], {}).get("karar")) for x in s if p.get(x["id"], {}).get("karar") != gold[x["id"]]["karar"]]
    print(v, ad, f"{ok}/{len(s)}", "farklar", Counter((g, c) for _, g, c in fark))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"altin": altin, "ver": lambda: ver(a[1]), "tutar": tutar, "olc": lambda: olc(a[1], a[2])}[a[0]]()
