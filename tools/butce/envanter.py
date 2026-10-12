"""SKILL-BUTCE-1 envanter: init'teki skill listesinin kaynak kırılımı, yinelenen kopyalar, kayıt başı karakter, skillUsage,
skillOverrides ve /context Skills tablosu (modelin gördüğü: "< 20" jeton = yalnız ad). Canlı ~/.claude yalnız OKUNUR, değer yazılmaz.
  python tools/butce/envanter.py <init.json> <context.md> [çıktı.tsv]"""
import collections, hashlib, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EV = Path.home()
PROJE = Path(r"C:\Projeler\omer-skills\.claude\skills")


def on_bilgi(md):
    """SKILL.md frontmatter → (ad, açıklama). Katlanmış (>, |) açıklama satırları birleştirilir."""
    t = md.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"---\s*\n(.*?)\n---", t, re.S)
    if not m:
        return None, ""
    ad, acik, sat = None, "", m.group(1).splitlines()
    for i, s in enumerate(sat):
        if s.startswith("name:"):
            ad = s[5:].strip().strip("\"'")
        if s.startswith("description:"):
            v = s[12:].strip()
            if v in ("", ">", "|", ">-", "|-"):
                ek = []  # ilk girintisiz satırda dur
                for x in sat[i + 1:]:
                    if not x.startswith((" ", "\t")):
                        break
                    ek.append(x.strip())
                v = " ".join(ek)
            acik = v.strip("\"'")
    return ad, acik


def disk_haritasi():
    """skill kimliği → SKILL.md yolu: ~/.claude/skills, proje .claude/skills, kurulu plugin'ler."""
    h = {}
    for kok, kaynak in ((EV / ".claude/skills", "kullanıcı"), (PROJE, "proje")):
        for md in kok.glob("*/SKILL.md"):
            ad = on_bilgi(md)[0] or md.parent.name
            h.setdefault(ad, (kaynak, md))
    ip = json.loads((EV / ".claude/plugins/installed_plugins.json").read_text(encoding="utf-8"))
    for anahtar, kayitlar in ip.get("plugins", ip).items():
        eklenti = anahtar.split("@")[0]
        for k in kayitlar:
            for md in Path(k["installPath"]).rglob("SKILL.md"):
                ad = on_bilgi(md)[0] or md.parent.name
                h.setdefault(f"{eklenti}:{ad}", ("plugin", md))
                h.setdefault(f"{eklenti}:{md.parent.name}", ("plugin", md))
    return h


def context_tablosu(yol):
    t = Path(yol).read_text(encoding="utf-8").split("### Skills", 1)[1]
    # claude.ai kopyaları tabloda öneksiz ("jev | claude.ai sync"): anahtar init'teki adla aynı olsun
    # (bazıları önekli gelir: "anthropic-skills:9router-paket")
    return {("anthropic-skills:" if "claude.ai" in p[2] else "") + p[1].strip().removeprefix("anthropic-skills:"): (p[2].strip(), p[3].strip())
            for p in (l.split("|") for l in t.splitlines())
            if len(p) >= 5 and p[1].strip() not in ("Skill", "") and not p[1].startswith("-")}


def main(init, ctx, cikti=None):
    adlar = json.loads(Path(init).read_text(encoding="utf-8"))["skills"]
    ayar = json.loads((EV / ".claude/settings.json").read_text(encoding="utf-8"))
    ovr = ayar.get("skillOverrides", {})
    kul = json.loads((EV / ".claude.json").read_text(encoding="utf-8")).get("skillUsage", {})
    disk, tab = disk_haritasi(), context_tablosu(ctx)
    satirlar = []
    for a in adlar:
        on = a.split(":")[0] if ":" in a else ""
        if on == "anthropic-skills":
            kaynak = "claude.ai senkronu"
        elif on:
            kaynak = "plugin"
        else:
            kaynak = disk.get(a, ("yerleşik/diğer",))[0]
        md = disk.get(a, (None, None))[1]
        acik = on_bilgi(md)[1] if md else ""
        govde = hashlib.sha1(md.read_bytes()).hexdigest()[:10] if md else ""
        ctx_j = tab.get(a, ("", "yok"))[1]
        satirlar.append(dict(ad=a, kaynak=kaynak, kok=a.split(":")[-1], ad_kr=len(a), acik_kr=len(acik), sha=govde,
                             ovr=ovr.get(a, "on"), kullanim=kul.get(a, {}).get("usageCount", 0), ctx=ctx_j))
    say = collections.Counter
    print("toplam", len(satirlar), "| kaynak:", dict(say(s["kaynak"] for s in satirlar)))
    print("plugin üst 8:", say(s["ad"].split(":")[0] for s in satirlar if s["kaynak"] == "plugin").most_common(8))
    print("override:", dict(say(s["ovr"] for s in satirlar)), "| ayar toplam", dict(say(ovr.values())))
    print("ad karakter toplamı", sum(s["ad_kr"] + 3 for s in satirlar), "| açıklama (diskte bulunan)",
          sum(s["acik_kr"] for s in satirlar), "| açıklaması okunan kayıt", sum(1 for s in satirlar if s["sha"]))
    print("skillUsage", len(kul), "kayıt; listede olan", sum(1 for s in satirlar if s["kullanim"]))
    gor = [s for s in satirlar if s["ctx"] not in ("< 20", "yok")]
    print("/context: tabloda", len(tab), "| açıklamalı (≥20 jeton)", len(gor), "| yalnız ad", sum(1 for s in satirlar if s["ctx"] == "< 20"),
          "| tabloda yok", sum(1 for s in satirlar if s["ctx"] == "yok"))
    print("açıklamalı → override:", dict(say(s["ovr"] for s in gor)), "kullanılmış:", sum(1 for s in gor if s["kullanim"]))
    print("açıklamasız ama override 'on':", sum(1 for s in satirlar if s["ovr"] == "on" and s["ctx"] == "< 20"))
    grup = collections.defaultdict(list)
    for s in satirlar:
        grup[s["kok"]].append(s)
    yin = {k: v for k, v in grup.items() if len(v) > 1}
    ayni = sum(1 for v in yin.values() if len({s["sha"] for s in v if s["sha"]}) == 1 and sum(1 for s in v if s["sha"]) > 1)
    print("yinelenen kök ad", len(yin), "grup /", sum(len(v) for v in yin.values()), "kayıt; fazla kopya",
          sum(len(v) - 1 for v in yin.values()), "| diskte içerik sha eşit grup", ayni)
    print("yinelenen kaynak çiftleri:", say(" + ".join(sorted({s["kaynak"] for s in v})) for v in yin.values()).most_common(6))
    for a in ("jev", "awesome-rehber", "departman-frontend", "departman-arastirma"):
        print(" ", a, [(s["ad"], s["kaynak"], s["ovr"], s["ctx"], s["kullanim"]) for s in grup.get(a, [])])
    if cikti:
        with open(cikti, "w", encoding="utf-8", newline="\n") as f:
            f.write("\t".join(satirlar[0]) + "\n")
            f.writelines("\t".join(str(v) for v in s.values()) + "\n" for s in satirlar)


if __name__ == "__main__":
    main(*sys.argv[1:])
