"""ARAC-AJAN-OZELLIK-1: docs/envanter/envanter.tsv + elle yazılmış çekirdek tablodan arac-ajan-ozellik.tsv üretir.
Kullanım: python tools/arac_ajan_envanter.py  (salt okuma + tek çıktı dosyası; ağ yok)"""
import csv, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
GIRDI = KOK / "docs/envanter/envanter.tsv"
CIKTI = KOK / "docs/envanter/arac-ajan-ozellik.tsv"
BASLIK = ["arac", "tur", "ozellik", "ne_yapar", "bizde_karsiligi", "akista_adim", "maliyet", "kurulu"]

# (anahtar regex, bizde karşılığı, akıştaki adım, RAM/token maliyeti) — ilk eşleşen kazanır
KURALLAR = [
    (r"swarm|hive|queen|consensus|raft", "ajan_sira + yonetici ajan", "adım 3: paralel alt iş (ORDU-1) — ajan_sira sırasına swarm görevleri eklenir", "yüksek RAM; tek tek aç, bitince pid kapat"),
    (r"a2a|cli-a2a|omni-agents", "ajan_sira + OmniRoute combos", "adım 3: ajanlar arası devir; model merdiveni ücretsiz→Haiku→Sonnet→Opus", "orta; yerel süreç"),
    (r"learn|pattern|intelligence|reasoningbank|continuous|instinct|autoharness|task-observer|self.improv", "2. beyin döngüsü + ruflo pattern-store", "başta pattern-search, sonda pattern-store (K2n/K6)", "düşük; ≤10 satır enjeksiyon"),
    (r"memory|mem-search|agentmemory|agentdb|second-brain|recall", "claude-mem + beyin + ruflo memory", "başta recall/mem2, sonda kaydet", "düşük"),
    (r"hook|guard|tdd-guard|gateguard|safety", "settings.json hooks + yarim_bekci/ram_bekci", "PreToolUse/Stop; kapı görevi", "düşük; her çağrıda ms"),
    (r"review|audit|verif|final-gate|quality|critic|judge|council|doubt", "DENETİM + phoenix final-gate", "kapanış öncesi bağımsız okuma (okuyucu ajan)", "orta; salt-okuma ajan"),
    (r"plan|spec|brainstorm|decompos|executing|autoplan|ceo|office-hours|interview|idea", "plan-kur + departman-surec-plan", "adım 1: planla; tablo satırı araç|adım", "düşük; konuşma turu"),
    (r"browser|playwright|chrome|rea\b|webcmd|computer-use|agent-browser", "playwright headless + REA + Claude in Chrome (K2q)", "kanıt: SS/ağ; varsayılan tarayıcı açılmaz", "yüksek RAM; headless, pid kapat"),
    (r"orchestr|workflow|dispatch|parallel|pipeline|loop|ralph|gsd|octo|conductor|herdr|loopy|maestro|devfleet|dmux", "ajan_sira + suite-kosucu/okuyucu", "adım 3: bölme ve paralel çalıştırma", "orta"),
    (r"router|combo|9router|omniroute|model-route|council-multi", "OmniRoute combos + yonlendir.py (K3)", "model merdiveni seçimi", "düşük"),
    (r"cost|token|headroom|compress|rtk|context-mode|code-mode|budget", "headroom + rtk + code-mode (cm.py)", "uzun çıktıyı süz; 2+ araç → cm.py", "tasarruf sağlar"),
    (r"security|strix|agentshield|semgrep|gitleaks|pentest", "departman-guvenlik + gitleaks/semgrep", "değişiklik sonrası tarama", "orta"),
]

# Elle yazılmış çekirdek: ad, tür, özellik, ne yapar, karşılık, adım, maliyet, kurulu
CEKIRDEK = [
    ("ruflo", "mcp", "swarm_init / hive-mind / agent_spawn", "çoklu ajan topolojisi, consensus, görev dağıtımı", "ajan_sira + yonetici ajan", "adım 3: bağımsız ≥2 iş; deneme _deneme/arac-ajan/ruflo/", "yüksek RAM; tek tek", "kurulu"),
    ("ruflo", "mcp", "hooks_intelligence_pattern-search/store, agentdb_*", "ReasoningBank desen belleği (HNSW)", "2. beyin döngüsü", "başta search, sonda store (zorunlu)", "düşük", "kurulu"),
    ("claude-mem", "plugin", "mem-search, work_state_write, knowledge-agent, timeline", "oturumlar arası gözlem belleği", "beyin + mem2.py", "oturum başı recall; iş durumu work_state", "düşük", "kurulu"),
    ("superpowers", "plugin", "subagent-driven-development, dispatching-parallel-agents, executing-plans, writing-plans", "plan→alt ajan→inceleme zinciri", "ORDU-1 + görev bölme", "adım 1 plan, adım 3 dağıt", "orta", "kurulu"),
    ("gstack", "plugin", "autoplan, pair-agent, review, qa, learn, router", "rol bazlı plan/inceleme/QA ajanları", "plan-kur + DENETİM", "plan: autoplan; kapanış: review/qa", "orta", "kurulu"),
    ("ecc", "plugin", "ajan/orkestrasyon paketleri (orch-*, council, santa-loop, team-*)", "çok ajanlı orkestrasyon kalıpları", "ajan_sira + kombinler", "karmaşık iş: orch-pipeline", "orta", "kurulu"),
    ("phoenix-*", "skill", "orchestrator, final-gate, verification-matrix", "bitiş kapısı ve doğrulama matrisi", "DENETİM + yarim_bekci", "kapanış: final-gate", "düşük", "kurulu"),
    ("headroom", "cli", "compress / retrieve / proxy", "çıktı sıkıştırma", "rtk + headroom hook", "büyük çıktı", "tasarruf", "kurulu"),
    ("code-mode (UTCP)", "cli", "cm.py run / search", "araç zincirini tek JS çağrısına indirir", "K2p", "2+ ardışık araç", "tasarruf", "kurulu"),
    ("graphify", "cli", "query / path / explain", "kod bilgi grafiği", "tara_hizli.py (RAM kuralı)", "kod keşfi", "RAM: tam update yasak", "kurulu"),
    ("CC kendi", "yerel", ".claude/agents, Agent/Task tipleri, hooks, output styles, plugin agents, workflows", "alt ajan tanımı, kanca, çıktı stili", "okuyucu, suite-kosucu, aday-arastirici, video-tarayici", "adım 3: Agent okuyucu/suite-kosucu", "orta", "kurulu"),
    ("OmniRoute", "cli", "combos / fallback", "çoklu model yönlendirme ve yedekleme", "ucretsiz_motor.py + K2h", "ücretsiz havuz önce", "$0 hedef", "kurulu"),
    ("oh-my-issues", "skill", "issue kümeleme → plan-master", "backlog'u kök nedene göre kümeler", "yarim-plan.md", "backlog işleri", "düşük", "kurulu"),
    ("idea-refine / brainstorming / interview-me", "skill", "ıraksak-yakınsak fikir inceleme", "ham fikri keskinleştirir", "plan-kur", "adım 1: belirsiz istek", "düşük", "kurulu"),
    ("doubt-driven-development", "skill", "varsayım çapraz sorgusu", "varsayımları sınar", "kök neden kanıtı kuralı", "karar öncesi", "düşük", "kurulu"),
]


def sec(satir):
    ad, tur, oz = satir["ad"], satir["tur"], satir["ozellik"]
    metin = f"{ad} {oz}"
    for rx, karsi, adim, mal in KURALLAR:
        if re.search(rx, metin, re.I):
            return karsi, adim, mal
    return "ajan_sira (genel)", "adım 3: işe uyarsa 32f seçimine girer", "bilinmiyor; ölçülecek"


def main():
    with open(GIRDI, encoding="utf-8", errors="replace", newline="") as f:
        satirlar = list(csv.DictReader(f, delimiter="\t"))
    rx = re.compile(r"agent|ajan|swarm|orchestr|subagent|hook|memory|workflow|judge|a2a|council", re.I)
    cikti = [list(c) for c in CEKIRDEK]
    gorulen = {c[0].lower() for c in CEKIRDEK}
    for s in satirlar:
        if s["tur"] == "arastirilan" or not rx.search(f"{s['ad']} {s['ozellik']}"):
            continue
        if s["ad"].lower() in gorulen:
            continue
        gorulen.add(s["ad"].lower())
        karsi, adim, mal = sec(s)
        kurulu = "kurulu" if s["nerede"] in ("CC", "ikisi", "claude.ai") else "KUR"
        cikti.append([s["ad"], s["tur"], s["ozellik"][:140], s["ozellik"][:140], karsi, adim, mal, kurulu])
    # KUR: araştırılıp henüz kurulmamış, ajan/orkestrasyon sözcüğü geçenler
    for s in satirlar:
        if s["tur"] != "arastirilan" or not rx.search(f"{s['ad']} {s['ozellik']}"):
            continue
        if s["ad"].lower() in gorulen:
            continue
        gorulen.add(s["ad"].lower())
        karsi, adim, mal = sec(s)
        # karar kaydı: KUR/UYARLA/DENE → kurulacak-denenecek; ZATEN VAR/KURULDU → kurulu; RED/ATLANDI → ÖMER satırı; kalan → ÖĞREN (konu kartı)
        v = s["ozellik"]
        durum = ("kurulu (zaten var)" if re.search(r"ZATEN VAR|KURULDU", v) else
                 "RED/ATLANDI (ÖMER satırı)" if re.search(r"\bRED\b|ATLANDI", v) else
                 "KUR" if re.search(r"\bKUR\b|UYARLA|DENE", v) else "ÖĞREN (konu kartı)")
        cikti.append([s["ad"], "arastirilan", v[:140], v[:140], karsi, adim, mal, durum])
    with open(CIKTI, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(BASLIK)
        w.writerows(cikti)
    kur = sum(1 for c in cikti if c[7] == "KUR")
    print(f"satır={len(cikti)} kurulu={len(cikti) - kur} KUR={kur} -> {CIKTI}")


if __name__ == "__main__":
    sys.exit(main())
