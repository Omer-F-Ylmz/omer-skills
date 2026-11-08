import os,shutil,re
T=r"C:\Projeler\omer-skills\sosyal-onizleme\tane-premium";Y=os.path.join(T,"yayin")
os.makedirs(Y,exist_ok=True)
for d in ["img","cut","seq"]:
    s=os.path.join(T,"assets",d);h=os.path.join(Y,"assets",d)
    if not os.path.isdir(s):continue
    for kok,_,fs in os.walk(s):
        for f in fs:
            p=os.path.join(kok,f)
            if os.path.getsize(p)==0:print("ATLA 0 bayt",p);continue
            q=os.path.join(h,os.path.relpath(p,s));os.makedirs(os.path.dirname(q),exist_ok=True)
            if not os.path.exists(q) or os.path.getmtime(q)<os.path.getmtime(p):shutil.copy2(p,q)
html=open(os.path.join(T,"index.html"),encoding="utf-8").read()
if not html.lstrip().lower().startswith("<!doctype"):
    html='<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="description" content="Tane Kahve — Huila çekirdeğinin kökünden fincanına yolculuğu.">\n'+html
open(os.path.join(Y,"index.html"),"w",encoding="utf-8",newline="\n").write(html)
ref=sorted(set(re.findall(r'assets/[A-Za-z0-9_./-]+\.(?:jpg|jpeg|png|webp|mp4|json|glb)',html)))
eks=[r for r in ref if not os.path.exists(os.path.join(Y,r)) and "/seq/" not in r]
print("videoYukle" in html,"ref",len(ref),"eksik",eks)
for kok,ds,fs in os.walk(Y):
    for f in fs:print(os.path.relpath(os.path.join(kok,f),Y),os.path.getsize(os.path.join(kok,f)))
