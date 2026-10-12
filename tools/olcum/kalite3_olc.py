"""KALİTE-3 Faz 3: pilot skill'lerin önce/sonra ölçümü (canlıya dokunmaz).

Kalite kolu: her skill iki sürümüyle (once = ~/.claude/skills/<ad> kopyası, sonra = .kalite3/pilot/<ad>) ayrı boş
proje klasörüne .claude/skills/k3-<ad> olarak konur; istem "Use the k3-<ad> skill" der → jeton, süre, USD, regex rubrik,
skill yüklendi mi, Read sayısı + okunan yollar (references okuması). Tekrarlar araya serpilir (tekrar → skill → varyant).
Tetik kolu (--tetik): skill listesi (pilot + sabit sahte adaylar) + görev istemleri → model her istem için skill seçer;
önce açıklamalar vs yeni açıklamalar (aciklama-yeni.jsonl, geçerli olanlar). Yeniden başlatınca yazılmış satırlar atlanır.
python tools/olcum/kalite3_olc.py <gorev.json> <cikti.tsv> [--tekrar 3] [--en-fazla 72] [--tetik aciklama-yeni.jsonl]
"""
import argparse, json, random, re, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kosucu import jeton, kos, puanla  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
CALISMA = KOK / ".kalite3" / "olc"
CANLI = Path.home() / ".claude" / "skills"
BASLIK = "ad\tvaryant\ttekrar\tinput\tcache_creation\tcache_read\toutput\tsure_sn\tusd\tkalite\tskill_yuklendi\tread_n\trc\n"


def hazirla(ad, varyant):
    kaynak = CANLI / ad if varyant == "once" else KOK / ".kalite3" / "pilot" / ad
    proje = CALISMA / varyant / ad
    hedef = proje / ".claude" / "skills" / f"k3-{ad}"
    if not hedef.exists():
        shutil.copytree(kaynak, hedef)
        s = hedef / "SKILL.md"
        s.write_text(re.sub(r"^name:.*$", f"name: k3-{ad}", s.read_text(encoding="utf-8"), count=1, flags=re.M),
                     encoding="utf-8", newline="\n")
    return proje


def yazilmis(cikti):
    if not cikti.exists():
        cikti.write_text(BASLIK, encoding="utf-8", newline="\n")
        return set()
    return {tuple(s.split("\t")[:3]) for s in cikti.read_text(encoding="utf-8").splitlines()[1:]}


def kalite_kolu(gorevler, cikti, tekrar, en_fazla):
    bitti, cagri = yazilmis(cikti), 0
    for t in range(1, tekrar + 1):
        for g in gorevler:
            for v in ("once", "sonra"):
                if (g["ad"], v, str(t)) in bitti or cagri >= en_fazla:
                    continue
                o = kos(f"Use the k3-{g['ad']} skill for this task. {g['istem']}", cwd=hazirla(g["ad"], v), model="sonnet",
                        timeout=900, butce=1.5)
                cagri += 1
                (CALISMA / "yanit").mkdir(parents=True, exist_ok=True)  # yargıç (jev) için yanıt metni
                (CALISMA / "yanit" / f"{g['ad']}-{v}-{t}.md").write_text(o["metin"], encoding="utf-8", newline="\n")
                i, cc, cr, out = jeton(o["usage"])
                skill = int(any(a == f"Skill:k3-{g['ad']}" or a.endswith(f":k3-{g['ad']}") for a in o["araclar"]))
                satir = [g["ad"], v, t, i, cc, cr, out, o["sure"], round(o["usd"], 4), puanla(o["metin"], g["rubrik"]),
                         skill, o["araclar"].count("Read"), o["rc"],
                         ",".join(y.split(f"k3-{g['ad']}/", 1)[-1] for y in o["okunan"])]  # okunan yol: skill köküne göre
                with open(cikti, "a", encoding="utf-8", newline="\n") as f:
                    f.write("\t".join(map(str, satir)) + "\n")
                print("\t".join(map(str, satir)), flush=True)
    return cagri


def tetik_kolu(gorevler, cikti, tekrar, yeni_jsonl, en_fazla):
    sys.path.insert(0, str(KOK / "tools"))
    from skill_filo_denetim import ayir
    yeni = {}
    for s in Path(yeni_jsonl).read_text(encoding="utf-8").splitlines():
        d = json.loads(s)
        if d["gecerli"]:
            yeni[d["ad"]] = d["yeni"]
    pilot = sorted(p.name for p in (KOK / ".kalite3" / "pilot").iterdir())
    rnd = random.Random(11)
    sahte = rnd.sample(sorted(p.name for p in CANLI.iterdir() if (p / "SKILL.md").exists() and p.name not in pilot), 40)
    eski = {a: ayir((CANLI / a / "SKILL.md").read_text(encoding="utf-8", errors="replace"))[0].get("description", "")
            for a in pilot + sahte}
    bitti, cagri = yazilmis(cikti), 0
    for t in range(1, tekrar + 1):
        for v in ("once", "sonra"):
            if ("_tetik", v, str(t)) in bitti or cagri >= en_fazla:
                continue
            liste = [(a, yeni.get(a, eski[a]) if v == "sonra" and a in pilot else eski[a]) for a in pilot + sahte]
            random.Random(t).shuffle(liste)
            istem = ("Pick the single best skill for each request. Skills:\n" + "\n".join(f"- {a}: {d[:1024]}" for a, d in liste)
                     + "\n\nRequests:\n" + "\n".join(f"{i}. {g['istem']}" for i, g in enumerate(gorevler))
                     + '\n\nReply with ONLY a JSON object {"0": "skill-name", ...}. Do not use tools.')
            o = kos(istem, model="sonnet", timeout=600, butce=1.0)
            cagri += 1
            m = re.search(r"\{.*\}", o["metin"], re.S)
            secim = json.loads(m.group(0)) if m else {}
            dogru = sum(secim.get(str(i)) == g["ad"] for i, g in enumerate(gorevler))
            i_, cc, cr, out = jeton(o["usage"])
            satir = ["_tetik", v, t, i_, cc, cr, out, o["sure"], round(o["usd"], 4), f"{dogru}/{len(gorevler)}", "", "", o["rc"]]
            with open(cikti, "a", encoding="utf-8", newline="\n") as f:
                f.write("\t".join(map(str, satir)) + "\n")
            print("\t".join(map(str, satir)), flush=True)
    return cagri


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("gorev")
    ap.add_argument("cikti")
    ap.add_argument("--tekrar", type=int, default=3)
    ap.add_argument("--en-fazla", type=int, default=72)
    ap.add_argument("--tetik")
    a = ap.parse_args()
    gorevler, cikti = json.loads(Path(a.gorev).read_text(encoding="utf-8")), Path(a.cikti)
    n = tetik_kolu(gorevler, cikti, a.tekrar, a.tetik, a.en_fazla) if a.tetik else kalite_kolu(gorevler, cikti, a.tekrar, a.en_fazla)
    print(f"bitti: {n} çağrı", flush=True)


if __name__ == "__main__":
    main()
