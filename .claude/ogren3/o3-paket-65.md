## gstack-autoplan
id: k03824 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03824_gstack-autoplan.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · gstack-autoplan
BAŞLIKLAR: 

## omni-github-skills
id: k03897 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03897_omni-github-skills.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · omni-github-skills
BAŞLIKLAR: 

## setup-matt-pocock-skills
id: k04040 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04040_setup-matt-pocock-skills.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · setup-matt-pocock-skills
BAŞLIKLAR: 

## omni-inference
id: k03743 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03743_omni-inference.txt (özgün: C:\Projeler\omer-skills\dist\yukle-7\omniroute-omni-inference.zip!omni-inference/SKILL.md) · 589 satır · araç adları (2): omni-inference · omniroute-omni-inference.zip!omni-inference
BAŞLIKLAR: ## Overview · ## Authentication · ## Endpoints · ### POST /api/v1/chat/completions · ### GET /api/v1/ws · ### POST /api/v1/providers/{provider}/chat/completions · ### POST /api/v1/api/chat · ### POST /api/v1/messages · ### POST /api/v1/messages/count_tokens · ### POST /api/v1/responses · ### POST /api/v1/embeddings · ### POST /api/v1/providers/{provider}/embeddings · ### POST /api/v1/images/generations · ### POST /api/v1/providers/{provider}/images/generations · ### POST /api/v1/audio/speech · ### POST /api/v1/audio/transcriptions · ### POST /api/v1/moderations · ### POST /api/v1/rerank · ### GET /api/v1 · ### GET /api/v1/providers/{provider}/models · ### POST /api/v1/ocr · ### POST /api/v1/audio/translations · ### GET /api/v1/providers/suggested-models · ### GET /api/v1/provider-plugin-manifest · ## Payloads · ## Chat completions · ### Endpoints · ### Discover · ### OpenAI format example · ### Anthropic format example · ### Tool use · ### Reasoning / thinking · ### Errors · ## Image generation · ### Endpoints · ### Discover · ### Generate example · ### Errors · ## Text-to-speech · ### Endpoint · ### Discover · ### Example · ### Voices · ### Errors · ## Speech-to-text · ### Endpoints · ### Discover · ### Example · ### Supported formats · ### Errors · ## Embeddings · ### Endpoint · ### Discover · ### Example · ### Batch input · ### Errors · ## Web search · ### Endpoint · ### Discover · ### Example · ### Parameters · ### Errors · ## Web fetch · ### Endpoint · ### Discover · ###

## claude-hud
id: k01523 · tür: plugin · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01523_claude-hud.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-hud\claude-hud\0.10.0) · 362 satır · araç adları (180): 0.10 · claude-hud · dist/auth.d.ts · dist/auth.js · dist/claude-config-dir.d.ts · dist/claude-config-dir.js · dist/config-reader.d.ts · dist/config-reader.js · dist/config.d.ts · dist/config.js · dist/cost.d.ts · dist/cost.js · dist/daily-cost.d.ts · dist/daily-cost.js · dist/debug.d.ts · dist/debug.js · dist/effort.d.ts · dist/effort.js · dist/external-usage.d.ts · dist/external-usage.js · dist/extra-cmd.d.ts · dist/extra-cmd.js · dist/git-runner.d.ts · dist/git-runner.js · dist/git.d.ts · dist/git.js · dist/i18n/en.d.ts · dist/i18n/en.js · dist/i18n/index.d.ts · dist/i18n/index.js
BAŞLIKLAR: # Claude HUD · ## Install · ## What You See · The default is two lines: · ## How It Works · ## Configuration · ### Options · ### Usage Limits · ### Cost · ### Prompt Cache · ### Jujutsu (jj) · ### Example · ### Auto-Refresh · ### Turning It Off for a Session · ## Security · ## Troubleshooting · ## Requirements · ## Development · ## License · ## Star History

## kurulum-turu-3
id: k03447 · tür: cli · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03447_kurulum-turu-3.txt (özgün: C:\Projeler\omer-skills\tools\kurulum-turu-3.sh) · 242 satır · araç adları (1): kurulum-turu-3
BAŞLIKLAR: # Kurulum turu 3c — tur-3 KUR/KUR-duzeltmeli + anahtarsız ku · # Girdi: docs/kurulumlar/tur3-sonuc-*.tsv, kurulum-sirasi.md · # Kullanım: bash tools/kurulum-turu-3.sh [--kuru]   (--kuru: · # Her adım: kuruluysa atla → kur → doğrula → hata ise yalnız · # MCP env'i ${AD} başvurusudur (değer yazılmaz). Anahtarsız  · # klonla repo sha → KD (pinli SHA'da klon) · # uzaktan betik çeken/çalıştıran dosya (md hariç) varsa şüph · # S|repo|sha   → SKILL.md klasörleri ~/.claude/skills/<ad> · # A|repo|sha|bölümler   → yalnız o üst klasörlerdeki *.md aj · # P|repo|sha|market   → marketplace'teki TÜM plugin'ler (pin · # I|ad@market   (tanımlı resmi marketten tek plugin) · # N|paket@sürüm|bayrak · # U|spec|ad · # M|ad|ENV listesi|komut   ENV: ADI → -e ADI=${ADI}; ADI=değ · # H|ad|url   (uzak http MCP, OAuth) · # K|ad|repo|sha|tür   → C:\Projeler\uygulamalar\<ad> (global · # E · # S: skill kopyası (tur-3 KUR + KUR-duzeltmeli) · # A: agency-agents yalnız engineering/design/security · # P: plugin marketplace · # N: npm (tdd-guard: yalnız CLI, hook bağlanmaz = kapalı/opt · # U: uv · # M: MCP (env ${AD} başvurusu) · # K: kendi ortamında uygulamalar (function-hook mod'ları yal

## skill-agent-topology
id: k03704 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03704_skill-agent-topology.txt (özgün: C:\Projeler\omer-skills\dist\yukle-12-kirmizi\octo-skill-agent-topology.zip!skill-agent-topology/SKILL.md) · 178 satır · araç adları (2): octo-skill-agent-topology.zip!skill-agent-topology · skill-agent-topology
BAŞLIKLAR: # Agent Topology Audit · ## When To Use · ## When Not To Use · ## Inputs · ## Workflow · ### 1. Draw the boundaries · ### 2. Name what is lost at each boundary · ### 3. Name what the boundary buys · ### 4. Compare against the single-expert null · ### 5. Reuse the overlap gate that already exists · ## Provider Or Data Priority · ## Stop Or Checkpoint Rules · ## Output Contract · Report in this order: · ## Verification

## help
id: k03086 · tür: komut · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03086_help.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-code-plugins\ralph-wiggum\1.0.0\commands\help.md) · 126 satır · araç adları (1): help
BAŞLIKLAR: # Ralph Wiggum Plugin Help · ## What is the Ralph Wiggum Technique? · ## Available Commands · ### /ralph-loop <PROMPT> [OPTIONS] · ### /cancel-ralph · ## Key Concepts · ### Completion Promises · ### Self-Reference Mechanism · ## Example · ### Interactive Bug Fix · ## When to Use Ralph · ## Learn More

## anthropics__skills
id: k04080 · tür: repo · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04080_anthropics__skills.txt (özgün: C:\Projeler\.tmp-kurulum6\anthropics__skills) · 98 satır · araç adları (75): anthropics__skills · skills · skills/algorithmic-art/templates/generator_template.js · skills/docx/scripts/__init__.py · skills/docx/scripts/accept_changes.py · skills/docx/scripts/comment.py · skills/docx/scripts/merge_runs.py · skills/docx/scripts/office/helpers/__init__.py · skills/docx/scripts/office/helpers/pptx_chart.py · skills/docx/scripts/office/helpers/pptx_slide.py · skills/docx/scripts/office/helpers/pptx_theme.py · skills/docx/scripts/office/soffice.py · skills/docx/scripts/office/validate.py · skills/docx/scripts/office/validators/__init__.py · skills/docx/scripts/office/validators/base.py · skills/docx/scripts/office/validators/docx.py · skills/docx/scripts/office/validators/pptx.py · skills/docx/scripts/office/validators/redlining.py · skills/mcp-builder/scripts/connections.py · skills/mcp-builder/scripts/evaluation.py · skills/pdf/scripts/check_bounding_boxes.py · skills/pdf/scripts/check_fillable_fields.py · skills/pdf/scripts/convert_pdf_to_images.py · skills/pdf/scripts/create_validation_image.py · skills/pdf/scripts/extract_form_field_info.py · skills/pdf/scripts/extract_form_structure.py · skills/pdf/scripts/fill_fillable_fields.py · skills/pdf/scripts/fill_pdf_form_with_annotations.py · skills/pptx/scripts/__init__.py · skills/pptx/scripts/add_slide.py
BAŞLIKLAR: # Skills · # About This Repository · ## Disclaimer · # Skill Sets · # Try in Claude Code, Claude.ai, and the API · ## Claude Code · ## Claude.ai · ## Claude API · # Creating a Basic Skill · # My Skill Name · ## Examples · ## Guidelines · # Partner Skills

## moli-cdp-server
id: k00343 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00343_moli-cdp-server.txt (özgün: C:\Users\pc\.claude\skills\moli-cdp-server\SKILL.md) · 73 satır · araç adları (1): moli-cdp-server
BAŞLIKLAR: # Run Moli's CDP Server · ## Workflow · ## Playwright over CDP · ## Integration rules

## model_sec
id: k03462 · tür: cli · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03462_model_sec.txt (özgün: C:\Projeler\omer-skills\tools\model_sec.py) · 40 satır · araç adları (1): model_sec
BAŞLIKLAR: # sınıf → başlangıç effort'u; araçsız sınıflar yalın oturum 

## pln-hedef-planlayici
id: k01083 · tür: agent · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01083_pln-hedef-planlayici.txt (özgün: C:\Users\pc\.claude\agents\pln-hedef-planlayici.md) · 23 satır · araç adları (1): pln-hedef-planlayici
BAŞLIKLAR: Rules:

## pln-sokulebilir-entegrasyon
id: k01097 · tür: agent · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01097_pln-sokulebilir-entegrasyon.txt (özgün: C:\Users\pc\.claude\agents\pln-sokulebilir-entegrasyon.md) · 20 satır · araç adları (1): pln-sokulebilir-entegrasyon
BAŞLIKLAR: Kurallar:

## cancel
id: k01589 · tür: komut · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01589_cancel.txt (özgün: C:\Users\pc\.claude\plugins\cache\openai-codex\codex\1.0.6\commands\cancel.md) · 8 satır · araç adları (1): cancel
BAŞLIKLAR: 
