"""14b onay · geri-al · dene: bekleyen/<ad>.md yapılandırılmış adımları (serbest kabuk yok) → kur · duman · geri alma;
docs/denemeler/<ad>.md → tavanlı `claude -p` A/B + Jev kalite puanı."""
import json
import re
import shutil
import subprocess
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


def esik(s):
    def sayi(desen, yok):
        x = re.search(desen, s or "", re.I)
        return float(x[1].replace(",", ".")) if x else yok
    return {"cikti": sayi(r"çıktı[^%]*%\s*(\d+(?:[.,]\d+)?)", 25), "maliyet": sayi(r"maliyet[^%]*%\s*(\d+(?:[.,]\d+)?)", None)}


def karar(a, b, e, gurultu, basari):
    """18 K1, sınır dahil: KUR yalnız (1) token hedefi (çıktı düşüşü ≥ eşik, maliyet eşiği varsa o da) VE (2) her görevde B başarı ≥ A başarı
    ortalaması VE (3) B kalite ≥ A − max(gürültü, 0.1). Kalite düşüşüne sabit pay yok; bant yalnız A'nın kendi tekrar gürültüsü."""
    yuzde = lambda k: round((a[k] - b[k]) / a[k] * 100, 6) if a.get(k) else 0.0
    dus, bant = yuzde("cikti"), max(gurultu, 0.1)
    tok = dus >= e["cikti"] and (e.get("maliyet") is None or yuzde("maliyet") >= e["maliyet"])
    dusen = [i + 1 for i, (sa, sb) in enumerate(basari) if sb < sa]
    kal = not dusen and round(b["kalite"] - a["kalite"] + bant, 6) >= 0
    red = [x for x, ok in (("token", tok), ("kalite", kal)) if not ok]
    ozet = (f"çıktı −%{dus:.1f} (eşik %{e['cikti']:g}) · kalite {a['kalite']:.2f}→{b['kalite']:.2f} (bant {bant:.2f}) · "
            f"başarısı düşen görev: {', '.join(map(str, dusen)) or 'yok'}")
    if e.get("maliyet") is not None:
        ozet += f" · maliyet −%{yuzde('maliyet'):.1f} (eşik %{e['maliyet']:g})"
    return ("KUR önerisi → ONAY" if not red else f"RED({', '.join(red)})") + f": {ozet}"


def _parca(g):
    """Görev dosyası → (istem satırları, beklenen maddeleri); `beklenen:` satırından sonrası modele gitmez."""
    ss = g.read_text(encoding="utf-8").splitlines()
    i = next((i for i, s in enumerate(ss) if s.strip() == "beklenen:"), len(ss))
    return ss[:i], [s.strip()[2:].strip() for s in ss[i + 1:] if s.strip().startswith("- ")]


def _istem(g):
    ss = _parca(g)[0]
    ek = [f"\n\n{x[6:].strip()}:\n```\n{(g.parent / x[6:].strip()).read_text(encoding='utf-8')}```" for x in ss if x.startswith("dosya:")]
    return "\n".join(x for x in ss if not x.startswith("dosya:")).strip() + "".join(ek)


def basari(g, yanit, kos):
    """18 K1 makine kontrolü: her `olgu:` deseni var · hiçbir `yasak:` deseni yok · `pytest:` yanıttaki son python bloğu görevin
    `dosya:`ı yerine geçici dizine yazılır, test yanında koşar ve geçer. Beklenen yoksa başarı."""
    ss, bk = _parca(g)
    for s in bk:
        tur, _, d = (x.strip() for x in s.partition(":"))
        if (tur == "olgu" and not re.search(d, yanit)) or (tur == "yasak" and re.search(d, yanit)):
            return False
        if tur == "pytest":
            kod = re.findall(r"```(?:python|py)?[ \t]*\r?\n(.*?)```", yanit, re.S)
            dosya = next((x[6:].strip() for x in ss if x.startswith("dosya:")), None)
            if not kod or not dosya:
                return False
            with tempfile.TemporaryDirectory() as t:
                (Path(t) / Path(dosya).name).write_text(kod[-1], encoding="utf-8")
                shutil.copy2(g.parent / d, Path(t) / Path(d).name)
                if kos(["uv", "run", "--no-project", "--with", "pytest", "python", "-m", "pytest", "-q", "-p", "no:cacheprovider", str(Path(t) / Path(d).name)], timeout=120)[0]:
                    return False
    return True


def govde(metin):
    return re.sub(r"\A---\r?\n.*?\r?\n---\r?\n", "", metin, count=1, flags=re.S)


def _ngram(s, n=8):
    w = re.findall(r"\w+", s.casefold())
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def ortusme(taslak, kaynak):
    """Taslağın 8-gram'larının kaynakta da geçen payı (küçük harf, kelime)."""
    t = _ngram(taslak)
    return len(t & _ngram(kaynak)) / len(t) if t else 0.0


def dene(ns, ctx):
    env, kok = ctx["env"], _kok(ctx)
    d = kok / "docs" / "denemeler"
    metin = (d / f"{ns.ad}.md").read_text(encoding="utf-8")
    ty = next((s.strip() for s in tr.bolum(metin, "Talimat").splitlines() if s.strip()), "")
    gorevler = sorted((d / "gorevler").glob("*.md"))
    if not ty or not (kok / ty).is_file() or not gorevler:
        print(f"deneme eksik: ## Talimat dosyası ({ty or 'yok'}) ya da docs/denemeler/gorevler/*.md yok")
        return 1
    if 3 * len(gorevler) > ns.tavan:
        print(f"tavan: {3 * len(gorevler)} claude -p gerekir (görev × A 2 + B 1), --tavan {ns.tavan}; koşulmadı")
        return 1
    talimat, istemler = govde((kok / ty).read_text(encoding="utf-8")), [_istem(g) for g in gorevler]
    alt_env, olcum = {**env, "JEV_SKILL_HOOK": "0"}, []  # hook iki kola farklı skill önerisi enjekte etmesin
    for gi, (g, ist) in enumerate(zip(gorevler, istemler)):
        a = ["claude", "-p", ist, "--model", "sonnet", "--output-format", "json"]
        for kol, args in (("A", a), ("A", a), ("B", a + ["--append-system-prompt", talimat])):  # A iki kez: gürültü
            rc, out, err = _kos(ctx, args, 600, env=alt_env)
            try:
                j = json.loads(out)
            except ValueError:
                j = {}
            if rc or j.get("is_error") or "result" not in j:
                print(f"hata: claude -p {kol} rc {rc}: {(err or out).decode('utf-8', 'replace')[-200:]}")
                return 1
            u = j.get("usage") or {}
            olcum.append({"kol": kol, "gorev": gi, "yanit": j["result"], "cikti": u.get("output_tokens", 0), "sure": (j.get("duration_ms") or 0) / 1000,
                          "girdi": sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")),
                          "maliyet": j.get("total_cost_usd") or 0, "basari": basari(g, j["result"], lambda x, timeout: _kos(ctx, x, timeout))})
    t = c.Tasiyici(env=env, en_fazla=len(olcum), gonder=ctx["gonder"], istek_tavan=ns.istek_tavan)
    cv = t.yargila([f"GÖREV:\n{istemler[o['gorev']]}\n\nYANIT:\n{o['yanit']}" for o in olcum], {"kalite": KALITE_Q})
    for o, x in zip(olcum, cv):
        if not x:
            print("hata: Jev kalite puanı yok")
            return 1
        o["kalite"] = x["kalite"]["score"]
    ort = {k: {f: sum(o[f] for o in olcum if o["kol"] == k) / sum(o["kol"] == k for o in olcum) for f in ALANLAR + ("basari",)} for k in "AB"}
    gor = [[o for o in olcum if o["gorev"] == i] for i in range(len(gorevler))]  # [A1, A2, B]
    gurultu = sum(abs(x[0]["kalite"] - x[1]["kalite"]) for x in gor) / len(gor)
    k = karar(ort["A"], ort["B"], esik(tr.bolum(metin, "Başarı eşiği")), gurultu, [((x[0]["basari"] + x[1]["basari"]) / 2, x[2]["basari"]) for x in gor])
    bugun = date.today().isoformat()
    satir = [f"# Deneme sonucu: {ns.ad}", "", f"{bugun} · sonnet · {len(istemler)} görev · claude -p {len(olcum)} (A 2 tekrar + B 1) · Jev istek {t.istek} · "
             f"hook kapalı (JEV_SKILL_HOOK=0) · toplam maliyet ${sum(o['maliyet'] for o in olcum):.4f}",
             f"B kolu: A + --append-system-prompt ({ty}, frontmatter hariç) · gürültü (A1-A2 kalite farkı ort.) {gurultu:.2f}", "", "## Kol ortalamaları",
             "| kol | başarı | kalite 0-3 | çıktı | girdi | süre sn | maliyet $ |", "|---|---|---|---|---|---|---|"]
    satir += [f"| {kol} | {v['basari']:.2f} | {v['kalite']:.2f} | {v['cikti']:.0f} | {v['girdi']:.0f} | {v['sure']:.1f} | {v['maliyet']:.4f} |" for kol, v in ort.items()]
    satir += ["", "## Görev başına", "| görev | A başarı | B başarı | A kalite | B kalite | A çıktı | B çıktı |", "|---|---|---|---|---|---|---|"]
    satir += [f"| {g.stem} | {int(x[0]['basari'])}/{int(x[1]['basari'])} | {int(x[2]['basari'])} | {x[0]['kalite']:.2f}/{x[1]['kalite']:.2f} | {x[2]['kalite']:.2f} | "
              f"{x[0]['cikti']}/{x[1]['cikti']} | {x[2]['cikti']} |" for g, x in zip(gorevler, gor)]
    satir += ["", "## Karar", k, ""]
    (d / f"{ns.ad}-sonuc.md").write_text("\n".join(satir), encoding="utf-8")
    _kayit(kok, ns.ad, {"karar": k, "deneme": f"docs/denemeler/{ns.ad}-sonuc.md", "tarih": bugun})
    print("\n".join(satir[2:4] + satir[7:9] + [k]))
    return 0


def uret(ns, ctx):
    """18 K2 skill fabrikası: docs/uyarlamalar/<ad>.md → taslak (oturum modeli yazar; yoksa brief, rc 3) → denetim (tavan · tetik ·
    8-gram · KAYNAK.md; hata rc 2, dene koşmaz) → docs/denemeler/<ad>.md → dene (kalite kapısı) → bekleyen + zip ya da bilgi kartı."""
    from . import ogren as og, uygula as uy  # uygula kur'u içe aktarır: döngü yalnız çağrı anında
    kok = _kok(ctx)
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
    if rc := dene(ns, ctx):
        return rc
    k = tr.bolum((d / f"{ns.ad}-sonuc.md").read_text(encoding="utf-8"), "Karar").strip()
    b = kok / "docs" / "kurulumlar" / "bekleyen" / f"{ns.ad}.md"
    if not k.startswith("KUR"):
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
