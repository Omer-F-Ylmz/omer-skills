"""MOTOR-M2a K1: hafif `claude -p` taşıyıcısı (a1 bayrakları, docs/tasarim/parti-motoru.md) → form + usage + total_cost_usd.
Kimlik/anahtar değeri ne loglanır ne döner; ANTHROPIC_BASE_URL alt süreçte kaldırılır (headroom vekili araçları gizliyor)."""
import base64
import re
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

MODEL = "claude-sonnet-5-5"
GORSEL = True  # kareler stream-json image bloğuyla gider; False → rapora "metin açıklamasıyla" açık kalemi
A1 = ["--tools", "", "--setting-sources", "", "--strict-mcp-config", "--safe-mode", "--disable-slash-commands", "--no-session-persistence",
      "--input-format", "stream-json", "--output-format", "stream-json", "--verbose"]


def _kos(args, girdi, env, timeout):
    return subprocess.run(args, input=girdi, capture_output=True, encoding="utf-8", errors="replace", env=env, timeout=timeout)


def _cagir(sistem, metin, sema, kareler, model, butce, timeout, env, kos, araclar):
    """→ {form, usage, usd, sure, hata}; hata varsa form None."""
    env = {k: v for k, v in (os.environ if env is None else env).items() if k != "ANTHROPIC_BASE_URL"}
    icerik = [{"type": "text", "text": metin}] + [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                                                "data": base64.b64encode(Path(k).read_bytes()).decode()}} for k in kareler]
    girdi = json.dumps({"type": "user", "message": {"role": "user", "content": icerik}}, ensure_ascii=False) + "\n"
    args = [shutil.which("claude") or "claude", "-p", "--model", model, "--system-prompt", sistem,
            "--json-schema", json.dumps(sema, ensure_ascii=False), "--max-budget-usd", f"{butce:.2f}", *A1]
    if araclar:  # M2b K2: araçlı mod — yalnız izinli liste; --allowedTools dışı araç -p'de reddedilir
        args[args.index("--tools") + 1] = ",".join(dict.fromkeys(a.split("(")[0] for a in araclar))
        args += ["--max-turns", "8", "--allowedTools", *araclar]
    t = time.monotonic()
    try:
        r = kos(args, girdi, env, timeout)
    except subprocess.TimeoutExpired:
        return {"form": None, "usage": {}, "usd": 0.0, "sure": round(time.monotonic() - t, 1), "hata": f"zaman aşımı {timeout} sn"}
    son = {}
    for s in (r.stdout or "").splitlines():
        try:
            x = json.loads(s)
        except ValueError:
            continue
        if isinstance(x, dict) and x.get("type") == "result":
            son = x
    form = son.get("structured_output")
    hata = None if isinstance(form, dict) and not son.get("is_error") else \
        f"{son.get('subtype') or 'rc ' + str(r.returncode)}: {str(son.get('result') or (r.stderr or '').strip()[-200:])[:200]}"
    return {"form": None if hata else form, "usage": son.get("usage") or {}, "usd": son.get("total_cost_usd") or 0.0,
            "sure": round(time.monotonic() - t, 1), "hata": hata}


def cagir(sistem, metin, sema, kareler=(), model=MODEL, butce=0.5, timeout=600, env=None, kos=_kos, araclar=()):
    """→ {form, usage, usd, sure, hata}; araclar boşsa araçsız a1 (--tools ""), doluysa yalnız izinli liste + `web` (WebSearch sayısı)."""
    ham = []
    y = _cagir(sistem, metin, sema, kareler, model, butce, timeout, env, lambda *a: ham.append(kos(*a)) or ham[-1], araclar)
    if araclar:
        y["web"] = len(re.findall(r'"name":\s*"WebSearch"', getattr(ham[0], "stdout", "") or "")) if ham else 0
    return y
