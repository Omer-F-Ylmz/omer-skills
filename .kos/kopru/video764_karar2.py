"""VIDEO-764-4: altın set + karar verici ölçümü + yeniden karar.
python video764_karar2.py altin | ver <altin|heldout> | tutar | olc <verici> <altin|heldout> | yeniden <verici>
verici: cf (cloudflare llama-3.3-70b) · groq (gpt-oss-120b) · haiku"""
import json, os, random, re, subprocess, sys, time
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import video764_kos as V  # noqa: E402

H = V.HAVUZ; OG = V.R / ".kos/kopru/ogren"
ALTIN = OG / "video-764-altin.json"; V2 = OG / "video-764-v2.tsv"; SAYAC = OG / "video-764-4-sayac.json"; TAHMIN = OG / "video-764-4-tahmin.json"
TAVAN = {"claude": 220, "havuz": 300, "tek": 60}  # tek: melez kipte tek-tek yeniden karar (claude içinde sayılır)
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


KUL = {"usd": 0.0, "tok": 0}  # bu süreçteki claude -p toplamı


def sayac(k):
    d = json.loads(SAYAC.read_text()) if SAYAC.exists() else {}
    d[k] = d.get(k, 0) + 1; SAYAC.write_text(json.dumps(d))
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
    u = j.get("usage") or {}; KUL["usd"] += j.get("total_cost_usd") or 0
    KUL["tok"] += sum(u.get(k) or 0 for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
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
          "haiku": lambda s: claude("haiku", s),
          "or-super": lambda s: havuz("openrouter", "nvidia/nemotron-3-super-120b-a12b:free", s),
          "or-ultra": lambda s: havuz("openrouter", "nvidia/nemotron-3-ultra-550b-a55b:free", s),
          "or-gemma": lambda s: havuz("openrouter", "google/gemma-4-31b-it:free", s),
          "or-minimax": lambda s: havuz("openrouter", "minimax/minimax-m3.1-flash:free", s)}
BEKLE = {"haiku": 0, "groq": 20, "or-super": 4, "or-ultra": 4, "or-gemma": 4, "or-minimax": 4}  # groq 7k TPM


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


def kapi(n=15):
    """held-out 30: tek-tek (altın kriter) + toplu iki koşu → uyum ≥29/30, tutarlılık ≥%93"""
    ver("heldout", n=1, anahtar="sonnet/heldout"); ver("heldout", n=n, anahtar="sonnet-toplu1/heldout"); ver("heldout", n=n, anahtar="sonnet-toplu2/heldout")
    t = tahmin_al(); g, a, b = (t[k] for k in ("sonnet/heldout", "sonnet-toplu1/heldout", "sonnet-toplu2/heldout"))
    print("uyum", sum(g[i]["karar"] == a[i]["karar"] for i in g if i in a), "/30 ikinci", sum(g[i]["karar"] == b[i]["karar"] for i in g if i in b), "tutarlılık", sum(a[i]["karar"] == b[i]["karar"] for i in a if i in b), "/30")
    print([(i, g[i]["karar"], a.get(i, {}).get("karar"), b.get(i, {}).get("karar")) for i in g if not g[i]["karar"] == a.get(i, {}).get("karar") == b.get(i, {}).get("karar")])


def yeniden(n=15, cagri=None, ids=None, melez=False):
    """karar-v2'si olmayan her videoyu (Haiku ön-karar etiketli ya da yeni/ek-50) Sonnet toplu kipte karara bağlar; eski karar satırı korunur, V2'ye eklenir.
    melez: toplu istem `guven` da ister; guven=dusuk ve ELE kararlılar tek-tek (ALTIN_A, n=1) yeniden karara bağlanır, tek-tek tavanı TAVAN['tek']."""
    cagri = cagri or (lambda s: claude("claude-sonnet-5-5", s))
    istem = ALTIN_A.replace('"kanit":"özetten birebir tek cümle"}', '"kanit":"özetten birebir tek cümle", "guven":"yuksek|dusuk"}') if melez else ALTIN_A
    yapilan = {ln.split("\t")[0] for ln in V2.read_text(encoding="utf-8").splitlines()} if V2.exists() else set()
    bekle = [x for x in veri().values() if x["id"] not in yapilan and (not ids or x["id"] in ids)]
    duz = lambda s: str(s).replace("\t", " ").replace("\n", " ")  # noqa: E731
    for i in range(0, len(bekle), n):
        b = bekle[i:i + n]; p = {o["id"]: o for o in json_oku(cagri(istem + metin(b)))}
        sat = [] if V2.exists() else ["id\tlink\tbaşlık\teski karar\tkarar-v2\tgerekçe\tkanıt\tetiket\työntem"]
        norm = lambda o: o and o.get("karar", "").upper().replace("OGREN", "ÖĞREN")  # noqa: E731
        yontem = {x["id"]: "toplu" for x in b}
        if melez:  # düşük güven ya da ELE → tek-tek; tavan dolunca toplu karar kalır, "toplu-tavan" etiketlenir
            dusuk = lambda x: str(p[x["id"]].get("guven", "")).lower().startswith("d")  # noqa: E731 (dusuk/düşük)
            sec = [x for x in b if p.get(x["id"]) and norm(p[x["id"]]) in SINIF and (dusuk(x) or norm(p[x["id"]]) == "ELE")]
            say = lambda: json.loads(SAYAC.read_text()).get("tek", 0) if SAYAC.exists() else 0  # noqa: E731
            kota = -(-(TAVAN["tek"] - say()) // -(-(len(bekle) - i) // n))  # kalan tavan kalan partilere yayılır (ilk partiler tavanı tüketmesin)
            for j, x in enumerate(sorted(sec, key=lambda x: not dusuk(x))):
                if j >= kota or say() >= TAVAN["tek"]:
                    yontem[x["id"]] = "toplu-tavan"; continue
                sayac("tek")
                try:
                    t = {o["id"]: o for o in json_oku(cagri(ALTIN_A + metin([x])))}.get(x["id"])
                except Exception as e:  # tek-tek düşerse toplu karar kalır
                    print("tek-tek hata", x["id"], str(e)[:80]); continue
                if norm(t) in SINIF:
                    p[x["id"]] = t; yontem[x["id"]] = "tek"
        for x in b:
            o = p.get(x["id"])  # yanıtta eksik video yazılmaz → sonraki koşuda yeniden denenir
            k = norm(o)
            if k in SINIF:
                sat.append("\t".join((x["id"], x["url"], duz(x["baslik"]), x["eski"][3] if x["eski"] else "", k, duz(o.get("gerekce", "")), duz(o.get("kanit", "")), "[karar-v2]", yontem[x["id"]])))
        if sat:
            with V2.open("a", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(sat) + "\n")
        print("parti", i // n + 1, len(p), "/", len(b), f"$ {KUL['usd']:.2f} tok {KUL['tok']}", flush=True)


def olc(v, ad, n=5, ilk=0):
    s = set_(ad); gold = tahmin_al()[f"sonnet/{ad}"]; p = {}
    if ilk:
        s = random.Random(5).sample(s, ilk)  # altın sette sınıf karışık rastgele alt küme
    for i in range(0, len(s), n):
        p.update(tsv_oku(VERICI[v](UCUZ + metin(s[i:i + n])))); time.sleep(BEKLE.get(v, 8))
    tahmin_yaz(f"{v}/{ad}" + (f"-ilk{ilk}" if ilk else ""), p)
    ok = sum(1 for x in s if p.get(x["id"], {}).get("karar") == gold[x["id"]]["karar"])
    fark = [(x["id"], gold[x["id"]]["karar"], p.get(x["id"], {}).get("karar")) for x in s if p.get(x["id"], {}).get("karar") != gold[x["id"]]["karar"]]
    print(v, ad, f"{ok}/{len(s)}", "farklar", Counter((g, c) for _, g, c in fark))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["ver"] and "--verici" in a:  # ver --verici sonnet [--melez] [--toplu N]
        assert a[a.index("--verici") + 1] == "sonnet"; sys.exit(yeniden(int(a[a.index("--toplu") + 1]) if "--toplu" in a else 15, melez="--melez" in a))
    {"altin": altin, "ver": lambda: ver(a[1]), "tutar": tutar, "kapi": kapi, "olc": lambda: olc(a[1], a[2], ilk=int(a[3]) if len(a) > 3 else 0)}[a[0]]()
