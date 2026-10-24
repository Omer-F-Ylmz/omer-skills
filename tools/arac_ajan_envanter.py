"""ARAC-AJAN-OZELLIK-1: docs/envanter/envanter.tsv + elle yazılmış çekirdek tablodan arac-ajan-ozellik.tsv üretir.
Kullanım: python tools/arac_ajan_envanter.py  (salt okuma + tek çıktı dosyası; ağ yok)"""
import csv, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
GIRDI = KOK / "docs/envanter/envanter.tsv"
CIKTI = KOK / "docs/envanter/arac-ajan-ozellik.tsv"
BASLIK = ["arac", "tur", "ozellik", "ne_yapar", "bizde_karsiligi", "akista_adim", "maliyet", "kurulu", "kart"]

# kart etiketi → regex (kelime sınırlı; yalnız açıklama/ad metninde). Öncelik sırası = sözlük sırası.
KART = {
    "swarm": r"\b(swarm|hive|queen|consensus|raft|multi-?agent)\b",
    "is-akisi": r"\b(workflow engine|orchestrat\w*|orkestrasyon|dispatch\w*|ralph|conductor|herdr|loopy|dmux|devfleet|gsd|octo|(agent|autonomous) loops?)\b",
    "ogrenen-bellek": r"\b(agent memory|long-term memory|memory (store|layer|system)s?|self-learning|continuous.learning|learning loop|instincts?|reasoningbank|self-improv\w*|mem-search|agentmemory|agentdb)\b",
    "hakem": r"\b(llm judge|judge model|council|multi-?model|arbiter|cross-model|a2a|model router|llm router|omniroute (combos?|routing)|yönlendirici|9router (combos?|routing))\b",
    "hook": r"\b((pre|post)-?tool-?use|(session-?start|stop|claude code|git|pre-commit) hooks?|hooks? (system|engine|runner|rules?)|tdd-guard|gateguard)\b",
    "ajan": r"\b(sub-?agents?|orchestrator|coordinator)\b",
}
# kart etiketi → (bizde karşılığı, akıştaki adım, RAM/token maliyeti)
ESLEME = {
    "swarm": ("ajan_sira + yonetici ajan", "adım 3: paralel alt iş (ORDU-1); swarm tek tek açılır", "yüksek RAM; bitince pid kapat"),
    "is-akisi": ("ajan_sira + suite-kosucu/okuyucu", "adım 3: bölme ve paralel çalıştırma", "orta"),
    "ogrenen-bellek": ("2. beyin döngüsü + claude-mem + ruflo pattern-store", "başta pattern-search/recall, sonda pattern-store (K2n/K6)", "düşük; ≤10 satır enjeksiyon"),
    "hakem": ("OmniRoute combos + yonlendir.py (K3) + DENETİM", "model merdiveni / çoklu-model karar", "düşük"),
    "hook": ("settings.json hooks + yarim_bekci/ram_bekci", "PreToolUse/Stop; kapı görevi", "düşük; her çağrıda ms"),
    "ajan": ("okuyucu/suite-kosucu + .claude/agents", "adım 3: Agent tipi olarak çağır", "orta; alt ajan bağlamı"),
}


def kartlar(ad, metin, sayac=None):
    """Etiket listesi: ad+açıklamada kelime eşleşmesi; eklentide sayaçtan (ajan>0, hook bayrağı)."""
    et = [k for k, rx in KART.items() if re.search(rx, f"{ad} {metin}", re.I)]
    if sayac:
        if sayac["ajan"] > 0 and "ajan" not in et:
            et.append("ajan")
        if sayac["hook"] and "hook" not in et:
            et.append("hook")
    return et


def eklenti_ayir(oz):
    """'N skill · N komut · N ajan · N MCP · [hook ·] açık · açıklama' → (sayaç, açıklama); biçim tutmazsa (None, oz)."""
    p = oz.split(" · ")
    if len(p) < 6 or not p[2].endswith("ajan"):
        return None, oz
    return {"ajan": int(p[2].split()[0]), "hook": "hook" in p[4:6]}, p[-1]


def sec(etiketler):
    # etiketsiz satır = konu kartı (karar sütunu geçerli); "genel" kovası kaldırıldı
    return ESLEME[etiketler[0]] if etiketler else ("yok; kurulu/KUR sütunundaki karar geçerli", "adım 1: konu kartı olarak okunur", "ölçülmedi")


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


def main():
    with open(GIRDI, encoding="utf-8", errors="replace", newline="") as f:
        satirlar = list(csv.DictReader(f, delimiter="\t"))
    cikti = [c + (", ".join(kartlar(c[0], c[2] + " " + c[3])) or "çekirdek-araç",) for c in CEKIRDEK]
    gorulen = {c[0].lower() for c in CEKIRDEK}
    for s in satirlar:
        if s["tur"] == "arastirilan" or s["ad"].lower() in gorulen:
            continue
        sayac, acik = eklenti_ayir(s["ozellik"]) if s["tur"] == "plugin" else (None, s["ozellik"])
        et = kartlar(s["ad"], acik, sayac)
        if s["tur"] == "ajan":  # alan uzmanı ajan tanımı araç özelliği değil; yalnız orkestrasyon/bellek/hakem/hook sözcüğü olanlar
            et = [k for k in et if k != "ajan"]
        if not et:
            continue
        gorulen.add(s["ad"].lower())
        karsi, adim, mal = sec(et)
        kurulu = "kurulu" if s["nerede"] in ("CC", "ikisi", "claude.ai") else "KUR"
        cikti.append([s["ad"], s["tur"], ", ".join(et), acik[:140], karsi, adim, mal, kurulu, ", ".join(et)])
    # araştırılıp karar verilmiş satırlar: kart etiketi taşıyanlar + KUR kararlılar (KUR hiç atlanmaz)
    for s in satirlar:
        if s["tur"] != "arastirilan" or s["ad"].lower() in gorulen:
            continue
        v = s["ozellik"]
        # karar kaydı: KUR/UYARLA/DENE → kurulacak-denenecek; ZATEN VAR/KURULDU → kurulu; RED/ATLANDI → ÖMER satırı; kalan → ÖĞREN (konu kartı)
        durum = ("kurulu (zaten var)" if re.search(r"ZATEN VAR|KURULDU|uygulandı|uyarlama: docs|deneme: docs|docs/(uyarlamalar|denemeler)/", v) else
                 "RED/ATLANDI (ÖMER satırı)" if re.search(r"\bRED\b|ATLANDI", v) else
                 "KUR" if re.search(r"\bKUR\b|UYARLA|DENE", v) else "ÖĞREN (konu kartı)")
        et = kartlar(s["ad"], v)
        if not et and durum != "KUR":
            continue
        gorulen.add(s["ad"].lower())
        karsi, adim, mal = sec(et)
        cikti.append([s["ad"], "arastirilan", ", ".join(et), v[:140], karsi, adim, mal, durum, ", ".join(et) or "konu"])
    with open(CIKTI, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(BASLIK)
        w.writerows(cikti)
    kur = sum(1 for c in cikti if c[7] == "KUR")
    print(f"satır={len(cikti)} kurulu={len(cikti) - kur} KUR={kur} -> {CIKTI}")


if __name__ == "__main__":
    sys.exit(main())
