import asyncio, subprocess, sys, os
O = r"C:\Users\pc\Desktop\Claude ile yapılanlar\sosyal-onizleme\ses-adaylari"
T = "Hi, I'm your little guide! Today we found a free tool that does the work of a paid one. Want to see how it works? Let's go!"
txt = os.path.join(O, "_metin.txt"); open(txt, "w", encoding="utf-8").write(T)
import edge_tts
async def edge():
    for v, a in [("en-US-AnaNeural", "edge-ana"), ("en-US-JennyNeural", "edge-jenny")]:
        await edge_tts.Communicate(T, v, rate="+8%", pitch="+10Hz").save(os.path.join(O, a + ".mp3"))
asyncio.run(edge())
py = r"C:\Users\pc\tts-venv\Scripts\python.exe"
for v in ["af_heart", "af_bella", "af_nicole", "af_sky"]:
    r = subprocess.run([py, r"C:\Users\pc\Desktop\Claude ile yapılanlar\sosyal-oto\kokoro_tts.py", txt, v, os.path.join(O, "kokoro-" + v + ".wav"), "1.05"], capture_output=True, text=True)
    print(v, r.returncode, r.stderr[-200:])
