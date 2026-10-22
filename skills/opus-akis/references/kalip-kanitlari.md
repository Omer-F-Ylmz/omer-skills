# Kalıp kanıtları (Opus kuyruk oturumları, damıtma: tools/akis_damit.py, ücretsiz model; her madde transkript satırıyla doğrulandı)

Oturumlar: telve-v2-faz1b-b (0eaa1c34), neffex-klon-4-b (e9f4af2a), bhs5-d0 (df9478f2). Ham kayıt: .kos/kopru/akis/kaliplar.jsonl (satır no + birebir alıntı).

| Çekirdek adımı | Oturum kanıtı (L = izlenen satır) |
|---|---|
| 1 Sınıfla → envanter | 0eaa L1 "iş türünü tek kelimeyle sınıfla"; 0eaa L2 `git status -sb && git log --oneline -5`; df94 L1, L8 hazır çıktıları ve görev dosyasını denetle |
| 2 Küçük adım + kanıt | 0eaa L71 `npm test … grep "# (tests\|pass\|fail)"` (geçen/kalan sayısı); e9f4 L33 SSIM ölçümü her adımda; df94 L37 üretilen görseli okuyup kanıt topla |
| 3 Hata sonrası | 0eaa L86 yalıtımlı koşu düştü → aynı araç seçenek kaldırılarak yeniden; df94 L77 hatalı çağrı düzeltilip zaman sınırıyla yeniden; df94 L55 otomasyondan önce çalışma zamanı durumu betikle doğrulandı |
| 4 DUR | 0eaa L122 "Görsel hakem kabulü karşılanmadı" → değişiklik yapmadan gerekçeyle bildir; e9f4 L168 SSIM 0.40 < 0.6 hedef, görsel puan 4/10 → durdur, hata analizi |
| 5 Kapsam/biçim | e9f4 L1 önsöz ayarlarına uyum; ön söz ve görev dosyası dışına çıkılmadı |

Ek ilke (fixing-smartass-opus-5, MIT): en önemli bilgi başta · her olgu bir kez · kanıtsız tamamlandı iddiası yok · yanlış varsayım nedeniyle reddedilir.
Ek ilke (fable-advisor, MIT): teslimden önce bağımsız gözle diff + doğrulama komutu yeniden · boş diff başarı sayılmaz · iki başarısız denemede yöntem/model değişir.
