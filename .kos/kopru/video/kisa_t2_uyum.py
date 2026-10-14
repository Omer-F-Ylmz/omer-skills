"""VİDEO-KISA-TOKEN-2 kapı: karar uyumu (eski tam-Claude ↔ t2a) + rapor bilgi alanları denetimi.
Eski formda KUR/DENE/ATLA yok → metinden ikili: "Fark yok" ya da ret sözcüğü = ATLA, açıklamalı öneri = olumlu (KUR/DENE)."""
import re
from collections import Counter
from pathlib import Path

K = Path(__file__).parent / "kisa"
RET = re.compile(r"yalnız adı geçiyor|belli değil|bilinmeyen|atla|gerek yok|ilgisiz|işe yaramaz|yaramaz|gereksiz|kurulmaz|karşılığı yok|uygun değil|değmez|fark yok", re.I)
AL = ("ad", "ne işe yarar", "link", "katalog", "karar")


def ogeler(p):
    """## Araçlar bölümü → {ad: (başlık satırı, açıklama satırı)}."""
    s = p.read_text(encoding="utf-8").split("## Araçlar", 1)[-1].split("\n## ", 1)[0].splitlines()
    out = {}
    for i, x in enumerate(s):
        m = re.match(r"- \*\*(.+?)\*\*(.*)", x)
        if m:
            out[m[1]] = (m[2], s[i + 1].strip() if i + 1 < len(s) and s[i + 1].startswith("  ") else "")
    return out


POZ = re.compile(r"işe yarar|kullanıl|bakılabilir|için|yerine", re.I)  # eski öneri dili: "Bizde X için", "pip yerine"


def ikili(t):
    return "olumlu" if POZ.search(t) and not RET.search(t) else "ATLA"


def main():
    n = uy = 0
    ayr, eksik, say = [], [], 0
    for y in sorted((K / "t2a").glob("ig-*.md")):
        e, t = ogeler(K / "eski-tamclaude" / y.name), ogeler(y)
        for ad, (bas, ac) in t.items():
            say += 1
            # alan denetimi: ad · ne işe yarar (açıklama boş/ad tekrarı değil) · link (yoksa açıkça yok) · katalog durumu · karar/fark
            al = {"ad": bool(ad), "ne işe yarar": bool(ac.split(" · ")[0].strip()), "link": "http" in bas or "katalogda" in ac,
                  "katalog": "katalogda" in ac, "karar": "karar:" in ac or "fark " in ac}
            if not all(al.values()):
                eksik.append((y.stem, ad, bas.split(" · ")[1] if " · " in bas else "?", tuple(k for k in AL if not al[k])))
            m = re.search(r"karar: (KUR|DENE|ATLA)", ac)
            if not m or ad not in e:
                continue
            yk = "ATLA" if m[1] == "ATLA" else "olumlu"
            ek = ikili(e[ad][1])
            n += 1
            uy += yk == ek
            if yk != ek:
                ayr.append(f"{y.stem} · {ad} · yeni {m[1]}: {ac.split('karar: ')[1][:110]} || eski: {e[ad][1][:160]}")
    print(f"karar uyumu {uy}/{n} = {uy / max(n, 1):.3f} (kapsam: yeni kararlı ve eski raporda aynı adla geçen araçlar)")
    print(*ayr, sep="\n")
    print(f"alan denetimi: {say} araç, eksik {len(eksik)}")
    print(Counter((t, k) for _, _, t, k in eksik))
    print(*[f"{v} {a} ({t}): {k}" for v, a, t, k in eksik if t != "teknik"][:12], sep="\n")


if __name__ == "__main__":
    main()
