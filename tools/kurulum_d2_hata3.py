"""D2-HATA-2: hata2 sonrası kalan HATA'lar. Her satır 'kanit' sütununda kanıt taşır; sıkıştırma kilidi (EBUSY) HATA sayılmaz.
Kullanım: python tools/kurulum_d2_hata3.py [--bolum llm,bin,misc,ebusy]"""
import json, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kurulum_d2_hata2 as H  # sys.argv'yi --tur2'ye çevirir, kurulum_d2'yi D olarak yükler

D = H.D
BOL = set(H._a[H._a.index("--bolum") + 1].split(",")) if "--bolum" in H._a else {"llm", "bin", "misc", "ebusy"}
son, hata, yaz, GROOT = H.son, H.hata, H.yaz, H.GROOT


def bolum_llm():
    D.YEDEK_TAVAN["max"] = 30  # sayısal tavan: yedek (OmniRoute dışı) en fazla 30 çağrı; OmniRoute yerel
    for r in [r for r in son().values() if hata(r, r"LLM-ERISILEMEDI")]:
        D.isle(next(x for x in D.oku(D.KOK / "kurulum-coz.tsv") if x["kalem"] == r["kalem"]))
    print("LLM yedek çağrı sayacı:", D.YEDEK_TAVAN["n"], "/", D.YEDEK_TAVAN["max"])


def bolum_bin():
    """npm -g kuruldu, bin yok: yol boş olabilir (npm:ad kaynağı) -> global köke bak; require/import ya da npm script ile sınıfla."""
    for r in [r for r in son().values() if hata(r, r"bin' tan")]:
        d = Path(r["yol"]) if r["yol"] else None
        ad = r["kaynak"].split(":", 1)[1] if r["kaynak"].startswith("npm:") else None
        if d and (d / "package.json").exists():
            ad = json.loads((d / "package.json").read_text(encoding="utf-8", errors="ignore")).get("name", ad)
        g = Path(GROOT) / (ad or "?")
        if not (g / "package.json").exists():
            yaz(r, "HATA", f"global bağ yok ({ad})", f"{g} yok"); continue
        pj = json.loads((g / "package.json").read_text(encoding="utf-8", errors="ignore"))
        c, o = D.run(["node", "-e", "require(process.argv[1]);console.log('ok')", str(g)], 60)
        if c == 0:
            yaz(r, "KURULDU-KUTUPHANE", f"require('{ad}') ok (bin yok: kütüphane)", f"node require {g} -> ok"); continue
        main = pj.get("main") or (pj["exports"] if isinstance(pj.get("exports"), str) else None)
        if main and (g / main).exists():
            c, o = D.run(["node", "--input-type=module", "-e", "import(process.argv[1]).then(()=>console.log('ok'))", (g / main).resolve().as_uri()], 60)
            if c == 0:
                yaz(r, "KURULDU-KUTUPHANE", f"ESM import('{ad}') ok (bin yok: kütüphane)", f"node import {main} -> ok"); continue
        sc = [s for s in ("start", "dev", "build", "serve", "setup") if s in pj.get("scripts", {})]
        if sc:
            yaz(r, "KURULDU-KAYNAK", f"uygulama/monorepo kaynağı global bağlandı; komut yok, çalıştırma: npm run {sc[0]} ({ad})", f"{g} var; scripts={sc}; require başarısız: {D.kok(o)[:100]}"); continue
        if main and (g / main).exists():
            yaz(r, "KURULDU-KAYNAK", f"uygulama kaynağı global bağlandı; bin yok, giriş {main}: node {main}", f"{g}/{main} var; package.json main={main}, bin/start yok; require: {D.kok(o)[:100]}"); continue
        yaz(r, "HATA", f"bin yok, require/import başarısız, script yok ({ad}): {D.kok(o)[:120]}", f"main={main}")


def bolum_misc():
    S = son()
    r = S.get("Aider-AI/aider")
    if r and r["durum"] == "KURULDU-DOGRULANMADI":
        ok, n = D.dogrula([str(D.BIN / "aider.exe")])
        yaz(r, "KURULDU" if ok else "KURULDU-DOGRULANMADI", "uv tool py3.12; " + n, n)
    r = S.get("Bar Replay")
    if r and r["durum"] == "HATA":
        g = Path(GROOT) / "BarReplay"; pj = json.loads((g / "package.json").read_text(encoding="utf-8"))
        yaz(r, "KURULDU-KAYNAK", f"express/redis uygulama kaynağı global bağlandı; bin yok, giriş {pj.get('main')}: node {pj.get('main')}", f"{g} var; package.json main={pj.get('main')}, bin yok, redis bağımlılığı")
    park = Path(__file__).resolve().parents[1] / ".kos/kopru/park"
    for k, ek in (("ValueCell", "ValueCell"), ("nexu-io/open-design", "open-design"), ("Fincept-Corporation/FinceptTerminal", "FinceptTerminal")):
        r = S.get(k)
        if r and r["durum"] in ("KURULDU-DOGRULANMADI", "HATA"):
            p = [q.name for q in park.glob(ek + "*.kurulum")]
            yaz(r, "KURULUM-YOLU-ELLE", "GUI kurulum programı (setup.exe) park/ içinde; çalıştırılmadı; elle kurulur", f"park: {p}", "")
    r = S.get("Triton")
    if r and r["durum"] == "HATA":
        yaz(r, "KURULUM-YOLU-YOK", "triton>=2.2 için win_amd64 wheel yok (yalnız manylinux x86_64/aarch64); Windows'ta kurulamaz", "uv pip install --dry-run triton (py3.12): 'no wheels matching platform tag win_amd64'; triton 3.9.0 yalnız manylinux")
    r = S.get("oMLX")
    if r and r["durum"] == "HATA":
        yaz(r, "KURULUM-YOLU-YOK", "yalnız Apple Silicon/macOS (MLX); Windows'ta kurulamaz", "jundot__omlx README: badge platform-Apple Silicon; pyproject 'Operating System :: MacOS'; mlx-audio git bağımlılığı indirilemedi")
    r = S.get("LEANN")
    if r and r["durum"] == "HATA":
        c, o = D.run(["uv", "tool", "install", "--python", "3.12", "--force", "leann"], 900)
        if c: yaz(r, "HATA", "uv tool py3.12: " + D.kok(o)[:140], D.kok(o)[:250])
        else:
            ok, n = D.dogrula([str(D.BIN / "leann.exe")])
            yaz(r, "KURULDU" if ok else "KURULDU-DOGRULANMADI", "uv tool install --python 3.12 leann; " + n, n)
    r = S.get("Paddle")
    if r and r["durum"] == "HATA":
        v = D.VENVK.parent / "ana-liste312-paddle"
        c, o = D.run(["uv", "venv", "-q", "--python", "3.12", str(v)], 120)
        c, o = D.run(["uv", "pip", "install", "--python", str(v / "Scripts/python.exe"), "paddlepaddle"], 900) if c == 0 else (c, o)
        c2, o2 = D.run([str(v / "Scripts/python.exe"), "-c", "import paddle;print(paddle.__version__)"], 180) if c == 0 else (1, o)
        if c2 == 0: yaz(r, "KURULDU-KUTUPHANE", f"pip:paddle yanlış PyPI projesi (snapy bağımlılığı cp312 wheel yok); paddlepaddle py3.12 venv'de kuruldu, import paddle {o2.strip()[-20:]}", f"{v}: import paddle -> {o2.strip()[-40:]}")
        else: yaz(r, "HATA", "paddlepaddle: " + D.kok(o2 or o)[:130], D.kok(o2 or o)[:250])


def bolum_ebusy():
    """Sıkıştırma (compact.exe) sürerken npm rename EBUSY verir: 3 deneme + 30 sn; hâlâ EBUSY ise HATA değil, SIKISTIRMA-SONRASI-YENIDEN."""
    ilk = True
    for r in [r for r in son().values() if hata(r, r"EBUSY")]:
        ad = r["kaynak"].split(":", 1)[1] if r["kaynak"].startswith("npm:") else None
        d = Path(r["yol"]) if r["yol"] else None
        hedef = ad or str(d)
        for den in range(3 if ilk else 1):
            with D.NPMKILIT:
                c, o = D.run(["npm.cmd", "i", "--prefix", str(D.NPMDIR), "--no-audit", "--no-fund", hedef], 600)
            if c == 0 or "EBUSY" not in o:
                break
            time.sleep(30)
        ilk = False
        if c and "EBUSY" in o:
            yaz(r, "SIKISTIRMA-SONRASI-YENIDEN", "npm rename EBUSY: eşzamanlı NTFS sıkıştırma kilidi (compact.exe sürüyor); sıkıştırma bitince yeniden kurulacak", D.npm_kok(o)[:250]); continue
        if c:
            yaz(r, "HATA", "npm: " + D.npm_kok(o)[:120], D.npm_kok(o)[:250]); continue
        ok, n = D.npm_dogrula(ad) if ad else (True, "npm install ok")
        yaz(r, "KURULDU" if ok else "HATA", n, n)


if __name__ == "__main__":
    for b in ("llm", "bin", "misc", "ebusy"):
        if b in BOL:
            print("== bölüm", b, flush=True)
            try:
                globals()["bolum_" + b]()
            except Exception as e:
                print("BÖLÜM HATA", b, type(e).__name__, str(e)[:200], flush=True)
    from collections import Counter
    print("TOPLAM:", dict(Counter(r["durum"] for r in son().values())))
