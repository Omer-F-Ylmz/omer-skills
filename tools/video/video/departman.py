"""19 departmanlar: aktif araçlar (skill · plugin · MCP · köprü CLI) → Jev choice → docs/departmanlar/{envanter.json, <dep>.md}.
Sıra: elle.json > elle-desen.json (joker) > önbellek > Jev; ad+açıklama hash'i değişmedikçe yeniden sorulmaz. Müdür skill'leri (skills/departman-<dep>) elle yazılır, burada denetlenir."""
import fnmatch
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from jev import cekirdek as c
from jev import skill as sk

KOK = Path(__file__).resolve().parents[3]
DEPARTMANLAR = {
    "frontend": "Arayüz tasarımı ve UI yapımı: marka, tipografi, renk, bileşen, landing, CSS/Tailwind, Figma, görsel üretim.",
    "test-qa": "Test yazma ve koşma, uygulamayı tarayıcıda deneme/kullanma, e2e, görsel QA, performans ölçümü.",
    "guvenlik": "Güvenlik denetimi, zafiyet taraması, pentest, sır taraması, tehdit modeli, KVKK/gizlilik uyumu.",
    "backend-dotnet": ".NET/C#/ASP.NET Core/MSBuild/NuGet ve sunucu tarafı API geliştirme.",
    "veri-db": "Veritabanı, SQL, Postgres/Supabase, EF Core sorguları, veri analitiği.",
    "verimlilik": "Token/context tasarrufu, çıktı sıkıştırma, oturum hafızası, maliyet düşürme, ajan verimliliği.",
    "arastirma-ogrenme": "Video izleme, web araştırması, kütüphane dokümantasyonu, kaynak tarama, öğrenme, bilgi grafiği.",
    "surec-plan": "Niyet netleştirme, brainstorm, spec, PRD, plan yazımı ve planı yürütme.",
    "surec-inceleme": "Kod review, sadeleştirme, doğrulama, kalite kapısı, PR yorumları.",
    "surec-git-yayin": "Git, commit, branch/worktree, PR, CI, sürüm, ship/deploy, canary.",
    "surec-ajan-arac": "Skill/plugin/MCP/hook/agent geliştirme, Claude Code ve ajan yardımcıları, genel CLI araçları.",
    "belge": "Belge üretimi: docx, pptx, pdf, xlsx, sunum, rapor, diyagram, yazı düzeltme.",
    "diger": "Yukarıdakilerin hiçbirine uymayan araçlar.",
}
SORU = "Bu Claude Code aracı (state: ad · tür · açıklama) hangi departmanın işine yarar? En yakın tek departmanı seç."
SATIR, ACIKLAMA, TOKEN, ESIK = 60, 200, 600, 3
NE_ZAMAN = re.compile(r"(?:Use (?:when|for|this|before|after)|USE (?:FOR|WHEN)|Trigger|TRIGGER|Activates? when|[^.]*\b(?:kullan|yükle|aç)\b)[^.]*", re.I)


def _json(y):
    try:
        return json.loads(Path(y).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _yaz(y, metin):
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(metin, encoding="utf-8", newline="\n")


def _hash(ad, aciklama):
    return hashlib.sha256(f"{ad}\n{aciklama}".encode()).hexdigest()[:16]


def topla(ev, kok):
    """Aktif araçlar [{ad, tur, aciklama}]. MCP'de yalnız sunucu adları okunur (env/args değerleri asla)."""
    cl = Path(ev) / ".claude"
    out = [{"ad": a, "tur": "skill", "aciklama": d or ""} for a, d in sk.adaylar(ev)]
    for ad, k, _ in sk._eklentiler(cl):
        out.append({"ad": ad, "tur": "plugin", "aciklama": ((_json(k / ".claude-plugin" / "plugin.json") or {}).get("description") or "")[:ACIKLAMA]})
    out += [{"ad": a, "tur": "mcp", "aciklama": ""} for a in (_json(Path(ev) / ".claude.json") or {}).get("mcpServers") or {}]
    izinli = (_json(Path(kok) / "tools" / "cc-kopru" / "kopru.json") or {}).get("izinli") or {}
    return out + [{"ad": a, "tur": "cli", "aciklama": ""} for a in izinli if not a.startswith("_")]


def durum(x):
    return f"{x['ad']} · {x['tur']} · {x['aciklama'] or '(açıklama yok)'}"


def soru():
    return {"departman": {"type": "choice", "instructions": SORU, "criteria": dict(DEPARTMANLAR)}}


def sec(cv):
    """choice yanıtı → (departman, p); yanıtsız → (diger, 0)."""
    pr = {k: v for k, v in (((cv or {}).get("departman") or {}).get("probabilities") or {}).items() if k in DEPARTMANLAR}
    d = max(pr, key=pr.get) if pr else "diger"
    return d, round(float(pr.get(d, 0.0)), 3)


def _elle(elle, x):
    return elle.get(f"{x['tur']}:{x['ad']}") or elle.get(x["ad"])


def _desen(desen, x):
    """elle-desen.json: ilk eşleşen joker (ad ya da tur:ad) → departman."""
    return next((d for k, d in desen.items() if fnmatch.fnmatchcase(x["ad"], k) or fnmatch.fnmatchcase(f"{x['tur']}:{x['ad']}", k)), None)


def siniflandir(araclar, eski, elle, yargila, yeniden=False, desen=None):
    """elle.json → elle-desen → önbellek (hash aynı, departman hâlâ var) → Jev (kalanlar tek yargila çağrısı). katman girdileri aktif değilse korunur."""
    onb = {(x["tur"], x["ad"]): x for x in eski}
    out, sor = [], []
    for a in araclar:
        x = {**a, "hash": _hash(a["ad"], a["aciklama"])}
        e = onb.get((a["tur"], a["ad"]))
        if d := _elle(elle, x):
            out.append({**x, "departman": d, "p": 1.0, "kaynak": "elle"})
        elif d := _desen(desen or {}, x):
            out.append({**x, "departman": d, "p": 1.0, "kaynak": "desen"})
        elif e and e.get("hash") == x["hash"] and e.get("kaynak") not in ("elle", "desen") and e.get("departman") in DEPARTMANLAR and not yeniden:
            out.append({**x, "departman": e["departman"], "p": e["p"], "kaynak": e["kaynak"]})
        else:
            sor.append(x)
    cevap = yargila([durum(x) for x in sor], soru()) if sor else []
    out += [{**x, **dict(zip(("departman", "p"), sec(cv))), "kaynak": "jev"} for x, cv in zip(sor, cevap)]
    aktif = {(x["tur"], x["ad"]) for x in araclar}
    return out + [x for x in eski if x.get("kaynak") == "katman" and (x["tur"], x["ad"]) not in aktif]


def denetle(araclar, envanter):
    """Her aktif araç tam bir departmanda; bilinmeyen departman yok."""
    say = Counter((x["tur"], x["ad"]) for x in envanter)
    h = [f"{t}:{a} {say[(t, a)]} departmanda" for t, a in sorted({(x["tur"], x["ad"]) for x in araclar}) if say[(t, a)] != 1]
    return h + [f"{x['tur']}:{x['ad']} bilinmeyen departman {x['departman']}" for x in envanter if x["departman"] not in DEPARTMANLAR]


def _aciklama(metin):
    m = re.match(r"---\n(.*?)\n---", metin.replace("\r\n", "\n"), re.S)
    a = re.search(r"^description:\s*(.+)$", m[1], re.M) if m else None
    return a[1].strip().strip("\"'") if a else ""


def mudur_denetle(yol):
    metin = Path(yol).read_text(encoding="utf-8")
    n, a = len(metin.splitlines()), _aciklama(metin)
    return ([f"{n} satır > {SATIR}"] if n > SATIR else []) + (
        ["description yok"] if not a else [f"description {len(a)} karakter > {ACIKLAMA}"] if len(a) > ACIKLAMA else [])


def mudurler(envanter):
    """Müdür gereken departmanlar: ≥3 araç (diger hariç); frontend daima."""
    return {d for d, n in Counter(x["departman"] for x in envanter).items() if n >= ESIK and d != "diger"} | {"frontend"}


def aciklama_token(kok):
    """Müdür skill'lerinin skill listesine eklediği maliyet: `- ad: description` satırları."""
    return sum(c.token(f"- {y.parent.name}: {_aciklama(y.read_text(encoding='utf-8'))}") for y in Path(kok).glob("skills/departman-*/SKILL.md"))


def sonraki(mudur, ad):
    """Müdürün numaralı adımlarında `ad`ın geçtiği adımdan sonraki adımın başlığı; yoksa '-'."""
    adim, kisa = re.findall(r"^\d+\. \*\*(.+?)\*\*(.*)$", mudur, re.M), ad.split(":")[-1]
    i = next((i for i, (_, g) in enumerate(adim) if f"`{kisa}`" in g), None)
    return adim[i + 1][0] if i is not None and i + 1 < len(adim) else "-"


def _hucre(s, n=90):
    s = " ".join(s.split()).replace("|", "\\|")
    return (s[:n - 1] + "…" if len(s) > n else s) or "-"


def katalog_yaz(kok, envanter):
    d = Path(kok) / "docs" / "departmanlar"
    for dep, aciklama in DEPARTMANLAR.items():
        y, md = d / f"{dep}.md", Path(kok) / "skills" / f"departman-{dep}" / "SKILL.md"
        eski = y.read_text(encoding="utf-8") if y.is_file() else ""
        elle = eski.split("\n## Elle\n", 1)[1] if "\n## Elle\n" in eski else ""
        mudur = md.read_text(encoding="utf-8") if md.is_file() else ""
        satir = [f"| {x['ad']} | {x['tur']} | {_hucre(re.split(r'(?<=[.!?])\s', x['aciklama'])[0])} | "
                 f"{_hucre((NE_ZAMAN.search(x['aciklama']) or [''])[0])} | {sonraki(mudur, x['ad'])} |"
                 for x in sorted(envanter, key=lambda x: (x["tur"], x["ad"])) if x["departman"] == dep]
        _yaz(y, "\n".join([f"# Departman: {dep}", "", f"> {aciklama}", "",
                           f"Müdür: `departman-{dep}`" if mudur else "Müdür: yok (<3 araç ya da henüz yazılmadı)",
                           "<!-- `video departman` üretir; yalnız '## Elle' altı korunur. Düzeltme: docs/departmanlar/elle.json -->", "",
                           "| araç | tür | ne işe yarar | ne zaman | sıradaki adım |", "|---|---|---|---|---|",
                           *(satir or ["| (araç yok) | | | | |"]), "", "## Elle", ""]) + elle)


def kaydet(kok, envanter):
    _yaz(Path(kok) / "docs" / "departmanlar" / "envanter.json",
         json.dumps(sorted(envanter, key=lambda x: (x["departman"], x["tur"], x["ad"])), ensure_ascii=False, indent=1) + "\n")
    katalog_yaz(kok, envanter)


def dosyala(kok, jev, ad, tur, aciklama):
    """katman: yeni aracı tek choice ile sınıflar (elle.json kazanır; Jev yoksa diger/0 → gözden geçir), envantere kaynak=katman."""
    d = Path(kok) / "docs" / "departmanlar"
    x = {"ad": ad, "tur": tur, "aciklama": aciklama}
    if dep := _elle(_json(d / "elle.json") or {}, x) or _desen(_json(d / "elle-desen.json") or {}, x):
        p = 1.0
    else:
        try:
            dep, p = sec(jev().yargila([durum(x)], soru())[0])
        except c.JevHata:
            dep, p = "diger", 0.0
    kaydet(kok, [e for e in _json(d / "envanter.json") or [] if (e["tur"], e["ad"]) != (tur, ad)]
           + [{**x, "hash": _hash(ad, aciklama), "departman": dep, "p": p, "kaynak": "katman"}])
    return dep, p


def departman(ns, ctx):
    """`video departman [--yeniden]`: envanter → sınıflama → katalog; rapor: dağılım · gözden geçir · müdürler · description token."""
    env = ctx["env"]
    kok, ev = Path(env.get("VIDEO_UYGULA_KOK") or KOK), Path(env.get("VIDEO_EV") or Path.home())
    d = kok / "docs" / "departmanlar"
    araclar, tk = topla(ev, kok), []

    def yargila(states, sorular):
        tk.append(c.Tasiyici(env=env, en_fazla=len(c.parcala(states)), gonder=ctx["gonder"], istek_tavan=ns.istek_tavan))
        return tk[0].yargila(states, sorular)

    e = siniflandir(araclar, _json(d / "envanter.json") or [], _json(d / "elle.json") or {}, yargila, ns.yeniden, _json(d / "elle-desen.json") or {})
    if hata := denetle(araclar, e):
        print("hata: " + " · ".join(hata[:20]))
        return 1
    kaydet(kok, e)
    b = c.bantlar_oku()
    say = Counter(x["departman"] for x in e)
    gg = sorted((x for x in e if x["kaynak"] not in ("elle", "desen") and x["p"] < b["act"]), key=lambda x: x["p"])
    gerek, var = mudurler(e), {y.parent.name.removeprefix("departman-"): y for y in kok.glob("skills/departman-*/SKILL.md")}
    mud = [f"departman-{m} " + ("eksik" if m not in var else "✓" if not (h := mudur_denetle(var[m])) else "; ".join(h))
           for m in sorted(gerek)] + [f"departman-{m} fazla ({say[m]} araç < {ESIK})" for m in sorted(set(var) - gerek)]
    tok = aciklama_token(kok)
    print("departman: " + " · ".join(f"{k} {n}" for k, n in say.most_common()) + f" (toplam {len(e)})")
    print(f"gözden geçir: {len(gg)} (Act<{b['act']}) — " + ", ".join(f"{x['ad']} ({x['departman']} {x['p']:.2f})" for x in gg[:25]))
    print("müdür: " + " · ".join(mud))
    print(f"description token: {tok}/{TOKEN} · Jev istek {tk[0].istek if tk else 0} (tavan {ns.istek_tavan}) · {d / 'envanter.json'}")
    return 1 if tok > TOKEN or any("fazla" in m or ">" in m or "yok" in m for m in mud) else 0
