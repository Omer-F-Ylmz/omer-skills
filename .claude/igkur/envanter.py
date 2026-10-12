"""Kurulu set envanteri (yalnız adlar; env değeri yok) → envanter.txt; araç-tipi adaylar → araclar.tsv."""
import json, os, pathlib, subprocess

H = pathlib.Path.home() / ".claude"
CIK = pathlib.Path(__file__).parent
sat = []
sat += [f"skill\t{p.name}" for p in (H / "skills").iterdir()]
for mp in (H / "plugins" / "cache").iterdir():
    for pl in mp.iterdir() if mp.is_dir() else []:
        sat.append(f"plugin\t{mp.name}/{pl.name}")
for f in [pathlib.Path.home() / ".claude.json", H / "settings.json"]:
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        continue
    sat += [f"mcp\t{k}" for k in d.get("mcpServers", {})]
    for pr in d.get("projects", {}).values():
        sat += [f"mcp\t{k}" for k in pr.get("mcpServers", {})]
    sat += [f"plugin-acik\t{k}" for k, v in d.get("enabledPlugins", {}).items() if v]
for kom, tur in [(["npm", "ls", "-g", "--depth=0", "--parseable"], "npm"), (["uv", "tool", "list"], "uv")]:
    try:
        o = subprocess.run(kom, capture_output=True, text=True, shell=True, timeout=60).stdout
        sat += [f"{tur}\t{x.strip().split(os.sep)[-1].split()[0]}" for x in o.splitlines() if x.strip() and not x.startswith("-")]
    except Exception:
        pass
sat = sorted(set(sat))
(CIK / "envanter.txt").write_text("\n".join(sat) + "\n", encoding="utf-8", newline="\n")
ARAC = {"CLI", "skill", "MCP", "plugin", "prompt"}
satir = (CIK / "birlesik.tsv").read_text(encoding="utf-8").splitlines()
ar = [satir[0]] + [s for s in satir[1:] if set(s.split("\t")[2].split(",")) & ARAC or "github.com" in s.split("\t")[3]]
(CIK / "araclar.tsv").write_text("\n".join(ar) + "\n", encoding="utf-8", newline="\n")
print(len(sat), "envanter;", len(ar) - 1, "araç adayı")
