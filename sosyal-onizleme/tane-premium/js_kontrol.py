import re,sys,subprocess,os,tempfile
t=open(sys.argv[1],encoding="utf-8").read()
ss=re.findall(r"<script(?![^>]*src)[^>]*>(.*?)</script>",t,re.S)
for i,s in enumerate(ss):
    p=os.path.join(tempfile.gettempdir(),f"tane_js_{i}.js");open(p,"w",encoding="utf-8").write(s)
    r=subprocess.run(["node","--check",p],capture_output=True,text=True,shell=True)
    print(i,len(s),"OK" if r.returncode==0 else "HATA "+r.stderr[:600])
