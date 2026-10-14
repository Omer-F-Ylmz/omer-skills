"""TOKEN-2 K8: ucuz alt adım — araştırma/lisans/katalog özetini Claude-dışı modele (OmniRoute combo) yaptırır.
Claude oturumu ham metni okumaz: bağlam dosyaları burada birleşir, yanıt dosyaya yazılır, stdout'a yalnız yol + model + jeton.
Claude aboneliği geçmez (combo Claude-dışı). Anahtar OMNIROUTE_KEY (env ya da HKCU) hiçbir çıktıya yazılmaz.
  python tools/ucuz_alt.py <istem.md> <cikti.md> [bağlam dosyaları...]"""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

URL = "http://127.0.0.1:20128/v1/chat/completions"
COMBO = "cc-yedek-dis"  # cc-kopru/omniroute.mjs OMNI_COMBO ile aynı (Claude-dışı)
TAVAN = 400_000  # bağlam karakteri; combo'daki en küçük pencereye sığsın


def anahtar():
    if os.environ.get("OMNIROUTE_KEY"):
        return os.environ["OMNIROUTE_KEY"]
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
        return winreg.QueryValueEx(k, "OMNIROUTE_KEY")[0]


def govde(istem, dosyalar):
    ek = "".join(f'\n\n<dosya yol="{Path(d).as_posix()}">\n{Path(d).read_text(encoding="utf-8", errors="ignore")}\n</dosya>'
                 for d in dosyalar)
    if len(istem) + len(ek) > TAVAN:
        raise ValueError(f"bağlam {len(istem) + len(ek)} karakter > {TAVAN}; dosyaları böl")
    # düşünme kapalı: flash düşünme jetonu max_tokens'u yiyordu (OMNIROUTE d3)
    return {"model": COMBO, "messages": [{"role": "user", "content": istem + ek}], "max_tokens": 4000, "reasoning_effort": "none"}


def iste(g, zaman=300):
    q = urllib.request.Request(URL, method="POST", data=json.dumps(g).encode(), headers={
        "content-type": "application/json", "authorization": f"Bearer {anahtar()}",
        "user-agent": "omer-skills-ucuz-alt/1"})  # Python-urllib UA'sı Groq'ta 403
    return json.load(urllib.request.urlopen(q, timeout=zaman))


def main(argv):
    istem, cikti, *dosyalar = argv
    t = time.time()
    try:
        j = iste(govde(Path(istem).read_text(encoding="utf-8"), dosyalar))
    except Exception as e:  # anahtar hata metnine girmez (yalnız tür + HTTP kodu)
        print(f"HATA {type(e).__name__} {getattr(e, 'code', '')}".strip())
        return 1
    c = j["choices"][0]
    Path(cikti).write_text(c["message"].get("content") or "", encoding="utf-8")
    u = j.get("usage") or {}
    print(f"{cikti} · model {j.get('model', '?')} · bitiş {c.get('finish_reason')} · "
          f"girdi {u.get('prompt_tokens')} çıktı {u.get('completion_tokens')} · {time.time() - t:.0f} sn")
    return 0 if c.get("finish_reason") != "length" else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
