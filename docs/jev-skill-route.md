# Jev skill yönlendirme A/B (2026-09-23, jev-1.13)

Veri `skill_route.jsonl`: 20 sentetik istem, her birine 1-3 kabul edilebilir altın skill. hit@k enjekte edilecek listede ölçülür (p ≥ act, p'ye göre sıralı).

| ölçü | değer |
|---|---|
| istem | 20 |
| aday (aktif skill) | 347 |
| aşama-1 isabeti (altın ∈ ilk 10) | 1.00 |
| hit@1 | 0.45 |
| hit@3 | 0.85 |
| gecikme p50 / p95 (sn) | 0.91 / 1.12 |
| istem başına girdi token (ort.) | 20699 |
| istem başına maliyet (ort.) | $0.00087 |
| günlük üst sınır (200 istem × ort.) | $0.17 |
| HTTP isteği | 40 |

Karar kuralı: hit@3 ≥ 0.80 VE p95 ≤ 1.8 sn VE günlük üst sınır ≤ $0.50.

**JEV_SKILL_HOOK=1 önerilir.**

Kayıt (`~/.claude/settings.json` → `hooks.UserPromptSubmit`); CC hook komutları Windows'ta bash ile koşar, yolda / kullan:

```json
{"hooks": [{"type": "command", "timeout": 3,
  "command": "powershell -NoProfile -ExecutionPolicy Bypass -File C:/Users/pc/.claude/hooks/jev-skill.ps1"}]}
```
