# Hunyuan3D (F6, 27 Eki) — ücretsiz yol: HF Space

Karar: yerel kurulum yok (VRAM v2 şekil 6 GB / şekil+doku 16 GB, v2.1 toplam 29 GB; model deposu ~75 GB; bu makinede GPU yok/belirsiz, RAM %92). Ücretsiz yol: Hugging Face ZeroGPU Space'leri `tencent/Hunyuan3D-2` ve `tencent/Hunyuan3D-2.1` (gradio, `gradio_client` ile).
Lisans: Tencent Hunyuan Community License; kapsam AB/Birleşik Krallık/Güney Kore hariç dünya, TR dışarıda değil (metin okuması, hukuki görüş değil); >1M aylık kullanıcıda ayrı lisans. Kişisel/iç kullanım etkilenmez. MIT/Apache değil → kullanım koşulu bu.
API uçları: `shape_generation`, `generation_all` (13 girdi; sırayı `Client("tencent/Hunyuan3D-2").view_api()` verir), v2'de `on_export_click`. Kota: anonim küçük, HF_TOKEN artırır (rakam doğrulanmadı).
Çıktı: trimesh → glb/obj; Blender 4.x'te File > Import > glTF 2.0 (yerleşik).
Blender hattı (plan): görsel → Space `generation_all` → glb → `blender-uretim` içe aktar → `tools/blender/lib/dogrula`. YAPILMADI: gerçek çağrı denenmedi (görsel dışarı gönderir, ücretsiz kota); skill değişikliği iki taraf kuralı ister.
