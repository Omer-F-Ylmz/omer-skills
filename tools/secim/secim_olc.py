"""SKILL-SECIM-1 ölçüm: 40 görevlik seçim seti (secim_gorevler.json) → doğru ilk seçim %, ilk seçime kadar tur, ilk istek girdi jetonu.
  python tools/secim/secim_olc.py cc <kol: once|sonra> [--tekrar 2] [--tavan 40] [--bas 1] [--usd 2.0]
    once  = canlı kurulum (senkron departman-* eski hali)
    sonra = senkron departman-* kapalı (yalnız bu süreçte, --settings), yerine .secim/eklenti plugin'i (dizinli departman-*)
  python tools/secim/secim_olc.py web <once|sonra>   → claude.ai vekili: skill'siz, ad listesi + Instructions istemde, 40 görev tek çağrıda
Çıktı: docs/kutuphane/olcum/<tarih>-secim-<taraf>-<kol>.tsv (satır satır). Canlı ayar değişmez; çağrı başı --max-budget-usd 1.0.
Doğru ilk seçim: departman-* dışındaki İLK Skill çağrısının kısa adı beklenen listede (departman → doğru skill = doğru yönlendirme)."""
import json
import os
import re
import shutil
import sys
import time
from itertools import zip_longest
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
KOK = DIZIN.parents[1]
sys.path.insert(0, str(KOK / "tools" / "olcum"))
from kosucu import kos  # noqa: E402

GOREV = json.loads((DIZIN / "secim_gorevler.json").read_text(encoding="utf-8"))
_dep = {}
for _g in GOREV:
    _dep.setdefault(_g["dep"], []).append(_g)
KARISIK = [g for k in zip_longest(*_dep.values()) for g in k if g]  # tavan/usd ile kesilen önek her departmandan örneklesin
CIKTI = KOK / "docs" / "kutuphane" / "olcum"
CALISMA = KOK / ".secim"  # gitignore dışı geçici: plugin + settings kopyası


def kisa(a):
    return a.split(":")[-1]


GENEL = ("", "general-purpose", "Explore", "Plan", "claude")  # uzman seçimi sayılmaz


def ilk_secim(araclar):
    """(ilk departman-dışı skill ya da uzman alt ajan kısa adı, o çağrıya kadar araç sayısı)"""
    for i, a in enumerate(araclar):
        if (a.startswith("Skill:") and not kisa(a).startswith("departman-")) or (a.startswith("Agent:") and kisa(a) not in GENEL):
            return kisa(a), i + 1
    return "", len(araclar)


def sonra_ek():
    """Dizinli departman-*'ı plugin olarak verir, senkron eski kopyaları bu süreçte kapatır (canlı overrides kopyası + 12 'off')."""
    ek = CALISMA / f"eklenti-{os.getpid()}"  # paralel sonra süreçleri birbirinin plugin klasörünü silmesin
    shutil.rmtree(ek, ignore_errors=True)
    (ek / ".claude-plugin").mkdir(parents=True)
    (ek / ".claude-plugin" / "plugin.json").write_text('{"name": "secim", "version": "0.0.1"}', encoding="utf-8")
    for d in (KOK / "skills").glob("departman-*"):
        shutil.copytree(d, ek / "skills" / d.name)
    ov = json.loads((Path.home() / ".claude/settings.json").read_text(encoding="utf-8")).get("skillOverrides", {})
    ov.update({f"anthropic-skills:{d.name}": "off" for d in (KOK / "skills").glob("departman-*")})
    s = CALISMA / f"settings-sonra-{os.getpid()}.json"
    s.write_text(json.dumps({"skillOverrides": ov}, ensure_ascii=False), encoding="utf-8")
    return ["--plugin-dir", str(ek), "--settings", str(s), "--max-turns", "4"]


def cc(kol, tekrar, tavan, bas=1, usd=2.0):
    """usd: bu sürecin ölçüm tavanı (plan limiti; 4 paralel süreç × 2.0 + web ≤ $10) — aşılınca durur."""
    ek = sonra_ek() if kol == "sonra" else ["--max-turns", "4"]
    yol = CIKTI / f"{time.strftime('%Y-%m-%d')}-secim-cc-{kol}.tsv"
    if not yol.exists():
        yol.write_text("gorev\ttekrar\tdogru\tsecilen\ttur\tgirdi\tusd\taraclar\n", encoding="utf-8")
    harcanan = 0.0
    for t in range(bas - 1, bas - 1 + tekrar):
        for g in KARISIK[:tavan]:
            if harcanan >= usd:
                return yol
            o = kos(g["istem"], ek=ek, cwd=str(KOK), butce=1.0)  # soğuk önbellek ilk çağrısı ~$0.73
            s, tur = ilk_secim(o["araclar"])
            harcanan += o.get("usd", 0)
            u = o.get("usage_ilk") or {}
            girdi = sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
            with yol.open("a", encoding="utf-8") as f:
                f.write(f"{g['id']}\t{t + 1}\t{int(s in g['beklenen'])}\t{s}\t{tur}\t{girdi}\t{o.get('usd', 0):.4f}\t{','.join(o['araclar'])[:300]}\n")
    return yol


SAYAC = CALISMA / "d4-usd.txt"  # d4 kümülatif tavan sayacı (tüm toplu çağrılar)
TOPLU_ISTEM = ("Aşağıdaki görevlerin HİÇBİRİNİ YAPMA. Her biri için bu oturumda ilk çağıracağın, işe EN ÖZGÜ skill ya da alt ajanın adını seç. "
               "departman-* yönlendirici skill'leri ve genel ajanlar (general-purpose, Explore, Plan) cevap sayılmaz ama departman skill'ini ve "
               "gösterdiği dosyaları Skill/Read/Grep ile açıp bakabilirsin. Agent çağırma. Son yanıtın yalnız satır satır `Sxx: ad`.\n\n")


def toplu(kol, tekrar=1, tavan=10.0, cagri=3.0, gorev=GOREV, set_ad="toplu"):
    """d4 düzeneği: görevler tek çağrıda, sıralı tek süreç, boş cwd (taban wt'deki dizin.md'leri göremez).
    Sayaç + bir çağrının üst sınırı tavanı aşacaksa çağrı yapılmaz."""
    ek = (sonra_ek()[:-2] if kol == "sonra" else []) + ["--max-turns", "40", "--disallowedTools", "Bash,Write,Edit,NotebookEdit,WebFetch,WebSearch"]
    yol = CIKTI / f"{time.strftime('%Y-%m-%d')}-secim-{set_ad}-{kol}.tsv"
    if not yol.exists():
        yol.write_text("gorev\ttekrar\tdogru\tsecilen\n", encoding="utf-8")
    t0 = yol.read_text(encoding="utf-8").count("#OZET")  # tekrar no dosyadaki önceki koşulardan devam eder
    for t in range(t0, t0 + tekrar):
        harcanan = float(SAYAC.read_text()) if SAYAC.exists() else 0.0
        if harcanan + cagri > tavan:
            print(f"DUR tavan: {harcanan:.2f}+{cagri} > {tavan}")
            return yol
        o = kos(TOPLU_ISTEM + "\n".join(f"{g['id']}: {g['istem']}" for g in gorev), ek=ek, butce=cagri, timeout=1500)
        SAYAC.write_text(f"{harcanan + o['usd']:.4f}")
        cevap = dict(re.findall(r"(S\d\d)\s*:\s*`?([A-Za-z0-9:_-]+)", o.get("metin") or ""))
        u0, u = o.get("usage_ilk") or {}, o["usage"]
        jet = lambda x: sum(x.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))  # noqa: E731
        with yol.open("a", encoding="utf-8") as f:
            for g in gorev:
                s = kisa(cevap.get(g["id"], ""))
                f.write(f"{g['id']}\t{t + 1}\t{int(s in g['beklenen'])}\t{s}\n")
            f.write(f"#OZET\t{t + 1}\t{sum(kisa(cevap.get(g['id'], '')) in g['beklenen'] for g in gorev)}/{len(gorev)}\t"
                    f"ilk_girdi={jet(u0)} son_girdi={jet(u)} cikti={u.get('output_tokens', 0)} tur={o['tur']} usd={o['usd']:.4f} rc={o['rc']} "
                    f"araclar={','.join(o['araclar'])[:400]}\n")
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
    # d4: boş cwd; taban claude.ai gibi dosya arayamaz (Grep/Read kapalı), sonra yalnız dizin-web.md'leri okuyabilir
    kapali = "Bash,Write,Edit,NotebookEdit,WebFetch,WebSearch,Agent" + ("" if kol == "sonra" else ",Glob,Grep,Read")
    ek = ["--strict-mcp-config", "--disable-slash-commands", "--max-turns", "15", "--disallowedTools", kapali] + (["--add-dir", str(KOK / "skills")] if kol == "sonra" else [])
    harcanan = float(SAYAC.read_text()) if SAYAC.exists() else 0.0
    if harcanan + 0.5 > 10.0:
        print(f"DUR tavan: {harcanan:.2f}+0.5 > 10")
        return None
    o = kos(istem, ek=ek, butce=0.5)
    SAYAC.write_text(f"{harcanan + o['usd']:.4f}")
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
    bas = int(a[a.index("--bas") + 1]) if "--bas" in a else 1
    usd = float(a[a.index("--usd") + 1]) if "--usd" in a else 2.0
    if a[0] == "toplu":
        z = "--set" in a  # --set zor → secim_gorevler_zor.json (opak adlı uzmanlar; taban/dizin ayrışsın)
        gorev = json.loads((DIZIN / "secim_gorevler_zor.json").read_text(encoding="utf-8")) if z else GOREV
        for kol in a[1].split(","):
            print(toplu(kol, tekrar if "--tekrar" in a else 1, cagri=float(a[a.index("--cagri") + 1]) if "--cagri" in a else 3.0,
                        gorev=gorev, set_ad="toplu-zor" if z else "toplu"))
    elif a[0] == "web":
        for kol in a[1].split(","):
            print(web(kol))
    else:
        print(cc(a[1], tekrar, tavan, bas, usd) if a[0] == "cc" else web(a[1]))
