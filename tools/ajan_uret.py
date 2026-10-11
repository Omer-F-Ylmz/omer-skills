"""matris.json -> ajanlar/kalite3/<departman>/<ad>.md + gorevler.json + katalog-ek.tsv.

Kullanım: python tools/ajan_uret.py [matris.json] [cikti_dizin]
İhlalde (ad tekrarı/çakışma, puan != 10, bozuk regex, katalogda olmayan skill) rc=1, dosya yazılmaz.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
ANA_KATALOG = ("2e88ec2", "skills/ajan-getir/katalog.tsv")
MODELLER = {"haiku", "sonnet", "opus"}


def skill_kumesi(dizin):
    """docs/departmanlar/*.md tablolarında tür=skill satırlarının ilk sütunu."""
    kume = set()
    for f in Path(dizin).glob("*.md"):
        for s in f.read_text(encoding="utf-8", errors="replace").splitlines():
            h = [x.strip() for x in s.split("|")]
            if s.startswith("| ") and len(h) > 3 and h[2] == "skill":
                kume.add(h[1])
    return kume


def mevcut_adlar():
    """228 gizli ajan (main katalog.tsv) + ~/.claude/agents dosya adları, küçük harf."""
    adlar = set()
    r = subprocess.run(["git", "-C", str(KOK), "show", "%s:%s" % ANA_KATALOG], capture_output=True, text=True, encoding="utf-8")
    for s in r.stdout.splitlines()[1:]:
        adlar.add(s.split("\t")[0].strip().lower())
    for f in (Path.home() / ".claude/agents").glob("*.md"):
        adlar.add(f.stem.lower())
    return adlar


def dogrula(kayitlar, mevcut, skiller):
    hata, gorulen = [], set()
    for k in kayitlar:
        ad = k.get("ad", "?")
        if not re.fullmatch(r"[a-z][a-z0-9]*(-[a-z0-9]+)+", ad):
            hata.append(f"{ad}: ad kebab-case değil")
        if ad in gorulen:
            hata.append(f"{ad}: ad tekrar")
        gorulen.add(ad)
        if ad.lower() in mevcut:
            hata.append(f"{ad}: mevcut ajanla çakışıyor")
        if k.get("model") not in MODELLER:
            hata.append(f"{ad}: model geçersiz")
        a = k.get("aciklama", "")
        if not a or len(a) > 300 or "\n" in a or ": " in a:
            hata.append(f"{ad}: aciklama boş/>300/satır sonu/': ' içeriyor")
        if not k.get("araclar") or not 3 <= len(k.get("adimlar", [])) <= 6 or not 2 <= len(k.get("kurallar", [])) <= 4:
            hata.append(f"{ad}: araclar/adimlar(3-6)/kurallar(2-4) eksik")
        if len(k.get("skiller", [])) > 3:
            hata.append(f"{ad}: skill > 3")
        for s in k.get("skiller", []):
            if s not in skiller:
                hata.append(f"{ad}: skill katalogda yok: {s}")
        g = k.get("gorev", {})
        r = g.get("rubrik", [])
        if not g.get("istem") or not 4 <= len(r) <= 6:
            hata.append(f"{ad}: görev eksik")
        if sum(x["puan"] for x in r) != 10:
            hata.append(f"{ad}: rubrik puan toplamı {sum(x['puan'] for x in r)} != 10")
        for x in r:
            try:
                re.compile(x["regex"])
            except re.error as e:
                hata.append(f"{ad}: regex derlenmedi {x['regex']!r}: {e}")
    return hata


def govde(k):
    s = [f"Sen {k['departman']} ekibinin {k['uzmanlik']} uzmanısın."]
    if k["skiller"]:
        s.append("Önce yükle: " + ", ".join(k["skiller"]) + ".")
    s.append("Adımlar:")
    s += [f"{i}. {a}" for i, a in enumerate(k["adimlar"], 1)]
    s.append("Kurallar:")
    s += [f"- {a}" for a in k["kurallar"]]
    s.append("Çıktı: " + k["cikti"])
    return "\n".join(s)


def uret(matris, cikti, mevcut, skiller):
    kayitlar = json.loads(Path(matris).read_text(encoding="utf-8"))
    hata = dogrula(kayitlar, mevcut, skiller)
    if hata:
        return hata
    cikti = Path(cikti)
    tsv = ["ad\tmodel\ttek_satir\tyol"]
    for k in kayitlar:
        yol = cikti / k["departman"] / (k["ad"] + ".md")
        yol.parent.mkdir(parents=True, exist_ok=True)
        fm = f"---\nname: {k['ad']}\ndescription: {k['aciklama']}\nmodel: {k['model']}\ntools: {', '.join(k['araclar'])}\n---\n"
        yol.write_text(fm + govde(k) + "\n", encoding="utf-8", newline="\n")
        tsv.append("\t".join([k["ad"], k["model"], k["aciklama"].replace("\t", " "), f"ajanlar/kalite3/{k['departman']}/{k['ad']}.md"]))
    gorevler = [{"ajan": k["ad"], "model": k["model"], **k["gorev"]} for k in kayitlar]
    (cikti / "gorevler.json").write_text(json.dumps(gorevler, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    (cikti / "katalog-ek.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8", newline="\n")
    return []


def main(argv):
    matris = argv[1] if len(argv) > 1 else KOK / "ajanlar/kalite3/matris.json"
    cikti = argv[2] if len(argv) > 2 else KOK / "ajanlar/kalite3"
    hata = uret(matris, cikti, mevcut_adlar(), skill_kumesi(KOK / "docs/departmanlar"))
    for h in hata:
        print("HATA", h)
    print("rc=1" if hata else "tamam")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
