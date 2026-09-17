# Çıktı ve effort notları · 2026-09-17
Kaynak: transcript'ler 09-10 → 09-17 (tüm projeler), effort A/B (Claude Code 2.1.274), platform.claude.com whats-new-opus-5 + effort, code.claude.com model-config. Hiçbir ayar değişmedi.
## Maliyet (7 gün, API fiyatı eşdeğeri; abonelikte fatura değil)
- Toplam $1,687 (1h cache yazımı 2x ile; tüm yazımlar 5m fiyatıyla $1,610): cache okuma $1,146 (%68) · cache yazma $278 (%16.5) · çıktı $262 (%15.5) · cache'siz girdi $0.17.
- Ana oturum %85 / subagent %15 · Opus 5 $1,632 · Sonnet 5 $31 · Fable 5.1 $22 · Haiku 4.5 $0.55 (claude-opus-4-8 39 istek fiyatsız).
- Thinking çıktı token'larının %41.1'i (4.46M / 10.86M); `usage.output_tokens_details.thinking_tokens` çıktının içinde, ayrıca faturalanmaz.
- En pahalı 5 ($ · çıktı payı · çıktı/girdi token): heryerde 034f9506 $353 · %11.8 · 0.003 | heryerde bd6fd52c $207 · %12.8 · 0.003 | Divisima cc751c9c $159 · %13.9 · 0.004 | EgeYapiPanel ffa0b7f5 $113 · %7.3 · 0.002 | EgeYapiPanel 1a0d739d $94 · %19.8 · 0.006.
- Maliyeti çıktı değil, büyük bağlamın her turda cache'ten yeniden okunması sürüklüyor (/usage 7 gün: kullanımın %82'si >150k context'te).
## Aşırı doğrulama (omer-skills, 27 KARAR bloğu)
- "≤10 git satırı + ≥5 doğrulama (claude -p + denetçi subagent)" koşuluna uyan blok 0; doğrulama yoğun bloklar büyük değişiklikliydi (UZUN-OTURUM-1: 156 satır, 15 claude -p). Sayılar yaklaşık: script içi çağrı ve anahtar kelimeyle denetçi sınıflaması.
## Effort A/B (C# `Kisalt` + 4 xUnit, ~40 satır; 3'er koşu, medyan)
| effort | tur | araç | girdi tok | çıktı tok | thinking | süre | $ | kabul |
|---|---|---|---|---|---|---|---|---|
| high | 6 | 5 | 116,134 | 1,608 | 44 | 47 sn | 0.257 | 3/3 |
| xhigh | 6 | 5 | 120,103 | 3,099 | 1,361 | 61 sn | 0.311 | 3/3 |
- 6 koşunun hepsi kırmızı-önce (derleme hatası) → uygulama → ilk testte 4/4, kod 40 satır. xhigh kalite farkı olmadan çıktıyı ~1.9x, thinking'i ~31x, süreyi +%30, maliyeti +%21 artırdı. Görev küçük (tavan etkisi); karar öncesi büyük görevde tekrar gerekir. Mevcut ayar `modelSettings.claude-opus-5.effortLevel: xhigh`; Claude Code'un Opus 5 varsayılanı `high`.
## Rapor uzunluğu (102 kapanış raporu)
- Ortalama 25.5 / medyan 19 satır; medyan heryerde 12.5 · omer-skills 25 · Divisima 54.
- "commit · test sayısı · CI · sapmalar" kuralı global değil, heryerde_2aa CLAUDE.md:29 (41ca99c, 09-10): orada 35 raporda dört alan %60, yalnız o alanlar (≤8 satır) %2.9; kuralsız omer-skills'te dört alan %2.9.
## Anthropic (birebir)
- effort: "Claude Opus 5 supports all five effort levels. **Start with `high`, the default**, and adjust based on your evals: step up to `xhigh` for demanding coding and agentic work" · "If you carried effort settings over from an earlier model, run a fresh effort sweep on your evals rather than reusing them."
- effort: "Effort controls thinking volume, not visible response length: on Claude Opus 5, changing effort does not reliably shorten responses, so prompt for length instead." · "Lower effort also means fewer and terser tool calls."
- whats-new-opus-5: "Default user-facing responses and written deliverables run longer." · "It also verifies its own work without being told to, so remove verification instructions carried over from earlier models ("include a final verification step," "use a subagent to verify"); they cause over-verification on Claude Opus 5."
- whats-new-opus-5: "Thinking tokens are billed as output tokens and count toward `max_tokens`, a hard limit on total output (thinking plus response text)"
