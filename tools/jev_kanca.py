"""UserPromptSubmit jev ipucu: jev-skill.ps1'in PowerShell katmanı (soğuk açılış 0,6-3 sn) olmadan, tek python süreci.
Fail-open: her durumda exit 0. Kapı/tavan/bütçe jev.skill.hook içinde."""
import os
import runpy
import sys

try:
    if os.environ.get("CC_PROFIL"):
        sys.exit(0)
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:  # kapı kullanıcı ortamında (PS sarmalayıcıyla aynı kaynak)
        kapi = winreg.QueryValueEx(k, "JEV_SKILL_HOOK")[0]
    if kapi != "1":
        sys.exit(0)
    os.environ["JEV_SKILL_HOOK"] = kapi
    jev = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jev")
    os.chdir(jev)
    sys.path.insert(0, jev)
    sys.argv = ["jev", "hook"]
    runpy.run_module("jev", run_name="__main__")
except BaseException:
    pass
sys.stdout.flush()
os._exit(0)
