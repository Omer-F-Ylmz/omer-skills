"""ARAC-BUL-2 adım 4: modlar.tsv ayıklayıcısını genişletir — 'X mode' dışında bayrak / env / hook olayı / dosya / kısayol / özellik / ek slash.
docs/video-tarama/derin/*.json (yalnız claude|anthropic geçen videolar) → regex adayları → belirsiz slash/bayrak adayları ücretsiz modelle sınıflanır.
modlar.tsv'ye yeni satırlar EKLER (mevcut satırlar korunur). Kullanım: python tools/mod_cikar_2.py [--model-yok]"""
import collections, csv, glob, json, os, re, sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RAPOR = os.path.join(KOK, ".kos", "kopru", "rapor")
MODLAR = os.path.join(RAPOR, "modlar.tsv")

SLASH = set("plan model fast loop schedule compact clear init memory agents mcp plugin hooks permissions config context cost usage resume rewind review security-review output-style vim btw ultrareview ultraplan goal skills doctor export ide terminal-setup statusline add-dir teleport sandbox todos voice chrome remote-control batch simplify".split())
KESIN = [  # (etiket öneki, regex, grup) — desen kendiliğinden kesin; model gerekmez
    ("env", re.compile(r"\b((?:CLAUDE_CODE|ANTHROPIC|CLAUDE)_[A-Z0-9_]{3,40}|DISABLE_[A-Z0-9_]{4,40}|MAX_THINKING_TOKENS|BASH_DEFAULT_TIMEOUT_MS|MCP_TIMEOUT)\b"), 1),
    ("hook", re.compile(r"\b(PreToolUse|PostToolUse|UserPromptSubmit|SessionStart|SessionEnd|SubagentStop|PreCompact|PermissionRequest|Notification hook|Stop hook)\b"), 1),
    ("dosya", re.compile(r"(?<![\w/])(CLAUDE\.md|AGENTS\.md|SKILL\.md|settings\.local\.json|settings\.json|\.mcp\.json|\.claudeignore|\.claude/(?:commands|agents|skills|hooks|rules))\b"), 1),
    ("kisayol", re.compile(r"\b(shift\s?\+\s?tab|ctrl\s?\+\s?[a-z]|esc\s?esc|double[- ]esc(?:ape)?|alt\s?\+\s?[tpm])\b", re.I), 1),
    ("ozellik", re.compile(r"\b(ultrathink|think hard(?:er)?|extended thinking|thinking budget|auto[- ]?compact|headless|git worktrees?|sub-?agents?|output style|status ?line|permission mode|bypass permissions|dangerously-skip-permissions|prompt caching|background tasks?|agent teams?|plugin marketplace|custom commands?|slash commands?|checkpoint(?:s|ing)?)\b", re.I), 1),
]
MODE = re.compile(r"\b([A-Za-z]+(?:[ -][A-Za-z]+)?) mode\b")
MOD_DUR = {"the", "a", "in", "this", "that", "your", "my", "to", "of", "and", "or", "is", "on", "for", "it", "with", "when", "one", "another", "other", "same", "different", "default", "normal", "ve", "bir", "bu", "an", "as", "at", "by", "be", "if", "so", "we", "you", "now", "dark", "light"}
FLAG = re.compile(r"(?<![\w-])(--[a-z][a-z0-9-]{3,30})\b")
SLASH_RE = re.compile(r"(?<![\w/.:<>-])/([a-z][a-z-]{2,24})\b")
YOL_DUR = {"usr", "bin", "etc", "var", "tmp", "home", "src", "lib", "dev", "api", "users", "node", "opt", "mnt", "app", "docs", "www", "tree", "blob", "main", "master", "issues", "pull", "wiki", "and", "the", "for", "not", "you", "can", "with", "this", "that", "from", "will", "all", "are", "was"}


def norm_ad(s):
    return s.lower().replace("\n", " ").strip()


def tara():
    adaylar = collections.defaultdict(lambda: {"vid": set(), "ek": set(), "ko": set(), "baglam": ""})
    for f in sorted(glob.glob(os.path.join(KOK, "docs/video-tarama/derin/*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        kod = d.get("kod") or os.path.basename(f)[:-5]
        ek = "\n".join([str(e.get("t", "")) for e in d.get("ekran") or [] if isinstance(e, dict)] + [str(d.get("kare_aciklama") or "")] + [str(x) for x in d.get("komutlar") or []])
        ko = " ".join(str(s.get("t", "")) for s in d.get("transkript") or [] if isinstance(s, dict))
        if not re.search(r"claude|anthropic", ek + " " + ko, re.I):
            continue
        for yer, txt in (("ek", ek), ("ko", ko)):
            for onek, rx, g in KESIN:
                for m in rx.findall(txt):
                    m = re.sub(r"\s+", "", m).lower() if onek == "kisayol" else re.sub(r"\s+", " ", m).strip()
                    if onek in ("ozellik", "dosya"):
                        m = m.lower() if onek == "ozellik" else m
                    x = adaylar[(onek, m)]
                    x["vid"].add(kod); x[yer].add(kod)
            for m in MODE.findall(txt):
                m = m.lower().replace("-", " ")
                if m.split()[-1] in MOD_DUR or m.split()[0] in MOD_DUR or len(m) < 4:
                    continue
                x = adaylar[("mod", m)]
                x["vid"].add(kod); x[yer].add(kod)
        # belirsiz adaylar: yalnız ekran/komut metninde (konuşma gürültülü)
        for m in SLASH_RE.findall(ek):
            if m in SLASH or m in YOL_DUR:
                continue
            x = adaylar[("slash?", "/" + m)]
            x["vid"].add(kod); x["ek"].add(kod)
        for m in FLAG.findall(ek):
            x = adaylar[("bayrak?", m)]
            x["vid"].add(kod); x["ek"].add(kod)
    return adaylar


def sinifla(belirsiz):
    """belirsiz (tip, ad) listesi → ücretsiz model: gerçek Claude Code slash komutu/CLI bayrağı mı? Dönüş: {(tip,ad): True}"""
    import ucretsiz_havuz
    onay = {}
    for i in range(0, len(belirsiz), 60):
        parca = belirsiz[i:i + 60]
        istem = ("Aşağıdaki her satır bir YouTube videosunun ekranından çıkan metin adayıdır. 'slash?' = '/komut' biçimi, 'bayrak?' = '--bayrak' biçimi. "
                 "Hangileri Claude Code'un (veya Claude Code ekosisteminin: skill/plugin/CLI) gerçek bir slash komutu ya da komut satırı bayrağı? "
                 "Yol parçası, URL parçası, OCR artığı, başka aracın komutu olanları ELE. Yalnız gerçek olanların satır numaralarını virgülle döndür (örn: 1,4,7); hiçbiri yoksa 'yok'.\n"
                 + "\n".join(f"{j + 1}. {t} {a}" for j, (t, a) in enumerate(parca)))
        y, kol, log = ucretsiz_havuz.cagir("ozet", istem, max_tokens=300)
        if not y:
            print("model yanıtsız", i, flush=True)
            continue
        for n in re.findall(r"\d+", y.split("\n")[-1] if "yok" not in y.lower() else ""):
            n = int(n) - 1
            if 0 <= n < len(parca):
                onay[parca[n]] = True
    return onay


def main():
    ad = tara()
    mevcut = set()
    with open(MODLAR, encoding="utf-8") as f:
        satirlar = list(csv.reader(f, delimiter="\t"))
    for r in satirlar[1:]:
        mevcut.add(norm_ad(r[0]))
    belirsiz = [k for k, x in ad.items() if k[0].endswith("?") and len(x["vid"]) >= 2]
    onay = {} if "--model-yok" in sys.argv else sinifla(sorted(belirsiz))
    yeni = []
    for (tip, a), x in ad.items():
        if tip.endswith("?"):
            if (tip, a) not in onay:
                continue
            tip = tip[:-1]
        elif tip == "mod" and len(x["vid"]) < 3:
            continue
        etiket = f"{tip}: {a}"
        if norm_ad(etiket) in mevcut:
            continue
        yer = "+".join(y for y, n in (("ekranda", x["ek"]), ("konuşmada", x["ko"])) if n)
        yeni.append([etiket, len(x["vid"]), yer, ",".join(sorted(x["vid"])[:5])])
    yeni.sort(key=lambda r: -r[1])
    with open(MODLAR, "ab") as f:  # bayt olarak ekle (mevcut dosya CRLF, csv.writer varsayılanı)
        for r in yeni:
            f.write(("\t".join(str(c) for c in r) + "\r\n").encode("utf-8"))
    print("eski", len(satirlar) - 1, "yeni", len(yeni), "belirsiz", len(belirsiz), "onaylı", len(onay), flush=True)
    for r in yeni[:15]:
        print(r[0], r[1])


if __name__ == "__main__":
    main()
