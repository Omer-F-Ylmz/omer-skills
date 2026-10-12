"""SKILL-BUTCE-1 profili: canlı skillOverrides üzerine iki değişiklik, bütçe (75000) aynı kalır.
  (b) tekilleştirme: ~/.claude/skills'te aynı adla duran skill'in claude.ai senkron kopyası (anthropic-skills:X) → off.
      Kalan kopya yerel olan: repo onay betikleriyle güncellenir; senkron kopya CC'de yereli gölgeliyordu (synced-skill-golgesi).
  (öncelik) açıklamalı ('on') küme = KORU (profil_uret) ∪ skillUsage'da olan; diğer 'on' skill'ler → name-only.
      Bütçe taşınca CC açıklamayı en az kullanılandan düşürüyor; 'on' küme bütçeye sığınca hiç kullanılmamış KORU (jev) de açıklamalı kalır.
Hiçbir skill silinmez; name-only skill Skill aracıyla ve departman-* yönlendiricisiyle çağrılabilir kalır. Canlı yalnız OKUNUR.
  python tools/butce/profil.py <context.md> <çıktı.json> [kapatmasiz] [butce=N]
  kapatmasiz (butce1b): (b) yok, hiçbir skill off olmaz; butce=N: SLASH_COMMAND_TOOL_CHAR_BUDGET env'i profile yazılır."""
import collections, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "olcum"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from envanter import context_tablosu  # noqa: E402
from profil_uret import koru  # noqa: E402

EV = Path.home()


def cc_koru(ad):
    """KORU, -desktop varyantları hariç: onlar Desktop içindir, CC'de aynı işi yapan asıl skill açıklamalı."""
    return koru(ad) and not ad.endswith("-desktop")


def uret(tablo, mevcut, kullanim, kapat=True):
    yerel = {ad for ad, (kaynak, _) in tablo.items() if kaynak == "User"}
    yeni = {}
    for ad in tablo:
        kok = ad.removeprefix("anthropic-skills:")
        if kapat and ad.startswith("anthropic-skills:") and kok in yerel:
            yeni[ad] = "off"
        elif mevcut.get(ad, "on") == "on" and not (cc_koru(ad) or ad in kullanim):
            yeni[ad] = "name-only"
        elif mevcut.get(ad) == "name-only" and cc_koru(ad):
            yeni[ad] = "on"
    return yeni


def main(ctx, cikti, *secenek):
    ayar = json.loads((EV / ".claude/settings.json").read_text(encoding="utf-8"))
    mevcut = ayar.get("skillOverrides", {})
    kullanim = json.loads((EV / ".claude.json").read_text(encoding="utf-8")).get("skillUsage", {})
    tablo = context_tablosu(ctx)
    yeni = uret(tablo, mevcut, kullanim, "kapatmasiz" not in secenek)
    print("değişen", len(yeni), dict(collections.Counter(f"{mevcut.get(a, 'on')}→{v}" for a, v in yeni.items())))
    son = {**mevcut, **yeni}
    print("listede on (açıklamalı aday):", sum(1 for a in tablo if son.get(a, "on") == "on"))
    profil = {"skillOverrides": son}
    for s in secenek:
        if s.startswith("butce="):
            profil["env"] = {"SLASH_COMMAND_TOOL_CHAR_BUDGET": s[6:]}
    Path(cikti).write_text(json.dumps(profil, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(*sys.argv[1:])
