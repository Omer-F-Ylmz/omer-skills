# ROUTER-1 tasarım (d3, 12 Eki)

İlke: model **düşürülmez**. Jeton tasarrufu sabit bağlam yükünden (CLAUDE.md, ~skill listesi, SessionStart hook enjeksiyonları,
MCP araç şemaları) gelir; kalite effort ile korunur/artırılır. Seçim `tools/model_sec.py` (bayrak `ROUTER_1=1`, varsayılan kapalı).

## Abonelik jetonu harcayan adımlar (claude -p) → sınıf
| Adım | Dosya | Bugün | Sınıf |
|---|---|---|---|
| Video tarama taşıyıcı | tools/video/video/hafif.py | zaten yalın (A1: --safe-mode, --tools "") | mekanik/ozet — dokunulmaz |
| Blender yalın spec | tools/blender/yalin.py | yalın + Write,Bash | ajan — dokunulmaz |
| Ölçüm koşucusu | tools/olcum/kosucu.py | profil/rota, MCP-HAFIF mcp_sec | ajan (gerçek oturum ölçer; yalınlaştırılmaz) |
| Deneme A/B (video kur) | tools/video/video/kur.py:661 | düz `claude -p --model sonnet` + kol ayarı | ölçüm — gerçek oturum, dokunulmaz |
| Jev / rubrik yargıcı | tools/olcum/jev_yargic.py | Jev (OpenRouter), claude -p değil | kapsam dışı |
| Yeni/elle `claude -p` adımları (köprü betikleri, tek seferlik sınıflandırma/özet/yargı) | .kos/kopru/*.py | çoğu düz | model_sec'in asıl hedefi |
| Alt ajanlar (okuyucu, suite-kosucu…) | .claude/agents | model alanı | ajan — tanımda model sabit |

## Kural (model_sec.bayraklar)
- mekanik → effort low · ozet → medium · yargi → high · ajan → medium
- Araçsız sınıf: `--safe-mode --tools "" --strict-mcp-config --disable-slash-commands --no-session-persistence`
- Ajan sınıfı: `--setting-sources "" --tools <liste> --allowedTools <liste>` + gerekirse mcp_sec'in `--mcp-config`'i (MCP-HAFIF)
- Geri düşüş (denetim başarısız): `kademe+1` → effort bir üst; xhigh'tan sonra **opus** (kalite yukarı, aşağı asla)

## Ölçüm
`tools/olcum/router1_olc.py`: 3 sınıf × A (düz `claude -p --model sonnet`) / B (model_sec) × 2 = 12 çağrı, çağrı başı ≤$0.6,
olcum_sira ile, RAM %95 kapısı, ham JSON dosyaya. KABUL: B doğruluk ≥ A ve B toplam jeton (girdi+cache) ≤ A'nın %50'si.
Sonuç: `olcum.tsv` (bu klasör).
