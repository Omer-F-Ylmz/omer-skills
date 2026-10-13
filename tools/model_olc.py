"""KALİTE-3 MODEL KURALI: alt ajan modeli ölçümü. Canlı ~/.claude/settings.json'daki CLAUDE_CODE_SUBAGENT_MODEL yalnız bu
koşunun oturumunda `--settings` env ile ezilir; değer yazdırılmaz, kanıt result.modelUsage'daki model adlarıdır.
Ana oturum haiku (alt ajan jetonu ayrı model anahtarında kalsın diye), ajan `--agents` ile verilir.
  python tools/model_olc.py dogrula        # ezme yok ↔ "" : frontmatter opus'lu ajan gerçekte hangi modelde koştu
  python tools/model_olc.py karsilastir    # her aileden ilk ajan × sonnet/opus → docs/kutuphane/olcum/kalite3-model.tsv
  python tools/model_olc.py pilot [N]      # departman sırasıyla (her turda her departmandan bir ajan): ajan kolu ↔ ana oturum kolu,
                                          # en fazla N çağrı → kalite3-ajan-pilot.tsv; yazılmış çiftler atlanır
  python tools/model_olc.py pilot N ES     # ES çift aynı anda (RAM < %95 beklenir)"""
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from olcum import kosucu  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
AJAN = KOK / "ajanlar/kalite3"
TSV = KOK / "docs/kutuphane/olcum/kalite3-model.tsv"
PILOT = KOK / "docs/kutuphane/olcum/kalite3-ajan-pilot.tsv"
YANIT = KOK / ".kalite3/ajan-yanit"
ANA = "haiku"
RAM_TAVAN = 95  # devam-12 EK (a): parti içi eşzamanlılıkta RAM ≤ %95


def tanim(yol, model):
    _, fm, govde = yol.read_text(encoding="utf-8").split("---", 2)
    f = dict(s.split(": ", 1) for s in fm.strip().splitlines() if ": " in s)
    return f["name"], {"description": f["description"], "prompt": govde.strip(), "model": model}


def ek(ad, t, ezme):
    """ezme None → canlı env aynen; aksi halde yalnız bu oturum için CLAUDE_CODE_SUBAGENT_MODEL=ezme."""
    e = ["--agents", json.dumps({ad: t}, ensure_ascii=False)]
    return e if ezme is None else e + ["--settings", json.dumps({"env": {"CLAUDE_CODE_SUBAGENT_MODEL": ezme}})]


def jeton(d):
    return sum(v.get(k, 0) for v in d.values() for k in ("inputTokens", "outputTokens", "cacheReadInputTokens", "cacheCreationInputTokens"))


def ana_model(model):
    """Delege eden oturumun modeli. Ajan haiku ise sonnet: aynı model anahtarında alt ajan jetonu/USD'si ayrılamıyor
    (r9: 3 haiku ajanında alt_model '-')."""
    return "sonnet" if model == "haiku" else ANA


def alt(mu, ana=ANA):
    """(alt ajan model(ler)i, jetonu) — ana oturum anahtarı hariç."""
    d = {m: v for m, v in mu.items() if ana not in m}
    return ",".join(sorted(d)) or "-", jeton(d)


def alt_usd(mu, ana=ANA):
    return round(sum(v.get("costUSD", 0) for m, v in mu.items() if ana not in m), 4)


def dene(*a, **k):
    """Boş yanıt puan 0 değil ölçüm hatasıdır: bir kez yeniden denenir, yine boşsa puan() 'hata' yazar."""
    o = kosucu.kos(*a, **k)
    return o if o["metin"].strip() else kosucu.kos(*a, **k)


def puan(o, rubrik):
    return kosucu.puanla(o["metin"], rubrik) if o["metin"].strip() else "hata"


def kos(ad, t, ezme, gorev):
    istem = f"Delegate this task to the {ad} subagent with the Agent tool, then return its answer verbatim.\n\n{gorev}"
    fm = [p.read_text(encoding="utf-8").split("---", 2)[1] for p in AJAN.glob(f"*/{ad}.md")]  # tools: → mcp_sec (OLCUM_MCP_HAFIF)
    return dene(istem, ek(ad, t, ezme), model=ana_model(t["model"]), butce=1.5, mcp=fm)


def ana(gorev, model):
    """Ana oturum kolu: görev ajansız, kurulu skill'lerle, ajanın modelinde."""
    return dene(gorev, [], model=model, butce=1.5)


def ram():
    """Ortak sıranın RAM ölçümü (yüzde); devam-13: parti içi her çift başlatmadan önce."""
    sys.path.insert(0, r"C:\Projeler\omer-skills\.kos\kopru")
    from olcum_sira import ram as r
    return r()


def pilot(en_fazla=48, es=1, atla=()):
    """Ajan modeli frontmatter'daki; canlı env ezmesin diye açık ezme verilir (dogrula 18:20: "" geri getirmiyor).
    es: aynı anda koşan çift sayısı (her başlatmadan önce RAM < RAM_TAVAN beklenir); atla: başka partide koşan ajanlar.
    Dönüş: bu çağrıda koşulan ajanlar."""
    sys.stdout.reconfigure(encoding="utf-8")
    gorevler = {g["ajan"]: g for g in json.loads((AJAN / "gorevler.json").read_text(encoding="utf-8"))}
    baslik = "aile\tajan\tkol\tpuan\tusd\tjeton\tana_jeton\talt_model\tsure\talt_usd\n"
    if not PILOT.exists():
        PILOT.write_text(baslik, encoding="utf-8", newline="\n")
    elif "alt_usd" not in PILOT.read_text(encoding="utf-8").split("\n", 1)[0]:  # r9 dosyası: sütun eklenir, eski satırlar boş
        PILOT.write_text(baslik + PILOT.read_text(encoding="utf-8").split("\n", 1)[1], encoding="utf-8", newline="\n")
    bitti = {tuple(s.split("\t")[1:3]) for s in PILOT.read_text(encoding="utf-8").splitlines()[1:]}
    YANIT.mkdir(parents=True, exist_ok=True)
    aileler = {a: [y.stem for y in sorted(a.glob("*.md")) if y.stem in gorevler] for a in sorted(p for p in AJAN.iterdir() if p.is_dir())}
    sira = [(a, ads[i]) for i in range(max(map(len, aileler.values()), default=0)) for a, ads in aileler.items() if i < len(ads)]
    secilen, cagri = [], 0
    for aile, ad in sira:
        if {(ad, "ajan"), (ad, "ana")} <= bitti or ad in atla:
            continue
        if cagri + 2 > en_fazla:
            break
        secilen.append((aile, ad))
        cagri += 2
    kilit = threading.Lock()

    def cift(aile, ad):
        g = gorevler[ad]
        _, t = tanim(aile / f"{ad}.md", g["model"])
        ana_m = ana_model(g["model"])
        for kol in ("ajan", "ana"):
            if (ad, kol) in bitti:
                continue
            o = kos(ad, t, g["model"], g["istem"]) if kol == "ajan" else ana(g["istem"], g["model"])
            mu = o.get("model") or {}
            am, aj = alt(mu, ana_m) if kol == "ajan" else (",".join(sorted(mu)) or "-", 0)
            au = alt_usd(mu, ana_m) if kol == "ajan" else ""
            (YANIT / f"{ad}-{kol}.md").write_text(o["metin"], encoding="utf-8", newline="\n")
            with kilit, PILOT.open("a", encoding="utf-8", newline="\n") as f:
                f.write("\t".join(map(str, [aile.name, ad, kol, puan(o, g["rubrik"]), round(o["usd"], 4),
                                            jeton(mu), jeton(mu) - aj, am, o["sure"], au])) + "\n")

    with ThreadPoolExecutor(es) as havuz:
        isler = []
        for aile, ad in secilen:
            while es > 1 and ram() >= RAM_TAVAN:
                time.sleep(30)
            isler.append(havuz.submit(cift, aile, ad))
            while es > 1 and sum(not i.done() for i in isler) >= es:  # yuva boşalınca RAM yeniden ölçülür
                time.sleep(1)
        for i in isler:
            i.result()
    return [ad for _, ad in secilen]


def satir(*a):
    print("\t".join(map(str, a)), flush=True)
    with TSV.open("a", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(map(str, a)) + "\n")


def main(kip):
    sys.stdout.reconfigure(encoding="utf-8")
    gorevler = {g["ajan"]: g for g in json.loads((AJAN / "gorevler.json").read_text(encoding="utf-8"))}
    if not TSV.exists():
        satir("tarih", "kip", "aile", "ajan", "kol", "alt_model", "puan", "usd", "jeton", "alt_jeton", "sure", "agent_cagri")
    if kip == "dogrula":
        isler = [("frontend", "fe-tasarim-yonu", "opus", ezme) for ezme in (None, "")]
    else:
        # Karsilastir açık ezme (sonnet/opus) kullanır; 18:20 dogrula: "" ezmesi frontmatter'ı geri getirmiyor (alt ajan ana modelde),
        # bu yüzden ön koşul yerine her satırda kanıt: alt model istenen değilse ezme işlemiyor → kalan çağrılar boşa gitmesin.
        isler = []
        for aile in sorted(p for p in AJAN.iterdir() if p.is_dir()):
            ad = next(y.stem for y in sorted(aile.glob("*.md")) if y.stem in gorevler)
            isler += [(aile.name, ad, m, m) for m in ("sonnet", "opus")]
    bitti = {tuple(s.split("\t")[1:5]) for s in TSV.read_text(encoding="utf-8").splitlines()[1:]}
    YANIT.mkdir(parents=True, exist_ok=True)
    for aile, ad, model, ezme in isler:
        kol = "yok" if ezme is None else (ezme or "bos")
        if kip == "karsilastir" and (kip, aile, ad, kol) in bitti:
            continue
        g = gorevler[ad]
        _, t = tanim(AJAN / aile / f"{ad}.md", model)
        o = kos(ad, t, ezme, g["istem"])
        (YANIT / f"{ad}-{kol}.md").write_text(o["metin"], encoding="utf-8", newline="\n")
        am, aj = alt(o.get("model") or {})
        satir(time.strftime("%H:%M"), kip, aile, ad, kol, am, puan(o, g["rubrik"]),
              round(o["usd"], 4), jeton(o.get("model") or {}), aj, o["sure"], sum(a == f"Agent:{ad}" for a in o["araclar"]))
        if kip == "karsilastir" and model not in am:
            sys.exit(f"{ad}: {model} ezmesi istendi, alt ajan modeli {am} — ezme işlemiyor, durdu")


if __name__ == "__main__":
    if sys.argv[1] == "pilot":
        pilot(*map(int, sys.argv[2:4]))
    else:
        main(sys.argv[1])
