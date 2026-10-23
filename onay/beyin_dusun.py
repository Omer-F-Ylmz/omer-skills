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
    """ASLA durmaz: her 2 dk sonsuz (yeniden başlatma/oturum açılışından sonra ilk dilimde sürer; AtLogOn tetiği yönetici ister, gerekmez), uykudan dönünce kaçan tur hemen (StartWhenAvailable), pilde de koşar, takılırsa 10 dk sonra öldürülür."""
    arg = f'--headless "{sys.executable}" "{BETIK}" tur'
    ps = (f"$a = New-ScheduledTaskAction -Execute 'C:\\Windows\\System32\\conhost.exe' -Argument '{arg}'; "
          "$t = New-ScheduledTaskTrigger -Once -At (Get-Date).Date -RepetitionInterval (New-TimeSpan -Minutes 2); "
          "$s = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 10); "
          f"Register-ScheduledTask -TaskName '{AD}' -Action $a -Trigger $t -Settings $s -Force | Out-Null; Start-ScheduledTask -TaskName '{AD}'")
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
