"""14a video-uygula: aday.md → katman (T0 kural · T1 yalnız-md skill · T2 onay · RED), uygulama, kayıt; projeler özeti."""
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path

from jev import cekirdek as c

from . import tarama as tr

KOK = Path(__file__).resolve().parents[3]
DENETIM = KOK / "tools" / "skill_denetim.py"
LISANS = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "0BSD", "ISC", "CC-BY-4.0"}
SERBEST = re.compile(r"^(LICEN[CS]E|NOTICE)(\.\w+)?$", re.I)  # lisans metni T1'e girebilir; kod değil
ALAN = re.compile(r"^(\w+):\s*(.*?)\s*$")
MADDE_NO = re.compile(r"^\s*(\d+)[.)]\s")
PROJELER = {"omer-skills": r"C:\Projeler\omer-skills", "Divisima": r"C:\Users\pc\Desktop\smart\Divisima.Solution",
            "Corvano": r"C:\Users\pc\Desktop\Corvano", "Garajım": r"C:\Users\pc\Desktop\Benim projelerim\Garajim",
            "HerYerde": r"C:\Users\pc\Desktop\heryerde_2aa"}


def alanlar(metin):
    """Başlıktan sonraki ilk `## `'e kadar `anahtar: değer` satırları."""
    out = {}
    for s in metin.splitlines()[1:]:
        if s.startswith("#"):
            break
        if x := ALAN.match(s):
            out[x[1]] = x[2]
    return out


def bakim_red(a, bugun):
    if a.get("lisans") not in LISANS:
        return f"lisans uygunsuz/yok: {a.get('lisans') or 'yok'}"
    if a.get("arsiv") == "evet":
        return "arşivlenmiş"
    try:
        son = date.fromisoformat(a.get("son_commit", ""))
    except ValueError:
        return "son commit bilinmiyor"
    if (bugun - son).days > 365:
        return f"12 aydır commit yok ({son})"
    return None


def md_disi(dosyalar):
    return [f for f in dosyalar if not (f.lower().endswith(".md") or SERBEST.match(Path(f).name))]


def sinifla(a, bugun, dosyalar=None, high=None):
    """(katman, gerekçe). Skill'de dosyalar kaynak klasöründen gerçekten listelenir, high SkillSpector'dan (None: koşmadı)."""
    if a.get("red"):
        return "RED", a["red"]
    if r := bakim_red(a, bugun):
        return "RED", r
    if a.get("tur") != "skill":
        return "T2", f"{a.get('tur') or '?'}: çalıştırılabilir, onay gerekir"
    if high is None:
        return "RED", "SkillSpector koşmadı (kaynak klonu yok ya da tarama başarısız)"
    if high:
        return "RED", f"SkillSpector HIGH/CRITICAL {high}"
    if s := md_disi(dosyalar):
        return "T2", f"md dışı dosya: {', '.join(s[:3])}"
    return "T1", "yalnız md · lisans izinli · HIGH 0"


def _kos(ctx, args, timeout=600):
    try:
        return ctx["kos"]([str(x) for x in args], timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, b"", str(e).encode()


def spector(ctx, ad, kaynak):
    out = ctx["kok"] / "skillspector" / f"{ad}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.unlink(missing_ok=True)
    _kos(ctx, ["skillspector", "scan", kaynak, "--no-llm", "--format", "json", "--output", out])
    try:  # rc'ye değil rapora bakılır: bulgu varken rc≠0 olabilir
        return sum(str(i.get("severity", "")).upper() in ("HIGH", "CRITICAL") for i in json.loads(out.read_text(encoding="utf-8")).get("issues", []))
    except (OSError, ValueError, AttributeError):
        return None


def t0(ctx, a, ad, tk):
    yollar = tr.kural_kaynaklari(ctx["env"], Path(ctx["env"].get("VIDEO_EV") or Path.home()))
    kural = a.get("kural") or ad
    if es := tr.kural_esle(tk, f"İPUCU: {ad}\n{kural}", tr.kurallar(yollar, ctx["kok"] / "kurallar.json")):
        return f"eklenmez: ÇİFT (kural: {es})", "-"
    hedef = next((y for y in yollar if y.stem == "omer-kurallar" and y.is_file()), None)  # global CLAUDE.md'ye yazılmaz
    if hedef is None:
        return "eklenmedi: omer-kurallar.md yok", "-"
    ham = hedef.read_bytes()  # yalnız sona eklenir; dosyanın satır sonu korunur (write_text Windows'ta LF'yi CRLF yapıyordu)
    nl = b"\r\n" if b"\r\n" in ham else b"\n"
    satir = ham.decode("utf-8").splitlines()
    n = max((int(x[1]) for s in satir if (x := MADDE_NO.match(s))), default=0) + 1
    hedef.write_bytes(ham + (b"" if not ham or ham.endswith(b"\n") else nl) + f"{n}. {kural} (video {a.get('video', '?')}, 14a)".encode("utf-8") + nl)
    return f"madde eklendi: {n}. {kural}", f"{hedef.name}:{len(satir) + 1} satırını sil"


def t1(ctx, kok, a, ad, kaynak):
    """skills/<ad>/ + LICENSE + KAYNAK.md → dist/yukle-14/yeni/<ad>.zip → skill_denetim. (karar, commit, geri alma) ya da None (geri alındı)."""
    rc, sha, _ = _kos(ctx, ["git", "-C", kaynak, "rev-parse", "HEAD"], 30)
    rc2, ust, _ = _kos(ctx, ["git", "-C", kaynak, "rev-parse", "--show-toplevel"], 30)
    sha = sha.decode().strip() if not rc else ""
    hedef, z = kok / "skills" / ad, kok / "dist" / "yukle-14" / "yeni" / f"{ad}.zip"
    if not re.fullmatch(r"[0-9a-f]{40}", sha) or hedef.exists():
        return None, "kaynak commit bilinmiyor" if not sha else f"skills/{ad} zaten var"
    shutil.copytree(kaynak, hedef, ignore=shutil.ignore_patterns(".git"))
    if not any(SERBEST.match(p.name) for p in hedef.iterdir()) and not rc2:
        for p in Path(ust.decode().strip()).iterdir():
            if SERBEST.match(p.name) and p.is_file():
                shutil.copy2(p, hedef / p.name)
    if not any(SERBEST.match(p.name) for p in hedef.iterdir()):
        shutil.rmtree(hedef)
        return None, "LICENSE dosyası yok"
    (hedef / "KAYNAK.md").write_text(f"# Kaynak\n\n{a.get('repo')}@{sha} · {a.get('lisans')} · video {a.get('video')} · 14a\n", encoding="utf-8")
    z.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(hedef.rglob("*")):
            if p.is_file():
                zf.write(p, f"{ad}/{p.relative_to(hedef).as_posix()}")
    if _kos(ctx, [sys.executable, DENETIM, z.parent.parent], 300)[0]:
        shutil.rmtree(hedef)
        z.unlink()
        return None, "zip denetimi hata verdi; geri alındı"
    return (f"skills/{ad} + {z.name}", sha, f"rm -r skills/{ad} dist/yukle-14/yeni/{ad}.zip"), str(z)


def katman(ns, ctx):
    env = ctx["env"]
    kok = Path(env.get("VIDEO_UYGULA_KOK") or KOK)
    kd = kok / "docs" / "kurulumlar"
    ky = kd / "kayit.jsonl"
    kayit, bugun, tk = tr.kayit_oku(ky), date.today(), None
    gorulen = {tr.normal(k["ad"]) for k in kayit}
    oto, onay, zipler, red, atla, oneri = [], [], [], [], [], []
    for yol in ns.adaylar:
        metin = Path(yol).read_text(encoding="utf-8")
        a = alanlar(metin)
        ad = a.get("ad") or Path(yol).stem
        if tr.normal(ad) in gorulen and not ns.yeniden:
            atla.append(ad)
            continue
        commit = None
        if a.get("tur") in tr.KURAL_TUR and not a.get("red"):
            if tk is None:
                n = 2 * len(ns.adaylar)
                tk = c.Tasiyici(env=env, en_fazla=n, gonder=ctx["gonder"], istek_tavan=ns.istek_tavan or n)
            kt, (karar, geri) = "T0", t0(ctx, a, ad, tk)
            oto.append(f"{ad} (T0: {karar})")
            if karar.startswith("madde"):
                oneri.append(a.get("kural") or ad)
        else:
            kaynak = Path(a["kaynak"]) if a.get("kaynak", "yok") not in ("", "yok") else None
            dosyalar = high = None
            if a.get("tur") == "skill" and kaynak and kaynak.is_dir() and not a.get("red") and not bakim_red(a, bugun):
                dosyalar = [p.relative_to(kaynak).as_posix() for p in sorted(kaynak.rglob("*")) if p.is_file() and ".git" not in p.relative_to(kaynak).parts]
                high = spector(ctx, ad, kaynak)
            kt, karar = sinifla(a, bugun, dosyalar, high)
            geri = "-"
            if kt == "T1":
                sonuc, ek = t1(ctx, kok, a, ad, kaynak)
                if sonuc:
                    karar, commit, geri = sonuc
                    zipler.append(ek)
                    oto.append(f"{ad} (T1: {karar})")
                else:
                    kt, karar = "T2", ek
            if kt == "T2":
                b = kd / "bekleyen" / f"{ad}.md"
                b.parent.mkdir(parents=True, exist_ok=True)
                b.write_text(f"# ONAY {ad}\n\nKatman T2 · {karar} · kurulmadı; onay gelirse Kurulum bloğu elle koşulur.\n\n{metin}", encoding="utf-8")
                geri = (tr.bolum(metin, "Geri alma").strip().splitlines() or ["kurulmadı"])[0]
                onay.append(f"ONAY {ad} ({karar})")
            elif kt == "RED":
                red.append(f"{ad} — {karar}")
        gorulen.add(tr.normal(ad))
        kayit = [k for k in kayit if tr.normal(k["ad"]) != tr.normal(ad)] + [
            {"ad": ad, "katman": kt, "karar": karar, "tarih": bugun.isoformat(), "video": a.get("video"), "kaynak_commit": commit, "geri_alma": geri}]
    ky.parent.mkdir(parents=True, exist_ok=True)
    tr.kayit_yaz(ky, kayit)
    for baslik, x in (("OTOMATİK UYGULANDI", oto), ("ONAY BEKLİYOR", onay), ("YÜKLENECEK ZIP", zipler), ("RED", red)):
        if x:
            print(f"{baslik}:")
            print("\n".join(f"- {s[:160]}" for s in x[:5]))
    if oneri:
        print("CLAUDE.md önerisi (elle, global dosyaya dokunulmadı): " + " · ".join(oneri)[:200])
    print((f"atlandı (kayıtta, --yeniden): {' '.join(atla)} · " if atla else "") + f"Jev istek {tk.istek if tk else 0} · kayıt: {ky}")
    return 0


def _ozet(y):
    if not y.is_file():
        return "CLAUDE.md yok"
    gov = [s.strip() for s in y.read_text(encoding="utf-8", errors="replace").splitlines()
           if s.strip() and not s.lstrip().startswith(("#", "---", "<!--", "```", "|"))]
    return " ".join(gov[:2])[:200] or "özet satırı yok"


def projeler(ns, ctx):
    env = ctx["env"]
    hedef = Path(env.get("VIDEO_UYGULA_KOK") or KOK) / "docs" / "projeler.md"
    kaynak = {ad: Path(d) / "CLAUDE.md" for ad, d in (json.loads(env["VIDEO_PROJELER"]) if env.get("VIDEO_PROJELER") else PROJELER).items()}
    if hedef.is_file() and all(not y.is_file() or y.stat().st_mtime <= hedef.stat().st_mtime for y in kaynak.values()):
        print(f"güncel: {hedef}")
        return 0
    # CLAUDE.md'de tanım satırı yoksa özet elle üretilir, `(elle)` ile biter ve yenilemede korunur
    elle = dict(re.findall(r"^- (.+?): (.+ \(elle\))$", hedef.read_text(encoding="utf-8"), re.M)) if hedef.is_file() else {}
    satir = [f"- {ad}: {elle.get(ad) or _ozet(y)}" for ad, y in kaynak.items()]
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text("# Ömer'in projeleri\n\nvideo-uygula K1 ölçütü; `video projeler` proje CLAUDE.md'lerinden üretir, mtime'la yenilenir.\n\n"
                     + "\n".join(satir) + "\n", encoding="utf-8")
    print("\n".join(satir) + f"\n{len(satir)} proje · {hedef}")
    return 0
