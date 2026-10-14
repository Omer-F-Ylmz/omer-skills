"""ÖĞREN-1 d2 kombin "görsel yargı": 1 küçük PNG → OmniRoute :free görsel model (tek çağrı) → Claude yalnız kısa hükmü okur.
  python -X utf8 .claude/ogren1/gorsel_mini.py <png>"""
import base64, json, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(r"C:\Projeler\omer-skills\.claude\omniroute1")))
from pilot import env_oku  # noqa: E402

png = Path(sys.argv[1])
govde = {"model": "openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free", "max_tokens": 3000, "messages": [{"role": "user", "content": [
    {"type": "text", "text": "Görselde ne var? Tek cümle Türkçe."},
    {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(png.read_bytes()).decode()}}]}]}
q = urllib.request.Request("http://127.0.0.1:20128/v1/chat/completions", data=json.dumps(govde).encode(), headers={
    "authorization": f"Bearer {env_oku('OMNIROUTE_KEY')}", "content-type": "application/json", "user-agent": "curl/8.4"})
t = time.time()
j = json.load(urllib.request.urlopen(q, timeout=180))
print(f"{png.stat().st_size} B png · {time.time() - t:.0f} s · {j.get('model')} · girdi {j['usage'].get('prompt_tokens')} · "
      f"hüküm: {(j['choices'][0]['message'].get('content') or '').strip()[:160]}")
