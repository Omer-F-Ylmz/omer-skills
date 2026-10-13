"""MCP-HAFIF-2 d6 onay betiği (Desktop koşar): CC Serena MCP her açılışta `uvx --from git+…@v1.7.0` ile git çekip ortam
çözüyor. `uv tool install` ile aynı etiketi bir kez kurar, ~/.claude.json girdisini kurulu serena.exe'ye çevirir.
d6 ölçümü (docs/kutuphane/olcum/mcp-hafif-2-d6.jsonl): açılış 22.8–34.1 sn → 6.7–9.9 sn (ilk soğuk koşu 31.3), ağaç RAM
187 → 134 MB, süreç 6 → 4, 30 araç eşit. Desktop yapılandırmasında Serena yok.
  python onay/mcp_hafif_2_serena.py --kuru   # varsayılan: yalnız PLAN
  python onay/mcp_hafif_2_serena.py uygula   # kurar, araç listesi uvx == sabit ise yazar
  python onay/mcp_hafif_2_serena.py --geri   # girdiyi uvx'e döndürür + uv tool uninstall serena"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "olcum"))
from mcp_acilis import GIZLI, kos  # noqa: E402

CJ = Path.home() / ".claude.json"
KAYNAK = "git+https://github.com/oraios/serena@v1.7.0"
UVX = {"command": "uvx", "args": ["--from", KAYNAK, "serena", "start-mcp-server"]}
EXE = Path.home() / ".local" / "bin" / "serena.exe"
SABIT = {"command": str(EXE), "args": ["start-mcp-server"]}
DAMGA = time.strftime("%Y%m%d-%H%M%S")


def oku():
    return json.loads(CJ.read_text(encoding="utf-8-sig"))


def yaz(d, eki):
    shutil.copy2(CJ, CJ.with_name(f".claude.json.bak-{eki}-{DAMGA}"))
    metin = json.dumps(d, ensure_ascii=False, indent=2)
    json.loads(metin)
    CJ.write_text(metin, encoding="utf-8")


def girdi_ile(d, yeni):
    s = dict(d["mcpServers"]["serena"])
    s.update(yeni)
    return s


def main(kip):
    d = oku()
    s = d["mcpServers"]["serena"]
    print(f"şimdi: {s.get('command')} {' '.join(s.get('args', []))} · serena.exe {'VAR' if EXE.exists() else 'YOK'}")
    if kip == "--geri":
        d["mcpServers"]["serena"] = girdi_ile(d, UVX)
        yaz(d, "serena-geri")
        subprocess.run(["uv", "tool", "uninstall", "serena"], capture_output=True, creationflags=GIZLI)
        print("geri alındı: uvx girdisi · uv tool uninstall serena")
        return
    if s.get("command") != "uvx" or KAYNAK not in s.get("args", []):
        print("ATLA: girdi beklenen uvx biçiminde değil")
        return
    if kip != "uygula":
        print(f"PLAN: uv tool install {KAYNAK} → {EXE} · serena girdisi → {SABIT['command']} start-mcp-server · "
              "yazmadan önce uvx/sabit araç listesi eşitliği")
        return
    k = subprocess.run(["uv", "tool", "install", KAYNAK], capture_output=True, text=True, creationflags=GIZLI)
    if k.returncode and not EXE.exists():
        raise SystemExit(f"uv tool install rc {k.returncode}: {k.stderr[-300:]}")
    a, b = kos(["uvx", "--from", KAYNAK, "serena", "start-mcp-server"]), kos([str(EXE), "start-mcp-server"])
    if a.get("durum") != "OK" or a.get("araclar") != b.get("araclar"):
        raise SystemExit(f"araç listesi eşit değil (uvx {a.get('durum')} {len(a.get('araclar') or [])}, sabit "
                         f"{b.get('durum')} {len(b.get('araclar') or [])}) — yazılmadı")
    adlar = sorted(d["mcpServers"])
    d = oku()  # CC arada yazmış olabilir
    d["mcpServers"]["serena"] = girdi_ile(d, SABIT)
    yaz(d, "serena")
    assert sorted(oku()["mcpServers"]) == adlar
    print(f"uygulandı: serena → {EXE} · {len(b['araclar'])} araç eşit · açılış {a['tools']} → {b['tools']} sn · "
          f"RAM {a['ram_mb']} → {b['ram_mb']} MB · MCP listesi önce=sonra ({len(adlar)}) · yeni CC oturumunda geçerli")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1] if len(sys.argv) > 1 else "--kuru")
