"""JEV-2 d5 kapanış: zip'i main dist'e kopyalar; rapor/devir/SIRA'ya bayt olarak yazar (CRLF yok)."""
import shutil
from pathlib import Path

K = Path("C:/Projeler/omer-skills/.kos/kopru")
(Path("C:/Projeler/omer-skills/dist/jev-2")).mkdir(parents=True, exist_ok=True)
shutil.copy2("C:/Projeler/omer-skills-wt/jev2/dist/jev-2/jev.zip", "C:/Projeler/omer-skills/dist/jev-2/jev.zip")

RAPOR = """
JEV-2 — Son rapor (d5, 13 Eki 00:45) · kol/jev2 c2bb6e0..HEAD (d3 499f177+ddebe63 üstüne 5 commit) · push yok
- Ortaklaştırma: jev_yargic.Onbellekli(Tasiyici) tek satırla ortak önbelleğe geçiriyor. Doğrudan çağıran 3 yol (kalite3_hiz:124, fable_ajan_tablo:51, video parti:653) başka dallarda; yamalar main birleşmesinden sonra uygulanacak, satırları devir/kalite-3-hiz-devam · fable-ajan-devam · video-16-devam notlarında.
- Güvenilirlik (ücretsiz, mevcut veri): Jev koşudan koşuya ρ 0.989 → önbellek kayıpsız, tekrar ortalaması yararsız. Karma yargı jev_yargic.belirsiz: orta bandın %20'si Opus'a → ρ 0.43→0.62, MAE 1.20→0.93, Opus çağrısı %80 az. JEV-1 hedefi 0.55 aşıldı; merkez 6-8 arasında hep ≥0.57. Uyarı: n=50, örneklem içi; rastgele %20 de 0.60 veriyor.
- (c) Tetikleme: canlı skill hook'u 1979 aktif skill yüzünden her istemde "hata" veriyordu (hook.log: 00:00'dan beri 95/95; ücret yok, istem başına ~0.3 sn kayıp). Kök düzeltme: aşama-1 60k sınırında isteklere bölünüyor. Hook tavan1=1 ile eskisi gibi ücretlenmeden düşüyor. Ölçüm (20 istem, 60 istek, ~$0.10): aşama-1 isabeti 0.95, hit@3 0.65, p95 3.79 sn, $0.96/gün → hook kendi kuralını geçemiyor.
- Video rapor_onyargi (d3) hazır; entegrasyonu VİDEO-16 seçer. Aile kararları d3'te verildi (review ERTELE, router/compaction KURMA). HKCU kalemi kapandı: anahtar köprüden ortamda geliyor. Repoda "Lana" adlı değerlendirici yok.
- Test: tools/jev + test_jev_yargic 97 yeşil (yeni 4 test, değişiklik öncesi kırmızı görüldü). Ölçüm harcaması ≈ $0.10 Jev, claude -p 0.
- İki taraf: onay/jev_2_uygula.py --kuru TEMİZ (7 commit, 11 dosya, çatışma yok, commitsiz dosyayla çakışma 0). uygula = main'e --no-ff birleşme; --geri = revert. claude.ai: dist/jev-2/jev.zip (zip_denetle TEMİZ).
- Ömer kararı: hook'u kapat (JEV_SKILL_HOOK kullanıcı değişkeni 0) ya da skill sayısını ~400'e indir. Bu oturum ayarlara dokunmadı.
"""
DEVIR = """JEV-2 devam — BİTTİ (d5, 13 Eki 00:45). kol/jev2 son commit için `git -C C:/Projeler/omer-skills-wt/jev2 log -1`.
Desktop: python onay/jev_2_uygula.py --kuru → uygula (main birleşmesi); claude.ai'ye dist/jev-2/jev.zip yükle.
Birleşmeden sonra: devir notlarındaki 3 tek satır Onbellekli yaması (KALİTE-3-HIZ / FABLE-AJAN / VİDEO-16 sahipleri). Hook kararı Ömer'de.
"""
SIRA = ("- 13 Eki 00:45 JEV-2 BİTTİ (d5): Onbellekli adaptörü + karma yargı belirsiz (%20 Opus → ρ 0.43→0.62, Opus −%80) + "
        "skill hook kırığı (1979 aday → her istem hata) bölünerek düzeltildi, hook ücretsiz düşüşte; ölçüm hit@3 0.65/p95 3.8 sn → hook kapalı "
        "kalmalı (Ömer kararı). onay/jev_2_uygula.py --kuru TEMİZ · dist/jev-2/jev.zip TEMİZ · 97 test yeşil · ~$0.10.\n")
with open(K / "rapor/jev-2.md", "ab") as f:
    f.write(RAPOR.encode("utf-8"))
(K / "devir/jev-2-devam.md").write_bytes(DEVIR.encode("utf-8"))
with open(K / "gorev/SIRA.md", "ab") as f:
    f.write((("" if (K / "gorev/SIRA.md").read_bytes().endswith(b"\n") else "\n") + SIRA).encode("utf-8"))
print("ok")
