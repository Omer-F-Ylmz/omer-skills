"""Yetenek sağlığı: çekirdek araçlara gerçek tek çağrı, sonuç .kos/kopru/saglik.md. Model çağrısı yok (0 jeton).
  python -I tools/yetenek_saglik.py"""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
SONUC = KOK / ".kos" / "kopru" / "saglik.md"
sys.path[:0] = [str(KOK / "tools" / "ruflo")]
os.environ["CLAUDE_FLOW_ENABLE_NATIVE_BRIDGE_ON_WINDOWS"] = "1"  # #3024 kapısı: yoksa ReasoningBank registry-null
import mcp_dene  # noqa: E402
from saglik import cagri  # noqa: E402  (tools/ruflo/saglik.py: MCP araç seçimi)


def kos(cmd, t=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=t, cwd=KOK)
        return r.returncode, (r.stdout + r.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 99, str(e)[:160]


def exe(ad):
    return shutil.which(ad) or ad


def metin(o, k):
    try:
        return json.loads(o[k]["result"]["content"][0]["text"])
    except (KeyError, IndexError, TypeError, json.JSONDecodeError):
        return {}


def ruflo():
    o, _ = mcp_dene.kos([
        cagri("memory_store", key="yetenek-saglik", value="sağlık kontrolü kayıt izi", namespace="saglik"),
        cagri("memory_search", query="sağlık denetimi izi", namespace="saglik"),
        cagri("agentdb_pattern-store", pattern="sağlık sinyali: önce kırmızı, sonra yeşil", type="ders", confidence=0.8),
        cagri("agentdb_pattern-search", query="kırmızıyı önce görmek", topK=3),
        cagri("agentdb_health"),
    ])
    arama = metin(o, 3).get("results", [])
    pat = metin(o, 5)
    health = metin(o, 6)
    anlamsal = any(x.get("key") == "yetenek-saglik" for x in arama)
    if not pat.get("degraded") and pat.get("controller") == "reasoningBank" and anlamsal and health.get("available"):
        return "ok", "semantik bulma + reasoningBank + native bridge"
    return "bozuk", f"degraded={pat.get('degraded')} anlamsal={anlamsal} health={health.get('available')}"


def komut(ad, args, rc_ok=(0,)):
    rc, cikti = kos([exe(ad)] + args)
    if rc in rc_ok:
        return "ok", f"rc={rc}"
    return "bozuk", (cikti.splitlines() or [f"rc={rc}"])[-1][:100]


def dosya(yol):
    return ("ok", yol) if (KOK / yol).exists() or Path(yol).expanduser().exists() else ("bozuk", f"yok: {yol}")


def ev(ad):
    return Path.home() / ".claude" / ad


DENETIM = [
    ("ruflo (store+semantik+pattern)", ruflo, "ruflo: `ruflo.cmd mcp start`; bridge env ~/.claude.json ruflo.env"),
    ("beyin (ara)", lambda: komut(sys.executable, ["-I", "-X", "utf8", "tools/beyin.py", "ara", "sağlık", "--k", "1"]), "tools/beyin.py çalışmıyor"),
    ("headroom", lambda: komut("headroom", ["--version"]), "pip/uv ile yeniden kur (uv tool)"),
    ("rtk", lambda: komut("rtk", ["--version"]), "rtk yeniden kur"),
    ("graphify (kod)", lambda: dosya("graphify-out/graph.json") if komut("graphify", ["--help"])[0] == "ok" else ("bozuk", "graphify yok"), "graphify update ."),
    ("mcp_kapi (ara)", lambda: komut(sys.executable, ["-I", "-X", "utf8", "tools/mcp_kapi.py", "ara", "ruflo"]), "kapi-katalog.json: mcp_kapi.py katalog"),
    ("context-mode", lambda: ("ok", "dizin") if ev("context-mode").is_dir() else ("bozuk", "~/.claude/context-mode yok"), "context-mode eklentisini kur"),
    ("playwright", lambda: ("ok", shutil.which("playwright")) if shutil.which("playwright") else ("bozuk", "playwright PATH'te yok"), "npm i -g playwright"),
    ("fable-dusunme", lambda: dosya(str(ev("skills") / "fable-dusunme" / "SKILL.md")), "skill'i yeniden kur"),
]
DESKTOP_KANITI = [("Desktop köprüsü (cc-kopru)", "tools/cc-kopru"), ("kuyruk ajanı (ajan-sira)", ".kos/kopru/ajan-sira"),
                  ("ücretsiz havuz", "tools/ucretsiz_havuz.py")]


def main():
    satir = []
    for ad, fn, onarim in DENETIM:
        durum, kanit = fn()
        satir.append((ad, durum, kanit, "" if durum == "ok" else onarim))
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = [f"# Yetenek sağlığı · {zaman}", "", "| Araç | CC | Kanıt | Onarım |", "|---|---|---|---|"]
    md += [f"| {a} | {d} | {k} | {o} |" for a, d, k, o in satir]
    md += ["", "| Yüzey | Kurulum (CC'den yalnız varlık) |", "|---|---|"]
    md += [f"| {ad} | {'ok' if (KOK / yol).exists() else 'bozuk'} `{yol}` |" for ad, yol in DESKTOP_KANITI]
    SONUC.write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    for a, d, k, _ in satir:
        print(f"{d:6} {a}: {k}")
    print("yazıldı:", SONUC.relative_to(KOK).as_posix())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
