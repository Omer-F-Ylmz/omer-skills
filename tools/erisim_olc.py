"""ERİŞİM-TAM-1 ölçüm: ajan_sira.baslat_argv ile `claude -p "OK yaz"` (haiku), TÜM MCP'ler açık, ENABLE_TOOL_SEARCH kolları → ilk istem jetonu.
  python erisim_olc.py <kol>...    kol: bos | profil | false | true | auto | unset (+ts: --tools'a ToolSearch ekle)  (bos = boş MCP tabanı); satırlar docs/token/erisim-tam-1.tsv'ye eklenir
Koşu başı --max-budget-usd 0.5."""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / ".kos" / "kopru"), str(KOK / "tools")]
import ajan_sira, mcp_profil  # noqa: E402

TSV = KOK / "docs" / "token" / "erisim-tam-1.tsv"
BASLIK = "tarih\tistem\tkol\tmcp_say\tarac_say\ttoolsearch\tilk_giris\tilk_okuma\tilk_yazma\ttop_giris\tmcp_cagri\tmcp_hata\tsure_s\thata"
ISTEM = os.environ.get("EO_ISTEM", "OK yaz")


def kos(kol):
    tmp = Path(tempfile.gettempdir())
    mcp = tmp / f"erisim-{os.getpid()}.json"
    t = mcp_profil.tanimlar()
    if kol.startswith("kapi"):  # kapı kolu: gerçek köprü profili (ruflo doğrudan + kapi + OAuth'lular), KEEP süzgeci açık
        mcp_profil.yaz(ISTEM, mcp)
        kol, kolad = kol.replace("kapi", "profil", 1), kol
    else:
        mcp.write_text(json.dumps({"mcpServers": {} if kol == "bos" else t}), encoding="utf-8")
        os.environ["CC_MCP_ERTELE"] = "0"
        kolad = kol
    argv, env = ajan_sira.baslat_argv("low", "haiku", mcp)
    if os.environ.get("EO_PROXY"):  # teşhis: istek gövdelerini kaydeden vekil (.kos/kopru/kapi-teshis/vekil.py)
        env["ANTHROPIC_BASE_URL"] = os.environ["EO_PROXY"]
    argv[argv.index("--output-format") + 1] = "stream-json"
    i = argv.index("--settings") + 1
    ayar = json.loads(Path(argv[i]).read_text(encoding="utf-8"))
    e = ayar.setdefault("env", {})
    if os.environ.get("EO_PROXY"):
        e["ANTHROPIC_BASE_URL"] = os.environ["EO_PROXY"]
    if kol != "profil":  # profil = baslat_argv'nin verdiği ayar/env aynen (gerçek köprü yolu)
        e.pop("ENABLE_TOOL_SEARCH", None)
        env.pop("ENABLE_TOOL_SEARCH", None)
    if kol in ("profil+auto", "profil+false", "profil+true"):  # kapı kolu + ENABLE_TOOL_SEARCH değeri
        kol = kol.split("+")[1]
    if kol.split("+")[0] in ("true", "false", "auto"):
        e["ENABLE_TOOL_SEARCH"] = kol.split("+")[0]
    sf = tmp / f"erisim-ayar-{os.getpid()}.json"
    sf.write_text(json.dumps(ayar), encoding="utf-8")
    argv[i] = str(sf)
    if kol.endswith("+ts"):  # ToolSearch --tools listesinde yoksa MCP araçları yine tam yüklenir (CC belgesi)
        j = argv.index("--tools") + 1
        argv[j] += ",ToolSearch"
        kol = kol[:-3]
    argv += ["--verbose", "--max-budget-usd", "0.5"]
    ts = time.time()
    p = subprocess.run(argv, input=ISTEM, capture_output=True, text=True, encoding="utf-8", env=env, timeout=int(os.environ.get("EO_SURE", "900")), cwd=str(tmp))
    sure = time.time() - ts
    mcp.unlink(missing_ok=True); sf.unlink(missing_ok=True)
    if os.environ.get("EO_DUMP"):  # teşhis: ham akışı kol adıyla yaz
        Path(os.environ["EO_DUMP"] + f".{kolad}.jsonl").write_text(p.stdout, encoding="utf-8")
    ev = [json.loads(x) for x in p.stdout.splitlines() if x.startswith("{")]
    init = next((x for x in ev if x.get("type") == "system" and x.get("subtype") == "init"), {})
    araclar = init.get("tools", [])
    asis = next((x for x in ev if x.get("type") == "assistant"), {})
    u = asis.get("message", {}).get("usage", {})
    um = {x["message"]["id"]: x["message"]["usage"] for x in ev if x.get("type") == "assistant" and "usage" in x.get("message", {})}
    istek = [u2.get("input_tokens", 0) + u2.get("cache_creation_input_tokens", 0) + u2.get("cache_read_input_tokens", 0) for u2 in um.values()]
    top = sum(istek)
    blok = [b for x in ev if x.get("type") == "assistant" for b in x["message"].get("content", []) if isinstance(b, dict)]
    ids = {b["id"] for b in blok if b.get("type") == "tool_use" and b["name"].startswith("mcp__")}
    hata = sum(1 for x in ev if x.get("type") == "user" for b in x["message"].get("content", []) if isinstance(b, dict) and b.get("tool_use_id") in ids and b.get("is_error"))
    return [time.strftime("%Y-%m-%d %H:%M"), ISTEM[:12], kolad, len(init.get("mcp_servers", [])), len(araclar), "ToolSearch" in araclar,
            u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0),
            u.get("cache_read_input_tokens", 0), u.get("cache_creation_input_tokens", 0), str(istek), len(ids), hata, round(sure), 0 if ev else p.returncode]


if __name__ == "__main__":
    if not TSV.exists():
        TSV.write_text(BASLIK + "\n", encoding="utf-8")
    for kol in sys.argv[1:]:
        s = "\t".join(map(str, kos(kol)))
        with TSV.open("a", encoding="utf-8", newline="\n") as f:
            f.write(s + "\n")
        print(s)
