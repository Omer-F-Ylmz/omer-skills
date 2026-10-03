# TOKEN-6b — ara ölçüm · etkileşimli TTL simülasyonu · HR uyarısı

## K3 HR uyarısı (`~/.claude/statusline.ps1`)
- Segment en başta: `HR` = settings.json'da `env.ANTHROPIC_BASE_URL` var ve 127.0.0.1:6767 açık · `!!HR KAPALI:env` = anahtar yok (Headroom Desktop çıkış/pause/auto-pause/çökme bekçisinde siler, token-6a §K1) · `!!HR KAPALI:port` = anahtar var ama proxy yanıt vermiyor.
- Port denemesi 200 ms; sonuç `%TEMP%\hr-port-<port>.txt` içinde 30 sn önbellekli. settings okuması yalnız boolean; değer basılmaz.
- Başta durur ki 80 karakter kesmesi uyarıyı yutmasın; model · ctx · cache · miss aynı sırada kalır.
- Görünce: `:env` → Headroom Desktop'ı aç/devam ettir (env'i geri yazar), sonra yeni oturum · `:port` → proxy'yi başlat.
- Test `tests/test_statusline_hr.py` (USERPROFILE/TEMP tmp, `HR_PORT` dikişi, Python soket dinleyici). Yedek `~/.claude/statusline.ps1.bakT6b`.
