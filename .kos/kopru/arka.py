"""Bir python betiğini kopuk süreçte koşar, çıktıyı günlüğe yazar: python arka.py [--bagimsiz] [--cwd DİZİN] <gunluk> <betik.py> [arg...]
--bagimsiz (KURTAR-FİX-1): süreç tek seferlik Görev Zamanlayıcı görevinden (pythonw sarmalayıcı, Desktop/yönetici job'u DIŞINDA) koşar;
Desktop ya da yönetici ölünce ölmez. Sarmalayıcı betik bitince görevi siler.
cwd varsayılanı repo kökü; worktree'deki betik göreli yollar kullanıyorsa --cwd ile o worktree verilir (11 Eki 18:17: kalite3 r2 ve
blender faz5 ölçümleri ana repo cwd'sinde göreli yolu bulamayıp rc 2 ile düştü). Günlük yolu göreliyse repo köküne göredir."""
import json, os, subprocess, sys, tempfile, time, uuid
kok = r"C:\Projeler\omer-skills"
arg = sys.argv[1:]
cwd = kok
bagimsiz = arg[:1] == ["--bagimsiz"]
ic = arg[:1] == ["--ic"]  # sarmalayıcı kipi: arg = [görev adı]; asıl argümanlar temp json'dan (schtasks /tr 261 karakter sınırı), betiği bekler, görevi siler
if bagimsiz or ic:
    arg = arg[1:]
if ic:
    gorev = arg[0]
    ic_json = os.path.join(tempfile.gettempdir(), gorev + ".json")
    cwd, arg = json.load(open(ic_json, encoding="utf-8"))
    os.remove(ic_json)
bitis, yeniden = "BITTI|BITIS", False  # ARKA-BEKCI-1: günlükte bitiş işareti (regex); --yeniden = ölürse bekçi 1 kez yeniden başlatır (yalnız idempotent betik)
while arg[:1] in (["--cwd"], ["--bitis"], ["--yeniden"]):
    if arg[0] == "--yeniden":
        yeniden, arg = True, arg[1:]
    elif arg[0] == "--bitis":
        bitis, arg = arg[1], arg[2:]
    else:
        cwd, arg = arg[1], arg[2:]
        if not os.path.isdir(cwd):
            sys.exit(f"--cwd yok: {cwd}")
betik = arg[1] if os.path.isabs(arg[1]) else os.path.join(cwd, arg[1])
if not os.path.isfile(betik):
    sys.exit(f"betik yok: {betik} (cwd {cwd})")
# TEKİL-YÖNETİCİ: canlı bir ajan_sira varsa ikinci kopya hiç başlamaz (ajan_sira.py kendi kilidini de denetler)
kilit = os.path.join(kok, ".kos", "kopru", "ajan-sira.kilit")
if os.path.basename(betik) == "ajan_sira.py" and os.path.isfile(kilit):
    eski = open(kilit, encoding="utf-8").read().split()[:1]
    if eski and eski[0].isdigit():
        ps = f"(Get-CimInstance Win32_Process -Filter 'ProcessId={eski[0]}').CommandLine"
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace", creationflags=0x08000000)
        if "ajan_sira.py" in r.stdout:
            print("zaten çalışıyor · ajan_sira pid", eski[0])
            sys.exit(0)
log = open(os.path.join(kok, arg[0]), "a", encoding="utf-8")


def kaydet(ad, pid, bagimsiz_):
    """ARKA-BEKCI-1: işi arka-kayit.json'a yazar (tools/arka_bekci.py izler). Kayıt hatası işi düşürmez; pytest altında ARKA_KAYIT yoksa yazılmaz."""
    if os.environ.get("PYTEST_CURRENT_TEST") and not os.environ.get("ARKA_KAYIT"):
        return
    yol = os.environ.get("ARKA_KAYIT") or os.path.join(kok, ".kos", "kopru", "arka-kayit.json")
    try:
        try:
            k = json.load(open(yol, encoding="utf-8"))
        except (OSError, ValueError):
            k = {}
        k[ad] = {"betik": betik, "gunluk": os.path.join(kok, arg[0]), "pid": pid, "basladi": time.time(), "bitis": bitis, "yeniden": yeniden,
                 "cwd": cwd, "arg": arg, "bagimsiz": bagimsiz_, "durum": "calisiyor"}
        tmp = f"{yol}.{os.getpid()}.tmp"
        json.dump(k, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, yol)
    except OSError:
        pass
env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1"}
# PENCERE-KÖK (23 Eki 17:50): çocuk betik pythonw ile koşarsa konsolu yoktur; onun başlattığı her konsol aracı (semgrep, git, node, cmd)
# Windows'ta YENİ GÖRÜNÜR pencere açar. python.exe + CREATE_NO_WINDOW gizli konsol verir, torunlar onu miras alır → hiç pencere çıkmaz.
py = os.path.join(os.path.dirname(sys.executable), "python.exe")
if not os.path.isfile(py):
    py = sys.executable
if ic:
    try:
        rc = subprocess.run([py, *arg[1:]], stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=cwd, env=env, creationflags=0x08000000).returncode
    finally:
        subprocess.run(["schtasks", "/delete", "/tn", gorev, "/f"], capture_output=True, creationflags=0x08000000)
    sys.exit(rc)
if bagimsiz:
    ad = "arka-" + uuid.uuid4().hex[:8]
    pw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    json.dump([cwd, arg], open(os.path.join(tempfile.gettempdir(), ad + ".json"), "w", encoding="utf-8"))
    tr = subprocess.list2cmdline([pw, os.path.abspath(__file__), "--ic", ad])
    for komut in (["/create", "/tn", ad, "/sc", "once", "/st", "00:00", "/f", "/tr", tr], ["/run", "/tn", ad]):
        r = subprocess.run(["schtasks", *komut], capture_output=True, text=True, errors="replace", creationflags=0x08000000)
        if r.returncode:
            sys.exit(f"schtasks {komut[0]} düştü: {r.stdout}{r.stderr}")
    kaydet(ad, None, True)
    print("arka bağımsız · görev", ad, "·", arg[0], "· cwd", cwd)
    sys.exit(0)
try:
    p = subprocess.Popen([py, *arg[1:]], stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                         cwd=cwd, env=env, creationflags=0x08000000 | 0x00000200 | 0x01000000, close_fds=True)
except OSError:
    p = subprocess.Popen([py, *arg[1:]], stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                         cwd=cwd, env=env, creationflags=0x08000000 | 0x00000200, close_fds=True)  # CREATE_NO_WINDOW: gizli konsol alt süreçlere miras (DETACHED'ta her konsol altı yeni pencere açar)
    print("UYARI: job'dan ayrılamadı (breakaway reddedildi); oturum bitince bu süreç de ölür · uzun işi arka-istek ile başlat")
kaydet("arka-" + uuid.uuid4().hex[:8], p.pid, False)
print("arka pid", p.pid, "·", arg[0], "· cwd", cwd)
