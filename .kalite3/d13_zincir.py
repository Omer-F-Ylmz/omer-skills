"""KALİTE-3-devam-13 zinciri (ortak sıra içinde tek yuva; parti içi ES çift aynı anda, her başlatmada RAM < %95):
d12'de koşanlar (.kalite3/d12-ajanlar.txt) dışındaki kalan ajanlar PARTI partide, departman sırasıyla. Her parti:
model_olc.pilot → ajan_jev (Jev + karar, ölçüt değişmez) → partinin GEÇEN ajanları kalite3-ajan-kabul.txt'ye → SIRA.md'ye tek satır.
Bütçe: claude -p ≤ 3 × 126 = 378 (+ boş yanıt yeniden denemesi), Jev ≈ $0.04."""
import subprocess, sys, time
from pathlib import Path

K = Path("C:/Projeler/omer-skills-wt/skill")
sys.path.insert(0, str(K / "tools"))
import model_olc as mo  # noqa: E402

KABUL = K / "docs/kutuphane/kalite3-ajan-kabul.txt"
SIRA = Path("C:/Projeler/omer-skills/.kos/kopru/gorev/SIRA.md")
D12 = set((K / ".kalite3/d12-ajanlar.txt").read_text(encoding="utf-8").split())
PARTI, AJAN_BASI, ES = 3, 63, 4  # 187 kalan ajan → 63/62/62


def tamam():
    r = {tuple(s.split("\t")[1:3]) for s in mo.PILOT.read_text(encoding="utf-8").splitlines()[1:]}
    return {a for a, k in r if k == "ajan" and (a, "ana") in r}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    # zincir öncesi kararlaşmış ajanlar (eşli RET'ler dahil) kabul listesine yeniden girmez; d12 partisinin geçenleri girer
    once = tamam() - D12
    for n in range(1, PARTI + 1):
        bas = time.time()
        print(time.strftime("%H:%M:%S"), f"parti {n}/{PARTI} başladı", flush=True)
        try:
            ajanlar = mo.pilot(2 * AJAN_BASI, es=ES, atla=D12)
        except Exception as e:  # yarım kalan çift sonraki partide yeniden seçilir; GEÇEN süzgeci listeye değil once'ye dayanır
            print("pilot hata:", repr(e)[:300], flush=True)
            ajanlar = sorted(tamam() - once - D12)
        j = subprocess.run([sys.executable, str(K / ".kalite3/ajan_jev.py")], cwd=K, capture_output=True, text=True, encoding="utf-8")
        print(j.stdout[-2000:], j.stderr[-1000:], "ajan_jev rc", j.returncode, flush=True)
        gecti = {s.split()[1] for s in j.stdout.splitlines() if s.startswith("GECTI ")}
        kabul = KABUL.read_text(encoding="utf-8").split()
        yeni = sorted(gecti - once - set(kabul))
        if yeni:
            with KABUL.open("a", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(yeni) + "\n")
        sure = round((time.time() - bas) / 60)
        satir = (f"- 12 Eki {time.strftime('%H:%M')} KALİTE-3 d13 zinciri parti {n}/{PARTI} BİTTİ ({sure} dk, {len(ajanlar)} ajan × 2, "
                 f"ajan_jev rc {j.returncode}): {len(yeni)} GEÇTİ → kalite3-ajan-kabul.txt {len(kabul) + len(yeni)}"
                 + (f" ({', '.join(yeni)})" if yeni else "") + " — onay toplu, Desktop uygular")
        with SIRA.open("a", encoding="utf-8", newline="\n") as f:
            f.write(satir + "\n")
        print(satir, flush=True)


if __name__ == "__main__":
    main()
