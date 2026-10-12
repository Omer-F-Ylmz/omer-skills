"""RUFLO-1 onay betiği — Desktop koşar. Ders yuvasını (tools/ogrenme/onsoz.py) ~/.claude/agents/*.md ajan filosuna ekler.

  python onay/ruflo_1_uygula.py --kuru   # plan: hangi ajan değişir, kabul durumu (varsayılan)
  python onay/ruflo_1_uygula.py uygula   # yedek alır → frontmatter sonrası işaretli ders bloğu
  python onay/ruflo_1_uygula.py --geri   # işaretli bloğu söker (yedek ayrıca ~/.claude/yedek/ruflo1-*)
Kapı: eşli A/B (docs/kutuphane/olcum/ruflo-1-ab-v3-*.tsv) ≥12 çift, dersli ort. puan ≥ derssiz VE jeton < derssiz; ders.py ana repoda
(kol/ruflo main'e birleşmiş) olmalı. Yalnız gevşek ~/.claude/agents dosyaları; plugin ajanlarına, settings.json'a, hook'lara
dokunulmaz; `ruflo init` koşulmaz. MCP listesi önce=sonra değilse rc=1.
"""
import shutil
import statistics
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "onay"), str(KOK / "tools" / "ogrenme")]
from kalite_3_uygula import EV, mcp_var_mi  # noqa: E402
import onsoz  # noqa: E402

TSV = [KOK / "docs" / "kutuphane" / "olcum" / f"ruflo-1-ab-v3-{a}.tsv" for a in ("kod", "rapor", "video")]


def kabul(tsv=TSV):
    """→ (geçti mi, açıklama). Yalnız iki kolu da koşmuş (aile, sıra) çiftleri; ≥12 çift. d7: v3 eşli TSV'ler (aynı sistem istemi);
    şart dersli ort. puan ≥ derssiz VE dersli toplam jeton (input+cache_creation+cache_read+output) < derssiz (Ömer: tabanın altına)."""
    try:
        satir = [s.split("\t") for t in ([tsv] if isinstance(tsv, Path) else tsv)
                 for s in t.read_text(encoding="utf-8").splitlines()[1:] if s.strip()]
    except OSError:
        return False, "ölçüm yok"
    son = {(s[1], s[2], s[3]): s for s in satir}  # aynı çift tekrar koştuysa son satır
    cift = [(a, n) for a, n, k in son if k == "derssiz" and (a, n, "dersli") in son]
    if len(cift) < 12:
        return False, f"ölçüm eksik ({len(cift)}/12 çift)"
    ort = {k: statistics.mean(float(son[(a, n, k)][4]) for a, n in cift) for k in ("derssiz", "dersli")}
    jet = {k: sum(int(x) for a, n in cift for x in son[(a, n, k)][7:11]) for k in ("derssiz", "dersli")}
    return (ort["dersli"] >= ort["derssiz"] and jet["dersli"] < jet["derssiz"],
            f"{len(cift)} çift · puan derssiz {ort['derssiz']:.3f} · dersli {ort['dersli']:.3f}"
            f" · jeton derssiz {jet['derssiz']} · dersli {jet['dersli']} ({jet['dersli'] / jet['derssiz'] - 1:+.1%})")


def ajanlar(ev=EV):
    return sorted((ev / ".claude" / "agents").glob("*.md"))


def main(ev=EV, kip=None, tsv=TSV, ders_py=Path(onsoz.DERS_PY)):
    kip = kip or (sys.argv[1] if len(sys.argv) > 1 else "--kuru")
    once = mcp_var_mi(ev)
    gecti, neden = kabul(tsv)
    print(f"kabul: {'GEÇTİ' if gecti else 'YOK'} ({neden}) · ders.py: {'var' if ders_py.exists() else 'YOK (kol/ruflo main değil)'}")
    if kip == "uygula":
        if not (gecti and ders_py.exists()):
            print("uygulanmadı")
            return 1
        yedek = ev / ".claude" / "yedek" / f"ruflo1-{time.strftime('%Y%m%d-%H%M%S')}"
        yedek.mkdir(parents=True)
        n = 0
        for f in ajanlar(ev):
            shutil.copy2(f, yedek / f.name)
            n += onsoz.enjekte(f)
        print(f"uygulandı {n} ajan · yedek {yedek}")
    elif kip == "--geri":
        print(f"geri alındı {sum(onsoz.enjekte(f, geri=True) for f in ajanlar(ev))} ajan")
    else:
        for f in ajanlar(ev):
            print(f"{f.stem}\t{'eklenecek' if onsoz.enjekte(f, kuru=True) else 'aynı'}")
    ok = once == mcp_var_mi(ev)
    print("mcp önce=sonra" if ok else "HATA: MCP listesi değişti")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
