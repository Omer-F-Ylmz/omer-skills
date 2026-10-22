"""EGITIM-1 damitma: Opus oturum dokumlerinden (~/.claude/projects/<proje>/*.jsonl) is-yapma kalibi istatistigi + is turu basina
ornek cikarir -> .kos/kopru/ogret/damit.json. Dusunme bloklari dokumde bos (redacted); dusunme kalibi gorunen metinden (secenek/gerekce/risk
kelimeleri) olculur. Kullanim: python tools/ogret/damit.py [en_fazla_oturum=250]"""
import glob, json, os, re, statistics, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / ".kos/kopru/ogret/damit.json"
PROJE = Path.home() / ".claude/projects/C--Projeler-omer-skills"
DESEN = json.loads((KOK / "tools/tur_setleri.json").read_text(encoding="utf-8"))["desen"]
DOGRULA = re.compile(r"(?i)pytest|dotnet test|npm (run )?test|\btest\b|gitleaks|semgrep|lighthouse|playwright|kapi|kapı|\bcheck\b|denetle|ruff|tsc")
DUSUNME = re.compile(r"(?i)alternatif|seçenek|secenek|yerine|gerekçe|gerekce|risk|kör nokta|kor nokta|neden .* değil|trade-?off")
SISTEM = re.compile(r"^\s*(<system-reminder>|<command-|\[Request interrupted|Caveat:)")


def tur_bul(metin):
    for ad, d in DESEN.items():
        if re.search(d, metin[:1500]):
            return ad
    return "diger"


def metin_al(icerik):
    if isinstance(icerik, str):
        return icerik
    return "\n".join(b.get("text", "") for b in icerik if isinstance(b, dict) and b.get("type") == "text")


def oturum(yol):
    model, ilk, araclar, son, dus, doğ_idx = Counter(), None, [], "", 0, []
    for satir in open(yol, encoding="utf-8", errors="replace"):
        if '"type":"assistant"' not in satir and '"type":"user"' not in satir:
            continue
        try:
            j = json.loads(satir)
        except ValueError:
            continue
        if j.get("isSidechain"):
            continue
        m = j.get("message", {})
        if j["type"] == "user":
            if ilk is None and not j.get("isMeta"):
                t = metin_al(m.get("content", "")).strip()
                if t and not SISTEM.match(t) and "tool_use_id" not in satir[:400]:
                    ilk = t
            continue
        model[m.get("model")] += 1
        for b in m.get("content", []):
            if b.get("type") == "tool_use":
                ad = b["name"]
                if ad == "Bash":
                    komut = str(b["input"].get("command", ""))
                    if DOGRULA.search(komut):
                        doğ_idx.append(len(araclar))
                    ad = "Bash:" + (komut.split() or ["?"])[0][:12]
                araclar.append(ad)
            elif b.get("type") == "text" and b["text"].strip():
                son = b["text"].strip()
                if DUSUNME.search(son):
                    dus += 1
    if not model or not ilk:
        return None
    return dict(model=model.most_common(1)[0][0], ilk=ilk, araclar=araclar, son=son, dus=dus, dogrulama=doğ_idx)


def evre(ad):
    if ad.startswith("Bash:") or ad == "PowerShell":
        return "Y"  # yurut/dogrula
    return {"Read": "O", "Grep": "O", "Glob": "O", "Edit": "W", "Write": "W", "Agent": "A", "Skill": "S"}.get(ad, "M")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 250
    dosyalar = sorted(glob.glob(str(PROJE / "*.jsonl")), key=os.path.getmtime, reverse=True)
    sonuc, okunan = [], 0
    for f in dosyalar:
        if okunan >= n * 3 or len(sonuc) >= n:
            break
        okunan += 1
        o = oturum(f)
        if o and "opus" in (o["model"] or "") and len(o["araclar"]) >= 15 and len(o["son"]) > 80:
            o["dosya"] = os.path.basename(f)
            sonuc.append(o)
    ist = {"oturum": len(sonuc), "model": dict(Counter(o["model"] for o in sonuc))}
    ist["arac_medyan"] = statistics.median(len(o["araclar"]) for o in sonuc)
    ist["dogrulamali_pay"] = round(sum(1 for o in sonuc if o["dogrulama"]) / len(sonuc), 2)
    ist["dogrulama_son_yari"] = round(sum(1 for o in sonuc if o["dogrulama"] and o["dogrulama"][-1] >= len(o["araclar"]) * 0.5) / len(sonuc), 2)
    ist["kapanis_once_dogrulama"] = round(sum(1 for o in sonuc if o["dogrulama"] and o["dogrulama"][-1] >= len(o["araclar"]) - 5) / len(sonuc), 2)
    ist["dusunme_metinli_pay"] = round(sum(1 for o in sonuc if o["dus"] >= 2) / len(sonuc), 2)
    ist["ilk_evre"] = dict(Counter("".join(evre(a) for a in o["araclar"][:4]) for o in sonuc).most_common(6))
    ist["evre_bigram"] = dict(Counter(e[i:i + 2] for o in sonuc for e in ["".join(evre(a) for a in o["araclar"])] for i in range(len(e) - 1)).most_common(8))
    ist["en_cok_arac"] = dict(Counter(a for o in sonuc for a in o["araclar"]).most_common(10))
    ornek = {}
    for o in sorted(sonuc, key=lambda o: abs(len(o["araclar"]) - 40)):
        t = tur_bul(o["ilk"])
        if o["dogrulama"] and o["dogrulama"][-1] >= len(o["araclar"]) - 8 and len(ornek.setdefault(t, [])) < 3:
            sira, onceki = [], None
            for a in o["araclar"]:
                a = re.sub(r"^mcp__", "", a)
                if a != onceki:
                    sira.append(a)
                onceki = a
            ornek[t].append(dict(istem=re.sub(r"\s+", " ", o["ilk"])[:300], sira=" > ".join(sira[:14]), kapanis=re.sub(r"\s+", " ", o["son"])[:450], dosya=o["dosya"]))
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    CIKTI.write_text(json.dumps(dict(ist=ist, ornek=ornek), ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(ist, ensure_ascii=False)[:1500])
    print({t: len(v) for t, v in ornek.items()})


if __name__ == "__main__":
    main()
