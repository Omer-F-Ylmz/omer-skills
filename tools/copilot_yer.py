import glob, os
k = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code")
b = glob.glob(k + r"\resources\app\extensions\*copilot*") + glob.glob(k + r"\*\resources\app\extensions\*copilot*")
open(r"C:\Projeler\omer-skills\.kos\kopru\log\copilot_yer.log", "w", encoding="utf-8").write("\n".join(b) or "YOK")
print(len(b))
