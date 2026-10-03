# TOKEN-6c — effort kayması · "diğer" kırılma teşhisi

## K1 Effort kayması
- Neden: oturum içinde `/effort xhigh` yapıldı (mod işi), CC bunu kalıcı yazdı. `/effort`, userSettings'te `modelSettings.<oturum modeli>.effortLevel` anahtarına yazar; `max` yazılmaz.
  - Kanıt: `~/.local/bin/claude.exe` 2.1.288, bayt 205779411: "For userSettings, takes effortLevel only and saves it as the default for the session's current model, under modelSettings as /effort saves it ('max' is session-only and is not written…)".
- Headroom Desktop'un payı yok, çünkü settings.json'a **anahtar yaması** ile yazıyor: güncel dosyayı okuyor, yalnız `root["env"]` anahtarına dokunuyor.
  - Kanıt: gglucass/headroom-desktop `src-tauri/src/client_adapters.rs#L3827-3851` (`configure_claude_settings_env_impl`) ve `#L4090-4100` (env anahtarı bazında kur/kaldır).
  - Pre-update snapshot yalnız Headroom'un kendi 3 durum dosyasını kapsıyor, settings.json yok (`storage.rs#L70-74`). Etkilenen değişiklik listesi bu yüzden gerekmedi.
- **Kullanım:** xhigh gereken oturum `claude --settings $HOME\.claude\xhigh.json` ile açılır. Oturum içinde `/effort` kullanılmaz.
  - `~/.claude/xhigh.json`: `{"modelSettings":{"claude-opus-5":{"effortLevel":"xhigh"},"claude-opus-5-5":{"effortLevel":"xhigh"}}}`. Oturum başı bayrak dosyasıdır, settings.json'a dokunmaz.
- Prob (claude -p 1/5): `claude -p "ok" --settings ~/.claude/xhigh.json --model claude-opus-5 --output-format stream-json --verbose`.
  - Sonuç: transcript'te `effort: "xhigh"` (ff9ba222, 13:29:29Z). settings.json sha 02372fb94f3e5e29 koşudan önce ve sonra aynı.
  - Sapma: probda `--model claude-opus-5` kullanıldı. Nedeni: varsayılan model opus-5-5'in settings.json değeri zaten xhigh, prob ayırt etmezdi. opus-5 için settings.json değeri `high`.
  - Effort düzeyi stream-json init'inde yok, yalnız `per_turn_effort_active` var. Kanıt transcript'teki `effort` alanı.
- Kalıntı: settings.json'da `claude-opus-5-5` hâlâ `xhigh`. Bu dalgada dokunulmadı, K4'te seçenek olarak duruyor.
