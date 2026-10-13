"""SKILL-SECIM-1 (a): katmanlı tembel dizin — üst katman oturum listesi/Instructions'taki departman-* satırları; alt katman
yalnız açılan departmanın SKILL.md sonuna gömülü "## Dizin" (d5: ayrı dosya okuma turu yok). Satır `ad: ≤8 kelime`, yalnız
adı işini söylemeyen (opak), anahtar.json'da notu olan ya da oturum listesinde görünmeyen skill'ler; listeleme bütçesi değişmez.
Yeni skill eklendikçe yeniden koş.
  python tools/secim/dizin_uret.py <init.json>
    → skills/departman-*/SKILL.md dizin bölümü: "claude.ai + Claude Code" (init'teki anthropic-skills: + KALİTE-3 ajanları) ve "yalnız Claude Code"
    → dist/skill-secim-1/kendi/departman-*.zip (claude.ai'ye yüklenir, CC senkron kopyadan görür)"""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools" / "butce"))
from envanter import on_bilgi  # noqa: E402


# ponytail: anahtar kelime puanı (ad ×3 + açıklama); yanlış dağılım görülürse kelime ekle, sınıflayıcı model gerekmez
ALAN = {
    "frontend": "ui ux css html react vue svelte angular nextjs tailwind frontend component landing animation anim motion gsap three threejs "
                "webgl blender 3d figma font typography color palette layout responsive icon canvas design designer shadcn web page site "
                "image gorsel tasarim arayuz svg logo brand",
    "backend-dotnet": "dotnet net csharp asp aspnet blazor efcore entity nuget msbuild xunit maui wpf winforms razor backend server "
                      "api rest grpc azure microservice java spring go golang rust python django fastapi node express",
    "guvenlik": "security secure vulnerability vuln owasp pentest pentesting secret secrets crypto cve exploit threat sast dast fuzz "
                "malware penetration zero trust kvkk gdpr compliance auth oauth jwt xss csrf injection guvenlik sifre",
    "test-qa": "test tests testing qa e2e playwright tdd coverage regression bug debug debugging flaky jest pytest cypress selenium hata",
    "veri-db": "sql database db postgres postgresql mysql sqlite mongo redis data dataset csv excel xlsx spreadsheet pandas analytics "
               "etl schema query bigquery supabase veri tablo",
    "belge": "doc docs docx pdf pptx powerpoint presentation slide slides report write writing writer copy copywriting blog content "
             "marketing seo email readme article resume cv invoice proposal ads ad social linkedin twitter instagram newsletter "
             "translate translation belge rapor yazi metin teklif fatura",
    "arastirma-ogrenme": "research search learn learning paper arxiv scrape scraper crawl crawler summarize summary youtube video "
                         "transcript tutorial explain wiki knowledge study course reddit news arastirma ogren",
    "surec-plan": "plan plans planning plannerbrainstorm brainstorming spec specs prd requirement requirements roadmap architecture "
                  "idea ideation estimate breakdown strategy milestone backlog sprint plani fikir",
    "surec-inceleme": "review reviewer refactor refactoring quality lint linter smell simplify simplification audit critique "
                      "clean inceleme denetim kalite",
    "surec-git-yayin": "git commit branch merge pr pull release deploy deployment ci cd github gitlab changelog version publish "
                       "docker kubernetes k8s vercel netlify cloudflare worktree pipeline yayin",
    "surec-ajan-arac": "agent agents skill skills mcp plugin hook hooks claude prompt prompting llm subagent automation automate "
                       "workflow n8n tool tools cli orchestration ajan arac otomasyon",
    "verimlilik": "token tokens context compress compression cache memory session fast speed cost budget productivity notes "
                  "obsidian todo efficient headroom rtk graph verimlilik",
}
KELIME = {d: set(k.split()) for d, k in ALAN.items()}
YEDEK = "arastirma-ogrenme"
# klasör = departman (ALAN dışıysa puanla); yalnız canlıya kurulmuş (kabul edilmiş) olanlar
KALITE3 = {md.stem: md for md in (KOK / "ajanlar" / "kalite3").glob("*/*.md") if (Path.home() / ".claude/agents" / md.name).exists()}


def kelimeler(s):
    return [w for w in re.split(r"[^a-z0-9çğıöşü]+", s.lower()) if w]


def departman(ad, acik):
    """En yüksek puanlı departman; puan 0 → YEDEK. Önek eşleşmesi ≥5 harfli anahtar için (testing ⊃ test)."""
    def puan(ws, d):
        k = KELIME[d]
        return sum(1 for w in ws if w in k or any(len(x) >= 5 and w.startswith(x) for x in k))
    a, b = kelimeler(ad.split(":")[-1]), kelimeler(acik)
    p = {d: 3 * puan(a, d) + puan(b, d) for d in ALAN}
    en = max(p, key=p.get)
    return en if p[en] else YEDEK


def ne_zaman(acik, n=80):
    """'Use when …' / 'Kullan: …' varsa onu, yoksa ilk cümleyi ≤n karaktere kısaltır."""
    acik = " ".join(acik.split())
    m = re.search(r"(?:use (?:this )?(?:skill )?when|use for|when the user|kullan(?:ım)?:?)\s*(.*)", acik, re.I)
    s = (m.group(1) if m and len(m.group(1)) > 15 else acik).split(". ")[0]
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


ANAHTAR = {k: v for k, v in json.loads((Path(__file__).with_name("anahtar.json")).read_text(encoding="utf-8")).items() if k != "_not"}
BAS, SON = "<!-- dizin:bas -->", "<!-- dizin:son -->"
GOVDE = ("## Dizin\nAdımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki "
         "`ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.")


def opak(ad, acik=""):
    """Adının hiçbir kelimesi departman anahtarlarına uymuyor (d3 ad-onerileri ölçütü) ve ≥4 harfli hiçbir kelimesi kendi
    açıklamasında geçmiyor → yalnız adla seçilemez. ponytail: kelime eşleşmesi; ürün adı (defuddle) açık sayılır, d4 tabanı bunları zaten buldu."""
    ws = kelimeler(ad.split(":")[-1])
    aw = set(kelimeler(acik))
    return not any(w in k or any(len(x) >= 5 and w.startswith(x) for x in k) for w in ws for k in KELIME.values())         and not any(len(w) >= 4 and w in aw for w in ws)


def satir(ad, acik):
    """ad: ≤8 kelime ne zaman (anahtar.json görev ifadesi/kaçın notu önce)."""
    k = ad.split(":")[-1]
    nz = "" if not (opak(ad, acik) or k in ANAHTAR) else ANAHTAR.get(k) or " ".join(ne_zaman(acik, 400).rstrip("…").split()[:8]).rstrip(".,;:")
    k = "ajan:" + k if ad.startswith("ajan:") else k
    return f"{k}: {nz}" if nz else k


def bolum(web, cc):
    """web/cc: [(ad, açıklama)] → SKILL.md sonuna gömülü dizin (sıralı, tarihsiz: önbellek dostu sabit metin)."""
    s = [BAS, GOVDE]
    if web:
        s += ["### claude.ai + Claude Code", *sorted(satir(a, x) for a, x in web)]
    if cc:
        s += ["### yalnız Claude Code", *sorted(satir(a, x) for a, x in cc)]
    return "\n".join(s + [SON])


def sec(kayit):
    """Dizine girenler: opak ad ya da anahtar.json'daki ad (oturum dışı üyeler SKILL.md 'Profil dışı' bölümünde adla var).
    Ajanlar yalnız web bölümünde (CC'de Agent aracı açıklamalı listeler)."""
    return [(a, x) for a, x in kayit if opak(a, x) or a.split(":")[-1] in ANAHTAR]


def tekille(skiller, oturum=()):
    """Aynı kısa ad birden çok plugin'den gelir (example-skills:pdf, claude-api:pdf …): kısa ad başına tek kayıt —
    oturum listesinde (init) olan, sonra öneksiz, sonra en kısa ad."""
    grup = {}
    for ad in skiller:
        grup.setdefault(ad.split(":")[-1], []).append(ad)
    secilen = (min(g, key=lambda a: (a not in oturum, ":" in a, len(a), a)) for g in grup.values())
    return {a: skiller[a] for a in secilen}


def dagit(skiller):
    """{ad: açıklama} → {departman: [(ad, ne_zaman)]}; departman-* kendileri dizine girmez."""
    out = {d: [] for d in ALAN}
    for ad, acik in skiller.items():
        if ad.split(":")[-1].startswith("departman-"):
            continue
        md = KALITE3.get(ad.split(":")[-1]) if ad.startswith("ajan:") else None
        dep = md.parent.name if md else ""
        out[dep if dep in ALAN else departman(ad, acik)].append((ad, acik))
    return out


def cc_skiller():
    from envanter import disk_haritasi
    out, gorulen = {}, set()
    for ad, (_, md) in disk_haritasi().items():  # plugin skill'i iki anahtarla gelir (ad + klasör): yol başına ilki
        if md not in gorulen:
            gorulen.add(md)
            out[ad] = on_bilgi(md)[1]
    for md in sorted(Path.home().glob(".claude/skills/synced/*/*/SKILL.md")):  # claude.ai senkron kopyaları haritada yok
        out.setdefault("anthropic-skills:" + md.parent.name, on_bilgi(md)[1])
    return out


def cc_ajanlar(oturum_ajan):
    """init'teki alt ajanlar (CC'de yüklü) → {'ajan:<ad>': açıklama}; açıklama ~/.claude/agents + plugin agents/ diskinden (kısa adla)."""
    acik = {}
    for md in [*Path.home().glob(".claude/agents/*.md"), *Path.home().glob(".claude/plugins/cache/**/agents/**/*.md")]:
        ad, a = on_bilgi(md)
        if ad:
            acik.setdefault(ad.split(":")[-1], a)
    return {f"ajan:{ad}": acik.get(ad.split(":")[-1], "") for ad in oturum_ajan}


def claude_ai_ajanlar():
    """claude.ai'de alt ajan yok: KALİTE-3 ajanları zip içinde ajanlar/<ad>.md olarak gider, talimat elle uygulanır."""
    return {f"ajan:{a}": on_bilgi(md)[1] for a, md in KALITE3.items()}


def claude_ai_skiller(cc, oturum):
    """claude.ai'de yüklü olanlar = init'teki anthropic-skills: senkron kopyaları; açıklama yerel diskteki aynı addan."""
    yerel = {k.split(":")[-1]: v for k, v in cc.items()}
    adlar = [s.split(":", 1)[1] for s in oturum if s.startswith("anthropic-skills:")]
    return {a: yerel.get(a, "") for a in adlar}


def yaz(kok, web, cc):
    """web/cc: {departman: [(ad, açıklama)]} (seçilmiş) → SKILL.md sonundaki dizin bölümü; d4'ün ayrı dizin dosyaları silinir (okuma turu yok)."""
    for dep in ALAN:
        d = kok / "skills" / f"departman-{dep}"
        for ad, _ in web.get(dep, []):  # KALİTE-3 ajan tanımı skill klasörüne (claude.ai zip'i + CC senkron kopyası)
            if ad.startswith("ajan:") and ad[5:] in KALITE3:
                (d / "ajanlar").mkdir(exist_ok=True)
                (d / "ajanlar" / f"{ad[5:]}.md").write_bytes(KALITE3[ad[5:]].read_bytes())
        for eski in ("dizin.md", "dizin-web.md"):
            (d / eski).unlink(missing_ok=True)
        g = re.sub(r"\nSkill dizini:[^\n]*\n", "", (d / "SKILL.md").read_text(encoding="utf-8"))
        g = re.sub(rf"\n*{BAS}.*?{SON}\n?", "\n", g, flags=re.S).rstrip("\n")
        (d / "SKILL.md").write_bytes(f"{g}\n\n{bolum(web.get(dep), cc.get(dep))}\n".encode("utf-8"))


def zipla(kok):
    """claude.ai yüklemesi (CC de bu senkron kopyayı görür): dist/skill-secim-1/departman-<x>.zip, kök klasör = skill adı."""
    import zipfile
    cikti = kok / "dist" / "skill-secim-1" / "kendi"
    cikti.mkdir(parents=True, exist_ok=True)
    for d in sorted((kok / "skills").glob("departman-*")):
        with zipfile.ZipFile(cikti / f"{d.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(d.rglob("*")):
                if f.is_file() and (f.parent.name != "ajanlar" or f.stem in KALITE3):
                    z.write(f, f"{d.name}/{f.relative_to(d).as_posix()}")
    return cikti


if __name__ == "__main__":
    import json
    sys.stdout.reconfigure(encoding="utf-8")
    init = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    oturum = set(init["skills"])
    cc = cc_skiller()
    w = dagit({**claude_ai_skiller(cc, oturum), **claude_ai_ajanlar()})
    w = {d: [(a, x) for a, x in k if a.startswith("ajan:")] + sec([(a, x) for a, x in k if not a.startswith("ajan:")]) for d, k in w.items()}
    wad = {a.split(":")[-1] for k in w.values() for a, _ in k}
    c = {d: [(a, x) for a, x in sec(k) if a.split(":")[-1] not in wad] for d, k in dagit(tekille(cc, oturum)).items()}
    yaz(KOK, w, c)
    print(" ".join(f"{d}={len(w[d])}+{len(c[d])}" for d in ALAN))
    print(zipla(KOK))
