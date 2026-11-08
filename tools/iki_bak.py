import subprocess as s, os, glob, time
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\iki_bak.log", "w", encoding="utf-8", buffering=1)
q = ("Get-Process | ? { $_.ProcessName -match 'postgres|initdb|pg_ctl|psql|install|cuda|python' } | "
     "% { '{0} {1} cpu={2:N0}s ram={3}MB basla={4}' -f $_.Id,$_.ProcessName,$_.CPU,[int]($_.WorkingSet64/1MB),$_.StartTime.ToString('HH:mm') }")
print(s.run(["powershell", "-NoProfile", "-Command", q], capture_output=True, text=True, errors="ignore", timeout=60).stdout, file=out)
for d in [r"C:\Program Files\PostgreSQL\17\bin\postgres.exe", r"C:\Program Files\PostgreSQL\17\data\PG_VERSION"]:
    print(d, os.path.exists(d), file=out)
t = os.environ["TEMP"]
for f in sorted(glob.glob(t + r"\install-postgresql*.log") + glob.glob(t + r"\bitrock*.log") + glob.glob(t + r"\*postgres*.log"), key=os.path.getmtime)[-2:]:
    print("=====", f, time.strftime("%H:%M", time.localtime(os.path.getmtime(f))), file=out)
    print("\n".join(open(f, encoding="utf-8", errors="ignore").read().splitlines()[-25:]), file=out)
q2 = "Get-CimInstance Win32_Process | ? { $_.CommandLine -match 'envanter_tara' } | % { $_.ProcessId }"
pid = s.run(["powershell", "-NoProfile", "-Command", q2], capture_output=True, text=True, timeout=60).stdout.split()
print("envanter_tara pid", pid, file=out)
print("BITTI", file=out)
