"""SUNUCU-KARAKTER-1: TTS adaylari (edge-tts bulut + yerel SAPI) ve ses-yonlu dudak senkronlu 1080x1920 klip."""
import os, sys, asyncio, subprocess, struct, wave, math, textwrap
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sunucu_rig as R
from sunucu_uret import BR, ROOT, bg

FF = r"C:\Users\pc\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
LINES = {
    "free-ai-drop": [("Hey, I'm Dropi, an AI host.", "eureka", 8, 175), ("Today's free drop: three AI tools that cost nothing.", "surprise", 140, 140),
                     ("Number one writes your captions. Number two cuts your videos.", "curious", 8, 120), ("Number three? It does both!", "laugh", 100, 100),
                     ("Follow for a new drop every day.", "eureka", 8, 175)],
    "curiosity-well": [("I'm Wick, an AI host.", "neutral", 8, 8), ("Why do old wells whisper?", "curious", 8, 120),
                       ("Villagers once thought the earth answered back.", "suspicion", 8, 8), ("The truth: sound bends against stone.", "eureka", 8, 175),
                       ("Stay curious. Follow for more.", "laugh", 60, 60)],
}
VOICES = {"free-ai-drop": [("edge-andrew", "en-US-AndrewNeural", "+8%"), ("edge-ava", "en-US-AvaNeural", "+8%")],
          "curiosity-well": [("edge-ryan", "en-GB-RyanNeural", "+0%"), ("edge-sonia", "en-GB-SoniaNeural", "+0%")]}


async def _edge(text, voice, rate, path):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(path)


def sapi(text, path):  # yerel Zira (Windows SAPI), tamamen cevrimdisi
    ps = "Add-Type -AssemblyName System.Speech;$s=New-Object System.Speech.Synthesis.SpeechSynthesizer;$s.Rate=1;$s.SetOutputToWaveFile('%s');$s.Speak([IO.File]::ReadAllText('%s'));$s.Dispose()" % (path, path + ".txt")
    open(path + ".txt", "w", encoding="utf-8").write(text)
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


def to_wav(src, dst):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, "-ar", "16000", "-ac", "1", dst], check=True)


def envelope(wav, fps=30):
    with wave.open(wav) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
        sr = w.getframerate()
    n = int(len(a) / sr * fps) + 1
    e = np.array([np.sqrt(np.mean(a[int(i * sr / fps):int((i + 1) * sr / fps) + 1] ** 2) + 1e-9) for i in range(n)])
    e = e / (np.percentile(e, 95) + 1e-9)
    return np.clip(e, 0, 1), len(a) / sr


def make_audio(key):
    out = os.path.join(ROOT, key, "ses"); os.makedirs(out, exist_ok=True)
    sample = " ".join(t for t, *_ in LINES[key]) + " " + " ".join(t for t, *_ in LINES[key])[:0]
    res = []
    for nm, v, rate in VOICES[key]:
        p = os.path.join(out, nm + ".mp3"); asyncio.run(_edge(sample, v, rate, p)); res.append(p)
    z = os.path.join(out, "local-zira.wav"); sapi(sample, z); res.append(z)
    return res


def font(b, s):
    return ImageFont.truetype(b["font"], s)


def render_video(key, audio, outp):
    b = BR[key]; fn = R.CHARS[b["ch"]]
    wav = os.path.join(os.environ["TEMP"], key + "_a.wav"); to_wav(audio, wav)
    env, dur = envelope(wav)
    lines = LINES[key]
    tot = sum(len(t) for t, *_ in lines); T = dur - 0.2
    bounds, acc = [], 0.1
    for t, *_ in lines:
        L = T * len(t) / tot; bounds.append((acc, acc + L)); acc += L
    W, H, fps = 1080, 1920, 30
    base = bg(b, (W, H), 7).convert("RGB")
    cache = {}
    ft, fb = font(b, 76), font(b, 40)
    p = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-i", audio,
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-shortest", outp], stdin=subprocess.PIPE)
    nf = int(dur * fps) + 8
    for f in range(nf):
        t = f / fps
        si = next((i for i, (a, z) in enumerate(bounds) if a <= t < z), None)
        speaking = si is not None
        li = si if speaking else (len(lines) - 1 if t >= bounds[-1][1] else 0)
        txt, ex, al, ar = lines[li]
        m = float(env[min(f, len(env) - 1)]) if speaking else 0.0
        mq = round(m * 5) / 5
        blink = (f % 95) in (0, 1, 2)
        # kol sallanma
        sw = int(6 * math.sin(t * 6)) if ar > 100 else 0
        yw = round(0.25 * math.sin(t * 1.9 + li) / 0.125) * 0.125
        tl = round(5 * math.sin(t * 2.3) / 2) * 2
        al2 = al + (int(10 * math.sin(t * 5)) // 5 * 5 if al > 100 else 0)
        key_ = (ex, mq, blink, al2, ar + sw // 3 * 3, yw, tl)
        if key_ not in cache:
            cache[key_] = R.render(b["ch"], tilt=tl, yaw=yw, expr=ex, mouth=mq if speaking else None, armL=al2, armR=ar + sw // 3 * 3, blink=blink).resize((960, 960), Image.LANCZOS)
        sp = cache[key_]
        fr = base.copy()
        by = int(6 * math.sin(t * 3.2))
        fr.paste(sp, (60, 270 + by), sp)
        d = ImageDraw.Draw(fr)
        # AI etiketi (her karede gorunur)
        d.rounded_rectangle([40, 60, 40 + 380, 60 + 78], radius=26, fill=(0, 0, 0), outline=b["acc"], width=4)
        d.text((40 + 190, 99), "AI host - " + b["name"], font=fb, fill=b["acc"], anchor="mm")
        d.text((W // 2, 1740), b["brand"], font=fb, fill=b["acc"], anchor="mm")
        # altyazi
        wrapped = textwrap.wrap(txt, 20)
        for i, ln in enumerate(wrapped):
            y = 1390 + i * 92
            d.text((W // 2 + 3, y + 3), ln, font=ft, fill=(0, 0, 0), anchor="mm")
            d.text((W // 2, y), ln, font=ft, fill=b["txt"], anchor="mm")
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    return dur


if __name__ == "__main__":
    for key in BR:
        auds = make_audio(key)
        for a in auds:
            print(key, a, round(envelope(_w := (to_wav(a, os.path.join(os.environ["TEMP"], "t.wav")) or os.path.join(os.environ["TEMP"], "t.wav")))[1], 1), "sn")
        if len(sys.argv) > 1:
            continue
        d = render_video(key, auds[0], os.path.join(ROOT, key, f"ornek-klip-{key}.mp4"))
        print("klip", key, round(d, 1))
