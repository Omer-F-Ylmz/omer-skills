# jev CLI (tools/jev, `uv tool install -e tools/jev`)
Context dışı yargıç: yol verilir, ≤25 satır tablo döner. Ortak: `--model jev-1.13|jev-latest` (varsayılan pinli 1.13) · `--en-fazla N` (batch tavanı, varsayılan 5) · `--istek-tavan M` (HTTP isteği, tekrarlar dahil, varsayılan 250) · `--json` (satırlar + `cagri: {batch, istek}`). Tablonun altında iki sayı da yazar.
Anahtar sırası TYPESAFE_API_KEY → OPENROUTER_API_KEY → JEV_MCP_TOKEN; hiçbiri yoksa exit 2. State'ler TR redaksiyonundan geçer.

- `jev log test.trx --diff src/A.cs,src/B.cs` → test · sınıf {regresyon, flaky, ortam-kurulum, derleme, test-kendisi} · bant · diff ilgili p
- `jev ilgili "kargo ücreti nerede hesaplanıyor" src/Kargo.cs src/Siparis.cs -k 5` → yol:a-b · alaka (0-3) · bant
- `jev kanit docs/rapor.md test-cikti.txt` → desteklenmeyen/Escalate iddialar: satır · iddia · destek p · bant
- `jev kanit`: ~28k token üstü kanıt parçalanır, iddia başına p = parçalar arası max.
- `jev triage gitleaks.json` → kural · dosya:satır · sınıf {güvenlik, kalite, yanlış-alarm} · gerçek p · önem · bant
- `jev tarama adaylar.json` → aday · çift p · izin riski · bakım · yıldız · puan (eleme yok)
- `jev kalibre [--bant-yaz]` → docs/jev-kalibre.md; öneri yalnız raporda, `--bant-yaz` ile bantlar.json'a max(öneri, 0.85/0.60) (ücretli, 2 batch; köprüde kapalı)
