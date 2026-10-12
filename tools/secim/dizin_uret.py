"""SKILL-SECIM-1 (a): hiyerarşik yönlendirme — kurulu TÜM skill'leri 12 departmana dağıtıp her departman-* klasörüne
dizin.md (ad — ne zaman, ≤80 kr) yazar; SKILL.md'ye "dizinde Grep, adla çağır" satırı eklenir. Dizin oturuma yüklenmez
(Grep ile aranır), listeleme bütçesi değişmez. Yeni skill eklendikçe yeniden koş.
  python tools/secim/dizin_uret.py <init.json>
    → skills/departman-*/dizin.md (CC: canlı disk ~/.claude/skills + plugin'ler, kısa ad başına tek kayıt)
    → dist/skill-secim-1/claude-ai/departman-*/dizin.md (claude.ai: init'teki anthropic-skills: adları)"""
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools" / "butce"))

SATIR = ("Skill dizini: bu klasördeki `dizin.md` — alandaki TÜM kurulu skill'ler (ad — ne zaman). Adımdaki araç işe tam uymuyorsa "
         "dizin.md'de Grep ile işin anahtar kelimesini ara (Read etme), bulunan adı Skill aracıyla çağır; listede yalnız adı görünen skill de çağrılabilir.")

# ponytail: anahtar kelime puanı (ad ×3 + açıklama); yanlış dağılım görülürse kelime ekle, sınıflayıcı model gerekmez
ALAN = {
    "frontend": "ui ux css html react vue svelte angular nextjs tailwind frontend component landing animation anim motion gsap three threejs "
                "webgl blender 3d figma font typography color palette layout responsive icon canvas design designer shadcn web page site "
                "image gorsel tasarim arayuz svg logo brand",
    "backend-dotnet": "dotnet net csharp asp aspnet blazor efcore entity nuget msbuild xunit maui wpf winforms razor backend server "
                      "api rest grpc azure microservice java spring go golang rust python django fastapi node express",
    "guvenlik": "security secure vulnerability vuln owasp pentest pentesting secret secrets crypto cve exploit threat sast dast fuzz "
                "malware kvkk gdpr compliance auth oauth jwt xss csrf injection guvenlik sifre",
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


def dizin_md(dep, kayitlar):
    sat = [f"# departman-{dep} — skill dizini ({len(kayitlar)} skill; Grep ile ara, adı Skill aracıyla çağır)", ""]
    sat += [f"- {ad} — {nz}" if nz else f"- {ad}" for ad, nz in sorted(kayitlar)]
    return "\n".join(sat) + "\n"


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
        out[departman(ad, acik)].append((ad, ne_zaman(acik)))
    return out


def cc_skiller():
    from envanter import disk_haritasi, on_bilgi
    out, gorulen = {}, set()
    for ad, (_, md) in disk_haritasi().items():  # plugin skill'i iki anahtarla gelir (ad + klasör): yol başına ilki
        if md not in gorulen:
            gorulen.add(md)
            out[ad] = on_bilgi(md)[1]
    return out


def claude_ai_skiller(cc, oturum):
    """claude.ai'de yüklü olanlar = init'teki anthropic-skills: senkron kopyaları; açıklama yerel diskteki aynı addan."""
    yerel = {k.split(":")[-1]: v for k, v in cc.items()}
    adlar = [s.split(":", 1)[1] for s in oturum if s.startswith("anthropic-skills:")]
    return {a: yerel.get(a, "") for a in adlar}


def yaz(hedef_kok, dagilim, skill_md=True):
    for dep, kay in dagilim.items():
        d = hedef_kok / f"departman-{dep}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "dizin.md").write_bytes(dizin_md(dep, kay).encode("utf-8"))
        sk = d / "SKILL.md"
        if skill_md and sk.exists():
            g = sk.read_text(encoding="utf-8")
            if SATIR not in g:
                sk.write_bytes(g.replace("\n## Adımlar", f"\n{SATIR}\n\n## Adımlar", 1).encode("utf-8"))


if __name__ == "__main__":
    import json
    sys.stdout.reconfigure(encoding="utf-8")
    oturum = set(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["skills"])
    cc = cc_skiller()
    for hedef, sk, smd in ((KOK / "skills", tekille(cc, oturum), True),
                           (KOK / "dist" / "skill-secim-1" / "claude-ai", claude_ai_skiller(cc, oturum), False)):
        dg = dagit(sk)
        yaz(hedef, dg, smd)
        print(hedef.name, " ".join(f"{d}={len(k)}" for d, k in dg.items()), "toplam", sum(map(len, dg.values())))
