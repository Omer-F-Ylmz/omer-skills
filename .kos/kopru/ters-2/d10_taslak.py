"""d10: 11 hedef için ground truth TASLAĞI — ücretsiz havuz (ucuz_alt --tur ozet), satır numaralı kopyalarla."""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path("C:/Projeler/omer-skills")
U = "C:/Projeler/uygulamalar"
J = KOK / "templates/jev-dotnet"
OUT = KOK / ".claude/ordu3/gt"
BILESEN = ("(1) akış sırası (2) sabit/veri tablosu (3) dış bağımlılık/HTTP/ortam davranışı "
           "(4) tür/örüntü envanteri (5) sınır/eşik durumu")
HEDEF = {
    "ink-theater": ("js", [f"{U}/openmontage/ink-theater/ink-theater.js"], "Ink Theater sahne oynatıcısı nasıl yapılmış?"),
    "cortex": ("js", [f"{U}/colibri/web/src/lib/cortex.ts"], "cortex.ts ne yapıyor, nasıl çalışıyor?"),
    "images": ("js", [f"{U}/colibri/web/src/lib/images.ts"], "images.ts ne yapıyor, nasıl çalışıyor?"),
    "transcript": ("js", [f"{U}/colibri/web/src/lib/transcript.ts"], "transcript.ts ne yapıyor, nasıl çalışıyor?"),
    "presets": ("js", [f"{U}/thinking-orbs/src/presets.ts"], "thinking-orbs presets.ts nasıl kurulu?"),
    "Jev": ("dotnet", sorted(str(p).replace("\\", "/") for p in (J / "Jev").glob("*.cs")), "Jev kütüphanesi nasıl çalışıyor?"),
    "Jev.Tests": ("dotnet", sorted(str(p).replace("\\", "/") for p in (J / "Jev.Tests").glob("*.cs")), "Jev.Tests testleri neyi sınıyor?"),
    "NativeAotFixture": ("dotnet", [str(KOK / ".kos/kopru/ters-2/d9-dn/nativeaot/Program.cs").replace("\\", "/")], "NativeAotFixture ne yapıyor?"),
    "giris-scroll": ("site", [str(KOK / "skills/animasyon-atolyesi/tarifler/giris-scroll.html").replace("\\", "/")], "Scroll ile sürülen giriş animasyonu nasıl yapılmış?"),
    "sayfa-gecisi": ("site", [str(KOK / "skills/animasyon-atolyesi/tarifler/sayfa-gecisi.html").replace("\\", "/")], "Sayfa geçişi (view transition) nasıl yapılmış?"),
    "parcacik-three": ("site", [str(KOK / "skills/animasyon-atolyesi/tarifler/parcacik-three.html").replace("\\", "/")], "three.js parçacık sahnesi nasıl yapılmış?"),
}


def numarali(ad, kaynaklar):
    d = OUT / ad
    d.mkdir(parents=True, exist_ok=True)
    yollar = []
    for k in kaynaklar:
        satirlar = Path(k).read_text(encoding="utf-8", errors="replace").splitlines()
        p = d / Path(k).name
        p.write_text("\n".join(f"{i}: {s}" for i, s in enumerate(satirlar, 1)), encoding="utf-8")
        yollar.append(str(p))
    return yollar


def calis(ad):
    tur, kaynaklar, soru = HEDEF[ad]
    yollar = numarali(ad, kaynaklar)
    istem = (f"Hedef: {ad}. Soru: {soru}\nDosyalar satır numaralıdır ('N: metin'). Ground truth için TAM 5 madde üret; "
             f"her biri farklı bileşen: {BILESEN} (site ise: mekanizma, değerler, bağımlılık, durum, sınır). "
             "Her madde somut/doğrulanabilir bir iddia olsun. Kanıt: tek satırlık, dosyadan BİREBİR alıntı "
             "(satır numarası öneki hariç, ≤110 karakter), doğru satır numarasıyla. "
             'ÇIKTI: ozet alanı düz anlatı OLMAMALI; yalnız çift tırnaklı geçerli JSON liste (5 öğe): [{"madde":"...","dosya":"<dosya adı>","satir":N,"alinti":"..."}]')
    cikti = OUT / f"{ad}.md"
    r = subprocess.run([sys.executable, str(KOK / "tools/ucuz_alt.py"), "--tur", "ozet", istem, str(cikti), *yollar],
                       capture_output=True, text=True, encoding="utf-8")
    return ad, r.returncode, (r.stdout + r.stderr).strip()[-200:]


if __name__ == "__main__":
    adlar = sys.argv[1:] or list(HEDEF)
    with ThreadPoolExecutor(4) as ex:
        for ad, rc, son in ex.map(calis, adlar):
            print(ad, rc, son.replace("\n", " | "))
