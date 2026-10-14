"""ENVANTER-4 m2: derin kılavuz partileri.

  kart       tekil.tsv temsilcilerinden okuma kartları (başlıklar + baş + komutlar) → .kos/kopru/envanter4/kart/pNNN.md
  birlestir  okuyucu çıktıları (.kos/kopru/envanter4/cikti/pNNN.jsonl) → doğrulanmış docs/katalog/derin.jsonl
Kart yalnız mekanizma ipucu taşır; anahtar/token değerleri maskelenir, ortam değişkeni yalnız ADI geçer.
"""
import collections
import csv
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
KAT = KOK / "docs" / "katalog"
IS = Path("C:/Projeler/omer-skills/.kos/kopru/envanter4")
ALAN = ("nasil", "neden", "en_iyi", "birlikte", "tuzak", "maliyet")
SIR = re.compile(r"(\bsk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bp]-[A-Za-z0-9-]+|eyJ[A-Za-z0-9_-]{20,})")
ON_EK = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.S)
KOMUT = re.compile(r"^\s*(?:\$ )?(npx|npm|pnpm|bunx?|uvx?|pip|python3?|node|claude|gh|git|docker|pwsh|powershell|curl|cargo|go|dotnet|playwright|ffmpeg|blender)\b.{3,}")
ENV = re.compile(r"\b[A-Z][A-Z0-9_]{2,}_(?:API_KEY|TOKEN|SECRET|KEY)\b")
ONCELIK = ["gstack", "mukul975", "davila7", "ecc", "nyldn-plugins", "phoenix-security", "superpowers-marketplace",
           "claude-plugins-official", "omni", "departman", "omer-skills", "omer-araclar"]
PARTI = 45


def maske(t):
    return SIR.sub("«gizli»", t)


def boy(n):
    return "küçük" if n < 4000 else "orta" if n < 15000 else "büyük"


def kart_skill(yol, n):
    t = yol.read_text(encoding="utf8", errors="ignore")
    m = ON_EK.match(t)
    fm, govde = (m.group(1), t[m.end():]) if m else ("", t)
    d = re.search(r"^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", fm, re.S | re.M)
    s = govde.splitlines()
    bas = [x.strip("# ").strip() for x in s if re.match(r"#{1,3} ", x)][:22]
    kom = list(dict.fromkeys(x.strip()[:110] for x in s if KOMUT.match(x)))[:8]
    env = sorted(set(ENV.findall(t)))[:6]
    yan = sorted(p.name + ("/" if p.is_dir() else "") for p in yol.parent.iterdir() if p.name != yol.name)[:14] if yol.name == "SKILL.md" else []
    return [f"açıklama: {' '.join((d.group(1) if d else '').split())[:320]}",
            f"başlıklar: {' | '.join(bas)}", f"komutlar: {' ‖ '.join(kom) or '-'}",
            f"ortam adları: {', '.join(env) or '-'}", f"yan dosyalar: {', '.join(yan) or '-'}", f"gövde boyu: {n} bayt ({boy(n)})",
            "baş: " + " ".join(govde.split())[:900]]


def kart_plugin(yol):
    man = yol / ".claude-plugin" / "plugin.json"
    j = json.loads(man.read_text(encoding="utf8", errors="ignore")) if man.exists() else {}
    say = {k: sorted({p.parent.name if k == "skills" else p.stem for p in yol.glob(f"**/{k}/*/SKILL.md" if k == "skills" else f"**/{k}/*.md")})
           for k in ("skills", "agents", "commands")}
    mcp = yol / ".mcp.json"
    mcpler = list((json.loads(mcp.read_text(encoding="utf8", errors="ignore")).get("mcpServers") or {}).keys()) if mcp.exists() else []
    oku = next((p for p in (yol / "README.md", yol / "readme.md") if p.exists()), None)
    return [f"açıklama: {j.get('description', '')[:320]}"] + [f"{k} ({len(v)}): {', '.join(v[:25])}" for k, v in say.items()] + [
        f"hooks: {'var' if any(yol.glob('**/hooks/hooks.json')) else 'yok'} · mcp: {', '.join(mcpler) or '-'}",
        "readme başı: " + (" ".join(oku.read_text(encoding="utf8", errors="ignore").split())[:700] if oku else "-")]


def kart():
    R = list(csv.DictReader(open(KAT / "tekil.tsv", encoding="utf8"), delimiter="\t"))
    kat = {json.loads(s)["ad"]: json.loads(s) for s in open(KAT / "yetenek.jsonl", encoding="utf8")}
    kopya = collections.defaultdict(list)
    for r in R:
        kopya[r["temsilci"]].append(r["ad"])
    tem = [r for r in R if r["ad"] == r["temsilci"]]
    sira = {a: i for i, a in enumerate(ONCELIK)}
    tem.sort(key=lambda r: (sira.get(r["aile"], 99), r["aile"], r["ad"]))
    (IS / "kart").mkdir(parents=True, exist_ok=True)
    (IS / "cikti").mkdir(exist_ok=True)
    partiler, aile_parti = [], collections.defaultdict(set)
    for r in tem:
        if not partiler or len(partiler[-1]) >= PARTI:
            partiler.append([])
        partiler[-1].append(r)
    for i, p in enumerate(partiler, 1):
        bloklar = []
        for r in p:
            k, yol = kat.get(r["ad"], {}), Path(r["yol"]) if r["yol"] else None
            bas = f"## {r['ad']}\ntür {r['tur']} · aile {r['aile']} · çağrı {k.get('cagri', '')} · kopyalar {', '.join(x for x in kopya[r['ad']] if x != r['ad'])[:200] or '-'}"
            try:
                govde = kart_plugin(yol) if r["tur"] == "plugin" and yol and yol.is_dir() else kart_skill(yol, int(r["bayt"])) if yol and yol.is_file() else [f"katalog metni: {k.get('metin', '')}"]
            except OSError as e:
                govde = [f"katalog metni: {k.get('metin', '')} (okunamadı: {e.__class__.__name__})"]
            bloklar.append(maske(bas + "\n" + "\n".join(govde)))
            aile_parti[r["aile"]].add(i)
        (IS / "kart" / f"p{i:03d}.md").write_text("\n\n".join(bloklar) + "\n", encoding="utf8")
    (IS / "aile-parti.json").write_text(json.dumps({a: sorted(v) for a, v in aile_parti.items()}, ensure_ascii=False), encoding="utf8")
    print(f"temsilci {len(tem)} · parti {len(partiler)} · ilk 12 parti aileleri:",
          ", ".join(f"p{i:03d}={'/'.join(sorted({r['aile'] for r in p}))}" for i, p in enumerate(partiler[:12], 1)))


def birlestir():
    R = [r for r in csv.DictReader(open(KAT / "tekil.tsv", encoding="utf8"), delimiter="\t") if r["ad"] == r["temsilci"]]
    tem = {f"{r['tur']}:{r['ad']}" for r in R}
    say = collections.Counter(r["ad"] for r in R)
    tek_tur = {r["ad"]: r["tur"] for r in R if say[r["ad"]] == 1}  # tur'suz eski kayıt yalnız ad tekse eşlenir
    anahtar = lambda j: f"{j.get('tur') or tek_tur.get(j.get('ad'))}:{j.get('ad')}"
    yol = KAT / "derin.jsonl"
    d = {anahtar(j): {**j, "tur": anahtar(j).split(":", 1)[0]} for j in map(json.loads, open(yol, encoding="utf8"))} if yol.exists() else {}
    hata = collections.Counter()
    dyol = IS / "ornek" / "dogruluk.json"
    dog, dis = json.loads(dyol.read_text(encoding="utf8")) if dyol.exists() else {}, set()
    for f in sorted((IS / "cikti").glob("p*.jsonl")):
        if f.stem.endswith("-t") and dog.get(str(int(f.stem[1:4])), 0) < 0.85:  # Desktop 14 Eki: <%85 ya da örneklemsiz taslak derin'e girmez
            dis.add(f.stem)
            continue
        for s in open(f, encoding="utf8"):
            if not s.strip():
                continue
            try:
                j = json.loads(s)
            except ValueError:
                hata[f"{f.stem}:json"] += 1
                continue
            k = anahtar(j)
            if j.get("durum") == "katalog" and k in tem:  # sınıflandırıcı engelli aile: katalog metni kalır, derin boş
                d[k] = {"ad": j["ad"], "tur": k.split(":", 1)[0], "durum": "katalog", **{a: "" for a in ALAN}}
                continue
            # uydurma diye silinen alan "?" gelir; hepsi boş/"?" ise kayıt yok sayılır
            if k not in tem or any(not isinstance(j.get(a), str) or not j[a].strip() for a in ALAN) or all(j[a].strip() == "?" for a in ALAN):
                hata[f"{f.stem}:alan/ad"] += 1
                continue
            kayit = {"ad": j["ad"], "tur": k.split(":", 1)[0], **{a: maske(" ".join(j[a].split())) for a in ALAN}}
            if j.get("konu"):
                kayit["konu"] = str(j["konu"])[:40]
            if j.get("dogrulandi") is False:
                kayit["dogrulandi"] = False
            for a in ALAN:
                if len(kayit[a]) > 160:
                    hata["160 kırpıldı"] += 1
                    kayit[a] = kayit[a][:159].rsplit(" ", 1)[0] + "…"
            d[k] = kayit
    with open(yol, "w", encoding="utf8", newline="\n") as f:
        for k in sorted(d):
            f.write(json.dumps(d[k], ensure_ascii=False) + "\n")
    kat = sum(j.get("durum") == "katalog" for j in d.values())
    print(f"derin dolu {len(d) - kat}/{len(tem)} · katalog işaretli {kat} · hata {dict(hata) or 0} · dışlanan parti {len(dis)}")


assert boy(100) == "küçük" and maske("x sk-" + "a" * 20) == "x «gizli»"

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"kart": kart, "birlestir": birlestir}[sys.argv[1]]()
