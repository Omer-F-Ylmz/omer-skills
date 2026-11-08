import psutil, time
anahtar = ["egit_surekli", "borsa egit", "sikistir_tum", "aday2_ara", "gece_kuyruk", "apt-get install"]
ps = []
for p in psutil.process_iter(["pid", "cmdline", "status"]):
    try:
        c = " ".join(p.info["cmdline"] or [])
        for a in anahtar:
            if a in c:
                p.cpu_percent(None)
                ps.append((a, p))
    except Exception:
        pass
time.sleep(3)
for a, p in ps:
    try:
        print(a, "|", p.status(), "| cpu", p.cpu_percent(None), "| ram", round(p.memory_info().rss / 2**20), "MB")
    except Exception as e:
        print(a, "| bitti/erisilemedi", type(e).__name__)
bul = {a for a, _ in ps}
for a in anahtar:
    if a not in bul:
        print(a, "| SUREC YOK")
