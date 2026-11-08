import os,shutil,subprocess,sys,glob
R=r"C:\Projeler\omer-skills";T=os.path.join(R,"sosyal-onizleme","tane-premium")
D=os.path.join(os.path.expanduser("~"),"Desktop","Claude ile yapılanlar","tane-premium","ref");os.makedirs(D,exist_ok=True)
C=os.path.join(T,"assets","cut");os.makedirs(C,exist_ok=True)
for f in ["cekirdek","degirmen","fincan","paket"]:
    src=os.path.join(T,"assets","ref",f+".png");dst=os.path.join(D,f+".png");shutil.copy(src,dst)
    r=subprocess.run([sys.executable,os.path.join(R,"tools","gorsel_uret.py"),"arkaplan",dst],capture_output=True,text=True,cwd=R)
    print(f,r.returncode,(r.stdout+r.stderr)[-200:])
for p in glob.glob(os.path.join(D,"*-arkaplansiz.png")):
    shutil.copy(p,os.path.join(C,os.path.basename(p).replace("-arkaplansiz","")));print(p)
