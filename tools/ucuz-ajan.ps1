# Ucuz ajan: `claude -p` alt süreci Ollama'ya bağlanır. Env YALNIZ bu süreçte; global ortam/ayar değişmez.
# Kullanım: tools\ucuz-ajan.ps1 -Model gpt-oss:120b-cloud -Istek "..."  (istek yoksa stdin)
param([Parameter(Mandatory)][string]$Model, [string]$Istek, [string]$Url = "http://localhost:11434")
if (-not $Istek) { $Istek = [Console]::In.ReadToEnd() }
$env:ANTHROPIC_BASE_URL = $Url
$env:ANTHROPIC_AUTH_TOKEN = "ollama"
$env:ANTHROPIC_API_KEY = ""
# --setting-sources "": kullanıcı settings env'i (headroom vekili) ezmesin
$Istek | claude -p --model $Model --setting-sources "" --output-format json
