# BASLANGIC-HIZ-2 · P3, register'ı ilk `ui.render`'a taşıma

**Sonuç: KAZANDI (`-p`'de), etkileşimli açılışta nötr, işlev kaybı yok.** Kalıcı ayar/mod dosyası değişmedi; yama UYGULANMADI.

## Deney
`deney_kur3.py`: glance kopyasında `$.command.register` `session.start`'tan çıkarıldı, ilk `ui.render` (AbovePrompt) içine bayraklı tek seferlik `void` çağrı olarak taşındı. Orijinal dokunulmadı; `--settings` geçici katman + `--plugin-dir deney3/glance`. Kontrol = 3 orijinal açık, diğer 66 hook eklentisi kapalı.

## (a) `claude -p x --model haiku` (ardışık, değişimli, aynı saat dilimi)
| Kol | Süre | Geçiş |
|---|---|---|
| ctl c1 / c2 | 31 s / 28 s | 4 / 4 |
| exp e1 / e2 | 26 s / 24 s | 3 / 3 |
Glance register `-p`'de hiç tetiklenmedi (ui.render yok) → modül başına −1 tam tarama, ≈ −4 s (−%14). `-p` içinde `/glance` artık listelenmez (kabul edilen yan etki: `-p`'de komut zaten kullanılmıyor).

## (b) Etkileşimli (pywinpty, geçici venv `ara/bh/venv-pty`, gitignore'lu)
- `/glance` açılışta ctl'de 4.7 s, exp'te 4.7–5.5 s'de listelendi (log başından); `ui.render` oturum başında hemen çalıştığı için gecikme/kazanç yok. 3 tekrar: geçiş sayısı 1/1, süre farkı ölçüm gürültüsünde.
- `/glance` yazıp Enter: iki kolda da aynı çıktı ("Meetings / PRs / Linear / Slack DMs" bantları) → işlev kaybı YOK.
- İlk etkileşimli çift koşuda exp'te +2 geçiş (46–48 s) görüldü: dış kaynaklı ayar yeniden yüklemesi ("Replacing all … rules"), sonraki 2 tekrarda yok → deneyle ilgisiz, karıştırıcı olarak elendi.

## Tasarım: toplu yama betiği (UYGULAMA YOK; Desktop KABUL'ü sonrası ayrı parça)
Kapsam ölçüldü: 25 modun 16'sında `command.register` var; 15'i `ui.render`'lı (agent-radar, browser-lanes, context-bar, glance, heatmap, merge-gate, mission-control, now-playing, prayer-times, reels, replay-theater, session-saver, snake, switchboard, where-am-i). `cache-clock` ui.render'sız → atlanır (P2: clock'a taşımak kazandırmadı). Görevdeki "27" bu sayımla uyuşmuyor; yama listesi çalışma anında taranarak çıkarılır.
1. `tools/mod_yama.py [--uygula|--geri|--durum]`; hedef `~/.claude/plugins/marketplaces/claude-code-mods/mods/*/hooks/register.ts*`.
2. Dönüşüm (deney_kur3 ile aynı, CRLF korunur): tek `await $.command.register({...}).catch(...)` satırı `session.start` içinden çıkar; ui.render işleyicisinde `const rest = await next(e)` sonrasına `if (!registered) { registered = true; void $.command.register({...}).catch(() => {}) }`; modül başına `let registered = false`. Kalıp tutmazsa o mod ATLANIR (assert değil, rapor).
3. Kayıt `.kos/kopru/mod-yama.json`: mod → {orijinal SHA-256, yamalı SHA-256, yedek yolu `.kos/kopru/yedek/mod-yama/<mod>/register.*`}. Uygulamadan önce SHA kayıtla eşleşmiyorsa (marketplace güncellemesi) önce yeni orijinal yedeklenir, sonra yeniden yamalanır.
4. `--geri`: yamalı SHA hâlâ kayıtlıysa yedekten geri yazar; SHA farklıysa (güncellenmiş) dokunmaz, uyarır. `--durum`: mod başına temiz/yamalı/güncellenmiş.
5. Yeniden uygulama tetiği: SessionStart'ta `--durum` (salt okuma, <100 ms); "güncellenmiş" görülürse yalnız uyarı yazar, otomatik yazmaz. Kabul: `-p` geçiş sayısı 28 → ≤13 (projeksiyon; ≈4 s/geçiş → ≈ −60 s, ÖLÇÜLMEDİ) ve her mod için `/komut` etkileşimli listelenir.
6. Risk: host kısıtları (plugin başına tek hooks modülü) değişmez; marketplace güncellemesi yamayı siler → betik yeniden uygular; yamalı dosyalar kullanıcı düzenlemesi sayıldığından marketplace `git pull` çakışabilir → `--geri` önce.
Kullanılmayan eklentileri kapatma ÖNERİLMEDİ (nihai 22/32(d)). REA çağrısı gerekmedi (kazanıldı) → node bellek tavanı konusu yok.

Maliyet ≈ $0.75 (hedef $0.50 aşıldı: etkileşimli ölçüm için pty harness kurulumu + 2 kez backslash/hang düzeltmesi). Dosyalar: `ara/bh/{deney_kur3,deney_olc3,etk_olc3,etk_analiz}.py`.
