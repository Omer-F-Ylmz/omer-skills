"""jev skill: istemi aktif skill'lere hiyerarşik sınıflar (istem başına 2 istek). İpucu verir, karar vermez.

Aday listesi köprünün katalogTopla'sının (tools/cc-kopru/hook.mjs) skill kısmının portu + synced (anthropic-skills:<ad>).
"""
import json
import math
import os
import re
import statistics
import time
from datetime import date
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
ASAMA1 = "Kullanıcının istemi (state) aşağıdaki Claude Code skill'lerinden hangisinin işi? Hiçbiri uymuyorsa 'hiçbiri'."
ASAMA2 = "Kullanıcının istemi (state) `{ad}` skill'inin işi mi? Skill'in açıklaması criteria.true içinde."


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


def _yollar(cl):
    ayar = _json(cl / "settings.json") or {}
    kapali = {k for k, v in (ayar.get("skillOverrides") or {}).items() if v == "off"}
    acik = {k.split("@")[0] for k, v in (ayar.get("enabledPlugins") or {}).items() if v is True}
    sd = cl / "skills"
    out = [(s.parent.name, s) for s in sd.glob("*/SKILL.md") if not {s.parent.name, ":" + s.parent.name} & kapali]
    out += [(f"anthropic-skills:{s.parent.name}", s) for s in sd.glob("synced/*/*/SKILL.md")
            if not {s.parent.name, f"anthropic-skills:{s.parent.name}"} & kapali]
    kok = cl / "plugins" / "cache"
    for p in (x for sahip in (kok.iterdir() if kok.is_dir() else []) if sahip.is_dir() for x in sahip.iterdir()):
        if p.name not in acik or not p.is_dir():
            continue
        k = next((k for k in [p, *sorted(p.iterdir())] if k.is_dir()
                  and any((k / x).exists() for x in ("commands", "agents", "skills", "plugin.json"))), None)
        if k:
            out += [(f"{p.name}:{s.parent.name}", s) for s in (k / "skills").glob("*/SKILL.md")
                    if not {s.parent.name, f"{p.name}:{s.parent.name}"} & kapali]
    return out


def adaylar(ev=None):
    """Aktif skill'ler [(ad, açıklama)], ada göre sıralı. Açıklama önbellekte; SKILL.md mtime'ı değişince yeniden okunur."""
    ev = Path(ev) if ev else Path.home()
    yol = ev / ".config" / "jev" / "skill_onbellek.json"
    eski, yeni = _json(yol) or {}, {}
    out = {}
    for ad, md in _yollar(ev / ".claude"):
        m = md.stat().st_mtime_ns
        k = str(md)
        yeni[k] = eski[k] if k in eski and eski[k][0] == m else [m, aciklama_oku(md)]
        out[ad] = yeni[k][1]
    if yeni != eski:
        yol.parent.mkdir(parents=True, exist_ok=True)
        yol.write_text(json.dumps(yeni, ensure_ascii=False), encoding="utf-8")
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


def yonlendir(istem, t, b, aday):
    """Aşama 1 (dilim başına choice, tek istek) → ≤10 aday; aşama 2 (aday başına noul, tek istek) → p≥act, ilk 5."""
    istem = istem.encode()[:ISTEM_BAYT].decode(errors="ignore")
    sorular = {f"d{i}": soru1(d) for i, d in enumerate(dilimle(aday))}
    if c.token(istem) + c.token(json.dumps(sorular, ensure_ascii=False)) >= ISTEK_TOKEN:
        raise c.JevHata("aşama 1 isteği 60k token sınırını aşıyor")
    cv = t.yargila([istem], sorular)[0]
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
    cv2 = t.yargila([istem], s2)[0] or {}
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


def hook(girdi, env, ev=None, gonder=None, bugun=None, aday=None, saat=time.monotonic):
    """UserPromptSubmit: fail-open. Kapı → günlük tavan → 2 istek (2 sn) → Act varsa ilk 3 ad. Her hata: boş çıktı."""
    try:
        bitis = saat() + HOOK_SN
        if env.get("JEV_SKILL_HOOK") != "1":
            return ""
        istem = (json.loads(girdi or "{}").get("prompt") or "").strip()
        ev = Path(ev) if ev else Path.home()
        if not istem or not _gunluk_al(ev / ".config" / "jev" / "gunluk.json", int(env.get("JEV_SKILL_GUNLUK") or 200),
                                       bugun or date.today().isoformat()):
            return ""

        def zamanli(url, basliklar, govde):
            kalan = bitis - saat()
            if kalan <= 0:
                raise TimeoutError
            return c.http_gonder(url, basliklar, govde, timeout=kalan)

        t = c.Tasiyici(env=env, en_fazla=2, istek_tavan=2, tekrar=0, gonder=gonder or zamanli, uyu=lambda s: None)
        _, sonuc = yonlendir(istem, t, _bantlar(ev), adaylar(ev) if aday is None else aday)
        if not sonuc:
            return ""
        ek = "Jev skill önerisi: " + ", ".join(s["ad"] for s in sonuc[:3])
        return json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": ek}}, ensure_ascii=False)
    except BaseException:
        return ""


def olc(ns, t, b):
    """K3: skill_route.jsonl üzerinde aşama-1 isabeti, hit@1/3, gecikme, token, maliyet → docs. Ücretli: istem başına 2 istek."""
    t.tekrar, t.en_fazla = 0, ns.istek_tavan
    satirlar = [json.loads(s) for s in Path(ns.veri).read_text(encoding="utf-8").splitlines() if s.strip()]
    aday = adaylar()
    ol = []
    for s in satirlar:
        k, t0 = len(t.kullanim), time.perf_counter()
        try:
            ilk, sonuc = yonlendir(s["istem"], t, b, aday)
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
            (f"günlük üst sınır ({gunluk} istem × ort.)", f"${ust:.2f}"), ("HTTP isteği", t.istek)]
    md = [f"# Jev skill yönlendirme A/B ({date.today().isoformat()}, {t.model})", "",
          f"Veri `{Path(ns.veri).name}`: {n} sentetik istem, her birine 1-3 kabul edilebilir altın skill. "
          "hit@k enjekte edilecek listede ölçülür (p ≥ act, p'ye göre sıralı).", "",
          "| ölçü | değer |", "|---|---|", *[f"| {a} | {v} |" for a, v in olcu], "",
          "Karar kuralı: hit@3 ≥ 0.80 VE p95 ≤ 1.8 sn VE günlük üst sınır ≤ $0.50.", "", karar, ""]
    Path(ns.cikti).parent.mkdir(parents=True, exist_ok=True)
    Path(ns.cikti).write_text("\n".join(md), encoding="utf-8")
    return ["ölçü", "değer"], [list(x) for x in olcu] + [["karar", karar.strip("*")]]
