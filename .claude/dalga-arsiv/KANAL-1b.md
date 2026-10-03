# KANAL-1b — etiket onarımı + kanal kimliği
KARAR (onay 3 Eki): tavan 35 araç (30'da commit+push). Model 0. Ölçüm günü: yalnız video motoru kodu/testleri, docs/, .video-cache/, .kos/.
Ömer onayı: kimlik çözme ağ isteği koşar (yalnız -J metadata). Envanter KOŞMAZ.
B1 KUR değerli (kaynak KUR); mutasyon KUR çıkar.
B2 30 bağsız karar: (a) aday dosyası kaynak/video alanı (b) rapor aday/karar bölümü; düz metin yok. >1 video "ortak", >3 "çözülemedi (aşırı eşleşme)". video-dışı etikete girmez.
B3 coz: "?" videolar + kimliksiz kanal başına 1 video; ≥2 sn, 429/403 2 deneme, 3 ardışık hata dur; --tavan 100. meta.json varsa ona; yoksa .kos/kanal/video-kanal.json (.video-cache klasörü AÇILMAZ). Mutasyon bekleme kaldır.
B4 liste dolu Ömer sütununu korur (ad→id anahtar değişiminde de).
_istek ortaklaştırması K2 testleri değişmeden yeşil; kırılırsa kod düzelir, olmazsa DUR.
Kapanış: suit (cc-kopru :25 kırmızıysa süreci tanımla) → gitleaks → arşiv KANAL-1b.md → commit+push → graphify update.
DURUM: kapandı — coz 83+18 istek: 80 video / 38 kanal kimlikli (0 kimliksiz) · canlıda bulunan hata: kayit.jsonl kaynak-*/kurulum-* satırları video sayılıyordu (test b5 + düzeltme) · 38 kanal takip 4 · bir-kez 33 · atla 1 · 123 video değerli 42 / değersiz 81 · B2 video 19 · video-dışı 7 · çözülemedi 1 (headroom-ayar) · suit 6/6 yeşil (cc-kopru 178/178) · gitleaks temiz.
