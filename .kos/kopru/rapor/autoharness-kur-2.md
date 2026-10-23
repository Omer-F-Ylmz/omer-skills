# autoharness-kur-2 (23 Eki)

- Kayba autoharness 0.1.0 (commit 7cfd52e, MIT): `uv tool install C:\Projeler\autoharness-kayba` (pipx yok; aynı iş, yerel kopya taranmış). Bağımlılık yalnız pyyaml. `autoharness` ~/.local/bin'de. Smoke: boş dizinde `guide --non-interactive --generator claude_code` → Doctor status: ready.
- Hook diff: yok. settings.json ve .claude.json kurulum öncesi/sonrası aynı (sha256 eşit); yedek `.bak-kayba-20261023`. Kayba CC'ye hook/skill eklemez (Python CLI).
- Ücretli API: gerekmedi. `claude_code` üreteci yerel CC oturumunu kullanır; `openai_responses` seçilmedikçe anahtar yok.
- MAKARA: `autoharness optimize` yeniden başlatılabilir döngü; gece döngüsüne `arka.py` ile hedef repo + `--generator claude_code` verip bir adım olarak eklenebilir. Bağlanmadı (hedef harness repo + benchmark komutu Ömer'den gerekir).
- Ajan kanıtı (tigerless autoharness): `claude -p --model haiku` → skill listesinde `autoharness:learn`. Maliyet 0,10 + 0,10 USD (ilk çağrının çıktısını ayrıştırıcım yedi, yeniden koştum).
- BULGU+DÜZELTME: plugin hooks.json önceki turda `cmd /c "set PYTHONPATH=...&& python3 ..."` biçimine çevrilmişti; Git Bash `/c`'yi yol sanıp bozuyor, SessionEnd hook'u "'ache' is not recognized" ile düşüyordu. Orijinal POSIX biçimi (`PYTHONPATH=... python3 -m autoharness.hook.dispatch`, hooks.json.bak) geri kondu (cache içi; yedek hooks.json.cmdc-bak), yeniden `claude -p` temiz. Plugin güncellenirse hooks.json ezilir.
- Desktop: skill tek (`learn`), `dist/autoharness/autoharness-learn.zip` var, zip_denetle TEMİZ (dist gitignore'da). Hook Desktop'ta çalışmaz; yalnız skill yüklenir.
- Envanter: `tools/envanter/topla.py` koşuldu, envanter.tsv'de 4 autoharness satırı.
- Ömer'in adımı: zip'i claude.ai'ye yükle; kayba'yı hangi repoda koşturacağını söyle (MAKARA bağlantısı için).
