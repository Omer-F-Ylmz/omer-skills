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
function Kur5Winget($k,$id){ if(-not $Sistem){Kayit $k WINGET ATLANDI "-Sistem yok: $id";return}
  Kur5Cal $k WINGET "winget install --id $id" { winget.exe install --id $id -e --silent --accept-package-agreements --accept-source-agreements 2>&1 | Out-Null } }
function Kur5Composer($k,$p){ Kur5Cal $k COMPOSER "composer global require $p" { composer.bat global require $p 2>&1 | Out-Null } }
function Kur5Vscode($k,$id){ Kur5Cal $k VSCODE "code --install-extension $id" { code.cmd --install-extension $id 2>&1 | Out-Null } }
function Kur5Indir($k,$url){ $ad=Split-Path $url -Leaf; $dst=Join-Path $indir $ad
  if(Test-Path $dst){Kayit $k INDIR ZATEN $dst;return}
  Kur5Cal $k INDIR "$url -> $dst (exe/msi'yi Omer calistirir)" { New-Item -ItemType Directory -Force $indir | Out-Null; Invoke-WebRequest -Uri $url -OutFile $dst -UseBasicParsing
    if($dst -like '*.zip'){ Expand-Archive $dst -DestinationPath ($dst -replace '\.zip$','') -Force } } }
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
Kur5Klon 'AI Travel Agent (Local & Cloud)' 'nirbar1985/ai-travel-agent'
Kur5Klon 'Creative-Ad Skill' 'hoangngocanh2407/creative-ads-skill-layer'
Kur5Klon 'Firecrawl MCP' 'firecrawl/firecrawl-mcp-server'
Kur5Klon 'Firecrawl MCP Server' 'firecrawl/firecrawl-mcp-server'
Kur5Klon 'Flux Kontext' 'black-forest-labs/flux'
Kur5Klon 'Local REST API with MCP' 'coddingtonbear/obsidian-local-rest-api'
Kur5Klon 'TARS (Agent TARS)' 'bytedance/UI-TARS-desktop'
Kur5Klon 'Tokens Studio' 'tokens-studio/figma-plugin'
Kur5Klon 'Unet Loader (GGUF)' 'city96/ComfyUI-GGUF'
Kur5Klon 'agent-radar' 'duanyytop/agents-radar'
Kur5Klon 'execute_sql' 'supabase-community/supabase-mcp'
Kur5Klon 'generate_typescript_types' 'supabase-community/supabase-mcp'
Kur5Klon 'AgentCouncil' 'zekigalip/AgentCouncil'
Kur5Klon 'Grok Build' 'xai-org/grok-build-plugin-cc'
Kur5Klon 'NVIDIA Kimodo' 'nv-tlabs/kimodo'
Kur5Klon 'agency-agents (msitarzewski/agency-agents)' 'msitarzewski/agency-agents'
Kur5Klon 'comfy-reshoot' 'Comfy-Org/comfy-reshoot'
Kur5Klon 'linkedin-automator' 'charlesdove977/linkedin-automator'
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
Kur5Klon 'Claude Blog' 'AgriciDaniel/claude-blog'
Kur5Klon 'ai-job-searchfreadme' 'ai-job-search-dev/ai-job-search'
Kur5Klon 'ClaudeAnimationBasereadme' 'JohnHeibel/ClaudeAnimationBase'
Kur5Klon 'dioramasreadme' 'blendi-remade/dioramas'
Kur5Klon 'OmniCloudirreadme' 'dimartarmizi/OmniCloud'
Kur5Klon 'OpenShell-tag' 'NVIDIA/OpenShell'
Kur5Klon 'kimi-k3-in-c' 'FareedKhan-dev/kimi-k3-in-c'
Kur5Klon 'Apify Tester MCP Client' 'apify/tester-mcp-client'
Kur5Npm '9Router' '9router'
Kur5Npm 'Agent TARS' '@agent-tars/cli'
Kur5Npm 'Claude Token Monitor' 'claude-token-monitor'
Kur5Npm 'Agent Client' '@agentclientprotocol/sdk'
Kur5Npm 'context-inspector' 'context-inspector'
Kur5Npm 'Agent SDK' '@anthropic-ai/claude-agent-sdk'  # lisans: SEE LICENSE IN README (Anthropic ticari sartlar)
Kur5Npm 'Angular' '@angular/core'
Kur5Npm 'BMAD' 'bmad-method'
Kur5Npm 'BMAD Method' 'bmad-method'
Kur5Npm 'Babel' '@babel/core'
Kur5Npm 'Bootstrap' 'bootstrap'
Kur5Npm 'E2B' 'e2b'
Kur5Npm 'GraphQL' 'graphql'
Kur5Npm 'Hyperframe' 'hyperframes'
Kur5Npm 'Metro' 'metro'
Kur5Npm 'Primer' '@primer/react'
Kur5Npm 'ProtoMaps' 'pmtiles'
Kur5Npm 'Ruflo router' 'ruflo'
Kur5Npm 'Swagger.io <Swagger.io>' 'swagger-ui'
Kur5Npm 'Tailwind CSS <tailwindcss.com>' 'tailwindcss'
Kur5Npm 'Three.js <https://threejs.org>' 'three'
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
Kur5Npm 'Tailwind CSS (Framework)' 'tailwindcss'
Kur5Npm 'Three.js (3D Rendering Library)' 'three'
Kur5Npm 'Codegraph' '@colbymchenry/codegraph'
Kur5Npm 'morluto/rea' 'rea-agents'
Kur5Pip 'MemZero' 'mem0ai'
Kur5Pip 'Triton' 'triton-windows'
Kur5Pip 'CLI-Hub' 'cli-anything-hub'
Kur5Pip 'Fish Audio' 'fish-audio-sdk'
Kur5Pip 'Brotli' 'brotli'
Kur5Pip 'Stan' 'cmdstanpy'  # lisans: BSD-3 (stan)
Kur5Pip 'Storm' 'knowledge-storm'
Kur5Pip 'DiffSynth-' 'diffsynth'
Kur5Indir 'nvm' 'https://github.com/coreybutler/nvm-windows/releases/download/v2.0.1/nvm-2.0.1-x64-setup.exe'
Kur5Indir 'RIFE' 'https://github.com/nihui/rife-ncnn-vulkan/releases/download/20221029/rife-ncnn-vulkan-20221029-windows.zip'
Kur5Indir 'Vim' 'https://github.com/vim/vim-win32-installer/releases/download/v9.2.1302/gvim_9.2.1302_x64.exe'  # lisans: Vim License
Kur5Indir 'go toolchain' 'https://go.dev/dl/go1.27.3.windows-amd64.msi'
Kur5Indir 'go version -m' 'https://go.dev/dl/go1.27.3.windows-amd64.msi'
Kur5Indir 'llama-cli' 'https://github.com/ggml-org/llama.cpp/releases/download/b12189/llama-b12189-bin-win-cpu-x64.zip'
Kur5Indir 'rustc' 'https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe'  # lisans: MIT/Apache-2.0
Kur5Skill 'Claude Flow' 'ruvnet/claude-flow' ''
Kur5Skill 'Marketing Skills for AI Agents' 'coreyhaines31/marketingskills' ''
Kur5Skill 'copy-editing' 'coreyhaines31/marketingskills' ''
Kur5Skill 'copywriting' 'coreyhaines31/marketingskills' ''
Kur5Skill 'marketingskills/skills/seo-audit' 'coreyhaines31/marketingskills' ''
Kur5Skill 'Marketing plugin' 'anthropics/knowledge-work-plugins' ''
Kur5Skill 'Official Marketing Plugin' 'anthropics/knowledge-work-plugins' ''
Kur5Skill 'Sales Plugin' 'anthropics/knowledge-work-plugins' ''
Kur5Skill 'Sales plugin (Sales Rep)' 'anthropics/knowledge-work-plugins' ''
Kur5Skill 'Support plugin' 'anthropics/knowledge-work-plugins' ''
Kur5Skill 'customer support plugin' 'anthropics/knowledge-work-plugins' ''
Kur5Skill 'data plugin' 'anthropics/knowledge-work-plugins' ''
Kur5Skill 'Anthropic Marketing plugin' 'anthropics/knowledge-work-plugins' ''
Kur5Skill 'Matt Pocock skills repo' 'mattpocock/skills' ''
Kur5Skill 'Teach' 'mattpocock/skills' ''
Kur5Skill 'setup-matt-docock-skills' 'mattpocock/skills' ''
Kur5Skill 'anthropic-automations-recommender' 'anthropics/claude-plugins-official' ''
Kur5Skill 'claude-md-management' 'anthropics/claude-plugins-official' ''
Kur5Skill 'code-architect' 'anthropics/claude-plugins-official' ''
Kur5Skill 'feature-dev' 'anthropics/claude-plugins-official' ''
Kur5Skill 'telegram@claude-plugins-official' 'anthropics/claude-plugins-official' ''
Kur5Skill 'coleschaffer/copywritingskills-rmbc' 'coleschaffer/copywritingskills-rmbc' ''
Kur5Skill 'gan-evaluator' 'affaan-m/everything-claude-code' ''
Kur5Skill 'get_observations' 'thedotmack/claude-mem' ''
Kur5Skill 'lark-vc-agent' 'larksuite/cli' ''
Kur5Skill 'B-Roll Finder' 'louisedesadeleer/b-roll-finder' ''
Kur5Skill 'firecrawl/firecrawl-workflows' 'firecrawl/firecrawl-workflows' 'skills'  # lisans: ISC
Kur5Skill 'hookify' 'anthropics/claude-plugins-official' 'plugins/hookify'
Kur5Skill 'scrum-sage' 'michalparkola/tapestry-skills-for-claude-code' 'scrum-sage'
Kur5Skill 'agents-sdk-dev' 'anthropics/claude-plugins-official' 'plugins/agent-sdk-dev'
Kur5Skill 'commit-commands' 'anthropics/claude-plugins-official' 'plugins/commit-commands'
Kur5Skill 'geo-crawlers' 'sickn33/agentic-awesome-skills' 'skills/geo-crawlers'
Kur5Skill 'ship-learn-next' 'michalparkola/tapestry-skills-for-claude-code' 'ship-learn-next'
Kur5Skill 'api-and-interface-design' 'addyosmani/agent-skills' 'skills/api-and-interface-design'
Kur5Skill 'schema (coreyhaines31/marketingskills)' 'coreyhaines31/marketingskills' 'skills/schema'
Kur5Skill 'Marketing Psychology' 'coreyhaines31/marketingskills' 'skills/marketing-psychology'
Kur5Skill 'Mattpocock' 'mattpocock/skills' ''
Kur5Skill 'docx' 'anthropics/skills' 'skills/docx'
Kur5Skill 'getagentseal/founder-playbook' 'getagentseal/founder-playbook' ''
Kur5Skill 'PDF (dosya biÃ§imi)' 'anthropics/skills' 'skills/pdf'
Kur5Skill 'public-relations' 'coreyhaines31/marketingskills' 'skills/public-relations'
Kur5Skill 'schema (Corey Haines''in marketingskills projesinde kullanÄ±lan kavram)' 'coreyhaines31/marketingskills' 'skills/schema'
Kur5Skill 'Loopy' 'Forward-Future/loopy' ''
Kur5Skill 'Make Interfaces Feel Better' 'jakubkrehel/make-interfaces-feel-better' ''
Kur5Uv 'GitHub Spec Kit' 'specify-cli --from git+https://github.com/github/spec-kit.git'
Kur5Uv 'OpenHandds' 'openhands'
Kur5Vscode 'Kilo' 'kilocode.Kilo-Code'
Kur5Winget 'Podman' 'RedHat.Podman'
Kur5Winget 'helm' 'Helm.Helm'
Kur5Winget 'C-Sharp' 'Microsoft.DotNet.SDK.10'
Kur5Winget 'CPython' 'Python.Python.3.13'  # lisans: PSF (gh other)
Kur5Winget 'Dart' 'Google.DartSDK'  # lisans: BSD-3
Kur5Winget 'Go' 'GoLang.Go'  # lisans: BSD-3
Kur5Winget 'Go 1.27.1' 'GoLang.Go'  # lisans: BSD-3
Kur5Winget 'Kotlin' 'JetBrains.Kotlin.Compiler'  # lisans: Apache-2.0 (gh spdx yok)
Kur5Winget 'Ninja' 'Ninja-build.Ninja'
Kur5Winget 'Node' 'OpenJS.NodeJS.LTS'  # lisans: MIT-benzeri (gh other)
Kur5Winget 'Node Runtime' 'OpenJS.NodeJS.LTS'  # lisans: MIT-benzeri (gh other)
Kur5Winget 'Node.js 20+' 'OpenJS.NodeJS.LTS'  # lisans: MIT-benzeri (gh other)
Kur5Winget 'PHP' 'PHP.PHP.8.3'  # lisans: BSD-3 (gh)
Kur5Winget 'PHP 8.3' 'PHP.PHP.8.3'  # lisans: BSD-3 (gh)
Kur5Winget 'Postgre' 'PostgreSQL.PostgreSQL.17'  # lisans: PostgreSQL (gh NOASSERTION)
Kur5Winget 'Python 3.10+' 'Python.Python.3.13'  # lisans: PSF (gh other)
Kur5Winget 'Rust' 'Rustlang.Rustup'
Kur5Winget 'WSL' 'Microsoft.WSL'
Kur5Winget 'python3' 'Python.Python.3.13'  # lisans: PSF (gh other)
Kur5Winget 'Node.js <nodejs.org/en>' 'OpenJS.NodeJS.LTS'  # lisans: MIT-benzeri (gh other)
Kur5Winget 'Python <www.python.org>' 'Python.Python.3.13'  # lisans: PSF (gh other)
Kur5Winget 'C# (C-Sharp)' 'Microsoft.DotNet.SDK.10'
Kur5Winget 'Go (programlama dili)' 'GoLang.Go'
Kur5Winget 'Java' 'Microsoft.OpenJDK.21'  # lisans: GPLv2+CE
Kur5Winget 'Microsoft Visual C++ Redistributable' 'Microsoft.VCRedist.2015+.x64'  # lisans: ticari ucretsiz
Kur5Winget 'Microsoft Visual C++ v14 x64 Redistributable' 'Microsoft.VCRedist.2015+.x64'  # lisans: ticari ucretsiz
Kur5Winget 'Zig' 'zig.zig'
Kur5Winget 'Node.js' 'OpenJS.NodeJS.LTS'  # lisans: MIT-benzeri (gh other)
Kur5Winget 'Python' 'Python.Python.3.12'  # lisans: PSF (gh other)
Kur5Indir 'Gradle' 'https://services.gradle.org/distributions/gradle-9.9.0-bin.zip'

# OMER-SOR: AI Breakup Recovery Agent | lisans=none | gh api 200; 0 SKILL.md; lisanssiz
# OMER-SOR: LoopTools | lisans=LGPL-3.0 | gh api 200; fizik kutuphanesi resmi olmayan ayna; LGPL
# OMER-SOR: mmBERT-base | lisans=repo none | HF api 200 (fill-mask); GitHub JHU-CLSP/mmBERT lisanssiz; model lisansi dogrulanmadi
# OMER-SOR: tinyagents | lisans=GPL-3.0 | gh api 200; GPL
# OMER-SOR: Claude Code v2.1.71 | lisans=none | gh api 200; lisans none (ozel); npm @anthropic-ai/claude-code, surum sabitleme Omer karari
# OMER-SOR: Finegrain Image Enhancer | lisans=NOASSERTION | gh api 200; 1 yildiz, lisans belirsiz
# OMER-SOR: hy-wu-edit | lisans=NOASSERTION | gh api 200; lisans belirsiz
# OMER-SOR: skool-platinum | lisans=NOASSERTION | gh api 200; 1 SKILL.md; lisans belirsiz
# OMER-SOR: smtg-ai/claude-squad | lisans=AGPL-3.0 | gh api 200; 8744 yildiz; AGPL
# OMER-SOR: oh-my-openagent | lisans=NOASSERTION | SKILL.md=61; git tree sayimi lisans belirsiz
# OMER-SOR: connect-apps-plugin | lisans=none | SKILL.md=864; git tree sayimi lisans bos; 864 klasorden secim Omer
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): 0NE API | RELEASE | songquanpeng/one-api
# OMER-SOR: AtomicParsley | lisans=GPL-2.0 | AtomicParsleyWindows.zip (<1MB) var; GPL
# OMER-SOR: Eigent | lisans=Apache-2.0 | GUI uygulama Eigent.Setup.1.0.7.exe=1035MB
# OMER-SOR: NaiboWang/EasySpider | lisans=AGPL-3.0 | GUI uygulama 7z=361MB; AGPL
# OMER-SOR: boykopovar/AnyPs5 | lisans=GPL-2.0 | prx-windows zip=91MB; GPL; PS5 jailbreak araci
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): nvm-windows | RELEASE | coreybutler/nvm-windows nvm-2.0.1-x64-setup.exe (10MB) ; WINGET CoreyButler.NVMf
# OMER-SOR: storytold/artcraft | lisans=Apache-2.0 | GUI uygulama ArtCraft_0.41.1_x64-setup.exe=40MB
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): youtube-dl | RELEASE | ytdl-org/youtube-dl youtube-dl.exe (7MB)
# OMER-SOR: Chocolatey | lisans=NOASSERTION | sistem paket yoneticisi, yonetici hakki; lisans GH'ta belirsiz
# OMER-SOR: FilmCraft CLI | lisans=Apache-2.0 | repo aciklamasi: dogrusal olmayan video editoru (GUI); portable zip var
# OMER-SOR: Orchestrator.inc (agent-orchestrator) | lisans=Apache-2.0 | Electron GUI Setup.0.14.10.exe=183MB
# OMER-SOR: ldid-procursus | lisans=AGPL-3.0 | AGPL
# OMER-SOR: AThevon/genjutsu | lisans=NOASSERTION | lisans belirsiz; v4.1.3
# OMER-SOR: AdaL CLI | lisans=yok | repo lisanssiz
# OMER-SOR: AgentLog | lisans=NOASSERTION | ad belirsiz (agentlogs/agentlog), lisans belirsiz
# OMER-SOR: BFXR | lisans=yok | release/paket yok, lisanssiz; yalniz kaynak klon
# OMER-SOR: BlenderGIS | lisans=GPL-3.0 | GPL
# OMER-SOR: Claude Toolkit | lisans=MIT | iki farkli proje, kaynak belirsiz
# OMER-SOR: ComfyUI-HunyuanVideo | lisans=yok | ComfyUI+GPU gerekir; lisanssiz; resmi Tencent repo ayri
# OMER-SOR: ComfyUI-HunyuanVideoWrapper | lisans=yok | ComfyUI+GPU gerekir; lisanssiz
# OMER-SOR: Claudex Loop | lisans=NOASSERTION | lisans belirsiz
# OMER-SOR: Filetree | lisans=yok | lisanssiz
# OMER-SOR: Hardflow | lisans=GPL-3.0 | Blender addon; GPL
# OMER-SOR: LLM Council | lisans=yok | lisanssiz; alt: tenfoldmarc/llm-council-skill
# OMER-SOR: Lago | lisans=AGPL-3.0 | AGPL; sunucu/docker
# OMER-SOR: LingoForge | lisans=yok | 3 yildiz, lisanssiz, kaynak belirsiz
# OMER-SOR (betik satiri yok: yöntem CARGO betikte desteklenmiyor): Ratatui | CARGO | crate ratatui 0.30.2 (static.crates.io 200)
# OMER-SOR: Scoop | lisans=NOASSERTION | sistem paket yoneticisi, uzaktan betik
# OMER-SOR: TARS | lisans=Apache-2.0 | ad belirsiz: Agent TARS ile ayni mi
# OMER-SOR: Whisker | lisans=MIT | ad belirsiz; bu repo AD saldiri araci, release yok
# OMER-SOR: Wifite | lisans=yok | Linux, lisanssiz, saldiri araci
# OMER-SOR: harness2-demo | lisans=yok | gh api repo 200, license.spdx_id null
# OMER-SOR: hbot CLI | lisans=NOASSERTION | gh api repo 200; son push 2022-03; ipucu eslesmesi belirsiz
# OMER-SOR: margin-analyzer | lisans=yok | gh api repo 200 license null; PyPI margin-analyzer 404
# OMER-SOR: rtmpdump | lisans=GPL-2.0 | gh api repo 200 GPL-2.0; Windows hazir release yok, kaynaktan derleme
# OMER-SOR: BU Bench | lisans=yok | gh api repo 200 license null; BU Bench V2.1; API anahtari/ucretli kosu
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): DataviewJS | RELEASE | blacksmithgu/obsidian-dataview (release 0.5.70: main.js,manifest.json,styles.css
# OMER-SOR: Devin CLI | lisans=proprietary (cognition.ai ToS) | npm registry 200 v3000.12.17 'Devin for Terminal'; lisans SEE LICENSE ToS
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Kafka | RELEASE | https://downloads.apache.org/kafka/4.2.2/
# OMER-SOR: Poppler | lisans=GPL (poppler) | HTTP 200 asset; GPL -> karar Omer
# OMER-SOR: Stable Diffusion Forge | lisans=AGPL-3.0 | gh api repo 200 AGPL-3.0; model agirliklari >2 GB
# OMER-SOR: Vane (Perplexica) | lisans=MIT | gh api repo 200 MIT; sunucu uygulamasi (Docker/Node, API anahtari) -> uygulama
# OMER-SOR: crap4clj | lisans=yok | gh contents: SKILL.md,README.md,deps.edn; license null
# OMER-SOR: docx/pptx/xlsx | lisans=proprietary (skill LICENSE.txt) | gh contents: LICENSE.txt,SKILL.md,scripts her uc klasorde; repo license null
# OMER-SOR: ffprobe | lisans=GPL | HTTP 200 asset (ffprobe.exe paketin icinde); GPL build; winget Gyan.FFmpeg OLCULEMEDI (zaman asimi)
# OMER-SOR: Algorithmic Art | lisans=repo NOASSERTION (skill-bazli, kaynak-ac | gh contents: algorithmic-art,pdf,pptx,xlsx var; lisans belirsiz
# OMER-SOR: Chromium | lisans=BSD-3 | kaynak agaci devasa (>2GB); Chrome zaten var
# OMER-SOR: Graphite | lisans=Apache-2.0 | kalem belirsiz: graphite-web (metrik) mi Graphite stacked-PR CLI mi
# OMER-SOR: Lua | lisans=gh lisans yok | mirror, lisans bilgisi yok
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Luau | RELEASE | luau-lang/luau (luau-windows.zip)
# OMER-SOR: MariaDB | lisans=GPL-2.0 | GPL
# OMER-SOR: Maxun | lisans=AGPL-3.0 | AGPL
# OMER-SOR: Meta Bind | lisans=GPL-3.0 | GPL
# OMER-SOR: Mongo | lisans=SSPL (gh lisans yok) | SSPL
# OMER-SOR: MySQL | lisans=GPL | GPL
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Ocis | RELEASE | owncloud/ocis
# OMER-SOR: PERL | lisans=gh lisans yok (Artistic/GPL) | lisans belirsiz
# OMER-SOR (betik satiri yok: paket adı yok): Pest | COMPOSER | composer require pestphp/pest
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Pinokio | RELEASE | pinokiocomputer/pinokio
# OMER-SOR: Postkog | lisans=gh lisans yok | kalem yazimi Postkog belirsiz; self-host agir
# OMER-SOR: S3-compatible storage | lisans=AGPL-3.0 | arsiv + AGPL
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Servo | RELEASE | servo/servo
# OMER-SOR: Web | lisans=MIT | kalem Web belirsiz, kaynak yonerge repo
# OMER-SOR: karpathy-guidelines | lisans=gh lisans yok | karpathy/guidelines yok; baska repoda skills/ var, lisanssiz
# OMER-SOR: pdf | lisans=repo NOASSERTION (skill-bazli, kaynak-ac | gh contents: algorithmic-art,pdf,pptx,xlsx var; lisans belirsiz
# OMER-SOR: pptx | lisans=repo NOASSERTION (skill-bazli, kaynak-ac | gh contents: algorithmic-art,pdf,pptx,xlsx var; lisans belirsiz
# OMER-SOR: xlsx | lisans=repo NOASSERTION (skill-bazli, kaynak-ac | gh contents: algorithmic-art,pdf,pptx,xlsx var; lisans belirsiz
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Codebase Memory Graph <localhost:9749> | RELEASE | DeusData/codebase-memory-mcp
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Codebase Memory UI <localhost:9749> | RELEASE | DeusData/codebase-memory-mcp
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): CodebaseMemory <DeusData/codehasememory-mcp> | RELEASE | DeusData/codebase-memory-mcp
# OMER-SOR: FLOW <AgriciDaniel/flow> | lisans=other | playbook/doc deposu, lisans other
# OMER-SOR: OneVOneJev <emrickgarrett/OneVoneJev> | lisans=gh lisans yok | lisanssiz/kucuk demo
# OMER-SOR: Telegram <https://t.me/+n> | lisans=GPL-3.0 | GPL
# OMER-SOR: Terraform <Terraform.io> | lisans=BUSL (gh other) | BUSL
# OMER-SOR: Terraform.io <Terraform.io> | lisans=BUSL (gh other) | BUSL
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): ink <80-days.ink> | RELEASE | inkle/ink (inklecate_windows.zip)
# OMER-SOR: baocutreadme | lisans=NOASSERTION | lisans belirsiz
# OMER-SOR: DeepDiagram | lisans=AGPL-3.0 | AGPL
# OMER-SOR: Dextopreadme | lisans=GPL-3.0 | GPL, Android
# OMER-SOR: evolution-goreadme | lisans=other | lisans other
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): mcptoonreadme | RELEASE | activeing123/mcptoon (mcptoon-0.8.34-win-x64.zip)
# OMER-SOR: OpenChatCut | lisans=AGPL-3.0 | AGPL
# OMER-SOR: pentest-agentsfreadme | lisans=gh lisans yok | lisanssiz + ofansif arac
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): plexoreadme | RELEASE | anmolkapil/plexo (plexo-1.0.0-rc.15-setup.exe)
# OMER-SOR: task-coe | lisans=other | arastirma kodu, lisans other
# OMER-SOR: netflix-clone | lisans=gh lisans yok | lisanssiz/kucuk demo
# OMER-SOR: CUDA | lisans=NVIDIA EULA | >2 GB, ticari
# OMER-SOR: CUDA 12.8 | lisans=NVIDIA EULA | >2 GB, ticari
# OMER-SOR: DaVinci | lisans=ticari | kaynak yok; >2GB ticari uygulama
# OMER-SOR: Hyper-V | lisans= | sistem ozelligi, yeniden baslatma, WSL2/VM cakisma riski
# OMER-SOR: LaTeX | lisans=LPPL | kaynak yok; buyuk dagitim (MiKTeX/TeX Live), Omer secimi
# OMER-SOR: MSSQL | lisans=ticari | kaynak yok; buyuk sunucu kurulumu
# OMER-SOR: MSVC | lisans=ticari | kaynak yok; Build Tools >2GB
# OMER-SOR: OpenClaw | lisans=MIT | gh api: MIT, "The AI that really does things"; kaynak sutunu bos, ad eslesmesi; kalem UYGULAMA
# OMER-SOR: Swift | lisans=Apache-2.0 | repo 1.4GB; Windows toolchain + VS bagimliligi buyuk (>2GB olasi) -> Omer karar
# OMER-SOR: SwiftPM | lisans=Apache-2.0 | bagimsiz kurulmaz, Swift toolchain parcasi
# OMER-SOR: T3 Code | lisans=MIT | kaynak create-t3-app (T3 Stack iskeleti) kalem degil; pingdotgg/t3code var (MIT, aciklama bos), hangisi kasted
# OMER-SOR: WSL2 | lisans=MIT | sistem ozelligi, yeniden baslatma gerekir
# OMER-SOR: WebKit | lisans=BSD/LGPL (gh spdx yok) | repo 13GB (>2GB), tarayici motoru kaynagi, kurulabilir urun degil
# OMER-SOR: Windsurf | lisans=ticari | kaynak yok; masaustu IDE, kapali lisans; winget OLCULEMEDI
# OMER-SOR: farion1231/cc-switch | lisans=MIT | v4.0.27 Windows.msi asset var; masaustu uygulama -> Omer karar
# OMER-SOR: ARES | lisans= | kaynak yok; hafiza: saldiri araci kurulumu classifier engelli, Omer onayi gerekir
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Codebase Memory Graph | RELEASE | DeusData/codebase-memory-mcp (releases/latest v0.12.1)
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Codebase Memory UI | RELEASE | DeusData/codebase-memory-mcp (releases/latest v0.12.1)
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): CodebaseMemory | RELEASE | DeusData/codebase-memory-mcp (releases/latest v0.12.1)
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Herdr | RELEASE | herdrdev/herdr (v0.9.5 herdr-windows-x86_64.zip)
# OMER-SOR: OneVOneJev | lisans=LISANSSIZ | ayni urun (1v1 quickscope arena, Three.js) ama lisans yok
# OMER-SOR: Swagger.io (API Design Framework) | lisans=Apache-2.0 | kaynak swagger-api/swagger-ui = dokuman goruntuleyici, API tasarim cercevesi (Editor/Hub) degil; npm swagger-u
# OMER-SOR: Telegram (Messaging Platform) | lisans=GPL-3.0 | tdesktop GPL-3.0; masaustu uygulama
# OMER-SOR: Terraform (Infrastructure as Code) | lisans=BUSL-1.1 (gh NOASSERTION) | hashicorp/terraform lisansi MIT/Apache degil (BUSL)
# OMER-SOR: Terraform.io (alternatif URL) | lisans=BUSL-1.1 (gh NOASSERTION) | hashicorp/terraform lisansi MIT/Apache degil (BUSL)
# OMER-SOR (betik satiri yok: asset URL'si yok (yalnız repo/dizin)): Ink (Inkle) | RELEASE | inkle/ink releases/latest v1.2.1 inklecate_windows.zip
# OMER-SOR: releases | lisans=AGPL-3.0 | headless browser, AGPL -> kural geregi Omer
# OMER-SOR: CPM-0.5B | lisans=OLCULEMEDI (HF lisans okunmadi) | HF API 200: uc openbmb *CPM-0.5B modeli var, hangisi belirsiz
# OMER-SOR: Agent CLI | lisans=AGPL-3.0 | npm view: postiz AGPL; genel ad, ayni mi emin degil
# OMER-SOR: Forgejo | lisans=OLCULEMEDI | Codeberg API 503 iki denemede; git forge sunucusu (CLI degil), puan 0.2
# OMER-SOR: ai-second-brain | lisans=MIT | repo var, 5206 yildiz, aktif; ad farkli, kalemle ayni mi belirsiz
# OMER-SOR: bug-hunter | lisans=MIT | repo var 5476 yildiz; ad farkli + saldirgan guvenlik paketi (82 skill)
# OMER-SOR: eval-viewer | lisans=NONE | gh api tree: dizin var (generate_review.py, viewer.html) ama repo lisanssiz; skill-creator parcasi
# OMER-SOR: reverse engineer anything repo | lisans=NONE | gh api: aciklama birebir "Reverse Engineer Anything Repo", 0 yildiz, lisanssiz; anthropic-skills:reverse-engin
# OMER-SOR: sqlite3 | lisans=OLCULEMEDI | winget show/search 25-40sn takildi, bos cikti; yerelde sqlite3 yok (command -v); sistem CLI
# OMER-SOR: tree | lisans=OLCULEMEDI | winget bos cikti; yerelde tree yok; Windows tree.com yerlesik
# OMER-SOR: wget | lisans=OLCULEMEDI | winget bos cikti; yerelde wget yok; curl mevcut
# OMER-SOR: xelatex | lisans=OLCULEMEDI | winget bos cikti; yerelde xelatex yok; TeX dagitimi >2GB olabilir
# OMER-SOR: Apowerui MCP toolkit | lisans=NOASSERTION (GPL-3.0 uygulama + MIT Soli | repo aciklamasi "A powerful MCP toolkit for coding" = kalem (Apowerui = A powerful); 31174 yildiz; GPL kosulu 
# OMER-SOR: Chatterbox | chatterbox-tts kütüphane (entry_points yok), torch/GB indirme: venv + uv pip; Ömer karar
# OMER-SOR: MLSharp | PyPI 'sharp' başka paket; doğrusu git+https://github.com/apple-aiml-research/ml-sharp, lisans NOASSERTION
# OMER-SOR: pgnx | install.js yalnız Node 22 (ABI 127) prebuild; makinede Node 24
