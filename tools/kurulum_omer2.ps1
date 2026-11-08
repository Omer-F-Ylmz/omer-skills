param([switch]$Deneme,[switch]$Sistem)
# KURULUM-5B (uretici: tools/kurulum_omer2_uret.py). Omer kosar. -Deneme kurulum yapmaz, ne yapacagini yazar.
# -Sistem: winget (calisma zamani/derleyici/uygulama) satirlari yalniz bu bayrakla kosar (Node/Python surumunu degistirebilir).
# Mevcut olan ZATEN atlanir. Anahtar/ortam degeri yazdirilmaz. Silme yok.
$ErrorActionPreference="Continue"
$sonuc="$PSScriptRoot/../rapor/kurulum-omer2-sonuc.tsv"
if(-not (Test-Path $sonuc)){"kalem`tyontem`tdurum`tnot" | Set-Content $sonuc -Encoding utf8}
$sk="$env:USERPROFILE\.claude\skills"; $klonkok="C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste"; $indir="$env:USERPROFILE\Downloads\kurulum5b"
$uvexe=(Get-Command uv.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
$npmexe=(Get-Command npm.cmd -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
$gitexe=(Get-Command git.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
function Kayit($k,$y,$d,$n){ "$k`t$y`t$d`t$n" | Add-Content $sonuc -Encoding utf8; Write-Host "$d $y $k" }
function Kur5Cal($k,$y,$tanim,[scriptblock]$is){ if($Deneme){Kayit $k $y DENEME $tanim;return}
  try{ & $is; if($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE){Kayit $k $y KURULDU $tanim}else{Kayit $k $y HATA "exit $LASTEXITCODE"} }catch{Kayit $k $y HATA $_.Exception.Message} }
function Kur5Npm($k,$p){ if(-not $npmexe){Kayit $k NPM HATA "npm.cmd yok";return}
  if($null -eq $script:npmliste){ $script:npmliste=(& $npmexe ls -g --depth 0 --parseable 2>$null) -join "`n" }
  if($script:npmliste -match ('(^|[\\/])'+[regex]::Escape($p)+'(\r?\n|$)')){Kayit $k NPM ZATEN $p;return}
  Kur5Cal $k NPM "npm i -g $p" { & $npmexe i -g $p 2>&1 | Out-Null } }
function Kur5Uv($k,$p){ if(-not $uvexe){Kayit $k UV HATA "uv.exe yok";return}
  $a=$p -split ' '; Kur5Cal $k UV "uv tool install $p" { & $uvexe tool install @a 2>&1 | Out-Null } }
function Kur5Pip($k,$p){ Kur5Cal $k PIP "pip install --user $p" { & python.exe -m pip install --user $p 2>&1 | Out-Null } }
function Kur5Venv($k,$p,$py){ $v="$env:USERPROFILE\.venvs\$($k -replace '[^\w.-]','_')"
  if(Test-Path $v){Kayit $k VENV ZATEN $v;return}
  Kur5Cal $k VENV "uv venv $v --python $py; uv pip install $p" { & $uvexe venv $v --python $py 2>&1 | Out-Null; & $uvexe pip install --python "$v\Scripts\python.exe" $p 2>&1 | Out-Null } }
$wgVar=@{'OpenJS.NodeJS.LTS'='node';'Python.Python.3.12'='py:3.12';'Python.Python.3.13'='py:3.13';'Microsoft.OpenJDK.21'='java:21';
  'Microsoft.DotNet.SDK.10'='dotnet:10';'Rustlang.Rustup'='cargo';'Microsoft.WSL'='wsl';'GoLang.Go'='go';'Hashicorp.Terraform'='terraform';
  'Helm.Helm'='helm';'RedHat.Podman'='podman';'Google.DartSDK'='dart';'JetBrains.Kotlin.Compiler'='kotlinc';'Ninja-build.Ninja'='ninja';
  'PHP.PHP.8.3'='php';'PostgreSQL.PostgreSQL.17'='psql';'zig.zig'='zig'}
function WgVar($id){ $t=$wgVar[$id]; if(-not $t){return $null}; $ad,$sur=$t -split ':'
  if($ad -eq 'cargo' -and (Test-Path "$env:USERPROFILE\.cargo\bin\cargo.exe")){return "$env:USERPROFILE\.cargo\bin\cargo.exe"}
  if($ad -eq 'py'){ $o=(& py.exe "-$sur" -c "import sys;print(sys.executable)" 2>$null); if($LASTEXITCODE -eq 0 -and $o){return "$o"}; return $null }
  $c=(Get-Command "$ad.exe","$ad.cmd","$ad.bat" -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source; if(-not $c){return $null}
  if($ad -eq 'java'){ if(((& $c -version 2>&1) -join ' ') -match ('version "'+$sur+'[."]')){return $c}; return $null }
  if($ad -eq 'dotnet'){ if((& $c --list-sdks 2>$null) -match ('^'+$sur+'\.')){return $c}; return $null }
  return $c }
function Kur5Winget($k,$id){ $var=WgVar $id; if($var){$global:LASTEXITCODE=0; Kayit $k WINGET ZATEN "$id -> $var";return}
  if(-not $Sistem){Kayit $k WINGET ATLANDI "-Sistem yok: $id";return}
  Kur5Cal $k WINGET "winget install --id $id" { winget.exe install --id $id -e --silent --accept-package-agreements --accept-source-agreements 2>&1 | Out-Null } }
function Kur5Composer($k,$p){ Kur5Cal $k COMPOSER "composer global require $p" { composer.bat global require $p 2>&1 | Out-Null } }
function Kur5Vscode($k,$id){ Kur5Cal $k VSCODE "code --install-extension $id" { code.cmd --install-extension $id 2>&1 | Out-Null } }
function Kur5Indir($k,$url){ $ad=Split-Path $url -Leaf; $dst=Join-Path $indir $ad
  if(Test-Path $dst){Kayit $k INDIR ZATEN $dst;return}
  Kur5Cal $k INDIR "$url -> $dst (exe/msi'yi Omer calistirir)" { New-Item -ItemType Directory -Force $indir | Out-Null; Invoke-WebRequest -Uri $url -OutFile $dst -UseBasicParsing
    if($dst -like '*.zip'){ Expand-Archive $dst -DestinationPath ($dst -replace '\.zip$','') -Force } } }
function Kur5Rel($k,$repo,$ipucu){ $ghexe=(Get-Command gh.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
  if(-not $ghexe){Kayit $k RELEASE HATA "gh.exe yok";return}
  if($Deneme){Kayit $k RELEASE DENEME "gh release $repo asset~'$ipucu' -> $indir";return}
  try{ $r=(& $ghexe api "repos/$repo/releases/latest" 2>$null | ConvertFrom-Json); $a=$r.assets | Where-Object { ($ipucu -and $_.name -like "*$ipucu*") -or (-not $ipucu -and $_.name -match '(win|x64|x86_64).*\.(zip|exe|msi)$|\.(exe|msi)$') } | Select-Object -First 1
    if(-not $a){Kayit $k RELEASE HATA "asset yok: $repo $ipucu";return}
    $dst=Join-Path $indir $a.name; if(Test-Path $dst){Kayit $k RELEASE ZATEN $dst;return}
    New-Item -ItemType Directory -Force $indir | Out-Null; Invoke-WebRequest -Uri $a.browser_download_url -OutFile $dst -UseBasicParsing
    if($dst -like '*.zip'){ Expand-Archive $dst -DestinationPath ($dst -replace '\.zip$','') -Force }
    Kayit $k RELEASE KURULDU "$($a.name) -> $dst (exe/msi'yi Omer calistirir)" }catch{Kayit $k RELEASE HATA $_.Exception.Message} }
function Kur5Klon($k,$repo){ $hedef=Join-Path $klonkok ($repo -replace '/','__')
  if(Test-Path $hedef){Kayit $k KLON ZATEN $hedef;return}
  Kur5Cal $k KLON "git clone --depth 1 $repo" { $env:GIT_TERMINAL_PROMPT=0; & $gitexe clone --depth 1 "https://github.com/$repo" $hedef 2>&1 | Out-Null } }
function Kur5Skill($k,$repo,$sub){ $kok=Join-Path $klonkok ($repo -replace '/','__')
  if($Deneme){Kayit $k SKILL DENEME "$repo $sub -> $sk";return}
  if(-not (Test-Path $kok)){ $env:GIT_TERMINAL_PROMPT=0; & $gitexe clone --depth 1 "https://github.com/$repo" $kok 2>&1 | Out-Null }
  $baz= if($sub){Join-Path $kok ($sub -replace '/','\')}else{$kok}
  if(-not (Test-Path $baz)){Kayit $k SKILL HATA "yol yok: $repo $sub";return}
  $say=0; Get-ChildItem $baz -Recurse -Filter SKILL.md -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '\\(node_modules|\.git)\\' } | ForEach-Object {
    $ad=Split-Path $_.DirectoryName -Leaf; $dst=Join-Path $sk $ad
    if(-not (Test-Path $dst)){ try{Copy-Item $_.DirectoryName $dst -Recurse -ErrorAction Stop; $say++}catch{Kayit $k SKILL HATA "$ad $($_.Exception.Message)"} } }
  if($say -gt 0){Kayit $k SKILL KURULDU "$repo $sub ($say skill)"}else{Kayit $k SKILL ZATEN "$repo $sub (yeni skill yok)"} }
function Kur5Ajan($k,$yol){ $ad=Split-Path $yol -Leaf; $dst="$env:USERPROFILE\.claude\agents\$ad"
  if(Test-Path $dst){Kayit $k AJAN ZATEN $ad;return}
  Kur5Cal $k AJAN "ECC $yol -> $dst" { Invoke-WebRequest -Uri "https://raw.githubusercontent.com/affaan-m/everything-claude-code/HEAD/$yol" -OutFile $dst -UseBasicParsing } }

Kur5Composer 'FilaCheck' 'laraveldaily/filacheck'
Kur5Composer 'Rector' 'rector/rector'
Kur5Uv 'LEANN' 'leann-core'
Kur5Venv 'ScriptCreatorGraph' 'scrapegraphai' '3.12'
Kur5Ajan 'build-error-resolver' 'agents/build-error-resolver.md'
Kur5Ajan 'e2e-runner' 'agents/e2e-runner.md'
Kur5Ajan 'harness-optimizer' 'agents/harness-optimizer.md'
Kur5Klon 'AI Breakup Recovery Agent' 'Shubhamsaboo/ai-breakup-recovery-agent'  # lisans: none
Kur5Klon 'CLAUDE HQ' 'RoString36222/claude-hq'
Kur5Klon 'ChatGPT MD' 'bramses/chatgpt-md'
Kur5Klon 'FrontierAgent' 'ApodexAI/FrontierAgent'
Kur5Klon 'HIA (Health Insights Agent)' 'harshhh28/hia'
Kur5Klon 'Hermes voice agent' 'onlockj/hermes-voice-agent'
Kur5Klon 'Luma Agents' 'lumalabs/luma-agents-cli'
Kur5Klon 'Mobbin MCP' 'mobbin/mobbin-mcp-server'
Kur5Klon 'Pocket TTS' 'kyutai-labs/pocket-tts'
Kur5Klon 'SkillClaw' 'AMAP-ML/SkillClaw'
Kur5Klon 'codex-computer-use' 'tmustier/codex-computer-use-mcp'
Kur5Klon 'letta-ai/claude-subconscious' 'letta-ai/claude-subconscious'
Kur5Klon 'reel-factory' 'Shaan-alpha/AI-Reel-Factory'
Kur5Klon 'tinyagents' 'tinyhumansai/tinyagents'  # lisans: GPL-3.0
Kur5Klon 'AI Travel Agent (Local & Cloud)' 'nirbar1985/ai-travel-agent'
Kur5Klon 'Creative-Ad Skill' 'hoangngocanh2407/creative-ads-skill-layer'
Kur5Klon 'Firecrawl MCP' 'firecrawl/firecrawl-mcp-server'
Kur5Klon 'Flux Kontext' 'black-forest-labs/flux'
Kur5Klon 'Local REST API with MCP' 'coddingtonbear/obsidian-local-rest-api'
Kur5Klon 'TARS (Agent TARS)' 'bytedance/UI-TARS-desktop'
Kur5Klon 'Tokens Studio' 'tokens-studio/figma-plugin'
Kur5Klon 'Unet Loader (GGUF)' 'city96/ComfyUI-GGUF'
Kur5Klon 'agent-radar' 'duanyytop/agents-radar'
Kur5Klon 'execute_sql' 'supabase-community/supabase-mcp'
Kur5Klon 'hy-wu-edit' 'Tencent-Hunyuan/HY-WU'  # lisans: NOASSERTION
Kur5Klon 'smtg-ai/claude-squad' 'smtg-ai/claude-squad'  # lisans: AGPL-3.0
Kur5Klon 'AgentCouncil' 'zekigalip/AgentCouncil'
Kur5Klon 'BlenderGIS' 'domlysz/BlenderGIS'  # lisans: GPL-3.0
Kur5Klon 'Claudex Loop' 'chaseai-yt/claudex-loop'  # lisans: NOASSERTION
Kur5Klon 'Grok Build' 'xai-org/grok-build-plugin-cc'
Kur5Klon 'LLM Council' 'karpathy/llm-council'  # lisans: yok
Kur5Klon 'NVIDIA Kimodo' 'nv-tlabs/kimodo'
Kur5Klon 'agency-agents (msitarzewski/agency-agents)' 'msitarzewski/agency-agents'
Kur5Klon 'comfy-reshoot' 'Comfy-Org/comfy-reshoot'
Kur5Klon 'harness2-demo' 'joesaas/harness2-demo'  # lisans: yok
Kur5Klon 'linkedin-automator' 'charlesdove977/linkedin-automator'
Kur5Klon 'margin-analyzer' 'tuffy-xie/margin-analyzer'  # lisans: yok
Kur5Klon 'mattgierhart/PRD-driven-context-engineering' 'mattgierhart/PRD-driven-context-engineering'
Kur5Klon 'superlite' 'iha2/superlite'
Kur5Klon 'whatsapp-rust' 'oxidezap/whatsapp-rust'
Kur5Klon 'Cua Driver' 'trycua/cua'
Kur5Klon 'JSON Canvas' 'obsidianmd/jsoncanvas'
Kur5Klon 'Loopy <Forward-Future/loopy>' 'Forward-Future/loopy'
Kur5Klon 'Make Interfaces Feel Better <jakubkrehel/make-interfaces-feel-better>' 'jakubkrehel/make-interfaces-feel-better'
Kur5Klon 'claude-blog <AgriciDaniel/claude-blog>' 'AgriciDaniel/claude-blog'
Kur5Klon 'morluto/rea <GITHUB.COM/TRENDING.TODAY>' 'morluto/rea'
Kur5Klon 'ai-employeesreadme' 'markfulton/ai-employees'
Kur5Klon 'Archify' 'tt-a1i/archify'
Kur5Klon 'awesome-gamedev-agent' 'gamedev-skills/awesome-gamedev-agent-skills'
Kur5Klon 'awesome-mcp-' 'punkpeye/awesome-mcp-servers'
Kur5Klon 'blender-skills' 'EL4CTEO/blender-skills'
Kur5Klon 'claude-memREADME' 'thedotmack/claude-mem'
Kur5Klon 'claude-remotion-skill' 'haidrrrry/claude-remotion-skill'
Kur5Klon 'ClaudeAnimationBaseFreadme' 'JohnHeibel/ClaudeAnimationBase'
Kur5Klon 'Concord MCP' 'Get-Concord-AI/concord-mcp'
Kur5Klon 'Council of High Intelligence' '0xNyk/council-of-high-intelligence'
Kur5Klon 'Ditto' 'yoheinakajima/ditto'
Kur5Klon 'flocireadme' 'floci-io/floci'
Kur5Klon 'HTML Anything' 'nexu-io/html-anything'
Kur5Klon 'openshipreadme' 'oblien/openship'
Kur5Klon 'youtube-automation-agent' 'darkzOGx/youtube-automation-agent'
Kur5Klon 'Web Interface Guidelines' 'vercel-labs/web-interface-guidelines'
Kur5Klon 'bitnet.cpp' 'microsoft/BitNet'
Kur5Klon 'FLOW' 'AgriciDaniel/flow'  # lisans: CC-BY-4.0 (icerik)
Kur5Klon 'OneVOneJev' 'emrickgarrett/OneVoneJev'  # lisans: LISANSSIZ
Kur5Klon 'ai-job-searchfreadme' 'ai-job-search-dev/ai-job-search'
Kur5Klon 'dioramasreadme' 'blendi-remade/dioramas'
Kur5Klon 'OmniCloudirreadme' 'dimartarmizi/OmniCloud'
Kur5Klon 'OpenShell-tag' 'NVIDIA/OpenShell'
Kur5Klon 'kimi-k3-in-c' 'FareedKhan-dev/kimi-k3-in-c'
Kur5Klon 'reverse engineer anything repo' 'chandraas44/rea'  # lisans: NONE
Kur5Klon 'Apify Tester MCP Client' 'apify/tester-mcp-client'
Kur5Npm '9Router' '9router'
Kur5Npm 'AdaL CLI' '@sylphai/adal-cli'  # lisans: yok
Kur5Npm 'Agent TARS' '@agent-tars/cli'
Kur5Npm 'Claude Token Monitor' 'claude-token-monitor'
Kur5Npm 'Devin CLI' 'devin'  # lisans: proprietary (cognition.ai ToS)
Kur5Npm 'BMAD' 'bmad-method'
Kur5Npm 'Hyperframe' 'hyperframes'
Kur5Npm 'Metro' 'metro'
Kur5Npm 'Ruflo router' 'ruflo'
Kur5Npm 'codegraph <https://colbymchenry.github.io/codegraph/>' '@colbymchenry/codegraph'
Kur5Npm 'beads' '@beads/bd'
Kur5Npm 'claude-task' 'task-master-ai'  # lisans: MIT + Commons Clause
Kur5Npm 'REA (Reverse Engineer)' 'rea-agents'
Kur5Npm 'TokenJuice' 'tokenjuice'
Kur5Npm 'TypeScript' 'typescript'
Kur5Npm 'ccusage' 'ccusage'
Kur5Npm 'designlang' 'designlang'
Kur5Npm 'gws' '@googleworkspace/cli'
Kur5Npm 'Freebuff' 'freebuff'
Kur5Pip 'MemZero' 'mem0ai'
Kur5Pip 'Triton' 'triton-windows'
Kur5Pip 'CLI-Hub' 'cli-anything-hub'
Kur5Pip 'Fish Audio' 'fish-audio-sdk'
Kur5Pip 'Brotli' 'brotli'
Kur5Pip 'Stan' 'cmdstanpy'  # lisans: BSD-3 (stan)
Kur5Pip 'Storm' 'knowledge-storm'
Kur5Pip 'DiffSynth-' 'diffsynth'
Kur5Rel '0NE API' 'songquanpeng/one-api' 'one-api.exe'
Kur5Rel 'Eigent' 'eigent-ai/eigent' 'Eigent.Setup.1.0.7.exe'
Kur5Rel 'NaiboWang/EasySpider' 'NaiboWang/EasySpider' ''  # lisans: AGPL-3.0
Kur5Rel 'nvm-windows' 'coreybutler/nvm-windows' 'nvm-2.0.1-x64-setup.exe'
Kur5Rel 'storytold/artcraft' 'storytold/artcraft' 'ArtCraft_0.41.1_x64-setup.exe'
Kur5Rel 'youtube-dl' 'ytdl-org/youtube-dl' 'youtube-dl.exe'  # lisans: Unlicense
Kur5Rel 'Orchestrator.inc (agent-orchestrator)' 'ComposioHQ/agent-orchestrator' 'Setup.0.14.10.exe'
Kur5Rel 'ldid-procursus' 'ProcursusTeam/ldid' 'ldid_w64_x86_64.exe'  # lisans: AGPL-3.0
Kur5Rel 'Hardflow' 'ugulay/hardflow' 'hardflow-1.23.0.zip'  # lisans: GPL-3.0
Kur5Indir 'nvm' 'https://github.com/coreybutler/nvm-windows/releases/download/v2.0.1/nvm-2.0.1-x64-setup.exe'
Kur5Rel 'DataviewJS' 'blacksmithgu/obsidian-dataview' ''
Kur5Indir 'Poppler' 'https://github.com/oschwartz10612/poppler-windows/releases/download/v26.09.0-0/Release-26.09.0-0.zip'  # lisans: GPL (poppler)
Kur5Indir 'RIFE' 'https://github.com/nihui/rife-ncnn-vulkan/releases/download/20221029/rife-ncnn-vulkan-20221029-windows.zip'
Kur5Indir 'Vim' 'https://github.com/vim/vim-win32-installer/releases/download/v9.2.1302/gvim_9.2.1302_x64.exe'  # lisans: Vim License
Kur5Indir 'go toolchain' 'https://go.dev/dl/go1.27.3.windows-amd64.msi'
Kur5Indir 'llama-cli' 'https://github.com/ggml-org/llama.cpp/releases/download/b12189/llama-b12189-bin-win-cpu-x64.zip'
Kur5Indir 'rustc' 'https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe'  # lisans: MIT/Apache-2.0
Kur5Rel 'Luau' 'luau-lang/luau' 'luau-windows.zip'
Kur5Rel 'Ocis' 'owncloud/ocis' ''
Kur5Rel 'Pinokio' 'pinokiocomputer/pinokio' ''
Kur5Rel 'Servo' 'servo/servo' ''  # lisans: MPL-2.0
Kur5Rel 'Codebase Memory Graph <localhost:9749>' 'DeusData/codebase-memory-mcp' ''
Kur5Rel 'ink <80-days.ink>' 'inkle/ink' 'inklecate_windows.zip'
Kur5Rel 'mcptoonreadme' 'activeing123/mcptoon' 'mcptoon-0.8.34-win-x64.zip'
Kur5Rel 'plexoreadme' 'anmolkapil/plexo' 'plexo-1.0.0-rc.15-setup.exe'
Kur5Rel 'SwiftPM' 'swiftlang/swift-package-manager' ''
Kur5Rel 'Herdr' 'herdrdev/herdr' 'herdr-windows-x86_64.zip'
Kur5Rel 'releases' 'lightpanda-io/browser' ''  # lisans: AGPL-3.0
Kur5Skill 'skool-platinum' 'charlesdove977/skool-platinum-claude-code' ''  # lisans: NOASSERTION
Kur5Skill 'Claude Flow' 'ruvnet/claude-flow' ''
Kur5Skill 'oh-my-openagent' 'code-yeongyu/oh-my-openagent' ''  # lisans: NOASSERTION
Kur5Skill 'Marketing Skills for AI Agents' 'coreyhaines31/marketingskills' ''
Kur5Skill 'Marketing plugin' 'anthropics/knowledge-work-plugins' ''
Kur5Skill 'Matt Pocock skills repo' 'mattpocock/skills' ''
Kur5Skill 'anthropic-automations-recommender' 'anthropics/claude-plugins-official' ''
Kur5Skill 'coleschaffer/copywritingskills-rmbc' 'coleschaffer/copywritingskills-rmbc' ''
Kur5Skill 'connect-apps-plugin' 'ComposioHQ/awesome-claude-skills' ''  # lisans: none
Kur5Skill 'gan-evaluator' 'affaan-m/everything-claude-code' ''
Kur5Skill 'get_observations' 'thedotmack/claude-mem' ''
Kur5Skill 'lark-vc-agent' 'larksuite/cli' ''
Kur5Skill 'AThevon/genjutsu' 'AThevon/genjutsu' 'skills'  # lisans: NOASSERTION
Kur5Skill 'B-Roll Finder' 'louisedesadeleer/b-roll-finder' ''
Kur5Skill 'Filetree' 'nekocode/filetree-skill' 'skills/filetree'  # lisans: yok
Kur5Skill 'firecrawl/firecrawl-workflows' 'firecrawl/firecrawl-workflows' 'skills'  # lisans: ISC
Kur5Skill 'hookify' 'anthropics/claude-plugins-official' 'plugins/hookify'
Kur5Skill 'scrum-sage' 'michalparkola/tapestry-skills-for-claude-code' 'scrum-sage'
Kur5Skill 'agents-sdk-dev' 'anthropics/claude-plugins-official' 'plugins/agent-sdk-dev'
Kur5Skill 'commit-commands' 'anthropics/claude-plugins-official' 'plugins/commit-commands'
Kur5Skill 'crap4clj' 'unclebob/crap4clj' ''  # lisans: yok
Kur5Skill 'docx/pptx/xlsx' 'anthropics/skills' 'skills/docx'  # lisans: proprietary (skill LICENSE.txt)
Kur5Skill 'geo-crawlers' 'sickn33/agentic-awesome-skills' 'skills/geo-crawlers'
Kur5Skill 'ship-learn-next' 'michalparkola/tapestry-skills-for-claude-code' 'ship-learn-next'
Kur5Skill 'api-and-interface-design' 'addyosmani/agent-skills' 'skills/api-and-interface-design'
Kur5Skill 'schema (coreyhaines31/marketingskills)' 'coreyhaines31/marketingskills' 'skills/schema'
Kur5Skill 'Marketing Psychology' 'coreyhaines31/marketingskills' 'skills/marketing-psychology'
Kur5Skill 'getagentseal/founder-playbook' 'getagentseal/founder-playbook' ''
Kur5Skill 'PDF (dosya biÃ§imi)' 'anthropics/skills' 'skills/pdf'
Kur5Skill 'public-relations' 'coreyhaines31/marketingskills' 'skills/public-relations'
Kur5Skill 'Loopy' 'Forward-Future/loopy' ''
Kur5Skill 'Make Interfaces Feel Better' 'jakubkrehel/make-interfaces-feel-better' ''
Kur5Uv 'GitHub Spec Kit' 'specify-cli --from git+https://github.com/github/spec-kit.git'
Kur5Uv 'OpenHandds' 'openhands'
Kur5Vscode 'Kilo' 'kilocode.Kilo-Code'
Kur5Winget 'Podman' 'RedHat.Podman'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'helm' 'Helm.Helm'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'C-Sharp' 'Microsoft.DotNet.SDK.10'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'CPython' 'Python.Python.3.13'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Dart' 'Google.DartSDK'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Go' 'GoLang.Go'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Kotlin' 'JetBrains.Kotlin.Compiler'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Ninja' 'Ninja-build.Ninja'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Node' 'OpenJS.NodeJS.LTS'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'PHP' 'PHP.PHP.8.3'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Postgre' 'PostgreSQL.PostgreSQL.17'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Rust' 'Rustlang.Rustup'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'WSL' 'Microsoft.WSL'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Java' 'Microsoft.OpenJDK.21'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Microsoft Visual C++ Redistributable' 'Microsoft.VCRedist.2015+.x64'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Zig' 'zig.zig'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Python' 'Python.Python.3.12'  # lisans: WINGET-OLCULEMEDI(zaman asimi)
Kur5Winget 'Terraform (Infrastructure as Code)' 'Hashicorp.Terraform'  # lisans: BUSL-1.1 (gh NOASSERTION)
Kur5Indir 'Gradle' 'https://services.gradle.org/distributions/gradle-9.9.0-bin.zip'

# OMER-SOR[BELIRSIZ: ayna]: LoopTools | lisans=LGPL-3.0 | gh api 200; fizik kutuphanesi resmi olmayan ayna; LGPL
# OMER-SOR (betik satiri yok: yöntem HF-MODEL betikte desteklenmiyor): mmBERT-base | HF-MODEL | jhu-clsp/mmBERT-base
# OMER-SOR (betik satiri yok: hedef GitHub repo yolu, npm paket adı değil): Claude Code v2.1.71 | NPM | anthropics/claude-code
# OMER-SOR[BELIRSIZ: yildiz, lisans belirsiz]: Finegrain Image Enhancer | lisans=NOASSERTION | gh api 200; 1 yildiz, lisans belirsiz
# OMER-SOR[BELIRSIZ: <1MB) var; GPL GPL]: AtomicParsley | lisans=GPL-2.0 | AtomicParsleyWindows.zip (<1MB) var; GPL
# OMER-SOR[BELIRSIZ: PS5]: boykopovar/AnyPs5 | lisans=GPL-2.0 | prx-windows zip=91MB; GPL; PS5 jailbreak araci
# OMER-SOR[BELIRSIZ: sistem]: Chocolatey | lisans=NOASSERTION | sistem paket yoneticisi, yonetici hakki; lisans GH'ta belirsiz
# OMER-SOR[BELIRSIZ: uygulama boyutu ölçülmemiş]: FilmCraft CLI | lisans=Apache-2.0 | repo aciklamasi: dogrusal olmayan video editoru (GUI); portable zip var
# OMER-SOR[BELIRSIZ: ad belirsiz]: AgentLog | lisans=NOASSERTION | ad belirsiz (agentlogs/agentlog), lisans belirsiz
# OMER-SOR[BELIRSIZ: ayna]: BFXR | lisans=yok | release/paket yok, lisanssiz; yalniz kaynak klon
# OMER-SOR[BELIRSIZ: ayna]: Claude Toolkit | lisans=MIT | iki farkli proje, kaynak belirsiz
# OMER-SOR[BELIRSIZ: GPU]: ComfyUI-HunyuanVideo | lisans=yok | ComfyUI+GPU gerekir; lisanssiz; resmi Tencent repo ayri
# OMER-SOR[BELIRSIZ: GPU]: ComfyUI-HunyuanVideoWrapper | lisans=yok | ComfyUI+GPU gerekir; lisanssiz
# OMER-SOR[BELIRSIZ: sunucu]: Lago | lisans=AGPL-3.0 | AGPL; sunucu/docker
# OMER-SOR[BELIRSIZ: ayna]: LingoForge | lisans=yok | 3 yildiz, lisanssiz, kaynak belirsiz
# OMER-SOR (betik satiri yok: yöntem CARGO betikte desteklenmiyor): Ratatui | CARGO | crate ratatui 0.30.2 (static.crates.io 200)
# OMER-SOR[BELIRSIZ: sistem]: Scoop | lisans=NOASSERTION | sistem paket yoneticisi, uzaktan betik
# OMER-SOR (betik satiri yok: hedef GitHub repo yolu, npm paket adı değil): TARS | NPM | bytedance/UI-TARS-desktop (npm:@agent-tars/cli)
# OMER-SOR[BELIRSIZ: ad belirsiz]: Whisker | lisans=MIT | ad belirsiz; bu repo AD saldiri araci, release yok
# OMER-SOR[BELIRSIZ: Linux]: Wifite | lisans=yok | Linux, lisanssiz, saldiri araci
# OMER-SOR[BELIRSIZ: eslesmesi belirsiz]: hbot CLI | lisans=NOASSERTION | gh api repo 200; son push 2022-03; ipucu eslesmesi belirsiz
# OMER-SOR[BELIRSIZ: release yok]: rtmpdump | lisans=GPL-2.0 | gh api repo 200 GPL-2.0; Windows hazir release yok, kaynaktan derleme
# OMER-SOR[BELIRSIZ: API anahtari]: BU Bench | lisans=yok | gh api repo 200 license null; BU Bench V2.1; API anahtari/ucretli kosu
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Kafka | RELEASE | https://downloads.apache.org/kafka/4.2.2/
# OMER-SOR[2GB: boyut >2 GB]: Stable Diffusion Forge | lisans=AGPL-3.0 | gh api repo 200 AGPL-3.0; model agirliklari >2 GB
# OMER-SOR[BELIRSIZ: sunucu]: Vane (Perplexica) | lisans=MIT | gh api repo 200 MIT; sunucu uygulamasi (Docker/Node, API anahtari) -> uygulama
# OMER-SOR[BELIRSIZ: OLCULEMEDI]: ffprobe | lisans=GPL | HTTP 200 asset (ffprobe.exe paketin icinde); GPL build; winget Gyan.FFmpeg OLCULEMEDI (zaman asimi)
# OMER-SOR[BELIRSIZ: ayna]: Algorithmic Art | lisans=repo NOASSERTION (skill-bazli, kaynak-ac | gh contents: algorithmic-art,pdf,pptx,xlsx var; lisans belirsiz
# OMER-SOR[2GB: boyut >2 GB]: Chromium | lisans=BSD-3 | kaynak agaci devasa (>2GB); Chrome zaten var
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): Graphite |  | graphite-project/graphite-web
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): Lua |  | lua/lua
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): MariaDB |  | MariaDB/server
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): Maxun |  | getmaxun/maxun
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): Meta Bind |  | mProjectsCode/obsidian-meta-bind-plugin
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): Mongo |  | mongodb/mongo
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): MySQL |  | mysql/mysql-server
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): PERL |  | Perl/perl5
# OMER-SOR (betik satiri yok: paket adı yok): Pest | COMPOSER | composer require pestphp/pest
# OMER-SOR[BELIRSIZ: kalem yazimi]: Postkog | lisans=gh lisans yok | kalem yazimi Postkog belirsiz; self-host agir
# OMER-SOR[BELIRSIZ: arsiv]: S3-compatible storage | lisans=AGPL-3.0 | arsiv + AGPL
# OMER-SOR[BELIRSIZ: kaynak yonerge]: Web | lisans=MIT | kalem Web belirsiz, kaynak yonerge repo
# OMER-SOR[BELIRSIZ: uygulama boyutu ölçülmemiş]: karpathy-guidelines | lisans=gh lisans yok | karpathy/guidelines yok; baska repoda skills/ var, lisanssiz
# OMER-SOR[BELIRSIZ: ayna]: pdf | lisans=repo NOASSERTION (skill-bazli, kaynak-ac | gh contents: algorithmic-art,pdf,pptx,xlsx var; lisans belirsiz
# OMER-SOR[BELIRSIZ: ayna]: pptx | lisans=repo NOASSERTION (skill-bazli, kaynak-ac | gh contents: algorithmic-art,pdf,pptx,xlsx var; lisans belirsiz
# OMER-SOR[BELIRSIZ: ayna]: xlsx | lisans=repo NOASSERTION (skill-bazli, kaynak-ac | gh contents: algorithmic-art,pdf,pptx,xlsx var; lisans belirsiz
# OMER-SOR[BELIRSIZ: playbook]: FLOW <AgriciDaniel/flow> | lisans=other | playbook/doc deposu, lisans other
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): OneVOneJev <emrickgarrett/OneVoneJev> |  | 
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): Telegram <https://t.me/+n> |  | telegramdesktop/tdesktop
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): Terraform <Terraform.io> |  | hashicorp/terraform
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): Terraform.io <Terraform.io> |  | hashicorp/terraform
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): baocutreadme |  | JimLiu/baocut
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): DeepDiagram |  | LingyiChen-AI/DeepDiagram
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): Dextopreadme |  | NarYuki/Dextop
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): evolution-goreadme |  | evolution-foundation/evolution-go
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): OpenChatCut |  | 0xsline/OpenChatCut
# OMER-SOR[BELIRSIZ: ofansif]: pentest-agentsfreadme | lisans=gh lisans yok | lisanssiz + ofansif arac
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): task-coe |  | Agent4Science-UTokyo/Task-CoEvolve
# OMER-SOR (betik satiri yok: yöntem  betikte desteklenmiyor): netflix-clone |  | 
# OMER-SOR[2GB: boyut >2 GB]: CUDA | lisans=NVIDIA EULA | >2 GB, ticari
# OMER-SOR[2GB: boyut >2 GB]: CUDA 12.8 | lisans=NVIDIA EULA | >2 GB, ticari
# OMER-SOR[2GB: boyut >2 GB]: DaVinci | lisans=ticari | kaynak yok; >2GB ticari uygulama
# OMER-SOR[BELIRSIZ: sistem]: Hyper-V | lisans= | sistem ozelligi, yeniden baslatma, WSL2/VM cakisma riski
# OMER-SOR[BELIRSIZ: kaynak yok]: LaTeX | lisans=LPPL | kaynak yok; buyuk dagitim (MiKTeX/TeX Live), Omer secimi
# OMER-SOR[BELIRSIZ: kaynak yok]: MSSQL | lisans=ticari | kaynak yok; buyuk sunucu kurulumu
# OMER-SOR[2GB: boyut >2 GB]: MSVC | lisans=ticari | kaynak yok; Build Tools >2GB
# OMER-SOR[BELIRSIZ: ayna]: OpenClaw | lisans=MIT | gh api: MIT, "The AI that really does things"; kaynak sutunu bos, ad eslesmesi; kalem UYGULAMA
# OMER-SOR[2GB: boyut >2 GB]: Swift | lisans=Apache-2.0 | repo 1.4GB; Windows toolchain + VS bagimliligi buyuk (>2GB olasi) -> Omer karar
# OMER-SOR[BELIRSIZ: ayna]: T3 Code | lisans=MIT | kaynak create-t3-app (T3 Stack iskeleti) kalem degil; pingdotgg/t3code var (MIT, aciklama bos), hangisi kasted
# OMER-SOR[BELIRSIZ: sistem]: WSL2 | lisans=MIT | sistem ozelligi, yeniden baslatma gerekir
# OMER-SOR[2GB: boyut >2 GB]: WebKit | lisans=BSD/LGPL (gh spdx yok) | repo 13GB (>2GB), tarayici motoru kaynagi, kurulabilir urun degil
# OMER-SOR[BELIRSIZ: kaynak yok]: Windsurf | lisans=ticari | kaynak yok; masaustu IDE, kapali lisans; winget OLCULEMEDI
# OMER-SOR[BELIRSIZ: uygulama boyutu ölçülmemiş]: farion1231/cc-switch | lisans=MIT | v4.0.27 Windows.msi asset var; masaustu uygulama -> Omer karar
# OMER-SOR[BELIRSIZ: kaynak yok]: ARES | lisans= | kaynak yok; hafiza: saldiri araci kurulumu classifier engelli, Omer onayi gerekir
# OMER-SOR[BELIRSIZ: ayna]: Swagger.io (API Design Framework) | lisans=Apache-2.0 | kaynak swagger-api/swagger-ui = dokuman goruntuleyici, API tasarim cercevesi (Editor/Hub) degil; npm swagger-u
# OMER-SOR[BELIRSIZ: uygulama boyutu ölçülmemiş]: Telegram (Messaging Platform) | lisans=GPL-3.0 | tdesktop GPL-3.0; masaustu uygulama
# OMER-SOR[BELIRSIZ: OLCULEMEDI]: CPM-0.5B | lisans=OLCULEMEDI (HF lisans okunmadi) | HF API 200: uc openbmb *CPM-0.5B modeli var, hangisi belirsiz
# OMER-SOR[BELIRSIZ: ayni mi]: Agent CLI | lisans=AGPL-3.0 | npm view: postiz AGPL; genel ad, ayni mi emin degil
# OMER-SOR[BELIRSIZ: sunucu]: Forgejo | lisans=OLCULEMEDI | Codeberg API 503 iki denemede; git forge sunucusu (CLI degil), puan 0.2
# OMER-SOR (betik satiri yok: yöntem SKILL KLON betikte desteklenmiyor): ai-second-brain | SKILL klon | eugeniughelbur/obsidian-second-brain
# OMER-SOR[BELIRSIZ: ad farkli]: bug-hunter | lisans=MIT | repo var 5476 yildiz; ad farkli + saldirgan guvenlik paketi (82 skill)
# OMER-SOR (betik satiri yok: yöntem SKILL KLASORU betikte desteklenmiyor): eval-viewer | SKILL klasoru | anthropics/skills:skills/skill-creator/eval-viewer
# OMER-SOR[BELIRSIZ: sistem]: sqlite3 | lisans=OLCULEMEDI | winget show/search 25-40sn takildi, bos cikti; yerelde sqlite3 yok (command -v); sistem CLI
# OMER-SOR[BELIRSIZ: OLCULEMEDI]: tree | lisans=OLCULEMEDI | winget bos cikti; yerelde tree yok; Windows tree.com yerlesik
# OMER-SOR[BELIRSIZ: OLCULEMEDI]: wget | lisans=OLCULEMEDI | winget bos cikti; yerelde wget yok; curl mevcut
# OMER-SOR[2GB: boyut >2 GB]: xelatex | lisans=OLCULEMEDI | winget bos cikti; yerelde xelatex yok; TeX dagitimi >2GB olabilir
# OMER-SOR (betik satiri yok: yöntem UV/MCP betikte desteklenmiyor): Apowerui MCP toolkit | UV/MCP | oraios/serena
# OMER-SOR: Chatterbox | chatterbox-tts kütüphane (entry_points yok), torch/GB indirme: venv + uv pip; Ömer karar
# OMER-SOR: MLSharp | PyPI 'sharp' başka paket; doğrusu git+https://github.com/apple-aiml-research/ml-sharp, lisans NOASSERTION
# OMER-SOR: pgnx | install.js yalnız Node 22 (ABI 127) prebuild; makinede Node 24
