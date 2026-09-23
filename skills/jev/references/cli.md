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
- `jev skill "<istem>"` → aktif skill'lerden ilk 5 · p · bant (ipucu, karar değil). Aşama 1: ≤210'luk dilim başına choice + `hiçbiri`, tek istek → ≤10 aday. Aşama 2: aday başına noul, tek istek → yalnız p ≥ act. İstem başına tam 2 HTTP isteği.
- `jev skill-olc` → docs/jev-skill-route.md (hit@1/3, p50/p95, istem başına $; ücretli, 40 istek). Hook: `~/.claude/hooks/jev-skill.ps1` (user env JEV_SKILL_HOOK=1, günlük JEV_SKILL_GUNLUK=200; fail-open).
- `jev hook-durum [-n 100]` → `~/.config/jev/hook.log` son N satırı: p50/p95 ms, sonuç dağılımı (öneri · act-yok · sessiz-kapı · sessiz-tavan · zaman-aşımı · hata). Ağ yok. Satırda istem/öneri adı/anahtar yok; 500 satırda döner.

CC hook komutları Windows'ta bash ile koşar, yolda / kullan:

```json
"UserPromptSubmit": [{"hooks": [{"type": "command", "timeout": 3,
  "command": "powershell -NoProfile -ExecutionPolicy Bypass -File C:/Users/pc/.claude/hooks/jev-skill.ps1"}]}]
```
