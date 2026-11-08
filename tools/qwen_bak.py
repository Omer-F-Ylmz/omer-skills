import subprocess
from pathlib import Path

ps = ("Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*qwen_kur*' -or $_.CommandLine -like '*Qwen3.6-35B*' -or $_.Name -eq 'llama-server.exe' } | "
      "ForEach-Object { \"$($_.ProcessId) $($_.Name) $($_.CreationDate) \" + $_.CommandLine.Substring(0,[Math]::Min(140,$_.CommandLine.Length)) };"
      "$o=Get-CimInstance Win32_OperatingSystem; 'RAM bos GB ' + [math]::Round($o.FreePhysicalMemory/1MB,1)")
r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace", timeout=50)
p = Path(r"C:\Users\pc\Desktop\Yerel Sansursuz Model\model\Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved-Q4_K_S.gguf")
Path(r"C:\Users\pc\Desktop\Yerel Sansursuz Model\bak.txt").write_text(r.stdout + r.stderr + "\nboyut %d" % p.stat().st_size, encoding="utf-8")
