# İş 4 kanca kaynak keşfi (d2, okuyucu alt ajanı; kanıt satırları örneklenmedi)
Not: kanca_tara.out SessionStart'ı çift sayıyor (JSON kancaların hook_success'i additional_context'te de var).
1. context-mode PreToolUse ipucu: plugins/cache/context-mode/context-mode/1.0.169/hooks/routing-block.mjs:83/87/91/95. ZATEN 1×/oturum
   (hooks/core/routing.mjs:121-143 guidanceOnce, %TEMP%/context-mode-guidance-s-<sid>/<tür>). Ayar yok. Olası: kendi SessionStart'ımız işaret
   dosyalarını önceden açar (~8 kr/istek, küçük) — ama ipucunun amacı (yönlendirme) kaybolur → davranış kapısı şart.
2. SessionStart:startup/oturum (kr): claude-mem 8693 (systemMessage 4177) · context-mode 4773 (sessionstart.mjs:166 koşulsuz) · ponytail 4570 ·
   superpowers 3604 (6.4.1/hooks/session-start:11,44) · ecc 824. Ayar: claude-mem ~/.claude-mem/settings.json (OBSERVATIONS 15, SESSION_COUNT 10,
   SHOW_LAST_SUMMARY, SHOW_TERMINAL_OUTPUT); ponytail PONYTAIL_DEFAULT_MODE / %APPDATA%\ponytail\config.json (off = kapatma → YASAK; lite az kazanç).
   superpowers + context-mode ayarsız → sarmalayıcı ya da plugin kapatma (YASAK).
3. PostToolUse:Edit/Write: payın çoğu dotnet-format.ps1 PowerShell başlığıydı — settings.json tam komut dizgesiyle ZATEN düzeldi (sonrası 0).
   Kalan: 6 azure plugin {"continue":true} (18 kr; kapatma YASAK), hookify {} (4 kr). → iş yok.
PreToolUse:Bash 121 kr/istek: ~3.0M block-destructive.ps1 başlığı (düzeldi; güvenlik kancası KAPSAM DIŞI; düzeltme sonrası 76 hook_cancelled 15 sn — Ömer'e bildir),
kalan rtk hook updatedInput (~480 kr) + rtk-onisle.py (~670 kr).
Açık: PreToolUse/PostToolUse hook_success içeriğinin modele girip girmediği kanıtsız; ponytail SubagentStart ölçülmedi.
