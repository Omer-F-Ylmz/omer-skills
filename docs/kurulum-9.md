# KURULUM-9a · web-sahne-desenleri denetimi · skill-ui · claude-design MCP

## 1 · web-sahne-desenleri (bb7dd15)
`skills/web-sahne-desenleri/SKILL.md` (121 satır) tek dosya; zip'lenip `skill_denetim.py` ile denetlendi → **0 hata**, 0 CRLF, 0 `~/.claude` uyarısı. `~/.claude/skills`'e kopyalanmadı; CC'ye claude.ai sync'iyle gelecek.

## 2 · skill-ui → DUR (kapı: skillspector HIGH)
- Klon: `gishamer/skill-ui` @ `3a91861f421f2ea0589aa3219e432e28071b21f0` (2026-07-10) → `C:\Projeler\.tmp-kurulum9\skill-ui`. KURULUM-8'deki "kurulamadı" satırı npm/release yokluğuydu; kaynaktan derleme ayrı bir yol.
- **Lisans: `package.json` `"license": "MIT"`, ama repoda LICENSE dosyası yok.** Metin olmadan MIT yalnız beyan; lisans kapısı için zayıf kanıt.
- `skillspector scan bundled-skills/skill-ui-cli --no-llm` → **52/100, HIGH, DO NOT INSTALL**. 3× HIGH `AE1 referenced artifact not inspected` (SKILL.md:21,134,301) + 1× MEDIUM `AS3 skill enumeration` (SKILL.md:120).
- Üç HIGH'ın üçü de metindeki backtick'li `SKILL.md` / `references/` / `scripts/` sözcüklerine takılıyor — skill, skill klasör yapısını **anlatan** bir doküman. `skill_denetim.py`'deki YANLIS_ALARM kalıbıyla aynı sınıf. Yine de tarif kapısı mutlak: npm ci / typecheck / test:* / dist:win / global CLI / zip **yapılmadı**.
- Devam kararı Ömer'in: ya YANLIS_ALARM benzeri bir muafiyet yazılır, ya kapı HIGH-AE1 için gevşetilir.

## 3 · claude-design MCP · 23 araç
| grup | araçlar | tek satır |
|---|---|---|
| proje | `list_projects` `create_project` `get_project` | projeyi listele / oluştur / meta-veri (ad, tür, paylaşım, URL) |
| dosya | `list_files` `read_file` `write_files` `copy_files` `delete_files` `create_support_js` | ağaç listele, oku (256 KiB, etag), yaz, sunucu-tarafı kopyala, sil, Design Components runtime'ı yaz |
| kapı/önizleme | `finalize_plan` `render_preview` | yazmadan önce yol kümesi + plan_token; dosyanın önizleme/editör bağlantısı |
| tasarım bağlamı | `list_design_systems` `read_design_skill` `get_claude_design_prompt` | tasarım sistemleri, hifi-design/frontend-design skill'i, sistem promptu |
| sohbet/yorum | `get_conversation` `put_conversation` `list_comments` `ack_comments` | proje sohbetini oku/yaz, pin'li yorumları listele, kuyruktan düşür |
| paylaşım | `update_sharing` `list_members` `add_member` `remove_member` `update_member_role` | bağlantı kapsamı ve üye yetkileri |

**claude.ai Design/artifact linkini okuyan araç: yok.** Her araç `project_id` (UUID) ile çalışır, URL kabul eden giriş yok. İçe aktarma yolu `copy_files` → `files[].src_project_id` (kaynak projede görüntüleme yetkisi şart, sunucu tarafı, 256 KiB sınırı dışında). Okuma yolu `get_project` → `list_files` → `read_file(project_id, path)`. `claude.ai/artifact/...` bağlantıları bu sunucunun kapsamı dışında (Artifact aracına ait). URL'deki UUID elle `project_id` olarak verilebilir.

Ölçüm sırasında yalnız `list_projects` çağrıldı (salt-okur, ücretsiz) → `[]`.
