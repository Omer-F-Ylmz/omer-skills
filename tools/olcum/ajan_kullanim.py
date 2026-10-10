"""KÜTÜPHANE-5: ajan listesi kısma adayı. /context dökümündeki Custom Agents tablosu + CC oturum transcript'lerinde
subagent_type sayımı → kullanılmayan PLUGIN ajanları için deny profili (permissions.deny Agent(<ad>)).
  python tools/olcum/ajan_kullanim.py .kos/kopru/context-tam.md [--gun 60] [--cikti profil-ajan.json]
Kullanıcı/proje ajanlarına dokunmaz. settings.json'a yazmaz; yalnız tools/olcum/<cikti> üretir."""
import argparse
import json
import re
import sys
import time
from pathlib import Path

D = Path(__file__).resolve().parent
KORU = re.compile(r"(code-reviewer|security|test|explore|plan|okuyucu|video|suite|aday|debug|build-error|csharp|dotnet|msbuild|frontend|a11y|performance)", re.I)


def ajanlar(context_md):
    L = Path(context_md).read_text(encoding="utf-8").splitlines()
    i = L.index("### Custom Agents")
    out = {}
    for l in L[i + 4:]:
        if not l.startswith("|"):
            break
        c = [x.strip() for x in l.strip("|").split("|")]
        t = c[2].replace("~", "").replace("<", "").strip()
        out[c[0]] = (c[1], float(t[:-1]) * 1000 if t.endswith("k") else float(t or 0))
    return out


def kullanim(gun):
    say = {}
    sinir = time.time() - gun * 86400
    for f in (Path.home() / ".claude" / "projects").rglob("*.jsonl"):
        try:
            if f.stat().st_mtime < sinir:
                continue
            with f.open(encoding="utf-8", errors="replace") as h:
                for s in h:
                    if "subagent_type" not in s:
                        continue
                    for m in re.finditer(r'"subagent_type"\s*:\s*"([^"]+)"', s):
                        say[m.group(1)] = say.get(m.group(1), 0) + 1
        except OSError:
            continue
    return say


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("context")
    p.add_argument("--gun", type=int, default=60)
    p.add_argument("--cikti", default="profil-ajan.json")
    ns = p.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    a = ajanlar(ns.context)
    k = kullanim(ns.gun)
    plugin = {n: v for n, v in a.items() if v[0] == "Plugin"}
    kullanilan = {n for n in a if k.get(n)}
    gizle = sorted(n for n in plugin if not k.get(n) and not KORU.search(n.split(":")[-1]))
    tasarruf = sum(plugin[n][1] for n in gizle)
    print(f"ajan {len(a)} (plugin {len(plugin)}, {int(sum(v[1] for v in plugin.values()))} jeton) · {ns.gun} günde kullanılan {len(kullanilan)}: "
          + ", ".join(f"{n}={k[n]}" for n in sorted(kullanilan, key=lambda x: -k[x])[:20]))
    print(f"gizlenecek plugin ajanı {len(gizle)} · tahmini −{int(tasarruf)} jeton · korunan plugin {len(plugin) - len(gizle)}")
    (D / ns.cikti).write_text(json.dumps({"permissions": {"deny": [f"Agent({n})" for n in gizle]}}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("->", D / ns.cikti)


if __name__ == "__main__":
    sys.exit(main())
