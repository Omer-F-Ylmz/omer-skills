"""14b onay · geri-al · dene: bekleyen/<ad>.md yapılandırılmış adımları (serbest kabuk yok) → kur · duman · geri alma;
docs/denemeler/<ad>.md → tavanlı `claude -p` A/B + Jev kalite puanı."""
import json
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import date
from pathlib import Path

from jev import cekirdek as c

from . import tarama as tr

KOK = Path(__file__).resolve().parents[3]
FIIL = {"plugin": (["claude", "plugin", "install"], ["claude", "plugin", "uninstall"]),
        "mcp": (["claude", "mcp", "add", "--scope", "user"], ["claude", "mcp", "remove", "--scope", "user"]),
        "uv": (["uv", "tool", "install"], ["uv", "tool", "uninstall"]),
        "npm": (["npm.cmd", "i", "-g"], ["npm.cmd", "rm", "-g"]),
        "winget": (["winget", "install", "--exact", "--id"], ["winget", "uninstall", "--exact", "--id"])}
META = re.compile(r"[;&|<>`]|\$\(")
KABUK = re.compile(r"\b(curl|wget|iwr|irm|iex|invoke-\w+|sh|bash|cmd|powershell|pwsh)\b|https?://\S+\.(sh|ps1|bat|cmd)\b", re.I)
ANAHTAR = re.compile(r"\b(sk-|pk-|ghp_|gho_|github_pat_|xox[bpas]-|AKIA)[\w-]{4,}")
ENVREF = re.compile(r"\$\{[A-Z_][A-Z0-9_]*\}")
SALT_OKUR = {"--version", "-v", "version", "--help", "-h", "help", "list", "ls", "show", "status", "info", "search", "get", "view", "doctor", "check"}
KALITE_Q = {"type": "score", "instructions": "Yanıt (state) görevi eksiksiz ve anlaşılır karşılıyor mu?",
            "criteria": ["karşılamıyor", "kısmen", "büyük ölçüde", "eksiksiz ve anlaşılır"]}
ALANLAR = ("cikti", "girdi", "sure", "maliyet", "kalite")
KONTROL_SN, DESEN_SN = 10, 1  # yanıt kontrolü · desen ön-denetimi (ayrı süreç, zaman aşımı)
REGEX = ("olgu", "yasak", "satir-desen")
DUSMAN = ["a" * 50000, "a\n" * 25000, " " * 50000, "\n" * 50000, "x " * 25000, "- `git a` b\n" * 4200]  # 50 KB'lık düşmanca metinler
_RE_KOD = "import json,re,sys\nd=json.loads(sys.stdin.buffer.read())\nprint(json.dumps([[bool(re.search(p,t)) for t in ts] for p,ts in d]))"


def _satirlar(metin, b):
    return [s.strip()[2:].strip() for s in tr.bolum(metin, b).splitlines() if s.strip().startswith("- ")]


def _alan(satirlar):
    return {k.strip(): v.strip() for k, _, v in (s.partition(":") for s in satirlar)}


def _suz(s, hata, yer):
    """Anahtar değeri mesaja yazılmaz; metakarakter/indirici satırı reddedilir."""
    if ANAHTAR.search(s):
        hata.append(f"{yer}: düz anahtar değeri (yalnız ${{AD}})")
    elif META.search(s) or KABUK.search(s):
        hata.append(f"{yer}: serbest kabuk/indirici: {s}")
    else:
        return False
    return True


def adimlar(satirlar, i, hata, yer):
    """i=0 kurulum fiili, 1 geri alma fiili → argv listeleri."""
    out = []
    for s in satirlar:
        tur, _, arg = s.partition(":")
        tur, arg = tur.strip(), arg.split()
        if tur not in FIIL or not arg:
            hata.append(f"{yer}: bilinmeyen tür ya da argümansız: {s}")
        elif not _suz(s, hata, yer):
            duz = [x.partition("=")[0] for x in arg if tur == "mcp" and re.fullmatch(r"[A-Za-z_]\w*=.+", x) and not ENVREF.fullmatch(x.partition("=")[2])]
            if duz:
                hata.append(f"{yer}: düz anahtar değeri {', '.join(duz)} (yalnız ${{AD}})")
            else:
                out.append(FIIL[tur][i] + arg)
    return out


def kopru_oku(kok):
    y = Path(kok) / "tools" / "cc-kopru" / "kopru.json"
    return json.loads(y.read_text(encoding="utf-8")) if y.is_file() else {}


def _kopru_yaz(kok, k):
    (Path(kok) / "tools" / "cc-kopru" / "kopru.json").write_bytes(json.dumps(k, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def bicim(metin, kopru=None):
    """(plan, hatalar). Kurulum · Duman testi · Geri alma zorunlu; Köprü izni ve Ayar isteğe bağlı."""
    hata, plan = [], {"duman": None, "kopru": None, "ayar": [], "telemetri": []}
    if re.search(r"^telemetri:\s*(açık|acik|evet|on)\b", metin, re.M | re.I):  # 17 K6: varsayılan açık telemetri kapatılmadan plan yok
        ts = _satirlar(metin, "Telemetri kapatma")
        if not ts:
            hata.append("Telemetri açık ama ## Telemetri kapatma bölümü yok ya da boş")
        plan["telemetri"] = [s for s in ts if not _suz(s, hata, "Telemetri kapatma")]
    for b, i in (("Kurulum", 0), ("Geri alma", 1)):
        ss = _satirlar(metin, b)
        if not ss:
            hata.append(f"{b} bölümü yok ya da boş")
        plan["kurulum" if i == 0 else "geri"] = adimlar(ss, i, hata, b)
        if i:
            plan["geri_adim"] = ss
    d = _alan(_satirlar(metin, "Duman testi"))
    if not d.get("komut"):
        hata.append("Duman testi bölümü yok ya da komutsuz")
    elif not _suz(d["komut"], hata, "Duman testi"):
        try:
            plan["duman"] = (d["komut"].split(), int(d.get("cikis") or 0), re.compile(d["desen"]) if d.get("desen") else None)
        except (ValueError, re.error) as e:
            hata.append(f"Duman testi: {e}")
    if k := _alan(_satirlar(metin, "Köprü izni")):
        arac, alt = k.get("arac", ""), [x.strip() for x in k.get("altIzin", "").split(",") if x.strip()]
        if not re.fullmatch(r"[\w.-]+", arac) or not alt:
            hata.append("Köprü izni: arac ve altIzin gerekli")
        elif yasak := [x for x in alt if x not in SALT_OKUR]:
            hata.append(f"Köprü izni salt-okur değil: {', '.join(yasak)}")
        elif arac in (kopru or {}).get("izinli", {}):
            hata.append(f"Köprü izni: {arac} kopru.json'da zaten var (yalnız yeni araç girdisi)")
        else:
            plan["kopru"] = (arac, alt)
    for s in _satirlar(metin, "Ayar"):
        yol, _, deger = (x.strip() for x in s.partition(": "))
        p = yol.split(".")
        if len(p) != 2 or ANAHTAR.search(deger):
            hata.append(f"Ayar: iki seviyeli yol ve anahtarsız değer: {yol}")
        elif p[0] == "env" and not ENVREF.fullmatch(deger):
            hata.append(f"Ayar: {yol} değeri yalnız ${{AD}}")
        else:
            try:
                p[0] == "env" or json.loads(deger)
                plan["ayar"].append((p, deger))
            except ValueError:
                hata.append(f"Ayar: {yol} değeri JSON değil")
    return plan, hata


def ps_blok(ayar):
    """settings.json değişikliği KOŞULMAZ; PowerShell 5.1 bloğu rapora. env değeri yazılmaz, kullanıcı ortamından okunur."""
    s = ['$y = "$env:USERPROFILE\\.claude\\settings.json"', "$s = Get-Content $y -Raw | ConvertFrom-Json"]
    for (ust, alt), deger in ayar:
        v = f"([Environment]::GetEnvironmentVariable('{deger[2:-1]}','User'))" if ust == "env" else f"('{deger.replace(chr(39), chr(39) * 2)}' | ConvertFrom-Json)"
        s += [f"if (-not $s.'{ust}') {{ $s | Add-Member -NotePropertyName '{ust}' -NotePropertyValue ([pscustomobject]@{{}}) }}",
              f"$s.'{ust}' | Add-Member -Force -NotePropertyName '{alt}' -NotePropertyValue {v}"]
    return s + ["[IO.File]::WriteAllText($y, ($s | ConvertTo-Json -Depth 100))"]


def _kos(ctx, args, timeout=600, **k):
    args = [str(x) for x in args]
    w = not Path(args[0]).suffix and shutil.which(args[0])
    if w and w.lower().endswith((".cmd", ".bat")):  # npm kısayolu: çıplak adla CreateProcess bulamaz (OSError 2)
        args[0] = w
    try:
        return ctx["kos"](args, timeout=timeout, **k)
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, b"", str(e).encode()


def _kok(ctx):
    return Path(ctx["env"].get("VIDEO_UYGULA_KOK") or KOK)


def _kayit(kok, ad, alan):
    """Adın son girdisi alanla birleşip sona eklenir (23c: append-only, eski satır değişmez)."""
    ky = kok / "docs" / "kurulumlar" / "kayit.jsonl"
    eski = next((x for x in reversed(tr.kayit_oku(ky)) if x["ad"] == ad), {"ad": ad})
    tr.kayit_ekle(ky, [{**eski, **alan}])


def onay(ns, ctx):
    kok = _kok(ctx)
    b = kok / "docs" / "kurulumlar" / "bekleyen" / f"{ns.ad}.md"
    if not b.is_file():
        print(f"bekleyen yok: {b}")
        return 1
    kj = kopru_oku(kok)
    plan, hata = bicim(b.read_text(encoding="utf-8"), kj)
    if hata:
        print("biçim hatası, koşulmadı: " + " · ".join(hata))
        return 2
    argv, cikis, desen = plan["duman"]
    satir = ([f"kur: {' '.join(a)}" for a in plan["kurulum"]] + [f"duman: {' '.join(argv)} → rc {cikis}" + (f" · /{desen.pattern}/" if desen else "")]
             + [f"geri alma: {' '.join(a)}" for a in plan["geri"]] + [f"telemetri kapat (elle, kurulumdan hemen sonra): {s}" for s in plan["telemetri"]])
    if plan["kopru"]:
        satir.append(f"köprü: izinli.{plan['kopru'][0]}.altIzin = {plan['kopru'][1]} (Desktop yeniden başlatma gerekli)")
    if plan["ayar"]:
        satir += ["settings.json KOŞULMAZ; elle (PowerShell):", *ps_blok(plan["ayar"])]
    if ns.kuru:
        print("\n".join([f"KURU {ns.ad} — hiçbir şey koşmaz", *satir]))
        return 0
    for a in plan["kurulum"]:
        if _kos(ctx, a)[0]:
            return _red(ctx, kok, ns.ad, plan, f"RED(adım): {' '.join(a)}")
    rc, out, err = _kos(ctx, argv, 120)
    if rc != cikis or (desen and not desen.search((out + err).decode("utf-8", "replace"))):
        return _red(ctx, kok, ns.ad, plan, f"RED(duman): rc {rc}")
    if plan["kopru"]:
        kj.setdefault("izinli", {})[plan["kopru"][0]] = {"altIzin": plan["kopru"][1]}
        _kopru_yaz(kok, kj)
    _kayit(kok, ns.ad, {"karar": "KUR", "kurulum_tarihi": date.today().isoformat(), "geri_alma": plan["geri_adim"],
                        "kopru": plan["kopru"] and plan["kopru"][0]})
    b.unlink()
    print("\n".join([f"KUR {ns.ad} · duman geçti", *satir]) + ("\nDesktop yeniden başlatma gerekli" if plan["kopru"] else ""))
    return 0


def _red(ctx, kok, ad, plan, karar):
    """Duman ya da adım başarısız: kurulum yerinde bırakılmaz, geri alma adımlarının hepsi koşar."""
    geri = [" ".join(a) for a in plan["geri"] if _kos(ctx, a)[0]]
    _kayit(kok, ad, {"karar": karar, "tarih": date.today().isoformat()})
    print(f"{karar} · geri alma koştu" + (f" · başarısız: {'; '.join(geri)}" if geri else ""))
    return 1


def geri_al(ns, ctx):
    kok = _kok(ctx)
    g = next((x for x in reversed(tr.kayit_oku(kok / "docs" / "kurulumlar" / "kayit.jsonl")) if x["ad"] == ns.ad and x.get("karar") == "KUR"), None)
    if not g:
        print(f"kayıtta kurulu (KUR) {ns.ad} yok")
        return 1
    hata = []
    geri = adimlar(g.get("geri_alma") or [], 1, hata, "Geri alma")
    if hata:
        print("geri alma kaydı bozuk, koşulmadı: " + " · ".join(hata))
        return 2
    kalan = [" ".join(a) for a in geri if _kos(ctx, a)[0]]
    if g.get("kopru"):
        kj = kopru_oku(kok)
        kj.get("izinli", {}).pop(g["kopru"], None)
        _kopru_yaz(kok, kj)
    karar = "geri alındı" if not kalan else f"geri alma eksik: {'; '.join(kalan)}"
    _kayit(kok, ns.ad, {"karar": karar, "geri_alma_tarihi": date.today().isoformat()})
    print(f"{ns.ad}: {karar}" + (" · köprü girdisi çıkarıldı (Desktop yeniden başlatma gerekli)" if g.get("kopru") else ""))
    return 0 if not kalan else 1


IZLI = ("mcpServers", "hooks")
AGSIZ = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN", "OPENAI_API_KEY")
_sha = lambda b: hashlib.sha256(b).hexdigest()


def _izli(j):
    """~/.claude.json'un yalnız ayar anahtarları; CC geri kalanını (sayaç, proje istatistiği) her oturumda yazar."""
    return {**{a: j[a] for a in IZLI if a in j},
            **{f"projects/{p}/{a}": v[a] for p, v in (j.get("projects") or {}).items() for a in IZLI if a in v}}


def parmak(ev):
    """20b ad → sha: settings.json tam · ~/.claude.json izli anahtarlar · hooks/ her dosya · skills/ üst düzey ad + SKILL.md (1.4 GB tam taranmaz)."""
    cl, p = ev / ".claude", {}
    if (cl / "settings.json").is_file():
        p["settings.json"] = _sha((cl / "settings.json").read_bytes())
    if (ev / ".claude.json").is_file():
        p |= {f".claude.json:{a}": _sha(json.dumps(v, sort_keys=True).encode())
              for a, v in _izli(json.loads((ev / ".claude.json").read_text(encoding="utf-8"))).items()}
    for f in sorted((cl / "hooks").rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            p[f.relative_to(cl).as_posix()] = _sha(f.read_bytes())
    for s in sorted((cl / "skills").glob("*")):
        p[f"skills/{s.name}"] = _sha((s / "SKILL.md").read_bytes()) if (s / "SKILL.md").is_file() else ""
    return p


def _yol(ev, ad):
    """Parmak izi adının dosyası; yedek için ev yerine yedek dizini verilir."""
    return ev / ".claude" / (f"{ad}/SKILL.md" if ad.startswith("skills/") else ad)


def _geri_yukle(ev, d, fark, once):
    """Önceki bayt/anahtar yedekten; öncede olmayan dosya/skill karantinaya taşınır (silinmez)."""
    yedek = json.loads((d / "yedek" / "claude.json").read_text(encoding="utf-8"))
    for ad in fark:
        if ad.startswith(".claude.json:"):
            j = json.loads((ev / ".claude.json").read_text(encoding="utf-8"))
            a = ad.split(":", 1)[1]
            *ust, son = a.split("/")
            h = j
            for x in ust:
                h = h[x]
            if a in yedek:
                h[son] = yedek[a]
            else:
                h.pop(son, None)
            (ev / ".claude.json").write_bytes(json.dumps(j, indent=2, ensure_ascii=False).encode("utf-8"))
        elif ad in once:
            _yol(ev, ad).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(_yol(d / "yedek", ad), _yol(ev, ad))
        else:
            k = d / "karantina" / Path(ad).name
            k.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(ev / ".claude" / ad), str(k))


def koru(ns, ctx):
    """20b K0: --al parmak izi + yedek; sonra (varsa `-- komut` koşulur) karşılaştır: fark → geri yükle, yalnız ad, rc 1 = DUR."""
    ev, d = Path(ctx["env"].get("VIDEO_EV") or Path.home()), _kok(ctx) / "docs" / "denemeler" / ".kos" / "caveman"
    if ns.al:
        p = parmak(ev)
        shutil.rmtree(d / "yedek", ignore_errors=True)
        (d / "yedek").mkdir(parents=True)
        for ad in p:
            if not ad.startswith(".claude.json:") and _yol(ev, ad).is_file():
                _yol(d / "yedek", ad).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(_yol(ev, ad), _yol(d / "yedek", ad))
        j = ev / ".claude.json"
        (d / "yedek" / "claude.json").write_bytes(json.dumps(_izli(json.loads(j.read_text(encoding="utf-8"))) if j.is_file() else {}).encode())
        (d / "once.json").write_bytes(json.dumps(p, indent=1).encode())
        print(f"parmak izi alındı: {len(p)} ad · {d / 'once.json'}")
        return 0
    if not (d / "once.json").is_file():
        print("hata: önce `video koru --al`")
        return 1
    arg, rc = ns.arg[1:] if ns.arg[:1] == ["--"] else ns.arg, 0
    if arg:
        env = {k: v for k, v in ctx["env"].items() if not (ns.agsiz and k in AGSIZ)}
        if ns.agsiz:
            env["ANTHROPIC_BASE_URL"] = env["OPENAI_BASE_URL"] = "http://127.0.0.1:9"
        rc, out, err = _kos(ctx, arg, 3600, env=env)
        sys.stdout.write((out + err).decode("utf-8", "replace"))
    once, simdi = json.loads((d / "once.json").read_text(encoding="utf-8")), parmak(ev)
    fark = sorted(a for a in once.keys() | simdi.keys() if once.get(a) != simdi.get(a))
    if not fark:
        print(f"parmak izi eşit ({len(simdi)} ad)")
        return rc
    _geri_yukle(ev, d, fark, once)
    print(f"DUR: onaysız ayar değişikliği, geri yüklendi: {', '.join(fark)}")
    return 1


def esik(s):
    def sayi(desen, yok):
        x = re.search(desen, s or "", re.I)
        return float(x[1].replace(",", ".")) if x else yok
    e = {"cikti": sayi(r"çıktı[^%]*%\s*(\d+(?:[.,]\d+)?)", None), "maliyet": sayi(r"maliyet[^%]*%\s*(\d+(?:[.,]\d+)?)", None)}
    if (g := sayi(r"girdi[^%]*%\s*(\d+(?:[.,]\d+)?)", None)) is None:  # 20a: girdi eşiği yoksa çıktı varsayılanı 25
        return {**e, "cikti": 25 if e["cikti"] is None else e["cikti"]}
    return {"cikti": e["cikti"], "girdi": g, "maliyet": e["maliyet"]}


def takas(s, d, esik_ok):
    """23b K9 omer-kurallar:21 kalite takası, sınır dahil. s tasarruf %, d kalite düşüşü % (bant içi 0) → (karar, tutan kademe)."""
    if d == 0:
        return ("AL", "düşüş 0, eşik aşıldı") if esik_ok else ("RED(token)", "düşüş 0, eşik aşılmadı")
    if d <= 10 and s >= 25:
        return "AL", "düşüş ≤%10 & tasarruf ≥%25"
    if d <= 15 and s >= 30:
        return "AL", "düşüş ≤%15 & tasarruf ≥%30"
    if 15 < d <= 20 and s >= 75:
        return "AL", "düşüş %15–20 & tasarruf ≥%75"
    if 15 < d <= 20:
        return ("SOR", "düşüş %15–20 & tasarruf %50–75") if s >= 50 else ("RED(takas)", "düşüş %15–20 & tasarruf <%50")
    if d > 20:
        return ("SOR", "düşüş >%20 & tasarruf ≥%50") if s >= 50 else ("RED(takas)", "düşüş >%20 & tasarruf <%50")
    return ("SOR", "ara durum, tasarruf ≥%25") if s >= 25 else ("RED(takas)", "tasarruf <%25, düşüş >0")


def tasarruf(a, b):
    """Göreli düşüş % (çıktı · girdi · sıcak maliyet); temel 0 ise 0."""
    return {k: round((a[k] - b[k]) / a[k] * 100, 6) if a.get(k) else 0.0 for k in ("cikti", "girdi", "maliyet")}


def karar(a, b, e, gurultu, basari):
    """23b K9: tasarruf = sıcak koşu maliyetinin göreli düşüşü; düşüş = max(kalite puanı göreli düşüşü, ort. başarı göreli düşüşü),
    kalite düşüşü A'nın tekrar gürültüsü bandında (max(gürültü, 0.1)) ise 0 → takas(). Eşik (## Başarı eşiği) yalnız düşüş 0'da."""
    t, bant = tasarruf(a, b), max(gurultu, 0.1)
    esik_ok = all(e.get(x) is None or t[x] >= e[x] for x in ("cikti", "girdi", "maliyet"))
    kd = 0.0 if round(a["kalite"] - b["kalite"] - bant, 6) <= 0 else (a["kalite"] - b["kalite"]) / a["kalite"] * 100
    bd = max(0.0, (a["basari"] - b["basari"]) / a["basari"] * 100) if a.get("basari") and "basari" in b else 0.0
    d = round(max(kd, bd), 6)
    k, kademe = takas(t["maliyet"], d, esik_ok)
    dusen = [i + 1 for i, (sa, sb) in enumerate(basari) if sb < sa]
    return (f"{k} [kademe: {kademe}]: tasarruf %{t['maliyet']:.1f} (sıcak $) · düşüş %{d:.1f} (kalite {a['kalite']:.2f}→{b['kalite']:.2f} bant {bant:.2f} · "
            f"başarı {a.get('basari', 0):.2f}→{b.get('basari', 0):.2f}; düşen görev: {', '.join(map(str, dusen)) or 'yok'}) · "
            f"çıktı −%{t['cikti']:.1f} · girdi −%{t['girdi']:.1f}")


def mekanizma_kaydi(kok, ad, t, dusen, hipotez):
    """23b K10(a): token tasarrufu (çıktı|girdi|maliyet >0) olan her özellik, kalite kararından bağımsız: docs/mekanizmalar/<ad>.md'ye bölüm (varsa dokunmaz)."""
    if not any(v > 0 for v in t.values()):
        return None
    y = Path(kok) / "docs" / "mekanizmalar" / f"{ad}.md"
    eski = y.read_text(encoding="utf-8") if y.is_file() else f"# Mekanizma: {ad}\n"
    if "## Tasarruf mekanizması" in eski:
        return y
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(eski.rstrip("\n") + "\n\n## Tasarruf mekanizması (23b K10a)\n"
                 f"- ölçülen: çıktı −%{t['cikti']:.1f} · girdi −%{t['girdi']:.1f} · sıcak $ −%{t['maliyet']:.1f}\n"
                 f"- neyi kısaltıyor/atlıyor/önbellekliyor: {hipotez or '? (deneme ## Hipotez boş)'}\n"
                 f"- kaliteyi etkileyen parça (düşen görevler): {', '.join(dusen) or 'yok'}\n"
                 f"- ayrılabilir mi: {'evet-aday (kayıp görevlerin bir kısmında)' if dusen else 'kalite kaybı yok, ayrıştırma gereksiz'}\n", encoding="utf-8")
    return y


def ayristir_aday(kok, ad, k, t, dusen):
    """23b K10(b): yalnız RED(kalite|takas)/SOR ve token tasarrufu varsa docs/uyarlamalar/<ad>-ayristir.md."""
    if not k.startswith(("SOR", "RED(kalite", "RED(takas")) or not any(v > 0 for v in t.values()):
        return None
    y = Path(kok) / "docs" / "uyarlamalar" / f"{ad}-ayristir.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    parca = " · ".join(f"{n} −%{t[x]:.1f}" for x, n in (("cikti", "çıktı"), ("girdi", "girdi"), ("maliyet", "sıcak $")) if t[x] > 0)
    y.write_text(f"# Ayrıştırma adayı: {ad}\n\n23b K10(b) · karar: {k[:160]} · `AYRIŞTIR {ad}` → `video uret {ad}-oz --tur 0..2`\n\n"
                 f"## Alınacak tasarruf parçası\n{parca} (mekanizma: docs/mekanizmalar/{ad}.md)\n\n"
                 f"## Ayıklanacak/onarılacak kalite parçası\nkalite/başarı düşen görevler: {', '.join(dusen) or '? (ölçümde görev ayrımı yok)'}\n\n"
                 "## Onarım fikri\nteknik terimleri, kod bloklarını, hata/komut satırlarını ve sayıları aynen koru; yalnız dolgu metni "
                 "(hitap, tekrar, geçiş cümlesi) kısalt. Her turda düşen görevlerin çıktısından kaybın sebebi çıkarılır, sürüm düzeltilir.\n\n"
                 "## Başarı eşiği\nsıcak maliyet −%25\n", encoding="utf-8")
    return y


def _parca(g):
    """Görev dosyası → (istem satırları, beklenen maddeleri); `beklenen:` satırından sonrası modele gitmez."""
    ss = g.read_text(encoding="utf-8").splitlines()
    i = next((i for i, s in enumerate(ss) if s.strip() == "beklenen:"), len(ss))
    return ss[:i], [s.strip()[2:].strip() for s in ss[i + 1:] if s.strip().startswith("- ")]


def _istem(g):
    ss = _parca(g)[0]
    ek = [f"\n\n{x[6:].strip()}:\n```\n{(g.parent / x[6:].strip()).read_text(encoding='utf-8')}```" for x in ss if x.startswith("dosya:")]
    ek += [f"\n\nDosya: {(g.parent / x[4:].strip()).resolve()}" for x in ss if x.startswith("oku:")]  # 20a okuma: içerik gömülmez, model araçla okur
    return "\n".join(x for x in ss if not x.startswith(("dosya:", "oku:", "araclar:"))).strip() + "".join(ek)


def _kollar(metin, kok, env, hata):
    """20a `## Kollar`: `- ad: temel · env K=V … · önek komut · sistem yol · mcp yol` (V düz adres ya da ${AD}; anahtar değeri reddedilir, mesaja yazılmaz).
    Bölüm yoksa 18 A/B: A düz, B `sistem <## Talimat>`. İlk `temel` (yoksa ilk kol) karşılaştırma tabanıdır."""
    ss = _satirlar(metin, "Kollar")
    if not ss:
        ty = next((s.strip() for s in tr.bolum(metin, "Talimat").splitlines() if s.strip()), "")
        ss = ["A: temel", f"B: sistem {ty}"] if ty else []
    kollar = []
    for s in ss:
        ad, _, tanim = s.partition(":")
        k = {"ad": ad.strip(), "temel": False, "env": {}, "onek": [], "ek": [], "rapor": [], "kimlik": ""}
        for p in (x.strip() for x in tanim.split("·") if x.strip()):
            tur, _, arg = p.partition(" ")
            if tur == "temel":
                k["temel"] = True
            elif tur == "env":
                for x in arg.split():
                    a, _, v = x.partition("=")
                    if not re.fullmatch(r"[A-Za-z_]\w*", a) or not ENVREF.fullmatch(v) and (ANAHTAR.search(v) or META.search(v)):
                        hata.append(f"kol {k['ad']}: env {a} değeri yalnız adres ya da ${{AD}}")
                    elif ENVREF.fullmatch(v) and v[2:-1] not in env:
                        hata.append(f"kol {k['ad']}: {v} ortamda yok")
                    else:
                        k["env"][a] = v
                k["rapor"].append(f"env {arg.strip()}")
            elif tur == "önek" and not _suz(arg, hata, f"kol {k['ad']}"):
                k["onek"] = arg.split()
                k["rapor"].append(f"önek {arg.strip()}")
            elif tur == "sistem" and (kok / arg.strip()).is_file():
                k["ek"] = ["--append-system-prompt", govde((kok / arg.strip()).read_text(encoding="utf-8")), *k["ek"]]
                k["kimlik"] = k["ek"][1]  # 18 önbellek hash'i korunur
                k["rapor"].append(f"sistem {arg.strip()}")
            elif tur == "mcp" and (kok / arg.strip()).is_file():  # 20b-devam: o çağrıya özel MCP; global ayar değişmez
                k["mcp"] = list(json.loads((kok / arg.strip()).read_text(encoding="utf-8"))["mcpServers"])
                k["ek"] += ["--mcp-config", str(kok / arg.strip())]
                k["kimlik"] += "\0mcp " + arg.strip()
                k["rapor"].append(f"mcp {arg.strip()}")
            elif tur not in ("önek",):
                hata.append(f"kol {k['ad']}: {tur} {arg.strip() if tur == 'sistem' else ''} geçersiz")
        if k["env"] or k["onek"]:
            k["kimlik"] += "\0" + json.dumps([k["onek"], k["env"]], sort_keys=True)
        kollar.append(k)
    if kollar and not any(k["temel"] for k in kollar):
        kollar[0]["temel"] = True
    return kollar


KORUNUM_Q = {"type": "score", "instructions": "KURAL (state) SIKIŞTIRILMIŞ METİN'de anlamca korunmuş mu?", "criteria": ["yok", "kısmen", "korunmuş"]}


def _sikistir(ns, ctx, metin, d):
    """20a compress: `## Kaynak` .kos/<ad>/ altına KOPYALANIR, `## Komut` yalnız kopyada koşar ({kopya}); kaynak baytı değişirse geri yazılır, RED.
    claude -p 0; token önce/sonra (c.token) + kaynaktaki her `- ` kuralı için Jev korunum puanı (≥1.5 korunmuş)."""
    kaynak = Path(tr.bolum(metin, "Kaynak").strip().splitlines()[0].strip())
    komut = next((s.strip() for s in tr.bolum(metin, "Komut").splitlines() if s.strip()), "")
    if not kaynak.is_file() or "{kopya}" not in komut or _suz(komut, hata := [], "Komut"):
        print(f"compress eksik: ## Kaynak dosyası ya da {{kopya}}'lı ## Komut yok/geçersiz {' · '.join(hata)}")
        return 1
    once = kaynak.read_bytes()
    kopya = d / ".kos" / ns.ad / kaynak.name
    kopya.parent.mkdir(parents=True, exist_ok=True)
    kopya.write_bytes(once)
    rc = _kos(ctx, [x.replace("{kopya}", str(kopya)) for x in komut.split()], 600)[0]
    if kaynak.read_bytes() != once:
        kaynak.write_bytes(once)
        print(f"RED: komut kaynak dosyaya yazdı ({kaynak}); özgün bayt geri yazıldı")
        return 1
    if rc:
        print(f"hata: komut rc {rc}")
        return 1
    ilk, sonra = once.decode("utf-8"), kopya.read_text(encoding="utf-8")
    kurallar = [s.strip()[2:].strip() for s in ilk.splitlines() if s.strip().startswith("- ")]
    t = c.Tasiyici(env=ctx["env"], en_fazla=max(len(kurallar), 1), gonder=ctx["gonder"], istek_tavan=ns.istek_tavan)
    cv = t.yargila([f"KURAL:\n{k}\n\nSIKIŞTIRILMIŞ METİN:\n{sonra}" for k in kurallar], {"korunum": KORUNUM_Q}) if kurallar else []
    kayip = [k for k, x in zip(kurallar, cv) if not x or x["korunum"]["score"] < 1.5]
    a, b = c.token(ilk), c.token(sonra)
    dus, esik_t = round((a - b) / a * 100, 1) if a else 0.0, float((re.search(r"token[^%]*%\s*(\d+)", tr.bolum(metin, "Başarı eşiği")) or [0, 30])[1])
    red = [x for x, ok in (("token", dus >= esik_t), ("kural", not kayip)) if not ok]
    k = ("KUR önerisi → ONAY" if not red else f"RED({', '.join(red)})") + f": token {a} → {b} (−%{dus}, eşik %{esik_t:g}) · korunmayan kural {len(kayip)}/{len(kurallar)}"
    satir = [f"# Deneme sonucu: {ns.ad}", "", f"{date.today().isoformat()} · compress · claude -p 0 · Jev istek {t.istek} · kaynak dokunulmadı (bayt aynı): {kaynak.as_posix()}",
             f"kopya: {kopya.relative_to(d).as_posix()} · komut: {komut}", "", f"token {a} → {b} (−%{dus})", f"korunmayan kural {len(kayip)}/{len(kurallar)}",
             *[f"- {x}" for x in kayip], "", "## Karar", k, ""]
    (d / f"{ns.ad}-sonuc.md").write_text("\n".join(satir), encoding="utf-8")
    _kayit(_kok(ctx), ns.ad, {"karar": k, "deneme": f"docs/denemeler/{ns.ad}-sonuc.md", "tarih": date.today().isoformat()})
    print(k)
    return 0


def _re_ara(ciftler, sn):
    """[(desen, [metin])] → [[bool]] ayrı süreçte; felaket geri izleme ana süreci kilitlemesin. Zaman aşımı/geçersiz desen → None."""
    try:
        r = subprocess.run([sys.executable, "-c", _RE_KOD], input=json.dumps(ciftler).encode(), capture_output=True, timeout=sn)
        return json.loads(r.stdout) if not r.returncode else None
    except (subprocess.TimeoutExpired, ValueError):
        return None


def desen_denetle(g):
    """18: görev yüklenirken, koşudan önce — her regex 50 KB düşmanca metinde DESEN_SN içinde bitmeli. Hata metni ya da None."""
    d = [x.partition(":")[2].strip() for x in _parca(g)[1] if x.partition(":")[0].strip() in REGEX]
    if d and _re_ara([(x, DUSMAN) for x in d], DESEN_SN) is None:
        return f"{g.name}: desen {DESEN_SN} sn'de bitmedi ya da geçersiz (felaket geri izleme?); satır sayısı için satir-en-fazla"
    return None


def basari(g, yanit, kos):
    """18 K1 makine kontrolü → (başarı, neden): her `olgu:` var · hiçbir `yasak:` yok · `satir-en-fazla/en-az: N` boş olmayan satır
    (kodla sayılır) · `satir-desen:` her boş olmayan satır tam eşleşir · `pytest:` yanıttaki son python bloğu görevin `dosya:`ı yerine
    geçici dizine yazılır, test yanında geçer. Regex'ler ayrı süreçte KONTROL_SN ile; aşılırsa başarısız. Beklenen yoksa başarı."""
    ss, bk = _parca(g)
    satir = [x.strip() for x in yanit.splitlines() if x.strip()]
    bk = [tuple(x.strip() for x in s.partition(":")[::2]) for s in bk]
    for tur, d in bk:
        if (tur == "satir-en-fazla" and len(satir) > int(d)) or (tur == "satir-en-az" and len(satir) < int(d)):
            return False, f"{tur} {d}: {len(satir)} satır"
    rx = [(tur, d) for tur, d in bk if tur in REGEX]
    if rx:
        r = _re_ara([(fr"\A(?:{d})\Z", satir) if tur == "satir-desen" else (d, [yanit]) for tur, d in rx], KONTROL_SN)
        if r is None:
            return False, "kontrol zaman aşımı"
        for (tur, d), v in zip(rx, r):
            if (tur == "olgu" and not v[0]) or (tur == "yasak" and v[0]) or (tur == "satir-desen" and not all(v)):
                return False, f"{tur}: {d}"
    for tur, d in bk:
        if tur == "pytest":
            kod = re.findall(r"```(?:python|py)?[ \t]*\r?\n(.*?)```", yanit, re.S)
            dosya = next((x[6:].strip() for x in ss if x.startswith("dosya:")), None)
            if not kod or not dosya:
                return False, "pytest: python bloğu yok"
            with tempfile.TemporaryDirectory() as t:
                (Path(t) / Path(dosya).name).write_text(kod[-1], encoding="utf-8")
                shutil.copy2(g.parent / d, Path(t) / Path(d).name)
                # pytest'li yalıtık ortam: alt süreçte "python" çağıranın pytest'siz yorumlayıcısına çözülebiliyor
                if kos(["uv", "run", "--no-project", "--with", "pytest", "python", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        str(Path(t) / Path(d).name)], timeout=120)[0]:
                    return False, "pytest başarısız"
    return True, ""


def govde(metin):
    return re.sub(r"\A---\r?\n.*?\r?\n---\r?\n", "", metin, count=1, flags=re.S)


def _ngram(s, n=8):
    w = re.findall(r"\w+", s.casefold())
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def ortusme(taslak, kaynak):
    """Taslağın 8-gram'larının kaynakta da geçen payı (küçük harf, kelime)."""
    t = _ngram(taslak)
    return len(t & _ngram(kaynak)) / len(t) if t else 0.0


def _mcp_say(env, sid, sunucular):
    """20b-devam: oturum transkriptinde (~/.claude/projects/*/<sid>.jsonl) yalnız kolun MCP sunucularına giden araç çağrısı sayısı."""
    t = next((Path(env.get("VIDEO_EV") or Path.home()) / ".claude" / "projects").glob(f"*/{sid}.jsonl"), None) if sid and sunucular else None
    n = 0
    for s in t.read_text(encoding="utf-8").splitlines() if t else []:
        try:
            ic = json.loads(s).get("message", {}).get("content")
        except ValueError:
            continue
        n += sum(1 for x in ic if isinstance(x, dict) and x.get("type") == "tool_use"
                 and str(x.get("name", "")).startswith(tuple(f"mcp__{a}__" for a in sunucular))) if isinstance(ic, list) else 0
    return n


def dene(ns, ctx):
    env, kok = ctx["env"], _kok(ctx)
    d = kok / "docs" / "denemeler"
    metin = (d / f"{ns.ad}.md").read_text(encoding="utf-8")
    if tr.bolum(metin, "Kaynak").strip():
        return _sikistir(ns, ctx, metin, d)
    set_ = getattr(ns, "gorevler", None)
    gd = d / ("gorevler" if not set_ else f"gorevler-{set_}")
    sec = _satirlar(metin, "Görevler")
    gorevler = [g for g in sorted(gd.glob("*.md")) if not sec or g.stem in sec]
    kollar = _kollar(metin, kok, env, hata := [])
    if hata or len(kollar) < 2 or not gorevler:
        print(f"deneme eksik: ≥2 kol (## Kollar ya da ## Talimat) ve {gd.relative_to(kok).as_posix()}/*.md gerekli {' · '.join(hata)}")
        return 1
    if h := [x for g in gorevler if (x := desen_denetle(g))]:
        print("görev reddedildi, koşulmadı: " + " · ".join(h), flush=True)
        return 1
    istemler = [_istem(g) for g in gorevler]
    on = d / ".kos" / ns.ad  # sürdürülebilir koşu: ücretli çağrı sonucu hash'iyle saklanır, aynısı yeniden çağrılmaz
    plan = []
    for gi, (g, ist) in enumerate(zip(gorevler, istemler)):
        araclar = next((x[8:].strip() for x in _parca(g)[0] if x.startswith("araclar:")), None)
        for n in (1, 2):  # 20a: her kol 2 koşu (soğuk · sıcak), görev içinde karışık sıra a1 b1 a2 b2 — önbellek kayması tek kolu kayırmasın
            for k in kollar:
                args = [*k["onek"], "claude", "-p", ist, "--model", "sonnet", "--output-format", "json", *k["ek"]]
                args += ["--allowedTools", araclar + "".join(f",mcp__{x}" for x in k.get("mcp", []))] if araclar else []
                if duz := {x: v for x, v in k["env"].items() if not ENVREF.fullmatch(v)}:  # settings.json env'i süreç env'ini ezer; ${AD} argv'ye girmez
                    args += ["--settings", json.dumps({"env": duz})]
                hs = hashlib.sha256(f"{ist}\0{k['kimlik']}".encode()).hexdigest()[:16]
                y = on / f"{g.stem}-{k['ad']}-{n}.json"
                try:
                    j = json.loads(y.read_text(encoding="utf-8"))
                    j = j["j"] if j.get("hash") == hs else None
                except (OSError, ValueError, KeyError):
                    j = None
                plan.append((gi, g, k, n, args, hs, y, j))
    if (gerek := sum(p[-1] is None for p in plan)) > ns.tavan:
        print(f"tavan: {gerek} claude -p gerekir (görev × kol × 2, önbellek hariç), --tavan {ns.tavan}; koşulmadı")
        return 1
    olcum = []
    for i, (gi, g, k, n, args, hs, y, j) in enumerate(plan, 1):
        kol = k["ad"]
        alt_env = {**env, "JEV_SKILL_HOOK": "0", **{x: env[v[2:-1]] if ENVREF.fullmatch(v) else v for x, v in k["env"].items()}}  # hook kollara farklı skill önerisi enjekte etmesin
        kaynak = "önbellek"
        if j is None:
            kaynak = "claude -p"
            rc, out, err = _kos(ctx, args, 600, env=alt_env)
            try:
                j = json.loads(out)
            except ValueError:
                j = {}
            if rc or j.get("is_error") or "result" not in j:
                print(f"hata: claude -p {kol} rc {rc}: {(err or out).decode('utf-8', 'replace')[-200:]}", flush=True)
                return 1
            j = {**{x: j.get(x) for x in ("result", "usage", "duration_ms", "total_cost_usd")}, "mcp": _mcp_say(env, j.get("session_id"), k.get("mcp", []))}
            y.parent.mkdir(parents=True, exist_ok=True)
            y.write_text(json.dumps({"hash": hs, "j": j}, ensure_ascii=False), encoding="utf-8")
        u = j.get("usage") or {}
        ok, neden = basari(g, j["result"], lambda x, timeout: _kos(ctx, x, timeout))
        olcum.append({"kol": kol, "n": n, "gorev": gi,"yanit": j["result"], "cikti": u.get("output_tokens", 0), "sure": (j.get("duration_ms") or 0) / 1000,
                      "girdi": sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")),
                      "maliyet": j.get("total_cost_usd") or 0, "basari": ok, "yeni": kaynak != "önbellek", "mcp": j.get("mcp") or 0})
        print(f"[{i}/{len(plan)}] {g.stem} {kol}{n} {kaynak}: çıktı {u.get('output_tokens', 0)} · ${j.get('total_cost_usd') or 0:.4f} · "
              f"başarı {'evet' if ok else 'hayır (' + neden + ')'}", flush=True)
    t = c.Tasiyici(env=env, en_fazla=len(olcum), gonder=ctx["gonder"], istek_tavan=ns.istek_tavan)
    cv = t.yargila([f"GÖREV:\n{istemler[o['gorev']]}\n\nYANIT:\n{o['yanit']}" for o in olcum], {"kalite": KALITE_Q})
    for o, x in zip(olcum, cv):
        if not x:
            print("hata: Jev kalite puanı yok")
            return 1
        o["kalite"] = x["kalite"]["score"]
    ort = {}
    for k in kollar:
        ok = [o for o in olcum if o["kol"] == k["ad"]]
        ort[k["ad"]] = {f: sum(o[f] for o in ok) / len(ok) for f in ALANLAR + ("basari",)}
        for ad, n in (("soguk", 1), ("sicak", 2)):
            ort[k["ad"]][ad] = sum(o["maliyet"] for o in ok if o["n"] == n) / sum(o["n"] == n for o in ok)
        ort[k["ad"]]["maliyet"] = ort[k["ad"]]["sicak"]  # 20a: karar sıcak koşu maliyetiyle; soğuk yalnız rapor
    tk = next(k["ad"] for k in kollar if k["temel"])
    ob = lambda kol, gi: sorted((o for o in olcum if o["kol"] == kol and o["gorev"] == gi), key=lambda o: o["n"])  # noqa: E731
    gurultu = sum(abs(ob(tk, i)[0]["kalite"] - ob(tk, i)[1]["kalite"]) for i in range(len(gorevler))) / len(gorevler)
    e = esik(tr.bolum(metin, "Başarı eşiği"))
    kararlar = {k["ad"]: karar(ort[tk], ort[k["ad"]], e, gurultu, [tuple(sum(o["basari"] for o in ob(x, i)) / 2 for x in (tk, k["ad"])) for i in range(len(gorevler))])
                for k in kollar if k["ad"] != tk}
    mcp = {k["ad"]: sum(o["mcp"] for o in olcum if o["kol"] == k["ad"]) for k in kollar}
    kararlar.update({k["ad"]: "KARAR YOK: sıkıştırma devreye girmedi (mcp çağrısı 0)" for k in kollar if k.get("mcp") and not mcp[k["ad"]] and k["ad"] != tk})
    kur_ = [f"{v.split(':')[0]} [{ad}]:{v.partition(':')[2]}" for ad, v in kararlar.items() if v.startswith(("AL", "SOR"))]
    kur_.sort(key=lambda x: not x.startswith("AL"))  # AL önce; SOR kendiliğinden AL/RED olmaz
    k = kur_[0] if kur_ else next(iter(kararlar.values())) if len(kararlar) == 1 else "RED(tüm kollar): " + " · ".join(kararlar)
    bugun = date.today().isoformat()
    satir = [f"# Deneme sonucu: {ns.ad}", "", f"{bugun} · sonnet · {len(istemler)} görev ({gd.name}) · {len(kollar)} kol × 2 koşu, karışık sıra · claude -p {len(olcum)} · "
             f"Jev istek {t.istek} · hook kapalı (JEV_SKILL_HOOK=0) · toplam maliyet ${sum(o['maliyet'] for o in olcum):.4f} (bu koşuda yeni çağrı {sum(o['yeni'] for o in olcum)})",
             "Kollar: " + " ; ".join(f"{x['ad']}{' (temel)' if x['temel'] else ''}: {' · '.join(x['rapor']) or 'düz'}" for x in kollar) + f" · gürültü (temel 1-2 kalite farkı ort.) {gurultu:.2f}",
             *(["mcp çağrı: " + " · ".join(f"{a} {n}" for a, n in mcp.items())] if any(k.get("mcp") for k in kollar) else []),
             "", "## Kol ortalamaları", "Karar sıcak (2. koşu) maliyetiyle; soğuk (1. koşu) bilgi.", "",
             "| kol | başarı | kalite 0-3 | çıktı | girdi | süre sn | soğuk $ | sıcak $ |", "|---|---|---|---|---|---|---|---|"]
    satir += [f"| {kol} | {v['basari']:.2f} | {v['kalite']:.2f} | {v['cikti']:.0f} | {v['girdi']:.0f} | {v['sure']:.1f} | {v['soguk']:.4f} | {v['sicak']:.4f} |" for kol, v in ort.items()]
    satir += ["", "## Görev başına", "| görev | kol | başarı 1/2 | kalite 1/2 | çıktı 1/2 | girdi 1/2 |", "|---|---|---|---|---|---|"]
    satir += [f"| {g.stem} | {x['ad']} | " + " | ".join("/".join(f"{o[f]:.2f}" if f == "kalite" else str(int(o[f])) for o in ob(x["ad"], i)) for f in ("basari", "kalite", "cikti", "girdi")) + " |"
              for i, g in enumerate(gorevler) for x in kollar]
    satir += ["", "## Karar", k, *[f"{ad}: {v}" for ad, v in kararlar.items()], ""]
    (d / f"{ns.ad}-sonuc.md").write_text("\n".join(satir), encoding="utf-8")
    _kayit(kok, ns.ad, {"karar": k, "deneme": f"docs/denemeler/{ns.ad}-sonuc.md", "tarih": bugun})
    if kol := next((x["ad"] for x in kollar if x["ad"] != tk and (len(kollar) == 2 or f"[{x['ad']}]" in k)), None):  # 23b K10 + SOR
        tas, bant = tasarruf(ort[tk], ort[kol]), max(gurultu, 0.1)
        fark = {i: sum(o["kalite"] for o in ob(tk, i)) / 2 - sum(o["kalite"] for o in ob(kol, i)) / 2 for i in range(len(gorevler))}
        dusen = [gorevler[i].stem for i in fark if fark[i] > bant or sum(o["basari"] for o in ob(kol, i)) < sum(o["basari"] for o in ob(tk, i))]
        mekanizma_kaydi(kok, ns.ad, tas, dusen, " ".join(tr.bolum(metin, "Hipotez").split()))
        ayristir_aday(kok, ns.ad, k, tas, dusen)
        if k.startswith("SOR"):
            orn = [f"### {gorevler[i].stem} (kalite {-fark[i]:+.2f})\n**{tk}:**\n```\n{ob(tk, i)[-1]['yanit'][:1500]}\n```\n**{kol}:**\n```\n{ob(kol, i)[-1]['yanit'][:1500]}\n```"
                   for i in sorted(fark, key=fark.get, reverse=True)[:2]]
            b = kok / "docs" / "kurulumlar" / "bekleyen" / f"sor-{ns.ad}.md"
            b.parent.mkdir(parents=True, exist_ok=True)
            b.write_text(f"# SOR {ns.ad}\n\n{k}\n\nÖmer karar verir: `AL {ns.ad}` ya da `RED {ns.ad}` → `video karar {ns.ad} AL|RED`. Kendiliğinden AL/RED yapılmaz.\n\n"
                         f"## Tasarruf\nçıktı −%{tas['cikti']:.1f} · girdi −%{tas['girdi']:.1f} · sıcak $ −%{tas['maliyet']:.1f}\n\n## Örnek çıktı karşılaştırması\n" + "\n\n".join(orn) + "\n",
                         encoding="utf-8")
    from . import ogren as og  # 21a K5: her deneme bir bilgi kartı bırakır
    (kok / "bilgi").mkdir(exist_ok=True)
    (kok / "bilgi" / f"{ns.ad}-deneme.md").write_text(og.kart_metni({"ad": ns.ad, "iddia": f"{ns.ad} denemesi: {k[:160]}",
                                                                     "url": f"docs/denemeler/{ns.ad}-sonuc.md", "guven": "orta",
                                                                     "dogrulama": f"docs/denemeler/{ns.ad}-sonuc.md", "etiketler": "dene, olcum"},
                                                                    date.today()), encoding="utf-8")
    print("\n".join(satir[2:4] + satir[8:10 + len(kollar)] + [k]))
    return 0


def uret(ns, ctx):
    """18 K2 skill fabrikası: docs/uyarlamalar/<ad>.md → taslak (oturum modeli yazar; yoksa brief, rc 3) → denetim (tavan · tetik ·
    8-gram · KAYNAK.md; hata rc 2, dene koşmaz) → docs/denemeler/<ad>.md → dene (kalite kapısı) → bekleyen + zip ya da bilgi kartı."""
    from . import ogren as og, uygula as uy  # uygula kur'u içe aktarır: döngü yalnız çağrı anında
    kok = _kok(ctx)
    led = kok / "docs" / "denemeler" / ".kos" / ns.ad / "ayristir.json"
    har = json.loads(led.read_text(encoding="utf-8")).get("harcanan", 0) if led.is_file() else 0
    if (tur := getattr(ns, "tur", None)) is not None:  # 23b K10(c) AYRIŞTIR: tur 0 ilk ölçüm, 1..2 onarım; tur ≤12, toplam ≤24 claude -p
        if tur > 2 or har >= 24:
            print(f"onarım tavanı: en fazla 2 onarım turu (tur 0..2) ve toplam claude -p ≤24 · tur {tur} · harcanan {har}; koşulmadı")
            return 2
        ns.tavan = min(ns.tavan, 12, 24 - har)
    u = kok / "docs" / "uyarlamalar" / f"{ns.ad}.md"
    if not u.is_file():
        print(f"uyarlama yok: {u}")
        return 1
    um = u.read_text(encoding="utf-8")
    a, talimat = uy.alanlar(um), None
    talimat = a.get("arac") == "talimat"  # her yanıta etki eden davranış skill değil talimattır
    tavan, km = int(a.get("token_tavani") or 200), a.get("kaynak_metin")
    rel = f"docs/uyarlamalar/{ns.ad}-talimat.md" if talimat else f"skills/{ns.ad}/SKILL.md"
    ty = kok / rel
    if not ty.is_file():
        print("\n".join([f"taslak yok: {rel} — oturum modeli yazar (writing-skills + skill-creator), sonra `video uret {ns.ad}` yeniden.",
                         f"girdi: docs/uyarlamalar/{ns.ad}.md · {a.get('aday') or 'aday yok'} ({a.get('ozellik') or '-'}) · kural kaynakları (`video kurallar`)",
                         f"kısıt: frontmatter name + description (tetik: 'Use when …' / '… kullan', ≤1024) · gövde ≤{tavan} token (bayt/4)",
                         f"kısıt: FİKİR alınır, METİN kopyalanmaz — {km or 'kaynak metin'} ile 8-gram örtüşme ≤%10"]))
        return 3
    tm = ty.read_text(encoding="utf-8")
    g, fm = govde(tm), {x[1]: x[2] for s in tm[:len(tm) - len(govde(tm))].splitlines() if (x := re.match(r"^(\w+):\s*(.*?)\s*$", s))}
    hata = [f"tavan: gövde {n} token > {tavan}"] if (n := c.token(g)) > tavan else []
    if not re.search(r"(?i)\buse when\b|kullan", fm.get("description", "")) or len(fm["description"]) > 1024:
        hata.append("description: tetik cümlesi yok ('Use when …' / '… kullan', ≤1024)")
    if km and (o := ortusme(g, (kok / km).read_text(encoding="utf-8"))) > 0.10:
        hata.append(f"örtüşme: {km} ile 8-gram %{o * 100:.0f} > %10 (fikir alınır, metin kopyalanmaz)")
    if hata:
        print("taslak hatası, dene koşmadı: " + " · ".join(hata))
        return 2
    if a.get("lisans") == "MIT":
        (ty.parent / ("KAYNAK.md" if not talimat else f"{ns.ad}-KAYNAK.md")).write_text(
            f"# Kaynak\n\nFikir: {a.get('aday') or '?'} ({a.get('ozellik') or '-'}) · MIT · metin kopyalanmadı (8-gram ≤%10, {km or '-'}) · 18 uret\n", encoding="utf-8")
    d = kok / "docs" / "denemeler"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{ns.ad}.md").write_text(
        f"# Deneme: {ns.ad}\n\n18 uret · {'talimat' if talimat else 'skill'} · gövde {n} token (tavan {tavan})\n\n## Hipotez\n{uy._ilk(um, 'Fikir') or '?'}\n\n"
        f"## Metrik\nçıktı token · toplam $ · görev başarısı (beklenen) · Jev kalite (gürültü bandı)\n\n## Bütçe\nclaude -p ≤{ns.tavan} · Jev ≤{ns.istek_tavan}\n\n"
        f"## Geri alma\n{rel} sil\n\n## Başarı eşiği\n{uy._ilk(um, 'Başarı eşiği') or 'çıktı token −%25'}\n\n## Talimat\n{rel}\n", encoding="utf-8")
    if not getattr(ns, "karar", None):  # 23b: `video karar` Ömer'in kararıyla gelir, dene yeniden koşmaz
        once = len(list(led.parent.glob("*.json")))
        rc = dene(ns, ctx)
        if getattr(ns, "tur", None) is not None:
            led.parent.mkdir(parents=True, exist_ok=True)
            led.write_text(json.dumps({"harcanan": har + len(list(led.parent.glob("*.json"))) - once}), encoding="utf-8")
        if rc:
            return rc
    k = getattr(ns, "karar", None) or tr.bolum((d / f"{ns.ad}-sonuc.md").read_text(encoding="utf-8"), "Karar").strip()
    b = kok / "docs" / "kurulumlar" / "bekleyen" / f"{ns.ad}.md"
    k = getattr(ns, "karar", None) or k
    if k.startswith("SOR"):
        print(f"SOR bekliyor: docs/kurulumlar/bekleyen/sor-{ns.ad}.md · Ömer `AL {ns.ad}` / `RED {ns.ad}` → video karar {ns.ad} AL|RED")
        return 0
    if not k.startswith("AL"):
        (kok / "bilgi").mkdir(exist_ok=True)
        (kok / "bilgi" / f"{ns.ad}.md").write_text(og.kart_metni({"ad": ns.ad, "iddia": f"{ns.ad} ({rel}) kalite kapısını geçmedi: {k[:160]}",
                                                                  "url": f"docs/denemeler/{ns.ad}-sonuc.md", "guven": "orta",
                                                                  "dogrulama": f"docs/denemeler/{ns.ad}-sonuc.md", "etiketler": "uret, olcum"}, date.today()), encoding="utf-8")
        print(f"sonuç: docs/denemeler/{ns.ad}-sonuc.md · bilgi kartı: bilgi/{ns.ad}.md")
        return 0
    b.parent.mkdir(parents=True, exist_ok=True)
    if talimat:  # ayar/CLAUDE.md değişikliği: KOŞULMAZ, Ömer PowerShell bloğunu elle koşar
        h = f"{ns.ad}.md"
        ps = ['$h = "$env:USERPROFILE\\.claude"', f'$g = (Get-Content "{kok}\\{rel.replace("/", chr(92))}" -Raw -Encoding UTF8) -replace \'(?s)\\A---.*?---\\r?\\n\', \'\'',
              f'[IO.File]::WriteAllText("$h\\{h}", $g, (New-Object Text.UTF8Encoding $false))',
              f'[IO.File]::AppendAllText("$h\\CLAUDE.md", "`r`n@{h}`r`n", (New-Object Text.UTF8Encoding $false))']
        b.write_text(f"# ONAY talimat {ns.ad}\n\n{k}\n\nAraç önerisi: global CLAUDE.md'ye `@{h}` satırı (gövde ~/.claude/{h}). "
                     f"Ayar değişikliği — koşulmadı; elle (PowerShell 5.1):\n\n```powershell\n" + "\n".join(ps) + f"\n```\n\n"
                     f"Geri alma: CLAUDE.md'den `@{h}` satırını ve ~/.claude/{h} dosyasını sil.\n", encoding="utf-8")
        print(f"ONAY bekliyor: {b.relative_to(kok).as_posix()} (PowerShell bloğu, koşulmadı)")
        return 0
    z = kok / "dist" / "yukle-18" / "yeni" / f"{ns.ad}.zip"
    z.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(ty.parent.rglob("*")):
            if p.is_file():
                zf.write(p, f"{ns.ad}/{p.relative_to(ty.parent).as_posix()}")
    b.write_text(f"# ONAY skill {ns.ad}\n\nT1 kendi skill'imiz · {k}\n\nzip: {z.relative_to(kok).as_posix()} (claude.ai yükle) · geri alma: rm -r skills/{ns.ad} {z.relative_to(kok).as_posix()}\n",
                 encoding="utf-8")
    print(f"ONAY bekliyor: {b.relative_to(kok).as_posix()} · zip: {z.relative_to(kok).as_posix()}")
    return 0


def karar_isle(ns, ctx):
    """23b: Ömer `AL <ad>` / `RED <ad>` der → bekleyen/sor-<ad>.md işlenir (dene yeniden koşmaz): AL uret'in AL kuyruğu, RED bilgi kartı; sor silinir."""
    kok = _kok(ctx)
    b = kok / "docs" / "kurulumlar" / "bekleyen" / f"sor-{ns.ad}.md"
    if not b.is_file():
        print(f"SOR bekleyen yok: {b}")
        return 1
    ns.karar = f"{ns.secim} (Ömer) · " + b.read_text(encoding="utf-8").splitlines()[2]
    ns.tavan = ns.istek_tavan = 0
    rc = uret(ns, ctx) if (kok / "docs" / "uyarlamalar" / f"{ns.ad}.md").is_file() else print(f"{ns.karar[:120]} (uret dışı deneme: yalnız kayıt)") or 0
    if rc == 0:
        _kayit(kok, ns.ad, {"karar": ns.karar, "tarih": date.today().isoformat()})
        b.unlink()
    return rc


def _geri_dusen(s, tk, x, bant):
    """Görev başına bölümünden kalite/başarısı düşen görevler: `| görev | kol | başarı 1/2 | kalite 1/2 |` tablosu ya da `- g: A n · q → B n · q` (18 biçimi)."""
    ort = lambda h: sum(map(float, h.split("/"))) / len(h.split("/"))  # noqa: E731
    t, g = tr.tablolar(tr.bolum(s, "Görev başına")), {}
    if t and "kol" in t[0][0]:
        ix = {h: i for i, h in enumerate(t[0][0])}
        for r in t[0][1]:
            g.setdefault(r[0], {})[r[ix["kol"]]] = (ort(r[ix["kalite 1/2"]]), ort(r[ix["başarı 1/2"]]) if "başarı 1/2" in ix else 0)
        return [a for a, v in g.items() if tk in v and x in v and (v[tk][0] - v[x][0] > bant or v[x][1] < v[tk][1])]
    return [m[1] for m in re.finditer(r"^- ([\w-]+): \S+ \d+ · ([\d.]+) → \S+ \d+ · ([\d.]+)", tr.bolum(s, "Görev başına (çıktı · kalite)"), re.M)
            if float(m[2]) - float(m[3]) > bant]


def takas_geri(ns, ctx):
    """23b K9 geriye dönük + K11: docs/denemeler/*-sonuc.md kol ortalamaları takas tablosuyla yeniden; tasarrufu olan → mekanizma kaydı,
    RED(kalite/takas)/SOR → ayrıştırma adayı. claude -p 0 · Jev 0; rapor docs/denemeler/takas-geri.md."""
    kok = _kok(ctx)
    d = kok / "docs" / "denemeler"
    satir, aday, degisen = [], [], 0
    for y in sorted(d.glob("*-sonuc.md")):
        ad, s = y.name[:-len("-sonuc.md")], y.read_text(encoding="utf-8")
        t = tr.tablolar(tr.bolum(s, "Kol ortalamaları"))
        if not t:
            continue
        ix = {h: i for i, h in enumerate(t[0][0])}
        v = lambda r, *h: next((float(r[ix[x]]) for x in h if x in ix), None)  # noqa: E731
        kol = {r[0]: {"cikti": v(r, "çıktı"), "girdi": v(r, "girdi"), "maliyet": v(r, "sıcak $", "maliyet $"), "kalite": v(r, "kalite 0-3"),
                      **({"basari": v(r, "başarı")} if "başarı" in ix else {})} for r in t[0][1]}
        tk = m[1] if (m := re.search(r"(\S+) \(temel\)", s)) and m[1] in kol else t[0][1][0][0]
        gur = float(m[1]) if (m := re.search(r"gürültü \([^)]*\)\s*([\d.]+)", s)) else 0.0
        dm = d / f"{ad}.md"
        e = esik(tr.bolum(dm.read_text(encoding="utf-8"), "Başarı eşiği") if dm.is_file() else "")
        kr = [x.strip() for x in tr.bolum(s, "Karar").splitlines() if x.strip()]
        for x in [k for k in kol if k != tk]:
            eski = next((z.partition(": ")[2] for z in kr if z.startswith(f"{x}: ")), kr[0] if kr else "?")
            yeni = eski if eski.startswith("KARAR YOK") else karar(kol[tk], kol[x], e, gur, [])
            sinif = lambda z: "AL" if z.startswith(("KUR", "AL")) else z.split("(")[0].split(" ")[0]  # noqa: E731
            degisti = sinif(eski) != sinif(yeni)
            degisen += degisti
            oa = ad if len(kol) == 2 else f"{ad}-{x}"
            satir.append(f"- {oa}: {eski[:70]} → {yeni[:110]}{' · DEĞİŞTİ' if degisti else ''}")
            if yeni.startswith("KARAR YOK"):
                continue
            tas, dusen = tasarruf(kol[tk], kol[x]), _geri_dusen(s, tk, x, max(gur, 0.1))
            hip = " ".join(tr.bolum(dm.read_text(encoding="utf-8"), "Hipotez").split()) if dm.is_file() else ""
            mek = mekanizma_kaydi(kok, oa, tas, dusen, hip)
            if ay := ayristir_aday(kok, oa, yeni, tas, dusen):
                aday.append(f"- {oa} · tasarruf çıktı −%{tas['cikti']:.1f} / sıcak $ −%{tas['maliyet']:.1f} · {yeni.split(' · ')[1]} · "
                            f"ayrılabilir: {'evet-aday' if dusen else 'belirsiz'} · {ay.relative_to(kok).as_posix()}" + (f" · {mek.relative_to(kok).as_posix()}" if mek else ""))
    md = [f"# Takas geriye dönük — {date.today().isoformat()}", "", f"23b K9/K11 · claude -p 0 · Jev 0 · değişen karar {degisen}", "",
          "## Kararlar (eski → yeni)", *satir, "", "## Ayrıştırma adayları (K11)", *(aday or ["- yok"]), ""]
    (d / "takas-geri.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md[2:]))
    return 0
