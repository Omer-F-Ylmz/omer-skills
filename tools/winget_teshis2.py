import subprocess as s, time, os, glob, stat
LOG = open(r"C:\Projeler\omer-skills\.kos\kopru\log\winget_teshis2.log", "w", encoding="utf-8", buffering=1)
la = os.environ["LOCALAPPDATA"]
for f in glob.glob(la + r"\Packages\Microsoft.DesktopAppInstaller_*\LocalState\**\*", recursive=True)[:400]:
    try:
        if os.path.isfile(f) and (f.endswith((".db", ".msix", ".json", "index.db")) or os.path.getsize(f) > 1e6):
            a = os.stat(f).st_file_attributes
            print(f.replace(la, "%LA%")[-110:], int(os.path.getsize(f)/1e6), "MB", "REPARSE" if a & 0x400 else "-", "COMP" if a & 0x800 else "-", file=LOG)
    except Exception as e: print(f, e, file=LOG)
q = "Get-CimInstance Win32_Process | ? { $_.Name -match 'winget|WindowsPackageManagerServer|AppInstaller' } | % { '{0} {1} {2}dk ebeveyn={3} {4}' -f $_.ProcessId,$_.Name,[int]((Get-Date)-$_.CreationDate).TotalMinutes,$_.ParentProcessId,(($_.CommandLine -replace '\s+',' ') -replace '^(.{0,160}).*','$1') }"
print(s.run(["powershell", "-NoProfile", "-Command", q], capture_output=True, text=True, errors="ignore", timeout=60).stdout, file=LOG)
print("BITTI", file=LOG)
