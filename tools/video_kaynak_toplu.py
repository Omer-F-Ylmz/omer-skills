"""VIDEO-KAYNAK (a): bekleyen linkleri izle -> kaynak/araç/site/yöntem çıkar. Ücretsiz modeller.
Kullanım: python tools/video_kaynak_toplu.py [--en-fazla N]. Durum: docs/video-tarama/kaynak/*.json (var olan atlanır)."""
import base64, json, os, subprocess, sys, time, urllib.request, urllib.error, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/video-tarama/kaynak"
CACHE = pathlib.Path("C:/Projeler/.video-cache")
OUT.mkdir(parents=True, exist_ok=True)
GEM, GROQ = os.environ.get("GEMINI_API_KEY"), os.environ.get("GROQ_API_KEY")
PROMPT = """Bu videoyu izleyen bir araştırmacısın. Videoda adı geçen/gösterilen her ARAÇ, SİTE, REPO, SKILL, MCP, MODEL ve her YÖNTEM'i çıkar.
Yalnız JSON döndür: {"baslik":"","ozet":"<=2 cümle","araclar":[{"ad":"","tur":"arac|site|repo|model|skill|mcp","url":"","ne":"<=12 kelime"}],"yontem":"uygulanabilir yöntem varsa 1-3 cümle, yoksa ''","kur_oneri":"kur|ogren-uygula|gecilebilir","kanit":"ekran yazısı/ses alıntısı <=15 kelime"}
Bilgi uydurma; emin olmadığın alanı boş bırak."""


def http(url, data, headers, timeout=180):
    req = urllib.request.Request(url, data=data, headers=headers)
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


def gemini(parts, model):
    body = json.dumps({"contents": [{"parts": parts}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1}}).encode()
    r = http(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEM}", body, {"Content-Type": "application/json"})
    return r["candidates"][0]["content"]["parts"][0]["text"]


def groq_chat(text, mdl="openai/gpt-oss-20b"):
    # 413/429: serbest katman TPM tavanı -> metni kısalt / bekle, 4 deneme
    n = 11000
    for _ in range(6):
        body = json.dumps({"model": mdl, "max_tokens": 1800, "messages": [{"role": "user", "content": PROMPT + "\n\n" + text[:n]}], "reasoning_effort": "low"}).encode()
        try:
            r = http("https://api.groq.com/openai/v1/chat/completions", body, {"Content-Type": "application/json", "Authorization": f"Bearer {GROQ}", "User-Agent": "curl/8"})
            return r["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code == 413:
                n //= 2
            elif e.code == 429:
                time.sleep(30)
            else:
                raise
    raise RuntimeError("groq-tavan")


def groq_whisper(mp3):
    b = "----vk"
    data = pathlib.Path(mp3).read_bytes()
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nwhisper-large-v3\r\n--{b}\r\nContent-Disposition: form-data; name=\"response_format\"\r\n\r\ntext\r\n--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode() + data + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request("https://api.groq.com/openai/v1/audio/transcriptions", body, {"Content-Type": f"multipart/form-data; boundary={b}", "Authorization": f"Bearer {GROQ}", "User-Agent": "curl/8"})
    return urllib.request.urlopen(req, timeout=180).read().decode()


def openrouter_vision(imgs, ctx):
    ks = os.environ.get("OPENROUTER_API_KEY")
    content = [{"type": "text", "text": PROMPT + "\n\n" + ctx}] + [{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(i.read_bytes()).decode()}} for i in imgs[:6]]
    for m in ("google/gemma-4-31b-it:free", "google/gemma-4-26b-a4b-it:free", "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"):
        try:
            body = json.dumps({"model": m, "messages": [{"role": "user", "content": content}], "max_tokens": 2500}).encode()
            r = http("https://openrouter.ai/api/v1/chat/completions", body, {"Content-Type": "application/json", "Authorization": f"Bearer {ks}"}, 240)
            t = r["choices"][0]["message"]["content"]
            if t:
                return re.sub(r"^```(?:json)?|```$", "", t.strip()).strip(), "openrouter:" + m
        except Exception:
            continue
    return None, ""


def openrouter_text(ctx):
    ks = os.environ.get("OPENROUTER_API_KEY")
    for m in ("google/gemma-4-31b-it:free", "openai/gpt-oss-120b:free", "google/gemma-4-26b-a4b-it:free"):
        try:
            body = json.dumps({"model": m, "messages": [{"role": "user", "content": PROMPT + "\n\n" + ctx[:14000]}], "max_tokens": 2500}).encode()
            r = http("https://openrouter.ai/api/v1/chat/completions", body, {"Content-Type": "application/json", "Authorization": f"Bearer {ks}"}, 240)
            t = r["choices"][0]["message"]["content"]
            if t:
                return re.sub(r"^```(?:json)?|```$", "", t.strip()).strip(), "openrouter:" + m
        except Exception:
            continue
    return None, ""


def vid_id(url):
    m = re.search(r"instagram\.com/(?:p|reel)/([^/?]+)", url)
    return ("ig-" + m.group(1)) if m else url.rstrip("/").split("/")[-1].split("?")[0]


def run(*a):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)


def isle(url):
    vid = vid_id(url)
    run("video", "ozet", url)
    d = CACHE / vid
    seg = d / "segmentler.jsonl"
    text = ""
    if seg.exists() and seg.stat().st_size:
        text = " ".join(json.loads(l)["metin"] for l in seg.read_text(encoding="utf-8").splitlines() if l.strip())
    meta = (d / "meta.json").read_text(encoding="utf-8") if (d / "meta.json").exists() else ""
    links = (d / "linkler.json").read_text(encoding="utf-8")[:1500] if (d / "linkler.json").exists() else ""
    mp4 = d / "goz-video.mp4"
    kaynak = "altyazi" if text else ""
    if not text and mp4.exists():
        mp3 = d / "ses.mp3"
        run("ffmpeg", "-y", "-i", str(mp4), "-vn", "-ac", "1", "-ar", "16000", "-b:a", "48k", str(mp3))
        if mp3.exists() and mp3.stat().st_size:
            try:
                text, kaynak = groq_whisper(mp3), "groq-whisper-large-v3"
            except Exception as e:
                kaynak = f"whisper-hata:{type(e).__name__}"
    ctx = f"META: {meta[:1200]}\nLINKLER: {links}\nDÖKÜM: {text[:22000]}"
    parts = [{"text": PROMPT + "\n\n" + ctx}]
    if mp4.exists() and mp4.stat().st_size < 14_000_000:
        parts.insert(0, {"inline_data": {"mime_type": "video/mp4", "data": base64.b64encode(mp4.read_bytes()).decode()}})
    out, model = None, ""
    for m in ("gemini-3.8-flash", "gemini-3-flash-preview"):
        try:
            out, model = gemini(parts, m), m
            break
        except urllib.error.HTTPError as e:
            if e.code != 429:
                model = f"{m}:{e.code}"
        except Exception as e:
            model = f"{m}:{type(e).__name__}"
    imgs = sorted(d.glob("gorsel-*.jpg"))
    if out is None and imgs and len(text.split()) < 15:
        out, model = openrouter_vision(imgs, ctx)
    if out is None and text:
        try:
            out = model = None
            for mdl in ("openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"):
                try:
                    out, model = groq_chat(ctx, mdl), "groq-" + mdl.split("/")[1]
                    break
                except Exception:
                    continue
            if out is None:
                raise RuntimeError("groq-tum-modeller")
        except Exception as e:
            out, model = openrouter_text(ctx)
            if out is None:
                return {"id": vid, "url": url, "hata": f"{model}|groq:{type(e).__name__}"}
    if out is None:
        return {"id": vid, "url": url, "hata": f"tum-modeller-basarisiz:{model}"}
    try:
        j = json.loads(out)
    except Exception:
        j = {"ham": out[:1500]}
    j.update(id=vid, url=url, model=model, dokum=kaynak or "yok", dokum_kelime=len(text.split()))
    return j


def main():
    n = int(sys.argv[sys.argv.index("--en-fazla") + 1]) if "--en-fazla" in sys.argv else 10**6
    urls = [l.strip() for l in open(str(ROOT / ".kos/kopru/arka/video-kaynak-linkler.txt"), encoding="utf-8") if l.strip()] if os.path.exists(str(ROOT / ".kos/kopru/arka/video-kaynak-linkler.txt")) else []
    done = 0
    if "--yt" in sys.argv:  # yalnız YouTube (IG işini bölmemek için paralel örnek)
        urls = [u for u in urls if "instagram" not in u]
    for u in urls:
        f = OUT / (vid_id(u) + ".json")
        if f.exists() and "hata" not in f.read_text(encoding="utf-8")[:400]:
            continue
        if done >= n:
            break
        try:
            r = isle(u)
        except Exception as e:
            r = {"id": vid_id(u), "url": u, "hata": f"{type(e).__name__}:{str(e)[:80]}"}
        f.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        done += 1
        print(time.strftime("%H:%M:%S"), r["id"], r.get("hata") or r.get("model"), flush=True)
        time.sleep(2)


main()
