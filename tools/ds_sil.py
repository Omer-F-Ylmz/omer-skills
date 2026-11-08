import shutil
import subprocess
from pathlib import Path

kok = Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored")
model = kok / "model"
subprocess.run(["taskkill", "/IM", "llama-server.exe", "/F"], capture_output=True)
once = shutil.disk_usage("C:\\").free / 2**30
silinen = []
for p in sorted(model.glob("*")):
    try:
        p.unlink()
        silinen.append(p.name)
    except Exception as e:
        silinen.append("HATA %s %r" % (p.name, e))
try:
    model.rmdir()
except Exception as e:
    silinen.append("klasor %r" % e)
sonra = shutil.disk_usage("C:\\").free / 2**30
ps = ("$c=Get-CimInstance Win32_ComputerSystem; $o=Get-CimInstance Win32_OperatingSystem; $p=Get-CimInstance Win32_Processor | Select-Object -First 1;"
      "'RAM ' + [math]::Round($c.TotalPhysicalMemory/1GB) + ' GB, bos ' + [math]::Round($o.FreePhysicalMemory/1MB,1) + ' GB';"
      "'CPU ' + $p.Name + ' cekirdek ' + $p.NumberOfCores + ' is parcacigi ' + $p.NumberOfLogicalProcessors;"
      "Get-CimInstance Win32_PhysicalMemory | ForEach-Object { 'DIMM ' + [math]::Round($_.Capacity/1GB) + ' GB ' + $_.ConfiguredClockSpeed + ' MT/s' }")
r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace", timeout=50)
g = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"], capture_output=True, text=True)
(kok / "sil_sonuc.txt").write_text("silinen %s\nbos once %.0f GB sonra %.0f GB\n%s\nGPU %s" % (silinen, once, sonra, r.stdout + r.stderr, g.stdout), encoding="utf-8")
