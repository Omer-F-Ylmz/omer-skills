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

## d2 ara (14 Eki ~18:35) — claude -p 6/6 harcandı
- K10 ölçüm (onek_kayit.py üst port 6769→6767; ajan profili, aynı istem, arka arkaya 2 oturum; 1. istek):
  - b (plugin deny + includeGitInstructions:false): koşu1 cw 22609 cr 0 · koşu2 cw 11318 cr 10940 (%49). Tek fark msg1.0 kar. 21321: ECC "önceki oturum özeti" — koşu 1'in kendi oturum sonu kancası yeniden yazıyor.
  - c (+ ECC_SESSION_START_CONTEXT=off): koşu1 cw 20763 cr 0 · **koşu2 cw 0 cr 20763 (%100, hedef ≥%80)**. Ağırlıklı 1. istek: d1 ~30.7k → aynı istemli 2. oturum 2.1k (−%93; K13 ölçüm koşuları bunu alır).
  - İçerik (kar., a→c): msg1 39477→24506 (ajan listesi 50→12: 38 plugin ajanı; ECC özeti yok), git durumu 3951→0, araçlar 99743→99352 (Bash'teki 4 satırlık "# Git" bölümü), toplam blok içeriği 159.5k→140.2k (−%12). Farklı istemli oturumlarda kazanç yalnız bu boyut düşüşü (önek msg0 istemi yüzünden araç+system'de kırılır).
- UYGULANDI (yerel profil, global ayar değil): profiller/cc-arka.json "ajan".ayar = {includeGitInstructions:false, env.ECC_SESSION_START_CONTEXT:off}; cc_profil.py (env çağıranınkiyle birleşir, çağıran kazanır) + sunucu.mjs ajanAyarYolu aynı ayarı --settings dosyasına yazar. Test: pytest test_cc_profil 19/19 (yeni: ayar birleşimi), node ajan-argv 12/12.
- Kalite kapısı (0 API, yakalanan gövdeden): 5 proje ajanı (okuyucu, suite-kosucu, video-tarayici(-haiku), aday-arastirici) + ajanTut 2 + yerleşikler listede; claude-mem bağlamı duruyor; atıf satırları (msg0.1) duruyor. Gerçek iş çıktısı kapısı claude -p kalmadığı için KOŞMADI. Risk: Bash'teki "# Git" satırları (commit yalnız istenince, varsayılan dalda dal aç, atıf satırı) köprü oturumlarında yok — köprü görevleri commit'i kendi tarif eder; CC_PROFIL_ZORLA=tam geri alır.
- K10 global öneri: claude-mem "recent context, <saat:dakika>" damgası dakikada bir kayar (aynı dakikadaki iki koşuda fark yoktu); global kanca/eklenti değişikliği gerektirir → yalnız öneri, uygulanmadı.
- K11 UYGULANDI: ajan-sira.tsv isteğe bağlı 4. sütun `efor=medium|high` → `--effort` (geçersiz değer ValueError); efor verilince CLAUDE_CODE_EFFORT_LEVEL alt süreçten çıkarılır (KÖPRÜ-EFFORT-1 ile aynı). tests/test_ajan_sira.py 3/3; canlı kuyruk 28 satır değişmeden ayrışıyor. Kalite: K9 kanıtı (medium mekanik adımda geçti); yeni örnek kapı claude -p kalmadığı için KOŞMADI.
