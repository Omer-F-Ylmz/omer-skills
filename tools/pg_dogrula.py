import subprocess as s, os, time, sys, psutil
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\pg_dogrula.log", "w", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=out)
B = r"C:\Program Files\PostgreSQL\17\bin"
D = os.path.join(os.environ["USERPROFILE"], "Desktop", "Claude ile yap\u0131lanlar", "araclar", "postgres17-veri")
p("postgres surecleri:", len([q for q in psutil.process_iter(["name"]) if q.info["name"] == "postgres.exe"]))
p("pg_kume.py takili:", [q.pid for q in psutil.process_iter(["cmdline"]) if "pg_kume.py" in " ".join(q.info["cmdline"] or [])])
with open(os.path.join(D, "_psql_test.txt"), "w", encoding="utf-8") as f:
    r = s.run([os.path.join(B, "psql.exe"), "-h", "localhost", "-U", "postgres", "-At", "-c", "select version();"], stdout=f, stderr=s.STDOUT, timeout=30)
p("psql exit", r.returncode, open(os.path.join(D, "_psql_test.txt"), encoding="utf-8", errors="ignore").read().strip()[:200])
bat = os.path.join(D, "_baslat.cmd")
open(bat, "w", encoding="ascii", errors="ignore").write(f'@echo off\r\n"{B}\\pg_ctl.exe" -D "{D}" -l "{D}\\sunucu.log" start\r\n'.encode("cp1254", "ignore").decode("ascii", "ignore") if False else "")
with open(bat, "w", encoding="cp1254") as f:
    f.write(f'@echo off\r\n"{B}\\pg_ctl.exe" status -D "{D}" >nul 2>&1 || "{B}\\pg_ctl.exe" -D "{D}" -l "{D}\\sunucu.log" start\r\n')
r = s.run(["schtasks", "/Create", "/TN", "omer-postgres17", "/TR", f'"{bat}"', "/SC", "ONLOGON", "/RL", "LIMITED", "/F"], capture_output=True, text=True, errors="ignore", timeout=60)
p("gorev:", r.returncode, (r.stdout + r.stderr).strip()[:300])
with open(r"C:\Projeler\omer-skills\rapor\yonetici-kur-sonuc.tsv", "a", encoding="utf-8") as t:
    t.write(f"PostgreSQL.PostgreSQL.17\tKURULDU-KULLANICI-KUMESI\tEDB initdb 'Turkish_Turkiye.1254 non-ASCII locale' ile coktu; kullanici kumesi {D} (locale C, UTF8, trust yalniz localhost), oturum acilisinda omer-postgres17 gorevi baslatir; psql exit {r.returncode}\n")
p("BITTI")
