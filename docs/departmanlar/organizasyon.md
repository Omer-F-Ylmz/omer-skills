# Organizasyon — uygulama yaşam döngüsü

Her iş önce ilgili departmanın müdür skill'ini (`departman-<ad>`) okur; müdür hangi aracın hangi sırayla kullanılacağını söyler.
Araç → departman eşlemesi `envanter.json` (üretilir, `video departman`); elle düzeltme `elle.json` (her zaman kazanır), sonra `elle-desen.json` (ad/`tur:ad` jokeri → departman), sonra önbellek, en son Jev.
Departman kataloğu `docs/departmanlar/<ad>.md`: araç · ne işe yarar · ne zaman · sıradaki adım.

| aşama | departman | müdür | çıktı / kapı |
|---|---|---|---|
| 1. Tasarım | frontend · surec-plan | departman-frontend, departman-surec-plan | DESIGN.md, yön kararı (DUR); spec/plan |
| 2. Yapım | frontend · backend-dotnet · veri-db | departman-frontend, departman-backend-dotnet, departman-veri-db | kırmızı-önce test, iki-pass, screenshot ≤4 tur |
| 3. Test | test-qa | departman-test-qa | suite yeşil, tarayıcıda deneme/e2e, görsel QA, a11y 0 hata |
| 4. Güvenlik | guvenlik | departman-guvenlik | sır taraması temiz, SAST/diff taraması, KVKK uyumu |
| 5. Yayın | surec-inceleme · surec-git-yayin | departman-surec-inceleme, departman-surec-git-yayin | review, commit + push, deploy, canary |
| 6. Kapanış | surec-git-yayin · belge | departman-surec-git-yayin | omer-kurallar:15 altı madde + kapanış raporu |

Her aşamada yan departmanlar: `verimlilik` (token/context, çıktı sıkıştırma), `arastirma-ogrenme` (dokümantasyon, video, kaynak), `surec-ajan-arac` (skill/plugin/hook/MCP geliştirme), `belge` (docx/pptx/pdf/xlsx teslim).

## Kapanış kontrol listesi (omer-kurallar:15)
1. Fonksiyon — gerçek uygulamada uçtan uca (test-qa)
2. Güvenlik — sır taraması + SAST (guvenlik)
3. Bağımlılık — lisans ve açık denetimi (guvenlik)
4. ZAP — çalışan uygulamaya DAST (guvenlik)
5. KVKK — veri işleme sınıflaması (guvenlik)
6. SEO/A11y — metadata + erişilebilirlik (frontend)

## Yeni araç
`video-uygula` katman adımı yeni aracı tek Jev sorusuyla bir departmana yazar (`kayit.jsonl` → `departman`, envanter `kaynak: katman`, katalog yenilenir). Yanlışsa `elle.json`'a `"ad": "departman"` ekle ve `video departman` koş.
