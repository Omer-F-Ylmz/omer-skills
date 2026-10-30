import json, os, re, glob, subprocess, datetime, sys
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
KEYS = """yarim-216 hic-122 karar-14 omer-karar-10 acik-31 acik-32 karar-30 envanter-dogrula-1 video-kaynak video-yeni-1 kalan-son derin-hiz-2 gpu-sinir-2 kod-modu-her-sey ertele-2 ertele-3 bosta-arac-1 mem-abone-1 profil-gorsel-1 yerel-gorsel-turbo yerel-medya-1 film-repo-8 arka-fix zip-yukle-30eki link-30eki-26 yaka-kapanis ilik-ucretsiz-3d ilik-tripo ilik-gece-yayin ucretsiz-3d-1 skill-mode yaka-d2 ab-taban ilik-v2""".split()
out = []
for k in KEYS:
    logs = sorted(glob.glob(os.path.join(D, k + "*.log")), key=os.path.getmtime)
    out.append("\n#### " + k + " logs=" + ",".join(os.path.basename(l) for l in logs[-4:]))
    if not logs:
        continue
    l = logs[-1]
    out.append("mtime " + datetime.datetime.fromtimestamp(os.path.getmtime(l)).strftime("%m-%d %H:%M"))
    txt = open(l, encoding="utf-8", errors="replace").read()
    res = None
    for line in txt.splitlines():
        if line.startswith("{") and '"type":"result"' in line:
            try:
                j = json.loads(line)
                res = j.get("result") or j.get("subtype")
            except Exception:
                m = re.search(r'"result":"(.*?)","(?:ttft|stop)', line)
                res = m.group(1) if m else None
    out.append("RESULT: " + (res or "yok; son: " + txt[-300:]).replace("\n", " ")[:900])
    g = subprocess.run(["git", "log", "--oneline", "-3", "-i", "--grep=" + k], capture_output=True, text=True, encoding="utf-8", cwd=D).stdout.strip()
    out.append("GIT: " + g.replace("\n", " | "))
open(os.path.join(D, "_yd1_ozet.txt"), "w", encoding="utf-8").write("\n".join(out))
print(len(out))
