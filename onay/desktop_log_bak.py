"""Desktop loglarinda code-mode / hostinger / config yazimi izleri (son satirlar). Cikti .kos/kopru/desktop_log_bak.txt"""
import glob, os, sys
sys.stdout = open(r"C:\Projeler\omer-skills\.kos\kopru\desktop_log_bak.txt", "w", encoding="utf-8")
for kok in [os.path.expandvars(r"%LOCALAPPDATA%\Claude\logs"), os.path.expandvars(r"%APPDATA%\Claude\logs"),
            os.path.expandvars(r"%LOCALAPPDATA%\Claude-Data\claude_pzs8sxrjxfjjc\logs")]:
    for p in sorted(glob.glob(os.path.join(kok, "*.log")), key=os.path.getmtime)[-40:]:
        print("##", p, os.path.getsize(p))
        try:
            satir = open(p, encoding="utf-8", errors="replace").read().splitlines()
        except Exception as e:
            print("  okunamadi", e); continue
        hit = [s for s in satir if any(k in s.lower() for k in ("code-mode", "hostinger", "claude_desktop_config", "mcpservers", "invalid", "removed", "schema"))]
        for s in hit[-15:]:
            print("  ", s[:300])
