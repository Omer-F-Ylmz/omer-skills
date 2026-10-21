"""KURULUM-V1 d2: planda ilk10 dışı, repo'lu YENI adaylardan puan sırasıyla ilk 15'i SkillSpector --no-llm + gitleaks + semgrep ile tara.
Devam edebilir: var olan <ad>.ss/.gl/.sg.json yeniden üretilmez, sonuc2.tsv'de satırı olan aday atlanır. Semgrep sırayla (RAM).
Kullanım: python -I -X utf8 kurulum_v1_d2_tara.py <yeni_bos_calisma_dizini>   (arka plan: .kos/kopru/arka.py ile)
Çıktı: <calisma_dizini>/sonuc2.tsv (ad, repo, lisans, SS_HIGH, SS_toplam, gitleaks, semgrep, boyut)"""
import csv, json, os, re, subprocess, sys
from pathlib import Path

W = sys.argv[1]
PLAN = Path(__file__).with_name("kurulum-v1-plan.tsv")
ENV = {**os.environ, "PYTHONUTF8": "1", "GIT_LFS_SKIP_SMUDGE": "1"}
S = os.path.join(W, "sonuc2.tsv")

satir = list(csv.reader(open(PLAN, encoding="utf-8"), delimiter="\t"))[1:]
aday = sorted((x for x in satir if x[2] == "YENI" and x[3] and not x[10]), key=lambda x: -int(x[7] or 0))[:15]
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
