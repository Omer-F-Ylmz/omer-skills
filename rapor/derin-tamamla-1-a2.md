DERIN-TAMAMLA-1-a2 (yarim-tara-27eki: DUR, 2 devam turu sonrasi hala eksik)
Komut: python -I ile .kos/kopru/derin-liste.txt (1945 link) vs docs/video-tarama/derin/<kod>.json varligi.
Sonuc: 897 link icin derin json hic yok (1048 var). Log son satirlari: link basina 323-756 sn (OCR agirlikli, GPU).
Tahmin: 897 x ~8 dk = ~120 saat GPU; olum-teshis-1 GPU/TDR suphesiyle (LiveKernelEvent 141) ayni hat coker.
Karar: ENGEL. Tek oturumda bitmez, GPU kararlilik teshisi (olum-teshis-1) cozulmeden toplu_gozetmen.py yeniden baslatilmadi.
Onerilen: nvidia-smi kaydi acikken tools/toplu_gozetmen.py ile gece kosusu, <4 dk parca.
