"""d2a A/B: ajan profili sabit bağlamı, taban (A) ↔ bağlam-diyeti (B: superpowers/ponytail/context-mode kapalı, claude-mem gözlem 5).
Her kol: 1 claude -p (proxy, 'tamam' → sabit bağlam) + 1 claude -p (görev testi, 'kur' beklenir). Kurulu ayara dokunmaz (geçici --settings).
  python d2a_ab.py → d2a_ab.json"""
import json, os, subprocess, sys, threading
import taban as t
a6, ok, cc_profil = t.a6, t.ok, t.cc_profil

KOLLAR = {
    "A_taban": {},
    "B_diyet": {"enabledPlugins": {"superpowers@claude-plugins-official": False, "ponytail@ponytail": False,
                                   "context-mode@context-mode": False},
                "env": {"CLAUDE_MEM_CONTEXT_OBSERVATIONS": "5"}},
}
GOREV = "tools/cc_profil.py dosyasının 24. satırında tanımlı fonksiyonun adını yalnız tek kelime yaz."


def argv_kur(ek, proxy_port=None, gecici="p"):
    ayar = json.loads(json.dumps(ek))
    if proxy_port:
        ayar.setdefault("env", {})["ANTHROPIC_BASE_URL"] = f"http://127.0.0.1:{proxy_port}"
    a, e = cc_profil.kur("ajan", ek_ayar=ayar, gecici=ok.DIZ.parent / gecici)
    return [r"C:\Users\pc\.local\bin\claude.exe", "-p", "--output-format", "json", "--model", "opus",
            "--disable-slash-commands", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', *a], e


def kos(argv, e, girdi):
    p = subprocess.run(argv, input=girdi.encode(), capture_output=True, cwd=str(t.KOK), env={**os.environ, **e},
                       creationflags=t.NW, timeout=300)
    return p.stdout.decode("utf-8", "replace")


ok.etiket = "d2a"; ok.DIZ.mkdir(parents=True, exist_ok=True)
s = ok.http.server.ThreadingHTTPServer(("127.0.0.1", 0), a6.V)
threading.Thread(target=s.serve_forever, daemon=True).start()
sonuc = {}
for kol, ek in KOLLAR.items():
    a6.yakala.clear()
    argv, e = argv_kur(ek, s.server_port, "p_" + kol)
    kos(argv, e, "Yalnız 'tamam' yaz, araç kullanma.")
    t.GOVDE, t.BASLIK = json.loads(a6.yakala["govde"]), a6.yakala["baslik"]
    r = t.m_profil()
    argv, e = argv_kur(ek, None, "p_" + kol)
    c = kos(argv, e, GOREV)
    try:
        j = json.loads(c); yanit = str(j.get("result", "")).strip(); mal = j.get("total_cost_usd")
    except Exception:  # noqa: BLE001
        yanit, mal = c[:80], None
    r["gorev_yanit"] = yanit; r["gorev_dogru"] = int(yanit.strip("`'\". ").lower() == "kur"); r["gorev_usd"] = mal
    sonuc[kol] = r
    print(kol, r, flush=True)
json.dump(sonuc, open(t.BU / "d2a_ab.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
