import sys, json, subprocess, os
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "tools")
import ucretsiz_havuz as h
E = "tools/envanter_tara.py"
env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
def run(*a):
    return subprocess.run([sys.executable, "-I", "-S", E, *a], capture_output=True, text=True, encoding="utf-8", env=env, timeout=120).stdout
JOBS = ["İLİK 3D ürün sahnesi: Blender ile parfüm şişesi render + web sitesi hero animasyonu", "borsa botu: BIST verisi çek, strateji geri-test et, günlük rapor üret"]
T = "Aşağıdaki araç/kaynak bağlamıyla şu iş için en çok 12 maddelik uygulama planı yaz (her adımda hangi araç/kaynak kullanılacağı belirt). İş: {j}\n\nBAĞLAM:\n{c}"
out = []
for j in JOBS:
    brief, tam = run(j, "--brief"), run(j)
    pb = h.cagir("orta", T.format(j=j, c=brief), max_tokens=1800)[0]
    pt = h.cagir("orta", T.format(j=j, c=tam), max_tokens=1800)[0]
    ctx = run(j, "--brief")  # hakem de tam bağlamı görür
    for sira in (0, 1):  # konum yanlılığını gidermek için iki sıra
        A, B = (pb, pt) if sira == 0 else (pt, pb)
        q = f"İş: {j}\nİki plan var. Hangi araç/kaynak eşlemesi daha isabetli ve uygulanabilir? Yalnız JSON: {{\"kazanan\":\"A|B|esit\",\"neden\":\"<=20 kelime\"}}\n\nPLAN A:\n{A}\n\nPLAN B:\n{B}"
        r = h.cagir("hakem", q, max_tokens=400, haric_aile=None)
        out.append((j[:20], "brief=A" if sira == 0 else "brief=B", (r[0] or "")[:200], r[1]))
        print(out[-1], flush=True)
    print("jeton bayt brief/tam", len(brief), len(tam), "plan", len(pb or ""), len(pt or ""), flush=True)
