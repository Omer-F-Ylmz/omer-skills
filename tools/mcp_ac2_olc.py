"""MCP-AÇ-2 ölçüm: ajan_sira.baslat_argv ile tek `claude -p` koşusu (stream-json) → init araç adları + giriş jetonu.
  python mcp_ac2_olc.py araclar            MCP başına araç adlarını .kos/kopru/mcp-araclar.json'a yazar (1 koşu)
  python mcp_ac2_olc.py olc <tur> <kol>    tur: ok|site|render, kol: bos|eski|yeni|filtre → docs/token/mcp-ac-2.tsv'ye satır
Koşu başı --max-budget-usd 0.5; haiku."""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / ".kos" / "kopru"), str(KOK / "tools")]
import ajan_sira, mcp_profil  # noqa: E402

ARAC_JSON = KOK / ".kos" / "kopru" / "mcp-araclar.json"
TSV = KOK / "docs" / "token" / "mcp-ac-2.tsv"
GOREV = {
    "ok": ("OK yaz", None),
    "site": ("site-3d: tek dosya index.html yaz — three.js (CDN importmap) ile dönen bir küp sahnesi. Başka dosya/araç yok.", "index.html"),
    "render": ("render: Blender'da küp ekleyip PNG render alan bpy betiğini render.py dosyasına yaz (Blender'ı çalıştırma). Başka dosya yok.", "render.py"),
}
KALITE = {"index.html": ("three", "<script"), "render.py": ("bpy", "render")}


def kos(metin, kol, cwd):
    os.environ["CC_MCP_ERTELE"] = {"yeni": "1", "filtre": "filtre"}.get(kol, "0")
    mcp = Path(tempfile.gettempdir()) / f"mcp-ac2-{os.getpid()}.json"
    ad = mcp_profil.yaz(metin, mcp)
    if kol == "bos":  # mcp-ac-1 tabanı: boş MCP
        mcp.write_text('{"mcpServers":{}}', encoding="utf-8"); ad = []
    argv, env = ajan_sira.baslat_argv("low", "haiku", mcp)
    argv[argv.index("--output-format") + 1] = "stream-json"
    argv += ["--verbose", "--max-budget-usd", "0.5"]
    t = time.time()
    p = subprocess.run(argv, input=metin, capture_output=True, text=True, encoding="utf-8", cwd=cwd, env=env, timeout=600)
    sure = time.time() - t
    ev = [json.loads(x) for x in p.stdout.splitlines() if x.startswith("{")]
    mcp.unlink(missing_ok=True)
    return ad, ev, sure, p


def ozet(ev):
    init = next((e for e in ev if e.get("type") == "system" and e.get("subtype") == "init"), {})
    asist = [e for e in ev if e.get("type") == "assistant" and not e.get("parent_tool_use_id")]
    u0 = (asist[0]["message"].get("usage") or {}) if asist else {}
    son = next((e for e in reversed(ev) if e.get("type") == "result"), {})
    us = son.get("usage") or {}
    tam = lambda u: (u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)
    return {"araclar": init.get("tools", []), "ilk_giris": tam(u0), "ilk_okuma": u0.get("cache_read_input_tokens") or 0,
            "top_giris": tam(us), "top_okuma": us.get("cache_read_input_tokens") or 0, "tur": son.get("num_turns"),
            "hata": bool(son.get("is_error")), "usd": son.get("total_cost_usd"), "sonuc": (son.get("result") or "")[:60]}


if __name__ == "__main__":
    if sys.argv[1] == "araclar":
        d = Path(tempfile.mkdtemp(prefix="mcp-ac2-"))
        os.environ["CC_MCP_ERTELE"] = "0"
        ad, ev, sure, p = kos("site-3d render video OK yaz", "eski", str(d))
        t = ozet(ev)["araclar"]
        sonuc = {}
        for a in t:
            if a.startswith("mcp__"):
                _, sunucu, *ara = a.split("__")
                sonuc.setdefault(sunucu, []).append("__".join(ara))
        ARAC_JSON.write_text(json.dumps({k: sorted(v) for k, v in sorted(sonuc.items())}, indent=1), encoding="utf-8")
        print({k: len(v) for k, v in sonuc.items()}, "yüklü:", ad)
    else:
        tur, kol = sys.argv[2], sys.argv[3]
        metin, dosya = GOREV[tur]
        d = Path(tempfile.mkdtemp(prefix="mcp-ac2-"))
        ad, ev, sure, p = kos(metin, kol, str(d))
        o = ozet(ev)
        kalite = "-" if not dosya else int((d / dosya).is_file() and all(k in (d / dosya).read_text(encoding="utf-8", errors="ignore").lower() for k in KALITE[dosya]))
        TSV.parent.mkdir(parents=True, exist_ok=True)
        if not TSV.exists():
            TSV.write_text("tarih\ttur\tkol\tmcp\tilk_giris\tilk_okuma\ttop_giris\ttop_okuma\tisabet%\tsure_s\ttur_say\tkalite\thata\tusd\n", encoding="utf-8")
        isabet = round(100 * o["top_okuma"] / o["top_giris"], 1) if o["top_giris"] else 0
        satir = [time.strftime("%Y-%m-%d %H:%M"), tur, kol, ",".join(ad), o["ilk_giris"], o["ilk_okuma"], o["top_giris"], o["top_okuma"], isabet, round(sure), o["tur"], kalite, int(o["hata"]), round(o["usd"] or 0, 4)]
        with TSV.open("a", encoding="utf-8") as f:
            f.write("\t".join(map(str, satir)) + "\n")
        print("\t".join(map(str, satir)), o["sonuc"])
