# openai-codex — 4 benzersiz kayıt

**Amaç:** Claude Code içinden OpenAI Codex ile kod incelemesi ya da görev devri.

**İç yapı:** codex [plugin] + iç yardımcı skill'ler: runtime sözleşmesi, sonuç sunumu, GPT-5.4 istem rehberi.

## En güçlü parçalar
- `codex` — Claude Code'dan Codex'e kod incelemesi ya da görev devretmek.
- `codex:gpt-5-4-prompting` — Codex/GPT-5.4 istemlerini kodlama, inceleme, teşhis, araştırma için kurar.

## Birlikte kullanım
- codex + codex:codex-result-handling: devredilen çıktıyı kullanıcıya sunmak.
- claude-code-plugins code-review ile ikinci görüş.

## Tuzaklar
- codex-cli-runtime ve codex-result-handling iç yardımcıdır, doğrudan çağrılmaz.
- Codex/OpenAI hesabı gerekir; ücret katalog metninde belirtilmemiş.

## Üyeler
- plugin (1): codex
- skill (3): codex:codex-cli-runtime, codex:codex-result-handling, codex:gpt-5-4-prompting
