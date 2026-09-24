# ONAY mcp-hizlandir (21c) — KOŞULMAZ, Ömer onaylar

Ölçüm: docs/olcumler/onek-kaymasi.md "21c". **Önbellek kazancı ≈ 0.** Kullanıcı istemi 58.6k bloğun önünde olduğundan yarışı gidermek bloğu oturumlar arasında okunur yapmaz. Kalan fayda: ilk turda "still connecting" listesi boşalır, araçlar hazır olur.
Değişen tek şey başlatma biçimi: 5 npx sunucusu `cmd /c npx -y paket@sürüm` yerine global kurulumdan `node <giriş.js>` ile başlar. Sunucu kapanmaz, sürüm aynı kalır. uvx sunucuları (code-review, fetch, git, time) dokunulmaz: exe'ye geçmek yalnız ~50 ms kazandırıyor.

Beklenen başlama (ms, initialize yanıtına; npx önbellek kopyasıyla ölçüldü):

| Sunucu | Şimdi (seri / 13'ü birlikte) | node ile |
|---|---|---|
| mcp-sequential-thinking | 1272–1550 / 1963–2391 | 44–48 |
| mcp-memory | 1401–1458 / 2088–2581 | 149–172 |
| mcp-filesystem | 1420–1613 / 2110–2618 | 163–209 |
| brave-search | 1498–1564 / 2193–2696 | 286–323 (soğuk ilk 4446) |
| stitch | 2084–2927 / 2943–3391 | 716–1361 |

## Uygula (PowerShell 5.1, CC tamamen kapalıyken)
```powershell
$cfg = "$HOME\.claude.json"
Copy-Item $cfg "$cfg.mcp-yedek" -Force
$node = (Get-Command node).Source
$root = (npm root -g).Trim()
$j = Get-Content $cfg -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($n in "mcp-sequential-thinking","mcp-memory","mcp-filesystem","stitch","brave-search") {
  $s = $j.mcpServers.$n; $a = @($s.args); $i = [array]::IndexOf($a, "-y")
  if ($s.command -ne "cmd" -or $i -lt 0) { "atlandi: $n"; continue }
  $pkg = $a[$i + 1]; $rest = @($a | Select-Object -Skip ($i + 2))
  $ad = if ($pkg.LastIndexOf("@") -gt 0) { $pkg.Substring(0, $pkg.LastIndexOf("@")) } else { $pkg }
  npm i -g $pkg | Out-Null
  $pj = Get-Content "$root\$ad\package.json" -Raw | ConvertFrom-Json
  $bin = if ($pj.bin -is [string]) { $pj.bin } else { @($pj.bin.PSObject.Properties.Value)[0] }
  $s.command = $node
  $s.args = @(Join-Path "$root\$ad" $bin) + $rest
  "$n -> node $pkg"
}
[IO.File]::WriteAllText($cfg, ($j | ConvertTo-Json -Depth 100), (New-Object Text.UTF8Encoding $false))
```
brave-search config'te sürümsüzse `npm i -g` o günkü sürümü kurar ve sabitler.

## Geri al (yalnız bu 5 girdi yedekten döner, CC'nin sonraki yazımları korunur)
```powershell
$cfg = "$HOME\.claude.json"
$y = Get-Content "$cfg.mcp-yedek" -Raw -Encoding UTF8 | ConvertFrom-Json
$j = Get-Content $cfg -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($n in "mcp-sequential-thinking","mcp-memory","mcp-filesystem","stitch","brave-search") { $j.mcpServers.$n = $y.mcpServers.$n }
[IO.File]::WriteAllText($cfg, ($j | ConvertTo-Json -Depth 100), (New-Object Text.UTF8Encoding $false))
```

## Doğrulama (K5) — 2 yakalama, $0 (her POST /v1/messages 400 alır, upstream'e gitmez)
```powershell
$d = "$env:TEMP\onek-dogrula"; New-Item $d -ItemType Directory -Force | Out-Null; Set-Location $d
@'
import http.server
n = [0]
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(s):
        b = s.rfile.read(int(s.headers.get("content-length", 0)))
        if s.path.startswith("/v1/messages"):
            n[0] += 1; open(f"istek-{n[0]}.json", "wb").write(b)
        s.send_response(400); s.send_header("content-length", "2"); s.end_headers(); s.wfile.write(b"{}")
    def log_message(s, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", 8791), H).serve_forever()
'@ | Set-Content kaydedici.py -Encoding ascii
@'
import glob, hashlib, json
for f in sorted(glob.glob("istek-*.json")):
    t = json.load(open(f, encoding="utf-8"))["messages"][1]["content"][0]["text"]
    i = t.find("still connecting")
    print(f, "m1", hashlib.sha1(t.encode()).hexdigest()[:8], "bekleyen", t[i:i + 400].split("\n\n")[0].split("\n")[1:] if i > 0 else [])
'@ | Set-Content karsilastir.py -Encoding ascii
'{"env":{"ANTHROPIC_BASE_URL":"http://127.0.0.1:8791"}}' | Set-Content ayar.json -Encoding ascii
$p = Start-Process python kaydedici.py -PassThru -WindowStyle Hidden
Push-Location C:\Projeler\omer-skills
1..2 | % { $null | claude -p "ok de" --model sonnet --settings "$d\ayar.json" | Out-Null }
Pop-Location; Stop-Process $p.Id; python karsilastir.py
```
Beklenen: her dosyada `bekleyen []`, iki koşu aynı dakikadaysa m1 özeti aynı. Farklı dakikada claude-mem damgası yüzünden m1 değişir (ayarlanamaz). Günlük önbellek kazancı ≈ 0 token (istem önde). Etkileşimli ilk isteklerde cache_read 17.565'te kalır.
