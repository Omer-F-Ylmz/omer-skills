import sys
t=open(sys.argv[1],encoding="utf-8").read().split("\n")
ks=sys.argv[2].split(",")
print("satir",len(t))
for i,l in enumerate(t):
    for k in ks:
        j=l.find(k)
        if j>=0:print(i+1,":",l.strip()[:60],"...",l[max(0,j-80):j+160]);break
