"""TOKEN-REA d1 taban: araç başı A/B (araç açık/kapalı), GERÇEK token = count_tokens (a6.py vekil yakalama kalıbı).
Claude çağrısı: tek `claude -p` (başlık yakalama) + ücretsiz count_tokens. Çıktı: taban.json. İçerik metni yazılmaz, yalnız sayı.
  python taban.py [araç ...]   (rtk headroom graphify claudemem baglam profil)"""
import hashlib, json, os, random, re, subprocess, sys, threading, time, urllib.request, urllib.parse
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
BU = Path(__file__).parent
for p in (KOK / "tools", KOK / ".claude" / "token3", KOK / ".claude" / "token4"):
    sys.path.insert(0, str(p))
import a6, onek_kayit as ok, cc_profil  # noqa: E401

NW = 0x08000000
SAYAC = {"say": 0}
SAY_TAVAN = 400
_onb = {}


def kur_baslik():
    ok.etiket = "taban"; ok.DIZ.mkdir(parents=True, exist_ok=True)
    s = ok.http.server.ThreadingHTTPServer(("127.0.0.1", 0), a6.V)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    ayar = {"env": {"ANTHROPIC_BASE_URL": f"http://127.0.0.1:{s.server_port}"}}
    a, e = cc_profil.kur("ajan", ek_ayar=ayar, gecici=ok.DIZ.parent / "profil")
    argv = [r"C:\Users\pc\.local\bin\claude.exe", "-p", "--output-format", "json", "--model", "opus",
            "--disable-slash-commands", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', *a]
    subprocess.run(argv, input="Yalnız 'tamam' yaz, araç kullanma.".encode(), capture_output=True, cwd=str(KOK),
                   env={**os.environ, **e}, creationflags=NW, timeout=300)
    return json.loads(a6.yakala["govde"]), a6.yakala["baslik"]


GOVDE, BASLIK = None, None


def tok(metin):
    """Gerçek input token (boş '.' mesajı farkı); ≥150k karakter kesilir (işaretlenir)."""
    if not metin:
        return 0
    metin = metin[:150000]
    h = hashlib.md5(metin.encode("utf-8", "replace")).hexdigest()
    if h in _onb:
        return _onb[h]
    if SAYAC["say"] >= SAY_TAVAN:
        raise RuntimeError("count_tokens tavanı")
    def g(t):
        SAYAC["say"] += 1
        return a6.say(BASLIK, {"model": GOVDE["model"], "messages": [{"role": "user", "content": t}]})
    if "bos" not in _onb:
        _onb["bos"] = g(".")
    _onb[h] = max(0, g(metin) - _onb["bos"])
    return _onb[h]


def kos(argv, cwd=KOK, tmo=120):
    t = time.time()
    try:
        p = subprocess.run(argv, capture_output=True, cwd=str(cwd), timeout=tmo, creationflags=NW, shell=False)
        c = (p.stdout + p.stderr).decode("utf-8", "replace")
        return c, time.time() - t, p.returncode
    except Exception as ex:  # noqa: BLE001
        return f"HATA {ex}", time.time() - t, -1


def ram():
    try:
        import psutil
        return psutil.virtual_memory().percent
    except Exception:  # noqa: BLE001
        return None


def ozet(satirlar, ad):
    """satir = dict(a_tok, b_tok, a_s, b_s, hit_a, hit_b, hata)"""
    n = len(satirlar)
    a = sum(s["a_tok"] for s in satirlar); b = sum(s["b_tok"] for s in satirlar)
    return {"arac": ad, "n": n, "a_tok": a, "b_tok": b, "kazanc_pct": round(100 * (a - b) / a, 1) if a else None,
            "a_sn": round(sum(s["a_s"] for s in satirlar), 2), "b_sn": round(sum(s["b_s"] for s in satirlar), 2),
            "kalite_a": f"{sum(s['hit_a'] for s in satirlar)}/{n}", "kalite_b": f"{sum(s['hit_b'] for s in satirlar)}/{n}",
            "hata": sum(s["hata"] for s in satirlar)}


# ---- RTK: A = çıplak komut, B = rtk komutu; kalite = tohumlu anahtar çıktıda kalıyor mu ----
def m_rtk():
    br = kos(["git", "branch", "--show-current"])[0].strip()
    konu = kos(["git", "log", "-1", "--format=%s"])[0].strip()[:25]
    # (ad, raw argv, rtk argv, anahtar|None=ham ilk dolu satır sözcüğü); egitim = ilk 10, held-out = son 4 (koşulmaz)
    E = [("git log -10", ["git", "log", "-10", "--oneline"], ["rtk", "git", "log", "-10", "--oneline"], konu),
         ("git status", ["git", "status"], ["rtk", "git", "status"], br),
         ("ls -la tools", ["ls", "-la", "tools"], ["rtk", "ls", "-la", "tools"], "token_olc.py"),
         ("grep AGIRLIK", ["git", "grep", "-n", "AGIRLIK", "--", "tools/token_olc.py"], ["rtk", "grep", "AGIRLIK", "tools/token_olc.py"], "AGIRLIK"),
         ("git diff --stat", ["git", "diff", "HEAD~3", "--stat"], ["rtk", "git", "diff", "HEAD~3", "--stat"], None),
         ("git log -30 --stat", ["git", "log", "-30", "--stat"], ["rtk", "git", "log", "-30", "--stat"], konu),
         ("read token_olc", ["cat", "tools/token_olc.py"], ["rtk", "read", "tools/token_olc.py"], "def parcala"),
         ("read -l aggressive token.md", ["cat", "docs/ogren/token.md"], ["rtk", "read", "-l", "aggressive", "docs/ogren/token.md"], "headroom"),
         ("ls -la kök", ["ls", "-la"], ["rtk", "ls", "-la"], "CLAUDE.md"),
         ("git diff HEAD~2", ["git", "diff", "HEAD~2"], ["rtk", "git", "diff", "HEAD~2"], None)]
    HELD = ["rtk pytest --co", "rtk find", "rtk git blame", "rtk tree"]  # d2 kapısı için mühürlü, koşulmadı
    S = []
    for ad, a, b, k in E:
        ca, ta, ra = kos(a); cb, tb, rb = kos(b)
        if k is None:  # anahtar: ham çıktıdan ilk 12+ harfli sözcük (dosya adı) tohumu
            m = re.search(r"[\w./-]{12,}", ca); k = m.group(0) if m else "?"
        S.append({"ad": ad, "a_tok": tok(ca), "b_tok": tok(cb), "a_s": ta, "b_s": tb, "hit_a": int(k in ca),
                  "hit_b": int(k in cb), "hata": int(rb != 0 or ra != 0)})
    return S, ozet(S, "rtk"), HELD


# ---- Headroom: compress() API'si, 6 sabit parça; kalite = ham metinden tohumlu 8 uzun sözcük çıktıda kalıyor mu ----
def m_headroom():
    from headroom import compress
    dos = [KOK / "docs/ogren/token.md", KOK / "tools/token_olc.py", KOK / ".kos/kopru/gorev/SIRA.md",
           KOK / ".kos/kopru/omni-ayir/cli-combo-list.json", KOK / "docs/ters/rea-tarama.md", KOK / "tools/ucuz_alt.py"]
    S = []
    rnd = random.Random(7)
    for f in dos:
        ham = f.read_text(encoding="utf-8", errors="replace")[:60000]
        sozc = sorted(set(re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü_0-9]{9,}", ham))); rnd.shuffle(sozc); k = sozc[:8]
        t = time.time(); r0 = ram()
        try:
            r = compress([{"role": "user", "content": "özetle"}, {"role": "tool", "content": ham}], model="claude-opus-5-5")
            cik = r.messages[-1]["content"] if isinstance(r.messages[-1]["content"], str) else json.dumps(r.messages[-1]["content"])
            hata = 0
        except Exception as ex:  # noqa: BLE001
            cik, hata = ham, 1
        S.append({"ad": f.name, "a_tok": tok(ham), "b_tok": tok(cik), "a_s": 0.0, "b_s": time.time() - t,
                  "hit_a": 1, "hit_b": round(sum(x in cik for x in k) / max(1, len(k)), 2), "hata": hata})
    return S, ozet(S, "headroom-compress-api"), []


# ---- graphify: A = git grep (çıplak, ilk 120 satır), B = graphify query; kalite = beklenen sembol çıktıda ----
def m_graphify():
    Q = [("token_olc ağırlıklı ölçüm", "token_olc"), ("cc_profil kur", "cc_profil"), ("onek_kayit vekil", "onek_kayit"),
         ("ucuz_alt free zincir", "ucuz_alt"), ("beyin kapı doğru", "beyin"), ("mem_bekci sağlık", "mem_bekci"),
         ("graphify_sor etiket", "graphify_sor"), ("nblm paket", "nblm"), ("zip_denetle", "zip_denetle"), ("kapi_kos ters", "kapi_kos")]
    HELD = ["dalga_durum", "headroom_claude_guard", "rtk_onisle", "ajan_sira", "model_olc"]
    S = []
    for q, k in Q:
        kw = q.split()[0]
        ca, ta, _ = kos(["git", "grep", "-n", "-I", "-i", kw, "--", "tools", ".claude", ".kos/kopru/*.py"])
        ca = "\n".join(ca.splitlines()[:120])
        cb, tb, rb = kos(["graphify", "query", q], tmo=90)
        S.append({"ad": q, "a_tok": tok(ca), "b_tok": tok(cb), "a_s": ta, "b_s": tb, "hit_a": int(k.lower() in ca.lower()),
                  "hit_b": int(k.lower() in cb.lower()), "hata": int(rb != 0)})
    return S, ozet(S, "graphify-query"), HELD


# ---- claude-mem: A = arama kapalı (0 token, 0 isabet), B = /api/search; ayrıca SessionStart enjeksiyonu ayrı satır (profil) ----
def m_claudemem():
    Q = [("MEM-FIX-3", "saglik"), ("RAM monitoring", "llama-server"), ("Bulut-1", "Local LLM"), ("ollama_log", "log"),
         ("PermissionError", "kopru"), ("ÖĞREN-2 d3", "ÖĞREN"), ("closure criteria", "ÖĞREN-6"), ("model policy cloud", "cloud"),
         ("pilot script", "model"), ("ajan-sira.log", "ajan-sira")]
    HELD = ["TELVE-TOKEN-1", "A6 köprü", "OMNİ-AYIR d2", "headroom retrieve", "karar tohumu"]
    S = []
    for q, k in Q:
        t = time.time(); hata = 0
        try:
            c = urllib.request.urlopen("http://127.0.0.1:37777/api/search?" + urllib.parse.urlencode({"query": q, "limit": 5}), timeout=15).read().decode("utf-8", "replace")
        except Exception as ex:  # noqa: BLE001
            c, hata = f"HATA {ex}", 1
        S.append({"ad": q, "a_tok": 0, "b_tok": tok(c), "a_s": 0.0, "b_s": time.time() - t, "hit_a": 0, "hit_b": int(k.lower() in c.lower()), "hata": hata})
    return S, ozet(S, "claude-mem-search"), HELD


# ---- sabit bağlam (ajan profili): sistem / araç / mesaj gövdesi gerçek token'ı ----
def m_profil():
    b = GOVDE; tam = a6.say(BASLIK, {k: b[k] for k in ("model", "system", "tools", "messages") if k in b})
    r = {"toplam": tam}
    for k in ("tools", "system"):
        y = {kk: vv for kk, vv in b.items() if kk in ("model", "system", "tools", "messages") and kk != k}
        r[k] = tam - a6.say(BASLIK, y) if y.get("messages") else None
    y = json.loads(json.dumps(b));
    for m in y["messages"]:
        if isinstance(m["content"], list):
            for c in m["content"]:
                if "text" in c: c["text"] = "."
        else: m["content"] = "."
    r["mesajlar_hook_enjeksiyon"] = tam - a6.say(BASLIK, {k: y[k] for k in ("model", "system", "tools", "messages") if k in y})
    return r


# ---- 3 iş profili toplam token (gerçek API kullanımı, oturum jsonl; son 14 gün, mesaj-id tekilleştirilmiş) ----
def m_profiller(gun=14):
    kok = Path.home() / ".claude" / "projects"; esik = time.time() - gun * 86400
    P = {"kod dalgası": [], "araştırma": [], "köprü kontrolü": []}
    def sinif(ad):
        a = ad.lower()
        if "observer" in a or "claude-mem" in a: return None
        if "ogren" in a or "video" in a or "arastirma" in a: return "araştırma"
        if "kopru" in a or "ajan-sira" in a or "envanter" in a or "ig-chrome" in a: return "köprü kontrolü"
        if "omer-skills" in a: return "kod dalgası"
        return None
    for d in kok.iterdir():
        s = sinif(d.name)
        if not s: continue
        for f in d.glob("*.jsonl"):
            if f.stat().st_mtime < esik: continue
            gor, g, cr, cw, c = set(), 0, 0, 0, 0
            for ln in f.open(encoding="utf-8", errors="replace"):
                if '"usage"' not in ln: continue
                try: j = json.loads(ln)
                except Exception: continue  # noqa: BLE001
                m = j.get("message") or {}; u = m.get("usage"); i = m.get("id") or j.get("uuid")
                if not u or i in gor: continue
                gor.add(i); g += u.get("input_tokens") or 0; cr += u.get("cache_read_input_tokens") or 0
                cw += u.get("cache_creation_input_tokens") or 0; c += u.get("output_tokens") or 0
            if gor: P[s].append((g, cr, cw, c, len(gor)))
    R = {}
    for s, L in P.items():
        if not L: R[s] = None; continue
        tot = [sum(x[i] for x in L) for i in range(5)]
        med = sorted(L, key=lambda x: x[0] + x[1] + x[2] + x[3])[len(L) // 2]
        R[s] = {"oturum": len(L), "girdi": tot[0], "cache_okuma": tot[1], "cache_yazma": tot[2], "cikti": tot[3], "istek": tot[4],
                "girdi_artı_cikti_ham": tot[0] + tot[1] + tot[2] + tot[3],
                "agirlikli": round(tot[0] + tot[1] * .1 + tot[2] * 1.25 + tot[3] * 5),
                "medyan_oturum_ham": med[0] + med[1] + med[2] + med[3], "medyan_istek": med[4]}
    return R


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    secim = sys.argv[1:] or ["rtk", "headroom", "graphify", "claudemem", "profil", "profiller"]
    cikti = {"ts": time.strftime("%Y-%m-%d %H:%M"), "ram_basta": ram()}
    GOVDE, BASLIK = kur_baslik()
    cikti["capture_ok"] = True
    F = {"rtk": m_rtk, "headroom": m_headroom, "graphify": m_graphify, "claudemem": m_claudemem}
    for a in secim:
        try:
            if a in F:
                S, O, H = F[a](); cikti[a] = {"ozet": O, "satirlar": S, "held_out_muhurlu": H}
            elif a == "profil": cikti[a] = m_profil()
            elif a == "profiller": cikti[a] = m_profiller()
        except Exception as ex:  # noqa: BLE001
            cikti[a] = {"hata": repr(ex)[:300]}
        print(a, "tamam", "ram", ram(), "say", SAYAC["say"])
    cikti["count_tokens_cagri"] = SAYAC["say"]; cikti["ram_sonda"] = ram()
    (BU / "taban.json").write_text(json.dumps(cikti, ensure_ascii=False, indent=1), encoding="utf-8")
    print("yazıldı taban.json")
