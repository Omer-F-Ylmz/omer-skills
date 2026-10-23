"""MCP-AÇ-1: köprü ajanlarına görev türüne göre MCP profili (ajan_sira.py --mcp-config).
Tür tespiti zorunlu_arac.GORSEL ile aynı sözlük; tanımlar ~/.claude.json + ecc eklentisi .mcp.json'dan alınır (env değerleri yalnız yeni dosyaya kopyalanır, basılmaz).
  python mcp_profil.py "<görev metni>"    seçilen MCP adları (sınama)"""
import json
import os
import re
import sys
from pathlib import Path

TEMEL = ["ruflo"]
TUR = [  # (desen, MCP'ler); türler birleşir
    (r"(?i)site-3d|\b(site|landing|three(\.js)?|webgl|3d|frontend)\b", ["rea", "playwright", "chrome-devtools", "context7", "21st"]),
    (r"(?i)\b(render\w*|blender)\b", ["blender"]),
    (r"(?i)\bvideo\w*", ["premiere-pro"]),
]
KEEP = {  # MCP-AÇ-2: yalnız bu araçlar açık kalır; listede olmayan MCP'ler (blender, context7, premiere-pro) tam kalır
    "ruflo": ["agentdb_pattern-search", "agentdb_pattern-store", "hooks_intelligence_pattern-search", "hooks_intelligence_pattern-store", "memory_search", "memory_store", "memory_retrieve"],
    "rea": ["capture_web_screenshot", "inspect_web_page", "analyze_web_bundle", "compare_web_screenshots", "compare_web_captures",
            "capture_browser_scenario", "list_browser_targets", "inspect_web_network_capture", "export_web_scripts", "observe_web_session",
            "trace_web_module_imports", "trace_web_source_location", "discover_webmcp_tools", "open_binary", "close_binary"],
    "playwright": ["browser_navigate", "browser_snapshot", "browser_take_screenshot", "browser_evaluate", "browser_click", "browser_resize",
                   "browser_wait_for", "browser_close", "browser_console_messages", "browser_type", "browser_fill_form", "browser_press_key"],
    "chrome-devtools": ["navigate_page", "new_page", "list_pages", "select_page", "close_page", "take_screenshot", "take_snapshot",
                        "evaluate_script", "resize_page", "emulate", "list_console_messages", "get_console_message", "list_network_requests",
                        "get_network_request", "click", "fill", "wait_for", "press_key", "lighthouse_audit", "get_css_styles"],
    "21st": ["search", "search_logo", "search_picker", "get_component", "get_inspiration", "get_theme", "get_generation", "get_generation_job"],
}
DOGRUDAN = ["figma", "canva", "claude-design"]  # OAuth'u CC tutar (kapıdan 401); katalog: tools/mcp_kapi.py katalog
ARACLAR = Path(__file__).resolve().parents[1] / ".kos" / "kopru" / "mcp-araclar.json"  # tools/mcp_ac2_olc.py araclar ile yenilenir
KAYNAK = [Path.home() / ".claude.json", *sorted((Path.home() / ".claude/plugins/cache/ecc/ecc").glob("*/.mcp.json"))]


CODEMODE = ("[codemode K2p] 2+ ardışık araç ya da büyük çıktı (git log/diff/show, web arama+fetch, tarayıcı gezintisi) gerektiğinde araçları tek tek "
            "çağırma: Bash ile `python C:/Projeler/omer-skills/tools/cm.py run -c \"<düz JS>\"` (önce `cm.py search \"<görev>\"`); say/süz, yalnız özeti return et.")


def codemode():
    """CODE-MODE-AB-1 (24 Eki varsayılan AÇIK; kapatmak: CC_CODEMODE=0) → ajan istemine K2p hatırlatması (Bash ajan profilinde zaten açık). Ölçüm: Bash+cm.py kolu token −73/−90%, doğruluk 6/6 (A: 4/6)."""
    return "" if os.environ.get("CC_CODEMODE") == "0" else "\n" + CODEMODE


def tanimlar():
    t = {}
    for f in KAYNAK:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for ad, v in d.get("mcpServers", d).items():
            if isinstance(v, dict):
                t.setdefault(ad, v)
    return t


def sec(metin):
    ad = list(TEMEL)
    for desen, mcp in TUR:
        if re.search(desen, metin):
            ad += [m for m in mcp if m not in ad]
    return ad


def kapat(adlar):
    """KEEP'li seçili MCP'lerin geri kalan araçları → --disallowedTools girdileri (sıralı, koşular arası aynı). Araç listesi yoksa boş."""
    try:
        tum = json.loads(ARACLAR.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [f"mcp__{m}__{a}" for m in adlar if m in KEEP for a in tum.get(m, []) if a not in KEEP[m]]


def ertele(argv, mcp, tam=True):
    """MCP-AÇ-2: KEEP dışı MCP araçlarını --disallowedTools ile kapatır (sıralı → istem öneki koşular arası sabit).
    ERİŞİM-TAM-1: ertelemeyi KEEP değil profiller/cc-arka.json "ajan" sağlar (ENABLE_TOOL_SEARCH=true + --tools'ta ToolSearch; docs/erisim-haritasi.md)."""
    kapali = kapat(list(json.loads(Path(mcp).read_text(encoding="utf-8"))["mcpServers"]))
    return list(argv) + ["--disallowedTools", ",".join(kapali)] if kapali else list(argv)


def agir(mcp):
    """ERİŞİM-TAM-1: doğrudan MCP araç sayısı > 20 ise ertelemeli yükleme (ToolSearch) kazandırır; değilse ToolSearch'ün sabit ~6.5k yükü zarar (kapı-tek: 15.8k, +ts: 22.3k)."""
    try:
        kat = json.loads((Path(__file__).resolve().parents[1] / ".kos" / "kopru" / "kapi-katalog.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        kat = {}
    ad = [m for m in json.loads(Path(mcp).read_text(encoding="utf-8"))["mcpServers"] if m != "kapi"]
    return sum(len(KEEP[m]) if m in KEEP else len(kat.get(m) if isinstance(kat.get(m), list) else [0] * 20) for m in ad) > 20


def yaz(metin, hedef):
    """Profil dosyasını hedef'e yazar; tanımı olmayan MCP atlanır. Döner: seçilen adlar."""
    t = tanimlar()
    ad = [m for m in sec(metin) if m in t]
    sunucular = {m: t[m] for m in ad}
    if os.environ.get("CC_MCP_KAPI") != "0":  # ERİŞİM-TAM-1: kalan tüm MCP'ler tek "kapi" arkasında (ara/cagir); OAuth'lular doğrudan
        sunucular["kapi"] = {"command": sys.executable, "args": ["-I", str(Path(__file__).with_name("mcp_kapi.py"))], "env": {"KAPI_HARIC": ",".join(ad + DOGRUDAN)}}
        if re.search(r"(?i)figma|canva|claude.design", metin):  # OAuth'lular yalnız anılınca (şemaları ~1.6k jeton)
            sunucular.update({m: t[m] for m in DOGRUDAN if m in t and m not in sunucular})
    Path(hedef).write_text(json.dumps({"mcpServers": sunucular}), encoding="utf-8")
    return ad


if __name__ == "__main__":
    print(" ".join(m for m in sec(" ".join(sys.argv[1:])) if m in tanimlar()))
