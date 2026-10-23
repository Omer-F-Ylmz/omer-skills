"""Code Mode (UTCP) sarmalayıcı — CODE-MODE-1.
Çok adımlı MCP zincirlerini TEK çağrıda koşar; ara sonuçlar modele dönmez, yalnız `return` edilen özet döner.
Kullanım:
  python tools/cm.py list                       # araç adları (manual.tool)
  python tools/cm.py search "<görev>"           # ilgili araçlar + TS arayüzleri
  python tools/cm.py info git.git_git_log       # tek araç arayüzü
  python tools/cm.py run dosya.js               # zinciri koş (JS gövde; araçlar senkron: git.git_git_log({...}); `return` ile özet)
  python tools/cm.py run -c "return gw.time_get_current_time({timezone:'Europe/Istanbul'})"
Notlar: kod düz JavaScript (TS tip açıklaması YOK); varsayılan zaman aşımı 60 sn (--timeout ms).
Yapılandırma: tools/code-mode/.utcp_config.json (MCP manual'ları)."""
import json, os, subprocess, sys

KOK = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(KOK, "code-mode")
CLI = os.path.join(D, "node_modules", "@utcp", "code-mode-cli", "dist", "index.js")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__); return 0
    a = list(argv)
    if a[0] == "run" and len(a) >= 2 and a[1] not in ("-c",) and not a[1].startswith("--") and os.path.isfile(a[1]):
        a = ["run", "--file", os.path.abspath(a[1])] + a[2:]
    if a[0] == "run" and "--timeout" not in a:
        a += ["--timeout", "60000"]
    r = subprocess.run(["node", CLI, *a, "--config", os.path.join(D, ".utcp_config.json")], cwd=D,
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    satirlar = [s for s in (r.stdout or "").splitlines() if s.strip() and not s.startswith(("[McpCommunicationProtocol]", "Calling tool", "Successfully registered", "UTCP Client closed"))]
    out = "\n".join(satirlar)
    try:
        j = json.loads(satirlar[-1]) if satirlar else None
        if isinstance(j, dict) and "result" in j:
            out = json.dumps({k: v for k, v in j.items() if not (k == "logs" and not v)}, ensure_ascii=False)
    except ValueError:
        pass
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(out)
    if r.returncode and r.stderr:
        hata = [s for s in r.stderr.splitlines() if not s.startswith(("[McpCommunicationProtocol]", "Calling tool", "Successfully registered", "UTCP Client closed"))]
        print("\n".join(hata)[-1500:], file=sys.stderr)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
