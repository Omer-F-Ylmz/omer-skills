YARIM-B1-DEVAM-B: DUR, dersli tekrar kabul (≤1/10) tutmadı; en iyi 2/10 kaçan (dersli 8/10 uygulandı), gevşetilmedi.
- Teşhis (4 sürekli kaçan): bhs5 + kur-eksik-ortam-red: ders bağlamda vardı, model yok saydı (küçük ücretsiz model, gürültülü); slash-satir-ici-skill: model İngilizce yanıtlıyordu, regex Türkçe → istem "Türkçe" eklendi; kok-neden-klasor-yolu: bağlam bütçesi tetik/ders metnini kesiyordu.
- Yapılan (ucuz→pahalı): K 5→3 ders, eylem ("dogru") başa alındı (bütçe kesince kural kalır), c83cde/19f7e7 eyleme dönük yeniden yazıldı, olc yanıt dili Türkçe, olc çıktısına "kacan" listesi.
- Ölçüm (dersli/derssiz uygulanan): 7/2 → 6/1 → 5/3 → 5/2 → 7/4 → 8/2 → 8/3. Koşular arası ±2 dalgalanma: 10 vaka + gürültülü model ≤1/10'u ayırt edemez.
- Yapılmadı: PreToolUse hook ile ihlal yakalama (adım 4; maliyet yüksek), olay aralığı yeniden ölçümü (yönetici yenilenmedi).
- Sonraki: vaka sayısı ≥30 ve her vaka 3 tekrar (çoğunluk) ya da daha güçlü ücretsiz model; sonra adım 4.
Test: test_ders_dongu+test_ders 30 geçti.
