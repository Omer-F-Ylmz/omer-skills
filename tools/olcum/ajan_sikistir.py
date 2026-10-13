"""TOKEN-10 iş 2: kendi ajanlarımızın description'larını sıkıştırır (yalnız açıklama; gövde/model/ad değişmez).
  python ajan_sikistir.py uret [parti...]  → claude -p sonnet, parti başına 1 çağrı → docs/token-10/uret_<n>.json
  python ajan_sikistir.py denetle          → uret_*.json + onar.json birleşir → docs/token-10/esleme.tsv; kural ihlallerini basar
Canlı ~/.claude'a yazmaz; ANTHROPIC_API_KEY alt sürece verilmez (api-kredi.kapali)."""
import ctypes, json, os, re, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf8")
sys.path.insert(0, str(Path(__file__).parent))
from ajan_aciklama import EV, aciklama, kaynaklar

WT = Path(__file__).resolve().parents[2]
CIK = WT / "docs/token-10"
PARTI = [["fe", "sec", "db"], ["qa", "ops", "dil", "pln"], ["dn", "dok", "ml", "otm", "urn"],
         ["ara", "vid", "ajn", "bl", "inc", "oyn", "be", "git", "vrm", "mob"]]
KURAL = """Rewrite each Claude Code subagent description below into ONE line, target <=90 characters (hard max 120).
Shape: what it does + when (distinctive trigger words) + what it is not confused with, only if room.
Keep the words that separate it from its siblings in the same family (same name prefix) - the agent picker must still choose correctly.
Keep the original language (English stays English; Turkish words that appear as triggers may stay).
No "Use when" boilerplate unless it fits; no trailing period needed. Do not invent capabilities.
Answer ONLY a JSON object {"<name>": "<new description>", ...} with every name below, nothing else.

"""


def ram():
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("y", ctypes.c_ulong), *[(f"f{i}", ctypes.c_ulonglong) for i in range(7)]]
    m = M(); m.l = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.y


def kendi():
    kay = kaynaklar(WT)
    return {p.stem: aciklama(p.read_text(encoding="utf8")) or "" for p in sorted(EV.glob("*.md")) if p.stem in kay}


def jaccard(a, b):
    a, b = set(re.findall(r"\w+", a.lower())), set(re.findall(r"\w+", b.lower()))
    return len(a & b) / len(a | b) if a | b else 0


def uret(no, eski):
    ad = {k: v for k, v in eski.items() if k.split("-")[0] in PARTI[no]}
    istem = KURAL + "\n".join(f"{k}: {v}" for k, v in ad.items())
    while ram() >= 86:
        time.sleep(30)
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}
    r = subprocess.run(["claude", "-p", "--output-format", "json", "--model", "sonnet", "--max-turns", "1", "--tools", ""],
                       input=istem, capture_output=True, text=True, encoding="utf8", cwd=WT, env=env, timeout=1500,
                       creationflags=0x08000000)
    j = json.loads(r.stdout)
    yeni = json.loads(re.search(r"\{.*\}", j["result"], re.S).group(0))
    (CIK / f"uret_{no}.json").write_text(json.dumps(yeni, ensure_ascii=False, indent=0), encoding="utf8")
    print("parti", no, "ajan", len(ad), "dönen", len(yeni), "eksik", sorted(set(ad) - set(yeni))[:5], flush=True)


def denetle(eski):
    yeni = {}
    for f in sorted(CIK.glob("uret_*.json")) + [CIK / "onar.json"]:
        if f.exists():
            yeni.update(json.loads(f.read_text(encoding="utf8")))
    hata = [f"eksik {k}" for k in eski if k not in yeni]
    for k, v in yeni.items():
        if k not in eski:
            hata.append(f"bilinmeyen {k}")
        elif "\n" in v or len(v) > 120 or not v.strip() or ":" in v[:1]:
            hata.append(f"biçim {k} {len(v)}")
    aile = {}
    for k in yeni:
        aile.setdefault(k.split("-")[0], []).append(k)
    for ks in aile.values():
        for i, a in enumerate(ks):
            for b in ks[i + 1:]:
                if jaccard(yeni[a], yeni[b]) >= 0.6:
                    hata.append(f"benzer {a}~{b} {jaccard(yeni[a], yeni[b]):.2f}")
    (CIK / "esleme.tsv").write_text("ad\teski\tyeni\n" + "".join(f"{k}\t{eski[k]}\t{yeni.get(k, eski[k])}\n" for k in eski), encoding="utf8")
    e, y = sum(map(len, eski.values())), sum(len(yeni.get(k, v)) for k, v in eski.items())
    print(f"ajan {len(eski)} · kr {e} → {y} (−{e - y}, %{100 * (e - y) // max(e, 1)}) · ≤90 {sum(len(v) <= 90 for v in yeni.values())} · ihlal {len(hata)}")
    for h in hata[:30]:
        print(" ", h)
    return hata


if __name__ == "__main__":
    CIK.mkdir(parents=True, exist_ok=True)
    eski = kendi()
    if sys.argv[1] == "uret":
        for no in map(int, sys.argv[2:] or range(len(PARTI))):
            uret(no, eski)
    else:
        sys.exit(1 if denetle(eski) else 0)
