"""TOKEN-8 f2b iş 2 önek ölçümü (4 claude -p): A = tam ~/.claude/agents, B = çekirdek liste.
İkisi de geçici CLAUDE_CONFIG_DIR (dizinler junction, dosyalar kopya) → yalnız agents farkı. Canlı ~/.claude'a yazılmaz.
Çıktı: kol başına wire girdisi (inp+cw+cr) + transcript agent_listing_delta tür sayısı/karakter + diğer ek boyutları."""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf8")
EV = Path.home() / ".claude"
WT = Path("C:/Projeler/omer-skills-wt/token8")
CEKIRDEK = [s.strip() for s in (Path(__file__).parent / "cekirdek.txt").read_text(encoding="utf8").split() if s.strip()]
TABAN = ["-p", "--output-format", "json", "--model", "sonnet", "--settings", json.dumps({"promptCacheTtl": "5m"})]


def kur(kok, tam):
    kok.mkdir()
    for p in EV.iterdir():
        if p.name == "agents":
            continue
        if p.is_dir():
            subprocess.run(["cmd", "/c", "mklink", "/J", str(kok / p.name), str(p)], capture_output=True, check=True)
        else:
            shutil.copy2(p, kok / p.name)
    shutil.copy2(Path.home() / ".claude.json", kok / ".claude.json")  # varsayılan kurulumun okuduğu dosya
    if tam:
        subprocess.run(["cmd", "/c", "mklink", "/J", str(kok / "agents"), str(EV / "agents")], capture_output=True, check=True)
    else:
        (kok / "agents").mkdir()
        for a in CEKIRDEK:
            shutil.copy2(EV / "agents" / f"{a}.md", kok / "agents" / f"{a}.md")


def sok(kok):
    for p in kok.iterdir():
        if p.is_junction():
            os.rmdir(p)  # junction: yalnız bağ silinir
    shutil.rmtree(kok)


def ekler(sid):
    for f in (EV / "projects").glob(f"*/{sid}.jsonl"):
        d = {}
        for s in f.read_text(encoding="utf8").splitlines():
            at = json.loads(s).get("attachment") or {}
            t = at.get("type")
            if t == "agent_listing_delta":
                d["ajan_n"] = len(at.get("addedTypes") or [])
                d["ajan_kr"] = len("\n".join(at.get("addedLines") or []))
            elif t == "skill_listing":
                d["skill_kr"] = len(json.dumps(at, ensure_ascii=False))
            elif t == "mcp_instructions_delta":
                d["mcp_kr"] = len(json.dumps(at, ensure_ascii=False))
        return d
    return None


if __name__ == "__main__":
    tmp = Path(tempfile.mkdtemp(prefix="t8ajan_"))
    try:
        kur(tmp / "A", True); kur(tmp / "B", False)
        sira = ["A", "B", "B", "A"]
        for kol in sira:
            env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}  # api-kredi.kapali
            env["CLAUDE_CONFIG_DIR"] = str(tmp / kol)
            r = subprocess.run(["claude", *TABAN], input="tamam", capture_output=True, text=True, encoding="utf8",
                               cwd=WT, env=env, timeout=300, creationflags=0x08000000)
            try:
                j = json.loads(r.stdout)
            except ValueError:
                print(kol, "rc", r.returncode, r.stdout[:200], r.stderr[:200]); continue
            u = j.get("usage", {})
            top = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
            print(json.dumps({"kol": kol, "sid": j.get("session_id"), "girdi": top, "cw": u.get("cache_creation_input_tokens"),
                              "cr": u.get("cache_read_input_tokens"), "ekler": ekler(j.get("session_id"))}, ensure_ascii=False), flush=True)
    finally:
        for k in ("A", "B"):
            if (tmp / k).exists():
                sok(tmp / k)
        shutil.rmtree(tmp, ignore_errors=True)
