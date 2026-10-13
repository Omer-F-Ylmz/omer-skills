"""SKILL-SECIM-1 onay betiği — Desktop/Ömer koşar. departman-* dizinleri (skill + ajan) İKİ TARAFA da zip yüklemesiyle gider:
CC'deki departman-* yalnız claude.ai senkron kopyasıdır (~/.claude/skills/synced/*/departman-*), gevşek kopya kurmak listeyi
ikiler (bütçe artar). Bu yüzden betik ~/.claude'a YAZMAZ; yüklemenin CC'ye ulaştığını doğrular.

  python onay/skill_secim_1_uygula.py --kuru   # (varsayılan) 12 departman: senkron kopyada dizin.md/dizin-web.md/ajanlar repo ile aynı mı
  python onay/skill_secim_1_uygula.py uygula   # aynı denetim; eksik varsa rc=1 (önce dist/skill-secim-1/kendi/*.zip "Upload and replace")
  python onay/skill_secim_1_uygula.py --geri   # yazılan bir şey yok; eski zip'ler yeniden yüklenerek geri alınır
Ayar (settings.json/skillOverrides) değişmez; hiçbir skill kapatılmaz; MCP listesi önce=sonra değilse rc=1.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kalite_3_uygula import EV, KOK, mcp_var_mi  # noqa: E402


def denetle(ev=EV, kok=KOK):
    """departman adı → eksik/farklı dosya listesi (boş = senkron kopya güncel)."""
    out = {}
    for d in sorted((kok / "skills").glob("departman-*")):
        kopya = next(iter(sorted(ev.glob(f".claude/skills/synced/*/{d.name}"))), None)
        dosyalar = [f for f in d.rglob("*") if f.is_file() and (f.parent.name != "ajanlar" or (ev / ".claude/agents" / f.name).exists())]
        out[d.name] = ["(senkron kopya yok)"] if kopya is None else [
            f.relative_to(d).as_posix() for f in dosyalar
            if not (kopya / f.relative_to(d)).is_file() or (kopya / f.relative_to(d)).read_bytes() != f.read_bytes()]
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    kip = (sys.argv[1:] or ["--kuru"])[0]
    if kip == "--geri":
        sys.exit(print("Yazılan bir şey yok; geri almak için önceki departman-* zip'lerini claude.ai'ye yeniden yükle.") or 0)
    once = mcp_var_mi()
    sonuc = denetle()
    for ad, eksik in sonuc.items():
        print(f"{ad}: {'GÜNCEL' if not eksik else 'BEKLİYOR ' + ', '.join(eksik[:3]) + (f' (+{len(eksik) - 3})' if len(eksik) > 3 else '')}")
    mcp_ok = mcp_var_mi() == once
    print(f"MCP önce=sonra: {mcp_ok}; güncel {sum(not e for e in sonuc.values())}/{len(sonuc)}")
    sys.exit(0 if kip == "--kuru" and mcp_ok else int(not mcp_ok or any(sonuc.values())))
