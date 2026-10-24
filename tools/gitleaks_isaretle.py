"""p1b-gitleaks.md'yi sınıflar: yüksek güvenli kural + test/örnek dışı yol = GERÇEK-SIR-SUPHESI (kurulum listesinden çıkar, silme yok).
Çıktı: .kos/kopru/ara/p1b-gitleaks-isaret.md (sır değeri içermez; girdi zaten yalnız kural+yol taşır)."""
import re
from pathlib import Path

ARA = Path(__file__).resolve().parent.parent / ".kos/kopru/ara"
ZAYIF = {"generic-api-key", "jwt", "curl-auth-header", "private-key"}  # örnek/test'te çok sık
BENIGN_YOL = re.compile(r"test|spec|example|sample|fixture|mock|demo|docs?/|\.md|testdata|\.gitallowed|lock|\.obsidian|node_modules|vendor|provenance", re.I)

supheli, ozel_ama_benign, kurulur = [], [], []
for satir in (ARA / "p1b-gitleaks.md").read_text(encoding="utf-8").splitlines()[1:]:
    m = re.match(r"(\S+): (\d+) bulgu; kurallar=\[(.*?)\]; ornek=(.*)", satir)
    if not m:
        continue
    ad, n, yol = m[1], int(m[2]), m[4]
    kurallar = {r.strip("' ") for r in m[3].split(",")}
    ozel = kurallar - ZAYIF
    if ozel and not BENIGN_YOL.search(yol):
        supheli.append((ad, n, sorted(ozel), yol))
    elif ozel:
        ozel_ama_benign.append(ad)
    else:
        kurulur.append(ad)

cikti = [f"# p1b-gitleaks işaret (24 Eki)", f"- GERÇEK-SIR-SUPHESI (kurulumdan çıkar, doğrulanmadı): {len(supheli)}",
         f"- özel kural ama test/örnek yolu (kurulur): {len(ozel_ama_benign)}", f"- yalnız zayıf kural (kurulur): {len(kurulur)}", ""]
cikti += [f"{a}: {n} bulgu; {k}; {y}" for a, n, k, y in supheli]
(ARA / "p1b-gitleaks-isaret.md").write_text("\n".join(cikti) + "\n", encoding="utf-8")
print("\n".join(cikti[:4]))
print("şüpheli:", [a for a, *_ in supheli])
