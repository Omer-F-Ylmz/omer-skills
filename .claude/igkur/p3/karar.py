"""P3 (sira 221–406) toplu karar → karar.tsv (d4 sütunları) + hesap.tsv. Kurallar: devir dolu → DEVİR; elle tablo (E) → kendi kararı; kalan bizde-var → KURULU."""
import csv, pathlib, sys
from collections import Counter

D = pathlib.Path(__file__).parent
SIRALI = pathlib.Path("C:/Projeler/omer-skills-wt/igkur/.claude/igkur/sirali.tsv")
UY, K, ICK = "UYARLA", "claudeai:kendi", "CC"
TOB = "trailofbits/skills"
REEL = "p3/skill/reel-plan"
HESAP = set()

# sira: (repo, lisans, karar, kanal, gerekce) — repo/lisans "" ise sirali'den alınır
E = {
    233: ("", "", "KURULU", "-", "çalışan ana araç (Claude Code)"),
    236: ("", "", "KURULU", "-", "skill:security-audit kurulu"),
    237: ("", "", "KURULU", "-", "plugin claude-video kurulu"),
    241: ("", "", "KURULU", "-", "npm codeburn kurulu"),
    245: ("", "", "KURULU", "-", "mcp n8n-mcp + skill kurulu"),
    247: ("", "", "KURULU", "-", "graphify skill + uv aracı kurulu"),
    248: ("", "", "KURULU", "-", "mcp playwright kurulu"),
    249: ("", "", "REF", "-", "araştırma karar modeli; iş akışımızda tüketicisi yok"),
    253: ("", "", "REF", "-", "genel ürün (Codex); codex eklentisi envanterde"),
    255: ("", "", "KURULU", "-", "obsidian-cli plugin açık"),
    257: ("vercel-labs/skills", "MIT", "REF", "-", "kurulum yolu; bizde onay betiği + marketplace (d4 ile aynı)"),
    259: ("", "", "REF", "-", "paket yöneticisi (npm) kurulu, aday değil"),
    261: ("", "", "REF", "-", "genel ürün (Cursor IDE)"),
    262: ("", "", "REF", "-", "protokol adı (MCP)"),
    263: ("ruvnet/flow-nexus", "yok", "REF", "-", "lisanssız, bulut hesabı ister, son push 2025-09; Ruflo eşi RUFLO-1'de"),
    264: ("anthropics/claude-plugins-official", "Apache-2.0", "KURULU", "-", "d4 onayında KUR (claude-code-setup); çift kurulmaz"),
    265: ("", "", "REF", "-", "genel terim (skills)"),
    266: ("", "", "REF", "-", "örnek MCP (Postgres); DB iş akışımız yok"),
    267: ("", "", "REF", "-", "genel ürün (Claude)"),
    282: ("coder/coder", "AGPL-3.0", "REF", "-", "self-host ajan çalışma alanı sunucusu; bizde worktree + arka.py"),
    286: ("vercel-labs/skills", "MIT", "REF", "-", "skill dizini; 257 ile aynı"),
    287: (TOB, "CC-BY-SA-4.0", "KUR", "CC+claudeai:ucuncu-taraf",
          "44 plugin'den yalnız differential-review KUR (SkillSpector SAFE, H+C 0); İNCELE: supply-chain-risk-auditor (H+C 6: SC4/PE3/E2/AR2), static-analysis (13: P6/TM1/TM2), insecure-defaults (2) — güvenlik aracı içeriği, elle bakılmadan kurulmaz"),
    288: ("", "", "REF", "-", "ücretli skill, repo yok; e-posta iş akışımız yok"),
    289: ("Jakeschincariol/replica-skill", "MIT", "KURULU", "-", "d4 onayında KUR; çift kurulmaz"),
    290: ("Jakeschincariol/replica-skill", "MIT", "KURULU", "-", "d4 onayında KUR; çift kurulmaz"),
    291: ("Jakeschincariol/replica-skill", "MIT", "KURULU", "-", "d4 onayında KUR; çift kurulmaz"),
    292: ("AgriciDaniel/claude-ads", "MIT", "KURULU", "-", "plugin claude-ads açık"),
    293: ("danyuchn/asd-ste100-skill", "MIT", UY, K,
          "kontrollü dil mekanizması (tek anlam, kısa cümle, etken çatı) → kapanış raporu yazım kuralına tek satır; raporlar Türkçe olduğundan skill kurulmaz"),
    294: ("", "", "REF", "-", "repo bulunamadı (gh search 0); seyahat rezervasyonu kapsam dışı"),
    295: ("Shubhamsaboo/awesome-llm-apps", "Apache-2.0", UY, K, "awesome liste → docs/kaynak/awesome kaynak satırı (awesome-rehber taraması)"),
    296: ("microsoft/SkillOpt", "MIT", UY, K,
          "iz-güdümlü skill metni düzenleme + doğrulama kapısı → tools/ogrenme/ders.py + skill-creator eval döngüsü; kendisi pip + LLM anahtarı ister"),
    297: ("VoltAgent/awesome-claude-code-subagents", "MIT", "REF", "-", "çift: bizde 150+ ajan (agency/ecc/departman)"),
    298: ("", "", "REF", "-", "genel terim (Claude Skills)"),
    299: ("", "", "REF", "-", "genel ürün (Devin)"),
    302: ("Maciek-roboblog/Claude-Code-Usage-Monitor", "MIT", "KURULU", "-", "d4 onayında KUR; çift kurulmaz"),
    303: ("HKUDS/CLI-Anything", "Apache-2.0", "KURULU", "-", "plugin cli-anything açık"),
    304: ("", "", "REF", "-", "paket yöneticisi (pip) kurulu"),
    305: ("alibaba/open-code-review", "Apache-2.0", "KURULU", "-",
          "npm -g @alibaba-group/open-code-review 1.12.13 kurulu; sağlayıcı anahtarı yapılandırması Ömer'de (hesap listesi)"),
    306: ("vercel-labs/skills", "MIT", "REF", "-", "257 ile aynı komut"),
    307: ("Fincept-Corporation/FinceptTerminal", "NOASSERTION", "REF", "-", "finans terminali, kapsam dışı; lisans belirsiz"),
    308: ("Javis603/token-monitor", "MIT", "REF", "-", "çift: codeburn (kurulu) + Claude-Code-Usage-Monitor (d4)"),
    309: ("coleam00/Archon", "MIT", "REF", "-", "d4 ile aynı: YAML iş akışı harness, bizde köprü/gsd"),
    310: ("morluto/rea", "MIT", "REF", "-", "d4 ile aynı: tersine mühendislik kapsam dışı, replica-skill karşılıyor"),
    311: ("", "", "REF", "-", "npx (Node ile kurulu)"),
    312: ("", "", "REF", "-", "genel ürün (Grok Build)"),
    313: ("", "", "KURULU", "-", "gh CLI + github MCP kurulu"),
    315: ("", "", "REF", "-", "ücretli avatar video servisi"),
    316: ("", "", "REF", "-", "ücretli görsel/video bağlayıcısı (hesap)"),
    319: ("", "", "REF", "-", "genel ürün (ChatGPT)"),
    320: ("", "", "REF", "-", "Kimi özelliği; slayt üretimi bizde pptx skill"),
    321: ("supabase/mcp", "Apache-2.0", "KURULU", "-", "plugin yerel-kurulum7/supabase"),
    322: ("", "", "REF", "-", "CRM servisi (hesap)"),
    323: ("The-Swarm-Corporation/AutoHedge", "MIT", "REF", "-", "otomatik alım-satım; kapsam dışı ve mali risk"),
    324: ("HKUDS/Vibe-Trading", "MIT", "REF", "-", "çok ajanlı alım-satım; kapsam dışı ve mali risk"),
    325: ("BloopAI/vibe-kanban", "Apache-2.0", "REF", "-", "bizde köprü/SIRA + worktree; ayrı UI sunucusu tarayıcı açar"),
    327: ("gitleaks/gitleaks", "MIT", "KURULU", "-", "gitleaks kurulu (tarama hattında)"),
    328: ("semgrep/semgrep", "LGPL-2.1", "KURULU", "-", "semgrep kurulu (tarama hattında)"),
    331: ("anthropics/claude-plugins-official", "Apache-2.0", "KURULU", "-", "resmi marketplace ekli"),
    332: ("", "", "REF", "-", "Vercel MCP örneği (hesap); deploy hattımız yok"),
    333: ("", "", "REF", "-", "veritabanı seçeneği; kullanmıyoruz"),
    334: ("", "", "REF", "-", "örnek prompt (Supabase)"),
    335: ("", "", UY, K,
          "işçi alt ajanlar + çıta örneğiyle reddeden katı denetçi döngüsü → departman-surec-plan kalite kapısı (p3/uyarla.md)"),
    337: ("", "", "REF", "-", "ücretli lead bağlayıcısı (hesap)"),
    338: ("", "", "REF", "-", "Email Voice örnek prompt (288)"),
    339: ("", "", "REF", "-", "Zapier/Beehive örnek prompt (hesap)"),
    340: ("Jakeschincariol/replica-skill", "MIT", "KURULU", "-", "d4 onayında KUR"),
    342: ("", "", UY, K, f"haftalık reel planı → {REEL} 'Plan' adımı"),
    343: ("", "", "REF", "-", "IG yorum/DM yanıtı; IG hesabı bağlantısı ister"),
    344: ("perplexityai/modelcontextprotocol", "MIT", "REF", "-", "çift: brave-search + agent-reach kurulu; Perplexity anahtarı ister"),
    347: ("ComposioHQ/composio", "MIT", "REF", "-", "tek bağlayıcı hesap ister; bizde ayrı MCP'ler + agent-reach"),
    357: ("morluto/rea", "MIT", "REF", "-", "REA örnek prompt (310)"),
    358: ("HKUDS/CLI-Anything", "Apache-2.0", "KURULU", "-", "CLI-Hub = cli-anything (kurulu)"),
    367: ("", "", "REF", "-", "paket yöneticisi (uv) kurulu"),
    368: ("shadcn-ui/ui", "MIT", "REF", "-", "proje başına npx shadcn; global kurulum gerekmez"),
    369: ("", "", "REF", "-", "ticari disassembler (Hopper)"),
    371: ("", "", "REF", "-", "marka adı, araç değil"),
    373: ("", "", "REF", "-", "görsel modelde karakter tutarlılığı prompt tekniği; görsel üretim aracımız yok"),
    387: ("", "", "REF", "-", "Claude uygulama modu (Cowork)"),
    388: ("", "", "REF", "-", "kişisel finans uygulaması, kapsam dışı"),
    389: ("", "", "REF", "-", "eğitim reklamı, araç değil"),
    393: ("", "", "REF", "-", "örnek prompt; graphify karşılıyor"),
    394: ("", "", "REF", "-", "örnek prompt; ses tarafı ElevenLabs (animasyon devri)"),
    397: ("", "", "KURULU", "-", "n8n-mcp kurulu"),
    398: ("", "", "REF", "-", "Cowork zamanlanmış görev örneği; bizde /schedule"),
    403: ("", "", "REF", "-", "kaynak platform; video-tarama kurulu"),
    405: ("", "", "KURULU", "-", "yerleşik komut (/compact)"),
    406: ("", "", "REF", "-", "claude.ai yerleşik bağlayıcı dizini"),
}
for s, b in {270: "Hook", 274: "Tutma denetimi", 275: "Tutma merdiveni", 281: "Hook madenciliği"}.items():
    E[s] = ("", "", UY, K, f"repo yok (ücretli set); reel-taste'te eksik → {REEL} '{b}' adımı")
for s in (269, 271, 272, 277, 278, 279, 280):
    E[s] = ("", "", "KURULU", "-", "reel-taste + motion-studio kurulu (konsept, cihaz rafı, kamera/geçiş, taste audit) karşılıyor")
for s in (390, 391, 392):
    E[s] = ("", "", UY, K, "skill yazım kuralı: önce skill'siz baseline, SKILL.md ≤500 satır → p3/uyarla.md (zip_denetle kontrolü)")
for s, ad in {326: "Kdenlive", 359: "OBS", 360: "GIMP", 361: "LibreOffice", 362: "Zoom", 363: "Krita", 364: "Inkscape",
              365: "FreeCAD", 366: "Zotero", 395: "Audacity", 396: "Godot"}.items():
    E[s] = ("", "", "REF", "-", f"CLI-Anything hub örneği ({ad}); gerekirse kurulu cli-anything ile")
for s in (374, 375, 376, 377, 378, 379, 380, 381):
    E[s] = ("", "", "REF", "-", "sunum aracı / veri kaynağı adı, kurulacak şey değil")
for s in (348, 349, 350, 351, 353, 354, 355, 356, 382, 383, 384, 385, 386, 400, 401, 402, 404):
    E[s] = ("", "", "REF", "-", "hesap isteyen servis/bağlayıcı ya da örneği; Ömer isterse claude.ai Connectors")
HESAP = {305: "LLM sağlayıcı anahtarı (ocr config provider; araç kurulu)", 296: "LLM anahtarı (yalnız kendisi kurulursa)",
         316: "Higgsfield hesabı", 337: "Clay hesabı", 344: "Perplexity API", 347: "Composio hesabı", 315: "HeyGen hesabı",
         322: "HubSpot", 332: "Vercel", 382: "Slack", 383: "Gmail", 384: "Apify", 386: "Make", 400: "Zapier"}


def main():
    rows = [x for x in csv.DictReader(open(SIRALI, encoding="utf-8"), delimiter="\t") if 221 <= int(x["sira"]) <= 406]
    out = ["sira\tad\trepo\tlisans\tkarar\tkanal\tgerekce"]
    for x in rows:
        s = int(x["sira"])
        if x["devir"] not in ("", "-"):
            r = (x["repo"], x["lisans"], "DEVİR", "-", f"devir/{x['devir']}-*.tsv; {x['devir']} departman ajanı")
        elif s in E:
            r = E[s]
        elif x["bizde"] not in ("", "-", "yok"):
            r = ("", "", "KURULU", "-", f"bizde: {x['bizde'][:60]}")
        else:
            sys.exit(f"karar yok: {s} {x['ad']}")
        out.append("\t".join([str(s), x["ad"], r[0] or x["repo"], r[1] or x["lisans"], *r[2:]]))
    assert len(out) == 187, len(out)
    (D / "karar.tsv").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    (D / "hesap.tsv").write_text("sira\tne\n" + "".join(f"{k}\t{v}\n" for k, v in sorted(HESAP.items())), encoding="utf-8", newline="\n")
    print(Counter(l.split("\t")[4] for l in out[1:]))


main()
