import json,os,sys,time,subprocess,urllib.request,uuid,shutil
R=r"C:\Projeler\omer-skills";T=os.path.join(R,"sosyal-onizleme","tane-premium");IMG=os.path.join(T,"assets","img")
OUT=os.path.join(os.path.expanduser("~"),"Desktop","Claude ile yapılanlar","tane-premium","sinema");os.makedirs(OUT,exist_ok=True)
SEQ=os.path.join(T,"assets","seq");os.makedirs(SEQ,exist_ok=True)
LOG=os.path.join(T,"sinema.log")
def log(*a):
    s=time.strftime("%H:%M:%S")+" "+" ".join(str(x) for x in a);print(s,flush=True);open(LOG,"a",encoding="utf-8").write(s+"\n")
U="http://127.0.0.1:8188"
def req(p,data=None,ct="application/json"):
    r=urllib.request.Request(U+p,data=data,headers={"Content-Type":ct} if data else {});return json.loads(urllib.request.urlopen(r,timeout=60).read() or b"{}")
def vram():
    try:return int(subprocess.run(["nvidia-smi","--query-gpu=memory.used","--format=csv,noheader,nounits"],capture_output=True,text=True).stdout.split()[0])
    except Exception:return 0
def bos_gb():
    try:
        import psutil;return psutil.virtual_memory().available/1e9
    except Exception:return 99
def acik():
    try:urllib.request.urlopen(U+"/system_stats",timeout=5);return True
    except Exception:return False
def yukle(path):
    b="----"+uuid.uuid4().hex;fn=os.path.basename(path)
    body=(f"--{b}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{fn}\"\r\nContent-Type: image/jpeg\r\n\r\n").encode()+open(path,"rb").read()+(f"\r\n--{b}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--{b}--\r\n").encode()
    return req("/upload/image",body,"multipart/form-data; boundary="+b)["name"]
NEG="blurry, distorted, warped, morphing objects, flicker, text, watermark, logo, low quality, cartoon, people, hands"
SAHNE=[("tarla","koken.jpg","slow cinematic aerial drone push-in over misty terraced coffee farm at dawn, low clouds drifting through the hills, soft golden light, gentle parallax, photorealistic, 35mm film"),
("kiraz","kiraz.jpg","macro shot, ripe red coffee cherries gently swaying on the branch, water droplets slowly sliding down, soft breeze, shallow depth of field, slow camera orbit, photorealistic"),
("kavrum","kavrum.jpg","freshly roasted coffee beans pouring out of the roaster drum into the cooling tray in slow motion, wisps of smoke swirling, warm tungsten light, slow push-in, photorealistic"),
("ogutum","ogutum.jpg","macro, freshly ground coffee settling and slowly shifting, a few coffee beans rolling, dramatic side light, very slow camera dolly, photorealistic"),
("fincan","fincan.jpg","espresso in white porcelain cup, golden crema slowly swirling, delicate steam rising and curling, soft window light, slow camera push-in, photorealistic")]
def main(sec):
    sab=json.load(open(os.path.join(R,"tools","gorsel","akislar","wan22_5b_t2v.json"),encoding="utf-8"))
    for ad,img,p in SAHNE:
        if sec and ad not in sec:continue
        if os.path.exists(os.path.join(SEQ,ad,"done")):log(ad,"var");continue
        for _ in range(240):
            if vram()<4000 and bos_gb()>=13:break
            if _%6==0:log("bekle VRAM",vram(),"bos GB",round(bos_gb(),1))
            time.sleep(20)
        if not acik():
            subprocess.run([sys.executable,os.path.join(R,"tools","gorsel_uret.py"),"ac"],cwd=R)
            for _ in range(60):
                if acik():break
                time.sleep(5)
        w=json.loads(json.dumps(sab));nm=yukle(os.path.join(IMG,img))
        w["20"]={"class_type":"LoadImage","inputs":{"image":nm}}
        w["21"]={"class_type":"ImageScale","inputs":{"image":["20",0],"upscale_method":"lanczos","width":1024,"height":576,"crop":"center"}}
        w["5"]["inputs"]["text"]=p;w["6"]["inputs"]["text"]=NEG
        w["7"]["inputs"].update({"width":1024,"height":576,"length":49,"start_image":["21",0]})
        w["8"]["inputs"]["seed"]=7;w["11"]["inputs"]["filename_prefix"]="tane/"+ad
        t0=time.time();pid=req("/prompt",json.dumps({"prompt":w}).encode())["prompt_id"];log(ad,"kuyrukta",pid)
        while True:
            time.sleep(10)
            try:h=req("/history/"+pid)
            except Exception as e:log(ad,"ComfyUI düştü",str(e)[:80]);break
            if pid in h:
                st=h[pid].get("status",{});
                if st.get("status_str")=="error":log(ad,"HATA",json.dumps(st)[:600]);break
                outs=h[pid]["outputs"];vid=None
                for o in outs.values():
                    for k in ("videos","images","gifs"):
                        for f in o.get(k,[]):vid=f
                if not vid:log(ad,"çıktı yok",json.dumps(outs)[:300]);break
                src=os.path.join(r"C:\AI\ComfyUI\output",vid.get("subfolder",""),vid["filename"]);mp4=os.path.join(OUT,ad+".mp4");shutil.copy(src,mp4)
                log(ad,"video",round(time.time()-t0),"sn",vid["filename"])
                d=os.path.join(SEQ,ad);os.makedirs(d,exist_ok=True)
                subprocess.run(["ffmpeg","-y","-loglevel","error","-i",mp4,"-vf","scale=1600:-2:flags=lanczos,unsharp=5:5:0.6","-q:v","4",os.path.join(d,"%03d.jpg")])
                n=len([x for x in os.listdir(d) if x.endswith(".jpg")]);open(os.path.join(d,"done"),"w").write(str(n));log(ad,"kare",n);break
            if time.time()-t0>2400:log(ad,"zaman aşımı");break
    subprocess.run([sys.executable,os.path.join(R,"tools","gorsel_uret.py"),"kapat"],cwd=R);log("BİTTİ, ComfyUI kapatıldı")
if __name__=="__main__":main(sys.argv[1:])
