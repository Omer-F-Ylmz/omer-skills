# Harness audit (ECC içinde)
ad: Harness audit (ECC içinde)
tur: skill
video: rABIViSQmsc
repo: affaan-m/ecc
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/affaan-m/ECC
telemetri: Denetim betiği yerel çalışır. Telemetri gönderdiği belgelenmiş değil, kodu incelemedim: bilinmiyor. ECC'nin ayrı bir GitHub App'i ve Pro katmanı var, ama o ayrı bir servis.
yildiz: bilinmiyor
alt_tur: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Everything Claude Code (ECC) paketindeki /harness-audit komutu. Bir deponun ajan kullanımına (korkuluklar, hook, skill, komut, ajan yapılandırması) hazır olup olmadığını denetler. 7 kategoride puan, bulgular, başarısız kontroller ve ilk 3 aksiyonu içeren öncelikli bir karne üretir.
## Mekanizma
Komut, deterministik bir Node betiğini çalıştırır: `node scripts/harness-audit.js <kapsam> --format <text/json> [--root yol]`. Kapsam repo, hooks, skills, commands veya agents olabilir. Puanlama ve kontroller betikten gelir. Komut tanımı modelin ek boyut ya da keyfi puan uydurmasını yasaklar. Çıktıda toplam puan, uygulanabilir kategoriler, dosya yoluyla başarısız kontroller, ilk 3 aksiyon ve sonraki adımda uygulanacak ECC skill önerileri bulunur. Bu bilgiler arama sonuçlarındaki komut açıklamasına dayanır. Betik kodunu okumadım.
## Kanıt
- Depodaki zayıf korkulukları denetler, depoyu puanlar ve düzeltmeleri önceliklendirir → doğrulandı · Arama sonucundaki commands/harness-audit.md açıklaması: 7 kategori puanı, bulgular, başarısız kontroller ve ilk 3 aksiyon. Video karesi de 'Audit first: Find weak guardrails, Score the repo, Prioritize fixes' diyor.
- Puanlama deterministik bir betikten gelir → sınanamadı · Komut açıklaması betiği doğruluk kaynağı olarak gösteriyor. Betiği çalıştırmadım ve kodunu okumadım.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code'da ECC eklentisini kur: `ecc@ecc` (README'deki yönlendirmeli kurulum ya da yerel eklenti komutları)
- Alternatif olarak npm paketi `ecc-universal`
- Çalıştır: `/harness-audit . --format text`
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajan döngüsüne güvenmeden önce zayıf korkulukları görünür kılar. Tekrarlanabilir, sayısal bir hazırlık puanı ve öncelikli düzeltme listesi verir.
## Maliyet/risk
Bağımsız bir araç değil, büyük ECC paketinin parçası. Tam kurulum çok sayıda hook, skill ve kural ekler. README, tam manuel kurulumun eklentinin üstüne yığılmamasını uyarıyor. Kontroller ECC'nin kendi konvansiyonlarına göre ölçülmüş olabilir ve başka depolarda ilgisiz puan kırabilir. Üçüncü taraf kopyalara karşı uyarı var, yalnızca resmi kaynaklardan kur.
## Tasarruf
Token aracı değil. Deterministik betik puanı hesapladığı için model analizinin token maliyeti dolaylı olarak azalır, ama bu belgelenmiş bir tasarruf iddiası değil.
## Üretilebilir
hedef_tur: skill
tarif: Bir 'harness-audit' skill'i yaz. İçine küçük bir Node ya da Python betiği koy. Betik depoda şunları kontrol eder: CLAUDE.md/AGENTS.md var mı, .claude/settings.json içinde izin ve hook tanımları, secret tarama (gitleaks gibi) yapılandırması, test ve lint komutları, CI iş akışları, skills/commands/agents dizin yapısı. Her kontrole sabit ağırlık verip kategori bazlı puan hesaplar ve text ya da json çıktı üretir. SKILL.md, modele puanı uydurmamasını, yalnızca betik çıktısını yorumlamasını ve ilk 3 aksiyonu önermesini söyler. Kontrol listesini önce ECC'nin scripts/harness-audit.js dosyasını okuyarak çıkar. Lisans MIT olduğu için kaynak gösterilerek uyarlanabilir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### Deterministik betik tabanlı puanlama (node scripts/harness-audit.js), text ve json çıktı
kaynak: https://github.com/affaan-m/ECC/blob/main/commands/harness-audit.md
### Kapsam seçimi: repo, hooks, skills, commands, agents
kaynak: https://github.com/affaan-m/ECC/blob/main/commands/harness-audit.md
### Başarısız kontrolleri dosya yoluyla listeler, ilk 3 aksiyonu ve önerilen ECC skill'lerini verir
kaynak: https://github.com/affaan-m/ECC/blob/main/commands/harness-audit.md
### MIT lisanslı, ECC eklentisi ecc@ecc ve npm ecc-universal ile dağıtılır
kaynak: https://github.com/affaan-m/ECC
## Destek
- rABIViSQmsc · 0:19 · Kodlama döngüsüne güvenmeden önce depodaki zayıf korkulukları denetleyip puanlayan adım. · kanıt: Karede 'Audit first' başlığı ve terminal görüntüsü var. (karede: Terminal penceresinde '/harness-audit . --format text'; sağda 'Audit first: Find weak guardrails, Score the repo, Prioritize fixes'.)
