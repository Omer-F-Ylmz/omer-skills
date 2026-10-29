"""ÖĞREN-2.tur d2 kombo A/B (betikli, model yok): tk-kod-sorusu · gv-sizinti-sast · tq-e2e-gorsel-regresyon.
Her kol: kalite · token (çıktı bayt/4) · süre (sn) · kullanış (adım sayısı). Sonuç .claude/ogren-tur2-d2/olc.json."""
import ast, json, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
CIK = KOK / ".claude/ogren-tur2-d2/olc.json"


def kos(komut, **kw):
    t = time.time()
    p = subprocess.run(komut, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=kw.pop("cwd", KOK), **kw)
    return (p.stdout or "") + (p.stderr or ""), time.time() - t


def tok(s):
    return len(s.encode("utf-8")) // 4


def kod_sorusu():
    # held-out: tools/*.py dosyalarından betikle 10 örnek; soru = docstring ilk cümlesi, cevap = o dosya
    import random
    dos = sorted(p for p in (KOK / "tools").glob("*.py"))
    ornek = []
    for p in dos:
        d = ast.get_docstring(ast.parse(p.read_text(encoding="utf-8", errors="replace")))
        if d and len(d) > 60:
            ornek.append((p.name, re.split(r"[.:\n]", d)[0][:140]))
    ornek = random.Random(21).sample(ornek, 10)
    a = dict(isabet=0, bayt=0, sure=0.0, adim=0)  # kombo: sor2 -> (yetmezse) graphify query
    b = dict(isabet=0, bayt=0, sure=0.0, adim=0)  # rakip: git grep, en uzun 2 sözcük
    for dosya, soru in ornek:
        o, s = kos([sys.executable, "-X", "utf8", "-I", "-S", ".kos/kopru/token-rea/sor2.py", soru], timeout=120)
        a["bayt"] += len(o.encode()); a["sure"] += s; a["adim"] += 1
        hit = dosya in o
        if not hit:
            o2, s2 = kos(["graphify", "query", soru], timeout=120)
            a["bayt"] += len(o2.encode()); a["sure"] += s2; a["adim"] += 1
            hit = dosya in o2
        a["isabet"] += hit
        sz = sorted(set(re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]{5,}", soru)), key=len, reverse=True)[:2]
        sz = sz or ["tools"]
        o3, s3 = kos(["git", "grep", "-l", "-i", "-e", sz[0], "--", "tools"] if len(sz) < 2 else
                     ["git", "grep", "-l", "-i", "--all-match", "-e", sz[0], "-e", sz[1], "--", "tools"], timeout=60)
        b["bayt"] += len(o3.encode()); b["sure"] += s3; b["adim"] += 1
        b["isabet"] += dosya in o3
    return dict(n=len(ornek), kombo=a, rakip=b)


TOHUM = {
    "gizli_aws.py": 'AWS_KEY = "AKIAIOSFODNN7EXAMPLE"\nAWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"\n',
    "gizli_gh.env": "GITHUB_TOKEN=ghp_" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8\n",
    "gizli_slack.txt": "slack = " + "xoxb-123456789012-1234567890123-AbCdEfGhIjKlMnOpQrStUvWx\n",
    "zaf_eval.py": "import sys\nprint(eval(sys.argv[1]))\n",
    "zaf_shell.py": "import subprocess, sys\nsubprocess.call('ls ' + sys.argv[1], shell=True)\n",
    "zaf_yaml.py": "import yaml, sys\nprint(yaml.load(open(sys.argv[1])))\n",
    "temiz.py": "def topla(a, b):\n    return a + b\n",
}
SIR = ("gizli_aws.py", "gizli_gh.env", "gizli_slack.txt")
ZAF = ("zaf_eval.py", "zaf_shell.py", "zaf_yaml.py")


def sizinti():
    d = Path(tempfile.mkdtemp(prefix="tur2d2-"))
    for ad, ic in TOHUM.items():
        (d / ad).write_text(ic, encoding="utf-8")
    o, s = kos(["semgrep", "scan", "--config", "auto", "--quiet", str(d)], timeout=300)
    sem = dict(o=o, s=s)
    o2, s2 = kos(["gitleaks", "detect", "--no-git", "-s", str(d), "--redact", "--no-banner", "-f", "json", "-r", "-"], timeout=120)
    sonuc = {}
    for ad, dosyalar, metin, sure, adim in (("rakip", SIR + ZAF, sem["o"], sem["s"], 1),
                                            ("kombo", SIR + ZAF, sem["o"] + o2, sem["s"] + s2, 2)):
        yak = [f for f in dosyalar if f in metin]
        sonuc[ad] = dict(yakalanan=len(yak), toplam=6, yakalanan_adlar=yak, yanlis_alarm="temiz.py" in metin,
                         token=tok(metin), sure=round(sure, 1), adim=adim)
    return sonuc  # geçici dizin silinmez (SİLME YOK); sistem temp'i temizler


SAYFALAR = {
    "renk": ('<h1 id=b style="color:#111">Merhaba</h1>', '<h1 id=b style="color:#c00">Merhaba</h1>'),
    "kayma": ('<div style="height:40px"></div><button id=b>Gönder</button>', '<div style="height:90px"></div><button id=b>Gönder</button>'),
    "gizle": ('<p id=b>Kayıt tamam</p>', '<p id=b style="display:none">Kayıt tamam</p>'),
}


def gorsel():
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageChops
    import io
    r = dict(assert_yakalar=0, gorsel_yakalar=0, yanlis_alarm_assert=0, yanlis_alarm_gorsel=0)
    t_as = t_gv = 0.0
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        sy = br.new_page(viewport=dict(width=400, height=300))

        def gor(html):
            sy.set_content("<body style='margin:0'>" + html)
            return sy.is_visible("#b"), sy.inner_text("#b"), sy.screenshot()
        for ad, (ref, deg) in SAYFALAR.items():
            t = time.time(); v0, m0, _ = gor(ref); v1, m1, _ = gor(deg); t_as += time.time() - t
            r["assert_yakalar"] += (v0, m0) != (v1, m1)
            t = time.time(); _, _, p0 = gor(ref); _, _, p1 = gor(deg); _, _, p2 = gor(ref)
            fark = lambda x, y: ImageChops.difference(Image.open(io.BytesIO(x)).convert("RGB"), Image.open(io.BytesIO(y)).convert("RGB")).getbbox() is not None
            r["gorsel_yakalar"] += fark(p0, p1) or (v0, m0) != (v1, m1)
            r["yanlis_alarm_gorsel"] += fark(p0, p2)  # aynı sayfa iki kez
            t_gv += time.time() - t
        br.close()
    return dict(rakip=dict(yakalanan=r["assert_yakalar"], toplam=3, yanlis_alarm=0, sure=round(t_as, 2), token=None, adim=1),
                kombo=dict(yakalanan=r["gorsel_yakalar"], toplam=3, yanlis_alarm=r["yanlis_alarm_gorsel"], sure=round(t_as + t_gv, 2), token=None, adim=3))


if __name__ == "__main__":
    out = {}
    for ad, f in (("tk-kod-sorusu", kod_sorusu), ("gv-sizinti-sast", sizinti), ("tq-e2e-gorsel-regresyon", gorsel)):
        try:
            out[ad] = f()
        except Exception as e:  # ölçüm düzeneği düştü: sonuç yok, uydurma yok
            out[ad] = dict(hata=f"{type(e).__name__}: {e}"[:300])
        print(ad, json.dumps(out[ad], ensure_ascii=False)[:700], flush=True)
    CIK.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
