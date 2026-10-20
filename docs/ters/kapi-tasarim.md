# TERS kapısı (d2'de koşulur)

**Set**: 10 held-out hedef, skill yazılırken görülmemiş: 6 site (animasyon/WebGL/scroll/geçiş çeşitleri, açık kaynak ya da kendi repomuz), 2 JS/Electron araç, 2 küçük açık kaynak ikili/.NET (REA kuruluysa; değilse 8 hedef, kapı "kısmi" işaretlenir). Her hedef için elle yazılmış ground truth: 5 mekanizma maddesi (kütüphane+sürüm, zamanlama değeri, vb.) ve bunları kanıtlayan dosya:satır.

**Puan (hedef başına 0–1, üç eşit bileşen)**
1. Mekanizma doğruluğu = ground truth maddelerinden doğru bulunan / 5.
2. Kanıt satırı = nottaki her iddiada alıntının kaynakta birebir bulunması (mekanik: alıntıyı kaynakta ara); bulunan / iddia sayısı.
3. Yeniden kurulum farkı = 1 − min(1, sayısal screenshot farkı oranı); Lighthouse performans farkı ≤10 puan ayrıca raporlanır, puana girmez.

**Kapı**: ortalama ≥0.70 ve hiçbir hedefte kanıt bileşeni <0.5.

**Hakem**: bileşen 1 için iki farklı aileden ücretsiz bulut model (ör. Groq llama + OpenRouter nemotron/gemma) kör puanlar; ayrışırsa o madde 0 sayılır (güvenli taraf). Bileşen 2 ve 3 tamamen mekanik. Claude yalnız son adımda: ayrışan maddeler ve kapı kararı. Yerel model yok, ücretli çağrı yok; bulut çağrı tavanı: en fazla 60.

**Zemin**: skill'siz aynı model, aynı hedef → aynı puanlama; skill fark yaratmıyorsa kapı geçmez.
