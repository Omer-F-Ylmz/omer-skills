"""Salt-okur: claude -p oturumlarını (başlangıç saati, bellek, cwd ipucu) ve RAM yüzdesini listeler. Hiçbir şeyi değiştirmez."""
import json, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
ps = ("$o = Get-CimInstance Win32_OperatingSystem; "
      "$r = [math]::Round(100 - $o.FreePhysicalMemory / $o.TotalVisibleMemorySize * 100); "
      "$p = Get-CimInstance Win32_Process -Filter \"Name='claude.exe'\" | "
      "Select-Object ProcessId,ParentProcessId,@{n='Bas';e={$_.CreationDate.ToString('HH:mm:ss')}},"
      "@{n='MB';e={[math]::Round($_.WorkingSetSize/1MB)}},CommandLine; "
      "@{ram=$r; p=@($p)} | ConvertTo-Json -Compress -Depth 4")
out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True,
                     encoding="utf-8", errors="replace", creationflags=0x08000000).stdout
d = json.loads(out, strict=False)
print("RAM %", d["ram"])
n = 0
for p in d["p"] or []:
    c = (p.get("CommandLine") or "").replace("\n", " ")
    if " -p" not in c:
        continue
    n += 1
    print(p["ProcessId"], p["Bas"], f'{p["MB"]}MB', "opus" if "opus" in c else "", c[:140])
print("claude -p oturumu:", n)
from durum_ozet import PROJ, durma_satiri  # noqa: E402 — aynı dizin; çalışan/son oturum = en yeni transkript
print(durma_satiri(PROJ.glob("*/*.jsonl")))
