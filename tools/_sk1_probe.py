import os, sys, json, base64, urllib.request, urllib.error, urllib.parse
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0"}
# 1) Pollinations
try:
    u = "https://image.pollinations.ai/prompt/" + urllib.parse.quote("flat vector mascot, friendly robot fox, purple background") + "?width=512&height=512&seed=7&nologo=true&model=flux"
    r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90)
    b = r.read(); open(out + "/poll.jpg", "wb").write(b); print("pollinations", r.status, len(b))
except Exception as e:
    print("pollinations ERR", repr(e)[:200])
# 2) Gemini
k = os.environ.get("GEMINI_API_KEY") or ""
for m in ("gemini-2.5-flash-image", "gemini-2.0-flash-preview-image-generation", "imagen-4.0-fast-generate-001"):
    try:
        if m.startswith("imagen"):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:predict"
            body = {"instances": [{"prompt": "flat vector mascot, friendly robot fox"}], "parameters": {"sampleCount": 1}}
        else:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"
            body = {"contents": [{"parts": [{"text": "flat vector mascot, friendly robot fox, purple background"}]}], "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
        req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json", "x-goog-api-key": k})
        r = urllib.request.urlopen(req, timeout=90); d = r.read().decode()
        print(m, r.status, len(d))
    except urllib.error.HTTPError as e:
        print(m, "HTTP", e.code, e.read().decode()[:160].replace("\n", " "))
    except Exception as e:
        print(m, "ERR", repr(e)[:150])
