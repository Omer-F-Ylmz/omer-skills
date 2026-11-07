# claude.ai yukleme listesi 7 Kas (yeni76, 49 SKILL satiri)

Uretici: tools/skill-paket/paketle.py --buyuk (yeni aile). Cikti: dist/yukle-1107/ (gitignore). Mevcut hicbir paket degismedi; 48 skill yeni 5 pakete girdi, 1 atlandi.
Hicbir yeni skill mevcut 179 paket zip'inde yoktu (taranan: dist/**/*paket*.zip), bu yuzden Replace yok, 5 YENI kayit (claude.ai'de +5).
Zip kurali: tek SKILL.md zip kokunde (<paket>/SKILL.md); alt skill'ler skills/<ad>/TALIMAT.md (paket sistemi, docs/kurulumlar/skill-paket-sistemi.md).

## Grup 1 (5 zip, 20'den az)
1. text-to-cad-paket.zip (35 kayit): bambu-labs, cad, dfam-check, dfm, dxf, engineering-drawing, gcode, sdf, sendcutsend, srdf, step-parts, urdf
2. kilocode-paket.zip (19 kayit): chart, gh-issues, icon-jetbrains, icon-vscode, jetbrains-arch, jetbrains-cli-pin, jetbrains-dev, jetbrains-sandbox, jetbrains-session, jetbrains-ui, kilocode-merge-minimizer, pr-track-v1, vscode-visual-regression, effect, rtl-aware-development
3. vue-ek-paket.zip (14 kayit): create-adaptable-composable, vue-debug-guides, vue-jsx-best-practices, vue-options-api-best-practices, vue-pinia-best-practices, vue-router-best-practices, vue-testing-best-practices
4. ugc-ek-paket.zip (11 kayit): ugc-ad-strategist, ugc-device-screen, ugc-minimax-mode, ugc-video-producer, ugc-vision-referee
5. karisik-1107-paket.zip (18 kayit, 1.4 MB): template (frontmatter name template-skill), addressing-pr-feedback, creating-pr, reviewing-pr-feedback, writing-result-code, zero-slop, taste-skill (frontmatter name design-taste-frontend), turkce-yazi, typer

## Atlanan
- omer-skills (Remove AI Slop satiri): ~/.claude/skills/omer-skills 963 dosya / 24 MB, deponun kendisi (meta skill), paketlenecek tek skill degil; aile paketine sigmaz (200 dosya, 9.5 MB sinir). Gerekirse ayri karar.

## Dogrulama (python -I, zipfile)
- 5 zip: kayit <= 35 (<=1000), testzip temiz, zip koku tek klasor, SKILL.md name == zip adi.
- 48/48 yeni skill skills/<ad>/TALIMAT.md olarak mevcut.
- zip_denetle.py: 4 zip TEMIZ; karisik-1107-paket 1 uyari = turkce-yazi/scripts/yapi.py icinde bos-karakter dedektoru sabitleri (ZWSP/ZWNJ/ZWJ/BOM harfi harfine kaynakta), zararsiz, icerik degistirilmedi.
