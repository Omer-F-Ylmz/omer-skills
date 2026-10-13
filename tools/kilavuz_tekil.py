"""ENVANTER-4 m1: katalog kayıtlarını gövde sha'sıyla tekilleştirir, aileye bağlar → docs/katalog/tekil.tsv.

Aynı gövdeli kopyalar (claude.ai senkron, plugin içi aynı skill) tek temsilciye iner; derin okuma yalnız temsilciler için.
Kullanım: python tools/kilavuz_tekil.py   (özet satırları basar)
"""
import collections
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home() / ".claude"
KAT = KOK / "docs" / "katalog"
ON_EK = re.compile(r"^---\s*\n.*?\n---\s*\n?", re.S)
ADI = re.compile(r"^name:\s*['\"]?(.+?)['\"]?\s*$", re.M)


def govde(metin):
    """Frontmatter'sız, boşluğu sadeleşmiş gövde — sha bunun üstünden."""
    return " ".join(ON_EK.sub("", metin, count=1).split())


assert govde("---\nname: a\n---\n x  y\n") == "x y"


def oku(p):
    return p.read_text(encoding="utf8", errors="ignore")


def yollar():
    """(tür, ad) → dosya yolu. Plugin skill anahtarı 'plugin:skill'."""
    d = {}
    for kok in (KOK / "skills", EV / "skills"):
        for md in kok.glob("*/SKILL.md"):
            d.setdefault(("skill", md.parent.name), md)
    for md in [*(EV / "skills" / "synced").glob("*/*/SKILL.md"), *(EV / "plugins" / "synced").glob("**/SKILL.md")]:
        d.setdefault(("synced", md.parent.name), md)
    ip = json.loads(oku(EV / "plugins" / "installed_plugins.json")).get("plugins") or {}
    for anahtar, kayitlar in ip.items():
        yol = Path(kayitlar[0]["installPath"])
        ad = anahtar.split("@")[0]
        d[("plugin", ad)] = yol
        for md in yol.glob("**/skills/*/SKILL.md"):
            d.setdefault(("skill", f"{ad}:{md.parent.name}"), md)
        for md in yol.glob("**/agents/*.md"):
            m = ADI.search(oku(md)[:600])
            d.setdefault(("ajan", m.group(1) if m else md.stem), md)
    for kok in (KOK / ".claude" / "agents", EV / "agents"):
        for md in kok.glob("**/*.md"):
            m = ADI.search(oku(md)[:600])
            d.setdefault(("ajan", m.group(1) if m else md.stem), md)
            d.setdefault(("ajan", md.stem), md)
    return d


def aile(r, yol):
    k, ad, tur = r["kaynak"], r["ad"], r["tur"]
    if "@" in k:
        return k.split("@", 1)[1]  # pazar yeri = sahip/paket
    if tur == "ajan":
        return ad.split("-")[0] if re.fullmatch(r"[a-z0-9]+-[a-z0-9-]+", ad) else "agency-agents"
    if tur == "skill" and yol and KOK in yol.parents:
        return "omer-skills"
    if tur == "skill":
        return ad.split("-")[0]
    return {"arac": "omer-araclar", "kutuphane": "omer-kutuphaneler"}.get(tur, tur)


def main():
    R = [json.loads(s) for s in open(KAT / "yetenek.jsonl", encoding="utf8")]
    Y = yollar()
    satir, cozulmeyen = [], collections.Counter()
    for r in R:
        tur, ad = r["tur"], r["ad"]
        yol = Y.get((tur, ad)) or (Y.get(("synced", ad)) if r["kaynak"] == "claude.ai senkron" else None)
        if tur == "plugin":
            yol = Y.get(("plugin", ad))
        if yol and yol.is_file():
            g = govde(oku(yol))
        else:
            if tur in ("skill", "ajan"):
                cozulmeyen[tur] += 1
            g = f"{tur}|{ad}|{r['metin']}"  # dosyasız kayıt: kendi metni tekil
        satir.append({"ad": ad, "tur": tur, "aile": aile(r, yol), "sha": hashlib.sha1(g.encode()).hexdigest()[:12],
                      "yol": str(yol or ""), "bayt": len(g.encode())})
    # senkron kopya kendi ailesini plugin/yerel eşinden alır; aile içi küçük önekler 'yerel-diger'e
    grup = collections.defaultdict(list)
    for s in satir:
        grup[s["sha"]].append(s)
    for uyeler in grup.values():
        sahip = next((u["aile"] for u in uyeler if u["tur"] != "skill" or "@" in u["aile"] or ":" in u["ad"]), None)
        temsil = min(uyeler, key=lambda u: (":" not in u["ad"], len(u["ad"])))["ad"]
        for u in uyeler:
            u["temsilci"] = temsil
            if sahip and u["tur"] == "skill" and ":" not in u["ad"]:
                u["aile"] = sahip
    say = collections.Counter(s["aile"] for s in satir)
    for s in satir:
        if s["tur"] == "skill" and say[s["aile"]] < 3:
            s["aile"] = "yerel-diger"
    alan = ["ad", "tur", "aile", "sha", "temsilci", "bayt", "yol"]
    with open(KAT / "tekil.tsv", "w", encoding="utf8", newline="") as f:
        w = csv.DictWriter(f, alan, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(sorted(satir, key=lambda s: (s["aile"], s["ad"])))
    tekil = {s["sha"]: s for s in satir}
    print(f"kayit {len(satir)} · benzersiz {len(tekil)} · kopya grubu {sum(len(u) > 1 for u in grup.values())} · cozulmeyen {dict(cozulmeyen)}")
    print("benzersiz/tur", dict(collections.Counter(s["tur"] for s in tekil.values())))
    aileler = collections.Counter(s["aile"] for s in tekil.values())
    print(f"aile {len(aileler)}:", ", ".join(f"{a}={n}" for a, n in aileler.most_common(40)))
    print("benzersiz bayt toplam", sum(s["bayt"] for s in tekil.values()))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
