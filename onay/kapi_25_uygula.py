"""KAPI-25 onay betiği — Desktop koşar. Kalite kapısını (kalite3_hiz, ölçüt aynen) GEÇEN 5 ajanı ~/.claude/agents'a kurar.

  python onay/kapi_25_uygula.py --kuru   # (varsayılan) plan: hangi ajan, model, yeni mi üzerine mi
  python onay/kapi_25_uygula.py uygula   # varsa eskisini ~/.claude/yedek/kapi25-<zaman>/ altına alır → ajanlar/kalite3/<aile>/<ad>.md kopyalar
  python onay/kapi_25_uygula.py --geri   # son yedeği geri koyar (önceden olmayan ajan silinir)
Yalnız gevşek ~/.claude/agents yazılır; departman-* skill'leri dist/kapi-25 zip'iyle claude.ai'ye gider. MCP listesi önce=sonra değilse rc=1.
"""
import json, re, shutil, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kalite_3_uygula import EV, KOK, mcp_var_mi  # noqa: E402

KABUL = ["otm-zamanlanmis-gorev", "oyn-seviye-tasarim", "ajn-slash-komut-yazar", "fe-form-tasarimci", "oyn-oyun-envanter"]


def plan(kok=KOK):
    kaynak = {f.stem: f for f in (kok / "ajanlar" / "kalite3").glob("*/*.md")}
    return [(ad, kaynak[ad]) for ad in KABUL if ad in kaynak]


def uygula(ev=EV, kok=KOK):
    once = mcp_var_mi(ev)
    yedek = ev / ".claude" / "yedek" / f"kapi25-{time.strftime('%Y%m%d-%H%M%S')}"
    yedek.mkdir(parents=True, exist_ok=True)
    liste = plan(kok)
    for ad, kaynak in liste:
        hedef = ev / ".claude" / "agents" / f"{ad}.md"
        if hedef.exists():
            shutil.copy2(hedef, yedek / hedef.name)
        hedef.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(kaynak, hedef)
    (ev / ".claude" / "yedek" / "kapi25-son.json").write_text(
        json.dumps({"yedek": str(yedek), "ajanlar": [a for a, _ in liste]}), encoding="utf-8")
    print(f"uygulandı {len(liste)} ajan · yedek {yedek}")
    return once == mcp_var_mi(ev)


def geri(ev=EV):
    once = mcp_var_mi(ev)
    son = json.loads((ev / ".claude" / "yedek" / "kapi25-son.json").read_text(encoding="utf-8"))
    for ad in son["ajanlar"]:
        hedef, eski = ev / ".claude" / "agents" / f"{ad}.md", Path(son["yedek"]) / f"{ad}.md"
        shutil.copy2(eski, hedef) if eski.exists() else hedef.unlink(missing_ok=True)
    print(f"geri alındı {len(son['ajanlar'])} ajan")
    return once == mcp_var_mi(ev)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    kip = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
    if kip == "uygula":
        ok = uygula()
    elif kip == "--geri":
        ok = geri()
    else:
        liste = plan()
        for ad, kaynak in liste:
            m = re.search(r"^model:\s*(\S+)", kaynak.read_text(encoding="utf-8"), re.M)
            var = (EV / ".claude" / "agents" / f"{ad}.md").exists()
            print(f"ajan {ad}\tmodel={m.group(1) if m else '-'}\t{'üzerine (yedekli)' if var else 'yeni'}")
        ok = len(liste) == len(KABUL)
        if not ok:
            print(f"HATA: havuzda eksik {sorted(set(KABUL) - {a for a, _ in liste})}")
    print("mcp önce=sonra" if ok else "HATA")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
