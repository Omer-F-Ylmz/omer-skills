import os, shutil, psutil, time
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\pg_baslangic.log", "w", encoding="utf-8")
D = os.path.join(os.environ["USERPROFILE"], "Desktop", "Claude ile yap\u0131lanlar", "araclar", "postgres17-veri")
st = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup", "postgres17-baslat.cmd")
shutil.copy2(os.path.join(D, "_baslat.cmd"), st)
print("baslangic:", st, os.path.exists(st), file=out)
for q in psutil.process_iter(["pid", "cmdline"]):
    if "pg_kume.py" in " ".join(q.info["cmdline"] or []):
        q.kill(); print("takili pg_kume.py kapatildi", q.info["pid"], file=out)
time.sleep(2)
print("postgres surecleri hala:", len([q for q in psutil.process_iter(["name"]) if q.info["name"] == "postgres.exe"]), file=out)
t = r"C:\Projeler\omer-skills\rapor\yonetici-kur-sonuc.tsv"
s = open(t, encoding="utf-8").read().replace("omer-postgres17 gorevi baslatir; psql exit 1", "Baslangic klasorundeki postgres17-baslat.cmd baslatir; psql 'select version()' = PostgreSQL 17.11 (8 Kas 03:23)")
open(t, "w", encoding="utf-8").write(s)
print("tsv duzeltildi", file=out)
