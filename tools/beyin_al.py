"""BEYIN-1 içe alma: kaynak md'leri Obsidian kasasına bölüm notları olarak yazar (model yok).

Kaynaklar silinmez/taşınmaz; kaynak sha'sı değişmediyse not yeniden yazılmaz.
Her not: frontmatter (kaynak, satir, tarih, tur, guven, etiket) + birebir gövde + [[bağlantı]] satırı.
Kullanım: python tools/beyin_al.py [--kasa YOL] [--qmd-yok]
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
KASA = Path(r"C:\Users\pc\Desktop\Obsidian")
BELLEK = Path.home() / ".claude/projects/C--Projeler-omer-skills/memory"
# (klasör, önek, tür, glob)
KAYNAKLAR = [
    ("10-kararlar", "gorev", "gorev", str(KOK / ".kos/kopru/gorev/*.md")),
    ("10-kararlar", "gecmis", "gorev", str(KOK / ".kos/kopru/gorev-gecmis/*.md")),
    ("10-kararlar", "kural", "kural", r"C:\Projeler\omer-kurallar.md"),
    ("10-kararlar", "global", "kural", str(Path.home() / ".claude/CLAUDE.md")),  # yalnız okunur
    ("10-kararlar", "global", "kural", str(Path.home() / ".claude/RTK.md")),
    ("20-ogren", "ogren", "ogren", str(KOK / "docs/ogren/*.md")),
    ("20-ogren", "kogren", "ogren", str(KOK / ".kos/kopru/ogren/*.md")),
    ("30-video", "kurulum", "kurulum", str(KOK / "docs/kurulumlar/*.md")),
    ("40-projeler", "devir", "devir", str(KOK / ".kos/kopru/devir/*.md")),
    ("50-dersler", "ders", "ders", str(BELLEK / "*.md")),
]
PARCA_TAVAN = 30  # satır; başlıksız uzun bölüm bu boyda kesilir


def bol(satirlar):
    """[(baslangic_satir_1tabanli, [satirlar])] — başlıkta ya da PARCA_TAVAN'da böler."""
    parcalar, bas, cur = [], 1, []
    for i, s in enumerate(satirlar, 1):
        if cur and (s.startswith("#") or len(cur) >= PARCA_TAVAN):
            parcalar.append((bas, cur))
            bas, cur = i, []
        cur.append(s)
    if cur:
        parcalar.append((bas, cur))
    return [(b, p) for b, p in parcalar if any(x.strip() for x in p)]


def ad_yap(onek, yol):
    return f"{onek}-" + re.sub(r"[^\w.-]+", "-", Path(yol).stem).strip("-")


def not_metni(kaynak, bas, govde, tarih, tur, etiket, onceki, sonraki):
    kar = any("★" in s for s in govde)
    etiketler = [etiket, tur] + (["karar"] if kar else [])
    fm = ["---", f"kaynak: {kaynak}", f"satir: {bas}", f"tarih: {tarih}", f"tur: {tur}",
          "guven: kaynak-birebir", f"etiket: [{', '.join(etiketler)}]", "---"]
    bag = " · ".join(f"[[{x}]]" for x in (onceki, sonraki, "index") if x)
    return "\n".join(fm + govde + ["", bag]) + "\n"


def yaz(yol, metin):
    yol.parent.mkdir(parents=True, exist_ok=True)
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)


def kaynak_al(kasa, klasor, ad, kaynak, metin, tarih, tur, eski_sayi):
    if tur == "ders":  # bellek notları [[slug]] ile bağlanır; kasada not adı ders-<slug>--1
        metin = re.sub(r"\[\[([^\]|#]+)\]\]", r"[[ders-\1--1|\1]]", metin)
    satirlar = metin.replace("\r\n", "\n").split("\n")
    parcalar = bol(satirlar)
    adlar = [f"{ad}--{i}" for i in range(1, len(parcalar) + 1)]
    for i, (bas, govde) in enumerate(parcalar):
        onceki = adlar[i - 1] if i else None
        sonraki = adlar[i + 1] if i + 1 < len(adlar) else None
        yaz(kasa / klasor / f"{adlar[i]}.md",
            not_metni(kaynak, bas, govde, tarih, tur, ad, onceki, sonraki))
    # kısalan kaynağın artık parçaları silinmez, geçersiz işaretlenir (beyin ara atlar)
    for i in range(len(parcalar) + 1, eski_sayi + 1):
        yaz(kasa / klasor / f"{ad}--{i}.md", f"---\nkaynak: {kaynak}\ngecersiz: true\n---\n")
    return len(parcalar)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--kasa", default=str(KASA))
    ap.add_argument("--qmd-yok", action="store_true")
    ap.add_argument("--zorla", action="store_true", help="sha aynı olsa da yeniden yaz")
    a = ap.parse_args(argv)
    kasa = Path(a.kasa)
    durum_yol = kasa / ".beyin/durum.json"
    durum = json.loads(durum_yol.read_text(encoding="utf-8")) if durum_yol.exists() else {}
    yazilan = atlanan = 0
    harita = {}  # klasör -> [(ad, kaynak, parça)]
    girdiler = []
    for klasor, onek, tur, desen in KAYNAKLAR:
        for yol in sorted(glob.glob(desen)):
            p = Path(yol)
            girdiler.append((klasor, ad_yap(onek, p), str(p), tur, p.read_bytes(),
                             datetime.date.fromtimestamp(p.stat().st_mtime).isoformat()))
    proj = subprocess.run(["video", "projeler"], capture_output=True)
    if proj.returncode == 0 and proj.stdout.strip():
        girdiler.append(("40-projeler", "proje-ozetleri", "video projeler", "proje", proj.stdout,
                         datetime.date.today().isoformat()))
    for klasor, ad, kaynak, tur, ham, tarih in girdiler:
        sha = hashlib.sha256(ham).hexdigest()[:16]
        eski = durum.get(kaynak, {})
        if not a.zorla and eski.get("sha") == sha and (kasa / klasor / f"{ad}--1.md").exists():
            atlanan += 1
            sayi = eski["parca"]
        else:
            sayi = kaynak_al(kasa, klasor, ad, kaynak, ham.decode("utf-8", "replace"), tarih, tur,
                             eski.get("parca", 0))
            durum[kaynak] = {"sha": sha, "parca": sayi, "klasor": klasor, "ad": ad}
            yazilan += 1
        harita.setdefault(klasor, []).append((ad, kaynak, sayi))
    # kaynağı silinmiş notlar: bakım tespit eder, burada dokunulmaz
    endeks = ["# Beyin haritası", "", "Arama: `python tools/beyin.py ara \"<soru>\" --k 5`", ""]
    for klasor in sorted(harita):
        endeks.append(f"## {klasor} ({len(harita[klasor])} kaynak)")
        endeks += [f"- [[{ad}--1]] — `{k}` ({n} parça)" for ad, k, n in harita[klasor]]
        endeks.append("")
    yaz(kasa / "index.md", "\n".join(endeks))
    for k in ("00-cekirdek", "90-log"):
        (kasa / k).mkdir(exist_ok=True)
    simdi = datetime.datetime.now()
    with open(kasa / "90-log" / f"{simdi.date()}.md", "a", encoding="utf-8", newline="\n") as f:
        f.write(f"- {simdi:%H:%M} beyin_al: {yazilan} yazıldı, {atlanan} değişmedi\n")
    yaz(durum_yol, json.dumps(durum, ensure_ascii=False, indent=1))
    print(f"beyin_al: {yazilan} kaynak yazıldı, {atlanan} değişmedi, kasa {kasa}")
    if not a.qmd_yok:
        qmd = shutil.which("qmd")  # Windows'ta qmd.cmd; düz "qmd" bulunmaz
        cols = subprocess.run([qmd, "collection", "list"], capture_output=True, text=True,
                              encoding="utf-8", errors="replace").stdout
        if "qmd://beyin/" not in cols:
            subprocess.run([qmd, "collection", "add", str(kasa), "--name", "beyin",
                            "--mask", "**/*.md"], check=True, capture_output=True)
        subprocess.run([qmd, "update"], check=True, capture_output=True)
        print("qmd: beyin koleksiyonu güncel")


if __name__ == "__main__":
    sys.exit(main())
