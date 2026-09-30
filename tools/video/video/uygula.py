"""14a video-uygula: aday.md → katman (T0 kural · T1 yalnız-md skill · T2 onay · RED), uygulama, kayıt; projeler özeti.
15: K1 karar kümesi (KUR · DENE · ÖĞREN · ZATEN VAR · ALTERNATİF · RED), kural/olgu, kart, çelişki, sponsor, bizde durum."""
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import date, datetime
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


BILINMIYOR = "son commit bilinmiyor"


def bakim_red(a, bugun, t2=False):
    """14a lisans listesi yalnız T1 (repoya kopyalama) içindir; 17 K6: T2'de kaynak-erişilebilir lisans RED değil, lisans notu."""
    if a.get("lisans") not in LISANS and not (t2 and a.get("lisans") in KAYNAK_ACIK):
        return f"lisans uygunsuz/yok: {a.get('lisans') or 'yok'}"
    if a.get("arsiv") == "evet":
        return "arşivlenmiş"
    try:
        son = date.fromisoformat(a.get("son_commit", ""))
    except (ValueError, TypeError):
        return BILINMIYOR
    if (bugun - son).days > 365:
        return f"12 aydır commit yok ({son})"
    return None


ARAC = {"skill", "plugin", "mcp", "cli", "hook", "uygulama"}


def arac_mu(a, metin):
    """24a K4: araç = kurulabilir paket/CLI/MCP/plugin/skill; repo ya da yapılandırılmış kurulum satırı yoksa teknik/kavram."""
    return (a.get("tur") or "").casefold() in ARAC and (a.get("repo", "yok") not in ("", "yok")
                                                        or bool(re.search(r"^- \w+:\s*\S", tr.bolum(metin, "Kurulum"), re.M)))


def md_disi(dosyalar):
    return [f for f in dosyalar if not (f.lower().endswith(".md") or SERBEST.match(Path(f).name))]


def sinifla(a, bugun, dosyalar=None, high=None):
    """(katman, gerekçe). Skill'de dosyalar kaynak klasöründen gerçekten listelenir, high SkillSpector'dan (None: koşmadı)."""
    if a.get("red"):
        return "RED", a["red"]
    if r := bakim_red(a, bugun, a.get("tur") != "skill"):
        return ("SOR", "eksik: son_commit") if r == BILINMIYOR else ("RED", r)  # M10 K2: bilinmeyen RED değil (M2c K2)
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


def prompt_bekleyen(kok, x, ad):
    """23c K7: şablonda olmayan kalıp → bekleyen/prompt-<slug>.md (şablona ekleme önerisi, onaysız eklenmez)."""
    slug = re.sub(r"[^a-z0-9]+", "-", x["kalip"].translate(SLUG).casefold()).strip("-")[:60].strip("-")
    b = kok / "docs" / "kurulumlar" / "bekleyen" / f"prompt-{slug}.md"
    b.parent.mkdir(parents=True, exist_ok=True)
    b.write_text(f"# UYARLA prompt kalıbı: {x['kalip']}\nkaynak: video {x['video']} · {x['zaman']} · aday {ad}\nteknik: {x.get('teknik') or '-'}\n"
                 f"hedef: skills/departman-frontend `## {SABLON}` (öneri; onaysız eklenmez)\n\nOnay: Ömer · ret: dosyayı sil.\n", encoding="utf-8")
    return b


def prompt_isle(kok, ad, metin, tk=None, liste=()):
    """23c K7: kalıbın şablon bölümü departman-frontend `## Yapım promptu şablonu` `- <bölüm>:` satırlarında varsa ZATEN VAR,
    yoksa UYARLA bekleyen/prompt-<slug>.md (şablona ekleme önerisi, onaysız eklenmez). Jev 0."""
    s = kok / "skills" / "departman-frontend" / "SKILL.md"
    bolum = {m[1].casefold() for m in re.finditer(r"^- (\w+):", tr.bolum(s.read_text(encoding="utf-8"), SABLON) if s.is_file() else "", re.M)}
    say, satir = {"ZATEN VAR": 0, "UYARLA": 0}, []
    for x in kaliplar(metin, alanlar(metin).get("video")):
        if x["sablon"].casefold() in bolum:
            karar, x["karsilik"] = "ZATEN VAR", f"şablon: {x['sablon']}"
        elif tk and (z := prompt_zaten(tk, f"{ad}: {x['kalip']}", liste)) and z[1] >= ZATEN_ESIK:  # 24c K4
            karar, x["karsilik"] = "ZATEN VAR", f"K4: {z[0]} (p {z[1]:.2f})"
        elif tk and z:  # 24d: olası tekrar → Desktop incelemesi
            b = olasi_yaz(kok, f"{ad}: {x['kalip']}", z, liste, x["video"])
            karar, x["karsilik"] = "OLASI TEKRAR", f"OLASI TEKRAR ({z[0]} p={z[1]:.2f}) · bekleyen/{b.name}"
        else:
            karar, x["karsilik"] = "UYARLA", "yok → bekleyen"
            prompt_bekleyen(kok, x, ad)
        say[karar] = say.get(karar, 0) + 1
        satir.append({**x, "aday": ad})
    kutuphane_ekle(kok, satir)
    return say


def lisans_norm(s):
    """24b K2: lisans yazımı tek biçime (MIT License→MIT, Apache 2.0→Apache-2.0, BSL 1.1→BUSL-1.1, yok/none/boş→yok); bilinmeyen → sade anahtar."""
    k = re.sub(r"[\s_.-]+|licen[cs]e|lisans", "", re.sub(r"\s*\(.*$", "", str(s or "")).casefold())
    if k in ("", "yok", "none", "noassertion"):
        return "yok"
    bilinen = {re.sub(r"[\s_.-]+", "", x.casefold()): x for x in LISANS | KAYNAK_ACIK} | {"apache": "Apache-2.0", "bsl11": "BUSL-1.1", "bsl": "BUSL-1.1"}
    return bilinen.get(k, k)


def kanit(o, a, metin, kok, env):
    """17 K4: RED gerekçesi kanıta bağlı mı. ölçüm: var olan docs/denemeler/*-sonuc.md · zaten var: katalog/durum.md adı ya da
    var olan dosya · lisans: aday lisansı izinli/kaynak-erişilebilir değil · güvenlik: aday dosyasında SkillSpector HIGH/CRITICAL.
    24b K2: gerekçedeki tüm ` · ` parçaları (`anahtar: değer`) okunur, biri kanıtlıysa yeter; lisans normalleştirilerek karşılaştırılır."""
    for p in o.get("gerekce", "").split(" · "):
        on, _, g = p.partition(":")
        on = re.sub(r"^\(?\d+\)\s*", "", on.strip()).casefold()
        if on == "ölçüm" and any((kok / y).is_file() for y in re.findall(r"docs/denemeler/[\w.-]+-sonuc\.md", g)):
            return True
        if on == "zaten var":
            adlar = {tr.normal(x) for x, _ in tr.sozluk_kur(Path(env.get("VIDEO_EV") or Path.home()), [])} | {tr.normal(x) for x, _ in og.ARACLAR}
            if (d := kok / "docs" / "durum.md").is_file():
                adlar |= {tr.normal(x) for x in re.findall(r"^- ([^\s:→]+)\s*(?:→|:)", d.read_text(encoding="utf-8"), re.M)}
            if any(tr.normal(w) in adlar or (kok / w).is_file() for w in re.findall(r"[\w.@/-]+", g) if tr.normal(w)):
                return True
        if on == "lisans" and (li := o.get("lisans") or a.get("lisans")) and lisans_norm(li) == lisans_norm(g) and lisans_norm(li) not in LISANS | KAYNAK_ACIK:
            return True
        if on == "güvenlik" and re.search(r"SkillSpector[^\n]*(HIGH|CRITICAL)", metin.replace(tr.bolum(metin, "Özellikler"), "")):
            return True  # bulgu özellik satırında değil aday dosyasının kendisinde olmalı
    return False


def ozellik_karar(o, a, metin, kok, env):
    """(karar, gerekçe). 17 K4: karar yoksa DENE; token etiketli özellikte kanıtsız RED → DENE."""
    k, g = o.get("karar") if o.get("karar") in og.KARAR else "DENE", o.get("gerekce", "")
    if k == "DENE" and "yarım" in a.get("arastirma", ""):  # 24a K1: yarım araştırmaya DENE verilmez
        return "ÖĞREN", f"K1: araştırma yarım, DENE verilmez ({g or '-'})"
    if k == "RED" and "token" in o.get("etiket", "").casefold() and not kanit(o, a, metin, kok, env):
        return "DENE", f"K4: kanıt bulunamadı — RED({g or 'gerekçesiz'}) → DENE"
    return k, g


YAPIM_TUR = ("plugin", "MCP", "CLI", "hook")  # 24e-2 K4: kod ürünü → yapım tarifi; skill/talimat mevcut `video uret`


def yapim_yaz(kok, o, oa, al, kaynak, lisans):
    """24e-2 K4: docs/uyarlamalar/<ad>-yapim.md — amaç · mekanizma+kaynak · arayüz · test planı · güvenlik/izin · maliyet · lisans; kod kopyalanmaz.
    Var olan dosya ezilmez (Desktop düzeltmiş olabilir). Ömer `ÜRET <ad>` derse Desktop yapım dalgası yazar."""
    y = Path(kok) / "docs" / "uyarlamalar" / f"{oa}-yapim.md"
    if not y.is_file():
        y.parent.mkdir(parents=True, exist_ok=True)
        b = (("Amaç", al["fikir"]), ("Alınan mekanizma + kaynağı", f"{o.get('mekanizma') or o.get('ne') or '?'} · kaynak {kaynak}"),
             ("Arayüz", o.get("arayuz") or "? (komut/araç adları yapım dalgasında)"), ("Test planı", o.get("test") or "? (kırmızı-önce, yapım dalgasında)"),
             ("Güvenlik/izin kapsamı", al["kapsam"]), ("Maliyet", f"yapım dalgası (CC) · etki: {al['etki']}"),
             ("Lisans notu", f"{lisans or '?'} · kaynak kodu kopyalanmaz, mekanizma yeniden yazılır"))
        y.write_text(f"# Yapım tarifi: {oa}\n\nhedef_tur: {al['hedef_tur']}\nvideo: {o.get('video', '?')}\n\n" + "".join(f"## {k}\n{v}\n\n" for k, v in b),
                     encoding="utf-8")
    return f"{oa} · {al['hedef_tur']} · docs/uyarlamalar/{y.name} · `ÜRET {oa}` → Desktop yapım dalgası"


def uyarla_alan(kok, o):
    """24a K6: fikir · hedef · etki · kapsam alan satırından ya da `gerekce` içindeki `anahtar: değer` parçalarından; fikir yoksa `ne`,
    hedef yoksa gerekçede anılan repo skill'i; eksik alan 'aday.md'de yok'. hedef_tur: alan > skill adı/`skill` > talimat."""
    g = {x[1]: x[2] for p in o.get("gerekce", "").split(" · ") if (x := ALAN.match(p.strip()))}
    al = {k: o.get(k) or g.get(k) for k in ("fikir", "hedef", "etki", "kapsam")}
    al["fikir"] = al["fikir"] or o.get("ne")
    sk_ = sorted((d.name for d in (Path(kok) / "skills").iterdir() if d.is_dir()), key=len, reverse=True) if (Path(kok) / "skills").is_dir() else []
    s = next((x for x in sk_ if re.search(rf"(?<![\w-]){re.escape(x)}(?![\w-])", f"{al['hedef'] or ''} {o.get('gerekce', '')}")), None)
    al["hedef"] = al["hedef"] or (f"skills/{s} (gerekçede anılan)" if s else None)
    h = al["hedef"] or ""
    tur = o.get("hedef_tur") or ("skill" if s or re.search(r"(?i)skill", h) else "talimat" if re.search(r"(?i)talimat|CLAUDE\.md", h) else next((t for t in YAPIM_TUR if re.search(rf"(?i)(?<![\w-]){t}(?![\w-])", h)), ""))
    return {**{k: v or "aday.md'de yok" for k, v in al.items()}, "hedef_tur": tur}


def uyarla_yaz(kok, o, ad):
    """17 K3: fikir kendi araçlarımıza uygulanır; yalnız doküman, kod yazılmaz (Desktop tarif verir)."""
    al = uyarla_alan(kok, o)
    y = Path(kok) / "docs" / "uyarlamalar" / f"{ad}.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(f"# Uyarlama: {ad}\n\n17 K3 · kod yazılmaz; Desktop tarif verir\n\n" + "".join(
        f"## {b}\n{al[k]}\n\n" for b, k in (("Fikir", "fikir"), ("Hedef araç/dosya", "hedef"), ("Beklenen etki", "etki"), ("Kapsam", "kapsam"))),
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


def brief_frontend(kok, metin):
    """24c K3: uygula raporunun son koşusundaki adayların videoları → frontend.md `## Teknikler` satırları + o videoların prompt kalıpları."""
    son = tr.kayit_son(tr.kayit_oku(kok / "docs" / "kurulumlar" / "kayit.jsonl"))
    vid = {v for k in son.values() if k["ad"] in metin or (k.get("aday") or "\0") in metin for v in re.split(r",\s*", k.get("video") or "") if v}
    fe = kok / "docs" / "departmanlar" / "frontend.md"
    tek = [s for s in tr.bolum(fe.read_text(encoding="utf-8"), "Teknikler").splitlines() if s.startswith("- ") and any(f"video {v}" in s for v in vid)] if fe.is_file() else []
    kal = [f"- {x['kalip']} · {x['video']} {x['zaman']} · şablon: {x['sablon']}" for y in sorted((kok / "docs" / "kurulumlar" / "adaylar").glob("*.md"))
           for m in [y.read_text(encoding="utf-8")] if alanlar(m).get("video") in vid for x in kaliplar(m, alanlar(m).get("video"))]
    ot = [f"- {m.get('öneri')} · {m.get('kaynak')}: {(m.get('kaynak satırı') or '')[:80]} · p={m.get('p')}"
          for y in sorted((kok / "docs" / "kurulumlar" / "bekleyen").glob("olasi-*.md"))
          for m in [dict(re.findall(r"^([^:\n]+): (.*)$", y.read_text(encoding="utf-8"), re.M))] if m.get("video") in vid]  # 24d
    return [("Site/UI teknikleri", tek[:6], "bu koşunun videolarında teknik yok"), ("Prompt anatomisi", kal[:6], "bu koşunun prompt adayı yok"),
            ("Olası tekrarlar", ot[:8], "bu koşuda 0.4–0.6 bandında öneri yok")]


def brief(ns, ctx):
    """17 K7: Desktop ikinci görüş girdisi, ≤60 satır. Uygula raporu: özellik kararları · departman · iddia sınama.
    24a K7 tarama raporu (`## Adaylar`): aday tablosu · departman (kayit.jsonl, o video) · İddialar · Site/UI · prompt anatomisi (o videonun aday.md'leri).
    Kaynağı boş bölüm '- yok (…)' yazar; başlık boş kalmaz."""
    metin, kok = Path(ns.rapor).read_text(encoding="utf-8"), Path(ctx["env"].get("VIDEO_UYGULA_KOK") or KOK)
    tablo = lambda b: (tr.tablolar(tr.bolum(metin, b)) or [([], [])])[0][1]  # noqa: E731
    link = list(dict.fromkeys(re.findall(r"https?://[^\s|)]+", metin)))
    if tr.bolum(metin, "Adaylar").strip():
        vid = (re.search(r"youtu(?:\.be/|be\.com/watch\?v=)([\w-]{11})", metin) or [None, ""])[1]
        son = tr.kayit_son(tr.kayit_oku(kok / "docs" / "kurulumlar" / "kayit.jsonl"))
        adaylar = [y.read_text(encoding="utf-8") for y in sorted((kok / "docs" / "kurulumlar" / "adaylar").glob("*.md"))]
        b = [("Adaylar", [f"- {s[0]} · {s[2]} · {s[4]} ({s[5]})" for s in tablo("Adaylar") if len(s) >= 6][:15], "raporda aday yok"),
             ("Departman", [f"- {k['ad']} → {k['departman']} · {k.get('yargi', '-')}" for k in son.values() if k.get("video") == vid and k.get("departman")][:8],
              "kayit.jsonl'de bu videonun kararı yok"),
             ("İddialar", [f"- {s[0]} ({s[1]} · {s[2]})" for s in tablo("İddialar") if len(s) >= 3][:10], "raporda iddia yok"),
             ("Site/UI teknikleri", [f"- {s[0]} · {s[2]} · bizde: {s[3]}" for s in tablo(tr.SITE_UI) if len(s) == 4][:6], "raporda site/UI tekniği yok"),
             ("Prompt anatomisi", [f"- {x['kalip']} · {x['zaman']} · şablon: {x['sablon']}" for m in adaylar if alanlar(m).get("video") == vid
                                   for x in kaliplar(m, vid)][:8], "bu videonun prompt adayı yok")]
    else:
        metin = metin.rsplit("\n## Koşu ", 1)[-1]  # 24a-kapanış: birden çok koşuda kararlar son koşudan (tablo da bunu okur)
        b = [("Özellik kararları", [s for s in tr.bolum(metin, "ÖZELLİK KARARLARI").splitlines() if s.startswith("- ")][:25], "raporda yok"),
             ("Departman", [s for s in tr.bolum(metin, "DEPARTMAN").splitlines() if s.startswith("- ")][:10], "raporda yok"),
             ("İddialar", [f"- {s[0]} → {s[2]} ({s[1]})" for s in tablo("İDDİA SINAMA") if len(s) >= 3][:16], "raporda yok"),  # 24c K3: ≤60 satır
             *([("Yapım tarifleri", yt, "")] if (yt := [s for s in tr.bolum(metin, "YAPIM TARİFLERİ").splitlines() if s.startswith("- ")][:8]) else []),  # 24e-2 K4: boşsa bölüm yok (≤60 satır)
             *brief_frontend(kok, metin)]
    print("\n".join([f"# brief: {Path(ns.rapor).name}", *[s for ad, x, yok in b for s in [f"## {ad}", *(x or [f"- yok ({yok})"])]],
                     "## Linkler", *([f"- {x}" for x in link[:6]] or ["- yok"])]))
    return 0


ESDEGER_Q = "Videodan gelen bu adayın (state: ad: ne) ana işini yapan bir araç listede var mı? Varsa onu seç; hiçbiri yapmıyorsa yok."


def esdeger(kok, jev, ad, ne, dep):
    """24a K8: aynı departman kataloğundan Ne ile en çok kelime paylaşan 5 araç → tek Jev choice. (araç, p) ya da None (yok/katalog boş)."""
    w = lambda s: set(re.findall(r"\w{3,}", s.casefold()))  # noqa: E731
    liste = sorted((x for x in dp._json(Path(kok) / "docs" / "departmanlar" / "envanter.json") or []
                    if x.get("departman") == dep and tr.normal(x["ad"].split(":")[-1]) != tr.normal(ad)),
                   key=lambda x: -len(w(ne) & w(f"{x['ad']} {x.get('aciklama', '')}")))[:5]
    if not liste:
        return None
    kr = {**{x["ad"]: (x.get("aciklama") or x["tur"])[:dp.ACIKLAMA] for x in liste}, "yok": "hiçbiri bu adayın ana işini yapmıyor"}
    try:
        y = jev().yargila([f"{ad}: {ne}"], {"es": {"type": "choice", "instructions": ESDEGER_Q, "criteria": kr}})[0] or {}
    except c.JevHata:
        return None
    pr = {k: v for k, v in ((y.get("es") or {}).get("probabilities") or {}).items() if k != "yok"}
    return max(pr.items(), key=lambda z: z[1]) if pr else None


def _departman(kok, jev, ad, a, metin, depl, envantere=True, onceki=None, site=False):
    """19 K5: yeni araç → departman (KUR/UYARLA envanter + katalog); 23 K2: karar ne olursa olsun departman; rapor DEPARTMAN bölümü.
    24a K8: eşdeğer için önceden sınıflandıysa (onceki) ikinci Jev isteği yok. 24b K4: p<0.6 notu (site → frontend / belirsiz) satıra yazılır."""
    ne = " ".join(tr.bolum(metin, "Ne").split())[:dp.ACIKLAMA]
    dep, p, nt = dp.dosyala(kok, jev, ad, a.get("tur") or "skill", ne, onceki, site) if envantere else onceki or dp.sinifla(kok, jev, ad, a.get("tur") or "skill", ne, site)
    depl.append(f"{ad} → {dep} ({p:.2f})" + (f" · {nt}" if nt else ""))
    return dep


def _kos(ctx, args, timeout=300):  # 24c K5: 600 → 300
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


BUYUK_REPO_KB = 100 * 1024  # 24c K5: gh api .size KB; üstü klonlanmaz


def on_tarama(ctx, repo_ad):
    """24b K1: araştırmadan ÖNCE sığ klon (önbellek <kök>/repo/<o__r>, 120 sn) + SkillSpector --no-llm → on.md `## Güvenlik ön taraması`."""
    ad = repo_ad.replace("/", "__")
    hedef = ctx["kok"] / "repo" / ad
    if not hedef.is_dir():
        rc, out, _ = _kos(ctx, ["gh", "api", f"repos/{repo_ad}", "--jq", ".size"], timeout=30)  # 24c K5
        kb = int(s) if not rc and (s := (out or b"").decode("utf-8", "replace").strip()).isdigit() else 0
        if kb > BUYUK_REPO_KB:
            return f"## Güvenlik ön taraması\natlandı (repo {kb // 1024} MB)\n"
        rc, _, err = _kos(ctx, ["git", "clone", "--depth", "1", f"https://github.com/{repo_ad}", hedef], timeout=120)
        if rc or not hedef.is_dir():
            return f"## Güvenlik ön taraması\nkoşmadı: klon başarısız ({(err or b'').decode('utf-8', 'replace').strip()[:120]})\n"
    high = spector(ctx, ad, hedef)
    return ("## Güvenlik ön taraması\n" + ("koşmadı: SkillSpector raporu yok" if high is None else f"SkillSpector --no-llm HIGH/CRITICAL {high}")
            + f"\nkaynak: {hedef.as_posix()}\n")


ISKELET_ALAN = ("lisans", "son_commit", "arsiv", "kaynak", "telemetri")
ISKELET_BOLUM = ("Kurulum", "İzinler", "Duman testi", "Geri alma", "Köprü izni", "Önerilen katman")


def iskelet(kok, video, ad, tur, repo_ad, on_yol, guvenlik=None, kurulu=None):
    """24c K1: araştırıcıdan ÖNCE hat aday.md iskeletini on.md'den yazar (başlıklar + bilinen alanlar, kalan "araştırılıyor",
    `arastirma: yarım`). Araştırıcı yalnız Edit ile günceller; tur biterse dosya yine geçerli. Var olan dosya ezilmez."""
    from video.cli import _slug  # cli bu modülü içe aktarır; döngü yalnız çağrıda çözülür
    y = kok / "docs" / "kurulumlar" / "adaylar" / f"{_slug(ad)}.md"
    if y.exists():
        return y
    if kurulu:  # parti-d: kurulu araç → on/araştırıcı yok; videodaki yeni kullanım ana ajan eliyle `### <x>` + `karar: ÖĞREN`
        g = f"kurulu: {kurulu}"
        s = [f"# {ad}", f"ad: {ad}", f"tur: {tur or 'araç'}", f"video: {video}", f"repo: {repo_ad or 'yok'}", "karar: ZATEN VAR", f"gerekce: {g}",
             "arastirma: tam: kurulu, araştırıcı yok", "## Ne", f"kurulu araç ({g})", "## Bizde durum", g, "## Beklenen fayda",
             "kurulu; videodaki yeni kullanım özellik düzeyinde ÖĞREN", "## Maliyet/risk", "yok: kurulum yapılmaz", "## Karar", "ZATEN VAR (kurulu)",
             "## Sonraki adım", "yeni kullanım varsa `## Özellikler` altına `### <x>` + `karar: ÖĞREN`", "## Özellikler", "### kurulu", "karar: ZATEN VAR", f"gerekce: {g}"]
        y.parent.mkdir(parents=True, exist_ok=True)
        y.write_text("\n".join(s) + "\n", encoding="utf-8")
        return y
    s = [f"# {ad}", f"ad: {ad}", f"tur: {tur or 'araştırılıyor'}", f"video: {video}", f"repo: {repo_ad or 'yok'}",
         *(f"{k}: araştırılıyor" for k in ISKELET_ALAN), "arastirma: yarım: hat iskeleti (araştırıcı Edit ile doldurur, bitince `arastirma: tam`)",
         "## Ne", "araştırılıyor", "## Kanıt", f"- ön getirme: {Path(on_yol).as_posix()}",
         *(f"- güvenlik ön taraması: {x}" for x in (guvenlik or "").splitlines()[1:2]), *(x for b in ISKELET_BOLUM for x in (f"## {b}", "araştırılıyor"))]
    if tur == "prompt":
        s += ["## Prompt anatomisi", *(f"{k}: araştırılıyor" for k in ANATOMI), "### Kalıplar"]
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text("\n".join(s) + "\n", encoding="utf-8")
    return y


def site_mi(env, video):
    """24b K4: video site/UI içerikli mi — yeniden kaydındaki içerik türü ya da tarama raporunda `tr.frontend_mu`."""
    from video.cli import TARAMA_DIZIN  # cli bu modülü içe aktarır; döngü yalnız çağrıda çözülür
    d = Path(env.get("VIDEO_TARAMA_DIZIN") or TARAMA_DIZIN)
    ks = [k for k in tr.kayit_oku(d / "kayit.jsonl") if k.get("id") == video] if video and (d / "kayit.jsonl").is_file() else []
    if any(k.get("tur") == tr.ICERIK[0] for k in ks):
        return True
    r = next((d / k["rapor"] for k in reversed(ks) if not k.get("etiket") and k.get("rapor")), None)
    return bool(r and r.is_file() and tr.frontend_mu(r.read_text(encoding="utf-8")))


T0_ORNEK = (("GLB dosya boyutu seçimi (2MB vs 6MB)", "prompt"), ("Yerelde ayağa kaldırma isteği", "ipucu"), ("GitHub'da kod paylaşımı", "ipucu"),
            ("Aşırı sade tasarımla akılda kalıcılık", "prompt"), ("Asla sözümden çıkma kesin talimat", "prompt"),
            ("Ayrı mobil/masaüstü performans optimizasyonu isteği", "prompt"), ("Düzeltme yerine mesajı Edit/Regenerate", "ipucu"),
            ("MiniMax API anahtarı oluşturma + bakiye yükleme", "araca-özel"), ("Büyüyen tek dosyada parçalama öner (god-file eşiği)", "kural"))
T0_SORU = ("Videodan çıkan bu öneri (state) dört türden hangisi? Sırayla sına: 1) öznesi Ömer'in eylemi (paylaş, çalıştır, yükle, düzenle, kopyala) → ipucu; "
           "2) site/tasarım/görsel içeriği ya da prompta yazılacak şey → prompt; 3) belirli bir araç/servis adı ve onun prosedürü → araca-özel; "
           "4) yalnız Claude/Claude Code'un her projede çalışma biçimini yöneten genel ilke → kural. Örnekler (öneri → doğru tür): "
           + " · ".join(f"{a} → {t}" for a, t in T0_ORNEK))
T0_OLCUT = {"kural": "Yalnız Claude/Claude Code'un her projede geçerli çalışma biçimini yöneten genel ilke; Ömer'in eylemi, site içeriği ya da araç prosedürü değil.",
            "prompt": "Site/UI/tasarım/görsel/video üretirken prompta yazılacak içerik ya da kalıp (ne ve nasıl tarif edilir; tasarım ilkesi dahil).",
            "ipucu": "Öznesi Ömer'in eylemi: bir aracı ya da çıktıyı kullanma alışkanlığı (paylaş, çalıştır, yükle, düzenle); Claude'un çalışma ilkesi değil.",
            "araca-özel": "Belirli bir aracın/hizmetin (adıyla) kurulum, hesap, anahtar, bakiye ya da mod prosedürü."}

MODEL_ADI = re.compile(r"\b(fable|opus|sonnet|haiku|gpt-?\d[\w.]*|gemini|llama|mistral|deepseek|qwen)\b", re.I)  # 15 K3: model olgusu


def t0_tur(tk, ad, a):
    """24b K5 + 24c K2: olgu | kural | prompt | ipucu | araca-özel — 15 K3 olgu sorusuyla aynı istekte. Soru örnekli (T0_ORNEK);
    model adı (15 K3) Jev'e sorulmadan olgu; araç/servis adı (MiniMax, codex…) sorulur: Jev ipucu/prompt/araca-özel derse o,
    kural derse ad geçiyorsa ya da olgu ağır basarsa olgu."""
    if MODEL_ADI.search(f"{ad} {a.get('iddia') or ''} {a.get('kural') or ''}"):
        return "olgu"
    q = {"tur": {"type": "choice", "instructions": og.TUR_SORU, "criteria": og.TUR_OLCUT},
         "t0": {"type": "choice", "instructions": T0_SORU, "criteria": T0_OLCUT}}
    y = tk.yargila([f"İPUCU: {ad}\nİddia: {a.get('iddia') or '-'}\nKural önerisi: {a.get('kural') or ad}"], q)[0] or {}
    t = {k: v for k, v in ((y.get("t0") or {}).get("probabilities") or {}).items() if k in T0_OLCUT}
    if (tt := max(t, key=t.get) if t else "kural") != "kural":
        return tt
    p = (y.get("tur") or {}).get("probabilities") or {}
    return "olgu" if og.ADLI.search(f"{ad} {a.get('iddia') or ''} {a.get('kural') or ''}") or p.get("olgu", 0) > p.get("kural", 0) else "kural"


ZATEN_SORU = ("Bu prompt/kural önerisini listedeki mevcut şablon satırı, prompt kalıbı, kural ya da DESIGN.md kuralı zaten karşılıyor mu? "
              "Karşılayanı seç; hiçbiri karşılamıyorsa hiçbiri.")
ZATEN_NOUL = "Mevcut satır bu öneriyi zaten karşılıyor mu (aynı şeyi ister ya da kapsar)? Satır: {k}"
ZATEN_KURAL = ("25", "26")  # omer-kurallar: site/UI yapım promptu + 3D CONFIG (24c K4, Ömer)
ZATEN_ESIK = 0.6
OLASI_ESIK = 0.4  # 24d (Ömer 28 Eyl (a)): 0.4 ≤ p < 0.6 → OLASI TEKRAR, Desktop incelemesi


def zaten_liste(kok, env, haric=None):
    """24c K4: [(id, metin)] — departman-frontend şablon satırları · frontend-promptlar.md kalıpları (haric aday hariç) ·
    omer-kurallar 25-26 · DESIGN.md kuralları (frontend-craft + departman-frontend)."""
    oku = lambda y: Path(y).read_text(encoding="utf-8") if Path(y).is_file() else ""  # noqa: E731
    out = [(f"şablon:{x[1]}", x[0][2:]) for x in re.finditer(r"^- (\w+):.*$", tr.bolum(oku(kok / "skills" / "departman-frontend" / "SKILL.md"), SABLON), re.M)]
    for i, s in enumerate(oku(kok / "docs" / "departmanlar" / "frontend-promptlar.md").splitlines()):
        h = [x.strip() for x in s.strip().strip("|").split("|")]
        if s.startswith("| ") and s != KUTUPHANE and len(h) >= 6 and not set(h[0]) <= set("-") and h[5] != haric:
            out.append((f"kalıp:{i + 1}", f"{h[0]} (teknik: {h[3]})"))
    for y in tr.kural_kaynaklari(env, Path(env.get("VIDEO_EV") or Path.home())):
        if "omer-kurallar" in Path(y).name:
            out += [(f"omer-kurallar:{x[1]}", x[2]) for x in re.finditer(r"^(\d+)\.\s+(.+)$", oku(y), re.M) if x[1] in ZATEN_KURAL]
    for ad, y in (("frontend-craft", kok / "plugins" / "frontend-craft" / "skills" / "frontend-craft" / "SKILL.md"),
                  ("departman-frontend", kok / "skills" / "departman-frontend" / "SKILL.md")):
        sat = oku(y).splitlines()
        for i, s in enumerate(sat):
            if "DESIGN.md" in s:  # `:` ile biten satırın girintili listesi de (ör. 6 başlık: … Tipografi …)
                alt = [x.strip() for x in sat[i + 1:i + 9] if s.rstrip().endswith(":")] if s.rstrip().endswith(":") else []
                alt = alt[:next((j for j, x in enumerate(sat[i + 1:i + 9]) if not x.startswith(" ")), len(alt))]
                out.append((f"DESIGN.md ({ad}:{i + 1})", " · ".join([s.strip().lstrip("-* ").strip(), *alt])))
    return [(i, x[:300]) for i, x in out]


def prompt_zaten(tk, oneri, liste):
    """24c K4: öneriyi mevcut satır karşılıyor mu — en yakın (1 istek) + noul (1 istek); p ≥0.4 → (id, p), değilse None.
    Bant çağıranda: p ≥ZATEN_ESIK ZATEN VAR · altı OLASI TEKRAR (24d)."""
    if not liste or not (ilk := tr.en_yakin(tk, f"ÖNERİ: {oneri}", liste, ZATEN_SORU)):
        return None
    y = (tk.yargila([f"ÖNERİ: {oneri}"], {"k": {"type": "noul", "instructions": ZATEN_NOUL.format(k=dict(liste).get(ilk, ilk))}})[0] or {}).get("k")
    return (ilk, y["noul"]) if y and y["noul"] >= OLASI_ESIK else None


def olasi_yaz(kok, oneri, z, liste, video):
    """24d K4 bandı: 0.4 ≤ p < 0.6 → bekleyen/olasi-<slug>.md (karar: Desktop incelemesi); kendiliğinden UYARLA/ZATEN VAR olmaz, var olanı ezmez."""
    slug = re.sub(r"[^a-z0-9]+", "-", oneri.translate(SLUG).casefold()).strip("-")[:60].strip("-")
    b = kok / "docs" / "kurulumlar" / "bekleyen" / f"olasi-{slug}.md"
    b.parent.mkdir(parents=True, exist_ok=True)
    if not b.exists():
        b.write_text(f"# OLASI TEKRAR: {oneri}\nöneri: {oneri}\nkaynak: {z[0]}\nkaynak satırı: {' '.join(str(dict(liste).get(z[0], z[0])).split())}\n"
                     f"p: {z[1]:.2f}\nvideo: {video}\nkarar: Desktop incelemesi\n\nOnay: Ömer · aynıysa dosyayı sil (ZATEN VAR) · değilse UYARLA önerisi.\n", encoding="utf-8")
    return b


def toplu_isaret(env, video, ad):
    """24c K6: en yeni toplu tablosunda bu videonun bu adayının işareti (ör. `ÇİFT (kural: CLAUDE:15)`); yoksa ''."""
    from video.cli import TARAMA_DIZIN, _slug  # cli bu modülü içe aktarır; döngü yalnız çağrıda çözülür
    d = Path(env.get("VIDEO_TARAMA_DIZIN") or TARAMA_DIZIN)
    for y in sorted(d.glob("*-toplu*.md"), key=lambda p: p.stat().st_mtime, reverse=True) if video and d.is_dir() else []:
        for s in y.read_text(encoding="utf-8").splitlines():
            h = [x.strip() for x in s.strip().strip("|").split("|")]
            if s.startswith("| ") and len(h) >= 7 and video in h[6] and (ad == h[0] or _slug(ad) == _slug(h[0])):  # 24e-1 K1: eski Türkçe ad da eşleşir
                return h[1]
    return ""


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
    slug = tr.slug(ad) or "kural"
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


T0_ALAN, T0_BOLUM = ("ad", "tur", "video", "etiket", "karar"), ("Kanıt", "İddia sınama", "Bizde durum")


def t0_denetle(metin):  # 24e-1 K5: T0 aday dosyası şeması
    a = alanlar(metin)
    h = [f"T0 alanı eksik: {k}" for k in T0_ALAN if not a.get(k)]
    if not a.get("kural") and not tr.bolum(metin, "Ne").strip():
        h.append("T0 alanı eksik: kural (ya da ## Ne)")
    return h + [f"T0 bölümü eksik: {b}" for b in T0_BOLUM if not tr.bolum(metin, b).strip()]


def kural_onay(ns, ctx):
    env = ctx["env"]
    kok = Path(env.get("VIDEO_UYGULA_KOK") or KOK)
    b = kok / "docs" / "kurulumlar" / "bekleyen" / f"kural-{tr.slug(ns.slug)}.md"  # 24e-1 K1: eski Türkçe slug da çözülür
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
    gorulen = {tr.normal(k.get("aday") or k["ad"]) for k in kayit if not k.get("karar", "").startswith("SORULMADI")}  # 24e-1 K4: sorulmayan tekrar koşulur
    oto, onay, zipler, red, atla, ogrenilen, celiski, dene, ozet, rapor, eksik, ozk, sinama, depl, uret_, yapim = ([] for _ in range(16))
    n = 9 * len(ns.adaylar) + 2 * sum(len(kaliplar(Path(y).read_text(encoding="utf-8"), None)) for y in ns.adaylar)  # 24c K4: kalıp başına 2 +  # aday başına tür 1 + çift 2 + çelişki 2 (+ sponsor 1) + departman 1 + eşdeğer 1

    def jev():
        nonlocal tk
        if tk is None:
            tk = c.Tasiyici(env=env, en_fazla=n, gonder=ctx["gonder"], istek_tavan=ns.istek_tavan or n, uyu=ctx["uyku"])
        return tk
    videodan, eklenen = {}, []
    listeler = (oto, onay, zipler, red, atla, ogrenilen, celiski, dene, ozet, rapor, eksik, ozk, sinama, depl, uret_)
    bag = []
    for yol in ns.adaylar:
        uz = [len(x) for x in listeler]
        try:
            metin = Path(yol).read_text(encoding="utf-8")
            a = alanlar(metin)
            ad = a.get("ad") or Path(yol).stem
            if tr.normal(ad) in gorulen and not ns.yeniden:
                atla.append(ad)
                continue
            me = og.meta(ctx, a.get("video"))
            kanal, sponsor = a.get("kanal") or me.get("channel"), og.sponsor_mu(ctx, me, a, jev)
            site = site_mi(env, a.get("video"))  # 24b K4
            if prompt_mu(metin):  # 23c K7: prompt anatomisi → site prompt kütüphanesi (Jev 0)
                ps = prompt_isle(kok, ad, metin, jev(), zaten_liste(kok, env, ad))
                ogrenilen.append(f"{ad}: prompt anatomisi → docs/departmanlar/frontend-promptlar.md · " + " · ".join(f"{k} {v}" for k, v in ps.items()))
            oz, on_dep, es = ozellikler(metin), None, None
            if (any(o.get("karar") == "KUR" for o in oz) if oz else a.get("karar") in (None, "KUR")) and arac_mu(a, metin) and not a.get("red"):
                ne = " ".join(tr.bolum(metin, "Ne").split())[:dp.ACIKLAMA]  # 24a K8: işlevsel eşdeğer, aday başına 1 istek
                on_dep = dp.sinifla(kok, jev, ad, a.get("tur") or "skill", ne, site)
                es = esdeger(kok, jev, ad, ne, on_dep[0])
            isaret = f" · işaret: olası eşdeğer {es[0]} (p {es[1]:.2f})" if es and 0.4 <= es[1] < 0.6 else ""
            if oz:  # 17 K3: özellik düzeyi; aday bütün olarak tartılmaz
                yeni, satir = [], []
                for o in oz:
                    yk, g = ozellik_karar(o, a, metin, kok, env)
                    if yk == "KUR" and es and es[1] >= 0.6:
                        yk, g = "ZATEN VAR", f"K8 işlevsel eşdeğer: {es[0]} (p {es[1]:.2f}); kurulum yok"
                    elif yk == "KUR":
                        g += isaret
                    oa, o = f"{ad}-{o['ozellik']}", {**({"video": a["video"]} if a.get("video") else {}), **o}
                    if yk == "UYARLA":
                        karar, al = uyarla_yaz(kok, o, oa), uyarla_alan(kok, o)
                        if al["hedef_tur"] in ("skill", "talimat"):  # 24a K6: hedef aday.md alanlarından
                            uret_.append(f"{oa} · kaynak {ad}/{o['ozellik']} · hedef: {al['hedef']} · fayda: {al['etki']} · maliyet: claude -p ≤24 · ≈${24 * CAGRI_USD:.2f} · `ÜRET {oa}`")
                        elif al["hedef_tur"].casefold() in {t.casefold() for t in YAPIM_TUR}:  # 24e-2 K4
                            yapim.append(yapim_yaz(kok, o, oa, al, f"{ad}/{o['ozellik']}", a.get("lisans")))
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
                dep = _departman(kok, jev, ad, a, metin, depl, any(k["yargi"] in ("KUR", "UYARLA") for k in yeni), on_dep, site)
                yeni = [{**k, "departman": dep} for k in yeni]
                videodan.setdefault((dep, "Videodan gelen"), []).extend(f"- {k['ad']} · {k['yargi']} · video {k.get('video') or '?'}" for k in yeni)
                ozet.append((sponsor, f"{ad} → özellik düzeyi: " + " · ".join(f"{o['ozellik']} {k['yargi']}" for o, k in zip(oz, yeni))))
                rapor.append((sponsor, [f"## {ad} → özellik düzeyi{' · sponsor' if sponsor else ''}", *satir, ""]))
                gorulen.add(tr.normal(ad))
                eklenen += yeni  # 23c: append-only; okuma kayit_son ile
                continue
            yargi = a.get("karar") if a.get("karar") in og.KARAR else "KUR"  # karar alanı yoksa 14a yolu
            if yargi == "DENE" and "yarım" in a.get("arastirma", ""):  # 24a K1
                yargi = "ÖĞREN"
            if "yarım" in a.get("arastirma", "") and not a.get("karar"):  # 24c K1: hat iskeletinde kalan aday lisans kapısına düşmez
                yargi = "ÖĞREN"
            if a.get("karar") and yargi != "RED" and (x := [b for b in ALTI if not tr.bolum(metin, b).strip()]):
                eksik.append(f"{ad}: {', '.join(x)}")
            commit, kt, karar, geri, ek = None, "-", "", "-", ""
            ti = toplu_isaret(env, a.get("video"), ad) if a.get("tur") in tr.KURAL_TUR else ""  # 24c K6: toplu kural çifti devralınır
            if ti.startswith("ÇİFT") and yargi not in ("KUR", "ZATEN VAR"):
                celiski.append(f"{ad} ↔ toplu {ti}: aday.md karar {yargi}")
            if yargi == "KUR" and ti.startswith("ÇİFT") and not a.get("red"):
                kt, yargi, karar = "T0", "ZATEN VAR", f"eklenmez: toplu {ti}"
            elif yargi == "KUR" and a.get("tur") in tr.KURAL_TUR and not a.get("red"):
                t0t = t0_tur(jev(), ad, a)  # 24b K5: yalnız "kural" bekleyen/kural-*.md üretir
                if t0t in ("olgu", "ipucu"):  # 15 K3: olgu kural dosyasına girmez · kullanım ipucu → bilgi kartı (etiket kullanım)
                    yargi, a = "ÖĞREN", ({**a, "etiketler": "kullanım"} if t0t == "ipucu" else a)
                elif t0t == "prompt":  # prompt kalıbı → kütüphane; yeni kalıp şablona UYARLA önerisi
                    x = {"kalip": a.get("kural") or ad, "video": a.get("video") or "?", "zaman": a.get("zaman") or "?", "teknik": a.get("teknik") or "-",
                         "aday": ad, "karsilik": "yok → bekleyen"}
                    zl = zaten_liste(kok, env, ad)
                    if (z := prompt_zaten(jev(), f"{ad}: {x['kalip']}", zl)) and z[1] >= ZATEN_ESIK:  # 24c K4: şablon/kütüphane/kural/DESIGN.md
                        kt, yargi, karar = "T0", "ZATEN VAR", f"K4 zaten var: {z[0]} (p {z[1]:.2f})"
                    elif z:  # 24d: p 0.4–0.6 → OLASI TEKRAR (UYARLA/ÖĞREN değil), Desktop incelemesi
                        b = olasi_yaz(kok, f"{ad}: {x['kalip']}", z, zl, x["video"])
                        kt, yargi, karar = "T0", "OLASI TEKRAR", f"OLASI TEKRAR ({z[0]} p={z[1]:.2f}) · bekleyen/{b.name}"
                    elif not tr.ZAMAN.search(x["zaman"]) or x["teknik"] == "-":  # 24c K4 (h): kaynaksız öneri UYARLA olamaz
                        kt, yargi, ek = "T0", "ÖĞREN", " · eksik kaynak (zaman/teknik yok)"
                    elif kutuphane_ekle(kok, [x]):
                        kt, yargi, b = "T0", "UYARLA", prompt_bekleyen(kok, x, ad)
                        karar, geri = f"prompt kalıbı → frontend-promptlar.md · bekleyen/{b.name}", f"rm {b.relative_to(kok).as_posix()}"
                        onay.append(f"UYARLA {b.stem}")
                    else:
                        kt, yargi, karar = "T0", "ZATEN VAR", "prompt kalıbı frontend-promptlar.md'de var"
                elif t0t == "araca-özel":  # aracın aday.md'sine prosedür satırı; kural değil
                    h = kd / "adaylar" / f"{a.get('arac')}.md"
                    h = h if a.get("arac") and h.is_file() else Path(yol)
                    m, s = h.read_text(encoding="utf-8"), f"- {ad}: {a.get('kural') or ad} (video {a.get('video') or '?'})"
                    if s not in m:
                        b_ = "## Araca özel prosedür\n"
                        h.write_text(m.replace(b_, b_ + s + "\n", 1) if b_ in m else m.rstrip("\n") + f"\n\n{b_}{s}\n", encoding="utf-8")
                    kt, yargi, karar = "T0", "ARACA ÖZEL", f"araca özel prosedür → adaylar/{h.name} (kural değil)"
                else:
                    kt, (karar, geri) = "T0", t0(ctx, a, ad, jev(), kok, metin)
                    if "ÇİFT" in karar:
                        yargi = "ZATEN VAR"
                    else:
                        onay.append(karar.split(" · ")[0])
                        if "ÇELİŞKİ" in karar:
                            celiski.append(f"{ad} ↔ {karar.split('ÇELİŞKİ (', 1)[1][:-1]}: {a.get('kural') or ad}")
            if yargi == "KUR" and kt == "-" and not arac_mu(a, metin):  # 24a K4: teknik/kavram lisans kapısına girmez
                yargi = "ÖĞREN"
            elif yargi == "KUR" and kt == "-" and es and es[1] >= 0.6:  # 24a K8
                yargi, a = "ZATEN VAR", {**a, "gerekce": f"K8 işlevsel eşdeğer: {es[0]} (p {es[1]:.2f}); kurulum yok"}
            if yargi == "ÖĞREN":
                karar, cel = og.ogren(jev(), kok, a, ad, bugun, _kurallar(ctx)[1])
                karar += ek
                if cel:
                    celiski.append(f"{ad} ↔ {cel}: {a.get('iddia') or a.get('kural') or ad}")
                else:
                    ogrenilen.append(f"{ad}: {karar}")
            elif yargi == "DENE":
                karar = og.deneme_yaz(kok, a, ad, metin)
                dene.append(f"{ad}: {karar}")
            elif yargi == "UYARLA" and kt == "-":
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
                if yargi == "KUR":
                    karar += isaret
            dep = _departman(kok, jev, ad, a, metin, depl, yargi in ("KUR", "UYARLA") and kt != "T0", on_dep, site)
            videodan.setdefault((dep, "Videodan gelen"), []).append(f"- {ad} · {yargi} · video {a.get('video') or '?'}")
            ozet.append((sponsor, f"{ad} → {yargi}{' (sponsor)' if sponsor else ''} — {karar}"))
            rapor.append((sponsor, [f"## {ad} → {yargi}{' · sponsor' if sponsor else ''}", f"- Sonuç: {karar}"]
                          + [f"- {b}: {' '.join(tr.bolum(metin, b).split())[:400] or ('-' if yargi == 'RED' else '(eksik)')}" for b in ALTI] + [""]))
            sina(kok, ad, metin, sinama, eksik)
            gorulen.add(tr.normal(ad))
            eklenen.append(
                {"ad": ad, "katman": kt, "yargi": yargi, "karar": karar, "tarih": bugun.isoformat(), "video": a.get("video"), "kanal": kanal,
                 "sponsor": sponsor, "kaynak_commit": commit, "geri_alma": geri, **({"departman": dep} if dep else {})})
        except c.TavanHata:
            raise
        except c.JevHata as e:  # 24e-1 K4: bağlantı koparsa aday işaretlenir, koşu sürer
            for x, k in zip(listeler, uz):
                del x[k:]
            bag.append(f"{ad} ({e})")
            eklenen.append({"ad": ad, "katman": "SORULMADI", "yargi": "SORULMADI", "karar": "SORULMADI: bağlantı", "tarih": bugun.isoformat(), "video": a.get("video")})
    tr.kayit_ekle(ky, eklenen)
    dp.katalog_ekle(kok, videodan)
    bayat = [f"{s} ({fm.get('bayatlama')})" for s, fm, _ in og.kartlar(kok) if fm.get("bayatlama", "") < bugun.isoformat()]
    bolumler = (("ÖZELLİK KARARLARI", ozk), ("ÖĞRENİLENLER", ogrenilen), ("ÇELİŞKİLER (otomatik eklenmedi, Ömer karar verir)", celiski), ("DENENECEKLER", dene),
                ("ÜRETİLEBİLİR", uret_), ("YAPIM TARİFLERİ", yapim), ("OTOMATİK UYGULANDI", oto), ("ONAY BEKLİYOR", onay), ("YÜKLENECEK ZIP", zipler), ("RED", red), ("DEPARTMAN", depl), ("YENİDEN DOĞRULA (bayat kart)", bayat))
    tam = kd / f"{bugun.isoformat()}-uygula.md"
    if rapor:  # sponsor adayları düşük öncelik: sona; 24a K5: aynı gün ikinci koşu ezmez, `## Koşu N` olarak eklenir
        eski = tam.read_text(encoding="utf-8").rstrip("\n") if tam.is_file() else ""
        bas = [eski, "", f"## Koşu {eski.count(chr(10) + '## Koşu ') + 2} — {datetime.now():%H:%M}", ""] if eski else [f"# video-uygula — {bugun.isoformat()}", ""]
        tam.write_text("\n".join(bas + [s for _, r in sorted(rapor, key=lambda x: x[0]) for s in r]
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
    if bag:
        print(f"UYARI bağlantı: {len(bag)} aday SORULMADI (sonraki koşu yeniden sorar) — " + " · ".join(bag)[:300])
    print((f"atlandı (kayıtta, --yeniden): {' '.join(atla)} · " if atla else "") + f"Jev istek {tk.istek if tk else 0} · kayıt: {ky}"
          + (f" · rapor: {tam}" if rapor else ""))
    return 1 if bag and len(bag) == len(eklenen) else 0  # 24e-1 K4: hepsi koptuysa hata


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
SLUG = tr.TR_ASCII


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
    from . import akil  # akil uygula'yı içe aktarır; döngüsel içe aktarmayı önler
    kok, bugun, ek, say = Path(ctx["env"].get("VIDEO_UYGULA_KOK") or KOK), date.today(), [], {"ÖĞREN": 0, "UYARLA": 0}
    for yol in ns.raporlar:
        metin = Path(yol).read_text(encoding="utf-8")
        vid = (re.search(r"youtu(?:\.be/|be\.com/watch\?v=)([\w-]{11})", metin) or [None, "?"])[1]
        t = tr.tablolar(tr.bolum(metin, tr.SITE_UI))
        for s in (t[0][1] if t else []):
            if len(s) != 4:
                continue
            tek, kanit, kut, bizde = s
            if akil._gozlem_mu(f"{tek} {kanit}"):  # M7 K3: site_ogren ile aynı gözlem süzgeci
                continue
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
