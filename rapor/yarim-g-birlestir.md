# YARIM-G-BIRLESTIR (24.10)

Kaynak: rapor/yarim-tara-1.tsv (334 satır) · .kos/kopru/yarim-plan.md

| Sayım | Adet |
|---|---|
| TSV satırı | 334 |
| Plandaki ad (yarim-a1…yarim-f1 içinde, ad eşleşmesi) | 125 |
| Plan dışı | 209 |
|, ZATEN BİTMİŞ (git log konu satırında BİTTİ/ZATEN; .kos/kopru/yarim-muaf.tsv) | 12 |
|, BEKLEMEDE (TELVE, logo, NEFFEX; Ömer'in kararı) | 24 |
|, Şablon/kural dosyası, iş değil (_sablon, SIRA, DEVAM-KURALI) | 3 |
|, Gruplanan açık iş | 170 |

Gruplar (≤8; her biri .kos/kopru/gorev-yarim-gN.md, ajan-sira.tsv'ye eklendi):

- yarim-g1 Kaynak ve Instagram: 14
- yarim-g2 Beyin, öğrenme ve kanca: 35
- yarim-g3 Araç kurulum ve kapı: 29
- yarim-g4 REA, Laya, CUDA, RAM: 22
- yarim-g5 Blender, usta, site, tasarım: 32
- yarim-g6 Token ve video: 28
- yarim-g7 Devir belgeleri ve kalan: 10

Notlar:
- Sınıflama iki kanıta dayanır: plan ad eşleşmesi (metin, kesin değil) ve git log konu satırı. "RAPOR_YOK" + "BİTTİ" olan işler gruplarda kendi ilk adımında "ZATEN BİTMİŞ" diye doğrulanacak; burada kapatılmadı.
- ajan-sira.tsv satırları yarim-a1 ile aynı koşul (`rea-kur.json::session_id`), efor=high, model=sonnet ile eklendi. Koşulun anlamı bu turda doğrulanmadı; runner gruplara geçmeden önce kontrol edilmeli.
- Çalıştırma yapılmadı; bu tur yalnız birleştirme ve sıraya ekleme.
- Commit yarim-plan.md'ye, başka bir oturumun bekleyen iki satırlık notunu (omer-site, takip-24eki-a2) da dahil etti.
- Push yok.
