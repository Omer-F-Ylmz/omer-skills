# KURULUM-9a · web-sahne-desenleri denetimi · skill-ui · claude-design MCP

## 1 · web-sahne-desenleri (bb7dd15)
`skills/web-sahne-desenleri/SKILL.md` (121 satır) tek dosya; zip'lenip `skill_denetim.py` ile denetlendi → **0 hata**, 0 CRLF, 0 `~/.claude` uyarısı. `~/.claude/skills`'e kopyalanmadı; CC'ye claude.ai sync'iyle gelecek.

## 2 · skill-ui (KARAR: kurulacak)
- Klon: `gishamer/skill-ui` @ `3a91861f421f2ea0589aa3219e432e28071b21f0` (2026-07-10) → `C:\Projeler\.tmp-kurulum9\skill-ui`. KURULUM-8'deki "kurulamadı" satırı npm/release yokluğuydu; kaynaktan derleme ayrı bir yol.
- **Lisans: `package.json` `"license": "MIT"`, repoda LICENSE dosyası yok.** Metin olmadan MIT yalnız beyan.
- `skillspector scan bundled-skills/skill-ui-cli --no-llm` → 52/100 HIGH. Ömer kabul etti, gerekçeler: 3× HIGH `AE1` (SKILL.md:21,134,301) skill klasör yapısını **anlatan** metindeki backtick'li `SKILL.md` / `references/` / `scripts/` sözcüklerine takılıyor (`skill_denetim.py` YANLIS_ALARM sınıfı); 1× MEDIUM `AS3` (:120) aracın GitHub token çözümlemesi — PR akışının parçası ve skill token yazdırmayı açıkça yasaklıyor.
- **npm Git Bash altında çalışmıyor**: PATH'teki `.../Java/jdk-17/bin"` girdisindeki kaçak tırnak bash→cmd PATH dönüşümünü o noktada kesiyor; `npm ci` postinstall'da `'node' is not recognized` ile düşüyor. PowerShell'den çalıştırıldı.
- `npm ci` → 0. npm 11 allow-scripts kapısı `electron` + `esbuild` postinstall'ını beklettiği için `npm approve-scripts electron esbuild` + `npm rebuild` gerekti; bunlar olmadan derleme yapılamıyor.
- `npm run typecheck` → 0 (node + web).
- `test:*` 6/6 geçti: `repo-config` PASS · `additional-files` PASS · `create-metadata` PASS · `skill-filters` PASS · `cli-help` PASS · `skill-ui-cli-skill` PASS.
  `create-metadata` ilk turda `Repository is not configured` ile düştü. `skill-ui.config.example.json` kopyalamak yetmiyor (CLI onu okumuyor); `skill-ui config set repoOwner/repoName` → `C:\Users\pc\.skill-ui\config.json` yazınca geçti. **Üst akış kusuru: test betiği belgelenmemiş bir ön koşula bağlı.**
- **Üst akış kusuru 2:** `npm run dist:win` `⨯ Package "electron" is only allowed in "devDependencies"` ile düşüyor. Klonda `electron` `dependencies`'ten `devDependencies`'e taşındı (yerel yama, upstream'e gönderilmedi) → derleme 0 ile bitti.
- Kurulum dosyası: `C:\Projeler\.tmp-kurulum9\skill-ui\release\0.1.0\Skill UI-0.1.0-setup.exe` · **79,9 MB** (imzasız; `win-unpacked\Skill UI.exe` 180,0 MB). Çalıştırılmadı — Ömer kuracak.
- CLI: `npm i -g .` → 0; `skill-ui --help` → **exit 0** (Skill UI CLI 0.1.0).
- Zip: `dist/yukle-9/parti-1/skill-ui-cli.zip` (4426 B). `yukle8` boru hattından geçirildi — ham `description` 325 karakter, claude.ai sınırı 200; `frontmatter()` 195'e indirdi. `--target ~/.claude/skills` (SKILL.md:121) için YANLIS_ALARM'a "CLI hedef dizini örneği" eklendi. Denetim → **0 hata**; tüm `dist` (319 zip) → 0 hata, regresyon yok.

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
