"""VIDEO-IZLE-KUR-1 adim 3: tur<N>.tsv icindeki repolu kalemleri klonla + SkillSpector/gitleaks/semgrep (kurulum_v1_d2_tara.py uyarlamasi).
Devam edebilir: var olan <ad>.ss/.gl/.sg.json yeniden üretilmez, sonuc.tsv'de satırı olan aday atlanır. Semgrep sırayla (RAM).
Kullanım: python -I -X utf8 video_izle_kur_1_tara.py <yeni_bos_calisma_dizini> <tur.tsv>   (arka plan: .kos/kopru/arka.py ile)
Çıktı: <calisma_dizini>/sonuc.tsv (ad, repo, lisans, SS_HIGH, SS_toplam, gitleaks, semgrep, boyut)"""
import csv, json, os, re, subprocess, sys, time
import psutil
from pathlib import Path

W = sys.argv[1]
TUR = sys.argv[2]
ENV = {**os.environ, "PYTHONUTF8": "1", "GIT_LFS_SKIP_SMUDGE": "1"}
S = os.path.join(W, "sonuc.tsv")


aday = [x for x in csv.reader(open(TUR, encoding="utf-8"), delimiter="	")][1:]
aday = [[x[0], "", "", x[3]] for x in aday if x[3].strip()]
bitti = {l.split("\t")[0] for l in open(S, encoding="utf-8")} if os.path.exists(S) else set()


def run(cmd, t=300):
    # subprocess.run zaman aşımında yalnız çocuğu öldürür; torun (semgrep-core) boruyu tutup communicate'i asar
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8",
                             errors="replace", env=ENV, creationflags=0x08000000)
    except Exception as e:
        return -1, str(e)
    try:
        o, _ = p.communicate(timeout=t)
        return p.returncode, o
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, creationflags=0x08000000)
        return -1, "ZAMAN AŞIMI"


def say(f, anahtar=None):
    try:
        j = open(f, encoding="utf-8").read()
        return len(json.load(open(f, encoding="utf-8")) or []) if anahtar is None else len(json.loads(j)[anahtar])
    except Exception:
        return "?"


for x in aday:
    ad, r = x[0], x[3]
    if ad in bitti:
        continue
    d = os.path.join(W, r.split("/")[1])
    if not os.path.isdir(d):
        c, _ = run(["git", "-c", "core.hooksPath=NUL", "clone", "--depth", "1", "--quiet", f"https://github.com/{r}.git", d])
        if c:
            open(S, "a", encoding="utf-8").write(f"{ad}\t{r}\t\t\t\t\t\tklon hata\n"); continue
    ss, gl, sg = (os.path.join(W, r.split("/")[1] + e) for e in (".ss.json", ".gl.json", ".sg.json"))
    za = set()
    if not os.path.exists(ss):
        if run(["skillspector", "scan", d, "--no-llm", "--format", "json", "--output", ss], 600)[1] == "ZAMAN AŞIMI":
            za.add("ss")
    if not os.path.exists(gl):
        if run(["gitleaks", "detect", "--no-git", "--redact", "--no-banner", "--source", d, "--report-format", "json", "--report-path", gl])[1] == "ZAMAN AŞIMI":
            za.add("gl")
    while psutil.virtual_memory().percent > 89:  # RAM kapisi (kural <=%89)
        time.sleep(30)
    if not os.path.exists(sg):
        c, o = run(["semgrep", "scan", "--config", "p/default", "--metrics=off", "--quiet", "--json", d], 300)
        if o.strip().startswith("{"):
            open(sg, "w", encoding="utf-8").write(o)
        elif o == "ZAMAN AŞIMI":
            za.add("sg")
    try:
        j = open(ss, encoding="utf-8").read()
        hi, top = len(re.findall(r'"severity":\s*"(?:HIGH|CRITICAL)"', j, re.I)), len(re.findall(r'"severity"', j))
    except OSError:
        hi = top = "?"
    lic = next((f for f in os.listdir(d) if f.lower().startswith("license")), "")
    kb = sum(os.path.getsize(os.path.join(a, f)) for a, _, fs in os.walk(d) if ".git" not in a for f in fs) // 1024
    open(S, "a", encoding="utf-8").write("\t".join(map(str, [ad, r, lic, "ZAMAN AŞIMI" if "ss" in za else hi, top, "ZAMAN AŞIMI" if "gl" in za else say(gl), "ZAMAN AŞIMI" if "sg" in za else say(sg, "results"), f"{kb}KB"])) + "\n")
print("BITTI")
