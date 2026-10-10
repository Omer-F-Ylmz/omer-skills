# Kurulum turu 5 (2026-10-10)

Kaynak: `kacan-adaylar.md` "Tur 5 adayları" (103 aday). Ayrıntı: `tur5-sonuc.tsv`. Betik: `tools/kurulum-turu-5.sh` (VERI boş, `--kuru` ve gerçek koşu 0 hata; log `.kos/kurulum-5/`, tam SHA `.kos/kurulum-5/kurtarma.json`).

## Sayılar
KUR 0 · ZATEN 6 · HESAP 22 · ÖNERİLMEZ 4 · AYRI-UYGULAMA 16 (i web 14 · ii 2) · RED 55 (gürültü 34 · bulunamadı 12 · lisans 6 · kapsam 3). Toplam 103.

## Kurulan
Yok. Skill/plugin içeren aday çıkmadı; yeni bir şey kopyalanmadı, `claude plugin list` ve ~/.claude/skills değişmedi.

## ZATEN
addyosmani/agent-skills (OCR "skillsl", plugin agent-skills) · DietrichGebert/ponytail (OCR "ponytall", plugin ponytail) · context7 (MCP+skill) · vantajs.com ve tengbao/vanta (skill vantajs) · developers.hostinger.com (hostinger MCP, deploy-app).

## ÖNERİLMEZ
- guillaumemeyer/watermarks-remover (+2 OCR yazımı, MIT, c5297e9e6972): AI metin filigranı ve C2PA/köken metadatasını siler, yani tespit atlatma. Video: ig-Dctk1TiK2KP.
- Andy00L/sharetopus: otomatik çoklu sosyal medya paylaşımı, lisans da yok.

## HESAP (hesaplar.md adayı)
Pixellab (4 satır), Stable Audio / Stability platform (3), Tripo3D (3), Higgsfield MCP (4 OCR yazımı → mcp.higgsfield.ai), Vanta, Strikingly, Cloudinary, PagerDuty, Cal.com, hostingdunyam (2), use.app. Hiçbirinde skill yok; hesap/API anahtarı ister.

## AYRI-UYGULAMA
i web: hazelengine, polyhaven docs, sketchfab ×2, freecodecamp, ibisworld, mordorintelligence, garrethbotha, gionatannese, graffico, revelatio, insforge, codercup, delta.dev. ii: zed.dev (editör), gpui.rs (Rust UI kütüphanesi). Kurulmaz.

## RED
Lisans yok: TeamDynamics, Timeora, CinePurr, creator-skill-generator, build-your-own-x, public-apis. Kapsam (SKILL.md yok): PolyDub, mantiz, StudioCherno/Coral. Bulunamadı (404): 12 satır (Qwen3.8/radixark model adları dahil). Gürültü: 34 satır (hız etiketleri "1.2k/day", "a4/letter", dosya yolları, kısa OCR kırıkları).
