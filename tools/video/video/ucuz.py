"""Hafif sınıflayıcı: Ollama REST /api/chat (format=json), claude -p'siz. KAÇAN? terimi → aday|kapat."""
import json
import urllib.request

URL = "http://localhost:11434/api/chat"
SISTEM = ('Claude Code için kurulabilir bir ARAÇ/skill/eklenti/repo/paket adı mı? Her terim için karar ver: '
          '"aday" = adı konmuş somut araç, skill, MCP, eklenti, GitHub repo (owner/ad) ya da paket; '
          '"kapat" = genel kelime, dosya yolu, mime türü, kare/açıklama, ikili terim, marka/doküman sitesi. '
          'Girdi {"0": terim, "1": terim, ...}. Yalnız JSON döndür: {"kararlar": {"0": "aday"|"kapat", "1": ...}} — her indeks için bir karar.')


def siniflandir(terimler, model="gpt-oss:120b-cloud", url=URL, zaman=300):
    """→ (kararlar, süre_dışı_ayrıntı). Sayı tutmazsa ValueError."""
    g = {"model": model, "stream": False, "format": "json", "think": False, "keep_alive": 0,
         "messages": [{"role": "system", "content": SISTEM},
                      {"role": "user", "content": json.dumps(dict(enumerate(terimler)), ensure_ascii=False)}]}
    r = urllib.request.Request(url, json.dumps(g).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=zaman) as f:
        y = json.load(f)
    d = json.loads(y["message"]["content"]).get("kararlar", {})
    if isinstance(d, list):  # eski biçim
        d = dict(enumerate(d))
    k = [d.get(str(i), d.get(i, "?")) for i in range(len(terimler))]
    return k, y
