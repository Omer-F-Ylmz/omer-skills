# Hook karar tablosu (HOOK-1, 2026-10-10)

Kaynak: plugin cache betikleri (ecc 2.2.3, octo 11.13.1, context-mode 1.0.169). Hiçbir ayar uygulanmadı.

| Hook | Karar | Gerekçe | Kapatma |
|---|---|---|---|
| ecc GateGuard (pre:bash / pre:edit-write / pre:powershell `gateguard-fact-force`) | KÖTÜ | İlk Bash/Edit/Write'ta "gerçek sun" reddi; başsız `claude -p` onay veremez (bir oturumda 7 ret) | `ECC_GATEGUARD=off` (gateguard-fact-force.js:1325); alternatif `ECC_DISABLED_HOOKS=pre:bash:gateguard-fact-force,pre:edit-write:gateguard-fact-force,pre:powershell:gateguard-fact-force` |
| ecc diğer hook'lar (observe, governance-capture, config-protection, mcp-health-check, doc-file-warning, suggest-compact, pre:compact, skill:track) | İZLE | Hepsi `standard,strict` profilinde; engel/ağ bulgusu yok. `ECC_HOOK_PROFILE=minimal` hepsini söndürür (config-protection dahil) — şimdilik dokunma | `ECC_HOOK_PROFILE`, `ECC_DISABLED_HOOKS` (hook-flags.js:7-8) |
| octo telemetry-webhook | İYİ (etkisiz) | Native Windows'ta (MINGW/MSYS) ilk satırda `exit 0`; ayrıca yalnız `OCTOPUS_WEBHOOK_URL` doluysa çalışır (bu makinede tanımsız), https/localhost şartı. Giden veri: olay adı, oturum id, faz, araç adı, zaman, çıktı uzunluğu; token varsa Bearer başlığı | URL'i tanımlama |
| octo UserPromptSubmit ×3 (user-prompt-submit, done-criteria, github-work-queue-watch) | KÖTÜ (bayrakla kapat) | 37 octo hook'unun hepsi MINGW'de `exit 0` ama her istemde 3 bash süreci doğar; router bağlamı opt-in olsa da bayrak kesinleştirir. done-criteria zaten `OCTO_DONE_CRITERIA=on` ister (varsayılan kapalı) | `OCTOPUS_AUTO_ROUTER_MODE=off`, `OCTOPUS_GITHUB_WORK_QUEUE=off` |
| octo SessionStart (auto-router, discipline, fable5, memory…) | İZLE | Native Windows'ta çıkış 0, bağlam eklemiyor; oturum başı bağlamda "octo" metni görünürse `eklenti-yama.ps1` | — |
| context-mode PreToolUse (Bash/Read/Grep/WebFetch/Agent) | İZLE | `deny`/`modify` ile ctx_* araçlarına yönlendirir; başsızda `CLAUDE_CODE_HEADLESS=1` ise geçirir (formatters/claude-code.mjs:32). `claude -p` koşucularına bu değişken verilmeli; global env'e yazılmadı (interaktifte nudge'ı da söndürür) | koşucu başına `CLAUDE_CODE_HEADLESS=1` |
| context-mode PostToolUse/SessionStart | İYİ | Oturum belleği + büyük çıktıyı sandbox'a alma = gerçek jeton kazancı | — |

## context-mode ↔ headroom
Kısmen çakışıyor: ikisi de araç çıktısını küçültüyor (headroom vekil/Bash sıkıştırması; context-mode sandbox + Bash/Read yönlendirmesi). CLAUDE.md "Read dar aralık" kuralı ile context-mode'un "Read yerine ctx_execute_file" nudge'ı zıt yönde; çift sıkıştırma headroom_retrieve zincirini uzatır. Karar: ikisi açık, İZLE; başsız koşucularda `CLAUDE_CODE_HEADLESS=1`. Jeton ölçümü (ctx stats vs headroom) sonraki tura.

## Eklenecek env (overrides-uygula.ps1)
`ECC_GATEGUARD=off`, `OCTOPUS_AUTO_ROUTER_MODE=off`, `OCTOPUS_GITHUB_WORK_QUEUE=off`.

## eklenti-yama.ps1
Bayrağı olmayan kötü hook çıkarsa: `.\tools\eklenti-yama.ps1 -Plugin <ad> -Desen '<komut regex>'` (geri: `-Geri`). Şu an hiçbir hook için gerekmedi.
