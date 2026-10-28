# OMNI-AYIR-DUZELT (10:26)
- Onceki: ozet kor hakem 78/84 (%92,9), kapi %98. Hata deseni: madde 3-4 (gereksinim/lisans) bilgi varken "README'de yok"; ayrica bos/parca maddeler ("2) README'de" gibi). Yanlis ornekler: O00,O02,O04,O07,O23,O24.
- Kok neden: istem/sema "yok" kosulunu ve madde butunlugunu zorlamiyor; dogrulayici yalniz alinti denetliyor.
- Duzeltme (tools/ucuz_alt.py): SEMA.ozet aciklamasi (her madde tam cumle, yok yalniz ipucu yoksa) + ozet dogrulayici (madde <15 kar = RET; madde 3/4 "yok" ama baglamda requirements/lisans ipucu = RET -> sonraki ucretsiz model) + SURUM v4 (onbellek bust).
- Sonra: OLCULEMEDI. Held-out kosusu (.kos/kopru/omni-ayir/duzelt_olc.py, ucretsiz hakem) cok yavas: 1/12 tamamlandi (4/4 DOGRU, cloudflare llama-3.3-70b).
- Sonuc: %98 KANITLANMADI -> ENGEL (tur siniri, ucretli yok). Sonraki: duzelt_olc.py 'once 3 12' arka planda, kalem suresi hata ayiklansin, sonra 24 kalemlik held-out.
- Risk: v4 dogrulayici diger ozet cagrilarinda RET (Claude'a donus) artirabilir; dogrulanmadi.
