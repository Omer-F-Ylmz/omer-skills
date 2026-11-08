import subprocess as s, time
LOG = open(r"C:\Projeler\omer-skills\.kos\kopru\log\defrag_dur.log", "w", encoding="utf-8", buffering=1)
def r(a, t=60):
    p = s.run(a, capture_output=True, timeout=t)
    print(time.strftime("%H:%M:%S"), " ".join(a)[-80:], "| exit", p.returncode, "|", (p.stdout + p.stderr).decode("cp857", "ignore").strip()[:600], file=LOG)
r(["sc", "query", "defragsvc"])
r(["powershell", "-NoProfile", "-Command", "Get-ScheduledTask -TaskPath '\\Microsoft\\Windows\\Defrag\\' | % { $_.TaskName + ' ' + $_.State }; Get-ScheduledTaskInfo -TaskPath '\\Microsoft\\Windows\\Defrag\\' -TaskName ScheduledDefrag | % { 'son ' + $_.LastRunTime + ' sonraki ' + $_.NextRunTime }"])
r(["schtasks", "/end", "/tn", r"\Microsoft\Windows\Defrag\ScheduledDefrag"])
r(["sc", "stop", "defragsvc"])
time.sleep(8)
r(["sc", "query", "defragsvc"])
r(["powershell", "-NoProfile", "-Command", "$o=Get-CimInstance Win32_OperatingSystem; [int](100-($o.FreePhysicalMemory/$o.TotalVisibleMemorySize*100))"])
print("BITTI", file=LOG)
