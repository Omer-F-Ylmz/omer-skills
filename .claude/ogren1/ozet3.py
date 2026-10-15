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

ESKI = KOK / ".kos/kopru/ogren/ozet-token-v3b.jsonl"  # d6: A alanları + doğrulanmış B oyları buradan yeniden kullanılır
CIKTI = KOK / ".kos/kopru/ogren/ozet-token-v3c.jsonl"  # d6: v3/v3b kalır, yeniden koşu yeni dosyaya
TAVAN, CAGRI, HAM = 100, 0, None
ETIKET = f"v3c-{int(time.time())}"  # d6: OmniRoute önbellek anahtarına güvenme — etiket kalıcı, her koşuda (yeniden denemede) değişir
KOL_A = [("omni", "openrouter/nvidia/nemotron-3-super-120b-a12b:free"), ("ollama", "gpt-oss:20b-cloud"), ("ollama", "qwen3.5:4b")]
KOL_B1 = [("omni", "openrouter/nvidia/nemotron-3-super-120b-a12b:free")]
KOL_B2 = [("groq", "openai/gpt-oss-120b")]
KOL_B3 = [("omni", "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"), ("ollama", "qwen3.5:4b")]  # d7: gemma :free kalıcı 429 (d6 29×)
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
UYARI = re.compile(r"\bNEVER\b|\bMUST NOT\b|\bDO NOT\b|\bASLA\b|\bYASAK\b")  # d7: başlıksız sınır satırları (vrm-headroom-geri-cagirma)


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
            if a == "ne_yapar" or (a in ILGILI and any(ILGILI[a].search(b) for b in basliklar)) or (a == "sinirlar" and UYARI.search(m)):
                return f"{a} boş, belgede ilgili bölüm var"
        elif len(n(al.get(a, ""))) < 10 or n(al[a]) not in n(m):
            return f"{a} alıntısı belgede yok"
        elif a == "komut" and not komut_mu(o[a], m):
            return "komut olay adı/yönerge, komut değil"
    return None


def komut_mu(k, m):
    """d7: komut = /slash · --bayrak · çağrı( · betik yolu ya da belgede bir kod biriminin (`…`, ``` satırı, girintili satır,
    usage:) BAŞINDA geçen küçük harfli belirteç; olay adı (SessionStart) / yönerge (Use when…) değil"""
    t = re.findall(r"[^\s`'\",;:]+", str(k))
    if any(re.match(r"-{1,2}[a-z]|/[a-z]|\w+\(|\S+\.(py|exe|js|sh|ps1)$", x) for x in t):
        return True
    birim = re.findall(r"`([^`\n]+)`", m) + re.findall(r"(?mi)usage:\s*(.+)$", m) + re.findall(r"(?m)^(?: {2,}|\t)\s*(.+)$", m) + \
        [s for b in re.findall(r"```[^\n]*\n(.*?)```", m, re.S) for s in b.splitlines()]
    bas = {re.sub(r"^[$>\s]+", "", b).split(maxsplit=1)[0] for b in birim if b.strip(" $>")}
    return any(re.fullmatch(r"[a-z][\w.-]{1,}", x) and x in bas for x in t)


def gecerli_b(o, m):
    mek = o.get("mekanizma")
    return (isinstance(mek, list) and 1 <= len(mek) <= 2 and all(x in MEKANIZMA for x in mek)
            and len(n(o.get("kanit", ""))) >= 15 and n(o["kanit"]) in n(m))


def oyla(oylar):
    """d6: tek-kol null ≠ çekişme — herhangi iki geçerli oy kesişirse kesişim kabul, yoksa [] (Claude'a)"""
    g = [o for o in oylar if o]
    return next(([v for v in x if v in y] for i, x in enumerate(g) for y in g[i + 1:] if set(x) & set(y)), [])


def icerik(h):
    """d6: kesik yanıt (finish=length; ollama done_reason=length) her kolda RET"""
    bitis, y = (h.get("done_reason"), h["message"].get("content")) if "message" in h else \
        (h["choices"][0].get("finish_reason"), h["choices"][0]["message"].get("content"))
    if bitis == "length":
        raise ValueError("kesik yanıt (finish=length)")
    y = y or ""
    return json.loads(y[y.index("{"):y.rindex("}") + 1])


def sor(kol, model, istem):
    global CAGRI
    assert CAGRI < TAVAN, "çağrı tavanı"
    CAGRI += 1
    url, h = {"omni": ("http://127.0.0.1:20128/v1/chat/completions", {"authorization": f"Bearer {env_oku('OMNIROUTE_KEY')}"}),
              "groq": ("https://api.groq.com/openai/v1/chat/completions", {"authorization": f"Bearer {env_oku('GROQ_API_KEY')}"}),
              "ollama": ("http://127.0.0.1:11434/api/chat", {})}[kol]
    govde = {"model": model, "max_tokens": 16000, "temperature": 0, "messages": [{"role": "user", "content": istem}]}
    if kol == "ollama":  # d6: /v1 4096 bağlam + düşünme içeriği yiyordu; think:false + num_ctx ile ~6 sn
        govde = {"model": model, "think": False, "stream": False, "options": {"num_ctx": 16384, "temperature": 0},
                 "messages": govde["messages"]}
    q = urllib.request.Request(url, method="POST", headers={"content-type": "application/json", "user-agent": "curl/8.4", **h},
                               data=json.dumps(govde).encode())
    global HAM
    HAM = json.load(urllib.request.urlopen(q, timeout=240))
    return icerik(HAM)


def kos(kollar, sema, ad, m, girdi, dogrula):
    for kol, model in kollar:
        try:
            # etiket: OmniRoute önbellek anahtarı max_tokens'u içermiyor → d4'ün kesik (finish=length) yanıtları dönüyordu
            o = sor(kol, model, f"{sema}\n\nAraç adı: {ad} [{ETIKET}]\n---\n{girdi}")
        except AssertionError:
            sys.exit("TAVAN")
        except Exception as e:
            print(ad, model, "HATA", type(e).__name__, str(e)[:80], flush=True)
            if HAM:  # d5: rtk-desktop teşhisi — ham yanıt gövdesi
                (KOK / f".claude/ogren1/ham-{ad}-{model.split('/')[-1].replace(':', '_')}-{ETIKET}.json").write_text(  # kanıt: üzerine yazılmaz
                    json.dumps(HAM, ensure_ascii=False, indent=1), encoding="utf-8")
            continue
        neden = dogrula(o, m)
        if neden:
            print(ad, model, "RET", neden if isinstance(neden, str) else "", flush=True)
            continue
        return o, model
    return None, None


if __name__ == "__main__":
    import ozet_kaynak  # yollar.tsv + v2 ek kaynakları (ozet.py import'ta koştuğu için ayrı)
    if sys.argv[1:2] == ["--d7"]:  # d7: görülmemiş örneklem (d7-ornek.tsv) ayrı çıktıya, eski satır yok
        ozet_kaynak.D = dict(s.split("\t")[::3] for s in (KOK / ".claude/ogren1/d7-ornek.tsv").read_text(encoding="utf-8").splitlines())
        CIKTI, ESKI, TAVAN, sys.argv[1:] = KOK / ".kos/kopru/ogren/ozet-token-d7.jsonl", KOK / ".kos/kopru/ogren/yok.jsonl", 180, sys.argv[2:]
    if sys.argv[1:] == ["--sina"]:
        g = bolumlu(ozet_kaynak.metin(ozet_kaynak.D["qmd"]))
        assert "Requirements" in g, "qmd Requirements bölümü girdiye girmedi"
        print("qmd: Requirements girdide ✓", len(g))
        sys.exit()
    # çekişmeli satır yeniden denenir (yeni etiket); dosyaya eklenir, okuyan son satırı alır (silme yok)
    bitti = {r["ad"] for r in map(json.loads, CIKTI.read_text(encoding="utf-8").splitlines()) if not r["cekismeli"]} if CIKTI.exists() else set()
    eski = {r["ad"]: r for r in map(json.loads, ESKI.read_text(encoding="utf-8").splitlines())} if ESKI.exists() else {}
    for ad in sys.argv[1:] or list(ozet_kaynak.D):
        if ad in bitti:
            continue
        try:
            m = ozet_kaynak.metin(ozet_kaynak.D[ad])
        except Exception as e:
            print(ad, "KAYNAK-YOK", type(e).__name__, flush=True)
            continue
        t, g = time.time(), bolumlu(m)
        gb = lambda o, m: None if gecerli_b(o, m) else "mekanizma/kanıt geçersiz"
        b1 = b2 = b3 = m3 = None
        if ad in eski:  # d6: v3b satırı — A alanları ve B oyları zaten doğrulanmış, yalnız eksik oy sorulur
            a = eski[ad]
            ma, (m1, m2), kollar = a["model"], a["model_b"][:2], a["mekanizma_kollar"][:2]
        else:
            a, ma = kos(KOL_A, SEMA_A, ad, m, g, gecerli_a)
            if not a:
                continue
            b1, m1 = kos(KOL_B1, SEMA_B, ad, m, g, gb)
            b2, m2 = kos(KOL_B2, SEMA_B, ad, m, g, gb)
            kollar = [(b1 or {}).get("mekanizma"), (b2 or {}).get("mekanizma")]
        if not oyla(kollar):
            b3, m3 = kos(KOL_B3, SEMA_B, ad, m, g, gb)
            kollar.append((b3 or {}).get("mekanizma"))
        ortak, o = oyla(kollar), b1 or b2 or b3 or {}
        a.update(ad=ad, kaynak=ozet_kaynak.D[ad], model=ma, model_b=[m1, m2, m3], mekanizma=ortak, mekanizma_kollar=kollar,
                 mekanizma_gerekce=a.get("mekanizma_gerekce") or o.get("mekanizma_gerekce", ""),
                 kanit=a.get("kanit") or o.get("kanit", ""), cekismeli=not ortak, etiket=ETIKET, sn=round(time.time() - t))
        with CIKTI.open("a", encoding="utf-8") as f:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
        print(ad, ma, m1, m2, "ok", a["mekanizma"], "ÇEKİŞMELİ" if a["cekismeli"] else "", flush=True)
    print("BITTI cagri", CAGRI, flush=True)
