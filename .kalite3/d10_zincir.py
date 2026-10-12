"""KALİTE-3-devam-10 ölçüm zinciri (ortak sıra içinde, en fazla 4 + 41 = 45 claude -p; Jev ≈ $0.01):
netlify-config eşli ×2 → ajan pilotu departman sırasıyla (3 güvenilmez yeniden + 19 yeni ajan) → Jev + karar."""
import subprocess, sys

K = "C:/Projeler/omer-skills-wt/skill"
for a in ([
    "tools/olcum/kalite3_olc.py", ".kalite3/esli2-gorev.json", "docs/kutuphane/olcum/kalite3-pilot-esli2.tsv",
    "--tekrar", "2", "--en-fazla", "4"], ["tools/model_olc.py", "pilot", "41"], [".kalite3/ajan_jev.py"]):
    print(a, "rc", subprocess.run([sys.executable, *a], cwd=K).returncode, flush=True)
