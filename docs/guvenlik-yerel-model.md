# Kendi projelerinde güvenlik taraması — kullanım kartı

Kapanış listesi madde 2-4 (sızma testi, bağımlılık, otomatik tarama). Yalnız Ömer'in kendi repoları ve kendi canlı adresleri hedeflenir. Bulguları Claude (Desktop) ya da CC yorumlar; yerel model gerekirse standart bir yerel model özet/rapor için kullanılabilir, tarama araçları modelden bağımsızdır.

## 0. Hazırlık
- Repo kökünde çalış: `cd <proje>`
- strix için Docker Desktop açık olmalı (iş bitince kapat — RAM kuralı).
- Çıktılar: `<proje>\guvenlik\` (git'e girmesin: `.gitignore`'a `guvenlik/` ekle).

## 1. Gizli anahtar (gitleaks 8.30)
```
gitleaks git . --log-opts="--all" --redact -v -r guvenlik\gitleaks-gecmis.json
gitleaks dir . --redact -r guvenlik\gitleaks-agac.json
```
`--redact` değerleri maskeler; rapora değer yazılmaz. Bulgu = anahtarı sağlayıcıda yenile (Ömer), geçmiş temizliği git-filter-repo (Ömer onayı).

## 2. Statik kod (semgrep)
```
set PYTHONUTF8=1
semgrep scan --metrics=off --config p/default --config p/secrets --config p/owasp-top-ten --error --json -o guvenlik\semgrep.json .
```
`--config auto` metrics kapalıyken çalışmaz. Çok bulgu varsa `jev triage guvenlik\semgrep.json`.
.NET projede `--config p/csharp`, JS/TS'de `--config p/javascript --config p/typescript` ekle.

## 3. Bağımlılıklar
```
dotnet list package --vulnerable --include-transitive
npm.cmd audit --omit=dev
uvx pip-audit -r requirements.txt
```

## 4. Dinamik tarama (OWASP ZAP, Docker)
```
docker run --rm -v %CD%\guvenlik:/zap/wrk -t zaproxy/zap-stable zap-baseline.py -t https://<kendi-adresin> -r zap.html
```
Baseline pasif taramadır; aktif tarama için `zap-full-scan.py` (yalnız kendi sitende, trafiği artırır). Yerel ZAP kurulumu bu makinede bulunamadı (3 Kas kontrol), Docker yolu kullanılır.
Yalnız kendi sitelerin (ör. garajim.runasp.net, Vercel "omer" takımı projeleri) ya da `localhost`.

## 5. Ajanlı sızma testi (strix)
```
set STRIX_LLM=<sağlayıcı/model>
set LLM_API_KEY=<ortamdaki anahtar>
strix --target .
strix --target https://<kendi-adresin>
```
Bayraklar sürüme göre değişir: önce `strix --help`. Hedef yalnız kendi projen.

## 6. Yorum ve kapanış
- Raporları Claude'a ver: "guvenlik\ altındaki raporları önem sırasına göre özetle, her bulgu için düzeltme öner".
- Her bulgu: risk (canlı / geçmişte / yerel) · dosya:satır · düzeltme · kim yapar.
- Düzeltmeden sonra 1-5 yeniden koşulur; sıfır yüksek/kritik bulgu = madde 2-4 geçti.
