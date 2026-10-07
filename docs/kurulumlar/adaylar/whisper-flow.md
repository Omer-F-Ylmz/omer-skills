# whisper-flow
ad: whisper-flow
tur: CLI
video: l_WQx_XUsRY
repo: yok
lisans: yok
son_commit: yok
arsiv: hayır
kaynak: yok
telemetri: açık
arastirma: tam
## Ne
Wispr Flow: kapalı kaynak, bulut tabanlı sesle yazdırma uygulaması (Windows/Mac). Videoda yazar prompt'u sesle yazdırmak için kullanıyor; "whisper flow" yazımı aslında Wispr Flow. Aday kod/CLI değil, GUI uygulaması.
## Kanıt
- ön getirme: .kos/l_WQx_XUsRY/whisper-flow/on.md
- repo yok (kapalı kaynak, lisans: yok = ticari); yıldız/son commit yok; SkillSpector: koşmadı (on.md), skill değil
- Karıştırma: dimastatz/whisper-flow (PyPI whisperflow) ayrı bir akış-transkripsiyon kütüphanesi; videodaki araç değil
## Kurulum
- Resmi winget paketi bulunamadı; kurulum wisprflow.ai indirici (betik/URL yasak) → Kurulum boş, elle. Yerel açık kaynak alternatif: Handy (winget cjpais.Handy), ayrı aday olarak değerlendirilmeli.
## İzinler
Mikrofon, klavye girişi enjeksiyonu, açılışta otomatik başlama (ilk açılışta onaysız). Ses her zaman buluta gider (çevrimdışı mod yok), AWS ABD. Serbest kurulum: indirici .exe, kullanıcı hesabı düzeyi; Kurulum satırı yok.
## Duman testi
- komut: yok (GUI uygulaması, CLI yok)
## Geri alma
Windows Ayarlar > Uygulamalar'dan kaldır; kullanıcı verisi kalır, hesap silme bulut geçmişini otomatik silmez (destek gerekir).
## Köprü izni
- arac: yok
## Önerilen katman
RED (gerekçe: kapalı kaynak GUI, otomatik kurulum yok, ses buluta gider; T2 olarak elle kurulabilir ama köprü/CLI yüzeyi yok)
## Telemetri kapatma
- Uygulama: Settings > Data and Privacy: model iyileştirme kapalı + Dictation Cloud Storage kapalı (ZDR)
## Özellikler
### sesle-yazdirma
ne: basılı tut-konuş, metin aktif uygulamaya yazılır; otomatik düzenleme, 100+ dil
kurulum: wisprflow.ai indirici, elle
lisans: ticari/kapalı
etiket: -
karar: ALTERNATİF
gerekce: lisans: kapalı kaynak, bulut zorunlu; yerel alternatif Handy / whisper.cpp (MIT) daha uygun
## Bağımsız kanıt
- https://wisprflow.ai/data-controls — transkripsiyon her zaman bulutta, çevrimdışı mod yok
- https://willowvoice.com/blog/wispr-flow-whisper-flow-willow-comparison — Windows sürümü Electron, RAM yükü ve VS Code'da donma raporları (üretici rakibi, düşük güven)
- https://suprflow.app/guides/whisper-flow-vs-wispr-flow-vs-whisper — Wispr Flow, Whisper tabanlı uygulamalardan ayrı, bulut hizmeti
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| yazar prompt'u sesle yazdırıyor ("whisper flow") | on.md altyazı | doğru | aracın adı Wispr Flow | - |
| yerelde çalışır | https://wisprflow.ai/data-controls | yanlış | yalnız bulut | - |
## Kötü yan + onarım + güçlendirme
- güvenlik · ses+transkript buluta gider, eğitimde varsayılan açık (üçüncü taraf denetim) · neden: wisprflow.ai/data-controls · ölçülen · onarım: Data and Privacy'de iki anahtarı kapat (ZDR) · kaynak: https://wisprflow.ai/data-controls
- performans · Electron, RAM yükü, açılışta otomatik başlama · neden: willowvoice karşılaştırması · tahmin · onarım: açılış girişini kapat · kaynak: https://willowvoice.com/blog/wispr-flow-whisper-flow-willow-comparison
güçlendirme: yerel Whisper tabanlı Handy ile ses → Claude Code prompt'u; graphify/departman skill'leriyle ilişkisi yok.
