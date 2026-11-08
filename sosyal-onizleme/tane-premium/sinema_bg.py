import subprocess,sys,os
d=os.path.dirname(os.path.abspath(__file__))
subprocess.Popen([sys.executable,os.path.join(d,"sinema.py")]+sys.argv[1:],cwd=d,creationflags=0x00000008|0x00000200,stdout=open(os.path.join(d,"sinema.out"),"a"),stderr=subprocess.STDOUT)
print("başladı")
