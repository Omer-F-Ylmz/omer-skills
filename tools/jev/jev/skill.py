"""jev skill: istemi aktif skill'lere hiyerarşik sınıflar (istem başına 2 istek). İpucu verir, karar vermez.

Aday listesi köprünün katalogTopla'sının (tools/cc-kopru/hook.mjs) skill kısmının portu + synced (anthropic-skills:<ad>).
"""
import json
import math
import os
import re
import statistics
import time
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from . import cekirdek as c

HICBIRI = "hiçbiri"
DILIM = 210
SORU_TOKEN = 30_000
ISTEK_TOKEN = 60_000
ISTEM_BAYT = 32_000  # ≈8k token
ACIKLAMA = 200
ESIK1, ILK1, ILK2 = 0.02, 10, 5
HOOK_SN = 2.0
LOG_SATIR = 500
ASAMA1 = "Kullanıcının istemi (state) aşağıdaki Claude Code skill'lerinden hangisinin işi? Hiçbiri uymuyorsa 'hiçbiri'."
ASAMA2 = "Kullanıcının istemi (state) `{ad}` skill'inin işi mi? Skill'in açıklaması criteria.true içinde."
HOOK_AYAR = ["Kayıt (`~/.claude/settings.json` → `hooks.UserPromptSubmit`); CC hook komutları Windows'ta bash ile koşar, yolda / kullan:", "",
             "```json", '{"hooks": [{"type": "command", "timeout": 3,',
             '  "command": "powershell -NoProfile -ExecutionPolicy Bypass -File C:/Users/pc/.claude/hooks/jev-skill.ps1"}]}', "```", ""]


def _json(yol):
    try:
        return json.loads(Path(yol).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def aciklama_oku(yol):
    """hook.mjs aciklamaOku portu: düz, tırnaklı, çok satırlı ve |/> blok description."""
    satirlar = Path(yol).read_text(encoding="utf-8", errors="replace")[:1500].splitlines()
    n = next((i for i, x in enumerate(satirlar) if re.match(r"description:\s*", x)), None)
    if n is None:
        s = next((x for x in satirlar if x.strip() and not re.match(r"(---|#|name:)", x.strip())), "")
    else:
        s = re.sub(r"^description:\s*", "", satirlar[n])
        devam = []
        for x in satirlar[n + 1:]:
            if not re.match(r"\s+\S", x):
                break
            devam.append(x.strip())
        g = re.fullmatch(r"([|>])[-+]?\d*", s.strip())
        if g:
            s = (devam[0] if devam else "") if g[1] == "|" else " ".join(devam)
        elif devam:
            s = " ".join([s.strip(), *devam])
    return s.strip().strip("\"'").strip()[:ACIKLAMA]


def _eski_kok(kd, ad):
    """installed_plugins.json'da yoksa: cache/*/<ad> altında bileşenli ilk klasör (sıralı)."""
    for sahip in sorted(kd.iterdir()) if kd.is_dir() else []:
        p = sahip / ad
        if p.is_dir():
            return next((k for k in [p, *sorted(p.iterdir())] if k.is_dir()
                         and any((k / x).exists() for x in ("commands", "agents", "skills", "plugin.json"))), None)
    return None


def _eklentiler(cl):
    """Açık plugin'ler [(ad, kök, skills|None)] — hook.mjs eklentiKokleri portu. Kök = installPath (CC'nin etkin sürümü);
    skills = marketplace girdisinin `skills` listesi (varsa yalnız onlar)."""
    ayar = _json(cl / "settings.json") or {}
    kurulu = (_json(cl / "plugins" / "installed_plugins.json") or {}).get("plugins") or {}
    out = []
    for anahtar, v in (ayar.get("enabledPlugins") or {}).items():
        if v is not True:
            continue
        ad, _, pazar = anahtar.partition("@")
        kok = next(iter(kurulu.get(anahtar) or []), {}).get("installPath")
        kok = Path(kok) if kok and Path(kok).is_dir() else _eski_kok(cl / "plugins" / "cache", ad)
        if kok is None:
            continue
        pz = _json(cl / "plugins" / "marketplaces" / pazar / ".claude-plugin" / "marketplace.json") or {}
        girdi = next((x for x in pz.get("plugins") or [] if x.get("name") == ad), {})
        out.append((ad, kok, girdi.get("skills") if isinstance(girdi.get("skills"), list) else None))
    return out


def _yollar(cl):
    """hook.mjs katalogTopla'nın skill kısmıyla aynı sıra ve süzgeç: yerel → plugin → synced."""
    ayar = _json(cl / "settings.json") or {}
    kapali = {k for k, v in (ayar.get("skillOverrides") or {}).items() if v == "off"}
    kaynaklar = [("", sorted((cl / "skills").glob("*")))]
    for p, kok, secili in _eklentiler(cl):
        kaynaklar.append((p, [kok / s for s in secili] if secili is not None else sorted((kok / "skills").glob("*"))))
    out, gorulen = [], set()
    for p, dizinler in kaynaklar:
        for d in dizinler:
            md = d / "SKILL.md"
            # çıplak ad override'ı yalnız yerel/synced'i kapatır; plugin skill'i `p:ad` ile (CC: canvas-design off, example-skills:canvas-design açık)
            if not md.is_file() or f"{p}:{d.name}" in kapali or (not p and d.name in kapali):
                continue
            gorulen.add(d.name)
            out.append((f"{p}:{d.name}" if p else d.name, md))
    for md in sorted((cl / "skills" / "synced").glob("*/*/SKILL.md")):
        ad = md.parent.name
        if ad in gorulen or {ad, f"anthropic-skills:{ad}"} & kapali:  # mükerrer kopya: yerel/plugin kazanır
            continue
        gorulen.add(ad)
        out.append((f"anthropic-skills:{ad}", md))
    return out


def _imza(cl):
    """Yapı imzası: ayar/kurulum/pazar dosyaları + skill klasörlerinin mtime'ı. Aynıysa klasör taraması yok."""
    yollar = [cl / "settings.json", cl / "plugins" / "installed_plugins.json", cl / "skills", cl / "skills" / "synced",
              *(cl / "skills" / "synced").glob("*"), *(cl / "plugins" / "marketplaces").glob("*/.claude-plugin/marketplace.json")]
    return {str(y): y.stat().st_mtime_ns if y.exists() else 0 for y in yollar}


def adaylar(ev=None):
    """Aktif skill'ler [(ad, açıklama)], ada göre sıralı. İmza aynıysa önbellekteki SKILL.md yolları kullanılır;
    açıklama SKILL.md mtime'ı değişince yeniden okunur."""
    # ponytail: installed_plugins.json değişmeden eklenen sürüm klasörünü imza görmez; görülürse imzaya cache/*/* ekle
    ev = Path(ev) if ev else Path.home()
    cl = ev / ".claude"
    yol = ev / ".config" / "jev" / "skill_onbellek.json"
    eski, imza = _json(yol) or {}, _imza(cl)
    onceki = eski.get("dosyalar") or {}
    liste = [(v[0], Path(k)) for k, v in onceki.items()] if eski.get("imza") == imza else _yollar(cl)
    yeni, out = {}, {}
    for ad, md in liste:
        try:
            m = md.stat().st_mtime_ns
        except OSError:
            continue
        v = onceki.get(str(md))
        yeni[str(md)] = v if v and v[0] == ad and v[1] == m else [ad, m, aciklama_oku(md)]
        out[ad] = yeni[str(md)][2]
    if yeni != onceki or eski.get("imza") != imza:
        yol.parent.mkdir(parents=True, exist_ok=True)
        yol.write_text(json.dumps({"imza": imza, "dosyalar": yeni}, ensure_ascii=False), encoding="utf-8")
    return sorted(out.items())


def soru1(dilim):
    return {"type": "choice", "instructions": ASAMA1,
            "criteria": {**{a: d or None for a, d in dilim}, HICBIRI: "Listedeki hiçbir skill bu istemin işi değil."}}


def dilimle(aday, n=DILIM, ust=SORU_TOKEN):
    """Ada göre sıralı listeyi dilimler: ≤n ad VE soru ≤ust token (bayt/4)."""
    taban = len(json.dumps(soru1([]), ensure_ascii=False).encode())
    out, cur, bayt = [], [], taban
    for a, d in aday:
        b = len(json.dumps({a: d}, ensure_ascii=False).encode())
        if cur and (len(cur) >= n or math.ceil((bayt + b) / 4) > ust):
            out.append(cur)
            cur, bayt = [], taban
        cur.append((a, d))
        bayt += b
    return out + [cur] if cur else out


def yonlendir(istem, t, b, aday, sayac=None):
    """Aşama 1 (dilim başına choice, tek istek) → ≤10 aday; aşama 2 (aday başına noul, tek istek) → p≥act, ilk 5.
    sayac: {aşama: [mantıksal çağrı, HTTP istek]} biriktirir."""
    sayac = {} if sayac is None else sayac

    def yargila(asama, sorular):
        c0, i0 = t.cagri, t.istek
        try:
            return t.yargila([istem], sorular)[0]
        finally:
            x = sayac.setdefault(asama, [0, 0])
            x[0], x[1] = x[0] + t.cagri - c0, x[1] + t.istek - i0

    istem = istem.encode()[:ISTEM_BAYT].decode(errors="ignore")
    sorular = {f"d{i}": soru1(d) for i, d in enumerate(dilimle(aday))}
    if c.token(istem) + c.token(json.dumps(sorular, ensure_ascii=False)) >= ISTEK_TOKEN:
        raise c.JevHata("aşama 1 isteği 60k token sınırını aşıyor")
    cv = yargila(1, sorular)
    if not isinstance(cv, dict):
        raise c.JevHata("aşama 1 yanıtsız")
    olas = {}
    for y in cv.values():
        for a, p in (y.get("probabilities") or {}).items():
            olas[a] = max(p, olas.get(a, 0.0))
    olas.pop(HICBIRI, None)
    ilk = [a for a, p in sorted(olas.items(), key=lambda x: (-x[1], x[0])) if p >= ESIK1][:ILK1]
    if not ilk:
        return [], []
    acik = dict(aday)
    s2 = {f"a{i}": {"type": "noul", "instructions": ASAMA2.format(ad=a),
                    "criteria": {"true": acik.get(a) or a, "false": "Bu skill'in işi değil."}} for i, a in enumerate(ilk)}
    cv2 = yargila(2, s2) or {}
    sonuc = [{"ad": a, "p": y["noul"], "bant": c.bant(c.kesinlik(y), b)}
             for i, a in enumerate(ilk) if (y := cv2.get(f"a{i}")) and y["noul"] >= b["act"]]
    return ilk, sorted(sonuc, key=lambda x: -x["p"])[:ILK2]


def _gunluk_al(yol, tavan, gun):
    """Günlük sayaç {gün: n}; başka gün = 0. Tavan doluysa False (ağa çıkılmaz)."""
    # ponytail: kilitsiz; eşzamanlı iki istem aynı sayıyı okuyabilir, tavan en fazla 1 kaçar
    n = (_json(yol) or {}).get(gun, 0)
    if n >= tavan:
        return False
    yol.parent.mkdir(parents=True, exist_ok=True)
    gecici = yol.with_suffix(".tmp")
    gecici.write_text(json.dumps({gun: n + 1}), encoding="utf-8")
    os.replace(gecici, yol)
    return True


def _bantlar(ev):
    v = _json(ev / ".config" / "jev" / "bantlar.json") or {}
    return {"act": float(v.get("act", c.VARSAYILAN_BANT["act"])), "flag": float(v.get("flag", c.VARSAYILAN_BANT["flag"]))}


def _hook_log(ev, ms, durum, n):
    """hook.log satırı: ISO zaman · ms · sonuç · aday sayısı. İstem, öneri adı, anahtar yazılmaz; son 500 satır kalır."""
    yol = ev / ".config" / "jev" / "hook.log"
    try:
        eski = yol.read_text(encoding="utf-8").splitlines() if yol.exists() else []
        yol.parent.mkdir(parents=True, exist_ok=True)
        satir = f"{datetime.now().astimezone().isoformat(timespec='seconds')} {ms} {durum} {n}"
        yol.write_text("\n".join([*eski, satir][-LOG_SATIR:]) + "\n", encoding="utf-8")
    except OSError:
        pass


def hook_durum(satirlar):
    """hook.log satırları → n, p50/p95 ms, sonuç dağılımı."""
    kayit = [s.split() for s in satirlar if len(s.split()) == 4]
    ms = sorted(int(k[1]) for k in kayit)
    n = len(ms)
    return {"n": n, "p50": statistics.median(ms) if n else 0, "p95": ms[math.ceil(0.95 * n) - 1] if n else 0,
            "sonuc": dict(Counter(k[2] for k in kayit))}


def hook(girdi, env, ev=None, gonder=None, bugun=None, aday=None, saat=time.monotonic, t0=None):
    """UserPromptSubmit: fail-open. Kapı → günlük tavan → 2 istek (t0'dan 2 sn) → Act varsa ilk 3 ad. Her hata: boş çıktı.
    t0 = süreç başı (__main__); her çağrı hook.log'a tek satır yazar."""
    t0 = saat() if t0 is None else t0
    bitis = t0 + HOOK_SN
    durum, n, cikti = "hata", 0, ""
    try:
        ev = Path(ev) if ev else Path.home()
        istem = (json.loads(girdi or "{}").get("prompt") or "").strip()
        if env.get("JEV_SKILL_HOOK") != "1" or not istem:
            durum = "sessiz-kapı"
        elif not _gunluk_al(ev / ".config" / "jev" / "gunluk.json", int(env.get("JEV_SKILL_GUNLUK") or 200),
                            bugun or date.today().isoformat()):
            durum = "sessiz-tavan"
        else:
            aday = adaylar(ev) if aday is None else aday
            n = len(aday)

            def zamanli(url, basliklar, govde):
                kalan = bitis - saat()
                if kalan <= 0:
                    raise TimeoutError
                return c.http_gonder(url, basliklar, govde, timeout=kalan)

            t = c.Tasiyici(env=env, en_fazla=2, istek_tavan=2, tekrar=0, gonder=gonder or zamanli, uyu=lambda s: None)
            _, sonuc = yonlendir(istem, t, _bantlar(ev), aday)
            durum = "öneri" if sonuc else "act-yok"
            if sonuc:
                ek = "Jev skill önerisi: " + ", ".join(s["ad"] for s in sonuc[:3])
                cikti = json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": ek}},
                                   ensure_ascii=False)
    except BaseException:
        durum = "zaman-aşımı" if saat() >= bitis else "hata"
    if isinstance(ev, Path):
        _hook_log(ev, round((saat() - t0) * 1000), durum, n)
    return cikti


def olc(ns, t, b):
    """K3: skill_route.jsonl üzerinde aşama-1 isabeti, hit@1/3, gecikme, token, maliyet → docs. Ücretli: istem başına 2 istek."""
    t.tekrar, t.en_fazla = 0, ns.istek_tavan
    satirlar = [json.loads(s) for s in Path(ns.veri).read_text(encoding="utf-8").splitlines() if s.strip()]
    aday = adaylar()
    ol, ns.asama = [], {}
    for s in satirlar:
        k, t0 = len(t.kullanim), time.perf_counter()
        try:
            ilk, sonuc = yonlendir(s["istem"], t, b, aday, ns.asama)
        except c.TavanHata:
            raise
        except c.JevHata:
            ilk, sonuc = [], []
        sure = time.perf_counter() - t0
        u = t.kullanim[k:]
        adlar = [x["ad"] for x in sonuc]
        ol.append({"a1": bool(set(s["altin"]) & set(ilk)), "h1": bool(set(s["altin"]) & set(adlar[:1])),
                   "h3": bool(set(s["altin"]) & set(adlar[:3])), "sure": sure,
                   "token": sum(x.get("prompt_tokens") or x.get("input_tokens") or 0 for x in u),
                   "maliyet": sum(float(x.get("cost") or 0) for x in u)})
    n = len(ol)
    oran = lambda ad: sum(x[ad] for x in ol) / n
    sureler = sorted(x["sure"] for x in ol)
    p50, p95 = statistics.median(sureler), sureler[math.ceil(0.95 * n) - 1]
    ort_token, ort_maliyet = sum(x["token"] for x in ol) / n, sum(x["maliyet"] for x in ol) / n
    gunluk = int(os.environ.get("JEV_SKILL_GUNLUK") or 200)
    ust = gunluk * ort_maliyet
    sebep = [m for m, kosul in (("hit@3 < 0.80", oran("h3") < 0.80), ("p95 > 1.8 sn", p95 > 1.8),
                                (f"günlük üst sınır ${ust:.2f} > $0.50 (maliyet)", ust > 0.50)) if kosul]
    karar = "**JEV_SKILL_HOOK=1 önerilir.**" if not sebep else "**Hook kurulu, kapalı kalır:** " + "; ".join(sebep) + "."
    olcu = [("istem", n), ("aday (aktif skill)", len(aday)), ("aşama-1 isabeti (altın ∈ ilk 10)", f"{oran('a1'):.2f}"),
            ("hit@1", f"{oran('h1'):.2f}"), ("hit@3", f"{oran('h3'):.2f}"), ("gecikme p50 / p95 (sn)", f"{p50:.2f} / {p95:.2f}"),
            ("istem başına girdi token (ort.)", f"{ort_token:.0f}"), ("istem başına maliyet (ort.)", f"${ort_maliyet:.5f}"),
            (f"günlük üst sınır ({gunluk} istem × ort.)", f"${ust:.2f}"), *[(f"aşama {k} çağrı · HTTP istek", f"{v[0]} · {v[1]}") for k, v in sorted(ns.asama.items())]]
    md = [f"# Jev skill yönlendirme A/B ({date.today().isoformat()}, {t.model})", "",
          f"Veri `{Path(ns.veri).name}`: {n} sentetik istem, her birine 1-3 kabul edilebilir altın skill. "
          "hit@k enjekte edilecek listede ölçülür (p ≥ act, p'ye göre sıralı).", "",
          "| ölçü | değer |", "|---|---|", *[f"| {a} | {v} |" for a, v in olcu], "",
          "Karar kuralı: hit@3 ≥ 0.80 VE p95 ≤ 1.8 sn VE günlük üst sınır ≤ $0.50.", "", karar, "", *HOOK_AYAR]
    Path(ns.cikti).parent.mkdir(parents=True, exist_ok=True)
    Path(ns.cikti).write_text("\n".join(md), encoding="utf-8")
    return ["ölçü", "değer"], [list(x) for x in olcu] + [["karar", karar.strip("*")]]
