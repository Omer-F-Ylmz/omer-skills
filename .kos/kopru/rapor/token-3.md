# TOKEN-3 — oturum başı, alt ajan, efor, ölçüm koşuları

## d1 ara (14 Eki ~18:05)
- Veri (son 6 sa, 56 oturumun 1. isteği): omer-skills cr hep 6613, TELVE 4702; cw 20–27k. Oturumlar arası önbellekte yalnız araç+system tabanı var.
- Ölçüm aracı: `.claude/token3/onek_kayit.py` — yerel kayıt vekili (taban URL yalnız çocuğun --settings env'inde, global ayara dokunmaz) + ajan profiliyle N claude -p. 2 koşu harcandı (claude -p 2/6); üst port 6769 bağlantıyı reddetti → API'ye istek gitmedi, ama 2 oturumun gövdeleri yakalandı (Headroom öncesi, CC'nin ham isteği).
- K10 blok karşılaştırması (oturum A ↔ B, aynı istem):
  - tools (27, 99.7k kar.) · system[0..2] (6k; cc system[1], system[2]) · msg0.0 CLAUDE.md (9.9k) · msg0.2 atıf · msg0.3 istem: AYNI.
  - msg0.1 bağlam (git durumu, 4k): FARK — git status her dosya değişiminde kayar.
  - msg1.0 (rol system, cc burada, 39.5k): FARK — claude-mem "recent context, <saat:dakika>" damgası + gözlem listesi.
- Yapısal sonuç: CC kullanıcı istemini msg0'a, SessionStart/ortam/ajan listesi bloğunu (msg1) istemden SONRA koyuyor. Farklı istemli oturumlar msg1'i asla paylaşamaz; oturumlar arası paylaşılabilir en uzun önek = araç+system (bugün okunan 6.6k). msg0.0–0.2 için kırılma noktası yok (CC 4 cc'yi system[1], system[2], msg1.0, son mesaja koyuyor). "2. oturum cr ≥ %80" yalnız AYNI istemli koşularda (K13) ulaşılabilir; bunun için git durumu + claude-mem damgası sabitlenmeli (global/eklenti ayarı → öneri).
- msg1 dökümü (kar.): Ponytail 2.9k · kod haritası 2.2k · context-mode 4.6k · superpowers 3.4k · work state 0.8k · claude-mem 4.9k · ECC özet 1.1k · ortam+üslup 2.3k · **ajan listesi 16.6k** · auto mode 0.6k.
- K2 deny yalnız ~/.claude/agents'ı kapsıyordu; listede 50 ajan kalmıştı, 38'i plugin ajanı (octo 14, ecc 10, commercial-legal 3, ...).
- UYGULANDI (yerel, global ayar değil): `tools/cc_profil.py` + `tools/cc-kopru/sunucu.mjs` ajanTut deny'ı installed_plugins.json'daki plugin ajanlarına genişletir (ad = eklenti:alt dizin:ad). Gerçek makinede deny 578→770, yakalanan listedeki 38 plugin ajanının 38'i kapsandı. Test: pytest test_cc_profil 18/18, node ajan-argv 12/12 (yeni iddia ikisinde de).
- Tahmin (doğrulanmadı): ajan listesi 16.6k→~3.5k kar. ≈ −3.3k token/oturum tabanı → 1.25 yazım + 16 adım × 0.1 okuma ≈ −9k ağırlıklı/oturum (köprü + ajan_sira oturumları). Gerçek API ölçümü d2'de.
- Kalite riski: gizlenen plugin ajanları yalnız köprü/ajan_sira ajan profilinde gizli (CC_PROFIL_ZORLA=tam geri alır); omer-skills iş akışlarının kullandığı proje ajanları (okuyucu, suite-kosucu, video-tarayici, aday-arastirici) ve yerleşikler listede kalıyor.
