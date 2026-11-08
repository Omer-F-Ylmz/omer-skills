---
type: report
status: done
tags: [strix, guvenlik, f1]
relatedTo: [docs/kurulumlar/strix.md]
---
# STRIX-2 (28 Eki)

Hedef: parfum-desktop statik sitesi (yerel `http.server`, :4180). Model: openrouter/nvidia/nemotron-3-ultra-550b-a55b:free. Kip: `strix -m quick`.
Betik: `tools/strix_deneme2.py` (Docker aç, RAM bekçisi, çıktı günlüğe akar). Günlük: `.kos/kopru/arka/strix2-strix.log`.

RAM: başlangıç %98, 09:52'de %85'e inince başladı (28 dk bekleme); strix 10:19'a dek koştu, çıkış 2 (bulgu var), "Penetration test completed".
Jeton: giriş 16,3M (önbellekli 14,2M), çıkış 30,5K.

## Sayılar
kritik 0 · yüksek 0 · orta 2 (toplam 2)

## Bulgular
1. vuln-0001 MEDIUM (CVSS 5.3, CWE-548): dizin listeleme açık (/vendor/, /vendor/three/, /vendor/gsap/, /vendor/lenis/, /js/, /docs/).
2. vuln-0002 MEDIUM (CVSS 5.3, CWE-693): güvenlik başlıkları yok.

İkisi de Python `http.server` yerel test sunucusunun doğası; site statik, canlı dağıtımda barındırıcı başlıkları ayarlanır. Düzeltme çabası düşük.

Çıktı: `strix_runs/host-docker-internal-4180_a261/` (rapor `penetration_test_report.md`, `vulnerabilities.csv`, `findings.sarif`).

## Kapanış
- STRIX sandbox konteyneri: strix kendisi kaldırdı, `docker ps -a` yalnız clodfarm gösteriyor; silinecek konteyner yoktu.
- `python tools/clodfarm_ac.py`: tamam, clodfarm Started (1021 MiB).
