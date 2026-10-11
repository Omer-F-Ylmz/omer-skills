"""KALİTE-3 MODEL KURALI: alt ajan modeli ölçümü. Canlı ~/.claude/settings.json'daki CLAUDE_CODE_SUBAGENT_MODEL yalnız bu
koşunun oturumunda `--settings` env ile ezilir; değer yazdırılmaz, kanıt result.modelUsage'daki model adlarıdır.
Ana oturum haiku (alt ajan jetonu ayrı model anahtarında kalsın diye), ajan `--agents` ile verilir.
  python tools/model_olc.py dogrula        # ezme yok ↔ "" : frontmatter opus'lu ajan gerçekte hangi modelde koştu
  python tools/model_olc.py karsilastir    # her aileden ilk ajan × sonnet/opus → docs/kutuphane/olcum/kalite3-model.tsv"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from olcum import kosucu  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
AJAN = KOK / "ajanlar/kalite3"
TSV = KOK / "docs/kutuphane/olcum/kalite3-model.tsv"
ANA = "haiku"


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


def alt(mu):
    """(alt ajan model(ler)i, jetonu) — ana (haiku) anahtarı hariç."""
    d = {m: v for m, v in mu.items() if ANA not in m}
    return ",".join(sorted(d)) or "-", jeton(d)


def kos(ad, t, ezme, gorev):
    istem = f"Delegate this task to the {ad} subagent with the Agent tool, then return its answer verbatim.\n\n{gorev}"
    return kosucu.kos(istem, ek(ad, t, ezme), model=ANA, butce=1.5)


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
        # dogrula'da "" ezmesi frontmatter opus'u gerçekten koşturmadıysa --settings env ezmesi işlemiyor: 32 çağrı boşa gitmesin
        if not any(s.split("\t")[4:6] == ["bos", "claude-opus-5-5"] for s in TSV.read_text(encoding="utf-8").splitlines()):
            sys.exit("dogrula: '' ezmesiyle opus görülmedi — karsilastir koşulmadı")
        isler = []
        for aile in sorted(p for p in AJAN.iterdir() if p.is_dir()):
            ad = next(y.stem for y in sorted(aile.glob("*.md")) if y.stem in gorevler)
            isler += [(aile.name, ad, m, m) for m in ("sonnet", "opus")]
    for aile, ad, model, ezme in isler:
        g = gorevler[ad]
        _, t = tanim(AJAN / aile / f"{ad}.md", model)
        o = kos(ad, t, ezme, g["istem"])
        am, aj = alt(o.get("model") or {})
        satir(time.strftime("%H:%M"), kip, aile, ad, "yok" if ezme is None else (ezme or "bos"), am, kosucu.puanla(o["metin"], g["rubrik"]),
              round(o["usd"], 4), jeton(o.get("model") or {}), aj, o["sure"], sum(a == f"Agent:{ad}" for a in o["araclar"]))


if __name__ == "__main__":
    main(sys.argv[1])
