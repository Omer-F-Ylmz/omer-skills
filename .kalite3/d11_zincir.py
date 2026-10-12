"""KALİTE-3-devam-11 ölçüm zinciri (ortak sıra içinde, en fazla 38 claude -p; Jev ≈ $0.004):
ajan pilotu sonraki parti departman sırasıyla (19 ajan × 2 kol) → Jev + karar (ajan_jev anahtarı HKCU'dan okur)."""
import subprocess, sys

K = "C:/Projeler/omer-skills-wt/skill"
for a in (["tools/model_olc.py", "pilot", "38"], [".kalite3/ajan_jev.py"]):
    print(a, "rc", subprocess.run([sys.executable, *a], cwd=K).returncode, flush=True)
