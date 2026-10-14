"""K15 kalite kapısı: OLCUM-Z planında 17 bağlayıcı madde var mı (regex). Kullanım: python k15_puan.py <yanıt.txt|kapi-*.json> ..."""
import json, re, sys

MADDE = {
    "kilit": r"\.kilit",
    "durum_ozet": r"durum_ozet",
    "katalog_kullanilan": r"Katalog: kullanılan",
    "omniroute": r"KOPRU_OMNIROUTE",
    "fatura": r"api-kredi|ANTHROPIC_API_KEY",
    "claude_p_tavan": r"(≤|en (çok|fazla) |sınır\w* )\**\s*6",
    "olcum_sira": r"olcum_sira",
    "strict_mcp": r"strict-mcp-config",
    "ram_88": r"%88",
    "ram_90_cik": r"BEKLE:",
    "dk40_birakma": r"60 tur|55\. tur|150\. dakika|3 saat",
    "durma_30": r"%30|≥\s*30",
    "ara_kayit_15": r"15\. dk|15 dakika|İlk 15",
    "bekle_py": r"bekle\.py",
    "devir_sema": r"(?s)KALAN.*ARKA PLAN.*SON COMMIT.*AÇIK KARAR",
    "iki_taraf": r"(?s)(?=.*zip_denetle)(?=.*onay betiğ)",
    "graphify_son": r"(?i)graphify update.{0,80}(başlatılmaz|başlatma)",
}


def puan(metin):
    return {k: bool(re.search(v, metin)) for k, v in MADDE.items()}


if __name__ == "__main__":
    for yol in sys.argv[1:]:
        t = open(yol, encoding="utf-8").read()
        p = puan(json.loads(t)["result"] if yol.endswith(".json") else t)
        print(yol, f"{sum(p.values())}/{len(p)}", "eksik:", [k for k, v in p.items() if not v])
