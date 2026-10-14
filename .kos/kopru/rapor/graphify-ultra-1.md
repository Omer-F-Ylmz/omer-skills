# GRAPHIFY-ULTRA-1 — Ara rapor 1 (d1, çağrı 42)
Katalog: kullanılan [graphify CLI/iç API, rtk] · atlanan [katalog_ara (tek alanlı araç işi), alt ajan (kural 0)]
- Önkoşul GRAPHIFY-RAM-1 bu oturumda bitirildi (rapor/graphify-ram-1.md): graf 337→28 MB, artımlı update 829 MB.
- G0 taban (`graphify_ultra_g0.py`, 14 Eki, 733 transkript, görsel hariç, sonuç jetonu ≈ karakter/4, headroom sonrası):
  keşif 4 874 çağrı · 2.89M jeton. read-tam 718 çağrı 984k (%34) · read-aralık 844/951k · rtk-grep 1 735/460k ·
  rtk-read 983/321k · Grep 478/141k · oku 44/14k · graphify 11/8k · Glob 61/5k.
  "Graf yanıtlardı" ≈ 347k (%12) — neredeyse tamamı >3k jetonluk dosyanın tam Read'i; sembol-desenli Grep yalnız 5k.
  Ders: kaldıraç sembol aramasında değil, büyük dosyanın tam okunmasında → G4 kancası (iskelet önce) en büyük kalem.
  En pahalı 20: rapor/graphify-ultra-1/g0-pahali.tsv (çoğu TELVE fincan.js, Temp/*.txt, transkript .jsonl tam okuması).
- G2 kısmi: artımlı yol çalışıyor (değişmeyen topolojide "outputs left untouched"), ama 48 sn — hedef ≤10 sn değil.
| ölçü | önce | şimdi | hedef |
|---|---|---|---|
| update tepe RSS | ~3.5 GB | 829 MB (artımlı) | ≤500 MB |
| update süre | ? (öldürüldü) | 48 sn | ≤10 sn |
| graph.json | 337 MB | 28 MB | — |
Kalan: G1–G6 (devir/graphify-ultra-1-devam.md).
