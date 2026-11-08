import subprocess,sys,os
R=r"C:\Projeler\omer-skills"
O=os.path.join(os.path.expanduser("~"),"Desktop","Claude ile yapılanlar","tane-premium","seq");os.makedirs(O,exist_ok=True)
S=", centered single subject floating in mid-air in the middle of the frame, pure black background, dramatic soft overhead spotlight, subtle warm amber rim light, faint volumetric haze, cinematic luxury product photography, ultra detailed, sharp focus, no text, no logo"
P=[("01-kiraz","a small cluster of ripe glossy deep red coffee cherries on a short stem with two dark green leaves"),
("02-yesil","a loose floating cluster of raw unroasted green coffee beans, pale olive green, matte"),
("03-kavrum","freshly roasted dark brown coffee beans floating with glowing orange embers and thin wisps of smoke"),
("04-ogutum","a dense cloud of freshly ground coffee particles bursting outward from a single roasted coffee bean"),
("05-espresso","a thick glossy golden-brown espresso stream pouring into a white porcelain espresso cup on a saucer"),
("06-fincan","a white porcelain espresso cup with tiger-striped golden crema on a saucer, delicate steam rising")]
sec=sys.argv[1:] or [p[0] for p in P]
for ad,p in P:
    if ad not in sec: continue
    c=[sys.executable,os.path.join(R,"tools","gorsel_uret.py"),"uret","--is","foto","--prompt",p+S,"--cikti",os.path.join(O,ad+".png"),"--boyut","1344x768","--tohum","11"]
    r=subprocess.run(c,capture_output=True,text=True,cwd=R);print(ad,r.returncode,(r.stdout+r.stderr)[-300:])
