"""TOKEN-2 mühür: settings.json · ~/.claude.json mcpServers · hooks (verdict hariç) + sayılar. Değer yazmaz, yalnız sha."""
import hashlib, json, pathlib, sys

H = pathlib.Path.home() / ".claude"
sha = lambda b: hashlib.sha256(b).hexdigest()[:16]
st = json.loads((H / "settings.json").read_text(encoding="utf-8"))
cj = json.loads((pathlib.Path.home() / ".claude.json").read_text(encoding="utf-8"))
hooks = {str(p.relative_to(H / "hooks")): sha(p.read_bytes()) for p in sorted((H / "hooks").rglob("*"))
         if p.is_file() and p.name != ".headroom-guard-verdict.json" and "__pycache__" not in p.parts}
m = {"settings": sha((H / "settings.json").read_bytes()),
     "mcpServers": sha(json.dumps(cj.get("mcpServers", {}), sort_keys=True).encode()),
     "hooks": sha(json.dumps(hooks, sort_keys=True).encode()), "hooks_dosya": hooks,
     "plugin": [sum(1 for v in st.get("enabledPlugins", {}).values() if v), len(st.get("enabledPlugins", {}))],
     "mcp": len(cj.get("mcpServers", {})), "skill": len(list((H / "skills").rglob("SKILL.md")))}
out = pathlib.Path(sys.argv[1])
if out.exists():
    eski = json.loads(out.read_text(encoding="utf-8"))
    fark = [k for k in m if m[k] != eski.get(k)]
    print("MÜHÜR EŞİT" if not fark else f"FARK: {fark}")
    for k in fark:
        if k == "hooks_dosya":
            print({f: (eski[k].get(f), m[k].get(f)) for f in set(eski[k]) | set(m[k]) if eski[k].get(f) != m[k].get(f)})
else:
    out.write_text(json.dumps(m, indent=1), encoding="utf-8")
    print("yazıldı", {k: v for k, v in m.items() if k != "hooks_dosya"})
