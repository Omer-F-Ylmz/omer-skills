<#
KURULUM-11g -- claude-code-mcp (Obsidian eklentisi) yerel guvenlik yamasi.

Neden: eklentinin HTTP/SSE sunucusu Access-Control-Allow-Origin: * yaziyor ve
validateOrigin() her zaman true donduruyordu; WS sunucusu ise { port: 0 } ile
TUM arayuzlere baglaniyordu ve lock dosyasinda authToken yok. Bu haliyle
Obsidian acikken ziyaret edilen herhangi bir web sayfasi kasayi okuyup
yazabilir; yazma yolu prompt injection kapisidir.

Kural: tarayici her WS el sikismasinda ve cross-origin istekte Origin gonderir.
Origin tasiyan istek reddedilir (HTTP 403 / WS el sikismasi red), CORS basligi
hic yazilmaz. mcp-remote koprusu Origin GONDERMIYOR (11g K6 olcumu), o yuzden
bearer token'a gerek yok.

host verilince node.listen DNS yoluna girer ve senkron olmaktan cikar; eklentinin
`this.wss.address().port` satiri null.port'a duser, hata dual-server'da yutulur ve
`.claude/ide/<port>.lock` YAZILMAZ (CC /ide kesfi kirilir). O yuzden port okumasi
'listening' olayini bekleyecek sekilde de yamanir.

Idempotent: yamasiz hash -> uygular | yamali hash -> dokunmaz | baska -> DUR.
Eklenti guncellenince yama SILINIR; guncellemeden sonra bu betigi yeniden kos.

Kullanim:
  powershell -ExecutionPolicy Bypass -File tools\obsidian-yama.ps1
  powershell -ExecutionPolicy Bypass -File tools\obsidian-yama.ps1 -Kontrol
#>
param(
  [string]$Kasa = "$env:USERPROFILE\Desktop\Obsidian",
  [switch]$Kontrol
)
$ErrorActionPreference = 'Stop'

$Main    = Join-Path $Kasa '.obsidian\plugins\claude-code-mcp\main.js'
$Yedek   = "$Main.bak11g"
$YAMASIZ = '784b49d6f243053a2271d1e69c6d0716a3bde407a5dfeda8fbb894eaf87ec043'
$YAMALI  = '4ee2c5d80b1baf9312d701708feb6adb0eee252ddd95f83d5737788998c0805c'

function Get-Sha256([string]$Yol) {
  (Get-FileHash -Algorithm SHA256 -LiteralPath $Yol).Hash.ToLower()
}

if (-not (Test-Path -LiteralPath $Main)) {
  Write-Host "DUR: main.js bulunamadi -> $Main"; exit 2
}

$simdi = Get-Sha256 $Main
Write-Host "main.js sha256: $simdi"

if ($simdi -eq $YAMALI) { Write-Host 'Zaten yamali -- dokunulmadi.'; exit 0 }
if ($simdi -ne $YAMASIZ) {
  Write-Host 'DUR: bilinmeyen hash. Eklenti surumu degismis olabilir.'
  Write-Host "  beklenen yamasiz: $YAMASIZ"
  Write-Host "  beklenen yamali : $YAMALI"
  Write-Host '  Capalar elle dogrulanmadan yama UYGULANMAZ.'
  exit 2
}
if ($Kontrol) { Write-Host 'Yamasiz (-Kontrol: degisiklik yapilmadi).'; exit 0 }

# --- capalar: her biri dosyada TAM 1 kez gecmeli ---
$eskiLog = @'
// src/mcp/server.ts
var fs = __toESM(require("fs"));
'@
$yeniLog = @'
// KURULUM-11g yamasi -- Origin olcum kaydi (yalniz baslik adi + degeri, govde yok).
function __k11gOriginLog(kanal, origin, ua) {
  try {
    const f = require("fs"), p = require("path");
    const d = "C:/Projeler/.tmp-mcp-trace";
    f.mkdirSync(d, { recursive: true });
    f.appendFileSync(
      p.join(d, "obsidian-origin.jsonl"),
      JSON.stringify({
        t: new Date().toISOString(),
        kanal,
        origin: origin === void 0 ? null : origin,
        "user-agent": ua === void 0 ? null : ua
      }) + "\n"
    );
  } catch (e) {
  }
}

// src/mcp/server.ts
var fs = __toESM(require("fs"));
'@

$eskiCors = @'
  setCORSHeaders(res) {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader(
      "Access-Control-Allow-Headers",
      "Content-Type, Accept, Last-Event-ID"
    );
    res.setHeader("Access-Control-Max-Age", "86400");
  }
'@
$yeniCors = @'
  setCORSHeaders(res) {
    // KURULUM-11g yamasi: CORS basligi HIC yazilmaz.
  }
'@

$eskiSse = @'
      Connection: "keep-alive",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type, Accept, Last-Event-ID"
    });
'@
$yeniSse = @'
      Connection: "keep-alive"
    });
'@

$eskiDogrula = @'
  validateOrigin(req) {
    return true;
  }
'@
$yeniDogrula = @'
  validateOrigin(req) {
    const o = req.headers && req.headers.origin;
    __k11gOriginLog("http", o, req.headers && req.headers["user-agent"]);
    return !o;
  }
'@

$eskiPort = @'
    this.port = this.wss.address().port;
'@
$yeniPort = @'
    this.port = (this.wss.address() || {}).port;
    if (!this.port) {
      await new Promise((r) => this.wss.once("listening", r));
      this.port = this.wss.address().port;
    }
'@

$eskiWss = @'
    this.wss = new import_websocket_server.default({ port: 0 });
'@
$yeniWss = @'
    this.wss = new import_websocket_server.default({
      port: 0,
      host: "127.0.0.1",
      verifyClient: (info) => {
        const h = (info.req && info.req.headers) || {};
        const o = info.origin || h.origin;
        __k11gOriginLog("ws", o, h["user-agent"]);
        return !o;
      }
    });
'@

$utf8 = New-Object System.Text.UTF8Encoding($false)
$s = [System.IO.File]::ReadAllText($Main, $utf8)

$ciftler = @(
  @{ ad = 'logger';        eski = $eskiLog;     yeni = $yeniLog },
  @{ ad = 'setCORSHeaders';eski = $eskiCors;    yeni = $yeniCors },
  @{ ad = 'sse writeHead'; eski = $eskiSse;     yeni = $yeniSse },
  @{ ad = 'validateOrigin';eski = $eskiDogrula; yeni = $yeniDogrula },
  @{ ad = 'ws sunucu';     eski = $eskiWss;     yeni = $yeniWss },
  @{ ad = 'ws port';       eski = $eskiPort;    yeni = $yeniPort }
)

# Betik CRLF olarak checkout edilmis olabilir (core.autocrlf=true); main.js LF.
foreach ($c in $ciftler) {
  $c.eski = $c.eski.Replace("`r`n", "`n")
  $c.yeni = $c.yeni.Replace("`r`n", "`n")
}

foreach ($c in $ciftler) {
  $n = ([regex]::Matches($s, [regex]::Escape($c.eski))).Count
  if ($n -ne 1) { Write-Host "DUR: '$($c.ad)' capasi $n kez gecti (1 bekleniyordu)."; exit 2 }
}

if (-not (Test-Path -LiteralPath $Yedek)) {
  Copy-Item -LiteralPath $Main -Destination $Yedek
  Write-Host "Yedek: $Yedek"
} else {
  Write-Host "Yedek zaten var: $Yedek"
}

foreach ($c in $ciftler) { $s = $s.Replace($c.eski, $c.yeni) }
[System.IO.File]::WriteAllText($Main, $s, $utf8)

$sonra = Get-Sha256 $Main
Write-Host "yamali sha256 : $sonra"
if ($sonra -ne $YAMALI) {
  Write-Host 'DUR: yama sonrasi hash beklenenle uyusmadi, yedek geri alindi.'
  Copy-Item -LiteralPath $Yedek -Destination $Main -Force
  exit 2
}
Write-Host 'Yama uygulandi. Obsidian yeniden baslatilmali.'
exit 0
