import tempfile,os
p=os.path.join(tempfile.gettempdir(),"gorsel-oturum.log")
print(open(p,encoding="utf-8",errors="replace").read()[-2500:] if os.path.exists(p) else "yok")
