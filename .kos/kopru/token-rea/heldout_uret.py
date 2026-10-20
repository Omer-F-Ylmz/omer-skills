"""Held-out üretici: tohumlu rtk2 komut seti ve sor2 doğal dil TR soru seti BETİKLE üretilir; geliştiren oturum içeriği OKUMAZ.
  python heldout_uret.py rtk2|sor2 <tohum>  → heldout/<tür>_<tohum>.json + .lock (sha256); yalnız sayı basar.
Skor betikleri: rtk2_e2e.py heldout <tohum> · sor2.py heldout <tohum> [genis]. Her kapı YENİ tohum (ör. tarih+sayı: 2010181)."""
import ast, hashlib, json, random, subprocess, sys
from pathlib import Path

BU = Path(__file__).parent
KOK = BU.parents[2]
HO = BU / "heldout"
NW = 0x08000000


def git(*a):
    return subprocess.run(["git", *a], cwd=KOK, capture_output=True, text=True, encoding="utf-8", creationflags=NW).stdout.splitlines()


def dizinler():
    sayi = {}
    for f in git("ls-files"):
        p = f.split("/")[:-1]
        for n in (1, 2):
            if len(p) >= n: sayi["/".join(p[:n])] = sayi.get("/".join(p[:n]), 0) + 1
    return sorted(d for d, n in sayi.items() if 3 <= n <= 400 and not d.startswith(("graphify-out", ".git")))


def rtk2_uret(rng):
    dz, n = dizinler(), int(git("rev-list", "--count", "HEAD")[0])
    h = lambda: rng.randint(1, min(12, n - 1))
    D = lambda: rng.choice(dz)
    kota = [  # (adet, üretici) — find / branch -a / ls / diff kapanmayan hedefler, kalanı karışık
        (2, lambda: (["find", D(), "-type", "f"], None)), (1, lambda: (["find", D(), "-maxdepth", "1", "-name", "*.py"], None)),
        (1, lambda: (["git", "branch", "-a"], "BR")), (3, lambda: (["ls", "-la", D()], None)), (2, lambda: (["git", "diff", f"HEAD~{h()}"], None)),
        (1, lambda: (["git", "diff", f"HEAD~{h()}", "--", D()], None))]
    rast = [lambda: (["git", "status"], "BR"), lambda: (["git", "status", "-s"], "BR"), lambda: (["git", "diff", f"HEAD~{h()}", "--stat"], None),
            lambda: (["git", "log", f"-{rng.randint(5, 25)}", rng.choice(["--stat", "--oneline", "--format=fuller"])], "KONU"),
            lambda: (["git", "show", f"HEAD~{h()}", "--stat"], None), lambda: (["git", "ls-files", D()], None),
            lambda: (["git", "branch", "-vv"], "BR"), lambda: (["ls", "-la", D()], None), lambda: (["find", D(), "-type", "f"], None)]
    cik, gor = [], set()
    for adet, f in [*kota, *[(1, rng.choice(rast)) for _ in range(5)]]:
        for _ in range(adet):
            argv, k = f()
            if " ".join(argv) not in gor:
                gor.add(" ".join(argv)); cik.append(["G " + " ".join(argv)[:40], argv, k])
    return cik


def ilk_satir(yol):
    try:
        src = (KOK / yol).read_text(encoding="utf-8", errors="ignore")
        d = ast.get_docstring(ast.parse(src)) or next((l.lstrip("# ").strip() for l in src.splitlines() if l.startswith("#") and len(l) > 25), "")
    except (SyntaxError, OSError):
        return ""
    return d.splitlines()[0][:180] if d else ""


def sor2_uret(rng, n=10):
    adaylar = [f for f in git("ls-files", "-co", "--exclude-standard") if f.endswith(".py") and f.startswith(("tools/", ".kos/kopru/", "onay/", "mcp/"))]
    rng.shuffle(adaylar)
    secim = []
    for f in adaylar:
        s, ad = ilk_satir(f), Path(f).stem
        if len(s) >= 30 and len(ad) >= 5 and ad.lower() not in s.lower() and not any(Path(g).stem == ad for g, *_ in secim):
            secim.append((f, ad, s))
        if len(secim) == n: break
    sys.path.insert(0, str(KOK / "tools")); import ucretsiz_havuz as H
    ist = ("Aşağıdaki numaralı satırlar birer betik açıklaması. Her birini, bir geliştiricinin o betiği bulmak için yazacağı KISA Türkçe soruya "
           "(en çok 12 sözcük) yeniden ifade et: açıklamadaki sözcükleri birebir kopyalama, eş anlamlı kullan, dosya adı uydurma. "
           "Çıktı yalnız satırlar, aynı sırayla, numarasız.\n" + "\n".join(f"{i + 1}. {s}" for i, (_, _, s) in enumerate(secim)))
    y, kaynak, _ = H.cagir("ozet", ist, max_tokens=900, haiku_tavan=0, etiket="heldout-sor2",
                           dogrula=lambda m: None if len([l for l in m.strip().splitlines() if l.strip()]) == len(secim) else "satır sayısı")
    if y:
        sor = [l.strip().lstrip("0123456789.) ") for l in y.strip().splitlines() if l.strip()]
    else:  # havuz yok: açıklama satırı doğrudan soru (dosya adı zaten içinde yok), yeniden ifade yok
        sor, kaynak = [s for _, _, s in secim], "yok"
    return [[q, ad] for q, (_, ad, _) in zip(sor, secim)], kaynak


if __name__ == "__main__":
    tur, tohum = sys.argv[1], sys.argv[2]
    rng = random.Random(f"{tur}-{tohum}")
    liste, kaynak = (rtk2_uret(rng), "betik") if tur == "rtk2" else sor2_uret(rng)
    HO.mkdir(exist_ok=True)
    (HO / f"{tur}_{tohum}.json").write_text(json.dumps(liste, ensure_ascii=False), encoding="utf-8")
    (HO / f"{tur}_{tohum}.lock").write_text(hashlib.sha256(json.dumps(liste, ensure_ascii=False).encode()).hexdigest(), encoding="utf-8")
    print(tur, tohum, "n", len(liste), "kaynak", kaynak)
