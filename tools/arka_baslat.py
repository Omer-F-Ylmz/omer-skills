import subprocess, sys, os
K = r"C:\Projeler\omer-skills"
betik = sys.argv[1]
ad = os.path.splitext(os.path.basename(betik))[0]
log = open(os.path.join(K, "tmp", ad + ".arka.log"), "ab")
p = subprocess.Popen([sys.executable, "-I", "-S", betik], cwd=K, stdout=log, stderr=subprocess.STDOUT,
                     creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
print("basladi", ad, p.pid)
