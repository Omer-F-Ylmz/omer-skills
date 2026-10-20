"""KURULUM-V1 d2: ccusage (salt okur, kurulumsuz) ile token_olc.py aynı pencerede alan alan kıyas.
  npx -y ccusage@latest daily --json --offline --since YYYYMMDD > ccu.json
  python tools/token_olc.py olc --gun N --cikti olc.json
  python tools/ccusage_kiyas.py ccu.json olc.json
Fark% = (token_olc - ccusage) / ccusage. Çıktıda yalnız sayı bulunur.
Ölçülen fark (19-21 Eki): cikti -%8,7 = token_olc aynı message.id için İLK akış kaydını tutuyor (ilk-kayıt 5.986.494 = olc); SON/en büyük kayıt 6.558.153, ccusage 6.556.851 (+%0,02).
Düşünme jetonu ayrı sayılmıyor (output_tokens'a dahil). usd +%6,9 = fiyat tablosu: girdi/cache ±%0,0 ve çıktı eksikken usd yüksek, token farkı açıklamaz."""
import json
import sys


def kiyasla(ccu, olc):
    cift = [("girdi", ccu["inputTokens"], olc["girdi"]), ("cikti", ccu["outputTokens"], olc["cikti"]),
            ("cache_okuma", ccu["cacheReadTokens"], olc["cache_okuma"]),
            ("cache_yazma", ccu["cacheCreationTokens"], olc["cache_5m"] + olc["cache_1h"]),
            ("usd", ccu["totalCost"], olc["usd"])]
    return [(ad, a, b, round(100 * (b - a) / a, 1) if a else None) for ad, a, b in cift]


if __name__ == "__main__":
    ccu = json.load(open(sys.argv[1], encoding="utf-8"))["totals"]
    olc = json.load(open(sys.argv[2], encoding="utf-8"))["toplam"]
    for r in kiyasla(ccu, olc):
        print("\t".join(map(str, r)))
