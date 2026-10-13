"""TOKEN-10 iş 1: ajan açıklama (frontmatter description) uzunluk ölçümü, çağrısız.
Canlı ~/.claude/agents/*.md ↔ repo kaynakları (ajanlar/** , skills/departman-*/ajanlar/**) ada göre eşlenir.
  python ajan_aciklama.py [wt]   → özet stdout + docs/token-10/aciklama.tsv"""
import json, re, statistics, sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf8")
EV = Path.home() / ".claude" / "agents"
WT = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[2])
ANAHTAR = re.compile(r"^[A-Za-z_][\w-]*:")


def aciklama(metin):
    """Frontmatter description değeri (çok satırlı dahil) ham metin olarak; yoksa None."""
    if not metin.startswith("---"):
        return None
    fm = metin.split("\n---", 1)[0].splitlines()[1:]
    for i, s in enumerate(fm):
        if s.startswith("description:"):
            parca = [s[len("description:"):].strip()]
            for t in fm[i + 1:]:
                if ANAHTAR.match(t):
                    break
                parca.append(t.strip())
            return " ".join(p for p in parca if p).strip().strip('"').strip("'")
    return None


def aciklama_degistir(metin, yeni):
    """Frontmatter'daki description (devam satırları dahil) tek satıra iner; başka bayt değişmez."""
    son = metin.index("\n---", 3)
    fm, govde = metin[:son], metin[son:]
    sat = fm.split("\n")
    i = next(i for i, s in enumerate(sat) if s.startswith("description:"))
    j = i + 1
    while j < len(sat) and not ANAHTAR.match(sat[j]):
        j += 1
    cr = "\r" if sat[i].endswith("\r") else ""
    deger = json.dumps(yeni, ensure_ascii=False) if re.search(r"[:#]|^[-\[{'\"!&*>|%@`]", yeni) else yeni  # YAML düz skaler kırılmasın
    sat[i:j] = [f"description: {deger}{cr}"]
    return "\n".join(sat) + govde


def kaynaklar(wt):
    k = {}
    for p in [*wt.glob("ajanlar/**/*.md"), *wt.glob("skills/departman-*/ajanlar/**/*.md")]:
        k.setdefault(p.stem, []).append(p)
    return k


if __name__ == "__main__":
    kay = kaynaklar(WT)
    satir, kendi, yabanci = [], [], []
    for p in sorted(EV.glob("*.md")):
        d = aciklama(p.read_text(encoding="utf8", errors="replace")) or ""
        src = kay.get(p.stem, [])
        ayni = [s for s in src if aciklama(s.read_text(encoding="utf8", errors="replace")) == d]
        (kendi if src else yabanci).append(len(d))
        ex = d.count("<example>")
        satir.append((p.stem, len(d), ex, len(src), len(ayni), ";".join(str(s.relative_to(WT)).replace("\\", "/") for s in ayni[:3])))
    out = WT / "docs/token-10/aciklama.tsv"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("ad\tkr\texample\tkaynak_n\tayni_n\tkaynak\n" + "".join("\t".join(map(str, s)) + "\n" for s in satir), encoding="utf8")

    def ozet(ad, x):
        if not x:
            return f"{ad}: 0"
        q = statistics.quantiles(x, n=10)
        return (f"{ad}: n {len(x)} · toplam {sum(x)} kr · ort {sum(x)//len(x)} · medyan {int(statistics.median(x))} · "
                f"p90 {int(q[8])} · max {max(x)} · >120 {sum(v > 120 for v in x)} · ≤90 {sum(v <= 90 for v in x)}")
    print(ozet("kendi (repo kaynaklı)", kendi))
    print(ozet("kaynaksız (~/.claude/agents, repo dışı)", yabanci))
    print("example bloklu", sum(s[2] > 0 for s in satir), "· kaynak var ama açıklama farklı", sum(s[3] > 0 and s[4] == 0 for s in satir),
          "· çok kaynaklı", sum(s[3] > 1 for s in satir))
    print("önek dağılımı (kendi):", Counter(s[0].split("-")[0] for s in satir if s[3]).most_common(25))
    print("en uzun 8:", [(s[0], s[1]) for s in sorted(satir, key=lambda s: -s[1])[:8]])
    kal = re.compile(r"\b(Use when|Use for|Use PROACTIVELY|including|with or without files)\b")
    print("kalıp sayıları:", Counter(m.group(1) for p in EV.glob("*.md") for m in kal.finditer(aciklama(p.read_text(encoding="utf8", errors="replace")) or "")))
