"""ENVANTER-2: yetenek kataloğu → docs/katalog/yetenek.jsonl + yetenek.tsv.

Girdi (yeniden kullanım): docs/envanter/envanter.tsv (tools/envanter/topla.py üretir; önce onu koş),
skills/ajan-getir/katalog.tsv (tools/ajan_katalog.py), SKILL.md frontmatter (yerel · plugin · claude.ai
senkron · repo skills/), plugin manifestleri, omer-kutuphaneler tablosu, tools/*.py docstring'leri.
Artımlı: önceki jsonl'de alt ajanın yazdığı 'is' (ozet=1) kaynak imzası aynıysa korunur; imza değişen ya da
açıklaması olmayan satır ozet_bekliyor=1 olur (özet partisi: tools/katalog_yenile.py --bekleyen → 'is' boş
satırlar; alt ajan çıktısı {ad, tur, is, tetik} jsonl → --birlestir <dosya> ozet=1 yazar).
Salt okuma; MCP/ayar dosyalarından yalnız ad okunur, sır/ortam değeri yazılmaz.
"""
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home() / ".claude"
CIKTI = KOK / "docs" / "katalog"
csv.field_size_limit(10**9)
SIR = re.compile(r"(\bsk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bp]-)")


def aciklama(md):
    # .claude/token11/skill_olc.py aciklama() ile aynı ayrıştırma
    m = re.search(r"^---\s*\n(.*?)\n---", md.read_text(encoding="utf8", errors="ignore"), re.S)
    if not m:
        return ""
    d = re.search(r"^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", m.group(1), re.S | re.M)
    return " ".join(d.group(1).strip().strip("\"'>|").split()) if d else ""


def kisa(metin, n=110):
    metin = " ".join(metin.split())
    return metin if len(metin) <= n else metin[: n - 1].rsplit(" ", 1)[0] + "…"


def skill_aciklamalari():
    """ad → açıklama; skill_olc.aciklamalar() + repo skills/. Plugin anahtarı 'plugin:skill'."""
    d = {}
    for kok in (KOK / "skills", EV / "skills"):
        for md in kok.glob("*/SKILL.md"):
            d.setdefault(md.parent.name, aciklama(md))
    # claude.ai senkron skill'lerin yerel kopyası skills/synced/<uuid>/<ad>/
    for md in [*(EV / "plugins" / "synced").glob("**/SKILL.md"), *(EV / "skills" / "synced").glob("*/*/SKILL.md")]:
        if not d.get(md.parent.name):
            d[md.parent.name] = aciklama(md)
    ip = json.loads((EV / "plugins" / "installed_plugins.json").read_text(encoding="utf8"))
    plug = {}
    # plugin.json'da açıklama yoksa pazar yeri marketplace.json'daki satır
    for m in (EV / "plugins" / "marketplaces").glob("*/.claude-plugin/marketplace.json"):
        for p in json.loads(m.read_text(encoding="utf8", errors="ignore")).get("plugins") or []:
            plug.setdefault(f"{p.get('name')}@{m.parents[1].name}", p.get("description") or "")
    for anahtar, kayitlar in (ip.get("plugins") or {}).items():
        for k in kayitlar[:1]:
            yol = Path(k["installPath"])
            for md in yol.glob("**/skills/*/SKILL.md"):
                d.setdefault(f"{anahtar.split('@')[0]}:{md.parent.name}", aciklama(md))
            man = yol / ".claude-plugin" / "plugin.json"
            if man.exists():
                plug[anahtar] = (json.loads(man.read_text(encoding="utf8", errors="ignore")).get("description") or "") or plug.get(anahtar, "")
    return d, plug


def paket_aciklamalari():
    """CLI paket adı → açıklama: npm -g package.json + uv tool METADATA Summary."""
    d = {}
    npm = Path(subprocess.run("npm root -g", shell=True, capture_output=True, text=True).stdout.strip() or ".")
    for pj in [*npm.glob("*/package.json"), *npm.glob("@*/*/package.json")]:
        j = json.loads(pj.read_text(encoding="utf8", errors="ignore"))
        d[j.get("name", "")] = j.get("description") or ""
    uv = Path(os.environ.get("APPDATA", "")) / "uv" / "tools"
    for meta in uv.glob("*/Lib/site-packages/*.dist-info/METADATA"):
        m = re.search(r"^Summary: (.*)$", meta.read_text(encoding="utf8", errors="ignore"), re.M)
        if m and meta.parents[3].name.lower() == meta.parent.name.split("-")[0].lower().replace("_", "-"):
            d[meta.parents[3].name] = m.group(1)
    return d


def kapali_skilller():
    try:
        ayar = json.loads((EV / "settings.json").read_text(encoding="utf8"))
    except (OSError, ValueError):
        return set()
    return {k for k, v in (ayar.get("skillOverrides") or {}).items() if v == "off"}


def kutuphaneler():
    md = (KOK / "skills" / "omer-kutuphaneler" / "SKILL.md").read_text(encoding="utf8")
    for s in md.splitlines():
        h = [x.strip() for x in s.strip().strip("|").split("|")]
        if s.startswith("|") and len(h) >= 5 and h[0] not in ("kütüphane",) and not h[0].startswith("---"):
            yield h[0], f"{h[1]}; {h[2]} için", h[4]


def repo_araclari():
    for py in sorted((KOK / "tools").glob("*.py")):
        m = re.match(r'\s*(?:#.*\n)*\s*"""(.*?)(?:"""|\n\n)', py.read_text(encoding="utf8", errors="ignore"), re.S)
        if m:
            yield py.stem, " ".join(m.group(1).split()), f"python tools/{py.name}"


def satirlar():
    sk, plug = skill_aciklamalari()
    kapali = kapali_skilller()
    paket = paket_aciklamalari()
    ajan = {}
    with open(KOK / "skills" / "ajan-getir" / "katalog.tsv", encoding="utf8") as f:
        for r in csv.reader(f, delimiter="\t"):
            if len(r) >= 3:
                ajan[r[0]] = r[2]
    # envanter.tsv 'is' sütunu TOKEN-10 sıkıştırmasıyla kayıplı; tam açıklama ajan .md frontmatter'ında
    ajan_md = {md.stem: aciklama(md) for kok in (EV / "agents", KOK / ".claude" / "agents") for md in kok.glob("*.md")}
    with open(KOK / "docs" / "envanter" / "envanter.tsv", encoding="utf8") as f:
        env = list(csv.DictReader(f, delimiter="\t"))
    env_ajan = {r["ad"] for r in env if r["tur"] == "ajan"}
    env += [dict(ad=a, tur="ajan", kaynak="agents/", nerede="CC", ozellik="", **{"is": ""})
            for a in ajan_md if a not in env_ajan]
    for r in env:
        ad, tur, kaynak, nerede = r["ad"], r["tur"], r["kaynak"], r["nerede"]
        if tur == "skill" and nerede != "yok":
            yield dict(ad=ad, tur="skill", kaynak=kaynak, aciklama=r["is"] or sk.get(ad, ""),
                       cagri=f"Skill {ad}", durum=nerede + (" · kapalı(override off)" if ad in kapali else ""))
        elif tur == "plugin-skill":
            p = kaynak.split("@")[0]
            tam = f"{p}:{ad}"
            yield dict(ad=tam, tur="skill", kaynak=kaynak, aciklama=r["is"] or sk.get(tam, ""),
                       cagri=f"Skill {tam}", durum=nerede + (" · kapalı(override off)" if tam in kapali else ""))
        elif tur == "plugin":
            yield dict(ad=ad, tur="plugin", kaynak=kaynak, aciklama=plug.get(kaynak, ""),
                       cagri=f"/plugin {kaynak} (skill/ajan/MCP'leri ayrı satırlarda)", durum=nerede + (f" · {r['ozellik']}" if r["ozellik"] else ""))
        elif tur == "ajan":
            yield dict(ad=ad, tur="ajan", kaynak=kaynak, aciklama=ajan_md.get(ad) or ajan.get(ad) or r["is"],
                       cagri=f"Agent {ad} (listede yoksa Skill ajan-getir)", durum=nerede)
        elif tur in ("mcp", "baglayici"):
            yield dict(ad=ad, tur="mcp", kaynak=kaynak, aciklama=r["is"],
                       cagri=f"ToolSearch '{ad}' → mcp__{ad}__*" if tur == "mcp" else "claude.ai bağlayıcısı", durum=nerede)
        elif tur == "cli" and ad != "-":
            yield dict(ad=ad, tur="cli", kaynak=kaynak, aciklama=r["is"] or paket.get(ad, ""), cagri=f"Bash: {ad} --help", durum=nerede)
    for ad, aciklama_, lisans in kutuphaneler():
        yield dict(ad=ad, tur="kutuphane", kaynak="omer-kutuphaneler", aciklama=aciklama_,
                   cagri="Skill omer-kutuphaneler (pinli kurulum satırı)", durum=f"lisans {lisans}")
    for ad, aciklama_, komut in repo_araclari():
        yield dict(ad=ad, tur="arac", kaynak="omer-skills tools/", aciklama=aciklama_, cagri=komut, durum="repo")


def uret(onceki):
    cikti, gor = [], set()
    for s in satirlar():
        anahtar = (s["ad"], s["tur"])
        if anahtar in gor:
            continue
        gor.add(anahtar)
        imza = hashlib.sha1(s["aciklama"].encode("utf8")).hexdigest()[:8]
        eski = onceki.get(anahtar)
        if eski and eski.get("ozet") and eski.get("imza") == imza:
            s.update(is_=eski["is"], tetik=eski.get("tetik", ""), ozet=1)
        else:
            s.update(is_=kisa(s["aciklama"]), tetik="", ozet=0)
        s["imza"] = imza
        s["ozet_bekliyor"] = int(not s["ozet"])
        s["metin"] = kisa(s.pop("aciklama"), 400)
        s["is"] = s.pop("is_")
        assert not SIR.search(json.dumps(s, ensure_ascii=False)), f"sır deseni: {s['ad']}"
        cikti.append(s)
    return cikti


def main():
    CIKTI.mkdir(parents=True, exist_ok=True)
    jl = CIKTI / "yetenek.jsonl"
    onceki = {}
    if jl.exists():
        for s in jl.read_text(encoding="utf8").splitlines():
            o = json.loads(s)
            onceki[(o["ad"], o["tur"])] = o
    if "--birlestir" in sys.argv:
        for s in Path(sys.argv[sys.argv.index("--birlestir") + 1]).read_text(encoding="utf8").splitlines():
            y = json.loads(s) if s.strip() else None
            if y and (y["ad"], y["tur"]) in onceki and y.get("is"):
                onceki[(y["ad"], y["tur"])].update(ozet=1,**{"is": kisa(y["is"]), "tetik": kisa(y.get("tetik", ""), 120)})
    rows = uret(onceki)
    if "--bekleyen" in sys.argv:
        sys.stdout.reconfigure(encoding="utf8")
        for o in rows:
            if not o["is"]:
                print(json.dumps({k: o[k] for k in ("ad", "tur", "kaynak", "durum")}, ensure_ascii=False))
        return
    jl.write_bytes("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in rows).encode("utf8"))
    sutun = ["ad", "tur", "kaynak", "is", "tetik", "cagri", "durum"]
    with open(CIKTI / "yetenek.tsv", "w", encoding="utf8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(sutun)
        for o in rows:
            w.writerow([o[k].replace("\t", " ") for k in sutun])
    from collections import Counter
    print(len(rows), dict(Counter(o["tur"] for o in rows)), "ozet_bekliyor", sum(o["ozet_bekliyor"] for o in rows),
          "is_bos", sum(not o["is"] for o in rows))


if __name__ == "__main__":
    main()
