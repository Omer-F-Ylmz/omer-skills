"""14b onay · geri-al · dene: bekleyen/<ad>.md yapılandırılmış adımları (serbest kabuk yok) → kur · duman · geri alma;
docs/denemeler/<ad>.md → tavanlı `claude -p` A/B + Jev kalite puanı."""
import json
import re
import subprocess
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
    hata, plan = [], {"duman": None, "kopru": None, "ayar": []}
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
    try:
        return ctx["kos"]([str(x) for x in args], timeout=timeout, **k)
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, b"", str(e).encode()


def _kok(ctx):
    return Path(ctx["env"].get("VIDEO_UYGULA_KOK") or KOK)


def _kayit(kok, ad, alan):
    """Adın girdisi güncellenip sona taşınır; yoksa eklenir."""
    ky = kok / "docs" / "kurulumlar" / "kayit.jsonl"
    ky.parent.mkdir(parents=True, exist_ok=True)
    k = tr.kayit_oku(ky)
    eski = next((x for x in reversed(k) if x["ad"] == ad), {"ad": ad})
    tr.kayit_yaz(ky, [x for x in k if x is not eski] + [{**eski, **alan}])


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
             + [f"geri alma: {' '.join(a)}" for a in plan["geri"]])
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


def esik(s):
    def sayi(desen, yok):
        x = re.search(desen, s or "", re.I)
        return float(x[1].replace(",", ".")) if x else yok
    return {"cikti": sayi(r"çıktı[^%]*%\s*(\d+(?:[.,]\d+)?)", 25), "kalite": sayi(r"kalite\D*(\d+(?:[.,]\d+)?)", 0.3),
            "maliyet": sayi(r"maliyet[^%]*%\s*(\d+(?:[.,]\d+)?)", None)}


def karar(a, b, e):
    """Sınır dahil: çıktı düşüşü ≥ eşik VE kalite düşüşü ≤ eşik (VE maliyet eşiği varsa maliyet düşüşü ≥ eşik)."""
    yuzde = lambda k: round((a[k] - b[k]) / a[k] * 100, 6) if a.get(k) else 0.0
    dus, kd = yuzde("cikti"), round(a["kalite"] - b["kalite"], 6)
    ok = dus >= e["cikti"] and kd <= e["kalite"]
    ozet = f"çıktı −%{dus:.1f} (eşik %{e['cikti']:g}) · kalite düşüşü {kd:.2f} (eşik {e['kalite']:g})"
    if e.get("maliyet") is not None:
        ok = ok and yuzde("maliyet") >= e["maliyet"]
        ozet += f" · maliyet −%{yuzde('maliyet'):.1f} (eşik %{e['maliyet']:g})"
    return ("KUR önerisi → ONAY" if ok else "RED(ölçüm)") + f": {ozet}"


def _istem(g):
    ss = g.read_text(encoding="utf-8").splitlines()
    ek = [f"\n\n{x[6:].strip()}:\n```\n{(g.parent / x[6:].strip()).read_text(encoding='utf-8')}```" for x in ss if x.startswith("dosya:")]
    return "\n".join(x for x in ss if not x.startswith("dosya:")).strip() + "".join(ek)


def dene(ns, ctx):
    env, kok = ctx["env"], _kok(ctx)
    d = kok / "docs" / "denemeler"
    metin = (d / f"{ns.ad}.md").read_text(encoding="utf-8")
    ty = next((s.strip() for s in tr.bolum(metin, "Talimat").splitlines() if s.strip()), "")
    gorevler = sorted((d / "gorevler").glob("*.md"))
    if not ty or not (kok / ty).is_file() or not gorevler:
        print(f"deneme eksik: ## Talimat dosyası ({ty or 'yok'}) ya da docs/denemeler/gorevler/*.md yok")
        return 1
    if 2 * len(gorevler) > ns.tavan:
        print(f"tavan: {2 * len(gorevler)} claude -p gerekir, --tavan {ns.tavan}; koşulmadı")
        return 1
    talimat, istemler = (kok / ty).read_text(encoding="utf-8"), [_istem(g) for g in gorevler]
    alt_env, olcum = {**env, "JEV_SKILL_HOOK": "0"}, []  # hook iki kola farklı skill önerisi enjekte etmesin
    for ist in istemler:
        a = ["claude", "-p", ist, "--model", "sonnet", "--output-format", "json"]
        for kol, args in (("A", a), ("B", a + ["--append-system-prompt", talimat])):
            rc, out, err = _kos(ctx, args, 600, env=alt_env)
            try:
                j = json.loads(out)
            except ValueError:
                j = {}
            if rc or j.get("is_error") or "result" not in j:
                print(f"hata: claude -p {kol} rc {rc}: {(err or out).decode('utf-8', 'replace')[-200:]}")
                return 1
            u = j.get("usage") or {}
            olcum.append({"kol": kol, "yanit": j["result"], "cikti": u.get("output_tokens", 0), "sure": (j.get("duration_ms") or 0) / 1000,
                          "girdi": sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")),
                          "maliyet": j.get("total_cost_usd") or 0})
    t = c.Tasiyici(env=env, en_fazla=len(olcum), gonder=ctx["gonder"], istek_tavan=ns.istek_tavan)
    cv = t.yargila([f"GÖREV:\n{istemler[i // 2]}\n\nYANIT:\n{o['yanit']}" for i, o in enumerate(olcum)], {"kalite": KALITE_Q})
    for o, x in zip(olcum, cv):
        if not x:
            print("hata: Jev kalite puanı yok")
            return 1
        o["kalite"] = x["kalite"]["score"]
    ort = {k: {f: sum(o[f] for o in olcum if o["kol"] == k) / len(istemler) for f in ALANLAR} for k in "AB"}
    e = esik(tr.bolum(metin, "Başarı eşiği"))
    k = karar(ort["A"], ort["B"], e)
    bugun = date.today().isoformat()
    satir = [f"# Deneme sonucu: {ns.ad}", "", f"{bugun} · sonnet · {len(istemler)} görev · claude -p {len(olcum)} · Jev istek {t.istek} · hook kapalı (JEV_SKILL_HOOK=0)",
             f"B kolu: A + --append-system-prompt ({ty})", "", "## Kol ortalamaları", "| kol | çıktı | girdi | süre sn | maliyet $ | kalite 0-3 |", "|---|---|---|---|---|---|"]
    satir += [f"| {kol} | {v['cikti']:.0f} | {v['girdi']:.0f} | {v['sure']:.1f} | {v['maliyet']:.4f} | {v['kalite']:.2f} |" for kol, v in ort.items()]
    satir += ["", "## Görev başına (çıktı · kalite)"] + [f"- {g.stem}: A {olcum[2 * i]['cikti']} · {olcum[2 * i]['kalite']:.2f} → B {olcum[2 * i + 1]['cikti']} · {olcum[2 * i + 1]['kalite']:.2f}"
                                                       for i, g in enumerate(gorevler)]
    satir += ["", "## Karar", k, ""]
    (d / f"{ns.ad}-sonuc.md").write_text("\n".join(satir), encoding="utf-8")
    _kayit(kok, ns.ad, {"karar": k, "deneme": f"docs/denemeler/{ns.ad}-sonuc.md", "tarih": bugun})
    print("\n".join(satir[2:3] + satir[8:10] + [k]))
    return 0
