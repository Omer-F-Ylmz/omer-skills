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


GURULTU = ("[McpCommunicationProtocol]", "Calling tool", "Successfully registered", "UTCP Client closed")


def suz(metin, json_ozet=True):
    """CLI çıktısından protokol gürültüsünü ayıklar; son satır {result,...} JSON ise boş `logs` düşer."""
    satirlar = [s for s in (metin or "").splitlines() if s.strip() and not s.startswith(GURULTU)]
    out = "\n".join(satirlar)
    if json_ozet:
        try:
            j = json.loads(satirlar[-1]) if satirlar else None
            if isinstance(j, dict) and "result" in j:
                out = json.dumps({k: v for k, v in j.items() if not (k == "logs" and not v)}, ensure_ascii=False)
        except ValueError:
            pass
    return out


def kisa_search(metin, en=8):
    """search ciktisi (~12k karakter, TS arayuzleri) -> ad + 100 karakter aciklama. Tam hali: search ... --tam"""
    try:
        j = json.loads(metin)
    except ValueError:
        return metin
    if not isinstance(j, dict) or not isinstance(j.get("tools"), list):
        return metin
    satir = [f"{t.get('name')} — {(t.get('description') or '')[:100]}" for t in j["tools"][:en]]
    return "\n".join(satir) + "\n(arayuz: cm.py info <ad> · tam liste: search ... --tam)"


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__); return 0
    a = list(argv)
    if a[0] == "run" and len(a) >= 2 and a[1] not in ("-c",) and not a[1].startswith("--") and os.path.isfile(a[1]):
        a = ["run", "--file", os.path.abspath(a[1])] + a[2:]
    tam = "--tam" in a
    if tam:
        a.remove("--tam")
    if a[0] == "run" and "--timeout" not in a:
        a += ["--timeout", "60000"]
    r = subprocess.run(["node", CLI, *a, "--config", os.path.join(D, ".utcp_config.json")], cwd=D,
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "gh_GITHUB_PAT": os.environ.get("GITHUB_PAT", "")},  # UTCP değişkeni manual adıyla önekler (gh_)
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cikti = suz(r.stdout)
    print(kisa_search(cikti) if a[0] == "search" and not tam else cikti)
    if r.returncode and r.stderr:
        print(suz(r.stderr, json_ozet=False)[-1500:], file=sys.stderr)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
