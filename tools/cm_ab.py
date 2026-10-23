"""CODE-MODE-AB-1: normal MCP (kol A) ↔ Bash + tools/cm.py (kol B) token A/B ölçümü.
  python tools/cm_ab.py kos [--model haiku|sonnet] [--saniye 480] [--paralel 2]   # eksik koşuları sürdürür (.kos/kopru/ab/sonuc.jsonl)
  python tools/cm_ab.py ozet                                                      # model×kol toplamları + doğruluk
Her koşu: claude -p stream-json, --strict-mcp-config, --setting-sources project,local (CLAUDE.md/hook yok, 7 sn başlangıç)."""
import json, os, random, re, shutil, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
AB = KOK / ".kos" / "kopru" / "ab"
SONUC = AB / "sonuc.jsonl"
CWD = Path(tempfile.gettempdir()) / "cm_ab"
GW = "http://127.0.0.1:47800/servers/{}/mcp"
MCP_A = {"mcpServers": {
    "git": {"command": r"C:\Users\pc\.local\bin\mcp-server-git.exe", "args": []},
    "fetch": {"type": "http", "url": GW.format("mcp-fetch")},
    "brave": {"type": "http", "url": GW.format("brave-search")},
    "pw": {"command": "node", "args": [r"C:\AI\mcp\playwright\node_modules\@playwright\mcp\cli.js", "--isolated", "--headless"]},
}}
SKILL_B = ("Araçların: yalnız Bash. Zincirli araç işi için TEK çağrıda: python C:/Projeler/omer-skills/tools/cm.py "
           "(list | search \"<görev>\" | info <araç> | run dosya.js | run -c \"js\"). Kod düz JavaScript, araçlar senkron "
           "(git.git_git_log({repo_path,max_count}), git.git_git_show, gw.fetch_fetch, gw.brave_brave_web_search, pw.pw_browser_navigate/snapshot/evaluate/close), "
           "ham çıktıyı döndürme, say/süz, yalnız özeti `return` et. Araç adı/şeması bilmiyorsan önce cm.py search/info.")
GOREV = {
    "a": ("C:\\Projeler\\omer-skills deposunda aa2436fd commit'inden (dahil) geriye son 30 commit'i konu satırındaki etikete "
          "(ilk ':' öncesi) göre say ve bu 30 commit'te değişen BENZERSİZ dosya sayısını ver. Yalnız tek satır JSON: "
          "{\"etiket_sayisi\":<farklı etiket sayısı>,\"dosya\":<benzersiz dosya>,\"en_cok\":\"<etiket> <adet>\"}"),
    "b": ("Üç ayrı web araması yap: 'UTCP code mode', 'Anthropic code execution with MCP', 'Cloudflare Code Mode MCP'. "
          "Sonuçlardan iki sayfayı fetch et. Bulgulardan TAM 5 maddelik Türkçe özet yaz (her madde '- ' ile başlasın, başka metin yok)."),
    "c": ("Playwright ile https://example.com ve http://info.cern.ch sayfalarını gez; her biri için sayfa başlığı ve <a> link sayısı. "
          "Yalnız tek satır JSON: [{\"url\":..,\"title\":..,\"links\":..}]"),
}


def dogru(gorev, metin):
    """Doğruluk: a = etiket 18 · dosya 204 · en_cok adet 3; b = tam 5 madde; c = iki başlık + info.cern.ch link 4 (example.com 0|1)."""
    if gorev == "a":
        try:
            j = json.loads(re.search(r"\{.*\}", metin, re.S).group(0))
            return j.get("etiket_sayisi") == 18 and j.get("dosya") == 204 and bool(re.search(r"\b3\b", str(j.get("en_cok"))))
        except (AttributeError, ValueError):
            return False
    if gorev == "b":
        return len(re.findall(r"^\s*[-•*] .{15,}", metin, re.M)) == 5
    try:
        j = json.loads(re.search(r"\[.*\]", metin, re.S).group(0))
        d = {x["url"].rstrip("/").split("//")[-1]: x for x in j}
        return len(d) == 2 and d["example.com"]["title"] == "Example Domain" and d["example.com"]["links"] in (0, 1) \
            and "info.cern.ch" in d["info.cern.ch"]["title"] and d["info.cern.ch"]["links"] == 4
    except (AttributeError, ValueError, KeyError, TypeError):
        return False


def argv(model, kol):
    a = [shutil.which("claude"), "-p", "--output-format", "stream-json", "--verbose", "--model", model, "--strict-mcp-config",
         "--setting-sources", "project,local", "--disable-slash-commands", "--max-turns", "40", "--max-budget-usd", "1.0"]
    if kol == "A":
        return a + ["--mcp-config", json.dumps(MCP_A), "--tools", "", "--allowedTools", "mcp__git,mcp__fetch,mcp__brave,mcp__pw"]
    return a + ["--mcp-config", '{"mcpServers":{}}', "--tools", "Bash", "--allowedTools", "Bash", "--append-system-prompt", SKILL_B]


def koş(anahtar):
    model, gorev, kol, tekrar = anahtar
    t0 = time.time()
    CWD.mkdir(exist_ok=True)
    p = subprocess.run(argv(model, kol), input=GOREV[gorev], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=str(CWD), timeout=900, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    araclar, son = {}, {}
    for s in p.stdout.splitlines():
        try:
            e = json.loads(s)
        except ValueError:
            continue
        if e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use":
                    araclar[c["name"]] = araclar.get(c["name"], 0) + 1
        elif e.get("type") == "result":
            son = e
    u = son.get("usage", {})
    metin = son.get("result") or ""
    return {"model": model, "gorev": gorev, "kol": kol, "tekrar": tekrar, "girdi": u.get("input_tokens", 0),
            "yaz": u.get("cache_creation_input_tokens", 0), "oku": u.get("cache_read_input_tokens", 0), "cikti": u.get("output_tokens", 0),
            "usd": son.get("total_cost_usd", 0), "tur": son.get("num_turns", 0), "sn": round(time.time() - t0, 1),
            "dogru": bool(metin) and dogru(gorev, metin), "araclar": araclar, "hata": bool(son.get("is_error")) or not son,
            "yanit": metin[:600]}


def plan(model):
    rng = random.Random(7)
    ks = [(m, g, k, t) for m in ("haiku", "sonnet") for g in "abc" for k in "AB" for t in (1, 2)]
    rng.shuffle(ks)
    return [x for x in ks if model in (None, x[0])]


def biten():
    if not SONUC.exists():
        return set()
    return {(r["model"], r["gorev"], r["kol"], r["tekrar"]) for r in map(json.loads, SONUC.read_text(encoding="utf-8").splitlines())}


def kos(model, saniye, paralel):
    AB.mkdir(parents=True, exist_ok=True)
    kuyruk = [x for x in plan(model) if x not in biten()]
    bas = time.time()
    def is_(x):
        if time.time() - bas > saniye:
            return None
        r = koş(x)
        with open(SONUC, "a", encoding="utf-8") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(x, f"tur={r['tur']} usd={r['usd']:.3f} dogru={r['dogru']} hata={r['hata']} sn={r['sn']}", flush=True)
        return r
    with ThreadPoolExecutor(paralel) as ex:
        list(ex.map(is_, kuyruk))
    print("kalan:", len([x for x in plan(model) if x not in biten()]))


def ozet():
    rs = [json.loads(s) for s in SONUC.read_text(encoding="utf-8").splitlines()]
    for m in ("haiku", "sonnet"):
        for g in ("a", "b", "c", "*"):
            satir = {}
            for k in "AB":
                x = [r for r in rs if r["model"] == m and r["kol"] == k and g in (r["gorev"], "*")]
                if x:
                    n = len(x)
                    satir[k] = (n, sum(r["girdi"] + r["yaz"] + r["oku"] for r in x) / n, sum(r["cikti"] for r in x) / n,
                                sum(r["usd"] for r in x) / n, sum(r["tur"] for r in x) / n, sum(r["sn"] for r in x) / n, sum(r["dogru"] for r in x))
            if len(satir) == 2:
                A, B = satir["A"], satir["B"]
                print(f"{m:6} {g} n={A[0]}/{B[0]} girdi A={A[1]:.0f} B={B[1]:.0f} ({100 * (B[1] / A[1] - 1):+.0f}%) cikti A={A[2]:.0f} B={B[2]:.0f} "
                      f"usd A={A[3]:.3f} B={B[3]:.3f} ({100 * (B[3] / A[3] - 1):+.0f}%) tur A={A[4]:.1f} B={B[4]:.1f} sn A={A[5]:.0f} B={B[5]:.0f} dogru A={A[6]}/{A[0]} B={B[6]}/{B[0]}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "kos":
        g = lambda ad, v: type(v)(a[a.index(ad) + 1]) if ad in a else v
        kos(g("--model", "x") if "--model" in a else None, g("--saniye", 480), g("--paralel", 2))
    elif a and a[0] == "ozet":
        ozet()
    else:
        print(__doc__)
