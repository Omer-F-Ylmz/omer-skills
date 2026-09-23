"""jev — context dışı yargıç. Ajan dosya YOLU verir; jev okur, parçalar, redakte eder, yargılatır, ≤25 satır tablo döner.
Jev işaretler, karar vermez: KABUL/DUR ve kod doğruluğu ajanda kalır."""
import argparse
import json
import math
import os
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

from . import cekirdek as c
from . import skill as sk

VERI = Path(__file__).resolve().parents[1] / "tests" / "veri" / "jev_kalibre.jsonl"
KANIT_TOKEN = 28_000
SINIF = {
    "regresyon": "Son kod değişikliği davranışı bozdu; test haklı.",
    "flaky": "Zamanlama, sıra, paralellik ya da ağ kaynaklı kararsızlık; tekrar koşunca geçebilir.",
    "ortam-kurulum": "Eksik paket, bağlantı, yapılandırma, izin ya da makine farkı.",
    "derleme": "Kod derlenmiyor ya da tip hatası; test hiç koşmadı.",
    "test-kendisi": "Testin beklentisi ya da kurgusu yanlış veya eskimiş.",
}
NIYET = {
    "kargo": "Gönderi, teslimat, takip numarası, gecikme, kurye.",
    "iade": "Ürünü geri gönderme, değişim, iade süreci.",
    "ödeme": "Ödeme, fatura, çekim, taksit, ücret, para iadesinin hesaba geçmesi.",
    "ürün": "Ürün özelliği, stok, beden, renk, kalite, kullanım sorusu.",
    "diğer": "Yukarıdakilerin dışında (hesap, öneri, teşekkür, genel şikâyet).",
}


def _oku(yol):
    return Path(yol).read_text(encoding="utf-8", errors="replace")


def _p(x):
    return f"{x:.2f}"


def log(ns, tas, b):
    from . import ayristir as a
    hatalar = a.log_hatalari(_oku(ns.dosya))
    if not hatalar:
        return "hata bulunmadı (Jev çağrılmadı)"
    q = {"sinif": {"type": "choice", "instructions": "Bu test/derleme hatasının kök sebebi hangi sınıfa girer?", "criteria": SINIF}}
    if ns.diff:
        q["ilgili"] = {"type": "noul", "instructions": "Hata şu dosyalardaki değişiklikle ilgili mi: " + ns.diff}
    satirlar = []
    for h, cv in zip(hatalar, tas().yargila([f"{h['ad']}\n{h['metin']}" for h in hatalar], q)):
        if cv is None:
            satirlar.append((2, [h["ad"], "yanıt yok", "Escalate", "-"]))
            continue
        bt = c.bant(c.kesinlik(cv["sinif"]), b)
        oncelik = (cv["sinif"]["choice"] == "regresyon") + (bt == "Escalate")
        satirlar.append((oncelik, [h["ad"], cv["sinif"]["choice"], bt, _p(cv["ilgili"]["noul"]) if "ilgili" in cv else "-"]))
    satirlar.sort(key=lambda x: -x[0])
    return ["test", "sınıf", "bant", "diff ilgili p"], [r for _, r in satirlar]


def ilgili(ns, tas, b):
    from . import ayristir as a
    parcalar = []
    for yol in ns.yollar:
        metin = _oku(yol)
        sat = metin.splitlines()
        parcalar += [(f"{yol}:{x}-{y}", "\n".join(sat[x - 1:y])) for x, y in a.parcala_dosya(yol, metin)]
    q = {"alaka": {"type": "score", "instructions": f"Bu kod parçası şu soruyu cevaplamak için ne kadar ilgili: {c.redakte(ns.soru)}",
                   "criteria": ["ilgisiz", "dolaylı", "ilgili", "doğrudan cevap"]}}
    cevaplar = tas().yargila([f"{ad}\n{m}" for ad, m in parcalar], q)
    sirali = sorted(zip(parcalar, cevaplar), key=lambda x: -(x[1]["alaka"]["score"] if x[1] else -1))[:ns.k]
    return ["yol:satır", "alaka (0-3)", "bant"], [
        [ad, _p(cv["alaka"]["score"]), c.bant(c.kesinlik(cv["alaka"]), b)] if cv else [ad, "-", "Escalate"] for (ad, _), cv in sirali]


def kanit(ns, tas, b):
    from . import ayristir as a
    iddialar = a.iddialar(_oku(ns.rapor))
    parcalar = c.bol_state("\n\n".join(f"### {y}\n{_oku(y)}" for y in ns.kanitlar), ust=KANIT_TOKEN)
    t, satirlar = tas(), []
    # Her kanıt parçası bir state, her iddia bir noul sorusu; iddia başına p = parçalar arası max.
    for grup in c.parcala(iddialar, 20):
        q = {f"i{n}": {"type": "noul", "instructions": f"Bu iddia state'teki KANIT tarafından destekleniyor mu? İddia: {c.redakte(i)}"} for n, i in grup}
        cevaplar = [cv for cv in t.yargila(parcalar, q) if cv]
        for n, i in grup:
            y = max((cv[f"i{n}"] for cv in cevaplar), key=lambda x: x["noul"], default=None)
            bt = c.bant(c.kesinlik(y), b) if y else "Escalate"
            if y is None or y["noul"] < 0.5 or bt == "Escalate":
                satirlar.append([n, i[:60], _p(y["noul"]) if y else "-", bt])
    if not satirlar:
        return f"{len(iddialar)} iddianın hepsi destekli (Act/Flag)"
    return ["satır", "iddia", "destek p", "bant"], satirlar


def triage(ns, tas, b):
    from . import ayristir as a
    bl = a.bulgular(json.loads(_oku(ns.dosya)))
    if not bl:
        return "bulgu yok (Jev çağrılmadı)"
    q = {
        "gercek": {"type": "noul", "instructions": "Bu bulgu gerçek bir risk mi (yanlış alarm değil)?"},
        "sinif": {"type": "choice", "instructions": "Bulgu hangi sınıfa girer?", "criteria": {
            "güvenlik": "Sömürülebilir açık, sızıntı, yetki sorunu.",
            "kalite": "Bakım, erişilebilirlik ya da stil sorunu; güvenlik değil.",
            "yanlış-alarm": "Bağlamda sorun değil (test verisi, örnek, bilinçli istisna)."}},
        "onem": {"type": "score", "instructions": "Bulgunun önemi", "criteria": ["düşük", "orta", "yüksek", "kritik"]},
    }
    satirlar = []
    for x, cv in zip(bl, tas().yargila([x["state"] for x in bl], q)):
        yer = f"{x['dosya']}:{x['satir']}" if x["satir"] is not None else x["dosya"]
        if cv is None:
            satirlar.append((9, [x["kural"], yer, "yanıt yok", "-", "-", "Escalate"]))
            continue
        k = min(c.kesinlik(cv["gercek"]), c.kesinlik(cv["sinif"]))
        satirlar.append((cv["onem"]["score"], [x["kural"], yer, cv["sinif"]["choice"], _p(cv["gercek"]["noul"]), _p(cv["onem"]["score"]), c.bant(k, b)]))
    satirlar.sort(key=lambda x: -x[0])
    return ["kural", "yer", "sınıf", "gerçek p", "önem (0-3)", "bant"], [r for _, r in satirlar]


def _kurulu_adlar():
    ev = Path.home() / ".claude"
    adlar = sorted(p.name for p in (ev / "skills").glob("*") if p.is_dir()) if (ev / "skills").is_dir() else []
    try:
        adlar += sorted(json.loads((ev / "plugins" / "installed_plugins.json").read_text(encoding="utf-8")).get("plugins", {}))
    except (OSError, ValueError):
        pass
    return adlar


def _bakim(tarih):
    try:
        gun = (datetime.now(timezone.utc) - datetime.fromisoformat(str(tarih).replace("Z", "+00:00")).astimezone(timezone.utc)).days
    except ValueError:
        return 0.0
    return 1.0 if gun <= 90 else 0.5 if gun <= 365 else 0.0


def tarama(ns, tas, b):
    adaylar = json.loads(_oku(ns.dosya))
    kurulu = ", ".join(_kurulu_adlar())
    q = {"cift": {"type": "noul", "instructions": "Bu aday, KURULU listesindeki bir skill/plugin ile işlevce çift mi?"},
         "risk": {"type": "score", "instructions": "Adayın istediği izin kapsamının riski", "criteria": ["yok", "dar", "orta", "geniş"]}}
    states = [f"ADAY: {x.get('ad')}\n{x.get('aciklama', '')}\nİzinler: {x.get('izinler', '?')}\n\nKURULU: {kurulu}" for x in adaylar]
    satirlar = []
    for x, cv in zip(adaylar, tas().yargila(states, q)):
        bakim = _bakim(x.get("son_commit"))
        yildiz = min(1.0, math.log10(int(x.get("yildiz") or 0) + 1) / 4)
        if cv is None:
            satirlar.append([x.get("ad"), "-", "-", bakim, _p(yildiz), "-"])
            continue
        cift, risk = cv["cift"]["noul"], cv["risk"]["score"] / 3
        puan = 0.35 * (1 - cift) + 0.35 * (1 - risk) + 0.15 * bakim + 0.15 * yildiz
        satirlar.append([x.get("ad"), _p(cift), _p(cv["risk"]["score"]), bakim, _p(yildiz), _p(puan)])
    satirlar.sort(key=lambda r: r[5], reverse=True)  # yalnız sıralama, eleme yok
    return ["aday", "çift p", "izin riski (0-3)", "bakım", "yıldız", "puan"], satirlar


def _esik(yargilar, hedef, destek=5):
    """Kesinliği ≥t olanlarda isabet ≥hedef veren en düşük t (en az `destek` örnekle); yoksa None."""
    for t in sorted({k for k, _ in yargilar}):
        ust = [d for k, d in yargilar if k >= t]
        if len(ust) >= destek and sum(ust) / len(ust) >= hedef:
            return round(t, 4)
    return None


def _olc(satirlar, cevaplar):
    yargilar, brier, doygun, doygun_sinir, isabet = [], [], [], [], 0
    for s, cv in zip(satirlar, cevaplar):
        if cv is None:
            continue
        n, ac = cv["niyet"], cv["acil"]
        isabet += n["choice"] == s["niyet"]
        brier.append((ac["noul"] - s["acil"]) ** 2)
        for k, d in ((c.kesinlik(n), n["choice"] == s["niyet"]), (c.kesinlik(ac), (ac["noul"] >= 0.5) == s["acil"])):
            yargilar.append((k, d))
            doygun.append(k >= 0.999)
            if s["sinir"]:
                doygun_sinir.append(k >= 0.999)
    bantlar = {}
    for ad in ("Act", "Flag", "Escalate"):
        ds = [d for k, d in yargilar if c.bant(k, c.VARSAYILAN_BANT) == ad]
        bantlar[ad] = (len(ds), sum(ds) / len(ds) if ds else None)
    oran = lambda xs: sum(xs) / len(xs) if xs else 0.0
    return {"isabet": isabet / len(satirlar), "brier": oran(brier), "doygunluk": oran(doygun), "doygunluk_sinir": oran(doygun_sinir),
            "act": _esik(yargilar, 0.95), "flag": _esik(yargilar, 0.80), "bantlar": bantlar, "yanitsiz": sum(cv is None for cv in cevaplar)}


def kalibre(ns, tas, b):
    satirlar = [json.loads(s) for s in _oku(ns.veri).splitlines() if s.strip()]
    q = {"niyet": {"type": "choice", "instructions": "Müşteri mesajının ana niyeti hangisi?", "criteria": NIYET},
         "acil": {"type": "noul", "instructions": "Mesaj aynı gün müdahale gerektirecek kadar acil mi?"}}
    t, olc = tas(), {}
    for m in c.MODELLER:
        t.model = m
        olc[m] = _olc(satirlar, t.yargila([s["mesaj"] for s in satirlar], q))
    oneri = max(c.MODELLER, key=lambda m: (olc[m]["isabet"], -olc[m]["brier"], m == "jev-1.13"))
    o, taban = olc[oneri], c.VARSAYILAN_BANT
    act = max(o["act"] or 0, taban["act"])  # taban: öneri 0.85/0.60'ın altına indiremez
    flag = min(max(o["flag"] or 0, taban["flag"]), act)
    n, ns_ = len(satirlar), sum(s["sinir"] for s in satirlar)
    md = [f"# Jev kalibrasyonu — {date.today().isoformat()}", "",
          f"Veri: {Path(ns.veri).name} · n={n} sentetik Türkçe mesaj ({ns_} sınır durum) · model başına 1 batch. "
          f"Kesinlik: choice `confidence`, noul `max(p, 1-p)`; niyet + acil yargıları birlikte ({2 * n} yargı/model).", "",
          "| model | niyet isabeti | acil Brier | doygunluk (≥0.999) | doygunluk sınır | Act önerisi (≥0.95) | Flag önerisi (≥0.80) | yanıtsız |",
          "|---|---|---|---|---|---|---|---|"]
    for m in c.MODELLER:
        x = olc[m]
        md.append(f"| {m} | {_p(x['isabet'])} | {x['brier']:.3f} | {_p(x['doygunluk'])} | {_p(x['doygunluk_sinir'])} | {x['act']} | {x['flag']} | {x['yanitsiz']} |")
    md += ["", "Varsayılan bantlarla (0.85/0.60) bant başına isabet:", "", "| model | Act n · isabet | Flag n · isabet | Escalate n · isabet |", "|---|---|---|---|"]
    for m in c.MODELLER:
        md.append(f"| {m} | " + " | ".join(f"{k} · {_p(v) if v is not None else '-'}" for k, v in olc[m]["bantlar"].values()) + " |")
    md += ["", f"**Önerilen model:** {oneri} (isabet, sonra Brier; eşitlikte pinli jev-1.13).",
           (f"**Yazılan bantlar (--bant-yaz):** act={act} · flag={flag} → `~/.config/jev/bantlar.json` (yazılan = max(öneri, 0.85/0.60); en az 5 örnek desteği)."
            if ns.bant_yaz else "**bantlar.json değişmedi:** öneri yalnız rapora girer; yazmak için `--bant-yaz` (yazılan = max(öneri, 0.85/0.60))."),
           f"Çağrı: {t.cagri} batch · {t.istek} HTTP istek.",
           "", f"Not: n={n}. Eşikler kaba; güven aralığı geniş. Doygunluk yüksekse kesinlik ayırt edici değildir, bant yerine sınıf/p'ye bakılır."]
    Path(ns.cikti).parent.mkdir(parents=True, exist_ok=True)
    Path(ns.cikti).write_text("\n".join(md) + "\n", encoding="utf-8")
    if ns.bant_yaz:
        c.BANT_YOLU.parent.mkdir(parents=True, exist_ok=True)
        c.BANT_YOLU.write_text(json.dumps({"act": act, "flag": flag, "model": oneri, "n": n, "tarih": date.today().isoformat(), "kaynak": "jev kalibre"}), encoding="utf-8")
    return ["model", "isabet", "Brier", "doygunluk", "Act", "Flag"], [
        [m, _p(olc[m]["isabet"]), f"{olc[m]['brier']:.3f}", _p(olc[m]["doygunluk"]), olc[m]["act"], olc[m]["flag"]] for m in c.MODELLER]


def skill(ns, tas, b):
    t = tas()
    t.tekrar = 0  # istem başına tam 2 HTTP isteği
    ns.asama = {}
    _, sonuc = sk.yonlendir(ns.istem, t, b, sk.adaylar(), ns.asama)
    return ["skill", "p", "bant"], [[x["ad"], _p(x["p"]), x["bant"]] for x in sonuc]


def hook_durum(ns, tas, b):
    yol = Path.home() / ".config" / "jev" / "hook.log"
    d = sk.hook_durum(yol.read_text(encoding="utf-8").splitlines()[-ns.n:] if yol.exists() else [])
    oran = d["sonuc"].get("zaman-aşımı", 0) / d["n"] if d["n"] else 0
    return ["ölçü", "değer"], [["satır", d["n"]], ["p50 ms", d["p50"]], ["p95 ms", d["p95"]], ["zaman-aşımı oranı", f"{oran:.0%}"],
                               *[[f"sonuç: {k}", v] for k, v in sorted(d["sonuc"].items())]]


KOMUT = {"log": log, "ilgili": ilgili, "kanit": kanit, "triage": triage, "tarama": tarama, "kalibre": kalibre,
         "skill": skill, "skill-olc": lambda ns, tas, b: sk.olc(ns, tas(), b), "hook-durum": hook_durum}


def main(argv=None, env=None, gonder=None, uyu=time.sleep, t0=None):
    p = argparse.ArgumentParser(prog="jev", description=__doc__)
    ortak = argparse.ArgumentParser(add_help=False)
    ortak.add_argument("--model", default="jev-1.13", choices=c.MODELLER, help="varsayılan pinli jev-1.13")
    ortak.add_argument("--en-fazla", type=int, default=5, metavar="N", help="en fazla N batch çağrısı; N+1. ağa çıkmadan hata (varsayılan 5)")
    ortak.add_argument("--istek-tavan", type=int, default=250, metavar="M", help="en fazla M HTTP isteği, tekrarlar dahil (varsayılan 250)")
    ortak.add_argument("--json", action="store_true", help="tablo yerine JSON")
    alt = p.add_subparsers(dest="komut", required=True)
    x = alt.add_parser("log", parents=[ortak], help="dotnet test (konsol/trx) · pytest çıktısındaki hataları sınıflar")
    x.add_argument("dosya")
    x.add_argument("--diff", help="virgüllü değişen dosya listesi")
    x = alt.add_parser("ilgili", parents=[ortak], help="dosyaları ≤80 satırlık parçalara böler, soruya en ilgili k aralığı döner")
    x.add_argument("soru")
    x.add_argument("yollar", nargs="+")
    x.add_argument("-k", type=int, default=5)
    x = alt.add_parser("kanit", parents=[ortak], help="rapordaki her iddia kanıt dosyalarınca destekleniyor mu")
    x.add_argument("rapor")
    x.add_argument("kanitlar", nargs="+")
    x = alt.add_parser("triage", parents=[ortak], help="semgrep · gitleaks · SARIF · SkillSpector · axe JSON bulgularını sınıflar")
    x.add_argument("dosya")
    x = alt.add_parser("tarama", parents=[ortak], help="aday skill/plugin listesini çift/izin/bakım ile sıralar (eleme yok)")
    x.add_argument("dosya")
    x = alt.add_parser("kalibre", parents=[ortak], help="40 sentetik mesajla 2 modeli ölçer, bantlar.json yazar (2 çağrı)")
    x.add_argument("--veri", default=str(VERI))
    x.add_argument("--cikti", default="docs/jev-kalibre.md")
    x.add_argument("--bant-yaz", action="store_true", help="öneriyi tabanla (max(öneri, 0.85/0.60)) bantlar.json'a yaz")
    x = alt.add_parser("skill", parents=[ortak], help="isteme uygun aktif skill'ler: 2 aşama, istem başına 2 istek; ilk 5 · p · bant (ipucu)")
    x.add_argument("istem")
    x = alt.add_parser("skill-olc", parents=[ortak], help="skill_route.jsonl ile aşama-1 isabeti, hit@1/3, gecikme, maliyet (ücretli)")
    x.add_argument("--veri", default=str(VERI.with_name("skill_route.jsonl")))
    x.add_argument("--cikti", default="docs/jev-skill-route.md")
    x = alt.add_parser("hook-durum", parents=[ortak], help="hook.log son N satırı: p50/p95 ms, sonuç dağılımı (ağ yok)")
    x.add_argument("-n", type=int, default=100)
    alt.add_parser("hook", help="UserPromptSubmit hook'u: stdin JSON; JEV_SKILL_HOOK=1 değilse ağa çıkmaz; her hatada sessiz exit 0")
    ns = p.parse_args(argv)
    env = os.environ if env is None else env
    if ns.komut == "hook":
        cikti = sk.hook(sys.stdin.read(), env, gonder=gonder, t0=t0)
        if cikti:
            print(cikti)
        return 0
    t = []  # komut başına tek taşıyıcı: sayaçlar çıktıya girer

    def tas():
        if not t:
            t.append(c.Tasiyici(env=env, en_fazla=ns.en_fazla, istek_tavan=ns.istek_tavan, model=ns.model, gonder=gonder, uyu=uyu))
        return t[0]

    try:
        b = None if ns.komut == "kalibre" else c.bantlar_oku()
        sonuc = KOMUT[ns.komut](ns, tas, b)
    except c.AnahtarYok as e:
        print(f"jev: {e}", file=sys.stderr)
        return 2
    except (c.JevHata, OSError, ValueError, KeyError, TypeError) as e:
        print(f"jev: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    cagri = {"batch": t[0].cagri, "istek": t[0].istek} if t else {"batch": 0, "istek": 0}
    asama = getattr(ns, "asama", None)
    if asama is not None:
        cagri["asama"] = {str(k): v for k, v in sorted(asama.items())}
    if ns.json:
        j = {"mesaj": sonuc} if isinstance(sonuc, str) else {"satirlar": [dict(zip(sonuc[0], r)) for r in sonuc[1]]}
        print(json.dumps({**j, "cagri": cagri}, ensure_ascii=False))
    else:
        print(sonuc if isinstance(sonuc, str) else c.tablo(*sonuc, ust=24))
        if asama is not None:
            tavan = t[0].en_fazla if t else ns.en_fazla
            print(" · ".join(f"aşama {k}: {v[0]} çağrı · {v[1]} istek" for k, v in sorted(asama.items()))
                  + f" (tavan {tavan} çağrı · {ns.istek_tavan} istek)")
        elif ns.komut != "hook-durum":
            print(f"çağrı: {cagri['batch']}/{ns.en_fazla} batch · {cagri['istek']}/{ns.istek_tavan} istek")
    return 0


def calistir(t0=None):
    for akis in (sys.stdout, sys.stderr):
        akis.reconfigure(encoding="utf-8")
    sys.exit(main(t0=t0))
