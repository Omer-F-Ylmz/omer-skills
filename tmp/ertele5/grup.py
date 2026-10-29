import re,sys,collections
sys.stdout.reconfigure(encoding="utf-8")
t=open(sys.argv[1],encoding="utf-8").read().split("### Skills",1)[1]
c=collections.Counter();n=collections.Counter()
for m in re.finditer(r"^\| (.+?) \| (.+?) \| .+\|$",t,re.M):
    if m.group(1) in("Skill","-------"):continue
    c[m.group(2)]+=len(m.group(1))+3;n[m.group(2)]+=1
tot=sum(c.values());print("toplam kr",tot,"~tok",tot//3)
for k,v in c.most_common(int(sys.argv[2])):print(f"{v//3:6d} tok {n[k]:5d} {k}")
