"""GPU-SINIR-2 doğrulama: 1 sn'de bir utilization.gpu örnekle (varsayılan 300 sn); %80 üstü oran + ort/tepe yaz.
Kullanım: python arka.py .kos/kopru/gpu-sinir-dogrula.log .kos/kopru/gpu_sinir_dogrula.py [sn]"""
import subprocess, sys, time

n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
u = []
for _ in range(n):
    t = time.time()
    r = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                       capture_output=True, text=True, timeout=20, creationflags=0x08000000).stdout.strip()
    u.append(float(r.splitlines()[0]))
    time.sleep(max(0, 1 - (time.time() - t)))
ust = sum(1 for x in u if x > 80)
print(f"örnek={len(u)} ort={sum(u)/len(u):.1f} tepe={max(u):.0f} >80 oran={100*ust/len(u):.2f}% (hedef <=2%)", flush=True)
