"""TOKEN-9 öneri 2: devam oturumunun 'durum çıkarma' evresini TEK komuta indirir.
Kullanım: python C:/Projeler/omer-skills/.kos/kopru/durum_ozet.py <görev> [wt_yolu]
Çıktı kısa ve sayısaldır (≈3k kr tavan); dosya içeriğini bağlama dökmez."""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(r"C:\Projeler\omer-skills")
KOPRU = KOK / ".kos" / "kopru"
PROJ = Path.home() / ".claude" / "projects"


def durma_orani(yol, son=20, girdi=3000):
    """TELVE-TOKEN-1: son `son` API adımında önbellek durması sayısı (cw=0 ve önbelleksiz girdi ≥ girdi;
    tools/token_olc.py --durma tanımı). Dönüş (durma, adım)."""
    adim, gorulen = [], set()
    with Path(yol).open(encoding="utf-8", errors="replace") as f:
        for s in f:
            try:
                o = json.loads(s)
            except ValueError:
                continue
            m = o.get("message") if isinstance(o, dict) else None
            if (o.get("type") != "assistant" or not isinstance(m, dict) or not isinstance(m.get("usage"), dict)
                    or m.get("id") in gorulen):
                continue
            gorulen.add(m.get("id"))
            u = m["usage"]
            adim.append(not u.get("cache_creation_input_tokens") and (u.get("input_tokens") or 0) >= girdi)
    adim = adim[-son:]
    return sum(adim), len(adim)


def durma_satiri(transkriptler):
    """En yeni transkriptin durma oranı tek satır; ≥%30 → DEVAM-KURALI önerisi: ara kayıt + DUR, yeni oturum."""
    j = max(transkriptler, key=lambda p: p.stat().st_mtime, default=None)
    if j is None:
        return "-- durma: transkript yok"
    d, n = durma_orani(j)
    return (f"-- durma: {j.parent.name[-28:]}/{j.stem[:8]} son {n} adımda {d} (%{100 * d / (n or 1):.0f})"
            + (" · ≥%30 → ara kayıt + DUR, yeni oturum" if n and d / n >= 0.3 else ""))


def git(wt, *a):
    r = subprocess.run(["git", "-C", str(wt), *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.stdout or r.stderr).strip()


def bas(yol, n):
    try:
        return "\n".join(Path(yol).read_text(encoding="utf-8", errors="replace").splitlines()[:n])
    except OSError:
        return "(yok)"


def son(yol, n):
    try:
        return "\n".join(Path(yol).read_text(encoding="utf-8", errors="replace").splitlines()[-n:])
    except OSError:
        return "(yok)"


def main():
    if len(sys.argv) < 2:
        sys.exit("kullanım: durum_ozet.py <görev> [wt_yolu]")
    gorev = sys.argv[1]
    wt = Path(sys.argv[2]) if len(sys.argv) > 2 else KOK
    print(f"== {gorev} · wt {wt}")
    st = git(wt, "status", "--short", "--untracked-files=no").splitlines()
    print(f"-- git: dal {git(wt, 'branch', '--show-current')} · izlenen değişiklik {len(st)}")
    for s in st[:10]:
        print("  ", s)
    print("-- son 3 commit:\n" + git(wt, "log", "-3", "--format=  %h %ad %s", "--date=format:%H:%M"))
    print("-- devir (ilk 15 satır):\n" + bas(KOPRU / "devir" / f"{gorev}-devam.md", 15))
    print("-- rapor (son 6 satır):\n" + son(KOPRU / "rapor" / f"{gorev}.md", 6))
    satirlar = []
    for sira in (KOPRU / "SIRA.md", KOPRU / "gorev" / "SIRA.md"):
        try:
            satirlar += [s[:220] for s in sira.read_text(encoding="utf-8", errors="replace").splitlines() if gorev.upper() in s.upper()]
        except OSError:
            pass
    print("-- SIRA (son 3):\n" + ("\n".join(satirlar[-3:]) or "(yok)"))
    kilitler = sorted(p.name for p in (KOPRU / "gorev").glob(f"{gorev}*.kilit"))
    print("-- kilitler: " + (", ".join(kilitler) or "(yok)"))
    print(durma_satiri((PROJ / re.sub(r"[^A-Za-z0-9]", "-", str(wt.resolve()))).glob("*.jsonl")))


if __name__ == "__main__":
    main()
