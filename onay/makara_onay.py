"""MAKARA onayı: kum havuzundaki kabul edilmiş kural önerisini gerçek hedef dosyaya ekler (yedekli, geri alınabilir). Claude token 0.
  python onay/makara_onay.py <id>          # uygula: hedefin yedeği .kos/makara/yedek/<id>.bak, sona kural eklenir
  python onay/makara_onay.py <id> --geri   # yedeği geri koy (hedef sonradan değiştiyse reddeder)"""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
M = KOK / ".kos/makara"


def ek(r, ham):
    nl = b"\r\n" if b"\r\n" in ham else b"\n"  # kullanıcı dosyasında satır sonu stilini koru (write_text CRLF tuzağı)
    return nl.join([b"", ("## Makara kuralı " + r["id"]).encode("utf-8"), b"- " + r["kural"].encode("utf-8"), b""])


def uygula(kid, geri=False, m=M):
    kayit = m / "kum" / f"{kid}.json"
    r = json.loads(kayit.read_text(encoding="utf-8"))
    hedef, yedek = Path(r["hedef"]), m / "yedek" / f"{kid}.bak"
    if geri:
        if r["durum"] != "uygulandi":
            return f"uygulanmamış ({r['durum']})"
        if hedef.read_bytes() != yedek.read_bytes() + ek(r, yedek.read_bytes()):
            return "hedef sonradan değişmiş: geri alma reddedildi"
        hedef.write_bytes(yedek.read_bytes())
        r["durum"] = "geri"
    else:
        if r["durum"] != "bekliyor":
            return f"zaten {r['durum']}"
        ham = hedef.read_bytes()
        yedek.parent.mkdir(parents=True, exist_ok=True)
        yedek.write_bytes(ham)
        hedef.write_bytes(ham + ek(r, ham))
        r["durum"] = "uygulandi"
    kayit.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    return f"{r['durum']}: {hedef}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print(uygula(sys.argv[1], "--geri" in sys.argv))
