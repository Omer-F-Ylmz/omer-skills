# REA SkillSpector 16 MEDIUM — sınıflandırma (TERS-1 d2)

Kaynak: `%TEMP%\rea-tarama\ss-skill.json` (`--no-llm`, yalnız `.agents/skills/reverse-engineer-anything`, 0 HIGH madde; toplam skor 53 → DO_NOT_INSTALL, tek tek okundu). Satırlar dosyadan doğrulandı.

| # | Kategori | Yer | Sınıf | Gerekçe |
|---|---|---|---|---|
| 1-5 | MCP Rug Pull (RP1 ×5) | SKILL.md 36, 50, 55, 70, 78 | **Gerçek, düşük** | Skill komutları `npx -y rea-agents@latest`; yukarı akış değişirse kod değişir. Önlem: biz MCP'yi `rea-agents@6.7.0` sabitledik, kurulu `rea` CLI'sı var; `@latest` komutları **çalıştırılmaz**. |
| 6 | Memory Poisoning (MP2) | connection-and-recovery.md 14 | Yanlış pozitif | Satır `## Choose remedy…` başlığı + tablo; dolgu içerik yok. |
| 7-12 | Prompt Injection / boşluk dolgusu (P9 ×6) | connection-and-recovery.md 14, 16-19, 21 | Yanlış pozitif | Markdown tablo ayırıcısı (`| --- | --- |`) uzun tire/boşluk dizisi; gizli talimat yok. |
| 13-15 | Rogue Agent / kalıcılık (RA2 ×3) | native-and-artifacts.md 311-313 | Yanlış pozitif | `project_apple_application_graph` aracının *çözümlediği* launchd plist/symlink'i anlatıyor; skill kalıcılık kurmuyor. |
| 16 | Excessive Agency (EA2) | native-and-artifacts.md 330 | **Gerçek, sınırlı** | "Native DMG traversal … salt-okunur mount, ayrıca izin gerekmez": araç DMG bağlar. Önlem: DMG/Apple hedefi kullanılmaz (Windows, hedef setinde yok). |

Sonuç: 2 gerçek (6 satır), 10 yanlış pozitif madde (10 satır); 0 kritik. Kullanım sınırı (tersine SKILL.md'ye işlendi): yalnız kurulu `rea` CLI / sabitli MCP; `npx …@latest` yok; DMG mount aracı yok; ağ/yazma araçları kullanılmaz, yalnız salt-okuma analiz (`analyze-javascript-application` gibi). Not: madde sayısı 5+1+6+3+1 = 16 ama sınıf satırı 6 + 10 = 16.
