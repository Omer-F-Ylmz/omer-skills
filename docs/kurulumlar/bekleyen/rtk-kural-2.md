# ONAY rtk-kural-2 (22 K2) — KOŞULMAZ, Ömer onaylar

Repo filtresi `.rtk/filters.toml` cc-kopru-suit artık `node --test` komutunu da eşliyor (son 3 günde 75 çağrı, ~15k tok; fixture'da %89 azalma). Filtre, güven verilene kadar etkin olmaz (21a'dan bekleyen `rtk trust`, bekleyen/rtk-kural.md):

```powershell
Set-Location C:\Projeler\omer-skills
rtk trust --yes
rtk verify --filter cc-kopru-suit      # satır içi test 1/1
# geri alma
rtk untrust
```

## Kullanıcı düzeyi: yeni kural yok
RTK'dan geçmeyen en büyük 10 aile (discover + transcript, son 3 gün): cat 256k · sed -n 156k · grep 100k · echo 82k · ls 76k · python - 75k · python -c 51k · git 43k · wc 39k · graphify query 38k (token).
- cat / sed -n / echo / python: dosya içeriği ya da tek seferlik analiz çıktısı. Satır süzmek içeriği bozar, bu yüzden kural yazılmaz.
- grep / ls / git / wc: RTK'nın kendi komutları var ama `cd X && …` ve `| head` zincirlerinde kanca yeniden yazmıyor. Bu kural değil alışkanlık meselesi.
- graphify query: `--budget` ile zaten sınırlı. Boş satır süzmek iki gerçek çıktıda ~%3 kazandırıyor. `[!] TRUNCATED` uyarısı korunmalı, `max_lines` de uyarıyı kesebilir. **21a'daki graphify-query önerisi (max_lines 120) geri çekildi.**

## PowerShell
settings.json'da PowerShell eşleyicisi `rtk hook claude`'a bağlı. Ancak kanca `tool_name: PowerShell` girdisine hiçbir şey döndürmüyor (Bash girdisi yeniden yazılıyor). `rtk --help` ve `rtk init --help` içinde PowerShell desteği yok. Bu kanca şu an işlevsiz; araç çıktısının %2.5'i (~126k tok) RTK dışında kalıyor. Blok yazılmadı: bağlanacak bir RTK girişi yok.
