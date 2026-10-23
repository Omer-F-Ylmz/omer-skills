# video-kurgu (DcNOMyTCXmO)

**Amaç:** AI ile video içindeki hareketleri 3D karakter animasyonuna dönüştürme.
**Araçlar:** Blender 5.1+, CUDA, ~8GB VRAM, Mixamo LLM Mocap (squall01337/mixamo-llm-mocap), GVHMR (SMPL-X mesh recovery), Python scriptleri (estimate_pose_gvhmr.py, analyze_landmarks.py, lift_to_mixamo.py, apply_mixamo_fk.py, run_in_blender.py, render_preview.py)

**Adımlar**
1. [] Locked camera ile çekilmiş video plate hazırlama (T-pose ile başlangıç ve bitiş).
2. [] GVHMR ile video içindeki hareketleri 3D mesh olarak tahmin etme.
3. [] Hareketleri sayısal olarak ayıklama ve zamanlama verisi oluşturma.
4. [] Tahmin edilen hareket verilerini JSON formatında kaydetme.
5. [] Hareket verilerini Mixamo karakterine uygun formatta dönüştürme.
6. [] Mixamo karakterine FK animasyonunu uygulama ve ayak yerleştirme ayarlama.
7. [] Animasyonu video ile frame-by-frame karşılaştırma ve kalite kontrolü.
8. [] İki karakterli plate varsa, ayrı ayrı işlemler ve birleştirme (setup_duo.py).
9. [] Blender'de gerçek mesh ile çarpışma testleri ve animasyon uygulama.
10. [] Sonuçları önizleme ve side-by-side gösterim hazırlama.

**Prompt/kod/ayar:** Mixamo LLM Mocap (squall01337/mixamo-llm-mocap) + Blender 5.1+ + CUDA
**Sonuç:** AI ile video içindeki hareketleri 3D karakter animasyonuna dönüştürme (Mixamo karakterleri için).
**Bizde (öneri, modelden):** kurulu araçlarla nasıl: Blender + Python scriptleri ile aynı adımlar takip edilebilir, ancak AI tabanlı otomatik retargeting için Mixamo LLM Mocap gereklidir.
**Daha iyi (öneri):** AI agenti ile end-to-end otomatikleştirme (insan müdahalesi olmadan).
