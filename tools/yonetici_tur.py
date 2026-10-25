"""YONETICI-API-1: ajan_sira.py döngüsünün 20 dk'lık kontrol turu (rol=kontrol).
Biten işleri ajan-sira.log'dan okur, KABUL/DUR'u tools/kontrol_onoku.py ile (ücretsiz önce, belirsizse Console haiku) ön-değerlendirir,
≤5 satır yonetici-ozet.md yazar; Ömer/nihai karar gerektiren DUR için 'DESKTOP:' satırı. Kod değiştirmez, push/silme yok. Anahtar bu modülde görünmez."""
import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
K = KOK / ".kos/kopru"
LOG, OZET, DURUM = K / "ajan-sira.log", K / "yonetici-ozet.md", K / "yonetici-tur.durum.json"
ARALIK, SEYREK, GUN_TAVAN, TUR_ISI = 1200, 2400, 2.0, 3  # sn · sn · USD/gün · tur başı en çok iş (≈ ≤$0.03: çağrı tavanı $0.01)


def biten_isler(metin, ofs):
    """(BİTTİ adları, yeni bayt ofseti) — ofsetten sonraki log satırlarından."""
    ham = metin.encode("utf-8")
    return re.findall(r"(?m)^\S+ BİTTİ (\S+) rc", ham[ofs:].decode("utf-8", "replace")), len(ham)


def aralik(bugun_usd):
    return SEYREK if bugun_usd >= GUN_TAVAN else ARALIK


def vakit(son_t, simdi, bugun_usd):
    return simdi - son_t >= aralik(bugun_usd)


def tur(adlar, kontrol, ozet, ram):
    """adlar → (karar, kaynak) kontrol(ad); ≤5 satır özet dosyaya yazılır ve döner."""
    if not adlar:  # boş tur, Desktop'un henüz okumadığı DESKTOP: satırlarını ezmez
        return []
    sat = [f"{time.strftime('%H:%M')} YONETICI tur · {len(adlar)} biten · RAM %{ram}"]
    for ad in adlar[:3]:
        karar, kaynak = kontrol(ad)
        if not karar:
            sat.append(f"{ad} KONTROL-BOŞ")
        elif karar.upper().startswith("DUR"):
            sat.append(f"DESKTOP: {ad} DUR [{kaynak}] {' '.join(karar.split())[3:90].strip(' :-')}")
        else:
            sat.append(f"{ad} KABUL [{kaynak}]")
    sat = sat[:5]
    Path(ozet).write_text("\n".join(sat) + "\n", encoding="utf-8")
    return sat


def calistir(log, ram, bugun_usd):
    """ajan_sira döngüsünden çağrılır; yeni biten, görev dosyası KABUL'lu ve sonucu olan işleri değerlendirir. log(...) YONETICI satırı yazar."""
    sys.path[:0] = [str(KOK / "tools"), str(K)]
    import kontrol_onoku
    d = json.loads(DURUM.read_text(encoding="utf-8")) if DURUM.exists() else {"ofs": LOG.stat().st_size, "bekle": []}
    yeni, ofs = biten_isler(LOG.read_text(encoding="utf-8", errors="replace"), d["ofs"])
    uygun = [a for a in dict.fromkeys(d["bekle"] + yeni)
             if (K / f"gorev-{a}.md").exists() and (K / "ajan-sira" / f"{a}.json").exists() and kontrol_onoku.kabul_satiri(K / f"gorev-{a}.md")]
    sat = tur(uygun[:TUR_ISI], lambda a: kontrol_onoku.kontrol(a, K / f"gorev-{a}.md"), OZET, ram)
    DURUM.write_text(json.dumps({"ofs": ofs, "bekle": uygun[TUR_ISI:]}), encoding="utf-8")
    for s in sat:
        log("YONETICI", s)
    log("YONETICI", f"sonraki tur {aralik(bugun_usd) // 60} dk sonra · bugün Console ${bugun_usd:.2f}")
    return sat
