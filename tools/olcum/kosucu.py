"""KÜTÜPHANE-3a: ölçüm koşucusu. Sabit görev setini (gorevler.json) `claude -p` ile koşar, gerçek usage + süre +
doğru-araç isabeti + rubrik puanını docs/kutuphane/olcum/<tarih>-<profil>.tsv'ye yazar.
  python tools/olcum/kosucu.py --profil tam [--gorev G01,G05] [--tavan 12]
Profiller profiller.json'da (ek `claude` argümanları); yeni profil = yeni anahtar. Ayar/env değiştirmez.
Puan: rubrikteki her madde {"puan": n, "regex": "..."} yanıt metninde eşleşirse n eklenir (toplam 10). Jev (LLM yargıç) isteğe bağlı sonraki adım."""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
KOK = DIZIN.parents[1]
CIKTI = KOK / "docs" / "kutuphane" / "olcum"
ROTA = ["--output-format", "stream-json", "--verbose", "--include-hook-events", "--no-session-persistence"]


def ayristir(stdout):
    """stream-json satırları → {usage, usd, sure_ms, metin, araclar, init, hook}. Anahtar/istem değeri taşımaz."""
    o = {"usage": {}, "usd": 0.0, "sure_ms": 0, "metin": "", "araclar": [], "init": {}, "hook": []}
    for s in (stdout or "").splitlines():
        try:
            x = json.loads(s)
        except ValueError:
            continue
        if not isinstance(x, dict):
            continue
        t, st = x.get("type"), x.get("subtype")
        if t == "system" and st == "init":
            o["init"] = {k: x.get(k) for k in ("tools", "mcp_servers", "slash_commands", "agents", "skills", "plugins", "model") if k in x}
        elif t == "system" and st and st.startswith("hook"):
            o["hook"].append({k: x.get(k) for k in ("subtype", "hook_name", "hook_event", "output", "stdout", "stderr", "exit_code") if k in x})
        elif t == "assistant":
            u = (x.get("message") or {}).get("usage") or {}
            if u and not o["usage"]:
                o["usage_ilk"] = o.get("usage_ilk") or u   # result olayı yoksa (bütçe/hata) ilk tur usage'ı
            for b in (x.get("message") or {}).get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    ad = b.get("name") or ""
                    if ad == "Skill":
                        ad = "Skill:" + str((b.get("input") or {}).get("skill") or (b.get("input") or {}).get("command") or "")
                    elif ad in ("Task", "Agent"):
                        ad = "Agent:" + str((b.get("input") or {}).get("subagent_type") or "")
                    o["araclar"].append(ad)
        elif t == "result":
            o["usage"] = x.get("usage") or {}
            o["usd"] = x.get("total_cost_usd") or 0.0
            o["sure_ms"] = x.get("duration_ms") or 0
            o["metin"] = str(x.get("result") or "")
    o["usage"] = o["usage"] or o.get("usage_ilk") or {}
    return o


def jeton(u):
    """(input, cache_creation, cache_read, output)"""
    return (u.get("input_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0))


def kos(istem, ek=(), cwd=None, model=None, timeout=600, butce=3.0):
    """Tek `claude -p`. ANTHROPIC_BASE_URL (headroom vekili) alt süreçte kaldırılır — araçları gizliyor. Boş cwd yoksa geçici boş klasör."""
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_BASE_URL"}
    args = ["claude", "-p", istem, *ROTA, "--max-budget-usd", f"{butce:.2f}", *([] if not model else ["--model", model]), *ek]
    with tempfile.TemporaryDirectory(prefix="olcum-") as bos:
        t = time.monotonic()
        r = subprocess.run(args, capture_output=True, encoding="utf-8", errors="replace", env=env, cwd=cwd or bos, timeout=timeout)
        sure = round(time.monotonic() - t, 1)
    o = ayristir(r.stdout)
    o["sure"], o["rc"], o["hata"] = sure, r.returncode, (r.stderr or "").strip()[-200:] if r.returncode else ""
    return o


def puanla(metin, rubrik):
    return min(10, sum(m["puan"] for m in rubrik if re.search(m["regex"], metin, re.I | re.S)))


def isabet(araclar, beklenen):
    """beklenen = [] → araç gerekmez (1); aksi halde beklenen adlardan biri kullanıldıysa 1 (önek eşleşmesi: 'Skill:' tüm skill'leri sayar)."""
    return 1 if not beklenen else int(any(a.startswith(b) for a in araclar for b in beklenen))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--profil", default="tam")
    p.add_argument("--gorev", help="virgüllü görev kimlikleri (varsayılan hepsi)")
    p.add_argument("--tavan", type=int, default=12, help="en fazla N claude -p")
    p.add_argument("--tarih", default=time.strftime("%Y-%m-%d"))
    ns = p.parse_args(argv)
    profiller = json.loads((DIZIN / "profiller.json").read_text(encoding="utf-8"))
    gorevler = json.loads((DIZIN / "gorevler.json").read_text(encoding="utf-8"))
    if ns.gorev:
        gorevler = [g for g in gorevler if g["id"] in ns.gorev.split(",")]
    gorevler = gorevler[:ns.tavan]
    ek = profiller[ns.profil]["ek"]
    CIKTI.mkdir(parents=True, exist_ok=True)
    yol = CIKTI / f"{ns.tarih}-{ns.profil}.tsv"
    satir = ["gorev\tinput\tcache_creation\tcache_read\toutput\tsure_sn\tusd\tarac_isabet\tkalite\taraclar\thata"]
    for g in gorevler:
        o = kos(g["istem"], ek, cwd=str(KOK) if g.get("cwd") == "repo" else None)
        i, cc, cr, out = jeton(o["usage"])
        satir.append("\t".join(str(v) for v in (g["id"], i, cc, cr, out, o["sure"], round(o["usd"], 4), isabet(o["araclar"], g["arac"]),
                                                puanla(o["metin"], g["rubrik"]), ",".join(dict.fromkeys(o["araclar"])), o["hata"])))
        print(satir[-1], flush=True)
    yol.write_text("\n".join(satir) + "\n", encoding="utf-8")
    print("->", yol)


if __name__ == "__main__":
    sys.exit(main())
