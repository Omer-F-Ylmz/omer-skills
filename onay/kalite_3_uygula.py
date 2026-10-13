"""KALİTE-3 onay betiği — Ömer koşar. Yalnız ölçümü GEÇEN skill'leri ~/.claude/skills'e uygular.

  python onay/kalite_3_uygula.py --kuru   # plan: hangi skill, ne değişir (varsayılan)
  python onay/kalite_3_uygula.py uygula   # yedek alır → bölünmüş gövde + yeni açıklama yazar
  python onay/kalite_3_uygula.py --geri   # son yedeği geri koyar
Kabul listesi docs/kutuphane/kalite3-kabul.txt (satır başına skill adı; Faz 3 karar tablosundan). Açıklama: .kalite3/aciklama-yeni.jsonl
içinde gecerli=true ve sonnet denetimi sorun bildirmemiş satırlar. Yalnız gevşek ~/.claude/skills/<ad> yazılır; plugin/synced
kopyaları dist zip'iyle gider. MODEL KURALI: ~/.claude/settings.json env'deki CLAUDE_CODE_SUBAGENT_MODEL kaldırılır
(her ajan frontmatter `model:` ile ölçülen en iyi modelde koşar; değer yazdırılmaz, settings.json yedeklenir).
AJANLAR: docs/kutuphane/kalite3-ajan-kabul.txt'teki (pilotu geçen) ajanlar/{kalite3,kalite3-d15,kalite3-ruflo,kalite3-d16,kalite3-d17}/*/<ad>.md → ~/.claude/agents/<ad>.md (varsa yedeklenir). Hiçbir skill silinmez/kapatılmaz; MCP listesi önce=sonra değilse rc=1.
"""
import json, re, shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home()


def mcp_var_mi(ev=EV):
    """~/.claude.json'daki MCP sunucu adları (değer yazdırılmaz, yalnız adlar)."""
    try:
        j = json.loads((ev / ".claude.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    adlar = set(j.get("mcpServers") or {})
    for p in (j.get("projects") or {}).values():
        adlar |= set((p or {}).get("mcpServers") or {})
    return adlar


def subagent_env_var_mi(ev=EV):
    """settings.json env'de CLAUDE_CODE_SUBAGENT_MODEL var mı (yalnız evet/hayır)."""
    try:
        return "CLAUDE_CODE_SUBAGENT_MODEL" in (json.loads((ev / ".claude" / "settings.json").read_text(encoding="utf-8")).get("env") or {})
    except (OSError, ValueError):
        return False


def aciklama_yaz(skill_md, yeni):
    metin = skill_md.read_text(encoding="utf-8")
    m = re.match(r"---\r?\n(.*?)\r?\n---", metin, re.S)
    if not m or not re.search(r"^description:[ \t]*[^|>\s].*$", m.group(1), re.M):
        return False  # çok satırlı ya da yok: elle
    deger = '"' + yeni.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'
    fm = re.sub(r"^description:.*$", lambda _: f"description: {deger}", m.group(1), count=1, flags=re.M)
    skill_md.write_text(metin[:m.start(1)] + fm + metin[m.end(1):], encoding="utf-8", newline="\n")
    return True


def plan(ev=EV, kok=KOK):
    kabul_yol = kok / "docs" / "kutuphane" / "kalite3-kabul.txt"
    kabul = [s.strip() for s in kabul_yol.read_text(encoding="utf-8").splitlines() if s.strip()] if kabul_yol.exists() else []
    yeni = {}
    jl = kok / ".kalite3" / "aciklama-yeni.jsonl"
    for s in (jl.read_text(encoding="utf-8").splitlines() if jl.exists() else []):
        d = json.loads(s)
        if d["gecerli"] and d.get("denetim", "yok") == "yok":
            yeni[d["ad"]] = d["yeni"]
    out = []
    for ad in kabul:
        hedef = ev / ".claude" / "skills" / ad
        if not (hedef / "SKILL.md").exists():
            continue
        bol = kok / ".kalite3" / "pilot" / ad
        out.append({"ad": ad, "hedef": hedef, "bolunmus": bol if (bol / "SKILL.md").exists() else None, "aciklama": yeni.get(ad)})
    return out


def ajan_plani(kok=KOK):
    yol = kok / "docs" / "kutuphane" / "kalite3-ajan-kabul.txt"
    kabul = [s.strip() for s in yol.read_text(encoding="utf-8").splitlines() if s.strip()] if yol.exists() else []
    # kalite3-d15: dil-cerceve (dil-) · altyapi (ops-) · ml-yapay-zeka (ml-) · urun-is (urn-) + mevcut aileler; kalite3-ruflo: ruflo mekanizmaları; kalite3-d16: + mobil (mob-) · backend (be-); kalite3-d17: d15 kalanı + Ruflo + IG araç ajanları
    kaynak = {f.stem: f for k in ("kalite3", "kalite3-d15", "kalite3-ruflo", "kalite3-d16", "kalite3-d17") for f in (kok / "ajanlar" / k).glob("*/*.md")}
    return [(ad, kaynak[ad]) for ad in kabul if ad in kaynak]


def katalog_farkli_mi(ev=EV, kok=KOK):
    """CC ajan-getir katalog.tsv repo'dakinden farklı mı (yalnız gevşek ~/.claude/skills/ajan-getir kuruluysa)."""
    canli, repo = ev / ".claude" / "skills" / "ajan-getir" / "katalog.tsv", kok / "skills" / "ajan-getir" / "katalog.tsv"
    return canli.exists() and repo.exists() and canli.read_bytes() != repo.read_bytes()


def uygula(ev=EV, kok=KOK):
    once = mcp_var_mi(ev)
    yedek = ev / ".claude" / "yedek" / f"kalite3-{time.strftime('%Y%m%d-%H%M%S')}"
    liste = plan(ev, kok)
    for p in liste:
        shutil.copytree(p["hedef"], yedek / p["ad"])
        if p["bolunmus"]:
            shutil.copytree(p["bolunmus"], p["hedef"], dirs_exist_ok=True)
        if p["aciklama"] and not aciklama_yaz(p["hedef"] / "SKILL.md", p["aciklama"]):
            print(f"  {p['ad']}: açıklama çok satırlı, elle")
    ayar_var = subagent_env_var_mi(ev)
    if ayar_var:
        ayar = ev / ".claude" / "settings.json"
        yedek.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ayar, yedek / "settings.json")
        j = json.loads(ayar.read_text(encoding="utf-8"))
        del j["env"]["CLAUDE_CODE_SUBAGENT_MODEL"]
        ayar.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print("  settings.json env: CLAUDE_CODE_SUBAGENT_MODEL kaldırıldı")
    ajanlar = ajan_plani(kok)
    for ad, kaynak in ajanlar:
        hedef = ev / ".claude" / "agents" / f"{ad}.md"
        if hedef.exists():
            (yedek / "agents").mkdir(parents=True, exist_ok=True)
            shutil.copy2(hedef, yedek / "agents" / hedef.name)
        hedef.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(kaynak, hedef)
    yedek.mkdir(parents=True, exist_ok=True)
    katalog = katalog_farkli_mi(ev, kok)
    if katalog:
        canli = ev / ".claude" / "skills" / "ajan-getir" / "katalog.tsv"
        shutil.copy2(canli, yedek / "ajan-getir-katalog.tsv")
        shutil.copy2(kok / "skills" / "ajan-getir" / "katalog.tsv", canli)
        print("  ajan-getir katalog.tsv güncellendi")
    (ev / ".claude" / "yedek" / "kalite3-son.json").write_text(json.dumps(
        {"yedek": str(yedek), "adlar": [p["ad"] for p in liste], "ayar": ayar_var, "ajanlar": [a for a, _ in ajanlar],
         "katalog": katalog}),
        encoding="utf-8")
    print(f"uygulandı {len(liste)} skill · {len(ajanlar)} ajan · yedek {yedek}")
    return once == mcp_var_mi(ev)


def geri(ev=EV):
    once = mcp_var_mi(ev)
    son = json.loads((ev / ".claude" / "yedek" / "kalite3-son.json").read_text(encoding="utf-8"))
    for ad in son["adlar"]:
        hedef = ev / ".claude" / "skills" / ad
        shutil.rmtree(hedef)
        shutil.copytree(Path(son["yedek"]) / ad, hedef)
    if son.get("ayar"):
        shutil.copy2(Path(son["yedek"]) / "settings.json", ev / ".claude" / "settings.json")
    for ad in son.get("ajanlar", []):
        hedef, eski = ev / ".claude" / "agents" / f"{ad}.md", Path(son["yedek"]) / "agents" / f"{ad}.md"
        shutil.copy2(eski, hedef) if eski.exists() else hedef.unlink(missing_ok=True)
    if son.get("katalog"):
        shutil.copy2(Path(son["yedek"]) / "ajan-getir-katalog.tsv", ev / ".claude" / "skills" / "ajan-getir" / "katalog.tsv")
    print(f"geri alındı {len(son['adlar'])} skill")
    return once == mcp_var_mi(ev)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    kip = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
    if kip == "uygula":
        ok = uygula()
    elif kip == "--geri":
        ok = geri()
    else:
        for p in plan():
            print(f"{p['ad']}\tbölünmüş={'evet' if p['bolunmus'] else 'hayır'}\taçıklama={'yeni' if p['aciklama'] else '-'}")
        print(f"settings.json env CLAUDE_CODE_SUBAGENT_MODEL: {'var → kaldırılacak' if subagent_env_var_mi() else 'yok'}")
        for ad, kaynak in ajan_plani():
            m = re.search(r"^model:\s*(\S+)", kaynak.read_text(encoding="utf-8"), re.M)
            var = (EV / ".claude" / "agents" / f"{ad}.md").exists()
            print(f"ajan {ad}\tmodel={m.group(1) if m else '-'}\t{'üzerine (yedekli)' if var else 'yeni'}")
        print(f"ajan-getir katalog.tsv: {'farklı → güncellenecek (yedekli)' if katalog_farkli_mi() else 'aynı'}")
        ok = True
    print("mcp önce=sonra" if ok else "HATA: MCP listesi değişti")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
