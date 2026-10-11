"""TOKEN-7f-doğrula: yakalama vekili (47896) + kosucu kolları. Canlı ayara dokunmaz (yalnız --settings/--mcp-config/--add-dir).
  python t7f2.py sonda            → vekil 'kes' modunda (istek kaydı + 400; ücret 0): ETS true/false istek gövdesi özeti
  python t7f2.py olc <kol> <G..>  → vekil headroom'a (6767) iletir + kayıt; kosucu ile görev koşar (kol: hr-true | hr-false | birlesik)
Kayıt: anahtar/başlık değeri YOK — yalnız sayılar, araç türleri, anthropic-beta bayrakları."""
import http.client, http.server, json, os, shutil, sys, threading
from pathlib import Path
KOK = Path(r"C:\Projeler\omer-skills"); sys.path[:0] = [str(KOK / "tools" / "olcum")]
import kosucu

PORT, HR = 47896, ("127.0.0.1", 6767)
KAYIT = KOK / ".claude" / "t7f2_istek.jsonl"
BIR = KOK / ".claude" / "t7f2-birlesik"
KES = False


class V(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, *a):
        pass

    def do_GET(self):
        self._ilet(b"")

    def do_HEAD(self):
        self._ilet(b"")

    def do_POST(self):
        self._ilet(self.rfile.read(int(self.headers.get("content-length") or 0)))

    def _ozet(self, govde):
        try:
            j = json.loads(govde)
        except ValueError:
            return {"yol": self.path, "bayt": len(govde)}
        t = j.get("tools") or []
        ad = lambda x: str(x.get("name", ""))
        return {"yol": self.path, "model": j.get("model"), "bayt": len(govde), "arac": len(t),
                "defer": sum(1 for x in t if x.get("defer_loading")), "mcp": sum(1 for x in t if ad(x).startswith("mcp__")),
                "mcp_defer": sum(1 for x in t if ad(x).startswith("mcp__") and x.get("defer_loading")),
                "tur_ozel": sorted({str(x.get("type")) for x in t if x.get("type") and x.get("type") != "custom"}),
                "arac_kb": round(len(json.dumps(t)) / 1024, 1), "sistem_kb": round(len(json.dumps(j.get("system") or "")) / 1024, 1),
                "mesaj_kb": round(len(json.dumps(j.get("messages") or [])) / 1024, 1),
                "beta": self.headers.get("anthropic-beta", "")}

    def _ilet(self, govde):
        oz = self._ozet(govde) if govde else {"yol": self.path, "yontem": self.command}
        if KES and oz.get("arac"):  # count_tokens (ücretsiz) — istek gövdesi bellekte kalır, yazılmaz
            j = json.loads(govde); h = {k: v for k, v in self.headers.items() if k.lower() not in ("host", "connection", "content-length")}
            c = http.client.HTTPConnection(*HR, timeout=120)
            c.request("POST", "/v1/messages/count_tokens?beta=true", headers=h, body=json.dumps(
                {k: j[k] for k in ("model", "messages", "system", "tools", "tool_choice", "thinking") if k in j}).encode())
            r = c.getresponse(); oz["ct_durum"] = r.status
            oz["ct_jeton"] = json.loads(r.read() or b"{}").get("input_tokens") if r.status == 200 else None; c.close()
        if govde and not KES:
            try:
                ms = (json.loads(govde).get("messages") or [])[-1:]
                oz["tool_result_hata"] = [bool(b.get("is_error")) for m in ms for b in (m.get("content") or []) if isinstance(b, dict) and b.get("type") == "tool_result"]
            except (ValueError, AttributeError, TypeError):
                pass
        if KES:
            oz["durum"] = 400
            b = json.dumps({"type": "error", "error": {"type": "invalid_request_error", "message": "t7f2 yakala"}}).encode()
            self.send_response(400); self.send_header("content-type", "application/json"); self.send_header("content-length", str(len(b)))
            self.end_headers(); self.wfile.write(b)
        else:
            c = http.client.HTTPConnection(*HR, timeout=600)
            h = {k: v for k, v in self.headers.items() if k.lower() not in ("host", "connection", "content-length")}
            c.request(self.command, self.path, body=govde or None, headers=h)
            r = c.getresponse(); oz["durum"] = r.status
            self.send_response(r.status)
            for k, v in r.getheaders():
                if k.lower() not in ("transfer-encoding", "connection", "content-length"):
                    self.send_header(k, v)
            self.end_headers()
            while (p := r.read1(65536)) if hasattr(r, "read1") else (p := r.read(65536)):
                self.wfile.write(p); self.wfile.flush()
            c.close()
        with KAYIT.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"etiket": os.environ.get("T7F2_ETIKET", ""), **oz}, ensure_ascii=False) + "\n")


def vekil():
    s = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), V)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def ayar(ets, ek_ayar=None):
    return ["--settings", json.dumps({**(ek_ayar or {}), "env": {"ANTHROPIC_BASE_URL": f"http://127.0.0.1:{PORT}", "ENABLE_TOOL_SEARCH": ets}})]


def birlesik_ek():
    """B2 aile ağacı (.claude/b2-aile) + TUR-6d aileleri + 6d stdio MCP; ayar = b2-aile skillOverrides + false + vekil."""
    sys.path.insert(0, str(KOK / ".kos" / "kopru" / "onay"))
    import tur_6d_kur as D
    if not BIR.exists():
        shutil.copytree(KOK / ".claude" / "b2-aile", BIR)
        for zp, _ in D._adaylar():
            D.B.aile_ac(zp, BIR / ".claude" / "skills")
        m = json.loads((BIR / "mcp.json").read_text(encoding="utf-8"))
        m["mcpServers"].update({a: {"type": "stdio", **v} for a, v in D.MCP_STDIO.items()})
        (BIR / "mcp.json").write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    ov = json.loads((BIR / "settings.json").read_text(encoding="utf-8"))
    y = BIR / "ayar-olcum.json"; y.write_text(ayar("false", ov)[1], encoding="utf-8")  # komut satırı 32k sınırı (WinError 206)
    return ["--add-dir", str(BIR), "--mcp-config", str(BIR / "mcp.json"), "--settings", str(y)]


if __name__ == "__main__":
    KAYIT.touch()
    if sys.argv[1] == "sonda":
        KES = True; vekil()
        for v in sys.argv[2:] or ["true", "false"]:
            os.environ["T7F2_ETIKET"] = f"ct-{v}"
            o = kosucu.kos("Yalnız ok yaz.", ek=birlesik_ek() if v == "birlesik" else ayar(v), butce=0.5, timeout=240)
            t = (o["init"] or {}).get("tools") or []
            print(v, "init_arac", len(t), "mcp", sum(1 for x in t if str(x).startswith("mcp__")), "rc", o["rc"], "usd", o["usd"], flush=True)
    else:
        kol, ids = sys.argv[2], sys.argv[3:]
        vekil(); os.environ["T7F2_ETIKET"] = kol
        ek = birlesik_ek() if kol == "birlesik" else ayar(kol.split("-")[1])
        g = {x["id"]: x for x in json.loads((kosucu.DIZIN / "gorevler.json").read_text(encoding="utf-8"))}
        kosucu.CIKTI.mkdir(parents=True, exist_ok=True)
        kosucu.kos_profil(f"t7f2-{kol}", {"ek": ek}, [g[i] for i in ids], "2026-10-11", 1)
