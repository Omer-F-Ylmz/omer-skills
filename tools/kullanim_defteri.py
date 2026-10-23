"""Kullanım defteri (ZORUNLU-KULLANIM-1 m5): kurulu her aracın son kullanım tarihi + sayısı, oturum dökümlerinden.
  python tools/kullanim_defteri.py [gün=14]   → .kos/kopru/kullanim-defteri.json + hiç kullanılmayanlar .kos/kopru/kullanim-kuyruk.md
Araç kaldırılmaz; kullanılmayan için 'neden' (seçilmedi mi, çalışmıyor mu) düzeltme işi olarak kuyruk dosyasına yazılır."""
import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import katalog_ara  # noqa: E402

PROJELER = Path.home() / ".claude/projects"
TUR = {"skill", "ajan", "cli", "mcp", "plugin"}


def tara(gun):
    """Son `gun` günde değişen dökümler → ({skill: [say, son]}, {ajan: ...}, {mcp sunucu: ...}, [(bash komutu, zaman)])."""
    esik = time.time() - gun * 86400
    sk, ag, mcp, sh = {}, {}, {}, []
    for yol in PROJELER.glob("*/*.jsonl"):
        try:
            t = yol.stat().st_mtime
            if t < esik:
                continue
            satirlar = [l for l in yol.open(encoding="utf-8", errors="replace") if '"tool_use"' in l]
        except OSError:  # başka oturum dökümü silmiş olabilir
            continue
        for l in satirlar:
            try:
                m = json.loads(l).get("message") or {}
            except ValueError:
                continue
            for b in m.get("content") if isinstance(m.get("content"), list) else ():
                if b.get("type") != "tool_use":
                    continue
                ad, gir = b.get("name", ""), b.get("input") or {}
                hedef, anahtar = (sk, str(gir.get("skill", "")).split(":")[-1]) if ad == "Skill" else \
                    (ag, str(gir.get("subagent_type", ""))) if ad in ("Agent", "Task") else \
                    (mcp, ad.split("__")[1]) if ad.startswith("mcp__") and ad.count("__") >= 2 else (None, None)
                if hedef is not None:
                    s = hedef.setdefault(anahtar, [0, 0])
                    s[0] += 1
                    s[1] = max(s[1], t)
                elif ad == "Bash":
                    sh.append((str(gir.get("command", "")), t))
    return sk, ag, mcp, sh


def defter(gun=14):
    sk, ag, mcp, sh = tara(gun)
    sonuc = {}
    for s in katalog_ara.KATALOG.read_text(encoding="utf8").splitlines():
        o = json.loads(s)
        if o["tur"] not in TUR:
            continue
        kisa = o["ad"].split(":")[-1]
        if o["tur"] in ("skill", "plugin"):
            say = sk.get(kisa, [0, 0])
        elif o["tur"] == "ajan":
            say = ag.get(kisa, [0, 0])
        elif o["tur"] == "mcp":
            say = mcp.get(o["ad"], [0, 0])
        else:
            r = re.compile(r"(?i)(?<![\w-])" + re.escape(kisa) + r"(?![\w-])")
            ts = [t for c, t in sh if r.search(c)]
            say = [len(ts), max(ts, default=0)]
        sonuc[o["ad"]] = {"tur": o["tur"], "sayi": say[0], "son": time.strftime("%Y-%m-%d", time.localtime(say[1])) if say[1] else None}
    return sonuc


if __name__ == "__main__":
    gun = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    d = defter(gun)
    (KOK / ".kos/kopru/kullanim-defteri.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    hic = sorted(a for a, v in d.items() if not v["sayi"])
    (KOK / ".kos/kopru/kullanim-kuyruk.md").write_text(
        f"# {gun} gündür hiç kullanılmayan araçlar ({len(hic)}/{len(d)})\nHer biri için: seçilmedi mi (zorunlu_arac seçimi) yoksa çalışmıyor mu? Düzelt; araç kaldırılmaz.\n\n"
        + "\n".join(f"- {a} ({d[a]['tur']})" for a in hic) + "\n", encoding="utf-8")
    print(f"{len(d)} araç · {gun} gün hiç kullanılmayan {len(hic)}")
