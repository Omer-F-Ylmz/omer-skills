"""ROUTER-1 ölçümü: 3 sınıf × 2 kol (A = bugünkü düz `claude -p --model sonnet`, B = model_sec) × 2 tekrar = 12 çağrı (tavan).
Kalite deterministik denetimle (beklenen yanıt), maliyet result JSON'undaki usage/total_cost_usd ile. Ham çıktı dosyaya yazılır
(belleğe biriktirilmez); RAM %95 altına inmezse (≤30 dk bekleme) çağrı yapılmaz. Koşum: arka.py <günlük> olcum_sira.py tools/olcum/router1_olc.py <çıktı_dizini>"""
import ctypes
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model_sec  # noqa: E402

CAGRI_TAVAN, USD_TAVAN = 12, 0.6  # çağrı başı --max-budget-usd; toplam ≤ $7.2 abonelik içi
TSV = """anahtar\tlisans\tyildiz
omniroute\tMIT\t1200
litellm\tMIT\t30000
routellm\tApache-2.0\t4000
martian\t-\t-
helicone\tApache-2.0\t4500
notdiamond\tticari\t-
portkey\tMIT\t9000
ccr\tMIT\t20000"""
KOD = '''def ortalama_pencere(xs, k):
    """xs üzerinde k uzunluklu kayan pencerelerin ortalamaları."""
    return [sum(xs[i:i + k]) / k for i in range(len(xs) - k)]'''
GOREV = {
    "mekanik": ("Aşağıdaki TSV'de lisansı MIT olan satırların anahtar alanlarını, TSV sırasıyla, yalnız JSON dizi olarak yaz "
                "(başka metin yok).\n\n" + TSV,
                lambda y: _json(y) == ["omniroute", "litellm", "portkey", "ccr"]),
    "ozet": ("Aşağıdaki fonksiyonun ne yaptığını tek cümleyle özetle; sonra ayrı satırda 'HATA: <var/yok>' yaz.\n\n" + KOD,
             lambda y: "HATA: var" in y.replace("**", "")),
    "yargi": ("Fonksiyondaki hatayı düzelten seçeneği seç. Yalnız harfi yaz.\n\n" + KOD +
              "\n\nA) range(len(xs) - k - 1)\nB) range(len(xs) - k + 1)\nC) range(1, len(xs) - k)\nD) hata yok",
              lambda y: y.strip().strip("*").strip().upper().startswith("B")),
}


def _json(y):
    try:
        return json.loads(y[y.index("["): y.rindex("]") + 1])
    except ValueError:
        return None


def ram():
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(f"x{i}", ctypes.c_ulonglong) for i in range(7)]
    m = M(); m.l = ctypes.sizeof(M)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.yuk


def kol(ad, sinif):
    if ad == "A":
        return ["--model", "sonnet", "--max-turns", "3"]
    return model_sec.bayraklar(sinif)


def main(cikti):
    cikti = Path(cikti); cikti.mkdir(parents=True, exist_ok=True)
    satirlar, n = ["sinif\tkol\ttekrar\tdogru\tgirdi\tcache_yaz\tcache_oku\tcikti\tusd\tsure_ms\thata"], 0
    for t in (1, 2):
        for sinif, (istem, denet) in GOREV.items():
            for ad in ("A", "B"):
                for _ in range(30):  # RAM %95 altına inene dek ≤30 dk bekle (Ömer 17:16: %97'ye kadar serbest, %2 pay)
                    if ram() < 95:
                        break
                    time.sleep(60)
                if n >= CAGRI_TAVAN or ram() >= 95:
                    satirlar.append(f"{sinif}\t{ad}\t{t}\t-\t\t\t\t\t\t\tatlandi(ram/tavan)"); continue
                n += 1
                ham = cikti / f"{sinif}-{ad}-{t}.json"
                with open(ham, "w", encoding="utf-8") as f:
                    subprocess.run(["claude", "-p", istem, "--output-format", "json", "--max-budget-usd", str(USD_TAVAN), *kol(ad, sinif)],
                                   stdout=f, stderr=subprocess.STDOUT, timeout=600, stdin=subprocess.DEVNULL)
                try:
                    d = json.loads(ham.read_text(encoding="utf-8"))
                except ValueError:
                    satirlar.append(f"{sinif}\t{ad}\t{t}\t0\t\t\t\t\t\t\tjson-yok"); continue
                u = d.get("usage", {})
                satirlar.append("\t".join(map(str, [sinif, ad, t, int(bool(denet(d.get("result", "") or ""))), u.get("input_tokens"),
                                u.get("cache_creation_input_tokens"), u.get("cache_read_input_tokens"), u.get("output_tokens"),
                                d.get("total_cost_usd"), d.get("duration_ms"), d.get("subtype") if d.get("is_error") else ""])))
                (cikti / "olcum.tsv").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    (cikti / "olcum.tsv").write_text("\n".join(satirlar) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
