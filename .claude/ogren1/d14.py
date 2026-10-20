"""ÖĞREN-1 d14 (Desktop 08:14): d13 yolu (Claude yazar + sert denetim) + KAYNAK ÇÖZÜMÜ + token-dışı + tohum 11.
Kaynak çözümü: kanca kalemi (Olay:eşleyici, hooks.json/settings.json) → kendi kayıt girdisi + çağrılan betiklerin TAM metni;
repo/eklenti dizini (kökte SKILL.md yok) → kök README + package.json/pyproject/plugin.json (alt skill dosyası DEĞİL).
Çözülen metin d14-kaynak/<ad>.txt'ye yazılır: yazar, hakem ve sert denetim aynı metni görür.
  python -X utf8 .claude/ogren1/d14.py denetim     → tüm token kalemlerinde kaynak denetimi → d14-denetim.tsv
  python -X utf8 .claude/ogren1/d14.py ornek       → d14-ornek.tsv (önceki tüm örnekler hariç, seed 11, 28 kalem)
  python -X utf8 .claude/ogren1/d14.py paket       → d14-paket-1..3.md
  python -X utf8 .claude/ogren1/d14.py birlestir   → ozet-token-d14.jsonl + hakem-d14.jsonl + token-disi-geri.tsv
  python -X utf8 .claude/ogren1/d14.py puan h1 h2"""
import json, random, re, sys, zipfile
from pathlib import Path

import ozet_kaynak
from d13 import A, B, O, sert
from ozet3 import BASLIK, adlari, kaynaksiz
from son import oku

K = O / "d14-kaynak"
BETIK = re.compile(r"[\w:./\\~${}%-]+\.(?:mjs|cjs|js|ts|py|ps1|sh)\b")
P, TOHUM = "d14", 11  # "t12" argümanı: ikinci kapı tohumu (Desktop 09:10: tohum 11 ve 12 ikisi de ≥%92)
TAVAN = 300_000  # shortcut: paketlenmiş (bundle) betik metne girmez, yalnız boyutu; gerekirse kaynak (src) dosyasına çöz


def kanca(ad, kaynak):
    """→ (kalemin kendi kayıt girdileri, çağrılan betik yolları)"""
    p = Path(kaynak)
    olay, esl = ad.split(":", 1)
    kayit = [g for g in json.loads(p.read_text(encoding="utf-8")).get("hooks", {}).get(olay, [])
             if g.get("matcher", "") == esl or esl == "*" and "matcher" not in g]  # eşleyicisiz kayıt katalogda "*" adını alır
    kok = p.parent.parent if p.name == "hooks.json" else p.parent
    yol = []
    for g in kayit:
        for h in g.get("hooks", []):
            c = h.get("command", "")
            for v in ("${CLAUDE_PLUGIN_ROOT}", "$CLAUDE_PLUGIN_ROOT", "%CLAUDE_PLUGIN_ROOT%"):
                c = c.replace(v, str(kok))
            for v in ("${HOME}", "$HOME", "~"):
                c = c.replace(v, str(Path.home()))
            for t in BETIK.findall(c):
                t = re.sub(r"^.*\$\{?\w+\}?[/\\]", "", t)  # claude-mem: "$_P/scripts/x.cjs" → eklenti köküne göreli
                y = Path(t) if Path(t).is_absolute() else kok / t
                if y.is_file() and y not in yol:
                    yol.append(y)
    return kayit, yol


def metin(ad, kaynak):
    if ".zip!" in kaynak:  # OmniRoute zip'indeki tek skill: "<zip>!<iç yol>"
        z, i = kaynak.split("!", 1)
        with zipfile.ZipFile(z) as f:
            return f.read(next(n for n in f.namelist() if n.endswith(i))).decode("utf-8", "replace")
    p = Path(kaynak)
    if p.name == ".claude.json":  # MCP kaydı: dosyanın tamamı değil, yalnız kalemin girdisi; env/headers değerleri gizli
        j = json.loads(p.read_text(encoding="utf-8"))
        s = [f"=== kayıt: {p} · {yer} · {ad} ===\n" + json.dumps({**g, **{k: {a: "<gizli>" for a in g[k]} for k in ("env", "headers") if k in g}}, ensure_ascii=False, indent=2)
             for yer, m in [("mcpServers", j.get("mcpServers", {}))] + [(f"projects.{q}", v.get("mcpServers", {})) for q, v in j.get("projects", {}).items()]
             for n, g in m.items() if n == ad]
        return "\n".join(s) + "\n" if s else ""
    if p.name in ("hooks.json", "settings.json") and ":" in ad:
        kayit, yol = kanca(ad, kaynak)
        s = [f"=== kayıt: {p} · {ad} ===", json.dumps(kayit, ensure_ascii=False, indent=2)]
        for y in yol:
            b = y.stat().st_size
            s += [f"=== betik: {y} ===", y.read_text(encoding="utf-8", errors="replace") if b <= TAVAN else f"(paketlenmiş betik, {b} bayt — metne alınmadı)"]
        return "\n".join(s) + "\n"
    if p.is_dir() and not (p / "SKILL.md").is_file():
        readme = next((n for n in ("README.md", "readme.md") if (p / n).is_file()), None)
        s = []
        for n in [readme] + ["package.json", "pyproject.toml", ".claude-plugin/plugin.json"]:
            if n and (p / n).is_file():
                s += [f"=== {n} ===", (p / n).read_text(encoding="utf-8", errors="replace")]
        return "\n".join(s) + "\n" if s else ""
    return ozet_kaynak.metin(kaynak)


def dosya(ad):
    return K / (re.sub(r"[^\w.-]", "_", ad) + ".txt")


def aday():
    return [s.split("\t") for s in (B / "d7-aday.tsv").read_text(encoding="utf-8").splitlines()]


def katalog_token():
    """tohum 12: d7-aday tükendi → güncel katalogun token kalemleri (kanonik), d7-aday biçiminde; aynı adlı ikinciler atılır"""
    t = [json.loads(x) for x in (O / "katalog-son.jsonl").read_text(encoding="utf-8").splitlines()]
    return list({r["ad"]: [r["ad"], r["tur"], str(r["bayt"]), r["yol"]] for r in reversed(t) if r["kategori_son"] == "token" and r["kanonik"] == r["id"]}.values())


def denetim():
    """her token kalemi: çözülen kaynak kalemin kendisine mi ait, boş mu, yalnız kayıt mı"""
    tum = {**ozet_kaynak.D, **{s[0]: s[3] for s in aday() if s[1] != "aday"}}
    say, satir = {}, []
    for ad, k in tum.items():
        try:
            m = metin(ad, k)
            if Path(k).name in ("hooks.json", "settings.json") and ":" in ad:
                kayit, yol = kanca(ad, k)
                d = "kayıt yok" if not kayit else "yalnız kayıt" if not yol else "tamam"
            else:
                bicim = {x.lower() for x in (ad, ad.split("__")[-1], re.sub(r"-(mcp|paket|skill|cli)$", "", ad))}
                d = "boş" if kaynaksiz(adlari(ad, k), m) else "tamam" if any(x in m.lower() or x in k.lower() for x in bicim) else "ait değil"
        except Exception as e:  # noqa: BLE001
            d = f"açılmıyor {type(e).__name__}"
        say[d] = say.get(d, 0) + 1
        if d != "tamam":
            satir.append(f"{ad}\t{d}\t{k}")
    (O / "d14-denetim.tsv").write_text("".join(s + "\n" for s in satir), encoding="utf-8")
    print(f"kalem {len(tum)} (aday satırları hariç {sum(s[1] == 'aday' for s in aday())}) · " + " · ".join(f"{d} {n}" for d, n in sorted(say.items())))
    for s in satir:
        print(s[:150])


def ornek():
    gorulen = set()
    for p in ["d7-ornek.tsv", "d9-ornek-ilk.tsv", "d9-ornek.tsv", "d13-ornek.tsv", "d14-ornek.tsv"]:
        if not (B / p).is_file():
            continue
        gorulen |= {s.split("\t")[0] for s in (B / p).read_text(encoding="utf-8").splitlines()}
    for p in list(O.glob("ozet-token*.jsonl")) + list(O.glob("hakem-*.jsonl")):
        gorulen |= set(oku(p))
    from d9 import acilir
    c = [s for s in (aday() if TOHUM == 11 else katalog_token()) if s[0] not in gorulen and "backup" not in s[0] and acilir(s[3])]
    c = [s for s in c if not kaynaksiz(adlari(s[0], s[3]), metin(s[0], s[3]))]
    sec = random.Random(TOHUM).sample(c, min(28, len(c)))
    K.mkdir(exist_ok=True)
    for s in sec:
        dosya(s[0]).write_text(metin(s[0], s[3]), encoding="utf-8")
    (B / f"{P}-ornek.tsv").write_text("".join("\t".join(s) + "\n" for s in sec), encoding="utf-8")
    print(f"aday {len(c)} (görülen {len(gorulen)} hariç) → {P}-ornek.tsv {len(sec)}: {' · '.join(s[0] for s in sec)}")


def D():
    return dict(s.split("\t")[::3] for s in (B / f"{P}-ornek.tsv").read_text(encoding="utf-8").splitlines())


def paket():
    d = list(D().items())
    for i in range(3):
        parca = []
        for ad, kaynak in d[i::3]:
            m, an = dosya(ad).read_text(encoding="utf-8"), sorted(adlari(ad, kaynak))
            parca += [f"## {ad}", f"kaynak: {dosya(ad)} (çözülmüş; özgün: {kaynak}) · {len(m.splitlines())} satır · araç adları ({len(an)}): {' · '.join(an[:30])}",
                      "BAŞLIKLAR: " + " · ".join(p.split("\n", 1)[0].strip()[:60] for p in BASLIK.split(m)[1:])[:1500], ""]
        (B / f"{P}-paket-{i + 1}.md").write_text("\n".join(parca), encoding="utf-8")
        print(f"{P}-paket-{i + 1}.md · kalem {len(d[i::3])}")


def birlestir():
    c = {}
    for p in sorted(B.glob(f"{P}-yazar-*.jsonl")):
        c.update(oku(p))
    son, ret = {}, {}
    for ad, kaynak in D().items():
        if ad not in c:
            ret[ad] = "yazar satırı yok"
            continue
        m, y = dosya(ad).read_text(encoding="utf-8"), c[ad]
        r = {"ad": ad, "kaynak": str(dosya(ad)), "ozgun": kaynak, **{a: y[a]["deger"] for a in A}, "alinti": {a: y[a].get("alinti", "") for a in A},
             "mekanizma": y["mekanizma"], "kanit": y.get("kanit", ""), "dogrulandi": "claude-yazar"}
        neden, r["uyari"] = sert(r, m, adlari(ad, kaynak))
        if neden:
            ret[ad] = neden
        son[ad] = r
    for ad, h in ret.items():
        print("RET", ad, h, sep="\t")
    for ad, r in son.items():
        for u in r["uyari"]:
            print("UYARI", ad, u, sep="\t")
    (O / f"ozet-token-{P}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in son.values()), encoding="utf-8")
    (O / f"hakem-{P}.jsonl").write_text("".join(json.dumps({k: r[k] for k in ["ad", "kaynak", "ozgun"] + A + ["mekanizma"]}, ensure_ascii=False) + "\n"
                                               for r in son.values()), encoding="utf-8")
    son_t = {r["ad"]: r for q in sorted(O.glob("ozet-token-d14*.jsonl")) for r in oku(q).values()}  # iki tohumun birleşimi
    disi = [r for r in son_t.values() if "token-dışı" in r["mekanizma"]]  # ÖĞREN-0b'ye kategori hatası geri bildirimi
    (O / "token-disi-geri.tsv").write_text("".join(f"{r['ad']}\t{r['ozgun']}\t{r['ne_yapar']}\t{r['kanit']}\n" for r in disi), encoding="utf-8")
    print(f"son {len(son)} · RET {len(ret)} · UYARI {sum(len(r['uyari']) for r in son.values())} · token-dışı {len(disi)}")


if __name__ == "__main__":
    k = sys.argv[1:]
    if k[0] == "t12":
        P, TOHUM, k = "d14-t12", 12, k[1:]
    if k[0] in ("paket", "birlestir", "puan"):
        ozet_kaynak.D = D()
    if k[0] == "puan":
        from d9 import puan
        puan(*k[1:3])
    else:
        {"denetim": denetim, "ornek": ornek, "paket": paket, "birlestir": birlestir}[k[0]]()
