"""JEV-2 d5: üç Jev çağıranının devir notuna Onbellekli yama satırı ekler (yalnız sona; bayt olarak, CRLF yok)."""
from pathlib import Path

D = Path("C:/Projeler/omer-skills/.kos/kopru/devir")
N = ("JEV-2 d5 (13 Eki 00:20) önbellek notu: kol/jev2 c2bb6e0 jev_yargic.Onbellekli(tasiyici) — Tasiyici yerine geçer, "
     "aynı (soru,state) ikinci kez ücretlenmez (Jev koşu-koşu ρ 0.989 → kayıpsız). kol/jev2 main'e birleşince tek satır: ")
YAMA = {
    "kalite-3-hiz-devam.md": "kalite3_hiz.py:124 `Tasiyici(env=ortam(), ...)` → `jev_yargic.Onbellekli(Tasiyici(env=ortam(), ...))` "
                             "(sys.path tools/olcum). Yeniden koşulan ajanda değişmeyen yanıt 0 istek.",
    "fable-ajan-devam.md": "fable_ajan_tablo.py:51 `Tasiyici(en_fazla=2, ...)` → `jev_yargic.Onbellekli(Tasiyici(en_fazla=2, ...))`; "
                           "elle eksik-süzme (satır 41-50) gereksizleşir.",
    "video-16-devam.md": "video/parti.py:653 `c.Tasiyici(env=env, ...)` → `jev_yargic.Onbellekli(c.Tasiyici(env=env, ...))` "
                         "(tools/olcum sys.path). Ön-yargıç: jev_yargic.rapor_onyargi(raporlar) hazır.",
}
for ad, satir in YAMA.items():
    with open(D / ad, "ab") as f:
        f.write(("\n" + N + satir + "\n").encode("utf-8"))
print("ok", len(YAMA))
