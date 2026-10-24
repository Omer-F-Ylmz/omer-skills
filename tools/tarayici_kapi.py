"""TARAYICI-KAPI-1: PreToolUse (Bash|PowerShell) kancası — varsayılan tarayıcıyı (Opera) açan komutları engeller (K2q).
Engel: stderr'e Türkçe gerekçe + çıkış 2. İzin: çıkış 0. Girdi yoksa/bozuksa sessizce izin."""
import json
import re
import sys

URL = r"""['"]?https?:"""
KALIPLAR = (
    (r"\bstart(\.exe)?\s+(\"\"\s+|''\s+)?" + URL, "start <url> varsayılan tarayıcıyı açar"),
    (r"\bexplorer(\.exe)?\s+" + URL, "explorer <url> varsayılan tarayıcıyı açar"),
    (r"\bcmd(\.exe)?\s+/c\s+start\b", "cmd /c start varsayılan uygulamayı/tarayıcıyı açar"),
    (r"\bwebbrowser\.open|-m\s+webbrowser\b", "webbrowser varsayılan tarayıcıyı açar"),
    (r"\bos\.startfile\b", "os.startfile varsayılan tarayıcıyı açabilir"),
    (r"\b(vite|webpack|webpack-dev-server|parcel|astro|nuxt|next|ng\s+serve|live-server|http-server|serve|npm|pnpm|yarn|npx|bun)\b[^\r\n]*\s--open\b",
     "dev server --open tarayıcı açar"),
    (r"\bgh\s+browse\b", "gh browse tarayıcı açar"),
    (r"\bnpm\s+docs\b", "npm docs tarayıcı açar"),
    (r"\bStart-Process\b[^\r\n]*" + URL, "Start-Process <url> varsayılan tarayıcıyı açar"),
)
INSPECTOR = "@modelcontextprotocol/inspector"


def karar(komut):
    """Engel gerekçesi (str) ya da None."""
    if INSPECTOR in komut and not re.search(r"(^|\s)--cli\b", komut):
        return "MCP Inspector arayüz kipi tarayıcı açar; yalnız --cli kipi serbest"
    for kalip, neden in KALIPLAR:
        if re.search(kalip, komut, re.I):
            return neden
    return None


def main():
    try:
        komut = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))["tool_input"]["command"]
    except Exception:
        return 0
    neden = karar(komut or "")
    if not neden:
        return 0
    sys.stderr.buffer.write(
        f"DUR (TARAYICI-KAPI-1): {neden}. Varsayılan tarayıcı Opera; sayfa gerekirse playwright headless ya da Claude in Chrome kullan.\r\n".encode("utf-8"))
    sys.stderr.buffer.flush()
    return 2


if __name__ == "__main__":
    sys.exit(main())
