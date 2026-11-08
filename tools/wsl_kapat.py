import subprocess as s, psutil, time
s.run(["wsl", "--shutdown"], capture_output=True, timeout=60)
time.sleep(5)
open(r"C:\Projeler\omer-skills\.kos\kopru\log\wsl_kapat.log", "w", encoding="utf-8").write(f"RAM % {psutil.virtual_memory().percent}\n")
