"""OLUM-TESHIS-1-A2: WER 141 anlarını eşlemek için 1 sn'lik GPU günlüğü (util, bellek, sıcaklık, güç, saat). En çok 6 saat, sonra BITTI.
Çıktı: stdout (arka.py günlüğe yazar). Satır: HH:MM:SS util mem_used temp power sm_clk mem_clk pstate"""
import subprocess, time
SON = time.time() + 6 * 3600
SORGU = "utilization.gpu,memory.used,temperature.gpu,power.draw,clocks.sm,clocks.mem,pstate"
while time.time() < SON:
    t = time.strftime("%H:%M:%S")
    try:
        r = subprocess.run(["nvidia-smi", f"--query-gpu={SORGU}", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=20, creationflags=0x08000000)
        print(t, r.stdout.strip().replace(", ", " ") or f"bos rc={r.returncode}", flush=True)
    except subprocess.TimeoutExpired:
        print(t, "SMI-ZAMAN-ASIMI", flush=True)
    time.sleep(1)
print("BITTI", flush=True)
