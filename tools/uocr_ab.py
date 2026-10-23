"""A/B: video_derin RapidOCR ↔ Unlimited-OCR (tools/uocr.py). 20 kare (20 ayrı videonun orta karesi) + 1 PDF.
Kullanım: python tools/uocr_ab.py   (çıktı: .kos/kopru/rapor/uocr-ab/)"""
import json, re, subprocess, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "tools"))
OUT = KOK / ".kos" / "kopru" / "rapor" / "uocr-ab"
OUT.mkdir(parents=True, exist_ok=True)
VPY = r"C:\AI\unlimited-ocr\.venv\Scripts\python.exe"
PDF = r"C:\AI\unlimited-ocr\repo\Unlimited-OCR.pdf"


def sec():
    kareler = []
    for d in sorted((KOK / ".claude" / "ig42").iterdir()):
        ks = sorted((d / "kare").glob("*.jpg"))
        if len(ks) >= 3:
            kareler.append(ks[len(ks) // 2])
    adim = max(1, len(kareler) // 20)
    return kareler[::adim][:20]


def uocr(*args):
    t = time.time()
    r = subprocess.run([sys.executable, str(KOK / "tools" / "uocr.py"), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ist = re.findall(r"uocr: (\{.*\})", r.stderr)
    return r.stdout, (json.loads(ist[-1]) if ist else {}), round(time.time() - t, 1), r.returncode, r.stderr[-400:]


def kume(m):
    return set(re.findall(r"\w{3,}", m.lower()))


def main():
    import video_derin as vd
    ks = sec()
    print(len(ks), "kare", flush=True)
    t = time.time()
    mot = vd.ocr_motor()
    isin = time.time() - t
    rapid = {}
    t = time.time()
    for k in ks:
        res, _ = mot(str(k))
        rapid[k.name] = "\n".join(x[1] for x in res or [])
    rapid_s = time.time() - t
    out, ist, toplam, rc, hata = uocr(*map(str, ks))
    print("uocr kare rc", rc, ist, toplam, hata if rc else "", flush=True)
    # kare başına bölüm: "## ad" başlıkları
    bol = {}
    for p in re.split(r"(?m)^## ", out):
        if p.strip():
            ad, _, govde = p.partition("\n")
            bol[ad.strip()] = govde.strip()
    rows = []
    for k in ks:
        a, b = kume(rapid[k.name]), kume(bol.get(k.name, ""))
        rows.append({"kare": k.name, "rapid_kar": len(rapid[k.name]), "uocr_kar": len(bol.get(k.name, "")),
                     "ortak": len(a & b), "sadece_rapid": len(a - b), "sadece_uocr": len(b - a)})
    (OUT / "kare.json").write_text(json.dumps({"rapid": rapid, "uocr": bol, "satir": rows, "rapid_isin_s": isin, "rapid_s": rapid_s, "uocr_ist": ist}, ensure_ascii=False, indent=1), encoding="utf-8")
    pout, pist, ptop, prc, phata = uocr(PDF, "--dpi", "200")
    (OUT / "pdf.md").write_text(pout, encoding="utf-8")
    ref = subprocess.run([VPY, "-c", "import fitz,sys;d=fitz.open(sys.argv[1]);sys.stdout.reconfigure(encoding='utf-8');print(' '.join(p.get_text() for p in d));[p.get_pixmap(dpi=200).save(sys.argv[2]+'/p%02d.png'%i) for i,p in enumerate(d)]", PDF, str(OUT)],
                         capture_output=True, text=True, encoding="utf-8").stdout
    t = time.time()
    rp = "\n".join("\n".join(x[1] for x in (mot(str(f))[0] or [])) for f in sorted(OUT.glob("p??.png")))
    rapid_pdf_s = time.time() - t
    (OUT / "pdf_rapid.txt").write_text(rp, encoding="utf-8")
    R = kume(ref)
    cov = lambda m: round(len(R & kume(m)) / max(1, len(R)), 3)
    print("PDF kelime kapsama (fitz referansı): uocr", cov(pout), "rapid", cov(rp), "rapid_s", round(rapid_pdf_s, 1), "ref_kelime", len(R))
    print("pdf rc", prc, pist, ptop, len(pout), phata if prc else "")
    print(json.dumps({"rapid_s_kare": round(rapid_s, 1), "uocr": ist, "toplam_kare_s": toplam, "pdf": pist, "pdf_toplam_s": ptop}))
    for r in rows:
        print(r)


main()
