"""ÖĞREN-0b: katalog.jsonl'yi bozmadan katalog-son.jsonl + ozet-0b.md + modeller.tsv üretir.
  python -X utf8 katalog_son.py sinifla   -> düşük güvenli kalemler 2 ücretsiz model oyu (+3. hakem), sinif-onbellek.jsonl (sürdürülebilir)
  python -X utf8 katalog_son.py kullanim  -> son 30 gün transkript sayımı -> kullanim-30g.json (yalnız sayım)
  python -X utf8 katalog_son.py ornek     -> elle etiket için rastgele 40 kalem (ad + açıklama)
  python -X utf8 katalog_son.py son       -> katalog-son.jsonl + ozet-0b.md + modeller.tsv (ağ yok)
Ücretli çağrı 0: yalnız OmniRoute openrouter :free + ollama. Env değeri yazdırılmaz."""
import hashlib, json, random, re, sys, threading, time, urllib.request, zipfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
BURASI = Path(__file__).resolve().parent
REPO = BURASI.parents[2]
sys.path.insert(0, str(BURASI))
from katalog import KATEGORI, KAT_RE, norm  # noqa: E402

KATLAR = [k for k, _ in KATEGORI] + ["diğer"]
ONBELLEK = BURASI / "sinif-onbellek.jsonl"
TAVAN = 320  # en fazla 320 model çağrısı (tüm kollar toplamı)
PARTI = 40
OY1 = "openrouter/nvidia/nemotron-3-super-120b-a12b:free"
OY2 = ("openrouter/google/gemma-4-31b-it:free", "openrouter/google/gemma-4-26b-a4b-it:free", "gemma4:cloud")  # son yedek ollama, aynı aile
HAKEM = "gpt-oss:20b-cloud"  # ollama
# özet/hafıza/yönlendirme gibi kural kaçaklarını yüksek güvenli olsa da yeniden oylat
TOKEN_IPUCU = re.compile(r"compress|cache|context|summar|\bcost|routing|router|memor|hafıza|özet|maliyet|yönlendir|sıkıştır|"
                         r"önbellek|bağlam|token|jeton|budget|bütçe", re.I)
TANIM = """token: LLM jeton/maliyet azaltma — sıkıştırma, önbellek, bağlam penceresi yönetimi, bağlamı küçülten özetleme, kullanım/maliyet ölçümü, model yönlendirme (router), bağlam tasarrufu için hafıza
frontend-tasarım: UI/UX, web arayüzü, CSS, React, animasyon, tipografi, web sitesi
video-medya: video, ses, müzik, görsel/resim üretme-düzenleme, ffmpeg, transkripsiyon
3d: Blender, three.js, 3B model, mesh, shader
test-qa: test, QA, kod inceleme (code review), lint, doğrulama, hata ayıklama
güvenlik: güvenlik açığı, pentest, gizli anahtar taraması, saldırı/savunma
backend-dotnet: backend, API, sunucu, .NET/C#, deploy, CI/CD, git, devops, bulut, altyapı
veri-db: veritabanı, SQL, veri analizi, ETL, tablo verisi
ajan-orkestrasyon: AI ajanları, subagent, MCP, Claude Code skill/plugin/hook yönetimi, çoklu ajan, iş akışı, prompt mühendisliği, LLM entegrasyonu
belge: doküman, PDF/Office, rapor, yazı, sunum, not alma, dokümantasyon
araştırma: web arama, scraping, tarayıcı otomasyonu, bilgi toplama
oyun-mod: oyun, oyun modu, Minecraft, Unity, Godot
pazarlama: pazarlama, satış, SEO, sosyal medya, marka, e-posta, iş stratejisi, ürün yönetimi
bilim: bilim, matematik, biyoloji, kimya, istatistik, akademik makale
diğer: hiçbiri"""
ISTEM = ("Her yazılım aracını (Claude Code skill/agent/komut/plugin/hook/mcp/cli/repo) TAM OLARAK bir kategoriye ata. Kategoriler:\n"
         + TANIM + "\nAracın ASIL işine bak; yalnız 'Claude' ya da 'agent' sözcüğü geçiyor diye ajan-orkestrasyon seçme. "
         "YALNIZ JSON nesnesi döndür, açıklama yazma: {\"<no>\": \"<kategori>\", ...} — her no için bir kategori, kategori adı listedekiyle birebir.\n\nAraçlar:\n")


def kurulu(k):
    return k["tur"] not in ("aday", "model") and k["kaynak"] != "cli:yok"


def kural_guven(k):
    p = sorted((len(r.findall(f"{k['ad']} {k['aciklama']}")) for _, r in KAT_RE), reverse=True)
    return "yüksek" if p[0] >= 2 and p[0] > p[1] else "düşük"


def anahtar(k):
    return f"{k['tur']}|{norm(k['ad'])}|{k['aciklama'][:150]}"


def oylanacak(k):
    # elle örnekte kuralın "yüksek" dediği kalemler de ıskaladı (sec-injection -> veri-db): tüm kurulu tekiller oylanır
    return kurulu(k)


def karar(oylar, kural):
    """oylar: {model: kategori}; çoğunluk -> (kategori, güven)."""
    c = Counter(v for v in oylar.values() if v in KATLAR)
    if not c:
        return kural, "kural"
    (en, n), = c.most_common(1)
    if n >= 2:
        return en, "iki-oy" if len(oylar) == 2 else "üç-oy"
    if len(oylar) < 3:
        return None, "bekliyor"  # hakem gerekli
    return (kural if kural in c else c.most_common(1)[0][0]), "düşük"


# ---------- sinifla ----------
CAGRI = 0
OLU = set()


def env_oku(ad):
    import os, winreg
    if os.environ.get(ad):
        return os.environ[ad]
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as h:
        return winreg.QueryValueEx(h, ad)[0]


def sor(model, istem):
    global CAGRI
    assert CAGRI < TAVAN, "çağrı tavanı"
    CAGRI += 1
    if model.startswith("openrouter/"):
        url, h = "http://127.0.0.1:20128/v1/chat/completions", {"authorization": f"Bearer {env_oku('OMNIROUTE_KEY')}", "user-agent": "curl/8.4"}
    else:
        url, h = "http://127.0.0.1:11434/v1/chat/completions", {}
    q = urllib.request.Request(url, method="POST", headers={"content-type": "application/json", **h},
                               data=json.dumps({"model": model, "max_tokens": 12000, "temperature": 0,
                                                "messages": [{"role": "user", "content": istem}]}).encode())
    y = json.load(urllib.request.urlopen(q, timeout=300))["choices"][0]["message"].get("content") or ""
    return json.loads(y[y.index("{"):y.rindex("}") + 1])


def parti_sor(modeller, parti):
    istem = ISTEM + "\n".join(f"{i}. [{k['tur']}] {k['ad']} — {k['aciklama'][:200] or '(açıklama yok)'}" for i, k in enumerate(parti, 1))
    for model in [m for m in modeller if m not in OLU]:
        for deneme in range(1 if model.endswith(":free") else 2):  # :free 429'da beklemeden yedeğe geç
            try:
                y = sor(model, istem)
                return model, {anahtar(k): str(y.get(str(i), "")).strip().lower() for i, k in enumerate(parti, 1)}
            except AssertionError:
                raise
            except Exception as e:  # noqa: BLE001 — 429/zaman aşımı: bekle, sonra yedek model
                if "429" in str(e) and model.endswith(":free"):
                    OLU.add(model)  # günlük/dakika kotası: bu koşuda bir daha deneme
                print("hata", model, type(e).__name__, str(e)[:120], flush=True)
                time.sleep(5)
    return None, {}


def onbellek():
    oy = defaultdict(dict)  # anahtar -> {kol: kategori}
    if ONBELLEK.exists():
        for s in ONBELLEK.read_text(encoding="utf-8").splitlines():
            d = json.loads(s)
            oy[d["k"]][d["kol"]] = d["c"]
    return oy


KILIT = threading.Lock()


def kol_isle(kol, modeller, kalemler, f, isci=3):
    def bir(p):
        model, y = parti_sor(modeller, p)
        with KILIT:
            for a, c in y.items():
                f.write(json.dumps({"k": a, "kol": kol, "m": model, "c": c}, ensure_ascii=False) + "\n")
            f.flush()
            print(kol, "parti", len(y), "çağrı", CAGRI, flush=True)
    with ThreadPoolExecutor(isci) as ex:  # nemotron yavaş (~5 dk/parti): kol içi 3 paralel parti
        list(ex.map(bir, [kalemler[i:i + PARTI] for i in range(0, len(kalemler), PARTI)]))


def sinifla(rows):
    tekil = {}
    for k in rows:
        if oylanacak(k):
            tekil.setdefault(anahtar(k), k)
    oy = onbellek()
    print("oylanacak tekil", len(tekil), "önbellekte", sum(1 for a in tekil if a in oy), flush=True)
    with open(ONBELLEK, "a", encoding="utf-8", newline="\n") as f:
        eksik1 = [k for a, k in tekil.items() if oy[a].get("oy1") not in KATLAR]
        eksik2 = [k for a, k in tekil.items() if oy[a].get("oy2") not in KATLAR]
        with ThreadPoolExecutor(2) as ex:  # iki kol paralel; her kol içinde sıralı
            list(ex.map(lambda x: kol_isle(*x, f), [("oy1", [OY1], eksik1), ("oy2", list(OY2), eksik2)]))
        oy = onbellek()
        hakem = [k for a, k in tekil.items() if karar({x: oy[a].get(x) for x in ("oy1", "oy2")}, k["kategori_tahmin"])[1] == "bekliyor"
                 and oy[a].get("oy3") not in KATLAR]
        print("hakeme giden", len(hakem), flush=True)
        kol_isle("oy3", [HAKEM], hakem, f)
    print("toplam çağrı", CAGRI)


# ---------- kullanim ----------
SEG = re.compile(r"&&|\|\||;|\|")


def ilk_sozcukler(komut):
    out = []
    for seg in SEG.split(komut or ""):
        w = [x for x in seg.strip().split() if "=" not in x[:40] or x.startswith(("-", "/"))]
        if w:
            out.append(re.sub(r"\.(exe|cmd|bat|ps1)$", "", w[0].strip("\"'&(").replace("\\", "/").rsplit("/", 1)[-1].lower()))
    return [x for x in out if x]


def mcp_sunucu(ad):
    s = ad.split("__")[1] if ad.count("__") >= 2 else ""
    return s.split("_", 2)[-1] if s.startswith("plugin_") else s


def satir_say(d, say, sinir):
    if d.get("timestamp", "9") < sinir:
        return
    icerik = (d.get("message") or {}).get("content")
    if d.get("type") == "user" and isinstance(icerik, str):
        for m in re.findall(r"<command-name>/?([^<]+)</command-name>", icerik):
            say["komut", norm(m.split(":")[-1])] += 1
    if d.get("type") != "assistant" or not isinstance(icerik, list):
        return
    for b in icerik:
        if b.get("type") != "tool_use":
            continue
        ad, g = b.get("name", ""), b.get("input") or {}
        if ad == "Skill":
            say["skill", norm(str(g.get("skill", "")).split(":")[-1])] += 1
        elif ad in ("Agent", "Task"):
            say["agent", norm(str(g.get("subagent_type", "")).split(":")[-1])] += 1
        elif ad.startswith("mcp__"):
            say["mcp", norm(mcp_sunucu(ad))] += 1
            say["mcp-arac", ad] += 1
        elif ad in ("Bash", "PowerShell"):
            for w in ilk_sozcukler(str(g.get("command", ""))):
                say["cli", w] += 1


def kullanim():
    import ctypes
    sinir_t = time.time() - 30 * 86400
    sinir = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(sinir_t))
    say, n = Counter(), 0
    for p in (Path.home() / ".claude/projects").rglob("*.jsonl"):
        if p.stat().st_mtime < sinir_t:
            continue
        n += 1
        with open(p, encoding="utf-8", errors="replace") as f:
            for s in f:
                if '"tool_use"' in s or "<command-name>" in s:
                    try:
                        satir_say(json.loads(s), say, sinir)
                    except ValueError:
                        pass
        if n % 500 == 0:
            m = (ctypes.c_ulong * 16)()
            m[0] = 64
            ctypes.windll.kernel32.GlobalMemoryStatusEx(m)
            assert m[1] < 85, f"RAM %{m[1]}"
            print(n, "dosya · RAM %", m[1], flush=True)
    (BURASI / "kullanim-30g.json").write_text(json.dumps({"dosya": n, "sinir": sinir, "sayim": {f"{a}\t{b}": c for (a, b), c in say.items()}},
                                                         ensure_ascii=False, indent=0), encoding="utf-8")
    print("dosya", n, "anahtar", len(say))


def kullanim_esle(rows, sayim):
    sinif = {"skill": "skill", "agent": "agent", "mcp": "mcp", "cli": "cli", "komut": "komut"}
    out = {}
    for k in rows:
        t = sinif.get(k["tur"])
        out[k["id"]] = sayim.get(f"{t}\t{norm(k['ad'])}", 0) if t else 0
    plug = Counter()
    for k in rows:
        if k["kaynak"].startswith("plugin:"):
            plug[k["kaynak"][7:].split("@")[0].lower()] += out[k["id"]]
    for k in rows:
        if k["tur"] == "plugin":
            out[k["id"]] = plug[norm(k["ad"])]
    return out


# ---------- katman / kanonik ----------
AKTIF = re.compile(r"^(telve|site-telve|video|fable-video|site-okulu|token)", re.I)


def a_metni():
    parcalar = [p.read_text(encoding="utf-8", errors="replace") for p in (REPO / "skills").glob("departman-*/**/*.md")]
    parcalar += [p.read_text(encoding="utf-8", errors="replace") for p in (Path.home() / ".claude/skills/is-akisi").rglob("*.md")]
    parcalar += [p.read_text(encoding="utf-8", errors="replace") for p in (REPO / ".kos/kopru/gorev").glob("*.md") if AKTIF.match(p.name)]
    return set(re.findall(r"[a-z0-9][a-z0-9_\-.]*[a-z0-9]", "\n".join(parcalar).lower()))


def adda_gecer(ad, sozcukler):
    n = norm(ad)
    # shortcut: kısa genel adlar (review, setup, test…) her metinde geçer; ayırt edici olmayan ad A'ya metinden girmez, kullanımdan girer
    return ("-" in n or len(n) >= 8) and n in sozcukler


def katmanla(rows, kull, sozcukler):
    kat = {}
    for k in rows:
        if kurulu(k) and (adda_gecer(k["ad"], sozcukler) or kull[k["id"]] >= 3):
            kat[k["id"]] = "A"
    a_grup = {k["kopya_grubu"] for k in rows if kat.get(k["id"]) == "A" and k["kopya_grubu"]}
    a_kaynak = {k["kaynak"] for k in rows if kat.get(k["id"]) == "A" and k["kaynak"].startswith("plugin:")}
    for k in rows:
        if not kurulu(k):
            kat[k["id"]] = "-"
        elif k["id"] not in kat:
            yakin = k["kopya_grubu"] in a_grup or k["kaynak"] in a_kaynak or 1 <= kull[k["id"]] <= 2
            kat[k["id"]] = "B" if yakin else "C"
    return kat


def dosya_bilgi(yol):
    dis, _, ic = yol.partition("!")
    p = Path(dis)
    try:
        mt = p.stat().st_mtime
        if ic:
            with zipfile.ZipFile(p) as z:
                veri = z.read(ic.replace("\\", "/"))
        else:
            veri = p.read_bytes() if p.is_file() else None
    except (OSError, KeyError, zipfile.BadZipFile):
        return 0, None
    return mt, hashlib.sha1(veri).hexdigest()[:8] if veri is not None else None


def kanonikle(rows, bilgi=dosya_bilgi):
    kan, fark = {k["id"]: k["id"] for k in rows}, {}
    grup = defaultdict(list)
    for k in rows:
        if k["kopya_grubu"]:
            grup[k["kopya_grubu"]].append(k)
    for g, uyeler in grup.items():
        b = {k["id"]: bilgi(k["yol"]) for k in uyeler}
        en = max(uyeler, key=lambda k: (b[k["id"]][0], k["bayt"]))
        shalar = {b[k["id"]][1] for k in uyeler} - {None}
        for k in uyeler:
            kan[k["id"]] = en["id"]
            fark[k["id"]] = g.startswith("ad:") and len(shalar) > 1
    return kan, fark


# ---------- modeller ----------
def modeller_tsv(json_yol, cikti):
    j = json.loads(Path(json_yol).read_text(encoding="utf-8"))
    L = ["model\tsağlayıcı\tfree\tmetin\tgörsel\tses\tkod\tbağlam"]
    for m in (j["data"] if isinstance(j, dict) else j):
        i, cap = m["id"], m.get("capabilities") or {}
        gir = set(m.get("input_modalities") or []) | set(m.get("output_modalities") or [])
        tip = m.get("type")
        metin = tip in (None, "embedding", "rerank") or "text" in gir
        gorsel = bool(cap.get("vision")) or tip in ("image", "video") or bool(gir & {"image", "video"})
        ses = tip == "audio" or "audio" in gir or bool(re.search(r"audio|whisper|transcrib|tts|speech", i, re.I))
        kod = bool(re.search(r"cod(e|er|ing|estral)|devstral", i, re.I))
        L.append("\t".join([i, m.get("owned_by", ""), str(":free" in i).lower()] + ["1" if x else "0" for x in (metin, gorsel, ses, kod)]
                           + [str(m.get("context_length") or m.get("max_input_tokens") or "")]))
    Path(cikti).write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    return len(L) - 1


# ---------- son ----------
def tekil_kurulu(rows):
    t = {}
    for k in rows:
        if kurulu(k):
            t.setdefault(k["kopya_grubu"] or k["id"], k)
    return t


def ornek(rows, n=40, tohum=15):
    t = sorted(tekil_kurulu(rows).values(), key=lambda k: k["id"])
    return random.Random(tohum).sample(t, n)


def son():
    rows = [json.loads(s) for s in (BURASI / "katalog.jsonl").read_text(encoding="utf-8").splitlines()]
    oy = onbellek()
    sayim = json.loads((BURASI / "kullanim-30g.json").read_text(encoding="utf-8"))["sayim"]
    kull = kullanim_esle(rows, sayim)
    kat = katmanla(rows, kull, a_metni())
    kan, fark = kanonikle(rows)
    bekleyen = 0
    for k in rows:
        if oylanacak(k):
            o = {x: oy[anahtar(k)].get(x) for x in ("oy1", "oy2", "oy3") if oy[anahtar(k)].get(x)}
            c, g = karar(o, k["kategori_tahmin"])
            if c is None:
                bekleyen += 1
                c, g = o.get("oy1") if o.get("oy1") in KATLAR else k["kategori_tahmin"], "düşük"
        else:
            c, g = k["kategori_tahmin"], ("kural" if kurulu(k) else "kural-kurulu-değil")
        k.update(kategori_son=c, kategori_guven=g, katman=kat[k["id"]], kanonik=kan[k["id"]], kullanim_30g=kull[k["id"]])
        if fark.get(k["id"]):
            k["icerik_farki"] = True
    with open(BURASI / "katalog-son.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for k in rows:
            f.write(json.dumps(k, ensure_ascii=False) + "\n")
    nm = modeller_tsv(REPO / ".kos/kopru/envanter/omni_models_api.json", BURASI / "modeller.tsv")
    elle_p = BURASI / "elle-40.json"
    elle = json.loads(elle_p.read_text(encoding="utf-8")) if elle_p.exists() else {}
    byid = {k["id"]: k for k in rows}
    uyum = [(i, c, byid[i]["kategori_son"]) for i, c in elle.items()]
    (BURASI / "ozet-0b.md").write_bytes(ozet0b(rows, uyum, nm, bekleyen, sayim).encode("utf-8"))
    print("yazıldı · bekleyen", bekleyen)


def ozet0b(rows, uyum, nm, bekleyen, sayim):
    kur = [k for k in rows if kurulu(k)]
    tek = tekil_kurulu(rows)
    tk = Counter((k["kategori_son"], k["katman"]) for k in tek.values())
    eski = Counter(k["kategori_tahmin"] for k in tek.values())
    yeni = Counter(k["kategori_son"] for k in tek.values())
    dogru = sum(a == b for _, a, b in uyum)
    L = ["# ÖĞREN-0b katalog son hali (Claude okuma tokenı 0; sınıflama ücretsiz modellerle)", "",
         f"Kurulu {len(kur)} satır · tekil {len(tek)} · kategori_son+katman dolu: {sum(bool(k.get('kategori_son')) and k['katman'] in 'ABC' for k in kur)}/{len(kur)}"
         f" · hakemsiz kalan {bekleyen}",
         "Güven: " + ", ".join(f"{g} {n}" for g, n in Counter(k["kategori_guven"] for k in kur).most_common()),
         f"Elle uyum (rastgele {len(uyum)} tekil, tohum 15): {dogru}/{len(uyum)} = %{100 * dogru / max(1, len(uyum)):.0f}"
         + (" · ıska: " + "; ".join([f"{i} elle={a} model={b}" for i, a, b in uyum if a != b][:8]) if dogru < len(uyum) else ""),
         f"Token kategorisi yeniden: {eski['token']} → {yeni['token']} tekil · diğer {eski['diğer']} → {yeni['diğer']}",
         f"Modeller: {nm} satır → ogren/modeller.tsv · kanonik: {sum(k['kanonik'] == k['id'] for k in kur if k['kopya_grubu'])} kanonik, "
         f"{sum(k['kanonik'] != k['id'] for k in kur)} alias, içerik farkı {sum(bool(k.get('icerik_farki')) for k in kur)} satır",
         f"Kullanım taraması: {sum(v for a, v in sayim.items() if not a.startswith('mcp-arac'))} sayım; kullanim_30g>0 olan kurulu tekil "
         f"{sum(k['kullanim_30g'] > 0 for k in tek.values())}", "",
         "## Kategori × katman (tekil kurulu) + tahmini okuma tokenı (A tam metin, B/C ad+açıklama özeti)",
         "| kategori | A | B | C | eski tahmin | okuma token |", "|---|---|---|---|---|---|"]
    for c in KATLAR:
        tok = sum(k["token_tahmin"] if k["katman"] == "A" else len(k["ad"] + k["aciklama"]) // 3 + 10
                  for k in tek.values() if k["kategori_son"] == c)
        L.append(f"| {c} | {tk[c, 'A']} | {tk[c, 'B']} | {tk[c, 'C']} | {eski[c]} | ~{tok:,} |")
    L += ["", "## A katmanı adları (kategori başı; kullanım sırasıyla, ilk 25 — tamamı katalog-son.jsonl katman=A)"]
    for c in KATLAR:
        a = sorted((k for k in tek.values() if k["kategori_son"] == c and k["katman"] == "A"), key=lambda k: (-k["kullanim_30g"], k["ad"]))
        if a:
            adlar = list(dict.fromkeys(k["ad"] for k in a))  # aynı ad farklı tür/kaynak satırı: bir kez
            L.append(f"- **{c}** ({len(a)} satır, {len(adlar)} ad): " + ", ".join(adlar[:25]) + (" …" if len(adlar) > 25 else ""))
    return "\n".join(L[:60]) + "\n"


if __name__ == "__main__":
    adim = sys.argv[1] if len(sys.argv) > 1 else "son"
    if adim == "sinifla":
        sinifla([json.loads(s) for s in (BURASI / "katalog.jsonl").read_text(encoding="utf-8").splitlines()])
    elif adim == "kullanim":
        kullanim()
    elif adim == "ornek":
        for k in ornek([json.loads(s) for s in (BURASI / "katalog.jsonl").read_text(encoding="utf-8").splitlines()]):
            print(k["id"], f"[{k['tur']}]", k["ad"], "—", k["aciklama"][:160])
    else:
        son()
