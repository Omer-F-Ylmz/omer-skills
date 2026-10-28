OLUM-TESHIS-1-a2 (yarim-tara-27eki: DUR, gorsel_hakem eksik; kok neden kanitlanmadi)
Bulgu (ajan-sira/olum-teshis-1-a2.json): 23.10 07:54:08 WER kaydi LiveKernelEvent kod 141 (GPU surucu TDR sinyali); yg1 device=cuda; ram-olay.log 07:50-08:00 RAM %90, python.exe 1953 MB. Bu cikarim, kanitlanmis neden degil.
Ek adim (yonetici pid olunce arka-istegi yeniden baslatsin): ajan_sira.py pid_canli(pid) (satir 161, 445) + commit f17c0eee/b662a8d2 (YONETICI-OLUM-2/3) ile yapilmis.
Kalan: nvidia-smi sicaklik/bellek gunlugu altinda yeniden uretim; GPU sinirli hat tekrar cokebilir, RAM kapisi %89.
Kural "kok neden kanitlanmadan duzeltme yok": duzeltme (device=cpu/--es dusurme) uygulanmadi. Sonuc: ENGEL (kok neden kanitsiz).
