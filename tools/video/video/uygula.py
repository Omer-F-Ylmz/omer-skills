"""14a video-uygula: aday.md → katman (T0 kural · T1 yalnız-md skill · T2 onay · RED), uygulama, kayıt; projeler özeti.
15: K1 karar kümesi (KUR · DENE · ÖĞREN · ZATEN VAR · ALTERNATİF · RED), kural/olgu, kart, çelişki, sponsor, bizde durum."""
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path

from jev import cekirdek as c

from . import departman as dp
from . import kur
from . import ogren as og
from . import tarama as tr

KOK = Path(__file__).resolve().parents[3]
DENETIM = KOK / "tools" / "skill_denetim.py"
LISANS = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "0BSD", "ISC", "CC-BY-4.0"}
KAYNAK_ACIK = {"BSL-1.1", "BUSL-1.1", "FSL-1.1-MIT", "FSL-1.1-Apache-2.0", "Elastic-2.0"}  # kendi makinede kullanım serbest, repoya kopyalanmaz
SONUC = ("doğru", "kısmen doğru", "abartılı", "yanlış", "doğrulanamadı")  # parantezli nitelik serbest: "doğru (ikincil kaynak)"
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


def bakim_red(a, bugun, t2=False):
    """14a lisans listesi yalnız T1 (repoya kopyalama) içindir; 17 K6: T2'de kaynak-erişilebilir lisans RED değil, lisans notu."""
    if a.get("lisans") not in LISANS and not (t2 and a.get("lisans") in KAYNAK_ACIK):
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
    if r := bakim_red(a, bugun, a.get("tur") != "skill"):
        return "RED", r
    if a.get("tur") != "skill":
        return "T2", f"{a.get('tur') or '?'}: çalıştırılabilir, onay gerekir" + (
            f" · lisans notu: {a['lisans']} (kaynak-erişilebilir, kendi kullanım serbest)" if a.get("lisans") in KAYNAK_ACIK else "")
    if high is None:
        return "RED", "SkillSpector koşmadı (kaynak klonu yok ya da tarama başarısız)"
    if high:
        return "RED", f"SkillSpector HIGH/CRITICAL {high}"
    if s := md_disi(dosyalar):
        return "T2", f"md dışı dosya: {', '.join(s[:3])}"
    return "T1", "yalnız md · lisans izinli · HIGH 0"


def ozellikler(metin):
    """17 K3: `## Özellikler` → [{ozellik, alan: değer…}]; her `### <slug>` bir özellik."""
    out = []
    for p in re.split(r"^### ", tr.bolum(metin, "Özellikler"), flags=re.M)[1:]:
        s = p.splitlines()
        out.append({"ozellik": s[0].strip(), **{x[1]: x[2] for y in s[1:] if (x := ALAN.match(y))}})
    return out



def mekanizma_denetle(metin):
    """20b-devam K6: token etiketli her özelliğin `## Mekanizma` altında `### <slug>`'ı ve nasıl · neden · koşul · bizde alanları dolu."""
    mek = {p.splitlines()[0].strip(): p for p in re.split(r"^### ", tr.bolum(metin, "Mekanizma"), flags=re.M)[1:]}
    h = []
    for o in ozellikler(metin):
        if not re.search("token|teknik", o.get("etiket", "").casefold()):
            continue
        if o["ozellik"] not in mek:
            h.append(f"{o['ozellik']}: ## Mekanizma yok")
            continue
        h += [f"{o['ozellik']}: Mekanizma {x} eksik" for x in ("nasıl", "neden", "koşul", "bizde")
              if not re.search(rf"^{x}:\s*\S", mek[o["ozellik"]], re.M)]
    return h

ANATOMI = ("bolumler", "hareket", "teknoloji", "dosya", "config", "asset", "kabul")
SABLON = "Yapım promptu şablonu"
KUTUPHANE = "| kalıp | video | zaman | teknik | şablonda karşılığı | aday |"


def prompt_mu(metin):
    """23c K7: `tur: prompt` aday ya da `etiket: prompt` taşıyan özellik → anatomi zorunlu."""
    return alanlar(metin).get("tur") == "prompt" or any("prompt" in o.get("etiket", "").casefold() for o in ozellikler(metin))


def kaliplar(metin, video):
    """`### Kalıplar` satırları: `- <kalıp> · <m:ss> · teknik: <x> · şablon: <bölüm|yok>`."""
    b = tr.bolum(metin, "Prompt anatomisi")
    out = []
    for s in (b.split("### Kalıplar", 1)[1] if "### Kalıplar" in b else "").splitlines():
        if s.startswith("- "):
            p = [x.strip() for x in s[2:].split(" · ")]
            al = {k.strip(): v.strip() for k, _, v in (x.partition(":") for x in p[2:])}
            out.append({"kalip": p[0], "zaman": p[1] if len(p) > 1 else "", "video": video or "", "teknik": al.get("teknik", ""), "sablon": al.get("şablon", "")})
    return out


def anatomi_denetle(metin):
    """23c K7: prompt adayında `## Prompt anatomisi` alanları dolu, ≥1 kalıp; kalıp ≤15 kelime (metin kopyalanmaz) + m:ss + şablon."""
    if not prompt_mu(metin):
        return []
    b = tr.bolum(metin, "Prompt anatomisi")
    if not b.strip():
        return ["## Prompt anatomisi yok (tur/etiket: prompt)"]
    h = [f"Prompt anatomisi {x}: eksik" for x in ANATOMI if not re.search(rf"^{x}:\s*\S", b, re.M)]
    k = kaliplar(metin, alanlar(metin).get("video"))
    h += [] if k else ["Prompt anatomisi ### Kalıplar: kalıp yok"]
    for x in k:
        if len(x["kalip"].split()) > 15:
            h.append(f"kalıp >15 kelime (kopya değil kalıp): {x['kalip'][:40]}")
        if not tr.ZAMAN.search(x["zaman"]) or not x["sablon"]:
            h.append(f"kalıp zaman/şablon eksik: {x['kalip'][:40]}")
    return h


def kutuphane_ekle(kok, satirlar):
    """23c K7: docs/departmanlar/frontend-promptlar.md — kaynak video ve zaman zorunlu; aynı kalıp ikinci kez eklenmez."""
    for x in satirlar:
        if not x.get("video") or not x.get("zaman"):
            raise ValueError(f"kütüphane satırı video ve zaman ister: {x.get('kalip')}")
    y = kok / "docs" / "departmanlar" / "frontend-promptlar.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    eski = y.read_text(encoding="utf-8") if y.is_file() else (
        "# Site prompt kütüphanesi (frontend)\n\nVideodan çıkan yapım promptu kalıpları; metin kopyalanmaz, kalıp yazılır. "
        "Kaynak: `video katman` (tur/etiket: prompt aday).\n\n" + KUTUPHANE + "\n|---|---|---|---|---|---|\n")
    var = {tr.normal(s.split("|")[1]) for s in eski.splitlines() if s.startswith("| ") and s != KUTUPHANE}
    ek = [x for x in satirlar if tr.normal(x["kalip"]) not in var]
    y.write_text(eski + "".join(f"| {x['kalip']} | {x['video']} | {x['zaman']} | {x.get('teknik') or '-'} | {x.get('karsilik') or '-'} | {x.get('aday') or '-'} |\n"
                                for x in ek), encoding="utf-8")
    return len(ek)


def prompt_isle(kok, ad, metin):
    """23c K7: kalıbın şablon bölümü departman-frontend `## Yapım promptu şablonu` `- <bölüm>:` satırlarında varsa ZATEN VAR,
    yoksa UYARLA bekleyen/prompt-<slug>.md (şablona ekleme önerisi, onaysız eklenmez). Jev 0."""
    s = kok / "skills" / "departman-frontend" / "SKILL.md"
    bolum = {m[1].casefold() for m in re.finditer(r"^- (\w+):", tr.bolum(s.read_text(encoding="utf-8"), SABLON) if s.is_file() else "", re.M)}
    say, satir = {"ZATEN VAR": 0, "UYARLA": 0}, []
    for x in kaliplar(metin, alanlar(metin).get("video")):
        if x["sablon"].casefold() in bolum:
            karar, x["karsilik"] = "ZATEN VAR", f"şablon: {x['sablon']}"
        else:
            karar, x["karsilik"] = "UYARLA", "yok → bekleyen"
            slug = re.sub(r"[^a-z0-9]+", "-", x["kalip"].translate(SLUG).casefold()).strip("-")[:60].strip("-")
            b = kok / "docs" / "kurulumlar" / "bekleyen" / f"prompt-{slug}.md"
            b.parent.mkdir(parents=True, exist_ok=True)
            b.write_text(f"# UYARLA prompt kalıbı: {x['kalip']}\nkaynak: video {x['video']} · {x['zaman']} · aday {ad}\nteknik: {x['teknik'] or '-'}\n"
                         f"hedef: skills/departman-frontend `## {SABLON}` (öneri; onaysız eklenmez)\n\nOnay: Ömer · ret: dosyayı sil.\n", encoding="utf-8")
        say[karar] += 1
        satir.append({**x, "aday": ad})
    kutuphane_ekle(kok, satir)
    return say


def kanit(o, a, metin, kok, env):
    """17 K4: RED gerekçesi kanıta bağlı mı. ölçüm: var olan docs/denemeler/*-sonuc.md · zaten var: katalog/durum.md adı ya da
    var olan dosya · lisans: aday lisansı izinli/kaynak-erişilebilir değil · güvenlik: aday dosyasında SkillSpector HIGH/CRITICAL."""
    on, _, g = o.get("gerekce", "").partition(":")
    on = on.strip().casefold()
    if on == "ölçüm":
        return any((kok / y).is_file() for y in re.findall(r"docs/denemeler/[\w.-]+-sonuc\.md", g))
    if on == "zaten var":
        adlar = {tr.normal(x) for x, _ in tr.sozluk_kur(Path(env.get("VIDEO_EV") or Path.home()), [])} | {tr.normal(x) for x, _ in og.ARACLAR}
        if (d := kok / "docs" / "durum.md").is_file():
            adlar |= {tr.normal(x) for x in re.findall(r"^- ([^\s:→]+)\s*(?:→|:)", d.read_text(encoding="utf-8"), re.M)}
        return any(tr.normal(w) in adlar or (kok / w).is_file() for w in re.findall(r"[\w.@/-]+", g) if tr.normal(w))
    if on == "lisans":
        li = o.get("lisans") or a.get("lisans") or ""
        return bool(li) and li in g and li not in LISANS | KAYNAK_ACIK
    if on == "güvenlik":  # bulgu özellik satırında değil aday dosyasının kendisinde olmalı
        return bool(re.search(r"SkillSpector[^\n]*(HIGH|CRITICAL)", metin.replace(tr.bolum(metin, "Özellikler"), "")))
    return False


def ozellik_karar(o, a, metin, kok, env):
    """(karar, gerekçe). 17 K4: karar yoksa DENE; token etiketli özellikte kanıtsız RED → DENE."""
    k, g = o.get("karar") if o.get("karar") in og.KARAR else "DENE", o.get("gerekce", "")
    if k == "RED" and "token" in o.get("etiket", "").casefold() and not kanit(o, a, metin, kok, env):
        return "DENE", f"K4: kanıt bulunamadı — RED({g or 'gerekçesiz'}) → DENE"
    return k, g


def uyarla_yaz(kok, o, ad):
    """17 K3: fikir kendi araçlarımıza uygulanır; yalnız doküman, kod yazılmaz (Desktop tarif verir)."""
    y = Path(kok) / "docs" / "uyarlamalar" / f"{ad}.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(f"# Uyarlama: {ad}\n\n17 K3 · kod yazılmaz; Desktop tarif verir\n\n" + "".join(
        f"## {b}\n{o.get(k) or '?'}\n\n" for b, k in (("Fikir", "fikir"), ("Hedef araç/dosya", "hedef"), ("Beklenen etki", "etki"), ("Kapsam", "kapsam"))),
        encoding="utf-8")
    return f"uyarlama: docs/uyarlamalar/{ad}.md"


def iddia_sinama(metin):
    """17 K5: `## İddia sınama` (iddia · kaynak · sonuç · not · kart) → (satırlar, hatalar); kaynaksız ya da geçersiz sonuç → doğrulanamadı."""
    t, out, h = tr.tablolar(tr.bolum(metin, "İddia sınama")), [], []
    for s in t[0][1] if t else []:
        x = dict(zip(("iddia", "kaynak", "sonuc", "not", "kart"), (s + [""] * 5)[:5]))
        if x["sonuc"].split(" (")[0] not in SONUC:
            h.append(f"sonuç geçersiz: {x['iddia']} → {x['sonuc']} ({'/'.join(SONUC)})")
            x["sonuc"] = "doğrulanamadı"
        elif x["kaynak"] in ("", "-") and x["sonuc"] != "doğrulanamadı":
            h.append(f"kaynaksız sonuç: {x['iddia']} → doğrulanamadı")
            x["sonuc"] = "doğrulanamadı"
        out.append(x)
    return out, h


def sina(kok, ad, metin, sinama, eksik):
    """K5 iddia sınaması her adayda: satırlar rapora, abartılı/yanlış + kart → karta not."""
    ss, sh = iddia_sinama(metin)
    eksik += [f"{ad}: {x}" for x in sh]
    for s in ss:
        sinama.append(s)
        if s["sonuc"].split(" (")[0] in ("abartılı", "yanlış") and s["kart"] not in ("", "-") and (y := kok / "bilgi" / f"{s['kart']}.md").is_file():
            y.write_text(y.read_text(encoding="utf-8").rstrip("\n") + f"\n- not: '{s['iddia']}' {s['sonuc']} ({s['kaynak']})\n", encoding="utf-8")


def brief(ns, ctx):
    """17 K7: Desktop ikinci görüş girdisi, ≤60 satır: özellik kararları · iddialar · linkler."""
    metin = Path(ns.rapor).read_text(encoding="utf-8")
    t = tr.tablolar(tr.bolum(metin, "İDDİA SINAMA"))
    idd = [f"- {s[0]} → {s[2]} ({s[1]})" for s in (t[0][1] if t else []) if len(s) >= 3]
    oz = [s for s in tr.bolum(metin, "ÖZELLİK KARARLARI").splitlines() if s.startswith("- ")]
    link = list(dict.fromkeys(re.findall(r"https?://[^\s|)]+", metin)))
    dep = [s for s in tr.bolum(metin, "DEPARTMAN").splitlines() if s.startswith("- ")]
    print("\n".join([f"# brief: {Path(ns.rapor).name}", "## Özellik kararları", *oz[:25], "## Departman", *dep[:10],
                     "## İddialar", *idd[:20],
                     "## Linkler", *[f"- {x}" for x in link[:9]]]))
    return 0


def _departman(kok, jev, ad, a, metin, depl, envantere=True):
    """19 K5: yeni araç → departman (KUR/UYARLA envanter + katalog); 23 K2: karar ne olursa olsun departman; rapor DEPARTMAN bölümü."""
    dep, p = (dp.dosyala if envantere else dp.sinifla)(kok, jev, ad, a.get("tur") or "skill", " ".join(tr.bolum(metin, "Ne").split())[:dp.ACIKLAMA])
    depl.append(f"{ad} → {dep} ({p:.2f})")
    return dep


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


def _kurallar(ctx):
    yollar = tr.kural_kaynaklari(ctx["env"], Path(ctx["env"].get("VIDEO_EV") or Path.home()))
    return yollar, tr.kurallar(yollar, ctx["kok"] / "kurallar.json")


def t0(ctx, a, ad, tk, kok, metin):
    """15b K1: kural önerisi kural dosyasına yazılmaz → bekleyen/kural-<slug>.md + ONAY; ekleme yalnız `video kural-onay`."""
    kl = _kurallar(ctx)[1]
    kural = a.get("kural") or ad
    if es := tr.kural_esle(tk, f"İPUCU: {ad}\n{kural}", kl):
        return f"eklenmez: ÇİFT (kural: {es})", "-"
    r = og.celiski(tk, f"İPUCU: {ad}\n{kural}", kl, og.kartlar(kok))  # 15 K5: çelişki Ömer'e gider, otomatik çözülmez
    if r and r[1] == "destekler" and not r[0].startswith("bilgi:"):  # kuralı destekleyen öneri: zaten var
        return f"eklenmez: ÇİFT (kural: {r[0]}, destekler)", "-"
    cel = r[0] if r and r[1] == "çelişir" else None
    slug = re.sub(r"\W+", "-", ad.casefold()).strip("-") or "kural"
    b = kok / "docs" / "kurulumlar" / "bekleyen" / f"kural-{slug}.md"
    b.parent.mkdir(parents=True, exist_ok=True)
    b.write_text(f"# ONAY kural {slug}\nad: {ad}\nmadde: {kural}\nkaynak: video {a.get('video', '?')}, 15b\n"
                 f"gerekce: {a.get('gerekce') or _ilk(metin, 'Beklenen fayda') or '-'}\nçift/çelişki: {f'ÇELİŞKİ ({cel})' if cel else 'yok'}\n\n"
                 f"Onay: `video kural-onay {slug}` · ret: dosyayı sil.\n\n{metin}", encoding="utf-8")
    return f"ONAY kural {slug}" + (f" · ÇELİŞKİ ({cel})" if cel else ""), f"rm {b.relative_to(kok).as_posix()}"


def kural_ekle(yollar, madde, kaynak):
    """omer-kurallar.md'ye yazan TEK fonksiyon: yalnız sona eklenir, satır sonu korunur, aynı madde varsa eklenmez."""
    hedef = next((y for y in yollar if y.stem == "omer-kurallar" and y.is_file()), None)  # global CLAUDE.md'ye yazılmaz
    if hedef is None:
        return "eklenmedi: omer-kurallar.md yok", "-"
    ham = hedef.read_bytes()  # write_text Windows'ta LF'yi CRLF yapıyordu
    nl = b"\r\n" if b"\r\n" in ham else b"\n"
    satir = ham.decode("utf-8").splitlines()
    if x := next((i for i, s in enumerate(satir, 1) if tr.normal(madde) in tr.normal(s)), None):
        return f"eklenmez: ÇİFT (omer-kurallar:{x})", "-"
    n = max((int(x[1]) for s in satir if (x := MADDE_NO.match(s))), default=0) + 1
    hedef.write_bytes(ham + (b"" if not ham or ham.endswith(b"\n") else nl) + f"{n}. {madde} ({kaynak})".encode("utf-8") + nl)
    return f"madde eklendi: {n}. {madde}", f"{hedef.name}:{len(satir) + 1} satırını sil"


def kural_onay(ns, ctx):
    env = ctx["env"]
    kok = Path(env.get("VIDEO_UYGULA_KOK") or KOK)
    b = kok / "docs" / "kurulumlar" / "bekleyen" / f"kural-{ns.slug}.md"
    if not b.is_file():
        print(f"bekleyen yok: {b}")
        return 1
    a = alanlar(b.read_text(encoding="utf-8"))
    madde = f"{ns.kapsam.strip().rstrip(':')}: {a['madde']}"  # 23c K6: kapsamsız onay yok
    karar, geri = kural_ekle(tr.kural_kaynaklari(env, Path(env.get("VIDEO_EV") or Path.home())), madde, a["kaynak"])
    print(f"{karar} · geri alma: {geri}")
    if karar.startswith("madde"):
        b.unlink()
        ky = kok / "docs" / "kurulumlar" / "kayit.jsonl"
        if eski := tr.kayit_son(tr.kayit_oku(ky)).get(a.get("ad")):
            tr.kayit_ekle(ky, [{**eski, "karar": karar, "geri_alma": geri, "kapsam": ns.kapsam}])
    return 0


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


ALTI = ("Ne", "Bizde durum", "Beklenen fayda", "Maliyet/risk", "Karar", "Sonraki adım")


CAGRI_USD = 0.30  # ponytail: sabit, geçmiş denemelerin sıcak koşu ortalaması (~$0.28-0.41); ölçüm biriktikçe güncelle


def _ilk(metin, b):
    return next((s.strip() for s in tr.bolum(metin, b).splitlines() if s.strip()), "")


def katman(ns, ctx):
    env = ctx["env"]
    kok = Path(env.get("VIDEO_UYGULA_KOK") or KOK)
    kd = kok / "docs" / "kurulumlar"
    ky = kd / "kayit.jsonl"
    kayit, bugun, tk = tr.kayit_oku(ky), date.today(), None
    gorulen = {tr.normal(k.get("aday") or k["ad"]) for k in kayit}
    oto, onay, zipler, red, atla, ogrenilen, celiski, dene, ozet, rapor, eksik, ozk, sinama, depl, uret_ = ([] for _ in range(15))
    n = 8 * len(ns.adaylar)  # aday başına tür 1 + çift 2 + çelişki 2 (+ sponsor 1) + departman 1

    def jev():
        nonlocal tk
        if tk is None:
            tk = c.Tasiyici(env=env, en_fazla=n, gonder=ctx["gonder"], istek_tavan=ns.istek_tavan or n)
        return tk
    videodan, eklenen = {}, []
    for yol in ns.adaylar:
        metin = Path(yol).read_text(encoding="utf-8")
        a = alanlar(metin)
        ad = a.get("ad") or Path(yol).stem
        if tr.normal(ad) in gorulen and not ns.yeniden:
            atla.append(ad)
            continue
        me = og.meta(ctx, a.get("video"))
        kanal, sponsor = a.get("kanal") or me.get("channel"), og.sponsor_mu(ctx, me, a, jev)
        if prompt_mu(metin):  # 23c K7: prompt anatomisi → site prompt kütüphanesi (Jev 0)
            ps = prompt_isle(kok, ad, metin)
            ogrenilen.append(f"{ad}: prompt anatomisi → docs/departmanlar/frontend-promptlar.md · " + " · ".join(f"{k} {v}" for k, v in ps.items()))
        if oz := ozellikler(metin):  # 17 K3: özellik düzeyi; aday bütün olarak tartılmaz
            yeni, satir = [], []
            for o in oz:
                yk, g = ozellik_karar(o, a, metin, kok, env)
                oa, o = f"{ad}-{o['ozellik']}", {**({"video": a["video"]} if a.get("video") else {}), **o}
                if yk == "UYARLA":
                    karar = uyarla_yaz(kok, o, oa)
                    h = o.get("hedef", "")
                    if (o.get("hedef_tur") or ("skill" if re.search(r"(?i)skill", h) else "talimat" if re.search(r"(?i)talimat|CLAUDE\.md", h) else "")) in ("skill", "talimat"):
                        uret_.append(f"{oa} · kaynak {ad}/{o['ozellik']} · fayda: {o.get('etki') or '?'} · maliyet: claude -p ≤24 · ≈${24 * CAGRI_USD:.2f} · `ÜRET {oa}`")
                elif yk == "DENE":
                    if "token" in o.get("etiket", "").casefold() and "token" not in (o.get("metrik") or "").casefold():
                        o["metrik"] = "girdi/çıktı token (K4 zorunlu) · " + (o.get("metrik") or "?")
                    karar = og.deneme_yaz(kok, o, oa, "")
                    dene.append(f"{ad}/{o['ozellik']}: {karar}")
                elif yk == "ÖĞREN":
                    karar, cel = og.ogren(jev(), kok, o, oa, bugun, _kurallar(ctx)[1])
                    (celiski if cel else ogrenilen).append(f"{ad}/{o['ozellik']}: {karar}")
                else:
                    karar = g or yk
                    if yk == "RED":
                        red.append(f"{ad}/{o['ozellik']} — {karar}")
                    elif yk == "KUR":
                        onay.append(f"{ad}/{o['ozellik']} KUR: aday düzeyi bekleyen/<ad>.md ile `video onay`")
                ozk.append(f"{ad}/{o['ozellik']} → {yk} — {g or karar}")
                satir.append(f"- {o['ozellik']} → {yk}: {karar}")
                yeni.append({"ad": f"{ad}/{o['ozellik']}", "aday": ad, "ozellik": o["ozellik"], "yargi": yk, "karar": karar, "gerekce": g,
                             "tarih": bugun.isoformat(), "video": a.get("video"), "kanal": kanal, "sponsor": sponsor})
            sina(kok, ad, metin, sinama, eksik)  # özelliklerden sonra: aynı koşuda yazılan ÖĞREN kartı da not alabilsin
            dep = _departman(kok, jev, ad, a, metin, depl, any(k["yargi"] in ("KUR", "UYARLA") for k in yeni))
            yeni = [{**k, "departman": dep} for k in yeni]
            videodan.setdefault((dep, "Videodan gelen"), []).extend(f"- {k['ad']} · {k['yargi']} · video {k.get('video') or '?'}" for k in yeni)
            ozet.append((sponsor, f"{ad} → özellik düzeyi: " + " · ".join(f"{o['ozellik']} {k['yargi']}" for o, k in zip(oz, yeni))))
            rapor.append((sponsor, [f"## {ad} → özellik düzeyi{' · sponsor' if sponsor else ''}", *satir, ""]))
            gorulen.add(tr.normal(ad))
            eklenen += yeni  # 23c: append-only; okuma kayit_son ile
            continue
        yargi = a.get("karar") if a.get("karar") in og.KARAR else "KUR"  # karar alanı yoksa 14a yolu
        if a.get("karar") and yargi != "RED" and (x := [b for b in ALTI if not tr.bolum(metin, b).strip()]):
            eksik.append(f"{ad}: {', '.join(x)}")
        commit, kt, karar, geri = None, "-", "", "-"
        if yargi == "KUR" and a.get("tur") in tr.KURAL_TUR and not a.get("red"):
            if og.olgu_mu(jev(), ad, a):  # 15 K3: olgu kural dosyasına girmez
                yargi = "ÖĞREN"
            else:
                kt, (karar, geri) = "T0", t0(ctx, a, ad, jev(), kok, metin)
                if "ÇİFT" in karar:
                    yargi = "ZATEN VAR"
                else:
                    onay.append(karar.split(" · ")[0])
                    if "ÇELİŞKİ" in karar:
                        celiski.append(f"{ad} ↔ {karar.split('ÇELİŞKİ (', 1)[1][:-1]}: {a.get('kural') or ad}")
        if yargi == "ÖĞREN":
            karar, cel = og.ogren(jev(), kok, a, ad, bugun, _kurallar(ctx)[1])
            if cel:
                celiski.append(f"{ad} ↔ {cel}: {a.get('iddia') or a.get('kural') or ad}")
            else:
                ogrenilen.append(f"{ad}: {karar}")
        elif yargi == "DENE":
            karar = og.deneme_yaz(kok, a, ad, metin)
            dene.append(f"{ad}: {karar}")
        elif yargi == "UYARLA":
            karar = uyarla_yaz(kok, a, ad)
        elif yargi in ("ZATEN VAR", "ALTERNATİF", "RED") and kt == "-":
            karar = a.get("gerekce") or _ilk(metin, "Karar") or yargi
            if yargi == "RED":
                red.append(f"{ad} — {karar}")
        elif yargi == "KUR" and kt == "-":
            kaynak = Path(a["kaynak"]) if a.get("kaynak", "yok") not in ("", "yok") else None
            dosyalar = high = None
            if a.get("tur") == "skill" and kaynak and kaynak.is_dir() and not a.get("red") and not bakim_red(a, bugun):
                dosyalar = [p.relative_to(kaynak).as_posix() for p in sorted(kaynak.rglob("*")) if p.is_file() and ".git" not in p.relative_to(kaynak).parts]
                high = spector(ctx, ad, kaynak)
            kt, karar = sinifla(a, bugun, dosyalar, high)
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
                bh = kur.bicim(metin, kur.kopru_oku(kok))[1]  # 14b: yapılandırılmış biçim yoksa onay koşamaz
                b.write_text((f"BİÇİM EKSİK: {' · '.join(bh)}\n\n" if bh else "")
                             + f"# ONAY {ad}\n\nKatman T2 · {karar} · kurulmadı; `video onay {ad} [--kuru]`.\n\n{metin}", encoding="utf-8")
                geri = (tr.bolum(metin, "Geri alma").strip().splitlines() or ["kurulmadı"])[0]
                onay.append(f"elle düzelt {ad} ({karar}; biçim eksik)" if bh else f"ONAY {ad} ({karar})")
            elif kt == "RED":
                yargi = "RED"
                red.append(f"{ad} — {karar}")
        dep = _departman(kok, jev, ad, a, metin, depl, yargi in ("KUR", "UYARLA") and kt != "T0")
        videodan.setdefault((dep, "Videodan gelen"), []).append(f"- {ad} · {yargi} · video {a.get('video') or '?'}")
        ozet.append((sponsor, f"{ad} → {yargi}{' (sponsor)' if sponsor else ''} — {karar}"))
        rapor.append((sponsor, [f"## {ad} → {yargi}{' · sponsor' if sponsor else ''}", f"- Sonuç: {karar}"]
                      + [f"- {b}: {' '.join(tr.bolum(metin, b).split())[:400] or ('-' if yargi == 'RED' else '(eksik)')}" for b in ALTI] + [""]))
        sina(kok, ad, metin, sinama, eksik)
        gorulen.add(tr.normal(ad))
        eklenen.append(
            {"ad": ad, "katman": kt, "yargi": yargi, "karar": karar, "tarih": bugun.isoformat(), "video": a.get("video"), "kanal": kanal,
             "sponsor": sponsor, "kaynak_commit": commit, "geri_alma": geri, **({"departman": dep} if dep else {})})
    tr.kayit_ekle(ky, eklenen)
    dp.katalog_ekle(kok, videodan)
    bayat = [f"{s} ({fm.get('bayatlama')})" for s, fm, _ in og.kartlar(kok) if fm.get("bayatlama", "") < bugun.isoformat()]
    bolumler = (("ÖZELLİK KARARLARI", ozk), ("ÖĞRENİLENLER", ogrenilen), ("ÇELİŞKİLER (otomatik eklenmedi, Ömer karar verir)", celiski), ("DENENECEKLER", dene),
                ("ÜRETİLEBİLİR", uret_), ("OTOMATİK UYGULANDI", oto), ("ONAY BEKLİYOR", onay), ("YÜKLENECEK ZIP", zipler), ("RED", red), ("DEPARTMAN", depl), ("YENİDEN DOĞRULA (bayat kart)", bayat))
    tam = kd / f"{bugun.isoformat()}-uygula.md"
    if rapor:  # sponsor adayları düşük öncelik: sona
        tam.write_text("\n".join([f"# video-uygula — {bugun.isoformat()}", ""] + [s for _, r in sorted(rapor, key=lambda x: x[0]) for s in r]
                                 + [s for b, x in bolumler if x for s in [f"## {b}"] + [f"- {y}" for y in x] + [""]]
                     + (["## İDDİA SINAMA", "| iddia | kaynak | sonuç | not |", "|---|---|---|---|"]
                        + [f"| {s['iddia']} | {s['kaynak']} | {s['sonuc']} | {s['not']} |" for s in sinama] + [""] if sinama else [])
                     + ["## Desktop ikinci görüş", ""]), encoding="utf-8")
    for _, s in sorted(ozet, key=lambda x: x[0]):
        print(f"- {s[:150]}")
    for baslik, x in bolumler:
        if x:
            print(f"{baslik}: " + " · ".join(s[:100] for s in x[:4]))
    if eksik:
        print("eksik alan: " + " · ".join(eksik)[:200])
    print((f"atlandı (kayıtta, --yeniden): {' '.join(atla)} · " if atla else "") + f"Jev istek {tk.istek if tk else 0} · kayıt: {ky}"
          + (f" · rapor: {tam}" if rapor else ""))
    return 0


def kurulum(ad, cl, katalog):
    """15b K3: ad düzeyinde doğrulanmış durum. Katalog (aktif skill) → açık; yoksa settings enabledPlugins/skillOverrides,
    ama yalnız dosyası gerçekten kuruluysa (installed_plugins.json · SKILL.md) kurulu sayılır."""
    n = tr.normal(ad)
    if k := next((k for k, _ in katalog if tr.normal(k.split(":")[-1]) == n), None):
        return f"kurulu-açık (katalog {k})"
    ayar = _json(cl / "settings.json")
    kurulu = _json(cl / "plugins" / "installed_plugins.json").get("plugins") or {}
    for k, v in (ayar.get("enabledPlugins") or {}).items():
        if tr.normal(k.partition("@")[0]) == n and k in kurulu:
            return f"kurulu-{'açık' if v is True else 'kapalı'} (settings enabledPlugins {k}={json.dumps(v)})"
    for k, v in (ayar.get("skillOverrides") or {}).items():
        d = k.split(":")[-1]
        if tr.normal(d) == n and v == "off" and any(g.parent.name == d for y in ("skills/*/SKILL.md", "skills/synced/*/*/SKILL.md",
                                                                                   "plugins/cache/*/*/*/skills/*/SKILL.md") for g in cl.glob(y)):
            return f"kurulu-kapalı (settings skillOverrides {k}=off)"
    return "yok (katalog ve settings'te yok)"


def _json(y):
    try:
        return json.loads(y.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _bizde_satir(metin, satir, desen):
    if re.search(desen, metin, re.M):
        return re.sub(desen, lambda _: satir, metin, count=1, flags=re.M)
    if re.search(r"^## Bizde durum", metin, re.M):
        return re.sub(r"^## Bizde durum.*$", lambda x: x[0] + "\n" + satir, metin, count=1, flags=re.M)
    return metin.rstrip("\n") + "\n## Bizde durum\n" + satir + "\n"


def bizde(ns, ctx):
    """K2 Bizde durum: adayın ne işe yaradığı → jev skill (2 istek); yalnız p≥act skill'ler aday.md'ye adıyla yazılır.
    15b K3: adayın kendi adı için kurulum satırı (katalog → settings)."""
    from jev import skill as sk
    env, n = ctx["env"], 2 * len(ns.adaylar)
    t = c.Tasiyici(env=env, en_fazla=n, gonder=ctx["gonder"], istek_tavan=ns.istek_tavan or n)
    t.tekrar = 0
    ev = Path(env.get("VIDEO_EV") or Path.home())
    b, liste = c.bantlar_oku(), sk.adaylar(ev)
    for yol in ns.adaylar:
        metin = Path(yol).read_text(encoding="utf-8")
        a = alanlar(metin)
        ne = a.get("ne") or _ilk(metin, "Ne") or a.get("ad") or Path(yol).stem
        _, sonuc = sk.yonlendir(ne, t, b, liste)
        satir = "- jev skill (Act): " + (", ".join(f"{x['ad']} {x['p']:.2f}" for x in sonuc) or "yok")
        kur = f"- kurulum: {kurulum(a.get('ad') or Path(yol).stem, ev / '.claude', liste)}"
        metin = _bizde_satir(_bizde_satir(metin, satir, r"^- jev skill \(Act\):.*$"), kur, r"^- kurulum:.*$")
        Path(yol).write_text(metin, encoding="utf-8")
        print(f"{Path(yol).stem}: {satir[2:]} · {kur[2:]}")
    print(f"Jev istek {t.istek}")
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


# --- 23 video-mükemmel ---

AJAN_TIP = re.compile(r"subagent_type:\s*`?([\w:-]+)")
SLUG = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def ajan_denetle(ns, ctx):
    """K1: video/departman SKILL.md'leri ve ajan tanımlarında geçen her subagent_type → .claude/agents/<ad>.md · model sonnet · tools dar (≤4, * yok)."""
    kok = Path(ctx["env"].get("VIDEO_UYGULA_KOK") or KOK)
    ad, tipler = kok / ".claude" / "agents", {}
    for y in [*kok.glob("skills/video-*/SKILL.md"), *kok.glob("skills/departman-*/SKILL.md"), *ad.glob("*.md")]:
        for t in AJAN_TIP.findall(y.read_text(encoding="utf-8")):
            tipler.setdefault(t, y.relative_to(kok).as_posix())
    h = []
    for t, kaynak in sorted(tipler.items()):
        if not (y := ad / f"{t}.md").is_file():
            h.append(f"{t}: tanım yok (.claude/agents/{t}.md · {kaynak}) — general-purpose'a düşülür")
            continue
        m = y.read_text(encoding="utf-8")
        model, tools = (re.search(rf"^{k}:\s*(.*?)\s*$", m, re.M) for k in ("model", "tools"))
        if not model or model[1] != "sonnet":
            h.append(f"{t}: model {model[1] if model else 'yok'} (sonnet olmalı)")
        ts = [x.strip() for x in (tools[1] if tools else "").split(",") if x.strip()]
        if not ts or "*" in ts or len(ts) > 4:
            h.append(f"{t}: tools {tools[1] if tools else 'yok'} (dar: ≤4, * yok)")
    for x in h:
        print(x)
    print(f"ajan-denetle: {len(tipler)} tip ({', '.join(sorted(tipler))}) · {'GEÇTİ' if not h else f'{len(h)} hata'}")
    return 1 if h else 0


def departman_geri(ns, ctx):
    """K2: kayit.jsonl'de departmanı olmayan karar kayıtları → aday başına bir sınıflama → kayıt + katalog 'Videodan gelen'."""
    env = ctx["env"]
    kok = Path(env.get("VIDEO_UYGULA_KOK") or KOK)
    ky, tk, dep, ek, n = kok / "docs" / "kurulumlar" / "kayit.jsonl", [], {}, {}, 0

    def jev():
        if not tk:
            tk.append(c.Tasiyici(env=env, en_fazla=ns.istek_tavan, gonder=ctx["gonder"], istek_tavan=ns.istek_tavan))
        return tk[0]
    kayit, yeni, bugun = tr.kayit_oku(ky), [], date.today().isoformat()
    son = tr.kayit_son(kayit)
    adaylar = sorted({k.get("aday") or k["ad"] for k in son.values() if k.get("departman")}, key=len, reverse=True)
    for i, k in enumerate(kayit):
        if son[k["ad"]].get("departman"):
            continue
        if "yargi" not in k:  # 23c K5: dene/onay işlem kaydı → ilgili adayın departmanı ya da uygulanamaz; eski satır değişmez
            a = next((x for x in adaylar if k["ad"] == x or k["ad"].startswith((f"{x}-", f"{x}/"))), None)
            d = next(v["departman"] for v in son.values() if (v.get("aday") or v["ad"]) == a and v.get("departman")) if a else "uygulanamaz (işlem kaydı)"
            yeni.append({"ad": k["ad"], "departman": d, "duzeltme": "departman", "satir": i + 1, "tarih": bugun})
            son[k["ad"]]["departman"], n = d, n + 1
            continue
        if (a := k.get("aday") or k["ad"]) not in dep:
            y = kok / "docs" / "kurulumlar" / "adaylar" / f"{a}.md"
            metin = y.read_text(encoding="utf-8") if y.is_file() else ""
            dep[a] = dp.sinifla(kok, jev, a, alanlar(metin).get("tur") or "skill", " ".join((tr.bolum(metin, "Ne") or a).split())[:dp.ACIKLAMA])[0]
        yeni.append({"ad": k["ad"], "departman": dep[a], "duzeltme": "departman", "satir": i + 1, "tarih": bugun})
        son[k["ad"]]["departman"], n = dep[a], n + 1
        ek.setdefault((dep[a], "Videodan gelen"), []).append(f"- {k['ad']} · {k['yargi']} · video {k.get('video') or '?'}")
    tr.kayit_ekle(ky, yeni)
    dp.katalog_ekle(kok, ek)
    print(f"geri dosyalanan: {n} kayıt · {len(dep)} aday · " + " · ".join(f"{a} → {d}" for a, d in dep.items())[:300]
          + f" · Jev istek {tk[0].istek if tk else 0} (tavan {ns.istek_tavan})")
    return 0


def teknik(ns, ctx):
    """K5: rapor '## Site/UI teknikleri' → bizde karşılığı varsa ÖĞREN (bilgi kartı, etiket frontend), yoksa UYARLA
    (bekleyen öneri: departman-frontend/omer-kutuphaneler, onaysız eklenmez); frontend kataloguna '## Teknikler'. Jev 0."""
    kok, bugun, ek, say = Path(ctx["env"].get("VIDEO_UYGULA_KOK") or KOK), date.today(), [], {"ÖĞREN": 0, "UYARLA": 0}
    for yol in ns.raporlar:
        metin = Path(yol).read_text(encoding="utf-8")
        vid = (re.search(r"youtu(?:\.be/|be\.com/watch\?v=)([\w-]{11})", metin) or [None, "?"])[1]
        t = tr.tablolar(tr.bolum(metin, tr.SITE_UI))
        for s in (t[0][1] if t else []):
            if len(s) != 4:
                continue
            tek, kanit, kut, bizde = s
            slug = re.sub(r"[^a-z0-9]+", "-", tek.translate(SLUG).casefold()).strip("-")
            if bizde.strip().casefold() not in ("", "-", "yok"):
                karar, y = "ÖĞREN", kok / "bilgi" / f"{slug}.md"
                if not y.is_file():
                    y.parent.mkdir(parents=True, exist_ok=True)
                    y.write_text(og.kart_metni({"ad": slug, "iddia": f"Site/UI tekniği: {tek}", "video": vid, "zaman": (tr.ZAMAN.search(kanit) or [""])[0],
                                                "etiketler": "frontend", "govde": f"# {tek}\nkanıt: {kanit}\nkütüphane/araç: {kut}\nbizde: {bizde}"}, bugun), encoding="utf-8")
            else:
                karar, y = "UYARLA", kok / "docs" / "kurulumlar" / "bekleyen" / f"teknik-{slug}.md"
                y.parent.mkdir(parents=True, exist_ok=True)
                y.write_text(f"# UYARLA teknik: {tek}\nkaynak: video {vid} · {kanit}\nkütüphane/araç: {kut}\n"
                             "hedef: departman-frontend müdür sırası ya da omer-kutuphaneler kaydı (öneri; onaysız eklenmez)\n\n"
                             "Onay: Ömer · ret: dosyayı sil.\n", encoding="utf-8")
            say[karar] += 1
            ek.append(f"- {tek} · {karar} · video {vid} · {kanit}")
    dp.katalog_ekle(kok, {("frontend", "Teknikler"): ek})
    print(f"teknik: ÖĞREN {say['ÖĞREN']} · UYARLA {say['UYARLA']} · docs/departmanlar/frontend.md ## Teknikler")
    return 0
