import subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
def ps(c):
    r = subprocess.run(["powershell", "-NoProfile", "-Command", c], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.stdout + r.stderr).strip()
print("GPU:", ps("Get-CimInstance Win32_VideoController | ForEach-Object { $_.Name + ' | ' + $_.PNPDeviceID + ' | sürücü ' + $_.DriverVersion }"))
print("ANAKART:", ps("$b=Get-CimInstance Win32_BaseBoard; $b.Manufacturer + ' ' + $b.Product"))
print("BIOS:", ps("$x=Get-CimInstance Win32_BIOS; $x.Manufacturer + ' ' + $x.SMBIOSBIOSVersion"))
print("CPU:", ps("(Get-CimInstance Win32_Processor).Name"))
print("FIRMWARE:", ps("$env:firmware_type; (Get-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\SecureBoot\\State' -ErrorAction SilentlyContinue).UEFISecureBootEnabled"))
print("SMI:", ps("& 'nvidia-smi' --query-gpu=name,pci.device_id,vbios_version,driver_version --format=csv,noheader"))
print("DISK:", ps("Get-Partition | Where-Object { $_.GptType -eq '{c12a7328-f81f-11d2-ba4b-00a0c93ec93b}' } | ForEach-Object { 'ESP disk' + $_.DiskNumber + ' ' + [math]::Round($_.Size/1MB) + 'MB' }"))
