param([switch]$Deneme)
# KURULUM-TESHIS: Omer kosar. -Deneme kurulum yapmaz, yalniz ne yapacagini yazar.
$ErrorActionPreference="Continue"
$sonuc="$PSScriptRoot/../rapor/kurulum-omer-sonuc.tsv"
if(-not (Test-Path $sonuc)){"kalem`tyontem`tdurum`tnot" | Set-Content $sonuc -Encoding utf8}
$sk="$env:USERPROFILE\.claude\skills"
function Kayit($k,$y,$d,$n){ "$k`t$y`t$d`t$n" | Add-Content $sonuc -Encoding utf8; Write-Host "$d $y $k" }
function Skill($k,$kok,$alt){ foreach($a in $alt){ $src=Join-Path $kok $a; $ad=Split-Path $a -Leaf; if(-not $a){$ad=Split-Path $kok -Leaf; $src=$kok}
  $dst=Join-Path $sk $ad; if(Test-Path $dst){Kayit $k SKILL ZATEN $ad;continue}
  if(-not (Test-Path "$src\SKILL.md")){Kayit $k SKILL HATA "SKILL.md yok: $a";continue}
  if($Deneme){Kayit $k SKILL DENEME "$src -> $dst";continue}
  try{Copy-Item $src $dst -Recurse -ErrorAction Stop;Kayit $k SKILL KURULDU $ad}catch{Kayit $k SKILL HATA $_.Exception.Message}}}
function Npm($k,$p){ if($Deneme){Kayit $k NPM DENEME "npm i -g $p";return}
  npm.cmd i -g $p 2>&1 | Out-Null; if($LASTEXITCODE -eq 0){Kayit $k NPM KURULDU $p}else{Kayit $k NPM HATA "exit $LASTEXITCODE"}}
function Uv($k,$p){ if($Deneme){Kayit $k UV DENEME "uv tool install $p";return}
  $uvexe=(Get-Command uv.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
  if(-not $uvexe){Kayit $k UV HATA "uv.exe bulunamadi";return}
  & $uvexe tool install $p 2>&1 | Out-Null; if($LASTEXITCODE -eq 0){Kayit $k UV KURULDU $p}else{Kayit $k UV HATA "exit $LASTEXITCODE"}}

# AYIR AYIR-KLON-YOK: AI Breakup Recovery Agent
# AYIR AYIR-RELEASE: 0NE API
# AYIR AYIR-YOL-YOK: 9Router
Uv 'AI Slop Detector' 'ai-slop-detector'
Skill 'AI Data Analysis Agent' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Shubhamsaboo__awesome-llm-apps' @('agent_skills/advisor-orchestrator-worker','agent_skills/commit-archaeologist','agent_skills/dependency-doctor','agent_skills/first-reader','agent_skills/project-graveyard','agent_skills/scope-creep-detector','agent_skills/thinking-out-loud','generative_ui_agents/ai-mcp-app-builder/apps/mcp-use-server/.agent/skills/chatgpt-app-builder','generative_ui_agents/ai-mcp-app-builder/apps/mcp-use-server/.agent/skills/mcp-apps-builder','generative_ui_agents/ai-mcp-app-builder/apps/mcp-use-server/.agent/skills/mcp-builder')
# AYIR AYIR-YOL-YOK: AThevon/genjutsu
# AYIR AYIR-YOL-YOK: AgentCouncil
# AYIR AYIR-YOL-YOK: AdaL CLI
# AYIR AYIR-YOL-YOK: AgentLog
# AYIR AYIR-YOL-YOK: Agent TARS
# AYIR AYIR-RELEASE: AtomicParsley
# OMER-SOR (1,56 GB, kurulmaz): Skill 'Atomic Chat' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\AtomicBot-ai__Atomic-Chat' @('src-tauri/resources/agent-skills/apple-calendar','src-tauri/resources/agent-skills/apple-notes','src-tauri/resources/agent-skills/apple-reminders','src-tauri/resources/agent-skills/audio-transcribe','src-tauri/resources/agent-skills/currency','src-tauri/resources/agent-skills/docker','src-tauri/resources/agent-skills/ffmpeg','src-tauri/resources/agent-skills/github','src-tauri/resources/agent-skills/gog-workspace','src-tauri/resources/agent-skills/imagemagick','src-tauri/resources/agent-skills/notion','src-tauri/resources/agent-skills/obsidian','src-tauri/resources/agent-skills/pandoc','src-tauri/resources/agent-skills/pdf','src-tauri/resources/agent-skills/skill-creator','src-tauri/resources/agent-skills/wikipedia','src-tauri/resources/agent-skills/wttr-weather','src-tauri/resources/agent-skills/xlsx')
Uv 'AutoResearchClaw' 'researchclaw'
# AYIR AYIR-YOL-YOK: B-Roll Finder
# AYIR AYIR-YOL-YOK: BFXR
# AYIR AYIR-YOL-YOK: BlenderGIS
# AYIR AYIR-KLON-YOK: CLAUDE HQ
# AYIR AYIR-KLON-YOK: ChatGPT MD
Uv 'Chatterbox' 'chatterbox-tts'
# AYIR AYIR-TOPLU: Claude Flow
# AYIR AYIR-YOL-YOK: Claude Toolkit
# AYIR AYIR-YOL-YOK: Claude Token Monitor
# AYIR AYIR-YOL-YOK: ComfyUI-HunyuanVideo
# AYIR AYIR-YOL-YOK: Claudex Loop
# AYIR AYIR-YOL-YOK: ComfyUI-HunyuanVideoWrapper
Npm 'Command Code' 'command-code'
# AYIR AYIR-YOL-YOK: Coucou (Louis-CFM/coucou)
Npm 'EditorConfig' 'editorconfig'
# AYIR AYIR-RELEASE: Eigent
# AYIR AYIR-YOL-YOK: Filetree
Uv 'Foreman' 'foreman-orchestrator'
Uv 'Free Claude Code Repo' 'free-claude-code'
# AYIR AYIR-YOL-YOK: FilaCheck
# AYIR AYIR-KLON-YOK: FrontierAgent
# AYIR AYIR-YOL-YOK: Ghostty
# AYIR AYIR-YOL-YOK: Gradle
# AYIR AYIR-YOL-YOK: Grok Build
# AYIR AYIR-KLON-YOK: HIA (Health Insights Agent)
# AYIR AYIR-KLON-YOK: Hermes voice agent
# AYIR AYIR-YOL-YOK: Hardflow
# AYIR AYIR-YOL-YOK: Homebrew (brew)
Uv 'LEANN' 'leann'
# AYIR AYIR-YOL-YOK: LLM Council
# AYIR AYIR-YOL-YOK: Lago
# AYIR AYIR-YOL-YOK: LingoForge
# AYIR AYIR-KLON-YOK: LoopTools
# AYIR AYIR-KLON-YOK: Luma Agents
Uv 'MCP Bridge' 'mcp-bridge'
# AYIR AYIR-YOL-YOK: MemZero
Uv 'MetaClaw' 'aiming-metaclaw'
# AYIR AYIR-KLON-YOK: Mobbin MCP
# AYIR AYIR-YOL-YOK: NVIDIA Kimodo
# AYIR AYIR-RELEASE: NaiboWang/EasySpider
Uv 'Pipecat CLI' 'pipecat-ai-cli'
# AYIR AYIR-KLON-YOK: Pocket TTS
# AYIR AYIR-RELEASE: Podman
# AYIR AYIR-YOL-YOK: Ratatui
# AYIR AYIR-YOL-YOK: Rector
# AYIR AYIR-YOL-YOK: Scoop
# AYIR AYIR-YOL-YOK: Sealos
# AYIR AYIR-KLON-YOK: SkillClaw
# AYIR AYIR-YOL-YOK: Slurm
# AYIR AYIR-YOL-YOK: TARS
# AYIR AYIR-YOL-YOK: Triton
# AYIR AYIR-YOL-YOK: Valkey
# AYIR AYIR-YOL-YOK: Whisker
# AYIR AYIR-YOL-YOK: Wifite
# AYIR AYIR-YOL-YOK: agency-agents (msitarzewski/agency-agents)
# AYIR AYIR-RELEASE: boykopovar/AnyPs5
# AYIR AYIR-YOL-YOK: bilawalsidhu/godseyeview
Npm 'claude-trace' '@mariozechner/claude-trace'
# AYIR AYIR-YOL-YOK: comfy-reshoot
# AYIR AYIR-KLON-YOK: codex-computer-use
Skill 'earthtojake/text-to-cad' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\earthtojake__text-to-cad' @('skills/bambu-labs','skills/cad','skills/dfam-check','skills/dfm','skills/dxf','skills/engineering-drawing','skills/gcode','skills/sdf','skills/sendcutsend','skills/srdf','skills/step-parts','skills/urdf')
# AYIR AYIR-YOL-YOK: dnf
# AYIR AYIR-YOL-YOK: firecrawl/firecrawl-workflows
# AYIR AYIR-KLON-YOK: fixai
# AYIR AYIR-YOL-YOK: gVisor
# AYIR AYIR-YOL-YOK: harness2-demo
# AYIR AYIR-YOL-YOK: hbot CLI
# AYIR AYIR-YOL-YOK: hookify
# AYIR AYIR-RELEASE: helm
# AYIR AYIR-RELEASE: codspeed
# AYIR AYIR-KLON-YOK: letta-ai/claude-subconscious
# AYIR AYIR-YOL-YOK: linkedin-automator
# AYIR AYIR-YOL-YOK: margin-analyzer
# AYIR AYIR-YOL-YOK: mattgierhart/PRD-driven-context-engineering
# AYIR AYIR-KLON-YOK: mmBERT-base
# AYIR AYIR-RELEASE: nvm-windows
# AYIR AYIR-YOL-YOK: nvm
# AYIR AYIR-TOPLU: oh-my-openagent
# AYIR AYIR-YOL-YOK: paru
Npm 'pgnx' 'pgnx'
# AYIR AYIR-YOL-YOK: oMLX
# AYIR AYIR-KLON-YOK: reel-factory
# AYIR AYIR-YOL-YOK: scrum-sage
# AYIR AYIR-YOL-YOK: rtmpdump
# AYIR AYIR-RELEASE: storytold/artcraft
# AYIR AYIR-YOL-YOK: superlite
# AYIR AYIR-KLON-YOK: tinyagents
# AYIR AYIR-YOL-YOK: whatsapp-rust
# AYIR AYIR-RELEASE: youtube-dl
# AYIR AYIR-YOL-YOK: Antigravity SDK
Npm '21st Day MCP Connector' '@21st-dev/cli'
Npm '21st Dev MCP' '@21st-dev/cli'
Npm '21st MCP' '@21st-dev/cli'
# AYIR AYIR-KLON-YOK: AI Travel Agent (Local & Cloud)
# AYIR AYIR-YOL-YOK: Agent Client
# AYIR AYIR-YOL-YOK: BU Bench
# AYIR AYIR-YOL-YOK: CLI-Hub
# AYIR AYIR-RELEASE: Chocolatey
# AYIR AYIR-KLON-YOK: Claude Code v2.1.71
# AYIR AYIR-YOL-YOK: Clawed Code Setup
# AYIR AYIR-KLON-YOK: Creative-Ad Skill
# AYIR AYIR-YOL-YOK: DataviewJS
# AYIR AYIR-YOL-YOK: Devin CLI
# AYIR AYIR-RELEASE: FilmCraft CLI
# AYIR AYIR-KLON-YOK: Finegrain Image Enhancer
# AYIR AYIR-KLON-YOK: Firecrawl MCP
# AYIR AYIR-KLON-YOK: Firecrawl MCP Server
# AYIR AYIR-YOL-YOK: Fish Audio
# AYIR AYIR-KLON-YOK: Flux Kontext
# AYIR AYIR-KLON-YOK: GNU make
# AYIR AYIR-YOL-YOK: Kafka
Skill 'Kilo Code' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Kilo-Org__kilocode' @('.kilo/skills/chart','.kilo/skills/gh-issues','.kilo/skills/icon-jetbrains','.kilo/skills/icon-vscode','.kilo/skills/jetbrains-arch','.kilo/skills/jetbrains-cli-pin','.kilo/skills/jetbrains-dev','.kilo/skills/jetbrains-sandbox','.kilo/skills/jetbrains-session','.kilo/skills/jetbrains-ui','.kilo/skills/kilocode-merge-minimizer','.kilo/skills/pr-track-v1','.kilocode/skills/vscode-visual-regression','.opencode/skills/effect','.opencode/skills/rtl-aware-development','packages/opencode/test/fixture/skills/agents-sdk','packages/opencode/test/fixture/skills/cloudflare')
Npm 'Lint' '@shadcn/lint'
# AYIR AYIR-KLON-YOK: Local REST API with MCP
Uv 'MLSharp' 'sharp'
# AYIR AYIR-TOPLU: Marketing Skills for AI Agents
# AYIR AYIR-TOPLU: Marketing plugin
# AYIR AYIR-TOPLU: Matt Pocock skills repo
Uv 'Mempalus' 'mempalace'
Skill 'Official Anthropic Skill Pack' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\anthropics__skills' @('template','skills/academy-guide','skills/algorithmic-art','skills/brand-guidelines','skills/canvas-design','skills/claude-api','skills/discernment-nudge','skills/doc-coauthoring','skills/docx','skills/frontend-design','skills/internal-comms','skills/mcp-builder','skills/pdf','skills/pptx','skills/skill-creator','skills/slack-gif-creator','skills/theme-factory','skills/web-artifacts-builder','skills/webapp-testing','skills/xlsx')
Skill 'Official GSAP Skills' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\greensock__gsap-skills' @('skills/gsap-core','skills/gsap-frameworks','skills/gsap-performance','skills/gsap-plugins','skills/gsap-react','skills/gsap-scrolltrigger','skills/gsap-timeline','skills/gsap-utils')
# AYIR AYIR-TOPLU: Official Marketing Plugin
# AYIR AYIR-RELEASE: Orchestrator.inc (agent-orchestrator)
# AYIR AYIR-YOL-YOK: Osaurus
Npm 'Oxfmt' 'oxfmt'
Skill 'Personal Agent Proxy' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\personalagentproxy__proxy' @('skills/addressing-pr-feedback','skills/creating-pr','skills/reviewing-pr-feedback','skills/skill-authoring','skills/writing-result-code')
Skill 'Pipecat Skills' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\pipecat-ai__skills' @('skills/deploy','skills/init','skills/talk')
Skill 'Playwright MCP (playwright-mcp)' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\microsoft__playwright-mcp' @('.claude/skills/playwright-triage')
# AYIR AYIR-YOL-YOK: Poppler
# AYIR AYIR-KLON-YOK: Post Strategist
# AYIR AYIR-YOL-YOK: RIFE
Skill 'Remotion Inside Claude Code' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\remotion-dev__skills' @('skills/remotion-best-practices','skills/remotion-captions','skills/remotion-create','skills/remotion-docs','skills/remotion-interactivity','skills/remotion-maps','skills/remotion-markup','skills/remotion-multimedia','skills/remotion-render','skills/remotion-saas','skills/remotion-studio','skills/remotion-upgrade')
Npm 'Remotion Lambda' '@remotion/lambda'
Skill 'Remotion ajan becerileri' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\remotion-dev__skills' @('skills/remotion-best-practices','skills/remotion-captions','skills/remotion-create','skills/remotion-docs','skills/remotion-interactivity','skills/remotion-maps','skills/remotion-markup','skills/remotion-multimedia','skills/remotion-render','skills/remotion-saas','skills/remotion-studio','skills/remotion-upgrade')
Skill 'Remotion becerileri' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\remotion-dev__skills' @('skills/remotion-best-practices','skills/remotion-captions','skills/remotion-create','skills/remotion-docs','skills/remotion-interactivity','skills/remotion-maps','skills/remotion-markup','skills/remotion-multimedia','skills/remotion-render','skills/remotion-saas','skills/remotion-studio','skills/remotion-upgrade')
Skill 'Remove AI Slop' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\manavmishra__ZeroSlop' @('.','distribution/plugins/zero-slop/skills/zero-slop','skills/zero-slop')
# AYIR AYIR-TOPLU: Sales Plugin
# AYIR AYIR-TOPLU: Sales plugin (Sales Rep)
Uv 'ScriptCreatorGraph' 'scrapegraphai'
Npm 'ScrollSmoother' 'gsap'
Skill 'Skill Geliştiren Skill' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\anthropics__skills' @('template','skills/academy-guide','skills/algorithmic-art','skills/brand-guidelines','skills/canvas-design','skills/claude-api','skills/discernment-nudge','skills/doc-coauthoring','skills/docx','skills/frontend-design','skills/internal-comms','skills/mcp-builder','skills/pdf','skills/pptx','skills/skill-creator','skills/slack-gif-creator','skills/theme-factory','skills/web-artifacts-builder','skills/webapp-testing','skills/xlsx')
# AYIR AYIR-TOPLU: Skill Spectre
# AYIR AYIR-YOL-YOK: Stable Diffusion Forge
# AYIR AYIR-TOPLU: Support plugin
# AYIR AYIR-KLON-YOK: TARS (Agent TARS)
# AYIR AYIR-YOL-YOK: Tail
Skill 'Taste Skill v2 Beta' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__taste-skill' @('skills/taste-skill')
# AYIR AYIR-TOPLU: Teach
# AYIR AYIR-KLON-YOK: The Hormozi Brain Toolkit for Claude Code
# AYIR AYIR-KLON-YOK: Tokens Studio
# AYIR AYIR-YOL-YOK: TrainLLMFromScratch
Skill 'Tweetclaw.skill' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Xquik-dev__tweetclaw' @('skills/tweetclaw')
Skill 'Türkçe yazı skill' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\ozgurbuluta__turkce-yazi-yazma' @('skills/turkce-yazi')
Skill 'Türkçe yazı skill''i (turkce-yazi.zip)' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\ozgurbuluta__turkce-yazi-yazma' @('skills/turkce-yazi')
Skill 'UGC content skill' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\kofiowusuai-lab__ugc-skills' @('skills/ugc-ad-strategist','skills/ugc-device-screen','skills/ugc-minimax-mode','skills/ugc-video-producer','skills/ugc-vision-referee')
Skill 'UGC generator skill' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\kofiowusuai-lab__ugc-skills' @('skills/ugc-ad-strategist','skills/ugc-device-screen','skills/ugc-minimax-mode','skills/ugc-video-producer','skills/ugc-vision-referee')
Skill 'UI UX Pro Max Scale' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\nextlevelbuilder__ui-ux-pro-max-skill' @('.claude/skills/banner-design','.claude/skills/brand','.claude/skills/design','.claude/skills/design-system','.claude/skills/slides','.claude/skills/ui-styling','.claude/skills/ui-ux-pro-max','cli/assets/skills/banner-design','cli/assets/skills/brand','cli/assets/skills/design','cli/assets/skills/design-system','cli/assets/skills/slides','cli/assets/skills/ui-styling')
Skill 'UI/UX ProMax (ui-ux-pro-max-skill)' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\nextlevelbuilder__ui-ux-pro-max-skill' @('.claude/skills/banner-design','.claude/skills/brand','.claude/skills/design','.claude/skills/design-system','.claude/skills/slides','.claude/skills/ui-styling','.claude/skills/ui-ux-pro-max','cli/assets/skills/banner-design','cli/assets/skills/brand','cli/assets/skills/design','cli/assets/skills/design-system','cli/assets/skills/slides','cli/assets/skills/ui-styling')
# AYIR AYIR-KLON-YOK: Unet Loader (GGUF)
# AYIR AYIR-YOL-YOK: Vane (Perplexica)
Uv 'Vibe CLI' 'mistral-vibe'
# AYIR AYIR-YOL-YOK: Vim
Npm 'Vite 5' 'vite@5'
Npm 'Vite 7' 'vite@7'
Skill 'Vue and Vite core team skills collection' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\vuejs-ai__skills' @('skills/create-adaptable-composable','skills/vue-best-practices','skills/vue-debug-guides','skills/vue-jsx-best-practices','skills/vue-options-api-best-practices','skills/vue-pinia-best-practices','skills/vue-router-best-practices','skills/vue-testing-best-practices')
# AYIR AYIR-KLON-YOK: agent-radar
# AYIR AYIR-YOL-YOK: agents-sdk-dev
# AYIR AYIR-TOPLU: anthropic-automations-recommender
Skill 'auto-dream' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\grandamenium__dream-skill' @('.')
Skill 'better-auth/better-icons' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\better-auth__better-icons' @('skills')
Uv 'build-error-resolver' 'llm-abstraction'
Skill 'ceo-advisor' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\ultrathink-art__ai-ceo' @('.')
# AYIR AYIR-TOPLU: claude-md-management
Npm 'claude-plugin-lock' 'claude-plugin-lock'
# AYIR AYIR-RELEASE: cmake
# AYIR AYIR-TOPLU: code-architect
# AYIR AYIR-TOPLU: coleschaffer/copywritingskills-rmbc
# AYIR AYIR-YOL-YOK: commit-commands
# AYIR AYIR-TOPLU: connect-apps-plugin
# AYIR AYIR-YOL-YOK: context-inspector
Skill 'continuedev/continue' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\continuedev__continue' @('.claude/skills/docs-style','skills/cn-check')
# AYIR AYIR-TOPLU: copy-editing
# AYIR AYIR-TOPLU: copywriting
# AYIR AYIR-YOL-YOK: crap4clj
# AYIR AYIR-TOPLU: customer support plugin
# AYIR AYIR-TOPLU: data plugin
Npm 'devcontainer' '@devcontainers/cli'
# AYIR AYIR-YOL-YOK: docx/pptx/xlsx
Uv 'e2e-runner' 'llm-abstraction'
Skill 'earshot compare' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__earshot' @('.venv-agir/Lib/site-packages/typer/.agents/skills/typer','skills/earshot','skills/real-sound')
Skill 'earshot critique' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__earshot' @('.venv-agir/Lib/site-packages/typer/.agents/skills/typer','skills/earshot','skills/real-sound')
Skill 'earshot describe' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__earshot' @('.venv-agir/Lib/site-packages/typer/.agents/skills/typer','skills/earshot','skills/real-sound')
Skill 'earshot find' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__earshot' @('.venv-agir/Lib/site-packages/typer/.agents/skills/typer','skills/earshot','skills/real-sound')
Skill 'earshot fit' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__earshot' @('.venv-agir/Lib/site-packages/typer/.agents/skills/typer','skills/earshot','skills/real-sound')
Skill 'earshot forge' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__earshot' @('.venv-agir/Lib/site-packages/typer/.agents/skills/typer','skills/earshot','skills/real-sound')
Skill 'earshot match' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__earshot' @('.venv-agir/Lib/site-packages/typer/.agents/skills/typer','skills/earshot','skills/real-sound')
Skill 'earshot rank' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__earshot' @('.venv-agir/Lib/site-packages/typer/.agents/skills/typer','skills/earshot','skills/real-sound')
Skill 'earshot realness' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__earshot' @('.venv-agir/Lib/site-packages/typer/.agents/skills/typer','skills/earshot','skills/real-sound')
Skill 'earshot timeline' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__earshot' @('.venv-agir/Lib/site-packages/typer/.agents/skills/typer','skills/earshot','skills/real-sound')
# AYIR AYIR-KLON-YOK: execute_sql
# AYIR AYIR-TOPLU: feature-dev
# AYIR AYIR-YOL-YOK: ffprobe
# AYIR AYIR-TOPLU: gan-evaluator
# AYIR AYIR-KLON-YOK: generate_typescript_types
# AYIR AYIR-YOL-YOK: geo-crawlers
# AYIR AYIR-TOPLU: get_observations
# AYIR AYIR-RELEASE: gh (GitHub CLI)
# AYIR AYIR-RELEASE: git add
# AYIR AYIR-RELEASE: git clone
# AYIR AYIR-RELEASE: git commit
# AYIR AYIR-YOL-YOK: go toolchain
# AYIR AYIR-YOL-YOK: go version -m
Npm 'gstack-slug' 'gstack'
Uv 'harness-optimizer' 'llm-abstraction'
# AYIR AYIR-KLON-YOK: hy-wu-edit
# AYIR AYIR-KLON-YOK: inbox-alerts-priority
Npm 'just-scrape' 'just-scrape'
Npm 'lark-cli' '@larksuite/cli'
# AYIR AYIR-TOPLU: lark-vc-agent
# AYIR AYIR-RELEASE: ldid-procursus
Skill 'learn-this' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\michalparkola__tapestry-skills' @('article-extractor','learn-this','scrum-sage','session-log','ship-learn-next','unblock-action','youtube-transcript')
# AYIR AYIR-YOL-YOK: llama-cli
# AYIR AYIR-TOPLU: lln-council
# AYIR AYIR-TOPLU: marketingskills/skills/seo-audit
Skill 'n8n AI Agent Claude Skill' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\czlonkowski__n8n-skills' @('skills/n8n-agents','skills/n8n-binary-and-data','skills/n8n-code-javascript','skills/n8n-code-python','skills/n8n-code-tool','skills/n8n-error-handling','skills/n8n-expression-syntax','skills/n8n-mcp-tools-expert','skills/n8n-multi-instance','skills/n8n-node-configuration','skills/n8n-self-hosting','skills/n8n-subworkflows','skills/n8n-validation-expert','skills/n8n-workflow-patterns','skills/using-n8n-mcp-skills')
Skill 'n8n Agent Builder Skill' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\czlonkowski__n8n-skills' @('skills/n8n-agents','skills/n8n-binary-and-data','skills/n8n-code-javascript','skills/n8n-code-python','skills/n8n-code-tool','skills/n8n-error-handling','skills/n8n-expression-syntax','skills/n8n-mcp-tools-expert','skills/n8n-multi-instance','skills/n8n-node-configuration','skills/n8n-self-hosting','skills/n8n-subworkflows','skills/n8n-validation-expert','skills/n8n-workflow-patterns','skills/using-n8n-mcp-skills')
Skill 'openai/codex-plugin-cc' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\openai__codex-plugin-cc' @('plugins/codex/skills/codex-cli-runtime','plugins/codex/skills/codex-result-handling','plugins/codex/skills/gpt-5-4-prompting')
Npm 'pi coding agent' '@mariozechner/pi-coding-agent'
Skill 'plugin-cc' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\openai__codex-plugin-cc' @('plugins/codex/skills/codex-cli-runtime','plugins/codex/skills/codex-result-handling','plugins/codex/skills/gpt-5-4-prompting')
Skill 'rendercv/rendercv-skill' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\rendercv__rendercv-skill' @('skills/rendercv')
# AYIR AYIR-YOL-YOK: rustc
# AYIR AYIR-TOPLU: setup-matt-docock-skills
# AYIR AYIR-YOL-YOK: ship-learn-next
# AYIR AYIR-KLON-YOK: skool-platinum
# AYIR AYIR-KLON-YOK: smtg-ai/claude-squad
Skill 'static-ad-generator skill' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\creatify-ai__static-ad-concept-generator' @('.')
# AYIR AYIR-TOPLU: telegram@claude-plugins-official
Npm 'tv_health_check' 'tradingview-mcp'
Skill 'unblock-action' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\michalparkola__tapestry-skills-for-claude-code' @('article-extractor','learn-this','scrum-sage','session-log','ship-learn-next','unblock-action','youtube-transcript')
Uv 'xet' 'hf-xet'
# AYIR AYIR-YOL-YOK: zqxwce/tap/vphone-cli
# AYIR AYIR-TOPLU: Anthropic Marketing plugin
Skill 'Anti-Slop Frontend Framework for AI Agents' 'C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste\Leonxlnx__taste-skill' @('skills/taste-skill')
