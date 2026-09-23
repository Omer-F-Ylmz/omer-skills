# caveman
ad: caveman
tur: teknik
video: fixture
karar: DENE
hipotez: Caveman stili ana oturum çıktı tokenını ≥%30 azaltır, kabul oranı düşmez.
metrik: tur başına çıktı token (thinking hariç) ve toplam $; kabul kriteri geçme oranı.
butce: 3+3 koşu A/B, Jev 0, ≤30 dk, ≤$3.
geri_alma: stil satırını/modu kaldır; ayar değişikliği yok.
esik: çıktı token −%30 ve toplam maliyet −%3 ya da daha iyi, kabul 3/3.
## Ne
Çıktı tokenını mağara adamı diliyle kısaltan prompt stili (caveman).
## Bizde durum
- jev skill (Act): yok
kısmen: Concise çıktı stili (settings outputStyle) + ≤15 satır kapanış raporu kuralı (global CLAUDE.md, omer-kurallar:9); omni-compression (synced, OmniRoute Caveman modu; CC'de kapalı) ve cli-compression (Caveman kuralları); RTK çıktı sıkıştırma. CACHE-1 (docs/cache-notlari.md) ve ÇIKTI-1 (docs/cikti-notlari.md): maliyet ≈ girdi context × tur, çıktı payı %15.5.
## Beklenen fayda
çıktı token/tur azalır; ama maliyetin %15.5'i çıktı (ÇIKTI-1), toplam etki küçük.
## Maliyet/risk
okunabilirlik düşer; rapor kuralıyla çakışır; kazanç maliyetin küçük payında.
## Karar
DENE
## Sonraki adım
14b'de docs/denemeler/caveman.md A/B.
