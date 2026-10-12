"""SKILL-SECIM-1 ölçüm: 40 görevlik seçim seti (secim_gorevler.json) → doğru ilk seçim %, ilk seçime kadar tur, ilk istek girdi jetonu.
  python tools/secim/secim_olc.py cc <kol: once|sonra> [--tekrar 2] [--tavan 40]
    once  = canlı kurulum (senkron departman-* eski hali)
    sonra = senkron departman-* kapalı (yalnız bu süreçte, --settings), yerine .secim/eklenti plugin'i (dizinli departman-*)
  python tools/secim/secim_olc.py web <once|sonra>   → claude.ai vekili: skill'siz, ad listesi + Instructions istemde, 40 görev tek çağrıda
Çıktı: docs/kutuphane/olcum/<tarih>-secim-<taraf>-<kol>.tsv (satır satır). Canlı ayar değişmez; çağrı başı --max-budget-usd 0.6.
Doğru ilk seçim: departman-* dışındaki İLK Skill çağrısının kısa adı beklenen listede (departman → doğru skill = doğru yönlendirme)."""
import json
import re
import shutil
import sys
import time
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
KOK = DIZIN.parents[1]
sys.path.insert(0, str(KOK / "tools" / "olcum"))
from kosucu import kos  # noqa: E402

GOREV = json.loads((DIZIN / "secim_gorevler.json").read_text(encoding="utf-8"))
CIKTI = KOK / "docs" / "kutuphane" / "olcum"
CALISMA = KOK / ".secim"  # gitignore dışı geçici: plugin + settings kopyası


def kisa(a):
    return a.split(":")[-1]


def ilk_secim(araclar):
    """(ilk departman-dışı skill kısa adı, o çağrıya kadar araç sayısı)"""
    for i, a in enumerate(araclar):
        if a.startswith("Skill:") and not kisa(a).startswith("departman-"):
            return kisa(a), i + 1
    return "", len(araclar)


def sonra_ek():
    """Dizinli departman-*'ı plugin olarak verir, senkron eski kopyaları bu süreçte kapatır (canlı overrides kopyası + 12 'off')."""
    ek = CALISMA / "eklenti"
    shutil.rmtree(ek, ignore_errors=True)
    (ek / ".claude-plugin").mkdir(parents=True)
    (ek / ".claude-plugin" / "plugin.json").write_text('{"name": "secim", "version": "0.0.1"}', encoding="utf-8")
    for d in (KOK / "skills").glob("departman-*"):
        shutil.copytree(d, ek / "skills" / d.name)
    ov = json.loads((Path.home() / ".claude/settings.json").read_text(encoding="utf-8")).get("skillOverrides", {})
    ov.update({f"anthropic-skills:{d.name}": "off" for d in (KOK / "skills").glob("departman-*")})
    s = CALISMA / "settings-sonra.json"
    s.write_text(json.dumps({"skillOverrides": ov}, ensure_ascii=False), encoding="utf-8")
    return ["--plugin-dir", str(ek), "--settings", str(s), "--max-turns", "6"]


def cc(kol, tekrar, tavan):
    ek = sonra_ek() if kol == "sonra" else ["--max-turns", "6"]
    yol = CIKTI / f"{time.strftime('%Y-%m-%d')}-secim-cc-{kol}.tsv"
    if not yol.exists():
        yol.write_text("gorev\ttekrar\tdogru\tsecilen\ttur\tgirdi\tusd\taraclar\n", encoding="utf-8")
    for t in range(tekrar):
        for g in GOREV[:tavan]:
            o = kos(g["istem"], ek=ek, cwd=str(KOK), butce=0.6)
            s, tur = ilk_secim(o["araclar"])
            u = o.get("usage_ilk") or {}
            girdi = sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
            with yol.open("a", encoding="utf-8") as f:
                f.write(f"{g['id']}\t{t + 1}\t{int(s in g['beklenen'])}\t{s}\t{tur}\t{girdi}\t{o.get('usd', 0):.4f}\t{','.join(o['araclar'])[:300]}\n")
    return yol


def web(kol):
    """claude.ai vekili: init'teki anthropic-skills adları + Instructions; sonra kolunda departman dizin-web.md'leri Grep'lenebilir."""
    init = json.loads(sorted(CIKTI.glob("*butce1b-init.json"))[-1].read_text(encoding="utf-8"))
    adlar = [kisa(s) for s in init["skills"] if s.startswith("anthropic-skills:")]
    ins = (KOK / "dist" / "skill-secim-1" / ("claude-ai-instructions.md" if kol == "sonra" else "claude-ai-instructions-once.md")).read_text(encoding="utf-8")
    gorevler = [g for g in GOREV if g.get("web", True)]
    dizin = (f"\nDepartman dizinleri (Grep ile ara): {KOK / 'skills'}/departman-*/dizin-web.md" if kol == "sonra" else "")
    istem = (f"Sen claude.ai'desin. Profil talimatın:\n{ins}\n\nYüklü skill'ler (yalnız ad):\n{' '.join(adlar)}{dizin}\n\n"
             "Her görev için kullanacağın TEK skill adını yaz; biçim: `Sxx: ad` satır satır, başka metin yok.\n\n"
             + "\n".join(f"{g['id']}: {g['istem']}" for g in gorevler))
    ek = ["--strict-mcp-config", "--disable-slash-commands", "--max-turns", "15"] + (["--add-dir", str(KOK / "skills")] if kol == "sonra" else [])
    o = kos(istem, ek=ek, cwd=str(KOK), butce=1.5)
    cevap = dict(re.findall(r"(S\d\d)\s*:\s*`?([A-Za-z0-9:_-]+)", o.get("metin") or ""))
    yol = CIKTI / f"{time.strftime('%Y-%m-%d')}-secim-web-{kol}.tsv"
    with yol.open("a", encoding="utf-8") as f:
        for g in gorevler:
            s = kisa(cevap.get(g["id"], ""))
            f.write(f"{g['id']}\t{int(s in g['beklenen'])}\t{s}\n")
    return yol


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    tekrar = int(a[a.index("--tekrar") + 1]) if "--tekrar" in a else 2
    tavan = int(a[a.index("--tavan") + 1]) if "--tavan" in a else 40
    print(cc(a[1], tekrar, tavan) if a[0] == "cc" else web(a[1]))
