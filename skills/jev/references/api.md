# Jev API tel biçimi

Kaynak: https://docs.typesafe.ai/api · https://docs.typesafe.ai/models · https://openrouter.ai/docs/guides/community/typesafe-sdk

## Uç noktalar (ikisi de `POST .../v1/systemone`, `Authorization: Bearer <anahtar>`)
| Backend | URL | Anahtar |
|---|---|---|
| TypeSafe | `https://api.typesafe.ai/v1/systemone` | `TYPESAFE_API_KEY` |
| OpenRouter | `https://openrouter.ai/api/v1/systemone` | `OPENROUTER_API_KEY` |

OpenRouter çıplak adları eşler: `jev-1.13` → `typesafe/jev-1.13`, `jev-latest` → `~typesafe/jev-latest`. Yanıttaki `model` OpenRouter kimliğidir (ör. `typesafe/jev-1.13-20260917`); OpenRouter ayrıca `id`, `provider`, `usage.cost` ekler. SDK'nın `models.list()` çağrısı OpenRouter'da çalışmaz.

## İstek
```json
{
  "model": "jev-latest",
  "state": "Help! My payouts are failing.",
  "questions": {
    "is_urgent": { "type": "noul", "instructions": "Does this convey urgency?", "criteria": { "true": "Explicitly time-sensitive", "false": "No urgency" } },
    "department": { "type": "choice", "instructions": "Which team should handle this?", "criteria": { "billing": "payments, refunds", "technical": null } },
    "frustration": { "type": "score", "instructions": "How frustrated is the customer?", "criteria": ["Calm", "Frustrated", "Very angry"] }
  }
}
```
`state`: string | object | array. `instructions`: string | object | array (zorunlu). `criteria`: noul için isteğe bağlı `{true,false}`; choice için seçenek haritası (≤255); score için seviye dizisi (2-10).

## Yanıt
```json
{
  "model": "jev-1.13.0",
  "answers": {
    "is_urgent": { "type": "noul", "noul": 0.95 },
    "department": { "type": "choice", "choice": "billing", "probabilities": { "billing": 0.88, "technical": 0.12 }, "confidence": 0.81 },
    "frustration": { "type": "score", "score": 1.05, "legend": { "0": "Calm", "1": "Frustrated", "2": "Very angry" }, "probabilities": { "0": 0.0, "1": 0.95, "2": 0.05 }, "confidence": 0.92 }
  },
  "usage": { "input_tokens": 304, "output_tokens": 18 }
}
```

## Sınırlar (Jev 1.13)
- Bağlam: istek başına 64k token; `state` + en uzun soru 32k.
- Hız: 250.000 token/sn · 1.200 istek/dk (dinamik, değişebilir).
- Ücret: girdi $0.042 / M token; çıktı ücretsiz.
- Girdi yalnız metin (string, JSON nesnesi, metin dizisi).

## Hatalar
`401` anahtar · `422` doğrulama (gövde alanı gösterir) · `429` hız sınırı · `529` aşırı yük. 408/429/5xx üstel geri çekilme + `retry-after` ile tekrar (SDK varsayılanı: en fazla 2 tekrar).
