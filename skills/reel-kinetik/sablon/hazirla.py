"""Metin → SAPI ses (public/ses.wav) + kelime zamanları (reel.json). Kullanım: hazirla.py "<metin>". Zamanlama: kelime uzunluğuna orantılı (shortcut: gerçek hizalama için whisper kullan)."""
import json, subprocess, sys, wave
from pathlib import Path
metin = sys.argv[1]
k = Path(__file__).parent
wav = k / "public" / "ses.wav"
ps = f"Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Rate=0; $s.SetOutputToWaveFile('{wav}'); $s.Speak([Console]::In.ReadToEnd()); $s.Dispose()"
subprocess.run(["powershell", "-NoProfile", "-Command", ps], input=metin, text=True, check=True)
with wave.open(str(wav)) as w: sure = w.getnframes() / w.getframerate()
kel = metin.split(); toplam = sum(len(x) + 1 for x in kel); t = 0.15; out = []
for x in kel:
    d = (sure - 0.15) * (len(x) + 1) / toplam
    out.append({"t": x, "start": round(t, 3), "end": round(t + d, 3)}); t += d
fps = 30
(k / "reel.json").write_text(json.dumps({"words": out, "audio": "ses.wav", "fps": fps, "durationInFrames": int((sure + 0.5) * fps)}, ensure_ascii=False), encoding="utf-8")
print(f"ses {sure:.2f} sn, {len(kel)} kelime")
