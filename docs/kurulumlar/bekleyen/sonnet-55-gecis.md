# Bekleyen: SOR — alt ajan tanımlarının Sonnet 5.5'e sabitlenmesi (MOTOR-M1 K2)

Yalnız öneri; bu dalgada tanımlar DEĞİŞMEDİ.

## Ölçüm (kaynaklı)
- CC sürümü: 2.1.284 (`claude --version`).
- Sonnet 5.5 kimliği `claude-sonnet-5-5`: API yanıtındaki `message.model` (29 Eyl alt ajan transcript'leri) ve K3 `modelUsage`. Sonnet 5 kimliği `claude-sonnet-5`: code.claude.com/docs/en/sub-agents ("Full model ID … `claude-sonnet-5`") + K3 a2 `modelUsage`.
- `sonnet` takma adı şu an **claude-sonnet-5-5**'e gidiyor: K3 a0 (`claude -p --model sonnet`) `modelUsage` anahtarı. context7'deki model-config anlık görüntüsü hâlâ "Anthropic API → Sonnet 5" diyor; doküman geride, ölçüm esas.
- En son alt ajan transcript'leri (video-tarayici ×4, suite-kosucu, Explore): hepsi `claude-sonnet-5-5`. Parti C alt ajanları `claude-sonnet-5` idi.
- `~/.claude/settings.json` env: `CLAUDE_CODE_SUBAGENT_MODEL` ve `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` anahtarları tanımlı (değerler yazdırılmadı). Doküman (sub-agents, env-vars; v2.1.257+): FORCE=1 iken alt ajan, takım üyesi ve iş akışı ajanlarının hepsi `CLAUDE_CODE_SUBAGENT_MODEL` modelinde koşar; tanımdaki `model:` ve çağrı başı model ezilir. Yerleşik Explore'un da claude-sonnet-5-5'te koşması FORCE'un etkin olduğuyla tutarlı.
- Sonuç: `video-tarayici-haiku` (`model: haiku`) yüklenmiş olsaydı bile FORCE altında Haiku'da koşmazdı. 2a'daki "haiku ölçülmedi" yalnız tanımın yüklenmemesinden kaynaklanmıyor.

## Öneri (Ömer onayı)
1. `video-tarayici`, `aday-arastirici`, `suite-kosucu`: `model: sonnet` → `model: claude-sonnet-5-5`. Takma ad kayarsa model sabit kalır; K3 ile aynı model.
2. Haiku 5.5 kolu denenecekse önce FORCE kaldırılır (ya da deneme süresince kapatılır). FORCE kalırsa tanımlardaki `model:` alanı yalnız belge işlevi görür.
3. M2 motoru model adımlarında alt ajan değil `claude -p --model claude-sonnet-5-5` kullanacak (docs/tasarim/parti-motoru.md); bu değişiklik yalnız mevcut skill akışını etkiler.
