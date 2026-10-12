"""MCP-HAFIF-2 hedef 2 (salt okur): canlı claude oturumlarının doğrudan çocukları (MCP sunucuları, hook kabukları, iç claude)
imzaya göre (görüntü adı + ilk iki argümanın dosya adı) gruplanır: kopya sayısı ve alt ağaç WorkingSet toplamı. Aynı imzanın
oturum sayısı kadar kopyası = paylaşım adayı. Komut satırı/env yazdırılmaz; anahtar/token/= içeren argüman imzaya girmez.
  python tools/olcum/mcp_kopya.py [cikti.tsv]"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kosucu  # noqa: E402
from mcp_hafif_kabul import torunlar  # noqa: E402

GIZLI = re.compile(r"(?i)key|token|secret|pass|=")


def anlik():
    ps = ("Get-CimInstance Win32_Process | ForEach-Object { [pscustomobject]@{p=$_.ProcessId;pp=$_.ParentProcessId;"
          "a=$_.Name;r=$_.WorkingSetSize;k=$_.CommandLine} } | ConvertTo-Json -Compress")
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], capture_output=True,
                       encoding="utf-8", errors="replace", creationflags=kosucu.PENCERESIZ, timeout=120)
    # PS 5.1 komut satırındaki denetim karakterini kaçırmıyor → strict=False
    return {x["p"]: (x["pp"], x["a"] or "", x["r"] or 0, x["k"] or "") for x in json.loads(r.stdout, strict=False)}


def imza(ad, komut):
    t, atla = [], False
    for x in re.findall(r'"[^"]*"|\S+', komut)[1:]:  # "-bayrak değer": değer (sır olabilir) de atlanır
        if not atla and not x.startswith(("-", "/")):
            t.append(x)
        atla = x.startswith("-") and "=" not in x
    t = [re.split(r"[\\/]", x.strip('"').rstrip("\\/"))[-1] for x in t if not GIZLI.search(x)]
    return " ".join([ad.lower(), *t[:2]])


def say(d):
    """→ ({imza: [kopya, toplam bayt]}, kök oturum sayısı); kök = ebeveyni claude olmayan claude.exe."""
    claude = {p for p, v in d.items() if v[1].lower() == "claude.exe"}
    agac = {p: v[:3] for p, v in d.items()}  # torunlar() (ppid, ad, ram) bekler
    kokler = [k for k in claude if d[k][0] not in claude]
    out = {}
    for kok in kokler:
        for c in (p for p, v in d.items() if v[0] == kok):
            s = out.setdefault(imza(d[c][1], d[c][3]), [0, 0])
            s[0] += 1
            s[1] += d[c][2] + sum(d[t][2] for t in torunlar(agac, c))
    return out, len(kokler)


if __name__ == "__main__":
    assert imza("uvx.exe", r'"C:\x\uvx.exe" mcp-server-git --repository .') == "uvx.exe mcp-server-git"
    assert imza("cmd.exe", r"cmd /c C:\P\tools\mcp-launch\fetch.cmd API_KEY=x") == "cmd.exe fetch.cmd"
    assert imza("node.exe", r"node C:\a\b\index.js --token abc") == "node.exe index.js"
    sahte = {1: (0, "claude.exe", 100, ""), 2: (1, "uvx.exe", 10, "uvx mcp-server-git"), 3: (2, "python.exe", 5, ""),
             4: (0, "claude.exe", 100, ""), 5: (4, "uvx.exe", 10, "uvx mcp-server-git")}
    assert say(sahte) == ({"uvx.exe mcp-server-git": [2, 25]}, 2)
    if len(sys.argv) < 2:
        print("ok")
        sys.exit()
    sayim, oturum = say(anlik())
    satir = sorted(sayim.items(), key=lambda x: -x[1][1])
    Path(sys.argv[1]).write_text("imza\tkopya\tmb\n" + "".join(f"{a}\t{k}\t{b / 2**20:.0f}\n" for a, (k, b) in satir),
                                 encoding="utf-8")
    print(f"kök claude {oturum} · çocuk toplamı {sum(b for _, b in sayim.values()) / 2**20:.0f} MB")
    for a, (k, b) in satir[:25]:
        print(f"{k}\t{b / 2**20:.0f}\t{a}")
