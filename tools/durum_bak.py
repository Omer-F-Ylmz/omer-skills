import subprocess
from pathlib import Path

kok = Path(r"C:\Projeler\omer-skills")
out = kok / ".kos" / "kopru" / "log" / "durum_bak.out.txt"
s = []
ps = ("Get-CimInstance Win32_Process -Filter \"Name='claude.exe' OR Name='node.exe'\" | Where-Object { $_.Name -eq 'claude.exe' -and $_.CommandLine -match ' -p ' } | "
      "ForEach-Object { \"$($_.ProcessId) $($_.CreationDate) \" + $_.CommandLine.Substring(0, [Math]::Min(160, $_.CommandLine.Length)) }")
r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace", timeout=50)
s.append("CLAUDE -p SURECLERI:\n" + (r.stdout.strip() or "yok"))
for p in [kok / ".kos/kopru/arka/cc-baslangic-token-1-ilerleme.md", kok / "rapor/cc-baslangic-token-1.md"]:
    s.append("%s: %s" % (p.name, p.read_text(encoding="utf-8")[-600:] if p.exists() else "YOK"))
out.write_text("\n".join(s), encoding="utf-8")
