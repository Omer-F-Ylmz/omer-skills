"""K36-GENISLET-1 kapısı: 6 iş türü · özet jetonu (1500-2500) · recall (A: sirali.tsv tam tarama altını, B: bağımsız altın) · kategori kapsamı.
  python -I .kos/kopru/kaynak-dizin/k36_olc.py"""
import json
import re
import subprocess
import sys
from pathlib import Path

import tiktoken

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK / "tools"))
import kategori_tara as K  # noqa: E402

D = K.DIZIN
ISLER = {  # iş türü: (sorgu, harita anahtarı, B: bağımsız altın)
    "site": ("site yap landing sayfası scroll animasyonlu", "site",
             ["frontend-craft", "departman-frontend", "impeccable", "ui-ux-pro-max", "taste-skill", "fe-site-mimarisi", "playwright", "rea", "tasarim-katalog", "omer-kutuphaneler", "fe-webgl-3d-hero", "kombin-rehber", "headroom-compress"]),
    "video": ("video üret kurgu altyazı remotion render ses", "gorsel-video-ses-3d",
              ["hyperframes-paket", "remotion-video-creation", "ffmpeg", "yt-dlp", "video-uygula", "pixeljury", "general-video", "embedded-captions", "kombin-rehber"]),
    "kurulum": ("yeni araç kurulum install model indir comfyui", "kurulum",
                ["liste_cikar", "ucretsiz_havuz", "model-kur-1", "medya-kur-2", "ComfyUI", "h3-hiz-1", "video-izle-kur-1"]),
    "kod": (".NET API backend efcore test yaz", "kod",
            ["departman-backend-dotnet", "dn-webapi-endpoint", "dn-minimal-api-kurucu", "dn-efcore-modelleme", "dn-efcore-migration", "dn-xunit-test-yazar", "dn-identity-auth", "dn-openapi-dokuman", "departman-test-qa", "gitleaks", "semgrep"]),
    "otomasyon": ("otomasyon instagram sosyal bot telegram n8n zamanlanmış görev", "otomasyon",
                  ["n8n", "arka_sira", "Telegram", "Instagram", "zapier", "Composio"]),
    "araştırma": ("araştırma raporu kaynak tarama deep research", "arastirma",
                  ["deep-research", "web-research", "firecrawl", "tavily", "ucretsiz-video-siteleri"]),
}


def calis(q):
    return subprocess.run([sys.executable, "-I", str(KOK / "tools/envanter_tara.py"), q, "--yenile"], capture_output=True, encoding="utf-8", errors="replace").stdout


def sirali():
    return [s.split("\t") for s in (D / "sirali.tsv").read_text(encoding="utf-8").splitlines()[1:] if s.count("\t") == 10]


def main():
    sr = sirali()
    enc = tiktoken.get_encoding("cl100k_base")
    adlar = {r[8].lower() for r in sr}
    toplam = [0, 0, 0, 0]
    for ad, (q, hk, b) in ISLER.items():
        out = calis(q)
        low = out.lower()
        jt = len(enc.encode(out))
        # A: kayıpsız özet doğrulaması = tam tarama (43k kalem, iş sorgusuna göre kategori başına en ilgili 3) ↔ özetteki ad
        sira = K.kategori_siralama(q)
        ga = [(k, a[:26].lower()) for k, (n, kan, l, hm) in sira.items() if hm and hm in (True,) for _, a in l]
        a_ok = [g for g in ga if g[1] in low]
        # B: bağımsız altın (geçmiş gerçek seçim / elle kanıtlı kalemler); dizinde hiç yoksa 'yok' sayılır, paydaya girmez
        var = [g for g in b if any(g.lower() in x for x in adlar)]
        yok = [g for g in b if g not in var]
        b_ok = [g for g in var if g.lower() in low]
        kat_tum = {int(r[0]) for r in sr if int(r[0]) > 0}
        kat_out = {int(m) for m in re.findall(r"(?m)^k(\d+) ", out)}
        print(f"{ad}: jeton {jt} · A {len(a_ok)}/{len(ga)} eksik={[g for g in ga if g not in a_ok][:6]} · B {len(b_ok)}/{len(var)} eksik={[g for g in var if g not in b_ok]} dizinde-yok={yok} · kategori satırı özette {len(kat_out)}/{len(kat_tum)} eksik={sorted(kat_tum - kat_out)}")
        toplam[0] += len(a_ok); toplam[1] += len(ga); toplam[2] += len(b_ok); toplam[3] += len(var)
    print(f"RECALL A {toplam[0]}/{toplam[1]} = {toplam[0] / max(toplam[1], 1):.0%} · B {toplam[2]}/{toplam[3]} = {toplam[2] / max(toplam[3], 1):.0%}")


main()
