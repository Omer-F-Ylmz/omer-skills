"""ÖĞRENME-2b d4 ($0): haftalık ders özeti → claude.ai skill zip'i (dist/ders-ozeti/ders-ozeti.zip). Yerel yola bağlı değil; yalnız elenmemiş
derslerin metni (en çok 25, desteği yüksek önce). Sonra: python tools/skill-paket/zip_denetle.py dist/ders-ozeti. Haftalık: görev zamanlayıcıdan bu betik.
Kullanım: python tools/ogrenme/ders_zip.py"""
import sys
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(KOK / "tools"))
import beyin_dusun as b  # noqa: E402

SKILL = """---
name: ders-ozeti
description: Omer'in 2. beyninden haftalik ders ozeti. Is baslarken ayni hatalari onlemek icin oku; hata, pahali adim ya da tekrar eden sorun varsa bu derslere bak.
---

# Haftalik ders ozeti

Her madde gercek islerden cikan, ucretsiz modelle uretilmis derstir. "kural" olanlar dogrulanmistir; "taslak" olanlar aday derstir, kesin sayma.

{dersler}
"""


def dersler_metni(oneriler, n=25):
    sec = sorted((x for x in oneriler if x.get("durum") != "elendi"), key=lambda x: (x.get("durum") == "kural", x.get("destek", 0)), reverse=True)[:n]
    return "\n".join(f"- [{x.get('durum', 'taslak')}] {x['metin'].replace(chr(10), ' ')}" for x in sec) or "- (henuz ders yok)"


def main(cikti=KOK / "dist/ders-ozeti"):
    cikti.mkdir(parents=True, exist_ok=True)
    yol = cikti / "ders-ozeti.zip"
    with zipfile.ZipFile(yol, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("ders-ozeti/SKILL.md", SKILL.format(dersler=dersler_metni(b.oneri_oku())))
    print(yol)


if __name__ == "__main__":
    main()
