"""K16 kayıp kontrolü: büyük çıktının özünden verilen karar = ham çıktıdan (regex) verilen karar mı? 3 örnek.
Ham metin Claude'a girmez; stdout yalnız boyut + iki karar."""
import re, subprocess, sys
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
D = KOK / ".claude/token3/k16"
D.mkdir(exist_ok=True)


def kos(*a, **k):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=KOK, **k)


def ham_karar(t):  # günlüğün son durumu: hata izi var mı, BITTI var mı
    return {"traceback": "Traceback" in t, "bitti": bool(re.search(r"BITTI|BİTTİ", t))}


# 1) pytest günlüğü → jev log (kural tabanlı)
ham = D / "pytest.log"
ham.write_text(kos(sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tools/video/tests").stdout, encoding="utf-8")
t = ham.read_text(encoding="utf-8")
oz = kos("jev", "log", str(ham)).stdout
kirmizi_ham = sorted(set(re.findall(r"^FAILED (\S+?)(?: - |$)", t, re.M)))
print("1 pytest", len(t), "kar → öz", len(oz), "kar")
print("  ham: kırmızı", len(kirmizi_ham), "·", re.findall(r"\d+ (?:passed|failed)", t)[-2:])
print("  öz kırmızıların hepsini içeriyor:", all(k.split("::")[-1] in oz for k in kirmizi_ham))
(D / "pytest-oz.txt").write_text(oz, encoding="utf-8")

# 2–3) büyük köprü günlüğü → ucuz_alt (Claude-dışı)
istem = D / "istem.md"
istem.write_text("Ekteki günlüğü özetle, en çok 8 satır. İlk iki satır tam olarak şu biçimde: `TRACEBACK: evet|hayır` ve "
                 "`BITTI: evet|hayır` (günlükte 'Traceback' ya da 'BITTI'/'BİTTİ' geçiyor mu). Sonra hatalar, sayılar, başarısız kalemler.",
                 encoding="utf-8")
for n, ad in ((2, "kalite3-hiz.log"), (3, "ig41b.log")):
    g = KOK / ".kos/kopru" / ad
    t = g.read_text(encoding="utf-8", errors="replace")
    c = D / f"{ad}.oz.md"
    r = kos(sys.executable, "tools/ucuz_alt.py", str(istem), str(c), str(g), timeout=600)
    oz = c.read_text(encoding="utf-8") if c.exists() else ""
    karar = {"traceback": bool(re.search(r"TRACEBACK:\s*\**evet", oz, re.I)), "bitti": bool(re.search(r"BITTI:\s*\**evet", oz, re.I))}
    print(n, ad, len(t), "kar → öz", len(oz), "kar · rc", r.returncode, r.stdout.strip()[-120:])
    print("  ham", ham_karar(t), "· öz", karar, "· EŞİT" if karar == ham_karar(t) else "· FARKLI")
print("BITTI")
