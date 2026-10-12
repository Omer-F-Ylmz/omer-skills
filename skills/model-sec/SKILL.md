---
name: model-sec
description: "Betikte claude -p çağrısı kurulurken: modeli düşürmeden bağlamı yalınlaştırır, effort'u iş sınıfına göre seçer, başarısızlıkta bir üst kademeye çıkar."
---

# model-sec — kaliteyi koruyan claude -p yönlendirmesi

Model düşürmek tasarruf yolu değildir. Tasarruf, her oturuma yüklenen sabit bağlamdan gelir (CLAUDE.md, skill listesi,
SessionStart hook enjeksiyonları, MCP araç şemaları). Kaliteyi effort korur.

## 1. Sınıfı seç
| Sınıf | İş | Başlangıç effort |
|---|---|---|
| mekanik | sınıflandırma, alan çıkarımı, biçim dönüşümü; tek doğru yanıt | low |
| ozet | özet, dönüşüm; içerik korunmalı | medium |
| yargi | rubrik puanı, karşılaştırma, hata bulma, tasarım kararı | high |
| ajan | dosya okur/yazar, araç gerekir | medium |

## 2. Bayraklar (model çağıranın modeli; değişmez)
- Araçsız sınıflar: `--model <M> --effort <E> --safe-mode --tools "" --strict-mcp-config --disable-slash-commands --no-session-persistence`
- ajan: `--model <M> --effort <E> --setting-sources "" --tools <liste> --allowedTools <liste> --strict-mcp-config --disable-slash-commands --no-session-persistence`;
  MCP gerekiyorsa yalnız istemde adı geçen sunucular `--mcp-config` ile verilir.
- Her çağrıya `--output-format json` ve `--max-budget-usd <tavan>`; stdout ile stderr'i ayrı tut (SessionEnd hook uyarıları JSON'u bozar).

## 3. Geri düşüş
Çıktı deterministik denetimden geçmezse aynı istemi bir üst kademeyle tekrarla: effort low→medium→high→xhigh, xhigh'tan sonra
`--model opus`. Kademe hiçbir zaman aşağı inmez. Tekrar sayısı için tavan koy (ör. en çok 2).

## 4. Ne zaman kullanılmaz
Davranışı ölçülen gerçek oturumlar (skill/hook/ajan A/B ölçümü): yalınlaştırma ölçülen şeyi siler.

Ölçüm (ROUTER-1, 12 Eki): bkz. omer-skills `docs/router-1/olcum.md`.
