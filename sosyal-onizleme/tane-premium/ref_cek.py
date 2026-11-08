import urllib.request,os,re,sys
B="https://rad-genie-17bb3c.netlify.app/"
O=r"C:\Projeler\omer-skills\sosyal-onizleme\tane-premium\assets\ref\mercury"
os.makedirs(O,exist_ok=True)
for f in ["index.html","scene.js","style.css"]:
    d=urllib.request.urlopen(urllib.request.Request(B+("" if f=="index.html" else f),headers={"User-Agent":"Mozilla/5.0"}),timeout=30).read()
    open(os.path.join(O,f),"wb").write(d);print(f,len(d))
t=open(os.path.join(O,"scene.js"),encoding="utf-8").read()
for k in ["currentTime","MeshPhysicalMaterial","RoomEnvironment","PMREM","TubeGeometry","Points","depth","scroll","lerp","ShaderMaterial","CatmullRom"]:
    idx=[m.start() for m in re.finditer(k,t)][:2]
    for i in idx:print("##",k,":",t[max(0,i-90):i+150].replace("\n"," "))
