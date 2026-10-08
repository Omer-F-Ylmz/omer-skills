"""MOTOR-M2a K1: hafif `claude -p` taşıyıcısı (a1 bayrakları, docs/tasarim/parti-motoru.md) → form + usage + total_cost_usd.
Kimlik/anahtar değeri ne loglanır ne döner; ANTHROPIC_BASE_URL alt süreçte kaldırılır (headroom vekili araçları gizliyor)."""
import base64
import mimetypes
import re
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import cc_profil  # noqa: E402 — tools/cc_profil.py (TOKEN-1)

MODEL = "claude-sonnet-5-5"
GORSEL = True  # kareler stream-json image bloğuyla gider; False → rapora "metin açıklamasıyla" açık kalemi
A1 = ["--tools", "", "--setting-sources", "", "--strict-mcp-config", "--safe-mode", "--disable-slash-commands", "--no-session-persistence",
      "--input-format", "stream-json", "--output-format", "stream-json", "--verbose"]
USAGE_YOL = Path(__file__).resolve().parents[3] / "olcum" / "motor-usage.jsonl"  # TOKEN-1: --no-session-persistence → jsonl'de yok


def _usage_yaz(args, stdout):
    """result usage'ı yalnız sayı olarak eklenir; istem/çıktı metni yazılmaz."""
    for s in (stdout or "").splitlines():
        try:
            x = json.loads(s)
        except ValueError:
            continue
        if isinstance(x, dict) and x.get("type") == "result":
            u = x.get("usage") or {}
            say = {k: v for k, v in u.items() if isinstance(v, int)}
            if isinstance(u.get("cache_creation"), dict):
                say["cache_creation"] = {k: v for k, v in u["cache_creation"].items() if isinstance(v, int)}
            USAGE_YOL.parent.mkdir(parents=True, exist_ok=True)
            with USAGE_YOL.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"ts": time.time(), "model": args[args.index("--model") + 1] if "--model" in args else None,
                                    "usage": say, "usd": x.get("total_cost_usd") or 0.0}) + "\n")


def _kos(args, girdi, env, timeout):
    r = subprocess.run(args, input=girdi, capture_output=True, encoding="utf-8", errors="replace", env=env, timeout=timeout)
    _usage_yaz(args, r.stdout)
    return r


def _cagir(sistem, metin, sema, kareler, model, butce, timeout, env, kos, araclar):
    """→ {form, usage, usd, sure, hata}; hata varsa form None."""
    env = {k: v for k, v in (os.environ if env is None else env).items() if k != "ANTHROPIC_BASE_URL"}
    icerik = [{"type": "text", "text": metin}] + [{"type": "image", "source": {"type": "base64", "media_type": mimetypes.guess_type(k)[0] or "image/jpeg",
                                                                                "data": base64.b64encode(Path(k).read_bytes()).decode()}} for k in kareler]
    girdi = json.dumps({"type": "user", "message": {"role": "user", "content": icerik}}, ensure_ascii=False) + "\n"
    args = [shutil.which("claude") or "claude", "-p", "--model", model, "--system-prompt", sistem,
            "--json-schema", json.dumps(sema, ensure_ascii=False), "--max-budget-usd", f"{butce:.2f}", *A1, *cc_profil.kur("ttl", env=env)[0]]
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
            "sure": round(time.monotonic() - t, 1), "hata": hata, "model": ",".join(son.get("modelUsage") or {}) or None}  # 1b-2a KAPANIŞ: yanıttaki gerçek model kimliği


def cagir(sistem, metin, sema, kareler=(), model=MODEL, butce=0.5, timeout=600, env=None, kos=_kos, araclar=()):
    """→ {form, usage, usd, sure, hata}; araclar boşsa araçsız a1 (--tools ""), doluysa yalnız izinli liste + `web` (WebSearch sayısı)."""
    ham = []
    y = _cagir(sistem, metin, sema, kareler, model, butce, timeout, env, lambda *a: ham.append(kos(*a)) or ham[-1], araclar)
    if araclar:
        y["web"] = len(re.findall(r'"name":\s*"WebSearch"', getattr(ham[0], "stdout", "") or "")) if ham else 0
    return y
