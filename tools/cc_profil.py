"""TOKEN-1: `claude -p` arka plan profili — profiller/cc-arka.json'dan yalnız başlatma argümanı + env eki üretir.
Kurulu hiçbir şeye dokunmaz: MCP alt kümesi geçici --mcp-config'e (~/.claude.json girdileri olduğu gibi, ${VAR} açılmaz),
skill gövdeleri tek geçici dosyaya (--append-system-prompt-file), plugin kapatma + TTL tek --settings JSON'una.
Hook kapatılmaz (disableAllHooks · --bare · --safe-mode yok). CC_PROFIL_ZORLA=tam → profil ek argüman üretmez."""
import json
import os
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
PROFIL = KOK / "profiller" / "cc-arka.json"


def _yaz(yol, metin):
    """İçerik aynıysa dokunmaz; LF korunur (önek koşular arasında bayt bayt sabit)."""
    yol.parent.mkdir(parents=True, exist_ok=True)
    b = metin.encode("utf-8")
    if not yol.is_file() or yol.read_bytes() != b:
        yol.write_bytes(b)
    return yol


def kur(ad, env=None, ana=Path.home() / ".claude.json", profiller=PROFIL, gecici=None, ek_ayar=None):
    """→ (argv eki, env eki). env eki yalnız enjeksiyon kapatan (pluginKapat'lı) profilde CC_PROFIL=ad — jev-skill.ps1 erken çıkar.
    ek_ayar: çağıranın kendi --settings JSON'u; profilinkiyle tek --settings'te birleşir (iki --settings birbirini ezmesin)."""
    env = os.environ if env is None else env
    tum = json.loads(Path(profiller).read_text(encoding="utf-8"))
    if ad not in tum:
        raise ValueError(f"bilinmeyen profil: {ad} (var: {', '.join(tum)})")
    p = {} if env.get("CC_PROFIL_ZORLA") == "tam" else tum[ad]
    gecici = Path(gecici or Path(tempfile.gettempdir()) / "cc_profil")
    args, ayar = [], dict(ek_ayar or {})
    if "mcp" in p:
        sunucu = json.loads(Path(ana).read_text(encoding="utf-8")).get("mcpServers", {})
        if yok := [m for m in p["mcp"] if m not in sunucu]:
            raise ValueError(f"bilinmeyen MCP: {', '.join(yok)}")
        mcp = json.dumps({"mcpServers": {m: sunucu[m] for m in p["mcp"]}}, ensure_ascii=False, indent=1)
        args += ["--strict-mcp-config", "--mcp-config", str(_yaz(gecici / f"{ad}-mcp.json", mcp))]
    if "skills" in p:
        yollar = [KOK / s for s in p["skills"]]  # mutlak yol KOK'u ezer
        if yok := [str(y) for y in yollar if not y.is_file()]:
            raise FileNotFoundError(f"skill dosyası yok: {', '.join(yok)}")
        govde = "\n\n".join(f'<skill yol="{y.as_posix()}">\n{y.read_text(encoding="utf-8")}\n</skill>' for y in yollar)
        args += ["--disable-slash-commands", "--append-system-prompt-file", str(_yaz(gecici / f"{ad}-skill.md", govde))]
    if "pluginKapat" in p:
        ayar["enabledPlugins"] = {x: False for x in p["pluginKapat"]}
    if "ttl" in p:
        ayar["promptCacheTtl"] = p["ttl"]
    if ayar:
        args += ["--settings", json.dumps(ayar)]
    return args, ({"CC_PROFIL": ad} if "pluginKapat" in p else {})
