"""RUFLO-1 d10 onay betiği — Desktop koşar. Günlük öğrenme kancasını (tools/ogrenme/kanca.py) ~/.claude/settings.json hooks'a ekler.

  python onay/ruflo_1_kanca.py --kuru   # plan: hangi olaya eklenecek, settings dışı farkı (varsayılan)
  python onay/ruflo_1_kanca.py uygula   # yedek (~/.claude/yedek/ruflo1-kanca-*) → SubagentStart · SubagentStop · SessionEnd girdisi
  python onay/ruflo_1_kanca.py --geri   # yalnız bu komutun girdilerini söker
Yalnız hooks altındaki bu üç olaya kendi girdisini ekler/söker; permissions, env, diğer kancalar (block-destructive, gitleaks,
push-kapı) dokunulmaz — değişirse yazmadan rc=1. kanca.py ana repoda (kol/ruflo main'e birleşmiş) olmalı. OGRENME_KANCA=0 kapatır.
"""
import json
import shutil
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "onay"))
from kalite_3_uygula import EV, mcp_var_mi  # noqa: E402

KANCA = Path("C:/Projeler/omer-skills/tools/ogrenme/kanca.py")
KOMUT = f'python -S "{KANCA}"'
OLAYLAR = ("SubagentStart", "SubagentStop", "SessionEnd")


def _bizim(g):
    return any(h.get("command") == KOMUT for h in g.get("hooks", []))


def degistir(ayar, geri=False):
    """→ (yeni ayar, değişen olaylar). Girdi sözlüğü değişmez."""
    yeni = json.loads(json.dumps(ayar))
    hooks, degisen = yeni.setdefault("hooks", {}), []
    for o in OLAYLAR:
        var = [g for g in hooks.get(o, []) if _bizim(g)]
        if geri and var:
            hooks[o] = [g for g in hooks[o] if not _bizim(g)]
            if not hooks[o]:
                del hooks[o]
            degisen.append(o)
        elif not geri and not var:
            hooks.setdefault(o, []).append({"hooks": [{"type": "command", "command": KOMUT, "timeout": 5}]})
            degisen.append(o)
    return yeni, degisen


def _diger(ayar):
    """Bizim girdilerimiz dışındaki her şey (güvenlik ayarları dahil) — önce = sonra şartı."""
    x = json.loads(json.dumps(ayar))
    for o in OLAYLAR:
        if o in x.get("hooks", {}):
            x["hooks"][o] = [g for g in x["hooks"][o] if not _bizim(g)] or None
    x.get("hooks", {}).update({o: None for o in OLAYLAR})
    return x


def main(ev=EV, kip=None, kanca_py=KANCA):
    kip = kip or (sys.argv[1] if len(sys.argv) > 1 else "--kuru")
    yol = ev / ".claude" / "settings.json"
    ayar = json.loads(yol.read_text(encoding="utf-8"))
    once = mcp_var_mi(ev)
    yeni, degisen = degistir(ayar, geri=kip == "--geri")
    if _diger(yeni) != _diger(ayar):
        print("HATA: kanca dışı ayar değişecekti — yazılmadı")
        return 1
    print(f"kanca.py: {'var' if kanca_py.exists() else 'YOK (kol/ruflo main değil)'} · değişecek: {', '.join(degisen) or '-'}")
    if kip in ("uygula", "--geri") and degisen:
        if kip == "uygula" and not kanca_py.exists():
            print("uygulanmadı")
            return 1
        yedek = ev / ".claude" / "yedek" / f"ruflo1-kanca-{kip.strip('-')}-{time.strftime('%Y%m%d-%H%M%S')}"
        yedek.mkdir(parents=True)
        shutil.copy2(yol, yedek / "settings.json")
        yol.write_bytes((json.dumps(yeni, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
        print(f"{'uygulandı' if kip == 'uygula' else 'geri alındı'} · yedek {yedek}")
    ok = once == mcp_var_mi(ev)
    print("mcp önce=sonra" if ok else "HATA: MCP listesi değişti")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
