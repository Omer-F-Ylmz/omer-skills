"""ÖĞREN-1 d4 özet hattı v3 (HİBRİT; v2 hakem %17.5 RED). Çıkarım alanları (ne_yapar · komut · girdi_cikti · sinirlar) kol A
(:free) + alan başına belgeden birebir alıntı makineyle doğrulanır; boş/"belirsiz" ilgili başlık belgede varsa ret → sonraki kol.
Yorum alanı `mekanizma`: kol B (başka aile, Groq gpt-oss-120b) BAĞIMSIZ seçer; kesişim varsa kabul, yoksa cekismeli=true → Claude özgünü açar.
metin(): uzun belgede Requirements/Limits/Usage/Options/Caveats bölümleri kırpılmadan girdiye alınır. Tavan en fazla 100 çağrı.
  python -X utf8 .claude/ogren1/ozet3.py [ad ...]   ·   python -X utf8 .claude/ogren1/ozet3.py --sina  (qmd bölüm kanıtı)"""
import json, re, sys, time, urllib.request
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / ".claude/omniroute1"))
from pilot import env_oku  # noqa: E402

CIKTI = KOK / ".kos/kopru/ogren/ozet-token-v3.jsonl"
TAVAN, CAGRI = 100, 0
KOL_A = [("omni", "openrouter/nvidia/nemotron-3-super-120b-a12b:free"), ("ollama", "gpt-oss:20b-cloud"), ("ollama", "qwen3.5:4b")]
KOL_B1 = [("omni", "openrouter/nvidia/nemotron-3-super-120b-a12b:free")]  # iki aile; yedek yok — biri düşerse çekişmeli
KOL_B2 = [("groq", "openai/gpt-oss-120b")]
MEKANIZMA = ["sıkıştırma", "önbellek", "bağlam dışı depolama", "delegasyon", "özetleme", "tur azaltma", "yönlendirme", "ölçüm"]
TANIM = ("Tanımlar: sıkıştırma=aynı içeriği daha az baytla verir; önbellek=önceki sonucu/öneki yeniden kullanır; "
         "bağlam dışı depolama=veriyi bağlam dışında tutar, yalnız sorgu sonucu girer; delegasyon=işi başka süreç/model/ajan yapar; "
         "özetleme=uzun metni kısa özete indirir; tur azaltma=daha az araç çağrısı/tur; yönlendirme=işi daha ucuz araca/modele seçer; "
         "ölçüm=yalnız tüketimi ölçer/raporlar, kendisi tasarruf etmez.")
CIKARIM = ["ne_yapar", "komut", "girdi_cikti", "sinirlar"]
SEMA_A = ("Aşağıdaki araç belgesini oku ve YALNIZ şu JSON nesnesini döndür (Türkçe, alan başına ≤2 cümle, uydurma yok; belgede gerçekten "
          'yoksa "belirsiz"): {"ne_yapar":"","komut":"en tipik 1-2 komut/çağrı","girdi_cikti":"","sinirlar":"gereksinim, sınır, uyarı",'
          '"ne_zaman":"","cakistigi_arac":"belgede adı geçen benzer/çakışan araçlar",'
          '"alinti":{"ne_yapar":"","komut":"","girdi_cikti":"","sinirlar":""}}\n'
          "alinti: her alan için o alanı destekleyen, belgeden BİREBİR kopyalanmış alıntı (≤200 karakter, çevirme, özgün dilde). "
          "Belgede Requirements/Limits/Caveats/Usage/Options bölümü varsa sinirlar ve komut onlardan doldurulur.")
SEMA_B = ("Aşağıdaki araç belgesini oku; bu aracın token/bağlam tasarrufunu NASIL yaptığını seç. YALNIZ şu JSON nesnesini döndür: "
          f'{{"mekanizma":["1-2 değer, YALNIZ şu listeden: {" | ".join(MEKANIZMA)}"],"mekanizma_gerekce":"1 cümle Türkçe",'
          '"kanit":"belgeden BİREBİR alıntı ≤200 karakter, özgün dilde"}\n' + TANIM)
ONEMLI = re.compile(r"requirement|prereq|limit|caveat|known issue|usage|option|command|gereksinim|sınır|uyarı|tuzak|kullanım|seçenek|komut", re.I)
BASLIK = re.compile(r"(?m)^(?=#{1,6} |[A-Z][A-Za-z /-]{2,30}:\s*$)")
ILGILI = {"sinirlar": re.compile(r"requirement|prereq|limit|caveat|known issue|gereksinim|sınır|uyarı|tuzak", re.I),
          "komut": re.compile(r"usage|option|command|kullanım|komut", re.I)}


def bolumlu(m, tavan=12000):
    """baş + önemli başlıklı bölümler (her biri ≤3000) tam; v2'nin düz [:9000] kırpması qmd Requirements'ı (README:569) düşürüyordu"""
    if len(m) <= tavan:
        return m
    on = [p[:3000] for p in BASLIK.split(m)[1:] if ONEMLI.search(p.split("\n", 1)[0])]
    bas = m[:max(tavan - sum(map(len, on)), 3000)]
    return bas + "\n…\n" + "\n".join(p for p in on if p not in bas)


def n(s):
    return " ".join(re.sub(r"[\"'`*_‘’“”]", "", str(s)).split()).lower()


def bos(v):
    return not str(v).strip() or n(v).startswith("belirsiz")


def gecerli_a(o, m):
    """alan başına: boş/belirsiz → ilgili başlık belgede varsa ret; dolu → alıntısı belgede birebir olmalı. Dönüş: ret nedeni ya da None"""
    al = o.get("alinti") if isinstance(o.get("alinti"), dict) else {}
    basliklar = [p.split("\n", 1)[0] for p in BASLIK.split(m)[1:]]
    for a in CIKARIM:
        if bos(o.get(a, "")):
            if a == "ne_yapar" or (a in ILGILI and any(ILGILI[a].search(b) for b in basliklar)):
                return f"{a} boş, belgede ilgili bölüm var"
        elif len(n(al.get(a, ""))) < 10 or n(al[a]) not in n(m):
            return f"{a} alıntısı belgede yok"
    return None


def gecerli_b(o, m):
    mek = o.get("mekanizma")
    return (isinstance(mek, list) and 1 <= len(mek) <= 2 and all(x in MEKANIZMA for x in mek)
            and len(n(o.get("kanit", ""))) >= 15 and n(o["kanit"]) in n(m))


def sor(kol, model, istem):
    global CAGRI
    assert CAGRI < TAVAN, "çağrı tavanı"
    CAGRI += 1
    url, h = {"omni": ("http://127.0.0.1:20128/v1/chat/completions", {"authorization": f"Bearer {env_oku('OMNIROUTE_KEY')}"}),
              "groq": ("https://api.groq.com/openai/v1/chat/completions", {"authorization": f"Bearer {env_oku('GROQ_API_KEY')}"}),
              "ollama": ("http://127.0.0.1:11434/v1/chat/completions", {})}[kol]
    q = urllib.request.Request(url, method="POST", headers={"content-type": "application/json", "user-agent": "curl/8.4", **h},
                               data=json.dumps({"model": model, "max_tokens": 4000, "temperature": 0,
                                                "messages": [{"role": "user", "content": istem}]}).encode())
    y = json.load(urllib.request.urlopen(q, timeout=240))["choices"][0]["message"].get("content") or ""
    return json.loads(y[y.index("{"):y.rindex("}") + 1])


def kos(kollar, sema, ad, m, girdi, dogrula):
    for kol, model in kollar:
        try:
            o = sor(kol, model, f"{sema}\n\nAraç adı: {ad}\n---\n{girdi}")
        except AssertionError:
            sys.exit("TAVAN")
        except Exception as e:
            print(ad, model, "HATA", type(e).__name__, str(e)[:80], flush=True)
            continue
        neden = dogrula(o, m)
        if neden:
            print(ad, model, "RET", neden if isinstance(neden, str) else "", flush=True)
            continue
        return o, model
    return None, None


if __name__ == "__main__":
    import ozet_kaynak  # yollar.tsv + v2 ek kaynakları (ozet.py import'ta koştuğu için ayrı)
    # d4 kanıtı: v2 qmd girdisi `qmd --help` (5.6 KB, kırpılmamış) — sınırlar README'de (Requirements); hakem README'ye baktı
    ozet_kaynak.D["qmd"] = str(Path(env_oku("APPDATA")).parent / "Local/Microsoft/WinGet/Packages"
                               / "OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node_modules/@tobilu/qmd/README.md")
    if sys.argv[1:] == ["--sina"]:
        g = bolumlu(ozet_kaynak.metin(ozet_kaynak.D["qmd"]))
        assert "Requirements" in g, "qmd Requirements bölümü girdiye girmedi"
        print("qmd: Requirements girdide ✓", len(g))
        sys.exit()
    bitti = {json.loads(s)["ad"] for s in CIKTI.read_text(encoding="utf-8").splitlines()} if CIKTI.exists() else set()
    for ad in sys.argv[1:] or list(ozet_kaynak.D):
        if ad in bitti:
            continue
        try:
            m = ozet_kaynak.metin(ozet_kaynak.D[ad])
        except Exception as e:
            print(ad, "KAYNAK-YOK", type(e).__name__, flush=True)
            continue
        t, g = time.time(), bolumlu(m)
        a, ma = kos(KOL_A, SEMA_A, ad, m, g, gecerli_a)
        if not a:
            continue
        gb = lambda o, m: None if gecerli_b(o, m) else "mekanizma/kanıt geçersiz"
        b1, m1 = kos(KOL_B1, SEMA_B, ad, m, g, gb)
        b2, m2 = kos(KOL_B2, SEMA_B, ad, m, g, gb)
        ortak = [x for x in (b1 or {}).get("mekanizma", []) if x in (b2 or {}).get("mekanizma", [])]
        a.update(ad=ad, kaynak=ozet_kaynak.D[ad], model=ma, model_b=[m1, m2], mekanizma=ortak,
                 mekanizma_kollar=[(b1 or {}).get("mekanizma"), (b2 or {}).get("mekanizma")],
                 mekanizma_gerekce=(b1 or {}).get("mekanizma_gerekce", ""), kanit=(b1 or b2 or {}).get("kanit", ""),
                 cekismeli=not ortak, sn=round(time.time() - t))
        with CIKTI.open("a", encoding="utf-8") as f:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
        print(ad, ma, m1, m2, "ok", a["mekanizma"], "ÇEKİŞMELİ" if a["cekismeli"] else "", flush=True)
    print("BITTI cagri", CAGRI, flush=True)
