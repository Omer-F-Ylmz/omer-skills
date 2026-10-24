"""BEYIN-DUSUN-1 onay betiği — Ömer koşar (CC tarafı).
python onay/beyin_dusun.py --kuru   # plan (varsayılan; hiçbir şey yazmaz)
python onay/beyin_dusun.py uygula   # settings.json'a 3 kanca (yedekli) + "omer-beyin-dusun" görevi (2 dk, pythonw, pencere yok)
python onay/beyin_dusun.py --geri   # kancaları çıkarır, görevi siler
Kanca: UserPromptSubmit/PostToolUse/PostToolUseFailure/Stop → tools/beyin_dusun.py kanca (0 jeton, hata oturumu bozmaz)."""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

AD = "omer-beyin-dusun"
PYW = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
BETIK = r"C:\Projeler\omer-skills\tools\beyin_dusun.py"
TR = f'C:\\Windows\\System32\\conhost.exe --headless "{sys.executable}" "{BETIK}" tur'  # mem_bekci ile aynı pencere-siz yol
KOMUT = f'python -S "{BETIK}" kanca'
OZET_KMT = f'python -S "{BETIK}" ozet'
AYAR = Path.home() / ".claude" / "settings.json"
OLAYLAR = ("UserPromptSubmit", "PostToolUse", "PostToolUseFailure", "Stop")


def _gorev_kur():
    """ASLA durmaz: 3 tetik — her 2 dk sonsuz; oturum açılışı (+ 5 dk canlılık tekrarı); uykudan dönüş (Power-Troubleshooter 1). Pilde de koşar, takılırsa 10 dk sonra öldürülür, çift tetik IgnoreNew ile tek koşar.
    Principal InteractiveToken kalır: S4U/"oturum kapalıyken de" yönetici ya da parola ister (non-admin Register → Erişim engellendi, 24.10 denendi)."""
    sid = subprocess.run(["powershell", "-NoProfile", "-Command", "[Security.Principal.WindowsIdentity]::GetCurrent().User.Value"], capture_output=True, text=True).stdout.strip()
    sorgu = ("&lt;QueryList&gt;&lt;Query Id=\"0\" Path=\"System\"&gt;&lt;Select Path=\"System\"&gt;"
             "*[System[Provider[@Name='Microsoft-Windows-Power-Troubleshooter'] and EventID=1]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;")
    xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.3" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Principals><Principal id="Author"><UserId>{sid}</UserId><LogonType>InteractiveToken</LogonType></Principal></Principals>
  <Settings><DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries><StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <StartWhenAvailable>true</StartWhenAvailable><MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy><ExecutionTimeLimit>PT10M</ExecutionTimeLimit></Settings>
  <Triggers>
    <TimeTrigger><StartBoundary>{time.strftime("%Y-%m-%d")}T00:00:00</StartBoundary><Repetition><Interval>PT2M</Interval></Repetition></TimeTrigger>
    <LogonTrigger><UserId>{sid}</UserId><Repetition><Interval>PT5M</Interval></Repetition></LogonTrigger>
    <EventTrigger><Subscription>{sorgu}</Subscription></EventTrigger>
  </Triggers>
  <Actions Context="Author"><Exec><Command>C:\\Windows\\System32\\conhost.exe</Command>
    <Arguments>--headless "{sys.executable}" "{BETIK}" tur</Arguments></Exec></Actions>
</Task>'''
    dosya = Path(os.environ.get("TEMP", ".")) / "omer-beyin-dusun.xml"
    dosya.write_bytes(xml.encode("utf-16"))
    ps = (f"Register-ScheduledTask -TaskName '{AD}' -Xml (Get-Content -Raw -Encoding Unicode '{dosya}') -Force -ErrorAction Stop | Out-Null; "
          f"Start-ScheduledTask -TaskName '{AD}'")
    return subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True)


def _kanca_mi(h):
    return "beyin_dusun.py" in h.get("command", "")


def _temizle(a):
    for o in list(a.get("hooks", {})):
        for g in a["hooks"][o]:
            g["hooks"] = [h for h in g.get("hooks", []) if not _kanca_mi(h)]
        a["hooks"][o] = [g for g in a["hooks"][o] if g.get("hooks")]
        if not a["hooks"][o]:
            del a["hooks"][o]


def _yaz(a):
    AYAR.write_bytes((json.dumps(a, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


kip = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
if kip == "--kuru":
    mevcut = subprocess.run(["schtasks", "/Query", "/TN", AD], capture_output=True).returncode == 0
    print(f"görev {AD}: {'VAR' if mevcut else 'yok'} · pythonw {os.path.exists(PYW)} · betik {os.path.exists(BETIK)}")
    print(f"uygula: Register-ScheduledTask {AD} (2 dk sonsuz, StartWhenAvailable, pilde de) · yalnız görev için: gorev")
    print(f"kanca olayları: {', '.join(OLAYLAR)} → {KOMUT}")
elif kip == "uygula":
    if not os.path.exists(PYW):
        sys.exit("pythonw.exe yok: " + PYW)
    yed = AYAR.with_name(f"settings.json.beyin-{time.strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(AYAR, yed)
    a = json.loads(AYAR.read_text(encoding="utf-8"))
    _temizle(a)
    for o in OLAYLAR:
        a.setdefault("hooks", {}).setdefault(o, []).append({"hooks": [{"type": "command", "command": KOMUT, "timeout": 5}]})
    a["hooks"].setdefault("SessionStart", []).append({"hooks": [{"type": "command", "command": OZET_KMT, "timeout": 5}]})  # BEYIN-CANLI-1: 2. beyin özeti oturum bağlamına
    _yaz(a)
    r = _gorev_kur()
    print("yedek:", yed.name, "·", r.stdout.strip() or r.stderr.strip() or "görev kuruldu")
elif kip == "gorev":  # yalnız zamanlanmış görevi (yeniden) kur; settings.json'a dokunmaz
    r = _gorev_kur()
    print(r.stdout.strip() or r.stderr.strip() or "görev kuruldu")
elif kip == "--geri":
    a = json.loads(AYAR.read_text(encoding="utf-8"))
    _temizle(a)
    _yaz(a)
    r = subprocess.run(["schtasks", "/Delete", "/TN", AD, "/F"], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
else:
    sys.exit("kip: --kuru | uygula | --geri")
