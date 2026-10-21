"""ARAÇ-DENETİM-1: son GUN gün köprü işleri için araç kullanım tablosu.

python tools/arac_denetim.py [--gun 7]  → docs/ogren/arac-denetim.tsv + özet (stdout)

Eşleme: is-kaydi.tsv satırının zaman (bitiş, yerel) ve dk penceresi (±2 dk pay) içinde
transkriptteki araç çağrıları (~/.claude/projects/<proje>/**/*.jsonl, subagents dahil).
Pencere tahmindir; is-kaydi'nde model kolonu yok, bu yüzden model dağılımı ölçülemez.
"""
import datetime as dt
import json
import sys
from pathlib import Path

K = Path(__file__).resolve().parent.parent
IS = K / ".kos/kopru/is-kaydi.tsv"
CIKTI = K / "docs/ogren/arac-denetim.tsv"
TR = Path.home() / ".claude/projects/C--Projeler-omer-skills"
KOLON = ("atlas", "katalog", "yonlendir", "departman", "havuz")
KATALOG_ONCE = ("atlas", "katalog", "yonlendir", "departman")
PAY = dt.timedelta(minutes=2)


def kategori(blok):
    ad, g = blok.get("name", ""), blok.get("input") or {}
    if ad == "Skill":
        s = g.get("skill", "")
        if s.startswith("departman-"):
            return "departman"
        if s in ("yetenek-getir", "find-skills"):
            return "katalog"
        return None
    if ad == "Read" and "docs/atlas" in str(g.get("file_path", "")).replace("\\", "/"):
        return "atlas"
    if ad == "Bash":
        c = g.get("command", "")
        if "katalog_ara.py" in c:
            return "katalog"
        if "yonlendir.py" in c:
            return "yonlendir"
        if "ucretsiz_havuz" in c or "ucuz_alt" in c:
            return "havuz"
    return None


def olaylar():
    ol = []
    for f in TR.rglob("*.jsonl"):
        for satir in f.open(encoding="utf-8", errors="replace"):
            if '"tool_use"' not in satir:
                continue
            try:
                d = json.loads(satir)
            except json.JSONDecodeError:
                continue
            icerik = (d.get("message") or {}).get("content")
            if not isinstance(icerik, list) or not d.get("timestamp"):
                continue
            t = dt.datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00")).astimezone().replace(tzinfo=None)
            for b in icerik:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    k = kategori(b)
                    if k:
                        ol.append((t, k))
    return ol


def sayi(metin, varsayilan=0.0):
    try:
        return float(metin)
    except ValueError:
        return varsayilan


def main():
    gun = int(sys.argv[sys.argv.index("--gun") + 1]) if "--gun" in sys.argv else 7
    sinir = dt.datetime.now() - dt.timedelta(days=gun)
    ol = olaylar()
    satirlar = IS.read_text(encoding="utf-8", errors="replace").splitlines()
    bas = satirlar[0].split("\t")
    cikti = ["\t".join(["zaman", "is", "efor", "dk", "usd", "sonuc", *KOLON, "katalog_once"])]
    toplam = {k: 0 for k in KOLON}
    atlanan, atlanan_usd, usd_top = 0, 0.0, 0.0
    for s in satirlar[1:]:
        r = dict(zip(bas, s.split("\t")))
        try:
            bitis = dt.datetime.strptime(r.get("zaman", ""), "%Y-%m-%d %H:%M")
        except ValueError:
            continue
        if bitis < sinir:
            continue
        dk, usd = sayi(r.get("dk", "")), sayi(r.get("usd", ""))
        bas_t, son_t = bitis - dt.timedelta(minutes=dk) - PAY, bitis + PAY
        say = {k: 0 for k in KOLON}
        for t, k in ol:
            if bas_t <= t <= son_t:
                say[k] += 1
        once = any(say[k] for k in KATALOG_ONCE)
        for k in KOLON:
            toplam[k] += say[k]
        usd_top += usd
        if not once:
            atlanan += 1
            atlanan_usd += usd
        cikti.append("\t".join([r.get("zaman", ""), r.get("is", ""), r.get("efor", ""), f"{dk:g}", f"{usd:.2f}",
                                r.get("sonuc", ""), *(str(say[k]) for k in KOLON), "evet" if once else "hayir"]))
    CIKTI.write_text("\n".join(cikti) + "\n", encoding="utf-8")
    print(f"is: {len(cikti) - 1} | katalog-once atlanan: {atlanan} | atlanan usd: {atlanan_usd:.2f} / toplam usd: {usd_top:.2f}")
    print(f"olay: {len(ol)} | havuz cagri (eslesen): {toplam['havuz']} | yazildi: {CIKTI}")


if __name__ == "__main__":
    main()
