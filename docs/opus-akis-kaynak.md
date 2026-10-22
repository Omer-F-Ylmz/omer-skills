# opus-akis kaynakları (AJAN-AKIS-1, 22 Eki 2026)

Mekanizma alındı, kod kopyası yok. İndirme: .kos/kopru/indir/opus-akis/ (gitignore).

| Kaynak | Lisans | Ne yapıyor | fable-dusunme ile fark → karar |
|---|---|---|---|
| disler/fixing-smartass-opus-5 | MIT | Tek sistem istemi Opus 5'in "yük taşıyan bilmiş" üslubunu kısa, kanıtlı, kapsam aşmayan mühendis ortağa çevirir (sonuç başta, olgu bir kez, kanıtsız tamamlandı yok, yanlış varsayımı reddet) | fable-dusunme düşünme sırası verir, üslup/kapsam disiplini yoktu → ÖĞREN: "kapsamı aşma, sonucu başa koy, yanlış varsayımı gerekçeyle düzelt" çekirdeğe girdi |
| DannyMac180/fable-advisor | MIT | Orkestrasyon: şartname (arayüz, kısıt, doğrulama komutu), adım başı model/efor etiketi, uygulama sonrası diff + komut yeniden, boş diff başarı değil, teslimden önce danışman incelemesi, 2 başarısız denemede danış | fable-dusunme'de bağımsız doğrulama yoktu → UYARLA: "teslimden önce diff + doğrulama komutunu yeniden koş", "2 başarısız denemede yöntem değiştir" |
| mrtooher/fable-mode | lisans YOK (GitHub licenseInfo=null) | Fable tarzı çok aşamalı plan + alt ajan devri + öz-doğrulama | Lisans kapısı: içeriği okunmadı, mekanizma alınmadı → ATLANDI (lisans eklenirse yeniden değerlendir) |
| MoreThought/Fable-5.1-Max-Reasoning-* | GitHub'da yok; HF veri kümesi (10k ajan izi, ~500M jeton) | Eğitim verisi, skill değil | Çekirdek için fazla büyük, lisansı HF kartında doğrulanmadı → ATLANDI |
| ahmdd4vd/Fable5res | "Other" (belirsiz) | 4665 CoT izinden damıtılmış düşünme skill'i | Lisans MIT/Apache değil → ATLANDI |

Kendi kaynağımız (asıl veri): 3 başarılı Opus kuyruk oturumu (telve-v2-faz1b-b, neffex-klon-4-b, bhs5-d0) → tools/akis_damit.py ile 17 kalıp damıtıldı, hepsi transkript satırı + birebir alıntıyla doğrulandı (references/kalip-kanitlari.md). Önceki egitim-1 analizi (160 Opus oturumu: %91 doğrulama komutu koşar) çekirdeğin 2. adımını destekler.
