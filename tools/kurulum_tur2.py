"""KUR-TUR2: kurulum_d2 HATA / KURULUM-YOLU-YOK / KURULDU-DOGRULANMADI kalemlerinin ikinci turu.
  python tools/kurulum_tur2.py --plan      kalem başına kök neden + eylem (kurulum YOK; yalnız okuma/yoklama) -> rapor/kur-tur2-plan.tsv
  python tools/kurulum_tur2.py --uygula    eylemleri koşar -> rapor/kur-tur2-sonuc.tsv (silme yok; yarım klon _arsiv'e taşınır)
Girdi: tools/kurulum_tur2_siniflandir.py çıktısı (tmp/tur2-siniflar.tsv). Eylemler: D2 (düzeltilmiş sınıf/yolla kurulum_d2 --tur2), PLUGIN,
KOMUT (.claude/commands), APT (WSL Ubuntu), WINGET, DOGRULA (gerçek komut adı), COZUMSUZ (neden yazılı)."""
import csv, json, os, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

R = Path(__file__).resolve().parents[1]
SINIF, D2SONUC = R / "tmp/tur2-siniflar.tsv", R / "docs/video-tarama/kurulum-d2-sonuc.tsv"
COZ, COZ2 = R / "docs/video-tarama/kurulum-coz.tsv", R / "tmp/kurulum-coz-tur2.tsv"
PLAN, SONUC = R / "rapor/kur-tur2-plan.tsv", R / "rapor/kur-tur2-sonuc.tsv"
NW = 0x08000000
HOME = Path.home()
APT = {"Wifite": "wifite", "tshark": "tshark", "binwalk": "binwalk", "vim": "vim",
       "wget": "wget", "gnu-tar": "tar", "rtmpdump": "rtmpdump", "whatweb": "whatweb", "fakeroot": "fakeroot", "dnf": "dnf"}
WINGET = {"Gradle": "Gradle.Gradle", "NSIS": "NSIS.NSIS",
"nvm-windows": "CoreyButler.NVMforWindows", "Poppler": "oschwartz10612.Poppler"}  # 7 Kas: nmap/JADX zip ile kuruldu; Chocolatey Omer'e soru
LINUX_ONLY = {"systemd": "Linux init sistemi; Windows'ta derlenemez/çalışmaz", "Sealos": "release yalnız linux (.deb/.rpm/.tar.gz)",
              "gVisor": "Linux çekirdek sandbox'ı; release yalnız linux tar", "paru": "Arch Linux AUR aracı", "yay": "Arch Linux AUR aracı",
              "Homebrew/brew": "macOS/Linux; release .pkg", "BlackArch": "Arch tabanlı dağıtım (PKGBUILD deposu)",
              "Scoop": "kurulum iex(irm ...) boru hattı; SUPHE kuralı (curl|iex) yasak"}


def run(a, t=120, cwd=None):
    try:
        r = subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=t, cwd=cwd, stdin=subprocess.DEVNULL, creationflags=NW)
        return r.returncode, (r.stdout + r.stderr).replace("\x00", "").strip()
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"[:200]


def oku(p):
    return list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t")) if Path(p).exists() else []


def tsv(p, baslik, satirlar):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(baslik); w.writerows(satirlar)


def npm_bin_var(ad):
    c, o = run(["npm.cmd", "view", ad, "bin", "--json"], 60)
    return c == 0 and o.strip() not in ("", "undefined", "null", "{}")


def karar(x, d2):
    """x: tur2-siniflar satırı; d2: d2 sonuç satırı. -> (eylem, arg, neden_kanit)"""
    n, dt, k, kay, sn = x["neden"], x["dizin_turu"], x["kalem"], x["kaynak"], x["sinif"]
    yol = Path(d2["yol"]) if d2["yol"] else None
    tur, _, ad = kay.partition(":")
    if k in LINUX_ONLY:
        return "COZUMSUZ", "", LINUX_ONLY[k]
    if n == "dogrulanmadi":
        return "DOGRULA", "", "kurulum tamam; komut adı/--version yoklaması başarısız (kanit sütunu)"
    plug = bool(yol and (yol / ".claude-plugin/marketplace.json").exists())
    kom = list((yol / ".claude/commands").glob("*.md")) if yol and (yol / ".claude/commands").is_dir() else []
    sk = bool(yol and yol.is_dir() and re.search(r"plugin|skills-alt", dt) and next((q for q in yol.rglob("SKILL.md") if "node_modules" not in q.parts), None))
    if n == "yolu-yok" and (plug or kom or sk) and sn == "CLI":
        if plug: return "PLUGIN", str(yol), "repo Claude Code eklentisi (.claude-plugin/marketplace.json); sınıf CLI yanlış"
        if kom: return "KOMUT", str(yol), f"repo .claude/commands/ içinde {len(kom)} slash komutu; sınıf CLI yanlış"
        return "D2", "SKILL", "repoda SKILL.md var; sınıf CLI→SKILL"
    if n in ("skill-yok", "bin-yok"):
        if plug:
            return "PLUGIN", str(yol), "repo Claude Code eklentisi (.claude-plugin/marketplace.json); SKILL.md yok"
        if kom:
            return "KOMUT", str(yol), f"repo .claude/commands/ içinde {len(kom)} slash komutu; SKILL.md yok"
        if dt in ("bos", "yolsuz") or (yol and not (yol / ".git/HEAD").exists()):
            return "D2", sn, "klon boş/yarım (git HEAD yok): yeniden klon (klonla: HEAD yoksa _arsiv'e taşı, uzak boşsa çözümsüz)"
        if sn == "SKILL":
            yeni = "CLI" if re.search(r"npm-bin|(^|\+)go(\+|$)|cargo", dt) else "PAKET"
            return "D2", yeni, f"SKILL.md yok; dizin={dt} -> sınıf SKILL→{yeni}"
        return "D2", sn, f"bin yok; gh_cli_kur düzeltmesi (bin'siz npm: global kurulmaz; release/derleme yolu, yoksa KURULDU-KAYNAK)"
    if n == "npm-0skill":
        yeni = "CLI" if npm_bin_var(ad) else "PAKET"
        return "D2", yeni, f"npm paketinde SKILL.md yok; npm view bin -> sınıf SKILL→{yeni}"
    if n == "buyuk":
        return "D2", sn, "repo büyük: --tur2 (SKILL: blobsuz+seyrek klon yalnız SKILL dizinleri; CLI: release/derleme)"
    if n == "npm-ebusy":
        return "D2", sn, "ortak node_modules'ta EBUSY rename çakışması -> kalem başına ayrı --prefix (ana-liste-npm-t2)"
    if n in ("klon", "llm", "npm-diger", "release"):
        if k == "BlackArch":
            return "COZUMSUZ", "", LINUX_ONLY["BlackArch"]
        if n == "release":
            return "COZUMSUZ", "", "release zip'i exe içermiyor (yalnız libs/prx: PS5 araç zinciri); Windows .exe yok"
        if k == "sound engine":
            return "COZUMSUZ", "", "node-gyp + vcpkg portaudio derlemesi code 1 (kanit); yerel ses SDK'sı yok"
        return "D2", sn, {"klon": "klon zaman aşımı/checkout hatası -> --tur2 600s, SKILL ise seyrek klon", "llm": "LLM kapısı erişilemedi -> yeniden", "npm-diger": "npm -g code 1 -> --tur2 yeniden"}[n]
    if n == "pip-uv":
        if k == "oMLX":
            return "COZUMSUZ", "", "bağımlılık mlx-audio git klonu 'invalid path' (Windows'ta geçersiz dosya adı); MLX yalnız Apple Silicon"
        return "D2", sn, ("requires-python>=3.14 -> uv_zincir'e 3.14 eklendi" if k.startswith("Free Claude") else
                          "pyproject Python paketi değil (flat-layout çoklu paket) -> release/derleme yoluna düşer" if k in ("Podman", "feder-cr/dots") else
                          "izole `uv pip install --dry-run` rc=0; toplu koşuda çakışma -> sıralı (--is 1) yeniden")
    if n == "diger" and kay.startswith("pip:"):
        return "PIPEK", "pillow", "import PIL ModuleNotFoundError: eksik bağımlılık venv'e eklenir, doğrulama yinelenir"
    if n == "yolu-yok":
        if k in APT:
            return "APT", APT[k], "Windows release yok; WSL Ubuntu apt paketi"
        if k in WINGET:
            return "WINGET", WINGET[k], "GitHub release'te win-x64 asset yok; winget paketi"
        if dt in ("cargo", "cargo+docker", "go+docker", "cmake", "cmake+make", "go"):
            return "D2", sn, f"kaynaktan derleme ({dt}): kaynak_derle Cargo/Go/CMake"
        if dt == "make":
            return "COZUMSUZ", "", "Makefile; Windows'ta make yok, yalnız Linux hedefi (WSL apt paketi eşleşmedi)"
        if dt in ("yalniz-readme", "bos", "yolsuz", "YOK-DIZIN"):
            return "COZUMSUZ", "", f"kurulacak kod/release yok (dizin={dt}); kanit: {x['not'][-70:]}"
        return "COZUMSUZ", "", f"dizin={dt}: Windows derleme/kurulum yolu yok; kanit: {x['not'][-70:]}"
    return "COZUMSUZ", "", f"eşleşen kural yok ({n}/{dt})"


def plan():
    d2 = {}
    for r in oku(D2SONUC): d2[r["kalem"]] = r
    sat = oku(SINIF)
    with ThreadPoolExecutor(6) as ex:
        kar = list(ex.map(lambda x: karar(x, d2[x["kalem"]]), sat))
    def yokla(xk):
        x, (e, a, nd) = xk
        ek = ""
        if e == "APT":
            c, o = run(["wsl", "-e", "bash", "-c", f"apt-cache policy {a} | sed -n 3p"], 90)
            ek = o.strip()[:50]
            if "(none)" in ek or not ek: e, nd = "COZUMSUZ", f"apt adayı yok ({a}): {ek}"
        if e == "WINGET":
            c, o = run(["winget", "show", "--id", a, "-e", "--accept-source-agreements"], 60)
            ek = "winget show rc=%d" % c
            if c: e, nd = "COZUMSUZ", f"winget kimliği bulunamadı ({a}): {o[-60:]}"
        return [x["kalem"], x["sinif"], x["kaynak"], x["neden"], x["dizin_turu"], e, a, nd, ek]
    with ThreadPoolExecutor(8) as ex:
        cikti = list(ex.map(yokla, zip(sat, kar)))
    tsv(PLAN, ["kalem", "sinif", "kaynak", "neden", "dizin_turu", "eylem", "arg", "kok_neden_cozum", "yoklama"], cikti)
    from collections import Counter
    print("eylem:", dict(Counter(r[5] for r in cikti)))
    print("neden x eylem:", dict(Counter((r[3], r[5]) for r in cikti)))
    return cikti


def d2_calistir(satirlar, d2):
    coz = {r["kalem"]: r for r in oku(COZ)}
    rows, secili = [], []
    for kalem, sinif in satirlar:
        c = dict(coz.get(kalem) or {"kalem": kalem, "sonuc": "DOGRULANDI", "kaynak": d2[kalem]["kaynak"], "puan": "1", "yol": ""})
        c["sinif"], c["sonuc"] = sinif, "DOGRULANDI"
        rows.append(c); secili.append(kalem)
    tsv(COZ2, ["kalem", "sinif", "sonuc", "kaynak", "puan", "yol"], [[r.get(h, "") for h in ("kalem", "sinif", "sonuc", "kaynak", "puan", "yol")] for r in rows])
    # sıralı (--is 1): toplu koşuda uv/npm çakışması gözlendi
    c, o = run([sys.executable, "-X", "utf8", str(R / "tools/kurulum_d2.py"), "--faz", "kur", "--coz", str(COZ2), "--tur2", "--is", "1", "--kalem", "|".join(secili)], 7200, cwd=str(R))
    return c, o[-300:]


def uv_tool_exeler(ad):
    c, o = run(["uv", "tool", "list"], 60)
    cur, exe = None, {}
    for l in o.splitlines():
        if l.startswith("- ") and cur: exe[cur].append(l[2:].strip())
        elif l and not l.startswith(" "): cur = l.split()[0].lower(); exe[cur] = []
    ad = ad.lower().replace("_", "-")
    for t, e in exe.items():
        if t == ad or ad.endswith("/" + t) or t == ad.split("/")[-1]: return e
    return []


def dogrula_kalem(r, d2):
    tur, _, ad = r["kaynak"].partition(":")
    exeler = []
    if tur == "npm":
        c, o = run(["npm.cmd", "view", ad, "bin", "--json"], 60)
        try:
            bj = json.loads(o); exeler = list(bj) if isinstance(bj, dict) else [ad.split("/")[-1]]
        except Exception:
            exeler = []
        yol = [Path(os.environ.get("APPDATA", "")) / "npm" / (e + ".cmd") for e in exeler]
    else:
        exeler = uv_tool_exeler(ad.split("/")[-1])
        yol = [HOME / ".local/bin" / (e + ".exe") for e in exeler]
    if not yol: return "KURULDU-DOGRULANMADI", "tür2: bin adı bulunamadı (npm view bin / uv tool list boş)"
    for p in yol:
        if not p.exists(): continue
        for a in ("--version", "--help"):
            c, o = run([str(p), a], 40)
            if c == 0 and o: return "KURULDU", f"tür2: {p.name} {a}: {o.splitlines()[0][:70]}"
        return "KURULDU-DOGRULANMADI", f"tür2: {p.name} var ama çalıştırma rc={c}: {o.splitlines()[-1][:110] if o else ''}"
    return "KURULDU-DOGRULANMADI", f"tür2: komut dosyası yok ({', '.join(p.name for p in yol)[:80]})"


def uygula():
    pl = plan()
    d2 = {r["kalem"]: r for r in oku(D2SONUC)}
    sonuc = []
    def kayit(k, e, dur, n): sonuc.append([k, e, dur, n[:220]]); print(f"{e:8} {dur:22} {k[:30]} {n[:90]}")
    yeni = {r[0]: r[6] for r in pl if r[5] == "D2"}  # arg = düzeltilmiş sınıf
    if yeni:
        c, o = d2_calistir(list(yeni.items()), d2)
        son = {r["kalem"]: r for r in oku(D2SONUC)}
        for k in yeni: kayit(k, "D2", son[k]["durum"], son[k]["not"] if son[k]["durum"] in ("HATA", "KURULUM-YOLU-YOK") else "kurulum_d2 --tur2: " + son[k]["not"])
    for r in pl:
        k, e, a = r[0], r[5], r[6]
        if e == "COZUMSUZ": kayit(k, e, "COZUMSUZ", r[7])
        elif e == "PLUGIN":
            m = json.loads((Path(a) / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
            c, o = run(["claude", "plugin", "marketplace", "add", a], 120)
            if c: kayit(k, e, "HATA", "marketplace add: " + o[-100:]); continue
            hatalar = []
            for p in m.get("plugins", []):
                c2, o2 = run(["claude", "plugin", "install", f"{p['name']}@{m['name']}"], 180)
                if c2: hatalar.append(f"{p['name']}: {o2[-60:]}")
            kayit(k, e, "HATA" if hatalar else "KURULDU", "; ".join(hatalar) or f"{m['name']}: {len(m.get('plugins', []))} eklenti")
        elif e == "KOMUT":
            dst = HOME / ".claude/commands"; dst.mkdir(parents=True, exist_ok=True); n = 0
            ow = Path(a).name.split("__")[0].lower()
            for f in (Path(a) / ".claude/commands").glob("*.md"):
                h = dst / f"{ow}-{f.name}"
                if not h.exists(): shutil.copy2(f, h); n += 1
            kayit(k, e, "KURULDU", f"{n} slash komutu ~/.claude/commands")
        elif e == "APT":
            c, o = run(["wsl", "-u", "root", "-e", "apt-get", "install", "-y", a], 900)
            c2, o2 = run(["wsl", "-e", "dpkg", "-s", a], 60)
            kayit(k, e, "KURULDU" if c == 0 and c2 == 0 else "HATA", f"apt {a}: " + (o2.splitlines()[1] if c2 == 0 and len(o2.splitlines()) > 1 else o[-100:]))
        elif e == "WINGET":
            c, o = run(["winget", "install", "--id", a, "-e", "--silent", "--accept-package-agreements", "--accept-source-agreements"], 900)
            kayit(k, e, "KURULDU" if c in (0, -1978335189) else "HATA", f"winget {a} rc={c}: {o[-80:]}")
        elif e == "DOGRULA":
            dur, n = dogrula_kalem({"kaynak": r[2]}, d2); kayit(k, e, dur, n)
        elif e == "PIPEK":
            c, o = run(["uv", "pip", "install", "--python", str(HOME / ".venvs/ana-liste/Scripts/python.exe"), a], 300)
            kayit(k, e, "KURULDU" if c == 0 else "HATA", f"uv pip install {a} rc={c}: {o[-80:]}")
    tsv(SONUC, ["kalem", "eylem", "durum", "not"], sonuc)
    from collections import Counter
    print("sonuç:", dict(Counter(s[2] for s in sonuc)))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--plan"]: plan()
    elif a[:1] == ["--uygula"]: uygula()
    else: sys.exit(__doc__)
