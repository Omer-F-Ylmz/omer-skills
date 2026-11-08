import psutil, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
K = r"C:\Projeler\omer-skills"
canli = {}
for p in psutil.process_iter(["pid", "cmdline"]):
    try:
        c = " ".join(p.info["cmdline"] or [])
        for a in ["sira9b_0811", "sira9a_0811", "sira8_0811", "sira3_devam"]:
            if a in c: canli.setdefault(a, []).append(p.pid)
    except Exception:
        pass
print("canli", canli, "RAM", psutil.virtual_memory().percent)
for f in [r"tmp\sira9b-0811.tsv", r"tmp\sira9a-0811.tsv", r"tmp\sira8-hakem-0811.tsv", r"tmp\bulunan-0811.tsv"]:
    p = os.path.join(K, f)
    if os.path.exists(p):
        print(f, sum(1 for _ in open(p, encoding="utf-8", errors="replace")), time.strftime("%H:%M", time.localtime(os.path.getmtime(p))))
print("9b ilerleme", open(os.path.join(K, r"tmp\sira9b-ilerleme-0811.txt"), encoding="utf-8", errors="replace").read()[-120:] if os.path.exists(os.path.join(K, r"tmp\sira9b-ilerleme-0811.txt")) else "yok")
with open(os.path.join(K, r".kos\kopru\beyin-olay.jsonl"), encoding="utf-8", errors="replace") as h:
    for i, l in enumerate(h, 1):
        if i == 8681:
            m = re.sub(r"([A-Za-z0-9_\-]{6})[A-Za-z0-9_\-]{14,}", r"\1<...>", l)
            print("8681:", m[:700])
            uzun = re.findall(r"[A-Za-z0-9_\-]{20,}", l)
            print("uzun token sayisi", len(uzun), "ornek bas", [u[:6] for u in uzun[:8]])
            break
