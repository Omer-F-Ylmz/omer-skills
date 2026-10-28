# TARA-KOD-1
- Kuruldu: tools/envanter_tara.py (aşama 1), tools/altin_ornek.py (kaydet/olc), skills/envanter-tara, arka_ajan.py görev kancası, dist/yukle-28eki-4/envanter-tara.zip (zip_denetle TEMİZ, açılıp çalıştı), 2 test yeşil.
- Sapma: zincir cm.py/code-mode MCP ile DEĞİL, tek Python süreci (alt süreçler) — ara sonuçlar aynı şekilde bağlama girmez. xerj PATH'te yok, atlanır. "katalog.tsv" yok; gerçek kaynak docs/katalog/yetenek.*.
- Recall (5 iş, altın seçimi ben kataloğu tarayarak yaptım, 53 araç): ilk sürüm %60,4 → aile/departman girişleri + satır başı grup payı sonrası %100. UYARI: ayar ve ölçüm aynı 5 işte (iyimser). Dışarıdan 3 iş (8 araç): %88,9 (kaçan: impeccable → çok yönlülere eklendi).
- Token/iş: eski yol (katalog_ara + kombin + envanter + kaynak ham okuma) ≈13,4k; yeni ≈2,3k + plan. Tahmin (bayt/4), gerçek model ölçümü yok.
- Önbellek: ilk koşu ≈20–25 sn (graphify yavaş), önbellekli 0,09 sn; yeni altın örnek önbelleği geçersiz kılar.
- Altın örnekler .kos/kopru/altin-ornek/ornekler.jsonl (5 kayıt); sonraki tarama bunlardan öğrenir, kaçıranlar beyne ders yazar.
