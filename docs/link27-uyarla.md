# LINK27 UYARLA planları (F7–F10) — 27 Eki

Kaynak videoların kendi raporu yerelde yok (F7 Deg4e9QjnaY, F8 De6cx6MRxbZ yalnız kimlik; F9/F10 yalnız ek-listesi başlığı). Aşağıdakiler madde başlığından türetilmiş plandır; video içeriği doğrulanmadı. Kod/skill değişikliği YAPILMADI (skill değişikliği iki taraf kuralı ister).

## F7 Metinden 3D oyun varlığı → blender-uretim
- Mevcut: `skills/blender-uretim`, `blender-oturum`, `tools/blender/lib`. Yeni akış: metin → varlık listesi (jev ile sınıfla) → Blender `-b` betiği (bpy, procedural mesh) → `tools/blender/lib/dogrula` → glb.
- İlk adım: blender-uretim SKILL.md'ye "metin→varlık" bölümü + tek örnek (ör. kutu/sandık) ve `tools/blender/lib/dogrula` ile kabul. Önkoşul: video akışını görmek (video-tarama kuyruğuna Deg4e9QjnaY).

## F8 Programatik reels (kinetik altyazı + ses) → reel otomasyon
- Mevcut: `reel-plan`, `reel-taste`, `remotion-*` skill'leri, `calesthio__OpenMontage` klonu. Plan: reel-plan çıktısı (sahne+metin+süre) → Remotion kompozisyonu (kinetik altyazı) → ses (`tts`/ElevenLabs ya da ücretsiz TTS) → render `reel-export`.
- İlk adım: OpenMontage README'sinden reel şablonunu bul, Remotion ile 1 reel smoke. Önkoşul: De6cx6MRxbZ videosu.

## F9 CC Mods
- Oturumlar arası mesaj → Hermes (`tools/hermes_motor.py`); basit iş → Haiku yönlendirmesi zaten `ajan_sira.py`'de (modelsiz satır haiku/medium). Eksik: oturumlar arası mesaj kanalı. Öneri: `.kos/kopru/mesaj/<alici>.jsonl` kuyruğu + Hermes okuyucu; dashboard için `ajan_sira` log + `oturumlar/*.json` (E2) yeterli.
- Bekleyen karar (Ömer): mesaj kanalı yazılsın mı.

## F10 27 ajanlı şirket (Gbrain+Hermes) vs departman-*
- Bizde 13 departman skill'i: arastirma-ogrenme, backend-dotnet, belge, diger, frontend, guvenlik, surec-ajan-arac, surec-git-yayin, surec-inceleme, surec-plan, test-qa, veri-db, verimlilik.
- Karşılaştırma için videonun 27 rol listesi gerekli (yerelde yok). Tipik şirket rolleri içinde bizde karşılığı görünmeyenler (doğrulanmadı): pazarlama/SEO, satış/müşteri, finans/muhasebe, hukuk, İK, ürün yönetimi. Çoğu için skill var (marketing-skills, sales, finance, legal), eksik olan departman müdürü yönlendiricisi.
