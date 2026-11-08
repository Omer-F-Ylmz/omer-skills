"""VIDEO-HIZ-7: uzun sesi tek dosya (opus/flac) olarak Groq'a gönderip referans transkriptle karşılaştırır.
Kullanım: hiz7_asr.py <biçim: opus24|opus32|flac|wav> <video_id>... ; ses .kos/kopru/ogren/hiz7/<id>/ altında önbelleklenir."""
import difflib
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import video_derin as vd

D = KOK / ".kos/kopru/ogren/hiz7"
NW = 0x08000000
BICIM = {"opus24": ("libopus", ["-b:a", "24k", "-application", "voip"], "ogg", "audio/ogg"),
         "opus32": ("libopus", ["-b:a", "32k", "-application", "voip"], "ogg", "audio/ogg"),
         "flac": ("flac", [], "flac", "audio/flac"),
         "wav": ("pcm_s16le", [], "wav", "audio/wav")}


def calis(*a, **k):
    return subprocess.run([str(x) for x in a], capture_output=True, text=True, creationflags=NW, **k)


def ham(vid):
    w = D / vid / "a.wav"
    if not w.exists():
        w.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://youtu.be/{vid}"
        calis("yt-dlp", *vd.cerez_arg(url), "-f", "ba", "--no-playlist", "-N", "4", "-o", w.parent / "v.%(ext)s", url, timeout=600)
        v = next(p for p in w.parent.glob("v.*") if p.suffix not in (".json", ".part"))
        calis("ffmpeg", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", w)
    return w


def kodla(w, bicim):
    kod, arg, uzanti, _ = BICIM[bicim]
    o = w.with_name(f"a_{bicim}.{uzanti}")
    if not o.exists():
        calis("ffmpeg", "-y", "-i", w, "-ac", "1", "-ar", "16000", "-c:a", kod, *arg, o)
    return o


def gonder(dosya, tip, dil=None):
    key = vd.os.environ["GROQ_API_KEY"]
    sinir = "h7" + str(time.time_ns())
    alan = lambda ad, de: f'--{sinir}\r\nContent-Disposition: form-data; name="{ad}"\r\n\r\n{de}\r\n'.encode()
    govde = (alan("model", "whisper-large-v3") + alan("response_format", "verbose_json") + alan("temperature", "0") + (alan("language", dil) if dil else b"")
             + f'--{sinir}\r\nContent-Disposition: form-data; name="file"; filename="{dosya.name}"\r\nContent-Type: {tip}\r\n\r\n'.encode()
             + dosya.read_bytes() + f"\r\n--{sinir}--\r\n".encode())
    req = urllib.request.Request(vd.GROQ_ASR, govde, {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={sinir}", "User-Agent": "curl/8.5.0"})
    for deneme in range(3):
        try:
            r = urllib.request.urlopen(req, timeout=300)
            return json.load(r), {k: v for k, v in r.headers.items() if "ratelimit" in k.lower()}
        except Exception as e:
            ra = float(getattr(e, "headers", None) and e.headers.get("retry-after") or 0)
            print("hata", str(e)[:100], "retry-after", ra, flush=True)
            if "429" in str(e) and 0 < ra <= 90 and deneme < 2:
                time.sleep(ra + 1)
                continue
            raise


def kel(metin):
    return re.sub(r"[^\w\s]", "", metin.lower()).split()


def main():
    bicim, ids = sys.argv[1], sys.argv[2:]
    for vid in ids:
        w = ham(vid)
        o = w if bicim == "wav" else kodla(w, bicim)
        boy = o.stat().st_size
        sure = w.stat().st_size / 32000
        cik = D / vid / f"groq_{bicim}.json"
        if cik.exists():
            r, hd = json.loads(cik.read_text(encoding="utf-8")), {}
        else:
            ref0 = json.loads((KOK / "docs/video-tarama/derin" / f"{vid}.json").read_text(encoding="utf-8"))
            dil = (ref0.get("asr") or {}).get("dil")
            t0 = time.time()
            r, hd = gonder(o, BICIM[bicim][3], dil if dil in vd.GROQ_DIL.values() else None)
            r["_sn"] = round(time.time() - t0, 1)
            cik.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
        ref = json.loads((KOK / "docs/video-tarama/derin" / f"{vid}.json").read_text(encoding="utf-8"))
        kr = kel(" ".join(s["t"] for s in ref["transkript"]))
        ky = kel(" ".join(s["text"] for s in r.get("segments", [])))
        asr = difflib.SequenceMatcher(None, kr, ky, autojunk=False).ratio()
        print(json.dumps({"id": vid, "bicim": bicim, "ses_sn": round(sure), "MB": round(boy / 1e6, 1), "asr": round(asr, 3), "kelime_ref": len(kr), "kelime_groq": len(ky), "groq_sn": r.get("_sn"), "kota": hd}), flush=True)


if __name__ == "__main__":
    main()
